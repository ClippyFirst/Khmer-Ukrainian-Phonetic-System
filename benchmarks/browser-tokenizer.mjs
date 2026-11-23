import { performance } from "node:perf_hooks";
import { tokenize } from "../src/khmer-engine-core.js";

const input = "ម".repeat(30000);
for (let warmup = 0; warmup < 2; warmup += 1) tokenize(input);
const samples = [];
let finalUnits = [];
for (let sample = 0; sample < 5; sample += 1) {
  const start = performance.now();
  finalUnits = tokenize(input);
  samples.push(performance.now() - start);
}
const sorted = [...samples].sort((a, b) => a - b);
const medianMs = sorted[Math.floor(sorted.length / 2)];
if (finalUnits.length !== input.length || finalUnits.join("") !== input) {
  throw new Error("tokenizer benchmark integrity check failed");
}
console.log(JSON.stringify({
  benchmark: "khmer-tokenizer-long-run-v1",
  code_points: input.length,
  units: finalUnits.length,
  samples_ms: samples.map((value) => Number(value.toFixed(2))),
  median_ms: Number(medianMs.toFixed(2)),
  code_points_per_second: Math.round(input.length / (medianMs / 1000)),
}, null, 2));
