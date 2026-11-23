import fs from "node:fs";

const main = fs.readFileSync("src/main.js", "utf8");
const client = fs.readFileSync("src/khmer-engine-client.js", "utf8");
const worker = fs.readFileSync("src/khmer-engine.worker.js", "utf8");
const html = fs.readFileSync("index.html", "utf8");

for (const [label, source, required] of [
  ["main", main, ['import { analyzeInWorker } from "./khmer-engine-client.js"', "await analyzeInWorker(inputText, profile, convert)", "renderRevision"]],
  ["client", client, ['new Worker(new URL("./khmer-engine.worker.js", import.meta.url)', 'postMessage({ id, text, profile })', "fallback(text, profile)"]],
  ["worker", worker, ['import { convert } from "./main.js"', "convert(text, profile)", 'self.addEventListener("message"']],
]) {
  for (const fragment of required) {
    if (!source.includes(fragment)) throw new Error(label + " worker contract missing: " + fragment);
  }
}
if (/fetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon/u.test(client + worker)) {
  throw new Error("browser engine worker must not send user input over the network");
}
if (!main.includes('if (typeof document !== "undefined")')) {
  throw new Error("engine module must remain importable in a worker without a DOM");
}
if (!html.includes('src="/src/main.js"') && !html.includes('src="./src/main.js"') && !html.includes('src="src/main.js"')) {
  throw new Error("public page no longer loads the main application module");
}
console.log("Khmer Web Worker contract: PASS");
