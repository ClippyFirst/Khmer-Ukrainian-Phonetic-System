import { spawnSync } from "node:child_process";
import { performance } from "node:perf_hooks";
import fixtures from "../data/tests/web-fixtures.json" with { type: "json" };
import { convert } from "../src/khmer-engine-core.js";

const inputs = Object.keys(fixtures);
for (let warmup = 0; warmup < 5; warmup += 1) {
  for (const value of inputs) convert(value, "khmer-pph-careful-citation-v1");
}
const rounds = 25;
const samples = [];
for (let round = 0; round < rounds; round += 1) {
  const start = performance.now();
  for (const value of inputs) convert(value, "khmer-pph-careful-citation-v1");
  samples.push(performance.now() - start);
}
samples.sort((a, b) => a - b);
const medianMs = samples[Math.floor(samples.length / 2)];
const python = spawnSync("python", ["scripts/benchmark_python_engine.py"], {
  encoding: "utf8",
  maxBuffer: 1024 * 1024,
});
if (python.status !== 0) throw new Error("Python benchmark failed: " + (python.stderr || python.stdout));
const reference = JSON.parse(python.stdout);
if (reference.fixture_count !== inputs.length) throw new Error("Python and JavaScript benchmark fixture counts differ");
const result = {
  fixture_count: inputs.length,
  rounds,
  javascript: {
    median_ms_per_fixture_batch: Number(medianMs.toFixed(4)),
    fixtures_per_second: Number((inputs.length * 1000 / medianMs).toFixed(2)),
  },
  python: reference,
  js_speedup_over_python: Number((reference.median_ms_per_fixture_batch / medianMs).toFixed(2)),
  note: "Same 36-fixture corpus, warmed runtimes, 25 measured batches. CI microbenchmark, not a universal device latency guarantee.",
};
console.log(JSON.stringify(result, null, 2));
