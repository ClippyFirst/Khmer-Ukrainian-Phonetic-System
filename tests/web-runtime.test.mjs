import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { convert, parseSyllable, scanOrthographicComponents, tokenize, getStatusNotice } from "../src/main.js";
import { parseOrthographicSyllables } from "../src/orthographic-syllables.js";

const adversarial = "ក គ កា គា កូ គូ កី គី កេ គេ កែ គែ កើ គើ កៅ គៅ ប ប៉ ប៊ ផ ព ត ថ ទ ធ ច ឆ ជ ឈ ស ហ វ";

const phoneticSchema = JSON.parse(readFileSync(new URL("../schemas/phonetic-result.schema.json", import.meta.url), "utf8"));
assert.equal(phoneticSchema.properties.schema.const, "khmer-phonetic-result/v1");
const serviceHtml = readFileSync(new URL("../index.html", import.meta.url), "utf8");
assert.doesNotMatch(serviceHtml, /source-result|source-card/u, "the original Khmer input must not be duplicated as a fourth output card");
assert.match(serviceHtml, /id="mode-phonetic"/u, "the phonetic mode must be selectable");
assert.match(serviceHtml, /id="mode-romanization"/u, "the romanization mode must be selectable");
assert.match(serviceHtml, /data-method-panel="romanization"/u, "romanization output must be isolated from phonetic output");
assert.match(serviceHtml, /data-method-panel="phonetic"/u, "IPA and phonetic Ukrainian output must be isolated");
assert.match(serviceHtml, /id="ua-romanization-status"/u, "an incomplete romanization-to-Ukrainian crosswalk must be explicit, not silently replaced with phonetic output");
const expectedIpa = "/kɑː/ /kɔː/ /kaː/ /kiə/ /koː/ /kuː/ /kəj/ /kiː/ /keː/ /kei/ /kaeː/ /kɛː/ /kɑːə/ /kəː/ /kau/ /kəu/ /ɓɑː/ /paː/ /ɓɔː/ /pʰɑː/ /pɔː/ /tɑː/ /tʰɑː/ /tɔː/ /tʰɔː/ /cɑː/ /cʰɑː/ /cɔː/ /cʰɔː/ /sɑː/ /hɑː/ /ʋɔː/";
const expectedUa = "ка ко ка кіє ко ку кей кі ке кей кае ке кае ке кау кеу ба па бо п'а по та т'а то т'о тьа ть'а тьо ть'о са га во";

const tokens = tokenize(adversarial);
assert.equal(tokens.filter((token) => /\S/u.test(token)).length, 32, "the 32-unit adversarial block must remain 32 orthographic units");

const result = convert(adversarial, "khmer-pph-careful-citation-v1");
assert.ok(result, "adversarial block must produce a result");
assert.equal(result.status, "PROPOSED");
assert.equal(result.ipa, expectedIpa);
assert.equal(result.ua, expectedUa);
assert.equal(result.units.filter((unit) => unit.status !== "PUNCTUATION").length, 32);
assert.ok(result.units.filter((unit) => unit.status !== "PUNCTUATION").every((unit) => unit.status === "PROPOSED"), "no linguistic unit in the 32-item regression block may remain unresolved");

const bySource = Object.fromEntries(result.units.map((unit) => [unit.source, unit]));
assert.deepEqual(
  { ipa: bySource["ប"].ipa, ua: bySource["ប"].ua },
  { ipa: "/ɓɑː/", ua: "ба" },
);
assert.deepEqual(
  { ipa: bySource["ប៉"].ipa, ua: bySource["ប៉"].ua },
  { ipa: "/paː/", ua: "па" },
);
assert.deepEqual(
  { ipa: bySource["ប៊"].ipa, ua: bySource["ប៊"].ua },
  { ipa: "/ɓɔː/", ua: "бо" },
);
assert.deepEqual(
  { ipa: bySource["ផ"].ipa, ua: bySource["ផ"].ua },
  { ipa: "/pʰɑː/", ua: "п'а" },
);

assert.equal(parseSyllable("កx").status, "INVALID_OR_UNSUPPORTED");
assert.deepEqual(parseSyllable("កx").unknown, ["x"]);
assert.equal(parseSyllable("កx").ipa, undefined);
const coengSubscriptFixtureCollision = tokenize("ក្ក");
assert.deepEqual(coengSubscriptFixtureCollision, ["ក្ក"], "a lexical fixture must never split a consonant following COENG from its orthographic base");
const coengSubscriptResult = convert("ក្ក", "khmer-pph-careful-citation-v1");
assert.equal(coengSubscriptResult.units.length, 1);
assert.equal(coengSubscriptResult.units[0].status, "NOT_ESTABLISHED", "a structurally valid cluster without IPA evidence is unresolved, not malformed");

