from __future__ import annotations

from khmer_ua.pcgn import analyze_pcgn_orthographic_chunk, resolve_pcgn_robat


def resolve(source: str, consonant: str | None):
    return resolve_pcgn_robat(analyze_pcgn_orthographic_chunk(source), consonant)


def test_pcgn_note6_robAt_returns_r_plus_caller_supplied_consonant_value():
    # Official guide example: ធម៌ -> thôrm; this resolver returns only the r+m component.
    result = resolve("ធម៌", "m")
    assert result.status == "RESOLVED"
    assert result.marked_character == "ម"
    assert result.marked_consonant_romanization == "m"
    assert result.romanization == "rm"
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_note6_accepts_values_from_the_published_consonant_inventory():
    for value in ("k", "kh", "ng", "ch", "chh", "nh", "d", "th", "t", "b", "p", "ph", "n", "m", "y", "r", "l", "v", "s", "h", "’"):
        result = resolve("ក៌", value)
        assert result.status == "RESOLVED", value
        assert result.romanization == "r" + value
        assert result.marked_character == "ក"


def test_pcgn_note6_abstains_without_explicit_supported_consonant_value():
    for value in (None, "", "x", "b,p", "m "):
        result = resolve("ធម៌", value)
        assert result.status == "UNRESOLVED", value
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note6_abstains_on_missing_misplaced_or_multiple_robat_marks():
    for source in ("ធម", "ធ៌ម", "ធម៌៌", "កា៌", "ក្x៌"):
        result = resolve(source, "m")
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note6_schema_preserves_component_only_and_explicit_context_boundary():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-robat-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "marked_character", "marked_consonant_romanization", "romanization",
        "status", "ipa", "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
