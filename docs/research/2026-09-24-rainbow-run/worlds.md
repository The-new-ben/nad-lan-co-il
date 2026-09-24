# Our 3D worlds, and how to put Rainbow inside the real Sde Dov (24.9.2026)

Read-only research pass. Repo `nad-lan-co-il` on `claude/production-truth-1.72.212` (HEAD a010ac9, live 1.72.256), public GETs of the live site, the find-place data on disk, OSM Overpass, and the Tel Aviv GIS REST. Screenshots were taken with headless Chrome on the machine's real GPU (ANGLE, AMD Radeon iGPU, D3D11) at 1440×900 unless marked mobile. They are in `worlds/`. Evidence tags: **[eyes]** means a screenshot I looked at, **[live]** a public GET or an in-page measurement, **[code]** read in source, **[data]** computed from data files. Nothing in the repo or on the site was changed. The Google browser key that the Earth pages expose by design is redacted here.

## Summary (12 lines)

1. We have two walkable three.js quarter tours (`/tour/sde-dov/`, `/tour/somail/`) and two photoreal "helicopter" worlds (`/earth/sde-dov/`, `/earth/somail/`, CesiumJS with Google Photorealistic 3D Tiles). All four return 200 and are noindex. **[live, eyes]**
2. The tours do what the owner remembers. They fly, they walk node to node (W/S to move, A/D to turn, double-tap to travel), any building opens a card, and a time machine switches 2026 and 2035. But the facilities are schematic (no real schools, stations or parks), and the look is low-poly massing, not cinema. **[eyes, code]**
3. The tours' layout is stylized, not geographic. In `/tour/sde-dov/` Rainbow stands **153 m** from the water; the real figure is **713 m**. The Einstein axis sits about 200 m north of Rainbow; in reality it is about 1 km. As Rainbow's surroundings, the tour would contradict the 713 m the owner insisted on. **[code, data]**
4. The Earth scenes are truthful. They show Google's real photography of today's Sde Dov: sand, the laid-out street grid, the sea. Our GLBs stand on parcel-verified coordinates, and all 15 nearby catalog projects have pins. **[eyes]**
5. Earth is not cinematic either. The light is baked into the photos, the GLBs are flat pastel boxes, and the resting camera frames away from the quarter. First tiles take 11–13 s, and it runs at 14–25 fps while streaming. The promised "click any building" fails (Cesium ion asset 96188 returns 401). Somail shows 10 placeholder pins stacked on the Tel Aviv city centroid. **[eyes, live console, data]**
6. Every other 3D surface is a map or a single-building viewer, not a world: the compound map (`/compound/sde-dov/`, Mapbox Standard, with only Rainbow pinned), the drone band on the homepage, the Rainbow stage with its floor view, the UTOPIA showroom, the designer and `/global/`. **[live, code]**
7. The Sde Dov quarter holds 9 catalog projects, plus 3 more on the Einstein axis. Of these 12, five have a real GLB: Rainbow, Dimri Yama, Ashira, UTOPIA and Einstein Tower. Somail has DUO and H Infinity, both with a GLB (full table in section 5). **[REST]**
8. Rainbow's pin (32.103168, 34.784441) is 18 m from the centroid of plot 111. It lies inside plan 4444 and TMA 3001. The 713 m to the OSM coastline, at a bearing of 287°, reproduced independently. The old memory note that the pin falls in Lamed is stale: the municipal neighbourhood layer still calls that area "תכנית ל׳". **[data]**
9. Real data for clickable facilities is already on disk:
   - the Sde Dov micro-atlas: 4,495 places, 574 parks and beaches, plot polygons 101–111 and 2xxx with links to the design plans, 194 construction sites, rail stations;
   - Tel Aviv GIS layer 513: 407 existing buildings with floors, heights and year of construction inside the quarter box. **[data, live]**
10. The proposal:
    - Keep `stage.js` as the hero. Replace its random "ghost" blocks with a geo-true quarter built from that data: a white-model skin with no per-visit cost.
    - Make the 11 Sde Dov and Einstein projects and about 50 facilities clickable, each with a real card and "what you see from Rainbow toward it".
    - Add a "real photo today" toggle: Google tiles in three.js (3d-tiles-renderer 0.5.3 with TileFlattening, plus the takram atmosphere).
    - Later, a drone Gaussian splat of plot 111 (Spark 2.x).
11. What to reuse:
    - from the tours: the interaction grammar (cards, the walk graph, the time machine, the GPU probe);
    - from `earth-experience.php`: the pins, the quota guard and the server-side key injection;
    - the pilot's 3d-tiles bootstrap;
    - `tools/deals/build_surroundings.py`.

    Drop the tours' geometry.
12. Found along the way (not fixed, read-only): `https://nad-lan.co.il/tour/ecocity/` serves an EcoCity Cesium tour live. It is a static nginx file, Last-Modified 30.8.2026 19:15 UTC, with a Google key embedded and no quota guard, despite the absolute EcoCity takedown order. Eight smaller defects are listed in section 9.

---

## 1. Every 3D world or quarter visualization, at a glance

