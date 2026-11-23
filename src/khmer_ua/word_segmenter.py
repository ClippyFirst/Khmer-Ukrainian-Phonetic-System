"""Dictionary/Viterbi Khmer word segmentation candidate.

The bundled lexicon is a 3,009-entry attributed sample. Word boundaries are
provisional and are not treated as linguistic gold.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_DATA_PATH = ROOT / "data" / "khmer" / "google-pronunciation-sample.json"
with _DATA_PATH.open(encoding="utf-8") as _handle:
    _DATASET = json.load(_handle)

WORD_SEGMENTER_ID = "google-khmer-pronunciation-frequency-viterbi-sample-v1"
WORD_DICTIONARY_SIZE = len(_DATASET["entries"])
_COENG = "\u17d2"
_MAX_CLUSTERS = 12
_COUNTS = {item["word"]: int(item["count"]) for item in _DATASET["entries"]}
_TOTAL = sum(_COUNTS.values())
_DENOMINATOR = _TOTAL + len(_COUNTS) + 1
_COSTS = {word: -math.log((count + 1) / _DENOMINATOR) for word, count in _COUNTS.items()}
_UNKNOWN_COST = -math.log(1 / _DENOMINATOR) + 4
_PREFIXES: set[str] = set()


@dataclass(frozen=True)
class WordSegment:
    text: str
    known: bool
    status: str
    source: str = WORD_SEGMENTER_ID


def _is_base(character: str) -> bool:
    return bool(character) and 0x1780 <= ord(character) <= 0x17B3


def _cluster_starts(text: str) -> tuple[list[str], list[int]]:
    chars = list(text)
    bounds = [0]
    for index in range(1, len(chars)):
        if _is_base(chars[index]) and chars[index - 1] != _COENG:
            bounds.append(index)
    bounds.append(len(chars))
    return chars, bounds


def _is_bare_letter(word: str) -> bool:
    chars, bounds = _cluster_starts(word)
    if len(bounds) != 2:
        return False
    return not any(
        0x17A3 <= ord(char) <= 0x17B3
        or 0x17B6 <= ord(char) <= 0x17C5
        or ord(char) in {0x17C7, 0x17C8}
        for char in chars
    )


def _merge_unknown_and_bare_letters(pieces: list[tuple[str, bool]]) -> list[tuple[str, bool]]:
    output: list[tuple[str, bool]] = []
    group: list[tuple[str, bool]] = []

    def flush() -> None:
        if not group:
            return
        if any(not known for _, known in group):
            output.append(("".join(value for value, _ in group), False))
        else:
            output.extend(group)
        group.clear()

    for value, known in pieces:
        if not known or _is_bare_letter(value):
            group.append((value, known))
        else:
            flush()
            output.append((value, known))
    flush()
    return output


for _word in _COUNTS:
    _chars, _bounds = _cluster_starts(_word)
    for _index in range(1, len(_bounds)):
        _PREFIXES.add("".join(_chars[:_bounds[_index]]))


def is_known_word(word: str) -> bool:
    return word in _COUNTS


def segment_words(text: str) -> list[WordSegment]:
    if not text:
        return []
    chars, bounds = _cluster_starts(text)
    count = len(bounds) - 1
    best = [math.inf] * (count + 1)
    back: list[tuple[int, bool] | None] = [None] * (count + 1)
    best[0] = 0.0

    for start in range(count):
        if math.isinf(best[start]):
            continue
        unknown_candidate = best[start] + _UNKNOWN_COST
        if unknown_candidate < best[start + 1]:
            best[start + 1] = unknown_candidate
            back[start + 1] = (start, False)

        for end in range(start + 1, min(start + _MAX_CLUSTERS, count) + 1):
            word = "".join(chars[bounds[start]:bounds[end]])
            if word not in _PREFIXES:
                break
            cost = _COSTS.get(word)
            if cost is not None and best[start] + cost < best[end]:
                best[end] = best[start] + cost
                back[end] = (start, True)

    reversed_segments: list[tuple[str, bool]] = []
    cursor = count
    while cursor > 0:
        edge = back[cursor]
        if edge is None:
            return [WordSegment(text, False, "OOV_RUN")]
        previous, known = edge
        reversed_segments.append(("".join(chars[bounds[previous]:bounds[cursor]]), known))
        cursor = previous
    merged = _merge_unknown_and_bare_letters(list(reversed(reversed_segments)))
    return [
        WordSegment(value, known, "DICTIONARY_MATCH" if known else "OOV_RUN")
        for value, known in merged
    ]


def describe_word_segmentation(tokens: list[str], fixture_keys: set[str] | None = None) -> dict:
    fixture_keys = fixture_keys or set()
    word_tokens = []
    for token in tokens:
        if not any(0x1780 <= ord(char) <= 0x17D3 for char in token):
            continue
        status = (
            "LEXICAL_FIXTURE" if token in fixture_keys
            else "DICTIONARY_MATCH" if is_known_word(token)
            else "OOV_RUN"
        )
        word_tokens.append({"text": token, "status": status})
    return {
        "method": "DICTIONARY_VITERBI_CANDIDATE",
        "engine": WORD_SEGMENTER_ID,
        "dictionary_entries": WORD_DICTIONARY_SIZE,
        "known_words": sum(item["status"] != "OOV_RUN" for item in word_tokens),
        "oov_runs": sum(item["status"] == "OOV_RUN" for item in word_tokens),
        "accuracy": None,
        "tokens": word_tokens,
        "note": "Word boundaries are provisional dictionary-Viterbi candidates; no independent segmentation accuracy has been measured for this project.",
    }
