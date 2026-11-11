# Kikar journey: how Ashira, DUO, Rainbow and the showroom engine work (inventory, 11.11.2026)

Read-only code inventory. Branch read: claude/apartment-experience-b1. Memory warns that the live copy of
inc/project-stage.php can differ from the repo, so read live before any hunk. Paths are under plugins/nadlan-config/
unless they start with docs/. PS = assets/project-stage.

## 0. Who is "Dor on Ibn Gvirol"
No project named Dor/דור exists in the repo or in the WP exports. The evidence points to DUO Tel Aviv (post 4893):
- address Arlozorov 85-87 / Ibn Gvirol 112א-118 (data/projects/duo-tel-aviv.json:22);
- project-stage.php:149 "אבן גבירול פינת ארלוזורוב, מתחם סומייל";
- AGENT-LOG.md:658 (6.8.2026) "the era when a buyer picked a unit on DOR and converted". That note comes from the
  showroom-engine era, so it means DUO on engine.js, before the stage of 28.9.

Second candidate: H Infinity (Hagag, Ibn Gvirol and Jabotinsky, post 6548). Nothing shows it ever had a 3D picker.

## 1. Journeys side by side

| | Ashira / Dimri (PS/ashira, PS/dimri) | DUO (PS/duo) | Rainbow (PS/rainbow) | Showroom engine (assets/showroom-engine; DUO in Aug, Aurelia now) | Kikar today (PS/world + journey + cockpit) |
|---|---|---|---|---|---|
| First screen | poster.jpg, then a 3.6 s intro flight (stage.js:2079-2090); hint pill rbs-hint "בחרו מגדל וקומה" (380, 44) | same, N/S towers | same, hint "בחרו קומה במגדל" | model-viewer GLB + chip "גררו לסיבוב... לחצו על נקודה בבניין" (mv-ux.js:102-112) | journey entry card before the grid, "בחרו את הדירה שלכם" (journey.js:171-190); desktop also mounts world.js |
| Turning | OrbitControls on the whole scene, drag; auto-orbit after 6 s idle (stage.js:726-740, 2118-2125); no per-tower turn | same | same | drag, snaps to 22.5° (mv-ux.js:53-99) | desktop: orbit; tower mode orbits the camera around the chosen tower (world.js:1858-1870); phone: no 3D, a still aerial |
| Pick | raycast on invisible per-tower proxies gives the floor (3314-3327, 1001-1009); then the floor ring: a tap near the ring snaps to an example-apartment side (1343-1359, 1072-1081); keyboard too | same | single tower proxy | DOM hotspot buttons per unit on the model (engine.js:372-376), plus a list | phone: pill buttons on a picture, then a floor slider, then a list of views (journey.js:103-125). Desktop: tap a tower in tower mode for the floor (world.js:3118-3131); facing only through 8 panel buttons (2845-2849), no tap on the facade |
| After pick | floor card: tower, "קומה N" + "דירה לדוגמה", facing line; actions להיכנס לדירה 360 / הנוף והמפה / לעצב את הדירה; CTA "לקבלת תוכניות ומחירים" (stage.js:398-420, bridge.js:157-166). Under the stage: the view from the floor (Mapbox satellite at floor height) beside the area map with the beam | same | same | side panel or unit-journey v2 (engine.js:459-486, 2243-2257) | full-screen cockpit, 9 tiles (cockpit.js:96-104) |

## 2. Next-tap cues
- **Stages:**
  - rbs-hint pill (stage.css:82-99)
  - hover glow, preview arrow and arc (mouse only)
  - the facingHint text
  - the steps bar 1-4, `nlps-step` with `aria-current` (project-stage.php:867-871, bridge.js:621-623)
  - the button `nlps-facbtn` "המתקנים בפרויקט"
  - No keyframes, pulse or coach marks in any stage.css. The only animation is tour.css:123 `nlat-door-halo` on 360 doors, and tour.js:72-74 shows "גררו כדי להסתכל מסביב".
- **Engine:** a pulsing ring on recommended units (showroom.css:111-113); a 3x pulse on "נוף מהחלון" (unit-journey.css:411-442).
- **Kikar:** only the glow band on the floor slider.

## 3. The beam
- **bridge.js `showBeam` (754-782):**
  - a Mapbox marker holding a 150px SVG wedge, #C2563A, gradient 0 to 0.55;
  - `rotationAlignment: map`, `setRotation(bearing)`;
  - `map.easeTo`: the bearing points up, the centre is 450 m ahead, zoom 14.3, 900 ms.
