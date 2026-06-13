# Rainbow 1.62.0 Product Showroom QA

Branch: `codex/rainbow-showroom-v1620`

## Intent

Upgrade the Rainbow project module from a large technical selector into a more product-like
showroom: building first, drag/tilt/zoom, forgiving apartment hit targets, no nested visible
scrollbars, and CMS fields for future developer-supplied material.

## Research Checked

- Zillow 3D Home floor plans: photos, floor plans and 3D tours are combined into one digital
  shopping surface. Source: https://www.zillow.com/3d-home/floor-plans/
- Zillow 3D Home: interactive room-to-room inspection is positioned as a buyer confidence tool.
  Source: https://www.zillow.com/3d-home/
- Zillow 2021 launch: stronger media experiences are framed as the next generation of home tours.
  Source: https://zillow.mediaroom.com/2021-02-17-Zillow-Launches-Next-Generation-3D-Tours
- Google Photorealistic 3D Tiles: future city-view layer should use a 3D tiles renderer and token
  governance, not page-load raster guessing. Source:
  https://developers.google.com/maps/documentation/tile/3d-tiles
- Cesium Photorealistic 3D Tiles: CesiumJS is the practical web renderer path for that future view.
  Source: https://cesium.com/learn/photorealistic-3d-tiles-learn/
- Render Vision 3D apartment viewer: the expected real-estate interaction is clickable building /
  floor / unit detail, not a static image. Source:
  https://render-vision.com/services/3d-apartment-viewer-services/
- DIGBY apartment selector: apartment selectors are strongest when the facade itself is the
  navigation surface and the data can be uploaded/changed by the project owner. Source:
  https://digby.hu/apartment-selector
- Baymard video and 360 examples: product pages benefit from spin/video media, but the controls must
  be obvious and not buried. Source: https://baymard.com/ecommerce-design-examples/video-and-360-views

## Code Changes To Gate

- `project_3d_model_type`, `project_3d_video_url`, `project_3d_tour_url`,
  `project_3d_cesium_tiles_url`, `project_3d_drawings_json`, and
  `project_3d_environment_json` are registered as `nadlan_project` meta and exposed to REST for
  authenticated editors.
- Unit JSON accepts `interior_url`, `tour_url`, and `view_note`.
- `project_3d_drawings_json` and `project_3d_environment_json` only save if they decode to JSON
  arrays.
- Healthcheck should report:
  - `project_3d.renderer = premium_showroom_v7_product_stage`
  - `project_3d.cms_material_fields = true`
  - `project_3d.hit_targets = true`
  - `project_3d.model_zoom_tilt = true`
  - `project_3d.cesium_ready = true`
- The newest CSS layer must remove visible nested scrollbars from the showroom console.
- Dragging the building changes horizontal angle and vertical tilt.
- Zoom buttons change model scale.
- Invisible SVG hit polygons expand apartment click areas beyond the visible line art.

## Manual Live Gate After Install

Run after merge, uPress/server sync, plugin update, and hard refresh:

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck" | jq '.version,.project_3d'
```

Expected version: `1.62.0`.

Browser checks:

- 1440px desktop: no horizontal overflow; module sits inside viewport; no visible raw class/script
  text; console has no gray inner scrollbar.
- 760px tablet: stage first, console stacks cleanly, unit/detail/form panels do not overlap.
- 390px mobile: no horizontal overflow; buttons and unit targets are usable; selected card appears
  below the stage instead of covering the whole building.
- Building-first default: map is not auto-opened.
- Drag on the building changes angle; vertical drag changes tilt.
- Double tap/click or zoom controls changes model scale.
- Clicking an apartment/floor updates the stage card, facts, compare tray and lead payload.
- "View" opens the map only on user request; Mapbox RTL plugin should keep Hebrew labels readable
  where Mapbox supports them.
- Price language remains estimate/source-aware or "by inquiry"; no fake official availability.

## What This Does Not Claim

- This is not official Rainbow BIM.
- This does not publish Madlan subscription transaction rows.
- This does not create a legally binding apartment purchase or hold.
- Cesium / Google Photorealistic 3D Tiles is a ready seam, not a live production renderer in this
  slice.
