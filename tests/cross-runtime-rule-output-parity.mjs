import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { convert } from "../src/khmer-engine-core.js";

const python = spawnSync("python", ["scripts/export_rule_output_parity.py"], {
  encoding: "utf8",
  maxBuffer: 4 * 1024 * 1024,
});
if (python.status !== 0) throw new Error("Python rule reference failed: " + (python.stderr || python.stdout));
const reference = JSON.parse(python.stdout);
assert.equal(reference.schema, "khmer-rule-output-parity-reference/v1");
const normalizeIpa = (value) => {
  if (value === null || value === undefined || /^⟦/u.test(value)) return null;
  return /^\/.*\/$/su.test(value) ? value.slice(1, -1) : value;
};
for (const expected of reference.cases) {
  const result = convert(expected.source, "khmer-pph-careful-citation-v1");
  assert.ok(result, "browser engine returned no result for " + expected.source);
  assert.equal(result.units.length, 1, "browser unit count mismatch: " + expected.source);
  const unit = result.units[0];
  const actual = {
    source: unit.source,
    ipa: normalizeIpa(unit.ipa),
    status: unit.status,
    rule_trace: unit.rule_trace ?? [],
    confidence_tier: unit.confidence_tier,
    evidence: unit.evidence ?? [],
  };
  if (expected.ipa !== null) actual.ukrainian = unit.ua;
  const normalizedExpected = {
    source: expected.source,
    ipa: expected.ipa,
    status: expected.status,
    rule_trace: expected.rule_trace,
    confidence_tier: expected.confidence_tier,
    evidence: expected.evidence,
  };
  if (expected.ipa !== null) normalizedExpected.ukrainian = expected.ukrainian;
  assert.deepEqual(actual, normalizedExpected, "rule output parity mismatch: " + expected.source);
}
console.log("Python ↔ JavaScript consonant/rule output parity: PASS (" + reference.cases.length + " cases)");
