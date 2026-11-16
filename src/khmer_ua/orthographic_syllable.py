"""Conservative Unicode 18 Khmer orthographic-syllable parsing.

The component scanner remains the sole Unicode inventory. This module applies
the §16.4 component-order production and returns a parse forest; it does not
select phonological syllables, words, pronunciation, IPA, or Ukrainian output.
"""
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

from .orthographic_structure import KhmerOrthographicScan, scan_orthographic_components

Status = Literal["PARSED", "AMBIGUOUS", "EVIDENCE_LIMITED", "INVALID_ORDER", "INVALID_OR_UNSUPPORTED"]
GRAMMAR = "B {R | C} {S {R}}* {{Z} V} {O} {S}"
MAX_PARSE_ALTERNATIVES = 256


@dataclass(frozen=True)
class KhmerOrthographicSyllable:
    source_text: str
    status: Status
    component_spans: tuple[tuple[int, int], ...]
    notes: tuple[str, ...] = ()
    grammar: str = GRAMMAR

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


@dataclass(frozen=True)
class KhmerOrthographicParseForest:
    source_text: str
    status: Status
    alternatives: tuple[tuple[dict, ...], ...]
    boundary_alternatives: tuple[tuple[tuple[int, int], ...], ...]
    rejected_spans: tuple[dict, ...]
    notes: tuple[str, ...] = ()
    truncated: bool = False
    grammar: str = GRAMMAR

    def to_dict(self) -> dict:
        return {
            "schema": "khmer-orthographic-parse-forest/v1",
            "source_text": self.source_text,
            "offset_unit": "unicode_code_point",
            "status": self.status,
            "grammar": self.grammar,
            "alternatives": [
                {"syllables": list(path)} for path in self.alternatives
            ],
            "boundary_alternatives": [
                [list(span) for span in path] for path in self.boundary_alternatives
            ],
            "selected_alternative": None,
            "rejected_spans": list(self.rejected_spans),
            "notes": list(self.notes),
            "truncated": self.truncated,
        }


def _ref(item) -> list[int]:
    return [item.start, item.end]


def _syllable_matches(items, start: int):
    """Return every complete §16.4 derivation beginning at component start."""
    if start >= len(items) or items[start].role != "BASE":
        return []
    matches = []

    # B {R | C}; Unicode also documents the ZWNJ-before-shifter shaping case.
    initial_options = [(start + 1, None)]
    if start + 1 < len(items) and items[start + 1].role in {"ROBAT", "SHIFTER"}:
        initial_options.append((start + 2, _ref(items[start + 1])))
    elif (
        start + 2 < len(items)
        and items[start + 1].role == "FORMAT_CONTROL"
        and items[start + 1].text == "\u200c"
        and items[start + 2].role == "SHIFTER"
    ):
        initial_options.append((start + 3, [_ref(items[start + 1]), _ref(items[start + 2])]))

    for after_initial, initial in initial_options:
        # {S {R}}*: retain both loop-vs-final-S derivations in the forest.
        chain_states = [(after_initial, ())]
        cursor = after_initial
        chain = []
        while cursor < len(items) and items[cursor].role == "SUBSCRIPT":
            sub = _ref(items[cursor])
            cursor += 1
            robat = None
            if cursor < len(items) and items[cursor].role == "ROBAT":
                robat = _ref(items[cursor])
                cursor += 1
            chain.append({"subscript": sub, "robat": robat})
            chain_states.append((cursor, tuple(chain)))

        for after_chain, subscript_chain in chain_states:
            # {{Z} V}
            vowel_options = [(after_chain, None)]
            if after_chain < len(items) and items[after_chain].role == "VOWEL":
                vowel_options.append((after_chain + 1, {"format_control": None, "vowel": _ref(items[after_chain])}))
            if (
                after_chain + 1 < len(items)
                and items[after_chain].role == "FORMAT_CONTROL"
                and items[after_chain + 1].role == "VOWEL"
            ):
                vowel_options.append((
                    after_chain + 2,
                    {"format_control": _ref(items[after_chain]), "vowel": _ref(items[after_chain + 1])},
                ))

            for after_vowel, vowel in vowel_options:
                # {O} {S}
                other_options = [(after_vowel, None)]
                if after_vowel < len(items) and items[after_vowel].role == "OTHER_SIGN":
                    other_options.append((after_vowel + 1, _ref(items[after_vowel])))
                for after_other, other in other_options:
                    final_options = [(after_other, None)]
                    if after_other < len(items) and items[after_other].role == "SUBSCRIPT":
                        final_options.append((after_other + 1, _ref(items[after_other])))
                    for end, final_subscript in final_options:
                        if end == len(items) or items[end].role == "BASE":
                            span_end = items[end - 1].end
                            matches.append({
                                "span": [items[start].start, span_end],
                                "base": _ref(items[start]),
                                "initial_robat_or_shifter": initial,
                                "subscript_chain": list(subscript_chain),
                                "vowel": vowel,
                                "other_sign": other,
                                "final_subscript": final_subscript,
                            })

    # Stable de-duplication without collapsing distinct parse-tree assignments.
    unique = []
    seen = set()
    for item in matches:
        key = repr(item)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique



