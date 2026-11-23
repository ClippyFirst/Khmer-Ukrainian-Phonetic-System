import fs from "node:fs";
import { tokenize } from "../src/khmer-engine-core.js";

const corpusPath = process.argv[2];
if (!corpusPath) throw new Error("usage: node evaluate_khpos_js.mjs OPEN-TEST.word");

const MARKERS = /[~_^]/gu;
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
  const gold = new Set();
  let offset = 0;
  let khmerWordTokens = 0;
  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];
    const start = offset;
    offset += token.length;
    if (flags[index]) {
      khmerWordTokens += 1;
      for (let position = start; position < offset; position += 1) {
        eligibleCharacters.add(position);
      }
    }
    if (index + 1 < tokens.length && flags[index] && flags[index + 1]) {
      gold.add(offset);
    }
  }
  const eligible = new Set();
  for (let position = 1; position < source.length; position += 1) {
    if (eligibleCharacters.has(position - 1) && eligibleCharacters.has(position)) {
      eligible.add(position);
    }
  }
  return { source, gold, eligible, khmerWordTokens };
}

function score(sentences, predictions) {
  let goldTotal = 0;
  let predictedTotal = 0;
  let truePositive = 0;
  let exactWithGold = 0;
  let sentencesWithGold = 0;
  let khmerTokens = 0;
  for (let index = 0; index < sentences.length; index += 1) {
    const sentence = sentences[index];
    const predicted = predictions[index];
    const gold = sentence.gold;
    goldTotal += gold.size;
    predictedTotal += predicted.size;
    for (const boundary of gold) {
      if (predicted.has(boundary)) truePositive += 1;
    }
    khmerTokens += sentence.khmerWordTokens;
    if (gold.size) {
      sentencesWithGold += 1;
      if (gold.size === predicted.size && [...gold].every((x) => predicted.has(x))) {
        exactWithGold += 1;
      }
    }
  }
  const falsePositive = predictedTotal - truePositive;
  const falseNegative = goldTotal - truePositive;
  const precision = predictedTotal ? truePositive / predictedTotal : 0;
  const recall = goldTotal ? truePositive / goldTotal : 0;
  const f1 = precision + recall ? 2 * precision * recall / (precision + recall) : 0;
  return {
    sentences: sentences.length,
    sentences_with_gold_boundaries: sentencesWithGold,
    exact_sentence_matches_with_gold_boundaries: exactWithGold,
    exact_sentence_match_rate: sentencesWithGold ? exactWithGold / sentencesWithGold : 0,
    khmer_gold_word_tokens: khmerTokens,
    gold_boundaries: goldTotal,
    predicted_boundaries: predictedTotal,
    true_positive_boundaries: truePositive,
    false_positive_boundaries: falsePositive,
    false_negative_boundaries: falseNegative,
    boundary_precision: precision,
    boundary_recall: recall,
    boundary_f1: f1,
  };
}

const lines = fs.readFileSync(corpusPath, "utf8").replace(/^\uFEFF/u, "").split(/\r?\n/u).filter((line) => line.length);
const sentences = lines.map(prepareSentence);
const predictions = sentences.map((sentence) => {
  const units = tokenize(sentence.source);
  const predicted = new Set();
  const reconstructed = [];
  let offset = 0;
  for (const unit of units) {
    if (unit === " ") {
      if (sentence.eligible.has(offset)) predicted.add(offset);
    } else {
      reconstructed.push(unit);
      offset += unit.length;
    }
  }
  if (reconstructed.join("") !== sentence.source) {
    throw new Error("JavaScript engine did not losslessly reconstruct khPOS input");
  }
  return predicted;
});

console.log(JSON.stringify({
  runtime: "javascript",
  corpus_sentences: lines.length,
  metrics: score(sentences, predictions),
}, null, 2));
