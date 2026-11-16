import { scanOrthographicComponents } from "./main.js";

export const KHMER_ORTHOGRAPHIC_GRAMMAR_PROFILE =
  "unicode-18.0.0-ch16.4-plus-ch16.4.1-shifter-control";
const MAX_PARSE_ALTERNATIVES = 128;

function roleAt(components, index) {
  return index < components.length ? components[index].role : null;
}

function syllableMatches(components, start) {
  if (roleAt(components, start) !== "BASE") return [];
  let states = new Map([[start + 1, []]]);

  // {R | C}, plus the explicit ZWNJ-before-shifter exception in §16.4.1.
  for (const [index, extensions] of [...states.entries()]) {
    const role = roleAt(components, index);
    if (role === "ROBAT" || role === "SHIFTER") states.set(index + 1, extensions);
    if (role === "FORMAT_CONTROL" && components[index].text === "\u200C"
        && roleAt(components, index + 1) === "SHIFTER") {
      states.set(index + 2, [...extensions, "U+200C-before-shifter (§16.4.1 textual exception)"]);
    }
  }

  // {S {R}}*
  const queue = [...states.entries()];
  for (let cursor = 0; cursor < queue.length; cursor += 1) {
    const [index, extensions] = queue[cursor];
    if (roleAt(components, index) !== "SUBSCRIPT") continue;
    let nextIndex = index + 1;
    if (roleAt(components, nextIndex) === "ROBAT") nextIndex += 1;
    if (!states.has(nextIndex)) {
      states.set(nextIndex, extensions);
      queue.push([nextIndex, extensions]);
    }
  }

  // {{Z} V}
  const afterVowel = new Map(states);
  for (const [index, extensions] of states) {
    if (roleAt(components, index) === "VOWEL") afterVowel.set(index + 1, extensions);
    else if (roleAt(components, index) === "FORMAT_CONTROL" && roleAt(components, index + 1) === "VOWEL") {
      afterVowel.set(index + 2, extensions);
    }
  }

  // {O} {S}
  const afterOther = new Map(afterVowel);
  for (const [index, extensions] of afterVowel) {
    if (roleAt(components, index) === "OTHER_SIGN") afterOther.set(index + 1, extensions);
  }
  const completed = new Map(afterOther);
  for (const [index, extensions] of afterOther) {
    if (roleAt(components, index) === "SUBSCRIPT") completed.set(index + 1, extensions);
  }
  return [...completed.entries()].map(([end, extensions]) => ({ end, extensions }))
    .sort((a, b) => a.end - b.end || a.extensions.join("|").localeCompare(b.extensions.join("|")));
}

export function parseOrthographicSyllables(sourceText) {
  const scan = scanOrthographicComponents(sourceText);
  const components = scan.components;
  const makeResult = (status, alternatives, notes) => ({
    schema: "khmer-orthographic-syllables/v1",
    grammar_profile: KHMER_ORTHOGRAPHIC_GRAMMAR_PROFILE,
    source_text: sourceText,
    offset_unit: "unicode_code_point",
    status,
    parse_count: alternatives.length,
    syllables: status === "PARSED" ? alternatives[0].syllables : null,
    alternatives,
    notes,
  });
  if (!sourceText || scan.status === "INVALID_OR_UNSUPPORTED") {
    return makeResult("INVALID_OR_UNSUPPORTED", [], scan.notes.length ? scan.notes : ["No complete Khmer orthographic structure was found."]);
  }
  if (!components.length || components[0].role !== "BASE") {
    return makeResult("INVALID_OR_UNSUPPORTED", [], ["A Unicode 18 orthographic syllable must begin with a base character."]);
  }

  const size = components.length;
  const pathsByIndex = new Map([[size, [[]]]]);
  for (let start = size - 1; start >= 0; start -= 1) {
    if (roleAt(components, start) !== "BASE") continue;
    const paths = [];
    for (const match of syllableMatches(components, start)) {
      if (match.end !== size && roleAt(components, match.end) !== "BASE") continue;
      for (const remainder of (pathsByIndex.get(match.end) ?? [])) {
        paths.push([{ startIndex: start, endIndex: match.end, extensions: match.extensions }, ...remainder]);
        if (paths.length > MAX_PARSE_ALTERNATIVES) break;
      }
      if (paths.length > MAX_PARSE_ALTERNATIVES) break;
    }
    const unique = new Map(paths.map((path) => [
      JSON.stringify(path.map((part) => [part.startIndex, part.endIndex, part.extensions])), path,
    ]));
    if (unique.size) pathsByIndex.set(start, [...unique.values()]);
  }

  const paths = pathsByIndex.get(0) ?? [];
  if (!paths.length) {
    return makeResult("EVIDENCE_LIMITED", [], [
      "Recognized components do not form a complete sequence under the Unicode 18 §16.4 ordering formula; no boundary was guessed.",
    ]);
  }
  if (paths.length > MAX_PARSE_ALTERNATIVES) {
    return makeResult("EVIDENCE_LIMITED", [], ["The parse forest exceeded the configured alternative limit."]);
  }

  const chars = [...sourceText];
  const alternatives = paths.map((path) => ({
    syllables: path.map(({ startIndex, endIndex, extensions }) => {
      const selected = components.slice(startIndex, endIndex);
      const start = selected[0].start;
      const end = selected[selected.length - 1].end;
      return {
        start, end, source_text: chars.slice(start, end).join(""),
        components: selected, grammar_extensions: extensions,
      };
    }),
  }));
  const status = alternatives.length > 1 ? "AMBIGUOUS" : "PARSED";
  return makeResult(status, alternatives, [
    "Orthographic syllables are not phonological syllables or lexical words.",
    "All complete grammar parses are retained; no best parse is selected.",
  ]);
}