| # | World | Live URL (status) | Code | Tech | Geometry from | Game-like? | Verdict |
|---|---|---|---|---|---|---|---|
| A | Sde Dov quarter tour V6 | `/tour/sde-dov/` 200, header `X-NL-Tour: v5c`; raw `/wp-content/uploads/2026/07/sde-dov-tour.html` 200, md5 174abb03 = repo | `experience/sde-dov/index.html` (4,387 lines); route `inc/tour-routes.php:24-33, 64-97` | three.js 0.160 + GSAP 3.12.5 ScrollTrigger, one file | procedural stylized grid "informed by" TA/4444 + 3 GLBs | film flight + node walk + WASD + click cards | most interactive; wrong geography; prototype look |
| B | Somail compound tour V6 | `/tour/somail/` 200; raw `.../2026/07/somail-tour.html` 200, md5 2241a7f4 = repo | `experience/somail/index.html` (3,990 lines) | same as A | procedural stylized city + DUO GLB | same as A | same as A; H Infinity still "בקרוב אצלנו" |
| C | Sde Dov helicopter (Earth) | `/earth/sde-dov/` 200 | `inc/earth-experience.php` (645 lines) | CesiumJS 1.143 + Google Photorealistic 3D Tiles | Google photogrammetry + GLBs at parcel coordinates | auto flight, then free orbit camera; no walk | most truthful; not cinematic |
| D | Somail helicopter (Earth) | `/earth/somail/` 200 | same file | same | same | same | truthful base; bad pins and framing |
| E | Google tiles pilot (three.js) | `/wp-content/uploads/2026/07/pilot-google-tiles.html` 200 (a key screen; runs only with `?key=` in the URL) | `experience/pilot-google-tiles.html` (261 lines) | three.js 0.160 + 3d-tiles-renderer 0.3.43 | Google tiles | orbit only | the right engine for our stack, never adopted |
| F | Sde Dov compound map | `/compound/sde-dov/` 200 | `inc/compound-map.php` + taxonomy `inc/compounds.php` | Mapbox GL 3.14, Standard style, fly-in + orbit | Mapbox basemap | map | a map; only Rainbow is tagged |
| G | Drone map band | homepage, `/premium/`, `/en/` (200) | `inc/drone-map.php` (REST `/nadlan/v1/project-map` at `:18-72`, map at `:216-233`) | Mapbox GL 3.7, dark/light + fill-extrusion + terrain DEM | Mapbox buildings | map | a catalog map, not a world |
| H | Rainbow ProjectStage + floor view | `/projects/rainbow-tel-aviv/` 200 | `assets/project-stage/rainbow/stage.js` (2,583 lines), `assets/project-stage/bridge.js`, `inc/project-stage.php` | three.js 0.170 white model; Mapbox 3.7 satellite-streets free camera | a hand-built model + random "ghost" blocks | orbit + floor/direction picking | the art direction to keep; its quarter is invented |
| I | Apartment designer | `/tour/designer/` 200 | uploads `2026/07/apartment-designer.html` | three.js 0.160 + GSAP, RoomEnvironment | interior | door → rooms | an interior, not a quarter |
| J | UTOPIA showroom | `/projects/utopia-sde-dov/` 200 | `inc/utopia-showroom.php:378, 453-467` | model-viewer 4.3.1 + Mapbox 3.7 | GLB + OSM POIs within 1.2 km | building-level | one building |
| K | Global "worlds" | `/global/`, `/global/dubai/` 200 | `inc/global-worlds.php:661-670, 928-941, 1082-1130` | Mapbox light 2D + model-viewer (generic tower) | demo | none | SEO location hubs, not 3D worlds |
| L | EcoCity "from the air" | **`/tour/ecocity/` 200 (static file)**; the old uploads file is 404 | not in repo; nginx static | CesiumJS 1.143 + Google tiles | Google | auto flight | **must not be live**; see section 9 |
| M | Einstein flagship v3 "Spatial Decision Room" | private (health: `public_release_enabled:false`, password gate) | `inc/flagship-surface.php`, `assets/flagship-v3/*` | custom WebGL2 | contract assets | private | not public, not a quarter |
| N | Urban renewal space | `/my-renewal/` 200 | `inc/urban-space.php`, `assets/urban/renewal-space.js` | model-viewer (standard-residential.glb) + Mapbox 3.7 | generic | no | a product demo |

The `/tours/` hub (page 7263) lists five experiences: A, B, C, D and I. `/sde-dov/` (the quarter guide) embeds A as an in-place overlay iframe (`nlsdt-ovfr`) and links all 9 Sde Dov projects. The teaser band (`inc/sdedov-teaser.php:11-44`) also shows on the homepage, `/premium/`, `/new-projects/` and the 12 member project pages. The feature bar (`inc/feature-bar.php:55-128`) links each Sde Dov page to A and C, and each Somail page to B and D. The worktrees (`C:\Users\777\nad-lan\worktrees\*`) hold only older copies of A, B, C and E. `einstein-tower-prototype` holds only reports and the EcoCity research. No other quarter world exists. **[code, live]**

---

## 2. The walkable tours (A, B): what they really are

### A. `/tour/sde-dov/`

- **Stack [code]:** one self-contained HTML file with an importmap for three@0.160 (`index.html:899-903`) and GSAP ScrollTrigger (`:897-898`).
  - Everything else is generated in-file: the FBM sky, the sea shader, facades via `duskify`, instanced massing and street life.
  - Three GLBs stream in the background, each trying the live URL first, then the repo copy, then a procedural fallback (`:2104-2114, 2228-2250`):
    - `sdedov-rich-dimri-v2.glb` (429 KB);
    - `sdedov-rich-ashira-v2.glb` (488 KB);
    - `sdedov-rainbow.glb` (147 KB).
  - The versions: V3 daylight and click-everything, V4 never-stuck cards, V5 the "night-street" render pass (AgX, PCFSoft sun shadows, FBM clouds), V6 auto-tour, the ☰ guide menu, he/en narration (`experience/narration/*.mp3`) and the walking feel (`:10-81`).
- **Geometry [code]:** "STYLIZED MASSING ... NOT an official rendering" (`:99-150`), on a straight N-S grid.
  - 108 fabric blocks and 28 towers are placed with a seeded random generator inside the compound bands (`:1985-2066`).
  - The six named catalog projects are instanced boxes on "approximate lots" (`QPROJECTS :1943-1979`).
  - The Einstein corridor is built lazily east of `x>500`.
  - **The layout is not geo-referenced** (units are metres):

    | Feature | In the tour | Real (parcel data + OSM) |
    |---|---|---|
    | Rainbow to the waterline | shoreline x = -183, Rainbow x = -30 → **153 m** (`:146, :2111`) | **713 m**, bearing 287° |
    | Rainbow to Dimri Yama | 108 m north | 142 m north |
    | Rainbow to Ashira | 445 m east, 198 m north | 305 m east, 275 m north |
    | Rainbow to UTOPIA | 240 m east, 123 m north | 27 m east, 320 m north |
    | Rainbow to FIRST | 843 m north | 1,220 m north |
    | Rainbow to Einstein Tower | 872 m east, 200 m north (`:3057`) | 376 m east, 947 m north |

  - The mobile mini-map shows the sea strip right next to Dimri and Rainbow (`worlds/tour-sde-dov-mobile-walk.png`). **[eyes]**