const kingdom = "ព្រះរាជាណាចក្រ";
const kingdomAnalysis = parseSyllable(kingdom);
assert.notEqual(kingdomAnalysis.status, "INVALID_OR_UNSUPPORTED", "the visible Khmer code points in the reported input are all represented in the orthographic inventory");
assert.deepEqual(kingdomAnalysis.unknown, [], "known Khmer graphemes and coeng sequences must not be misreported as unknown");
assert.equal(kingdomAnalysis.graphemes.map((g) => g.text).join(""), kingdom, "the structural trace must account for every source code point");
assert.ok(kingdomAnalysis.additional_consonants.length > 0, "additional known consonants must remain structural rather than being classified as unknown");
assert.equal(kingdomAnalysis.syllabification_status, "NOT_ESTABLISHED", "multiple consonants in one conservative chunk must not trigger guessed syllable boundaries");
const kingdomResult = convert(kingdom, "khmer-pph-careful-citation-v1");
assert.equal(kingdomResult.source, kingdom);
assert.ok(kingdomResult.units.every((unit) => unit.status !== "INVALID_OR_UNSUPPORTED"), "lack of a lexical IPA fixture is NOT_ESTABLISHED, not malformed Unicode");
assert.equal(kingdomResult.complete, false, "structural recognition must not be mistaken for established pronunciation");
const astralUnsupported = parseSyllable("🧪");
assert.deepEqual(astralUnsupported.unknown, ["🧪"], "unsupported supplementary-plane characters must be reported as one code point, not UTF-16 surrogates");
assert.deepEqual(astralUnsupported.unknown_codepoints, ["U+1F9EA"]);

const mixedScriptUnit = convert("កx", "khmer-pph-careful-citation-v1");
assert.equal(mixedScriptUnit.status, "EVIDENCE_LIMITED");
assert.equal(mixedScriptUnit.units.length, 2);
assert.equal(mixedScriptUnit.units[0].source, "ក");
assert.equal(mixedScriptUnit.units[0].status, "PROPOSED");
assert.equal(mixedScriptUnit.units[1].source, "x");
assert.equal(mixedScriptUnit.units[1].status, "INVALID_OR_UNSUPPORTED");
assert.equal(mixedScriptUnit.ipa, "/kɑː/⟦INVALID_OR_UNSUPPORTED⟧");

assert.equal(parseSyllable("ក៊").status, "EVIDENCE_LIMITED");
assert.equal(parseSyllable("គ៉").status, "EVIDENCE_LIMITED");
assert.equal(parseSyllable("ក៊").register_rule, "NON_STANDARD_SHIFTER_USE");

const mixed = convert("ក ☃ គ", "khmer-pph-careful-citation-v1");
assert.equal(mixed.status, "EVIDENCE_LIMITED");
assert.equal(mixed.complete, false);
assert.equal(mixed.partial, true);
assert.equal(mixed.ipa, "/kɑː/ ⟦INVALID_OR_UNSUPPORTED⟧ /kɔː/");
assert.equal(mixed.ua, "ка ⟦НЕПІДТРИМУЄТЬСЯ⟧ ко");
const unresolved = mixed.units.find((x) => x.status === "NOT_ESTABLISHED" || x.status === "INVALID_OR_UNSUPPORTED");
assert.ok(unresolved, "mixed input must isolate an unresolved unit rather than hiding neighboring evidence-backed units");
assert.equal(mixed.units.find((x) => x.source === "ក")?.ua, "ка");
assert.equal(mixed.units.find((x) => x.source === "គ")?.ua, "ко");
assert.equal(mixed.phonetic_result.schema, "khmer-phonetic-result/v1");
assert.equal(mixed.phonetic_result.partial, true);
assert.deepEqual(mixed.phonetic_result.pipeline, ["source-orthography", "structural-analysis", "source-phonology", "ipa", "ukrainian-target-adaptation"]);
assert.equal(mixed.phonetic_result.units[0].ipa, "kɑː", "typed result stores bare IPA, without display delimiters");
assert.equal(mixed.phonetic_result.units[0].ipa_kind, "UNRESOLVED", "the web runtime must not guess a phonemic or phonetic transcription kind before expert approval");
assert.deepEqual(mixed.phonetic_result.units[0].rule_trace, ["KHMER_LEXICAL_FIXTURE", "IPA_TO_UKRAINIAN_LONGEST_MATCH"]);
assert.equal(mixed.phonetic_result.units.length, mixed.units.length);
assert.equal(mixed.phonetic_result.units[0].provenance.phonology[0], "wiktionary:ka", "lexical provenance must remain distinct from structural Unicode provenance");
assert.equal(mixed.phonetic_result.units[1].ipa_kind, "NOT_APPLICABLE", "punctuation has no IPA transcription kind");
assert.equal(mixed.phonetic_result.units[2].ipa_kind, "UNRESOLVED");
assert.equal(mixed.phonetic_result.units[2].uncertainty[0].status, "INVALID_OR_UNSUPPORTED");
assert.ok(phoneticSchema.required.every((key) => Object.hasOwn(mixed.phonetic_result, key)));
assert.ok(phoneticSchema.$defs.unit.required.every((key) => Object.hasOwn(mixed.phonetic_result.units[0], key)));
assert.deepEqual(Object.keys(mixed.phonetic_result.units[0]).sort(), Object.keys(phoneticSchema.$defs.unit.properties).sort());


