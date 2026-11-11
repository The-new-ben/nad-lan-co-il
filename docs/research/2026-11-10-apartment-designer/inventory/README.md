# HAD-701 inventory: what we already have for the new apartment engine

10.11.2026. Read-only research for the engine that replaces `/tour/designer/`: a plan the buyer designs, turning into an interior 3D, tied to each project's apartment plans, with finishes, prices, a spec sheet and a video call with shared control.

Files in this folder:

- `README.md`: this inventory, with a reuse, rebuild or drop verdict per component.
- `links-to-old-designer.csv`: every place that links to the old designer (file, line, live URL, context). 23 rows.
- `plans-by-project.md`: the real, derived and schematic plans we hold, per project.
- `screenshots/`: 30 images. Captures of live pages and of the local walkthrough lab, taken with headless Chrome over CDP, plus copies of earlier evidence (files 50 to 55). `_capture-log-*.json` holds the load times, request counts and console errors of each capture.

Nothing outside this folder was changed. The live site got GET requests only. Nothing was committed.

---

## 1. The short answer

- **The old designer** is a single 139 KB HTML file with a three.js scene of one invented four-room flat ("דירת דוגמה ברובע שדה דב"). It has no plan, no dimensions and no prices. It links to no project data. Its last step sends the visitor to WhatsApp. Whatever page opens it, it still says "רובע שדה דב".
- **"The other designer that is also with the plan"** is most likely the **Plan Studio** (HAD-543, 18.10.2026, "סטודיו התוכנית · אשירה", "מעצבים לפי התוכנית"). Its commit says it was made "replacing the door designer". It redraws Ashira's four published sales plans of building E. Clicking a room opens its 360. It also has a floor slider, an outside view with the flat lit up, the window's field of view drawn on the plan, a table of what the window sees, the facilities, and WhatsApp plus a video call button. It exists only as local files and a private artifact (https://claude.ai/artifact/363bRm1N5CsXXc1jG4PWZx). It was never released. A second candidate is the July **2D Apartment Studio** (`studio.js`). It drags real-size furniture on a schematic plan and is live today on one page only, https://nad-lan.co.il/projects/aurelia/ (screenshots 20, 21).
- **Links to the old designer:** 6 live surfaces, from 10 code or content places: the feature bar, the Hebrew header menu, the language-home menus, the stage step, the floor-card action and the /tours/ card. Together they reach every Hebrew page, all 1,088 project URLs, 20 stage pages, 4 language homes and /tours/. All 23 rows are in the CSV.
- **Search Console weight of /tour/designer/: none.** 0 clicks and 0 impressions from 10.8 to 9.11.2026 (and since 1.5.2026). URL Inspection says "Excluded by 'noindex' tag", last crawled 3.8.2026. Replacing it carries no search risk. The URL must still answer 200 until the new page owns the intent (no 301, no 404).

---

## 2. Live truth versus the repo (read this before reusing anything)

The repo's working copy is **not** what runs live for the designer chain.

| File | Live (1.72.639, fetched 10.11) | Repo working copy (branch `claude/apartment-experience-b1`, 045d3725) |
|---|---|---|
| `assets/tours/designer-tour.html` | sha256 `0fc3397a…`, 139,264 bytes. This is the v103 contact build of 29.9, identical to `docs/live-sources/tour-designer/designer-tour-1.72.366.html` and to the `live-truth` worktree. It has no `?project=&unit=`, no REST call, and `PAY_DEMO=false`. | sha256 `569c6459…`, 152,285 bytes. This is v102 UnitDesignRequest ("Batch 2, local only", commit 6286d747) plus v103. It reads `?project=&unit=&pn=&ul=`, keeps one design per unit and POSTs `/lead` and then `/rfp`. **Never released.** |
| `assets/project-stage/bridge.js` | 39,328 bytes. `location.href = DESIGNER` with no unit (line 424). | 55,620 bytes. `designerUrl()` adds the unit (lines 594-604). |
| `assets/showroom-engine/studio.js` | 22,273 bytes, no per-unit document. | 29,318 bytes, v102 per-unit document, undo and redo. |
| `assets/showroom-engine/buyflow.js` | 21,115 bytes | 26,398 bytes (v102) |
| `inc/rfp.php` | The live-truth copy has no `nadlan_rfp_clean_design` (no UnitDesignRequest). | Has the design document contract (lines 76-196). |
| `assets/project-stage/world/cockpit.js` | Designer link already removed ("the old designer left on Ben's word, 10.11 night"). | Commit 045d3725 still has it at line 126; the working copy removed it (uncommitted). |

The proof is in `screenshots/12-designer-ctx-390-entered.png`. `/tour/designer/?project=hamedina&unit=C-30-w` opened live, and the brand line reads "דירת דוגמה · רובע שדה דב" for a Kikar Hamedina apartment.

---

## 3. Verdict per component

**Reuse** = take as is or with small changes. **Rebuild** = keep the idea and the data, write new code or design. **Drop** = do not carry forward.

| # | Component | Files | Live? | Verdict | Why |
|---|---|---|---|---|---|
| 1 | Old designer page | `plugins/nadlan-config/assets/tours/designer-tour.html` | yes | **Drop** (keep the URL answering) | An invented flat with no plan, no scale and no prices. Gold on purple with a wooden door is the banned look. The owner called it embarrassing. See section 4. |
| 2 | Tour route `/tour/{slug}/` | `inc/tour-routes.php` | yes | **Reuse** | An allowlist plus a plugin-first file stream with a deploy header. The new engine can be served the same way, or `designer` can stay mapped until the new page owns the intent. |
| 3 | Unit design document `nadlan-unit-design` v1 plus the RFP pipeline | `inc/rfp.php` (lines 76-333), `inc/conversion-cta.php` (`/lead`, lead_key at 348-387) | partly (the RFP exists live without design layers) | **Reuse and ship** | Server-side unit facts, a design frozen into the request, a lead linked only with an HMAC key, one document per `client_ref`, and a printable document at `/nadlan/v1/rfp/<token>`. Extend it with plan geometry, finishes, prices and a spec sheet. |
| 4 | 2D Apartment Studio | `assets/showroom-engine/studio.js` | yes, only on /projects/aurelia/ | **Rebuild UI, reuse logic** | Good logic: a catalogue of 20 real-size items in cm, SI 1918 clearance templates (150 cm wheelchair turn, 80 cm door), per-document undo and redo, a storage key per geometry revision, unreadable drafts set aside, auto-arrange, notes, and attach to RFP. Weak parts: the plan is empty schematic boxes, the icons are emoji and the background is cream. |
| 5 | **Plan Studio (HAD-543)** | `docs/sales/ashira-meeting-2026-10/tour/studio/index.html`, `plan-studio-mockup.html`, `studio-artifact/index.html` | no | **Reuse as the starting point** | It already does "plan to interior" on real plans. Room polygons in cm with ids and sizes, plan to 360 per room, 4 styles, a floor slider, the outside view with the flat marked, the field-of-view wedge, distances to 791 places, facilities. Its drafting-sheet identity passes the owner's design law. |
| 6 | Walkthrough lab (park to lobby to lift to apartment) | `C:\Users\777\nad-lan\walkthrough-3d-lab\` (`walkthrough3d.js` 120 KB, `index.html`, `server.py`) | no (local only, **not in git**) | **Reuse parts** | `mountWalkthrough3D(host, opts)` is a clean mount contract. Worth taking: the dollhouse cutaway, the laser measure in cm with a click-to-click ruler, the floor slider 1-40, sun positions (SunCalc), and the real city from world.json and city.json. The chrome is dark with gold and needs a new look. Put it under git before anything else. |
| 7 | First-person CSS-3D interior | `inc/interior-fp.php` | yes (property pages; its assets print on every project page) | **Drop the renderer, reuse `nadlan_ifp_rooms()`** | CSS planes are not a 3D engine. The room-list builder from listing facts is a useful fallback. |
| 8 | Property plan SVG | `inc/property-showroom.php` `nadlan_pshow_plan_svg()` | yes | **Reuse as a listing fallback** (outside the engine) | An honest schematic for resale listings (screenshots 23, 25). |
| 9 | International planSvg plus its "Design this apartment" button | `inc/global-worlds.php` 1260-1292 | yes | **Drop** (and fix the link) | The button goes to `/studio/`, the advertiser editor behind a login. |
| 10 | 360 viewer | `assets/project-stage/tour.js` (+ `tour.css`) | yes | **Reuse** | three.js sphere with scenes by direction, spot and floor, doors, a lift panel and a style switch. It has `getView()`, `setView()`, `project()` and `pick()` for the shared room, and the `nl:tour` and `nl:view` events. Screenshots 31, 32. |
| 11 | Stage bridge | `assets/project-stage/bridge.js` | yes | **Reuse** | The entry point: `nl:floor`, `nl:facing` and `window.__nlpsPick` already carry the chosen floor, side and unit. Only the designer target changes. |
| 12 | Kikar journey plus apartment cockpit | `assets/project-stage/world/journey.js`, `cockpit.js`, `hamedina/cockpit.json` | yes, behind `?kikar=next` | **Reuse as the host** | A full-screen app for one apartment. Its plan tile, inside-360 with 4 styles, price and cost, and video call tiles are where the new engine's "design" tile belongs. |
| 13 | Blender interior pipeline | `scripts/interior/*.py` (Blender 5.2 installed) | offline | **Reuse** | Plan-accurate apartments (`ashira_apartment.py` models E-4A, E-3B, E-5E and E-5F from the sales plans), 4 styles (`studio_kit.py`), 360 cuts and cards (`cut_tour.py`, `cut_kikar_tour.py`), a living 360 per tower, floor and side, and a window view per floor. Section 6. |
| 14 | Rendered 360 sets | `assets/project-stage/{ashira,rainbow,duo,hamedina}/tour/`, `hamedina/views/` | yes (except Ashira's e3b, e4a, e5e and e5f) | **Reuse** | Ashira 159 files, Rainbow 123, Kikar 83 plus 194 view files, DUO 18. |
| 15 | Meshy runner | `C:\Users\777\Documents\agent-tools\meshy\run.cjs` | offline | **Reuse for furniture GLBs** (costs credits: ask first) | Text to 3D, image to 3D, rig, balance. So far it has made only a rigged walker (a person), in `scripts/interior/_renders/kikar/meshy/`. Not run here. |
| 16 | GLB models | `assets/showroom-engine/models/*.glb` (14), `assets/engine/**`, `assets/projects/**` | yes | **Reuse for the outside view only** | All are building massing models (0.1-1 MB). **The repo has no furniture or interior GLB.** |
| 17 | TogetherRoom | `inc/together.php`, `assets/together/together.js` (+ css) | yes (LiveKit on Ashira, DUO, Rainbow and Kikar since 1.72.463) | **Reuse and extend** | Video, roles, the leader's view at 10 Hz, notes pinned to points, the apartment's file. Missing: shared editing and handing control over. Section 8. |
| 18 | Older co-tour | `inc/cotour.php` | code present | **Drop** | Superseded by TogetherRoom. |
| 19 | Unit identity contract | `C:\Users\777\nad-lan\worktrees\codex-rainbow-unit-lab-2026-09-27\labs\unit-journey\` (`unit.schema.json`, `unit-contract.md`, `designer-context.mjs`) | lab | **Reuse as the spec** | One opaque `selected_id` with project-scoped aliases, azimuth and eye-height rules, and "never guess the nearest unit". |
| 20 | Unit facts in the CMS | post meta `project_3d_units` (via `inc/showroom-engine.php`), `inc/project-stage.php` arrays | yes | **Reuse** | The server's source for floor, rooms, m², direction and status. The RFP already re-reads it server-side. |
| 21 | Feature bar item "studio" | `inc/feature-bar.php` 108-113 | yes | **Rebuild** (point it at the new engine) | The biggest link source. |

---

## 4. The old designer, in detail

### How it works

- **Served by** `inc/tour-routes.php`. The rewrite `^tour/([a-z0-9-]+)/?$` matches the allowlist entry `'designer' => '2026/07/apartment-designer.html'`. The plugin copy `assets/tours/designer-tour.html` is served first, with the response header `X-NL-Tour: plugin-311`. The uploads file is the fallback. `Cache-Control: public, max-age=300`. `<meta name="robots" content="noindex">`.
- **Stack:** one HTML file (live 2,170 lines, repo 2,317 lines) with all CSS and JS inline. **three.js 0.160.0** comes from jsDelivr through an import map (plus `BufferGeometryUtils`, `RoundedBoxGeometry` and `RoomEnvironment`). **GSAP 3.12.5** comes from cdnjs and the Heebo font from Google. The renderer uses ACES tone mapping, PCF soft shadows, a PMREM room environment, and a pixel ratio capped at 1.8 on phones and 2 on desktop. The budget is 140 draw calls.
- **Geometry:** fully procedural, with no assets. One flat of 4 rooms: living, kitchen, bedroom and a sea-view balcony. `GEOM_REV = 'sdedov-sample-2026-07'`. The camera runs on rails between fixed nodes (`NODES`, `LOOKS_AT`), with CatmullRom glides and drag-to-look. Textures are canvas-generated (oak, walnut, stone, terrazzo, deck, plaster). Three light moods: morning, sunset and evening.
- **Catalogue (no prices):** wall colour 5, floor 4, sofa fabric 5, kitchen fronts 4 (18 options), 3 "looks", and 8 low-poly furniture pieces (extra sofa, armchair, side table, single bed, dresser, plant, rug, floor lamp), at most 12 placed. A note can be attached to the walls, floor, sofa, kitchen, doors and windows. The only money on the page was a mock "מקדמת עיצוב · סימולציה ₪2,500". `PAY_DEMO=false` hides it on live.
- **Save:** browser `localStorage` only. Live key `nadlan-apt-designer-v2`, with the older `nadlan-apt-style-v1` migrated. It stores the choices, mood, notes, furniture **and the contact name, phone and email**. The repo's v102 key is `nadlan-apt-designer-v3:<project>:<unit>:<GEOM_REV>`.
- **Lead flow, live:** the steps are design, then summary, then details, then "המשך · שיחה עם נציג". The last step is a `wa.me/972525101555` link with a text summary. The number is hard-coded in the file. **No server call.**
- **Lead flow, repo only (v102):** first `POST /wp-json/nadlan/v1/lead` (`source: apartment-designer`, `goal: design-request`, project and unit, consent), which returns `lead_id` and `lead_key`. Then `POST /wp-json/nadlan/v1/rfp` with `{project, unit, lead_id, lead_key, client_ref, design}`. That creates a private `nadlan_rfp` post named `rfp-<client_ref>` with an `rfp_token`, and writes `rfp_id` on the lead. `GET /nadlan/v1/rfp/<token>` renders the printable request. The design document is `{schema: nadlan-unit-design, v: 1, project, unit_id, geometry_revision, source: designer-3d, layers.space3d {units m, origin centre, rot rad, items}, notes[], choices[], mood}`. The 2D studio writes `layers.plan2d` in cm from the top-left, in degrees. rfp.php says outright that **no transform exists between the two**.

### Weaknesses

Technical:

1. **Not tied to any apartment.** One invented Sde Dov flat for every project. On live, even the unit name in the link is ignored; the v102 fix never shipped.
2. **No plan, no measurement.** The visitor cannot see or change a layout. There are no dimensions, so a "real size" check is impossible.
3. **Two incompatible design formats** (3D in metres from the centre, 2D in cm from the top-left). Neither one is anchored to real plan geometry.
4. **Nothing reaches the server on live.** The design lives in one browser, and personal details sit in `localStorage`.
5. **A monolith.** A 140-150 KB inline file with Hebrew strings hard-coded (the `T` dictionary covers only V2 strings), so the 4 other site languages get a Hebrew-only page. The feature bar sends EN, FR, RU and AR visitors there.
6. **Heavy start.** An entry film behind a gesture, real-time shadows, and `touch-action: none` on the whole body. Under headless software GL the first screen (logo and loading line) was still on show after 7 s (screenshot 01); a real phone GPU is faster, but nothing here measures it.
7. **Accessibility.** Everything happens by raycast clicks on a canvas. Furniture cannot be placed with the keyboard, and `user-select: none` is set on everything.
8. **Two copies drift.** The plugin file and the uploads fallback, plus the live and repo versions, already differ (section 2).

Visual (screenshots 01-04, 10-12, 14, 15):

1. The banned "luxury" look: gold `#d8b46a` on deep purple `#131022`, a wooden door poster ("פתחו את הדלת"), gold ring hotspots.
2. Toy-like low-poly furniture: sphere trees, a black slab for a TV, a flat gradient sunset.
3. On a phone the bottom controls take about a quarter of the screen. The header button says "סיכום והזמנה" (summary and order) when there is no order.
4. The demo ribbon "הדגמה · אין תשלום באתר" and the line "דירת דוגמה · רובע שדה דב" show for every project.

What is worth keeping from it: the idea of light moods, notes on any element, autosave that keeps an unreadable draft aside, and the server contract written for it (#3 in the table).

---

## 5. "The other designer with the plan": the candidates

| Candidate | What it does | Where it renders | Screenshots | Reusable |
|---|---|---|---|---|
| **Plan Studio v1/v2 (HAD-543)**, most likely the one | It is titled "אשירה · מעצבים לפי התוכנית". Pick a type (E-4A, E-3B, E-5E, E-5F penthouse), then click a room on the plan to open that room's 360 in warm, light, stone or as-delivered. Also: floor slider 1-16, building view (outside or inside 360), the field-of-view wedge on the plan, room sizes in cm, a "what the window sees" table with distance and walking minutes (from 791 places), 7 facilities in 360, "לקבלת התוכנית והמחיר בוואטסאפ" and "שיחת וידאו על הדירה". | Not live. Local: `docs/sales/ashira-meeting-2026-10/tour/studio/index.html` (needs the repo next to it; it loads `plugins/nadlan-config/assets/project-stage/ashira/tour/` and `places.json` by relative path). Private artifact https://claude.ai/artifact/363bRm1N5CsXXc1jG4PWZx. Commits 395e4b75, 4eacab0c, 0b6d123a (18.10.2026). | 50, 51, 52, 53 | **High.** The room-polygon format, the plan-to-360 link, the identity (IBM Plex Sans Hebrew and Plex Mono, drafting white, ink navy, blueprint blue, dimension red: not the default look), the window table and the FOV wedge. |
| 2D Apartment Studio v1 (July 2026) | "Design before you buy". Drag 20 real-size items on a scaled schematic plan built from the unit's rooms and m². Accessibility templates, notes, rotate, auto-arrange, undo, then "צירוף התכנון לבקשת הצעה", WhatsApp, video call. | Live only on https://nad-lan.co.il/projects/aurelia/ (the one project in showroom mode out of 1,087). The "עיצוב הדירה בסטודיו" button in the unit panel. | 20, 21, 22 | The logic (#4 in the table). |
| Walkthrough lab | The Kikar Hamedina and Ashira buildings from park to lobby, pool and parking, then the lift to floors 1-40 and the apartment. Walk, dollhouse or guided tour, a design studio (bare, warm, light, stone, furniture, curtains) and a laser measure in cm. | Local only: `python server.py` in `C:\Users\777\nad-lan\walkthrough-3d-lab` (serves the repo's stage data read-only). | 26, 27, 28, 29 | Dollhouse, measure, floor slider, sun (#6). |
| First-person interior from unit data | CSS-3D rooms built from rooms, m², mamad, balcony and direction, with door hotspots. | Property pages ("🚶 סיור פנימי" tab), and the engine's tour tab when a unit has no tour. | (the CSS-3D view rendered blank in headless capture) | The room list only (#7). |
| Property plan view | Schematic plan of the listing ("תוכנית הדירה · קומה 6"). | https://nad-lan.co.il/properties/balfour-batyam-35r-demo/ | 23, 25 | Fallback (#8). |
| TogetherRoom plan mode | "התוכנית והחתכים" plus a mini plan "איפה אתם בדירה" of an example apartment, inside the video room. | Project pages with `?room=<id>` | 55 (call film poster) | The room itself (#17). |
| Kikar cockpit plan tile | A typical floor of tower C floor 30 (derived) with zoom. | https://nad-lan.co.il/projects/hamedina/?kikar=next | 33, 54 | The host (#12). |

---

## 6. Rendering assets we own

**Blender pipeline** (`scripts/interior/`, Blender 5.2 on this machine, Cycles):

- Apartments: `kikar_interior.py` (tower C floor 30 example; shots living, bedroom, balcony, living360, view and living_eve; times day, sunset and evening; styles bare, warm, light and stone), `ashira_interior.py` (the S1 example living room or balcony on floors 10, 25 and 34, in 4 directions), `ashira_apartment.py` (building E types **from the official sales plans**: E-4A floors 5, 10, 15; E-3B, E-5E and E-5F on floor 10), `rainbow_interior.py`, `duo_interior.py`.
- Styles: `studio_kit.py`, with three palettes (warm, light, stone) built from primitives only (no downloaded assets). That is why the furniture looks generic.
- Facilities: `kikar_facility.py`, `ashira_facility.py` (lobby, pool, spa, gym, club, cinema, kids), `rainbow_facility.py`, `duo_facility.py`, `kikar_cafe.py`.
- Worlds (the real city in the window): `kikar_world.py`, `ashira_world.py`, `duo_world.py`, built from the municipal GIS at true heights with the sun at the true hour.
- Batch runners and cutting: `render_kikar_360s.py` (a living 360 per tower, floor and side), `render_kikar_views.py` (96 window views, about 70 s each at 1280 px and 48 samples), `render_ashira.py`, `render_styles.py`, `render_floors.py`. `cut_tour.py` and `cut_kikar_tour.py` produce a 4096 and 2048 equirect, a 1200×675 straight "card" view and a 480 thumb. `make_comparisons.py` and `ashira_sheets.py` produce contact sheets.
- Cost: a 2048-wide living 360 at 64 samples takes about 814 s (A30-270, 10.11). The 4096×2048 Ashira balconies took 642-821 s each. **It can render 360s per room, per style, per floor and per direction. It cannot make a real-time interior**: the output is panoramas, not a walkable model.

**360 engine:** `assets/project-stage/tour.js` (36 KB, three.js `openTour()`), wired by `bridge.js` (`openTourAt(floor, side)`) and by `inc/project-stage.php` (`'tour' => dirs, facing, style`). It has scenes per direction, spot (living or balcony), floor and style, doors between scenes, a lift panel, the building's rooms (`group: fac`), and a handle for the shared room.

**Ashira data:** `assets/project-stage/ashira/tour/` holds 159 files (36 MB). Living on floors 10, 25 and 34 in n, e, s and w (floor 25 in bare, warm, light and stone; floor 10 in bare and warm), balconies 10w, 25w and 34w, and 7 facilities (lobby, pool, spa, gym, club, cinema, kids). `walk.json` (BuildingWalk v96: apartment stops, lift, facility doors), `views.json` (distances and bearings from each window), `facilities.json` (7 sourced facility hotspots on the model), `places.json`, `city.json`, `quarter.json`. The building E types `e3b-*`, `e4a-*` (floors 5, 10, 15, plus the master bedroom), `e5e-*` and `e5f-*` are 11 scenes (33 files). They are **untracked in git and not live** (404 on 10.11), and several are only 10-30 KB, which looks like low quality.

**Kikar data:** `hamedina/tour/` holds 83 files (C30 west living 360 in 4 styles, stills, twist, 6 facilities, `examples.json`). `hamedina/views/` holds 96 window views in 2 sizes. `cockpit.json` holds the built facts, deals, tax, arnona, mortgage defaults and the plan.

**Meshy:** `run.cjs` with `text3d`, `image3d`, `rig`, `get` and `balance`. The key stays in its env file, which was not read. Not run.

**GLB:** see #16 in the table. There are building massing models only, so furniture GLBs must be generated (Meshy) or sourced.

---

## 7. Plan data

See `plans-by-project.md`. In short: real plans exist for **Ashira** (4 sales plans, already redrawn as room polygons with sizes), **Utopia** (7 official sample PDFs, not traced) and **SIX-8** (2 drawings, not traced). Rainbow, DUO, Dimri and Kikar have only demo units and schematic or derived layouts. 1,075 of the 1,087 projects have nothing.

---

## 8. The video call: TogetherRoom

What exists (`inc/together.php`, `assets/together/together.js`, design system v77, 28.9.2026; video live since 1.72.463):

- **Entry:** the project page itself with `?room=<id>`, or `?room=new` to create one. There is no new URL. When a representative is marked available (`nadlan_tr_rep_now`), the hero button "שיחת וידאו עם נציג" opens a chooser between now and booking. `GET /nadlan/v1/room/available` answered `{"now": false}` on 10.11.
- **Transport:** **LiveKit** (`livekit-client@2.22.3` from jsDelivr, loaded only after the join click). The server mints a 2-hour token with `roomJoin`, `canPublish`, `canSubscribe` and `canPublishData`. Data topics: `view` (lossy, the leader's camera about 10 times a second), `mode` and `notes` (reliable). Without a key there is a **REST fallback**: the leader posts `/room/state` (up to about 3 writes a second) and everyone polls every 1.5 s.
- **Who joins:** the representative (needs `edit_posts`), then from a link with a name and role: buyer, partner, friend, interior designer, engineer, lawyer. No sign-up. Colour groups: rep, buyer, family, pro. A room closes after 6 hours without activity. Notes are kept 30 days (`nadlan_room` private posts, a daily cron).
- **Shared state:** `{m: building|plan|inside|view, u: unit, f: floor, v: camera, pt: pointer}`. Only the rep can lead ("עקבו אחריי"). Others can look away and press "חזרה למה ש… מראה".
- **Notes:** anyone can pin a numbered note to a point (stage, 360 or view), marked "בקשה לשינוי בדירה (כפוף לאישור היזם)". The apartment's file is at `?room=<id>&file=1`, and it can be sent on WhatsApp.
- **Not there:** screen share, recording (deliberately not recorded), any co-editing.

What shared control of a 3D design space needs:

1. **A design channel.** A reliable `design` topic with operations (add, move, rotate, remove an item; change a finish), each with its author, the item id and a revision. The server holds the latest revision, and the last writer wins per item. Add the REST fallback the same way, batching drags under the 3-writes-a-second limit.
2. **Handing over control.** Today only `rep` can lead. Add "give control" (the rep hands the pen to the buyer and takes it back), and show whose hand is on the design.
3. **A design mode.** Add `design` to `MODES` in `together.js` and to `nadlan_tr_mode()` in `together.php` (line 215, now `building|plan|inside|view`).
4. **Unit ids.** `nadlan_tr_clean_state()` accepts `u` only as `^\d{1,3}-[a-z]{1,3}$`. Kikar ids (`C-30-w`, `A30-262`) and the lab's opaque ids are dropped. Widen it to the unit identity contract (#19).
5. **Persistence.** Snapshot the shared design into the unit's `nadlan-unit-design` document, so the call ends in a request or spec sheet (the RFP pipeline, #3).
6. **The camera.** The leader's 10 Hz view sync already works. The new engine needs to expose the same `getView()` and `setView()` handle that `tour.js` does.
7. **Phone layout:** the video dock and a design toolbar on one 390 px screen.

---

## 9. Links to the old designer (full list in the CSV)

Live surfaces and their reach (verified by GET on 62 sampled pages plus 10 more):

| Surface | Source | Reach |
|---|---|---|
| Feature bar "מעצב הדירות שלנו" | `inc/feature-bar.php:112` | every project page, 1,088 URLs in all 5 languages |
| Site header menu "סיורים וירטואליים > מעצב הדירות" | `inc/home-v3.php:166` | every Hebrew page with the new header |
| Language-home mega menu "Apartment designer" and its translations | `inc/home-v2.php:323` | /en/, /fr/, /ru/, /ar/ |
| Stage step "מעצבים את הדירה" | `inc/project-stage.php:871` plus `bridge.js:630` | Ashira, Rainbow, DUO and Dimri in 5 languages (20 pages) |
| Floor card "לעצב את הדירה" | `bridge.js:168` and `:611` | the same 20 pages |
| Tours hub card "כניסה למעצב ←" | WordPress page 7263 (database) | /tours/ |

Dormant references (not live): `showroom-engine/engine.js:2790` (unit v2 off), `flagship-surface.php:2014` and the two flagship-v3 JS fallbacks. Already removed: the Kikar cockpit. Not live: the Echo City snapshot (that page answers 404) and the lab adapter.

Related wrong links (not the old designer, same intent): `global-worlds.php:1292` ("Design this apartment") and `site-map.php:232` ("סטודיו לעיצוב הדירה") both send buyers to `/studio/`, the advertiser editor behind a login.

For the replacement: change the 6 sources to the new engine in one release, and keep `/tour/designer/` answering 200 (the route in `tour-routes.php:31`). No redirect. The URL can simply stop being linked, or later serve the new engine itself.

---

## 10. Search Console

- `gsc_api.py query --site sc-domain:nad-lan.co.il --start 2026-08-10 --end 2026-11-09 --dimensions query,page --filter-page contains:/tour/designer`: **0 rows**. The URL-prefix property `https://nad-lan.co.il/` answered 403, because the property is a domain property.
- Widened to 1.5 to 9.11.2026 and to any page containing `/tour/`: **0 rows**.
- `gsc_inspect.py --url https://nad-lan.co.il/tour/designer/`: **NEUTRAL, "Excluded by 'noindex' tag", last crawl 2026-08-03.**
- Conclusion: the page has no search weight. Its value is only internal (the links above) and direct visits.

---

## 11. Other findings on the way (reported only)

1. The live designer names the wrong project for every non-Sde-Dov apartment (screenshot 12), and the live bridge drops the chosen unit. The v102 fix for both sits unreleased in the repo.
2. The designer keeps the visitor's name, phone and email in `localStorage`.
3. The walkthrough lab (`C:\Users\777\nad-lan\walkthrough-3d-lab`) is not under version control. One deleted folder would lose it.
4. Ashira's building-E 360s (`e3b`, `e4a`, `e5e`, `e5f`) and `balcony-34w` are untracked in git.
5. TogetherRoom's unit filter rejects Kikar unit ids (section 8, point 4).
6. Redirect-shaped code seen while reading (finding only): `inc/showroom-engine.php` line 30 sends `/home.html` with a 301, and `inc/site-map.php` line 146 sends `/sitemap/` with a 301.

---

## 12. Method and limits

- **Code:** grep over `plugins/nadlan-config` (205 `inc/` files), the theme folders (`parts/`, `patterns/`, `templates/`, `functions.php`), `scripts/`, `docs/`, the `live-truth` worktree, `C:\Users\777\nad-lan\walkthrough-3d-lab`, the unit-journey lab worktree and `_private-research`. The search terms were: `tour/designer`, `designer-tour`, `nadlan-unit-design`, `UnitDesignRequest`, `rfp`, `LS_KEY`, `designerUrl`, plan, floorplan and תוכנית.
- **Live:** GET only. The pages were fetched with a plain user agent. Live JS files were compared by sha256 with the repo and the live-truth copies. The public REST API was read for all 1,087 projects and 26 listings (`project_mode`, units, drawings, panoramas). The sitemap index has 4,665 URLs.
- **Screenshots:** headless Chrome 156 over CDP, with SwiftShader GL, at 390×844 (2x, mobile, touch) and 1440×900. SwiftShader is slower than a phone's GPU: load times in the logs show software rendering, not field speed. The first two capture batches (designer) carried no analytics. The third batch (Aurelia, the property page, Ashira, Kikar, Rainbow, 11 page loads) ran before analytics blocking was added. Its GA requests show as aborted at page close, but a few page views may have been recorded. The last batch blocked GA, GTM, Hotjar and Clarity.
- **Not tested:** the TogetherRoom live (opening a room is a POST that writes a room), the 2D studio's "attach to request" (it would create a lead), and the v102 send flow (not live).
- **The walkthrough lab** was served locally on port 47951 by its own `server.py` (read-only over the repo), captured, then stopped.
