# COWORK MEGA PROMPT - The Image Factory (research-first sketch plates)
Paste this whole file as the session prompt. Mission: populate every image
blank on nad-lan.co.il with ACCURATE, AUTHENTIC sketch-style architectural
plates that share one visual DNA. No glossy AI-photo look, ever.

## 0. THE DNA (the owner-approved reference)
The reference is the "Rainbow Residences" plate saved at
`handoff/claude-design/2026-07-02-image-refs/rainbow-reference.png` (and the
Dimri Yama page hero). Its ingredients - reproduce ALL of them every time:
1. **Medium**: fine-line architectural ink/pencil sketch on warm cream paper
   (#FAF7F1 family), like a master architect's presentation plate. Visible
   hand-drawn line quality, cross-hatching in shadows.
2. **Color**: mostly monochrome ink with RESTRAINED watercolor washes only -
   muted sea-teal for water, warm sand, soft sunset amber on the horizon, a
   single gold accent (#9C7A3C family) for highlighted elements. Never
   saturated, never photoreal, never "AI-colorful".
3. **Composition**: the building is the hero, drawn accurately (floor count,
   massing, facade rhythm); the REAL surrounding city fades to lighter sketch
   toward the edges (vignette into the paper).
4. **The 3D peek**: one apartment highlighted with a thin gold outline on the
   facade, connected by leader lines to a CUTAWAY 3D interior of that
   apartment floating beside the tower (furniture sketched, balcony visible).
5. **Annotations**: a small data card (floor, rooms, sqm, exposure, view),
   margin floor plans, a compass, feature icons with short labels, serif
   headline. Labels in clean English or Hebrew - match the page's language.
6. **Honesty**: everything geographic is TRUE (see the gate below). These are
   labeled on-site as "הדמיה להמחשה" - the drawing itself must never lie.

## 1. THE RESEARCH GATE (no image without it - this is the law)
Before writing any image prompt, build a FACT SHEET for the subject:
1. Pull the real record from our catalog (REST):
   `GET /wp-json/wp/v2/nadlan_project?slug=<slug>` then read meta via the page
   (floors, units, city, developer, lat/lng) - or ask the site healthcheck agent.
2. **Compute the true distance to the sea** (Tel Aviv coast sits at longitude
   ~34.7752 near Sde Dov):
   `distance_m = (lng - 34.7752) * 111320 * cos(lat_in_radians)`
   Verified today: Rainbow ~870m, Ashira ~1,170m from the shoreline.
   RULE: under 250m = seafront framing allowed; 250-1500m = the sea appears
   ONLY as a distant horizon band beyond city blocks; over 1500m = no sea.
3. Check the real surroundings on a map (what is actually north/south/east/
   west). Verified anchor facts for Sde Dov plates: the Reading power-station
   chimney stands ON THE COASTLINE to the SOUTHWEST, at the Yarkon river mouth,
   essentially at the water's edge - it must appear on the SEA side of the
   horizon, never inland (a test plate got this wrong). Around the towers:
   low-rise construction quarter with cranes; park strips; streets.
4. Confirm the building form from our data: floor count, podium, roughly
   rectangular vs twisting massing. Rainbow=40 floors with a gentle twist,
   Ashira=20 floors boutique, Dimri=24 floors. Never draw the wrong height.
5. Write the fact sheet INTO the prompt (the generator cannot research - you
   feed it the truth).

## 2. THE MASTER PROMPT TEMPLATE (fill from the fact sheet)
```
Architectural presentation plate, hand-drawn fine-line ink and pencil sketch on
warm cream paper, in the style of a classic architect's illustrated poster.
Subject: {PROJECT_NAME}, a real {FLOORS}-floor residential tower in
{NEIGHBORHOOD}, Tel Aviv. Draw the tower accurately: {MASSING_NOTES}.
Geography (must be accurate): the Mediterranean sea appears {SEA_TREATMENT};
{LANDMARK_NOTES}; surrounding blocks are {SURROUNDINGS_NOTES}, sketched lighter
and fading into the paper toward the edges.
One apartment on floor {N} facing {DIRECTION} is highlighted with a thin gold
outline on the facade, with fine leader lines to a floating 3D cutaway of that
apartment beside the tower: open living room, kitchen island, {ROOMS} rooms,
wraparound balcony with two sketched chairs, furniture drawn in the same ink
style.
Margin elements: a small data card titled "{UNIT_LABEL}" listing floor {N},
{ROOMS} rooms, {SQM} sqm interior, balcony, exposure {DIRECTION}, view
{VIEW_DESC}; two small floor plans top-right; a compass; three small circular
feature icons on the left with short labels; an elegant serif project title
top-left.
Color: monochrome ink with restrained watercolor washes only - muted teal for
distant water, warm sand tones, a soft amber sunset on the horizon, single
muted gold accents for the highlighted apartment and rules. No saturated
colors, no photorealism, no lens effects, no people. Square 1:1, extremely
detailed linework, clean cream background.
```
SEA_TREATMENT values: "as a thin distant horizon band beyond several city
blocks, clearly {DIST}m away - the tower does NOT sit on the beach" (250-1500m)
or "prominently along the west edge" (only if truly under 250m) or omit.

## 3. THE IMAGE MAP (every blank to fill, with sizes)
Generate at 2048px+, downscale on upload. One subject at a time, QA each.
| # | Surface | Subject | Ratio | Notes |
|---|---|---|---|---|
| 1 | Ashira project hero + og | Ashira plate (example below) | 1:1 + 1200x630 crop | replaces current poster on page + sharing |
| 2 | Rainbow project hero + og | 40-floor twist, sea ~870m distant | same | fix the reference's wrong beachfront framing |
| 3 | Dimri Yama hero + og | 24 floors, honest sea distance | same | keep its DNA, move the sea to the horizon |
| 4 | Homepage hero flag card | best of #1-3, tighter crop | 16:11 | the card beside the H1 |
| 5-11 | 7 demo listings (IDs 4951-4957) | each listing's real street/type: tower/midrise/garden/penthouse per its meta; interior cutaway matching its rooms/sqm | 4:3 | replaces the flat SVG sketches; keep "לדוגמה" honesty |
| 12-19 | Areas grid cities (תל אביב, ירושלים, חיפה...) | one recognizable REAL cityscape vignette each (researched skyline/landmark, e.g. Jerusalem stone + light rail, Haifa slope + bay) | 4:3 | small washes, same paper |
| 20 | /en/ hub hero | Ashira plate variant with English labels | 16:9 | |
| 21 | /advertise/ header | plate showing a tower + the gold-outlined apartment + a lead card - "the selection moment" | 16:9 | the sales story in one image |
| 22+ | News/magazine fallback images | keep the existing branded flat graphics (they are fine) | - | skip |
Professionals keep their monogram portraits - do NOT generate faces.

## 4. THE PROCESS (per image)
1. Fact sheet (Part 1) -> fill the template (Part 2).
2. Generate (ChatGPT/DALL-E or equivalent). 2-3 candidates.
3. QA gate before upload - reject if ANY fails:
   - geography honest (sea distance, landmarks on the correct side)
   - floor count within +-1 of reality; massing recognizable
   - palette matches the DNA (cream/ink/muted washes/gold), no AI-gloss
   - no garbled text in the plate (regenerate or ask for blank labels and
     add text later); no invented brand names; no people
   - style-match: put it beside the Rainbow reference - must look like the
     same artist made both
4. Upload to WP media (`POST /wp-json/wp/v2/media`, filename slugged, Hebrew
   alt text describing the REAL subject + "הדמיה להמחשה").
5. Place: set as featured image / project_model_poster meta / page content as
   the slot requires; verify on the live page (rendered body, not head).
6. Log each plate in docs/content/2026-07-02-publish-log.md: subject, fact
   sheet used, media ID, placement, QA result.

## 5. LAWS (unchanged, always)
No em-dash in any user-facing text. Site name "נדלן"/NadLan only. Never imply
beachfront when it is not. Everything labeled honestly. Generated plates are
illustrations, not renderings of contract - the disclaimer stays on pages.