const mixedScriptNumeralSource = "កLlenguatgeគ៦១១";
const mixedScriptNumeralTokens = tokenize(mixedScriptNumeralSource);
assert.deepEqual(mixedScriptNumeralTokens, ["ក", "Llenguatge", "គ", "៦១១"]);
const mixedScriptNumeralResult = convert(mixedScriptNumeralSource, "khmer-pph-careful-citation-v1");
assert.equal(mixedScriptNumeralResult.units.map((unit) => unit.source).join(""), mixedScriptNumeralSource);
assert.deepEqual(mixedScriptNumeralResult.units.map((unit) => unit.status), [
  "PROPOSED", "INVALID_OR_UNSUPPORTED", "PROPOSED", "NON_LINGUISTIC",
]);
assert.equal(mixedScriptNumeralResult.units[3].ipa, "៦១១");
assert.equal(mixedScriptNumeralResult.units[3].ua, "៦១១");
assert.equal(mixedScriptNumeralResult.phonetic_result.units[3].ipa_kind, "NOT_APPLICABLE");
assert.deepEqual(mixedScriptNumeralResult.phonetic_result.units[3].uncertainty, []);
assert.equal(mixedScriptNumeralResult.ipa, "/kɑː/⟦INVALID_OR_UNSUPPORTED⟧/kɔː/៦១១");
const numeralOnlyResult = convert("៦១១", "khmer-pph-careful-citation-v1");
assert.equal(numeralOnlyResult.status, "NOT_ESTABLISHED");
assert.equal(numeralOnlyResult.complete, false);
assert.equal(numeralOnlyResult.ipa, "៦១១");
assert.equal(numeralOnlyResult.ua, "៦១១");
assert.equal(numeralOnlyResult.phonetic_result.units[0].status, "NON_LINGUISTIC");
assert.equal(numeralOnlyResult.phonetic_result.units[0].ipa_kind, "NOT_APPLICABLE");
console.log("Mixed-script and Khmer numeral boundaries: PASS");

console.log("web-runtime regression tests: PASS");


// Single selected pronunciation profile: careful citation-form Khmer from Phnom Penh.
const selectedProfile = convert("ច្រើន", "khmer-pph-careful-citation-v1");
assert.equal(selectedProfile.ipa, "/craən/");
assert.equal(selectedProfile.ua, "тьраен");
assert.equal(selectedProfile.status, "PROPOSED");
for (const rejectedProfile of ["careful_standard", "phnom_penh_colloquial", "established_form"]) {
  assert.throws(() => convert("ច្រើន", rejectedProfile), /Unsupported pronunciation profile/);
}

assert.deepEqual(tokenize("ប\u200C៊"), ["ប\u200C៊"], "ZWNJ must remain inside its Khmer run");
const zwnj = parseSyllable("ប\u200C៊");
assert.equal(zwnj.register, "second", "ZWNJ must not disrupt register-shifter resolution");
assert.equal(zwnj.register_rule, "TRIISAP");
assert.equal(zwnj.status, "ESTABLISHED_STRUCTURE");

