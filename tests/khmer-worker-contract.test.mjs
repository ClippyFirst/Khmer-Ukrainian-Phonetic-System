import assert from "node:assert/strict";
import fs from "node:fs";

const main = fs.readFileSync("src/main.js", "utf8");
const client = fs.readFileSync("src/khmer-engine-client.js", "utf8");
const worker = fs.readFileSync("src/khmer-engine.worker.js", "utf8");
const core = fs.readFileSync("src/khmer-engine-core.js", "utf8");
const html = fs.readFileSync("index.html", "utf8");

for (const [label, source, required] of [
  ["main", main, ['import { analyzeInWorker } from "./khmer-engine-client.js"', "await analyzeInWorker(inputText, profile, fallbackConvert, outputLevelMode)", "async function fallbackConvert(...args)", 'await import("./khmer-engine-core.js")', "if (!inputText.trim())", "renderRevision"]],
  ["client", client, ['new Worker(new URL("./khmer-engine.worker.js", import.meta.url)', 'postMessage({ id, text, profile, outputLevel })', "fallback(text, profile, options)", "teacher_checkpoint_sha256: artifact.teacher?.checkpoint_sha256 ?? null"]],
  ["worker", worker, ['import { convert } from "./khmer-engine-core.js"', "convert(text, profile, { outputLevel, distilledSyllables })", "teacher_checkpoint_sha256: artifact.teacher?.checkpoint_sha256 ?? null", 'self.addEventListener("message"']],
]) {
  for (const fragment of required) {
    if (!source.includes(fragment)) throw new Error(label + " worker contract missing: " + fragment);
  }
}
if (/XMLHttpRequest|WebSocket|sendBeacon/u.test(client + worker)) {
  throw new Error("browser engine worker must not use remote inference or telemetry transports");
}
if (!worker.includes('fetch(new URL("../data/google-neural-distilled-syllables.json", import.meta.url)')) || !worker.includes('outputLevel !== "strict"')) {
  throw new Error("Soft and Super-soft must load the static same-origin distilled table");
}
if (!client.includes('fetch(new URL("../data/google-neural-distilled-syllables.json", import.meta.url)')) || !client.includes('outputLevel !== "strict"')) {
  throw new Error("the local fallback must load the same static same-origin distilled table for Soft and Super-soft");
}
if (worker.includes("fetch(text") || worker.includes("fetch(inputText") || worker.includes("body: text")) {
  throw new Error("Khmer source text must never be sent as a network request body");
}
if (main.includes('from "./khmer-engine-core.js"')) {
  throw new Error("the main page must not eagerly import the large deterministic engine bundle");
}
if (main.indexOf("if (!inputText.trim())") > main.indexOf("await analyzeInWorker(")) {
  throw new Error("empty page initialization must not create/download the engine worker");
}
if (!main.includes('if (typeof document !== "undefined")') || core.includes("document.")) {
  throw new Error("UI must be isolated from the worker-safe engine core");
}
if (!html.includes('src="/src/main.js"') && !html.includes('src="./src/main.js"') && !html.includes('src="src/main.js"')) {
  throw new Error("public page no longer loads the main application module");
}
const { analyzeInWorker } = await import("../src/khmer-engine-client.js");
const asyncFallbackResult = await analyzeInWorker("fallback probe", "khmer-pph-careful-citation-v1", async () => ({
  source: "fallback probe",
  status: "FALLBACK_ASYNC_OK",
}));
assert.equal(asyncFallbackResult.status, "FALLBACK_ASYNC_OK",
  "worker construction failure must await the asynchronous local engine fallback");
console.log("Khmer Web Worker contract: PASS");
