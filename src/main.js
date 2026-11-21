import consonants from "../data/khmer/consonants.json" with { type: "json" };
import registers from "../data/khmer/registers.json" with { type: "json" };
import signs from "../data/khmer/signs.json" with { type: "json" };
import vowels from "../data/khmer/vowels.json" with { type: "json" };
import practicalPolicy from "../data/ukrainian/practical-policy.json" with { type: "json" };
import fixtures from "../data/tests/web-fixtures.json" with { type: "json" };
import { khmerToLatin } from "@gmana/km-translit";
import { mapIpa } from "./ukrainian-practical.js";
import { renderKhmerRomanizationText, renderRomanizedText } from "./khmer-romanization-ukrainian.js";

const CONSONANTS = Object.fromEntries(consonants.map((item) => [item.char, item]));
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

const normalize = (text) => text.normalize("NFC");
const isKhmerConsonant = (char) => Object.hasOwn(CONSONANTS, char);

function isSeparator(char) {
  return !char || /\s/u.test(char) || PUNCTUATION.test(char);
}

function startsNewOrthographicSyllable(chars, index) {
  if (!isKhmerConsonant(chars[index]) || index === 0) return false;
  if (chars[index - 1] === COENG) return false;
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

function tokenize(text) {
  const units = [];
  let current = "";
  let currentBucket = null;
  const chars = [...normalize(text)];
  const fixtureKeys = Object.keys(fixtures).sort((a, b) => [...b].length - [...a].length);

  const flush = () => {
    if (current) {
      units.push(current);
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

    const remainder = chars.slice(index).join("");
    const fixtureKey = chars[index - 1] === COENG ? undefined : fixtureKeys.find((key) => {
      if (!remainder.startsWith(key)) return false;
      const next = chars[index + [...key].length];
      return next === undefined || isSeparator(next);
    });

    if (fixtureKey) {
      flush();
      units.push(fixtureKey);
      index += [...fixtureKey].length;
      continue;
    }

    const bucket = scriptBucket(char) ?? currentBucket ?? "other";
    if (current && currentBucket !== null && bucket !== currentBucket) flush();
    if (!current) currentBucket = bucket;

    if (current && bucket === "khmer" && startsNewOrthographicSyllable(chars, index)) {
      flush();
      currentBucket = "khmer";
    }
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
        return { status: "INVALID_OR_UNSUPPORTED", raw, unknown: sub ? [COENG, sub] : [COENG], unknown_codepoints: unknownCodepoints(sub ? [COENG, sub] : [COENG]), reason: "Malformed coeng sequence: " + unknownCodepoints(sub ? [COENG, sub] : [COENG]).join(", ") + ".", orthographic_structure };
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
    return {
      source: fixture.source,
      ipa: "⟦EVIDENCE_LIMITED⟧",
      ua: "⟦НЕВСТАНОВЛЕНО⟧",
      status: fixture.status,
      rule_trace: ["KHMER_LEXICAL_FIXTURE_WITHHELD"],
      note: fixture.note,
      profile,
      mapping_check: null,
      evidence: fixture.evidence ?? [],
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
      };
    }
  }

  // Last-resort onset-only IPA: the source grapheme is never mapped
  // directly to Ukrainian and no vowel/coda/tone is inferred.
  if (analysis.onset_ipa && analysis.status !== "INVALID_OR_UNSUPPORTED" && !analysis.unknown?.length) {
    const onsetIpa = renderIpaProfile(analysis.onset_ipa, profile);
    const onsetMapping = mapIpa(onsetIpa, practicalPolicy);
    if (onsetMapping.value !== null) {
      return {
        source: unit,
        ipa: "⟦NOT_ESTABLISHED⟧",
        ua: "⟦НЕВСТАНОВЛЕНО⟧",
        status: "NOT_ESTABLISHED",
        rule_trace: ["KHMER_STRUCTURE_PARSED", "IPA_NOT_ESTABLISHED", "ONSET_ONLY_PREVIEW"],
        note: "Канонічну вимову не встановлено. Окрема низькодостовірна підказка містить лише IPA початкового приголосного; голосну, підрядкові приголосні, фіналь і тон не виведено.",
        analysis,
        profile,
        provisional_ipa: onsetIpa,
        provisional_ukrainian: onsetMapping.value + "?",
        unresolved_graphemes: [...unit].slice(1),
        fallback_status: "PROVISIONAL",
        fallback_trace: [{ source: unit, position: "onset", ipa: onsetIpa, ukrainian: onsetMapping.value + "?", rule_id: "KHMER-PREVIEW-ONSET-IPA-V1", certainty: "PROVISIONAL" }],
      };
    }
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
  if (["PROPOSED", "PROVISIONAL"].includes(item.status) && item.ipa && item.ua && item.evidence?.length) return "B";
  if (item.provisional_ipa || ["EVIDENCE_LIMITED", "PROPOSED", "PROVISIONAL", "ANALYSIS_DEPENDENT"].includes(item.status)) return "C";
  if (["PUNCTUATION", "NON_LINGUISTIC"].includes(item.status)) return "N/A";
  return "D";
}

function getStatusNotice(data) {
  if (!data) return "";
  if (data.status === "PROVISIONAL") {
    return "Показано лише низькодостовірні IPA-підказки відомих початкових приголосних. Знак ? позначає невстановлену частину; голосні, фіналі й тон не вгадуються.";
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
  // Keep every unit aligned through the complete IPA-first pipeline. Unknown
  // units retain explicit markers at their own positions; neighboring results
  // are never discarded and the overall status still signals incompleteness.
  const ipa = rendered.map((item) => item.ipa).join("");
  const ua = rendered.map((item) => item.ua).join("");
  const complete = linguistic.length > 0 && linguistic.every((item) =>
    item.status === "PROPOSED" && !/⟦/.test(item.ipa) && !/⟦/.test(item.ua)
  );
  const phoneticResults = rendered.map((item) => ({
    source: item.source,
    status: item.status,
    ipa_kind: ["PUNCTUATION", "NON_LINGUISTIC"].includes(item.status) ? "NOT_APPLICABLE" : "UNRESOLVED",
    rule_trace: item.rule_trace ?? [],
    ipa: item.status !== "PUNCTUATION" && /^\/.*\/$/su.test(item.ipa) ? item.ipa.slice(1, -1) : item.ipa,
    ukrainian: item.ua,
    profile,
    provenance: {
      phonology: item.evidence ?? [],
      structure: item.analysis ? ["unicode17-ch16"] : [],
      target_policy: item.mapping_check ? ["data/ukrainian/practical-policy.json"] : [],
    },
    uncertainty: ["PUNCTUATION", "NON_LINGUISTIC", "PROPOSED"].includes(item.status)
      ? []
      : [{ status: item.status, note: item.note ?? "", unresolved_graphemes: item.analysis?.graphemes?.slice(1).map((g) => g.text) ?? item.analysis?.unknown ?? [] }],
  }));

  return {
    source: normalized,
    ipa,
    ua,
    complete,
    partial: !complete && resolved.length > 0,
    status: combineStatus(linguistic),
    confidence_tier: linguistic.length ? linguistic.map((item) => item.confidence_tier).sort((a, b) => ({A:0,B:1,C:2,D:3}[b] - {A:0,B:1,C:2,D:3}[a]))[0] : "D",
    note: "Локальний аналіз: " + resolved.length + " одиниць мають зафіксовану IPA та проєктну українську форму; "
      + unresolved.length + " потребують окремого встановлення або перевірки (" + notEstablished
      + " не встановлено, " + evidenceLimited + " з обмеженою доказовістю, " + invalid
      + " некоректних/непідтримуваних). Невизначеність позначено на місці відповідної одиниці; сусідні результати збережено."
      + (unresolvedNames.length ? " Невстановлені/проблемні одиниці: " + unresolvedNames.join(" · ") + "." : ""),
    profile,
    units: rendered,
    phonetic_result: {
      schema: "khmer-phonetic-result/v1",
      pipeline: ["source-orthography", "structural-analysis", "source-phonology", "ipa", "ukrainian-target-adaptation"],
      complete,
      partial: !complete && resolved.length > 0,
      units: phoneticResults,
    },
    analyses,
    vowelModel: vowels.coverage_policy,
  };
}

export { convert, tokenize, parseSyllable, scanOrthographicComponents, mapIpa, getStatusNotice };

if (typeof document !== "undefined") {
  const $ = (id) => document.getElementById(id);
  const source = $("source");
  const romanizationResult = $("romanization-result");
  const results = $("results");
  const empty = $("empty");
  const issue = $("issue");
  const live = $("live");
  const modePhonetic = $("mode-phonetic");
  const modeRomanization = $("mode-romanization");
  const outputMethodNote = $("output-method-note");
  let activeMode = "phonetic";

  function setOutputMode(mode) {
    activeMode = mode;
    document.querySelectorAll("[data-method-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.methodPanel !== mode;
    });
    modePhonetic.classList.toggle("is-active", mode === "phonetic");
    modePhonetic.setAttribute("aria-pressed", String(mode === "phonetic"));
    modeRomanization.classList.toggle("is-active", mode === "romanization");
    modeRomanization.setAttribute("aria-pressed", String(mode === "romanization"));
    outputMethodNote.textContent = mode === "phonetic"
      ? "Фонетичний режим: детерміновані правила орфографія → IPA → українська адаптація; непідтверджені форми не вгадуються."
       : "Романізаційний режим: можна ввести кмерський текст (автоматична ASCII-романізація) або готову латинську BGN/PCGN-форму з діакритиками; вводьте один формат за раз. Профіль вимови діє лише у фонетичному режимі. Невідомі фрагменти не вгадуються; IPA-fallback не використовується.";
    render();
  }

  function render() {
    $("count").textContent = `${[...source.value].length} символів`;
    const data = convert(source.value, $("profile").value);
    if (!data) {
      results.hidden = true;
      issue.hidden = true;
      empty.hidden = false;
      return;
    }
    empty.hidden = true;
    results.hidden = false;
    const hasKhmer = [...data.source].some(char => /\p{Script=Khmer}/u.test(char) && /[\p{L}\p{M}]/u.test(char));
    const hasLatin = /\p{Script=Latin}/u.test(data.source);
    const hasMixedScript = hasKhmer && hasLatin;
    const usesKhmerRomanizer = hasKhmer && !hasLatin;
    const latinRomanization = usesKhmerRomanizer ? khmerToLatin(data.source) : data.source;
    romanizationResult.textContent = latinRomanization;
    const uaRomanized = usesKhmerRomanizer
      ? renderKhmerRomanizationText(data.source, khmerToLatin)
      : renderRomanizedText(data.source);
    $("romanization-title").textContent = hasMixedScript
      ? "Змішаний ввід · потрібен один формат"
      : usesKhmerRomanizer
        ? "Романізація · BGN/PCGN-derived ASCII"
        : "Вхідна романізація · BGN/PCGN 1972";
    $("romanization-description").textContent = hasMixedScript
      ? "Одночасний кмерський і латинський текст не підтримується як один профіль; кмерські літери позначено."
      : usesKhmerRomanizer
        ? "Автоматичний латинський запис із кмерського письма; не IPA."
        : "Готовий латинський запис обробляється без повторної романізації.";
    $("romanization-note").textContent = hasMixedScript
      ? "Розділіть кмерський текст і BGN/PCGN-романізацію на окремі запуски."
      : usesKhmerRomanizer
        ? "Пакет @gmana/km-translit 0.1.2 відкидає діакритики BGN/PCGN; контекстні голосні не можна відновити однозначно."
        : "Діакритичні форми BGN/PCGN підтримуються за таблицею; невідомі латинські фрагменти залишаються в ⟦…⟧. Українські відповідники — проєктні кандидати.";
    $("ua-romanization-result").textContent = uaRomanized.text || "—";
    $("ua-romanization-status").textContent = uaRomanized.status === "PROVISIONAL"
      ? usesKhmerRomanizer
        ? "PROVISIONAL · буквена передача з ASCII-результату; пакет відкидає BGN/PCGN діакритики, тому контекстні голосні не можна відновити однозначно."
        : "PROVISIONAL · пряма передача з BGN/PCGN-романізації; українські відповідники мають статус проєктних кандидатів."
      : uaRomanized.status === "PARTIAL"
        ? "PARTIAL · зіставлено " + uaRomanized.mapped + " фрагм.; " + uaRomanized.unsupported + " непідтримуваних фрагм. позначено в ⟦…⟧."
        : "PASSTHROUGH · латинських фрагментів для романізації немає; сторонній текст збережено.";
    $("ipa-result").textContent = data.ipa;
    $("ua-result").textContent = data.ua;
    $("status").textContent = data.status.replaceAll("_", " ") + " · доказовий рівень " + data.confidence_tier;
    $("details").textContent = data.note;
    const unitDetails = $("unit-details");
    unitDetails.replaceChildren();
    const unitHeading = document.createElement("h3");
    unitHeading.textContent = "Одиничний аналіз";
    unitDetails.append(unitHeading);
    data.units.filter((unit) => unit.status !== "PUNCTUATION").forEach((unit) => {
      const card = document.createElement("article");
      card.className = "unit-detail";
      card.dataset.fallbackRuleId = unit.fallback_trace?.[0]?.rule_id ?? "";
      card.dataset.fallbackPosition = unit.fallback_trace?.[0]?.position ?? "";
      const heading = document.createElement("div");
      heading.className = "unit-detail-heading";
      const sourceLabel = document.createElement("strong");
      sourceLabel.className = "unit-source";
      sourceLabel.lang = "km";
      sourceLabel.textContent = unit.source;
      const statusLabel = document.createElement("span");
      statusLabel.className = "unit-status";
      statusLabel.textContent = unit.status.replaceAll("_", " ") + " · рівень " + unit.confidence_tier;
      heading.append(sourceLabel, statusLabel);
      const values = document.createElement("p");
      values.className = "unit-values";
      values.textContent = "IPA: " + unit.ipa + " · Українська: " + unit.ua
        + (unit.provisional_ipa ? " · Попередня підказка: " + unit.provisional_ipa + " → " + unit.provisional_ukrainian + " [PROVISIONAL]" : "");
      const note = document.createElement("p");
      note.className = "unit-note";
      note.textContent = unit.note || "Окремого пояснення для цієї одиниці немає.";
      card.append(heading, values, note);
      unitDetails.append(card);
    });
    unitDetails.hidden = activeMode !== "phonetic" || data.units.every((unit) => unit.status === "PUNCTUATION");
    const notice = getStatusNotice(data);
    issue.hidden = activeMode !== "phonetic" || !notice;
    if (!issue.hidden) {
      $("issue-text").textContent = notice;
      $("issue").querySelector("strong").textContent =
        data.status === "PROPOSED" ? "Результат попередній" : "Результат потребує обережності";
    }
    live.textContent = "Результат оновлено";
  }
  
  modePhonetic.addEventListener("click", () => setOutputMode("phonetic"));
  modeRomanization.addEventListener("click", () => setOutputMode("romanization"));
  setOutputMode("phonetic");
  source.addEventListener("input", render);
  $("profile").addEventListener("change", render);
  $("example").addEventListener("click", () => {
    source.value = fixtures["ភាសាខ្មែរ"] ? "ភាសាខ្មែរ" : Object.keys(fixtures)[0];
    render();
    source.focus();
  });
  $("clear").addEventListener("click", () => {
    source.value = "";
    render();
    source.focus();
  });
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      const element = $(button.dataset.copy);
      try {
        const copyText = "value" in element ? element.value : element.textContent;
        await navigator.clipboard.writeText(copyText);
        const old = button.textContent;
        button.textContent = "Скопійовано";
        window.setTimeout(() => { button.textContent = old; }, 900);
      } catch {
        live.textContent = "Не вдалося скопіювати автоматично. Виділіть результат і скопіюйте вручну.";
      }
    });
  });
  
}
