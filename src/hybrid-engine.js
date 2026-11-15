/**
 * Browser-side port of the evidence-gated hybrid IPA candidate contract.
 *
 * The rule engine remains the only authority for published IPA/Ukrainian
 * values. Optional provider functions contribute typed diagnostics only.
 * This module has no network, model, storage or backend dependency.
 */
export const DEFAULT_PROFILE = "khmer-pph-careful-citation-v1";
export const IPA_KINDS = Object.freeze(["PHONEMIC", "PHONETIC_BROAD", "PHONETIC_NARROW"]);
export const CANDIDATE_STATUSES = Object.freeze(["COMPLETE", "PARTIAL"]);

export const PROVIDER_PRIORITY = Object.freeze({
  mekongphon: 10,
  "khmer-phonemizer": 20,
  khmer_phonemizer: 20,
  epitran: 30,
  goruut: 90,
});
export const DEFAULT_PROVIDER_PRIORITY = 50;

const IPA_SYMBOLS = new Set("ˈˌːˑ˥˦˧˨˩͜͡‿.·|/-[]");
const IPA_DIGITS = new Set("0123456789");
const IPA_CLICKS = new Set("ʘǀǃǂǁ");
const IPA_MODIFIER_LETTERS = new Set("ˈˌːˑʰʱʲʷʶʴʵˠˤʼ˞ᵝᶣᵊᵐⁿᵑᶬᶮᶯ");

