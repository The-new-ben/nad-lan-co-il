# The unit layer we already had, and the recipes every project page must follow (24.9.2026)

Read-only research. Nothing was deployed or written to the site. It builds on `engine-journey.md` in this folder and does not repeat it.

**Evidence tags:**
- **code**: read in source, with file:line.
- **REST**: a live public GET of `/wp-json/wp/v2/nadlan_project/<id>` on 24.9 (live 1.72.256).
- **HTML**: a live raw-HTML GET of the page on 24.9 (view-source, not DOM).
- **snap**: the public-source snapshots of 24.8 and 25.8, when the fleet was still in showroom mode, kept in the Aurelia package.
- **pkg**: the Aurelia master-recipe package.
- **mem**: memory or docs.
- **unverified**: not proven.

Paths are under `plugins/nadlan-config/` unless they are marked `repo:` (the nad-lan-co-il root) or `pkg:`.

`pkg:` is `C:\Users\777\Documents\ChatGPT-Work\nad-lan-co-il\handoff\codex\2026-08-25-aurelia-master-recipe\`. That folder is a separate clone on branch `codex/aurelia-master-recipe-2026-08-25`, commit 3bf0c63. The commit is **not** in the main repo, its worktrees or the Einstein repo. Zips of the same package sit in `pkg:downloads\` and in `C:\Users\777\Documents\Codex\2026-08-24\...\outputs\`.

## Summary (15 lines)

1. **The old engine picked apartments, not floors.** Rainbow's payload (meta `project_3d_units`, post 4464, REST) holds 6 apartments: floors 7, 8, 16, 24, 31 and 38; 3 to 5 rooms; 82 to 210 m². Each one has its own facing (225/270/315/135/270/270°), plan, hotspot, camera orbit and facade tile. The payload is byte-identical to the 24.8 public showroom page (snap).
2. **All six are demo, by the data's own words:** "יחידת הדגמה למיפוי חוויית showroom. להחלפה בתוכנית מכר רשמית." and "לא BIM רשמי". Every price is 0. The statuses (5 "available", 1 "reserved") are invented. The five plans are generic SVGs with "ILLUSTRATIVE PLAN" printed on the image.
3. **The model mapping was Tier C only.** The hotspots are hand-placed on a single-mesh GLB that has no anchors. All six normals are `0 0 1`, whatever the facing. So the facing lived only in `dir`, which drove the cone, the window view and the sun.
4. **What the engine gave each apartment** (`assets/showroom-engine/engine.js`, frozen):
   - highlight and filter dimming, the card, and the plan (a zoom tool in v2);
   - the window view at floor height: drag, ±30° turns, fullscreen, and a 360° orbit when the bearing is unknown;
   - the terracotta cone that turns the area map, and the named-landmark ring;
   - sun hours, the studio, the walk-inside, `?unit=` sharing, co-tour, and a lead that carries the unit id.

   It never had a cutaway, facility hotspots, or neighbouring buildings you could click or read.
5. **The fleet:**
   - Only Aurelia has a real apartment grid: 320 units in lines, 320 `UNIT_ANCHOR` nodes in the GLB, and surface-tap selection.
   - SIX-8 has 2 units with sourced sizes.
   - H-Infinity and Einstein have one stand-in unit per floor.
   - DUO, Ashira and Dimri have 4 or 5 demo units each (Ashira shows a "sold" unit; Dimri shows internal price estimates).
6. **The Aurelia master recipe was found:** 20 page sections, 138 checks in 17 domains (R01-R17), 67 unit-selection checks and the Tier A/B/C selection contract. §3 merges it with v1, v2 and the Einstein registry into one ordered checklist, with a verify method on every row.
7. **The Einstein prototype** holds the "Spatial Decision Room":
   - a contract-enforced 9-slot page;
   - a shareable-state deep link with all-or-nothing restore;
   - six evidence states on every scene, and scenes anchored on the model;
   - a verified-unit contract that refuses a cone without a sourced bearing;
   - co-tour that asks consent first, fail-closed release gates, and a template factory with 15 build gates.

   The runtime also sits in nad-lan, dormant since the 16.8 flip. The live Einstein page has no 3D at all.
8. **"Echo City" in that repo is EcoCity**, the developer taken down on 30.8 (posts 6693-6695, snippet x-echo-city). The repo still holds EcoCity plans and tour material and does not record the takedown. Only its real-inventory intake format is safe to reuse.
9. **The new Rainbow stage** is live in 1.72.256 (`assets/project-stage/rainbow/stage.js`). It picks a floor (1-40) and then any facing on that floor's ring. It has:
   - no unit id, plan, rooms, m² or inventory;
   - no `?unit=`, no stored lead (WhatsApp only);
   - no 360°, interior walk, studio or co-tour;
   - Hebrew only: the EN sibling page has no stage.
10. **Recipe gaps on the live Rainbow page (HTML):**
    - The answer paragraph is generic.
    - The hero has no CTAs and no facts.
    - Progress comes after the map.
    - There is no FAQPage schema, but two visible FAQ blocks.
    - The 76,000 ₪/m² estimate is labelled "לפי היזם".
    - The page says 480 units; the official figure is 459.
11. **The numbers disagree:**
    - Tower floors: 38 in the old engine, 39 official, 40 in the new stage.
    - Boutique buildings: 8 floors official, 8 or 9 in the stage.
    - Floor 16's eye height: 50.4 m (engine), 56.8 m (stage), 59.3 m (the July view config).
12. **Proposal:** a unit is a floor plus an arc of the stage's facade ring. The ring already stores 1,440 samples, each with an outward normal and a true bearing. The facing is the normal at the arc's centre. The five tower units map to arcs centred on 225, 270, 315, 135 and 270°. The boutique unit waits until the blocks can be picked.
13. **Selection** uses Tier B (the floor from `hitTower` plus the nearest ring sample picks the unit whose arc holds that bearing) and Tier C (44px projected dots that hide when they face away or are hidden behind the tower). A new `nl:unit` event feeds what bridge.js already has (`showView`, `showBeam`), plus a plan dialog, a consented lead that carries the unit id, and `?unit=`.
14. **Honest reuse:**
    - Show rooms, m², balcony and the plan under one label: "דירה לדוגמה, להמחשה".
    - Hide the statuses and every note field.
    - Say a direction in words, never in degrees.
    - Fix floors to 39 and one floor-height source.
15. **Clone path:** move the tower, blocks, coast, sectors and units into per-project config, and gate each fleet project on how truthful its unit data is (§6.7).

---

## 1. Rainbow's old unit data, exactly

### 1.1 Where it lives
- **Storage:** post meta `project_3d_units` on `nadlan_project` 4464 (`rainbow-tel-aviv`). It is REST-exposed; this pass read it with a public GET (REST).
- **How the engine reads it:** `inc/showroom-engine.php:172-331` (`nadlan_showroom_engine_build_project`) decodes it and passes it through untouched as `units` (`:331`). It is printed into `window.NADLAN_SHOWROOM` only in showroom mode (`:925`, see engine-journey §1).
- **The 24.8 public page** (`pkg:01-DEMO-LAB/evidence/rainbow-public-source-2026-08-24.html`, engine 1.72.218) carries the same six units, byte-identical after key sorting (snap).
- **Older repo copies** (July): `repo:assets/projects/rainbow-tel-aviv/unit-map.json` holds the same six units with GitHub-raw plan URLs. `repo:.../view-layer-config.json` holds per-unit `bearing_degrees` and `altitude_m`, from the formula `ground 8.0 + 4.0 + (floor-1)×3.05 + 1.55`.
- **The window-view camera:** the engine replaced that July config. It uses its own camera at `floor×fh+1.6` (`engine.js:1406-1421`).

### 1.2 The six apartments

**Where they sit:**

| id | floor | line | `dir` (raw) → enum → bearing | view (payload) | `hotspot_position` / normal | `camera_orbit` | facade tile x,y,w,h (%) | rec |
|---|---|---|---|---|---|---|---|---|
| unit-08-sw | 8 | SW | דרום מערב → south-west → 225° | מבט לחצר ולים | `0 31 6` / `0 0 1` | 45deg 66deg | 40,72,17,9 | no |
| unit-16-w | 16 | W | מערב → west → 270° | קו החוף ושדה דב | `-5 55 7` / `0 0 1` | 35deg 63deg | 50,56,17,9 | no |
| unit-24-nw | 24 | NW | צפון מערב → north-west → 315° | ים, פארק וצפון תל אביב | `-6 80 5` / `0 0 1` | 24deg 61deg | 34,40,17,9 | yes |
| unit-31-se | 31 | SE | דרום מזרח → south-east → 135° | קו הרקיע והחצר הפנימית | `6 101 -5` / `0 0 1` | 310deg 64deg | 46,26,17,9 | no |
| unit-38-penthouse | 38 | PENTHOUSE | מערב → west → 270° | פנטהאוז גבוה לכיוון הים | `0 124 7` / `0 0 1` | 32deg 58deg | 40,13,20,9 | yes |
| unit-boutique-07 | 7 | 07 | מערב → west → 270° | בניין בוטיק סביב הלגונה | `-42 25 24` / `0 0 1` | 55deg 67deg | 10,78,16,9 | no |

Every camera orbit ends in `auto` (radius).

**What each one is:**

| id | label (= title) | rooms | m² | balcony | status (demo) | plan (uploads/2026/07/) | `interior_url` |
|---|---|---|---|---|---|---|---|
| unit-08-sw | דירת 3 חדרים, קומה 8 | 3 | 82 | 10 | available | plan-3br.svg | – |
| unit-16-w | דירת 4 חדרים, קומה 16 | 4 | 112 | 14 | available | plan-4br.svg | interior-rainbow-tel-aviv-unit-16-w.jpg |
| unit-24-nw | דירת 4 חדרים, קומה 24 | 4 | 128 | 16 | available | plan-4br.svg | – |
| unit-31-se | דירת 5 חדרים, קומה 31 | 5 | 156 | 22 | available | plan-5br.svg | – |
| unit-38-penthouse | דירת 5 חדרים, קומה 38 | 5 | 210 | 42 | available | plan-penthouse.svg | interior-rainbow-tel-aviv-unit-38-penthouse.jpg |
| unit-boutique-07 | דירת 4 חדרים, קומה 7 | 4 | 118 | 18 | reserved | plan-boutique.svg | – |

**Same on all six:**
- `building` is "Rainbow Tel Aviv", even on the boutique unit.
- `points` is empty, and `price` and `price_estimate` are both 0.
- `tour_url` is empty.

**Assets:** all five plan SVGs, both interiors, `models/rainbow-facade.jpg` and the GLB answer HTTP 200 (HEAD, 24.9). The GLB is 851,668 B, the same size as `repo:assets/projects/rainbow-tel-aviv/model.glb` (md5 f059226e…).

**Project-level fields the engine used** (24.8 page, snap):
- `floors` 38. `project_floors` is empty, so this is the highest unit floor (`showroom-engine.php:191-196`).
- `floor_height_m` 3.05. The meta is "0", so the engine falls back.
- `frame_radius_m` 162.
- `geo` `{32.103168, 34.784441, confidence: "parcel-centroid-verified"}`.
- `hero_eyebrow` "רובע שדה דב · מול הים".
- `units_total` 480.
- `price.avg_psqm` 76,000, with the note "…שמוצג במדלן לפרויקט/סביבה, נבדק 14.6.2026…".
- `default_interior` is the unit-16-w image.
- `facade_image` is `models/rainbow-facade.jpg` (viewbox `0 0 1000 1333`, `concept:true`, `approved:false`).
- `default_tour`: 12 standard images.
- `faq`: 6.
- `config.selected_unit_surface` false, so Rainbow used the **legacy card**. `studio` "on".

**The six landmarks** (`project_env_landmarks`, 5 languages each):

| Landmark | Coordinates |
|---|---|
| מתחם שדה דב | 32.1078 / 34.7808 |
| פארק הירקון | 32.094 / 34.784 |
| רידינג | 32.0966 / 34.7757 |
| הים | 32.103168 / 34.7727 |
| נמל תל אביב | 32.0967 / 34.7722 |
| רכבת אוניברסיטה | 32.104 / 34.8047 |

"הים" sits due west, about 1.1 km out. The new stage measures the shore at 713 m and 287° (`stage.js:113-116`).

### 1.3 How each unit mapped onto the 3D model
- **The GLB** (`rainbow-rich-model.glb`, the repo copy parsed locally) is **one node and one mesh**, "Rainbow illustrative tower, boutique ring and amenity court". It has 12 materials, **no extras, and no `UNIT_ANCHOR` or `UNIT_PICK` nodes**. Bounds are x −81 to 86, y 0 to 138, z −64 to 77 (code).
- **Tier C only.** `engine.js:372-376` renders one `<button slot="hotspot-<id>" data-position data-normal>` per unit. The position comes from `unitPos()` (`:171-197`): an authored `hotspot_position` wins, and otherwise a floor × direction formula on a 13.2 m square. model-viewer projects the button and hides it when it faces away.
- **No Tier B.** There is no surface tap or `positionAndNormalFromPoint` on Rainbow; only Aurelia's snippet has that (§1.4).
- **No Tier A.** There are no pick meshes.
- **The authored y values** are 31/55/80/101/124 for floors 8/16/24/31/38. That fits roughly 3.1 m per floor over a base of about 6 m in the GLB, not the engine's 3.05 × floor.
- **All six normals are `0 0 1`** and the camera orbits sit at 24-55° or 310°. So every apartment, including the south-east one, sits on and is flown to the model's +Z front (code).
- **Where the facing lived.** It was carried only by `dir` → `dirKey()` (`engine.js:46-52`) → `DIR_BEARING` (`:1297`). That drove the cone (`:1336-1352`), the window camera (`:1406-1421`), sun hours (`:1302-1314`) and the "sunlit" ring (`:793-805`).
- **The 2D alternative:** facade tiles in % on `rainbow-facade.jpg` (`engine.js:383-388`), shown with the 3D/facade toggle (`:415`).
- **An axis note** (code, not verified by eye). The fleet does not agree on which way is north:
  - The engine's map sync assumes model −z is north (`:1282`, map bearing = −θ).
  - Its fallback formula puts north at +z (`DIRV` at `:170`).
  - H-Infinity's 52 facings match +z = north on 51 floors and −z on only 13 (REST, computed).
  - The Einstein model spec also says +Z is north (§4.2).
  - Aurelia keeps `camera_orbit` θ equal to the azimuth, which faces the right wall only for east and west lines.

  A rebuild must pick one convention and write it into each project's config. With −z as north, θ = (180 − azimuth) mod 360.

### 1.4 Sourced or demo: the data's own words
- **Every unit row says it is demo:**
  - `note` "יחידת הדגמה למיפוי חוויית showroom. להחלפה בתוכנית מכר רשמית."
  - `availability` "זמינות להדגמה בלבד עד לקבלת מלאי רשמי מהיזם"
  - `source_note` "מודל אבטיפוס מקורי על בסיס מקורות פומביים, לא BIM רשמי."
  - `price_note`, `price_source` and `market_note` "אומדן מחיר יוצג רק לאחר אישור מקור נתונים. לא הצעה ולא התחייבות."
  - `view_note` "תוכנית המחשה מקורית לדירת … יש להחליף בתוכנית מכר רשמית."
- **Sourced facts exist only at project level**, and the rows do not carry them (`repo:data/projects/rainbow-sde-dov.json`):
  - Israel Canada; contractor Ashtrom; architects ברעלי לויצקי כסיף דה לה פונטיין; interiors Orly Shrem.
  - 1 tower of 39 floors plus 6 boutique buildings of 8 floors.
  - 459 units (the annual report updated 480 → 459).
  - At 31.12.2025: 270 sold, 189 remaining, 59% marketed, average sold price **80,300 ₪/m² incl. VAT**, from the Israel Canada 2025 annual report.
- **Plans:** `plan-*.svg` (2.3-2.6 KB) are schematic. They have "ILLUSTRATIVE PLAN" printed on the image, and no north arrow or dimensions (code). That breaks "label in the caption, not on the image" (v1 row 14) and R07-003/004.
- **Unrendered fields:** the engine never reads `note`, `availability`, `market_note`, `source_note`, `price_note`, `price_source`, `view_note`, `line`, `building`, `title` or `points` (grep, code). They are provenance only, and several use waiting phrases from the blacklist family ("עד לקבלת…מהיזם", "יוצג רק לאחר…").

### 1.5 The rest of the fleet in one table
Sources: REST on 24.9 for the units; snapshots of 25.8 (`pkg:04-RESEARCH/prior-forensic-baseline/09-…snapshots-2026-08-25.zip`) for the engine config, geo and landmarks.

**Data:**

| Project (post) | Units, id pattern | Floors in data / engine floors × fh | `dir` form → cone? | Status | Plans / interiors |
|---|---|---|---|---|---|
| **Rainbow** 4464 | 6, `unit-08-sw` | 7-38 / 38 × 3.05 | Hebrew → enum, yes | 5 available, 1 reserved | 6/6 SVG / 2 |
| **SIX-8** 7219 | 2 (10 on 25.8), `floor-11-demo`, `floor-18-demo` | 11-18 / 18 × 3.6 | `west`, yes | unknown | 2/2 real plan JPGs / 2 |
| **H-Infinity** 6548 | 52, `floor-01…52`, one per floor | 1-52 / 52 × 3.35 | `se`/`w`/`ne` letters → **no cone** | unknown | 0 / 0 |
| **Einstein** 4867 | 28, `floor-01…28` | 1-28 / 28 × 2.97 | long form, yes | unknown | 0 / 0 |
| **DUO** 4893 | 5, `duo-a-09…duo-b-45` (two towers) | 9-45 / 54 × 3.1 | Hebrew, yes | 4 available, 1 reserved | 0 / 2 |
| **Ashira** 4744 | 5, `ashira-18-west` | 4-18 / **18** × 3.2 (35 real) | enum, yes | 3 available, 1 reserved, **1 sold** | 0 / 2 |
| **Dimri** 4745 | 4, `dimriyama-u1…u4` | 12-39 / 39 × 3.2 | Hebrew, yes | 2 available, 2 reserved | 0 / 2 |
| **Aurelia** 7514 (showroom) | 320: lines A-F on floors 6-43, PH-E/PH-W on 44-47, garden lines G1-G12 on 2-8 | 2-47 / 47 × 3.05 | Hebrew with hyphen, yes | unknown | 320/320 PNG / a 360° tour per unit (`?aurelia_tour=`) |

**Mapping, and what the data says about itself:**

| Project | Mapping (tier) | Geo · landmarks | Engine surface (25.8) | The data's own note | Verdict |
|---|---|---|---|---|---|
| **Rainbow** | C, authored, all normals +Z; facade tiles | parcel-centroid-verified · 6 | legacy card | quoted above | demo |
| **SIX-8** | C, authored, normal −x | address-approx · 7 | v2 surface | "שטח הדירה והמרפסות לפי דיווח פומבי משנת 2025" | sizes sourced, framed "דוגמה" |
| **H-Infinity** | C, authored normals per floor (they follow the +z = north formula) | address-approx · 6 | v2 | "תמהיל הדירות בקומה יפורסם עם קבלת נתוני היזם" (a waiting phrase) | stand-ins; facings spread, not sourced |
| **Einstein** | C, authored positions, no normals | address · 6 | v2 (flagship-v3 dormant) | none | directions are an owner-ordered demo (16.8) |
| **DUO** | C, authored, normals +Z; facade tiles | parcel-centroid-verified · 6 | legacy | "יחידת אב-טיפוס להמחשת הבחירה במגדלי DUO. יש לאמת זמינות, מחיר ותוכנית מול היזם." | demo; uses Rainbow's interior |
| **Ashira** | formula (no `hotspot_position`); facade tiles | parcel-centroid-verified · 6 | legacy | none | demo |
| **Dimri** | formula; facade tiles plus SVG `points` | parcel-centroid-verified · 6 | legacy | "יחידת אב-טיפוס…"; `price_estimate` 3.75M, 6.2M and 8.9M, "אומדן פנימי" | demo with internal prices |
| **Aurelia** | **B + C**: 320 `UNIT_ANCHOR__<id>` nodes with `extras` (floor, line, normal, hit_region); surface tap plus projected dots (`repo:scripts/aurelia/snippet_experience.php:64-84`) | lat/lng 0 → no map (a live defect) | legacy card plus the x-aurelia-experience snippet | "הדמיה להמחשה" (pkg) | concept (fictional) |

"The 30.8 order" means everything moved to review mode on 30.8. Today only Aurelia still runs the engine (engine-journey §1).

---

## 2. What the old engine could do, with file:line
All rows are in `assets/showroom-engine/engine.js` unless marked otherwise (code). "Legacy" is the Rainbow, DUO, Ashira, Dimri and Aurelia card. "v2" is the SIX-8, H-Infinity and Einstein surface.

| Capability | Where | What it did | Limits and honesty flags |
|---|---|---|---|
| Unit hotspots on the model | `:370-436` theater; `:372-376` one hotspot per unit; `:171-197` `unitPos` | model-viewer hotspot slots with status classes (`nl-hot--reserved/--sold`) and a `--rec` pulse; legend `:423` | Tier C only; stays pure DOM; 0×0 chips on mobile across the fleet (Aurelia receipt #8) |
| Highlight and linked selection | `:4039` / `:4114` `is-active` across hotspot, facade tile and card; `:4040-4046` scrim spotlight; `:4162-4174` two-beat camera fly; `:4178-4200` lift-out card; `:4153-4158` reset | selecting in any place marks all three | the camera fly uses `camera_orbit` exactly as stored (see the axis note in §1.3) |
| Filters that mark the building | `:813-831` `applyStageFilter` (dims non-matching hotspots and tiles); chips `:670-674` (all, available, 3, 4, 5, favourites, with counts) | the building itself reflects the filter | counts demo "available" units |
| Floor bands | `:598-627` (more than 24 units → decade bands, penthouse first) | H-Infinity-scale inventory | – |
| Inventory cards | `:629-679` (legacy and v2 markup); recently viewed `:565-587` | the list and the model stay in sync | – |
| Unit card, legacy | `:459-486` `panelBody` | status badge, rooms, m², balcony, view, sun hours (`:488-492`), scarcity (`:496-503`), mortgage (`:512-519`), tabs plan/view/tour (`:471-475`), save/compare/share/WhatsApp, "בנו לי הצעה" (`:482`), brochure PDF (`:483`), studio (`:484`), inquire | scarcity and "N דירות לבחירה" (`:350-357`) come from demo stock; the payload's note fields are never shown |
| Unit card, v1/v2 | `:2260-2290` summary; `:2243-2258` v2 screen; `:2162-2209` v2 facts; `:2211-2241` doors (plan/view/tour/studio); `unit-sheet.js` two-detent sheet (20.8) | in-place card, "back to the building" | owner 26.8: a compact card with no expanded state |
| Plan viewer | legacy `:521` (plain `<img>`); v2 tool `:3005-3029` plus `mountPlanTool` `:3206-3325` (pinch, wheel, ± and reset, keyboard) | per-unit plan | empty state `plan_coming` "…לאחר קבלת תוכנית מכר מאושרת" (a waiting phrase) |
| Window view | legacy tab `:520-555`; `winStageInit` `:1422-1470`; `winCam` `:1406-1421` (FreeCamera at `floor×fh+1.6`, pitch 86 adjustable 35-90); `winLook` ±30° `:1471-1476`; fullscreen `:1480-1511`; big-map window `winView` `:1515-1545` (on `#nlpjx-map`, looks 700 m ahead and draws the cone); v2 dialog `mountWindowViewport` `:3816-4017` (drag, arrows ±15°, ±30° buttons; **360° slow orbit when the bearing is unknown** `:3829-3840,3927-3940`) | satellite-streets-v12, sky, Mapbox building extrusions `#d8d2c4` | legacy **invents west (270°)** when `dir` is unknown (`:1408,1429,1452,1473,1519`); `winview_note` claims "גובה הקומה והכיוון אמיתיים" (`i18n.js:95`) |
| Surrounding buildings in the view | `:1437-1442`, `:3910-3923` | only anonymous grey extrusions and the base style's street and place labels; the map is `interactive:false` | **neighbouring buildings are neither clickable nor named**. The only named surroundings are the landmark ring (below) and the area map's project price chips (`inc/project-experience.php:470-499`: popups that link to each project's page, POIs, purple future plans) |
| Per-unit cone on the area map | `showViewCone` `:1318-1335` (150px terracotta SVG marker, `rotationAlignment:"map"`); `easeMapToUnitView` `:1336-1352` (bearing ease over 900ms; without a bearing it only recentres at zoom 15.2); late map `:1354-1357`; map adopted under the theater `:1270-1280`; model orbit → map bearing `:1283-1296` | a press turns the map to what the apartment faces | **frozen**; no fly-in and no named targets |
| Landmark ring ("beam v2") | landmarks `:1702-1747` (true bearing and distance); panel beam `:1749-1821` plus `mountBeamScene` `:1847-1961` (zoom 15.9, pitch 52, `nl-bld-3d`, view-up); v2 beam `:2079-2160` | names what lies within ±26° of the window, with distances | the gold mini-beam was removed from the unit screen by owner order on 13.8 (`:2252-2254`) |
| 360° | interior panoramas through Pannellum `:1068-1092` (`project_interior_panoramas`); the 360° window orbit above; Aurelia per-unit tour at `?aurelia_tour=<id>` (`repo:scripts/aurelia/snippet_experience.php:93-148`, 3 room hotspots, noindex) | – | Rainbow has no panoramas |
| Interior tour | `interiorTour` `:953-973` (tour_url > panoramas > the project's own walk > per-unit `interior_url` walk `:966-969` > the standard default walk); default walk `:984-1057`; iframe tour `:1058-1067`; walk-inside `fpRooms/fpMarkup` `:1362-1400` plus `inc/interior-fp.php:25-156` | Rainbow: a 2-interior unit walk and 12 standard images | walk-inside falls back to **4 rooms and 85 m²** (`:1363-1364`) |
| Cutaway | – | **does not exist anywhere** (0 grep hits; v1 row 15 "רכיב ליבה חסר") | – |
| Studio | `studio.js` (SI 1918 clearances `:5-6`, notes per unit in key `nlstudio:<project>:<unit>` `:45`, hand-off to rfp `:310`, the "studio-video-call" lead `:314`); `openStudio` `:4143-4150`; dock `:409`; v2 iframe `/tour/designer/` `designerToolUrl` `:2783-2807` | per-unit furnishing that joins the offer request | – |
| Facilities | `inc/facility-chips.php:77-173` (chips → `/premium/?fac=`) | labels only | no "tap the pool, see the pool" (v1 R10-007 red) |
| Sun path and compass | sundial slider `:404-411`; `sunPos/applyLight/updateSunMark` `:744-809` (exposure, colour grade, sun marker, sunlit facades); `sunHours` `:1302-1314`; orientation pins `:377-382`; compass rose and 22.5° detents in `mv-ux.js:1-16`; the beam's N tick `:1779-1781` | equinox geometry at the project's latitude | geometric only; buildings cast no shade |
| Share and deep link `?unit=` | read `:19`; boot selection `:1254-1257`; `deeplink()` `:4354-4359`; share `:4250-4254`; per-unit WhatsApp link `:505-509`; favourites `:4218-4230`; compare `:4231-4243` (TOPSIS `:1151-1172`; v2 tool `:2954-3000`) | reload opens the same apartment | deep link opens with an empty top (HAD-208, still open in the fleet) |
| Co-tour | `:684-737` (host or join, broadcast every 1.6s: unit, orbit, light, sun, filter, view); button `:410`; REST `inc/cotour.php:21-57` (room kept 5 min) | a shared 3D view | the server whitelist drops the sun minute `s` (`inc/cotour.php` keeps p/u/o/l/f/v); no voice or video |
| Lead with the unit id | legacy form `onSubmit` `:4300-4351` (unit, floor, rooms, m², direction, status, consent); **shows success even when the send fails** `:4347-4349`; v2 contact tool `:3443-3467` (`source:"showroom_unit_journey_v2"`, card_id, unit, direction enum, consent text; strict `ok:true` `:3482`); rfp `buyflow.js:234-261` (unit plus the studio export `:246`, then `/nadlan/v1/rfp` `:258-261`) | the lead knows the apartment | owner and Brokers-Law limits (engine-journey §4) |
| The payload's `concept` flag | `inc/showroom-engine.php:264` | – | never used; `config.demo` is hard-coded false (`:386`) |

---

## 3. The canonical project-page recipe, as one ordered checklist

**Merged from:**
- **V1**: `repo:docs/playbooks/3d-project-page-checklist.md`, 31 rows.
- **V2**: `repo:docs/playbooks/master-project-checklist-v2.md`, 20 sections and R01-R17.
- **AUR**: the Aurelia package: `pkg:03-DOCS/01-MASTER-PAGE-RECIPE.md`, `02-PLACEMENT-AND-SPACING-SPEC.md`, `12-UNIT-SELECTION-SCIENTIFIC-SPEC.md`, `01-DEMO-LAB/data/page-sequence.json`, `master-checklist.json` (138 checks) and `unit-selection-audit.json` (67 checks).
- **EIN**: `assets/flagship-v3/contracts/registry.json`, the "Spatial Decision Room".
- **FSR**: `repo:docs/playbooks/flagship-showroom-recipe.md`.
- **SEO skill**: `repo:handoff/codex/2026-06-23-source-context/skills/skills__skill-project-page-seo-and-assembly.md`.
- **CLAUDE.md**: the iron laws.

**Verify codes:**
- **VS**: raw view-source GET and grep.
- **REST**: meta check.
- **DOM**: built-in browser DOM check.
- **EYES**: a real screenshot, looked at, 📱390 and 🖥1280 (1440 for AUR).
- **E2E**: pressed end to end, result seen.
- **AUD**: `tools/source_audit.py` snapshot plus diff.

### 3.A Rules that apply to every row
| # | Rule | Sources | Verify |
|---|---|---|---|
| A1 | **Blacklist = 0**: "בהמתנה לחומרי היזם", "יחליף אותו עם קבלתו", "בבדיקה מול היזם", "יוצגו עם קבלת נתונים", "תוכנית תתווסף", "טרם התקבלו", "מחכים ליזם", "אין שרטוטים", "0 חדרים", "כיוון בבדיקה", "· בקרוב", plus the language-DNA list, "אטלס" and slogans. Never write "מהיזם" in an empty state | V1 laws, V2 layer 0, mem | VS grep plus DOM text grep, in every state (a picked unit, open tools) |
| A2 | **Unknown = omitted.** An illustration fills the space, labelled "הדמיה להמחשה" in the caption, never on the image. It never becomes a price, stock, bearing or status. Zero values never render | V1, V2, FSR §2.1, EIN `unknown_values_must_remain_null` | DOM and EYES |
| A3 | **Evidence class on every green** (eyes or code). Nothing is done until controls were pressed in a real browser | CLAUDE.md iron law 1, V2, AUR | receipt |
| A4 | **Additive law:** classify every change as RETAINED, REUSED, WRAPPED, EXTENDED, SIMULATED, REPLACED or REMOVED. REMOVED needs the owner's word | V2 layer 0 | receipt |
| A5 | **Frozen:** the terracotta cone mechanism and engine.js internals. Build around them. The v2 freeze list also names Rainbow and DUO; the owner reopened Rainbow on 24.9 (mem) | CLAUDE.md iron law 2, V2 | diff |
| A6 | **One h1** (count after stripping style and comments). No em or en dashes. Plain buyer Hebrew, never tech or demo talk | V1, FSR §2.6-2.7, language-dna | VS and grep |
| A7 | **URL word law** for any new slug (`tools/gsc/url_word_audit.py`). No 301. No pagination | V2, CLAUDE.md iron law 9 | tool output |
| A8 | **The 5,000-word × 5-language article** is written in the owner's ChatGPT; the agent writes the brief | V2, FSR §2.8 | – |
| A9 | **Public-source audit** before and after every release. An unexplained diff is a finding | CLAUDE.md iron law 9a | AUD |
| A10 | **Legal:** Brokers Law, so no arranging viewings or relaying offers for third-party developers; review voice "לא מטעם היזם". Lead consent is an active checkbox that is sent and stored | mem, engine-journey §4 | E2E |
| A11 | **Mobile first:** the building shows in the first fold at 390; a card never covers or shrinks the building; 44px targets; no horizontal overflow at 320/360/390/430 | V1, R16, AUR | EYES |
| A12 | **Budgets:** GLB ≤1MB (a graded budget), page about 4MB, clean console after each tool, libraries loaded once, Mapbox lazy (it is billed per load) | V1 row 22, R05, R16 | DevTools and VS |
| A13 | **After every deploy:** spot-check Rainbow, H-Infinity and the home page | V2, CLAUDE.md iron law 7 | EYES |

### 3.B The page, in order: 30 rows
| # | Section and requirement | Sources | Verify |
|---|---|---|---|
| 1 | **Portal header**: logo, projects, guides, professionals, language, saved items. It never competes with the project's CTA | V2 §1, AUR seq 1 | VS |
| 2 | **Clickable breadcrumbs** (בית › פרויקטים › name) with the current item marked, plus exactly one `BreadcrumbList` JSON-LD. No city link (the city layer died 25.8). Visible on mobile | V1 row 3, V2 §2, R03-001/002, AUR seq 2 | VS (count JSON-LD); EYES 📱 |
| 3 | **Head:** a unique title of about 60 characters (brand + he/en + developer or place + value + the brand tail "\| נדלן"); a meta description with sourced or non-binding price only; one self canonical; full OG; JSON-LD that matches the visible text; no Ashira or placeholder in the source | V1 row 1, R02-001…008, SEO skill §2.3 | VS, AUD |
| 4 | **Hero:** one bilingual h1 ("Rainbow Tel Aviv - ריינבו תל אביב"), a truthful eyebrow, 2 facts that match the meta, a primary CTA (lead) and a secondary one ("לבחירת דירה", which scrolls to the picker), the building in the first fold, no black flash | V1 rows 2 and 4, V2 §3, R04-001…006, AUR seq 3, FSR §8 | VS h1=1; EYES first fold 📱🖥; press both CTAs |
| 5 | **Answer paragraph**, 4-7 lines, keywords first: every project name (he+en), the developer, the exact place, the status (permit, construction, estimated occupancy), the unit mix, a **real price range with its source and date**, and what you can do here. No disclaimer before it | V1 row 5, V2 §4, R13-001, AUR seq 4, CLAUDE.md iron law 4 | VS: the first `<p>` after the h1 holds each token |
| 6 | **A one-line non-affiliation notice after the lead** (Einstein order and FSR). The full disclaimer block goes last (row 28) | EIN `page_order`[2], FSR §9.2, V1 row 30 | VS position |
| 7 | **Progress:** planning, permit, construction and occupancy, with the current step, placed before the showroom and never sticky over the building | V2 §5, R03-003…007, AUR seq 5 | VS order; EYES 📱 |
| 8 | **Six quick facts:** location, floors, units, mix, price range, status, each matching the meta and sources | V2 §6, AUR seq 6 | REST vs DOM |
| 9 | **Showroom intro:** title, a one-line instruction, an availability count (only when real), reset | V2 §7, AUR seq 7 | EYES |
| 10 | **The stage:** model and inventory in one frame; a poster that matches the model; no empty stage; a default orbit per project (meta); rotate, zoom and reset; camera limits keep you out of the model; the facade fallback works; hotspots are 44px, spread and all tappable; filters appear only when data backs them and they mark the building; floor bands above 24 units | V1 rows 6-10, V2 §8, R05-001…012, R06-001…003, AUR seq 8 | EYES cold reload; drag; tap 3 hotspots on 📱 |
| 11 | **The selection contract:** `unit_id` is the only key. The chain is GLB anchor/mesh → hit → unit_id → inventory → card → plan → map cone → window view → tour → studio → lead. Tier A `UNIT_PICK__{id}`, Tier B surface resolver, Tier C projected hotspot. Tap ≤6px and ≤900ms selects; drag rotates; `touch-action: pan-y`; Enter or Space; up to 8 dots on desktop and 5 on mobile, plus the selected one; `stage_x/y` never at runtime; the card opens in place; a back-to-building control; no automatic fullscreen; **no cone without a verified bearing** | V2 layer 3, AUR spec 12, SEL-DATA/GLB/HIT/GEST/PROJ/SYNC/UX/A11Y/PERF (67), EIN `selection_behavior` | the 67 SEL checks (digest in §3.C) |
| 12 | **The unit card.** 📱 low, compact, no expanded state, the building's height identical before and after, pixel for pixel. 🖥 a fixed side panel. It shows floor and direction in words, rooms, m², balcony, price (a real range or omitted) and the plan, view, tour and studio doors; each icon opens the same tool as the door above it; a quick lead | V1 row 11 (owner 20.8), V2 §9, R06-004…009, AUR seq 9, owner decision 26.8 #3 | EYES before and after diff; press every icon |
| 13 | **The plan**, per unit: the house style (ink and watercolour); fullscreen with zoom; the caption "תשריט אילוסטרטיבי להמחשה", not on the image; a north arrow; openings; dimensions; area matching the card; download and share; a hand-off to the studio | V1 row 14, V2 §10, R07-001…008, AUR seq 10 | E2E each unit; blacklist 0 |
| 14 | **View, beam and map:** one project point; the unit's azimuth and floor height; **the cone turns on the one area map attached under the model**; names and distances of what lies in the cone; left and right turns; fullscreen; an unknown bearing gives an honest 360° from floor height with no "בבדיקה"; geo confidence `city` turns the window off | V1 rows 12, 13 and 24, V2 §11, R08-001…008, AUR seq 11, EIN `window_view`, FSR §8 | E2E press → EYES cone and view; drag; test the 360° fallback |
| 15 | **Interior tour:** the unit is preserved; room hotspots; a project's own set is tagged as its own, otherwise the labelled standard set | V1 row 16, V2 §12, R09-001…003, AUR seq 12 | E2E |
| 16 | **Cutaway**, from the unit: a 3D section of the type, then on to the studio | V1 row 15, V2 R09 addition | E2E (missing across the fleet) |
| 17 | **Facilities as places:** every facility opens an image, level, description, hours and accessibility, and sits on a real zone of the model; no icon that fails to open | V2 §13, R10-001…007, AUR seq 13, EIN governed scenes | E2E each |
| 18 | **Environment:** one map (never two) with price pins, POI layers with true counts, purple future plans, satellite and 3D; "כל מה שמסביב" groups with real content; no empty headings; no "(0)" layer on by default | V1 rows 24-25, V2 §14, R11-001…007, AUR seq 14 | EYES; toggle every layer |
| 19 | **Studio:** opens from the card; drag furniture; choices saved per unit and attached to the request | V1 rows 17-18, V2 §15, R09-004…009, R12, AUR seq 15 | E2E |
| 20 | **Communication:** a payload with unit_id, card_id and consent; success shown only on `ok:true`; the WhatsApp pill with `data-nl-whatsapp`; co-tour host and join keep the room and the unit; no demo lead to a live contact; review voice | V1 rows 18 and 20, V2 §16, R14-001…009, AUR seq 16, EIN `lead_contract` | E2E test lead plus `lead_e2e` in health |
| 21 | **Real price and deals:** the real deal range, a ₪/m² chip, a deals table (date, rooms, m², price, ₪/m²) with a named source; high on the page | V1 row 23, R13-005, teardown §4.1 | each number traced to its source |
| 22 | **Gallery:** 8 or more house-style assets, captioned "הדמיה להמחשה" | V1 row 26 | count |
| 23 | **The article:** 5,000+ words, woven through, with a table of contents; it comes after the decision tools | V1 row 27, V2 §17, R13-002/003/006 | word count |
| 24 | **Entities and a fact table:** developer, architect, contractor and consultants, each linked, plus an updated date | V2 §18, R13-004 | VS links |
| 25 | **FAQ:** one visible accordion and **exactly one** `FAQPage` JSON-LD from the same data | V1 row 28, R13-007, SEO skill §1.4 | VS count = 1 |
| 26 | **Money and the wider world:** a monthly estimate labelled non-binding; professionals, calculators, guides | V1 row 29 | 5 links return 200 |
| 27 | **Final step:** a unit summary before the footer. The AUR "final appointment" is a scheduler, which the owner's 31.8 order removed in review mode, so it needs his word | V2 §20, AUR seq 20, mem | E2E |
| 28 | **Disclaimers last**, small ("אתר עצמאי", direct contact with the developer) | V1 row 30 | VS position |
| 29 | **Five languages:** a sibling per language (`-en/-fr/-ru/-ar`), two-way hreflang plus x-default, a real switcher; the stage and labels translated; no Hebrew leaking in | V1 row 31, R15-001…007 | VS on 4 siblings |
| 30 | **Admin lights:** each light shows a fact, its evidence and a link to the field, and never blocks; a source snapshot with its SHA; the recipe version | V2 layer 4, R17-001…008, AUR `03-CHECKLIST-MECHANISM` | admin |

**Layout tokens** (AUR `page-sequence.json` and `02-PLACEMENT`):
- an 8px grid and 44px controls;
- desktop showroom columns of 250px / 1fr / 340px;
- a mobile stage of clamp(540px, 76vh, 690px), with the card flowing under it;
- a 780px text measure.

**Einstein journey:** understand → locate → explore → verify → compare → collaborate → inquire → return.

**Evidence states:** verified, measured, planned, simulated, illustrative, unknown.

**Exit gate** (V1 and V2): eyes screenshots of every core row on 🖥 and 📱; blacklist grep = 0; a clean console; the fleet spot-check; every deviation logged as a receipt row with its reason.

### 3.C The 67 unit-selection checks, in groups (`pkg:01-DEMO-LAB/data/unit-selection-audit.json`)
| Group | Checks | What they cover |
|---|---|---|
| Identity and contract | SEL-DATA-001…006 | a stable unique id; one project; floor, line, direction and azimuth present; `plan_id` exists; price and status travel with the unit; `stage_x/y` kept for migration only |
| GLB and coordinates | SEL-GLB-001…008 | SHA; axes are metres with Y up, X east and −Z north; floor pitch taken from the model; anchors, extras and bounds; unit normals; `UNIT_PICK` |
| Hit and resolve | SEL-HIT-001…008 | a surface hit; a floor band; normal dot; distance; exactly one unit or an explicit ambiguity; tap on an unmarked floor; trees and ground never pickable |
| Gesture | SEL-GEST-001…006 | 6px and 900ms; drag never selects; `pan-y`; multi-touch |
| Projection and occlusion | SEL-PROJ-001…010 | `queryHotspot`; no stored top/left; hidden behind the camera, off frame or behind the shell; updates on each camera change and resize; the selected dot first; no hundreds of dots; 44px, 48px on mobile |
| unit_id sync | SEL-SYNC-001…012 | one event; the URL; inventory; card; plan; Mapbox azimuth; the window view; the tour; the studio; the lead; round trips; the deep link |
| UX | SEL-UX-001…006 | the building never moves when the card opens; no automatic camera turn; a "turn to the facade" button; the mobile card never covers the building |
| Accessibility | SEL-A11Y-001…005 | names; focus; Enter and Space; a calm live region; reduced motion |
| Performance and proof | SEL-PERF-001…006 | the GLB budget; rAF; the raycast limited to the pick root; the fingerprint; the light never blocks; the 1440/390/320 replay |

---

## 4. The Einstein Tower prototype: what only it has, and what Echo City means
This comes from a read-only pass over `C:\Users\777\nad-lan\einstein-tower-prototype`, run by a subagent and summarised here.

**Paths used below:**
- `R`: the repo root.
- `FH`: `R\final-handoff-2026-08-15\prototype-repository\`.
- `SRC`: `FH\source\repository\`.
- `PL`: `SRC\plugins\nadlan-config\`.

**Code identity:**
- The nad-lan copies of `flagship-surface.php`, `flagship-integrations.js` and `flagship-playground.js` equal `R\releases\1.72.211\patched-source\`, ignoring line endings.
- `flagship.js`, `flagship-viewer.js`, `flagship-cotour.js`, `inc/flagship-cotour.php` and `registry.json` are byte-identical to `PL`.

### 4.1 What the repo is and where it stands
- **What it holds:**
  - the WIP snapshot for candidate 1.72.209 (status HOLD);
  - the final handoff of 1.72.210 (`FH`: docs 00-29, RUNBOOK, POSTMORTEM, skills, template contracts, a 62-file WordPress overlay);
  - receipts for 1.72.211 and later, the flip, the Einstein lab, the EcoCity war room, SEO waves and a new-machine kit.
- **History:** 1.72.211 went live on 16.8. The same day, the **flip** (`R\releases\flip-2026-08-16\RECEIPT.md:3-12`, commit 359886a) moved Einstein 4867 off flagship-v3 and back to the fleet engine, and dropped the film. On 30.8 everything went to review mode.
- **Today:** health reports `flagship_v3.public_release_enabled:false`. The live Einstein HTML has no v3 surface, no engine and no `model-viewer` (HTML). The v3 runtime sits in nad-lan too, **dormant**: it runs only when a post has `project_surface_version = flagship-v3` (`inc/flagship-surface.php:243-250`), and the flip deleted that meta.
- **Stale pointers:** the "Current state pointers" in `nad-lan\CLAUDE.md` and `R\README-NEXT-SESSION.md` ("SUPERSEDED 2026-08-16") are out of date.

### 4.2 What the Spatial Decision Room has that the fleet engine lacks
It lives in both repos but runs nowhere today.

| Feature | Where | What it does |
|---|---|---|
| Contract-enforced page | `registry.json:26-37`; enforced at `flagship-surface.php:1855-1910`; rendered at `:2633-2680` (h1 2640, lead 2641, notice 2642, model 2644, map 2664, CTAs 2665, tools 2666, film 2673, article 2674) | Journey understand → return; a 9-slot order; a CTA pixel budget (`FH\docs\18:49-68`: 1136/1688/640/1600 px) |
| Shareable state | `flagship.js:6-11,217-240,428-506,1022-1027,515-613,1088-1100` | The deep-link parameter `nlfs` carries selectedEntity, model, map and media; restore is validated and all-or-nothing, with rollback; a deep link never opens deeper media; share falls back from Web Share to the clipboard to manual; a public API `window.NadlanFlagshipV3` |
| Six evidence states | `registry.json:44`; UI at `flagship-surface.php:2658-2662,2209-2229`; `flagship.js:255-301` | Every selection and scene shows its state (verified, measured, planned, simulated, illustrative, unknown); the four Einstein scenes are all "illustrative" |
| Selection laws | `registry.json:45-52`; `flagship-surface.php:2638`; `flagship.js:302-348,722-734,756`; `flagship-integrations.js:37-40,232-278,1141-1151` | The card opens in place; "back to building" restores **the map camera from before the selection**; the cone only with a verified bearing; the map pans only to cited coordinates, otherwise `unavailable-no-source`; hotspots projected every frame and disabled until the model is ready |
| Governed scenes on the model | `registry.json:286-402`; validation `flagship-surface.php:1111-1361`; render `:2231-2298` | 4 WebP scenes in 3 hotspot groups, each with a model position, a normal and a zone vs exact-point confidence (for example 0.68 / 0.18) |
| Calibration | `registry.json:225-252`; `flagship-surface.php:859-860,920-923`; `SRC\assets\projects\einstein-tower\model-spec.json:17-20,57,94-200` | HD model (2.42 MB, 39,912 triangles), LOD (32 KB) and a poster, loaded in that order; `north_degrees` must be 0; `real_world_orientation_calibrated:false` and a list of prohibited inferences. **The model spec says +Z is north, while engine.js assumes −Z** (§1.3 axis note) |
| Window view | `flagship-integrations.js:322-626` | FreeCamera at the illustrative tower height of 93.22 m; pitch 62-85; drag, arrow keys and Home; **−45°, +45° and 360° buttons**; one full turn in 30 s, paused when hidden or under reduced motion; an honest "unavailable" state with no token; only the Einstein point is labelled, and neighbouring buildings are anonymous and cannot be clicked |
| Attached area map | `flagship-integrations.js:1022-1118,222,305-315` | Adopts the existing `#nlpjx-map` and gives it back on teardown; readiness means style and tiles loaded; correlation states idle / panned / cone / unavailable-no-source / unavailable-no-bearing |
| Co-tour v3 | `inc/flagship-cotour.php:1-8,334-359,550-593,907-958`; `flagship-cotour.js:178-318` | A `__Host-` cookie; a 6-byte room code; 600 s; 1 host and 1 follower; **the follower restores only after consent**; no audio or video |
| Lead contract | `registry.json:111-128`; `flagship-surface.php:2555-2571`; `flagship-integrations.js:685-738` | Consent, a honeypot, `ok:true` only; retention and rights fields; the unit fields are always sent empty |
| Release and asset governance | `flagship-surface.php:358-809,2808-2891`; `registry.json:141-224` | Hashed private and public assets, extensionless aliases, fail-closed live gates (article SHA, marker, deployment id, token, lead pipeline) |
| Decision content | `flagship-surface.php:1364-1517,2300-2363` | Current and future context layers; sea distance measured as a straight line to the Tel Baruch beach polygon (975 m, source S017); a buyer-decision block; capabilities that lack data show as text, never as dead chips |

**Only in the prototype repo:**
- The **template factory** (`SRC\assets\flagship-template\contracts\`: 16 schemas; 5 verticals in `vertical-capability-profiles.json`; `bootstrap_project.py`, which emits six HOLD artifacts).
- The skills (`FH\skills\`):
  - `build-…` has **15 non-skippable gates**: canonical identity, source ledger, data readiness, media integrity, state invariants, page order, no teleport, evidence lane, mobile and a11y, failure honesty, inquiry minimisation, collaboration consent, performance, documentation, independent acceptance.
  - `audit-…` has a 14-row matrix, runs real Chrome at 320×568, 390×844, 568×320 and 1280×800, and says "never lower a threshold".
  - `release-…` has 11 fail-closed gates.
- The model generator and validator; the evidence registers; docs 00-29, including a Building Lifecycle roadmap (doc 29); `tools\tour-generator.py` and `refresh-narration.py`.
- **The verified-unit contract.** It is the only place in either repo that says what a unit must carry before a per-unit cone may be drawn:
  - the unit: `verified:true`, `id`, an integer `floor`, `bearing_state:"verified"`, `bearing` in 0-360 and 1 to 32 `bearing_source_ids`;
  - the project: `production_enabled:true`, `inventory_state:"verified"` and `verified_unit_ids[]` (`flagship-integrations.js:26-40,184-194,1119-1129`; `registry.json:129-134`);
  - the new-residential profile: floor, unit and viewpoint entities; inventory needs `unit_id, availability, valid_as_of`; the window view needs `unit_id, floor, height_m, verified_bearing` (`vertical-capability-profiles.json:34-62`).

**What it does not have:**
- **Apartments.** v3 enforces zero inventory: a non-empty `project_3d_units` gives the error `zero_inventory_required` (`flagship-surface.php:826-829`).
- **Sun simulation.** It is off, because orientation is not calibrated (`flagship-viewer.js:5-14,279-286`).
- **Plan images.**
- Since the flip, the live unit layer is 28 `floor-NN` stand-ins. Their facings come from a 137.5° golden angle, with rooms and m² at 0 (`R\releases\flip-2026-08-16\seed212/214/215.py`). The CEO report calls this "a fake inventory" (`R\docs\reports\nadlan-3d-ceo-report-2026-08-19.md:767`).
- The same report's thesis: "You can demo a working apartment picker tomorrow. It is not a BIM building" (`:11`).

### 4.3 Echo City
**Echo City is EcoCity**, the developer the owner ordered taken down on 30.8 (mem `nadlan-ecocity-takedown-order.md`).
- `R\ECHO-CITY-BOOTSTRAP.md:20` names the client "EcoCity (אקו סיטי, ecocity.co.il)". `:27` sets out "a branded Echo City war room".
- The night-1 receipt lists posts 6693, 6694 and 6695, `/echo-city/` and `ecocity-tour.html`, which are exactly what the takedown drafted or switched off (snippet 603 "x-echo-city").

**Purpose:** a pitch cockpit for EcoCity's CEO, in phases P0-P5:
- a recon of 22 assets;
- voice;
- a helicopter tour over their buildings;
- 1-2 flagship models;
- a hub at `/echo-city/`;
- a feed for their real materials.

It reused the Einstein lab standard, and the Einstein backlog was parked for it.

**Backlog** (`R\ECHO-CITY-BACKLOG.md`): a mobile peek card (done); flagships opening the tour; depth badges; owner-editable narration; deals data (the government API is blocked by a captcha); real building fronts (17 of 20); a POI layer; dual voice; a branded tour generator; a site anchor. Also recap items: a voice-clone rig, an EcoCity brand skin, GLB improvements, GSC indexing and others.

**Status:** the last commit is c689430 (18.8). **The repo does not record the takedown** and still holds EcoCity material:
- a plan index of 88 URLs;
- a copy of the tour HTML;
- config JSONs.

`tools\tour-generator.py:20` extracts its template from the offline `ecocity-tour.html`. Under the 30.8 order none of this may be republished.

**Reusable, and not EcoCity-specific:** the **P5 real-inventory intake format** (`docs\echo-city\P5-MATERIALS-FEED.md:5,16,18`):
- apartment number, floor, rooms, area, balcony or garden, facing, status, price;
- mapped to `project_3d_units` with long-form directions;
- `unit.plan` per apartment type.

### 4.4 Hygiene findings in that repo
- **A public Mapbox `pk.` token URL** sits inside `R\releases\1.72.211\evidence\matrix.json` (`failed_requests`), although `R\docs\05-MAPBOX-WINDOW-VIEW.md:27` promises the token is never serialised. It is a public-class key, not reproduced here, but it breaks the stated rule.
- **Two 1.72.211 QA checks pass without proving their claim:**
  - `ctas_active` passes on "active>0" and records the CTA at 2,766 px, never compared with the 1,600 px limit;
  - `scene_opens_with_image` passes with `shownImgs:0` (`qa211-live.mjs:110-112,147-149`).

### 4.5 What to take from it for Rainbow
Take these patterns: the state and deep-link pattern (`nlfs`, all-or-nothing restore); "back to building" that restores the previous map camera; the in-place card; the evidence-state chip; the window view's −45°, +45° and 360° controls; honest "unavailable" states; the CTA pixel budget; the audit viewports.

Its **verified-unit contract** also sets the bar for per-unit cones (§6.6). The owner has granted a direction demo before: `OWNER-2026-08-13-DIRECTION-DEMO` in the registry's `owner_decision_ids`.

---

## 5. Gaps: the new Rainbow page against §2 and §3
The page was read on live 1.72.256 (HTML, code). The site moved to 1.72.257 before this pass ended; that release changed the professionals' recommendations, not Rainbow.

**New files:**
- `assets/project-stage/rainbow/stage.js` (2,583 lines)
- `assets/project-stage/bridge.js`
- `inc/project-stage.php`

**How the page is put together:** `project-stage.php:192-223` composes it on the finished HTML, in this order: h1, lead, stage with rail, then the view and the area map side by side. It runs only in review mode (`:70`) and only on the Hebrew slug (`:38`). **The -en sibling has no `#nlps`** (HTML).

### 5.1 Against the engine's unit capabilities (§2)
| # | Capability | Old engine | New stage today | Gap |
|---|---|---|---|---|
| 1 | Pick an **apartment** | 6 units with ids, rooms, m², balcony, dir and plan | floor 1-40 (`hitTower` `stage.js:706-714`), then any facing on the ring (`:871-890`); events `nl:floor` and `nl:facing` (`:10-14`) | **no unit id and no apartment**; the payload is not loaded at all |
| 2 | Marks on the model | per-unit hotspots, status colours, recommended pulse, filter dimming, sunlit ring | floor band highlight, ring with 8 compass ticks, facing arrow (`:765-813`) | no per-unit mark, no legend |
| 3 | Inventory list and filters | cards, filter chips with counts, bands | none | missing (the list-to-model sync of AUR seq 8) |
| 4 | Unit card | the full legacy panel (§2) | label "קומה N", the project-wide line "בפרויקט דירות 2 עד 5 חדרים, לפי פרסומי השיווק" (`:22-40`, `:984-994`), the facing words, a CTA | no rooms, m², balcony, plan or tour doors |
| 5 | Plan | 6/6 plans (`plan-3br/4br/5br/penthouse/boutique.svg`, live 200) plus the v2 zoom tool | none | the plans exist and go unused (they need restyling, §1.4) |
| 6 | Window view | FreeCamera at floor height, drag, ±30°, fullscreen, keyboard, 360° fallback | `bridge.js:137-188` (the same camera, drag only) | no turn buttons, fullscreen, keyboard or 360°; a different height model (§5.3) |
| 7 | Per-unit cone | `showViewCone` and `easeMapToUnitView` from `dir` | `showBeam` `bridge.js:198-225` (the same wedge; the map turns and centres 450 m ahead, zoom 14.3, pitch 0) | works per facing but **not per unit** |
| 8 | Named targets | a 6-landmark ring with in-cone hits and distances | 6 sector phrases ("לכיוון הים", `project-stage.php:47-54`) | no names with distances; the old "הים" landmark (≈1.1 km at 270°) disagrees with the stage's measured shore (713 m at 287°) |
| 9 | Sun | time slider, sunlit facades, sun hours per unit, compass rose | 2 light presets (sunset, noon) and compass ticks | no time slider, no sun hours |
| 10 | Interior and 360° | a 2-interior walk (unit-16-w, penthouse), the standard walk, walk-inside | none | missing |
| 11 | Cutaway | none | none | missing on both (V1 row 15) |
| 12 | Studio | studio.js per unit | none | missing |
| 13 | Facilities | chips only | pools and courtyard modelled, not tappable | missing (R10) |
| 14 | Share and `?unit=` | read, write and reload | **no URL state** (0 hits for `history.`/`URLSearchParams` besides the QA flag `nlps3d`) | missing |
| 15 | Co-tour | host and join | none | missing |
| 16 | Lead with unit_id | form, v2 contact, rfp | a WhatsApp link with the floor and facing words (`bridge.js:82-87,127-133`); GA events only | **no stored lead, no consent, no card_id** |
| 17 | Compare, favourites, recent | yes | none | missing |
| 18 | Boutique buildings | unit-boutique-07 (hotspot `-42 25 24`) | 6 blocks drawn but **not pickable**: only `towerProxy` is raycast (`:2489-2494`) | missing |
| 19 | Languages | 5 (with gaps) | Hebrew only, HE slug only | missing |

### 5.2 Against the recipe (§3), on the live page (HTML)
| Row | Live now | Status |
|---|---|---|
| 2 breadcrumbs | `nav.nlptop` "בית › פרויקטים › Rainbow Tel Aviv - ריינבו תל אביב", clickable; one BreadcrumbList | pass (code) |
| 3 head | title "ריינבו תל אביב Rainbow - ישראל קנדה, שדה דב \| מחירים ודירות \| נדלן"; canonical; ApartmentComplex + AggregateOffer | pass (code); JSON-LD vs text not checked |
| 4 hero | the h1 "ריינבו תל אביב Rainbow Tel Aviv" is visible and bilingual, with the kicker "ישראל קנדה · רובע שדה דב, צפון תל אביב" (`project-stage.php:160-166`) | **no facts, no CTAs**. The building appears in the stage right after the lead; whether it falls inside the first fold at 390 is unverified |
| 5 answer paragraph | "Rainbow Tel Aviv הוא אחד מפרויקטי הדגל של שדה דב. העמוד הזה מרכז מידע ציבורי…" | **fail**: no developer, status, mix, price or source. The sourced facts exist (§1.4: 459 units, 39 floors + 6×8, 270 sold/189 remaining, 80,300 ₪/m² incl. VAT, annual report 2025) |
| 6 notice | `nl-projnotice` "אתר עצמאי…" appears after the stage, map and prices, before the article | partial (EIN wants it right after the lead) |
| 7 progress | `nlms` "איפה הפרויקט עומד" comes after the map and prices | **order fail** |
| 8 quick facts | only inside the article ("תמונת נתונים קצרה") | **missing before the showroom** |
| 10-12 stage, selection, card | see §5.1 | **the core gap** |
| 14 view, beam, map | the view and the map sit side by side under the stage | partial (per facing, not per unit) |
| 21 real price | `nlcp-projctx`: "בפרויקט, לפי היזם 76,000 ₪ למ"ר", from `inc/catalog-plus.php:535` and `catalog-plus-map.php:171`. Both files are untracked in git on this branch, although the site runs them. The meta's own note says the 76,000 is a web/Madlan estimate. The annual report's 80,300 incl. VAT is not used | **mislabelled figure** (a breach of the honesty law) |
| 25 FAQ | **0 FAQPage** (review mode gates it off, `inc/schema.php:128`) but **two** visible H2 "שאלות נפוצות על Rainbow Tel Aviv" (the SEO guide and the article) | **fail** |
| 28 disclaimers | `nl-legal` in the footer; the notice mid-page | partial |
| 29 languages | hreflang he/en/fr/ru/ar + x-default (pass); the stage is HE only | partial |
| numbers | `num_units` 480 (official 459); tower 40 floors (`stage.js:97`, official 39, old engine 38); blocks with 9 floors (`:105-112`, official 8) | **fix the data** |
| CTA within two screens | no in-flow CTA before the stage; the stage CTA is hidden until a floor is picked (`nlps-view__cta hidden`); only the floating `#nlcta` pill | likely fail (confirm by eye) |

### 5.3 Three height models for one floor (code)
Eye height in metres for Rainbow's unit floors:

| Floor | Engine `winCam` (floor × 3.05 + 1.6) | New stage `floorEyeHeight` (7.2 + (n−1)×3.2 + 1.6) | July view config (8 + 4 + (n−1)×3.05 + 1.55) |
|---|---|---|---|
| 8 | 26.0 | 31.2 | 34.9 |
| 16 | 50.4 | 56.8 | 59.3 |
| 24 | 74.8 | 82.4 | 83.7 |
| 31 | 96.15 | 104.8 | 105.05 |
| 38 | 117.5 | 127.2 | 126.4 |

The meta `project_3d_floor_height_m` is "0" and `project_floors` is empty (REST). Pick one source and write it to the meta.

---

## 6. Proposal: put apartments into the new stage

### 6.1 The data: reuse the payload, add nothing invented
- **Source:** `project_3d_units` (REST, identical to the 24.8 engine payload).
- **Delivery:** `project-stage.php` adds a whitelisted `units` array to the existing `data-cfg` (`:147-158`): `id, floor, rooms, sqm, balcony, dir, label, plan, interior_url, building`.
- **Never shipped to the stage:** `status`, `availability`, `note`, `market_note`, `source_note`, `price*` and `view_note`. They are demo or waiting phrases.
- **Derived, not stored:** `azimuth = DIR_BEARING[dirKey(dir)]`, the same tables as `engine.js:46-51` and `:1297`. For Rainbow that gives 225, 270, 315, 135, 270 and 270.
- **Meta to fix first:** `project_floors = 39`, `project_3d_floor_height_m` set to one value, `num_units = 459`.
- **The stage reads floors and floor height from config** instead of `TOWER.floors: 40` and `fh: 3.2` (`stage.js:97`). The blocks go to 8 floors (`:105-112`).

### 6.2 The geometry: a unit is a floor plus an arc of the ring
- **The ring is already there:** 1,440 samples, each with a facade point, a ring point, a world outward normal and `sb`, the normal's scene bearing (`stage.js:725-742`). `trueBearing(sb) = sb + bearingOffset` (`:718-720`).
- **The arc:** `arc(u) = { i : angleDiff(trueBearing(ring[i].sb), u.azimuth) ≤ u.half }`.
  - `u.half` defaults to 22.5°, one of eight 45° lines.
  - It narrows only when two units share a floor and a direction.
  - The ellipse's normal bearing is monotonic, so each arc is one contiguous run of samples.
- **The anchor:** `i0 = idxForSceneBearing(u.azimuth − offset)` (`:745-753`).
  - position = `(ring[i0].fx, floorLevel(f) + fh/2, ring[i0].fz)`, the facade at mid-floor;
  - normal = `(ring[i0].nx, 0, ring[i0].nz)`;
  - the facing shown is `u.azimuth` itself, said as words through the page's sectors (bridge `facingWords`, `bridge.js:49-56`), never as degrees.
- **Rainbow's five tower units** give these arcs, with the words from `project-stage.php:47-54`:
  - unit-08-sw: 202.5-247.5° ("לכיוון הצפון הישן").
  - unit-16-w: 247.5-292.5° ("לכיוון הים").
  - unit-24-nw: 292.5-337.5° ("לכיוון הים").
  - unit-31-se: 112.5-157.5° ("לכיוון פארק הירקון").
  - unit-38-penthouse: 247.5-292.5° ("לכיוון הים").
- **unit-boutique-07** needs pickable block proxies with their own rings (phase 2). The stage's six blocks ring the courtyard to the north, east and south, and the tower takes the west side (`BLOCKS`, `:105-112`). So a west-facing boutique unit has no obvious host block. Place it only once the data or the block geometry is fixed, and never move its facing silently.

### 6.3 Selection: Tier B plus Tier C inside three.js (Aurelia's rules)
- **Tier B, surface resolver.** On a tap (≤6px and ≤600ms today in `:903-908`; AUR wants 900ms):
  1. `hitTower` gives floor f and the hit point.
  2. `nearestIdx(hit.x, hit.z, true)` (`:754-763`) gives the ring sample, and so the bearing b.
  3. The candidates are the units on floor f whose arc holds b.
  4. One candidate selects that unit.
  5. None keeps today's floor-then-facing behaviour.
  6. Two with nearly equal scores show a small line chooser, never a guess (AUR spec §thresholds).
- **Tier C, projected dots.** Each honest unit gets a 44px DOM button placed each frame through `projectToStage(anchor)` (`:1104-1107`, the same path as the label and chip).
  - It hides when `normal · (camera − anchor) ≤ 0`.
  - It hides when a ray from the camera hits `towerProxy` before the anchor (occlusion).
  - At most 8 on desktop and 5 on mobile, plus the selected one.
  - It is focusable, with Enter or Space, and aria "דירת 4 חדרים, קומה 16, לכיוון הים".
- **Highlight:** a thicker tube along the arc on the floor's ring, with the existing arrow at `i0` (`placeArrow`, `:808-813`). No status colours, because the statuses are demo.
- **Keyboard:** ArrowUp and ArrowDown change the floor (as today), ArrowLeft and ArrowRight step through that floor's units, then free facings.

### 6.4 The card and its tools: reuse the stage label
- **Title:** "דירת 4 חדרים · קומה 16".
- **Line:** "112 מ״ר · מרפסת 14 מ״ר".
- **Facing:** words.
- **Chip:** "דירה לדוגמה, להמחשה".
- **Doors:**
  - **Plan:** a `<dialog>` with pinch, wheel and ± zoom, ported from `mountPlanTool` (`engine.js:3206-3325`). Captioned "תשריט להמחשה". The SVGs still need north arrows and the house style, and the on-image English must come off.
  - **The view from the window:** the existing `showView`.
  - **On the map:** the existing `showBeam`.
  - **Inside the apartment:** only when `interior_url` exists (unit-16-w and the penthouse), labelled "הדמיה להמחשה".
  - **"לקבלת תוכניות ומחירים":** the existing WhatsApp link, with the unit label added to the text. Optionally, a consented POST to `/wp-json/nadlan/v1/lead` in the v2 shape (`engine.js:3443-3467`: `source:"project_stage_unit"`, `card_id:4464`, `unit`, `floor`, `rooms`, `sqm`, `direction`, `consent_text`, strict `ok:true`), in review voice ("עונים עצמאית, לא מטעם היזם"). Any routing to the developer waits for the owner's legal word.
- **The inventory strip under the stage:** a short list of the units (floor, rooms, m², facing words) that stays in sync with the stage both ways. Show rooms filters only because this data backs them.

### 6.5 The map, the view and the URL: bridge.js
- **The stage emits `nl:unit`** with `{unitId, floor, heightM, bearing: azimuth, rooms, sqm, label, plan}`. It keeps emitting `nl:floor` and `nl:facing` so nothing breaks.
- **bridge.js on `nl:unit`:**
  - calls `showView({floor, heightM, bearing})` and `showBeam(azimuth)`, which exist today (`:110-125`, `:147-188`, `:198-225`);
  - sets the view title to the unit;
  - adds the unit to the WhatsApp text;
  - writes `?unit=<id>` with `history.replaceState`.
- **On boot:** read `?unit=` and call a new `stage.selectUnit(id)` once `ready` resolves.
- **Window view parity with the engine:** add ±30° buttons, fullscreen, arrow keys and the 360° slow orbit, copying `engine.js:3816-4017` into bridge.js without touching engine.js.
- **Named targets in the cone:** port the landmark ring (`engine.js:1702-1747`) into bridge. Rainbow's six landmarks come from `project_env_landmarks`, and the caption names what lies within ±26°, with distances. **Fix the "הים" landmark first** to the measured shore point (287°, 713 m).
- **Never a second beam:** `bridge.js:199` stays.

### 6.6 Honesty and language rules for the reuse
**Needs the owner's word: demo facings and the verified-bearing law.** The six facings are invented demo data (§1.4). CLAUDE.md iron law 3 bans invented bearings. The Einstein contract draws no per-unit cone without a sourced bearing (§4.2). There are three ways to go:
- **(a)** Show "example apartments" with their demo facing and cone, clearly labelled. This is what the owner is asking for, and it matches his earlier `OWNER-2026-08-13-DIRECTION-DEMO`, but it needs his explicit word for Rainbow.
- **(b)** Show the units as **types** (rooms, m², balcony, plan) with no stated facing. The visitor's own pick on the ring drives the view and the cone, as it does today. This is honest by construction.
- **(c)** Wait for real inventory through the P5 intake format (§4.3).

The default is (b) until he rules.

**The rest of the rules:**
- Show no status, scarcity, price, "N דירות לבחירה" or "נמכרה".
- Leave out every payload note.
- Never say "הכיוון אמיתי" or "גובה הקומה אמיתי". The view caption stays "מבט משוער… אינו צילום מהדירה" (`bridge.js:118`).
- Say a direction in words from the sectors, never in degrees or compass letters.
- Run the blacklist and language-DNA grep on every state.
- Fix "לפי היזם" on the 76,000 figure (catalog-plus) and use the annual report's 80,300 incl. VAT, with its source and date, in the answer paragraph.

### 6.7 The clone path
- **Move the per-project numbers out of `stage.js` into config:** `TOWER` (cx, cz, rot, A, B, y0, fh, floors), `BLOCKS`, `GRID_ANGLE`, `COAST_X`, the sectors and the landmarks. Use `nadlan_ps_config()` or a JSON meta `project_stage_json`. One `stage.js` then serves every project; the units always come from `project_3d_units`.
- **Readiness per fleet project** (§1.5):

| Readiness | Projects | What they can do |
|---|---|---|
| **Apartments, demo** | Rainbow (5 tower units now, boutique later), DUO (5 units over two towers, so it needs two ellipse rings), Dimri (4) and Ashira (5) | Allowed only under the §6.6 rules: hide Ashira's "sold" and Dimri's internal prices |
| **Apartments, sourced sizes** | SIX-8 (2 units, real 2025 sizes, real plans) | The strongest real unit data in the fleet |
| **Floor plus facing only** | H-Infinity (normalise `se/w/…` to full words and drop its waiting note) and Einstein (owner-ordered demo directions) | Today's stage behaviour, per project |
| **Line grid** | Aurelia (320 units in lines A-F, PH and G, with `directionAzimuth`) | Proves the arc model at scale, but it is a concept page with lat/lng 0 |

### 6.8 Order of work (each step verified)
1. Fix the meta: 39 floors, one floor height, 459 units (REST before and after; AUD).
2. Move the stage config out of `stage.js`, and set blocks to 8 floors and the tower to 39 (EYES 🖥📱; the same poster).
3. Load the units, build the arcs and anchors, run the Tier B resolver and the Tier C dots (tap each of the 5 units on 📱; press the arrows; the building never moves).
4. Add `nl:unit` to bridge, plus the card, plan dialog and interior doors, and `?unit=` (reload each unit's URL; E2E).
5. Bring window-view parity and the landmark ring (drag, ±30°, 360°; the cone names the targets).
6. Add the consented lead with the unit id, only after the owner's word (E2E test lead; health `lead_e2e`).
7. Clone the stage to DUO as the second config (the owner's "DUO stage", mem).
8. Fleet spot-check and receipt (Rainbow, H-Infinity, home; blacklist 0; AUD diff explained).
