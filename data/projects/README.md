# `data/projects/` — the canonical project database (single source of truth)

**Every** project page, the 3D project map, and the page factory read from
here. Nothing about a project is hard-coded in a template or invented at render
time. If a fact isn't in this database with a source, it does not go on a page.
This is the place the owner asked for: "save all this data so all future
project generations use this database, inside the repo, accessible to all
agents."

## Layout
- `_schema.json` — the record shape (rich: identity, location, context/POIs,
  building_form, units+prices, market, urban_future, media, **assets_3d**,
  **content** (5-language article bodies), provenance, db_meta).
- `<slug>.json` — one file per project (easy diffs, no write conflicts between
  agents, the factory just globs the folder).
- `index.json` — generated roll-up (id, name, city, developer, status,
  ready_for_page).
- `_excluded.json` — sold-out / occupied / completed projects with the reason,
  so we never waste a research pass re-adding them.

## The honesty contract (non-negotiable, mirrors the god-skill)
1. Every non-null structured value carries a source (`<field>_src`) and, where
   possible, a verbatim quote in `evidence`. Unknown = `null`, never invented.
2. **Coordinates are only trusted when `location.geocode_status = "geocoded"`
   with a `geocode_source`.** Model-estimated coords live in
   `coord_estimate_unverified` and MUST NOT be used on the map. (This is why
   Rainbow was ~2–3 km off — it was a model eyeball pin. Every current record is
   `needs_geocode` until our pipeline geocodes the address via
   govmap.gov.il / Mapbox.)
3. `content.article.*` is REAL editorial per language — never
   machine-translated-and-passed-as-native.
4. A record ships a page only when `db_meta.ready_for_page = true`
   (geocoded + media + 5-lang article + no null in the page-critical set).

## Current state (2026-07-04)
- 31 records ingested from the ChatGPT Gush Dan batch. URLs HTTP-200 confirmed;
  a sample content-verified. **All are `ready_for_page: false`** — they need
  geocode + price + media + article before a page can be built honestly.
- Our own priority projects (Ashira, Dimri Yama) were NOT in the ChatGPT batch
  (it only crawled a few developer catalogues) — added as stubs to be filled.
- See `handoff/research/2026-07-04-gushdan-dataset-audit-and-prompt-v2.md` for
  the audit and the per-developer collection prompt, and
  `handoff/research/2026-07-04-rich-project-data-mega-prompt.md` for the deep
  per-project enrichment prompt that fills these records to page-grade.

## Pipeline to make a record `ready_for_page`
1. Collect (per-developer prompt) → base record here.
2. Geocode the address → `lat/lng`, `geocode_status:"geocoded"`.
3. Price pass (Madlan/Yad2/gov) → `units.price_*` + sources.
4. Enrich (rich prompt) → context POIs, building_form, media URLs, USPs.
5. Author `content.article.*` (5 languages, real).
6. Factory → `assets_3d` (GLB, facade variants, unit hotspots).
7. Flip `ready_for_page:true` → factory generates the page.
