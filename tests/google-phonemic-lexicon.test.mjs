import assert from "node:assert/strict";
import {
  GOOGLE_PHONEMIC_LEXICON_MANIFEST,
  GOOGLE_PHONEMIC_LEXICON_SOURCE,
  GOOGLE_PHONEMIC_UNRESOLVED_ROWS,
  lookupGooglePhonemicCandidates,
} from "../src/google-phonemic-lexicon.js";

assert.equal(GOOGLE_PHONEMIC_LEXICON_SOURCE.license, "CC-BY-4.0");
assert.equal(GOOGLE_PHONEMIC_LEXICON_MANIFEST.source_rows, 62179);
assert.equal(GOOGLE_PHONEMIC_LEXICON_MANIFEST.nonempty_pronunciation_rows, 62118);
assert.equal(GOOGLE_PHONEMIC_LEXICON_MANIFEST.empty_pronunciation_rows, 61);
assert.equal(GOOGLE_PHONEMIC_LEXICON_MANIFEST.unique_spellings_with_pronunciation, 62114);
assert.equal(GOOGLE_PHONEMIC_LEXICON_MANIFEST.multi_pronunciation_words, 4);
assert.equal(GOOGLE_PHONEMIC_LEXICON_MANIFEST.observed_phone_tokens, 54);
assert.equal(GOOGLE_PHONEMIC_LEXICON_MANIFEST.mapped_phone_tokens, 54);
assert.equal(GOOGLE_PHONEMIC_LEXICON_MANIFEST.ipa_gold_count, 0);
assert.equal(GOOGLE_PHONEMIC_UNRESOLVED_ROWS.length, 61);

const one = lookupGooglePhonemicCandidates("ក");
assert.equal(one.length, 1);
assert.equal(one[0].parsed.ipa, "kɑː");
assert.equal(one[0].parsed.ipa_kind, "PHONEMIC");
assert.equal(one[0].parsed.status, "PROVISIONAL");
assert.ok(one[0].source_row > 0);

const variants = lookupGooglePhonemicCandidates("ការី");
assert.equal(variants.length, 2);
assert.deepEqual(
  new Set(variants.map((candidate) => candidate.source_phonemic)),
  new Set(["k aa . r ii", "k aa . r ə j"]),
);
assert.ok(variants.every((candidate) => candidate.parsed.status === "PROVISIONAL"));

const profileConflict = lookupGooglePhonemicCandidates("ខ្មែរ");
assert.equal(profileConflict.length, 1);
assert.equal(profileConflict[0].parsed.ipa, "kmae");
assert.equal(profileConflict[0].parsed.status, "PROVISIONAL");
assert.ok(profileConflict[0].parsed.uncertainty.includes("TARGET_PROFILE_EQUIVALENCE_UNVERIFIED"));

assert.equal(lookupGooglePhonemicCandidates("not-a-khmer-word").length, 0);
assert.equal(lookupGooglePhonemicCandidates("ភាសា")[0].parsed.ipa, "pʰiə.saː");

console.log("Google Khmer phonemic lexicon browser lookup: PASS");
