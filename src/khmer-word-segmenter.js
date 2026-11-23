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

function isBareLetter(word) {
  const { chars, bounds } = clusterStarts(word);
  if (bounds.length !== 2) return false;
  return !chars.some((char) => {
    const cp = char.codePointAt(0);
    return (cp >= 0x17A3 && cp <= 0x17B3)
      || (cp >= 0x17B6 && cp <= 0x17C5)
      || cp === 0x17C7 || cp === 0x17C8;
  });
}

function mergeUnknownAndBareLetters(pieces) {
  const output = [];
  let group = [];
  const flush = () => {
    if (!group.length) return;
    if (group.some((item) => !item.known)) {
      output.push({ text: group.map((item) => item.text).join(""), known: false });
    } else {
      output.push(...group);
    }
    group = [];
  };
  for (const item of pieces) {
    if (!item.known || isBareLetter(item.text)) {
      group.push(item);
    } else {
      flush();
      output.push(item);
    }
  }
  flush();
  return output;
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
  const merged = mergeUnknownAndBareLetters(reversed.reverse());
  return merged.map((item) => ({
    ...item,
    status: item.known ? "DICTIONARY_MATCH" : "OOV_RUN",
    source: WORD_SEGMENTER_ID,
  }));
}

export function segmentKhmerWords(text) {
  return segmentKhmerWordsDetailed(text).map((item) => item.text);
}

export function describeWordSegmentation(units, fixtureKeys = new Set(), sourceText = "") {
  const tokens = units
    .filter((unit) => /[\u1780-\u17d3]/u.test(unit))
    .map((text) => ({
      text,
      status: fixtureKeys.has(text)
        ? "LEXICAL_FIXTURE"
        : isKnownKhmerWord(text) ? "DICTIONARY_MATCH" : "OOV_RUN",
    }));
  const candidateRuns = [...sourceText.matchAll(/[\\u1780-\\u17d3\\u17dd\\u200c\\u200d]+/gu)].map(([run]) => {
    const protectedFixtures = [...fixtureKeys].filter((key) => {
      if (!run.includes(key)) return false;
      const { chars, bounds } = clusterStarts(key);
      return bounds.length - 1 >= 2;
    }).sort();
    if (protectedFixtures.length) {
      return {
        source: run,
        status: "LEXICAL_FIXTURE_PROTECTED",
        protected_fixtures: protectedFixtures,
        candidates: [],
      };
    }
    return {
      source: run,
      status: "CANDIDATES_AVAILABLE",
      protected_fixtures: [],
      candidates: segmentKhmerWordsCandidates(run, 3).map((candidate, index) => ({
        rank: index + 1,
        ...candidate,
      })),
    };
  });

  return {
    method: "DICTIONARY_VITERBI_CANDIDATE",
    engine: WORD_SEGMENTER_ID,
    dictionary_entries: WORD_DICTIONARY_SIZE,
    known_words: tokens.filter((item) => item.status !== "OOV_RUN").length,
    oov_runs: tokens.filter((item) => item.status === "OOV_RUN").length,
    accuracy: null,
    tokens,
    candidate_limit: 3,
    candidate_runs: candidateRuns,
    score_note: "Candidate costs are uncalibrated negative-log frequency scores, not probabilities or confidence values.",
    note: "Word boundaries are provisional dictionary-Viterbi candidates; no independent segmentation accuracy has been measured for this project.",
  };
}


export function segmentKhmerWordsCandidates(text, limit = 3) {
  if (!Number.isInteger(limit) || limit < 1 || limit > 10) {
    throw new RangeError("limit must be an integer from 1 to 10");
  }
  if (!text) return [];
  const { chars, bounds } = clusterStarts(text);
  const count = bounds.length - 1;
  const paths = Array.from({ length: count + 1 }, () => []);
  paths[0] = [{ cost: 0, pieces: [] }];

  const addPath = (end, candidate) => {
    const signature = JSON.stringify(candidate.pieces);
    if (paths[end].some((item) => JSON.stringify(item.pieces) === signature)) return;
    paths[end].push(candidate);
    paths[end].sort((a, b) => a.cost - b.cost);
    if (paths[end].length > limit) paths[end].length = limit;
  };

  for (let start = 0; start < count; start += 1) {
    for (const path of paths[start]) {
      const unknownPiece = chars.slice(bounds[start], bounds[start + 1]).join('');
      addPath(start + 1, {
        cost: path.cost + unknownCost,
        pieces: [...path.pieces, { text: unknownPiece, known: false }],
      });

      for (let end = start + 1; end <= Math.min(start + MAX_CLUSTERS, count); end += 1) {
        const word = chars.slice(bounds[start], bounds[end]).join('');
        if (!prefixes.has(word)) break;
        const cost = costs.get(word);
        if (cost !== undefined) {
          addPath(end, {
            cost: path.cost + cost,
            pieces: [...path.pieces, { text: word, known: true }],
          });
        }
      }
    }
  }

  const candidates = [];
  const seen = new Set();
  for (const path of paths[count]) {
    const merged = mergeUnknownAndBareLetters(path.pieces);
    const signature = JSON.stringify(merged);
    if (seen.has(signature)) continue;
    seen.add(signature);
    candidates.push({
      cost: Number(path.cost.toFixed(8)),
      segments: merged.map((item) => ({
        ...item,
        status: item.known ? 'DICTIONARY_MATCH' : 'OOV_RUN',
      })),
    });
  }
  return candidates.slice(0, limit);
}