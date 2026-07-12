# International Project Intake Pipeline (the standing workflow)

When a developer/agent sends materials (or a site link), this is the assembly
line that turns them into a live premium project page. Proven end-to-end on
LION APARTMENTS (Oliel Group, Paphos) 2026-07-12 - use that run as the worked
example (dossier: handoff/cyprus-flagship/lion-apartments-intake.md).

## Stage 0 - AUTHORIZATION (never skip)
The owner confirms the developer asked to be listed. Real names/branding only
with explicit permission; otherwise anonymize and badge as illustrative.

## Stage 1 - MATERIAL INTAKE (30-60 min)
1. Source sweep: developer site / brochure / drive. If a WP site: the
   `*-sitemap.xml` files enumerate every property page (worked when the cards
   were JS-rendered and REST hid the CPT).
2. Extract the VERIFIED SPEC: name, exact location, plot, buildings, floors,
   unit count + mix (rooms/sqm ranges), price-from, status, full amenity list,
   payment plan. Copy the developer's own numbers - never invent.
3. Download the materials: hero render, 3-5 renders/interiors, EVERY
   architectural plan sheet. VIEW THEM (Read tool renders images) - the master
   plan drives the 3D massing; the facade renders drive the style notes.
4. Write the intake dossier to `handoff/<project>/<name>-intake.md`:
   spec, visual DNA, unit-inventory derivation, build plan. This file is the
   contract for the rest of the pipeline and survives context loss.

## Stage 2 - WORLD CHECK (5 min)
The project's country must exist in `nadlan_gw_worlds()` (inc/global-worlds.php)
with full HE+EN content (SEO head, intro, 8 facts, guide, FAQ, dated sources).
If missing - write it first (Cyprus entry = the template).

## Stage 3 - THE 3D MODEL (30 min)
1. Derive the site spec JSON from the master plan: building rectangles
   (x,z,w,d,floors), courtyard/pool position, floor_h from the section or
   3.0-3.2 default. Keep real proportions (plot sqm -> site extents).
2. `python3 scripts/generate-rich-building.py <spec.json> \
    plugins/nadlan-config/assets/showroom-engine/models/<slug>.glb`
3. Sanity: bounds match the plot, tris < 20K, size < 500KB.
4. `python3 scripts/build-inventory.py` + commit (GLBs are never silent).
The model ships INSIDE the plugin zip - no separate upload.

## Stage 4 - MEDIA (10 min)
Upload renders + plans to OUR media library via POST /wp/v2/media with clean
names (`<slug>-hero.jpg`, `<slug>-masterplan.png`). NEVER hotlink the source.

## Stage 5 - DATA (20 min)
1. Unit inventory: derive per building x floor x type from the real mix
   (Lion: 72 = 4 buildings x 3 floors x 6 types), price scaled by type +
   floor premium, statuses mixed unless the developer supplies real ones.
2. Model layout JSON: `{fh, buildings:[{x,z,w,d,floors}]}` - MUST equal the
   GLB spec, this is what places the hotspots on the right facade.
3. Facilities pairs [he,en] from the developer's real amenity list.

## Stage 6 - SEED + SHIP
Add the row to the gw-seed rows (or fill the metabox by hand - every field
is CMS-editable on the nadlan_intl edit screen): slug, world, district he/en,
lat/lng (verify on a map!), price/units/floors/delivery, yield note (labeled,
never a promise), payment, fees, about he/en, fac, glb, layout, apts_custom,
gallery, plans, `real => true` (real projects are NOT demo-badged; their
honesty note - "data from the developer's publications; the 3D model is a
conceptual visualization" - lives in the about text).
Then the WELDED CHAIN (skill: wordpress-agent-deploy) + POST /gw-seed?refresh=1.

## Stage 7 - VERIFY (the aesthetic-ownership duties)
- Page 200 in HE + EN; hotspot count = unit count; picker panel opens with
  the right unit; floor chips filter; gallery + plans render; map pin on the
  real coordinates; lead form posts; GLB loads (curl the .glb URL).
- Word/honesty audit: no em/en dashes, every estimate labeled, the developer's
  numbers match the source page.
- Report to the owner with the live URL and what remains for his eyes.

## Failure modes learned on the Lion run
- JS-rendered card grids hide property links -> use the sitemap.
- `\"` inside single-quoted PHP prints a literal backslash -> plain `"`.
- The generic-tower hotspot geometry floats off low-rise sites -> the layout
  JSON exists precisely so hotspots ride the real buildings.
