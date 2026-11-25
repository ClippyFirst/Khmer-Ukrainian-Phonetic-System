import onsetInventory from "../data/khmer/romanization_ipa_onsets.json" with { type: "json" };
import { fromProvisionalIpa, fromUnknownSourceUnit, adaptPhoneticResult } from "./khmer-ipa-result.js";

const entries = onsetInventory.entries;
const longestTokens = [...new Set(entries.map((entry) => entry.romanization))]
  .sort((left, right) => right.length - left.length);

function unresolved(source, reason, provenance = []) {
  const trace = [...new Set(["ROMANIZATION-MEDIATED-IPA-V1", ...provenance])];
  const typed_ipa = fromUnknownSourceUnit(source || "?", {
    provenance: trace,
    uncertainty: [reason, "ROMANIZATION-DID-NOT-ESTABLISH-IPA"],
  });
  return {
    status: "UNRESOLVED",
    typed_ipa,
    ukrainian: adaptPhoneticResult(typed_ipa) || "???",
    romanized_onset: null,
    provenance: trace,
    uncertainty: [reason, "ROMANIZATION-DID-NOT-ESTABLISH-IPA"],
  };
}

/**
 * Produce a provisional onset-only IPA candidate after cross-checking the
 * romanized onset against the original Khmer base consonant. No vowel, coda,
 * syllable boundary, tone, or dialect detail is inferred.
 */
export function buildRomanizationIpaCandidate(sourceUnit, romanizedUnit) {
  const source = String(sourceUnit ?? "").normalize("NFC");
  const romanized = String(romanizedUnit ?? "").normalize("NFC").toLowerCase();
  const provenance = [
    "ROMANIZATION-MEDIATED-IPA-V1",
    "data/khmer/romanization_ipa_onsets.json",
    "PCGN-1972-CONSONANT-TABLE",
    "data/khmer/consonants.json",
  ];
  if (!source || !romanized) return unresolved(source, "EMPTY-SOURCE-OR-ROMANIZATION", provenance);
  if (source[0] === "ប" && /^[bp]/u.test(romanized)) {
    return unresolved(source, "AMBIGUOUS-PCGN-B-P-ALTERNATION", provenance);
  }

  const token = longestTokens.find((candidate) => romanized.startsWith(candidate));
  if (!token) return unresolved(source, "NO-RECOGNIZED-PCGN-ONSET-TOKEN", provenance);

  const entry = entries.find((candidate) =>
    candidate.romanization === token && candidate.source_units.includes(source[0])
  );
  if (!entry) {
    const ambiguous = source[0] === "ប";
    return unresolved(
      source,
      ambiguous ? "AMBIGUOUS-PCGN-B-P-ALTERNATION" : "ROMANIZATION-SOURCE-ONSET-MISMATCH",
      provenance,
    );
  }

  const uncertainty = [
    "ROMANIZATION-MEDIATED-ONSET-ONLY",
    "VOWEL_CODA_AND_SYLLABLE_NOT_ESTABLISHED",
    "UPSTREAM-ROMANIZER-MAY-HAVE-DROPPED-DIACRITICS",
  ];
  const typed_ipa = fromProvisionalIpa(entry.ipa, {
    unresolvedGraphemes: [...source].slice(1),
    provenance: [...provenance, entry.rule_id],
    uncertainty,
    appendUnknownTail: true,
  });
  return {
    status: "PROVISIONAL",
    typed_ipa,
    ukrainian: adaptPhoneticResult(typed_ipa) || "???",
    romanized_onset: token,
    provenance: [...provenance, entry.rule_id],
    uncertainty,
  };
}
