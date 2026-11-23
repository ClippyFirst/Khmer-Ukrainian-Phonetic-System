import { convert } from "./main.js";

self.addEventListener("message", (event) => {
  const { id, text, profile } = event.data ?? {};
  if (!Number.isSafeInteger(id) || typeof text !== "string" || typeof profile !== "string") {
    self.postMessage({ id, error: "INVALID_REQUEST" });
    return;
  }
  try {
    const result = convert(text, profile);
    self.postMessage({ id, result });
  } catch (error) {
    self.postMessage({
      id,
      error: "ENGINE_FAILURE",
      message: error instanceof Error ? error.message : String(error),
    });
  }
});
