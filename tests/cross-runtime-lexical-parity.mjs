import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { convert } from "../src/khmer-engine-core.js";

const python = spawnSync("python", ["scripts/export_lexical_parity.py"], {
  encoding: "utf8",
  maxBuffer: 4 * 1024 * 1024,
});
if (python.status !== 0) {
  throw new Error("Python lexical reference failed: " + (python.stderr || python.stdout));
}
const reference = JSON.parse(python.stdout);
assert.equal(reference.schema, "khmer-lexical-parity-reference/v1");
const normalizeIpa = (value) => {
  if (value === null || value === undefined || /^⟦/u.test(value)) return null;
  return /^\/.*\/$/su.test(value) ? value.slice(1, -1) : value;
};
const normalizeUa = (value) => value === null || value === undefined || /^⟦/u.test(value) ? null : value;
for (const row of reference.cases) {
  const actual = convert(row.input, "khmer-pph-careful-citation-v1");
  assert.ok(actual, "browser engine returned no result for " + row.input);
  assert.equal(actual.units.length, row.units.length, "unit count mismatch: " + row.input);
  for (let index = 0; index < row.units.length; index += 1) {
    const expected = row.units[index];
    const unit = actual.units[index];
    assert.deepEqual({
      source: unit.source,
      ipa: normalizeIpa(unit.ipa),
      ukrainian: normalizeUa(unit.ua),
      status: unit.status,
      lexical_mapping_agrees: unit.mapping_check?.agrees ?? null,
    }, expected, "lexical IPA/UA parity mismatch: " + row.input);
  }
}
console.log("Python ↔ JavaScript lexical fixture parity: PASS (" + reference.cases.length + " fixtures)");
