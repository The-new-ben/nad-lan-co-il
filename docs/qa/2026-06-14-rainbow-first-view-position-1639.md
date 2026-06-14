# Rainbow 1.63.9 first-view stage position

## Reason

1.63.8 confirmed that the Rainbow showroom no longer renders as a blank stage, but the visible fallback tower still sat too low in the first buyer viewport. The owner-facing problem was simple: the visitor could see a tower, but not enough of the building body for the stage to read as a premium showroom immediately.

## Change

- Raised the visible procedural tower guard from `bottom:178px` to `bottom:260px` on desktop.
- Raised the mobile guard from `bottom:128px` to `bottom:182px`.
- Increased tower opacity from `.86` to `.9`.
- Moved project 3D CSS/JS cache-busters to `1.63.9` so the live browser loads the corrected stage rules.

## Gate

- `nadlan-config` header, healthcheck, manifest, and ZIP all report `1.63.9`.
- The ZIP is rootless and uses forward-slash paths.
- The inline project-3D JavaScript passes `node --check`.
- Live Chrome QA must show:
  - one H1,
  - no horizontal overflow,
  - no visible `class=`/markup leak,
  - model-viewer script rendered as `type="module"`,
  - the generic model-viewer hand prompt hidden,
  - the tower visible higher in the first showroom viewport.
