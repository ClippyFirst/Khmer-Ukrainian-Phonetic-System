import { createMekongPhonTokenizers } from "./mekongphon-tokenizer.js";

let runtimePromise;

function asset(path) {
  return new URL("../" + path, import.meta.url).href;
}

async function loadRuntime(postProgress) {
  if (runtimePromise) return runtimePromise;
  runtimePromise = (async () => {
    postProgress("Завантаження локального ONNX Runtime…");
    const ortUrl = asset("vendor/onnxruntime-web/ort.wasm.min.mjs");
    const ort = await import(/* @vite-ignore */ ortUrl);
    ort.env.wasm.wasmPaths = asset("vendor/onnxruntime-web/");
    ort.env.wasm.numThreads = 1;
    ort.env.logLevel = "warning";

    postProgress("Завантаження словників моделі…");
    const [manifest, encoderJson, decoderJson] = await Promise.all([
      fetch(asset("models/mekongphon/manifest.json")).then(checkJson),
      fetch(asset("models/mekongphon/encoder_tokenizer.json")).then(checkJson),
      fetch(asset("models/mekongphon/decoder_tokenizer.json")).then(checkJson),
    ]);
    const tokenizers = createMekongPhonTokenizers(encoderJson, decoderJson);
    const modelBytes = Object.entries(manifest.files ?? {})
      .filter(([name]) => name.endsWith(".int8.onnx"))
      .reduce((total, [, item]) => total + (item.bytes ?? 0), 0);

    postProgress(
      "Завантаження ваг MekongPhon (~" + (modelBytes / 1048576).toFixed(1)
      + " MB; лише на цей пристрій)…",
    );
    const [encoder, decoder] = await Promise.all([
      ort.InferenceSession.create(asset("models/mekongphon/encoder.int8.onnx"), {
        executionProviders: ["wasm"],
        graphOptimizationLevel: "all",
      }),
      ort.InferenceSession.create(asset("models/mekongphon/decoder.int8.onnx"), {
        executionProviders: ["wasm"],
        graphOptimizationLevel: "all",
      }),
    ]);
    return { ort, manifest, tokenizers, encoder, decoder, modelBytes };
  })().catch((error) => {
    runtimePromise = undefined;
    throw error;
  });
  return runtimePromise;
}

async function checkJson(response) {
  if (!response.ok) throw new Error("MODEL_ASSET_HTTP_" + response.status);
  return response.json();
}

function tensor(ort, type, values, dimensions) {
  return new ort.Tensor(type, values, dimensions);
}

function repeatArray(source, count) {
  const output = new source.constructor(source.length * count);
  for (let index = 0; index < count; index += 1) {
    output.set(source, index * source.length);
  }
  return output;
}

function topLogProbabilities(row, limit) {
  let maximum = -Infinity;
  for (let i = 0; i < row.length; i += 1) maximum = Math.max(maximum, row[i]);
  let sum = 0;
  for (let i = 0; i < row.length; i += 1) sum += Math.exp(row[i] - maximum);
  const logNormalizer = maximum + Math.log(sum);
  const best = [];
  for (let tokenId = 0; tokenId < row.length; tokenId += 1) {
    const score = row[tokenId] - logNormalizer;
    let insertAt = best.findIndex((item) => score > item.logProbability);
    if (insertAt < 0) {
      if (best.length < limit) best.push({ tokenId, logProbability: score });
    } else {
      best.splice(insertAt, 0, { tokenId, logProbability: score });
      if (best.length > limit) best.pop();
    }
  }
  return best;
}

