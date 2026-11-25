import { convert } from "./khmer-engine-core.js";

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
        return Object.fromEntries(artifact.candidates.map((item) => [item.orthography, {
          ...item,
          teacher_checkpoint_sha256: artifact.teacher?.checkpoint_sha256 ?? null,
        }]));
      })
      .catch(() => null);
  }
  return distilledTablePromise;
}

self.addEventListener("message", async (event) => {
  const { id, text, profile, outputLevel = "balanced" } = event.data ?? {};
  if (!Number.isSafeInteger(id) || typeof text !== "string" || typeof profile !== "string") {
    self.postMessage({ id, error: "INVALID_REQUEST" });
    return;
  }
  try {
    const distilledSyllables = outputLevel === "exploratory" ? await loadDistilledTable() : null;
    const result = convert(text, profile, { outputLevel, distilledSyllables });
    self.postMessage({ id, result });
  } catch (error) {
    self.postMessage({
      id,
      error: "ENGINE_FAILURE",
      message: error instanceof Error ? error.message : String(error),
    });
  }
});