- **Interactions [code + eyes]:**
  - FILM: a scroll-scrubbed CatmullRom flight in 6 narrated chapters that starts by itself; chapter rail and arrows.
  - EXPLORE: a graph of **25 walk nodes** (`NODES :3040`, `EDGES :3070`).
    - W/S or ↑/↓ glide to the next node in view, A/D turn (`:3778-3787`), drag to look, pinch for FOV.
    - Double-tap the ground to travel there (routed through the nearest node), a clickable minimap, a sky overview.
    - Deep links: `?focus=rainbow|dimri|ashira|utopia-sde-dov|...` (`FOCUS_NODE :4362`).
  - Time machine "היום 2026 / הרובע 2035" with cranes and skeletons in 2026; day and dusk; he/en; a WhatsApp CTA.
  - This is Street-View-style hopping, not free roaming with collisions.
- **Click → info [eyes: `tour-sde-dov-3-click-building.png`]:** a real mouse click on the UTOPIA massing opened this card:
  - "רובע שדה דב · בקטלוג שלנו", UTOPIA, developer and architect, a description, "קומות: עד 36 · דירות: כ־337 · סטטוס: בבנייה — בשיווק · מיקום: משוער על פי פרסומים", and a CTA to `/projects/utopia-sde-dov/`.
  - The flagship cards carry floors, units, status and a link (`:712-749`).
  - Generic massing gets "מתחם X · ~N קומות · בתכנון" (`:2037-2062`).
  - **Facilities are schematic only:**
    - "מבנה ציבור מתוכנן" pavilions on the runway park (`:1768`);
    - "חזית מסחרית בטיילת" (`:2572`);
    - generic cafés, benches and walkers.
  - There is no real school, station, beach or clinic.
- **Performance [live, GPU headless]:**
  - Boot to interactive (`window.__bootMs`) took 836–4,535 ms over four loads (4.5 s cold).
  - 65–76 draw calls and 44–57k triangles.
  - 23 fps in the overview with real shadows forced on (`fx=hi`).
  - Mobile emulation at 390×844: "full tier", 16.9 ms/frame, 47 fps.
  - About 2.9 MB decoded. Zero console errors.
- **Visual level:** a clean low-poly architectural game. Sand-colored ground, grey window-textured boxes, capsule people (`tour-sde-dov-1-overview.png`, `tour-sde-dov-2-walk-rainbow.png`, `tour-sde-dov-4-film.png`). **Not cinematic.** On a 390 px phone the HUD collides: "חזרה לטיסה" overlaps the עב/EN pill, and the minimap covers the scene (`tour-sde-dov-mobile-walk.png`). **[eyes]**

### B. `/tour/somail/`

- It is the same engine and the same grammar (`experience/somail/index.html`).
  - The research header covers TA/2988, DUO and Somail North (`:10-120`).
  - The DUO GLB comes from the plugin (`duo-rich.glb`, 1 MB, `:1967-1970`).
  - The city is stylized: 680 fabric blocks and 31 towers.
- **Performance [live]:** 1.5–2.5 s to interactive, 83–92 draw calls, about 75k triangles, 46 fps. Real shadows switched themselves off once at 32 ms/frame.
- **Stale content [eyes: `tour-somail-4-film.png`, code `:1832`]:** H Infinity is still a "סומייל צפון" card with "בקרוב אצלנו — דברו איתנו". It has had a live flagship page, `/projects/h-infinity-somail-tel-aviv/` (6548), since August.

---

## 3. The photoreal Earth worlds (C, D)

- **Stack [code: `inc/earth-experience.php`]:**
  - The route is `/earth/{slug}/`, with an allowlist of `sde-dov` and `somail` (`:56-77`).
  - Cesium 1.143 from jsDelivr, with `globe:false`, no ion token (`:355`), and `createGooglePhotorealistic3DTileset` (`:585-601`).
  - The API key is injected server-side from option `nadlan_gmaps_key`.
  - A daily load cap of 75 applies (`nadlan_earth_quota_guard :91-102`, filter `nadlan_earth_daily_cap`).
  - Google bills per root request. The Enterprise SKU gives 1,000 free per month, then about $6 per 1,000; one root request covers a session of up to 3 hours.
- **Projects in the world [code + live]:**
  - `nadlan_earth_projects()` (`:118-192`) runs a SQL bounding box of 2.2 km (Sde Dov) or 1.4 km (Somail) and drops language siblings.
  - Projects with `project_model_glb` get the GLB planted at their lat/lng. Ground height comes from `sampleHeightMostDetailed`, raced against a 6 s timer (`:547-583`). The metas `earth_heading`, `earth_scale` and `earth_alt` calibrate each model.
  - Pins are DOM elements, so the Hebrew renders correctly. They are projected every frame and fade with distance (`:418-472`).
  - Measured live:
    - Sde Dov: 15 pins, 5 gold with a model (Rainbow, Dimri, Ashira, UTOPIA, Einstein Tower);
    - Somail: 15 pins, 2 gold (DUO, H Infinity).
- **Interactions:**
  - An auto "helicopter" tour (`:512-541`) makes nearest-neighbour hops over up to 5 GLB projects (3 s flight, 1.7 s hold), then hands over a standard Cesium orbit, pan and zoom camera. There is no walking and no WASD.
  - Hovering or tapping a pin opens a card (`:402-408`). Live on Rainbow it showed "Rainbow Tel Aviv - ריינבו תל אביב · ישראל קנדה · תל אביב יפו · לעמוד הפרויקט · למודל התלת ממד". There is no status, units, floors or price (`earth-sde-dov-3-rainbow-card.png`).
  - Clicking a planted model opens the same card and flies there.
  - The FAB "🚶 לרדת לרחוב" opens `/tour/{slug}/?mode=explore`.
