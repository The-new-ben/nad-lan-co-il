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

## Gates Run

```text
php -l patterns/project-showroom-ashira-sde-dov.php
php -l docs/previews/ashira-showroom-preview.php
node scripts/validate-project-showroom-payload.mjs --payload assets/projects/ashira-sde-dov/showroom-payload.json
node --check assets/js/nadlan-project-showroom.js
npx --yes @gltf-transform/cli inspect assets/projects/ashira-sde-dov/model-prototype.glb
node scripts/qa-ashira-preview.mjs
```

## Screenshot Proof

- Desktop: `docs/qa/screenshots/ashira-showroom-factory-2026-06-26/desktop-1440.png`
- Tablet: `docs/qa/screenshots/ashira-showroom-factory-2026-06-26/tablet-768.png`
- Mobile: `docs/qa/screenshots/ashira-showroom-factory-2026-06-26/mobile-390.png`
- Interaction: `docs/qa/screenshots/ashira-showroom-factory-2026-06-26/desktop-clicked-15-02.png`

## Findings

- PASS: Schema payload validates with 5 prototype units and 3 material slots.
- PASS: The GLB is valid glTF 2.0 and very small for a prototype.
- PASS: Desktop/tablet/mobile screenshots show no horizontal overflow after replacing the hidden honeypot positioning.
- PASS: Mobile stacks model, facade, selected card and form without facade overflow.
- PASS: Apartment click updates selected card; tour tab changes the media panel; dismiss hides the card.
- PASS: Public copy uses `NadLan` only and does not leak internal system wording in the new files.
- FIXED: Earlier context art made the project look like it was in the sea. The new art places Ashira on land, sea to the west, and adds Reading/Namal, Eshkol and Sde Dov labels.

## Remaining Truth

- The model and facade are original prototypes, not official BIM or official developer material.
- Exact prices, availability, floor plans and unit geometry still need developer-approved data.
- Headless browser QA logs WebGL performance warnings. No page errors were emitted.
