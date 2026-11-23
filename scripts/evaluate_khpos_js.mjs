import fs from "node:fs";
import { createHash } from "node:crypto";
import { tokenize } from "../src/khmer-engine-core.js";

const corpusPath = process.argv[2];
if (!corpusPath) throw new Error("usage: node evaluate_khpos_js.mjs OPEN-TEST.word");

const MARKERS = /[~_^]/gu;
const codePointLength = (value) => [...value].length;
const isKhmerWordToken = (token) => {
  if (!token) return false;
  const chars = [...token];
  return chars.every((char) => {
    const cp = char.codePointAt(0);
    return cp >= 0x1780 && cp <= 0x17ff;
  }) && chars.some((char) => {
    const cp = char.codePointAt(0);
    return cp >= 0x1780 && cp <= 0x17b3;
  });
};

function prepareSentence(line) {
  const tokens = line.trim().split(/\s+/u).filter(Boolean)
    .map((token) => token.replace(MARKERS, "").normalize("NFC"))
    .filter(Boolean);
  const source = tokens.join("");
  const flags = tokens.map(isKhmerWordToken);
  const eligibleCharacters = new Set();
  const goldBoundaries = new Set();
  const goldTokenSpans = new Set();
  const goldKhmerWordSpans = new Set();
  let offset = 0;
  let khmerWordTokens = 0;
  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];
    const start = offset;
    offset += codePointLength(token);
    goldTokenSpans.add(`${start}:${offset}`);
    if (flags[index]) {
      khmerWordTokens += 1;
      goldKhmerWordSpans.add(`${start}:${offset}`);
      for (let position = start; position < offset; position += 1) {
        eligibleCharacters.add(position);
      }
    }
    if (index + 1 < tokens.length && flags[index] && flags[index + 1]) {
      goldBoundaries.add(offset);
    }
  }
  const eligibleBoundaries = new Set();
  const sourceCodePoints = [...source];
  for (let position = 1; position < sourceCodePoints.length; position += 1) {
    if (eligibleCharacters.has(position - 1) && eligibleCharacters.has(position)) {
      eligibleBoundaries.add(position);
    }
  }
  return {
    source,
    goldBoundaries,
    eligibleBoundaries,
    goldTokenSpans,
    goldKhmerWordSpans,
    khmerWordTokens,
  };
}

function spanMetrics(sentences, predictions, field) {
  let gold = 0;
  let predicted = 0;
  let truePositive = 0;
  let exactSentenceMatches = 0;
  for (let index = 0; index < sentences.length; index += 1) {
    const expected = sentences[index][field];
    const actual = predictions[index];
    gold += expected.size;
    predicted += actual.size;
    for (const span of expected) {
      if (actual.has(span)) truePositive += 1;
    }
    if (expected.size === actual.size && [...expected].every((span) => actual.has(span))) {
      exactSentenceMatches += 1;
    }
  }
  const falsePositive = predicted - truePositive;
  const falseNegative = gold - truePositive;
  const precision = predicted ? truePositive / predicted : 0;
  const recall = gold ? truePositive / gold : 0;
  const f1 = precision + recall ? 2 * precision * recall / (precision + recall) : 0;
  return {
    gold,
    predicted,
    true_positive: truePositive,
    false_positive: falsePositive,
    false_negative: falseNegative,
    precision,
    recall,
    f1,
    exact_sentence_matches: exactSentenceMatches,
  };
}

