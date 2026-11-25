const BYTE_ENCODER = (() => {
  const bytes = [
    ...Array.from({ length: 94 }, (_, i) => i + 33),
    ...Array.from({ length: 12 }, (_, i) => i + 161),
    ...Array.from({ length: 82 }, (_, i) => i + 174),
  ];
  const codepoints = [...bytes];
  let extra = 0;
  for (let byte = 0; byte < 256; byte += 1) {
    if (!bytes.includes(byte)) {
      bytes.push(byte);
      codepoints.push(256 + extra);
      extra += 1;
    }
  }
  return new Map(bytes.map((byte, index) => [byte, String.fromCodePoint(codepoints[index])]));
})();

const BYTE_DECODER = new Map([...BYTE_ENCODER].map(([byte, character]) => [character, byte]));
const PRETOKENIZER = /'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+/gu;

function mergeKey(left, right) {
  return left + " " + right;
}

function buildTokenizer(data) {
  if (data?.model?.type !== "BPE" || data?.pre_tokenizer?.type !== "ByteLevel"
      || data?.decoder?.type !== "ByteLevel" || !data.model.vocab || !Array.isArray(data.model.merges)) {
    throw new TypeError("Unsupported MekongPhon tokenizer JSON contract");
  }
  const vocab = data.model.vocab;
  const reverseVocab = new Map(Object.entries(vocab).map(([token, id]) => [id, token]));
  const merges = new Map();
  data.model.merges.forEach((pair, index) => {
    const key = Array.isArray(pair) ? mergeKey(pair[0], pair[1]) : pair;
    merges.set(key, index);
  });
  const specialIds = new Set((data.added_tokens ?? []).filter((item) => item.special).map((item) => item.id));
  const unknownId = vocab[data.model.unk_token ?? "[UNK]"] ?? 0;

  function bpe(token) {
    let symbols = [...token];
    while (symbols.length > 1) {
      let selectedIndex = -1;
      let selectedRank = Infinity;
      for (let index = 0; index < symbols.length - 1; index += 1) {
        const rank = merges.get(mergeKey(symbols[index], symbols[index + 1]));
        if (rank !== undefined && rank < selectedRank) {
          selectedRank = rank;
          selectedIndex = index;
        }
      }
      if (selectedIndex < 0) break;
      symbols.splice(selectedIndex, 2, symbols[selectedIndex] + symbols[selectedIndex + 1]);
    }
    return symbols;
  }

  function encode(text, { maxLength = data.truncation?.max_length ?? 128 } = {}) {
    const ids = [];
    for (const piece of String(text).match(PRETOKENIZER) ?? []) {
      const bytes = new TextEncoder().encode(piece);
      const byteEncoded = [...bytes].map((byte) => BYTE_ENCODER.get(byte)).join("");
      for (const token of bpe(byteEncoded)) ids.push(vocab[token] ?? unknownId);
      if (ids.length >= maxLength) break;
    }
    return ids.slice(0, maxLength);
  }

  function decode(ids, { skipSpecialTokens = true } = {}) {
    let byteString = "";
    for (const id of ids) {
      if (skipSpecialTokens && specialIds.has(Number(id))) continue;
      const token = reverseVocab.get(Number(id));
      if (token === undefined) continue;
      byteString += token;
    }
    const bytes = [];
    for (const character of byteString) {
      const byte = BYTE_DECODER.get(character);
      if (byte === undefined) {
        // Preserve a literal unknown token rather than silently dropping it.
        if (character === "[") bytes.push(...new TextEncoder().encode("["));
        else bytes.push(...new TextEncoder().encode(character));
      } else {
        bytes.push(byte);
      }
    }
    return new TextDecoder("utf-8", { fatal: false }).decode(new Uint8Array(bytes));
  }

  return { encode, decode };
}

export function createMekongPhonTokenizers(encoderJson, decoderJson) {
  return {
    encoder: buildTokenizer(encoderJson),
    decoder: buildTokenizer(decoderJson),
  };
}
