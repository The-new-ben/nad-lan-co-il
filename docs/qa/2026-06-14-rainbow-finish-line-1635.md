# QA: Rainbow Finish-Line 1.63.5

Date: 2026-06-14
Page: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`
Branch: `codex/rainbow-page-perfect`

## Why This Patch Exists

Live 1.63.4 had the Rainbow GLB field and `<model-viewer>` markup, but Chrome rejected the
model-viewer library because WordPress rendered it as a classic script:

`<script id="nadlan-model-viewer-js" src="...model-viewer.min.js?...">`

`model-viewer` 4.3.1 is an ES module. Without `type="module"`, Chrome throws
`Unexpected token 'export'`, the custom element never registers, and the buyer does not see the
real 3D model.

## Fixed In 1.63.5

- Added a `script_loader_tag` filter for `nadlan-model-viewer` so the rendered tag is:
  `<script type="module" ... id="nadlan-model-viewer-js"></script>`.
- Changed the GLB rail to `reveal="auto"` and `loading="auto"` so the model appears without a
  first click, while keeping the poster frame.
- Bumped plugin header, healthcheck, CSS/JS cache-busters, manifest and ZIP to `1.63.5`.
- Added `project_3d.model_viewer_module_tag=true` and `project_3d.model_viewer_reveal=auto` to
  healthcheck.
- Added one-shot Rainbow showroom seeding for missing GLB/poster/unit/drawings/environment fields
  from the committed project assets.
- Updated the 3D module opening copy so the first visible paragraph starts with Rainbow, Sde Dov,
  Israel Canada and non-binding price/availability wording.
- Allowed structured `project_3d_environment_json` with `layers[].items[]` and drawings objects
  with `items[]`.

## Local Gates

| Gate | Result |
| --- | --- |
| Manifest parses | PASS |
| Manifest version/download URL | PASS, `1.63.5` |
| Project asset JSON parses | PASS, unit-map/drawings/environment |
| Inline 3D JavaScript syntax | PASS, `node --check` on extracted 48,984-byte JS |
| ZIP path style | PASS, 0 backslashes, 0 absolute paths |
| ZIP contains module-tag fix | PASS |
| ZIP plugin header version | PASS, `1.63.5` |
| Raw GLB URL | PASS, HTTP 200, 944,660 bytes |
| Raw poster URL | PASS, HTTP 200, 76,447 bytes |
| Raw unit map URL | PASS, HTTP 200, 7,506 bytes |
| Raw environment URL | PASS, HTTP 200, 11,064 bytes |
| PHP lint | NOT RUN locally, `php` is not installed on this Windows shell |

## Required Live Chrome Gate After Deploy

1. Healthcheck reports `version: 1.63.5`.
2. Healthcheck reports `project_3d.model_viewer_ready: true`.
3. Healthcheck reports `project_3d.model_viewer_module_tag: true`.
4. Healthcheck reports `project_3d.projects_with_glb >= 1`.
5. Rendered page has a `<script id="nadlan-model-viewer-js" type="module" ...>`.
6. Chrome console has no `Unexpected token 'export'`.
7. `customElements.get('model-viewer')` returns a function.
8. `<model-viewer>` is visible and not stuck on a blank stage.
9. Drag/rotate works on desktop.
10. One H1, no visible raw `class=`, no visible JavaScript/HTML fragments, no horizontal overflow.

## Screenshot Slots

To be filled after live deploy:

- Desktop 1440: `docs/qa/screenshots/rainbow-1635-desktop.png`
- Tablet 768: `docs/qa/screenshots/rainbow-1635-tablet.png`
- Mobile 390: `docs/qa/screenshots/rainbow-1635-mobile.png`
