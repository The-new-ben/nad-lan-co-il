# Rainbow 1.63.0 Live Deploy And Prototype Model QA

Branch: `codex/rainbow-prototype-model-1631`

## Live Deploy Proof

PR #162 was merged into `origin/main` as `2332909`.

Live healthcheck after the WordPress plugin update:

- `version`: `1.63.0`
- `project_3d.renderer`: `premium_showroom_v9_model_viewer`
- `project_3d.model_viewer_ready`: `true`
- `project_3d.model_viewer_version`: `4.3.1`
- `project_3d.model_viewer_lazy`: `true`
- `project_3d.model_viewer_hotspots`: `true`
- `project_3d.static_featured_image_suppressed`: `true`
- `project_3d.projects_with_glb`: `0`

`projects_with_glb:0` is expected until `project_model_glb` is populated on the Rainbow project.

## Live Browser QA

Public 1440 viewport:

- One H1 was rendered on the page.
- `.nlp3d` present.
- `<model-viewer>` absent before GLB, as expected.
- Model-viewer script count: `0` before GLB, as expected.
- Static featured image hidden.
- No raw `class="nlpf"` leak.
- `scrollWidth` equals viewport width: `1440`.
- Screenshot: `docs/previews/live-rainbow-1630-desktop1440.png`

Public 390 viewport:

- One H1.
- `.nlp3d` present.
- `<model-viewer>` absent before GLB, as expected.
- Model-viewer script count: `0` before GLB, as expected.
- Static featured image hidden.
- No raw `class="nlpf"` leak.
- `scrollWidth` equals viewport width: `390`.
- Screenshot: `docs/previews/live-rainbow-1630-mobile390.png`

## Prototype Model Package

Added `assets/projects/rainbow-tel-aviv/`:

- `model.glb` - original lightweight architectural massing.
- `poster.png` - lightweight poster.
- `unit-map.json` - demo units with `hotspot_position`, `hotspot_normal`, and `camera_orbit`.
- `project-meta-example.json` - CMS copy/paste map for v1.63.0 fields.
- `drawings.json` - official drawing slots.
- `environment.json` - starter surroundings data.
- `source-notes.md` - public-source and licensing boundaries.
- `qa.md` - artifact-level validation.

Prototype model proof:

- GLB size: 508,888 bytes.
- Poster size: 13,195 bytes.
- Local HTTP `<model-viewer>` preview loads the GLB: `loaded:true`, `modelIsVisible:true`.
- Six hotspot buttons render.
- Clicking a hotspot updates the selected-unit readout.
- Preview screenshot: `docs/previews/rainbow-model-viewer-prototype-final-1440.png`

## CMS Wiring After This Branch Merges

Use the values in `assets/projects/rainbow-tel-aviv/project-meta-example.json`.

For the live Rainbow post:

- `project_model_glb`: URL to `model.glb` after it is hosted on GitHub raw, WordPress Media, or a CDN.
- `project_model_poster`: URL to `poster.png`.
- `project_model_usdz`: empty for now.
- `project_3d_units`: the units array from `project-meta-example.json`.

The preferred production URL after merge is:

`https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/model.glb`

Until this branch is merged, use the branch raw URL only for a temporary QA pass.

## Honest Boundary

This closes the "empty rail" problem with a real, web-loadable prototype model, but it is not official Rainbow BIM, not official floor plans, not official inventory, and not binding pricing. It is the massing-now asset agreed in the research steer: use it for demo/wow and replace it with developer BIM later.
