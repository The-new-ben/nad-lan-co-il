# GLB factory — intake spec (what data a project needs to get a 3D model, facade & hotspots)

The "choose your apartment from inside the building" experience needs three
layers per project. This spec defines exactly what data each layer consumes, so
research prompts and the factory agree on one contract. Storage: the project's
record in `data/projects/<slug>.json` (`building_form`, `assets_3d`) + sidecar
files in `assets/projects/<slug>/`.

## Repo GLB inventory (audited 2026-07-04, trimesh)
| model | tris | extents (m) | verdict |
|---|---|---|---|
| `assets/projects/rainbow-tel-aviv/model.glb` | **15,588** | 168×138×141 | **THE rich Rainbow** — flagship-grade |
| `plugins/.../showroom-engine/models/rainbow.glb` | 3,540 | 1090×129×1000 | old-showroom scene (building+context plate) |
| `plugins/.../showroom-engine/models/dimri.glb` | 3,192 | 1090×81×1000 | best Dimri we have (scene-grade, not rich) |
| factory 07-03 models (rainbow/dimri/ashira/duo) | ~2k | 440×~125×360 | anchored-scene massing |
| `assets/projects/*/model-{context,prototype}.glb` | tiny | — | placeholders |

**Honest finding:** Rainbow has a genuinely rich model. Dimri Yama's best is the
old-showroom scene — a truly detailed Dimri GLB does not exist in the repo; if
one exists elsewhere (Lovable run, local disk), upload it; otherwise the factory
generates tier-B massing from data below. **No GLB carries unit-named nodes** —
apartment selection ALWAYS comes from sidecar data, never from mesh names.

## Layer 1 — the building model (tiers, best available wins)
- **Tier A – authored/BIM:** developer GLB/IFC or our hand-built rich model
  (Rainbow). Requirement: real-world meters, Y-up, origin at ground center,
  building separable from context (distinct geometries).
- **Tier B – generated massing:** built by the factory from data. REQUIRED
  fields (in `building_form`): `floors` (per building), `floor_height_m`
  (default 3.05), `footprint_shape` + `footprint_dims_m{x,z}`, `num_buildings` +
  relative placement, `has_podium`/`podium_floors`, `main_facade_orientation_deg`,
  `facade_material`/palette, balcony pattern. Context anchors from `context`:
  `dist_to_sea_m` + `sea_bearing_deg` (sea plane only if honest), streets,
  neighboring heights (`skyline`), landmark.
- **Tier C – default building:** brand-styled generic massing, clearly labeled
  "המחשה" — used only so no project page ships without 3D.

## Layer 2 — facade selection grid (2D pick on a photo/render)
REQUIRED: a facade image (render or photo, straight-on), plus per-image:
`viewbox`, and a grid of unit cells `{unit_id, x, y, w, h}` (percent-of-image).
Source data to collect: how many "lines" (עמודות דירות) per facade, which
facade faces which street/sea, floors per line. Existing example:
`assets/projects/ashira-sde-dov/showroom-payload.json`.

## Layer 3 — unit hotspots on the 3D model
Per unit (in `assets_3d.unit_hotspots`, merged with `unit-map.json` facts):
```json
{ "unit_id": "a-08-03", "position": [x,y,z], "normal": [nx,ny,nz],
  "camera_orbit": {"theta":deg,"phi":deg,"radius":m},
  "floor": 8, "line": "SW", "status": "available" }
```
- Tier-B models: hotspots are COMPUTED (floor index × floor_height on the
  facade plane given orientation + line offsets) — needs `apartments_per_floor`
  and their line order, from the typical-floor plan (תוכנית קומה טיפוסית).
- Tier-A models: hotspots authored once in a calibration pass (click-to-place
  tool, TODO) or computed against the model's measured bounding envelope.
- Selecting a unit = highlight the exact volume: colored box `floor_height ×
  line_width × depth` at the hotspot, not just a dot (owner requirement).

## Data collection additions (feed into mega-prompt v3)
For every project ALSO collect: floors per building (exact), typical floor
plan image URL, apartments-per-floor + line layout, facade renders (per
orientation), building placement sketch/site plan, podium/lobby floors, roof
feature, facade materials/colors, balcony pattern, floor height if published.
Every item with source URL. These fields make Tier-B models honest instead of
generic.

## Honesty rules (inherited from the god-skill)
- Generated massing is always labeled "הדמיה להמחשה" on-page.
- No sea in the scene unless `dist_to_sea_m` is sourced and < ~1500m.
- Unit statuses/prices only from sourced inventory; otherwise "demo mapping"
  labels exactly as `unit-map.json` does today.