const zeroWidthBoundary = convert("ក\u200Bគ", "khmer-pph-careful-citation-v1");
assert.equal(zeroWidthBoundary.ipa, "/kɑː/ /kɔː/");
assert.equal(zeroWidthBoundary.ua, "ка ко");
assert.equal(zeroWidthBoundary.status, "PROPOSED");

const mixedZeroWidth = tokenize("ក\u200Bគ");
assert.deepEqual(mixedZeroWidth, ["ក", "\u200B", "គ"]);

assert.throws(() => convert("ក", "unsupported_profile"), /Unsupported pronunciation profile/);
assert.equal(convert("   ", "khmer-pph-careful-citation-v1"), null);


const proposedNotice = getStatusNotice(convert("ក", "khmer-pph-careful-citation-v1"));
assert.match(proposedNotice, /PROPOSED/u);
assert.match(proposedNotice, /дослідницькими пропозиціями/u);
assert.equal(getStatusNotice({ status: "ESTABLISHED_STRUCTURE", note: "structure only" }), "");
assert.equal(
  getStatusNotice({ status: "NOT_ESTABLISHED", note: "not enough evidence" }),
  "not enough evidence",
);
assert.match(
  getStatusNotice({ status: "INVALID_OR_UNSUPPORTED", note: "unsupported" }),
  /не підтримується повністю/u,
);

const greetingSentence = "សួស្តី! ខ្ញុំឈ្មោះ សុភា។ ខ្ញុំមកពីប្រទេសកម្ពុជា ហើយខ្ញុំចូលចិត្តរៀនភាសាថ្មីៗ និងអានសៀវភៅ។";
const greetingResult = convert(greetingSentence, "khmer-pph-careful-citation-v1");
assert.equal(greetingResult.source, greetingSentence.normalize("NFC"));
assert.equal(greetingResult.units.map((unit) => unit.source).join(""), greetingSentence.normalize("NFC"));
assert.ok(greetingResult.units.length > 0);
assert.equal(greetingResult.complete, false);
assert.ok(!greetingResult.ipa.includes("⟦ВИМОВУ НЕ ВСТАНОВЛЕНО ДЛЯ ЧАСТИНИ ВВОДУ⟧"));
assert.ok(!greetingResult.ua.includes("⟦ТРАНСКРИПЦІЮ НЕ ВСТАНОВЛЕНО ДЛЯ ЧАСТИНИ ВВОДУ⟧"));
assert.ok(greetingResult.ipa.includes("/kam.pu.ciə/"), "known lexical IPA must survive an unresolved neighboring unit");
assert.ok(greetingResult.ua.includes("кампутьіє"), "known IPA-derived Ukrainian output must survive an unresolved neighboring unit");
assert.ok(greetingResult.ipa.includes("⟦NOT_ESTABLISHED⟧"), "unresolved units must remain explicitly marked in place");
console.log("full Khmer sentence integrity: PASS");

const unicodePunctuation = "ក。គ";
assert.deepEqual(tokenize(unicodePunctuation), ["ក", "。", "គ"]);
const unicodePunctuationResult = convert(unicodePunctuation, "khmer-pph-careful-citation-v1");
assert.equal(unicodePunctuationResult.source, unicodePunctuation);
assert.equal(unicodePunctuationResult.units.map((unit) => unit.source).join(""), unicodePunctuation);
assert.deepEqual(
  unicodePunctuationResult.units.map((unit) => unit.status),
  ["PROPOSED", "PUNCTUATION", "PROPOSED"],
  "Unicode punctuation must separate neighboring Khmer units without downgrading either one",
);
assert.equal(unicodePunctuationResult.ipa, "/kɑː/。/kɔː/");
assert.equal(unicodePunctuationResult.ua, "ка。ко");
console.log("Unicode punctuation boundary preservation: PASS");



