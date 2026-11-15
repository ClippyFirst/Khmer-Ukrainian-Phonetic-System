from __future__ import annotations

from khmer_ua.pcgn import (
    PCGN_WEAK_SUBSCRIPTS,
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_series,
)


def test_pcgn_note3_weak_subscript_inventory_is_exact():
    assert PCGN_WEAK_SUBSCRIPTS == frozenset("ងញណនមយរលវ")
    assert "ស" not in PCGN_WEAK_SUBSCRIPTS


def test_pcgn_note3_weak_foot_uses_base_series_when_base_is_not_weak():
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ថ្ម"))

    assert result.series == "â"
    assert result.basis == "BASE"
    assert result.status == "RESOLVED"
    assert result.onset_exception is None
    assert result.source_locator == "PCGN 1972, Note 3 (pp. 2–3)"


def test_pcgn_note3_nonweak_foot_selects_foot_series():
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("គ្ក"))

    assert result.series == "â"
    assert result.basis == "SUBSCRIPT"
    assert result.status == "RESOLVED"


def test_pcgn_note3_weak_base_does_not_override_weak_foot():
    # ង is weak and second-series; ណ is weak and first-series.
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ង្ណ"))

    assert result.series == "â"
    assert result.basis == "SUBSCRIPT"
    assert result.status == "RESOLVED"


def test_pcgn_note3_ba_with_subscript_has_documented_p_in_a_exception():
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ប្ក"))

    assert result.series == "â"
    assert result.basis == "BASE"
    assert result.onset_exception == "BA_WITH_FOOT_P_IN_A_SERIES"
    assert "PCGN_NOTE_3_BA_WITH_FOOT_P_EXCEPTION" in result.warnings


def test_pcgn_series_without_subscript_uses_base_register():
    assert resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ក")).series == "â"
    assert resolve_pcgn_series(analyze_pcgn_orthographic_chunk("គ")).series == "ô"


def test_pcgn_series_abstains_on_shifters_multiple_feet_and_unsupported_input():
    for source in ("ក៊", "ក្ប្ល", "ក្x", "ឥ"):
        result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk(source))
        assert result.status == "UNRESOLVED"
        assert result.series is None
        assert result.basis == "UNRESOLVED"
        assert result.onset_exception is None


def test_pcgn_series_decision_serializes_source_locator_and_no_phonetic_output():
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ថ្ម"))
    payload = result.to_dict()

    assert payload["series"] == "â"
    assert payload["source_locator"] == "PCGN 1972, Note 3 (pp. 2–3)"
    assert payload["status"] == "RESOLVED"
    assert "NO_VOWEL_OR_ROMANIZATION_OUTPUT" not in payload["warnings"]