- **The broken promise:**
  - The HUD says "כל בניין אחר נלחץ ומספר מה הוא". Clickability depends on `Cesium.createOsmBuildingsAsync()` (`:605-607`), which needs a Cesium ion token.
  - Live, every load logs `401 https://api.cesium.com/v1/assets/96188/endpoint`, and a click on a neighbouring building showed nothing (`earth-sde-dov-4-click-building.png`, metrics `building_click: null`). **[live]**
- **Framing:**
  - `START` puts the camera *above* the scene centre, pitched down 30–32° (`:370-378`). At rest, the middle of the frame lands 1.3–1.4 km away, over Tel Baruch in Sde Dov and over the port and Reading in Somail.
  - After the Somail tour, a camera readback put the camera 1,880 m above the compound (its configured height is 750 m), looking north-north-west. The frame shows the Reading chimney, the Yarkon mouth and the port; the Somail compound is below the frame (`earth-somail-1-autotour.png`). **[eyes, live]**
- **Wrong pins in Somail [data]:** 10 of the 15 pins are urban-renewal stubs with `geo_confidence = city`, all at exactly 32.0853, 34.781806, the Tel Aviv centroid. That point happens to sit inside the Somail radius: Hadar Yosef, Kfar Shalem, Hassan Arafa, Neve Sharet and others. Site-wide, 112 projects are city-level.
- **Performance [live]:**
  - Tiles ready 11.5 s (Sde Dov) and 12.9 s (Somail) after navigation.
  - 14 and 25 fps while streaming.
  - 251 requests; 7.0 MB and 4.4 MB transferred.
- **Visual level [eyes: `earth-sde-dov-2-rainbow.png`]:** this is the frame that comes closest to the owner's picture. It shows the real Eshkol compound streets and roundabouts on the sand, the runway trace, the sea about 700 m beyond, and Rainbow, Dimri, UTOPIA and Ashira standing on their plots with labelled pins.
  - The light is Google's baked daylight and cannot be relit.
  - Our GLBs are untextured pastel massing that look pasted on, with no contact shadows and no atmosphere.
  - Rainbow's GLB (`rainbow-rich-model.glb`, one mesh) bakes in its own invented surroundings, under the materials "future district silhouette", "coastal sand", "promenade paving" and "lagoon water". Earth plants all of it on top of the real photography: those are the grey boxes around Rainbow. **[data: GLB material list]**
  - **Truthful and impressive, not cinematic.**

The pilot (E, `experience/pilot-google-tiles.html`) is the same idea in **three.js**: 3d-tiles-renderer 0.3.43 with OrbitControls. It never got a server-side key; it reads `?key=` from the URL, which the Earth module rightly forbids. Today it shows only the key screen (`pilot-google-tiles-gate.png`). **[eyes, code]**

---

## 4. The other 3D surfaces (F–K), briefly

- **F `/compound/sde-dov/` [live, code, eyes]:**
  - Mapbox GL 3.14, `mapbox://styles/mapbox/standard` (`compound-map.php:217`), with a 5.2 s fly-in and a 20 s orbit (`:150-230`).
  - Pins come from taxonomy `nadlan_compound`. The term "רובע שדה דב" (id 25) has **count 1** (Rainbow only; the seed matches only "rainbow", `compounds.php:30-55`).
  - Headless capture shows a flat map with one pin and a heading card over it (`compound-sde-dov-mapbox.png`).
- **G drone band (homepage, `/premium/`, `/en/`):**
  - Mapbox 3.7 dark or light, fill-extrusion 3D buildings, terrain DEM ×1.35 (`drone-map.php:216-233`).
  - Pins with data tags come from `/nadlan/v1/project-map` (961 projects).
  - `/projects/` itself now uses the catalog-plus map (`nlcp-map`) instead (`drone-map-homepage.png`).
- **H Rainbow stage [code, eyes: `rainbow-stage-now.png`, `rainbow-view-and-areamap-now.png`]:**
  - `stage.js` runs three@0.170 and draws an architect's white model at golden hour: tower, six boutique blocks, pool, garden. It ran at 48 fps.
  - The local frame is in metres, with local −z = grid north turned 20° east (`:92-97`). The sea is at `COAST_X = -743`, 713 m from the tower (`:113-116`).
  - **The quarter around it is random:** a 9×9 grid of 128 m × 104 m plates with seeded "ghost" volumes (`buildWorld :2160`, quarter `:2218-2237`, `ghostCell :2556-2583`).
  - `bridge.js` shows the view from the chosen floor on Mapbox `satellite-streets-v12` with extrusions (`:159-169`) and turns the beam on the engine's area map (price pins and POI chips).
- **I designer:** an interior scene (three 0.160, RoomEnvironment, GSAP), "דירת 4 חדרים מול ים" (`tour-designer.png`).
- **J UTOPIA:** model-viewer plus a Mapbox environment map of lot 103, with OSM POIs within 1.2 km.
- **K `/global/`:** Mapbox light 2D plus a generic model-viewer tower on demo projects.

---

## 5. Our projects in the Sde Dov quarter, the Einstein axis and Somail

Sources:
- `/wp-json/nadlan/v1/project-map` (live, 961 items; coordinates, geo confidence, status enum, units, ₪/m²);
- `/wp-json/wp/v2/nadlan_project` meta (GLB, floors, raw status);
- `inc/sdedov-teaser.php:26-33` (the 12 member slugs).

Distances and directions are measured from Rainbow's pin, using Rainbow's own sector words from `nadlan_ps_config()`. **[REST, data]**

