"""Conservative parser for one Khmer orthographic syllable.

The parser implements the component-order production in Unicode 18.0,
Chapter 16 §16.4. It deliberately does not segment a multi-base input into
syllables: that requires additional orthographic/lexical evidence.
"""
from dataclasses import dataclass
from typing import Literal

from .orthographic_structure import KhmerOrthographicScan, scan_orthographic_components

Status = Literal["PARSED", "INVALID_ORDER", "INVALID_OR_UNSUPPORTED", "EVIDENCE_LIMITED"]


@dataclass(frozen=True)
class KhmerOrthographicSyllable:
    source_text: str
    status: Status
    component_spans: tuple[tuple[int, int], ...]
    notes: tuple[str, ...] = ()
    grammar: str = "B {R | C} {S {R}}* {{Z} V} {O} {S}"

    def to_dict(self) -> dict:
        return {
            "schema": "khmer-orthographic-syllable/v1",
            "source_text": self.source_text,
            "offset_unit": "unicode_code_point",
            "status": self.status,
            "grammar": self.grammar,
            "component_spans": [list(span) for span in self.component_spans],
            "notes": list(self.notes),
        }


def parse_orthographic_syllable(text: str) -> KhmerOrthographicSyllable:
    """Validate one supplied span against Unicode 18's Khmer component order.

    A ZWNJ immediately before a shifter is accepted as the documented
    shaping exception. Multiple un-subscripted bases are not split or assigned
    coda/syllable roles; the caller must provide a narrower span or evidence.
    """
    scan: KhmerOrthographicScan = scan_orthographic_components(text)
    spans = scan.component_spans
    if scan.status == "INVALID_OR_UNSUPPORTED":
        return KhmerOrthographicSyllable(text, "INVALID_OR_UNSUPPORTED", spans, scan.notes)

    items = scan.components
    bases = [item for item in items if item.role == "BASE"]
    if len(bases) != 1:
        return KhmerOrthographicSyllable(
            text, "EVIDENCE_LIMITED", spans,
            ("The supplied span contains multiple un-subscripted bases or no unique base; "
             "Unicode component order does not determine syllable boundaries or coda roles.",),
        )

    roles = [item.role for item in items]
    i = 0
    if not roles or roles[0] != "BASE":
        return KhmerOrthographicSyllable(text, "INVALID_ORDER", spans, ("A syllable must begin with B (base character).",))
    i += 1

    # B {R | C}; Unicode §16.4 also documents ZWNJ immediately before C
    # as a shaping exception, so retain that exact, narrowly-scoped variant.
    if i < len(items) and items[i].role == "FORMAT_CONTROL":
        if items[i].text != "\u200c" or i + 1 >= len(items) or items[i + 1].role != "SHIFTER":
            return KhmerOrthographicSyllable(text, "INVALID_ORDER", spans, ("A format control is only accepted before V, or as the documented ZWNJ-before-shifter exception.",))
        i += 1
        i += 1
    elif i < len(items) and roles[i] in {"ROBAT", "SHIFTER"}:
        i += 1

    # {S {R}}*
    while i < len(items) and roles[i] == "SUBSCRIPT":
        i += 1
        if i < len(items) and roles[i] == "ROBAT":
            i += 1

    # {{Z} V}
    if i < len(items) and roles[i] == "FORMAT_CONTROL":
        if i + 1 >= len(items) or roles[i + 1] != "VOWEL":
            return KhmerOrthographicSyllable(text, "INVALID_ORDER", spans, ("Z must immediately precede a dependent vowel V in this production.",))
        i += 1
        i += 1
    elif i < len(items) and roles[i] == "VOWEL":
        i += 1

    # {O} {S}
    if i < len(items) and roles[i] == "OTHER_SIGN":
        i += 1
    if i < len(items) and roles[i] == "SUBSCRIPT":
        i += 1

    if i != len(items):
        unexpected = items[i]
        return KhmerOrthographicSyllable(
            text, "INVALID_ORDER", spans,
            (f"Component {unexpected.role} at code-point offset {unexpected.start} is not permitted at this position by Unicode 18 §16.4.",),
        )

    return KhmerOrthographicSyllable(text, "PARSED", spans, ("Single-base component order conforms to the Unicode 18 §16.4 production; this does not establish pronunciation or word boundaries.",))
