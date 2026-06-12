# Project 3D Sales Experience Skill

Use this when adding or improving an interactive real-estate project model on nad-lan.co.il.

## Standard

- Start with a fast, premium model that can ship without BIM: architectural massing, floor selection, unit selection, and clear inquiry flow.
- The model must be interactive, not a static image. Minimum interaction: drag-to-rotate, floor selection, unit selection, selected-unit facts, and a view/inside preview mode.
- Do not publish invented prices, availability, apartment numbers, or floorplans. If data is illustrative, label it clearly and render price as `לפי פנייה`.
- Keep all real interest capture inside the existing lead system. Do not create a second lead endpoint.
- Every unit-level CTA must include `card_id`, `unit`, `floor`, `rooms`, `sqm`, and a source marker so the owner can see which apartment created the lead.
- A theoretical purchase CTA is allowed only as a non-binding inquiry. It must say availability, price, and terms require human verification.
- Use dark blueprint, champagne linework, restrained glass, and architectural geometry. Avoid cartoon buildings, fake stock photos, fake people, and fantasy renders.
- Make mobile usable first: no horizontal overflow at 390px, 44px tap targets for model controls, and stacked forms.

## CMS Contract

Use the existing `nadlan_project` metadata:

- `project_3d_image`
- `project_3d_viewbox`
- `project_3d_units`
- `project_3d_demo`

Recommended unit JSON fields:

```json
{
  "id": "R-34-E",
  "title": "קו E",
  "floor": 34,
  "rooms": 5,
  "sqm": 158,
  "balcony": 22,
  "dir": "צפון מערב",
  "line": "E",
  "view": "ים, פארק ושדה דב",
  "price": 0,
  "status": "available",
  "plan": ""
}
```

`price: 0` means `לפי פנייה`. Only official owner/developer data should set a price.

## Long-Term Upgrade Path

- Phase 1: pseudo-3D tower picker in `inc/project-3d.php`.
- Phase 2: owner-approved elevation image and real unit inventory.
- Phase 3: traced polygons or GeoJSON per floor.
- Phase 4: compound map with Mapbox 3D buildings and project pins.
- Phase 5: real BIM/IFC/glTF/3D Tiles when the developer provides source files.

## Sde Dov To Countrywide Rollout

Treat Sde Dov as the first district template, not as a one-off.

For each district:

- Create one `nadlan_compound` term for the district or subdistrict.
- Assign every real project card to that compound.
- Require city, lat, lng, developer, project status, unit count when sourced, and official links.
- Enable the compound map only after token, term, and project pins are present.
- Add project-level 3D only where the card has `project_3d_demo=1` or real unit/elevation metadata.

For countrywide expansion:

- Start with high-value districts: Sde Dov, Park Hayam Bat Yam, Glilot, Pi Glilot, Bavli, Kikar Hamedina, Givat Amal, Ramat Hasharon west, Herzliya marina and business district, Jerusalem entrance district.
- Normalize every project into the same unit JSON contract so one renderer can power all projects.
- Keep official data provenance in the project body or references list.
- Never generate fake inventory to fill gaps. Use a premium illustrative model with clear demo labeling until official data arrives.

## Data Quality Levels

- `concept`: visual massing only, no official unit data. Price shows `לפי פנייה`.
- `traced`: owner-approved elevation/floor polygons, but availability not verified. Price shows `לפי פנייה`.
- `inventory`: verified unit fields from owner/developer, still non-binding unless contract process exists.
- `bim`: real BIM/IFC/glTF/3D Tiles source connected to project/unit data.

Only `inventory` and `bim` can show specific prices or availability.

## v1.60.0 — Fully interactive buyer layer (Claude)

What shipped on top of the v1.59.x picker (all inside `inc/project-3d.php`, same look/borders):

- **FIX**: floor strip rendered zero buttons since 1.59.0 (`[].slice.call(new Set(...))` returns
  `[]` — Set is not array-like). Floor navigation works now. Lesson: never spread a Set with
  `slice.call`; use an indexOf-dedupe or `Array.from`.
