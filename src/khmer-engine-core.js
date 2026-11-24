import consonants from "../data/khmer/consonants.json" with { type: "json" };
import registers from "../data/khmer/registers.json" with { type: "json" };
import signs from "../data/khmer/signs.json" with { type: "json" };
import vowels from "../data/khmer/vowels.json" with { type: "json" };
import practicalPolicy from "../data/ukrainian/practical-policy.json" with { type: "json" };
import fixtures from "../data/tests/web-fixtures.json" with { type: "json" };
import provisionalIpaCandidates from "../data/khmer/provisional-ipa-candidates.json" with { type: "json" };
import sources from "../data/khmer/sources.json" with { type: "json" };
import { khmerToLatin } from "@gmana/km-translit";
import { mapIpa } from "./ukrainian-practical.js";
import { segmentKhmerWords, describeWordSegmentation } from "./khmer-word-segmenter.js";
import { renderLatinWord } from "./khmer-romanization-ukrainian.js";

const CONSONANTS = Object.fromEntries(consonants.map((item) => [item.char, item]));
const PRONUNCIATION_SOURCE_STATUSES = new Set(["PRIMARY_PHONETIC_SOURCE", "SPECIALIST_REFERENCE", "SECONDARY_LEXICAL_REFERENCE"]);
const REGISTERED_PRONUNCIATION_SOURCE_IDS = new Set(sources.filter(item => PRONUNCIATION_SOURCE_STATUSES.has(item.status)).map(item => item.id));
const SIGN_BY_CHAR = Object.fromEntries(signs.map((item) => [item.char, item]));
const INDEPENDENT_VOWELS = new Set(signs.filter((item) => item.kind === "independent_vowel").map((item) => item.char));
const VOWEL_SIGNS = new Set(
  signs
    .filter((item) => ["dependent_vowel", "composite_vowel", "vowel_modifier"].includes(item.kind))
    .map((item) => item.char),
);
const COENG = "្";
const ZWNJ = "\u200C";
const ZWSP = "\u200B";
const SHIFTERS = new Set(["៉", "៊"]);
const SHIFTER_ELIGIBILITY = Object.fromEntries(Object.entries(registers.shifter_eligibility).map(([key, values]) => [key === "muusikatoan" ? "៉" : "៊", new Set(values)]));
const PUNCTUATION = /^\s|^\p{P}$/u;
const PROFILES = new Set(["khmer-pph-careful-citation-v1"]);
const FIXTURE_TRIE = (() => {
  const root = { children: new Map(), value: null };
  for (const key of Object.keys(fixtures)) {
    let node = root;
    for (const char of key) {
      if (!node.children.has(char)) node.children.set(char, { children: new Map(), value: null });
      node = node.children.get(char);
    }
    node.value = key;
  }
  return root;
})();

const normalize = (text) => text.normalize("NFC");
const isKhmerConsonant = (char) => Object.hasOwn(CONSONANTS, char);

function isSeparator(char) {
  return !char || /\s/u.test(char) || PUNCTUATION.test(char);
}

function startsNewOrthographicSyllable(chars, index) {
  if (!isKhmerConsonant(chars[index]) || index === 0) return false;
  if (chars[index - 1] === COENG) return false;
  // Unicode 18 §16 documents a subscript independent-vowel sequence followed
  // by a coda consonant as one orthographic unit (e.g. ផ្ឯម). Mirror the
  // Python parser's explicit exception rather than splitting after the vowel.
  if (index >= 2 && chars[index - 2] === COENG && INDEPENDENT_VOWELS.has(chars[index - 1])) return false;
  if (chars[index + 1] === COENG) return false;
  const previousKind = SIGN_BY_CHAR[chars[index - 1]]?.kind;
  if (["dependent_vowel", "composite_vowel", "vowel_modifier", "sign"].includes(previousKind)) {
    return isSeparator(chars[index + 1]);
  }
  return true;
}

const isNumeric = (char) => Boolean(char && /\p{N}/u.test(char));
const scriptBucket = (char) => {
  if (!char || char === ZWNJ) return null;
  if (isNumeric(char)) return "number";
  if (/\p{Script=Khmer}/u.test(char)) return "khmer";
  if (/\p{M}/u.test(char)) return null;
  if (/\p{L}/u.test(char)) return "foreign";
  return "other";
};

function isMultiClusterFixture(word) {
  const chars = [...word];
  let clusters = 0;
  for (let index = 0; index < chars.length; index += 1) {
    if (isKhmerConsonant(chars[index]) && chars[index - 1] !== COENG) clusters += 1;
  }
  return clusters >= 2;
}

