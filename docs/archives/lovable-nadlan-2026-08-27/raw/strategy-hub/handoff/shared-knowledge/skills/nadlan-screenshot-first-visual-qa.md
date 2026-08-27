# NadLan Screenshot-First Visual QA

Status: active

Date: 2026-06-23

Use this for every NadLan UI, showroom, listing, page, design, prototype, WordPress admin, or Lovable output.

## Rule

Do not call a visual task done from text claims alone. Capture screenshots, save them to the repo, inspect them, and write a visual QA note.

## Required Screenshots

For every changed public UI route, capture at minimum:

- mobile 390px
- desktop 1440px
- Hebrew state when Hebrew exists
- English state when English exists
- every important product state: real model, facade fallback, empty asset, loading, empty result, error, paid listing, non-paid listing

For admin or internal dashboards, capture:

- list/table view
- detail view
- empty state
- error or permission state when relevant

## Save Location

Save screenshots in the repository, not only in chat:

- Codex work: `handoff/codex/<run>/screenshots/`
- Lovable imports: `handoff/lovable/<run>/screenshots/`
- Claude imports: `handoff/claude/<run>/screenshots/`

Use stable names:

`<route-or-screen>--<lang>--<state>--<viewport>.png`

Examples:

- `home--he--default--mobile-390.png`
- `listings--en--paid-ranking--desktop-1440.png`
- `showroom-rainbow--he--real-glb--mobile-390.png`
- `showroom-dimri--he--facade-fallback--desktop-1440.png`

## Visual QA Note

For every screenshot set, write a report or HTML readout that covers:

- what was captured
- what passed visually
- what failed visually
- text overflow or clipping
- horizontal scroll risk
- RTL/LTR direction errors
- font mismatch, especially Hebrew fallback problems
- CTA visibility and hierarchy
- asset truth: real, reused, generated, placeholder, missing
- whether the screen is contractor-sellable or only a prototype
- what must be fixed before porting or publishing

## Image Truth

Important project results must not use generic mock photos that look unrelated to the source project.

Priority order:

1. real contractor/client/source image
2. real source facade/render/floor plan from the project
3. researched public image with source recorded
4. generated prototype image only when clearly labeled as illustrative
5. neutral premium missing-state when no truthful image exists

Do not present an unrelated stock image as a real project image.

## Language And Copy Hygiene

- Public and owner-readable text should not use internal phrases such as money page, KD, war room, or prompt unless the document is explicitly internal.
- Avoid em dashes in new owner/public copy. Use a hyphen, colon, comma, or sentence break.
- Remove generic AI-sounding filler. Say what is real, what is missing, and what changed.

## Acceptance

A visual task is not accepted until:

- screenshots are saved in the repo
- the screenshot set covers the changed surface and core states
- the visual QA note exists
- known gaps are named honestly
- the branch is synced or the unsynced status is clearly reported

