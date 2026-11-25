# Google Khmer phonology inventory — reference only, redistribution blocked

This project records the following upstream reference for research and source auditing only:

- Project: Google `language-resources`
- Path: `km/festvox/phonology.json`
- Pinned commit: `a90601024f07ab7e96c911243324e0adeb16da96`
- Upstream file blob SHA: `8fb697ff66b09ef0c2a17f17b35600af410a92a9`
- Upstream URL: https://github.com/google/language-resources/blob/a90601024f07ab7e96c911243324e0adeb16da96/km/festvox/phonology.json

## Rights status

<badge>BLOCKED — license scope unresolved</badge>

The file has no file-level license header. At the pinned revision, the upstream repository README states that original files are Apache-2.0 unless otherwise noted and that some datasets are CC BY 4.0. The 2018 paper broadly describes data as CC BY 4.0 unless otherwise noted. These statements do not unambiguously establish the license for this exact companion JSON file. The project's third-party-rights audit therefore leaves its license scope unresolved pending authoritative clarification.

**The file is not copied into this repository and must not be redistributed or included in generated artifacts until the rights conflict is resolved.** The previous experimental copy `google-phonology.json` was removed from this branch.

## What remains usable

The pinned Google `km/data/lexicon.tsv` itself declares CC BY 4.0 in its file header. Its 54 distinct non-empty Khmer lexical phone tokens are the only token inventory required by the current parser. The project-authored `google-phonemic-to-ipa.json` map is checked directly against those observed tokens. The extra `sil` and `pau` silence symbols from the unlicensed/uncleared companion inventory are not needed and are not included.

The upstream inventory is referenced here only to document the audit and to explain why the project previously checked a 56-phone inventory. This is not an IPA conversion table, target-profile authority or independent pronunciation gold.
