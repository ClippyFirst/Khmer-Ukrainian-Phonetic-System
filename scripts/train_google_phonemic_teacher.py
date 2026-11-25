#!/usr/bin/env python3
"""Train an offline neural teacher on pinned Google Khmer source phonemic labels.

This model is a research/build-time teacher only. It does not emit project IPA
and is not imported by the browser or deterministic runtime.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from khmer_ua.google_phonemic import load_google_phonemic_lexicon
from khmer_ua.google_teacher_data import SPECIAL_TOKENS, split_for_word, tokenize_source, tokenize_target
from google_teacher.model import KhmerPhonemicSeq2Seq

PAD, BOS, EOS, UNK = SPECIAL_TOKENS
DEFAULT_OUTPUT = ROOT / "dist" / "google-khmer-teacher"


@dataclass(frozen=True)
class Example:
    word: str
    source: tuple[str, ...]
    target: tuple[str, ...]
    source_row: int


def load_examples(max_words: int | None = None) -> tuple[list[Example], dict]:
    lexicon = load_google_phonemic_lexicon()
    examples: list[Example] = []
    for word, variants in lexicon.entries.items():
        for row in variants:
            examples.append(Example(
                word=word,
                source=tokenize_source(word),
                target=tokenize_target(row.source_phonemic),
                source_row=row.source_row,
            ))
    examples.sort(key=lambda item: (item.word, item.source_row))
    if max_words is not None:
        allowed = set(sorted({item.word for item in examples})[:max_words])
        examples = [item for item in examples if item.word in allowed]
    manifest = {
        **lexicon.manifest,
        "source_vocab_scope": "input-only character inventory from the pinned corpus",
        "target_vocab_scope": "54 observed source phones plus explicit syllable boundary and special tokens",
        "split_policy": "SHA-256 spelling-grouped deterministic 90/5/5",
        "teacher_label_semantics": "Google source phonemic transcription; not IPA gold",
    }
    return examples, manifest


def vocabularies(examples: list[Example]) -> tuple[dict[str, int], dict[str, int]]:
    source_tokens = sorted({token for row in examples for token in row.source})
    target_tokens = sorted({token for row in examples for token in row.target})
    source_vocab = {token: index for index, token in enumerate((*SPECIAL_TOKENS, *source_tokens))}
    target_vocab = {token: index for index, token in enumerate((*SPECIAL_TOKENS, *target_tokens))}
    return source_vocab, target_vocab


def collate(rows: list[Example], source_vocab: dict[str, int], target_vocab: dict[str, int]):
    source_sequences = [
        torch.tensor(
            [source_vocab[BOS], *[source_vocab.get(token, source_vocab[UNK]) for token in row.source], source_vocab[EOS]],
            dtype=torch.long,
        )
        for row in rows
    ]
    target_sequences = [
        torch.tensor(
            [target_vocab[BOS], *[target_vocab.get(token, target_vocab[UNK]) for token in row.target], target_vocab[EOS]],
            dtype=torch.long,
        )
        for row in rows
    ]
    source_lengths = torch.tensor([len(item) for item in source_sequences], dtype=torch.long)
    return (
        pad_sequence(source_sequences, batch_first=True, padding_value=source_vocab[PAD]),
        source_lengths,
        pad_sequence(target_sequences, batch_first=True, padding_value=target_vocab[PAD]),
    )


def edit_distance(left: list[str], right: list[str]) -> int:
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (a != b),
            ))
        previous = current
    return previous[-1]


def batches(rows: list[Example], batch_size: int, seed: int, shuffle: bool):
    ordered = list(rows)
    if shuffle:
        random.Random(seed).shuffle(ordered)
    for start in range(0, len(ordered), batch_size):
        yield ordered[start:start + batch_size]


@torch.no_grad()
def evaluate(model, rows, source_vocab, target_vocab, batch_size, device, *, greedy: bool):
    model.eval()
    loss_fn = nn.CrossEntropyLoss(ignore_index=target_vocab[PAD])
    total_loss = 0.0
    total_tokens = 0
    total_distance = 0
    total_reference = 0
    exact = 0
    boundary_count_match = 0
    covered = 0
    seen = 0
    id_to_target = {value: key for key, value in target_vocab.items()}
    for batch in batches(rows, batch_size, 0, False):
        source, source_lengths, target = collate(batch, source_vocab, target_vocab)
        source, source_lengths, target = source.to(device), source_lengths.to(device), target.to(device)
        logits = model(source, source_lengths, target[:, :-1])
        gold = target[:, 1:]
        loss = loss_fn(logits.reshape(-1, logits.shape[-1]), gold.reshape(-1))
        valid = int((gold != target_vocab[PAD]).sum().item())
        total_loss += float(loss.item()) * valid
        total_tokens += valid
        if greedy:
            predictions = model.greedy_decode(
                source, source_lengths, bos_id=target_vocab[BOS],
                eos_id=target_vocab[EOS], max_length=64,
            )
            for predicted_ids, target_ids in zip(predictions, target.tolist()):
                reference_ids = []
                for token_id in target_ids[1:]:
                    if token_id == target_vocab[PAD] or token_id == target_vocab[EOS]:
                        break
                    reference_ids.append(token_id)
                predicted = [id_to_target.get(token_id, UNK) for token_id in predicted_ids]
                reference = [id_to_target.get(token_id, UNK) for token_id in reference_ids]
                distance = edit_distance(predicted, reference)
                total_distance += distance
                total_reference += len(reference)
                exact += int(predicted == reference)
                boundary_count_match += int(predicted.count(".") == reference.count("."))
                covered += int(bool(predicted) and UNK not in predicted)
                seen += 1
    result = {"loss": total_loss / max(total_tokens, 1), "token_count": total_tokens}
    if greedy:
        result.update({
            "phoneme_token_error_rate": total_distance / max(total_reference, 1),
            "word_exact_match": exact / max(seen, 1),
            "syllable_boundary_count_accuracy": boundary_count_match / max(seen, 1),
            "output_coverage": covered / max(seen, 1),
            "evaluated_words": seen,
            "metric_semantics": "source-label prediction only; not independent IPA accuracy",
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--epochs", type=int, default=6)
    parser.add_argument("--batch-size", type=int, default=192)
    parser.add_argument("--embedding-size", type=int, default=64)
    parser.add_argument("--hidden-size", type=int, default=96)
    parser.add_argument("--seed", type=int, default=20261125)
    parser.add_argument("--max-words", type=int, default=None, help="small smoke-test subset")
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        raise SystemExit("epochs and batch-size must be positive")

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(min(4, torch.get_num_threads()))
    device = torch.device("cpu")

    examples, source_manifest = load_examples(args.max_words)
    split_by_word = {word: split_for_word(word, args.seed) for word in {row.word for row in examples}}
    train_rows = [row for row in examples if split_by_word[row.word] == "train"]
    dev_rows = [row for row in examples if split_by_word[row.word] == "dev"]
    test_rows = [row for row in examples if split_by_word[row.word] == "test"]
    if not train_rows or not dev_rows or not test_rows:
        raise SystemExit("word-disjoint train/dev/test split is empty")
    source_vocab, target_vocab = vocabularies(examples)
    model = KhmerPhonemicSeq2Seq(
        len(source_vocab), len(target_vocab),
        embedding_size=args.embedding_size, hidden_size=args.hidden_size,
        padding_index=source_vocab[PAD],
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.0001)
    loss_fn = nn.CrossEntropyLoss(ignore_index=target_vocab[PAD])
    best_dev = math.inf
    best_state = None
    stale_epochs = 0
    history = []

    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        total_tokens = 0
        for batch in batches(train_rows, args.batch_size, args.seed + epoch, True):
            source, source_lengths, target = collate(batch, source_vocab, target_vocab)
            source, source_lengths, target = source.to(device), source_lengths.to(device), target.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(source, source_lengths, target[:, :-1])
            gold = target[:, 1:]
            loss = loss_fn(logits.reshape(-1, logits.shape[-1]), gold.reshape(-1))
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            valid = int((gold != target_vocab[PAD]).sum().item())
            total_loss += float(loss.item()) * valid
            total_tokens += valid
        train_loss = total_loss / max(total_tokens, 1)
        dev = evaluate(model, dev_rows, source_vocab, target_vocab, args.batch_size, device, greedy=False)
        history.append({"epoch": epoch, "train_loss": train_loss, "dev_loss": dev["loss"]})
        if dev["loss"] < best_dev:
            best_dev = dev["loss"]
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            stale_epochs = 0
        else:
            stale_epochs += 1
        if stale_epochs >= 2:
            break

    if best_state is None:
        raise SystemExit("training did not produce a model checkpoint")
    model.load_state_dict(best_state)
    test_metrics = evaluate(
        model, test_rows, source_vocab, target_vocab, args.batch_size, device, greedy=True
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "architecture": "bidirectional-GRU-encoder/GRU-decoder-v1",
        "embedding_size": args.embedding_size,
        "hidden_size": args.hidden_size,
        "seed": args.seed,
        "epochs_requested": args.epochs,
        "epochs_completed": len(history),
        "batch_size": args.batch_size,
        "optimizer": "AdamW",
        "learning_rate": 0.001,
        "weight_decay": 0.0001,
        "device": "cpu",
        "source_tokenization": "NFC Unicode code points",
        "target_tokenization": "atomic Google phone tokens; dot is a boundary token",
        "source_vocab": source_vocab,
        "target_vocab": target_vocab,
    }
    checkpoint = {
        "state_dict": model.state_dict(),
        "config": config,
        "source": source_manifest,
        "split_words": {name: sum(value == name for value in split_by_word.values()) for name in ("train", "dev", "test")},
    }
    torch.save(checkpoint, args.output_dir / "teacher.pt")
    report = {
        "schema": "google-khmer-neural-teacher-report/v1",
        "source": source_manifest,
        "config": {key: value for key, value in config.items() if key not in {"source_vocab", "target_vocab"}},
        "dataset": {
            "examples": len(examples),
            "unique_words": len(split_by_word),
            "train_examples": len(train_rows),
            "dev_examples": len(dev_rows),
            "test_examples": len(test_rows),
            "split_policy": "SHA-256 normalized spelling groups; 90/5/5",
        },
        "history": history,
        "test": test_metrics,
        "accuracy": None,
        "accuracy_status": "NOT_ASSESSED_NO_INDEPENDENT_IPA_GOLD",
        "profile_equivalence": "UNVERIFIED",
        "checkpoint": "teacher.pt",
    }
    (args.output_dir / "metrics.json").write_text(
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
