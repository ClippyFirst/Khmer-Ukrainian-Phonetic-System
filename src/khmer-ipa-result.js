import practicalPolicy from "../data/ukrainian/practical-policy.json" with { type: "json" };
import { mapIpa } from "./ukrainian-practical.js";

const RESULT_STATUSES = new Set(["SUPPORTED", "UNCERTAIN", "PROVISIONAL", "UNRESOLVED"]);
const MODIFIERS = new Set(["ˈ", "ˌ", "ː", "ˑ"]);
const BOUNDARIES = new Set([" ", "\t", "\n", ".", "·", "‧"]);
const IPA_SYMBOLS = [
  ...new Set([
    ...Object.keys(practicalPolicy.segments ?? {}),
    ...Object.keys(practicalPolicy.sequences ?? {}),
  ]),
].filter(Boolean).sort((a, b) => b.length - a.length);

function stripOuterDelimiters(ipa) {
  const value = ipa.trim();
  if (value.length >= 2 && ((value[0] === "/" && value.at(-1) === "/")
      || (value[0] === "[" && value.at(-1) === "]"))) return value.slice(1, -1);
  return value;
}

function segmentKind(symbol) {
  if (MODIFIERS.has(symbol)) return "modifier";
  if (BOUNDARIES.has(symbol)) return "boundary";
  return "aeiouɑɒæɛɜəɨɪɔɵœɐɤɯʊʌʏʉ".includes(symbol[0]) ? "vowel" : "consonant";
}

function makeResult({
  phonemic_ipa = null,
  segments = [],
  status = "SUPPORTED",
  provenance = [],
  uncertainty = [],
  vowel_length = null,
}) {
  const value = {
    phonemic_ipa,
    segments,
    syllable_boundaries: [0, segments.length],
    vowel_length,
    tone_category: null,
    tone_contour_ipa: null,
    status,
    provenance: [...provenance],
    uncertainty: [...uncertainty],
  };
  value.toJSON = () => ({
    phonemic_ipa: value.phonemic_ipa,
    segments: value.segments.map((segment) => ({ ...segment })),
    syllable_boundaries: [...value.syllable_boundaries],
    vowel_length: value.vowel_length,
    tone_category: value.tone_category,
    tone_contour_ipa: value.tone_contour_ipa,
    status: value.status,
    provenance: [...value.provenance],
    uncertainty: [...value.uncertainty],
  });
  return value;
}

export function fromIpa(ipa, {
  status = "SUPPORTED",
  provenance = [],
  uncertainty = [],
} = {}) {
  if (!RESULT_STATUSES.has(status) || ["PROVISIONAL", "UNRESOLVED"].includes(status)) {
    throw new TypeError("fromIpa requires SUPPORTED or UNCERTAIN status");
  }
  if (typeof ipa !== "string" || !ipa.trim()) {
    return fromUnknownSourceUnit("?", {
      provenance,
      uncertainty: [...uncertainty, "EMPTY-IPA-RESULT"],
    });
  }

  const raw = stripOuterDelimiters(ipa);
  const segments = [];
  const unsupported = [];
  for (let index = 0; index < raw.length;) {
    const char = raw[index];
    if (BOUNDARIES.has(char) || MODIFIERS.has(char)) {
      segments.push({ ipa: char, kind: segmentKind(char), provenance: [...provenance], certainty: status });
      index += 1;
      continue;
    }
    const match = IPA_SYMBOLS.find((symbol) => raw.startsWith(symbol, index));
    if (!match) {
      unsupported.push(char);
      segments.push({ ipa: char, kind: "unknown", provenance: [...provenance], certainty: "UNRESOLVED" });
      index += 1;
      continue;
    }
    segments.push({ ipa: match, kind: segmentKind(match), provenance: [...provenance], certainty: status });
    index += match.length;
  }

  if (unsupported.length) {
    return makeResult({
      phonemic_ipa: null,
      segments,
      status: "UNRESOLVED",
      provenance,
      uncertainty: [...new Set([...uncertainty, "UNSUPPORTED-IPA-SEGMENT"])],
    });
  }
  return makeResult({
    phonemic_ipa: raw,
    segments,
    status,
    provenance,
    uncertainty,
    vowel_length: raw.includes("ː") ? "long" : null,
  });
}

