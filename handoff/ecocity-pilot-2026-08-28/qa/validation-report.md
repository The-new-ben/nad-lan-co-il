# Package validation report

Validation date: 2026-08-28 UTC  
Scope: local artifact only  
Publication/live-site action: not performed and not authorized

## Automated checks

| Check | Result | Evidence |
|---|---|---|
| JSON syntax | Pass | `jq empty` for the schema and both content records |
| Content-schema validation | Pass | `node qa/validate-package.mjs` |
| Fact-register CSV shape | Pass | 31 data rows, 10 columns |
| Media-rights CSV shape | Pass | Header only, 22 columns; the empty state is intentional |
| Fact ID resolution | Pass | All displayed fact cards and FAQ references resolve |
| Unsafe content payloads | Pass | `inventory`, `price` and `geo` are null; `media` is empty in both records |
| Required package files | Pass | Validator confirms 10 core handoff files |
| Manifest syntax and guards | Pass | YAML parsed; 2 projects, 5 locales, publication and live mutation disabled |
| Validator syntax | Pass | `node --check qa/validate-package.mjs` |
| Placeholder/encoding scan | Pass | No em dash, TODO, TBD or lorem placeholder detected |

## Editorial coverage check

Both Hebrew source-of-truth documents contain:

- Positioning, canonical opening and fact capsule.
- Architecture/residences and explicit missing fields.
- Streets/neighborhood, transport, education, culture, leisure, park, beach and useful-service logic.
- Buyer journey, FAQs, Hebrew promotion metadata and internal-link plan.
- Independent-site and transaction-information disclosures.

The shared product documents cover page architecture, conditional structured data, media, 3D, forms, conversion, measurement, privacy, accessibility and performance. The localization document contains audience treatment and project-specific copy sets for English, French, Russian and Arabic, plus per-section adaptation and QA rules.

## Deliberately non-green items

- Inventory and prices: no approved feed.
- Permits and professional credits: primary documentation missing.
- Media: no approved rights rows.
- 3D: approved geometry, coordinates, true north and unit manifest missing.
- Forms: recipient, endpoint, privacy/legal text and operational owner missing.
- Localization: bilingual editorial/legal review not completed.
- Aurelia: exact repository checklist not present in this artifact; Claude must read the canonical local version before implementation.
- Publication: prohibited by the user and remains red regardless of local build quality.

These are controlled blockers, not validation failures. Their unsafe values are suppressed from the content records.
