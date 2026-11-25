let worker;
let nextId = 1;
const pending = new Map();

function getWorker() {
  if (worker) return worker;
  worker = new Worker(new URL("./mekongphon-browser.worker.js", import.meta.url), { type: "module" });
  worker.addEventListener("message", ({ data }) => {
    const request = pending.get(data?.id);
    if (!request) return;
    if (data.progress) {
      request.onProgress?.(data.progress);
      return;
    }
    pending.delete(data.id);
    if (data.error) request.resolve({ error: data.error, message: data.message });
    else request.resolve({ result: data.result });
  });
  const failWorker = () => {
    worker?.terminate();
    worker = undefined;
    for (const request of pending.values()) {
      request.resolve({ error: "WORKER_UNAVAILABLE" });
    }
    pending.clear();
  };
  worker.addEventListener("error", failWorker);
  worker.addEventListener("messageerror", failWorker);
  return worker;
}

/** Run the pinned neural candidate entirely on-device; only static model assets are fetched. */
export function analyzeWithMekongPhon(text, onProgress) {
  try {
    const activeWorker = getWorker();
    const id = nextId++;
    return new Promise((resolve) => {
      pending.set(id, { resolve, onProgress });
      try {
        activeWorker.postMessage({ id, text });
      } catch {
        pending.delete(id);
        resolve({ error: "WORKER_POST_FAILED" });
      }
    });
  } catch (error) {
    return Promise.resolve({
      error: "WORKER_UNAVAILABLE",
      message: error instanceof Error ? error.message : String(error),
    });
  }
}