- **What fires with it:** every `nl:facing` (349-368) also runs:
  - `showView`: Mapbox satellite-streets in 3D at floor height (680-746);
  - `showNear`: the list from quarter.json (229-264);
  - the unit line above the map, "האלומה במפה: הכיוון מהדירה" (520-548).
- **Origin:** engine.js `showViewCone` (1318-1335) plus `easeMapToUnitView`. The doctrine is docs/playbooks/the-beam-field-guide.md.
- **Layout:** the `.nlps-below` grid has two columns, view | #nlpjx-map (project-stage.php:874, 1644-1646). Under 1100px it becomes one column (1680). #nlpjx-map is moved up from the page bottom (990-997).
- **Kikar:**
  - bridge.js is NOT loaded for world configs (project-stage.php:1048-1049, 1583, 1597).
  - The area map is moved under the world (1248-1249), but nothing beams on it.
  - world.js draws a gold 45° wedge, 70 m long, inside the 3D scene (buildSelection/updateSelection 1456-1521). It has no map.

## 4. Inquiry about one apartment
- **Stage CTA** (floor card and #nlps-wa): opens wa.me/<site> with the text "שלום, אשמח לקבל תוכניות ומחירים לדירה בקומה N ב<project>, <sector words> (nad-lan.co.il)" (bridge.js:305-312). Language pages use i18n-dom.js:22-40. The unit id is NOT in this text. It is in `?unit=` (keepUnit 324-331) and in `__nlpsPick` (352).
- **Consult sheet** (site pill, inc/cta-sheet.php:137-180):
  - context line "<tower> · קומה N · <facing> (דירה לדוגמה, S1-25-w)";
  - chips תוכניות ומחירים / הנוף מהדירה / שינויים ועיצוב / פגישה עם נציג;
  - when to call back, a note, an editable message;
  - the link page?unit=<id>;
  - GA `whatsapp_sheet_open` and `whatsapp_click`, both carrying the unit.
- **Designer:** `/tour/designer/?project=&unit=&pn=&ul=` (bridge.js:594-603). It sends `/lead` and `/rfp` (designer-tour.html:2036-2055).
- **Basket:** `nl:facing` fills the unit (basket.js:42-57). Its WhatsApp text leaves the unit id out (321-333).
- **Video:** TogetherRoom opens with `?room=new`. The unit syncs from `nl:facing` (together.js:990-1030), but it is not sent when the room is created (453).
- **Engine:**
  - "הפנייה מתייחסת לדירה {label} · קומה..." (engine.js:4290-4293);
  - forms that carry the unit (4308-4314, 3443-3467);
  - the buyflow RFP carries the unit (buyflow.js:280-294).
- **Kikar:**
  - The cockpit's WhatsApp icon uses the page link "שלום, אשמח לפרטים נוספים על %s" (project-stage.php:1058, 1155; cockpit.js:236). No unit.
  - world.js sets `__nlpsPick` with `unit: ''` (1969-1973). The journey path sets no `__nlpsPick` at all.
- **Real use:** one anonymous Ashira visitor chose an apartment, looked at the view and pressed WhatsApp (docs/sales/ashira-meeting-2026-10/BRIEF-film.md:6-7; memory nadlan-ashira-meeting-2026-10). The repo holds no counts and no exports.

## 5. After the pick
- **Stages:**
  - tour.js 360: rooms and balcony, `nlat-door` doors, `walkTo` crossfade (339-434), a lift panel (437-497), styles bare/warm (125-162).
  - BuildingWalk (bridge.js:424-460), driven by the `walk` entry in facilities.json on DUO and Rainbow.
  - slice.js: the floor plan as wedges, which calls `selectUnit`; it also opens the basket (slice.js:206).
  - The designer (bridge.js:610).
  - Facility pins with a 360 (stage.js:1905-1935).
  - Quarter pins with "מה רואים מאשירה לכיוונו", through `lookToward` (1936-1977).
  - Ashira's free walk in an iframe (project-stage.php:793-796).
- **Kikar cockpit:**
  - view renders;
  - one living-room 360 per tower, floor and side, with no doors;
  - plan, facilities 360, price, area, film, compare and send.
  - The designer was removed in 1.72.639.

## 6. Analytics
- **The GA function:** `nadlanGA` (conversion-cta.php:155).
- **bridge.js events:** stage_floor 340, stage_facing 355, quarter_pin 372, whatsapp_click 379/382, floor_slice 409, tour_room 450, tour_open 468/475, tour_direction 483, facility_tour 492, map_back 589, floor_action 608, stage_step 628, quarter_legend 647, deal_floor_click 657.
- **Kikar events:**
  - journey_* (journey.js:134-168);
  - cockpit_open, _tile, _save, _share, _call, _wa (cockpit.js:259-300);
  - stage_floor and stage_step from the world boot.
- **Ashira:** walk_open (project-stage.php:796).
- **Visit trail** (inc/visit-trail.php, live since 1.72.602):
  - It listens to nl:floor, facing, view, quarter, facility, facility-tour, floor-cta, floor-action, tour and example (trail.js:39-42).
  - The facing line template is at 392.
  - The lines go into the lead's meta and into the new-lead email (707-724).
  - A WhatsApp tap is not a lead row, so it carries no trail (21).

## 7. Kikar: what was lost
1. The beam on the map, because bridge.js is not loaded.
2. Tapping a direction on the building (the ring and the example-apartment arcs). Kikar picks the facing with buttons or a list.
3. 3D on the phone. Phones get a picture and a slider, no model.
4. The unit id in the inquiry. The cockpit's WhatsApp is generic, and `__nlpsPick.unit` is empty.
5. Moving room to room in 360 (tour.js doors, BuildingWalk), the designer (removed in 639), and the quarter pins with "what you see from here".

Also lost:
- the steps bar 1-4;
- the view from the floor beside the map;
- the `?unit=` deep link (Kikar uses `#dira=`).

## 8. Reuse map

**a) Each tower turns on its own**
- Exists: nowhere.
- Closest: world.js tower mode, a camera orbit around one tower (1858-1870); orbit.js, a 24-frame drag picture (not used).
- To bring it: new work.