| id | slug | name | lat, lng (geo conf) | status (map enum / raw) | units | floors (REST) | ₪/m² on file | 3D model | from Rainbow |
|---|---|---|---|---|---|---|---|---|---|
| 4464 | rainbow-tel-aviv | Rainbow Tel Aviv, Israel Canada | 32.103168, 34.784441 (parcel-centroid-verified; plot 111, 18 m) | construction / בבנייה | 480 | **empty** (developer says 39; stage 40; tour card "כ־38") | 76,000 | GLB `uploads/2026/07/rainbow-rich-model.glb` (852 KB); tour `sdedov-rainbow.glb`; stage draws its own | — |
| 4745 | dimri-yama-sde-dov | DIMRI YAMA, Y.H. Dimri | 32.104441, 34.784472 (parcel) | marketing / בשיווק | 458 | 39 | 75,000 | GLB plugin `models/dimri-rich.glb` | 142 m, לכיוון תל ברוך והרצליה |
| 4747 | zohi-sde-dov | ZOHI, Levinstein/Mivne/Allied | 32.102851, 34.785483 (parcel) | marketing / בשיווק | 230 | 12 (tour says up to 16) | 90,000 | none (generic in engine) | 104 m, לכיוון פארק הירקון |
| 4750 | shikun-binui-sde-dov | Shikun & Binui rental, lot 109 | 32.103371, 34.785624 (parcel) | — / בהיתר בנייה | 324 | 38 | — | none | 114 m, לכיוון רמת אביב והאוניברסיטה |
| 4749 | utopia-sde-dov | UTOPIA, Nechemias | 32.106063, 34.784732 (parcel) | — / permits | 337 | 34 | — | GLB plugin `models/utopia-rich-v1.glb` | 323 m, לכיוון תל ברוך והרצליה |
| 4744 | ashira-sde-dov | ASHIRA, Avisror | 32.105643, 34.787673 (parcel) | marketing / בשיווק | 406 | 35 | 75,000 | GLB plugin `models/ashira-rich.glb` | 410 m, לכיוון רמת אביב והאוניברסיטה |
| 4748 | gindi-vogue-sde-dov | GINDI VOGUE, Gindi | 32.110644, 34.783587 (parcel) | marketing / בשיווק | 708 | 44 | 54,000 | none (tour: east-zone "gindi-rova" massing) | 835 m, לכיוון תל ברוך והרצליה |
| 4743 | first-sde-dov | FIRST, Hagag | 32.114141, 34.784411 (parcel) | marketing / בשיווק | 350 | 45 | 75,000 | none | 1,220 m, לכיוון תל ברוך והרצליה |
| 4751 | migdalei-hayam-sde-dov | senior living, Migdalei HaYam HaTichon | 32.123298, 34.786813 (parcel) | planning / בתכנון | 300 | 20 | — | none | 2,249 m, לכיוון תל ברוך והרצליה |
| 4867 | einstein-tower | EINSTEIN TOWER, Hagag (Einstein axis) | 32.111736, 34.788433 (address) | construction | 215 | 28 | — | GLB `uploads/2026/08/einstein-tower-model-hd.glb` (2.4 MB) | 1,024 m, לכיוון תל ברוך והרצליה |
| 4874 | einstein-19 | Einstein 19, Azorim (Einstein axis) | 32.1133, 34.793685 (parcel) | — | 80 | — | — | none | 1,424 m, לכיוון רמת אביב והאוניברסיטה |
| 4875 | ashdar-einstein | Ashdar Einstein (Neve Avivim) | 32.11345, 34.798809 (parcel) | — | 45 | — | — | none | 1,772 m, לכיוון רמת אביב והאוניברסיטה |
| 4893 | duo-tel-aviv | DUO, Africa Israel (Somail) | 32.0847, 34.7824 (parcel) | — | 668 | **empty** | — | GLB plugin `models/duo-rich.glb` (1 MB) | 2,063 m, לכיוון מגדלי העיר |
| 6548 | h-infinity-somail-tel-aviv | H Infinity, Hagag (Somail) | 32.086, 34.7821 (address-approx) | construction | 242 | 52 | — | GLB `uploads/2026/08/h-infinity.glb` (697 KB) | 1,922 m, לכיוון מגדלי העיר |

**Notes:**
- All 12 Sde Dov and Einstein projects appear in tour A, at approximate lots. All 12 appear as Earth pins in C, together with three urban-renewal compounds: שמעוני 29-27, ברזיל and טאגור.
- Language siblings (`-en/-fr/-ru/-ar`) exist for Rainbow, UTOPIA and DUO and are excluded above.
- The repo's canonical record `data/projects/rainbow-sde-dov.json` still says `needs_geocode`, with an unverified estimate of 32.1298, 34.786. The live meta is the truth.

---

## 6. Real data we already own for "click a facility and learn something"

