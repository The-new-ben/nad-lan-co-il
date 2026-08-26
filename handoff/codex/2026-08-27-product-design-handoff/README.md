# Nadlan product and design handoff — 2026-08-27

This is the repository handoff for the Nadlan product work produced during the Lovable design lab. It is intentionally exploded into reviewable files. There is no new ZIP in this delivery.

## Read this first

The Lovable screens are **visual references**, not production code and not an approved final redesign. They are useful for information architecture, page sequencing, component decomposition, mobile behavior and meeting flow. The live WordPress repository remains the source of truth.

The recommended product direction is:

1. Projects and apartment choice are the visual product lead.
2. Listings, tools, guides and professionals support the decision journey.
3. Seeded content remains clearly marked as demo until a real source is connected.
4. Internal quality checks are advisory. They never block save, preview or publish.
5. Every indexed URL owns one intent, one H1 and one canonical.

## Contents

- `01-PRODUCT-DECISION-HE.md` — what the work means and which decisions to keep.
- `02-WORDPRESS-IMPLEMENTATION-HE.md` — block, template, data and release mapping.
- `03-design-tokens.json` — portable visual tokens, not a forced theme replacement.
- `04-SEO-AND-MEASUREMENT-HE.md` — ownership, seeded state, schema and events.
- `05-qa-matrix.csv` — screen-level acceptance evidence.
- `06-LOVABLE-REFERENCE-ROUTES.md` — private reference links and their purpose.
- `screenshots/` — desktop and mobile evidence for the seven-screen journey.

## How to hand this to an implementer

Ask the implementer to work in this order:

1. Approve or revise the tokens and component hierarchy.
2. Build reusable header, footer, cards, filters and mobile drawer.
3. Build archive/detail templates for projects and properties.
4. Connect real WordPress fields and retain the seeded-state label where needed.
5. Add SEO metadata, schema and analytics.
6. Verify 390, 768 and 1440 widths before any release.

Do not ask the implementer to recreate screenshots as static HTML. The screenshots describe product behavior; the WordPress templates own the implementation.

## Relationship to the existing Aurelia package

The full, evidence-backed project-page system remains in:

- `handoff/codex/2026-08-25-aurelia-master-recipe/`
- `handoff/codex/2026-08-26-aurelia-live-qa-remediation/`

Those packages are deeper and more authoritative for project detail, 3D, unit selection and facilities. This handoff adds the broader site journey around that project experience.

## Status

- Repository delivery only.
- No live WordPress change.
- No Lovable runtime dependency.
- No secrets, private credentials or customer data.
