import { scanOrthographicComponents } from "./main.js";

export const KHMER_ORTHOGRAPHIC_GRAMMAR_PROFILE =
  "unicode-18.0.0-ch16.4-plus-ch16.4.1-shifter-control";
const MAX_PARSE_ALTERNATIVES = 128;

function roleAt(components, index) {
  return index < components.length ? components[index].role : null;
}

function syllableMatches(components, start) {
  if (roleAt(components, start) !== "BASE") return [];
  const keyFor = (index, extensions, grammarRoles) =>
    JSON.stringify([index, extensions, grammarRoles]);
  const add = (map, index, extensions, grammarRoles) => {
    const key = keyFor(index, extensions, grammarRoles);
    if (map.has(key)) return false;
    map.set(key, { index, extensions, grammarRoles });
    return true;
  };
  const states = new Map();
  add(states, start + 1, [], ["BASE"]);

  // {R | C}, plus the explicit ZWNJ-before-shifter exception in §16.4.1.
  for (const { index, extensions, grammarRoles } of [...states.values()]) {
    const role = roleAt(components, index);
    if (role === "ROBAT") add(states, index + 1, extensions, [...grammarRoles, "INITIAL_ROBAT"]);
    else if (role === "SHIFTER") add(states, index + 1, extensions, [...grammarRoles, "INITIAL_SHIFTER"]);
    if (role === "FORMAT_CONTROL" && components[index].text === "\u200C"
        && roleAt(components, index + 1) === "SHIFTER") {
      add(states, index + 2,
        [...extensions, "U+200C-before-shifter (§16.4.1 textual exception)"],
        [...grammarRoles, "SHIFTER_CONTROL", "INITIAL_SHIFTER"]);
    }
  }

  // {S {R}}*
  const queue = [...states.values()];
  for (let cursor = 0; cursor < queue.length; cursor += 1) {
    const { index, extensions, grammarRoles } = queue[cursor];
    if (roleAt(components, index) !== "SUBSCRIPT") continue;
    let nextIndex = index + 1;
    let nextRoles = [...grammarRoles, "SUBSCRIPT_CLUSTER"];
    if (roleAt(components, nextIndex) === "ROBAT") {
      nextIndex += 1;
      nextRoles = [...nextRoles, "ROBAT_AFTER_SUBSCRIPT"];
    }
    if (add(states, nextIndex, extensions, nextRoles)) {
      queue.push({ index: nextIndex, extensions, grammarRoles: nextRoles });
    }
  }

  // {{Z} V}
  const afterVowel = new Map(states);
  for (const { index, extensions, grammarRoles } of states.values()) {
    if (roleAt(components, index) === "VOWEL") {
      add(afterVowel, index + 1, extensions, [...grammarRoles, "DEPENDENT_VOWEL"]);
    } else if (roleAt(components, index) === "FORMAT_CONTROL" && roleAt(components, index + 1) === "VOWEL") {
      add(afterVowel, index + 2, extensions, [...grammarRoles, "JOIN_CONTROL_BEFORE_VOWEL", "DEPENDENT_VOWEL"]);
    }
  }

  // {O} {S}; the final S is distinct from the repeated S production.
  const afterOther = new Map(afterVowel);
  for (const { index, extensions, grammarRoles } of afterVowel.values()) {
    if (roleAt(components, index) === "OTHER_SIGN") {
      add(afterOther, index + 1, extensions, [...grammarRoles, "OTHER_SIGN"]);
    }
  }
  const completed = new Map(afterOther);
  for (const { index, extensions, grammarRoles } of afterOther.values()) {
    if (roleAt(components, index) === "SUBSCRIPT") {
      add(completed, index + 1, extensions, [...grammarRoles, "TRAILING_SUBSCRIPT"]);
    }
  }
  return [...completed.values()]
    .map(({ index, extensions, grammarRoles }) => ({ end: index, extensions, grammarRoles }))
    .sort((a, b) => a.end - b.end
      || a.grammarRoles.join("|").localeCompare(b.grammarRoles.join("|"))
      || a.extensions.join("|").localeCompare(b.extensions.join("|")));
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
        paths.push([{
          startIndex: start, endIndex: match.end,
          extensions: match.extensions, grammarRoles: match.grammarRoles,
        }, ...remainder]);
        if (paths.length > MAX_PARSE_ALTERNATIVES) break;
      }
      if (paths.length > MAX_PARSE_ALTERNATIVES) break;
    }
    const unique = new Map(paths.map((path) => [
      JSON.stringify(path.map((part) => [part.startIndex, part.endIndex, part.extensions, part.grammarRoles])), path,
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
    syllables: path.map(({ startIndex, endIndex, extensions, grammarRoles }) => {
      const selected = components.slice(startIndex, endIndex);
      const start = selected[0].start;
      const end = selected[selected.length - 1].end;
      return {
        start, end, source_text: chars.slice(start, end).join(""),
        components: selected, grammar_roles: grammarRoles,
        grammar_extensions: extensions,
      };
    }),
  }));
  const status = alternatives.length > 1 ? "AMBIGUOUS" : "PARSED";
  return makeResult(status, alternatives, [
    "Orthographic syllables are not phonological syllables or lexical words.",
    "All complete grammar parses and component-role assignments are retained; no best parse is selected.",
  ]);
}
