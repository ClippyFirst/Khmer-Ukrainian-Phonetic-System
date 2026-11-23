#!/usr/bin/env python3
"""Controlled khPOS comparison against a pinned upstream Rust tokenizer.

The CC BY-NC-SA corpus is fetched/checksummed on demand and never retained.
The upstream core is built from a pinned checkout; both Rust strategies use
this repository's exact 61,980-row word/count table as caller-supplied data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

from evaluate_khpos import (
    EXPECTED_GIT_BLOB_SHA, EXPECTED_SENTENCES, EXPECTED_TOKENS,
    BenchmarkSentence, RuleBasedKhmerEngine, download_corpus,
    prediction_signature, predicted_spans_from_units, prepare_sentence,
    score_predictions,
)

EXPECTED_RUNTIME_SHA256 = "a5d901e2ddce5f2370bbaf2f502a264e07127f5e97c395859a983d5a4f16b362"
EXPECTED_ENTRIES = 61980
UPSTREAM_REVISION = "f38eae5924d4e41a46fd2204cf6951cdb0dc8908"

RUST_MAIN = r'''
use khmer_tokenizer_core::{normalize, split_kcc, KhmerTokenizer, Strategy};
use std::{collections::HashSet, fs, io::{self, BufRead, Write}};

fn frequencies(path: &str) -> Vec<(String, u64)> {
    fs::read_to_string(path).expect("frequency table")
        .lines().filter(|line| !line.trim().is_empty() && !line.starts_with('#'))
        .map(|line| {
            let (word, count) = line.rsplit_once('\t').expect("word<TAB>count");
            (word.to_string(), count.parse::<u64>().expect("integer count"))
        }).collect()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).expect("strategy");
    let dict_path = args.get(2).expect("dictionary path");
    let freq_path = args.get(3).expect("frequency path");

    // Orthographic integrity: KCCs remain indivisible, normalization is
    // idempotent/length-preserving on the pinned repairs, and OOV runs group.
    assert_eq!(split_kcc("ស្ត្រី"), vec!["ស្ត្រី"]);
    for (raw, expected) in [("សិទិ្ធ", "សិទ្ធិ"), ("ស្រ្តី", "ស្ត្រី"), ("ំា", "ាំ")] {
        let fixed = normalize(raw);
        assert_eq!(fixed, expected);
        assert_eq!(normalize(&fixed), fixed);
        assert_eq!(fixed.len(), raw.len());
    }
    assert_eq!(
        KhmerTokenizer::from_words(["ក"]).without_normalization().segment("ឆ្នាំថ្មី"),
        vec!["ឆ្នាំថ្មី"]
    );

    let dict = fs::read_to_string(dict_path).expect("dictionary");
    let mut tk = KhmerTokenizer::from_dict_str(&dict).without_normalization();
    match mode.as_str() {
        "minwords" => tk = tk.with_strategy(Strategy::MinWordsDp),
        "unigram" => tk = tk.with_strategy(Strategy::UnigramDp)
            .with_frequencies(frequencies(freq_path)),
        _ => panic!("unknown strategy {mode}"),
    }

    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = io::BufWriter::new(stdout.lock());
    for line in stdin.lock().lines() {
        let source = line.expect("input line");
        let clusters = split_kcc(&source);
        let mut kcc_boundaries = HashSet::from([0usize]);
        let mut cluster_offset = 0usize;
        for cluster in clusters {
            cluster_offset += cluster.chars().count();
            kcc_boundaries.insert(cluster_offset);
        }
        let tokens = tk.segment(&source);
        let mut offset = 0usize;
        for token in &tokens {
            assert!(!token.contains('\t') && !token.contains('\n'));
            offset += token.chars().count();
            assert!(kcc_boundaries.contains(&offset), "token boundary splits a KCC");
        }
        assert_eq!(offset, source.chars().count(), "token output lost source characters");
        writeln!(out, "{}", tokens.join("\t")).expect("output");
    }
}
'''

def load_rows(path: Path) -> list[tuple[str, int]]:
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED_RUNTIME_SHA256:
        raise RuntimeError(f"runtime dictionary SHA mismatch: {actual}")
    payload = json.loads(raw)
    meta, entries = payload.get("metadata", {}), payload.get("entries")
    if meta.get("entry_count") != EXPECTED_ENTRIES or meta.get("fields") != ["word", "count"]:
        raise RuntimeError("runtime dictionary metadata mismatch")
    if meta.get("phonemic_strings_included") is not False:
        raise RuntimeError("phonemic source strings must not enter this frequency benchmark")
    if not isinstance(entries, list) or len(entries) != EXPECTED_ENTRIES:
        raise RuntimeError("runtime dictionary must contain exactly 61,980 rows")
    rows, seen = [], set()
    for row in entries:
        if not isinstance(row, list) or len(row) != 2:
            raise RuntimeError("malformed dictionary row")
        word, count = row
        if not isinstance(word, str) or not word or type(count) is not int or count < 0 or word in seen:
            raise RuntimeError("invalid or duplicate word/count row")
        seen.add(word)
        rows.append((word, count))
    return rows

def rust_harness(root: Path, core: Path) -> Path:
    project = root / "rust-harness"
    (project / "src").mkdir(parents=True)
    (project / "Cargo.toml").write_text(
        '[package]\nname="khpos-pinned-rust-harness"\nversion="0.1.0"\nedition="2021"\n\n'
        f'[dependencies]\nkhmer-tokenizer-core={{path="{core.resolve()}"}}\n',
        encoding="utf-8",
    )
    (project / "src" / "main.rs").write_text(RUST_MAIN, encoding="utf-8")
    return project / "Cargo.toml"

def score_rust(binary: Path, strategy: str, dictionary: Path, frequency: Path,
               sentences: list[BenchmarkSentence]) -> dict:
    started = time.perf_counter()
    result = subprocess.run(
        [str(binary), strategy, str(dictionary), str(frequency)],
        input="".join(s.source + "\n" for s in sentences),
        capture_output=True, text=True, check=True,
    )
    elapsed = time.perf_counter() - started
    lines = result.stdout.splitlines()
    if len(lines) != len(sentences):
        raise RuntimeError(f"{strategy}: output lines {len(lines)} != sentences {len(sentences)}")
    boundaries, all_spans, khmer_spans = [], [], []
    for sentence, line in zip(sentences, lines, strict=True):
        tokens = line.split("\t") if line else []
        # The shared evaluator records a boundary when it sees an explicit
        # single-space unit. Rust returns token arrays, so reconstruct those
        # separators here; offsets do not advance across the separator.
        units = []
        for index, token in enumerate(tokens):
            if index:
                units.append({"source": " "})
            units.append({"source": token})
        b, a, k = predicted_spans_from_units(units, sentence)
        boundaries.append(b); all_spans.append(a); khmer_spans.append(k)
    return {
        "strategy": strategy,
        "elapsed_seconds": round(elapsed, 4),
        "prediction_signature": prediction_signature(boundaries, all_spans, khmer_spans),
        "metrics": score_predictions(sentences, boundaries, all_spans, khmer_spans),
    }

def score_current(sentences: list[BenchmarkSentence]) -> dict:
    engine = RuleBasedKhmerEngine()
    boundaries, all_spans, khmer_spans = [], [], []
    started = time.perf_counter()
    for sentence in sentences:
        units = engine.analyze(sentence.source)["units"]
        b, a, k = predicted_spans_from_units(units, sentence)
        boundaries.append(b); all_spans.append(a); khmer_spans.append(k)
    return {
        "strategy": "project-viterbi-current",
        "elapsed_seconds": round(time.perf_counter() - started, 4),
        "prediction_signature": prediction_signature(boundaries, all_spans, khmer_spans),
        "metrics": score_predictions(sentences, boundaries, all_spans, khmer_spans),
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--runtime-dictionary", type=Path,
                        default=Path("data/khmer/google-pronunciation-full-frequency.json"))
    args = parser.parse_args()
    core = args.upstream / "core"
    if not (core / "Cargo.toml").is_file():
        raise RuntimeError(f"not an upstream checkout: {args.upstream}")
    rows = load_rows(args.runtime_dictionary)

    with tempfile.TemporaryDirectory(prefix="khpos-pinned-rust-") as temp:
        root = Path(temp)
        corpus = root / "OPEN-TEST.word"
        raw = download_corpus(corpus)
        lines = raw.decode("utf-8-sig").splitlines()
        if len(lines) != EXPECTED_SENTENCES:
            raise RuntimeError(f"sentence count mismatch: {len(lines)}")
        sentences, token_count = [], 0
        for line in lines:
            sentence, count = prepare_sentence(line)
            sentences.append(sentence); token_count += count
        if token_count != EXPECTED_TOKENS:
            raise RuntimeError(f"gold token count mismatch: {token_count}")

        dictionary, frequency = root / "dictionary.txt", root / "frequencies.tsv"
        dictionary.write_text("# Google Khmer spellings; CC BY 4.0.\n" +
                              "".join(word + "\n" for word, _ in rows), encoding="utf-8")
        frequency.write_text("# FineWeb-2 counts; ODC-By 1.0.\n" +
                             "".join(f"{word}\t{count}\n" for word, count in rows),
                             encoding="utf-8")
        manifest = rust_harness(root, core)
        subprocess.run(["cargo", "build", "--release", "--offline", "--manifest-path", str(manifest)],
                       check=True)
        binary = manifest.parent / "target" / "release" / "khpos-pinned-rust-harness"

        report = {
            "status": "MEASURED",
            "upstream": {"repository": "https://github.com/Alujack/khmer-tokenizer",
                         "revision": UPSTREAM_REVISION, "core_version": "0.3.0"},
            "dictionary": {"sha256": EXPECTED_RUNTIME_SHA256, "entries": len(rows),
                           "fields": "word/count only"},
            "corpus": {"revision": "0211405c145b0a340ad558569bd06c946b2296b4",
                       "git_blob_sha1": EXPECTED_GIT_BLOB_SHA, "sentences": len(sentences),
                       "gold_tokens": token_count,
                       "license": "CC BY-NC-SA 4.0; temporary download only"},
            "controls": {
                "normalization": "disabled for corpus scoring to preserve exact source spans",
                "normalization_fixtures": "PASS (idempotent and byte-length-preserving)",
                "kcc_boundaries": "PASS (every output token ends on a KCC boundary)",
                "oov_run_grouping": "PASS (pinned assertion)",
                "same_dictionary": "both Rust strategies use the identical 61,980 rows",
                "tagger": "not used; no non-commercial trained model",
            },
            "results": [
                score_current(sentences),
                score_rust(binary, "minwords", dictionary, frequency, sentences),
                score_rust(binary, "unigram", dictionary, frequency, sentences),
            ],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