function score(sentences, boundaryPredictions, allTokenPredictions, khmerWordPredictions) {
  const allTokenWordLevel = spanMetrics(sentences, allTokenPredictions, "goldTokenSpans");
  const khmerWordLevel = spanMetrics(sentences, khmerWordPredictions, "goldKhmerWordSpans");

  let gold = 0;
  let predicted = 0;
  let truePositive = 0;
  let exactSentenceMatchesWithGoldBoundaries = 0;
  let sentencesWithGoldBoundaries = 0;
  for (let index = 0; index < sentences.length; index += 1) {
    const expected = sentences[index].goldBoundaries;
    const actual = boundaryPredictions[index];
    gold += expected.size;
    predicted += actual.size;
    for (const boundary of expected) {
      if (actual.has(boundary)) truePositive += 1;
    }
    if (expected.size) {
      sentencesWithGoldBoundaries += 1;
      if (expected.size === actual.size && [...expected].every((x) => actual.has(x))) {
        exactSentenceMatchesWithGoldBoundaries += 1;
      }
    }
  }
  const falsePositive = predicted - truePositive;
  const falseNegative = gold - truePositive;
  const precision = predicted ? truePositive / predicted : 0;
  const recall = gold ? truePositive / gold : 0;
  const f1 = precision + recall ? 2 * precision * recall / (precision + recall) : 0;

  return {
    sentences: sentences.length,
    sentences_with_gold_boundaries: sentencesWithGoldBoundaries,
    khmer_gold_word_tokens: sentences.reduce((sum, sentence) => sum + sentence.khmerWordTokens, 0),
    all_token_word_level: allTokenWordLevel,
    khmer_word_level: khmerWordLevel,
    khmer_boundary_level: {
      gold,
      predicted,
      true_positive: truePositive,
      false_positive: falsePositive,
      false_negative: falseNegative,
      precision,
      recall,
      f1,
      exact_sentence_matches_with_gold_boundaries: exactSentenceMatchesWithGoldBoundaries,
      exact_sentence_match_rate: sentencesWithGoldBoundaries
        ? exactSentenceMatchesWithGoldBoundaries / sentencesWithGoldBoundaries
        : 0,
    },
  };
}

const lines = fs.readFileSync(corpusPath, "utf8")
  .replace(/^\uFEFF/u, "")
  .split(/\r?\n/u)
  .filter((line) => line.length);
const sentences = lines.map(prepareSentence);

const boundaryPredictions = [];
const allTokenPredictions = [];
const khmerWordPredictions = [];
for (const sentence of sentences) {
  const units = tokenize(sentence.source);
  const boundaries = new Set();
  const allTokenSpans = new Set();
  const khmerWordSpans = new Set();
  const reconstructed = [];
  let offset = 0;

  for (const unit of units) {
    if (unit === " ") {
      if (sentence.eligibleBoundaries.has(offset)) boundaries.add(offset);
      continue;
    }
    const start = offset;
    offset += codePointLength(unit);
    reconstructed.push(unit);
    if (unit.length) {
      allTokenSpans.add(`${start}:${offset}`);
      if (isKhmerWordToken(unit)) khmerWordSpans.add(`${start}:${offset}`);
    }
  }
  if (reconstructed.join("") !== sentence.source) {
    throw new Error("JavaScript engine did not losslessly reconstruct khPOS input");
  }
  boundaryPredictions.push(boundaries);
  allTokenPredictions.push(allTokenSpans);
  khmerWordPredictions.push(khmerWordSpans);
}

const predictionRows = sentences.map((_, index) => [
  [...boundaryPredictions[index]].sort((a, b) => a - b),
  [...allTokenPredictions[index]]
    .map((span) => span.split(":").map(Number))
    .sort((a, b) => a[0] - b[0] || a[1] - b[1]),
  [...khmerWordPredictions[index]]
    .map((span) => span.split(":").map(Number))
    .sort((a, b) => a[0] - b[0] || a[1] - b[1]),
]);
const predictionSignature = createHash("sha256")
  .update(JSON.stringify(predictionRows), "utf8")
  .digest("hex");

console.log(JSON.stringify({
  runtime: "javascript",
  corpus_sentences: lines.length,
  prediction_signature: predictionSignature,
  metrics: score(sentences, boundaryPredictions, allTokenPredictions, khmerWordPredictions),
}, null, 2));
