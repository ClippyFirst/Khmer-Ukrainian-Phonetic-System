# Hybrid Khmer IPA candidate engine

## Runtime contract

The engine has two distinct result layers:

- `ipa` / `ukrainian`: canonical fields from `RuleBasedKhmerEngine`; these are never overwritten by an external model.
- `external_candidates`: every successfully validated external IPA candidate, with provider, IPA kind, profile, uncertainty and provenance.
- `provisional_candidate`: when canonical IPA is unresolved, the first configured provider whose IPA passes the Ukrainian adapter is exposed as a source-attributed `PROVISIONAL` candidate. If no provider candidate maps completely, the first valid IPA candidate is still exposed with a null Ukrainian field and its exact mapping failure. It is not relabelled as established, gold or accurate.

Provider order is a reproducible selection order, not a quality ranking. No majority vote or synthetic consensus is performed. The caller can inspect every candidate and its failure reasons. A provider output that cannot be mapped to Ukrainian remains visible in `external_candidates` with `ukrainian_mapping_failure`, but is not selected as a full practical result.

The `profile` field identifies the target profile requested from the adapter boundary; `profile_match` separately records whether the provider is actually validated for that profile. The built-in external adapters currently return `profile_match: "UNVERIFIED"`. This prevents a target-profile label from being mistaken for evidence of provider/profile equivalence.

## Observed smoke candidate

The pinned Khmer Phonemizer 0.0.3 workflow was run on the reported input `កម្ពុជាប្រជាធិបតេយ្យ`. It returned this raw broad-phonetic candidate:

- IPA candidate: `kampuciə prɑciətʰɨppaʔtaj`
- Ukrainian adapter candidate: `кампутьіє пратьієт'иппатай`
- Status: `PROVISIONAL` / provider candidate `PARTIAL`
- Provider profile match: `UNVERIFIED`
- Provider tokenization: `កម្ពុជា` + `ប្រជាធិបតេយ្យ`

This is evidence that an available G2P engine can produce an IPA-like candidate instead of returning no candidate. It is **not** a claim that this candidate is the correct Phnom Penh careful-citation pronunciation: the provider's dialect/style convention, tone, stress and segmental choices have not been adjudicated. The project's canonical deterministic IPA remains unchanged. The CI artifact is a raw provider diagnostic, not a gold label or benchmark score.

The pinned MekongPhon model was also exercised independently on the same phrase. It returned `kampucieprɑcietʰiʔpaʔtay`. The current Ukrainian adapter deliberately withholds a complete target spelling at the final `y` segment rather than guessing its intended value. This second candidate remains visible with `ukrainian: null` and `ukrainian_mapping_failure: "y"`. The model output is therefore useful as an independent IPA-like candidate, but not yet a fully mappable Ukrainian result. A combined hybrid run can retain both candidates and choose the Khmer Phonemizer candidate for the complete provisional Ukrainian output while preserving MekongPhon as an alternative.

## Built-in optional providers

### Khmer Phonemizer

The pinned optional adapter targets `khmerphonemizer==0.0.3` (MIT). It uses the documented `phonemize` API and preserves token-aligned phone lists in provenance. The concatenated output is typed as broad phonetic and PARTIAL. The package's variety/style conventions have not been shown to match the project's Phnom Penh careful-citation profile, and it does not establish tone, stress or narrow phonetic detail.

Install the optional extra:

```bash
pip install -e ".[phonemizer]"
```

When the package is installed, `create_hybrid_engine()` discovers it automatically. It can also be forced explicitly:

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
