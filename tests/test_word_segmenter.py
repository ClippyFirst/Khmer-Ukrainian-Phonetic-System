import json
from pathlib import Path

from khmer_ua.rule_engine import RuleBasedKhmerEngine
from khmer_ua.word_segmenter import (
    WORD_DICTIONARY_SIZE,
    WORD_SEGMENTER_ID,
    segment_words,
    segment_words_candidates,
    describe_word_segmentation,
)

ROOT = Path(__file__).resolve().parents[1]


def test_full_word_dictionary_is_attributed_and_preserves_the_original_sample():
    full = json.loads((ROOT / "data/khmer/google-pronunciation-full-frequency.json").read_text(encoding="utf-8"))
    sample = json.loads((ROOT / "data/khmer/google-pronunciation-sample.json").read_text(encoding="utf-8"))
    assert WORD_DICTIONARY_SIZE == 61980
    assert len(full["entries"]) == 61980
    assert full["metadata"]["google_source_license"] == "CC BY 4.0"
    assert full["metadata"]["frequency_source_license"] == "ODC-By 1.0"
    assert full["metadata"]["phonemic_strings_included"] is False
    assert len(sample["entries"]) == 3009
    full_counts = {word: count for word, count in full["entries"]}
    assert all(full_counts.get(item["word"]) == item["count"] for item in sample["entries"])
    assert WORD_SEGMENTER_ID == "google-khmer-pronunciation-frequency-viterbi-full-v1"


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
    parity = json.loads((ROOT / "data/tests/word-segmentation-parity.json").read_text(encoding="utf-8"))
    assert parity["schema"] == "khmer-word-segmentation-parity/v1"
    cases = parity["cases"]
    engine = RuleBasedKhmerEngine()
    for case in cases:
        result = engine.analyze(case["input"])
        actual = [unit["source"] for unit in result["units"]]
        assert actual == case["units"], case["input"]


def test_concatenated_lexical_fixture_and_unknown_word_keep_word_boundary():
    result = RuleBasedKhmerEngine().analyze("កម្ពុជាប្រជាធិបតេយ្យ")
    assert [unit["source"] for unit in result["units"]] == [
        "កម្ពុជា", " ", "ប្រជាធិបតេយ្យ"
    ]
    unresolved = [unit for unit in result["units"] if unit["status"] == "NOT_ESTABLISHED"]
    assert len(unresolved) == 1
    assert unresolved[0]["source"] == "ប្រជាធិបតេយ្យ"


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



def test_ranked_candidates_are_lossless_distinct_and_keep_the_existing_best_path():
    for source in ("កម", "ផ្ឯម", "ខ្ញុំស្រឡាញ់ប្រទេសកម្ពុជា", "សុខសប្បាយទេ"):
        candidates = segment_words_candidates(source, 3)
        assert candidates
        assert len(candidates) <= 3
        assert [item["cost"] for item in candidates] == sorted(item["cost"] for item in candidates)
        assert len({
            tuple((segment["text"], segment["known"]) for segment in item["segments"])
            for item in candidates
        }) == len(candidates)
        assert all("".join(segment["text"] for segment in item["segments"]) == source for item in candidates)
        best = segment_words(source)
        assert candidates[0]["segments"] == [
            {
                "text": piece.text,
                "known": piece.known,
                "status": piece.status,
            }
            for piece in best
        ]


def test_candidate_limit_is_bounded_and_validated():
    import pytest

    with pytest.raises(ValueError, match="1 to 10"):
        segment_words_candidates("កម", 0)
    with pytest.raises(ValueError, match="1 to 10"):
        segment_words_candidates("កម", 11)
    with pytest.raises(ValueError, match="1 to 10"):
        segment_words_candidates("កម", True)


def test_candidate_diagnostics_protect_registered_lexical_spans():
    result = RuleBasedKhmerEngine().analyze("ក្រុងចតុម្មុខ")
    run = result["word_segmentation"]["candidate_runs"][0]
    assert run["source"] == "ក្រុងចតុម្មុខ"
    chunks = run["chunks"]
    assert "".join(chunk["source"] for chunk in chunks) == run["source"]
    protected = [chunk for chunk in chunks if chunk["method"] == "LEXICAL_FIXTURE_PROTECTED"]
    assert any(chunk["source"] == "ចតុម្មុខ" for chunk in protected)
    assert all(
        "".join(segment["text"] for segment in candidate["segments"]) == chunk["source"]
        for chunk in chunks
        for candidate in chunk["candidates"]
    )


def test_candidate_diagnostics_are_explicitly_not_probabilities_or_accuracy():
    result = RuleBasedKhmerEngine().analyze("កម")
    diagnostics = result["word_segmentation"]
    assert diagnostics["candidate_limit"] == 3
    assert "not probabilities" in diagnostics["score_note"]
    assert diagnostics["accuracy"] is None
    assert diagnostics["candidate_runs"][0]["chunks"][0]["method"] == "DICTIONARY_VITERBI_NBEST"



def test_every_full_dictionary_entry_remains_a_single_known_word():
    data = json.loads((ROOT / "data/khmer/google-pronunciation-full-frequency.json").read_text(encoding="utf-8"))
    for word, _count in data["entries"]:
        pieces = segment_words(word)
        assert len(pieces) == 1, word
        assert pieces[0].text == word and pieces[0].known, word


def test_long_runs_skip_only_nbest_diagnostics_and_keep_the_input():
    source = "ម" * 129
    assert segment_words_candidates(source, 3) == []
    diagnostics = describe_word_segmentation([], set(), source)
    chunk = diagnostics["candidate_runs"][0]["chunks"][0]
    assert chunk["source"] == source
    assert chunk["method"] == "DIAGNOSTICS_SKIPPED_LENGTH_LIMIT"
    assert chunk["candidates"] == []
    assert diagnostics["candidate_runs"][0]["status"] == "DIAGNOSTICS_LIMITED"
