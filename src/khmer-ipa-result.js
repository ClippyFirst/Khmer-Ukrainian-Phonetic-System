const MODIFIERS = new Set(["ˈ", "ˌ", "ː", "ˑ"]);
const TONE_MARKS = new Set(["˥", "˦", "˧", "˨", "˩"]);
const BOUNDARIES = new Set([" ", "\t", "\n", ".", "·", "‧"]);
const TIE_BARS = new Set(["͡", "͜"]);
const isIpaBase = (character) => /[\p{Script=Latin}\p{Script=Greek}]/u.test(character);
const isModifierLetter = (character) => /\p{Lm}/u.test(character);

function segmentKind(symbol) {
  if (TONE_MARKS.has(symbol)) return "tone";
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
  return {
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
}

export function serializePhoneticResult(result) {
  return {
    phonemic_ipa: result.phonemic_ipa,
    segments: result.segments.map((segment) => ({ ...segment })),
    syllable_boundaries: [...result.syllable_boundaries],
    vowel_length: result.vowel_length,
    tone_category: result.tone_category,
    tone_contour_ipa: result.tone_contour_ipa,
    status: result.status,
    provenance: [...result.provenance],
    uncertainty: [...result.uncertainty],
  };
}

function tokenizeIpa(ipa, provenance, certainty) {
  const chars = [...ipa];
  const segments = [];
  const unsupported = [];
  for (let index = 0; index < chars.length;) {
    const character = chars[index];
    if (BOUNDARIES.has(character) || MODIFIERS.has(character) || TONE_MARKS.has(character)) {
      segments.push({ ipa: character, kind: segmentKind(character), provenance: [...provenance], certainty });
      index += 1;
      continue;
    }
    if (!isIpaBase(character)) {
      unsupported.push(character);
      segments.push({ ipa: character, kind: "unknown", provenance: [...provenance], certainty: "UNRESOLVED" });
      index += 1;
      continue;
    }
    let token = character;
    index += 1;
    while (index < chars.length && /\p{M}/u.test(chars[index]) && !TIE_BARS.has(chars[index])) {
      token += chars[index];
      index += 1;
    }
    if (index < chars.length && TIE_BARS.has(chars[index])) {
      token += chars[index];
      index += 1;
      if (index < chars.length && isIpaBase(chars[index])) {
        token += chars[index];
        index += 1;
        while (index < chars.length && /\p{M}/u.test(chars[index]) && !TIE_BARS.has(chars[index])) {
          token += chars[index];
          index += 1;
        }
      } else {
        unsupported.push(token);
      }
    }
    while (index < chars.length && isModifierLetter(chars[index]) && !TONE_MARKS.has(chars[index])) {
      token += chars[index];
      index += 1;
    }
    segments.push({ ipa: token, kind: segmentKind(token), provenance: [...provenance], certainty });
  }
  return { segments, unsupported };
}

export function fromIpa(ipa, {
  status = "SUPPORTED",
  provenance = [],
  uncertainty = [],
} = {}) {
  if (!["SUPPORTED", "UNCERTAIN"].includes(status)) {
    throw new TypeError("fromIpa requires SUPPORTED or UNCERTAIN status");
  }
  if (typeof ipa !== "string" || !ipa.trim()) {
    return fromUnknownSourceUnit("?", {
      provenance,
      uncertainty: [...uncertainty, "EMPTY-IPA-RESULT"],
    });
  }
  let raw = ipa.trim();
  if (raw.length >= 2 && ((raw[0] === "/" && raw.at(-1) === "/")
      || (raw[0] === "[" && raw.at(-1) === "]"))) raw = raw.slice(1, -1);
  const { segments, unsupported } = tokenizeIpa(raw, provenance, status);
  if (unsupported.length) {
    return makeResult({
      segments,
      status: "UNRESOLVED",
      provenance,
      uncertainty: [...new Set([...uncertainty, "UNSUPPORTED-IPA-NOTATION"])],
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
  if (!result || !["SUPPORTED", "UNCERTAIN", "PROVISIONAL", "UNRESOLVED"].includes(result.status)
      || !Array.isArray(result.segments)) {
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
      if (segment.kind === "unknown" || segment.kind === "tone") {
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
      || result.segments.some((segment) => segment.kind === "unknown" || segment.kind === "tone")) return null;
  const mapped = mapIpa(result.segments.map((segment) => segment.ipa).join(""), practicalPolicy);
  return mapped.value;
}
