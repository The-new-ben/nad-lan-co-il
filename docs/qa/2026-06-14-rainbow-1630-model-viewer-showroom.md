# Rainbow 1.63.0 Model-Viewer Showroom QA

Branch: `codex/rainbow-showroom-1621-polish`

## Why This Patch Exists

The procedural Rainbow tower is useful as a fallback, but it cannot meet the owner's showroom goal
by itself. A contractor-grade project page needs a real 3D model rail: spin the building like a
premium product, click apartments on the model, keep the selected unit connected to the lead funnel,
and clone the same CMS contract to the next project.

This patch upgrades the 3D engine from "CSS/procedural only" to "GLB model when supplied, honest
fallback when not supplied".

## Research Basis

- Google `<model-viewer>` is the correct first production rail for a web showroom because it gives
  camera controls, AR support, lazy loading, and HTML hotspots without building a custom Three.js
  engine.
- Official model-viewer hotspot docs use `slot="hotspot..."`, `data-position`, `data-normal`, and
  `data-visibility-attribute="visible"` for model-attached annotations.
- Official model-viewer loading docs support lazy/reveal behavior; this patch uses a poster-gated
  reveal when a poster exists and auto reveal when no poster exists so the stage never feels dead.
- glTF Transform is the documented optimization path for `inspect` and `optimize` pipelines before a
  GLB is uploaded to WordPress/CDN.
- Google Photorealistic 3D Tiles and Cesium remain the future environment/view layer, not the
  building-product layer. They should stay click-gated because they are token/cost-bearing.

## CMS Contract Added

Project meta:

- `project_model_glb` - public GLB URL for the real showroom model.
- `project_model_usdz` - optional USDZ URL for iOS AR / Quick Look.
- `project_model_poster` - optional lightweight poster image, preferably WebP/JPG.

Unit JSON fields:

- `hotspot_position` - model coordinates, three numbers separated by spaces.
- `hotspot_normal` - optional model normal, three numbers separated by spaces.
- `camera_orbit` - optional model-viewer camera orbit for this unit.

Compatibility aliases:

- `model_position` can feed `hotspot_position`.
- `model_normal` can feed `hotspot_normal`.

## Runtime Behavior

- If `project_model_glb` is empty, nothing changes: the existing procedural/facade showroom renders.
- If `project_model_glb` exists, the stage renders `<model-viewer>` with camera controls, auto-rotate,
  AR modes, lazy loading, and model-attached unit hotspots.
- Fallback tower/facade art stays visible until the model successfully loads. If the GLB fails, the
  fallback remains usable instead of leaving an empty dark stage.
- Model hotspots call the existing `selectUnit()` flow, so the selected-unit card, comparison,
  inquiry payload, lead routing, and analytics stay the same.
- The 360/spin control drives the real model when the real model exists.

## Static Gate

Expected code markers:

- `project_model_glb`
- `project_model_usdz`
- `project_model_poster`
- `class="nlp3d-model-viewer"`
- `slot="hotspot-`
- `data-position`
- `data-normal`
- `nadlan-model-viewer`
- `model_viewer_ready`
- `projects_with_glb`

Expected healthcheck after install:

```json
{
  "version": "1.63.0",
  "project_3d": {
    "renderer": "premium_showroom_v9_model_viewer",
    "model_viewer_ready": true,
    "model_viewer_version": "4.3.1",
    "model_viewer_lazy": true,
    "model_viewer_hotspots": true
  }
}
```

Local package proof:

- `project-3d` inline JavaScript parse: PASS, 49,555 bytes.
- `git diff --check`: PASS, with Windows CRLF warnings only.
- Encoding scan: no BOM and no UTF-8 replacement characters in changed plugin/docs files.
- ZIP: `plugin-dist/nadlan-config-1.63.0.zip`, 130 entries, root `nadlan-config/`, zero backslash
  paths.
- ZIP markers present: `Version: 1.63.0`, `project_model_glb`, `project_model_usdz`,
  `project_model_poster`, `nlp3d-model-viewer`, `nadlan-model-viewer`, `model_viewer_ready`,
  `projects_with_glb`, `premium_showroom_v9_model_viewer`.
- Local PHP lint: NOT RUN because this Windows shell has no `php` binary. Claude/deploy gate must
  run `php -l` on PHP 8.x.

## Live Baseline Before 1.63.0 Install

Browser QA against production before this package is deployed showed the current live page is still
not at the target standard:

- Desktop: no document-level horizontal overflow and no raw `class="nlpf"` leak.
- Desktop: static `.wp-block-post-featured-image` still renders above the showroom.
- Desktop: no `<model-viewer>` element exists yet because no GLB rail is deployed/populated.
- Mobile: no document-level horizontal overflow, but `.nlp3d` and the legacy `.nlpf` card sit off
  the visual gutter. This package adds an `.nlpf` containment guard and first-screen suppression for
  3D project pages.
- Production browser session used for measurement did not show a WordPress admin bar in the in-app
  browser; live admin work should use the logged-in Chrome session if needed.

## Manual Browser Gate

On a project with no GLB:

- The existing procedural/facade showroom still renders.
- Drag, unit selection, Mapbox view, comparison and inquiry still work.
- No blank stage.

On a project with a valid GLB:

- The real model is visible in the same stage.
- Plain drag rotates the model; zoom controls adjust the field of view.
- Unit hotspots are visible when the model-viewer visibility attribute says they should be.
- Clicking a model hotspot selects the same unit in the console and lead payload.
- If the model has a poster, the poster/lazy reveal is visible before interaction.
- If the model fails, the fallback procedural/facade stage remains visible and usable.

## Honest Boundary

This patch creates the production rail for real 3D project models, but it does not fabricate official
Rainbow BIM, official floor plans, official availability, or binding purchase terms. Until the owner
or developer supplies model/drawing/inventory data, Rainbow remains a high-quality prototype with
explicit demo/source notes.
