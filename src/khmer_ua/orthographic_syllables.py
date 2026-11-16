"""Unicode 18 Khmer orthographic-syllable parsing with a packed parse forest."""
from dataclasses import dataclass
from math import prod
from typing import Literal

from .orthographic_structure import KhmerOrthographicComponent, scan_orthographic_components

GRAMMAR_PROFILE = "unicode-18.0.0-ch16.4-plus-ch16.4.1-shifter-control"
MAX_SEGMENTATION_ALTERNATIVES = 128
ParseStatus = Literal["PARSED", "AMBIGUOUS", "EVIDENCE_LIMITED", "INVALID_OR_UNSUPPORTED"]


@dataclass(frozen=True)
class KhmerOrthographicGrammarAlternative:
    grammar_roles: tuple[str, ...]
    grammar_extensions: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "grammar_roles": list(self.grammar_roles),
            "grammar_extensions": list(self.grammar_extensions),
        }


@dataclass(frozen=True)
class KhmerOrthographicSyllable:
    start: int
    end: int
    source_text: str
    components: tuple[KhmerOrthographicComponent, ...]
    grammar_alternatives: tuple[KhmerOrthographicGrammarAlternative, ...]

    @property
    def grammar_roles(self) -> tuple[str, ...] | None:
        return self.grammar_alternatives[0].grammar_roles if len(self.grammar_alternatives) == 1 else None

    @property
    def grammar_extensions(self) -> tuple[str, ...] | None:
        return self.grammar_alternatives[0].grammar_extensions if len(self.grammar_alternatives) == 1 else None

    def to_dict(self) -> dict:
        return {
            "start": self.start,
            "end": self.end,
            "source_text": self.source_text,
            "components": [
                {"role": item.role, "text": item.text, "start": item.start, "end": item.end,
                 "codepoints": list(item.codepoints), "status": item.status}
                for item in self.components
            ],
            "grammar_roles": list(self.grammar_roles) if self.grammar_roles is not None else None,
            "grammar_extensions": list(self.grammar_extensions) if self.grammar_extensions is not None else None,
            "grammar_alternatives": [item.to_dict() for item in self.grammar_alternatives],
        }


@dataclass(frozen=True)
class KhmerOrthographicParseAlternative:
    syllables: tuple[KhmerOrthographicSyllable, ...]

    def to_dict(self) -> dict:
        return {"syllables": [item.to_dict() for item in self.syllables]}


@dataclass(frozen=True)
class KhmerOrthographicSyllableParse:
    source_text: str
    status: ParseStatus
    alternatives: tuple[KhmerOrthographicParseAlternative, ...]
    derivation_count: int
    notes: tuple[str, ...] = ()

    @property
    def syllables(self) -> tuple[KhmerOrthographicSyllable, ...] | None:
        if self.status != "PARSED" or len(self.alternatives) != 1:
            return None
        return self.alternatives[0].syllables

    def to_dict(self) -> dict:
        return {
            "schema": "khmer-orthographic-syllables/v1",
            "grammar_profile": GRAMMAR_PROFILE,
            "source_text": self.source_text,
            "offset_unit": "unicode_code_point",
            "status": self.status,
            "parse_count": str(self.derivation_count),
            "segmentation_count": len(self.alternatives),
            "syllables": [item.to_dict() for item in self.syllables] if self.syllables is not None else None,
            "alternatives": [item.to_dict() for item in self.alternatives],
            "notes": list(self.notes),
        }


def _role(components: tuple[KhmerOrthographicComponent, ...], index: int) -> str | None:
    return components[index].role if index < len(components) else None


def _syllable_matches(
    components: tuple[KhmerOrthographicComponent, ...], start: int
) -> tuple[tuple[int, KhmerOrthographicGrammarAlternative], ...]:
    """Match B {R | C} {S {R}}* {{Z} V} {O} {S}.

    Local grammar-role alternatives are returned separately so the caller can
    pack them per syllable instead of expanding their Cartesian product across
    an entire input. The §16.4.1 ZWNJ-before-shifter exception is traceable.
    """
    if _role(components, start) != "BASE":
        return ()
    states: set[tuple[int, tuple[str, ...], tuple[str, ...]]] = {
        (start + 1, (), ("BASE",))
    }

    # {R | C}
    for index, extensions, grammar_roles in tuple(states):
        role = _role(components, index)
        if role == "ROBAT":
            states.add((index + 1, extensions, grammar_roles + ("INITIAL_ROBAT",)))
        elif role == "SHIFTER":
            states.add((index + 1, extensions, grammar_roles + ("INITIAL_SHIFTER",)))
        if (
            role == "FORMAT_CONTROL"
            and components[index].text == "\u200c"
            and _role(components, index + 1) == "SHIFTER"
        ):
            states.add((
                index + 2,
                extensions + ("U+200C-before-shifter (§16.4.1 textual exception)",),
                grammar_roles + ("SHIFTER_CONTROL", "INITIAL_SHIFTER"),
            ))

    # {S {R}}*
    queue = list(states)
    while queue:
        index, extensions, grammar_roles = queue.pop()
        if _role(components, index) != "SUBSCRIPT":
            continue
        next_index = index + 1
        next_roles = grammar_roles + ("SUBSCRIPT_CLUSTER",)
        if _role(components, next_index) == "ROBAT":
            next_index += 1
            next_roles += ("ROBAT_AFTER_SUBSCRIPT",)
        state = (next_index, extensions, next_roles)
        if state not in states:
            states.add(state)
            queue.append(state)

    # {{Z} V}
    after_vowel = set(states)
    for index, extensions, grammar_roles in states:
        if _role(components, index) == "VOWEL":
            after_vowel.add((index + 1, extensions, grammar_roles + ("DEPENDENT_VOWEL",)))
        elif _role(components, index) == "FORMAT_CONTROL" and _role(components, index + 1) == "VOWEL":
            after_vowel.add((
                index + 2, extensions,
                grammar_roles + ("JOIN_CONTROL_BEFORE_VOWEL", "DEPENDENT_VOWEL"),
            ))

    # {O} {S}
    after_other = set(after_vowel)
    for index, extensions, grammar_roles in after_vowel:
        if _role(components, index) == "OTHER_SIGN":
            after_other.add((index + 1, extensions, grammar_roles + ("OTHER_SIGN",)))
    completed = set(after_other)
    for index, extensions, grammar_roles in after_other:
        if _role(components, index) == "SUBSCRIPT":
            completed.add((index + 1, extensions, grammar_roles + ("TRAILING_SUBSCRIPT",)))

    matches = {
        (end, KhmerOrthographicGrammarAlternative(grammar_roles, extensions))
        for end, extensions, grammar_roles in completed
    }
    return tuple(sorted(matches, key=lambda item: (item[0], item[1].grammar_roles, item[1].grammar_extensions)))


