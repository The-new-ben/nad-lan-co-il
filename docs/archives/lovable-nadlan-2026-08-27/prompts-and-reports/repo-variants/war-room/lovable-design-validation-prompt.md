# Lovable Design Validation Prompt

Use this only if the owner decides to spend Lovable credits. Do not run it automatically.

## Goal

Review the NadLan design-system and screen-library package as an advisor. Do not rebuild the app unless explicitly approved by the owner in Lovable. Produce critique, missing states, mobile risks, and a clearer screen-by-screen implementation specification.

## Repository And Folder Rules

Write all outputs to:

`handoff/lovable/2026-06-23-war-room-sync/reports/design-validation/`

If screenshots or exports are created, put them under:

- `handoff/lovable/2026-06-23-war-room-sync/screenshots/design-validation/`
- `handoff/lovable/2026-06-23-war-room-sync/exports/design-validation/`

Do not overwrite `handoff/codex/`, `handoff/claude/`, or existing reports.

## Read First

Read these files before responding:

1. `strategy/war-room/design-system-screen-library.md`
2. `strategy/war-room/design-system-screen-library.csv`
3. `strategy/war-room/design-system-screen-library-rtl.html`
4. `strategy/war-room/objective-completion-audit.csv`
5. `strategy/war-room/current-site-evidence-2026-06-23.csv`
6. `strategy/war-room/keyword-to-page-owner.csv`
7. `strategy/war-room/page-architecture-map.csv`
8. `strategy/11-project-showroom-3d-spec.md`
9. `strategy/10-listings-ux-spec.md`

## Required Output

Create these files:

1. `design-validation-report.md`
2. `screen-gap-table.csv`
3. `mobile-risk-table.csv`
4. `asset-truth-risk-table.csv`
5. `codex-implementation-notes.md`
6. `owner-summary-rtl.html`

## Review Requirements

Check:

- Whether the design system can support homepage, listings, listing detail, projects catalog, project page, 3D showroom, professionals, tools, international pages, contractor intake, and admin war room.
- Whether public copy leaks internal language.
- Whether any screen implies unverified official assets, unverified availability, unverified prices, or unverified 3D.
- Whether 390px mobile is realistic.
- Whether the design is premium enough for contractors and foreign investors.
- Whether every proposed screen can map back to a page ID or keyword owner.
- Whether the design avoids cannibalization by keeping one canonical owner per money keyword.

## Tone And Constraints

Be direct and critical. Do not flatter the current design. Do not say something is out of scope because the competition is strong. NadLan is going after the whole Israeli real-estate market and international investor demand over time.

Do not create production code in this run unless explicitly approved by the owner.
