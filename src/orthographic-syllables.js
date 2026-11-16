import { scanOrthographicComponents } from "./main.js";

export const KHMER_ORTHOGRAPHIC_GRAMMAR_PROFILE =
  "unicode-18.0.0-ch16.4-plus-ch16.4.1-shifter-control";
const MAX_SEGMENTATION_ALTERNATIVES = 128;

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

  // {O} {S}
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


function rejectedSpans(components) {
  const size = components.length;
  for (let start = 0; start < size; start += 1) {
    if (roleAt(components, start) !== "BASE") continue;
    const matches = syllableMatches(components, start);
    const viableNext = matches.filter(({ end }) => end === size || roleAt(components, end) === "BASE");
    if (viableNext.length) continue;
    const invalidEnds = matches.filter(({ end }) => end < size && roleAt(components, end) !== "BASE").map(({ end }) => end);
    if (invalidEnds.length) {
      const rejected = components[Math.max(...invalidEnds)];
      const detail = ["MALFORMED_COENG", "UNMODELED_CHARACTER"].includes(rejected.status)
        ? rejected.status + " component " + rejected.text
        : rejected.role;
      return [{
        start: rejected.start,
        end: rejected.end,
        reason: detail + " at this position prevents a complete Unicode 18 §16.4 component-order production.",
      }];
    }
  }
  return components.filter((item) => ["MALFORMED_COENG", "UNMODELED_CHARACTER"].includes(item.status))
    .map((item) => ({
      start: item.start,
      end: item.end,
      reason: item.status + " component " + item.text + " is outside the modeled Unicode 18 grammar inventory.",
    }));
}

export function parseOrthographicSyllables(sourceText) {
  const scan = scanOrthographicComponents(sourceText);
  const components = scan.components;
  const makeResult = (status, alternatives, derivationCount, notes, rejected = []) => ({
    schema: "khmer-orthographic-syllables/v1",
    grammar_profile: KHMER_ORTHOGRAPHIC_GRAMMAR_PROFILE,
    source_text: sourceText,
    offset_unit: "unicode_code_point",
    status,
    parse_count: String(derivationCount),
    segmentation_count: alternatives.length,
    syllables: status === "PARSED" ? alternatives[0].syllables : null,
    alternatives,
    notes,
    rejected_spans: rejected,
  });
  if (!sourceText || scan.status === "INVALID_OR_UNSUPPORTED") {
    return makeResult("INVALID_OR_UNSUPPORTED", [], 0, scan.notes.length ? scan.notes : ["No complete Khmer orthographic structure was found."], rejectedSpans(components));
  }
  if (!components.length || components[0].role !== "BASE") {
    return makeResult("INVALID_OR_UNSUPPORTED", [], 0, ["A Unicode 18 orthographic syllable must begin with a base character."], components.length ? [{ start: components[0].start, end: components[0].end, reason: "The first component is not a base character (B)." }] : []);
  }

  const size = components.length;
  const pathsByIndex = new Map([[size, [[]]]]);
  for (let start = size - 1; start >= 0; start -= 1) {
    if (roleAt(components, start) !== "BASE") continue;
    const matchesByEnd = new Map();
    for (const match of syllableMatches(components, start)) {
      if (match.end !== size && roleAt(components, match.end) !== "BASE") continue;
      if (!matchesByEnd.has(match.end)) matchesByEnd.set(match.end, new Map());
      const key = JSON.stringify([match.extensions, match.grammarRoles]);
      matchesByEnd.get(match.end).set(key, {
        grammar_roles: match.grammarRoles,
        grammar_extensions: match.extensions,
      });
    }

    const paths = [];
    for (const [end, packedMap] of [...matchesByEnd.entries()].sort((a, b) => a[0] - b[0])) {
      const packed = [...packedMap.values()].sort((a, b) =>
        a.grammar_roles.join("|").localeCompare(b.grammar_roles.join("|"))
        || a.grammar_extensions.join("|").localeCompare(b.grammar_extensions.join("|")));
      for (const remainder of (pathsByIndex.get(end) ?? [])) {
        paths.push([{ startIndex: start, endIndex: end, grammarAlternatives: packed }, ...remainder]);
        if (paths.length > MAX_SEGMENTATION_ALTERNATIVES) break;
      }
      if (paths.length > MAX_SEGMENTATION_ALTERNATIVES) break;
    }
    const unique = new Map(paths.map((path) => [
      JSON.stringify(path.map((part) => [
        part.startIndex, part.endIndex, part.grammarAlternatives,
      ])), path,
    ]));
    if (unique.size) pathsByIndex.set(start, [...unique.values()]);
  }

  const paths = pathsByIndex.get(0) ?? [];
  if (!paths.length) {
    return makeResult("EVIDENCE_LIMITED", [], 0, [
      "Recognized components do not form a complete sequence under the Unicode 18 §16.4 ordering formula; no boundary was guessed.",
    ], rejectedSpans(components));
  }
  if (paths.length > MAX_SEGMENTATION_ALTERNATIVES) {
    return makeResult("EVIDENCE_LIMITED", [], 0, ["The number of distinct syllable-boundary segmentations exceeded the configured limit."], [{ start: 0, end: [...sourceText].length, reason: "The configured segmentation-alternative limit was reached; the forest is incomplete." }]);
  }

  const chars = [...sourceText];
  let derivationCount = 0n;
  const alternatives = paths.map((path) => {
    let pathDerivations = 1n;
    const syllables = path.map(({ startIndex, endIndex, grammarAlternatives }) => {
      const selected = components.slice(startIndex, endIndex);
      const start = selected[0].start;
      const end = selected[selected.length - 1].end;
      pathDerivations *= BigInt(grammarAlternatives.length);
      const uniqueRoles = grammarAlternatives.length === 1 ? grammarAlternatives[0].grammar_roles : null;
      const uniqueExtensions = grammarAlternatives.length === 1 ? grammarAlternatives[0].grammar_extensions : null;
      return {
        start, end, source_text: chars.slice(start, end).join(""),
        components: selected,
        grammar_roles: uniqueRoles,
        grammar_extensions: uniqueExtensions,
        grammar_alternatives: grammarAlternatives,
      };
    });
    derivationCount += pathDerivations;
    return { syllables };
  });
  const status = derivationCount > 1n ? "AMBIGUOUS" : "PARSED";
  return makeResult(status, alternatives, derivationCount, [
    "Orthographic syllables are not phonological syllables or lexical words.",
    "All boundary paths and local grammar-role alternatives are retained in a packed forest; no best parse is selected.",
  ]);
}
