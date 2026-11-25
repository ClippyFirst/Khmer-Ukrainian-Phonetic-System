import assert from "node:assert/strict";
import { test } from "node:test";
import { buildRomanizationIpaCandidate } from "../src/khmer-romanization-ipa.js";

test("confirms a romanized onset only against its source consonant class", () => {
  const result = buildRomanizationIpaCandidate("ខ្មែរ", "khmer");
  assert.equal(result.status, "PROVISIONAL");
  assert.equal(result.typed_ipa.status, "PROVISIONAL");
  assert.deepEqual(result.typed_ipa.segments.map((segment) => segment.ipa), ["kʰ", "?"]);
  assert.equal(result.ukrainian, "к'???");
  assert.ok(result.provenance.includes("PCGN-ONSET-KH"));
});

test("does not accept a romanization token that conflicts with the source onset", () => {
  const result = buildRomanizationIpaCandidate("ក", "kh");
  assert.equal(result.status, "UNRESOLVED");
  assert.equal(result.ukrainian, "???");
});

test("does not guess the context-sensitive PCGN b/p alternation", () => {
  const result = buildRomanizationIpaCandidate("ប", "b");
  assert.equal(result.status, "UNRESOLVED");
  assert.match(result.uncertainty.join(" "), /AMBIGUOUS/u);
});

test("does not infer a vowel from a diacritic-stripped ASCII romanization", () => {
  const result = buildRomanizationIpaCandidate("ខ្មែរ", "khmer");
  assert.equal(result.typed_ipa.phonemic_ipa, null);
  assert.ok(result.typed_ipa.segments.some((segment) => segment.kind === "unknown"));
  assert.ok(result.uncertainty.includes("VOWEL_CODA_AND_SYLLABLE_NOT_ESTABLISHED"));
});

test("does not treat a coeng-only subscript as an independent onset", () => {
  const result = buildRomanizationIpaCandidate("្ក", "k");
  assert.equal(result.status, "UNRESOLVED");
});

test("keeps provenance and explicit uncertainty on every provisional segment", () => {
  const result = buildRomanizationIpaCandidate("ង", "ng");
  assert.equal(result.status, "PROVISIONAL");
  assert.ok(result.typed_ipa.segments.every((segment) => segment.certainty === "PROVISIONAL"));
  assert.ok(result.typed_ipa.segments.every((segment) => segment.provenance.length > 0));
});