- **Sde Dov micro-atlas**, `C:\Users\777\Documents\Codex\2026-08-27\https-www-nadlan-gov-il-https\outputs\sde-dov-micro-atlas\` (27.8.2026, TLV OpenData + OSM, commercial reuse allowed with attribution per its README). It contains:
  - `places.geojson`: 4,495 places (education 283, sport 267, transport 317, health 66, culture 28 and more);
  - `parks-beaches-nature.geojson`: 574 items;
  - `plans-and-parcels.geojson/.csv`: TA/4444, the three detailed plans, per-lot design plans such as "מגרש 111, אשכול" with municipal document links;
  - `construction-projects.geojson`: 194 sites with permit numbers;
  - `mobility-networks.geojson`: the Green Line, bike network and bus lanes;
  - `transactions-matched.csv`: 7,857 deals since 2019.

  The same entities are bundled in `platform/data/generated/sde-dov-v0.bundle.json` and `north-tlv-v1.bundle.json`, which `tools/deals/build_surroundings.py` reads. **[data]**
- **What that gives Rainbow today** (`tools/deals/project-surroundings-v1.json`, key 4464):
  - Reading light-rail station, 467 m (approved, not operating);
  - Kochav HaTsafon school, 262 m; Aran school, 777 m;
  - the Yarkon estuary, 761 m; Reading beach, 841 m;
  - 9 active construction sites within 500 m, the nearest at 60 m (permits 20240293/20261155);
  - inside plan 4444 and TMA 3001; the linear park plan nearby.

  Within 1.6 km the bundles hold 23 plot polygons (101–111, 301–306, 407, 409, 2102–2270), 55 places, 5 open spaces and 125 construction sites. **[data]**
- **Tel Aviv GIS layer 513 "מבנים"** (`https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/513`, maxRecordCount 2000):
  - footprints with `ms_komot` (floors), `min_height`/`max_height`, `year`, `dsm_max` and building type;
  - **407 buildings** in the box 34.772–34.792 E, 32.098–32.112 N.

  These are the existing city around the quarter (Kochav HaTsafon, Lamed, the port, Reading), clickable with real floors and years, and no Cesium ion is needed. **[live]**
- **OSM:** the coastline (the 713 m), streets (Shai Agnon at 32.1018–32.1031, Levi Eshkol at 34.7888–34.7890 by Rainbow), and the parks. **[data]**
- **Transit alignment and stations** (Green, Red and Purple lines, metro): `platform/data/frozen/north-tlv-gis-v1/` (TLV GIS layers 423, 760–766, 954).

---

## 7. Proposal: Rainbow inside the real Sde Dov

### 7.1 Which world is "best", honestly

- **Most interactive:** tour A. Its grammar (walk graph, click-everything registry, never-stuck cards, time machine, narration, GPU probe) is proven, but its geometry is invented and its look is prototype.
- **Most truthful:** Earth C. It shows the real place today and parcel-true projects, but it runs on a different engine (Cesium), and its lighting and models are not cinematic.
- **Best art direction:** the Rainbow stage (H), which is already the three.js scene on the page, with floor and direction picking wired to the view and the beam.

So the answer is **not** "embed the old tour". It is:

> Build Rainbow's quarter inside `stage.js` from real data, give it the tour's interaction grammar, and offer Google's real photography as a toggle.

It is one engine (three.js), one coordinate frame (the stage's metres), and nothing contradicts the 713 m.

### 7.2 Architecture

1. **One local frame.**
   - The origin is Rainbow's parcel point (32.103168, 34.784441). Convert with local ENU in metres, then rotate by the stage's grid angle (20°, `stage.js:92-97`). With E and N as local east and north metres: `x = E·cos20° − N·sin20°`, `z = −(E·sin20° + N·cos20°)`.
   - Acceptance tests:
     - the OSM coastline converts to x ≈ −743 near the site (`COAST_X`);
     - Dimri Yama lands about 142 m to grid-north (roughly x −43, z −128);
     - Zohi lands about 104 m to local east-south-east.
2. **Build step:** a new script next to `tools/deals/build_surroundings.py`, run offline, no live calls at page time. It reads:
   - TLV GIS 513 buildings within about 1.5 km (the existing city, extruded, with `{kind:'building', floors, year}`);
   - the micro-atlas plots (101–111, 2xxx) as flat plates, and the planned massing as translucent "ghost" volumes on the **real plot shapes**, labelled "על פי התכנית · הדמיה להמחשה";
   - the coastline, beach and coastal park polygons; the streets; the Green Line track and stations;
   - `project-map` plus meta for our 11 projects: their GLBs, or schematic volumes from `num_floors` on their plots, labelled "מסה סכמטית".

   It outputs one Draco/Meshopt GLB (`sde-dov-context.glb`, target ≤ 1.5 MB) and `sde-dov-pois.json` (projects and facilities with source and date).
3. **stage.js change:** keep `mountRainbowStage`, the tower, blocks, plot, floor ring, `nl:*` events, sky and sea. Replace only the quarter section of `buildWorld` (`:2218-2237`) and `ghostCell` (`:2556-2583`) with a context loader, gated by an option (`world: 'quarter'`). The procedural blocks stay as the fallback. `engine.js` and the beam stay untouched (the frozen beam law).
4. **Pins and cards:** port the DOM pin overlay from `earth-experience.php:418-472` (bidi-safe Hebrew, distance fade, gold for GLB projects) and the tour's card system (`regClick`, `openDyn`, the four ways to close). The data comes from a small REST route built on `nadlan_earth_projects()` (`:118-192`) plus `num_floors`, the status enum and ₪/m².
   - **A project card** shows:
     - name, developer, status, floors and units;
     - ₪/m² only when it is on file (unknowns are omitted, per the honesty law);
     - distance and direction from Rainbow in sector words ("142 מ׳ לכיוון תל ברוך והרצליה"), never degrees;
     - "לעמוד הפרויקט" and WhatsApp "לקבלת תוכניות ומחירים";
     - **"מה רואים מריינבו לכיוונו"**, which sets the stage's floor and facing to that bearing, so `bridge.js` shows the view and turns the beam.
   - **A facility card** (school, kindergarten, station, park, beach, clinic) shows the name, category, walking minutes from Rainbow, "קיים היום" or "עתידי · מאושר", and the source and date.
   - **An existing building** (layer 513) shows its floors and year built. **A plot** shows its lot number, plan and status, with a link to the municipal design documents.
5. **Modes (the "video game"):**
   - **Orbit**, the stage's default.
   - **Fly**, Earth's nearest-neighbour hop over our projects (`:500-541`), now in three.js with eased CatmullRom paths.
   - **Walk**, the tour's node graph, W/S/A/D and double-tap travel (`index.html:3040-3087, 3559, 3778`), with nodes generated from real street centerlines around plot 111: Shai Agnon, the plaza, the linear park, the promenade.
   - **Time machine**: "היום" (the plots as they are, cranes) and "2035" (the plan's ghost volumes rise), reusing `applyYear`.
6. **"Real photo" toggle (phase 3):**
   - Load Google Photorealistic 3D Tiles **inside the same three.js scene** with 3d-tiles-renderer 0.5.3:
     - `GoogleCloudAuthPlugin`;
     - `ReorientationPlugin` at the same origin;
     - `TileFlatteningPlugin` to press the sand flat under our volumes;
     - the fade plugin.
   - Load it only on an explicit tap. Reuse the server-side key injection and the quota guard from `earth-experience.php` (never `?key=` as in the pilot).
   - Label it "צילום אוויר של היום · Google", and keep Google's on-screen attribution.
   - Tiles are Google's daylight and cannot be relit, so grade them to the stage's presets with the takram atmosphere and aerial perspective.
7. **Later:** a drone capture of plots 105–111 as a Gaussian splat, streamed with Spark 2.x in the same scene. This is Zillow SkyTour's approach. It needs a drone permit near the former airport and a capture vendor.

### 7.3 What "cinematic" requires (checklist to accept the work)

- **Truth first:** the geo-true layout above. "Cinematic" in a real-estate world means the viewer recognises the real place.
- **Hero fidelity:** Rainbow at facade level (balcony slabs, glass, mullions, the curved boutique blocks). The stage is partly there. Our other GLBs need the same pass, or they stay honest schematic volumes.
- **Light:**
  - the sun by date and time for Tel Aviv (golden hour);
  - soft shadows limited to about 1.5 km;
  - GTAO or N8AO ambient occlusion;
  - golden-hour IBL, AgX tone mapping (already in the tours), bloom on lit windows at dusk;
  - atmosphere and height fog (takram);
  - light depth of field on the context in the overview. Hauzd, the owner's benchmark, blurs its photogrammetry context and keeps the hero sharp (`hauzd/03-exterior-home-d.png`).
- **Camera:** a skippable 15–20 s opening, sea → coastal park → plots → Rainbow rises → floor → the view, then free control. Eased paths, never jumpy.
- **Life:** the sea glitter (the stage has it), instanced cars on Namir, Levi Eshkol and Shai Agnon, promenade walkers, birds and palms (from the tours), sound, and he/en narration from the existing edge-tts pipeline.
- **Budgets:** first frame under 4 s on a mid-range Android over 4G; ≤ 150 draw calls; KTX2 textures and Draco/Meshopt geometry; the adaptive DPR and GPU tier probe (stage and tour) kept on.
- **Honesty labels everywhere:** "הדמיה להמחשה", "על פי התכנית", and the capture date on photos. No invented inventory.

### 7.4 Order of work (each step verifiable by screenshots on the real GPU)

- **0. Data truth** (small, first):
  - fix the defects in section 9 that feed this world (city-level pins, the compound term, Rainbow's floors);
  - build `sde-dov-context.glb` and `sde-dov-pois.json`;
  - pass the three acceptance tests in 7.2.
- **1. Rainbow in the real quarter** (white-model skin): the context loader in `stage.js`; pins and cards for the 11 projects and about 50 facilities; "the view from Rainbow toward it"; the time machine; Hebrew first; performance budgets.
- **2. Cinematic pass:** light, the opening flight, life, sound, mobile tuning.
- **3. Photo toggle:** Google tiles in three.js, the quota guard, the atmosphere grade.
- **4. Roll-out:** make it a generic "quarter world" module keyed by scene. Somail with DUO and H Infinity comes next. Re-georeference or retire the stylized tours A and B, keeping their walk and cards on the real layout.

**Running cost:** the white-model skin has no per-visit fees. Mapbox, used only by `bridge.js`, gives 50,000 free map loads a month, then $5 per 1,000. Google 3D Tiles gives 1,000 free root requests a month, then about $6 per 1,000, so the photo toggle must stay opt-in and guarded.

---

## 8. Current best practice (brief web check, September 2026)

- **Google Photorealistic 3D Tiles in three.js:** [3DTilesRendererJS](https://github.com/NASA-AMMOS/3DTilesRendererJS). npm `3d-tiles-renderer` is at 0.5.3 (18.9.2026). Its plugins include `GoogleCloudAuthPlugin`, `ReorientationPlugin`, `TileFlatteningPlugin`, `GLTFExtensionsPlugin` and `UpdateOnChangePlugin` (verified in `src/three/plugins`). Google's docs: [Photorealistic 3D Tiles](https://developers.google.com/maps/documentation/tile/3d-tiles), [usage and billing](https://developers.google.com/maps/documentation/tile/usage-and-billing) (a root request allows up to 3 h of tile requests; default cap 10,000 root requests a day), and the [price list](https://developers.google.com/maps/billing-and-pricing/pricing) (1,000 free a month, then about $6 per 1,000).
- **Cinematic atmosphere for those tiles:** [takram three-geospatial](https://github.com/takram-design-engineering/three-geospatial) (`@takram/three-atmosphere` 0.19.1, three-clouds). It adds physically based sky, aerial perspective and volumetric clouds that cast shadows, designed to run with 3DTilesRendererJS ([Tokyo demo](https://takram-design-engineering.github.io/three-geospatial/?path=%2Fstory%2Fclouds-3d-tiles-renderer-integration--tokyo)).
- **Cesium alternative:** [clipping polygons](https://cesium.com/learn/cesiumjs-learn/cesiumjs-clipping-polygons/) cut photogrammetry to insert our models, and [3D Gaussian splats with hierarchical LOD in 3D Tiles](https://cesium.com/blog/2026/04/27/3d-gaussian-splats-lod/) (April 2026) can combine with Google tiles. CesiumJS is at 1.145; we run 1.143. Staying on Cesium would mean a second engine beside `stage.js`.
- **Google's own 3D Maps (Map3DElement, Model3DElement, flyCameraAround):** generally available for the web, billed on the Immersive Maps SKU ([reference](https://developers.google.com/maps/documentation/javascript/reference/3d-map), [2026 tutorial](https://spatialized.io/insights/google-maps/data-layers-and-overlays/immersive-3d-maps)). It is simple, but it is a closed renderer: no custom shaders or grade, so it cannot carry our stage.
- **Mapbox Standard:** light presets (dawn, day, dusk, night), shadows, AO, 3D landmarks, a GLB `model` layer with shadows, and a [clip layer](https://docs.mapbox.com/mapbox-gl-js/example/clip-layer-building/) to replace buildings ([v3 guide](https://docs.mapbox.com/mapbox-gl-js/guides/migrate-to-v3/), [3D models](https://docs.mapbox.com/style-spec/guides/using-3d-models/)). mapbox-gl is at 3.31; we run 3.5–3.14. [Pricing](https://docs.mapbox.com/mapbox-gl-js/guides/pricing/): 50,000 free loads, then $5 per 1,000 ([breakdown](https://storerocket.io/learn/mapbox-pricing)). This is a good upgrade for `bridge.js`'s floor view (dusk preset plus shadows), not for the hero.
- **Gaussian splats:** [Spark](https://github.com/sparkjsdev/spark) by World Labs renders splats inside three.js, mixed with meshes. [Spark 2.0](https://www.worldlabs.ai/blog/spark-2.0) (April 2026) streams huge splat worlds with LOD; npm `@sparkjsdev/spark` is at 2.2.0. This is the way to show a drone capture of the real site.
- **Data-true city massing precedent:** [Tel Aviv 2035](https://github.com/galbenyosef/fable-build-day-tlv-2026), a Fable Build Day winner on 17.9.2026, uses MapLibre fill-extrusion from TLV GIS layer 513 plus permit heights from layer 772. It is data-true but not cinematic. It confirms the layer-513 route; see the [OSM forum on TLV heights](https://community.openstreetmap.org/t/using-gis-tel-aviv-for-buildings-heights/85546).
- **Baked light:** for the white-model skin, bake AO or lightmaps into the context GLB (Blender Cycles) instead of computing them live. It gives the cheapest large gain in "model-maker" realism on phones.

---

## 9. Defects and gaps found along the way (not fixed; for Linear/Notion per the no-silent-gaps law)

1. **EcoCity is live, against the absolute 30.8 takedown order [live].**
   - `https://nad-lan.co.il/tour/ecocity/` returns 200 from nginx as a static file. The title is "אקו סיטי מהאוויר — הדגמת סיור פרטית", the h1 "ברוכים הבאים לאקו סיטי", Last-Modified is 30.8.2026 19:15 UTC, and robots is noindex.
   - It runs Cesium 1.143 with Google tiles and a Google key embedded in the file. It bypasses the Earth quota guard, so every visit bills a root request.
   - The old `/wp-content/uploads/2026/08/ecocity-tour.html` is 404, as ordered. It is not in the repo, so it was placed on the server directly.
   - This needs the owner's word and removal via uPress.
