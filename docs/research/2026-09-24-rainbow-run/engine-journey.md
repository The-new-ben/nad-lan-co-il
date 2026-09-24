# The showroom engine journey: what exists, what is live, what breaks if we flip (24.9.2026)

This was a read-only pass. It used the repo on branch `claude/production-truth-1.72.212`, live 1.72.254, public REST and page GETs, one built-in-browser DOM check of /projects/aurelia/, and the memory files. Evidence tags: **code** means read in source, **REST/HTML** means a live public GET, **DOM** means the built-in browser at 375px, and **mem** means the memory files or docs. Paths are under `plugins/nadlan-config/` unless stated otherwise.

## Summary
1. One meta controls the mode: `project_mode`. Anything other than `showroom` counts as review. Live, 1,030 of 1,031 published projects are in review. **Only Aurelia 7514 is showroom** (REST).
2. The gate runs at 7 call sites. The main one drops the engine and its payload (`inc/showroom-engine.php:925`). No query-param preview exists.
3. In code, the engine already covers most of the owner's journey: hotspots, the unit card, the Mapbox window view at floor height, the terracotta cone, the walk inside, the studio, co-tour, scheduling and 5 languages.
4. **Missing entirely:**
   - LiveKit video calls. LiveKit exists only in the owner's Hadmaya project.
   - Clicking a facility to see its image.
   - A real photo from the window.
   - A map that flies in and names what lies inside the cone. Today it only rotates.
5. Fleet inventory is demo data. Rainbow has 6 units, Dimri 4, Ashira 5 and DUO 5. ToHa2 and The Park have 75 and 44 floors, all marked "available" and all facing west. Unit-level demo labels exist in the data but never render.
6. Flipping as-is brings back what the owner ordered removed. That includes the investor "לתיאום שיחה" block, the scheduler and the empty "…מהיזם / יוצגו עם קבלת נתונים" states. It also brings false claims: "נמכרה", "הדירה הזמינה האחרונה", "75 דירות לבחירה" and "הכיוון אמיתי".
7. The legal reason behind the 30.8 decision still stands. The Brokers Law bars arranging viewings or relaying offers for third-party developers. Showroom was reserved for Aurelia or for a signed developer.
8. A live defect already exists: Aurelia publicly shows "חסרות קואורדינטות למפה" (DOM). Its lat/lng is 0, so it has no map, no window view and no cone.
9. The only nad-lan videos are the 118s developer film (attachment 5727, silent, meant "for developers, not buyers") and a 38s promo on the homepage.
10. Uncommitted, unloaded work sits in the repo: `inc/project-stage.php` with `assets/project-stage/bridge.js`, a Rainbow three.js stage for review mode. It steps aside on showroom pages, so flipping Rainbow hides it.

## 1. Review vs showroom
**The gate** (code): `inc/project-mode.php:11-16` returns `showroom` only on an exact meta match. Everything else becomes `review`. The filter `nadlan_project_mode` exists, but nothing hooks it. The meta is registered in REST at `:19-25` (values review, showroom or empty; writing needs `edit_posts`).

| Call site | Review | Showroom |
|---|---|---|
| `inc/showroom-engine.php:925-927` | no `#nl-root`, no `NADLAN_SHOWROOM` payload, no engine, model-viewer, studio, buyflow or Mapbox assets | full shortcode `:495-664` (payload, assets, inquiry form, investor block) |
| `inc/showroom-engine.php:1322` | chapter weave and table of contents skipped | `nlw-toc` + chapters |
| `inc/schema.php:128` | no FAQPage | FAQPage from `project_faq_json` |
| `inc/scheduler.php:685` | no booking band | `#nlsch` "בחרו תאריך" |
| `inc/feature-bar.php:190-215` | only chips with a real link, reviewer voice, 5 languages | all chips incl. engine anchors |
| `inc/conversion-cta.php:54-67` | pill reads "…עונים עצמאית, לא מטעם היזם" | generic "לפרטים נוספים" |
| `inc/project-stage.php:41` (untracked, not in loader `nadlan-config.php:33`) | Rainbow ProjectStage | steps aside |