function tokenize(text) {
  const units = [];
  let current = "";
  let currentBucket = null;
  const chars = [...normalize(text)];

  const flush = () => {
    if (current) {
      if (currentBucket === "khmer") {
        const words = segmentKhmerWords(current);
        words.forEach((word, index) => {
          if (index > 0 || (units.length && units.at(-1) !== " "
              && scriptBucket([...units.at(-1)].at(-1)) === "khmer")) units.push(" ");
          units.push(word);
        });
      } else {
        units.push(current);
      }
      current = "";
    }
    currentBucket = null;
  };

  for (let index = 0; index < chars.length;) {
    const char = chars[index];

    if (char === ZWSP) {
      flush();
      units.push(ZWSP);
      index += 1;
      continue;
    }

    if (PUNCTUATION.test(char)) {
      flush();
      units.push(char);
      index += 1;
      continue;
    }

    if (isNumeric(char)) {
      flush();
      let numeric = "";
      while (index < chars.length && isNumeric(chars[index])) {
        numeric += chars[index];
        index += 1;
      }
      units.push(numeric);
      continue;
    }

    let fixtureKey;
    if (chars[index - 1] !== COENG) {
      let node = FIXTURE_TRIE;
      for (let cursor = index; cursor < chars.length; cursor += 1) {
        node = node.children.get(chars[cursor]);
        if (!node) break;
        if (node.value && isMultiClusterFixture(node.value)
            && (isSeparator(chars[cursor + 1]) || isKhmerConsonant(chars[cursor + 1]))) fixtureKey = node.value;
      }
    }

    if (fixtureKey) {
      flush();
      const previous = units.at(-1);
      if (previous && scriptBucket([...previous].at(-1)) === "khmer"
          && scriptBucket([...fixtureKey][0]) === "khmer") units.push(" ");
      units.push(fixtureKey);
      index += [...fixtureKey].length;
      continue;
    }

    const bucket = scriptBucket(char) ?? currentBucket ?? "other";
    if (current && currentBucket !== null && bucket !== currentBucket) flush();
    if (!current) currentBucket = bucket;

    current += char;
    index += 1;
  }
  flush();
  return units;
}

function resolveRegister(base, raw) {
  const structural = [...raw].filter((char) => char !== ZWNJ);
  const positions = structural.flatMap((char, index) => SHIFTERS.has(char) ? [index] : []);
  if (!positions.length) return { register: base.register, rule: null, status: "ESTABLISHED_STRUCTURE" };
  if (positions.length > 1) return { register: base.register, rule: "MULTIPLE_REGISTER_SHIFTERS", status: "EVIDENCE_LIMITED" };
  if (positions[0] !== 1) return { register: base.register, rule: "MISPLACED_REGISTER_SHIFTER", status: "EVIDENCE_LIMITED" };
  const shifter = structural[positions[0]];
  if (!SHIFTER_ELIGIBILITY[shifter]?.has(base.char)) return { register: base.register, rule: "NON_STANDARD_SHIFTER_USE", status: "EVIDENCE_LIMITED" };
  if (base.char === "ប" && shifter === "៉") return { register: "first", rule: "BA_TO_PA_EXCEPTION", status: "ESTABLISHED_STRUCTURE" };
  if (shifter === "៉" && base.register === "second") return { register: "first", rule: "MUUSIKATOAN", status: "ESTABLISHED_STRUCTURE" };
  if (shifter === "៊" && base.register === "first") return { register: "second", rule: "TRIISAP", status: "ESTABLISHED_STRUCTURE" };
  return { register: base.register, rule: "NON_STANDARD_SHIFTER_USE", status: "EVIDENCE_LIMITED" };
}


