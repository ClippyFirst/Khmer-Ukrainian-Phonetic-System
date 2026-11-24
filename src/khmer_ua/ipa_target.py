"""Single typed IPA → Ukrainian target adapter.

The adapter consumes only TypedPhoneticResult. It never inspects Khmer
orthography, grapheme positions, or romanization.
"""
from __future__ import annotations

from .ipa_result import TypedPhoneticResult
from .practical import map_ipa_string


def adapt_phonetic_result(
    result: TypedPhoneticResult,
    *,
    allow_uncertain: bool = False,
) -> str | None:
    """Adapt typed IPA; preserve provisional status and unresolved regions."""
    if not isinstance(result, TypedPhoneticResult):
        raise TypeError("Ukrainian adaptation requires a TypedPhoneticResult")

    if result.status == "UNRESOLVED":
        return "???" if not any(segment.kind != "unknown" for segment in result.segments) else None

    if result.status == "PROVISIONAL":
        output: list[str] = []
        known_run: list[str] = []
        unknown_run = False

        def flush_known() -> None:
            nonlocal unknown_run
            if not known_run:
                return
            raw = "".join(known_run)
            known_run.clear()
            mapped, unsupported = map_ipa_string(raw)
            if unsupported is not None or mapped is None:
                if not unknown_run:
                    output.append("???")
                unknown_run = True
            else:
                output.append(mapped)
                unknown_run = False

        for segment in result.segments:
            if segment.kind in {"unknown", "tone"}:
                flush_known()
                if not unknown_run:
                    output.append("???")
                unknown_run = True
                continue
            if segment.certainty != "PROVISIONAL":
                return None
            known_run.append(segment.ipa)
        flush_known()
        return "".join(output) or "???"

    if result.status == "UNCERTAIN" and not allow_uncertain:
        return None
    if result.status not in {"SUPPORTED", "UNCERTAIN"} or not result.segments:
        return None
    if any(segment.kind in {"unknown", "tone"} for segment in result.segments):
        return None
    raw = "".join(segment.ipa for segment in result.segments)
    mapped, unsupported = map_ipa_string(raw)
    return mapped if unsupported is None else None
