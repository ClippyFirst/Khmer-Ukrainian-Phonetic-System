"""Unicode 18 Khmer orthographic-syllable parsing.

This module parses Unicode Standard 18.0.0 Chapter 16 §16.4. It reuses the
lossless component scanner and never derives phonological syllables, words,
pronunciation, IPA, or Ukrainian output.
"""
from dataclasses import dataclass
from typing import Literal

from .orthographic_structure import KhmerOrthographicComponent, scan_orthographic_components

GRAMMAR_PROFILE = "unicode-18.0.0-ch16.4-plus-ch16.4.1-shifter-control"
MAX_PARSE_ALTERNATIVES = 128
ParseStatus = Literal["PARSED", "AMBIGUOUS", "EVIDENCE_LIMITED", "INVALID_OR_UNSUPPORTED"]


@dataclass(frozen=True)
class KhmerOrthographicSyllable:
    start: int
    end: int
    source_text: str
    components: tuple[KhmerOrthographicComponent, ...]
    grammar_roles: tuple[str, ...]
    grammar_extensions: tuple[str, ...] = ()

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
            "grammar_roles": list(self.grammar_roles),
            "grammar_extensions": list(self.grammar_extensions),
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
    notes: tuple[str, ...] = ()
    rejected_spans: tuple[dict, ...] = ()

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
            "parse_count": len(self.alternatives),
            "syllables": [item.to_dict() for item in self.syllables] if self.syllables is not None else None,
            "alternatives": [item.to_dict() for item in self.alternatives],
            "notes": list(self.notes),
            "rejected_spans": list(self.rejected_spans),
        }


def _role(components: tuple[KhmerOrthographicComponent, ...], index: int) -> str | None:
    return components[index].role if index < len(components) else None


def _syllable_matches(
    components: tuple[KhmerOrthographicComponent, ...], start: int
) -> tuple[tuple[int, tuple[str, ...], tuple[str, ...]], ...]:
    """Match B {R | C} {S {R}}* {{Z} V} {O} {S}.

    The same SUBSCRIPT terminal can be assigned to the repeated S production
    or the final S production. Both grammar trees are retained. Unicode 18
    §16.4.1's ZWNJ-before-shifter exception is also explicitly traced.
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

    # {S {R}}*: retain every number of repeated S components and their roles.
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

    # {O}
    after_other = set(after_vowel)
    for index, extensions, grammar_roles in after_vowel:
        if _role(components, index) == "OTHER_SIGN":
            after_other.add((index + 1, extensions, grammar_roles + ("OTHER_SIGN",)))

    # {S}: this is a distinct production from S in the repeated group above.
    completed = set(after_other)
    for index, extensions, grammar_roles in after_other:
        if _role(components, index) == "SUBSCRIPT":
            completed.add((index + 1, extensions, grammar_roles + ("TRAILING_SUBSCRIPT",)))

    return tuple(sorted(completed, key=lambda item: (item[0], item[2], item[1])))



def _rejected_spans(
    components: tuple[KhmerOrthographicComponent, ...],
) -> tuple[dict, ...]:
    """Locate the first component that prevents any complete grammar path."""
    size = len(components)
    for start, component in enumerate(components):
        if component.role != "BASE":
            continue
        matches = _syllable_matches(components, start)
        viable_next = [
            end for end, _extensions, _grammar_roles in matches
            if end == size or _role(components, end) == "BASE"
        ]
        if viable_next:
            continue
        invalid_ends = [
            end for end, _extensions, _grammar_roles in matches
            if end < size and _role(components, end) != "BASE"
        ]
        if invalid_ends:
            rejected = components[max(invalid_ends)]
            return ({
                "start": rejected.start,
                "end": rejected.end,
                "reason": (
                    f"{rejected.role} at this position prevents a complete "
                    "Unicode 18 §16.4 component-order production."
                ),
            },)
    unsupported = [
        item for item in components
        if item.status in {"MALFORMED_COENG", "UNMODELED_CHARACTER"}
    ]
    return tuple({
        "start": item.start,
        "end": item.end,
        "reason": f"{item.status} component {item.text!r} is outside the modeled Unicode 18 grammar inventory.",
    } for item in unsupported)


def parse_orthographic_syllables(text: str) -> KhmerOrthographicSyllableParse:
    """Return all complete Unicode 18 parses for one continuous Khmer text span.

    No normalization occurs. Offsets are half-open Unicode code-point offsets.
    Adjacent un-subscripted bases may begin separate orthographic syllables.
    Parse alternatives include both syllable boundaries and component-role
    assignments; no best parse is selected.
    """
    scan = scan_orthographic_components(text)
    components = scan.components
    if not text or scan.status == "INVALID_OR_UNSUPPORTED":
        return KhmerOrthographicSyllableParse(
            text, "INVALID_OR_UNSUPPORTED", (), scan.notes or ("No complete Khmer orthographic structure was found.",), _rejected_spans(components)
        )
    if not components or components[0].role != "BASE":
        return KhmerOrthographicSyllableParse(
            text, "INVALID_OR_UNSUPPORTED", (), ("A Unicode 18 orthographic syllable must begin with a base character.",),
            ({"start": components[0].start, "end": components[0].end, "reason": "The first component is not a base character (B)."},)
        )

    size = len(components)
    paths_by_index: dict[int, list[tuple[tuple[int, int, tuple[str, ...], tuple[str, ...]], ...]]] = {size: [()]}
    for start in range(size - 1, -1, -1):
        if _role(components, start) != "BASE":
            continue
        paths = []
        for end, extensions, grammar_roles in _syllable_matches(components, start):
            if end != size and _role(components, end) != "BASE":
                continue
            for remainder in paths_by_index.get(end, ()):
                paths.append(((start, end, extensions, grammar_roles),) + remainder)
                if len(paths) > MAX_PARSE_ALTERNATIVES:
                    break
            if len(paths) > MAX_PARSE_ALTERNATIVES:
                break
        if paths:
            paths_by_index[start] = list(dict.fromkeys(paths))

    paths = paths_by_index.get(0, [])
    if not paths:
        return KhmerOrthographicSyllableParse(
            text, "EVIDENCE_LIMITED", (),
            ("Recognized components do not form a complete sequence under the Unicode 18 §16.4 ordering formula; no boundary was guessed.",),
            _rejected_spans(components),
        )
    if len(paths) > MAX_PARSE_ALTERNATIVES:
        return KhmerOrthographicSyllableParse(
            text, "EVIDENCE_LIMITED", (),
            ("The parse forest exceeded the configured alternative limit.",),
            ({"start": 0, "end": len(text), "reason": "The configured parse-alternative limit was reached; the forest is incomplete."},),
        )

    alternatives = []
    for path in paths:
        syllables = []
        for start_index, end_index, extensions, grammar_roles in path:
            selected = components[start_index:end_index]
            start, end = selected[0].start, selected[-1].end
            syllables.append(KhmerOrthographicSyllable(
                start, end, text[start:end], selected, grammar_roles, extensions
            ))
        alternatives.append(KhmerOrthographicParseAlternative(tuple(syllables)))

    status: ParseStatus = "AMBIGUOUS" if len(alternatives) > 1 else "PARSED"
    return KhmerOrthographicSyllableParse(
        text, status, tuple(alternatives),
        ("Orthographic syllables are not phonological syllables or lexical words.",
         "All complete grammar parses and component-role assignments are retained; no best parse is selected."),
    )
