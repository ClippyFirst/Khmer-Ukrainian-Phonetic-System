import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { convert, parseSyllable, scanOrthographicComponents, parseOrthographicSyllable, parseOrthographicSequence, tokenize, getStatusNotice } from "../src/main.js";

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
assert.equal(mixedScriptUnit.status, "INVALID_OR_UNSUPPORTED");
assert.equal(mixedScriptUnit.units.length, 1);
assert.equal(mixedScriptUnit.units[0].status, "INVALID_OR_UNSUPPORTED");
assert.equal(mixedScriptUnit.units[0].ipa, "⟦INVALID_OR_UNSUPPORTED⟧");

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
assert.deepEqual(mixed.phonetic_result.units[0].rule_trace, ["KHMER_LEXICAL_FIXTURE", "IPA_TO_UKRAINIAN_LONGEST_MATCH"]);
assert.equal(mixed.phonetic_result.units.length, mixed.units.length);
assert.equal(mixed.phonetic_result.units[0].provenance.phonology[0], "wiktionary:ka", "lexical provenance must remain distinct from structural Unicode provenance");
assert.equal(mixed.phonetic_result.units[2].uncertainty[0].status, "INVALID_OR_UNSUPPORTED");
assert.ok(phoneticSchema.required.every((key) => Object.hasOwn(mixed.phonetic_result, key)));
assert.ok(phoneticSchema.$defs.unit.required.every((key) => Object.hasOwn(mixed.phonetic_result.units[0], key)));
assert.deepEqual(Object.keys(mixed.phonetic_result.units[0]).sort(), Object.keys(phoneticSchema.$defs.unit.properties).sort());

console.log("web-runtime regression tests: PASS");


// Single selected pronunciation profile: careful citation-form Khmer from Phnom Penh.
const selectedProfile = convert("ច្រើន", "khmer-pph-careful-citation-v1");
assert.equal(selectedProfile.ipa, "/craən/");
assert.equal(selectedProfile.ua, "тьраен");
assert.equal(selectedProfile.status, "PROPOSED");
for (const rejectedProfile of ["careful_standard", "phnom_penh_colloquial", "established_form"]) {
  assert.throws(() => convert("ច្រើន", rejectedProfile), /Unsupported pronunciation profile/);
}

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


const bnfCases = ["ខ្ញុំ", "ស៊ី", "ប៉ី", "ក៌", "ផ្ឯ"];
for (const source of bnfCases) assert.equal(parseOrthographicSyllable(source).status, "PARSED", source);
assert.equal(parseOrthographicSyllable("ប‌៊").status, "PARSED");
assert.equal(parseOrthographicSyllable("កា៉").status, "INVALID_ORDER");
assert.equal(parseOrthographicSyllable("កាី").status, "INVALID_ORDER");
assert.equal(parseOrthographicSyllable("ច្រើន").status, "EVIDENCE_LIMITED");
assert.equal(parseOrthographicSyllable("សង្គ្រាម").status, "EVIDENCE_LIMITED");
assert.equal(parseOrthographicSyllable("ក្").status, "INVALID_OR_UNSUPPORTED");


const forestSingle = parseOrthographicSequence("ផ្ឯ");
assert.equal(forestSingle.status, "PARSED");
assert.deepEqual(forestSingle.boundary_alternatives, [[[0, 3]]]);
assert.equal(forestSingle.alternatives.length, 2);
const forestAmbiguous = parseOrthographicSequence("ច្រើន");
assert.equal(forestAmbiguous.status, "EVIDENCE_LIMITED");
assert.deepEqual(forestAmbiguous.boundary_alternatives, [[[0, 4], [4, 5]]]);
assert.equal(forestAmbiguous.selected_alternative, null);
assert.ok(forestAmbiguous.rejected_spans.some((item) => item.start === 4 && item.reason.includes("coda-versus-next-syllable")));
const forestInvalid = parseOrthographicSequence("កាី");
assert.equal(forestInvalid.status, "INVALID_ORDER");
assert.ok(forestInvalid.rejected_spans.length > 0);
assert.equal(forestInvalid.rejected_spans[0].start, 2);
for (const source of ["ខ្ញុំ", "ច្រើន", "សង្គ្រាម", "ហើ្យ", "សញ្ញា", "ស៊ី", "ប៉ី", "ម៉្ងៃ", "ប‌៊ីយែរ", "ផ្ឯម", "អាយ៌", "ពត៌មាន"]) {
  const forest = parseOrthographicSequence(source);
  assert.ok(["PARSED", "EVIDENCE_LIMITED", "AMBIGUOUS"].includes(forest.status), source);
  for (const path of forest.boundary_alternatives) {
    assert.equal(path.map(([start, end]) => [...source].slice(start, end).join("")).join(""), source);
  }
}
