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
    assert result.series_before_shifter == "â"
    assert result.shifter_effect is None


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


def test_pcgn_note2_absent_shifter_preserves_omission_uncertainty_warning():
    # The guide says Khmer diacritical marks are frequently omitted. A resolved
    # graphemic default must therefore not imply that no shifter was intended.
    for source, expected in (("ក", "â"), ("គ", "ô")):
        result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk(source))
        assert result.status == "RESOLVED"
        assert result.series == expected
        assert (
            "PCGN_NOTE_2_DIACRITICS_MAY_BE_OMITTED_CONSULT_REFERENCE_IF_SERIES_UNCERTAIN"
            in result.warnings
        )


def test_pcgn_series_abstains_on_shifters_multiple_feet_and_unsupported_input():
    for source in ("ក៉", "ក្ប្ល", "ក្x", "ក្ឡ", "ឥ"):
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


def test_pcgn_series_schema_enforces_explicit_resolved_and_unresolved_shapes():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-series-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "series", "basis", "status", "onset_exception", "series_before_shifter", "shifter_effect", "source_locator", "warnings"
    }
    assert schema["properties"]["source_locator"]["enum"] == ["PCGN 1972, Note 3 (pp. 2–3)", "PCGN 1972, Notes 2–3 (pp. 2–3)"]
    assert schema["allOf"][0]["then"]["properties"]["series"]["enum"] == ["â", "ô"]
    assert schema["allOf"][1]["then"]["properties"]["series"]["const"] is None


def test_pcgn_note2_triisap_changes_a_series_to_o_series():
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ហ៊"))
    assert result.series_before_shifter == "â"
    assert result.series == "ô"
    assert result.shifter_effect == "TRIISAP_A_TO_O"
    assert result.status == "RESOLVED"
    assert result.source_locator == "PCGN 1972, Notes 2–3 (pp. 2–3)"


def test_pcgn_note2_muusikatoan_changes_o_series_to_a_series():
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ញ៉"))
    assert result.series_before_shifter == "ô"
    assert result.series == "â"
    assert result.shifter_effect == "MUUSIKATOAN_O_TO_A"
    assert result.status == "RESOLVED"


def test_pcgn_note3_ba_with_muusikatoan_preserves_p_in_a_exception():
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ប៉"))
    assert result.series == "â"
    assert result.onset_exception == "BA_WITH_MUUSIKATOAN_P_IN_A_SERIES"
    assert result.series_before_shifter == "â"
    assert result.shifter_effect == "BA_MUUSIKATOAN_P_IN_A"


def test_pcgn_note2_triisap_applies_to_base_plus_weak_foot_cluster():
    # Note 3 selects the base series because ម is a weak foot; Note 2 then
    # shifts the resulting â-series cluster to ô. Unicode requires the mark
    # immediately after the base, before COENG+foot.
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ថ៊្ម"))
    assert result.series_before_shifter == "â"
    assert result.series == "ô"
    assert result.basis == "BASE"
    assert result.shifter_effect == "TRIISAP_A_TO_O"
    assert "PCGN_NOTE_2_APPLIED_TO_BASE_PLUS_FOOT_CLUSTER" in result.warnings


def test_pcgn_note2_triisap_applies_after_note3_foot_series_selection():
    # ម is weak and ហ is non-weak; Note 3 selects the foot's â series.
    # Note 2 TRIISAP then changes the whole cluster to ô.
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ម៊្ហ"))
    assert result.series_before_shifter == "â"
    assert result.series == "ô"
    assert result.basis == "SUBSCRIPT"
    assert result.shifter_effect == "TRIISAP_A_TO_O"


def test_pcgn_note2_muusikatoan_applies_to_base_plus_weak_foot_cluster():
    # A weak foot does not override a non-weak base under Note 3.
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("គ៉្ង"))
    assert result.series_before_shifter == "ô"
    assert result.series == "â"
    assert result.basis == "BASE"
    assert result.shifter_effect == "MUUSIKATOAN_O_TO_A"


def test_pcgn_note2_shifters_abstain_on_wrong_direction_position_and_ba_exceptions():
    for source in ("ក៉", "គ៊", "ហា៊", "ហ៊៉", "ថ៉្ម", "ប៊្ក", "ប៉្ក"):
        result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk(source))
        assert result.status == "UNRESOLVED"
        assert result.series is None
        assert result.shifter_effect is None



def test_pcgn_note3_ba_with_triisap_is_p_in_a_series():
    # Note 3 explicitly overrides the ordinary ô-series base value for ប
    # with TRIISAP: the consonant is romanized p in the â-series.
    result = resolve_pcgn_series(analyze_pcgn_orthographic_chunk("ប៊"))
    assert result.status == "RESOLVED"
    assert result.series_before_shifter == "ô"
    assert result.series == "â"
    assert result.basis == "BASE"
    assert result.onset_exception == "BA_WITH_TRIISAP_P_IN_A_SERIES"
    assert result.shifter_effect == "BA_TRIISAP_P_IN_A"
    assert "PCGN_NOTE_3_BA_TRIISAP_P_IN_A_EXCEPTION" in result.warnings
    assert result.source_locator == "PCGN 1972, Notes 2–3 (pp. 2–3)"


def test_pcgn_ba_triisap_schema_enum_covers_the_documented_exception():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-series-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert "BA_WITH_TRIISAP_P_IN_A_SERIES" in schema["properties"]["onset_exception"]["enum"]
    assert "BA_TRIISAP_P_IN_A" in schema["properties"]["shifter_effect"]["enum"]
