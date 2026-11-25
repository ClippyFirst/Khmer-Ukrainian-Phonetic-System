import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { test } from "node:test";
import { buildRomanizationIpaCandidate } from "../src/khmer-romanization-ipa.js";

test("Python and JavaScript romanization-mediated IPA results have exact semantic parity", () => {
  const python = spawnSync("python", ["scripts/export_romanization_ipa_parity.py"], {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
  });
  assert.equal(python.status, 0, python.stderr || python.stdout);
  const expected = JSON.parse(python.stdout);
  const cases = [
    ["ខ្មែរ", "khmer"],
    ["ង", "ng"],
    ["ប", "b"],
    ["ក", "kh"],
    ["្ក", "k"],
  ];
  const actual = cases.map(([source, romanized]) => {
    const result = buildRomanizationIpaCandidate(source, romanized);
    return {
      source,
      romanized,
      status: result.status,
      ukrainian: result.ukrainian,
      romanized_onset: result.romanized_onset,
      typed_ipa: result.typed_ipa,
      provenance: result.provenance,
      uncertainty: result.uncertainty,
    };
  });
  assert.deepEqual(actual, expected);
});
