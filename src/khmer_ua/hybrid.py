"""Hybrid Khmer IPA engine with explicit provisional external candidates.

The deterministic rule engine remains the canonical authority. Optional,
pinned G2P providers can supply a separately labelled best-effort IPA and
Ukrainian candidate when deterministic IPA is unavailable. Provider output is
never relabelled as established or expert-adjudicated.
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
                ukrainian, unsupported = map_ipa_string(candidate.ipa)
                candidates.append({
                    "provider": candidate.provider,
                    "priority": PROVIDER_PRIORITY.get(provider_id, DEFAULT_PROVIDER_PRIORITY),
                    "ipa_raw": candidate.raw_output,
                    "profile": candidate.profile,
                    "kind": candidate.kind,
                    "status": candidate.status.value,
                    "uncertainty": list(candidate.uncertainty),
                    "provenance": raw.get("provenance", {}),
                    "ukrainian_candidate": ukrainian,
                    "ukrainian_mapping_failure": unsupported,
                    "promotion": "WITHHELD_PENDING_INDEPENDENT_PROFILE_MATCHED_ADJUDICATION",
                })
            except Exception as exc:
                failures.append({"provider": provider_id, "reason": str(exc) or type(exc).__name__})

        # Keep canonical fields untouched. When they are unresolved, expose the
        # first provider candidate that crosses the existing Ukrainian IPA
        # adapter as a clearly provisional, source-attributed alternative.
        canonical_ipa = result.get("ipa")
        canonical_unresolved = not canonical_ipa or "⟦" in str(canonical_ipa)
        mapped_candidate = next(
            (item for item in candidates if item.get("ukrainian_candidate") is not None),
            None,
        )
        provisional_candidate = None
        if canonical_unresolved and mapped_candidate is not None:
            provisional_candidate = {
                "ipa": mapped_candidate["ipa_raw"],
                "ukrainian": mapped_candidate["ukrainian_candidate"],
                "status": "PROVISIONAL",
                "provider": mapped_candidate["provider"],
                "profile": mapped_candidate["profile"],
                "kind": mapped_candidate["kind"],
                "uncertainty": list(mapped_candidate["uncertainty"]) + [
                    "Candidate selected by configured provider order, not by measured accuracy or majority vote."
                ],
                "provenance": mapped_candidate["provenance"],
                "selection": "FIRST_MAPPABLE_CONFIGURED_PROVIDER",
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
                "exposed separately as PROVISIONAL; no majority vote or accuracy claim"
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


def make_khmerphonemizer_backend(
    *,
    beam: int = 500,
    min_beam: int = 100,
    beam_score: float = 0.6,
    use_lexicon: bool = True,
) -> Provider:
    """Lazy adapter for the MIT-licensed Khmer Phonemizer 0.0.3 package.

    The package returns token-aligned phone lists rather than profile-matched
    narrow IPA. The result is retained as a PARTIAL broad-phonetic candidate.
    """
    def predict(text: str) -> dict[str, Any]:
        try:
            from khmerphonemizer import phonemize
        except ImportError as exc:
            raise RuntimeError(
                "Install the optional phonemizer extra: pip install .[phonemizer]"
            ) from exc
        tokens, phone_lists = phonemize(
            text,
            beam=beam,
            min_beam=min_beam,
            beam_score=beam_score,
            use_lexicon=use_lexicon,
        )
        if not tokens or not phone_lists or len(tokens) != len(phone_lists):
            raise ValueError("Khmer Phonemizer returned no aligned token/phone output")
        ipa = " ".join("".join(str(phone) for phone in phones) for phones in phone_lists)
        return {
            "ipa": ipa,
            "profile": DEFAULT_PROFILE,
            "kind": "PHONETIC_BROAD",
            "status": "PARTIAL",
            "uncertainty": [
                "Khmer Phonemizer output is an external G2P candidate, not independently adjudicated.",
                "Its dialect, style and segmental conventions have not been demonstrated equivalent to the project's Phnom Penh careful-citation profile.",
                "Token-level output does not establish lexical stress, tone or narrow phonetic detail."
            ],
            "provenance": {
                "engine": "khmerphonemizer",
                "package_version": "0.0.3",
                "license": "MIT",
                "tokens": list(tokens),
                "beam": beam,
                "min_beam": min_beam,
                "beam_score": beam_score,
                "use_lexicon": use_lexicon,
            },
        }
    return predict


def create_hybrid_engine(
    providers: dict[str, Provider] | None = None,
    *,
    include_khmerphonemizer: bool = False,
    include_mekongphon: bool = False,
) -> HybridKhmerEngine:
    """Create an engine with explicitly opted-in optional G2P providers."""
    selected = dict(providers or {})
    if include_khmerphonemizer:
        selected.setdefault("khmer-phonemizer", make_khmerphonemizer_backend())
    if include_mekongphon:
        selected.setdefault("mekongphon", make_mekongphon_backend())
    return HybridKhmerEngine(providers=selected)


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




__all__ = [
    "HybridKhmerEngine",
    "RuleBasedKhmerEngine",
    "create_hybrid_engine",
    "make_mekongphon_backend",
    "make_khmerphonemizer_backend",
    "make_command_backend",
]
