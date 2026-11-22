# Hybrid Khmer IPA candidate engine

## Runtime contract

The engine has two distinct result layers:

- `ipa` / `ukrainian`: canonical fields from `RuleBasedKhmerEngine`; these are never overwritten by an external model.
- `external_candidates`: every successfully validated external IPA candidate, with provider, IPA kind, profile, uncertainty and provenance.
- `provisional_candidate`: when the canonical IPA is unresolved, the first configured provider whose IPA also passes the project's Ukrainian IPA adapter is exposed as a source-attributed `PROVISIONAL` candidate. It is not relabelled as established, gold or accurate.

Provider order is a reproducible selection order, not a quality ranking. No majority vote or synthetic consensus is performed. The caller can inspect every candidate and its failure reasons. A provider output that cannot be mapped to Ukrainian remains visible in `external_candidates` with `ukrainian_mapping_failure`, but is not selected as a full practical result.

## Built-in optional providers

### Khmer Phonemizer

The pinned optional adapter targets `khmerphonemizer==0.0.3` (MIT). It uses the documented `phonemize` API and preserves token-aligned phone lists in provenance. The concatenated output is typed as broad phonetic and PARTIAL. The package's variety/style conventions have not been shown to match the project's Phnom Penh careful-citation profile, and it does not establish tone, stress or narrow phonetic detail.

Install and enable:

```bash
pip install -e ".[phonemizer]"
```

```python
from khmer_ua import create_hybrid_engine

engine = create_hybrid_engine(include_khmerphonemizer=True)
result = engine.analyze("កម្ពុជាប្រជាធិបតេយ្យ")
print(result["provisional_candidate"])
print(result["external_candidates"])
```

### MekongPhon Khmer IPA model

The pinned `byumatrixlab/khmer-ipa` model is licensed Apache-2.0 on its Hugging Face model card and can be enabled separately. It is a 33.6M-parameter encoder-decoder model; its documented `pron_no_tones` output does not establish tone. Its model training/evaluation setup is not independent expert adjudication for this project's selected profile.

Install and enable:

```bash
pip install -e ".[mekongphon]"
```

```python
engine = create_hybrid_engine(include_mekongphon=True)
result = engine.analyze("កម្ពុជាប្រជាធិបតេយ្យ")
```

Do not infer that Apache-2.0 model weights grant rights to redistribute the separate MekongPhon source corpus. The corpus/repository rights and source-label provenance remain separately restricted in the research register.

## Provider contract

Every provider returns a structured mapping with:

- `ipa`: raw IPA string;
- `kind`: `PHONEMIC`, `PHONETIC_BROAD`, or `PHONETIC_NARROW`;
- `status`: `COMPLETE` or `PARTIAL`;
- `profile`: currently `khmer-pph-careful-citation-v1`;
- non-empty `uncertainty` for PARTIAL;
- optional `provenance`.

Bare strings and malformed IPA are rejected. Raw IPA is preserved exactly. COMPLETE is a provider assertion, not adjudication. The project's IPA validator validates notation and metadata; it does not validate pronunciation truth.

## Important deployment boundary

The public GitHub Pages service is static, local-first and has no runtime API or Python backend. The browser can therefore expose the independent IPA and romanization routes, but it cannot invoke these Python providers at runtime. This module is available to Python/CLI callers and CI diagnostics only until a separately deployed, rights-reviewed inference service is introduced. No network endpoint or remote inference service is silently called by the public page.

Independent expert-adjudicated Phnom Penh IPA gold remains 0; empirical accuracy remains NOT_ASSESSED. The optional providers produce candidates, not ground truth.