**Renders in both modes:** the article (`showroom-engine.php:876-919`), facility chips, the Mapbox POI map `#nlpjx-map` and price band (`inc/project-experience.php:142-369`), catalog-plus price and surroundings, and the walk-inside assets on every project page (`showroom-engine.php:1374-1380`). Utopia runs its own ungated model runtime (`inc/utopia-showroom.php`).

**Live** (HTML, 11 flagship pages): `nl-root` and engine.js appear only on /projects/aurelia/. Password-protected private labs keep the engine in any mode (`showroom-engine.php:59-76`).

**How to flip one project:** `POST /wp-json/wp/v2/nadlan_project/<id>` with `{"meta":{"project_mode":"showroom"}}`, using an app password. Revert with `""`.
- Every language sibling is its own post and needs its own flip.
- Each save fires IndexNow (mem trap) and needs a LiteSpeed purge.
- Expect a source-audit diff.
- Never flip by filter: that puts the generic `standard-residential.glb` engine (`:250-254`) on about 990 imported pages, because `nadlan_showroom_engine_active_for()` returns true for all (`:836-839`).

**Preview without flipping:** none exists today. Three options:
- The `[nadlan_showroom_engine project="slug"]` shortcode has no mode check (`:457-478`), so it works on a private page, but without `#nlpjx-map` there is no cone.
- A password-protected private-lab clone.
- A new admin-only `nadlan_project_mode` callback triggered by `?nl_showroom=1`, with no-cache.