function isPlainObject(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function isIpaSegmentLetter(character) {
  return /\p{L}/u.test(character)
    && !/\p{Lm}/u.test(character)
    && (/[\p{Script=Latin}\p{Script=Greek}]/u.test(character));
}

function isIpaModifierLetter(character) {
  return /\p{Lm}/u.test(character)
    && (/[\p{Script=Latin}\p{Script=Greek}]/u.test(character)
      || IPA_MODIFIER_LETTERS.has(character));
}

export function validateIpaNotation(ipa) {
  if (typeof ipa !== "string" || !ipa || !ipa.trim()) {
    throw new TypeError("candidate IPA must be a non-empty string");
  }
  if (ipa !== ipa.trim()) {
    throw new TypeError("candidate IPA must not have leading or trailing whitespace");
  }
  if (ipa.normalize("NFC") !== ipa) {
    throw new TypeError("candidate IPA must be NFC-normalized; output is never silently rewritten");
  }

  const delimiters = [...ipa].filter((character) => "/[]".includes(character));
  if (delimiters.length && (
    ipa.length < 2
    || !((ipa.startsWith("/") && ipa.endsWith("/")) || (ipa.startsWith("[") && ipa.endsWith("]")))
    || /[/\[\]]/u.test(ipa.slice(1, -1))
  )) {
    throw new TypeError("candidate IPA has unbalanced or misplaced outer delimiters");
  }

  let hasSegment = false;
  let previousWasBase = false;
  for (const [index, character] of [...ipa].entries()) {
    const categoryMark = /\p{M}/u.test(character);
    if ("/[]".includes(character)) continue;
    if (isIpaSegmentLetter(character)) {
      hasSegment = true;
      previousWasBase = true;
      continue;
    }
    if (isIpaModifierLetter(character)) continue;
    if (categoryMark) {
      if (!previousWasBase) throw new TypeError("orphan combining mark at IPA offset " + index);
      previousWasBase = character === "͡" || character === "͜";
      continue;
    }
    if (IPA_DIGITS.has(character)) {
      previousWasBase = false;
      continue;
    }
    if (/\s/u.test(character)) {
      previousWasBase = false;
      continue;
    }
    if (IPA_SYMBOLS.has(character)) {
      if ((character === "͡" || character === "͜") && !previousWasBase) {
        throw new TypeError("orphan IPA tie bar at offset " + index);
      }
      previousWasBase = character === "͡" || character === "͜";
      continue;
    }
    if (IPA_CLICKS.has(character)) {
      hasSegment = true;
      previousWasBase = true;
      continue;
    }
    throw new TypeError(
      "unsupported non-IPA character U+" + character.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")
        + " at IPA offset " + index,
    );
  }

  if (!hasSegment) throw new TypeError("candidate IPA must contain at least one IPA segment letter");
  return ipa;
}

export function validateIpaCandidate(rawOutput, {
  profile = DEFAULT_PROFILE,
  kind,
  status,
  provider,
  uncertainty = [],
  provenance = {},
} = {}) {
  if (typeof profile !== "string" || profile !== DEFAULT_PROFILE) {
    throw new TypeError("unsupported pronunciation profile: " + profile);
  }
  if (!IPA_KINDS.includes(kind)) throw new TypeError("unsupported IPA kind: " + kind);
  if (!CANDIDATE_STATUSES.includes(status)) throw new TypeError("unsupported candidate status: " + status);
  if (typeof provider !== "string" || !provider.trim()) {
    throw new TypeError("candidate provider must be a non-empty string");
  }
  if (!Array.isArray(uncertainty) || uncertainty.some((note) => typeof note !== "string" || !note.trim())) {
    throw new TypeError("candidate uncertainty must be an array of non-empty strings");
  }
  if (status === "PARTIAL" && uncertainty.length === 0) {
    throw new TypeError("PARTIAL candidate must include at least one uncertainty note");
  }
  if (!isPlainObject(provenance)) throw new TypeError("candidate provenance must be a mapping/object");
  validateIpaNotation(rawOutput);

  return Object.freeze({
    raw_output: rawOutput,
    ipa: rawOutput,
    profile,
    kind,
    status,
    provider,
    uncertainty: Object.freeze([...uncertainty]),
    provenance: Object.freeze({ ...provenance }),
  });
}

export class HybridKhmerEngine {
  constructor({ ruleEngine, providers = {} } = {}) {
    if (typeof ruleEngine !== "function") {
      throw new TypeError("HybridKhmerEngine requires a deterministic ruleEngine function");
    }
    if (!isPlainObject(providers)) throw new TypeError("providers must be a mapping/object");
    this.ruleEngine = ruleEngine;
    this.providers = { ...providers };
  }

  analyze(text, profile = DEFAULT_PROFILE, additionalProviders = {}) {
    const result = this.ruleEngine(text, profile);
    if (result === null || result === undefined) return null;
    if (!isPlainObject(additionalProviders)) {
      throw new TypeError("additionalProviders must be a mapping/object");
    }

    const providers = { ...this.providers, ...additionalProviders };
    const normalized = result.normalized ?? result.source ?? text;
    const candidates = [];
    const failures = [];

    const ordered = Object.entries(providers).sort(([left], [right]) => {
      const leftPriority = PROVIDER_PRIORITY[left] ?? DEFAULT_PROVIDER_PRIORITY;
      const rightPriority = PROVIDER_PRIORITY[right] ?? DEFAULT_PROVIDER_PRIORITY;
      return leftPriority - rightPriority || left.localeCompare(right);
    });

    for (const [providerId, provider] of ordered) {
      try {
        if (typeof provider !== "function") throw new TypeError("provider must be a function");
        const raw = provider(normalized);
        if (!isPlainObject(raw)) {
          throw new TypeError("provider must return typed candidate metadata; bare IPA strings are rejected");
        }
        const candidate = validateIpaCandidate(raw.ipa, {
          profile: raw.profile ?? profile,
          kind: raw.kind,
          status: raw.status,
          provider: providerId,
          uncertainty: raw.uncertainty ?? [],
          provenance: raw.provenance ?? {},
        });
        candidates.push({
          provider: candidate.provider,
          priority: PROVIDER_PRIORITY[providerId] ?? DEFAULT_PROVIDER_PRIORITY,
          ipa_raw: candidate.raw_output,
          profile: candidate.profile,
          kind: candidate.kind,
          status: candidate.status,
          uncertainty: [...candidate.uncertainty],
          provenance: { ...candidate.provenance },
          promotion: "WITHHELD_PENDING_INDEPENDENT_PROFILE_MATCHED_ADJUDICATION",
        });
      } catch (error) {
        failures.push({
          provider: providerId,
          reason: error instanceof Error ? error.message : String(error),
        });
      }
    }

    // Preserve the deterministic rule result exactly; providers are diagnostic only.
    return {
      ...result,
      hybrid_engine: "khmer-evidence-gated-hybrid-browser-v1",
      external_candidates: candidates,
      backend_failures: failures,
      external_candidate_count: candidates.length,
      provider_priority_policy: "lower_number_runs_first_and_orders_candidates; priorities are research triage only, not accuracy, confidence, voting or promotion",
      selection_policy: "internal deterministic output is preserved; typed external candidates are diagnostic only; no voting or promotion",
    };
  }
}