2. **Earth "click any building" is dead [live].** Cesium OSM Buildings returns 401, because there is no ion token (`earth-experience.php:355, 605`). Either drop the promise from the HUD and the card copy, or add a real building source (TLV layer 513, as in section 6).
3. **Somail Earth plants 10 city-level placeholder pins at one point [data].** `nadlan_earth_projects()` does not filter `geo_confidence = city`.
4. **Both Earth scenes rest with the quarter out of frame [eyes, live].** The camera is placed above the centre, not offset back (`:370-378`). Somail's post-tour rest was read back at 1,880 m above the compound, looking at the port. Separately, Rainbow's planted GLB carries a fake sand, promenade and lagoon context plus "future district" boxes, which land on the real photography. Earth should plant a building-only GLB.
5. **The compound map pins only Rainbow [live].** The `nadlan_compound` term "sde-dov" has 1 project. The other 8 Sde Dov projects are not tagged.
6. **Rainbow's floor count disagrees across surfaces [REST, code].**
   - The developer page says a 39-floor tower plus six 8-floor buildings (`data/projects/rainbow-sde-dov.json`).
   - `stage.js` draws 40 (`:97`), the tour card says "כ־38 קומות", and REST `num_floors` is empty.
   - DUO's `num_floors` is also empty.
7. **Stale or missing links:**
   - The Somail tour still calls H Infinity "בקרוב אצלנו" (`somail/index.html:1832`).
   - The Sde Dov teaser deep-links only the 3 flagships (`sdedov-teaser.php:37-40`), though the tour supports `?focus=` for all 9 projects plus the Einstein ones.