def parse_orthographic_syllables(text: str) -> KhmerOrthographicSyllableParse:
    """Return a packed forest of all complete Unicode 18 parses.

    Boundary alternatives are retained at the top level. Grammar-role
    alternatives are packed per syllable, avoiding exponential expansion when
    independent syllables each contain the BNF's repeated/final-S ambiguity.
    No normalization, phonological syllabification, or word segmentation occurs.
    """
    scan = scan_orthographic_components(text)
    components = scan.components
    if not text or scan.status == "INVALID_OR_UNSUPPORTED":
        return KhmerOrthographicSyllableParse(
            text, "INVALID_OR_UNSUPPORTED", (), 0,
            scan.notes or ("No complete Khmer orthographic structure was found.",)
        )
    if not components or components[0].role != "BASE":
        return KhmerOrthographicSyllableParse(
            text, "INVALID_OR_UNSUPPORTED", (), 0,
            ("A Unicode 18 orthographic syllable must begin with a base character.",)
        )

    size = len(components)
    paths_by_index: dict[int, list[tuple[tuple[int, int, tuple[KhmerOrthographicGrammarAlternative, ...]], ...]]] = {size: [()]}
    for start in range(size - 1, -1, -1):
        if _role(components, start) != "BASE":
            continue
        matches_by_end: dict[int, set[KhmerOrthographicGrammarAlternative]] = {}
        for end, grammar_alternative in _syllable_matches(components, start):
            if end != size and _role(components, end) != "BASE":
                continue
            matches_by_end.setdefault(end, set()).add(grammar_alternative)

        paths = []
        for end, grammar_alternatives in sorted(matches_by_end.items()):
            packed = tuple(sorted(grammar_alternatives, key=lambda item: (item.grammar_roles, item.grammar_extensions)))
            for remainder in paths_by_index.get(end, ()):
                paths.append(((start, end, packed),) + remainder)
                if len(paths) > MAX_SEGMENTATION_ALTERNATIVES:
                    break
            if len(paths) > MAX_SEGMENTATION_ALTERNATIVES:
                break
        if paths:
            paths_by_index[start] = list(dict.fromkeys(paths))

    paths = paths_by_index.get(0, [])
    if not paths:
        return KhmerOrthographicSyllableParse(
            text, "EVIDENCE_LIMITED", (), 0,
            ("Recognized components do not form a complete sequence under the Unicode 18 §16.4 ordering formula; no boundary was guessed.",)
        )
    if len(paths) > MAX_SEGMENTATION_ALTERNATIVES:
        return KhmerOrthographicSyllableParse(
            text, "EVIDENCE_LIMITED", (), 0,
            ("The number of distinct syllable-boundary segmentations exceeded the configured limit.",)
        )

    alternatives = []
    derivation_count = 0
    for path in paths:
        syllables = []
        path_derivations = 1
        for start_index, end_index, grammar_alternatives in path:
            selected = components[start_index:end_index]
            start, end = selected[0].start, selected[-1].end
            syllables.append(KhmerOrthographicSyllable(
                start, end, text[start:end], selected, grammar_alternatives
            ))
            path_derivations *= len(grammar_alternatives)
        derivation_count += path_derivations
        alternatives.append(KhmerOrthographicParseAlternative(tuple(syllables)))

    status: ParseStatus = "AMBIGUOUS" if derivation_count > 1 else "PARSED"
    return KhmerOrthographicSyllableParse(
        text, status, tuple(alternatives), derivation_count,
        ("Orthographic syllables are not phonological syllables or lexical words.",
         "All boundary paths and local grammar-role alternatives are retained in a packed forest; no best parse is selected."),
    )
