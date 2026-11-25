import assert from "node:assert/strict";
import {
  parseGooglePhonemic,
} from "../src/google-phonemic-ipa.js";
import {
  adaptPhoneticResult,
  serializePhoneticResult,
} from "../src/khmer-ipa-result.js";

const basic = parseGooglePhonemic("k ɑɑ . k ɔɔ");
assert.equal(basic.ipa, "kɑː.kɔː");
assert.equal(basic.ipa_kind, "PHONEMIC");
assert.equal(basic.status, "PROVISIONAL");
assert.equal(basic.mapping_status, "SOURCE_CORROBORATED");
assert.equal(basic.profile, "khmer-pph-careful-citation-v1");
assert.equal(basic.candidate.ipa_kind, "PHONEMIC");
assert.equal(basic.candidate.phonemic_ipa, "kɑː.kɔː");
assert.equal(basic.candidate.status, "PROVISIONAL");
assert.ok(basic.candidate.segments.every((segment) => segment.certainty === "PROVISIONAL"));
assert.equal(serializePhoneticResult(basic.candidate).ipa_kind, "PHONEMIC");
assert.equal(serializePhoneticResult(basic.candidate).profile, "khmer-pph-careful-citation-v1");
assert.equal(typeof adaptPhoneticResult(basic.candidate), "string");

const diphthong = parseGooglePhonemic("ph ie . s aa");
assert.equal(diphthong.ipa, "pʰiə.saː");
assert.equal(diphthong.mapping_status, "SOURCE_CORROBORATED");
assert.deepEqual(diphthong.syllable_boundaries, [0, 2, 4]);

const provisional = parseGooglePhonemic("th ea");
assert.equal(provisional.ipa, "tʰea");
assert.equal(provisional.mapping_status, "PROVISIONAL");
assert.ok(provisional.uncertainty.includes("UNVERIFIED_PHONE_MAPPING:th"));
assert.ok(provisional.uncertainty.includes("UNVERIFIED_PHONE_MAPPING:ea"));

for (const raw of ["", "   ", ". k", "k .", "k . . ɑɑ", "k sil"]) {
  const result = parseGooglePhonemic(raw);
  assert.equal(result.status, "UNRESOLVED", raw);
  assert.equal(result.ipa, null, raw);
  assert.equal(result.candidate, null, raw);
}

const unknown = parseGooglePhonemic("k xyz");
assert.equal(unknown.status, "UNRESOLVED");
assert.ok(unknown.uncertainty.includes("UNMAPPED_GOOGLE_PHONE:xyz"));

console.log("Google Khmer phonemic → typed IPA adapter: PASS");