function scanOrthographicComponents(raw) {
  const chars = [...raw];
  const dependentVowels = new Set(signs.filter((item) => ["dependent_vowel", "composite_vowel"].includes(item.kind)).map((item) => item.char));
  const shifters = new Set(signs.filter((item) => item.kind === "register_shifter").map((item) => item.char));
  const components = [];
  const notes = [];
  let baseCount = 0;
  let unsupported = false;

  const add = (role, text, start, status = "RECOGNIZED") => components.push({
    role, text, start, end: start + [...text].length,
    codepoints: [...text].map((char) => "U+" + char.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")),
    status,
  });

  for (let index = 0; index < chars.length;) {
    const char = chars[index];
    if (char === COENG) {
      const sub = chars[index + 1];
      if (sub && (isKhmerConsonant(sub) || INDEPENDENT_VOWELS.has(sub))) {
        add("SUBSCRIPT", char + sub, index);
        index += 2;
        continue;
      }
      add("UNSUPPORTED", char, index, "MALFORMED_COENG");
      notes.push("Malformed COENG at code-point offset " + index + ".");
      unsupported = true;
      index += 1;
      continue;
    }
    if (isKhmerConsonant(char) || INDEPENDENT_VOWELS.has(char)) {
      baseCount += 1;
      add("BASE", char, index, baseCount === 1 ? "RECOGNIZED" : "AMBIGUOUS_BASE_ROLE");
    } else if (char === "\u17CC") {
      add("ROBAT", char, index);
    } else if (shifters.has(char)) {
      add("SHIFTER", char, index);
    } else if (char === ZWNJ || char === "\u200D") {
      add("FORMAT_CONTROL", char, index);
    } else if (dependentVowels.has(char)) {
      add("VOWEL", char, index);
    } else if (SIGN_BY_CHAR[char] && !["unmodeled_letter", "structural"].includes(SIGN_BY_CHAR[char].kind)) {
      add("OTHER_SIGN", char, index);
    } else {
      add("UNSUPPORTED", char, index, "UNMODELED_CHARACTER");
      notes.push("Unmodeled character U+" + char.codePointAt(0).toString(16).toUpperCase().padStart(4, "0") + " at code-point offset " + index + ".");
      unsupported = true;
    }
    index += 1;
  }

  let status;
  if (!chars.length || baseCount === 0) {
    status = "INVALID_OR_UNSUPPORTED";
    if (!chars.length) notes.push("Empty input has no Khmer orthographic base.");
    else notes.push("No modeled Khmer consonant or independent-vowel base was found.");
  } else if (unsupported) {
    status = "INVALID_OR_UNSUPPORTED";
  } else if (baseCount > 1) {
    status = "EVIDENCE_LIMITED";
    notes.push("Multiple un-subscripted base letters occur in one supplied span; the scanner preserves them but does not decide coda versus syllable boundary.");
  } else {
    status = "ESTABLISHED_STRUCTURE";
  }
  return { schema: "khmer-orthographic-components/v1", source_text: raw, offset_unit: "unicode_code_point", status, notes, components };
}

function parseSyllable(raw) {
  const orthographic_structure = scanOrthographicComponents(raw);
  const chars = [...raw];
  if (!chars.length) return { status: "NOT_ESTABLISHED", raw, orthographic_structure };
  const first = chars[0];
  const unknownCodepoints = (values) => values.map((char) => "U+" + char.codePointAt(0).toString(16).toUpperCase().padStart(4, "0"));
  if (!isKhmerConsonant(first)) {
    if (first === COENG || SHIFTERS.has(first)) {
      return { status: "INVALID_OR_UNSUPPORTED", raw, unknown: [], unknown_codepoints: [], reason: "Khmer combining structure cannot begin a standalone orthographic unit.", orthographic_structure };
    }
    if (INDEPENDENT_VOWELS.has(first)) {
      return {
        status: "ESTABLISHED_STRUCTURE", raw, base: null, register: null,
        subscripts: [], subscript_independent_vowels: [], additionalConsonants: [],
        vowelSigns: [], independent_vowel: first, unknown: [],
        graphemes: [{ text: first, kind: "independent_vowel" }],
        onset_ipa: null, orthographic_structure,
      };
    }
    if (SIGN_BY_CHAR[first]) return { status: "NOT_ESTABLISHED", raw, unknown: [], unknown_codepoints: [], reason: "Відомий знак без базового приголосного; його вимову окремо не встановлено.", orthographic_structure };
    return { status: "INVALID_OR_UNSUPPORTED", raw, unknown: chars, unknown_codepoints: unknownCodepoints(chars), reason: "Немає підтримуваного кмерського базового приголосного або відомого знака: " + unknownCodepoints(chars).join(", ") + ".", orthographic_structure };
  }
  let index = 1;
  const base = first;
  const subscripts = [];
  const subscriptIndependentVowels = [];
  const additionalConsonants = [];
  const vowelSigns = [];
  const unknown = [];
  const graphemes = [{ text: base, kind: "consonant" }];

  while (index < chars.length) {
    const char = chars[index];
    if (char === ZWNJ) {
      graphemes.push({ text: char, kind: "format_control" });
      index += 1;
      continue;
    }
    if (char === COENG) {
      const sub = chars[index + 1];
      if (!sub || (!isKhmerConsonant(sub) && !INDEPENDENT_VOWELS.has(sub))) {
        return {
          status: "INVALID_OR_UNSUPPORTED", raw, base,
          subscripts, subscript_independent_vowels: subscriptIndependentVowels,
          additionalConsonants, vowelSigns, unknown: sub ? [COENG, sub] : [COENG],
          unknown_codepoints: unknownCodepoints(sub ? [COENG, sub] : [COENG]),
          graphemes: [...graphemes, ...chars.slice(index).map((text) => ({ text, kind: "invalid_sequence_component" }))],
          reason: "Malformed coeng sequence: " + unknownCodepoints(sub ? [COENG, sub] : [COENG]).join(", ") + ".",
          orthographic_structure,
        };
      }
      if (isKhmerConsonant(sub)) {
        subscripts.push(sub);
        graphemes.push({ text: COENG + sub, kind: "subscript" });
      } else {
        subscriptIndependentVowels.push(sub);
        graphemes.push({ text: COENG + sub, kind: "subscript_independent_vowel" });
      }
      index += 2;
      continue;
    }
    if (isKhmerConsonant(char)) {
      // A conservative orthographic unit may contain more than one base
      // consonant before a validated syllable boundary is available. Preserve
      // known consonants as structure; never mislabel them as unknown glyphs.
      additionalConsonants.push(char);
      graphemes.push({ text: char, kind: "consonant" });
    } else {
      if (VOWEL_SIGNS.has(char)) vowelSigns.push(char);
      else if (!SIGN_BY_CHAR[char]) unknown.push(char);
      graphemes.push({ text: char, kind: SIGN_BY_CHAR[char]?.kind ?? "unknown" });
    }
    index += 1;
  }

  // Unknown characters must not inherit a supported structural status from
  // the recognized base consonant. Match the Python parser's fail-closed rule.
  if (unknown.length) {
    return {
      status: "INVALID_OR_UNSUPPORTED", raw, base, subscripts, additionalConsonants, vowelSigns,
      unknown, unknown_codepoints: unknownCodepoints(unknown), graphemes,
      reason: "Unknown character(s) inside Khmer orthographic unit: " + unknownCodepoints(unknown).join(", ") + ".", orthographic_structure,
    };
  }
  const register = resolveRegister(CONSONANTS[base], raw);
  return {
    status: register.status,
    raw,
    base,
    register: register.register,
    register_rule: register.rule,
    subscripts,
    subscript_independent_vowels: subscriptIndependentVowels,
    additional_consonants: additionalConsonants,
    syllabification_status: additionalConsonants.length ? "NOT_ESTABLISHED" : "NOT_ASSESSED",
    vowelSigns,
    unknown,
    graphemes,
    orthographic_structure,
    inherent_vowel: register.register === "first" ? "first-series" : register.register === "second" ? "second-series" : null,
    onset_ipa: base === "ប" && register.rule === "BA_TO_PA_EXCEPTION" ? "p" : CONSONANTS[base].onset_ipa,
  };
}

function renderIpaProfile(ipa, profile) {
  if (!PROFILES.has(profile)) throw new Error("Unsupported pronunciation profile: " + profile);
  // The selected profile is contemporary Phnom Penh careful citation speech.
  // Colloquial /r/-loss is variable and must never be synthesized by a
  // deterministic spelling/IPA regex in this single-profile workflow.
  return ipa;
}

function renderFixture(fixture, profile) {
  if (!PROFILES.has(profile)) throw new Error("Unsupported pronunciation profile: " + profile);
  if (!fixture.ipa) {
    // A withheld full-word fixture must not erase independently supported
    // phonetic material. For evidence-limited register conflicts, preserve
    // only the structurally identifiable onset; never infer the vowel,
    // register realization, coda, tone or complete lexical pronunciation.
    const analysis = fixture.status === "EVIDENCE_LIMITED" ? parseSyllable(fixture.source) : null;
    const onsetIpa = analysis?.status === "EVIDENCE_LIMITED" ? analysis.onset_ipa : null;
    const onsetMapping = onsetIpa ? mapIpa(onsetIpa, practicalPolicy) : null;
    const hasPartialOnset = Boolean(onsetIpa && onsetMapping?.value !== null);
    const partialUkrainian = hasPartialOnset ? onsetMapping.value + "???" : null;
    return {
      source: fixture.source,
      ipa: fixture.status === "NOT_ESTABLISHED" ? "⟦NOT_ESTABLISHED⟧" : "⟦EVIDENCE_LIMITED⟧",
      ua: "⟦НЕВСТАНОВЛЕНО⟧",
      status: fixture.status,
      rule_trace: hasPartialOnset
        ? ["KHMER_LEXICAL_FIXTURE_WITHHELD", "PARTIAL_ONSET_IPA_ONLY"]
        : ["KHMER_LEXICAL_FIXTURE_WITHHELD"],
      note: hasPartialOnset
        ? fixture.note + " Частковий результат: початковий приголосний /" + onsetIpa
          + "/ розпізнано окремо; голосну, регістр, фіналь і тон не встановлено. Знак ??? позначає невстановлений залишок."
        : fixture.note,
      profile,
      mapping_check: null,
      evidence: fixture.evidence ?? [],
      source_locator: fixture.source_locator ?? null,
      ...(hasPartialOnset ? {
        analysis,
        phonology_evidence: CONSONANTS[analysis.base]?.evidence ?? [],
        provisional_ipa: onsetIpa,
        provisional_ukrainian: partialUkrainian,
        partial_ipa: onsetIpa,
        partial_candidate_kind: "ONSET_ONLY",
      } : {}),
    };
  }

  const sourceIpa = fixture.ipa.replace(/^\//, "").replace(/\/$/, "");
  const ipa = renderIpaProfile(sourceIpa, profile);
  const mapped = mapIpa(ipa, practicalPolicy);
  const agrees = mapped.value !== null && mapped.value === fixture.ua;

  if (!agrees) {
    return {
      source: fixture.source,
      ipa: "/" + ipa + "/",
      ua: mapped.value ?? "⟦НЕВСТАНОВЛЕНО⟧",
      status: "EVIDENCE_LIMITED",
      rule_trace: ["KHMER_LEXICAL_FIXTURE", "IPA_TO_UKRAINIAN_LONGEST_MATCH", "LEXICAL_TARGET_CONFLICT"],
      note: "УВАГА: лексична українська форма не збігається з канонічною IPA → українська політикою. Суперечливий override не використовується; показано канонічний результат політики.",
      profile,
      mapping_check: { policy_render: mapped.value, lexical_render: fixture.ua ?? null, agrees: false },
      evidence: fixture.evidence ?? [],
      source_locator: fixture.source_locator ?? null,
    };
  }

  return {
    source: fixture.source,
    ipa: "/" + ipa + "/",
    ua: mapped.value,
    status: fixture.status,
    rule_trace: ["KHMER_LEXICAL_FIXTURE", "IPA_TO_UKRAINIAN_LONGEST_MATCH"],
    note: fixture.note + " Профіль: " + profile + ".",
    profile,
    mapping_check: fixture.ua ? { policy_render: mapped.value, lexical_render: fixture.ua, agrees: true } : null,
    evidence: fixture.evidence ?? [],
      source_locator: fixture.source_locator ?? null,
  };
}

function deriveDeterministicIpa(analysis) {
  if (analysis.status === "INVALID_OR_UNSUPPORTED") return null;
  if (analysis.subscripts?.length || analysis.subscript_independent_vowels?.length || analysis.additional_consonants?.length || analysis.vowelSigns?.length || analysis.unknown?.length) return null;
  if (analysis.register_rule === "MULTIPLE_REGISTER_SHIFTERS" || analysis.register_rule === "MISPLACED_REGISTER_SHIFTER" || analysis.register_rule === "NON_STANDARD_SHIFTER_USE") return null;

  const onset = analysis.onset_ipa;
  if (!onset || onset.includes("~")) return null;

  const inherent = analysis.register === "first" ? "ɑː" : "ɔː";
  return onset + inherent;
}

function deriveOrthographicRomanizationFallback(unit) {
  // This is deliberately a separate orthographic route, not a guessed IPA
  // reconstruction. It offers the best existing BGN/PCGN-derived candidate
  // for a complete unit while keeping phonetic status unresolved.
  const latin = khmerToLatin(unit);
  if (!latin || /[\p{Script=Khmer}]/u.test(latin)) return null;
  const rendered = renderLatinWord(latin);
  if (!rendered.text || rendered.unsupported > 0 || /[⟦\p{Script=Khmer}]/u.test(rendered.text)) return null;
  return rendered.text;
}

function renderUnknownUnit(unit, profile) {
  const analysis = parseSyllable(unit);
  if (analysis.status === "INVALID_OR_UNSUPPORTED") {
    return {
      source: unit,
      ipa: "⟦INVALID_OR_UNSUPPORTED⟧",
      ua: "⟦НЕПІДТРИМУЄТЬСЯ⟧",
      status: "INVALID_OR_UNSUPPORTED",
      rule_trace: ["KHMER_UNICODE_VALIDATION_FAILED"],
      note: analysis.reason ?? "Некоректна або непідтримувана Unicode-послідовність.",
      analysis,
      profile,
    };
  }

  const derivedIpa = deriveDeterministicIpa(analysis);
  if (derivedIpa) {
    const profiledIpa = renderIpaProfile(derivedIpa, profile);
    const mapped = mapIpa(profiledIpa, practicalPolicy);
    if (mapped.value !== null) {
      return {
        source: unit,
        ipa: "/" + profiledIpa + "/",
        ua: mapped.value,
        status: "PROPOSED",
        rule_trace: ["KHMER_REGISTER_SERIES_INHERENT_VOWEL", "IPA_TO_UKRAINIAN_LONGEST_MATCH"],
        note: "Вимову виведено з документованої структури: базовий приголосний + встановлений регістр/шифтер + притаманна голосна серії. Українська форма є проєктною; результат не є лексичним винятком.",
        analysis,
        profile,
        mapping_check: { policy_render: mapped.value, lexical_render: null, agrees: true },
        evidence: CONSONANTS[analysis.base]?.evidence ?? [],
      };
    }
  }

  // Keep the orthographic candidate available for diagnostics, but never
  // let it pre-empt an independently supported IPA onset hint.
  const orthographicFallback = deriveOrthographicRomanizationFallback(unit);

  // A unit may have a recognized base consonant while its coda, subscript,
  // vowel sequence or syllable boundary remains unresolved. In that case the
  // onset-only preview is still useful and must be surfaced before the
  // orthographic-only fallback.
  if (analysis.onset_ipa && analysis.status !== "INVALID_OR_UNSUPPORTED" && !analysis.unknown?.length) {
    const onsetIpa = renderIpaProfile(analysis.onset_ipa, profile);
    const onsetMapping = mapIpa(onsetIpa, practicalPolicy);
    if (onsetMapping.value !== null) {
      const provisionalUkrainian = onsetMapping.value + "???";
      return {
        source: unit,
        ipa: "⟦NOT_ESTABLISHED⟧",
        ua: "⟦НЕВСТАНОВЛЕНО⟧",
        status: analysis.status === "EVIDENCE_LIMITED" ? "EVIDENCE_LIMITED" : "NOT_ESTABLISHED",
        rule_trace: ["KHMER_STRUCTURE_PARSED", "IPA_NOT_ESTABLISHED", "PARTIAL_ONSET_IPA_ONLY"],
        note: "Повну вимову одиниці не встановлено. Попередній фонетичний результат містить лише початковий приголосний /"
          + onsetIpa + "/; голосну, підрядкові приголосні, фіналь і тон не виведено. ??? позначає невстановлену частину."
          + (orthographicFallback ? " Окремий орфографічний кандидат «" + orthographicFallback + "» не є вимовою." : ""),
        analysis,
        profile,
        provisional_ipa: onsetIpa,
        provisional_ukrainian: provisionalUkrainian,
        partial_ipa: onsetIpa,
        partial_candidate_kind: "ONSET_ONLY",
        unresolved_graphemes: [...unit].slice(1),
        phonology_evidence: (CONSONANTS[analysis.base]?.evidence ?? []).filter((sourceId) => sourceId !== "unicode17-ch16"),
        orthographic_fallback_ukrainian: orthographicFallback,
        fallback_trace: [{
          source: unit,
          position: "onset",
          ipa: onsetIpa,
          ukrainian: provisionalUkrainian,
          rule_id: "KHMER-PREVIEW-ONSET-IPA-V1",
          evidence: (CONSONANTS[analysis.base]?.evidence ?? []).filter((sourceId) => sourceId !== "unicode17-ch16"),
          certainty: "PROVISIONAL",
        }],
      };
    }
  }

  // If no positional IPA hint exists, retain the independent orthographic
  // romanization candidate as a secondary diagnostic only.
  if (orthographicFallback && analysis.status !== "INVALID_OR_UNSUPPORTED") {
    return {
      source: unit,
      ipa: "⟦NOT_ESTABLISHED⟧",
      ua: orthographicFallback,
      status: "NOT_ESTABLISHED",
      rule_trace: ["KHMER_STRUCTURE_PARSED", "IPA_NOT_ESTABLISHED", "BGN_PCNG_ORTHOGRAPHIC_UKRAINIAN_FALLBACK"],
      note: "IPA-вимову для цієї одиниці не встановлено. Показано найкращий доступний попередній український кандидат із BGN/PCGN-похідної романізації; це орфографічна апроксимація, а не підтверджена вимова.",
      analysis,
      profile,
      fallback_status: "PROVISIONAL",
      fallback_ukrainian: orthographicFallback,
      fallback_trace: [{
        source: unit,
        position: "whole-unit",
        ukrainian: orthographicFallback,
        rule_id: "KHMER-BGN-PCGN-ORTHOGRAPHIC-FALLBACK-V1",
        certainty: "PROVISIONAL",
        source_path: "BGN/PCGN-derived ASCII romanization",
      }],
    };
  }

  return {
    source: unit,
    ipa: "⟦NOT_ESTABLISHED⟧",
    ua: "⟦НЕВСТАНОВЛЕНО⟧",
    status: analysis.status === "EVIDENCE_LIMITED" ? "EVIDENCE_LIMITED" : "NOT_ESTABLISHED",
    rule_trace: ["KHMER_STRUCTURE_PARSED", "IPA_NOT_ESTABLISHED"],
    note: "Структуру запису розпізнано, але для цієї одиниці немає достатньо встановленої орфографія → IPA моделі. Система не вгадує вимову.",
    analysis,
    profile,
  };
}

function combineStatus(items) {
  if (!items.length) return "NOT_ESTABLISHED";
  const statuses = new Set(items.map((item) => item.status));
  const invalidCount = items.filter((item) => item.status === "INVALID_OR_UNSUPPORTED").length;
  if (invalidCount > 0 && invalidCount === items.length) return "INVALID_OR_UNSUPPORTED";
  if (invalidCount > 0 || statuses.has("EVIDENCE_LIMITED")) return "EVIDENCE_LIMITED";
  if (statuses.has("NOT_ESTABLISHED")) return "NOT_ESTABLISHED";
  if (statuses.has("PROVISIONAL")) return "PROVISIONAL";
  if (statuses.has("PROPOSED")) return "PROPOSED";
  return "ESTABLISHED_STRUCTURE";
}

function confidenceTier(item) {
  if (item.status === "ADJUDICATED_GOLD" && item.profile_adjudicated === true) return "A";
  if (
    ["PROPOSED", "PROVISIONAL"].includes(item.status) &&
    item.ipa &&
    item.ua &&
    item.source_locator &&
    item.evidence?.some(sourceId => REGISTERED_PRONUNCIATION_SOURCE_IDS.has(sourceId))
  ) return "B";
  if (item.provisional_ipa || item.fallback_status === "PROVISIONAL" || ["EVIDENCE_LIMITED", "PROPOSED", "PROVISIONAL", "ANALYSIS_DEPENDENT"].includes(item.status)) return "C";
  if (["PUNCTUATION", "NON_LINGUISTIC"].includes(item.status)) return "N/A";
  return "D";
}

function getStatusNotice(data) {
  if (!data) return "";
  if (data.selected_external_candidate) {
    return "Показано зовнішній IPA-кандидат від " + data.selected_external_candidate.provider
      + ". Це неперевірений широкофонетичний результат: profile_match=UNVERIFIED, незалежної ад'юдикації немає. ??? наприкінці IPA та українського зіставлення позначає весь результат як PROVISIONAL; інші виходи провайдерів збережено в деталях.";
  }
  if (data.ukrainian_output_kind === "ORTHOGRAPHIC_ROMANIZATION_FALLBACK") {
    return "Український рядок містить попередню орфографічну підказку з романізації, а не підтверджену вимову. ??? позначає невстановлену фонетичну частину; IPA залишається окремо невстановленою.";
  }
  if (data.ukrainian_output_kind === "IPA_DERIVED_PARTIAL") {
    return "Показано лише низькодостовірні IPA-підказки відомих початкових приголосних. Знак ??? позначає невстановлену частину; голосні, фіналі й тон не вгадуються.";
  }
  if (data.status === "PROVISIONAL") {
    return "Показано зовнішній IPA-кандидат зі статусом PROVISIONAL; його профіль не підтверджений незалежною ад'юдикацією.";
  }
  if (data.status === "PROPOSED") {
    return "Результат має статус PROPOSED: IPA та українське читання є дослідницькими пропозиціями для цих записів, а не підтвердженою універсальною моделлю. Перевіряйте джерела й лексичний контекст перед використанням.";
  }
  if (data.status === "EVIDENCE_LIMITED" || data.status === "NOT_ESTABLISHED") {
    return data.note;
  }
  if (data.status === "INVALID_OR_UNSUPPORTED") {
    return "Ввід не підтримується повністю. Перегляньте статус кожної одиниці та не використовуйте маркери непідтвердженого результату як вимову.";
  }
  return "";
}

function convert(text, profile) {
  const normalized = normalize(text);
  if (!normalized.trim()) return null;

  const units = tokenize(normalized);
  const rendered = units.map((unit) => {
    if (unit === ZWSP) return { source: unit, ipa: " ", ua: " ", status: "PUNCTUATION", note: "U+200B ZERO WIDTH SPACE трактовано як невидиму межу слова.", profile };
    if (PUNCTUATION.test(unit)) return { source: unit, ipa: unit, ua: unit, status: "PUNCTUATION", note: "", profile };
    if (/^\p{N}+$/u.test(unit)) return {
      source: unit, ipa: unit, ua: unit, status: "NON_LINGUISTIC",
      note: "Числовий запис збережено без фонетичного читання; вимову чисел не встановлено.",
      rule_trace: ["NON_LINGUISTIC_NUMERAL_PASSTHROUGH"], profile,
    };
    const fixture = fixtures[unit];
    return fixture ? renderFixture(fixture, profile) : renderUnknownUnit(unit, profile);
  });

  rendered.forEach((item) => { item.confidence_tier = confidenceTier(item); });
  const linguistic = rendered.filter((item) => !["PUNCTUATION", "NON_LINGUISTIC"].includes(item.status));
  const analyses = linguistic.map((item) => item.analysis).filter(Boolean);
  const resolved = linguistic.filter((item) => item.status === "PROPOSED");
  const unresolved = linguistic.filter((item) => item.status !== "PROPOSED");
  const unresolvedNames = unresolved.map((item) => item.source).filter(Boolean).slice(0, 12);
  const evidenceLimited = linguistic.filter((item) => item.status === "EVIDENCE_LIMITED").length;
  const notEstablished = linguistic.filter((item) => item.status === "NOT_ESTABLISHED").length;
  const invalid = linguistic.filter((item) => item.status === "INVALID_OR_UNSUPPORTED").length;
  // Keep every unit aligned through the complete IPA-first pipeline. The
  // detailed per-unit records below retain every status, but the public IPA
  // line must not repeat the same abstention token for each unresolved
  // orthographic unit in one uninterrupted Khmer word/run.
  const rawIpa = rendered.map((item) => item.partial_candidate_kind === "ONSET_ONLY"
    ? "/" + item.partial_ipa + "/???"
    : item.ipa).join("");
  const ipa = rawIpa.replace(/(⟦NOT_ESTABLISHED⟧){2,}/gu, "⟦NOT_ESTABLISHED⟧");
  // Lao-style final abstention: retain supported neighbours, but use a clear
  // three-question-mark placeholder for any unresolved linguistic unit.
  // Detailed per-unit diagnostics and provisional hints remain separate.
  const uaParts = [];
  let pendingUnresolved = false;
  const flushUnresolved = () => {
    if (!pendingUnresolved) return;
    uaParts.push("???");
    pendingUnresolved = false;
  };
  for (const item of rendered) {
    if (item.status === "PUNCTUATION") {
      flushUnresolved();
      uaParts.push(item.ua);
      continue;
    }
    if (item.status === "NON_LINGUISTIC") {
      flushUnresolved();
      uaParts.push(item.ua);
      continue;
    }
    if (item.partial_candidate_kind === "ONSET_ONLY") {
      flushUnresolved();
      uaParts.push(item.provisional_ukrainian);
      continue;
    }
    if (item.status === "PROPOSED") {
      flushUnresolved();
      uaParts.push(item.ua);
      continue;
    }
    // A BGN/PCGN-derived fallback is retained on the unit and in the typed
    // diagnostics, but is never folded into the IPA-derived result field.
    pendingUnresolved = true;
  }
  flushUnresolved();
  const ua = uaParts.join("");
  const hasOrthographicFallback = rendered.some((item) =>
    item.partial_candidate_kind !== "ONSET_ONLY"
      && (Boolean(item.orthographic_fallback_ukrainian)
        || (item.fallback_status === "PROVISIONAL" && Boolean(item.fallback_ukrainian)))
  );
  const hasPartialOnset = rendered.some((item) => item.partial_candidate_kind === "ONSET_ONLY");
  const provisionalUaParts = [];
  let pendingProvisionalUnknown = false;
  const flushProvisionalUnknown = () => {
    if (!pendingProvisionalUnknown) return;
    provisionalUaParts.push("???");
    pendingProvisionalUnknown = false;
  };
  for (const item of rendered) {
    if (item.status === "PUNCTUATION" || item.status === "NON_LINGUISTIC") {
      flushProvisionalUnknown();
      provisionalUaParts.push(item.ua);
      continue;
    }
    if (item.status === "PROPOSED") {
      flushProvisionalUnknown();
      provisionalUaParts.push(item.ua);
      continue;
    }
    if (item.partial_candidate_kind === "ONSET_ONLY") {
      flushProvisionalUnknown();
      provisionalUaParts.push(item.provisional_ukrainian);
      continue;
    }
    if (item.fallback_status === "PROVISIONAL" && item.fallback_ukrainian) {
      flushProvisionalUnknown();
      provisionalUaParts.push(item.fallback_ukrainian + "???");
      continue;
    }
    pendingProvisionalUnknown = true;
  }
  flushProvisionalUnknown();
  const provisionalUa = provisionalUaParts.join("");
  const complete = linguistic.length > 0 && linguistic.every((item) =>
    item.status === "PROPOSED" && !/⟦/.test(item.ipa) && !/⟦/.test(item.ua)
  );
  const phoneticResults = rendered.map((item) => ({
    source: item.source,
    status: item.status,
    ipa_kind: ["PUNCTUATION", "NON_LINGUISTIC"].includes(item.status) ? "NOT_APPLICABLE" : "UNRESOLVED",
    rule_trace: item.rule_trace ?? [],
    ipa: item.partial_ipa ?? (item.status !== "PUNCTUATION" && /^\/.*\/$/su.test(item.ipa) ? item.ipa.slice(1, -1) : item.ipa),
    ukrainian: item.partial_candidate_kind === "ONSET_ONLY"
      ? item.provisional_ukrainian
      : (item.orthographic_fallback_ukrainian || item.fallback_ukrainian)
        ? (item.orthographic_fallback_ukrainian || item.fallback_ukrainian) + "???"
        : item.ua,
    ukrainian_kind: item.partial_candidate_kind === "ONSET_ONLY"
      ? "IPA_DERIVED_PROVISIONAL"
      : item.orthographic_fallback_ukrainian || item.fallback_status === "PROVISIONAL"
        ? "ORTHOGRAPHIC_ROMANIZATION_FALLBACK"
        : ["PUNCTUATION", "NON_LINGUISTIC"].includes(item.status)
          ? "NOT_APPLICABLE"
          : item.status === "PROPOSED" ? "IPA_DERIVED" : "UNRESOLVED",
    profile,
    provenance: {
      phonology: item.phonology_evidence ?? item.evidence ?? [],
      structure: item.analysis ? ["unicode17-ch16"] : [],
      target_policy: item.mapping_check || item.partial_candidate_kind === "ONSET_ONLY"
        ? ["data/ukrainian/practical-policy.json"]
        : item.fallback_status === "PROVISIONAL" ? ["src/khmer-romanization-ukrainian.js"] : [],
    },
    uncertainty: ["PUNCTUATION", "NON_LINGUISTIC", "PROPOSED"].includes(item.status)
      ? []
      : [{ status: item.status, note: item.note ?? "", unresolved_graphemes: item.analysis?.graphemes?.slice(1).map((g) => g.text) ?? item.analysis?.unknown ?? [] }],
  }));

  const canonicalStatus = combineStatus(linguistic);
  const providerEntry = provisionalIpaCandidates.entries[normalized] ?? null;
  const externalCandidates = (providerEntry?.candidates ?? []).map((candidate) => {
    const mapping = candidate.profile === profile
      ? mapIpa(candidate.ipa, practicalPolicy)
      : { value: null, unsupported: "PROFILE_MISMATCH" };
    const mappedUkrainian = mapping.value !== null ? mapping.value : null;
    return {
      ...candidate,
      mapped_ukrainian: mappedUkrainian,
      mapping_failure: mapping.unsupported,
      mapping_agrees: candidate.ukrainian_candidate === null
        ? mappedUkrainian === null
        : mappedUkrainian === candidate.ukrainian_candidate,
      selected: false,
    };
  });
  const selectedExternalCandidate = externalCandidates.find((candidate) =>
    candidate.provider === providerEntry?.selected_provider
    && candidate.status === "PROVISIONAL"
    && candidate.profile_match === "UNVERIFIED"
    && candidate.mapped_ukrainian !== null
    && candidate.mapping_agrees
  ) ?? null;
  if (selectedExternalCandidate) selectedExternalCandidate.selected = true;
  const canonicalIpa = ipa;
  const canonicalUa = ua;
  const displayIpa = selectedExternalCandidate
    ? "/" + selectedExternalCandidate.ipa + "/???"
    : canonicalIpa;
  const displayUa = selectedExternalCandidate
    ? selectedExternalCandidate.mapped_ukrainian + "???"
    : hasOrthographicFallback || hasPartialOnset ? provisionalUa : canonicalUa;
  const ukrainianOutputKind = selectedExternalCandidate
    ? "EXTERNAL_IPA_PROVISIONAL"
    : hasOrthographicFallback ? "ORTHOGRAPHIC_ROMANIZATION_FALLBACK"
      : hasPartialOnset ? "IPA_DERIVED_PARTIAL" : "CANONICAL_IPA_DERIVED_OR_UNRESOLVED";
  const displayStatus = selectedExternalCandidate || hasOrthographicFallback || hasPartialOnset
    ? "PROVISIONAL" : canonicalStatus;
  const confidence = selectedExternalCandidate || hasOrthographicFallback || hasPartialOnset
    ? "C"
    : linguistic.length
      ? linguistic.map((item) => item.confidence_tier).sort((a, b) => ({A:0,B:1,C:2,D:3}[b] - {A:0,B:1,C:2,D:3}[a]))[0]
      : "D";
  const wordSegmentation = describeWordSegmentation(units, new Set(Object.keys(fixtures)), normalized);
  const segmentationNote = wordSegmentation.tokens.length
    ? " Сегментація слів: " + wordSegmentation.known_words + " словникових збігів, "
      + wordSegmentation.oov_runs + " невідомих фрагментів; межі є кандидатними, точність не виміряна."
    : "";
  const resultNote = "Локальний аналіз: " + resolved.length + " одиниць мають зафіксовану IPA та проєктну українську форму; "
    + unresolved.length + " потребують окремого встановлення або перевірки (" + notEstablished
    + " не встановлено, " + evidenceLimited + " з обмеженою доказовістю, " + invalid
    + " некоректних/непідтримуваних); " + linguistic.filter((item) => item.fallback_status === "PROVISIONAL").length
    + " мають попередній орфографічний український кандидат; "
    + rendered.filter((item) => item.partial_candidate_kind === "ONSET_ONLY").length
    + " мають окрему IPA-підказку лише для початкового приголосного; "
    + rendered.filter((item) => item.partial_candidate_kind !== "ONSET_ONLY"
      && (Boolean(item.orthographic_fallback_ukrainian)
        || (item.fallback_status === "PROVISIONAL" && Boolean(item.fallback_ukrainian)))).length
    + " мають орфографічну українську підказку, показану з ???. Це не IPA й не підтверджена вимова. Невизначеність IPA збережено."
    + (unresolvedNames.length ? " Невстановлені/проблемні одиниці: " + unresolvedNames.join(" · ") + "." : "");
  const note = selectedExternalCandidate
    ? resultNote + " Додатково показано зовнішній IPA-кандидат від " + selectedExternalCandidate.provider
      + "; profile_match=UNVERIFIED, статус PROVISIONAL. Знак ??? наприкінці позначає неперевіреність; деталі та інші провайдери наведено нижче."
    : resultNote;

  return {
    source: normalized,
    ipa: displayIpa,
    ua: displayUa,
    canonical_ipa: canonicalIpa,
    canonical_ua: canonicalUa,
    canonical_status: canonicalStatus,
    external_candidates: externalCandidates,
    backend_failures: providerEntry?.backend_failures ?? [],
    selected_external_candidate: selectedExternalCandidate,
    complete,
    partial: !complete && (resolved.length > 0 || Boolean(selectedExternalCandidate)
      || hasPartialOnset || hasOrthographicFallback),
    status: selectedExternalCandidate ? "PROVISIONAL" : canonicalStatus,
    display_status: displayStatus,
    ukrainian_output_kind: ukrainianOutputKind,
    confidence_tier: confidence,
    note: note + segmentationNote,
    profile,
    units: rendered,
    word_segmentation: wordSegmentation,
    phonetic_result: {
      schema: "khmer-phonetic-result/v1",
      pipeline: ["source-orthography", "structural-analysis", "source-phonology", "ipa", "ukrainian-target-adaptation"],
      complete,
      partial: !complete && (resolved.length > 0 || hasPartialOnset || hasOrthographicFallback),
      units: phoneticResults,
    },
    analyses,
    vowelModel: vowels.coverage_policy,
  };
}

export { convert, tokenize, parseSyllable, scanOrthographicComponents, mapIpa, getStatusNotice };

