"""Command-line interface for the Khmer IPA-first analysis engine."""
from __future__ import annotations

import argparse
import json

from .parser import analyze as analyze_structure
from .rule_engine import RuleBasedKhmerEngine


def _canonical_ipa(result: dict) -> str | None:
    value = result.get("ipa")
    if isinstance(value, str) and value and not value.startswith("⟦"):
        return value
    return None


def _canonical_ukrainian(result: dict) -> str | None:
    value = result.get("ukrainian")
    if isinstance(value, str) and value and not value.startswith("⟦"):
        return value
    return None


def _display_ipa(result: dict) -> str:
    canonical = _canonical_ipa(result)
    if canonical is not None:
        return canonical
    provisional = result.get("provisional_ipa")
    if provisional:
        return provisional + "???"
    return "???"


def _display_ukrainian(result: dict) -> str:
    canonical = _canonical_ukrainian(result)
    if canonical is not None:
        return canonical
    provisional = result.get("provisional_ukrainian")
    if provisional:
        return provisional
    return "???"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="khmer-ua")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("analyze", "syllables", "ipa", "transliterate", "explain"):
        command = sub.add_parser(name)
        command.add_argument("text")
    for name in ("validate", "generate", "benchmark", "coverage"):
        sub.add_parser(name)
    args = parser.parse_args(argv)

    if args.command == "syllables":
        structure = analyze_structure(args.text)
        print(json.dumps(structure.syllables, ensure_ascii=False, indent=2, default=str))
        return

    if args.command in {"analyze", "ipa", "transliterate", "explain"}:
        result = RuleBasedKhmerEngine().analyze(args.text)
        if args.command == "ipa":
            print(_display_ipa(result))
        elif args.command == "transliterate":
            print(_display_ukrainian(result))
        else:
            # The JSON envelope includes the typed IPA segments, confidence,
            # provenance, uncertainty and the IPA-derived target result.
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        return

    print(json.dumps({
        "command": args.command,
        "status": "IMPLEMENTATION_REQUIRED",
        "reason": "No empirical corpus or complete generators are claimed yet.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