def _first_rejected_component(items, start: int):
    """Locate the first token left outside the ordered production for diagnostics."""
    i = start + 1
    if i < len(items) and items[i].role == "FORMAT_CONTROL":
        if i + 1 < len(items) and items[i].text == "\u200c" and items[i + 1].role == "SHIFTER":
            i += 2
        elif i + 1 < len(items) and items[i + 1].role == "VOWEL":
            i += 2
        else:
            return items[i]
    elif i < len(items) and items[i].role in {"ROBAT", "SHIFTER"}:
        i += 1
    while i < len(items) and items[i].role == "SUBSCRIPT":
        i += 1
        if i < len(items) and items[i].role == "ROBAT":
            i += 1
    if i < len(items) and items[i].role == "FORMAT_CONTROL":
        if i + 1 < len(items) and items[i + 1].role == "VOWEL":
            i += 2
        else:
            return items[i]
    elif i < len(items) and items[i].role == "VOWEL":
        i += 1
    if i < len(items) and items[i].role == "OTHER_SIGN":
        i += 1
    if i < len(items) and items[i].role == "SUBSCRIPT":
        i += 1
    return items[i] if i < len(items) else items[-1]


def parse_orthographic_sequence(text: str) -> KhmerOrthographicParseForest:
    """Parse a continuous source span and retain every viable BNF parse path.

    A BASE following a completed production is a candidate next-syllable
    onset. If the scanner marks its base role ambiguous, the candidate forest
    is returned as EVIDENCE_LIMITED rather than selected as a syllabification.
    """
    scan: KhmerOrthographicScan = scan_orthographic_components(text)
    if scan.status == "INVALID_OR_UNSUPPORTED":
        return KhmerOrthographicParseForest(
            text, "INVALID_OR_UNSUPPORTED", (), (), (), scan.notes
        )
    items = scan.components
    if not items or items[0].role != "BASE":
        return KhmerOrthographicParseForest(
            text, "INVALID_ORDER", (), (), ({"start": 0, "end": len(text), "reason": "A sequence must begin with B (base character)."},),
            ("The first component is not a modeled base character.",),
        )

    rejected = []
    truncated = False

    @lru_cache(maxsize=None)
    def parse_from(position: int):
        nonlocal truncated
        if position == len(items):
            return ((),)
        paths = []
        matches = _syllable_matches(items, position)
        if not matches:
            item = _first_rejected_component(items, position)
            rejected.append({
                "start": item.start,
                "end": item.end,
                "reason": f"{item.role} at this position prevents a complete Unicode 18 §16.4 production.",
            })
            return ()
        for match in matches:
            end_component = next(
                (i for i, item in enumerate(items) if item.start == match["span"][1]),
                len(items),
            )
            if end_component == len(items):
                tails = ((),)
            elif items[end_component].role == "BASE":
                tails = parse_from(end_component)
            else:
                item = items[end_component]
                rejected.append({
                    "start": item.start,
                    "end": item.end,
                    "reason": f"{item.role} remains after a complete production and cannot begin the next one.",
                })
                tails = ()
            for tail in tails:
                if len(paths) >= MAX_PARSE_ALTERNATIVES:
                    truncated = True
                    break
                paths.append((match,) + tail)
            if truncated:
                break
        return tuple(paths)

    alternatives = parse_from(0)
    boundary_paths = []
    for path in alternatives:
        spans = tuple(tuple(syllable["span"]) for syllable in path)
        if spans not in boundary_paths:
            boundary_paths.append(spans)

    ambiguous_components = [item for item in items if item.status == "AMBIGUOUS_BASE_ROLE"]
    ambiguous_base = bool(ambiguous_components)
    for item in ambiguous_components:
        rejected.append({
            "start": item.start,
            "end": item.end,
            "reason": "Potential coda-versus-next-syllable base role is not determined by Unicode 18 §16.4; this candidate boundary is not selected.",
        })
    if truncated:
        status: Status = "EVIDENCE_LIMITED"
        notes = ("Parse forest exceeded the configured alternative cap; no alternative was selected.",)
    elif not alternatives:
        status = "INVALID_ORDER"
        notes = ("No complete parse of the supplied component sequence satisfies Unicode 18 §16.4.",)
    elif ambiguous_base:
        status = "EVIDENCE_LIMITED"
        notes = ("The scanner marks one or more un-subscripted bases as role-ambiguous; candidate parses are retained without selecting syllable boundaries.",)
    elif len(boundary_paths) > 1:
        status = "AMBIGUOUS"
        notes = ("Multiple complete boundary segmentations satisfy the component-order grammar; all are retained.",)
    else:
        status = "PARSED"
        notes = ("A complete component-order parse was found. These are orthographic candidates, not phonological syllables or word boundaries.",)

    return KhmerOrthographicParseForest(
        text, status, tuple(alternatives), tuple(boundary_paths),
        tuple(rejected), tuple(notes), truncated,
    )


def parse_orthographic_syllable(text: str) -> KhmerOrthographicSyllable:
    """Validate a single supplied span against Unicode 18 §16.4."""
    scan: KhmerOrthographicScan = scan_orthographic_components(text)
    spans = scan.component_spans
    if scan.status == "INVALID_OR_UNSUPPORTED":
        return KhmerOrthographicSyllable(text, "INVALID_OR_UNSUPPORTED", spans, scan.notes)
    bases = [item for item in scan.components if item.role == "BASE"]
    if len(bases) != 1:
        return KhmerOrthographicSyllable(
            text, "EVIDENCE_LIMITED", spans,
            ("The supplied span contains multiple un-subscripted bases or no unique base; candidate syllable boundaries are not selected.",),
        )
    forest = parse_orthographic_sequence(text)
    if not forest.alternatives:
        return KhmerOrthographicSyllable(text, "INVALID_ORDER", spans, forest.notes)
    if forest.status == "EVIDENCE_LIMITED":
        return KhmerOrthographicSyllable(text, "EVIDENCE_LIMITED", spans, forest.notes)
    return KhmerOrthographicSyllable(text, "PARSED", spans, forest.notes)
