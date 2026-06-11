# Rainbow Tel Aviv 3D Experience QA

Branch: `codex/rainbow-3d-prototype`

Target version: `1.59.0`

Live baseline before this branch: `1.58.1`

Live project: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`

## What Changed

- Replaced the flat SVG-overlay apartment picker in `plugins/nadlan-config/inc/project-3d.php` with a premium dark-blueprint pseudo-3D tower picker.
- Kept the existing feature flag `nadlan_feature_project_3d`.
- Kept the existing shortcode `[nadlan_project_3d]`.
- Kept the existing auto-append rule for `nadlan_project` pages with `project_3d_units`, `project_3d_image`, or `project_3d_demo=1`.
- Kept the existing public lead route. No new REST route was added.
- Added floor selection, drag-to-rotate, angle controls, orbit mode, unit cards, selected-unit facts, view-from-unit mode, and two inquiry intents: callback and theoretical purchase request.
- Lead payload now includes `card_id`, `unit`, `floor`, `rooms`, `sqm`, `source=project_3d`, and `purchase_intent`.
- Removed fake default prices from demo units. Demo mode always renders `לפי פנייה` for price until official data exists.
- Added healthcheck marker `project_3d.renderer=premium_tower_picker`.

## Why This Is Safe

- No stock photos, no faces, no copied skyline imagery.
- No invented public prices in the default demo inventory.
- The purchase button is phrased as a non-binding inquiry. The public form states that availability, price, and terms must be verified before any progress.
- The component is scoped to `.nlp3d`, so it does not restyle catalogs, homepage, WooCommerce, or admin pages.
- It uses current WordPress metadata fields instead of a parallel CMS.
- It posts to the already-owned `/nadlan/v1/lead` endpoint, so Chunk B/C/D lead routing, AI qualification, and nurture continue to own the downstream workflow.

## Source Research Used

| Source | What Was Used |
| --- | --- |
| https://sdedov.co.il/faq-en/ | Sde Dov district context: former airport, coastal district, planned public transport, mixed towers/open spaces, long-term district scale. |
| https://sdedov.co.il/project/rainbow/ | Rainbow context: Israel Canada, building permit language, resort-positioned amenities, sea/skyline positioning. |
| https://docs.mapbox.com/mapbox-gl-js/example/3d-buildings/ | Long-term compound map direction: 3D building extrusion and camera patterns. |
| https://docs.mapbox.com/mapbox-gl-js/example/3d-extrusion-floorplan/ | Future unit/floor data model: height/base/color per polygon once real floorplan geometry exists. |
| https://cesium.com/industries/real-estate/ | Long-term digital twin direction: BIM/drone/geospatial data with availability and decision-support overlays. |

## Local Visual Preview

Preview file:

- `docs/previews/rainbow-3d-prototype.html`

Screenshots:

- `docs/qa/screenshots/2026-06-11-rainbow-3d-prototype/desktop.png`
- `docs/qa/screenshots/2026-06-11-rainbow-3d-prototype/mobile.png`

Playwright proof from the local preview:

```json
[
  {
    "name": "desktop",
    "width": 1440,
    "height": 1050,
    "hasStage": true,
    "hasTower": true,
    "floorActive": "קומה 34",
    "unitActive": "קו E · קומה 34",
    "viewOpen": true,
    "dragChangedAngle": true,
    "payloadHasCard": true,
    "payloadHasPurchase": true,
    "labelsFit": true,
    "scrollWidth": 1440,
    "clientWidth": 1440,
    "buttonMinHeight": 44,
    "buttonMinWidth": 44,
    "overflow": false
  },
  {
    "name": "mobile",
    "width": 390,
    "height": 980,
    "hasStage": true,
    "hasTower": true,
    "floorActive": "קומה 34",
    "unitActive": "קו E · קומה 34",
    "viewOpen": true,
    "dragChangedAngle": true,
    "payloadHasCard": true,
    "payloadHasPurchase": true,
    "labelsFit": true,
    "scrollWidth": 390,
    "clientWidth": 390,
    "buttonMinHeight": 44,
    "buttonMinWidth": 44,
    "overflow": false
  }
]
```

## Static Checks

| Check | Result |
| --- | --- |
| Inline JavaScript extracted from `project-3d.php` and checked with `node --check` | PASS |
| Preview drag-to-rotate changes model angle | PASS |
| Preview view-from-unit mode opens | PASS |
| `git diff --check` | PASS, CRLF warnings only |
| ZIP root folder | `nadlan-config/` |
| ZIP backslash paths | 0 |
| Header version | `1.59.0` |
| Healthcheck version | `1.59.0` |
| Manifest version | `1.59.0` |

## Local Limitation

This Windows shell does not have `php`, WSL, or Docker available, so `php -l` could not run locally. Claude must run PHP lint during the deploy gate.

## Manual Gate For Claude

1. Install the ZIP on a staging copy with `nadlan_feature_project_3d=1`.
2. Open `https://nad-lan.co.il/projects/rainbow-tel-aviv/`.
3. Confirm `.nlp3d-premium` appears instead of the old flat `.nlp3d-svg` polygon picker.
4. Confirm model angle buttons rotate the tower.
5. Drag across the model and confirm the tower rotates without horizontal page overflow.
6. Confirm floor buttons update the selected unit list.
7. Confirm selected unit facts render `לפי פנייה` when price is absent or demo mode is active.
8. Click `מבט מהדירה` and confirm the view panel opens with the selected unit view text.
9. Submit a test lead with the callback CTA and confirm `lead_card_id=4464` and `utm_source=project_3d`.
10. Submit a test lead with the purchase-intent CTA and confirm the lead message says it is a non-binding theoretical purchase request.
11. Confirm no duplicate `/nadlan/v1/lead` registration was added.
12. Confirm the healthcheck returns `project_3d.renderer=premium_tower_picker`.

## Still Not Done

- This is not real BIM yet.
- It does not contain official Rainbow apartment inventory.
- It does not contain official prices or availability.
- It does not create a legal purchase transaction.
- The compound/district Mapbox layer still needs `nadlan_feature_compound_map=1`, a Mapbox token option, and the seeded Sde Dov compound term to exist on live.
