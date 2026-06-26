# Ashira Showroom Factory QA

Date: 2026-06-26

## Scope

Theme-first Ashira prototype page pattern and data folder:

- `patterns/project-showroom-ashira-sde-dov.php`
- `assets/projects/ashira-sde-dov/`
- `assets/css/nadlan-project-showroom.css`
- `scripts/build-ashira-prototype-glb.py`
- `scripts/qa-ashira-preview.mjs`

## Research Anchors

- Official Avisror Ashira page: `https://avisror.com/residential/אשירה-בשדה-דב/`
- Ashira English microsite: `https://ashirabyavisror.com/en/`
- Sde Dov / Ashira public context: `https://sdedov.co.il/a-seaside-paradise-the-story-of-avisror-moshe-sons-landmark-project/`
- Madlan public project page: `https://www.madlan.co.il/projects/מגרש_101_מתחם_אשכול_תל_אביב`
- Walla project facts: `https://nadlan.walla.co.il/item/3647895`
- Globes market context: `https://en.globes.co.il/en/article-sde-dov-penthouse-sells-for-nis-195m-1001486549`
- Magdilim market context: `https://magdilim.co.il/110820241333-2/`
- Product-grade 3D model research: `docs/research/2026-06-26-product-grade-3d-model-generation.md`
- Earlier configurator research: `docs/2026-06-12-3d-configurator-research.md`
- Local quality reference: `assets/projects/rainbow-tel-aviv/model.glb`

## Gates Run

```text
php -l patterns/project-showroom-ashira-sde-dov.php
php -l docs/previews/ashira-showroom-preview.php
node scripts/validate-project-showroom-payload.mjs --payload assets/projects/ashira-sde-dov/showroom-payload.json
node --check assets/js/nadlan-project-showroom.js
npx --yes @gltf-transform/cli inspect assets/projects/ashira-sde-dov/model-prototype.glb
node scripts/qa-ashira-preview.mjs
```

## Model Gate

- Rainbow reference: 851,668 byte GLB, 31,176 uploaded vertices, 12 materials.
- Ashira before upgrade: 2,364 byte GLB, 24 uploaded vertices, 1 material.
- Ashira after upgrade: 72,660 byte GLB, 1,596 uploaded vertices, 11 materials.
- Camera changed to product-viewer behavior:
  - `camera-orbit="-34deg 62deg 34m"`
  - `min-camera-orbit="-Infinity 62deg 30m"`
  - `max-camera-orbit="Infinity 62deg 54m"`
  - `field-of-view="22deg"`
  - `rotation-per-second="5deg"`
- Honest boundary: this is still a prototype context model, not official BIM and not segmented
  apartment geometry.

## Screenshot Proof

- Desktop: `docs/qa/screenshots/ashira-showroom-factory-2026-06-26/desktop-1440.png`
- Tablet: `docs/qa/screenshots/ashira-showroom-factory-2026-06-26/tablet-768.png`
- Mobile: `docs/qa/screenshots/ashira-showroom-factory-2026-06-26/mobile-390.png`
- Interaction: `docs/qa/screenshots/ashira-showroom-factory-2026-06-26/desktop-clicked-15-02.png`

## Hierarchy Gate

The opener was compacted after visual QA showed the poster could consume the first viewport.

- Desktop: one H1, document width 1440 on a 1440 viewport, showroom starts around 497px.
- Tablet: one H1, document width 768 on a 768 viewport, showroom starts around 614px.
- Mobile: one H1, document width 390 on a 390 viewport, showroom starts around 555px.

This keeps project context and the first paragraph visible, but moves the actual model/facade
selector into the first reading screen.

## Findings

- PASS: Schema payload validates with 5 prototype units and 3 material slots.
- PASS: The GLB is valid glTF 2.0, uses multiple materials, and includes tower, podium, boutique buildings, sea, land, sun and Reading reference.
- PASS: Desktop/tablet/mobile screenshots show no horizontal overflow:
  - 1440 viewport / 1440 document width
  - 768 viewport / 768 document width
  - 390 viewport / 390 document width
- PASS: Mobile stacks model, facade, selected card and form without facade overflow.
- PASS: Apartment click updates selected card; tour tab changes the media panel; dismiss hides the card.
- PASS: Public copy uses `NadLan` only and does not leak internal system wording in the new files.
- FIXED: Earlier context art made the project look like it was in the sea. The new art places Ashira on land, sea to the west, and adds Reading/Namal, Eshkol and Sde Dov labels.
- FIXED: QA click used brittle Playwright element action against animated apartment cells. The script now clicks the center point like a buyer tap and verifies the rendered selected card.
- FIXED: `.nlps-showroom-page` now uses `box-sizing:border-box`; without it, padding caused 816px document width on a 768px tablet and 408px on a 390px phone.

## Remaining Truth

- The model and facade are original prototypes, not official BIM or official developer material.
- Exact prices, availability, floor plans and unit geometry still need developer-approved data.
- Headless browser QA logs WebGL performance warnings. No page errors were emitted.
