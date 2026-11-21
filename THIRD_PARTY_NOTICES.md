# Third-party notices and research-data rights

This inventory is a research aid, not legal advice. It records known upstream declarations and unresolved rights; it does not grant rights in third-party material.

## Repository-owned material

- Original software code: PolyForm Noncommercial 1.0.0 — see [LICENSE](LICENSE).
- Original documentation and explanatory prose: CC BY-NC 4.0 — see [LICENSE-DOCS](LICENSE-DOCS).
- Original project-authored research datasets, annotations and curated database contributions: CC BY-NC 4.0 for noncommercial research, only where the maintainers/contributors own the rights being licensed — see [LICENSE-DATA](LICENSE-DATA).
- The project licenses do not override third-party source terms, grant permission for unknown-rights materials, or make NC-only data eligible for the commercial/product gold-corpus export gate.

## Known third-party materials and restrictions

The authoritative per-source inventory is [data/khmer/sources.json](data/khmer/sources.json). Important examples:

- **MekongPhon (2026):** the paper's CC BY-NC 4.0 publication license is not the dataset license. Dataset redistribution rights remain UNKNOWN; its lexicon seed and OPUS-derived sentence pairs have source-level rights issues and the committed source pipeline drops per-row provenance. Do not import or redistribute as gold pending dataset-specific permission and item-level provenance.
- **Open-Dict IPA Khmer data:** identified upstream as CC BY-NC-SA 4.0. Preserve attribution and ShareAlike conditions; do not include in a differently licensed or commercial product corpus without separate permission.
- **PhonSobon / NCKL-derived Khmer pronunciation datasets:** exact redistribution and derivative-use permissions remain unresolved. The model's MIT license does not grant rights to the underlying NCKL-derived data.
- **BYU MATRIX Khmer IPA model:** model card declares Apache-2.0 for the model artifact; this does not establish rights to the MekongPhon training data.
- **Google Language Resources Khmer:** the `km/data/lexicon.tsv` header declares CC BY 4.0. The companion Festival phonology JSON and prompt data have unresolved scope differences between repository README and paper-level statements. Do not assume every companion file is covered by the lexicon header.
- **OpenSLR SLR42 Khmer TTS archive:** provider archive page and linked license declare CC BY-SA 4.0. The paper's older/general CC BY statement does not supersede the current archive-specific terms without version reconciliation.
- **Kirby research audio and supplementary files:** the DataShare item metadata declares CC BY 4.0 for the reviewed 2011 audio and supplementary resources. Verify the exact archive item and preserve attribution before reuse.
- **Wayland (2005):** the source record identifies CC BY-SA 4.0. Cite the original study and comply with the source terms; do not treat its sample as project-owned gold.
- **DDD Khmer ASR Cultural Dataset:** source metadata identifies CC BY-SA 4.0 and requires attribution to Digital Divide Data. Audio/text items remain governed by that source license and its metadata.
- **Common Voice Khmer:** source metadata identifies CC0-1.0 for the dataset but also records provider restrictions against speaker identification and re-hosting/re-sharing. Follow the provider's current terms and privacy restrictions; CC0 is not permission to identify speakers.
- **Goruut Khmer Central lexicon/model:** upstream code is MIT, but the separate language dataset repository has no declared repository license and no per-language Khmer Central grant was verified. The project audit authorizes temporary test-only use; it does not authorize vendoring, caching for redistribution, packaging or production use. See [the Goruut asset audit](docs/audits/current/GORUUT-ASSET-LICENSE-REVIEW-2026-11-01.md).


- **`@gmana/km-translit` 0.1.2 (npm runtime dependency):** package metadata in the generated npm lockfile declares MIT; package tarball is integrity-pinned in `package-lock.json`. It is used only for the separate BGN/PCGN-derived Khmer-to-Latin romanization path, not for Khmer IPA or phonetic transcription. The project's Ukrainian rendering adapter remains original project code and its outputs remain PROVISIONAL. Package license metadata is not a license grant for third-party dictionary/corpus data beyond the package's own declared distribution terms; preserve the package's upstream notice when redistributing.

## Reuse rule

For every external code, font, model, dictionary, corpus, recording or copied data item, record the exact upstream URL and version, component/file, code license, data/model license, attribution, commercial-use restrictions, redistribution/adaptation conditions, artifact hash, and whether material was actually copied. A source paper's license does not automatically license its dataset, model, audio, dictionary, or derived artifacts.

Where rights are unknown, conflicting, source-specific, or subject to privacy/consent restrictions, keep the material out of redistributable corpora and production packages. Preserve external locators and evidence without copying protected content.

## Wiktionary Khmer lexical IPA fixtures

The following small lexical IPA values are used as provisional source-backed fixtures, with exact entry URLs and the relevant Pronunciation > standard IPA locator recorded in `data/khmer/sources.json` and `data/tests/web-fixtures.json`:

- ខ្មែរ — https://en.wiktionary.org/wiki/ខ្មែរ
- ភាសា — https://en.wiktionary.org/wiki/ភាសា
- ភ្នំពេញ — https://en.wiktionary.org/wiki/ភ្នំពេញ
- កម្ពុជា — https://en.wiktionary.org/wiki/កម្ពុជា
- ខ្ញុំ — https://en.wiktionary.org/wiki/ខ្ញុំ

Wiktionary states that entry text is dual-licensed under CC BY-SA 4.0 and the GNU Free Documentation License (GFDL). Preserve attribution and links to the source pages; treat these fixture rows as separately licensed third-party data, not as covered by the repository's code license. Do not assume embedded third-party media or underlying dictionary material shares the same terms. The entries are community-maintained lexical references, not independent Phnom Penh profile adjudication. See https://en.wiktionary.org/wiki/Wiktionary:Copyrights.
