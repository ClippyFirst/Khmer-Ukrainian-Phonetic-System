# Phnom Penh Khmer IPA pilot: private blind-intake and discrepancy-review runbook

**Status:** operational design ready; NOT executed. No annotators, adjudicator or curator are currently recorded as recruited. Gold remains empty.  
**Target profile:** contemporary Phnom Penh Khmer, careful citation forms. The profile and the PHONETIC_BROAD convention draft remain subject to specialist approval; this is not a claim that all Phnom Penh speech is homogeneous.

## Non-negotiable boundary

The project repositories are public. GitHub issues, pull requests, commits, Actions logs and artifacts in these repositories are NOT blind or private intake. Do not submit annotator identities, private audio, raw submissions, contact details, consent forms or blind keys there. The repository may contain only sanitized, rights-cleared, pseudonymous records after the blind phase and rights gate.

A private workspace must be provisioned separately by the owner before collection. Access must be limited to the curator and the relevant role; annotator A must not be able to read B's submission, B must not read A's, and neither annotator may read the other's identity or draft. The adjudicator receives both locked submissions only after both are closed. A public upload URL is not an authenticated private workspace; do not use an upload-only link for sensitive personal data or restricted recordings without a separate privacy/consent assessment.

## Roles and separation of duties

| Role | Minimum duty | Must not do |
|---|---|---|
| Curator | Recruit and qualify participants; approve sources/rights; choose 30 attested lexeme groups; create opaque IDs; prepare identical packets; lock and hash submissions; preserve blind key | Annotate or edit IPA labels |
| Annotator A | Independently annotate all assigned items under the approved convention | See B's labels, engine predictions or adjudication |
| Annotator B | Independently annotate the same items under the same convention | See A's labels, engine predictions or adjudication |
| Adjudicator C | Independently review disagreements after both locks; document decision and evidence | Be either annotator; silently overwrite source evidence |
| Rights reviewer | Verify each item/source and derivative permission; sign the rights ledger | Infer permission from a paper's publication license or repository code license |
| Release maintainer | Validate schema, hashes, provenance, split integrity and permitted export | Access the identity key unless operationally necessary |

One person may not combine curator and annotator roles for the same pilot. Adjudicator C must be independent of A and B. Record qualifications and conflicts of interest outside the public repository; publish only role qualification summaries and pseudonyms if consented.

## Private intake sequence

1. **Provision:** owner creates a private, access-controlled workspace outside the public repositories. Enable MFA, least privilege, audit logging, encryption at rest/in transit and a documented retention/deletion policy. Confirm contractual and jurisdictional requirements before accepting personal data or audio.
2. **Separate destinations:** curator creates distinct A-only and B-only submission destinations. Only curator can read both. Adjudicator has no access before both locks. No shared folder is writable/readable by both annotators.
3. **Blind packet:** curator assigns random opaque record IDs unrelated to word order, source ID or predicted output. Both annotators receive identical orthography, neutral gloss/context, approved profile/convention, and the same source evidence that rights permit. Remove engine output, prior IPA, annotator identity, and other annotator work.
4. **Independent work:** each annotator submits a complete typed IPA object, confidence, uncertainty note, source-evidence reference and convention version. Missing/uncertain evidence must be marked, not guessed.
5. **Lock:** curator records submission timestamp, file digest (SHA-256), item count, convention version and packet digest. Corrections after lock require a new version and audit entry; never replace the original silently.
6. **Blindness check:** curator verifies the two packets are equivalent and neither annotator could access the other submission. Preserve access/audit evidence.
7. **Adjudication:** only after both locks, adjudicator C receives the two labels side-by-side, without annotator identities. C records per-item decision (AGREEMENT, RESOLVED, or UNRESOLVED), exact final IPA where justified, rationale, cited evidence and unresolved alternatives.
8. **Independent discrepancy audit:** a separate qualified reviewer checks all RESOLVED and UNRESOLVED cases for process compliance and a pre-registered sample of AGREEMENT cases. This reviewer cannot be A or B. Any process breach returns the affected record to review; it is not silently repaired.
9. **Release preparation:** curator removes personal data and identity mappings, exports only records whose item-level rights allow the intended use, then the release maintainer runs schema/provenance/rights/split validation. Keep the pilot separate from held-out evaluation if it informs model changes.

## Khmer-specific stimulus coverage

The 30 groups are a process pilot, not a representative accuracy benchmark. Select only attested lexemes with exact locators and rights clearance. Stratify where sources permit across consonant series and series-conditioned nuclei; dependent and independent vowel spellings; vowel quality, length and diphthongs; open/closed and coda classes; onset clusters and transition states; stress/prominence; mono-/disyllabic forms; and candidate /r/-loss or phonation/pitch contexts. Do not turn orthographic distinctions into phonetic labels. Keep careful-citation and colloquial variants in separate profile fields. Record unsupported or absent cells as NOT_ESTABLISHED, not inferred.

## Discrepancy taxonomy

For every non-identical pair, record one or more categories: onset series/aspiration/voicing; vowel quality; vowel length; diphthong trajectory; coda identity; syllable boundary; stress/prominence; pitch/F0; phonation/breathiness; cluster transition vs phonological segment; /r/-retention/loss; citation vs colloquial register; lexical/profile ambiguity; source conflict; transcription-granularity mismatch; insufficient evidence. Distinguish a genuine pronunciation disagreement from an inconsistent convention application.

Do not force a consensus. UNRESOLVED must remain null in the gold export. Exact typed-object agreement is a record-level outcome, not a reliability coefficient. Do not report accuracy from the 30-item process pilot as population accuracy.

## Required audit record (private)

- pilot ID and protocol/convention version;
- role pseudonyms, qualifications, conflict declarations and access grants;
- source ID, exact edition/version, page/entry/audio locator, checksum, rights decision and evidence;
- packet manifest and SHA-256;
- independent submission timestamps, digests and lock events;
- adjudication and independent discrepancy-audit records;
- access log, retention/deletion events and incident log;
- final item inclusion/exclusion decision and export digest.

## Pilot acceptance gate

- [ ] Specialist-approved, versioned Phnom Penh careful-citation convention; second specialist challenge recorded.
- [ ] Two qualified, independent Khmer annotators and separate adjudicator C recruited.
- [ ] Independent curator and rights reviewer assigned.
- [ ] Private destinations tested with synthetic data; cross-account visibility test passes.
- [ ] 30 attested lexeme groups selected with source locators and coverage rationale.
- [ ] Every source item has a documented rights decision for annotation, retention, derivative use and redistribution.
- [ ] Both submissions locked independently; hashes and packet equivalence verified.
- [ ] All disagreements adjudicated; unresolved cases excluded from gold.
- [ ] Independent discrepancy audit completed.
- [ ] Schema, provenance, rights, duplicate and leakage checks pass.

**Current result:** NOT STARTED. The runbook does not create a private channel, recruit people, approve the convention, clear third-party rights or supply IPA labels.