export function fromProvisionalIpa(ipaHint, {
  unresolvedGraphemes = [],
  provenance = [],
  uncertainty = [],
  appendUnknownTail = true,
} = {}) {
  let typed = null;
  if (ipaHint) {
    typed = fromIpa(ipaHint, { status: "UNCERTAIN", provenance, uncertainty });
    if (typed.status === "UNRESOLVED") return typed;
  }
  const segments = (typed?.segments ?? []).map((segment) => ({
    ...segment,
    provenance: [...new Set([...segment.provenance, ...provenance])],
    certainty: "PROVISIONAL",
  }));
  if (appendUnknownTail || unresolvedGraphemes.length || !segments.length) {
    segments.push({
      ipa: "?",
      kind: "unknown",
      provenance: [...provenance],
      certainty: "PROVISIONAL",
    });
  }
  return makeResult({
    phonemic_ipa: null,
    segments,
    status: ipaHint ? "PROVISIONAL" : "UNRESOLVED",
    provenance: [...new Set([...provenance, "FALLBACK:GRAPHEME-POSITION-PREVIEW"])],
    uncertainty: [...new Set([...uncertainty, "PHONETIC-READING-PROVISIONAL"])],
  });
}

export function fromUnknownSourceUnit(surface, {
  provenance = [],
  uncertainty = [],
} = {}) {
  if (typeof surface !== "string" || !surface) throw new TypeError("Unknown source unit must not be empty");
  const trace = [...new Set([...provenance, "FALLBACK:UNKNOWN-SOURCE-UNIT"])];
  return makeResult({
    segments: [{
      ipa: "?",
      kind: "unknown",
      provenance: trace,
      certainty: "UNRESOLVED",
    }],
    status: "UNRESOLVED",
    provenance: trace,
    uncertainty: [...new Set([...uncertainty, "PHONETIC-READING-UNKNOWN"])],
  });
}

export function adaptPhoneticResult(result, { allowUncertain = false } = {}) {
  if (!result || !RESULT_STATUSES.has(result.status) || !Array.isArray(result.segments)) {
    throw new TypeError("Ukrainian adaptation requires a typed phonetic result");
  }
  if (result.status === "UNRESOLVED") {
    return result.segments.every((segment) => segment.kind === "unknown") ? "???" : null;
  }
  if (result.status === "PROVISIONAL") {
    const output = [];
    let knownRun = [];
    let unknownRun = false;
    const flushKnown = () => {
      if (!knownRun.length) return;
      const mapped = mapIpa(knownRun.join(""), practicalPolicy);
      knownRun = [];
      if (mapped.value === null) {
        if (!unknownRun) output.push("???");
        unknownRun = true;
      } else {
        output.push(mapped.value);
        unknownRun = false;
      }
    };
    for (const segment of result.segments) {
      if (segment.kind === "unknown") {
        flushKnown();
        if (!unknownRun) output.push("???");
        unknownRun = true;
      } else {
        if (segment.certainty !== "PROVISIONAL") return null;
        knownRun.push(segment.ipa);
      }
    }
    flushKnown();
    return output.join("") || "???";
  }
  if (result.status === "UNCERTAIN" && !allowUncertain) return null;
  if (!["SUPPORTED", "UNCERTAIN"].includes(result.status) || !result.segments.length
      || result.segments.some((segment) => segment.kind === "unknown")) return null;
  const mapped = mapIpa(result.segments.map((segment) => segment.ipa).join(""), practicalPolicy);
  return mapped.value;
}
