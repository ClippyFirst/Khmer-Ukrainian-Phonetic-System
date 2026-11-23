"""Evidence-gated research adapter for external Khmer IPA candidates.

The deterministic rule engine remains the sole final-output authority.
External provider results cross the shared typed IPA validation boundary and
are returned as diagnostic candidates only; this module never promotes them.
"""
from __future__ import annotations

from typing import Any, Callable

from .ipa import IPACandidateStatus, validate_ipa_candidate
from .rule_engine import RuleBasedKhmerEngine
from .practical import map_ipa_string

Provider = Callable[[str], dict[str, Any]]

PROVIDER_PRIORITY = {
    "mekongphon": 10,
    "khmer-phonemizer": 20,
    "khmer_phonemizer": 20,
    "epitran": 30,
    "goruut": 90,
}
DEFAULT_PROVIDER_PRIORITY = 50
DEFAULT_PROFILE = "khmer-pph-careful-citation-v1"


class HybridKhmerEngine:
    """Run internal rules and collect explicitly typed, non-authoritative IPA."""

    def __init__(
        self,
        providers: dict[str, Provider] | None = None,
        rule_engine: RuleBasedKhmerEngine | None = None,
    ):
        self.providers = dict(providers or {})
        self.rule_engine = rule_engine or RuleBasedKhmerEngine()

    def analyze(self, text: str) -> dict[str, Any]:
        result = dict(self.rule_engine.analyze(text))
        candidates: list[dict[str, Any]] = []
        failures: list[dict[str, str]] = []
        normalized = result.get("normalized", text)

        for provider_id, provider in sorted(
            self.providers.items(),
            key=lambda item: (PROVIDER_PRIORITY.get(item[0], DEFAULT_PROVIDER_PRIORITY), item[0]),
        ):
            raw: Any = None
            try:
                raw = provider(normalized)
                if not isinstance(raw, dict):
                    raise ValueError("provider must return typed candidate metadata; bare IPA strings are rejected")
                candidate = validate_ipa_candidate(
                    raw.get("ipa"),
                    profile=raw.get("profile", DEFAULT_PROFILE),
                    kind=raw.get("kind"),
                    status=raw.get("status"),
                    provider=provider_id,
                    uncertainty=raw.get("uncertainty", ()),
                )
                profile_match = raw.get("profile_match", "UNVERIFIED")
                if not isinstance(profile_match, str) or not profile_match.strip():
                    raise ValueError("provider profile_match must be a non-empty string")
                ukrainian, mapping_failure = map_ipa_string(candidate.ipa)
                candidates.append({
                    "provider": candidate.provider,
                    "priority": PROVIDER_PRIORITY.get(provider_id, DEFAULT_PROVIDER_PRIORITY),
                    "ipa_raw": candidate.raw_output,
                    "profile": candidate.profile,
                    "profile_match": profile_match,
                    "kind": candidate.kind,
                    "status": candidate.status.value,
                    "uncertainty": list(candidate.uncertainty),
                    "provenance": raw.get("provenance", {}),
                    "ukrainian_candidate": ukrainian,
                    "ukrainian_mapping_failure": mapping_failure,
                    "promotion": "WITHHELD_PENDING_INDEPENDENT_PROFILE_MATCHED_ADJUDICATION",
                })
            except Exception as exc:
                failure = {"provider": provider_id, "reason": str(exc) or type(exc).__name__}
                if isinstance(raw, dict) and isinstance(raw.get("ipa"), str):
                    failure["raw_output"] = raw["ipa"]
                failures.append(failure)

        # Canonical deterministic fields remain untouched. If they are
        # unresolved, expose the first mappable provider result (or the first
        # valid IPA candidate when none maps completely) as a separate
        # provisional result. Provider order is triage, never accuracy ranking.
        canonical_ipa = result.get("ipa")
        canonical_unresolved = not canonical_ipa or "⟦" in str(canonical_ipa)
        selected_candidate = next(
            (item for item in candidates if item["ukrainian_candidate"] is not None),
            candidates[0] if candidates else None,
        )
        provisional_candidate = None
        if canonical_unresolved and selected_candidate is not None:
            provisional_candidate = {
                "ipa": selected_candidate["ipa_raw"],
                "ukrainian": selected_candidate["ukrainian_candidate"],
                "ukrainian_mapping_failure": selected_candidate["ukrainian_mapping_failure"],
                "status": "PROVISIONAL",
                "provider": selected_candidate["provider"],
                "profile": selected_candidate["profile"],
                "profile_match": selected_candidate["profile_match"],
                "kind": selected_candidate["kind"],
                "candidate_status": selected_candidate["status"],
                "uncertainty": list(selected_candidate["uncertainty"]) + [
                    "Candidate selected by configured provider order, not by measured accuracy or majority vote."
                ],
                "provenance": selected_candidate["provenance"],
                "selection": "FIRST_MAPPABLE_OR_FIRST_VALID_CONFIGURED_PROVIDER",
            }
        result.update({
            "hybrid_engine": "khmer-evidence-gated-hybrid-v3",
            "external_candidates": candidates,
            "provisional_candidate": provisional_candidate,
            "backend_failures": failures,
            "external_candidate_count": len(candidates),
            "provider_priority_policy": (
                "lower_number_runs_first_and_orders_candidates; priorities are research "
                "triage only, not accuracy, confidence, voting or promotion"
            ),
            "selection_policy": (
                "canonical deterministic output is preserved; when unresolved, the first "
                "configured provider whose typed IPA maps through the Ukrainian adapter is "
                "exposed separately as PROVISIONAL; if none maps, the first valid IPA candidate "
                "is still exposed with its mapping failure; no majority vote or accuracy claim"
            ),
        })
        return result


