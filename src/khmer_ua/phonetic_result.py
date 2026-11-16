"""Typed, provenance-aware results for the Khmer IPA-first pipeline."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

PHONETIC_RESULT_SCHEMA = "khmer-phonetic-result/v1"
PHONETIC_PIPELINE = (
    "source-orthography",
    "structural-analysis",
    "source-phonology",
    "ipa",
    "ukrainian-target-adaptation",
)


@dataclass(frozen=True)
class PhoneticUncertainty:
    status: str
    note: str
    unresolved_graphemes: tuple[str, ...] = ()


@dataclass(frozen=True)
class PhoneticUnitResult:
    source: str
    status: str
    ipa: str
    ukrainian: str
    profile: str
    rule_trace: tuple[str, ...] = ()
    provenance: dict[str, tuple[str, ...]]
    uncertainty: tuple[PhoneticUncertainty, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["provenance"] = {
            key: list(items) for key, items in self.provenance.items()
        }
        value["uncertainty"] = [asdict(item) for item in self.uncertainty]
        return value


@dataclass(frozen=True)
class PhoneticResult:
    units: tuple[PhoneticUnitResult, ...]
    complete: bool
    partial: bool
    schema: str = PHONETIC_RESULT_SCHEMA
    pipeline: tuple[str, ...] = PHONETIC_PIPELINE

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "pipeline": list(self.pipeline),
            "complete": self.complete,
            "partial": self.partial,
            "units": [unit.to_dict() for unit in self.units],
        }