- **Live view-from-unit**: when `nadlan_mapbox_token` option is set AND the project has `lat`/`lng`
  meta, the "מבט מהדירה" panel lazy-loads Mapbox GL v3.14.0 and places a free camera at
  `ground_elevation + 4.0 + (floor-1) × floor_height + 1.55` meters, looking 900m along the
  facade bearing, with 3D building extrusions. Honest fallback (gradient + "יופעל כאשר מפתח
  המפות יוזן") when tokenless. Camera math documented in
  docs/2026-06-11-rainbow-research-and-inventions.md (strand 2).
- **Sun insight (אור ושמש tool)**: pure-JS solar position (SunCalc-core formulas, no API), direct
  sun windows for summer/winter solstice per facade bearing (±70° cone, >8° elevation, Israel
  clock). Validated against NOAA: TA solstice noon elevation 81.3° exact. Sun hours also appear
  in the comparison table.
- **Compare**: up to 3 units, chips tray + overlay table (floor/rooms/sqm/balcony/dir/view/sun/
  status), "בחר" from table selects the unit. Persisted in localStorage per project.
- **Lead wizard**: 2 steps with progress dots (contact → progression details), multi-select
  advisors checkboxes (lawyer/mortgage/inspection/designer) joined into the lead payload
  (`advisor`, plus full list in message). Research basis: multi-step forms convert ~37% better.
- **Plan lightbox**: image plans open in-overlay; PDFs in iframe; other URLs default.
- **Deal-step tracker**: after successful submit, "בחירה" (and "ליווי" if advisors chosen) are
  marked done; lead reference id shown when the REST response includes one.
- **Selection persistence**: last selected unit restored per visitor (localStorage).

### Replication playbook — onboarding the NEXT project (fill-in-the-details)

No code changes needed per project. Per-building checklist:

1. Create/locate the `nadlan_project` post. Set post meta:
   - `lat`, `lng` (decimal WGS84) — enables live view + sun insight.
   - `project_3d_floor_height_m` (default 3.05; luxury towers 3.1–3.3).
   - `project_3d_ground_elevation_m` (coastal TA ≈ 5–25; from Google Elevation or city GIS).
   - `developer_name`, `project_status`, `num_units`, `city`, `address`.
2. Facade: upload an ORIGINAL elevation render → set `project_3d_image` + `project_3d_viewbox`
   (e.g. `0 0 1000 1000`). Trace per-unit polygons in those viewBox coordinates.
3. Units: fill `project_3d_units` JSON (one object per sellable line/unit). Template:
   `docs/templates/project-3d-units-template.json`. Required: `id`, `floor`. Strongly
   recommended: `dir` (Hebrew compass words — drives camera bearing AND sun calc), `points`
   (facade polygon), `plan` (drawing URL → lightbox), `rooms`, `sqm`, `balcony`, `view`,
   `building`, `availability`, `status` (available|reserved|sold).
4. If no verified inventory yet: tick `project_3d_demo` — prices show "לפי פנייה" and the demo
   disclaimer renders. NEVER enter invented prices.
5. Flag: `nadlan_feature_project_3d` must be ON; Mapbox token once globally in NadLan Features.
6. Verify: healthcheck `project_3d` block shows `renderer: premium_tower_picker_v4`,
   `view_from_unit: mapbox_live` (or `awaiting_token`), `sun_insight/unit_compare/lead_wizard:
   true`. On the page: click a floor on the tower, click a facade polygon, open אור ושמש (real
   hours appear if lat/lng set), compare 2 units, run the 2-step form, confirm the lead arrives
   with unit/floor/advisors/camera params.

### Countrywide note
Everything above is data-driven from post meta — the Sde Dov content seeder (MISSION-CODEX-
CONTENT) can populate steps 1–3 for every compound project programmatically. The same template
serves any tower in Israel.
