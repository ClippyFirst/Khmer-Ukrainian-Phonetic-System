import { performance } from "node:perf_hooks";
import { tokenize } from "../src/khmer-engine-core.js";
import consonants from "../data/khmer/consonants.json" with { type: "json" };
import signs from "../data/khmer/signs.json" with { type: "json" };
import fixtures from "../data/tests/web-fixtures.json" with { type: "json" };

const COENG = "្";
const ZWNJ = "\u200C";
const ZWSP = "\u200B";
const CONSONANTS = new Set(consonants.map((item) => item.char));
const SIGN_BY_CHAR = Object.fromEntries(signs.map((item) => [item.char, item]));
const INDEPENDENT_VOWELS = new Set(signs.filter((item) => item.kind === "independent_vowel").map((item) => item.char));
const PUNCTUATION = /^\s|^\p{P}$/u;
const isSeparator = (char) => !char || /\s/u.test(char) || PUNCTUATION.test(char);
const isNumeric = (char) => Boolean(char && /\p{N}/u.test(char));

function startsNewOrthographicSyllable(chars, index) {
  if (!CONSONANTS.has(chars[index]) || index === 0) return false;
  if (chars[index - 1] === COENG) return false;
  if (index >= 2 && chars[index - 2] === COENG && INDEPENDENT_VOWELS.has(chars[index - 1])) return false;
  if (chars[index + 1] === COENG) return false;
  const previousKind = SIGN_BY_CHAR[chars[index - 1]]?.kind;
  if (["dependent_vowel", "composite_vowel", "vowel_modifier", "sign"].includes(previousKind)) {
    return isSeparator(chars[index + 1]);
  }
  return true;
}

// Reference implementation of the pre-trie tokenizer's repeated remainder
// construction. Kept only in this benchmark to compare like-for-like behavior.
function tokenizeLegacy(text) {
  const units = [];
  let current = "";
  let currentBucket = null;
  const chars = [...text.normalize("NFC")];
  const fixtureKeys = Object.keys(fixtures).sort((a, b) => [...b].length - [...a].length);
  const flush = () => {
    if (current) units.push(current);
    current = "";
    currentBucket = null;
  };
  for (let index = 0; index < chars.length;) {
    const char = chars[index];
    if (char === ZWSP || PUNCTUATION.test(char)) {
      flush();
      units.push(char);
      index += 1;
      continue;
    }
    if (isNumeric(char)) {
      flush();
      let numeric = "";
      while (index < chars.length && isNumeric(chars[index])) numeric += chars[index++];
      units.push(numeric);
      continue;
    }
    const remainder = chars.slice(index).join("");
    const fixtureKey = chars[index - 1] === COENG ? undefined : fixtureKeys.find((key) => {
      if (!remainder.startsWith(key)) return false;
      return isSeparator(chars[index + [...key].length]);
    });
    if (fixtureKey) {
      flush();
      units.push(fixtureKey);
      index += [...fixtureKey].length;
      continue;
    }
    const bucket = char === ZWNJ ? null
      : /\p{N}/u.test(char) ? "number"
        : /\p{Script=Khmer}/u.test(char) ? "khmer"
          : /\p{M}/u.test(char) ? null
            : /\p{L}/u.test(char) ? "foreign" : "other";
    const effectiveBucket = bucket ?? currentBucket ?? "other";
    if (current && currentBucket !== null && effectiveBucket !== currentBucket) flush();
    if (!current) currentBucket = effectiveBucket;
    if (current && effectiveBucket === "khmer" && startsNewOrthographicSyllable(chars, index)) {
      flush();
      currentBucket = "khmer";
    }
    current += char;
    index += 1;
  }
  flush();
  return units;
}

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
const optimized = measure(tokenize);
const legacy = measure(tokenizeLegacy, 3);
if (optimized.result.length !== input.length || optimized.result.join("") !== input
    || JSON.stringify(optimized.result) !== JSON.stringify(legacy.result)) {
  throw new Error("tokenizer benchmark parity/integrity check failed");
}
console.log(JSON.stringify({
  benchmark: "khmer-tokenizer-trie-vs-pre-trie-v1",
  code_points: input.length,
  units: optimized.result.length,
  optimized_ms: optimized.timings.map((value) => Number(value.toFixed(2))),
  optimized_median_ms: Number(optimized.median.toFixed(2)),
  optimized_code_points_per_second: Math.round(input.length / (optimized.median / 1000)),
  legacy_ms: legacy.timings.map((value) => Number(value.toFixed(2))),
  legacy_median_ms: Number(legacy.median.toFixed(2)),
  speedup_ratio: Number((legacy.median / optimized.median).toFixed(1)),
}, null, 2));
