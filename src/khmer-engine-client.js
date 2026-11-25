let worker;
let nextId = 1;
const pending = new Map();
let distilledTablePromise;

function loadDistilledTable() {
  if (!distilledTablePromise) {
    distilledTablePromise = fetch(new URL("../data/google-neural-distilled-syllables.json", import.meta.url), { cache: "force-cache" })
      .then((response) => {
        if (!response.ok) throw new Error("DISTILLED_TABLE_UNAVAILABLE");
        return response.json();
      })
      .then((artifact) => {
        if (artifact.schema !== "google-khmer-neural-distilled-syllables/v1" || !Array.isArray(artifact.candidates)) {
          throw new Error("DISTILLED_TABLE_SCHEMA_MISMATCH");
        }
        return Object.fromEntries(artifact.candidates.map((item) => [item.orthography, item]));
      })
      .catch(() => null);
  }
  return distilledTablePromise;
}

async function runFallback(text, profile, fallback, outputLevel) {
  const options = { outputLevel };
  if (outputLevel === "exploratory") options.distilledSyllables = await loadDistilledTable();
  try { return await fallback(text, profile, options); }
  catch { return null; }
}

function getWorker() {
  if (worker) return worker;
  worker = new Worker(new URL("./khmer-engine.worker.js", import.meta.url), { type: "module" });
  worker.addEventListener("message", ({ data }) => {
    const resolve = pending.get(data?.id);
    if (!resolve) return;
    pending.delete(data.id);
    if (data.error) resolve({ error: data.error, message: data.message });
    else resolve({ result: data.result });
  });
  const failWorker = () => {
    worker?.terminate();
    worker = undefined;
    for (const resolve of pending.values()) resolve({ error: "WORKER_UNAVAILABLE" });
    pending.clear();
  };
  worker.addEventListener("error", failWorker);
  worker.addEventListener("messageerror", failWorker);
  return worker;
}

/**
 * Run the deterministic IPA-first engine off the UI thread.
 * Fallback uses the same local static candidate table, never a remote service.
 */
export function analyzeInWorker(text, profile, fallback, outputLevel = "balanced") {
  try {
    const activeWorker = getWorker();
    const id = nextId++;
    return new Promise((resolve) => {
      pending.set(id, (response) => {
        if (response.result !== undefined) resolve(response.result);
        else runFallback(text, profile, fallback, outputLevel).then(resolve);
      });
      try {
        activeWorker.postMessage({ id, text, profile, outputLevel });
      } catch {
        pending.delete(id);
        runFallback(text, profile, fallback, outputLevel).then(resolve);
      }
    });
  } catch {
    return runFallback(text, profile, fallback, outputLevel);
  }
}
