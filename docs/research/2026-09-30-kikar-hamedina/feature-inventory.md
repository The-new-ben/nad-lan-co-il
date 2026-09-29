# Kikar Hamedina, P0: the inventory of everything already built for the project pages (30.9.2026)

Phase P0 of `docs/loop/KIKAR-HAMEDINA-LOOP.md` (Linear HAD-375). Read-only pass. Nothing was deployed, pushed or written
to the site; no WordPress API was called and no secrets folder was read. This file is the only output.

**Evidence.** Everything below is **code** (read in the repo) or **doc** (read in the loop, research, coordination and
checklist files). Nothing was checked on the live site in this pass.
- **live** = released, as of 1.72.368.
- **branch** = only on the local branch `claude/apartment-experience-b1`, not released. This covers Batch 1 v101 (644d0025),
  v101.2 (65760d31) and Batch 2 v102 (6286d747). The released WhatsApp commits 3b81761d and f1d5454a are live.

**Project codes used in the tables:** R = Rainbow, U = DUO, D = Dimri Yama, A = Ashira, H = H Infinity.

Paths are under `plugins/nadlan-config/` unless they start with `scripts/`, `tools/`, `docs/` or `data/`
(the repo root `C:\Users\777\nad-lan\nad-lan-co-il`).

---

## 0. The ten findings that matter most (details in sections 1 to 3)

1. **Every stage is a full copy of one engine, and none can turn a floor.**
   - Each `assets/project-stage/<dir>/stage.js` is 164-182 KB with the same `createEngine()` (about 1,900 lines), the
     same shaders and the same geometry helpers; only the scene constants differ. Kikar would be the fifth copy.
   - The local batches v101-v102 changed the same 59 lines in each of the four copies (`git diff --stat 65af09be HEAD`).
   - No stage has a per-floor twist. Kikar's 1.25° a floor (about 50° over 40 floors) reaches:
     - the tower geometry and `floorPlan()`;
     - the example-apartment bearings, `nadlan_ps_unit_resolve()` and the slice;
     - the sight lines and the 360 renders.
   - A ring-twist formula already exists in `docs/playbooks/glb-gen-toha2-v2.py` (`ring(..., twist)`, `TWIST`).
2. **The direction model is one point, one sector list and four fixed side bearings per project.**
   - Kikar has three towers, each turning, so it needs bearings per tower and per floor, and sectors per tower.
   - The only precedent: DUO moved its south apartment to the other tower because the north tower's south face looks at
     the south tower (`duo-tel-aviv` 'tour' dirs; `scripts/interior/duo_interior.py`).
3. **Loop question Q1: option (a) is already built, and (b) partly is.**
   - **(a), the free true-height world.** `scripts/project-stage/build_city_*.py` read Tel Aviv's GIS layers
     (GET only): 513 buildings with surveyed heights, 837 lots, 507/508 streets, 503 green areas, 628 trees and
     579 beaches.
     - DUO's `city.json` origin (32.0857, 34.7829) is roughly 650 m west of the square. That distance is our own
       estimate from approximate coordinates; P1/P2 must confirm it.
     - So DUO's 750 m ring likely already covers much of Kikar's surroundings. DUO's `places.json` does name the
       square's school (580 m), community centre (593 m) and shops (647-698 m), at bearings 66-73°.
   - **(b), Google photoreal tiles.** `inc/earth-experience.php` is a working build: Google Photorealistic 3D Tiles
     through CesiumJS, a 'somail' scene next door, the option `nadlan_gmaps_key` and a quota guard of 85 root requests
     a day. But `/earth/` answers 401 (FORGOTTEN row 13).
4. **What a new page leans on is still branch-only.**
   - Not released:
     - the floor card docked under the stage (`cardHost`) and the + / − zoom;
     - the map-first landing with the unit line and "חזרה לבניין" (v101.2);
     - the "מחיר מוערך" labels on the map;
     - the film's play fallback;
     - the designer opened for the unit;
     - the per-unit RFP and `nadlan_ps_unit_resolve()`.
   - **A live defect this creates.** The live ConsultSheet (`inc/cta-sheet.php`) and the source line
     (`inc/wa-source.php` v103.1, both 1.72.366-368) read `window.__nlpsPick`. Only the unreleased bridge.js sets it,
     so on the live site the floor and direction never reach the WhatsApp message.
5. **Rainbow defaults leak into any new project whose config key is missing.**
   - `nadlan_ps_parts()` falls back to Rainbow's:
     - tour direction words ("לכיוון תל ברוך והרצליה");
     - `view_src` ("…הפרויקטים המתוכננים ברובע…");
     - `poster_alt` ("…מגדל ובנייני בוטיק סביב גינה");
     - `src_line` ("…הפרויקטים ברובע…").
   - It hard-codes the 360 floors (25, 10, 36) and the gate file `tour/living-25w-card.jpg`.
   - bridge.js's "view" step auto-picks `'25-' + seaSide`.
6. **The inside of the buildings is uneven across the fleet.**

   | | Apartment 360 | Facility rooms | Styles | Walk |
   |---|---|---|---|---|
   | Rainbow | 24 scenes (floors 10/25/36 × 4 sides × living/balcony) | 3 | floor 25 | yes |
   | DUO | 4 scenes (floor 25, living room) | 3 | none | yes |
   | Dimri, Ashira | none | none | none | none |

   - 28 Rainbow `*-card.jpg` renders are untracked in git and answer 404 live.
   - The owner rules the interiors "far higher quality". Real furniture waits for his OK to download CC0 models.
7. **Prices are shown only when sourced.**
   - ProjectDeals needs at least 2 deals tied to a floor, each with a source.
   - `basket_hint` is only a published average, and it is never multiplied into a price.
   - Kikar's "from 10 million" comes from one marketing site and is unverified, so no price or deal appears until P1
     sources them.
8. **The pipeline has hard-coded project lists and live-page dependencies.**
   - Kikar must be added by hand to:
     - `build_places.py` PROJECTS;
     - `measure_eyes.py` P, which measures the **live** stage;
     - `stage_harvest.py` PAGES;
     - `content_first_check.py` PAGES;
     - `source_audit.py` WATCHLIST;
     - the `$space` table in `nadlan_ps_unit_resolve()`.
   - Two live-site dependencies: `build_places.py` reads `quarter.json` first, and its `token()` reads the Mapbox token
     from the live project page.
   - The skill `project-page-factory` (SITE-LOOP S1) was never written.
9. **The selling path stops at WhatsApp.**
   - No LiveKit key, so the shared room has no video.
   - The basket is Hebrew only.
   - `lead_e2e`: 0 leads in 7 days (28.9). Payments were never proven, and HubSpot is not wired.
   - A lost response still creates a duplicate lead (Codex OFF-3).
   - The designer is a generic sample apartment.
   - The DESIGN-TO-DEAL slice (HAD-373) waits for Codex's agreement.
10. **The SEO scaffolding has exact requirements.**
    - The lead must be the content's first paragraph of 100+ characters (`nadlan_lead_extract()`).
    - The non-affiliation notice needs the article wrapped in `<div class="nadlan-project-article">`.
    - On a stage page, the FAQPage is built only from a visible Hebrew `<h2>שאלות נפוצות…` with h3 + p pairs (2 to 12).
      Language pages need the `_nl_faq_schema` meta.
    - The slug must pass `tools/gsc/url_word_audit.py`:
      - "kikar" is owned by /tel-aviv-plans/kikar-atarim/;
      - CLAUDE.md lists "tel-aviv" among the owned head words;
      - "hamedina" is free.
    - Whether a catalogue post for Kikar already exists is not known from the repo. Check it in P7, read-only.

