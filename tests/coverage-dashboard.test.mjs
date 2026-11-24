import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const root = new URL("../", import.meta.url);
const report = JSON.parse(readFileSync(new URL("../reports/khmer-coverage-audit.json", import.meta.url), "utf8"));
const register = JSON.parse(readFileSync(new URL("../data/khmer/vowel-context-register.json", import.meta.url), "utf8"));
const source = readFileSync(new URL("../src/coverage.js", import.meta.url), "utf8");
const page = readFileSync(new URL("../system.html", import.meta.url), "utf8");

assert.match(page, /id="coverage-context-table"/u);
assert.match(page, /id="coverage-context-rows"/u);
assert.match(source, /function renderContextRows\(\)/u);
assert.match(source, /report\.contextual_vowel_evidence\?\.observations/u);
assert.match(source, /textContent/u, "source evidence must be inserted as text, never HTML");
assert.equal(report.contextual_vowel_evidence.observations.length, register.cases.length);
assert.equal(report.contextual_vowel_evidence.cross_product_assessment.status, "NOT_ESTABLISHED");
assert.ok(report.contextual_vowel_evidence.observations.every(row =>
  row.profile === "NOT_SPECIFIED_PER_CASE" &&
  row.phonological_syllable_type === "NOT_ESTABLISHED"
));
console.log("coverage dashboard contextual evidence tests: PASS");
