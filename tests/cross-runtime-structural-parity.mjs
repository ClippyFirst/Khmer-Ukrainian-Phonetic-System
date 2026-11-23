import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { parseSyllable, tokenize } from "../src/khmer-engine-core.js";

const python = spawnSync("python", ["scripts/export_structural_parity.py"], {
  encoding: "utf8",
  maxBuffer: 4 * 1024 * 1024,
});
if (python.status !== 0) {
  throw new Error("Python structural reference failed: " + (python.stderr || python.stdout));
}
const reference = JSON.parse(python.stdout);
assert.equal(reference.schema, "khmer-structural-parity-reference/v1");
for (const row of reference.cases) {
  assert.deepEqual(tokenize(row.input), row.tokens, "token boundary mismatch: " + row.input);
  for (const expected of row.units) {
    const actual = parseSyllable(expected.source);
    if (expected.syllable === null) continue;
    const normalized = {
      base_consonant: actual.base ?? null,
      register: actual.register ?? null,
      subscripts: actual.subscripts ?? [],
      subscript_independent_vowels: actual.subscript_independent_vowels ?? [],
      vowel_signs: actual.vowelSigns ?? [],
      independent_vowel: actual.independent_vowel ?? null,
      status: actual.status,
      inherent_vowel: actual.inherent_vowel ?? null,
      register_shifter: actual.register_rule ?? null,
      confidence: actual.status === "ESTABLISHED_STRUCTURE" ? 0.9 : actual.status === "EVIDENCE_LIMITED" ? 0.6 : 0,
      sources: actual.status === "INVALID_OR_UNSUPPORTED" && !actual.base
        ? []
        : ["unicode17-ch16", ...(actual.subscript_independent_vowels?.length ? ["unicode18-ch16"] : [])],
      graphemes: (actual.graphemes ?? []).map((grapheme) => ({
        text: grapheme.text,
        kind: grapheme.kind,
        codepoints: [...grapheme.text].map((char) => "U+" + char.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")),
      })),
      onset_ipa: actual.onset_ipa ?? null,
    };
    assert.deepEqual(normalized, expected.syllable, "structural parity mismatch: " + expected.source);
  }
}
console.log("Python ↔ JavaScript structural parity: PASS (" + reference.cases.length + " cases)");
