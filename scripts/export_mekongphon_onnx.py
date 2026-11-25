#!/usr/bin/env python3
"""Export the pinned MekongPhon Khmer→IPA model to browser-runnable ONNX.

Only the model weights/config/tokenizers are downloaded from the Apache-2.0
model repository. The upstream training/evaluation corpus is not downloaded.
The exporter creates separate encoder and decoder graphs, dynamic-int8
variants, and a reproducible manifest. It also checks ONNX Runtime parity
against the original Transformers implementation on fixed probes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path
from typing import Any

MODEL_ID = "byumatrixlab/khmer-ipa"
MODEL_REVISION = "20e069d384b240da76320e1569958568c12a54bc"
MODEL_LICENSE = "Apache-2.0"
DEFAULT_PROBES = ("សួស្តី", "ខ្ញុំជាសិស្ស", "សភាតំណាងប្រជាជនកម្ពុជា")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--opset", type=int, default=17)
    parser.add_argument("--probe", action="append", default=[])
    args = parser.parse_args()
    if args.max_length < 8 or args.max_length > 512:
        parser.error("--max-length must be between 8 and 512")

    import numpy as np
    import onnx
    import onnxruntime as ort
    import torch
    from huggingface_hub import snapshot_download
    from onnxruntime.quantization import QuantType, quantize_dynamic
    from transformers import AutoTokenizer, EncoderDecoderModel

    torch.set_num_threads(1)
    torch.manual_seed(0)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source_dir = Path(snapshot_download(
        repo_id=MODEL_ID,
        revision=MODEL_REVISION,
        allow_patterns=[
            "README.md", "config.json", "generation_config.json", "model.safetensors",
            "encoder_tokenizer/*", "decoder_tokenizer/*",
        ],
    ))
    model = EncoderDecoderModel.from_pretrained(
        source_dir, local_files_only=True, attn_implementation="eager"
    ).to("cpu").eval()
    encoder_tokenizer = AutoTokenizer.from_pretrained(
        source_dir / "encoder_tokenizer", local_files_only=True
    )
    decoder_tokenizer = AutoTokenizer.from_pretrained(
        source_dir / "decoder_tokenizer", local_files_only=True
    )

    class EncoderGraph(torch.nn.Module):
        def __init__(self, encoder):
            super().__init__()
            self.encoder = encoder

        def forward(self, input_ids, attention_mask):
            return self.encoder(
                input_ids=input_ids,
                attention_mask=attention_mask,
                return_dict=False,
            )[0]

    class DecoderGraph(torch.nn.Module):
        def __init__(self, decoder):
            super().__init__()
            self.decoder = decoder

        def forward(self, decoder_input_ids, encoder_hidden_states, encoder_attention_mask):
            decoder_attention_mask = torch.ones_like(decoder_input_ids)
            return self.decoder(
                input_ids=decoder_input_ids,
                attention_mask=decoder_attention_mask,
                encoder_hidden_states=encoder_hidden_states,
                encoder_attention_mask=encoder_attention_mask,
                use_cache=False,
                return_dict=False,
            )[0]

    probes = args.probe or list(DEFAULT_PROBES)
    encoded = encoder_tokenizer(
        probes[:2], return_tensors="pt", padding=True,
        truncation=True, max_length=args.max_length,
    )
    input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]
    with torch.no_grad():
        encoder_hidden = model.encoder(
            input_ids=input_ids, attention_mask=attention_mask, return_dict=False
        )[0]
    decoder_input_ids = torch.tensor(
        [[model.config.decoder_start_token_id, 4, 5],
         [model.config.decoder_start_token_id, 6, 7]],
        dtype=torch.long,
    )

    encoder_fp32 = output_dir / "encoder.onnx"
    decoder_fp32 = output_dir / "decoder.onnx"
    started = time.perf_counter()
    torch.onnx.export(
        EncoderGraph(model.encoder),
        (input_ids, attention_mask),
        str(encoder_fp32),
        input_names=["input_ids", "attention_mask"],
        output_names=["encoder_hidden_states"],
        dynamic_axes={
            "input_ids": {0: "batch", 1: "source_sequence"},
            "attention_mask": {0: "batch", 1: "source_sequence"},
            "encoder_hidden_states": {0: "batch", 1: "source_sequence"},
        },
        opset_version=args.opset,
        do_constant_folding=True,
        dynamo=False,
    )
    torch.onnx.export(
        DecoderGraph(model.decoder),
        (decoder_input_ids, encoder_hidden, attention_mask),
        str(decoder_fp32),
        input_names=["decoder_input_ids", "encoder_hidden_states", "encoder_attention_mask"],
        output_names=["logits"],
        dynamic_axes={
            "decoder_input_ids": {0: "batch", 1: "target_sequence"},
            "encoder_hidden_states": {0: "batch", 1: "source_sequence"},
            "encoder_attention_mask": {0: "batch", 1: "source_sequence"},
            "logits": {0: "batch", 1: "target_sequence"},
        },
        opset_version=args.opset,
        do_constant_folding=True,
        dynamo=False,
    )
    for path in (encoder_fp32, decoder_fp32):
        onnx.checker.check_model(str(path), full_check=True)

    encoder_int8 = output_dir / "encoder.int8.onnx"
    decoder_int8 = output_dir / "decoder.int8.onnx"
    quantize_dynamic(
        str(encoder_fp32), str(encoder_int8),
        weight_type=QuantType.QInt8, per_channel=True,
    )
    quantize_dynamic(
        str(decoder_fp32), str(decoder_int8),
        weight_type=QuantType.QInt8, per_channel=True,
    )
    for path in (encoder_int8, decoder_int8):
        onnx.checker.check_model(str(path), full_check=True)

    options = ort.SessionOptions()
    options.intra_op_num_threads = 1
    options.inter_op_num_threads = 1
    encoder_session = ort.InferenceSession(str(encoder_fp32), sess_options=options, providers=["CPUExecutionProvider"])
    decoder_session = ort.InferenceSession(str(decoder_fp32), sess_options=options, providers=["CPUExecutionProvider"])
    encoder_q_session = ort.InferenceSession(str(encoder_int8), sess_options=options, providers=["CPUExecutionProvider"])
    decoder_q_session = ort.InferenceSession(str(decoder_int8), sess_options=options, providers=["CPUExecutionProvider"])

    with torch.inference_mode():
        torch_encoder = model.encoder(
            input_ids=input_ids, attention_mask=attention_mask, return_dict=False
        )[0].cpu().numpy()
        torch_logits = model.decoder(
            input_ids=decoder_input_ids,
            attention_mask=torch.ones_like(decoder_input_ids),
            encoder_hidden_states=torch.from_numpy(torch_encoder),
            encoder_attention_mask=attention_mask,
            use_cache=False,
            return_dict=False,
        )[0].cpu().numpy()

    fp_encoder = encoder_session.run(
        ["encoder_hidden_states"],
        {"input_ids": input_ids.numpy(), "attention_mask": attention_mask.numpy()},
    )[0]
    fp_logits = decoder_session.run(
        ["logits"],
        {
            "decoder_input_ids": decoder_input_ids.numpy(),
            "encoder_hidden_states": fp_encoder,
            "encoder_attention_mask": attention_mask.numpy(),
        },
    )[0]
    q_encoder = encoder_q_session.run(
        ["encoder_hidden_states"],
        {"input_ids": input_ids.numpy(), "attention_mask": attention_mask.numpy()},
    )[0]
    q_logits = decoder_q_session.run(
        ["logits"],
        {
            "decoder_input_ids": decoder_input_ids.numpy(),
            "encoder_hidden_states": q_encoder,
            "encoder_attention_mask": attention_mask.numpy(),
        },
    )[0]

    fp_encoder_max_abs = float(np.max(np.abs(torch_encoder - fp_encoder)))
    fp_logits_max_abs = float(np.max(np.abs(torch_logits - fp_logits)))
    q_logits_max_abs = float(np.max(np.abs(fp_logits - q_logits)))
    fp_top1_agreement = float(np.mean(np.argmax(torch_logits, axis=-1) == np.argmax(fp_logits, axis=-1)))
    q_top1_agreement = float(np.mean(np.argmax(fp_logits, axis=-1) == np.argmax(q_logits, axis=-1)))
    if fp_encoder_max_abs > 2e-3 or fp_logits_max_abs > 2e-3 or fp_top1_agreement < 0.999:
        raise RuntimeError(
            f"FP32 ONNX parity failed: encoder_abs={fp_encoder_max_abs}, "
            f"logits_abs={fp_logits_max_abs}, top1={fp_top1_agreement}"
        )
    if q_top1_agreement < 0.95:
        raise RuntimeError(f"INT8 top-1 parity too low: {q_top1_agreement}")

    def greedy_onnx(text: str, quantized: bool) -> str:
        enc = encoder_tokenizer(
            text, return_tensors="np", truncation=True, max_length=args.max_length
        )
        enc_session = encoder_q_session if quantized else encoder_session
        dec_session = decoder_q_session if quantized else decoder_session
        hidden = enc_session.run(
            ["encoder_hidden_states"],
            {"input_ids": enc["input_ids"], "attention_mask": enc["attention_mask"]},
        )[0]
        ids = [int(model.config.decoder_start_token_id)]
        for _ in range(args.max_length - 1):
            logits = dec_session.run(
                ["logits"],
                {
                    "decoder_input_ids": np.asarray([ids], dtype=np.int64),
                    "encoder_hidden_states": hidden,
                    "encoder_attention_mask": enc["attention_mask"],
                },
            )[0]
            next_id = int(np.argmax(logits[0, -1]))
            ids.append(next_id)
            if next_id == int(model.config.eos_token_id):
                break
        return decoder_tokenizer.decode(ids, skip_special_tokens=True)

    generation_results = []
    for probe in probes:
        tokenized = encoder_tokenizer(
            probe, return_tensors="pt", truncation=True, max_length=args.max_length
        )
        with torch.inference_mode():
            reference_ids = model.generate(
                **tokenized, max_length=args.max_length, num_beams=1, early_stopping=True
            )[0]
        reference = decoder_tokenizer.decode(reference_ids, skip_special_tokens=True)
        fp32_output = greedy_onnx(probe, quantized=False)
        int8_output = greedy_onnx(probe, quantized=True)
        if reference != fp32_output:
            raise RuntimeError(
                f"FP32 greedy generation mismatch for probe {probe!r}: "
                f"Transformers={reference!r}, ONNX={fp32_output!r}"
            )
        generation_results.append({
            "input": probe,
            "transformers_greedy": reference,
            "onnx_fp32_greedy": fp32_output,
            "onnx_int8_greedy": int8_output,
            "int8_matches_fp32": int8_output == fp32_output,
        })

    shutil.copy2(source_dir / "README.md", output_dir / "UPSTREAM_MODEL_CARD.md")
    files = {}
    for path in sorted(output_dir.glob("*.onnx")):
        files[path.name] = {"bytes": path.stat().st_size, "sha256": sha256_file(path)}
    manifest = {
        "schema_version": "1.0",
        "model_id": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "model_license": MODEL_LICENSE,
        "model_license_evidence": "upstream model-card metadata license: apache-2.0 at the pinned revision",
        "training_corpus_included": False,
        "architecture": "BERT encoder-decoder; separate encoder and decoder ONNX graphs; no KV cache",
        "generation": {
            "decoder_start_token_id": int(model.config.decoder_start_token_id),
            "eos_token_id": int(model.config.eos_token_id),
            "max_length": args.max_length,
            "beam_count_in_browser_spike": 1,
        },
        "quantization": "ONNX Runtime dynamic per-channel QInt8 weights",
        "opset": args.opset,
        "runtime_versions": {
            "torch": torch.__version__,
            "transformers": __import__("transformers").__version__,
            "onnx": onnx.__version__,
            "onnxruntime": ort.__version__,
        },
        "export_elapsed_seconds": round(time.perf_counter() - started, 3),
        "parity": {
            "fp32_encoder_max_abs_error": fp_encoder_max_abs,
            "fp32_decoder_logits_max_abs_error": fp_logits_max_abs,
            "fp32_decoder_top1_agreement": fp_top1_agreement,
            "int8_decoder_top1_agreement_vs_fp32": q_top1_agreement,
            "generation_probes": generation_results,
        },
        "files": files,
    }
    write_json(output_dir / "manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
