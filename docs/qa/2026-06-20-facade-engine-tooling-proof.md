# Facade Engine Tooling Proof - 2026-06-20

## What Was Installed Or Verified

This run installed/verified the local toolchain needed to build and gate reusable project facades
and showroom pages before more Dimri/Rainbow visual work ships.

| Tool | Verification |
|---|---|
| GitHub CLI | `gh --version` -> `gh version 2.94.0`; `gh auth status` reports the saved CLI token is invalid |
| Node.js | `node --version` -> `v25.2.1` |
| npm | `npm.cmd --version` -> `11.6.2` |
| Playwright | `npx.cmd playwright --version` -> `Version 1.61.0` |
| Playwright Chromium | `npx.cmd playwright install chromium` completed; local browser `chromium-1228` present |
| Lighthouse | `npx.cmd lighthouse --version` -> `13.4.0` |
| ImageMagick | `C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe -version` -> `ImageMagick 7.1.2-25` |
| Blender | `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe --version` -> `Blender 5.1.2` |
| glTF Transform | `npx.cmd gltf-transform --version` -> `4.4.0` |
| axe Playwright | installed in `package-lock.json` as `@axe-core/playwright` |

Note: npm reported dependency audit findings in local QA packages. Do not run `npm audit fix`
blindly inside a production release. Treat package remediation as a separate tooling maintenance
task so it cannot rewrite the project dependency tree during a visual hotfix.

GitHub note: the CLI binary is installed, but the saved `gh` token is currently invalid. Do not
hard-code a token into this repo. Until CLI auth is refreshed, use the connected GitHub app or the
logged-in browser for PR actions.

## Research Grounding

Tool and product direction was grounded in:

- Playwright: deterministic screenshots and browser automation.
  https://playwright.dev/docs/intro
- Lighthouse: performance, SEO, accessibility and best-practice audits.
  https://github.com/GoogleChrome/lighthouse
- ImageMagick: command-line image optimization and diffing.
  https://imagemagick.org
- Blender command line: scriptable 3D render/model export.
  https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
- glTF Transform: inspect and optimize GLB/glTF assets.
  https://gltf-transform.dev/
- axe Playwright: accessibility testing in Playwright.
  https://www.npmjs.com/package/@axe-core/playwright
- Render Vision apartment selector: clickable units on a real building render.
  https://render-vision.com/apartment-selector/
- Image Map Pro real-estate tutorial: uploaded building image plus traced polygons.
  https://www.imagemappro.com/tutorials/real-estate
- Homes.com Matterport: interior walkthrough expectation in buyer journeys.
  https://www.homes.com/solutions/matterport
- Zillow 3D Home: buyer-facing 3D/floor-plan/tour expectation.
  https://www.zillow.com/3d-home/

## New Geometry Gate

Added `scripts/qa-showroom-geometry.mjs` and npm script `qa:showroom:geometry`.

The script:

1. Opens a public project URL at desktop, tablet, mobile and Edge-mobile widths.
2. Captures screenshots into `docs/qa/screenshots/<run>/`.
3. Saves a `geometry-report.json` with `getBoundingClientRect()` for model, facade, selected card,
   media, close buttons, unit cells, lead forms and floating rails.
4. Fails when there is horizontal overflow, a media/model/facade rectangle outside the viewport or
   showroom root, multiple visible facade surfaces, a selected card covering the facade too much,
   a floating rail covering the card/form, or tap targets below 44px.

## Live Dimri Baseline

Command:

```bash
node scripts/qa-showroom-geometry.mjs --slug dimri-yama-sde-dov --out docs/qa/screenshots/v1683-geometry-baseline-dimri --strict
```

Result: failed as expected. This is a baseline defect report, not an approval.

| Viewport | Hard failures |
|---|---|
| desktop-1440 | tap target below 44px: 40px |
| tablet-768 | tap target below 44px: 40px |
| mobile-390 | facade outside stage |
| edge-mobile-390 | facade outside stage |

Warnings in every viewport: floating action rail overlaps the selected-apartment card.

Screenshots and full machine geometry report are saved in:

`docs/qa/screenshots/v1683-geometry-baseline-dimri/`

## Next Implementation Standard

No future facade/showroom PR should be considered visually accepted unless the same geometry run
passes after the change. Screenshot review remains required, but screenshot review alone is no
longer enough.