## 2. The journey in showroom mode (code; paths in `assets/showroom-engine/engine.js` unless noted)
| Step | Implementation | Today | Gap |
|---|---|---|---|
| Pick on the model | theater `:370-436` (model-viewer 4.3.1, one hotspot button per unit; position from `hotspot_position` or floor×direction formula `:171-197`); floor bands above 24 units `:590-680`; `selectUnit :4023`/`selectUnitLegacy :4106`; camera fly `:4162` | works (320 hotspots on Aurelia, DOM) | mesh tap does nothing; pills are sparse on some projects |
| Info card, legacy (Rainbow, DUO, Ashira, Dimri, Aurelia) | `panelBody :459-486` | status word from payload (he: available "להמחשה", reserved "בעדיפות", sold "נמכרה"); rooms, m², balcony, view or direction; sun hours `:1302` (geometric); scarcity `:496`; monthly payment from `u.price/price_estimate` `:512`; tabs plan/view/tour; save, compare, share `?unit=`, WhatsApp, "בנו לי הצעה" (buyflow.js), PDF, studio, inquire | unit `note/availability/source_note/price_note` are **never rendered**; payload `concept` (`showroom-engine.php:264`) is unused and `config.demo` is hard-coded false (`:386`); average ₪/m² appears only in the project `#price` block (`:851-900`) |
| Info card, v1/v2 (ToHa2×5, Park×5, H-Infinity, SIX-8, Einstein) | `unitSummaryMarkup :2260`, `renderUnitScreenV2 :2336`, doors `:1984`, tools `:3002-3150` | in-place scene, mini beam, compare, area and contact dialogs | the owner called the gold mini-beam a worthless duplicate (mem 13.8); undecided |
| Window view | inline tab `:520-555` + `winStageInit :1422`; camera `winCam :1406-1421`; big-map jump `winView :1515`; v2 dialog `mountWindowViewport :3816-4017` | `satellite-streets-v12` style, sky, 3D building extrusions; FreeCamera at `floor×fh+1.6 m`, pitch 86 adjustable 35-90; drag 0.35° per px turn and 0.22° per px tilt; ±30° buttons; fullscreen; the v2 dialog orbits 360° when direction is unknown; gated on non-city coordinates plus a token (`preciseGeo :1640`) | legacy **invents a west view (270°)** when direction is unknown (`:1408`, `:1519`); no real photo (no field, no Street View; photoreal Google tiles only on /earth/, `inc/earth-experience.php`, 85 root loads a day) |
| Beam and map | map `inc/project-experience.php:324-346,450-540` (light style, zoom 14.4, POI and price chips, future plans, 3D and satellite toggles, lazy; sets `window.NLPJX_MAP` and fires `nlpjx:map` `:463-464`); adopted under the theater `:1270`; model orbit turns the map `:1283`; `showViewCone :1318-1335`; `easeMapToUnitView :1336-1352` | on a press the map only rotates its bearing (900ms); the cone is a fixed **150px** terracotta wedge; with no direction there is no cone and the map re-centres at zoom 15.2 | no fly-in, tilt or automatic 3D; nothing inside the cone is named; the landmark ring (`project_env_landmarks`, `showroom-engine.php:336-366`) appears only in the mini beam (`:1749`); the beam is frozen and changes only by an owner spec |
| Walk inside | `:1362-1400` + `inc/interior-fp.php` (CSS-3D rooms, doors) | labelled "הדמיה סכמטית" | missing data defaults to **4 rooms, 85 m²** (`:1363`), which is invented |
| Studio | `studio.js` (real-size furniture, SI-1918 clearances, notes go into the offer request); opened `:4143`, dock `:409`, panel `:484`; v2 iframes `/tour/designer/` (`:2783-2807`, `inc/tour-routes.php:24-33`, live 200) | works (code) | `inc/studio.php` is the advertiser editor, a different thing |
| Facilities | `inc/facility-chips.php:75-138`: chips link to `/premium/?fac=` | label chips only | no "click the gym, see the gym"; Einstein's dormant v3 scenes (`inc/flagship-surface.php:1123-1330`) and the Aurelia lab (`docs/design-lab/aurelia-sports/`) sit outside the engine |
| Video call | `inc/cotour.php`: the host shares camera, unit, sun and filter every 1.6s over REST (`:684-737`); rooms live 5 min; the live route answers. `inc/flagship-cotour.php`: "no chat, audio, video" | a shared 3D view, no voice or video | **no LiveKit in nad-lan** (0 grep hits). It lives in Hadmaya: Supabase `video-sessions-api`, `LIVEKIT_API_KEY/SECRET/SERVER_URL`, livekit-client 2.15 (mem courtai `hadmaya-run-plan-2026-09-24.md:27`). Porting needs a WP token route, a representative's answer screen, consent, and a Brokers-Law check on who the representative is |
| Scheduling | `inc/scheduler.php` (slots and booking REST, ICS, Google calendar, WhatsApp confirm, owner's calendar by default, 5 languages) | live on Aurelia (DOM) | arranging viewings of third-party projects counts as intermediation |
| Languages | `i18n.js`: he/en 414 keys; fr/ru/ar 409, missing 5 (`inv_band`, `inv_bands_aria`, `unit_beam_view_short`, `unit_beam_around`, `unit_window_panorama_note`), which fall back to English; page language from slug suffix (`showroom-engine.php:210-224,631-634`); 14 projects have 4 siblings | buyflow, mv-ux, scheduler and feature bar are also in 5 languages | sibling payloads carry Hebrew unit text (REST: `rainbow-tel-aviv-en` view "מבט לחצר ולים"), which leaks raw into the legacy card |

## 3. Data per project
From the REST meta of each base post; units come from `project_3d_units`.

| Project (id) | GLB (bytes) | Units | Geo · floors × floor height | Other |
|---|---|---|---|---|
| rainbow-tel-aviv 4464 | uploads/2026/07/rainbow-rich-model.glb (851,668) | **6 demo** (5 available, 1 reserved; floors 7-38; plans; hotspots authored) vs 480 in `num_units` | 32.103168, 34.784441 · floors empty (engine uses 38) × 3.05 | 2 interiors, FAQ 6, ₪76,000/m² "אומדן"; legacy card |
| dimri-yama-sde-dov 4745 | models/dimri-rich.glb (429,444) | **4 demo** (2 available, 2 reserved; `price_estimate` 3.75M/6.2M/8.9M "אומדן פנימי"; formula hotspots) | 32.104441, 34.784472 · 39×3.2 | ₪75,000/m² |
| ashira-sde-dov 4744 | models/ashira-rich.glb (488,188) | **5 demo** incl. **1 "sold"** | 32.105643, 34.787673 · 35×3.2 | 3 real Tax-Authority comps; default interior is Rainbow's |
| duo-tel-aviv 4893 | models/duo-rich.glb (1,060,876) | **5 demo** (towers A/B) | 32.0847, 34.7824 · floors 0 × 3.1 | Africa Israel (the 30.8 warning); Rainbow interior |
| h-infinity-somail-tel-aviv 6548 | uploads/2026/08/h-infinity.glb (696,908) | 52 floors, status unknown; directions `se/w/ne` are **not recognised**, so no cone | 32.086, 34.7821 · 52×3.35 | 6 landmarks (mem), v2 |
| einstein-tower 4867 | einstein-tower-model-hd.glb (2,420,492) + LOD (32,244) | 28 floors, status unknown; long-form directions seeded 16.8 as owner-ordered demo, so the cone points | 32.111736, 34.788433 · 28×2.97 | 6 landmarks, v2, `is_demo`; v3 surface dormant (4 governed scenes); protected article |
| six-8-herbert-samuel-tel-aviv 7219 | six8-herbert-samuel-massing-v2.glb (92,724; same bytes as `docs/playbooks/`) | 2 "דוגמה" units (floor 11: 7 rooms, 232 m²; floor 18 penthouse, 339 m²), facing west per the developer | 32.068524, 34.763321 · 18×3.6 | plans, interiors, gallery 9, press price ₪200,000/m², area data, 7 landmarks |
| utopia-sde-dov 4749 | models/utopia-rich-v1.glb (309,148) | none in the engine; own runtime (29 plan references) | 32.106063, 34.784732 · 34 | concept interior |
| toha2-tel-aviv 6213 | toha2-tower-2.glb (940,000) | **75 floors all "available", all west** (office) | 32.073479, 34.795307 · 75×3.51 | landmarks, v2, no poster |
| the-park-bnei-brak 6182 | the-park-tower.glb (1,173,216) | **44 floors all "available", all "מערב"** | 32.103671, 34.82964 · 52 | empty poster, v2 |
| aurelia 7514 (showroom) | aurelia-tower-semantic-v2.glb (330,508) | 320 concept units (rooms, m², plan) | **0,0** · 47×3.05 | 4 panoramas, gallery 5; **252KB inline payload** |

All model files are listed in `INVENTORY.md` and `assets/showroom-engine/models/`. Facility data is not exposed in REST.

## 4. Why review mode, the conditions and the honesty rules
**30.8 order** (mem `nadlan-session-handoff.md:219`; release 1.72.224, commit 97bc90f):
- **The trigger:** at the Zoom meeting, EcoCity said the pages were too low-level and asked to be removed. A friend who is a CEO warned about developers such as Africa Israel (DUO), and a Gemini legal opinion scared the owner.
- **His orders:** remove EcoCity; switch everything to review; remove the engine's "meeting coordination" investor block.
- **31.8 follow-up (1.72.225-226):** it also killed the scheduler, the table of contents and the dead chips, and switched to reviewer voice.

**The condition to return:** *"reserved for the conceptual flagship (Aurelia) and projects with a signed developer partnership"* (`inc/project-mode.php:6-7`). No fleet project meets it. Today's order overrides it knowingly.

**Honesty rules:**
- Iron law 3 in CLAUDE.md: invent no inventory, bearings, facilities, prices, dates or views; omit what is unknown; "0 rooms" and "כיוון בבדיקה" are forbidden.
- Recipe §2.1: statuses and "הדמיה להמחשה" labels.
- Owner, 19.8: purge empty states and never write "מהיזם".
- Owner, 16.8: a demo is allowed on Einstein.
- 3D report: say "six demonstration apartments", never 480.

**EcoCity:** no published project has an EcoCity slug, title or developer (all 1,031 scanned via REST). Bnei Dan 6693, Striker 6694 and EcoCity 6695 stay drafts. Any flip script must filter `status=publish`.

## 5. The specs and the open defects
**Specs:**
- `docs/playbooks/flagship-showroom-recipe.md`: laws, meta contract, QA gates in §12.
- `docs/playbooks/the-beam-field-guide.md`: the beam's link, ground, context and honesty laws.
- `assets/flagship-v3/contracts/registry.json`: the "Spatial Decision Room" contract.
  - **Journey:** understand → locate → explore → verify → compare → collaborate → inquire → return.
  - **Page order:** lead → notice → model → attached map → actions → tools → film → article.
  - **Selection:** the card opens in place, a back-to-building control, and no cone without a verified bearing.
- Prototype repo `C:\Users\777\nad-lan\einstein-tower-prototype`: `DEPLOYMENT-RECEIPT-1.72.210/211.md`, `docs/05-MAPBOX-WINDOW-VIEW.md`, and the skills in `final-handoff-2026-08-15/prototype-repository/skills/*-spatial-decision-room/`.
- Owner additions, 20.8: a unit press turns the cone; mini floor plans, areas and parking on cards; filters that mark the building; 360°, amenities and gallery.

**Open defects:**
- **Left open after 211** (the five defects of 1.72.210 were fixed):
  - mobile CTA at 1,823px against a 1,688px budget;
  - WhatsApp adoption timing;
  - the "selectable" copy;
  - the dotted-.webp rule;
  - the five language pages;
  - construction progress;
  - co-tour tested with two viewers.
- **Standing complaint, 16.8:** the tap jumps the page, the card covers the model, the tools should be image tiles, and the theater needs to be bigger ("10,000 times").
- **3D CEO report** (`einstein-tower-prototype/docs/reports/nadlan-3d-ceo-report-2026-08-19.md` §8):
  - Rainbow's window tab painted no panorama on a live click;
  - a camera-fly race;
  - a lazy hero model;
  - USDZ files return 404;
  - two model-viewer versions;
  - floating buttons over the stage;
  - Einstein at 2.4MB with no LOD;
  - the feature bar promises a window view where there is no map.
- **Pending the owner:** the lead-form bug and the mini-beam's fate.
- **Stale pointers:** CLAUDE.md "Current state pointers" still say live is 1.72.210 and Einstein is the showroom.

## 6. The videos
Durations come from WP media REST; there is no ffprobe on the machine.

| ID | File | Length | Content |
|---|---|---|---|
| 5727 | uploads/2026/08/nadlan-developer-film-hq.mp4 | 118s, 720p, 28.9MB, silent | product-concept film: "חיפוש והבנת הפרויקט · סיור בשכונה ובמודל · בדיקת תצפית וחללי המחשה · בחינת אפשרויות והמשך להחלטה" (registry). Shown on /film/ and /developers/ (`inc/developers-page.php:21-38`). Owner, 16.8: "for developers, not buyers". |
| 5724 / 5719 | …-720p.mp4 / …film.mp4 | 97s / 118s at 600×338 | 5719 is the same file as repo `media/film/nadlan-developer-film.mp4` (8,098,101B; copies in 6 worktrees, Documents\ChatGPT-Work and Codex) |
| 5052/5051, 5010 | uploads/2026/07/nadlan-promo-v2.mp4/.webm, nadlan-promo.mp4 | 38s | promo on the homepage band "סיור תלת ממדי וסרטון היכרות" |
| 5575 | damac-riverside-views-hero-video.mp4 | 15s | Dubai international page |
| 8099/8100 | meital-katzir-listings-*.mp4 | – | a broker's listings |

No storyboard was found. The other videos under C:\Users\777 belong to Hadmaya/courtai.

## 7. Risks of flipping today
1. **Invented claims go live.**
   - "נמכרה" on an Ashira demo unit.
   - Scarcity lines computed from demo stock (`engine.js:496-503`).
   - A hero counter "N דירות לבחירה" counting demo "available" units (`:350-357`): 75 on ToHa2 and 44 on The Park, both office towers.
   - A monthly payment computed from Dimri's internal estimates (`:512`).
   - All ToHa2 and The Park floors facing west.
   - The west-view default (`:1408`).
   - Walk-inside defaults (`:1363`).
   - Rainbow's interior shown on DUO and Ashira.
   - Copy "גובה הקומה והכיוון אמיתיים" (`winview_note`) and "הכיוון אמיתי" (`unit_map_unverified`).
2. **What the owner banned comes back.**
   - The investor "קונים מחו״ל · לתיאום שיחה" block (`engine.js:1095-1101`), which is live on Aurelia.
   - The scheduler.
   - The strings "…יוצגו עם קבלת נתונים מאומתים", "סיור 360 מהיזם יעלה…", "טרם התקבלו תוכניות מהיזם" and "…אחרי העלאת חזית רשמית מהיזם".
   - Empty "כל מה שמסביב" and "פרויקטים סמוכים" sections where there is no `project_area_json` (only SIX-8 and Aurelia have it).
3. **Legal (Brokers Law).**
   - The scheduler and a future "representative" video call both arrange viewings.
   - "בנו לי הצעה", whose consent reads "נדלן תעביר את הפנייה ליזם".
   - The WhatsApp pill drops its "לא מטעם היזם" line.
4. **Language law.**
   - Blacklisted words in the engine's Hebrew: "סימולציית שמש", "הדמיה סכמטית" and "תרשים סכמטי", "נתוני הדגמה", "המודל", "כיוון בבדיקה" (banned outright), "המפה החיה", an em dash, and mv-ux's "לחצו על נקודה בבניין". No "אטלס" found.
   - Hebrew text leaks onto the -en/-fr/-ru/-ar pages.
5. **Duplicates.**
   - Two beams: the gold mini-beam plus the cone.
   - Three price surfaces: the engine `#price` block, `nlpjx-price` (`project-experience.php:196`) and catalog-plus.
   - Up to 4 live Mapbox maps on one phone, each a billable load.
   - Rainbow's ProjectStage disappears.
6. **Aurelia is already broken.**
   - The public text "חסרות קואורדינטות למפה" (`assets/showroom-engine/mapbox-init.js:55-56`).
   - No window view, map or cone.
   - The legend shows sold and reserved while every unit is unknown.
   - "קומה 6 · קומה 6" repeated in a label.
   - The GLB had not loaded after about 10 seconds in the built-in browser (unverified).
   - The model starts at 2,355px of a 17,163px page on mobile.
7. **Weight.**
   - Libraries: model-viewer 292KB and mapbox-gl 307KB (both compressed), loaded eagerly whenever a token exists (`showroom-engine.php:579-584`); engine.js 68KB compressed, i18n.js 89KB, CSS 60 to 114KB.
   - Models: 0.09 to 2.42MB.
   - Payload: up to 252KB inline JSON.
   - Page: Aurelia's HTML is 458KB against 246KB for Rainbow in review.
8. **Lead loss.** The legacy form shows success even when the request fails: `.then(done).catch(done)` at `engine.js:4346-4350`.
9. **Mobile.** The card overflows the model, the WhatsApp pill overlaps the stage (seen in the Aurelia screenshot), hotspot pills are sparse, and the theater is small.
10. **Operations.** Every sibling needs its own flip. Every flip means a purge, an IndexNow ping, a source-audit diff and an FAQ-schema change. Drafts and the EcoCity IDs must never be touched.

**Bottom line:** flipping the meta alone restores a layer with known faults. A pre-flip pass needs to cover:
- per-project data that is real or labelled;
- removing or re-voicing the investor block, the scheduler and the "מהיזם" states;
- the lead-form, west-view and walk-inside default fixes;
- an owner decision on a beam upgrade (a geographic cone, a fly-in, named targets) and on the mini-beam.

Facility scenes, a window photo and LiveKit are new builds.
