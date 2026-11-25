import manifest from "../data/khmer/google-phonemic-source-lexicon.json" with { type: "json" };
import shard0 from "../data/khmer/google-phonemic-source-lexicon-0.json" with { type: "json" };
import shard1 from "../data/khmer/google-phonemic-source-lexicon-1.json" with { type: "json" };
import shard2 from "../data/khmer/google-phonemic-source-lexicon-2.json" with { type: "json" };
import shard3 from "../data/khmer/google-phonemic-source-lexicon-3.json" with { type: "json" };
import shard4 from "../data/khmer/google-phonemic-source-lexicon-4.json" with { type: "json" };
import shard5 from "../data/khmer/google-phonemic-source-lexicon-5.json" with { type: "json" };
import shard6 from "../data/khmer/google-phonemic-source-lexicon-6.json" with { type: "json" };
import shard7 from "../data/khmer/google-phonemic-source-lexicon-7.json" with { type: "json" };
import { parseGooglePhonemic } from "./google-phonemic-ipa.js";

const shards = [
  shard0.entries, shard1.entries, shard2.entries, shard3.entries,
  shard4.entries, shard5.entries, shard6.entries, shard7.entries,
];

if (manifest.schema_version !== "google-phonemic-source-lexicon/v1") {
  throw new Error("Unsupported Google Khmer phonemic source lexicon schema");
}
if (manifest.manifest.shard_count !== shards.length) {
  throw new Error("Google Khmer phonemic source lexicon shard count mismatch");
}
for (let index = 0; index < shards.length; index += 1) {
  const shard = [shard0, shard1, shard2, shard3, shard4, shard5, shard6, shard7][index];
  if (shard.shard_id !== index || shard.source_revision !== manifest.source.revision) {
    throw new Error(`Google Khmer phonemic source lexicon shard ${index} provenance mismatch`);
  }
}

export const GOOGLE_PHONEMIC_LEXICON_MANIFEST = manifest.manifest;
export const GOOGLE_PHONEMIC_LEXICON_SOURCE = manifest.source;
export const GOOGLE_PHONEMIC_UNRESOLVED_ROWS = manifest.unresolved_rows;

export function lookupGooglePhonemicCandidates(word) {
  const normalized = String(word ?? "").normalize("NFC").trim();
  if (!normalized) return [];
  const shardId = normalized.codePointAt(0) % shards.length;
  const rows = shards[shardId][normalized] ?? [];
  return rows.map(([source_phonemic, source_row, source_label]) => ({
    word: normalized,
    source_phonemic,
    source_row,
    source_label,
    parsed: parseGooglePhonemic(source_phonemic),
  }));
}