async function generateBeam({ ort, encoder, decoder, tokenizers, manifest }, text, postProgress) {
  const maxLength = manifest.generation?.max_length ?? 128;
  const beamSize = 4;
  const lengthPenalty = manifest.generation?.length_penalty ?? 1.0;
  const encodedInput = tokenizers.encoder.encodeWithMetadata(text, { maxLength });
  const inputIds = encodedInput.ids;
  if (!inputIds.length) throw new Error("EMPTY_MODEL_INPUT");
  const attention = new BigInt64Array(inputIds.length).fill(1n);
  const encoderInputs = {
    input_ids: tensor(ort, "int64", BigInt64Array.from(inputIds), [1, inputIds.length]),
    attention_mask: tensor(ort, "int64", attention, [1, attention.length]),
  };
  const encoderOutput = await encoder.run(encoderInputs);
  const hidden = encoderOutput.encoder_hidden_states;
  const sourceMask = attention;
  const sourceLength = hidden.dims[1];
  const hiddenSize = hidden.dims[2];
  const repeatedHidden = repeatArray(hidden.data, beamSize);
  const repeatedMask = repeatArray(sourceMask, beamSize);
  const hiddenTensor = tensor(ort, "float32", repeatedHidden, [beamSize, sourceLength, hiddenSize]);
  const maskTensor = tensor(ort, "int64", repeatedMask, [beamSize, sourceLength]);
  const startId = manifest.generation?.decoder_start_token_id ?? 2;
  const eosId = manifest.generation?.eos_token_id ?? 3;
  let beams = Array.from({ length: beamSize }, (_, index) => ({
    ids: [startId],
    score: index === 0 ? 0 : -1e9,
  }));
  const finished = [];

  for (let step = 0; step < maxLength - 1; step += 1) {
    postProgress("Генерація IPA · крок " + (step + 1));
    const targetLength = beams[0].ids.length;
    const decoderIds = new BigInt64Array(beamSize * targetLength);
    beams.forEach((beam, beamIndex) => {
      beam.ids.forEach((id, tokenIndex) => {
        decoderIds[beamIndex * targetLength + tokenIndex] = BigInt(id);
      });
    });
    const output = await decoder.run({
      decoder_input_ids: tensor(ort, "int64", decoderIds, [beamSize, targetLength]),
      encoder_hidden_states: hiddenTensor,
      encoder_attention_mask: maskTensor,
    });
    const logits = output.logits.data;
    const vocabularySize = output.logits.dims[2];
    const candidates = [];
    for (let beamIndex = 0; beamIndex < beamSize; beamIndex += 1) {
      const start = (beamIndex * targetLength + targetLength - 1) * vocabularySize;
      const row = logits.subarray(start, start + vocabularySize);
      for (const item of topLogProbabilities(row, 2 * beamSize)) {
        candidates.push({
          score: beams[beamIndex].score + item.logProbability,
          parent: beamIndex,
          tokenId: item.tokenId,
        });
      }
    }
    candidates.sort((left, right) => right.score - left.score);
    const nextBeams = [];
    for (let rank = 0; rank < Math.min(candidates.length, 2 * beamSize); rank += 1) {
      const candidate = candidates[rank];
      const ids = [...beams[candidate.parent].ids, candidate.tokenId];
      if (candidate.tokenId === eosId) {
        // Match Transformers BeamSearchScorer: store the parent without EOS.
        if (rank < beamSize) {
          finished.push({ ids: beams[candidate.parent].ids, score: candidate.score });
          finished.sort((left, right) =>
            (right.score / (Math.max(1, right.ids.length - 1) ** lengthPenalty))
              - (left.score / (Math.max(1, left.ids.length - 1) ** lengthPenalty))
          );
          finished.splice(beamSize);
        }
      } else if (nextBeams.length < beamSize) {
        nextBeams.push({ ids, score: candidate.score });
      }
      if (nextBeams.length >= beamSize) break;
    }
    beams = nextBeams;
    if (!beams.length) break;
    if (finished.length >= beamSize) {
      const earlyStopping = manifest.generation?.early_stopping ?? false;
      if (earlyStopping === true) break;
      if (earlyStopping === false) {
        const worstFinished = Math.min(
          ...finished.map((item) => item.score / (Math.max(1, item.ids.length - 1) ** lengthPenalty)),
        );
        const bestSumLogprobs = candidates[0].score;
        const currentGeneratedLength = Math.max(1, targetLength - 1);
        if (worstFinished >= bestSumLogprobs / (currentGeneratedLength ** lengthPenalty)) break;
      }
    };
  }

  if (finished.length < beamSize) finished.push(...beams);
  if (!finished.length) throw new Error("MODEL_GENERATION_EMPTY");
  finished.sort((left, right) =>
    (right.score / (Math.max(1, right.ids.length - 1) ** lengthPenalty))
      - (left.score / (Math.max(1, left.ids.length - 1) ** lengthPenalty))
  );
  const bestIds = finished[0].ids;
  return {
    ipa: tokenizers.decoder.decode(bestIds),
    input_token_count: inputIds.length,
    input_truncated: encodedInput.truncated,
    output_token_count: bestIds.length,
    beam_size: beamSize,
  };
}

self.addEventListener("message", async ({ data }) => {
  const { id, text } = data ?? {};
  if (!Number.isSafeInteger(id) || typeof text !== "string") {
    self.postMessage({ id, error: "INVALID_REQUEST" });
    return;
  }
  const progress = (message) => self.postMessage({ id, progress: message });
  try {
    if (!/\p{Script=Khmer}/u.test(text)) throw new Error("KHMER_SCRIPT_INPUT_REQUIRED");
    const started = performance.now();
    const runtime = await loadRuntime(progress);
    progress("Модель готова · локальна генерація");
    const generated = await generateBeam(runtime, text, progress);
    const elapsed = performance.now() - started;
    self.postMessage({
      id,
      result: {
        ...generated,
        provider: "MekongPhon",
        model_id: runtime.manifest.model_id,
        model_revision: runtime.manifest.model_revision,
        model_license: runtime.manifest.model_license,
        profile: "khmer-pph-careful-citation-v1",
        profile_match: "UNVERIFIED",
        kind: "PHONETIC_BROAD",
        status: "PROVISIONAL",
        uncertainty: [
          "Neural model candidate; not independently adjudicated for this profile.",
          "External source and dialect/style equivalence to the selected careful-citation profile are unverified.",
          "The model was trained on a source corpus whose dataset redistribution rights remain unresolved; only the separately Apache-2.0-licensed model artifact is distributed.",
          "The model's published diagnostic performance is source-attested, not independent project accuracy.",
        ],
        elapsed_ms: Math.round(elapsed),
        execution_provider: "onnxruntime-web-wasm",
        input_sent_to_server: false,
        model_bytes: runtime.modelBytes,
      },
    });
  } catch (error) {
    self.postMessage({
      id,
      error: "MEKONGPHON_INFERENCE_FAILED",
      message: error instanceof Error ? error.message : String(error),
    });
  }
});
