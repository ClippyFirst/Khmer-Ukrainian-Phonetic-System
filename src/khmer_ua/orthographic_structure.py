"""Lossless structural scan of Khmer orthographic components.

This scanner classifies Unicode-encoded components. It does not infer word
boundaries, pronounce components, or force ambiguous adjacent base letters
into a single syllable. Offsets are half-open Python Unicode code-point offsets
into the exact input string; this function does not normalize its input.
"""
from dataclasses import dataclass
from typing import Literal

from .data import CONSONANTS, SIGNS

COENG = "\u17D2"
ZWNJ = "\u200C"
ZWJ = "\u200D"

_CONSONANTS = {item["char"] for item in CONSONANTS}
_SIGN_KIND = {item["char"]: item.get("kind", "other_sign") for item in SIGNS}
_INDEPENDENT_VOWELS = {
    char for char, kind in _SIGN_KIND.items() if kind == "independent_vowel"
}
_DEPENDENT_VOWELS = {
    char for char, kind in _SIGN_KIND.items()
    if kind in {"dependent_vowel", "composite_vowel"}
}
_SHIFTERS = {
    char for char, kind in _SIGN_KIND.items() if kind == "register_shifter"
}
_ROBAT = "\u17CC"

ComponentRole = Literal[
    "BASE", "SUBSCRIPT", "ROBAT", "SHIFTER", "VOWEL",
    "FORMAT_CONTROL", "OTHER_SIGN", "UNSUPPORTED",
]


@dataclass(frozen=True)
class KhmerOrthographicComponent:
    role: ComponentRole
    text: str
    start: int
    end: int
    codepoints: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class KhmerOrthographicScan:
    source_text: str
    components: tuple[KhmerOrthographicComponent, ...]
    status: str
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "schema": "khmer-orthographic-components/v1",
            "source_text": self.source_text,
            "offset_unit": "unicode_code_point",
            "status": self.status,
            "notes": list(self.notes),
            "components": [
                {
                    "role": item.role,
                    "text": item.text,
                    "start": item.start,
                    "end": item.end,
                    "codepoints": list(item.codepoints),
                    "status": item.status,
                }
                for item in self.components
            ],
        }

    @property
    def protected_spans(self) -> tuple[tuple[int, int], ...]:
        """Atomic encoded component spans, not complete syllable or word spans."""
        return tuple((item.start, item.end) for item in self.components)


def _component(role: ComponentRole, text: str, start: int, status: str = "RECOGNIZED"):
    return KhmerOrthographicComponent(
        role=role,
        text=text,
        start=start,
        end=start + len(text),
        codepoints=tuple(f"U+{ord(char):04X}" for char in text),
        status=status,
    )


def scan_orthographic_components(text: str) -> KhmerOrthographicScan:
    """Classify known Khmer component encodings without guessing segmentation.

    A COENG + consonant/independent-vowel pair is one SUBSCRIPT component,
    following Unicode 18 Chapter 16. Adjacent un-subscripted base letters are
    retained as BASE components but make the overall scan EVIDENCE_LIMITED:
    they may be coda/other components or the beginning of another orthographic
    syllable. This scanner intentionally does not decide between those parses.
    """
    components: list[KhmerOrthographicComponent] = []
    notes: list[str] = []
    index = 0
    base_count = 0
    unsupported = False

    while index < len(text):
        char = text[index]
        if char == COENG:
            if index + 1 < len(text) and (
                text[index + 1] in _CONSONANTS
                or text[index + 1] in _INDEPENDENT_VOWELS
            ):
                components.append(_component("SUBSCRIPT", text[index:index + 2], index))
                index += 2
                continue
            components.append(_component("UNSUPPORTED", char, index, "MALFORMED_COENG"))
            notes.append(f"Malformed COENG at code-point offset {index}.")
            unsupported = True
            index += 1
            continue

        if char in _CONSONANTS or char in _INDEPENDENT_VOWELS:
            base_count += 1
            status = "RECOGNIZED" if base_count == 1 else "AMBIGUOUS_BASE_ROLE"
            components.append(_component("BASE", char, index, status))
            index += 1
            continue

        if char == _ROBAT:
            components.append(_component("ROBAT", char, index))
        elif char in _SHIFTERS:
            components.append(_component("SHIFTER", char, index))
        elif char in {ZWNJ, ZWJ}:
            components.append(_component("FORMAT_CONTROL", char, index))
        elif char in _DEPENDENT_VOWELS:
            components.append(_component("VOWEL", char, index))
        elif char in _SIGN_KIND and _SIGN_KIND[char] not in {"unmodeled_letter", "structural"}:
            # Includes nikahit and other signs. In Unicode's component order,
            # O means an additional sign; nikahit may combine with a V.
            components.append(_component("OTHER_SIGN", char, index))
        else:
            components.append(_component("UNSUPPORTED", char, index, "UNMODELED_CHARACTER"))
            notes.append(f"Unmodeled character U+{ord(char):04X} at code-point offset {index}.")
            unsupported = True
        index += 1

    if not text:
        status = "INVALID_OR_UNSUPPORTED"
        notes.append("Empty input has no Khmer orthographic base.")
    elif unsupported:
        status = "INVALID_OR_UNSUPPORTED"
    elif base_count == 0:
        status = "INVALID_OR_UNSUPPORTED"
        notes.append("No modeled Khmer consonant or independent-vowel base was found.")
    elif base_count > 1:
        status = "EVIDENCE_LIMITED"
        notes.append(
            "Multiple un-subscripted base letters occur in one supplied span; "
            "the scanner preserves them but does not decide coda versus syllable boundary."
        )
    else:
        status = "ESTABLISHED_STRUCTURE"

    return KhmerOrthographicScan(text, tuple(components), status, tuple(notes))