const orthographicComponents = scanOrthographicComponents("ខ្ញុំ");
assert.equal(orthographicComponents.schema, "khmer-orthographic-components/v1");
assert.equal(typeof orthographicComponents.source_text, "string");
assert.equal(orthographicComponents.status, "ESTABLISHED_STRUCTURE");
assert.deepEqual(orthographicComponents.components.map((item) => [item.role, item.text, item.start, item.end]), [
  ["BASE", "ខ", 0, 1], ["SUBSCRIPT", "្ញ", 1, 3], ["VOWEL", "ុ", 3, 4], ["OTHER_SIGN", "ំ", 4, 5],
]);
assert.equal(parseSyllable("ខ្ញុំ").orthographic_structure.status, "ESTABLISHED_STRUCTURE");
const ambiguousOrthography = scanOrthographicComponents("សង្គ្រាម");
assert.equal(ambiguousOrthography.status, "EVIDENCE_LIMITED");
assert.ok(ambiguousOrthography.components.some((item) => item.status === "AMBIGUOUS_BASE_ROLE"));
const supplementaryOffset = scanOrthographicComponents("🧪ខ្ញុំ");
assert.deepEqual(supplementaryOffset.components.slice(0, 3).map((item) => [item.start, item.end]), [[0, 1], [1, 2], [2, 4]]);
assert.equal(supplementaryOffset.offset_unit, "unicode_code_point");


const subscriptIndependentVowel = parseSyllable("ផ្ឯម");
assert.deepEqual(subscriptIndependentVowel.subscript_independent_vowels, ["ឯ"]);
assert.deepEqual(subscriptIndependentVowel.subscripts, []);
assert.equal(subscriptIndependentVowel.status, "ESTABLISHED_STRUCTURE");
assert.equal(subscriptIndependentVowel.syllabification_status, "NOT_ESTABLISHED");
assert.equal(subscriptIndependentVowel.orthographic_structure.status, "EVIDENCE_LIMITED");
assert.equal(subscriptIndependentVowel.ipa, undefined, "subscript independent-vowel structure must not manufacture IPA");



// Unicode 18 §16.4 orthographic-syllable grammar parser: structural only.
const grammarExamples = new Map([
  ["ទេ", ["ទេ"]],
  ["ខ្ញុំ", ["ខ្ញុំ"]],
  ["ច្រើន", ["ច្រើ", "ន"]],
  ["សង្គ្រាម", ["ស", "ង្គ្រា", "ម"]],
  ["ហើ្យ", ["ហើ្យ"]],
  ["ហើយ", ["ហើ", "យ"]],
  ["សញ្ញា", ["ស", "ញ្ញា"]],
  ["ស៊ី", ["ស៊ី"]],
  ["ប៉ី", ["ប៉ី"]],
  ["អាយ៌", ["អា", "យ៌"]],
  ["ម៉្ងៃ", ["ម៉្ងៃ"]],
  ["ប‌៊ីយែរ", ["ប‌៊ី", "យែ", "រ"]],
  ["ពត៌មាន", ["ព", "ត៌", "មា", "ន"]],
  ["រាជរ្សី", ["រា", "ជ", "រ្សី"]],
  ["ម៊្ហែត", ["ម៊្ហែ", "ត"]],
  ["វ‌ិទូ", ["វ‌ិ", "ទូ"]],
  ["វ‍ិទូ", ["វ‍ិ", "ទូ"]],
]);
for (const [source, expected] of grammarExamples) {
  const parsed = parseOrthographicSyllables(source);
  assert.equal(parsed.status, "PARSED", "Unicode 18 grammar example must parse: " + source);
  assert.deepEqual(parsed.syllables.map((item) => item.source_text), expected);
  assert.equal(parsed.syllables.map((item) => item.source_text).join(""), source);
  assert.ok(parsed.syllables.every((item) => item.end > item.start));
  assert.ok(parsed.syllables.every((item) => [...item.source_text].length === item.end - item.start));
}
const documentedShifterControl = parseOrthographicSyllables("ប\u200C៊");
assert.equal(documentedShifterControl.status, "PARSED");
assert.deepEqual(documentedShifterControl.syllables[0].grammar_extensions, [
  "U+200C-before-shifter (§16.4.1 textual exception)",
]);
assert.equal(parseOrthographicSyllables("ក្").status, "INVALID_OR_UNSUPPORTED");
assert.equal(parseOrthographicSyllables("កx").status, "INVALID_OR_UNSUPPORTED");
assert.match(parseOrthographicSyllables("កx").rejected_spans[0].reason, /UNMODELED_CHARACTER component/);
assert.match(parseOrthographicSyllables("ក្").rejected_spans[0].reason, /MALFORMED_COENG component/);
for (const unsupported of ["ឣ", "ឤ", "\u17B4", "\u17B5", "\u17D8"]) {
  assert.equal(parseOrthographicSyllables(unsupported).status, "INVALID_OR_UNSUPPORTED");
}
assert.equal(parseOrthographicSyllables("កេិ").status, "EVIDENCE_LIMITED");
assert.deepEqual(parseOrthographicSyllables("កេិ").rejected_spans.map((item) => [item.start, item.end]), [[2, 3]]);
assert.equal(parseOrthographicSyllables("ក\u200Cេ").status, "PARSED");
assert.equal(parseOrthographicSyllables("ក\u200Dេ").status, "PARSED");
assert.equal(parseOrthographicSyllables("ក\u200D៉").status, "EVIDENCE_LIMITED");
assert.equal(parseOrthographicSyllables("ក៌៉").status, "EVIDENCE_LIMITED");
assert.equal(parseOrthographicSyllables("ក្រ៌").status, "PARSED");
const grammarOffsets = parseOrthographicSyllables("ខ្ញុំ");
assert.deepEqual(grammarOffsets.syllables[0].components.map((item) => [item.start, item.end]), [[0, 1], [1, 3], [3, 4], [4, 5]]);
assert.equal(grammarOffsets.grammar_profile, "unicode-18.0.0-ch16.4-plus-ch16.4.1-shifter-control");
console.log("Unicode 18 Khmer orthographic-syllable parser: PASS");



