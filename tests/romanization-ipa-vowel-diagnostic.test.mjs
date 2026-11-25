import { test } from "node:test";
import { khmerToLatin } from "@gmana/km-translit";

test("temporary diagnostic: inspect PCGN output for simple series-conditioned Khmer vowel syllables", () => {
  const samples = [
    "កិ","គិ","កឹ","គឹ","កឺ","គឺ","កុ","គុ","កូ","គូ",
    "កេ","គេ","កែ","គែ","កៃ","គៃ","កោ","គោ","កៅ","គៅ",
    "កើ","គើ","កឿ","គឿ","កួ","គួ",
  ];
  for (const source of samples) {
    console.log("ROMANIZATION_DIAGNOSTIC", JSON.stringify({source, romanized:khmerToLatin(source)}));
  }
});
