# Rainbow 3D v1.60.5 App Selector Polish

Branch: `codex/rainbow-3d-app-selector-1604`
Scope: plugin-only polish for the Rainbow project 3D module. No new public routes, no fake inventory, no live deployment from Codex.

## What Changed

- Default mode is the building selector again. The Mapbox apartment view no longer auto-opens on page load.
- The selected unit now appears in a main-stage card with unit title, status, view, price/estimate state, and three actions: details, view, next step.
- Forced nested scrollbars are removed from the 3D console, unit list, facts table, and tool panel. The page scrolls normally.
- Tower floor plates are less random and more building-like: tapered stack, floor labels, and unit markers.
- Optional price estimate support was added:
  - unit `price` remains official/explicit.
  - unit `price_estimate` displays as a non-binding estimate.
  - project `project_3d_avg_price_per_sqm` can compute a non-binding estimate from unit sqm.
  - project `project_3d_price_source_note` carries the visible trust note.
- Healthcheck now exposes `renderer=premium_tower_picker_v6_app_selector`, `mapbox_default=user_open_only`, `app_selector=true`, `stage_unit_card=true`, and `nested_scrollbars=false`.

## Research Notes

- Render Vision describes high-end apartment viewers as building-first: buyers rotate the exterior, select floors/units on the facade, see a structured info card, filter by price/area/type, and compare units. Source: https://render-vision.com/services/3d-apartment-viewer-services/
- Product 360 viewers are valuable because they give users control to inspect the product before committing. The Rainbow default should therefore be the draggable building, not the map. Source: https://www.zakeke.com/blog/benefits-of-360-product-viewer-for-ecommerce/
- Mapbox counts a map load when a Mapbox GL JS `Map` object is initialized, while later interaction in that session does not create extra map-load charges. Source: https://docs.mapbox.com/mapbox-gl-js/guides/pricing/
- Mapbox recommends hybrid patterns such as a static or non-map preview with a "load map" action to delay interactive map cost. v1.60.5 follows that pattern by lazy-initializing only after the buyer asks for the view. Source: https://docs.mapbox.com/help/troubleshooting/manage-web-map-costs/

## Local QA

Static gates to run before PR:

```powershell
rg -n "premium_tower_picker_v6_app_selector|mapbox_default|user_open_only|stage_unit_card|nested_scrollbars|project_3d_avg_price_per_sqm|price_estimate" plugins/nadlan-config/inc/project-3d.php
rg -n "1.60.5" plugins/nadlan-config/nadlan-config.php plugin-dist/nadlan-config.json plugins/nadlan-config/inc/project-3d.php
```

Expected behavior after Claude deploys:

- On `/projects/rainbow-tel-aviv/`, first view is the building selector, not the Mapbox view.
- Dragging the main stage rotates the building. Floor plates are clickable and keyboard focusable.
- Selecting a floor/unit updates the main-stage card and side detail panel.
- Clicking `מבט` opens the Mapbox stage view. Returning closes it and shows the building again.
- No visible gray nested scrollbar inside `.nlp3d-console`, `.nlp3d-facts`, `.nlp3d-units`, or `.nlp3d-tool-panel`.
- If no price data exists, price stays `לפי פנייה`.
- If `project_3d_avg_price_per_sqm` and unit `sqm` exist, the stage card shows an `אומדן` with `לא מחייב`.
- If unit `price_estimate` exists, it wins over the project average estimate.
- If unit `price` exists, it displays as official price text without the estimate label.

## Honest Boundaries

- This slice does not create real architectural drawings, Cesium/Google 3D Tiles, or official Rainbow inventory.
- Mapbox RTL label handling, animated sun slider, drawings CMS gallery, floating contact dock, and server-space ZIP pruning are follow-up content-layer work.
- PHP lint is a Claude-side gate in this Windows shell because `php` is not installed locally.
