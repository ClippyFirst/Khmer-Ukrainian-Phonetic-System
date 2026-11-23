#!/usr/bin/env python3
"""Ephemeral, non-commercial research benchmark for khPOS-trained HMM/taggers.

The restricted train/test corpus is fetched on demand, checksum-verified,
exact-overlap filtered, and removed with the temporary directory. Models are
trained in memory only: no model file or corpus is committed or uploaded.
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import tempfile
import time
import unicodedata
import urllib.request
import zipfile
from pathlib import Path

from evaluate_khpos import (
    EXPECTED_GIT_BLOB_SHA, EXPECTED_SENTENCES, EXPECTED_TOKENS,
    BenchmarkSentence, download_corpus, git_blob_sha, prediction_signature,
    predicted_spans_from_units, prepare_sentence, score_predictions,
)
from evaluate_khpos_external_rust import (
    EXPECTED_RUNTIME_SHA256, RuleBasedKhmerEngine, load_rows, score_current,
)

UPSTREAM_REVISION = "f38eae5924d4e41a46fd2204cf6951cdb0dc8908"
KHPOS_REVISION = "0211405c145b0a340ad558569bd06c946b2296b4"
TRAIN_PATH = "corpus-draft-ver-1.0/data/before-replace/train6.word"
TRAIN_BLOB_SHA1 = "3467e80897f192c4bbdb4b88fed488aaa16a830a"
TRAIN_SENTENCES = 12000
TRAIN_URL = (
    "https://raw.githubusercontent.com/ye-kyaw-thu/khPOS/"
    f"{KHPOS_REVISION}/{TRAIN_PATH}"
)
ALT_RECORD_URL = "https://zenodo.org/api/records/3937914/files/km-nova.zip/content"
ALT_ARCHIVE_MD5 = "20d39d8fa1b874b11ec374139fbe5654"
ALT_MEMBER_SUFFIX = "km-nova/data_km.km-tok.nova"

RUST_MAIN = r'''
use khmer_tokenizer_core::{split_kcc, HmmModel, KhmerTokenizer, Strategy};
use khmer_tokenizer_eval::{parse_khpos, train_hmm, train_tagger};
use std::{collections::HashSet, fs, io::{self, BufRead}, time::Instant};

fn read_frequencies(path: &str) -> Vec<(String, u64)> {
    fs::read_to_string(path).expect("frequency table")
        .lines().filter(|line| !line.trim().is_empty() && !line.starts_with('#'))
        .map(|line| {
            let (word, count) = line.rsplit_once('\t').expect("word<TAB>count");
            (word.to_string(), count.parse::<u64>().expect("integer count"))
        }).collect()
}

fn check_kcc(source: &str, tokens: &[String]) {
    let mut boundaries = HashSet::from([0usize]);
    let mut offset = 0usize;
    for cluster in split_kcc(source) {
        offset += cluster.chars().count();
        boundaries.insert(offset);
    }
    let mut output_offset = 0usize;
    for token in tokens {
        assert!(!token.contains('\t') && !token.contains('\n'));
        output_offset += token.chars().count();
        assert!(boundaries.contains(&output_offset), "token boundary splits a KCC");
    }
    assert_eq!(output_offset, source.chars().count(), "token output lost source characters");
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let dictionary_path = args.get(1).expect("dictionary path");
    let frequency_path = args.get(2).expect("frequency path");
    let training_path = args.get(3).expect("filtered training corpus path");

    let dict = fs::read_to_string(dictionary_path).expect("dictionary");
    let frequencies = read_frequencies(frequency_path);
    let training_raw = fs::read_to_string(training_path).expect("filtered khPOS training corpus");
    let training_examples = parse_khpos(&training_raw);
    assert!(!training_examples.is_empty(), "empty filtered training corpus");

    let training_started = Instant::now();
    let hmm_counts = train_hmm(&training_examples);
    let hmm = HmmModel::from_counts(hmm_counts.start, hmm_counts.trans, hmm_counts.emit);
    let tagger = train_tagger(&training_examples, 5);
    eprintln!("model_training_seconds={:.4}", training_started.elapsed().as_secs_f64());
    eprintln!("training_examples={}", training_examples.len());
    eprintln!("tagger_feature_count={}", tagger.feature_count());

    let variants: Vec<(&str, KhmerTokenizer)> = vec![
        ("minwords", KhmerTokenizer::from_dict_str(&dict)
            .with_strategy(Strategy::MinWordsDp).without_normalization()),
        ("unigram", KhmerTokenizer::from_dict_str(&dict)
            .with_strategy(Strategy::UnigramDp).with_frequencies(frequencies.clone())
            .without_normalization()),
        ("minwords-hmm", KhmerTokenizer::from_dict_str(&dict)
            .with_strategy(Strategy::MinWordsDp).with_hmm(hmm.clone()).without_normalization()),
        ("unigram-hmm", KhmerTokenizer::from_dict_str(&dict)
            .with_strategy(Strategy::UnigramDp).with_frequencies(frequencies.clone())
            .with_hmm(hmm.clone()).without_normalization()),
        ("minwords-tagger-fallback", KhmerTokenizer::from_dict_str(&dict)
            .with_strategy(Strategy::MinWordsDp).with_tagger(tagger.clone()).without_normalization()),
        ("unigram-tagger-fallback", KhmerTokenizer::from_dict_str(&dict)
            .with_strategy(Strategy::UnigramDp).with_frequencies(frequencies)
            .with_tagger(tagger.clone()).without_normalization()),
        ("tagger-full", KhmerTokenizer::empty()
            .with_strategy(Strategy::Tagger).with_tagger(tagger).without_normalization()),
    ];

    let stdin = io::stdin();
    let inputs: Vec<String> = stdin.lock().lines()
        .map(|line| line.expect("test input line")).collect();

    for (name, tokenizer) in variants {
        println!("__MODE__{name}");
        let started = Instant::now();
        for source in &inputs {
            let tokens = tokenizer.segment(source);
            check_kcc(source, &tokens);
            println!("{}", tokens.join("\t"));
        }
        println!("__TIME__{name}\t{:.6}", started.elapsed().as_secs_f64());
    }
}
'''

def download_train(destination: Path) -> bytes:
    request = urllib.request.Request(TRAIN_URL, headers={"User-Agent": "ClippyFirst-khPOS-local-model-research/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        raw = response.read()
    actual = git_blob_sha(raw)
    if actual != TRAIN_BLOB_SHA1:
        raise RuntimeError(f"khPOS train6.word Git blob SHA mismatch: expected {TRAIN_BLOB_SHA1}, got {actual}")
    destination.write_bytes(raw)
    return raw

def download_alt_test(destination: Path) -> bytes:
    request = urllib.request.Request(
        ALT_RECORD_URL,
        headers={"User-Agent": "ClippyFirst-khPOS-local-model-research/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        raw = response.read()
    actual = hashlib.md5(raw).hexdigest()
    if actual != ALT_ARCHIVE_MD5:
        raise RuntimeError(f"ALT archive MD5 mismatch: expected {ALT_ARCHIVE_MD5}, got {actual}")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = [name for name in archive.namelist() if name.endswith(ALT_MEMBER_SUFFIX)]
        if len(names) != 1:
            raise RuntimeError(f"expected one {ALT_MEMBER_SUFFIX} member in ALT archive, found {names}")
        data = archive.read(names[0])
    destination.write_bytes(data)
    return data

def parse_alt_test(raw: bytes) -> tuple[list[BenchmarkSentence], int, int]:
    sentences: list[BenchmarkSentence] = []
    token_count = 0
    source_lines = raw.decode("utf-8-sig").splitlines()
    for line in source_lines:
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        id_parts = parts[0].split(".")
        if len(id_parts) < 2:
            continue
        try:
            article_id = int(id_parts[1])
        except ValueError:
            article_id = 0
        if article_id % 10 != 0:
            continue
        raw_tokens = parts[1].split()
        if not raw_tokens:
            continue
        sentence, count = prepare_sentence(parts[1])
        expected_source = "".join(unicodedata.normalize("NFC", token) for token in raw_tokens)
        if sentence.source != expected_source:
            raise RuntimeError("ALT test tokens contain a khPOS-only compound marker; refusing lossy normalization")
        sentences.append(sentence)
        token_count += count
    if not sentences:
        raise RuntimeError("ALT parser produced no article-id-mod-10 test sentences")
    return sentences, token_count, len(source_lines)

def build_manifest(root: Path, core: Path, evaluation: Path) -> Path:
    project = root / "model-harness"
    (project / "src").mkdir(parents=True)
    manifest = (
        '[package]\nname="khpos-local-model-harness"\nversion="0.1.0"\nedition="2021"\n\n'
        f'[dependencies]\nkhmer-tokenizer-core={{path="{core.resolve()}"}}\n'
        f'khmer-tokenizer-eval={{path="{evaluation.resolve()}"}}\n'
    )
    (project / "Cargo.toml").write_text(manifest, encoding="utf-8")
    (project / "src" / "main.rs").write_text(RUST_MAIN, encoding="utf-8")
    return project / "Cargo.toml"

def score_variant(name: str, lines: list[str], sentences: list[BenchmarkSentence], elapsed: float) -> dict:
    if len(lines) != len(sentences):
        raise RuntimeError(f"{name}: output line count {len(lines)} != {len(sentences)}")
    boundaries, all_spans, khmer_spans = [], [], []
    for sentence, line in zip(sentences, lines, strict=True):
        tokens = line.split("\t") if line else []
        units = []
        for index, token in enumerate(tokens):
            if index:
                units.append({"source": " "})
            units.append({"source": token})
        b, a, k = predicted_spans_from_units(units, sentence)
        boundaries.append(b); all_spans.append(a); khmer_spans.append(k)
    return {
        "strategy": name,
        "elapsed_seconds_all_test_corpora": round(elapsed, 4),
        "prediction_signature": prediction_signature(boundaries, all_spans, khmer_spans),
        "metrics": score_predictions(sentences, boundaries, all_spans, khmer_spans),
    }

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--runtime-dictionary", type=Path,
                        default=Path("data/khmer/google-pronunciation-full-frequency.json"))
    args = parser.parse_args()

    core, evaluation = args.upstream / "core", args.upstream / "eval"
    if not (core / "Cargo.toml").is_file() or not (evaluation / "Cargo.toml").is_file():
        raise RuntimeError(f"not a complete pinned upstream checkout: {args.upstream}")
    rows = load_rows(args.runtime_dictionary)

    with tempfile.TemporaryDirectory(prefix="khpos-local-model-research-") as temporary:
        root = Path(temporary)
        test_path = root / "OPEN-TEST.word"
        test_raw = download_corpus(test_path)
        test_lines = test_raw.decode("utf-8-sig").splitlines()
        if len(test_lines) != EXPECTED_SENTENCES:
            raise RuntimeError(f"expected {EXPECTED_SENTENCES} test sentences, got {len(test_lines)}")
        sentences, token_count = [], 0
        for line in test_lines:
            sentence, count = prepare_sentence(line)
            sentences.append(sentence); token_count += count
        if token_count != EXPECTED_TOKENS:
            raise RuntimeError(f"expected {EXPECTED_TOKENS} test tokens, got {token_count}")
        khpos_sentences = sentences
        khpos_token_count = token_count
        alt_path = root / "data_km.km-tok.nova"
        alt_raw = download_alt_test(root / "km-nova.zip")
        alt_sentences, alt_token_count, alt_source_lines = parse_alt_test(alt_raw)
        all_sentences = [*khpos_sentences, *alt_sentences]
        test_sources = {sentence.source for sentence in all_sentences}

        train_path = root / "train6.filtered.word"
        train_raw = download_train(root / "train6.word")
        train_lines = [line for line in train_raw.decode("utf-8-sig").splitlines() if line.strip()]
        if len(train_lines) != TRAIN_SENTENCES:
            raise RuntimeError(f"expected {TRAIN_SENTENCES} khPOS training sentences, got {len(train_lines)}")
        filtered_lines, excluded_exact_overlaps = [], 0
        for line in train_lines:
            source = prepare_sentence(line)[0].source
            if source in test_sources:
                excluded_exact_overlaps += 1
            else:
                filtered_lines.append(line)
        if not filtered_lines:
            raise RuntimeError("exact-overlap filtering removed the entire training corpus")
        train_path.write_text("\n".join(filtered_lines) + "\n", encoding="utf-8")

        dictionary_path, frequency_path = root / "dictionary.txt", root / "frequencies.tsv"
        dictionary_path.write_text("# Google Khmer spellings; CC BY 4.0.\n" +
                                   "".join(word + "\n" for word, _ in rows), encoding="utf-8")
        frequency_path.write_text("# FineWeb-2 counts; ODC-By 1.0.\n" +
                                  "".join(f"{word}\t{count}\n" for word, count in rows),
                                  encoding="utf-8")
        manifest = build_manifest(root, core, evaluation)
        subprocess.run(["cargo", "build", "--release", "--offline", "--manifest-path", str(manifest)],
                       check=True)
        binary = manifest.parent / "target" / "release" / "khpos-local-model-harness"
        result = subprocess.run(
            [str(binary), str(dictionary_path), str(frequency_path), str(train_path)],
            input="".join(sentence.source + "\n" for sentence in all_sentences),
            capture_output=True, text=True, check=True,
        )
        parsed = result.stdout.splitlines()
        cursor = 0
        results_by_corpus = {
            "khpos_open_test": [score_current(khpos_sentences)],
            "alt_test": [score_current(alt_sentences)],
        }
        modes = ["minwords", "unigram", "minwords-hmm", "unigram-hmm",
                 "minwords-tagger-fallback", "unigram-tagger-fallback", "tagger-full"]
        for mode in modes:
            expected_marker = f"__MODE__{mode}"
            if cursor >= len(parsed) or parsed[cursor] != expected_marker:
                raise RuntimeError(f"expected {expected_marker} in Rust harness output")
            cursor += 1
            token_lines = parsed[cursor:cursor + len(all_sentences)]
            cursor += len(all_sentences)
            if cursor >= len(parsed) or not parsed[cursor].startswith(f"__TIME__{mode}\t"):
                raise RuntimeError(f"missing timing marker for {mode}")
            elapsed = float(parsed[cursor].split("\t", 1)[1])
            cursor += 1
            khpos_lines = token_lines[:len(khpos_sentences)]
            alt_lines = token_lines[len(khpos_sentences):]
            results_by_corpus["khpos_open_test"].append(
                score_variant(mode, khpos_lines, khpos_sentences, elapsed)
            )
            results_by_corpus["alt_test"].append(
                score_variant(mode, alt_lines, alt_sentences, elapsed)
            )
        if cursor != len(parsed):
            raise RuntimeError("unexpected trailing output from Rust model harness")

        report = {
            "status": "MEASURED_LOCAL_ONLY",
            "upstream": {"repository": "https://github.com/Alujack/khmer-tokenizer",
                         "revision": UPSTREAM_REVISION, "core_version": "0.3.0"},
            "test_corpora": {
                "khpos_open_test": {"revision": KHPOS_REVISION,
                                    "path": "corpus-draft-ver-1.0/data/OPEN-TEST.word",
                                    "git_blob_sha1": EXPECTED_GIT_BLOB_SHA,
                                    "sentences": len(khpos_sentences),
                                    "gold_tokens": khpos_token_count,
                                    "license": "CC BY-NC-SA 4.0"},
                "alt_test": {"record": "https://zenodo.org/records/3937914",
                             "archive_md5": ALT_ARCHIVE_MD5,
                             "member": ALT_MEMBER_SUFFIX,
                             "source_lines": alt_source_lines,
                             "test_sentences": len(alt_sentences),
                             "gold_tokens": alt_token_count,
                             "split": "article ID modulo 10 equals zero, matching upstream parse_alt",
                             "license": "CC BY-NC-SA 4.0"},
            },
            "training_corpus": {"revision": KHPOS_REVISION, "path": TRAIN_PATH,
                                "git_blob_sha1": TRAIN_BLOB_SHA1,
                                "source_sentences": len(train_lines),
                                "exact_test_input_overlaps_excluded_across_both_test_sets": excluded_exact_overlaps,
                                "training_sentences_after_filter": len(filtered_lines),
                                "license": "CC BY-NC-SA 4.0"},
            "dictionary": {"sha256": EXPECTED_RUNTIME_SHA256, "entries": len(rows),
                           "fields": "word/count only"},
            "controls": {
                "models": "trained in memory only; no model file written or uploaded",
                "training": "HMM counts from train split; averaged-perceptron tagger trained for 5 epochs",
                "exact_overlap": "training rows with NFC-normalized input identical to any khPOS OPEN-TEST or ALT test input were excluded",
                "normalization": "disabled during corpus scoring to preserve source spans",
                "kcc_boundaries": "PASS (all emitted token boundaries are KCC boundaries)",
                "frequency_data": "FineWeb-2 counts used for UnigramDp; no khPOS-derived frequencies",
                "license_boundary": "research-only, non-commercial; no redistributable model produced",
            },
            "training_seconds": next((line.split("=", 1)[1] for line in result.stderr.splitlines()
                                      if line.startswith("model_training_seconds=")), None),
            "training_examples": next((line.split("=", 1)[1] for line in result.stderr.splitlines()
                                       if line.startswith("training_examples=")), None),
            "tagger_feature_count": next((line.split("=", 1)[1] for line in result.stderr.splitlines()
                                          if line.startswith("tagger_feature_count=")), None),
            "results_by_corpus": results_by_corpus,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
