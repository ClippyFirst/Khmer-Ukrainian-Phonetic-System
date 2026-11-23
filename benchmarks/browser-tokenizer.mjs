import { tokenize } from "../src/khmer-engine-core.js";
import { WORD_DICTIONARY_SIZE } from "../src/khmer-word-segmenter.js";

const input = "ម".repeat(8000);
const measure = (fn, samples = 5) => {
  const timings = [];
  let result = [];
  for (let sample = 0; sample < samples; sample += 1) {
    const start = performance.now();
    result = fn(input);
    timings.push(performance.now() - start);
  }
  const sorted = [...timings].sort((a, b) => a - b);
  return { timings, median: sorted[Math.floor(sorted.length / 2)], result };
};

const measured = measure(tokenize);
const words = measured.result.filter((unit) => unit !== " ");
if (words.length !== input.length || words.join("") !== input) {
  throw new Error("word-segmentation benchmark lost or duplicated source code points");
}
console.log(JSON.stringify({
  benchmark: "khmer-word-segmentation-viterbi-v1",
  code_points: [...input].length,
  word_units: words.length,
  output_units_including_candidate_spaces: measured.result.length,
  inserted_candidate_boundaries: measured.result.length - words.length,
  dictionary_entries: WORD_DICTIONARY_SIZE,
  median_ms: Number(measured.median.toFixed(2)),
  code_points_per_second: Math.round([...input].length / (measured.median / 1000)),
  source_preserved: true,
  note: "Stress microbenchmark of the deterministic dictionary segmenter; not a universal device latency guarantee or segmentation accuracy measure."
}, null, 2));
