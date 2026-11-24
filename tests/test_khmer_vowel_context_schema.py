import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "data" / "khmer" / "vowel-context-register.json"
SCHEMA = ROOT / "schemas" / "khmer-vowel-context-register.schema.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_contextual_vowel_register_matches_its_schema():
    schema = load_json(SCHEMA)
    register = load_json(REGISTER)

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(register), key=lambda error: list(error.absolute_path))
    assert not errors, "\n".join(
        f"{list(error.absolute_path)}: {error.message}" for error in errors
    )


def test_contextual_vowel_evidence_references_are_resolvable_and_not_gold():
    register = load_json(REGISTER)
    source_ids = set(register["sources"])
    case_ids = [case["id"] for case in register["cases"]]

    assert len(case_ids) == len(set(case_ids)), "case IDs must be unique"
    for case in register["cases"]:
        assert case["ipa_source"] in source_ids, case["id"]
        assert case["evidence_level"] == case["status"], case["id"]
        assert case["status"] != "ADJUDICATED_GOLD", case["id"]
        for alternative in case.get("alternatives", []):
            source_id = alternative.get("source")
            if source_id is not None:
                assert source_id in source_ids, (case["id"], source_id)

        if case["status"] == "CONFLICTING_SOURCE_ANALYSES":
            assert case["ipa"] is None, case["id"]
            assert case["ukrainian_adaptation"] is None, case["id"]
            assert case["ukrainian_status"] == "NOT_ESTABLISHED", case["id"]


def test_context_dimensions_have_resolvable_sources_and_explicit_boundaries():
    register = load_json(REGISTER)
    source_ids = set(register["sources"])
    dimensions = register["context_dimensions"]
    dimension_ids = [item["id"] for item in dimensions]

    assert len(dimensions) >= 1
    assert len(dimension_ids) == len(set(dimension_ids))
    for item in dimensions:
        assert item["source_ids"], item["id"]
        assert set(item["source_ids"]) <= source_ids, item["id"]
        assert item["environment"], item["id"]
        assert item["locator"], item["id"]
        assert item["profile_scope"], item["id"]
        assert item["implementation"], item["id"]
        # Context findings are not lexical gold or permission to infer a
        # deterministic output from an incomplete cross-product.
        assert len(item["implementation"]) >= 20, item["id"]


def test_source_attested_coda_examples_without_word_level_ipa_stay_unresolved():
    register = load_json(REGISTER)
    cases = {case["id"]: case for case in register["cases"]}

    for case_id in ("KHV-010", "KHV-011", "KHV-012", "KHV-013", "KHV-014"):
        case = cases[case_id]
        assert case["ipa_source"] == "r12a-orthography"
        assert case["status"] == "SOURCE_ATTESTED_NOT_GOLD"
        assert case["ipa"] is None
        assert case["ukrainian_adaptation"] is None
        assert case["ukrainian_status"] == "NOT_ESTABLISHED"
        assert case["source_locator"]
        assert case["limitations"]


def test_source_attested_rhyme_patterns_preserve_class_and_coda_conditioning():
    register = load_json(REGISTER)
    source_ids = set(register["sources"])
    patterns = register["coda_pattern_observations"]
    pattern_ids = [item["id"] for item in patterns]

    assert len(pattern_ids) == len(set(pattern_ids))
    assert len(patterns) == 15
    by_id = {item["id"]: item for item in patterns}
    assert by_id["REAHMUK-A-17C1"]["source_ipa"] == "/eh/"
    assert by_id["REAHMUK-O-17C1"]["source_ipa"] == "/ih/"
    assert by_id["REAHMUK-O-17C4"]["source_ipa"] == "/uə̆h/"
    assert by_id["REAHMUK-O-BARE"]["source_ipa"] == "/eə̆h/"
    assert by_id["SAMYOK-O-VELAR"]["source_ipa"] == "/eə̆/"
    assert by_id["SAMYOK-O-NONVELAR"]["source_ipa"] == "/oə̆/"

    for item in patterns:
        assert item["source_id"] in source_ids, item["id"]
        assert item["source_locator"], item["id"]
        assert item["profile_scope"], item["id"]
        assert item["evidence_status"] == "SOURCE_ATTESTED_NOT_GOLD"
        assert item["ukrainian_adaptation"] is None
        assert item["ukrainian_status"] == "NOT_ESTABLISHED"
        assert item["limitations"], item["id"]
