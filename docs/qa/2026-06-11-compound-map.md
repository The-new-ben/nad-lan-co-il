# v1.58.0 Compound 3D Map QA

Branch: `codex/compound-map`
Feature flag: `nadlan_feature_compound_map` default `0`
Shortcode: `[nadlan_compound_map compound="sde-dov" lat="32.1108" lng="34.7805" zoom="14.2" pitch="60" bearing="-20"]`

## Research Basis

- Sde Dov official district page: the district is about 1,500 dunam, about 16,000 planned housing units, divided into Eshkol, Central and Northern zones, with first Eshkol occupancy projected for 2029: https://sdedov.co.il/about-sde-dov-district/
- Sde Dov official projects page lists marketed projects including GINDI VOGUE, ASHIRA BY AVISROR, Rainbow Tel Aviv, זוהי, UTOPIA, FIRST BY HAGAG and DIMRI YAMA: https://sdedov.co.il/projects/
- Simplex 3D real-estate pattern: urban-scale 3D map, future construction layers, views, measurements and due-diligence context, not just decoration: https://www.simplex3d.com/real-estate-brokers/
- Mapbox GL JS 3D building pattern: `fill-extrusion` from the `building` layer with height/min_height: https://docs.mapbox.com/mapbox-gl-js/example/3d-buildings/
- Mapbox GL JS custom extrusion pattern: GeoJSON features can drive `fill-extrusion-height`, `fill-extrusion-base` and `fill-extrusion-color`: https://docs.mapbox.com/mapbox-gl-js/example/3d-extrusion-floorplan/
- CesiumJS long-term path: open-source 3D globe/maps, 3D Tiles, WGS84 precision and massive-dataset scaling: https://cesium.com/platform/cesiumjs/

## Gate Matrix

| Gate | Expected | Local proof | Status |
|---|---|---|---|
| G1 flag off | No map output, no Mapbox assets enqueued. | `nadlan_cmpmap_enabled()` requires `get_option('nadlan_feature_compound_map','0') === '1'`; shortcode returns `''`; `wp_enqueue_scripts` bails through `nadlan_cmpmap_needs_assets()`. | Ready for Claude runtime test |
| G2 token missing | Friendly RTL notice, no JS error. | `nadlan_cmpmap_render()` returns `nadlan_cmpmap_notice()` before enqueue; notice text includes `המפה תופעל בקרוב`. | Ready for Claude runtime test |
| G3 pins | Pins built from `nadlan_project` posts in `nadlan_compound` term with numeric `lat` and `lng`. | `nadlan_cmpmap_project_pins()` queries term by slug, requires `lat`/`lng` meta, validates coordinate ranges, emits `id,title,lat,lng,permalink,status,units`. JSON output uses `wp_json_encode(... JSON_HEX_*)`. | Ready for Claude runtime test |
| G4 attr sanitization | Slug sanitized, floats clamped. | `nadlan_cmpmap_attrs()` uses `sanitize_title()` and `nadlan_cmpmap_clamp_float()` for lat/lng/zoom/pitch/bearing. | Ready for Claude runtime test |
| G5 lazy init | Map loads only near viewport. | Inline JS uses `IntersectionObserver` with `rootMargin:'180px 0px'`; fallback initializes only if unsupported. | Ready for Claude runtime test |
| G6 packaging | Version 1.58.0, manifest, ZIP forward-slash paths. | Local checks: header/healthcheck/manifest all `1.58.0`; `plugin-dist/nadlan-config-1.58.0.zip` has 127 entries, zero bad paths, and includes `nadlan-config/inc/compound-map.php`. PHP lint unavailable locally because this Windows shell has no `php`; Claude deploy gate must run `php -l`. | Local package ready |
| G7 accessibility | Container role/label, keyboard-reachable project pins. | Map container has `role="application"`, `aria-label`, `tabindex="0"`; markers are `<button type="button">` elements with `aria-label`; popup CTA is an `<a>`. | Ready for Claude runtime test |
| G8 skill | Reusable skill captured. | `skills/skill-compound-3d-map.md`. | Done |

## Manual Runtime Commands For Claude

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=$RANDOM" | jq '.version,.feature_flags.compound_map,.compound_map'
```

Flag-off smoke:

```bash
curl -s "https://nad-lan.co.il/compound/sde-dov/?cb=$RANDOM" | grep -E "mapbox-gl|nlcmp|המפה תופעל בקרוב" || true
```

Token-missing smoke after turning flag on without token:

```bash
curl -s "https://nad-lan.co.il/compound/sde-dov/?cb=$RANDOM" | grep -E "המפה תופעל בקרוב|mapbox-gl"
```

Expected: notice appears, `mapbox-gl` does not.

Token-present smoke after adding `nadlan_mapbox_token` and assigning projects to compound:

```bash
curl -s "https://nad-lan.co.il/compound/sde-dov/?cb=$RANDOM" | grep -E "mapbox-gl-js/v3.14.0|nlcmp-data|לעמוד הפרויקט"
```

Expected: Mapbox assets present, `nlcmp-data` JSON present, popup CTA strings present.

## Notes

- This PR does not create Sde Dov posts or copy media from `sdedov.co.il`. Cowork owns project-content creation and media harvesting per the 2026-06-11 channel directive.
- The live healthcheck before this PR showed `compounds.count: 0`, so `pins_count` will remain `0` until Cowork or the owner assigns Rainbow and other projects to `nadlan_compound=sde-dov`.
- Live pre-PR URL check: `/`, `/projects/` and `/projects/rainbow-tel-aviv/` returned 200; `/compound/sde-dov/` returned 404 because the compound term does not exist yet. Rainbow post 4464 has `lat=32.102264`, `lng=34.785036`, `developer_name=ישראל קנדה`, `num_units=480`, `paid_tier=premier`.
- The near-term stack is Mapbox GL JS because it gets us a Simplex-like drone feel quickly. The long-term all-Israel digital twin path should move to CesiumJS / 3D Tiles only when real 3D city assets or photogrammetry tiles exist.
- Static checks run locally: `git diff --check` clean, Mapbox GL JS/CSS CDN HEAD requests returned 200, extracted inline JS passed `node --check`. PHP lint is not available in this Windows shell.
