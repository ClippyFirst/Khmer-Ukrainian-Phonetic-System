from __future__ import annotations

from khmer_ua.pcgn import analyze_pcgn_orthographic_chunk, resolve_pcgn_toandakhiat


def resolve(source: str, marked_character: str | None):
    return resolve_pcgn_toandakhiat(
        analyze_pcgn_orthographic_chunk(source),
        marked_character,
    )


def test_pcgn_note8_requires_the_caller_to_identify_the_silent_character():
    result = resolve("ក៍", "ក")
    assert result.status == "RESOLVED"
    assert result.marked_character == "ក"
    assert result.marked_token_kind == "unstacked_consonant"
    assert result.effect == "OMIT_MARKED_CHARACTER"
    assert result.romanization is None
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_note8_supports_explicit_subscript_grapheme_identification():
    result = resolve("ក្យ៍", "្យ")
    assert result.status == "RESOLVED"
    assert result.marked_character == "្យ"
    assert result.marked_token_kind == "subscript_consonant"
    assert result.effect == "OMIT_MARKED_CHARACTER"
    assert result.romanization is None


def test_pcgn_note8_abstains_when_marked_character_is_missing_or_mismatched():
    cases = (
        ("ក៍", None),
        ("ក៍", ""),
        ("ក៍", "គ"),
        ("ក", "ក"),
        ("ក៍គ", "ក"),
    )
    for source, marked_character in cases:
        result = resolve(source, marked_character)
        assert result.status == "UNRESOLVED", (source, marked_character)
        assert result.effect is None
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note8_abstains_on_multiple_marks_and_nonconsonant_attachment():
    for source, marked_character in (("ក៍៍", "ក"), ("កា៍", "ា"), ("ក្៍", "្")):
        result = resolve(source, marked_character)
        assert result.status == "UNRESOLVED", source
        assert result.effect is None
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note8_schema_preserves_explicit_silent_character_boundary():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-toandakhiat-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "marked_character", "marked_token_kind", "effect", "romanization",
        "status", "ipa", "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["romanization"]["const"] is None
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
