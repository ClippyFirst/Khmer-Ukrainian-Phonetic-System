#!/usr/bin/env python3
"""Distill offline teacher predictions into a deterministic OOV syllable table.

The output is a research artifact, not a promoted runtime rule set. Every
candidate remains PROVISIONAL and retains the source/model/profile caveats.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import torch
from torch.nn.utils.rnn import pad_sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from google_teacher.model import KhmerPhonemicSeq2Seq
from train_google_phonemic_teacher import (
    BOS, EOS, PAD, UNK, Example, edit_distance, load_examples,
)
from khmer_ua.google_phonemic import load_google_phonemic_lexicon, parse_google_phonemic
from khmer_ua.google_teacher_data import split_for_word, tokenize_source
from khmer_ua.orthographic_syllables import parse_orthographic_syllables
from khmer_ua.ipa_target import adapt_phonetic_result


def load_teacher(path: Path):
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)
    config = checkpoint["config"]
    source_vocab = config["source_vocab"]
    target_vocab = config["target_vocab"]
    model = KhmerPhonemicSeq2Seq(
        len(source_vocab),
        len(target_vocab),
        embedding_size=config["embedding_size"],
        hidden_size=config["hidden_size"],
        padding_index=source_vocab[PAD],
    )
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return model, checkpoint, source_vocab, target_vocab


@torch.inference_mode()
def predict_many(model, words, source_vocab, target_vocab, batch_size=192):
    results = {}
    for start in range(0, len(words), batch_size):
        batch = words[start:start + batch_size]
        sequences = [
            torch.tensor(
                [
                    source_vocab[BOS],
                    *[source_vocab.get(token, source_vocab[UNK]) for token in tokenize_source(word)],
                    source_vocab[EOS],
                ],
                dtype=torch.long,
            )
            for word in batch
        ]
        lengths = torch.tensor([len(row) for row in sequences], dtype=torch.long)
        source = pad_sequence(sequences, batch_first=True, padding_value=source_vocab[PAD])
        decoded = model.greedy_decode(
            source, lengths, bos_id=target_vocab[BOS], eos_id=target_vocab[EOS], max_length=64
        )
        inverse = {value: key for key, value in target_vocab.items()}
        for word, token_ids in zip(batch, decoded):
            results[word] = [inverse.get(token_id, UNK) for token_id in token_ids]
    return results


def build_syllable_inventory(lexicon):
    known_words = set(lexicon.entries)
    syllables = set()
    ambiguous_words = 0
    invalid_words = 0
    for word in known_words:
        parsed = parse_orthographic_syllables(word)
        if parsed.status != "PARSED" or parsed.syllables is None:
            if parsed.status == "AMBIGUOUS":
                ambiguous_words += 1
            else:
                invalid_words += 1
            continue
        syllables.update(item.source_text for item in parsed.syllables)
    oov = sorted(
        syllable for syllable in syllables
        if syllable not in known_words and 1 <= len(syllable) <= 16
    )
    return sorted(syllables), oov, {
        "known_lexical_words": len(known_words),
        "unique_orthographic_syllables": len(syllables),
        "oov_syllable_candidates": len(oov),
        "ambiguous_orthographic_words_skipped": ambiguous_words,
        "invalid_or_evidence_limited_words_skipped": invalid_words,
    }


def compose_test_diagnostic(model, examples, source_vocab, target_vocab, batch_size):
    eligible = []
    all_syllables = set()
    for row in examples:
        parsed = parse_orthographic_syllables(row.word)
        if parsed.status != "PARSED" or parsed.syllables is None:
            continue
        if len(parsed.syllables) != row.target.count(".") + 1:
            continue
        syllables = tuple(item.source_text for item in parsed.syllables)
        eligible.append((row, syllables))
        all_syllables.update(syllables)

    predictions = predict_many(model, sorted(all_syllables), source_vocab, target_vocab, batch_size)
    total_distance = 0
    total_reference = 0
    exact = 0
    boundary_count_match = 0
    covered = 0
    for row, syllables in eligible:
        composed = []
        valid = True
        for index, syllable in enumerate(syllables):
            phones = predictions.get(syllable, [])
            if not phones or UNK in phones or "." in phones:
                valid = False
                break
            if index:
                composed.append(".")
            composed.extend(phones)
        if not valid:
            continue
        reference = list(row.target)
        total_distance += edit_distance(composed, reference)
        total_reference += len(reference)
        exact += int(composed == reference)
        boundary_count_match += int(composed.count(".") == reference.count("."))
        covered += 1
    return {
        "alignment_assumption": "orthographic syllable count equals Google phonological dot count; count-only diagnostic, not expert alignment",
        "eligible_heldout_word_variants": len(eligible),
        "covered_heldout_word_variants": covered,
        "output_coverage": covered / max(len(eligible), 1),
        "word_exact_match": exact / max(covered, 1),
        "phoneme_token_error_rate": total_distance / max(total_reference, 1),
        "syllable_boundary_count_accuracy": boundary_count_match / max(covered, 1),
        "metric_semantics": "held-out Google source-label composition diagnostic; not independent IPA accuracy",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=192)
    args = parser.parse_args()

    model, checkpoint, source_vocab, target_vocab = load_teacher(args.checkpoint)
    lexicon = load_google_phonemic_lexicon()
    all_syllables, oov_syllables, inventory = build_syllable_inventory(lexicon)
    predictions = predict_many(model, oov_syllables, source_vocab, target_vocab, args.batch_size)
    mapping = {}
    table = []
    rejected = {"empty_prediction": 0, "unknown_phone": 0, "internal_boundary": 0, "unmapped_ipa": 0}
    for syllable in oov_syllables:
        phones = predictions.get(syllable, [])
        if not phones:
            rejected["empty_prediction"] += 1
            continue
        if UNK in phones:
            rejected["unknown_phone"] += 1
            continue
        if "." in phones:
            rejected["internal_boundary"] += 1
            continue
        parsed = parse_google_phonemic(" ".join(phones))
        if parsed.ipa is None or parsed.candidate is None:
            rejected["unmapped_ipa"] += 1
            continue
        ukrainian = adapt_phonetic_result(parsed.candidate, allow_uncertain=True)
        record = {
            "orthography": syllable,
            "google_phonemic_tokens": phones,
            "ipa": parsed.ipa,
            "ipa_kind": "PHONEMIC",
            "ukrainian_candidate": ukrainian,
            "status": "PROVISIONAL",
            "mapping_status": parsed.mapping_status,
            "uncertainty": [
                "NEURAL_TEACHER_PREDICTION_NOT_SOURCE_ATTESTED",
                "TARGET_PROFILE_EQUIVALENCE_UNVERIFIED",
                *parsed.uncertainty,
            ],
        }
        table.append(record)
        mapping[syllable] = phones

    examples, source_manifest = load_examples()
    split = {word: split_for_word(word, checkpoint["config"]["seed"]) for word in {row.word for row in examples}}
    heldout = [row for row in examples if split[row.word] == "test"]
    composition = compose_test_diagnostic(
        model, heldout, source_vocab, target_vocab, args.batch_size
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    teacher_sha = hashlib.sha256(args.checkpoint.read_bytes()).hexdigest()
    artifact = {
        "schema": "google-khmer-neural-distilled-syllables/v1",
        "source": {
            "id": source_manifest["source_id"],
            "revision": source_manifest["source_revision"],
            "tsv_sha256": source_manifest["source_tsv_sha256"],
            "license": "CC-BY-4.0",
            "attribution": "Google language-resources Khmer pronunciation lexicon and Festvox phonology inventory",
        },
        "teacher": {
            "architecture": checkpoint["config"]["architecture"],
            "checkpoint_sha256": teacher_sha,
            "seed": checkpoint["config"]["seed"],
            "profile_equivalence": "UNVERIFIED",
            "accuracy": None,
        },
        "candidate_policy": "OOV orthographic syllable strings only; deterministic lookup candidate, never SUPPORTED without independent evidence",
        "inventory": inventory,
        "rejected": rejected,
        "candidates": table,
    }
    (args.output_dir / "distilled-syllables.json").write_text(
        json.dumps(artifact, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    report = {
        "schema": "google-khmer-neural-distillation-report/v1",
        "source": source_manifest,
        "teacher_checkpoint_sha256": teacher_sha,
        "inventory": inventory,
        "accepted_candidates": len(table),
        "rejected_candidates": rejected,
        "composition_test": composition,
        "accuracy": None,
        "accuracy_status": "NOT_ASSESSED_NO_INDEPENDENT_IPA_GOLD",
        "promotion": "ZERO_RULES_PROMOTED",
    }
    (args.output_dir / "distillation-metrics.json").write_text(
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