8. **Tour mobile HUD overlap [eyes]:** at 390 px, "חזרה לטיסה" overlaps the עב/EN pill, and the minimap covers the scene.
9. **The tours' stylized geography contradicts the real one [code + data]:** the sea at 153 m instead of 713 m, and the Einstein axis compressed (table in section 2). It is labelled "הדמיה להמחשה", but it cannot become Rainbow's surroundings without re-georeferencing.

---

## 10. Evidence index

**Screenshots (`worlds/`, real GPU, headless Chrome):**
- Tours:
  - `tour-sde-dov-1-overview.png`, `tour-sde-dov-2-walk-rainbow.png`, `tour-sde-dov-3-click-building.png`, `tour-sde-dov-4-film.png`, `tour-sde-dov-mobile-walk.png`;
  - `tour-somail-1-overview.png`, `tour-somail-2-walk-duo.png`, `tour-somail-4-film.png`.
- Earth:
  - `earth-sde-dov-1-autotour.png`, `earth-sde-dov-2-rainbow.png`, `earth-sde-dov-3-rainbow-card.png`, `earth-sde-dov-4-click-building.png`;
  - `earth-somail-1-autotour.png`.
- Maps and pages:
  - `compound-sde-dov-mapbox.png`, `drone-map-homepage.png`;
  - `rainbow-stage-now.png`, `rainbow-view-and-areamap-now.png`;
  - `tour-designer.png`, `pilot-google-tiles-gate.png`.

**Scripts:** the capture harness and metrics are in the session scratchpad (`scratchpad/worlds/shoot.py`, `metrics.json`). The metrics hold draw calls, frame rates, boot times, transfer sizes, console lines and the Earth scene contents.

**Earth quota used by this research:** 5 loads of `/earth/*` on 24.9, against the 75-a-day cap.

**Geo checks:**
- OSM Overpass: the coastline and the streets.
- The coast distances from the parcel pins:

  | Project | Distance to coast |
  |---|---|
  | Rainbow | 713 m @ 286.8° |
  | Dimri | 680 m |
  | UTOPIA | 667 m |
  | Gindi | 461 m |
  | FIRST | 419 m |
  | Migdalei HaYam | 309 m |

  The coastline crosses Rainbow's latitude at 34.77594 E.
- Plot 111's centroid is 18 m from Rainbow's pin (the micro-atlas bundle).
- TLV GIS layer 513: count query of 407 for the box.

**Versions checked on npm (24.9.2026):** three 0.186.1, 3d-tiles-renderer 0.5.3, @takram/three-atmosphere 0.19.1, @sparkjsdev/spark 2.2.0, cesium 1.145.0, mapbox-gl 3.31.0. We run three 0.160 in the tours and 0.170 in the stage, cesium 1.143 and mapbox-gl 3.5–3.14.
