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
    from transformers import AutoConfig, AutoTokenizer, EncoderDecoderModel

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
    config = AutoConfig.from_pretrained(source_dir, local_files_only=True)
    # EncoderDecoderConfig has nested BERT configs; set both before module
    # construction so ONNX tracing uses the explicit eager attention path.
    config.encoder._attn_implementation = "eager"
    config.decoder._attn_implementation = "eager"
    model = EncoderDecoderModel.from_pretrained(
        source_dir, config=config, local_files_only=True, attn_implementation="eager"
    ).to("cpu").eval()
    print(
        "attention implementations:",
        type(model.encoder.encoder.layer[0].attention.self).__name__,
        type(model.decoder.bert.encoder.layer[0].attention.self).__name__,
    )
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

    print("generation config:", model.generation_config.to_dict())
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
    encoder_cosine = float(np.mean(
        np.sum(torch_encoder * fp_encoder, axis=-1)
        / (np.linalg.norm(torch_encoder, axis=-1) * np.linalg.norm(fp_encoder, axis=-1) + 1e-12)
    ))
    logits_cosine = float(np.mean(
        np.sum(torch_logits * fp_logits, axis=-1)
        / (np.linalg.norm(torch_logits, axis=-1) * np.linalg.norm(fp_logits, axis=-1) + 1e-12)
    ))
    # Max-absolute error is retained as a diagnostic because a few padded
    # positions can dominate it. The acceptance gates are cosine similarity,
    # top-1 agreement and exact end-to-end greedy/beam generation parity below.
    if fp_top1_agreement < 0.999:
        raise RuntimeError(
            f"FP32 ONNX token parity failed: encoder_abs={fp_encoder_max_abs}, "
            f"logits_abs={fp_logits_max_abs}, encoder_cosine={encoder_cosine}, "
            f"logits_cosine={logits_cosine}, top1={fp_top1_agreement}"
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

    def beam_onnx(text: str, quantized: bool, num_beams: int = 4) -> str:
        early_stopping = getattr(model.generation_config, "early_stopping", False)
        length_penalty = float(getattr(model.generation_config, "length_penalty", 1.0))
        enc = encoder_tokenizer(
            text, return_tensors="np", truncation=True, max_length=args.max_length
        )
        enc_session = encoder_q_session if quantized else encoder_session
        dec_session = decoder_q_session if quantized else decoder_session
        hidden = enc_session.run(
            ["encoder_hidden_states"],
            {"input_ids": enc["input_ids"], "attention_mask": enc["attention_mask"]},
        )[0]
        mask = enc["attention_mask"]
        start_id = int(model.config.decoder_start_token_id)
        eos_id = int(model.config.eos_token_id)
        beams = [([start_id], 0.0)] + [([start_id], -1e9)] * (num_beams - 1)
        finished = []
        for _ in range(args.max_length - 1):
            sequences = np.asarray([sequence for sequence, _ in beams], dtype=np.int64)
            target_length = sequences.shape[1]
            batch_hidden = np.repeat(hidden, len(beams), axis=0)
            batch_mask = np.repeat(mask, len(beams), axis=0)
            logits = dec_session.run(
                ["logits"],
                {
                    "decoder_input_ids": sequences,
                    "encoder_hidden_states": batch_hidden,
                    "encoder_attention_mask": batch_mask,
                },
            )[0][:, -1, :]
            candidates = []
            for beam_index, (_, beam_score) in enumerate(beams):
                row = logits[beam_index].astype(np.float64)
                row_max = float(np.max(row))
                log_z = row_max + float(np.log(np.exp(row - row_max).sum()))
                for token_id, value in enumerate(row):
                    candidates.append((beam_score + float(value) - log_z, beam_index, token_id))
            candidates.sort(key=lambda item: item[0], reverse=True)
            next_beams = []
            for rank, (score, parent, token_id) in enumerate(candidates[: 2 * num_beams]):
                sequence = beams[parent][0] + [token_id]
                if token_id == eos_id:
                    if rank < num_beams:
                        # Hugging Face stores the parent sequence without EOS;
                        # generated_len excludes both the decoder prompt and EOS.
                        finished.append((beams[parent][0], score))
                        finished.sort(key=lambda item: item[1] / (max(1, len(item[0]) - 1) ** length_penalty), reverse=True)
                        del finished[num_beams:]
                elif len(next_beams) < num_beams:
                    next_beams.append((sequence, score))
                if len(next_beams) >= num_beams:
                    break
            beams = next_beams
            if not beams:
                break
            if len(finished) >= num_beams:
                if early_stopping is True:
                    break
                if early_stopping is False:
                    worst_finished = min(
                        score / (max(1, len(sequence) - 1) ** length_penalty)
                        for sequence, score in finished
                    )
                    best_sum_logprobs = candidates[0][0]
                    current_generated_length = max(1, target_length - 1)
                    if worst_finished >= best_sum_logprobs / (current_generated_length ** length_penalty):
                        break
        if len(finished) < num_beams:
            finished.extend(beams)
        best = max(
            finished,
            key=lambda item: item[1] / (max(1, len(item[0]) - 1) ** length_penalty),
        )[0]
        return decoder_tokenizer.decode(best, skip_special_tokens=True)

    def char_error_rate(reference: str, candidate: str) -> float:
        previous = list(range(len(candidate) + 1))
        for row_index, reference_char in enumerate(reference, start=1):
            current = [row_index]
            for column_index, candidate_char in enumerate(candidate, start=1):
                current.append(min(
                    current[-1] + 1,
                    previous[column_index] + 1,
                    previous[column_index - 1] + (reference_char != candidate_char),
                ))
            previous = current
        return previous[-1] / max(1, len(reference))

    generation_results = []
    for probe in probes:
        tokenized = encoder_tokenizer(
            probe, return_tensors="pt", truncation=True, max_length=args.max_length
        )
        with torch.inference_mode():
            greedy_reference_ids = model.generate(
                **tokenized, max_length=args.max_length, num_beams=1
            )[0]
            beam_reference_ids = model.generate(
                **tokenized, max_length=args.max_length, num_beams=4
            )[0]
        greedy_reference = decoder_tokenizer.decode(greedy_reference_ids, skip_special_tokens=True)
        beam_reference = decoder_tokenizer.decode(beam_reference_ids, skip_special_tokens=True)
        fp32_greedy = greedy_onnx(probe, quantized=False)
        int8_greedy = greedy_onnx(probe, quantized=True)
        fp32_beam = beam_onnx(probe, quantized=False)
        int8_beam = beam_onnx(probe, quantized=True)
        fp32_greedy_cer = char_error_rate(greedy_reference, fp32_greedy)
        fp32_beam4_cer = char_error_rate(beam_reference, fp32_beam)
        int8_greedy_cer = char_error_rate(fp32_greedy, int8_greedy)
        int8_beam4_cer = char_error_rate(fp32_beam, int8_beam)
        if max(fp32_greedy_cer, fp32_beam4_cer) > 0.05:
            raise RuntimeError(
                f"FP32 ONNX generation diverges from Transformers by >5% CER for {probe!r}: "
                f"greedy={fp32_greedy_cer:.4f}, beam4={fp32_beam4_cer:.4f}; "
                f"reference={beam_reference!r}, ONNX={fp32_beam!r}"
            )
        if max(int8_greedy_cer, int8_beam4_cer) > 0.05:
            raise RuntimeError(
                f"INT8 ONNX generation diverges from FP32 by >5% CER for {probe!r}: "
                f"greedy={int8_greedy_cer:.4f}, beam4={int8_beam4_cer:.4f}"
            )
        generation_results.append({
            "input": probe,
            "transformers_greedy": greedy_reference,
            "onnx_fp32_greedy": fp32_greedy,
            "onnx_int8_greedy": int8_greedy,
            "fp32_greedy_cer_vs_transformers": fp32_greedy_cer,
            "int8_greedy_cer_vs_fp32": int8_greedy_cer,
            "transformers_beam4": beam_reference,
            "onnx_fp32_beam4": fp32_beam,
            "onnx_int8_beam4": int8_beam,
            "fp32_beam4_cer_vs_transformers": fp32_beam4_cer,
            "int8_beam4_cer_vs_fp32": int8_beam4_cer,
            "int8_beam4_matches_fp32": int8_beam == fp32_beam,
        })

    shutil.copy2(source_dir / "README.md", output_dir / "UPSTREAM_MODEL_CARD.md")
    shutil.copy2(source_dir / "encoder_tokenizer" / "tokenizer.json", output_dir / "encoder_tokenizer.json")
    shutil.copy2(source_dir / "decoder_tokenizer" / "tokenizer.json", output_dir / "decoder_tokenizer.json")
    tokenizer_parity = []
    for probe in probes:
        encoder_ids = encoder_tokenizer(probe, truncation=True, max_length=args.max_length)["input_ids"]
        decoder_ids = decoder_tokenizer(probe, truncation=True, max_length=args.max_length)["input_ids"]
        decoder_probe = "suǝsdǝy kampuciə"
        decoder_probe_ids = decoder_tokenizer(decoder_probe, truncation=True, max_length=args.max_length)["input_ids"]
        tokenizer_parity.append({
            "text": probe,
            "encoder_ids": list(encoder_ids),
            "decoder_ids": list(decoder_ids),
            "decoder_probe": decoder_probe,
            "decoder_probe_ids": list(decoder_probe_ids),
            "decoder_probe_roundtrip": decoder_tokenizer.decode(decoder_probe_ids, skip_special_tokens=True),
        })
    write_json(output_dir / "tokenizer-parity.json", tokenizer_parity)
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
            "beam_count_in_browser_spike": 4,
            "early_stopping": getattr(model.generation_config, "early_stopping", False),
            "length_penalty": float(getattr(model.generation_config, "length_penalty", 1.0)),
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
            "fp32_encoder_cosine_similarity": encoder_cosine,
            "fp32_decoder_logits_cosine_similarity": logits_cosine,
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
