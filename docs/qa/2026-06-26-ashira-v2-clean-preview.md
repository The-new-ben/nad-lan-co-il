# Ashira Showroom V2 Clean Preview QA

Date: 2026-06-26
Branch: `codex/ashira-showroom-v2-clean`
Preview: `docs/previews/ashira-showroom-v2-preview.html`

## Scope

This is a local theme-first preview, not a live deploy and not a plugin ZIP.

The goal was to prove the clean v2 contract:

- rotating GLB/model-viewer is the context surface;
- fixed facade/elevation is the apartment selector;
- selected-apartment card sits below the scene and does not block the facade;
- all new selectors use `.nlv2-*` and `data-nlv2-*`;
- no `.nlps` or `.nlp3d` compatibility layer is introduced.

## Chrome Screenshot Proof

Captured in Google Chrome through the Chrome channel at:

- `docs/qa/screenshots/ashira-v2-clean-preview-2026-06-26/desktop-1440-full.png`
- `docs/qa/screenshots/ashira-v2-clean-preview-2026-06-26/desktop-1440-selected-tour.png`
- `docs/qa/screenshots/ashira-v2-clean-preview-2026-06-26/tablet-768-full.png`
- `docs/qa/screenshots/ashira-v2-clean-preview-2026-06-26/mobile-390-full.png`

## Results

| Gate | Result |
|---|---|
| Desktop 1440 screenshot | PASS |
| Tablet 768 screenshot | PASS |
| Mobile 390 screenshot | PASS |
| No horizontal overflow | PASS |
| No console/page errors | PASS |
| Facade beside model on desktop | PASS |
| Model above facade on mobile | PASS |
| Apartment cells embedded on facade | PASS |
| Selected card does not cover facade | PASS |
| H2/H3 align above paragraph column | PASS |
| Public copy avoids internal wording | PASS |
| New files avoid `.nlps`, `.nlp3d`, `!important` | PASS |
| JS syntax check | PASS |
| PHP lint for `functions.php` and pattern | PASS |

## Honest Limits

- The GLB is still a temporary massing model. It proves the model-viewer rail, not official Ashira geometry.
- The facade and hero are generated prototype images. They must be replaced with approved developer assets before a commercial launch.
- Unit positions, prices and statuses are illustrative. They are wired as the correct product structure, not official inventory.

## Commands Run

```powershell
node --check assets\js\nadlan-showroom-v2.js
php -l functions.php
php -l patterns\project-showroom-ashira-v2.php
Select-String -Path assets\css\nadlan-showroom-v2.css,assets\js\nadlan-showroom-v2.js,patterns\project-showroom-ashira-v2.php,docs\previews\ashira-showroom-v2-preview.html -Pattern '\.nlp3d|\.nlps|data-nlps|!important'
```

