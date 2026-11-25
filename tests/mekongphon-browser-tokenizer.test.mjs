import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { createMekongPhonTokenizers } from "../src/mekongphon-tokenizer.js";

const root = path.resolve(process.argv[2] ?? "dist/mekongphon");
const encoderJson = JSON.parse(fs.readFileSync(path.join(root, "encoder_tokenizer.json"), "utf8"));
const decoderJson = JSON.parse(fs.readFileSync(path.join(root, "decoder_tokenizer.json"), "utf8"));
const expected = JSON.parse(fs.readFileSync(path.join(root, "tokenizer-parity.json"), "utf8"));
const manifest = JSON.parse(fs.readFileSync(path.join(root, "manifest.json"), "utf8"));
const maxLength = manifest.generation.max_length;
const tokenizers = createMekongPhonTokenizers(encoderJson, decoderJson);

for (const row of expected) {
  assert.deepEqual(
    tokenizers.encoder.encode(row.text, { maxLength }),
    row.encoder_ids,
    "encoder ByteLevel BPE IDs differ from the pinned Transformers tokenizer",
  );
  assert.deepEqual(
    tokenizers.decoder.encode(row.text, { maxLength }),
    row.decoder_ids,
    "decoder ByteLevel BPE IDs differ from the pinned Transformers tokenizer",
  );
  assert.deepEqual(
    tokenizers.decoder.encode(row.decoder_probe, { maxLength }),
    row.decoder_probe_ids,
    "decoder tokenizer IDs differ from the pinned Transformers tokenizer on IPA text",
  );
  assert.equal(
    tokenizers.decoder.decode(row.decoder_probe_ids),
    row.decoder_probe_roundtrip,
    "decoder ByteLevel decoding differs from the pinned Transformers tokenizer",
  );
}
console.log("MekongPhon browser ByteLevel BPE tokenizer parity passed:", expected.length, "probes");
