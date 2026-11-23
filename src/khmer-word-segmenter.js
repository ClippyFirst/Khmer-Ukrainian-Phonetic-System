import dataset from "../data/khmer/google-pronunciation-sample.json" with { type: "json" };

export const WORD_SEGMENTER_ID = "google-khmer-pronunciation-frequency-viterbi-sample-v1";
export const WORD_DICTIONARY_SIZE = dataset.entries.length;
const COENG = "\u17D2";
const MAX_CLUSTERS = 12;
const entries = new Map(dataset.entries.map(({ word, count }) => [word, Number(count)]));
const totalCount = [...entries.values()].reduce((sum, count) => sum + count, 0);
const denominator = totalCount + entries.size + 1;
const costs = new Map([...entries].map(([word, count]) => [
  word,
  -Math.log((count + 1) / denominator),
]));
const unknownCost = -Math.log(1 / denominator) + 4;
const prefixes = new Set();

function isKhmerBase(char) {
  const cp = char?.codePointAt(0) ?? -1;
  return cp >= 0x1780 && cp <= 0x17B3;
}

function clusterStarts(text) {
  const chars = [...text];
  const bounds = [0];
  for (let index = 1; index < chars.length; index += 1) {
    if (isKhmerBase(chars[index]) && chars[index - 1] !== COENG) bounds.push(index);
  }
  bounds.push(chars.length);
  return { chars, bounds };
}

for (const word of entries.keys()) {
  const { chars, bounds } = clusterStarts(word);
  for (let index = 1; index < bounds.length; index += 1) {
    prefixes.add(chars.slice(0, bounds[index]).join(""));
  }
}

export function isKnownKhmerWord(word) {
  return entries.has(word);
}

export function segmentKhmerWordsDetailed(text) {
  if (!text) return [];
  const { chars, bounds } = clusterStarts(text);
  const count = bounds.length - 1;
  const best = Array(count + 1).fill(Number.POSITIVE_INFINITY);
  const back = Array(count + 1).fill(null);
  best[0] = 0;

  for (let start = 0; start < count; start += 1) {
    if (!Number.isFinite(best[start])) continue;
    const unknownCandidate = best[start] + unknownCost;
    if (unknownCandidate < best[start + 1]) {
      best[start + 1] = unknownCandidate;
      back[start + 1] = { previous: start, known: false };
    }

    for (let end = start + 1; end <= Math.min(start + MAX_CLUSTERS, count); end += 1) {
      const word = chars.slice(bounds[start], bounds[end]).join("");
      if (!prefixes.has(word)) break;
      const cost = costs.get(word);
      if (cost !== undefined && best[start] + cost < best[end]) {
        best[end] = best[start] + cost;
        back[end] = { previous: start, known: true };
      }
    }
  }

  const reversed = [];
  let cursor = count;
  while (cursor > 0) {
    const edge = back[cursor];
    if (!edge) return [{ text, known: false, status: "OOV_RUN" }];
    reversed.push({
      text: chars.slice(bounds[edge.previous], bounds[cursor]).join(""),
      known: edge.known,
    });
    cursor = edge.previous;
  }
  reversed.reverse();

  const merged = [];
  for (const item of reversed) {
    if (!item.known && merged.length && !merged.at(-1).known) {
      merged.at(-1).text += item.text;
    } else {
      merged.push({ ...item });
    }
  }
  return merged.map((item) => ({
    ...item,
    status: item.known ? "DICTIONARY_MATCH" : "OOV_RUN",
    source: WORD_SEGMENTER_ID,
  }));
}

export function segmentKhmerWords(text) {
  return segmentKhmerWordsDetailed(text).map((item) => item.text);
}

export function describeWordSegmentation(units, fixtureKeys = new Set()) {
  const tokens = units
    .filter((unit) => /[\u1780-\u17d3]/u.test(unit))
    .map((text) => ({
      text,
      status: fixtureKeys.has(text)
        ? "LEXICAL_FIXTURE"
        : isKnownKhmerWord(text) ? "DICTIONARY_MATCH" : "OOV_RUN",
    }));
  return {
    method: "DICTIONARY_VITERBI_CANDIDATE",
    engine: WORD_SEGMENTER_ID,
    dictionary_entries: WORD_DICTIONARY_SIZE,
    known_words: tokens.filter((item) => item.status !== "OOV_RUN").length,
    oov_runs: tokens.filter((item) => item.status === "OOV_RUN").length,
    accuracy: null,
    tokens,
    note: "Word boundaries are provisional dictionary-Viterbi candidates; no independent segmentation accuracy has been measured for this project.",
  };
}
