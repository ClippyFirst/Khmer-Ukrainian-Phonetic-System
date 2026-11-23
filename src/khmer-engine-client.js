let worker;
let nextId = 1;
const pending = new Map();

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
 * The fallback is the same pinned in-process engine, never a remote service.
 */
export function analyzeInWorker(text, profile, fallback) {
  try {
    const activeWorker = getWorker();
    const id = nextId++;
    return new Promise((resolve) => {
      pending.set(id, (response) => {
        if (response.result !== undefined) resolve(response.result);
        else {
          try { resolve(fallback(text, profile)); }
          catch { resolve(null); }
        }
      });
      try {
        activeWorker.postMessage({ id, text, profile });
      } catch {
        pending.delete(id);
        try { resolve(fallback(text, profile)); }
        catch { resolve(null); }
      }
    });
  } catch {
    return Promise.resolve().then(() => fallback(text, profile)).catch(() => null);
  }
}
