import assert from "node:assert/strict";
import { test } from "node:test";
import { khmerToLatin } from "@gmana/km-translit";
import onsetInventory from "../data/khmer/romanization_ipa_onsets.json" with { type: "json" };
import consonants from "../data/khmer/consonants.json" with { type: "json" };
import sources from "../data/khmer/sources.json" with { type: "json" };
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

test("real upstream romanizer output is cross-checked before any IPA onset is shown", () => {
  const source = "ខ្មែរ";
  const romanized = khmerToLatin(source);
  const result = buildRomanizationIpaCandidate(source, romanized);
  assert.ok(["PROVISIONAL", "UNRESOLVED"].includes(result.status));
  assert.equal(result.typed_ipa.status, result.status);
  if (result.status === "PROVISIONAL") {
    assert.ok(result.typed_ipa.segments.some((segment) => segment.kind === "unknown"));
    assert.equal(result.typed_ipa.phonemic_ipa, null);
  }
});

test("every executable onset rule has an inspectable PCGN locator and IPA evidence", () => {
  assert.ok(onsetInventory.entries.length >= 18);
  for (const entry of onsetInventory.entries) {
    assert.match(entry.pcgn_source_url, /^https:\/\//u);
    assert.ok(entry.pcgn_source_locator);
    assert.deepEqual(entry.ipa_evidence, ["unicode17-ch16", "r12a-orthography"]);
    assert.match(entry.scope, /base consonant onset only/u);
  }
});

test("every mapped IPA onset equals the repository's source-registered consonant IPA", () => {
  const byChar = Object.fromEntries(consonants.map((item) => [item.char, item]));
  for (const entry of onsetInventory.entries) {
    const bases = entry.source_units.filter((unit) => byChar[unit]);
    assert.ok(bases.length > 0, entry.rule_id + " must include a base consonant");
    for (const base of bases) {
      assert.equal(byChar[base].onset_ipa, entry.ipa, entry.rule_id + " must not invent IPA for " + base);
    }
    assert.ok(entry.source_ids.includes("bgn-pcgn-khmer-1972"));
    assert.ok(sources.some((source) => source.id === "bgn-pcgn-khmer-1972"));
    assert.ok(entry.source_ids.includes("unicode17-ch16"));
    assert.ok(entry.source_ids.includes("r12a-orthography"));
  }
});

test("exact source-aligned representative series vowels produce provisional IPA without a fabricated tail", () => {
  for (const fixture of onsetInventory.representative_syllables) {
    const romanized = khmerToLatin(fixture.source).toLowerCase();
    assert.equal(romanized, fixture.romanization, fixture.source + " upstream PCGN romanization");
    const result = buildRomanizationIpaCandidate(fixture.source, romanized);
    assert.equal(result.status, "PROVISIONAL", fixture.source);
    assert.equal(result.typed_ipa.status, "PROVISIONAL", fixture.source);
    assert.equal(result.typed_ipa.segments.map((segment) => segment.ipa).join(""), fixture.ipa, fixture.source);
    assert.ok(result.typed_ipa.segments.every((segment) => segment.certainty === "PROVISIONAL"));
    assert.ok(result.typed_ipa.segments.every((segment) => segment.kind !== "unknown"));
    assert.ok(result.uncertainty.includes("NOT_GENERALIZED_TO_OTHER_VOWEL_OR_CODA_CONTEXTS"));
  }
});

test("same ASCII romanization can remain distinct when original Khmer series context differs", () => {
  const first = buildRomanizationIpaCandidate("ក", khmerToLatin("ក"));
  const dependent = buildRomanizationIpaCandidate("កា", khmerToLatin("កា"));
  assert.equal(first.status, "PROVISIONAL");
  assert.equal(dependent.status, "PROVISIONAL");
  assert.notEqual(
    first.typed_ipa.segments.map((segment) => segment.ipa).join(""),
    dependent.typed_ipa.segments.map((segment) => segment.ipa).join(""),
  );
});
