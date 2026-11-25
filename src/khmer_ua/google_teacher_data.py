"""Deterministic, word-disjoint training data preparation for the offline G2P teacher.

The teacher learns Google source phonemic labels. These labels are not IPA gold.
Only unambiguous single-orthographic-syllable / single-source-syllable pairs are
used here so that the training target has a defensible unit boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import unicodedata
from typing import Iterable

from .google_phonemic import GooglePhonemicLexicon, load_google_phonemic_lexicon
from .orthographic_syllables import parse_orthographic_syllables

SPECIAL_TOKENS = ("<pad>", "<bos>", "<eos>", "<unk>")
DEFAULT_SEED = 20261125


@dataclass(frozen=True)
class GoogleTeacherExample:
    word: str
    source_tokens: tuple[str, ...]
    target_tokens: tuple[str, ...]
    source_row: int
    variant_index: int


@dataclass(frozen=True)
class GoogleTeacherDataset:
    examples: tuple[GoogleTeacherExample, ...]
    split_by_word: dict[str, str]
    source_revision: str
    source_tsv_sha256: str
    seed: int
    skipped: dict[str, int]

    @property
    def source_vocab(self) -> tuple[str, ...]:
        return tuple(sorted({token for row in self.examples for token in row.source_tokens}))

    @property
    def target_vocab(self) -> tuple[str, ...]:
        return tuple(sorted({token for row in self.examples for token in row.target_tokens}))

    def split(self, name: str) -> tuple[GoogleTeacherExample, ...]:
        if name not in {"train", "dev", "test"}:
            raise ValueError("split must be train, dev, or test")
        return tuple(row for row in self.examples if self.split_by_word[row.word] == name)

    def manifest(self) -> dict:
        return {
            "schema": "google-khmer-teacher-dataset/v1",
            "source_revision": self.source_revision,
            "source_tsv_sha256": self.source_tsv_sha256,
            "seed": self.seed,
            "examples": len(self.examples),
            "unique_words": len(self.split_by_word),
            "split_words": {
                name: sum(value == name for value in self.split_by_word.values())
                for name in ("train", "dev", "test")
            },
            "split_examples": {
                name: len(self.split(name)) for name in ("train", "dev", "test")
            },
            "source_vocab_size": len(self.source_vocab),
            "target_vocab_size": len(self.target_vocab),
            "skipped": dict(sorted(self.skipped.items())),
            "label_semantics": "Google source phonemic labels; not independent IPA gold or pronunciation accuracy",
            "alignment_policy": "one unambiguous Unicode orthographic syllable paired with one Google phonemic syllable",
        }


def split_for_word(word: str, seed: int = DEFAULT_SEED) -> str:
    """Assign a normalized spelling to a stable 90/5/5 split."""
    normalized = unicodedata.normalize("NFC", word.strip())
    digest = hashlib.sha256(f"{seed}\0{normalized}".encode("utf-8")).digest()
    bucket = int.from_bytes(digest[:4], "big") % 100
    if bucket < 90:
        return "train"
    if bucket < 95:
        return "dev"
    return "test"


def tokenize_source(text: str) -> tuple[str, ...]:
    """NFC-normalized Unicode code points; preserve every Khmer sign/code point."""
    normalized = unicodedata.normalize("NFC", text)
    return tuple(normalized)


def tokenize_target(phonemic: str) -> tuple[str, ...]:
    """Atomic source phones with the explicit syllable boundary retained."""
    tokens = tuple(phonemic.split())
    if not tokens or any(token in {"sil", "pau"} for token in tokens):
        raise ValueError("empty or non-lexical Google phonemic target")
    if tokens[0] == "." or tokens[-1] == "." or any(
        left == right == "." for left, right in zip(tokens, tokens[1:])
    ):
        raise ValueError("malformed Google phonemic syllable boundaries")
    return tokens


def build_google_teacher_dataset(
    lexicon: GooglePhonemicLexicon | None = None,
    *,
    seed: int = DEFAULT_SEED,
) -> GoogleTeacherDataset:
    source = lexicon if lexicon is not None else load_google_phonemic_lexicon()
    examples: list[GoogleTeacherExample] = []
    skipped = {
        "ambiguous_or_nonunique_orthography": 0,
        "multiple_or_mismatched_phonological_syllables": 0,
        "invalid_phonemic_target": 0,
    }

    for word, rows in source.entries.items():
        orthographic = parse_orthographic_syllables(word)
        if orthographic.status != "PARSED" or orthographic.syllables is None:
            skipped["ambiguous_or_nonunique_orthography"] += len(rows)
            continue
        if len(orthographic.syllables) != 1:
            skipped["multiple_or_mismatched_phonological_syllables"] += len(rows)
            continue

        for variant_index, row in enumerate(rows):
            try:
                target_tokens = tokenize_target(row.source_phonemic)
            except ValueError:
                skipped["invalid_phonemic_target"] += 1
                continue
            if "." in target_tokens:
                skipped["multiple_or_mismatched_phonological_syllables"] += 1
                continue
            examples.append(GoogleTeacherExample(
                word=word,
                source_tokens=tokenize_source(word),
                target_tokens=target_tokens,
                source_row=row.source_row,
                variant_index=variant_index,
            ))

    split_by_word = {
        word: split_for_word(word, seed)
        for word in sorted({row.word for row in examples})
    }
    return GoogleTeacherDataset(
        examples=tuple(sorted(examples, key=lambda row: (row.word, row.variant_index, row.source_row))),
        split_by_word=split_by_word,
        source_revision=source.manifest["source_revision"],
        source_tsv_sha256=source.manifest["source_tsv_sha256"],
        seed=seed,
        skipped=skipped,
    )


@lru_cache(maxsize=2)
def load_google_teacher_dataset(seed: int = DEFAULT_SEED) -> GoogleTeacherDataset:
    return build_google_teacher_dataset(seed=seed)


def validate_word_disjoint_splits(dataset: GoogleTeacherDataset) -> None:
    """Raise if any normalized spelling or pronunciation variant crosses splits."""
    observed: dict[str, set[str]] = {}
    for row in dataset.examples:
        observed.setdefault(row.word, set()).add(dataset.split_by_word[row.word])
    leaking = sorted(word for word, splits in observed.items() if len(splits) != 1)
    if leaking:
        raise ValueError(f"word-disjoint split leakage: {len(leaking)} spellings")
    if set(dataset.split_by_word.values()) != {"train", "dev", "test"}:
        raise ValueError("train/dev/test splits must all be non-empty")
