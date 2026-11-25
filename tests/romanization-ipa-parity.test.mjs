import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { test } from "node:test";
import { buildRomanizationIpaCandidate } from "../src/khmer-romanization-ipa.js";
import onsetInventory from "../data/khmer/romanization_ipa_onsets.json" with { type: "json" };

const unlistedVowels = [
  ["កិ","ke"],["គិ","ki"],["កឹ","koe"],["គឹ","koe"],
  ["កឺ","koe"],["គឺ","koe"],["កុ","ko"],["គុ","ku"],
  ["កូ","ko"],["គូ","ku"],["កេ","ke"],["គេ","ke"],
  ["កែ","ke"],["គែ","ke"],["កៃ","kai"],["គៃ","key"],
  ["កោ","kao"],["គោ","ko"],["កៅ","kau"],["គៅ","kou"],
  ["កើ","kaeu"],["គើ","keu"],["កឿ","koea"],["គឿ","koea"],
  ["កួ","kuo"],["គួ","kuo"],
];

test("Python and JavaScript romanization-mediated IPA results have exact semantic parity", () => {
  const python = spawnSync("python", ["scripts/export_romanization_ipa_parity.py"], {
    encoding: "utf8",
    maxBuffer: 1024 * 1024,
  });
  assert.equal(python.status, 0, python.stderr || python.stdout);
  const expected = JSON.parse(python.stdout);
  const cases = [
    ...onsetInventory.entries.map((entry) => [entry.source_units[0], entry.romanization]),
    ...(onsetInventory.representative_syllables ?? []).map((entry) => [entry.source, entry.romanization]),
    ["ប", "b"],
    ["ក", "kh"],
    ["្ក", "k"],
    ...unlistedVowels,
    ["កី", "ki"],
    ["គី", "kei"],
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
