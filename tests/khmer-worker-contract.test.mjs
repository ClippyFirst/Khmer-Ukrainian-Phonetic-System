import fs from "node:fs";

const main = fs.readFileSync("src/main.js", "utf8");
const client = fs.readFileSync("src/khmer-engine-client.js", "utf8");
const worker = fs.readFileSync("src/khmer-engine.worker.js", "utf8");
const core = fs.readFileSync("src/khmer-engine-core.js", "utf8");
const html = fs.readFileSync("index.html", "utf8");

for (const [label, source, required] of [
  ["main", main, ['import { analyzeInWorker } from "./khmer-engine-client.js"', "await analyzeInWorker(inputText, profile, convert, outputLevelMode)", "renderRevision"]],
  ["client", client, ['new Worker(new URL("./khmer-engine.worker.js", import.meta.url)', 'postMessage({ id, text, profile, outputLevel })', "fallback(text, profile, { outputLevel })"]],
  ["worker", worker, ['import { convert } from "./khmer-engine-core.js"', "convert(text, profile, { outputLevel, distilledSyllables })", 'self.addEventListener("message"']],
]) {
  for (const fragment of required) {
    if (!source.includes(fragment)) throw new Error(label + " worker contract missing: " + fragment);
  }
}
if (/XMLHttpRequest|WebSocket|sendBeacon/u.test(client + worker)) {
  throw new Error("browser engine worker must not use remote inference or telemetry transports");
}
if (!worker.includes('fetch(new URL("../data/google-neural-distilled-syllables.json", import.meta.url)')) {
  throw new Error("Super-soft must load only the static same-origin distilled table");
}
if (worker.includes("fetch(text") || worker.includes("fetch(inputText") || worker.includes("body: text")) {
  throw new Error("Khmer source text must never be sent as a network request body");
}
if (!main.includes('if (typeof document !== "undefined")') || core.includes("document.")) {
  throw new Error("UI must be isolated from the worker-safe engine core");
}
if (!html.includes('src="/src/main.js"') && !html.includes('src="./src/main.js"') && !html.includes('src="src/main.js"')) {
  throw new Error("public page no longer loads the main application module");
}
console.log("Khmer Web Worker contract: PASS");