---

## 1. Every feature on the existing project pages

**How to read the table:**
- **Where** is the file plus the function or JSON key.
- **Who** is which projects have the feature.
- **Data** is the data class:
  - **official**: the city's GIS, a permit, a design plan or a company report;
  - **sourced**: developer or press, named on the page;
  - **example**: "דירה לדוגמה" or "מתקן לדוגמה";
  - **generated**: an illustration drawn or rendered by us.
- **Kikar** is what the new page needs:
  - **reuse**: as it is;
  - **reuse + improve**: with the change named;
  - **new data**: the data named has to be made.

### 1.A The page: order, head and structure

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 1 | Page order (checklist C1-C8) | Phones first: H1 → answer paragraph → CTAs → stage → view + map → facts → tour → deals → article. On desktop, 3 columns in the first fold (text, stage, rail) | `inc/project-stage.php` `nadlan_ps_compose()` (an outer output buffer on the finished HTML, fails open) + the head style `nadlan-ps-css` (grid areas; ≤1099 px one column, ≤600 px stage 60svh) | R U D A | - | reuse; `tools/content_first_check.py` must pass at 412×915 and 1440×900 |
| 2 | Visible H1, Hebrew + English | `<h1 id="nl-project-page-title" class="nlps-h1">` name + `<span lang="en">` name_en | `nadlan_ps_parts()` $hero; config `name`, `name_en`. The machine H1 it replaces: `inc/showroom-engine.php:950`. Pages without a stage: `nadlan_pt_compose()` (ProjectTitle v39/v50) | R U D A; H via `nadlan_pt_compose` | sourced (names chosen from GSC) | new data: the searched names (P3: "מגדלי כיכר המדינה" 260/mo, "kikar hamedina towers" 320/mo …) |
| 3 | Kicker under the H1 | "developer · place" | `nadlan_ps_parts()` `.nlps-kicker`; config `developer`, `place` | R U D A | sourced | new data: who "the developer" is here (the landowners; Electra + Ashtrom execute): a P1 decision, and the same name goes in the `developer_name` meta for the notice |
| 4 | Answer paragraph `.nl-lead` | 4-7 lines: names, developer, place, status, mix, a dated sourced price, what the page does | `inc/legal-notice.php` `nadlan_lead_extract()` (the content's first `<p>` of 100+ characters; bylines and provenance lines parked at the end) + `nadlan_lead_recompose()`. Fallback `nadlan_pt_synth_lead()` makes it from the article's `.bottom-line` (DUO) | all | sourced | new data: the text (checklist C2); no price until sourced |
| 5 | Hero CTAs | "לקבלת תוכניות ומחירים" (WhatsApp with the project's name; per-language templates), "לבחירת קומה" (#nlps-t), "שיחת וידאו עם נציג" (#nlsch), "סרטון הפרויקט · N שניות · ללא קול" | `nadlan_ps_parts()` $cta | R U D A (film R only) | - | reuse |
| 6 | Steps under the stage | "1 בוחרים קומה · 2 הנוף והמפה · 3 נכנסים לדירה · 4 מעצבים את הדירה", each a button | `nadlan_ps_parts()` `.nlps-steps` (step 3 only when `tour/living-25w-card.jpg` exists); bridge.js `[data-nlps-step]` | R U D A (step 3: R U) | - | reuse + improve: the gate file name and the auto-pick `'25-'+seaSide` are hard-coded; make them config |
| 7 | Rail: a professional's square + the empty "רוצה להופיע כאן?" square | An advertisement card (marked "פרסומת"), WhatsApp to the professional; an invitation to /brokers/#join | `nadlan_ps_square()`, `nadlan_ps_slot()`; config `rail` (post ids) | R (Meital 7833); U D A slot only; Hebrew pages only | real directory data | reuse (the empty square); a paid square only when a real professional buys it |
| 8 | Six quick facts | Tiles: value + source line | `nadlan_ps_parts()` `.nlpf`; config `facts` | R U D A; H has a fact table in its article instead (ProjectDossier v74, `scripts/project-stage/hinfinity_content.py`) | sourced / official | new data (P1): place, towers and floors (40/37/40), 453 homes, parking 1,620 (906 + 720 public), facilities, status, with the conflict **2026 (Ashtrom) vs 4.2027 (Wikipedia)** shown |
| 9 | Progress ladder | done / now / next with dates | `nadlan_ps_parts()` `.nlprog`; config `progress`. The older band, `inc/milestones.php` (from the `project_status` meta), is not printed on stage pages | R U D A | sourced | new data: permit 12.2022, construction, completion (the conflict) |
| 10 | Non-affiliation notice | "אתר עצמאי · עמוד זה אינו האתר הרשמי של %s…" opening the article (the owner's order of 29.8), in 5 languages | `inc/legal-notice.php` `nadlan_project_notice_render()`: placed before `<div class="nadlan-project-article`; names the `developer_name` meta | all | - | reuse; wrap the article in `nadlan-project-article`; `developer_name` must be exact |
| 11 | The article | 5,000+ words, written by the owner's ChatGPT | the post content; its CSS in `inc/project-experience.php` (ProjectFrame v63: 12/20 px frame, 1400 max, 780 px column; ProjectDossier v64/65/67/74, gated by class: `project-article`, `nlfs-article`, `<table`, `nlv2-data-grid`) | R U D A; H short (its prompts are ready, HAD-357) | sourced | new data: P6 prompt, modelled on `docs/research/2026-09-28-h-infinity/prompt-he.md` / `plan-he.md` |
| 12 | FAQ + exactly one FAQPage | a visible accordion; one JSON-LD | `nadlan_ps_compose()`: from the first `<h2>שאלות נפוצות…</h2>` with h3 + p pairs (2 to 12), only if no FAQPage is already there. `inc/schema.php` uses `project_faq_json` only in showroom mode. `inc/schema-meta.php` prints `_nl_faq_schema` (language pages, `docs/playbooks/project-factory.md` §2) | all | sourced | reuse; the article must carry that Hebrew h2 + h3/p; EN/FR/RU/AR need `_nl_faq_schema` |
| 13 | Breadcrumbs + one BreadcrumbList | בית › פרויקטים › name, clickable, 44 px reach | `inc/project-topbar.php` (visible, the_content 32), `inc/breadcrumbs.php` (the single BreadcrumbList; Yoast's piece dropped) | all | - | reuse |
| 14 | Language pills at the top | links to -en/-fr/-ru/-ar | `inc/project-topbar.php` | R U D A (H has no siblings) | - | reuse; needs the siblings |
| 15 | Title + meta description | a ≤66-character title and a ≤160-character description from the page's own sourced facts | Yoast fields written by `scripts/seo/project_meta.py` (guarded, before/after in `docs/qa/seo-meta-2026-09-28`). Fallbacks: `inc/seo-gaps.php` (90), `nadlan_pjx_meta_desc()` (93), `inc/bulk-project-seo.php` (95) | R U D A H | sourced | new data: add Kikar to `META` in project_meta.py (P3) |
| 16 | Structured data | ApartmentComplex (geo, address, amenities), VideoObject, FAQPage, BreadcrumbList | `inc/schema.php`; film `nadlan-ps-film` in project-stage.php | all; VideoObject R | from meta | reuse; the meta must match the visible text |
| 17 | hreflang + x-default | a two-way cluster over `<slug>-en/-fr/-ru/-ar` | `inc/project-lang.php` (slug-suffix families; canonicals untouched) | R U D A | - | reuse |
| 18 | One map per page | the surroundings band's static map hidden on stage pages | the CSS rule `.nlcp-surr__map{display:none}` in `nadlan-ps-css` | R U D A | - | reuse |
| 19 | First picture (LCP) | the poster painted with the HTML, then the live 3D | `nadlan_ps_poster_set()` (poster.jpg 1432w + poster-716.jpg 716w, srcset, `fetchpriority=high`, head preload); `modulepreload` of three@0.170.0 and stage.js; the layout CSS at the end of the head. `scripts/project-stage/firstpic.py` measures it on a mid Android | R U D A | generated | new data: kikar/poster.jpg + poster-716.jpg from the stage's hero camera (Rainbow 146 KB / DUO 309 KB) |
| 20 | The edit-screen checklist box | the 7 content-first rules on the WordPress project edit screen | `add_meta_box('nadlan-ps-checklist')` in project-stage.php | all | - | reuse |

### 1.B The 3D stage

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 21 | The per-project stage | a three.js white model at golden hour; loaded lazily after the poster | `assets/project-stage/<dir>/stage.js` `mount<Name>Stage()` + stage.css (351 lines each); config `dir`, `mount`. Dimri/Ashira are the most general: several `TOWERS` with per-floor level tables `levels()`, `buildTower`/`buildBlock`, `SCENE` {hero, intro, fac, build}, `anchorOf()` | R U D A (H none, HAD-356) | official lot + generated facades | new data + new engine work: copy `dimri/stage.js`; three towers on the real lot with the **1.25°/floor turn**, heights 160/157 m; the square's ring, the park and the lake. Consider a shared engine before a fifth copy |
| 22 | Official lot and buildings | the lot's line, the buildings' footprints and floors from the records; a source line under the stage | stage constants (`LOT_OUTLINE`, `*_POLY`, `TOWERS`); `docs/research/2026-09-28-stages/stage-geometry.md` (evidence classes OFFICIAL/DRAWING/DEVELOPER/ILLUSTRATION; frame §0.2: origin = lot centroid, x = grid east, z = grid south, the grid angle); config `src_line` | R U D A | official + drawing | new data: the parcel (GIS 837 / govmap), the towers' footprints and levels, the plan's heights (P1/P5) |
| 23 | The real city around | today's buildings at their surveyed heights, the far city to the sea, the plan's lots, streets, green areas, trees, the coast | `city.json` (`b`, `f`, `lots`, `g`, `s`, `t`, `labels`, `coast`) from `scripts/project-stage/build_city_rainbow.py` / `build_city_duo.py` / `build_city_sdedov.py` (TLV ArcGIS IView2, GET only) | R U D A | official | reuse the builder: clone `build_city_duo.py` with Kikar's origin, leaving its own lot to the stage |
| 24 | Weak-device fallback | the poster stays on a software renderer; `?nlps3d` forces the scene (QA) | stage.js `probeWebGL()`, `force3D` | all | - | reuse |
| 25 | Light presets and the sun | "שקיעה / צהריים", the sun and the exposure | stage.js `PRESETS` | R U D A | generated | reuse + improve: the sunset sun sits at 208°/16°, wrong for late September (FORGOTTEN row 3) |
| 26 | Intro, auto-orbit, glide | a short intro, a slow orbit, the camera glides to a picked floor; honours reduced motion | stage.js `DEFAULTS` (intro, autoOrbit, glide, adaptive pixel ratio) | all | - | reuse; the opening cinematic flight is designed and parked (R6 part 2) |
| 27 | Wheel and zoom | the wheel zooms only after a click on the stage; + / − buttons and a hint | stage.js `wheel:'engaged'` (live); the +/− and hint are v101 (**branch**) | all | - | reuse + improve: Codex flagged the 4 s wheel renewal (rainbow stage.js:845-850) as a scroll-trap suspect |
| 28 | Floor pick → floor card | the floor, a sourced line, the direction, actions ("להיכנס לדירה · 360°", "הנוף והמפה", "לעצב את הדירה"), "לקבלת תוכניות ומחירים" | stage.js label (`rbs-label`); bridge.js `floorNote()` (a sold deal on that floor from `deals[].note`, else `lowNote`/`highNote`); StageCard v94 (**live 1.72.355**: dock, fold, drag); card docked under the stage in `#nlps-pick` (v101, **branch**) | R U D A (floor notes: R U) | sourced / example | reuse; floor notes from Kikar's sourced deals |
| 29 | Example apartments by side | one "דירה לדוגמה" per side of a floor; a tap snaps to its arc; the sea side answers first | config `units` [[side, bearing]] ×4; bridge.js `units {sides, half, label}`, `autoFacing: seaSide` | R U D A | example | new data + new engine work: with a turning floor, bearing = base(tower) + 1.25° × (floor − 1). Config, bridge `facingWords`, slice, `unit_resolve` and the renders all need a per-floor bearing |
| 30 | Unit id + deep link | `?unit=25-w` or `?unit=N-25-w` opens that apartment; the address keeps it | bridge.js `keepUnit()`, `stage.selectUnit()`; server `nadlan_ps_unit_resolve()` with a hard-coded floors table per dir (**branch**, v102) | R U D A | example | reuse + improve: add `'kikar' => [A, B, C]` with the homes floors |
| 31 | Several towers | pick a tower, then a floor; the card names the tower | `TOWERS` / `TOWER_BY` in duo/dimri/ashira stage.js; `.dus-label-kick`; `selectFloor(n, tower)` | U (N/S), D (A/C), A (S1/N2) | official | reuse the pattern for A/B/C |
| 32 | Floor slice "חתך הקומה" | the floor as a plan: glass line, balconies, an illustrative core, the example apartments by bearing; tap one to pick it | `assets/project-stage/slice.js` `openSlice()` + slice.css; `stage.floorPlan(n, tower)`; config `slice_note` (R only) | R U D A | generated + example | reuse + improve: `floorPlan()` must turn with the floor; a slice note only if a source gives homes per floor |
| 33 | Facility pins and cards | pins on the model; a card with sourced lines, an "illustration" note, a WhatsApp question naming the facility, "כניסה ב־360°" when there is a room | `<dir>/facilities.json` (`id`, `name`, `pin`, `icon`, `anchors`, `ask`, `lines`, `note`, `tour`); stage.js `anchorOf()` | R 5, U 6, D 8, A 7 | sourced + generated places | new data: pool, gym, spa, treatment rooms, halls, the public park and lake, the retail ring, parking; each line sourced |
| 34 | "המתקנים בפרויקט N" pill on the model | one tap shows the facilities alone | `.nlps-facbtn` in `nadlan_ps_parts()` (StageFacilities v95), in step with the legend chip (`data-nlps-phase`) | R U D A | - | reuse |
| 35 | The quarter's legend | chips: מתקנים / קיים היום N בניינים / בבנייה / בשיווק / בשלב ההיתר; a chip shows its group alone | `nadlan_ps_parts()` $legend (counts from quarter.json + city.json); `stage.focusPhase()` | R U D A | from our pages + GIS | reuse |
| 36 | Quarter pins | our nearby project pages as pale volumes by their floors, and named places; a card (developer, status, floors, units, distance, source; never another project's prices) + "מה רואים מ-X לכיוונו" | `<dir>/quarter.json` (`origin`, `tower`, `projects`, `places`); stage.js qpins/qcard, `lookToward()`; `scripts/project-stage/pincheck.py` (no overlaps) | R 8, U 1, D 8, A 8 | our pages + GIS | new data: DUO, H Infinity and our other pages near the square, the square's own places |
| 37 | Stage caption | "הדמיה להמחשה בלבד…; חלוקת הקומה לדירות היא לדוגמה…" | stage.js `TEXT.caption`; bridge.js text override | all | - | reuse |
| 38 | Analytics | GA events: stage_floor, stage_facing, whatsapp_click, floor_action, stage_step, quarter_legend, quarter_pin, deal_floor_click, floor_slice, tour_open, tour_room, tour_direction, facility_tour, map_back, pro_click | bridge.js `ga()` → `window.nadlanGA` (conversion-cta.php) | all | - | reuse |
| 39 | The stage's public API | `ready`, `selectFloor`, `selectUnit`, `getSelection`, `floorHeight`, `floorPlan`, `focusPhase`, `lookToward`, `getView`/`setView`/`home`/`pickPoint`/`project` (for the shared room) | the `handle` at the end of `mount*Stage()` (duo/stage.js ~480-536) | R U D A | - | reuse: keep the same API, so bridge.js, slice.js, together.js and the probes work unchanged |

### 1.C The view from the floor and the map

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 40 | The view from the floor | satellite with 3D buildings from the floor's eye height, turned to the picked direction; drag to look; "מבט משוער מגובה של כ-N מ׳, לפי מפה" | bridge.js `showView()`, `winCam()` (Mapbox GL v3.7 free camera); the eye height from `stage.floorHeight()` (the +1.6 m counted twice was fixed in 1.72.286) | R U D A | generated from the map | reuse; eye heights from Kikar's level tables |
| 41 | Labels in the view + "מה יש לכיוון הזה" | named places and our projects at their positions (±55°), nearest first, with walking minutes and status | bridge.js `addViewPins()`, `showNear()` (quarter.json) + `arealife.js groupsEl()` | R U D A | sourced (TLV, OSM, our pages) | reuse |
| 42 | Sight lines per floor band | only what a window can see is named (street / roof / hidden per band) | `places.json` `bands`, `eye`, per-place `sight`; eyes from `scripts/project-stage/measure_eyes.py` (the live stage's `floorHeight()`); bands: R 10/25/36 (formula), U 10/25/45, D 10/25/36, A 10/22/32 | R U D A | computed over GIS 513 | new data: bands **per tower** (three towers, two heights); `build_places.py` computes from ONE tower point today |
| 43 | The beam (cone) on the area map | the terracotta wedge turns to the picked direction | bridge.js `showBeam()` (the frozen engine's wedge drawn again from outside; none when engine.js is on the page) | R U D A | - | reuse (frozen look) |
| 44 | The area map `#nlpjx-map` | one Mapbox map, moved next to the view; layers: ₪ prices, education, parks, transit, shops, health, food, ◆ future plans (purple), 3D, satellite; 5 languages | `inc/project-experience.php` `nadlan_pjx_bottom()` (`NLPJX_POIS`, `NLPJX_PLANS`); moved up by `nadlan_ps_compose()` | all (H too) | OSM + our catalogue | reuse |
| 45 | AreaMap place registry (AreaLife v97/v100) | 7 groups of daily life, walking minutes, 5/10/15-minute walking areas, a list and a summary; names in `<bdi>` | `assets/arealife/areamap.js` (data-places), `assets/project-stage/arealife.js`; `<dir>/places.json` (`groups`, `places`, `landmarks`, `iso`) from `scripts/project-stage/build_places.py` | R 860, U 1,391, D 835, A 791 places; H falls back to OSM in a straight line | findplace.co.il (TLV open data + OSM), OSM, Mapbox walking | new data: `places.json` for Kikar. findplace covers north of lat 32.0845 (`build_places.py` docstring), which should include the square (unverified: check its south edge) |
| 46 | Map landing, unit line, "חזרה לבניין" | after "הנוף והמפה" the whole cone is in view, clear of the bar; the map comes before the view in one column | bridge.js `toBelow()`, `.nlps-mapsum`, `order:-1` (v101 / v101.2, **branch**) | - | - | reuse after release |
| 47 | "מחיר מוערך" on estimated prices | every map price chip says it is an estimate, per m², not binding | `project-experience.php` `NLPJX_PRICE` (v101, **branch**) | - | - | reuse after release |
| 48 | Price band, comparison table, area price line | "~N ₪/מ״ר, אומדן לא מחייב"; nearby projects' ₪/m²; the city's median from recorded deals | `nadlan_pjx_price_band()` (the `project_3d_avg_price_per_sqm` meta, REST `/nadlan/v1/comps`); `inc/area-price-line.php` (`wp_nadlan_deals`, at least 5 deals) | where meta exists | catalogue estimate / Tax Authority | reuse; the ppsqm meta only with a sourced number |

### 1.D Inside the building

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 49 | The example apartment in 360 | a full-screen viewer: the living room (and the balcony) per direction and floor; drag, pinch, keys, Esc; the "דירה לדוגמה" chip | `assets/project-stage/tour.js` `openTour()` + tour.css; the `.nlat` card in `nadlan_ps_parts()`; files `tour/living-<floor><dir>.jpg` / `-2k` / `-card`, `balcony-*`; config `tour` (dirs words, facing, height, view_src, card_alt, card_title). Renders: `scripts/interior/rainbow_interior.py`, `render_floors.py`, `duo_world.py`, `duo_interior.py`, `render_duo.py`, `cut_tour.py` (Blender 5.2 Cycles) | R: 3 floors × 4 dirs × living + balcony = 24; U: floor 25 × 4; D A: none | generated + example | new data: `kikar_world.py` / `kikar_interior.py` from duo_*; the view at the real eye height and the turned facing. Keep the file names (the PHP hard-codes floors 25/10/36 and the gate file), and give `tour` config words, or Rainbow's words print |
| 50 | Design styles in the 360 | "כמו במסירה · עץ חם · בהיר · אבן" inside the room | `scripts/interior/render_styles.py` + `studio_kit.py`; files `living-<f><d>-<style>*.jpg`; the styles panel in tour.js | R only (floor 25 living, 4 dirs) | generated | new data: renders at higher quality |
| 51 | Facility 360 rooms | "כניסה לבריכה" etc. from the facility card | `tour/fac-*.jpg`; facilities.json `tour` {src, small, label, title, place, stopSub, doors}; `nl:facility-tour` → tour.js. On D A no 360 button is printed (code: only with `tour.src`) | R (roof pool, club, lobby), U (pool, lobby, wellness) | generated | new data: the pool, spa and gym, the lobby, the park with the lake at street level |
| 52 | The building walk | one viewer: the apartment's door → "לאן?" at the lift → the lobby, club, pool → back | facilities.json `walk` {order, aptDoor per side, aptStops, labels, liftTitle, liftNote, routeNote}; bridge.js `walkOpts()` / `openWalk()`; doors measured in the render scripts (RBF_LOCATE, DUO_LOCATE) | R U | generated ("every connection is illustrative") | new data: lift stops per tower (like DUO's `aptStops`), doors measured in the new renders |
| 53 | Names in the 360 windows | the places a window really sees, named in the panorama | `arealife.js looksFor()` (from `sight` per band) | R U | computed | reuse; needs Kikar's bands |

### 1.E Selling and contact

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 54 | WhatsApp bar "ייעוץ חינם" | a wide bar with the NadLan mark and WhatsApp on every page, never a circle; review voice on project pages | `inc/conversion-cta.php` (WhatsAppBarEverywhere v103/v103.1, **live 1.72.366-368**); `tools/wa_bar_audit.py` | all | - | reuse |
| 55 | ConsultSheet | an editable message with chips (what, when, a note); per-unit drafts; opens WhatsApp, stores nothing | `inc/cta-sheet.php` (**live**). It reads `window.__nlpsPick`, set only by the **branch** bridge.js | all | - | reuse; release bridge v101 so the floor and direction reach it |
| 56 | The source line in every WhatsApp message | "מקור: <H1> · פרויקט · קומה N" + the path, only when it is short and Latin (≤45 ASCII characters) | `inc/wa-source.php` (v103.1, live) | all | - | reuse; a short Latin slug keeps the link in the message |
| 57 | Floor / unit WhatsApp | "…תוכניות ומחירים לדירה בקומה N ב<שם>, לכיוון X", in the page's language | bridge.js `waUrl()`; i18n-dom.js `L.wa()` | R U D A | example | reuse |
| 58 | Video call with a representative | the booking band `#nlsch`, kind "video" on review-mode project pages | `inc/scheduler.php` (VideoCall v73); the hero button when `nadlan_sched_on()` and no `nadlan_sched_off` meta | all | - | reuse |
| 59 | The shared viewing room | `?room=new`: a representative leads; buyer, family and professionals join from a link; the same view of the stage, the 360 and the view; pinned notes; the file to WhatsApp | `inc/together.php` (REST `/room`, `/room/token`, `/room/state`, `/room/notes`, `/room/file`; post type `nadlan_room`; 30-day retention; LiveKit options `nadlan_tr_lk_*`) + `assets/together/together.js` (LiveKit, else REST polling every 1.5 s) | any slug in `nadlan_ps_config()` | example | reuse: works once Kikar is in the config. No video until the LiveKit key exists (owner) |
| 60 | The basket (BasketOne v86) | the apartment + style + a team of **real** professionals + the full price with purchase tax (single / additional / foreign resident) + a lawyer's fee → WhatsApp or the shared room; "nothing is sold here" | `inc/basket.php` (REST `/nadlan/v1/basket/pros`, `nadlan_bk_team()`), `assets/basket/basket.js` (localStorage `nl-basket:<slug>`); config `basket_hint` | R U D A on Hebrew pages; hint: R U D | sourced hint | reuse; `basket_hint` only after a price is sourced |
| 61 | The apartment designer `/tour/designer/` | a 3D designer of a **sample** apartment (`GEOM_REV sdedov-sample-2026-07`), furniture, notes, a contact step (the demo card form is off) | `assets/tours/designer-tour.html` served by `inc/tour-routes.php` (the plugin copy first); live 1.72.366: `PAY_DEMO=false`. The floor card's "לעצב את הדירה": live = the bare URL (the unit is lost); **branch** v102 = `?project=&unit=&pn=&ul=` + one design per unit | all stage pages | example | reuse; release Batch 2 first, or the Kikar unit is lost in the designer |
| 62 | The request document (RFP) | a printable request with the unit, the choices, the notes, suggested real professionals | `inc/rfp.php` (POST `/nadlan/v1/rfp`, GET `/rfp/<token>`). **Branch**: plan2d/space3d layers, 80 notes, `client_ref` idempotency, `lead_key`, 422 unit_unknown | engine + designer | example | reuse after Batch 2 |
| 63 | 2D studio, "בנו לי הצעה", compare, favourites, co-tour | per-unit furniture planning with SI 1918 clearances; the Tesla-style offer flow | `assets/showroom-engine/studio.js`, `buyflow.js`, `engine.js` (**frozen**), `inc/cotour.php` | showroom mode only (Aurelia) | example | not on stage pages; do not route Kikar through engine.js |
| 64 | The lead endpoint | forms post here; test mode | `/nadlan/v1/lead` in conversion-cta.php; `inc/lead-e2e.php` | all | - | reuse; 0 leads in 7 days (28.9) |

### 1.F Data sections

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 65 | ProjectDeals | "דירות שנמכרו ב… לפי קומה": floor, apartment, price, ₪/m² (calculated, said so), date, source; "לקומה במגדל" opens that floor; a summary line; no buyer named | `nadlan_ps_deals()`; config `deals` (floor, n, bld, apt, price, psqm, date, src, url, via, note), `deals_intro`, `deals_sum`; printed only with 2+ rows | R 7, U 3 (D A none) | sourced (Tax Authority via the press, company reports) | new data: Kikar's floor-tied deals (Madlan's Tax Authority rows, Globes, the developers' reports) |
| 66 | Facility chips in the hero | Booking-style chips → /premium/?fac= | `inc/facility-chips.php` (the `project_facilities` meta, else the premium catalogue row) | where data exists | sourced | new data: the `project_facilities` meta |
| 67 | Money, advisors, designers, "כל מה שסביב הפרויקט" | a monthly estimate from ₪/m²; paid advisors; interior designers; links to the developer, professionals, calculators, the buying guide and the glossary | `nadlan_pjx_bottom()` | all | estimate | reuse + improve: the empty heading "מימון, ייעוץ ועיצוב" when nothing fills it (FORGOTTEN row 40) |

### 1.G The film

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 68 | Project film + player | the hero's "סרטון הפרויקט · 49 שניות · ללא קול" opens a dialog (wide on desktop, upright on phones); a VideoObject; a play fallback and a retry on error (v101, **branch**) | config `film` (wide, tall, posters, secs, date, desc, audio, voice); the footer dialog `#nlfilm`; `nadlan_ps_film_media()` (branch: narrated cut behind `nadlan_film_voice_on`) | R live (silent); U data ready (`scripts/project-video/data/build_duo.py`), not rendered | every line sourced | new data, after the stage is live. The pipeline: `scripts/project-video/` (capture.py stills of the live stage → `data/<slug>.json` → composer.html → render.py → upload_media.py). Hebrew voice: Chatterbox, not on the site yet |

### 1.H Languages

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 69 | Language sibling pages | `/projects/<slug>-en/-fr/-ru/-ar/`, separate posts; the whole page outside the article in its language | `inc/project-lang.php` (context, hreflang, chrome); `inc/lang-pages.php` (a server pass with `i18n/lang-pages.json`); `tools/lang_pages_check.py` | R U D A (56 fleet pages); H none (404) | translated | new data: Hebrew + English first, then fr/ru/ar (Arabic titles in English, the owner's ruling of 28.9) |
| 70 | The stage in the buyer's language | the stage, 360, slice and cards translated in the browser; the stage's server parts translated on the server | `nadlan_ps_current()` maps `<slug>-xx` to the base config (drops film, deals, basket_hint, rail); `i18n/stage-dict.json` (exact 346, patterns 184, names 42) + `assets/project-stage/i18n-dom.js`; `scripts/i18n/stage_harvest.py` (PAGES hard-coded) + `build_stage_dict.py` | R U D A | translated | new data: Kikar's strings (facility names, sectors, tour words, place names); add Kikar to stage_harvest PAGES; brands stay Latin |
| 71 | Place names by language | a place shows on a language page only with a name in that language (or English) | `places.json` `names{en,ru,ar}`; `arealife.js nameOf()` | R U D A | OSM / findplace | reuse |

### 1.I Honesty and legal

| # | Feature | What the visitor sees / does | Where | Who | Data | Kikar |
|---|---|---|---|---|---|---|
| 72 | "דירה לדוגמה" labelling | on the card, the view's title, the map's unit line, the 360 chip, the slice; "מתקן לדוגמה"; the owner's ruling (a) of 25.9 | bridge.js `units.label`, `setTitle()`; tour.js; slice.js; `.nlds-sample` | R U D A | example | reuse |
| 73 | Illustration captions | "הדמיה להמחשה בלבד…" on the stage, the view, the 360, the film; the balcony note (the plan: tower balconies ≤2 m) | stage.js `TEXT.caption`; bridge.js; project-stage.php `$balnote`; the film bar | all | - | reuse |
| 74 | The blacklist and the language DNA | zero waiting phrases ("בהמתנה לחומרי היזם", "0 חדרים", "כיוון בבדיקה"…), no tech talk | `tools/source_audit.py` BLACKLIST; the skill `language-dna` | all | - | reuse |

### 1.J Quality gates and tools

| # | Feature | What it checks | Where | Kikar |
|---|---|---|---|---|
| 75 | content_first_check | C3/C4 rendered at 412×915 (mobile Googlebot) and 1440×900 | `tools/content_first_check.py` (PAGES hard-coded) | add the Kikar page |
| 76 | Public-source audit | raw HTML snapshots + a diff; H1 count, notice position, blacklist, bytes and words | `tools/source_audit.py` (WATCHLIST hard-coded; `docs/source-snapshots/registry.json`) | add Kikar + its siblings; a baseline before the first release |
| 77 | Touch targets 44 px | every control ≥44 px, no overlaps | stage.css, nlds.css, project-topbar.php, facility-chips.php … (TouchTargets v62/v66). The sweep tool (`sweep.py`) is **not in the repo** (a session scratchpad) | reuse; put the sweep into `scripts/project-stage/` |
| 78 | Local harness + shots | the page top composed locally with the real bridge.js; taps floors, sides, facilities; screenshots, frame rate, console | `scripts/project-stage/duo_harness.html`, `dimri_harness.html`, `ashira_harness.html`, `sdedov_serve.py`, `duo_shots.py`, `sdedov_shots.py`; `pagejourney.py`, `firstpic.py`, `pincheck.py`; branch: `preview_v101.py`, `serve_journey.py`, `test_journey.py`, `probe_*.py` | clone as `kikar_harness.html` / `kikar_shots.py` |
| 79 | The release runner | health; a token-gated temporary REST bridge; a drift check vs live; `php -l`; `.bakNNN` backups; MD5-verified swaps; page checks (needs / nevers); automatic rollback; deploy-result + speed JSON | `scripts/project-stage/deployNNN.py` (latest `deploy368.py`; the stage-adding model `deploy333.py` NEWFILES/FILES) | a new runner with `assets/project-stage/kikar/*` |

### 1.K Around the page

| # | Feature | Where | Kikar |
|---|---|---|---|
| 80 | Quarter tours `/tour/sde-dov/`, `/tour/somail/` (three.js, time machine 2026/2035, narration) | `assets/tours/*.html` (plugin first, `inc/tour-routes.php`); the tour band via `inc/sdedov-teaser.php` slugs; `inc/feature-bar.php` (the "somail family") | optional: a Kikar pin in the Somail tour |
| 81 | Earth experience (Google Photorealistic 3D Tiles + CesiumJS, clickable surroundings) | `inc/earth-experience.php` (scenes sde-dov, somail; key option `nadlan_gmaps_key`; quota guard 85/day); /earth/ answers 401 | relevant to the loop's Q1(b): fix the key before any spend |
| 82 | Home "סיור וירטואלי" on project cards; the home map's 3D pills | `inc/home-v3.php:339` (any slug in `nadlan_ps_config()`); `inc/drone-map.php` (3D pills, "{n} פרויקטים בתלת־ממד") | automatic via the config; check how drone-map flags a 3D project |
| 83 | The Einstein "Spatial Decision Room" (dormant): a 9-slot contract page, a shareable deep link, evidence states, a verified-unit contract | `assets/flagship-v3/`, `inc/flagship-surface.php`; `docs/research/2026-09-24-rainbow-run/unit-layer-and-recipes.md` §4 | ideas to reuse: evidence states and "no cone without a sourced bearing" |

---

## 2. Forgotten or partial: what exists on one project and not the others, and the open defects

### 2.1 On one project, not the others

| What | Has it | Missing on | Note for Kikar |
|---|---|---|---|
| Apartment 360, three floors, living + balcony | R | U (floor 25 living only), D, A | plan three bands per tower from the start |
| Design styles in the 360 | R (floor 25 living) | U D A | FORGOTTEN row 4: "DUO: no balcony 360 and no design styles" |
| Facility 360 rooms + the building walk | R U | D A (no `tour`, no `walk` in facilities.json) | - |
| ProjectDeals + floor notes on the card | R U | D A | Kikar needs sourced deals first |
| `basket_hint` | R U D | A | - |
| `slice_note`, `lowNote` / `highNote` | R | U D A | only with a source |
| The film | R (silent) | U (data ready, never rendered: FORGOTTEN row 23), D A H | - |
| A professional's square in the rail | R (Meital) | U D A (slot only) | - |
| The 3D stage | R U D A | H (HAD-356; its 187 m height has no source) | - |
| Language pages | R U D A | H (404; HAD-357 article in 5 languages pending) | - |
| Place registry (walking minutes, isochrones) | R U D A | H (OSM straight-line fallback) | - |

### 2.2 Open defects and gaps that would hurt a new flagship page

**From `docs/loop/FORGOTTEN-2026-09-28.md`:**
1. **Row 1 (HAD-346, HAD-221): the designer loses the chosen apartment.**
   - Codex's UnitCut section cut and designer adapter are not integrated.
   - Batch 2 fixes the unit link, but only on the branch.
2. **Row 2 (HAD-329): the RFP.**
   - The studio choices never reach `/nadlan/v1/rfp`.
   - `sanitize_key()` strips ':' from unit ids.
   - Fixed on the branch, not live.
3. **Row 3: stage accuracy.**
   - The sunset sun sits at 208°/16°, wrong for late September.
   - DUO's lobby glass is drawn at 6 m; the developer says about 7 m.
   - A lounger stands inside DUO's toddler pool.
   - Rainbow's balconies are drawn as waves 0.7-3.6 m deep; the design plan allows ≤2 m (HAD-295).
4. **Row 4:** Dimri and Ashira are below Rainbow inside the building. The "inert 360 buttons" claim is not supported by the
   code: no button is printed without `tour.src`. Unverified live.
5. **Row 6 (HAD-361): the language pages are not finished.**
   - They still use the old theme header, a sideways strip on phones.
   - The browser dictionary is 17 KB gzip; trim it.
   - The film, the steps, the deals table and the basket are left out.
   - The shared room was never tested there.
   - /ar/'s footer touches the edge at 390 px.
6. **Row 9: what is left of Rainbow.**
   - R6 part 2 is parked: the opening flight, the sun path with soft shadows, haze and the tower's detail.
   - Existing buildings are not clickable.
   - R8: the Tax Authority's full deals list, a price-range chip, the deals table in 5 languages.
7. **Row 10 (HAD-186): Hauzd's gaps, not built anywhere.**
   - a sorted table of all the units, and filters that mark units on the building;
   - a plan and keyplan per type;
   - similar units and favourites;
   - a developer dashboard;
   - live price and status.
8. **Row 13: SEO and copy.**
   - The /earth/ layer returns 401.
   - Template titles run over 60 characters.
   - The surroundings text has "תכנית ל'", "find-place" and bare permit numbers.
9. **Row 14 (HAD-220): leads.** Site leads never reach HubSpot. Live health shows 0 leads in 7 days.
10. **Row 16: repo hygiene.** 28 Rainbow `*-card.jpg` renders are untracked (checked in this pass: 28 files in
    `assets/project-stage/rainbow/tour/`), and they answer 404 live.
11. **Rows 20, 21, 23, 27: owner-blocked items.**
    - No LiveKit key: the shared room has no video.
    - The narrated films are not on the site.
    - The DUO film was never rendered.
    - The interior quality: the real-furniture download waits for his OK.
12. **Row 25: commercial spaces and continuous walking.**
    - Commercial spaces are cards only: no 360 and no data per shop.
    - "Walking continuously inside the building" is still panorama jumps (BuildingWalk).
13. **Row 26 (HAD-358): the full buying process.**
    - Designed in DS v93, not built: the reservation request, a file number, a personal apartment-file page and a requests
      screen for the team.
    - Payments were never proven (row 33).
14. **Row 30:** the `project-page-factory` skill (S1) was never created.
15. **Row 40:** the empty heading "מימון, ייעוץ ועיצוב" on pages where nothing fills it.

**From Codex (`docs/coordination/claude-codex.md`):**
1. **Lost-response idempotency.** With lead test mode off, a retried identical request creates a second lead (OFF-3).
2. **The studio at 320 px.** The work area is about 147 px tall. It needs a small-phone layout, Design first.
3. **MAP-INT-04, price chips on the cone.** Designed in v130, not implemented. The comps chips can cover part of the
   frozen cone.
4. **An RTL warning in the map worker.** At 1440 with `?unit=`, when both maps start on load. Labels render fine.
5. **The accessibility button** covers the first word of the moved notice at 390 px.
6. **The canvas at 320 px:** its bottom 12 px sit under the bar at the landing.
7. **The scroll distance from the stage to the map canvas:** 875 / 932 / 568 px (390 / 320 / 1440).
8. **Phone studio reopen:** a second tap reaches the engine as `select`. It is inside the frozen engine and needs an
   adapter.
9. **Selection identity vs scene identity.** 13-e opens the 360 on the nearest floor with pictures (10) and says so.
   Keep the two separate: the chosen unit is never the scene.
10. **The designer's placement.**
    - It checks a centre and a radius, not a rotated footprint: a 2 m bed can stick out 0.15 m.
    - The tray hides the toolbar.
    - The phone mood buttons lose their names.
    - The mock "success" is not a delivery.
    - The WhatsApp summary carries only the first 6 notes.
11. **The continuous interior:** a portal graph and rail/volume clearance on the unit's own geometry. Labs only
    (`rail-clearance.mjs`, NAV-VOLUME-01).
12. **DESIGN-TO-DEAL (HAD-373):** one local slice (need → alternatives → studio → BOM in the RFP), waiting for Codex to
    agree the contract.
13. **Codex's business tracks, open:**
    - the failed listing-publication path;
    - the stale lead/task email;
    - a professional graph from evidenced work;
    - unit campaigns on the existing rails.

**From the recipe (`unit-layer-and-recipes.md` §3), rows no project page meets:**
1. **Row 13:** a plan per unit. No public plans exist.
2. **Row 16:** a cutaway. Missing across the fleet; Codex's UnitCut exists only in the lab.
3. **Row 21:** the deals high on the page.
4. **Row 22:** a gallery of 8+ house-style assets.
5. **Row 24:** the entities with links (developer, architect, contractor).
6. **Row 27:** a unit summary before the footer.
7. **Row 30:** the admin lights.
8. **Rule A12, the budgets.** DUO's `city.json` is 394 KB and its `places.json` 383 KB, on top of a 178 KB stage.js.
   A three-tower Kikar world must stay within the first-view budget (≤10 MB) and the Mapbox-per-load cost.

**Found in this pass:**
1. **The stage README is missing.** `rainbow/stage.js` says "See README.md for the full API", but no README exists in
   `assets/project-stage/`.
2. **The shared room cannot give video on Kikar either.** The room works for any slug in the config, but the LiveKit
   options are empty.
3. **`data/projects/duo-tel-aviv.json` is a July stub** (`needs_geocode`, `ready_for_page:false`). The real per-project
   data lives in `nadlan_ps_config()` and the stage folders.
   - The rich records are `rainbow-sde-dov.json`, `dimri-yama.json` and `ashira-sde-dov.json`.
   - The film's facts are in `scripts/project-video/data/duo-tel-aviv.json`.
   - **Kikar should get one canonical fact record, not a third copy.**

---

## 3. The build recipe for a new project (as DUO, Dimri Yama and Ashira were added)

**What the commits show.** The research ran first; the stage and the config went live in one release; the rest came in
later releases.
- **DUO:**
  1. `docs/research/2026-09-28-stages/stage-geometry.md` §3 and `duo-config-proposal.php.txt`;
  2. 1.72.333 (34edcfb8): stage + city + config;
  3. the slice (344), the deals (342-343), the 360 rooms (353), the walk (359), the places (365).
- **Dimri Yama + Ashira:**
  1. the proposals `dimri-config-proposal.php.txt` and `ashira-config-proposal.php.txt`;
  2. 1.72.336 (4637d6be): both stages;
  3. the slice (344-345), the places (365).

**Each first release carried:**
- `assets/project-stage/<dir>/`: stage.js, stage.css, city.json, quarter.json, facilities.json, poster.jpg, poster-716.jpg;
- the config in `inc/project-stage.php`;
- `nadlan-config.php` (the version);
- the builder script, the harness, the shots script and the runner;
- one line added to `tools/content_first_check.py`.

**The ordered steps for Kikar Hamedina:**

0. **Gates.**
   - Claude Design: a new version of the artifact L9Nqz7Viv7K3MYeZrBc9s8, component "KikarHamedinaWorld".
   - Linear HAD-375 and its Notion row.
   - Read `docs/checklists/PROJECT-PAGE-CHECKLIST.md` and the recipe §3.
   - Run `python tools/gsc/url_word_audit.py --token <word>` for every slug word.
1. **Facts (P1).** Write `docs/research/2026-09-30-kikar-hamedina/facts.md` in the H Infinity model:
   - evidence classes OFFICIAL / DEV / PRESS / DATA / CALC / LISTING;
   - conflicts side by side;
   - a "not published" list.

   Then `serp-he.md` (and the other languages), `competitors-dna.md`, `plan-*.md` and `prompt-*.md`.
2. **Geometry.** Add a stage-geometry section in the `stage-geometry.md` style:
   - the reference point;
   - the lot outline (GIS 837);
   - the towers' footprints and levels (GIS 513 / the plan);
   - the facilities' places;
   - the frame (the origin, the grid angle).

   Then a `kikar-config-proposal.php.txt` with the config below.
3. **The WordPress post.** Check read-only whether a catalogue post exists; else create the `nadlan_project` (Hebrew).
   - **Meta:** geocoded `lat`/`lng`, `developer_name`, `city`, `address`, `architect_name`, `num_floors`, `num_units`,
     `project_status`, `project_facilities`; `project_3d_avg_price_per_sqm` only if sourced. `project_mode` stays
     review.
   - **Content:**
     - the answer paragraph as the first ≥100-character `<p>`;
     - the article wrapped in `<div class="nadlan-project-article">`;
     - the FAQ as `<h2>שאלות נפוצות</h2>` + h3/p.
   - **Yoast title and description:** add the page to `scripts/seo/project_meta.py`.
   - **The language siblings `<slug>-en` (later fr/ru/ar):** each with `_nl_faq_schema`. Siblings inherit the stage
     automatically through `nadlan_ps_current()`.
   - **Watch the meta traps** in `docs/playbooks/project-factory.md` §4: gershayim, never ASCII quotes, and read back
     every write.
4. **The city.** Clone `scripts/project-stage/build_city_duo.py` as `build_city_kikar.py`:
   - the origin is the lot centroid;
   - `b` within 750 m, `f` out to 1.5 km and the sea;
   - Kikar's own lot is left to the stage.

   It writes `assets/project-stage/kikar/city.json` and `quarter.json`:
   - `origin` and `tower`;
   - our pages nearby: DUO and H Infinity, through their public REST;
   - the square's places.
5. **The stage.** Copy `dimri/stage.js` as `kikar/stage.js`, exporting `mountKikarStage`, and copy stage.css.
   - **Set these constants:**
     - `LOT_OUTLINE`;
     - `TOWERS` A/B/C (poly, floors, `lv` levels, techH, line);
     - the per-floor turn in the geometry and in `floorPlan()`;
     - `GRID_ANGLE`;
     - `SCENE` (the hero, intro and facility cameras, and `build()` for the ring, the park and the lake);
     - `anchorOf()`;
     - `TEXT` (the caption, the tower names).
   - **Keep the events and the public API as they are** (§1.B row 39).
   - **Decision to take in Design (P4/P5):** extract the shared engine once, or accept a fifth copy.
6. **`kikar/facilities.json`** (the schema of §1.B row 33): one sourced line per claim, and "the place in the model is
   an illustration" wherever the plan fixes no place.
7. **The config: a `nadlan_ps_config()` entry.**
   - `dir`, `mount`, `name`, `name_en`, `developer`, `place`, `rail => array()`, `poster_alt`, `src_line`;
   - the six `facts`, `progress`, `units` (made floor-aware);
   - `tower_lat`/`tower_lng` (the view's origin);
   - `sectors` (per tower if a tower faces a sister tower);
   - only when sourced: `deals`, `deals_intro`, `deals_sum`, `basket_hint`, `slice_note`, `low_note`/`high_note`;
   - `tour` words (dirs, facing, height, view_src, card_alt, card_title) before any interior pictures ship.
   - Add `'kikar'` to the `$space` table in `nadlan_ps_unit_resolve()` (once the branch is released).
8. **The local harness.**
   - Copy `duo_harness.html` → `kikar_harness.html`, and serve it with `python -m http.server 47961 --bind 127.0.0.1`.
   - Copy `duo_shots.py` → `kikar_shots.py`.
   - Check at 1440 and 390, and look at every shot.
   - Capture `poster.jpg` (1432×1320) and `poster-716.jpg`.
9. **The runner** (`scripts/project-stage/deployNNN.py`, from `deploy368.py`, with NEWFILES/FILES in the `deploy333.py`
   style).
   - **Files:** `assets/project-stage/kikar/*`, `inc/project-stage.php`, `nadlan-config.php`.
   - **Needs:**
     - `id="nlps"`, `mountKikarStage`, `project-stage/kikar/stage.js`, `class="nlps-h1"`;
     - both names;
     - `data-nlps-phase="facilities"`, the source line;
     - `id="nlsch"`, `nadlan-project-article`.
   - **Nevers:** Rainbow's alt text "מגדל ובנייני בוטיק סביב גינה", `class="nlpt-h1"`, and the blacklist.
   - Run `--dry` first.
10. **Before and after the release:**
    - add the page to `tools/content_first_check.py` PAGES and `tools/source_audit.py` WATCHLIST, with a snapshot
      before;
    - after: `content_first_check`, `source_audit`, `tools/wa_bar_audit.py`, `pagejourney.py`, `firstpic.py` and
      `pincheck.py`;
    - a live look on phone and desktop;
    - the fleet spot-check: Rainbow, H Infinity, the home;
    - a Linear comment, the Notion row, and a Hebrew report with screenshots.
11. **The eyes and the places** (both need the stage live, or a change to read a local harness).
    - Add `'kikar'` to `measure_eyes.py` P, with bands per tower, e.g. 10/25/38.
    - Add `'kikar'` to `build_places.py` PROJECTS. It reads `quarter.json`, and its `token()` reads the live page.
      Make the sight lines per tower.
    - This writes `kikar/places.json`.
    - The rest is automatic: the area map, the view lists and the 360 window names follow.
12. **The inside.**
    - Write `scripts/interior/kikar_world.py`, `kikar_interior.py` and `kikar_facility.py` from the duo_* scripts, and
      `render_kikar.py`.
    - Cut them with `cut_tour.py` into `tour/living-<f><d>.jpg` / `-2k` / `-card` and `fac-*.jpg`.
    - Then fill facilities.json `tour` and `walk`: `aptDoor`, `aptStops` per tower, doors measured in the renders.
    - Styles through `render_styles.py`, at the higher quality the owner asked for.
13. **The deals and prices.** Add them to the config as sourced rows only: the deals table, the floor notes, the basket
    hint, the price band meta.
14. **The languages.**
    - Add the page to `scripts/i18n/stage_harvest.py` PAGES.
    - Rebuild `build_stage_dict.py` (Kikar's names; brands stay Latin) and `build_lang_pages.py` (the chrome: developer
      and street names).
    - Run `tools/lang_pages_check.py`.
15. **The film** (after the stage is live): `scripts/project-video/capture.py` → `data/<slug>.json` (every line sourced)
    → `render.py` → `upload_media.py` → config `film`.
16. **Around the page, optional:**
    - a Kikar pin in the Somail tour;
    - a 'kikar' earth scene, once `/earth/` works;
    - a premium-catalogue row for the facility chips;
    - check that the home map's 3D pill includes it.
17. **The release after that:** turn this recipe into the `project-page-factory` skill (SITE-LOOP S1), so the next
    project does not rediscover it.