def make_mekongphon_backend(
    model_id: str = "byumatrixlab/khmer-ipa",
    revision: str = "20e069d384b240da76320e1569958568c12a54bc",
    *,
    num_beams: int = 4,
) -> Provider:
    """Lazy pinned CPU inference adapter; dependencies remain optional."""
    state: dict[str, Any] = {}

    def predict(text: str) -> dict[str, Any]:
        if not state:
            try:
                import torch
                from transformers import AutoTokenizer, EncoderDecoderModel
            except ImportError as exc:
                raise RuntimeError("Install optional torch and transformers for MekongPhon") from exc
            torch.set_num_threads(1)
            torch.manual_seed(0)
            model = EncoderDecoderModel.from_pretrained(model_id, revision=revision).to("cpu")
            encoder = AutoTokenizer.from_pretrained(
                model_id, subfolder="encoder_tokenizer", revision=revision
            )
            decoder = AutoTokenizer.from_pretrained(
                model_id, subfolder="decoder_tokenizer", revision=revision
            )
            model.eval()
            state.update(torch=torch, model=model, encoder=encoder, decoder=decoder)

        encoded = state["encoder"](
            [text], return_tensors="pt", padding=True, truncation=True, max_length=128
        )
        with state["torch"].inference_mode():
            generated = state["model"].generate(
                **encoded, max_length=128, num_beams=num_beams, early_stopping=True
            )
        ipa = state["decoder"].decode(generated[0], skip_special_tokens=True)
        return {
            "ipa": ipa,
            "profile": DEFAULT_PROFILE,
            "kind": "PHONETIC_BROAD",
            "status": "PARTIAL",
            "uncertainty": ["External model output has not been independently adjudicated for this profile."],
            "provenance": {
                "engine": model_id,
                "revision": revision,
                "device": "cpu",
                "num_beams": num_beams,
                "training_split_independence": "NOT_ESTABLISHED",
                "tone_coverage": "NOT_EVALUATED_BY_pron_no_tones",
            },
        }

    return predict


def make_command_backend(command: list[str], *, engine_id: str, revision: str) -> Provider:
    """Adapter for pinned CLI wrappers; output is always an unadjudicated candidate."""
    import subprocess

    def run(text: str) -> dict[str, Any]:
        completed = subprocess.run(
            command, input=text + "\n", text=True, capture_output=True, check=True
        )
        return {
            "ipa": completed.stdout.rstrip("\r\n"),
            "profile": DEFAULT_PROFILE,
            "kind": "PHONETIC_BROAD",
            "status": "PARTIAL",
            "uncertainty": ["CLI provider output has not been independently adjudicated for this profile."],
            "provenance": {"engine": engine_id, "revision": revision, "stderr": completed.stderr},
        }

    return run


def create_hybrid_engine(providers: dict[str, Provider] | None = None) -> HybridKhmerEngine:
    return HybridKhmerEngine(providers=providers)


__all__ = [
    "HybridKhmerEngine",
    "RuleBasedKhmerEngine",
    "create_hybrid_engine",
    "make_mekongphon_backend",
    "make_command_backend",
]
