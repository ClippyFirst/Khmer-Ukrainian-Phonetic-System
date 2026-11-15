"""Evidence-backed BGN/PCGN romanization letter inventory.

This is a character-inventory validator, not a transliterator. It preserves
source code points exactly and does not normalize, map, or emit IPA/Ukrainian.
"""
from __future__ import annotations

import unicodedata
from dataclasses import asdict, dataclass
from typing import Literal

PCGN_CHARACTER_INVENTORY_LOCATOR = "PCGN 1972, Note 10 (p. 5)"

# Exact forms listed in Note 10. The breve forms are two-code-point sequences;
# do not silently compose, decompose, or otherwise normalize them.
PCGN_SPECIAL_LETTER_CODEPOINTS: dict[str, tuple[str, ...]] = {
    "â": ("U+00E2",),
    "Â": ("U+00C2",),
    "ă": ("U+0103",),
    "Ă": ("U+0102",),
    "á": ("U+00E1",),
    "Á": ("U+00C1",),
    "ê": ("U+00EA",),
    "Ê": ("U+00CA",),
    "ĕ": ("U+0115",),
    "Ĕ": ("U+0114",),
    "é": ("U+00E9",),
    "É": ("U+00C9",),
    "ĭ": ("U+012D",),
    "Ĭ": ("U+012C",),
    "ô": ("U+00F4",),
    "Ô": ("U+00D4",),
    "ó": ("U+00F3",),
    "Ó": ("U+00D3",),
    "ŏ": ("U+014F",),
    "Ŏ": ("U+014E",),
    "œ": ("U+0153",),
    "Œ": ("U+0152",),
    "œ̆": ("U+0153", "U+0306"),
    "Œ̆": ("U+0152", "U+0306"),
    "ŭ": ("U+016D",),
    "Ŭ": ("U+016C",),
}
PCGN_SPECIAL_LETTERS = tuple(
    sorted(PCGN_SPECIAL_LETTER_CODEPOINTS, key=len, reverse=True)
)


@dataclass(frozen=True)
class PCGNRomanizationCharacterInventoryDecision:
    source_text: str
    status: Literal["VALID", "UNSUPPORTED_LETTER"]
    recognized_special_letters: tuple[str, ...]
    unsupported_letters: tuple[str, ...]
    non_letter_characters: tuple[str, ...]
    codepoint_trace: tuple[str, ...]
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def validate_pcgn_romanization_characters(
    text: str,
) -> PCGNRomanizationCharacterInventoryDecision:
    """Validate letter forms against PCGN Note 10 without changing the text.

    Basic ASCII Roman letters are accepted. Modified letters must match the
    exact Note 10 inventory, including the two decomposed œ + COMBINING BREVE
    sequences. Non-letter punctuation, spacing and digits are passed through
    and reported separately; this function does not validate their policy.
    """
    recognized: list[str] = []
    unsupported: list[str] = []
    non_letters: list[str] = []
    i = 0

    while i < len(text):
        matched = next(
            (token for token in PCGN_SPECIAL_LETTERS if text.startswith(token, i)),
            None,
        )
        if matched is not None:
            recognized.append(matched)
            i += len(matched)
            continue

        char = text[i]
        if char.isascii() and char.isalpha():
            i += 1
            continue

        category = unicodedata.category(char)
        if category.startswith(("L", "M")):
            unsupported.append(char)
        else:
            non_letters.append(char)
        i += 1

    return PCGNRomanizationCharacterInventoryDecision(
        source_text=text,
        status="UNSUPPORTED_LETTER" if unsupported else "VALID",
        recognized_special_letters=tuple(recognized),
        unsupported_letters=tuple(unsupported),
        non_letter_characters=tuple(non_letters),
        codepoint_trace=tuple(f"U+{ord(char):04X}" for char in text),
        source_locator=PCGN_CHARACTER_INVENTORY_LOCATOR,
        warnings=(
            "PCGN_NOTE_10_CHARACTER_INVENTORY_VALIDATION_ONLY",
            "SOURCE_CODEPOINTS_PRESERVED_NO_NORMALIZATION_OR_TRANSLITERATION",
            "NON_LETTER_CHARACTERS_NOT_VALIDATED",
            "NO_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


__all__ = [
    "PCGN_CHARACTER_INVENTORY_LOCATOR",
    "PCGN_SPECIAL_LETTER_CODEPOINTS",
    "PCGN_SPECIAL_LETTERS",
    "PCGNRomanizationCharacterInventoryDecision",
    "validate_pcgn_romanization_characters",
]
