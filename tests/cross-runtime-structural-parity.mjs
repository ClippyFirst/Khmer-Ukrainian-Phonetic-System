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
      onset_ipa: actual.onset_ipa ?? null,
    };
    assert.deepEqual(normalized, expected.syllable, "structural parity mismatch: " + expected.source);
  }
}
console.log("Python ↔ JavaScript structural parity: PASS (" + reference.cases.length + " cases)");
