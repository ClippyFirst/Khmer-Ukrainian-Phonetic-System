import assert from "node:assert/strict";
import {
  fromIpa,
  fromProvisionalIpa,
  fromUnknownSourceUnit,
  adaptPhoneticResult,
} from "../src/khmer-ipa-result.js";
import { convert } from "../src/khmer-engine-core.js";

const full = fromIpa("kʰmae", {
  status: "UNCERTAIN",
  provenance: ["wiktionary:khmae"],
  uncertainty: ["profile not independently adjudicated"],
});
assert.equal(full.status, "UNCERTAIN");
assert.equal(full.phonemic_ipa, "kʰmae");
assert.deepEqual(full.segments.map((segment) => segment.ipa), ["kʰ", "m", "a", "e"]);
assert.ok(full.segments.every((segment) => segment.certainty === "UNCERTAIN"));
assert.equal(adaptPhoneticResult(full, { allowUncertain: true }), "к'мае");
assert.equal(full.status, "UNCERTAIN", "target adaptation must not promote confidence");

const provisional = fromProvisionalIpa("k", {
  unresolvedGraphemes: ["្", "ក"],
  provenance: ["KHMER-PREVIEW-ONSET-IPA-V1"],
  uncertainty: ["VOWEL_CODA_AND_SYLLABLE_NOT_ESTABLISHED"],
});
assert.equal(provisional.status, "PROVISIONAL");
assert.equal(provisional.phonemic_ipa, null);
assert.deepEqual(provisional.segments.map((segment) => segment.ipa), ["k", "?"]);
assert.ok(provisional.segments.every((segment) => segment.certainty === "PROVISIONAL"));
assert.equal(adaptPhoneticResult(provisional), "к???");
assert.equal(provisional.tone_category, null);
assert.equal(provisional.tone_contour_ipa, null);

const syllabified = fromIpa("a.ja", { status: "SUPPORTED" });
assert.deepEqual(syllabified.segments.map((segment) => segment.ipa), ["a", ".", "j", "a"]);
assert.deepEqual(syllabified.syllable_boundaries, [0, 1, 2, 4]);

const affricate = fromIpa("t͡s", { status: "SUPPORTED" });
assert.deepEqual(affricate.segments.map((segment) => segment.ipa), ["t͡s"]);
const longVowel = fromIpa("ɑː", { status: "UNCERTAIN" });
assert.deepEqual(longVowel.segments.map((segment) => segment.ipa), ["ɑ", "ː"]);
assert.equal(longVowel.vowel_length, "long");

const tone = fromIpa("k˥", { status: "UNCERTAIN" });
assert.deepEqual(tone.segments.map((segment) => segment.kind), ["consonant", "tone"]);
assert.equal(tone.tone_category, null);
assert.equal(tone.tone_contour_ipa, null);
assert.equal(adaptPhoneticResult(tone, { allowUncertain: true }), null);

const unknown = fromUnknownSourceUnit("☃", {
  provenance: ["KHMER_UNICODE_VALIDATION_FAILED"],
});
assert.equal(unknown.status, "UNRESOLVED");
assert.equal(adaptPhoneticResult(unknown), "???");

const unsupported = fromIpa("kʰɥ", { status: "UNCERTAIN" });
assert.equal(unsupported.status, "UNCERTAIN", "valid IPA remains valid even when the Ukrainian target table lacks a correspondence");
assert.deepEqual(unsupported.segments.map((segment) => segment.ipa), ["kʰ", "ɥ"]);
assert.equal(adaptPhoneticResult(unsupported, { allowUncertain: true }), null);

const lexical = convert("ខ្មែរ", "khmer-pph-careful-citation-v1");
assert.equal(lexical.phonetic_result.units[0].typed_ipa.status, "UNCERTAIN");
assert.equal(lexical.phonetic_result.units[0].ukrainian, "к'мае");
const onset = convert("ក្ក", "khmer-pph-careful-citation-v1");
assert.equal(onset.phonetic_result.units[0].typed_ipa.status, "PROVISIONAL");
assert.equal(onset.phonetic_result.units[0].typed_ipa.phonemic_ipa, null);
assert.equal(onset.phonetic_result.units[0].ukrainian, "к???");
assert.equal(onset.phonetic_result.units[0].ukrainian_kind, "IPA_DERIVED_PROVISIONAL");
assert.equal(onset.phonetic_result.units[0].typed_ipa.tone_category, null);

console.log("Typed IPA result and single Ukrainian adapter contract: PASS");
