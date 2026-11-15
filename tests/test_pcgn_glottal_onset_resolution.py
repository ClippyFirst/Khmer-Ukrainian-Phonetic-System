from __future__ import annotations

from khmer_ua.pcgn import analyze_pcgn_orthographic_chunk, resolve_pcgn_glottal_onset


def resolve(source: str, word_initial: bool | None, followed_by_vowel: bool | None):
    return resolve_pcgn_glottal_onset(
        analyze_pcgn_orthographic_chunk(source),
        word_initial,
        followed_by_vowel,
    )


def test_pcgn_note4_glottal_onset_is_apostrophe_component():
    result = resolve("អ", False, False)
    assert result.status == "RESOLVED"
    assert result.source_character == "អ"
    assert result.romanization == "’"
    assert result.romanization_options == ("’",)
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_note4_apostrophe_is_optional_only_word_initial_before_vowel_letter():
    result = resolve("អ", True, True)
    assert result.status == "RESOLVED"
    assert result.romanization == "’"
    assert result.romanization_options == ("’", "")

    for word_initial, followed_by_vowel in ((True, False), (False, True), (False, False)):
        result = resolve("អ", word_initial, followed_by_vowel)
        assert result.status == "RESOLVED"
        assert result.romanization_options == ("’",)


def test_pcgn_note4_requires_explicit_position_and_following_vowel_context():
    for word_initial, followed_by_vowel in ((None, True), (True, None), (None, None)):
        result = resolve("អ", word_initial, followed_by_vowel)
        assert result.status == "UNRESOLVED"
        assert result.romanization is None
        assert result.romanization_options == ()


def test_pcgn_note4_abstains_on_noncarrier_or_mixed_orthographic_input():
    for source in ("ក", "អា", "អ៊", "អ្x"):
        result = resolve(source, True, True)
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None
        assert result.romanization_options == ()
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note4_schema_preserves_optional_apostrophe_context():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-glottal-onset-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_character", "word_initial", "followed_by_vowel_letter",
        "romanization", "romanization_options", "status", "ipa", "ukrainian",
        "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