**b) Tap an apartment on the tower**
- Exists: stage.js ring, `unitArc` and proxies (1072-1359); engine hotspots (engine.js:372-376).
- To bring it: port the ring and arc into world.js tower mode. world.js already has `rayCylinder` floors and the `aptCorners` PLAN (1557-1588).

**c) A map with a beam that reacts at once**
- Exists: bridge.js `showBeam`, `showView`, `showNear`, `setMapSum` (229-782).
- To bring it: world.js already emits `nl:facing` with a bearing, so a slim beam-only bridge that listens to it on hamedina is enough. It needs `cfg.lat`/`lng`/`token` and `NLPJX_MAP`.
- Risks: on phones the area map sits far down the page. Kikar's three towers need a lat/lng origin per tower, while bridge uses one point.

**d) A pulse on the next thing to tap**
- Exists: only in the engine CSS (showroom.css:111-113, unit-journey.css:411-442) and tour.css `nlat-door-halo`. The stages have none.
- To bring it: must be built.

**e) The apartment panel leading to design, inside view, facilities**
- Exists: the floor card actions (bridge.js:157-166, 606-611). The cockpit tiles already exist on Kikar.

**f) Moving room to room inside the apartment**
- Exists: tour.js doors and BuildingWalk, live on Ashira, DUO and Rainbow.
- To bring it: Kikar has single panoramas only. It needs door hotspots and more renders per apartment.

**g) Facilities and neighbouring buildings tappable from outside, "like Google Earth"**
- Exists: stage quarter and facility pins (stage.js:1815-1977); world.js places and labels (2123-2580); the CesiumJS earth (inc/earth-experience.php, /earth/sde-dov and /earth/somail/, capped at 85 a day, not linked).
- Risk: the cost of the Google tiles.

**h) An inquiry tied to the specific apartment**
- Exists: cta-sheet.php `pickLine` and `?unit=`; bridge `waUrl`; the designer's lead and RFP.
- To bring it: Kikar needs `__nlpsPick.unit` filled, and the cockpit's WhatsApp must carry the unit. Ben's rule is that the WhatsApp wording is his alone, so get his word before changing the text.

## Not found
- Real counts of apartment taps or WhatsApp presses.
- GA or Hotjar exports.
- Which apartment the Ashira lead was about.
- Per-tower rotation anywhere.
- Which posts currently have `project_mode=showroom`. That is database state.