// A single COENG pair can occupy either S production; retain both parse trees.
const ambiguousCoeng = parseOrthographicSyllables("ក្ក");
assert.equal(ambiguousCoeng.status, "AMBIGUOUS");
assert.equal(ambiguousCoeng.parse_count, "2");
assert.equal(ambiguousCoeng.segmentation_count, 1);
assert.equal(ambiguousCoeng.syllables, null);
assert.deepEqual(
  ambiguousCoeng.alternatives[0].syllables[0].grammar_alternatives.map((alternative) => alternative.grammar_roles).sort(),
  [["BASE", "SUBSCRIPT_CLUSTER"], ["BASE", "TRAILING_SUBSCRIPT"]].sort(),
);
assert.deepEqual(
  parseOrthographicSyllables("ខ្ញុំ").syllables[0].grammar_roles,
  ["BASE", "SUBSCRIPT_CLUSTER", "DEPENDENT_VOWEL", "OTHER_SIGN"],
);
assert.deepEqual(
  parseOrthographicSyllables("ហើ្យ").syllables[0].grammar_roles,
  ["BASE", "DEPENDENT_VOWEL", "TRAILING_SUBSCRIPT"],
);
console.log("Unicode 18 Khmer ambiguous grammar parse forest: PASS");



const subscriptIndependentVowelParse = parseOrthographicSyllables("ផ្ឯម");
assert.equal(subscriptIndependentVowelParse.status, "AMBIGUOUS");
assert.equal(subscriptIndependentVowelParse.parse_count, "2");
assert.equal(subscriptIndependentVowelParse.segmentation_count, 1);
assert.deepEqual(
  subscriptIndependentVowelParse.alternatives[0].syllables.map((syllable) => syllable.source_text),
  ["ផ្ឯ", "ម"],
);
assert.deepEqual(
  subscriptIndependentVowelParse.alternatives[0].syllables[0].grammar_alternatives.map((alternative) =>
    alternative.grammar_roles).sort(),
  [["BASE", "SUBSCRIPT_CLUSTER"], ["BASE", "TRAILING_SUBSCRIPT"]].sort(),
);
console.log("Unicode 18 Khmer subscript-independent-vowel ambiguity: PASS");


const manyAmbiguousSyllables = parseOrthographicSyllables("ក្ក".repeat(20));
assert.equal(manyAmbiguousSyllables.status, "AMBIGUOUS");
assert.equal(manyAmbiguousSyllables.parse_count, String(2 ** 20));
assert.equal(manyAmbiguousSyllables.segmentation_count, 1);
assert.equal(manyAmbiguousSyllables.alternatives[0].syllables.length, 20);
assert.ok(manyAmbiguousSyllables.alternatives[0].syllables.every((syllable) =>
  syllable.grammar_alternatives.length === 2));
console.log("Unicode 18 Khmer packed parse forest: PASS");


const repetitionMark = parseOrthographicSyllables("ម៊្ហែតៗ");
assert.equal(repetitionMark.status, "INVALID_OR_UNSUPPORTED");
assert.deepEqual(repetitionMark.rejected_spans.map((item) => [item.start, item.end]), [[6, 7]]);
assert.match(repetitionMark.rejected_spans[0].reason, /UNMODELED_CHARACTER component/);
console.log("Unicode 18 Khmer rejected-span diagnostics: PASS");
