import json
from pathlib import Path

from khmer_ua.rule_engine import RuleBasedKhmerEngine
from khmer_ua.word_segmenter import (
    WORD_DICTIONARY_SIZE,
    WORD_SEGMENTER_ID,
    segment_words,
)

ROOT = Path(__file__).resolve().parents[1]


def test_bundled_word_dictionary_is_attributed_and_sample_sized():
    data = json.loads((ROOT / "data/khmer/google-pronunciation-sample.json").read_text(encoding="utf-8"))
    assert WORD_DICTIONARY_SIZE == 3009
    assert len(data["entries"]) == 3009
    assert data["metadata"]["pronunciation_data_license"] == "CC BY 4.0"
    assert data["metadata"]["frequency_data_license"] == "ODC-By 1.0"
    assert WORD_SEGMENTER_ID == "google-khmer-pronunciation-frequency-viterbi-sample-v1"


def test_sentence_is_segmented_into_dictionary_known_words():
    pieces = segment_words("ខ្ញុំស្រឡាញ់ប្រទេសកម្ពុជា")
    assert [piece.text for piece in pieces] == ["ខ្ញុំ", "ស្រឡាញ់", "ប្រទេស", "កម្ពុជា"]
    assert all(piece.known and piece.status == "DICTIONARY_MATCH" for piece in pieces)


def test_unknown_kcc_run_is_not_split_around_a_bare_letter_name():
    pieces = segment_words("ផ្ឯម")
    assert len(pieces) == 1
    assert pieces[0].text == "ផ្ឯម"
    assert pieces[0].known is False
    assert pieces[0].status == "OOV_RUN"


def test_python_tokenizer_matches_shared_browser_parity_cases():
    parity = json.loads((ROOT / "data/tests/tokenizer-parity.json").read_text(encoding="utf-8"))
    assert parity["schema"] == "khmer-tokenizer-parity/v2"
    cases = parity["cases"]
    engine = RuleBasedKhmerEngine()
    for case in cases:
        result = engine.analyze(case["input"])
        actual = [unit["source"] for unit in result["units"]]
        assert actual == case["units"], case["input"]


def test_engine_exposes_provisional_word_segmentation_without_claiming_pronunciation_gold():
    result = RuleBasedKhmerEngine().analyze("ខ្ញុំស្រឡាញ់ប្រទេសកម្ពុជា")
    assert [unit["source"] for unit in result["units"]] == [
        "ខ្ញុំ", " ", "ស្រឡាញ់", " ", "ប្រទេស", " ", "កម្ពុជា"
    ]
    assert result["word_segmentation"]["method"] == "DICTIONARY_VITERBI_CANDIDATE"
    assert result["word_segmentation"]["known_words"] == 4
    assert result["word_segmentation"]["oov_runs"] == 0
    assert result["word_segmentation"]["accuracy"] is None
    assert result["complete"] is False
