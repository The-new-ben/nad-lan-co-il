# Properties Catalog — architecture & build plan

> **Notice to all agents:** the owner wants a competitive **properties catalog** (listings). This is a substantial build with a real data model, archive/single templates, filters, map, and monetization hooks. This skill is the architecture + phased plan so any agent (Codex, Claude, Antigravity) builds it consistently. Design comes from `design-page-patterns.md` §city + `design-components.md` §listing-card + `design-monetization-surfaces.md`. Data model from `strategy-master.md` §9.

## Strategic framing (read first)

We will NOT win a head-to-head inventory war with Yad2/Madlan (they have hundreds of thousands of listings; verified in `serp-snapshots-2026-05.md`). So the catalog is **not** a generic listings board. It is:
1. **A curated/quality catalog** tied to our pillars and the lawyer-owner's deal flow — fewer, better, verified.
2. **A data-intelligence layer** over open `nadlan.gov.il` transaction data — price trends, ₪/m², neighborhood profiles (this is Madlan's winning move; we do it with editorial restraint).
3. **A monetization surface** — sponsored listings, developer projects, premier professional placements (see `design-monetization-surfaces.md`).

The catalog's job is to make a visitor at the highest-intent moment (browsing actual properties) convert into a lead for the law practice / partners.

## Data model — CPTs (register in the `nadlan-config` plugin, NOT the theme)

Per the plugin discipline + theme-can-be-swapped lesson, all catalog CPTs live in `nadlan-config` (the plugin that reliably loads). Plugin v1.1.0+ scope.

### CPT `nadlan_property`
Slug: `/properties/{slug}/`. Public, REST-enabled. Fields (meta or ACF-free `register_post_meta`):
- `listing_type` enum: sale | rent
- `property_type` enum: apartment | penthouse | garden | cottage | commercial | land | new_project_unit
- `price` int (₪) · `price_per_sqm` (derived)
- `rooms` float · `floor` int · `total_floors` int
- `size_sqm` int · `balcony_sqm` int
- `parking` bool · `elevator` bool · `ac` bool · `accessibility` bool · `protected_room` (ממ"ד) bool
- `city_id` · `neighborhood_id` · `street` · `building_number`
- `lat` · `lng`
- `status` enum: active | under_offer | sold | rented
- `listed_at` · `updated_at`
- `agent_id` (→ `nadlan_professional`) · `project_id` (→ `nadlan_project`, nullable)
- `photos[]` (media IDs) · `description` (clean Hebrew)
- `source` enum: own | partner | gov_import
- **Monetization (from design-monetization-surfaces.md):** `is_sponsored` bool · `sponsor_name` · `sponsor_logo` (media) · `sponsored_until` datetime · `sponsored_position_preference` int
- Schema: emit `RealEstateListing` JSON-LD only for visible facts (per quality gates).

### CPT `nadlan_project` (developer projects — high monetization)
Slug: `/projects/{slug}/`. Fields: name, developer_id, city/neighborhood, lat/lng, status (presale/marketing/under_construction/occupancy), price_min/max, units_total/available, delivery_eta, brochure_url, gallery[], `is_sponsored` + sponsor fields. This is where developer ad revenue lands (20-80K ₪/mo per `monetization-lawyer-angle.md`).

### CPT `nadlan_professional` (directory — recurring revenue)
Slug: `/professionals/{slug}/`, taxonomy `profession` (broker/mortgage_advisor/lawyer/appraiser/inspector/architect). Fields: full_name, license_no, agency, cities[], specialties[], photo, bio, languages[], `tier` enum(free/pro/premier), `verified` bool, reviews_avg/count. Tier differentials in `design-monetization-surfaces.md` §F.

### Custom table `nadlan_transactions` (gov data mirror — the intelligence layer)
Volume too large for `wp_posts`. Custom table: gov_id, city_id, neighborhood_id, street, building_number, date, price, rooms, size_sqm, floor, year_built. Source: `nadlan.gov.il` open data. **Legal note:** confirm re-publication rights (owner is a lawyer — should make this call; flagged in `honesty-statement.md`). Drives the price-trend charts + neighborhood ₪/m².

### Taxonomies (shared)
`city` (→ `/cities/{slug}/`) and `neighborhood` (→ `/cities/{city}/{nbhd}/`). These already have content pages (the 11 Codex city pages) — the catalog binds properties to them.

## Templates (theme — block templates / patterns)

| Template | Source spec |
|---|---|
| Archive `/properties/` | `design-page-patterns.md` §city listings grid + sticky filter bar (`design-components.md` filter chips) |
| Single property | new — build from listing-card hero + spec table + map + agent card + lead form + `RealEstateListing` schema |
| Project single | `design-page-patterns.md` §G projects + brochure + developer contact |
| Map archive view | `design-components.md` §map widget (monochrome cream basemap, gold pins, MapLibre + OSM, no Google) |

Listing card: full state spec is in Lovable round-2 GAP 3 (`docs/design/lovable-output-round-2.md`) — save/favorite toggle, new/price-drop badge, skeleton loading, empty grid state. The `.listing-card` CSS class is **already in the live bundle**.

## Filters (the competitive UX)

Sticky filter bar: listing_type · city · property_type · price range (dual slider) · rooms · size · special (parking/elevator/ממ"ד). Implemented as a REST-query front-end (`/wp/v2/nadlan_property?...`) with the luxury `.input-underline` + hairline pill chips. No page reloads — fetch + re-render the grid. Vanilla JS, like the calculators.

## Map (the "wow" for the catalog)

MapLibre GL JS + OSM tiles (Stadia/MapTiler free tier — confirm with owner, no new paid commitment without approval). Monochrome cream basemap matching the palette. Gold pins, cluster bubbles, hover popovers. Full spec in Lovable round-2 GAP 2. **This is the Madlan-killer when paired with the gov-data price overlay.**

## Build phases (incremental, each verifiable)

- **Phase A — CPTs + a few seed properties (no map).** Register `nadlan_property` in plugin v1.1.0 (function_exists-guarded, English labels, one capability per release per plugin lessons). Add 5-10 seed properties via REST. Build a basic archive (grid of `.listing-card`) + single template. Verify via healthcheck + REST.
- **Phase B — Filters.** Front-end filter bar querying the REST endpoint. No reload.
- **Phase C — Map.** MapLibre archive view with gold pins + popovers.
- **Phase D — Projects + Professionals CPTs.** Developer projects (ad revenue) + professional directory (subscription revenue) with tier differentials.
- **Phase E — Gov-data intelligence.** Import `nadlan_transactions`, build price-trend charts on city/neighborhood pages, ₪/m² overlays on the map. (Legal opinion on re-publication first.)
- **Phase F — Monetization activation.** Flip `is_sponsored` flags, premier tiers, the reserved ad slots (`design-monetization-surfaces.md`). Revenue becomes a content decision, not a rebuild.

## Who builds what

- **Plugin CPT registration + REST endpoints**: Claude or Codex, in `nadlan-config` plugin (one capability per version, healthcheck-verified — `nadlan-config-plugin.md` rules).
- **Templates + filter/map JS**: Claude (precision) or Codex (bulk), using the live luxury bundle classes.
- **Property content + photos**: Codex (Hebrew descriptions + `image-pipeline.md` for photos). Gov data import: a scripted ETL (PowerShell/Python on owner's machine or a scheduled job).
- **Legal (gov-data rights, broker-law compliance for listings)**: owner (lawyer).

## Open decisions for owner

- [ ] Where do the first real listings come from? (Own deal flow? A partner broker's feed? Gov data only?) This decides Phase-A seed.
- [ ] Map tiles: OK to use MapTiler/Stadia free tier (no cost at low volume)? Needed for Phase C.
- [ ] Legal: can we re-publish `nadlan.gov.il` transaction data in a commercial catalog? (Owner's call.)
- [ ] Broker-law (חוק המתווכים): if we display third-party listings, confirm the disclosure/structure so we're not acting as an unlicensed broker. (Owner's call.)

## Open TODOs

- [ ] Phase A: register `nadlan_property` CPT in plugin v1.1.0 (after owner answers "where do listings come from").
- [ ] Mirror the live header override to `docs/wp-state/template-part-header.html`.
- [ ] Pull the listing-card / map full specs from Lovable round-2 GAP 2 + GAP 3 into `design-components.md` (currently referenced, not inlined).

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Owner asked to "start to develop the catalog" — this is the architecture + phased plan; Phase A build pending the owner's listings-source decision._

## Update 2026-05-28 — Phase A foundation shipped

- **Plugin v1.1.0 built**: registers `nadlan_property` + `nadlan_project` + `nadlan_professional` CPTs (public, REST-enabled, with archives at `/properties/`, `/projects/`, `/professionals/`), plus `nadlan_city` hierarchical taxonomy + `nadlan_profession` taxonomy. English labels (admin-only) per lessons. function_exists-guarded. Single capability addition per release.
- Healthcheck endpoint now reports catalog readiness: `catalog.nadlan_property_cpt`, etc.
- Owner approved: gov.il data, free map tiles, legal re-publishing — all green-lit.
- Plugin ZIP at repo root: `nadlan-config.zip` (built from `plugin-build/`). Owner uploads via standard WP admin (delete old → upload new → activate).
- **Next on Phase A** (after owner installs v1.1.0):
  1. Verify CPTs via healthcheck `catalog` block.
  2. Add `register_post_meta` for the property fields (listing_type, price, rooms, sqm, lat, lng, photos, agent_id, is_sponsored, etc.) — gated for REST writes.
  3. Seed 5–10 properties via REST.
  4. Build archive template using `.listing-card` class (already in the luxury CSS bundle).
  5. Build single-property template with `RealEstateListing` schema.
