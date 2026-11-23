import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { convert } from "../src/khmer-engine-core.js";

const python = spawnSync("python", ["scripts/export_segmentation_candidates.py"], {
  encoding: "utf8",
  maxBuffer: 4 * 1024 * 1024,
});
if (python.status !== 0) {
  throw new Error("Python segmentation candidate reference failed: " + (python.stderr || python.stdout));
}
const reference = JSON.parse(python.stdout);
assert.equal(reference.schema, "khmer-segmentation-candidate-parity/v1");
for (const row of reference.cases) {
  const actual = convert(row.input, "khmer-pph-careful-citation-v1");
  assert.ok(actual, "browser engine returned no result for " + row.input);
  assert.deepEqual(
    actual.word_segmentation.candidate_runs,
    row.candidate_runs,
    "Python ↔ JavaScript segmentation candidate parity mismatch: " + row.input,
  );
}
console.log("Python ↔ JavaScript n-best segmentation candidate parity: PASS (" + reference.cases.length + " fixtures)");
