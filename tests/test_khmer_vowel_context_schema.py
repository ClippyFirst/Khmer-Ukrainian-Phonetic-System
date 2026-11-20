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
