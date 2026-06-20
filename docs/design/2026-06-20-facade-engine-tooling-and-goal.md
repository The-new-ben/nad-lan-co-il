# Facade Engine Goal And Tooling - 2026-06-20

## Goal

Build a reusable premium facade engine for NadLan project pages, with Dimri Yama as the first live
implementation, and every later project using the same factory contract.

The facade is not a decoration and not a one-off generated picture. It is the apartment inventory
surface:

1. Every project has a facade/elevation surface tied to `project_3d_facade_images`.
2. Units are mapped onto that surface with real clickable zones (`points` / stage geometry), not
   fake CSS grids and not floating dots.
3. A tap/click on a unit opens the selected-apartment journey: facts, availability, non-binding
   price context, view, plan/tour/media when supplied, and contact/developer inquiry.
4. If official material is missing, the page must show either a high-quality original illustrative
   concept with a visible label, or a visible missing-asset state. Never silently pretend that a
   schematic grid is a facade.
5. The same contract must work for Sde Dov, Ramat Aviv, urban renewal, towers, compounds, and
   smaller buildings.

## Installed Local Toolchain

These tools were installed or verified on the Windows workstation for faster facade/model work and
repeatable QA:

| Tool | Installed / Verified | Purpose |
|---|---:|---|
| GitHub CLI (`gh`) | installed (`2.94.0`); saved CLI token currently invalid | PR status, PR creation/merge after re-auth; use GitHub connector/Chrome until then |
| Node.js | `v25.2.1` | project scripts and QA runners |
| npm | `11.6.2` via `npm.cmd` | package installation without PowerShell script-policy failures |
| Playwright | `1.61.0` | deterministic desktop/tablet/mobile screenshots and interaction QA |
| Playwright Chromium | installed (`chromium-1228`) | repeatable browser rendering without relying on manual Chrome state |
| Lighthouse | `13.4.0` | external performance, SEO, accessibility and best-practice audit |
| ImageMagick | `7.1.2-25 Q16-HDRI` | image conversion, WebP/JPG export, compression, visual diffing |
| Blender | `5.1.2` | 3D massing, facade composition, GLB/poster generation |
| glTF Transform CLI | `4.4.0` | GLB inspection, optimization and texture compression |
| axe Playwright | `4.11.3` | accessibility assertions inside Playwright QA runs |

Notes:

- `node_modules/` is ignored in `.gitignore`; dependencies are recorded in `package.json` and
  `package-lock.json`.
- npm reported dependency audit findings in installed QA packages. Do not run `npm audit fix`
  blindly; it may rewrite package versions. Audit updates should be a separate tooling PR.
- ImageMagick and Blender may require full executable paths until a new shell picks up PATH
  changes:
  - `C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe`
  - `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`

## Research Sources Used For Tool Choice

- Playwright official docs: browser automation, screenshots and cross-browser testing.
  https://playwright.dev/docs/intro
- Lighthouse official GoogleChrome project: automated performance, SEO, accessibility and
  best-practice audits. https://github.com/GoogleChrome/lighthouse
- ImageMagick official site: command-line image processing and conversion.
  https://imagemagick.org
- Blender official command-line/manual: scriptable 3D creation, rendering and export.
  https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
- glTF Transform official docs: inspect, optimize and texture-compress glTF/GLB assets.
  https://gltf-transform.dev/
- axe-core Playwright package: accessibility checks integrated into Playwright tests.
  https://www.npmjs.com/package/@axe-core/playwright
- Render Vision apartment selector: real building/facade surface with unit information.
  https://render-vision.com/apartment-selector/
- Image Map Pro real-estate tutorial: uploaded building image with traced clickable polygons.
  https://www.imagemappro.com/tutorials/real-estate
- Homes.com Matterport: interior walkthrough as part of the buyer journey.
  https://www.homes.com/solutions/matterport
- Zillow 3D Home: buyer-facing 3D/interior tour expectation.
  https://www.zillow.com/3d-home/

## Facade Engine Acceptance Gate

A project facade is not accepted until all of these are true:

1. `project_3d_facade_images` contains an official image/render or an original illustrative concept
   clearly marked as concept.
2. No fake CSS/SVG apartment grid is emitted when no real facade image exists.
3. Unit zones are anchored on the visible facade image and are large enough for touch.
4. Available/reserved/sold states are visible before opening the card.
5. Selected unit card can be dismissed and does not permanently cover the facade on mobile.
6. Unit click carries context into the existing lead path.
7. Interior/media path is present when `interior_url`, `tour_url`, drawing URL or project video
   exists.
8. Playwright screenshots pass at 1440, 768, 390 and Edge-mobile widths.
9. Lighthouse report is captured for the live project page after deployment.
10. axe/Playwright reports no serious accessibility blockers on the selector controls.
11. GLB files pass `gltf-transform inspect` and are optimized before publication.
12. Image assets are optimized with ImageMagick and kept outside the plugin ZIP unless the asset is
    an explicit prototype seed for a release.
13. Playwright geometry QA measures the rendered rectangles of the model, facade, selected card,
    dismiss buttons, map/view panel, lead form and floating action rail. It must fail when:
    - the document has horizontal overflow,
    - a component extends outside its parent viewport by more than 2px,
    - the selected card covers the active facade cell or primary CTA,
    - the close/dismiss control overlaps the concept label or unit label,
    - mobile layout stacks the facade over the model instead of below/near it,
    - any fixed button overlaps the lead form or footer CTA.
14. Every visual PR must include screenshots plus a JSON geometry report. A screenshot without
    measured rectangles is not enough for this project anymore.

## Overflow And Overlap Detection Method

The required QA method for every showroom page is:

1. Open the public URL with Playwright at `1440`, `768`, `390` and Edge-mobile widths.
2. Query the important surfaces:
   - `.nlp3d`
   - `.nlp3d-stage-wrap`
   - `.nlp3d-model-viewer`
   - `.nlp3d-facade-plane`
   - `.nlp3d-stage-pick`
   - `.nlp3d-stage-card`
   - `.nlp3d-fp-close`
   - lead form and floating action rail selectors.
3. Save each element's `getBoundingClientRect()` to a JSON report.
4. Compute:
   - page overflow: `document.documentElement.scrollWidth - window.innerWidth`;
   - parent containment for each surface;
   - overlap area between selected card and facade plane/cells;
   - overlap area between floating controls and forms/footer;
   - minimum tap target size.
5. Fail the run if any hard threshold is exceeded. Do not "visually approve" a page that the
   geometry report says is overflowing.

## Next Dimri Step

Do not replace the current Dimri concept with another random generated tower. The next Dimri asset
must be one of:

1. official developer facade/elevation/render;
2. a Blender-generated concept based on the known four-building coastal compound structure, with
   clean facade rhythm and readable apartment zones;
3. a generated bitmap concept that is visually superior to the current 1.68.2 asset and still
   labeled as concept.

If the asset is not visually better in screenshots, do not package it.
