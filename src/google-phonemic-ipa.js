import defaultMap from "../data/khmer/google-phonemic-to-ipa.json" with { type: "json" };
import { fromProvisionalFullIpa } from "./khmer-ipa-result.js";

export const GOOGLE_PHONEMIC_PROFILE = "khmer-pph-careful-citation-v1";

function unresolved(raw, sourceTokens, uncertainty, provenance, profile = GOOGLE_PHONEMIC_PROFILE) {
  return {
    raw: typeof raw === "string" ? raw : "",
    source_tokens: sourceTokens,
    ipa: null,
    ipa_kind: "UNRESOLVED",
    status: "UNRESOLVED",
    mapping_status: "UNRESOLVED",
    profile,
    provenance: [...provenance],
    uncertainty: [...uncertainty],
    syllable_boundaries: [],
    candidate: null,
  };
}

export function parseGooglePhonemic(raw, {
  mapping = defaultMap,
  profile = GOOGLE_PHONEMIC_PROFILE,
  provider = "google-khmer-pronunciation-lexicon",
} = {}) {
  const provenance = [
    `GOOGLE_SOURCE:${mapping.source?.id ?? "unregistered"}`,
    `GOOGLE_PHONOLOGY:${mapping.source?.source_revision ?? "unversioned"}`,
    `IPA_MAP:${mapping.map_version ?? "unversioned"}`,
  ];
  if (typeof raw !== "string" || !raw.trim()) {
    return unresolved(raw, [], ["EMPTY_SOURCE_PHONEMIC"], provenance, profile);
  }

  const sourceTokens = raw.trim().split(/\s+/u);
  if (!sourceTokens.length || sourceTokens[0] === "." || sourceTokens.at(-1) === ".") {
    return unresolved(raw, sourceTokens, ["MALFORMED_SYLLABLE_BOUNDARY"], provenance, profile);
  }

  const ipaParts = [];
  const uncertainty = ["TARGET_PROFILE_EQUIVALENCE_UNVERIFIED"];
  const syllableBoundaries = [0];
  const usedMappingStatuses = [];
  let phoneIndex = 0;
  let previousWasBoundary = false;

  for (const token of sourceTokens) {
    if (token === ".") {
      if (previousWasBoundary || phoneIndex === syllableBoundaries.at(-1)) {
        return unresolved(raw, sourceTokens, ["MALFORMED_SYLLABLE_BOUNDARY"], provenance, profile);
      }
      ipaParts.push(".");
      syllableBoundaries.push(phoneIndex);
      previousWasBoundary = true;
      continue;
    }

    const entry = mapping.tokens?.[token];
    if (!entry) {
      return unresolved(raw, sourceTokens, [`UNMAPPED_GOOGLE_PHONE:${token}`], provenance, profile);
    }
    if (typeof entry.ipa !== "string" || !entry.ipa) {
      return unresolved(raw, sourceTokens, [`NON_LEXICAL_GOOGLE_PHONE:${token}`], provenance, profile);
    }
    ipaParts.push(entry.ipa);
    phoneIndex += 1;
    previousWasBoundary = false;
    usedMappingStatuses.push(entry.mapping_status ?? "UNRESOLVED");
    if (entry.mapping_status !== "SOURCE_CORROBORATED") {
      uncertainty.push(`UNVERIFIED_PHONE_MAPPING:${token}`);
    }
  }

  if (!usedMappingStatuses.length || previousWasBoundary) {
    return unresolved(raw, sourceTokens, ["EMPTY_OR_TRAILING_SYLLABLE"], provenance, profile);
  }

  const ipa = ipaParts.join("");
  const candidate = fromProvisionalFullIpa(ipa, {
    kind: "PHONEMIC",
    profile,
    provenance,
    uncertainty: [...new Set(uncertainty)],
  });
  if (candidate.status === "UNRESOLVED" || candidate.ipa_kind !== "PHONEMIC") {
    return unresolved(raw, sourceTokens, ["INVALID_MAPPED_IPA"], provenance, profile);
  }

  if (syllableBoundaries.at(-1) !== phoneIndex) syllableBoundaries.push(phoneIndex);
  return {
    raw,
    source_tokens: sourceTokens,
    ipa,
    ipa_kind: "PHONEMIC",
    status: "PROVISIONAL",
    mapping_status: usedMappingStatuses.every((status) => status === "SOURCE_CORROBORATED")
      ? "SOURCE_CORROBORATED"
      : "PROVISIONAL",
    profile,
    provenance,
    uncertainty: [...new Set(uncertainty)],
    syllable_boundaries: syllableBoundaries,
    candidate,
  };
}
