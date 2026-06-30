# Sketch-art generation spec — the one visual language, sitewide

Owner-approved style reference (2 images, 2026-06-30): hand-drawn sepia/graphite architectural
axonometric illustration — NOT photoreal AI rendering ("I don't want AI-generated colored
pictures... it looks cheap"). This is the art direction for every static/thumbnail image on
the site: project heroes, area cards, listing cards, professional profile frames, article
headers, gallery images. The live interactive 3D model is a SEPARATE thing (see part 2).

## What makes the reference images work (so regenerations stay consistent)
- Monochrome/sepia pencil-and-ink line art on aged paper, NOT full color photoreal.
- Loose construction/guide lines visible at the edges (compass rose, dimension lines, floor
  plans floating in the margin) — reads as an architect's working drawing, not a finished ad.
- One aerial 3/4 view of the tower + its podium/low-rise context + the real shoreline/skyline.
- Where it shows interior: an exploded/cantilevered floor slab cut away from the tower, furniture
  and rooms drawn in the same sketch line weight (not a separate photo pasted in).
- Light, sparse color accents only (a gold highlight ring on one floor, pale sunset wash) —
  never full saturation.
- Optional UI chrome drawn INTO the image for marketing/hero use: project name lockup, compass,
  a small "residence card" (floor/rooms/sqm/exposure/view), bottom icon nav. Thumbnails for
  cards/listings should NOT include this chrome — clean illustration only, chrome is real HTML.

## Reusable prompt template (hand to Cowork -> ChatGPT image generation)

```
Hand-drawn architectural axonometric illustration, sepia and graphite pencil on aged paper,
in the style of a luxury real-estate developer's presentation sketch (not a photo-real render,
not full color, not a flat vector icon). Aerial three-quarter view of {PROJECT_NAME}, a
{FLOOR_COUNT}-floor residential tower in {LOCATION}, with {CONTEXT: e.g. "a low-rise podium
with rooftop pool, palm-lined boulevards, the Mediterranean coastline and marina to the west,
the Tel Aviv skyline and Reading Power Station chimney to the east"}. Loose construction lines,
a compass rose, and a fragment of floor plan visible at the edges. Soft sepia wash with one or
two pale gold highlight accents, never full saturation. {VARIANT}.
```

`{VARIANT}` by use case:
- **Exterior hero / thumbnail card:** "Clean illustration only, no text or UI overlay."
- **Interior / unit reveal:** "with one floor slab cantilevered out from the tower in an
  exploded cutaway, furnished rooms (living room, kitchen, bedrooms) drawn in the same sketch
  line weight, labelled lightly in the margin."
- **Area / neighborhood card:** "wider view emphasizing the surrounding streets, parks and
  shoreline rather than the tower itself."
- **Article / guide header:** "a relevant real-estate scene (e.g. a notary's desk with house
  keys and documents, a family viewing a floor plan) in the same sketch line language."

## Part 2 — the interactive 3D model is a separate problem, not solved by images

The owner wants the actual GLB geometry (what `model-viewer` renders and the floor/apartment
hotspots sit on) to be far more detailed than the current concept massing blocks, AND wants a
"select a floor -> it highlights/embosses that exact volume -> a drawer slides out revealing
the interior" interaction. Two different gaps:

1. **Better geometry.** No contractor BIM/CAD exists yet. The owner's current method is
   reverse-engineering from each developer's own public marketing renders/floor plans. A
   reusable pipeline for this needs an image-to-3D or text-to-3D generation step Claude Code
   cannot run directly (no such tool in this environment) — this is a Cowork-driven job: try an
   image/text-to-3D generator (e.g. Meshy, Tripo, Luma) seeded with the gathered marketing
   images + floor plans per project, export GLB, drop into
   `plugins/nadlan-config/assets/showroom-engine/models/{slug}.glb` +
   `assets/engine/{slug}.glb` (same file, both places, as already established). Claude Code
   then wires it in immediately — that swap is a one-line config change, already proven safe.
2. **The select -> emboss -> drawer interaction.** This is real frontend engineering Claude Code
   CAN build now, against the CURRENT models, so it does not have to wait on better geometry.
   Scoped next: highlight the selected unit's hotspot volume (model-viewer hotspot + a styled
   overlay sized from `stage_x/y/w/h` or `position`/`normal`, already in the data), animate the
   existing slide-out unit panel as a "drawer," and use the interior tour slot that already
   shipped (`engine.js` `interiorTour()`, PR6/1.69.59 — supports `tour_url` or
   `interior_panoramas[]`, lazy-loaded, currently empty for every unit) to show the sketch-style
   interior image from Part 1 once generated. The mechanism already exists; it just has no
   content yet.

## Status
Not yet generated or wired. This is the spec Cowork executes against (Job 5 in
`docs/agent-comms/cowork-next-missions.md`).
