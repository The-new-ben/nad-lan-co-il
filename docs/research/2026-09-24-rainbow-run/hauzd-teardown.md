# Hauzd "Olae Tower": hands-on teardown with the 3D rendered (24.9.2026)

**Target:** https://olae-tower.hauzd.app/ (Hauzd platform, Olae Tower, Veracruz, Mexico: 25 floors, 94 units).
**Method:** Python Playwright driving headless Google Chrome 153 on this machine's real GPU (ANGLE on AMD Radeon iGPU, D3D11, WebGL 2, verified with `WEBGL_debug_renderer_info`). The command-queue harness kept the 3D loaded between steps. I looked at every screenshot before taking the next step. Network was recorded with Playwright plus CDP. Four sessions:
- `d1`: desktop 1440×900, 25 min
- `d2`: fresh desktop, 15 min
- `p1`: phone 390×844, DPR 2, touch, Android UA, 8 min
- `n1`/`np1`: nad-lan Rainbow on desktop and phone

**Safety:** I clicked "English" and "I agree" (owner-approved 24.9). I submitted no form, typed nothing, and did not sign in, reserve or pay. No captcha appeared. For WhatsApp and share, I stubbed `window.open` and captured the link without opening it. I only looked at "Contact us" and "Request Quote" and closed them.

**Evidence classes:** **eyes** = a real GPU screenshot I looked at (file names below). **code** = DOM, network or JS-source check. **unverified** = marketing claim only.

Screenshots are in `docs/research/2026-09-24-rainbow-run/hauzd/`. The suffix `-d` means desktop and `-p` means phone.

---

## 1. The level to beat, in 15 lines

1. It is a full-screen, app-like 3D showroom: no page and no scroll. It runs Hauzd's own C++ engine compiled to WebAssembly on WebGL 2. It is not Unity or three.js (code).
2. The tower is a textured, photoreal model with plants, pool, cars and furniture. It sits inside a real drone panorama of the site, with a depth-of-field blur on the surroundings (eyes 03, 18).
3. Each of the 94 units is its own zone on the facade. Hovering paints the unit translucent green with a number pill. Clicking flies the camera to it and opens a unit card (eyes 06, 07, 26a).
4. The unit card shows: number, price (MX$) or "Unavailable", beds, baths, m², interior m², exterior m², parking, type, a 3D thumbnail of the unit, Keyplan / Floorplan / Request Quote, share, favourite and one "similar unit" (eyes 07, code).
5. The filter chips (Status, 1 Bed+Flex, 2 Bed, 2 Beds+Flex, 3 Beds) recolour the facade itself, so the building is the search result (eyes 24, 25).
6. A sortable price list of all 94 units is one tab away. Clicking a row flies the camera to that unit (eyes 22, 23, 23b).
7. **Keyplan** drops the camera onto the floor plate with every unit labelled. **Floorplan** is one rail of five modes: 2D CAD, 2D with room dimensions, furnished 3D top-down, pitched dollhouse, and first-person walk (eyes 08–17).
8. The walk is real-time 3D. You drag to look, and click the floor to glide there with a ring cursor. The windows show the real drone photo for that height (eyes 14–17b).
9. "360 Views" is built from 11 geo-placed drone 360° photos: 10 stacked every 7 m from 19 m to 82 m on the tower's axis, plus one aerial. The rendered tower is composited into the photo (eyes 18, 19; code).
10. The motion is cinematic but restrained:
    - a push-in after "I agree"
    - an eased fly-to on every selection
    - smooth walk glides
    - after 5 idle minutes, an attract-mode "movie" that tours units and the exterior with fades (eyes 21a–d; code).
11. The data is live and shareable. The app polls an AWS API every 10 s, and price and status come per unit from a sales JSON. Every view state is in the URL, even the walk position (`/Nivel14/Dpto1401?isTour=1&tourPos=…`) (code).
12. The phone version is a real adaptation: bottom tab bar, a bottom sheet for the unit card, swipe to orbit and pinch to zoom. Every desktop feature is present (eyes 40–54).
13. Its weak spots (eyes 37, 38, 28a, 34, 35; code):
    - **Weight and wait:** 659 MB streamed in a 15-minute desktop visit and 532 MB in 8 minutes on the phone profile. The finished image took about 22 s on desktop. On the phone profile it was still untextured 20 s after agree, with a 25 s download stall.
    - **State bugs:** the view got stuck in the interior after switching tabs.
    - **Location:** only a plain Google map.
    - **Leads:** "Contact" and "Request Quote" are the developer's homepage in an iframe, and the unit is not passed.
    - **Data display:** areas show broken decimals ("167791 m²").
    - **Language:** Spanish labels leak into the English UI.
14. It has no search presence. The HTML is a 1.3 KB shell with no text, no meta description and no Open Graph tags, so shared links get no preview (code).
15. **The bar:** unit-level picking on a photoreal facade, plans-to-walk on one rail, and real drone views per height, full-screen on web and phone. nad-lan beats it only if it adds these and keeps its own strengths: 6 MB instead of 600 MB, indexable Hebrew content, neighbourhood data, and 5 languages.

---

## 2. The user journey, step by step

### Desktop (1440×900)

| # | Screenshot(s) | What the user sees | What the user does / what happens |
|---|---|---|---|
| 1 | `01-landing-d.png` | A black screen with the Olae logo and two buttons, "Español" and "English". | Clicks English. Before this click, the page has loaded 1.9 MB of shell and engine WASM. The 3D `.ibf` stream starts about 5 s after the page opens, so 62 MB of 3D data had arrived before the first click in session d1 (code). |
| 2 | `02-disclaimer-d.png` | A dimmed tower image with a disclaimer (CGI is illustrative, sizes approximate, not a contract). Buttons: "I agree" and a back arrow. | Clicks "I agree". **3D chunks already stream behind these two gates**: in session d1 the gates stayed on screen for about 44 s, and 122 MB of `.ibf` 3D data arrived before "I agree" (code). |
| 3 | `03a-cold-load-0-6s-after-agree-d.png`, `03b-cold-load-7-23s-after-agree-d.png`, `03-exterior-home-d.png` | Timings from the fresh session d2, counted from "I agree": a spinner on black, then fog, then grey massing (about 6 s), then the white detailed model (about 13–15 s), then full facade materials (about 17 s), then the drone-panorama backdrop, the finished look (about 21–23 s). Around it: header tabs (Exterior, Amenities, 360 Views, List, Location, Gallery), WhatsApp, Contact us, Fullscreen, Back, filter chips, a left sidebar of unit cards (2502, 2501, 2404…), rotate and zoom buttons, and a compass. | Waits. The camera does a slow push-in onto the tower, then settles (eyes: session d1 load frames kept in the scratchpad; `03` shows the settled result). |
| 4 | `04-exterior-rotated-d.png`, `05-exterior-zoomed-d.png` | The orbit follows the drag smoothly. The wheel zooms toward the facade. | Drag to orbit, wheel to zoom. Each fires a `camera_interact` analytics event (code). |
| 5 | `06-unit-hover-highlight-d.png` | Hovering a unit fills that unit's facade segment with translucent green and shows a white pill ("1401"). Green means available. | Hover only. It works per unit, not per floor. |
| 6 | `07-unit-selected-card-d.png` | The camera eases to unit 1401. The sidebar becomes the unit card: 1401, MX$7,162,000, 2.5 beds, 3 baths, area, interior/exterior m², parking 2, type G, a 3D isometric thumbnail, Keyplan / Floorplan / Request Quote, share, heart, and a "similar unit" (1201, MX$7,073,000). The breadcrumb reads "Olae Tower \ 14th Floor \ 1401". | Clicked the unit. The URL becomes `?selRelAddr=Nivel14/Dpto1401`. |
| 7 | `08-keyplan-d.png`, `08b-keyplan-hover-other-unit-d.png`, `09-keyplan-iso-stack-d.png` | The camera drops to a top-down floor plate of floor 14 with a pill on each unit (1401–1406). Hovering another unit lights it green. A side rail offers "3D" and "pitched": pitched tilts to a dollhouse view with the floors below in grey. | Keyplan, then hover, then pitched. The URL becomes `/Nivel14?selRelAddr=Dpto1401&isPitched=1`. |
| 8 | `10-floorplan-d.png`, `11-floorplan-dimensions-d.png`, `12-unit-3d-topdown-d.png`, `13-unit-3d-dollhouse-d.png` | A 2D CAD line plan of 1401 on dark teal, then the same plan with room dimensions, then the furnished 3D top-down, then the pitched dollhouse. There are five mode buttons on a vertical rail. | Clicks each mode. URL flags: `show2d=1`, `showDim=1`, `isPitched=1`. |
| 9 | `14-interior-tour-start-d.png`, `15-interior-tour-lookaround-d.png`, `16-interior-tour-living-view-d.png`, `17a-interior-walk-glide-mid-d.png`, `17b-interior-walk-arrived-d.png` | A first-person view inside 1401 at 1.5 m eye height: furnished bedroom, bathroom, walk-in closet, living room, kitchen, balcony. The curved glass shows the **real drone photo of the coast and breakwaters**. Dragging turns the head. Hovering the floor shows a ring cursor. Clicking it turns the ring green and the camera glides there. | The walk mode on the rail. The URL records `isTour=1&tourPos=…&tourCamUV=…`. Keyboard arrows, WASD and the wheel do nothing (code: URL unchanged). |
| 10 | `18-360views-drone-composite-d.png`, `19-360views-lookaround-d.png` | A full-screen drone 360° photo of the coast with the rendered tower composited in, and a compass. Drag looks around; the wheel zooms into the photo. | Clicked "360 Views" from the exterior. From inside the walk it failed (see step 22). |
| 11 | `20-amenities-d.png`, `20a-amenities-flyto-mid-d.png`, `20b-amenities-level-d.png`, `20c-amenities-3d-plan-d.png`, `20d-amenities-3d-pitched-d.png`, `20e-amenities-walk-d.png` | The camera swings to the pool-deck side. There is one "Amenities" card with a thumbnail. Clicking it flies to the podium, shows an "Amenities" pill and breadcrumb, and a Floorplan button. Floorplan opens a 3D plan of the amenity level (pool, loungers, bar, lounge), then a pitched version, then a walk (lobby corridor). | No per-amenity hotspots or cards. The amenity renders live only in the Gallery. |
| 12 | `21a-idle-movie-sheet-unit-d.png`, `21b-idle-movie-sheet-exterior-d.png`, `21c-idle-movie-facade-boat-d.png`, `21d-idle-movie-unit-glide-d.png` | After 5 idle minutes the UI hides. A logo and a caption appear and the camera tours by itself: a slow glide over a furnished unit (1604), fade to dark, facade close-ups with a boat sailing past, exterior orbits, and an "Amenities" shot. Any click stops it. | This is the attract mode for sales-centre screens (code: `inactivityThreshold = 300000`, `triggerMovie`). |
| 13 | `22-list-d.png`, `23-list-sorted-by-price-d.png`, `23b-list-row-click-selects-unit-d.png` | A full-width table of all 94 units. Columns: unit, beds, baths, m², ext m², int m², type, parking, price/status, and a "Request Quote" button per row. The unit column stays frozen. Sorting by price puts 1704 at MX$8,449,000 first. Clicking a row closes the list, flies to the unit and opens its card. | Sorting and row clicks work. |
| 14 | `24-filter-status-colorcode-d.png`, `25-filter-2bed-d.png` | "Status" paints every available unit green on the facade; the unavailable penthouses stay plain. "2 Bed" lights only the 2-bed units (floors 17–24 on the south face) and filters the sidebar. | Only one chip is active at a time: choosing "2 Bed" turned "Status" off (code). |
| 15 | `26a-card-click-camera-flyto-sheet-d.png`, `26b-card-click-flyto-arrived-d.png` | Clicking a sidebar card (2403) makes the camera dolly in with easing and frame the filtered block. The pill "2403" appears on the facade. | About 1 s eased fly-to. |
| 16 | `27-location-d.png` | Google Maps satellite with a red pin and Google's default business POIs (restaurants, Walmart, schools). No curated categories, distances or travel times. | Pan and zoom like any Google map. |
| 17 | `28a-gallery-empty-first-5s-d.png`, `28-gallery-d.png`, `29-gallery-interiors-d.png`, `30-gallery-image-viewer-d.png` | Three group tiles (Exteriors, Interiors, Amenities) that stay **blank for 5–8 s**, then renders. Interiors are per type, with Spanish names in the English UI ("Comedor XG"). The lightbox has arrows. | Tiles load one by one, with no placeholders. |
| 18 | `31-favorite-added-tab-appears-d.png`, `32-favorites-view-d.png` | Tapping the heart on a card adds a new "Favorites" tab to the header. The Favorites view lists the saved units and frames the tower. | Stored in localStorage (`{project}_favs`). No compare. |
| 19 | `33-share-popup-d.png` | Copy link, Facebook, LinkedIn, Twitter (old bird) and WhatsApp. The link is a per-unit deep link, `/Nivel24/Dpto2404`, with the text "2404 - Olae Tower". | Observed only (window.open stubbed). |
| 20 | `34-contact-us-embedded-dev-site-d.png`, `35-request-quote-embedded-dev-site-d.png` | Both open **the developer's homepage (olaetower.mx) in a full-screen iframe** with a close X. The unit is not passed, so the buyer must start over. | Closed without touching anything. |
| 21 | `36-sidebar-collapsed-turned-d.png` | Turn buttons rotate the view in fixed steps with easing. The sidebar collapses to give a clean full view. The compass shows N/E/S/W. WhatsApp opens `wa.me/52…?text=Hello, I'm interested in Olae Tower!` with no unit in the text (code; number masked here). | – |
| 22 | `37-bug-views-tab-stuck-in-interior-d.png`, `38-bug-amenities-plan-stuck-on-exterior-d.png` | **Bug 1:** after the walk, switching to "360 Views" and then "Exterior" left the canvas stuck in the interior. "Back" dumped me to the language gate, and only a reload fixed it. **Bug 2:** once (after the idle movie), the amenities Floorplan kept showing the exterior. It worked in a fresh session. | This is state-machine fragility. |

### Phone (390×844, DPR 2, touch)

| # | Screenshot(s) | What the user sees / does |
|---|---|---|
| 1 | `40-landing-p.png`, `41-disclaimer-p.png` | The same two gates, stacked vertically. |
| 2 | `42a-cold-load-sheet-p.png`, `42b-cold-load-late-frames-p.png`, `42-exterior-home-p.png` | Grey tower about 4.5 s after agree, and still untextured 20 s after agree. **The download stalled for about 25 s at 34 MB.** The next frame I captured, 93 s after agree, was finished; the exact moment in between was not captured. Layout: back and WhatsApp/Contact/Fullscreen at the top, horizontal filter chips, the tower, compass, a collapsed unit card peeking above a bottom tab bar (Exterior, Amenities, 360 Views, List, Location, Gallery). |
| 3 | `43-swipe-rotate-p.png`, `44-pinch-zoom-p.png` | A one-finger swipe orbits and a pinch zooms, both smoothly. |
| 4 | `45-tap-unit-p.png` | Tapping the facade selects 1601 (green segment and pill). The bottom sheet expands into the full unit card with Keyplan / Floorplan / Request Quote. |
| 5 | `46-floorplan-2d-p.png`, `47-unit-dollhouse-p.png`, `48-interior-tour-p.png`, `49-interior-tour-swipe-p.png` | The same five-mode rail down the left side. The walk works by swipe. |
| 6 | `50-360views-p.png`, `51-list-p.png`, `52-location-p.png`, `53-gallery-p.png`, `54-contact-us-p.png` | Everything is present on the phone. The list scrolls sideways with a frozen first column. The Google map and gallery were slow to fill (the first shots were empty). Contact is again the developer's site in an iframe. |

On the phone profile the canvas rendered at 390×844 backing pixels on a DPR-2 screen, so the image is visibly soft. That is because Hauzd enables native pixel density only for GPU tier 3, and this profile was classified tier 1 "FALLBACK" (code).

---

## 3. Tech stack, with evidence

| Layer | What it is | Evidence (URLs, types, sizes) |
|---|---|---|
| App shell | A 1,284-byte HTML page. Inline config lists 4 content packs: `twin` (model), `twinmap` (surroundings), `twinpresent` (UI, gallery, drone shots), `twinsales` (prices, forms). Also `monoArch:"ibf"`, `monoBuilds:["Raw","Pvr","Etc2","Dxt","Bc7","Astc"]` and `hauzdPlatform="EMSCRIPTEN"`. Version path `/2.01.0092/`. | `GET https://olae-tower.hauzd.app/` (text/html, 1.3 KB). No meta description, no OG, `<title>Olae Tower</title>`. |
| UI layer | About 40 vanilla-JS modules (`appPopup`, `appSidebar`, `appList`, `appFilters`, `appMovie`, `appXR`, `appStudio`, `appLive`, `Hauzd.js`, `Twin.js` and others), with no framework. The UI is HTML/CSS overlaid on the canvas; the unit pills are HTML projected from 3D. | `/2.01.0092/js/*.js`, about 0.4 MB gzip in total. CSS: 4 files, 31 KB. Fonts: Poppins ×3 plus SF NS Display OTF, 320 KB. |
| 3D engine | A proprietary C++ engine compiled with Emscripten. JS and C++ talk through a JSON message bridge (`ivanSend`, `Module._ivanExchange`). It draws with WebGL 2 on `canvas#canvas`. rAF measured 60.5 fps on the iGPU. The same core runs their iOS, Android and Windows apps; the web UI is reused through `hauzdPlatform`. | `HauzdApp2Job.wasm` 820 KB gzip, 2.05 MB decoded. `HauzdApp2.wasm` 42 KB gzip, 113 KB decoded. Glue `HauzdApp2.js` 73 KB and `HauzdApp2Job.js` 51 KB. `Module` keys: `_main`, `_malloc`, `ivanExchange`, `pauseMainLoop`… |
| GPU tiering | `detect-gpu` benchmarks with tiers at 0/50/100/150 fps. Memory hint comes from `navigator.deviceMemory`. Native pixel density only on tier 3. | `/js/detect-gpu/detect-gpu.umd.js`, `/benchmarks-min/d-amd.json` (72 KB). Phone profile: `{tier:1, type:"FALLBACK"}`, canvas 390×844 at DPR 2. |
| 3D content | A proprietary **`.ibf` chunked binary pack format**, gzip, `Content-Type: application/x-binary`, streamed progressively. Textures come pre-compressed in six GPU formats, picked per device; desktop AMD got **BC7**. They use no glTF, Draco, KTX2 or Basis. | `https://incdregprod-us-east-1.s3.amazonaws.com/{proj}/m/{monoUuid}/Bc7/shared/d.ibf{0…59}`, chunks up to 19.6 MB each. Per-scene packs: `/Bc7/s/s_2/p/{sceneId}/d.ibf{n}`. Unique data seen: **859 MB** (shared 633 MB; exterior scene p325 82 MB; map context p18 35 MB; unit/level scenes 1–33 MB each). |
| Lighting and look | Baked lightmaps (`floorGenBakeBgt` "Floorplan gen. light map size"), per-scene exposure (`ev100`, limits), tone mapping (average, contrast, desaturation, with separate walk values), bloom, "FX sun" post effect, background blending of drone shots and the surroundings scene. | `twin.json` propDefs (309 properties); scene JSON per node (`ev100`, `toneAvg`, `postSun`, `seqAsset4K/8K`). |
| Drone views | 11 `Image360` gallery entries with position and azimuth. **p01–p10** sit at x −0.8, y −6.33 (the tower's own axis), **z = 19, 26 … 82 m**. **PA** is an aerial at (−63, 150, 85 m), azimuth 215. Low, 4K and 8K variants; 8K only on desktop with MAX_TEXTURE_SIZE ≥ 8192. The engine blends the nearest shot behind the model (`DroneBlend`), and that includes the walk's windows. | `twinpresent` JSON `570e23b1…json` (30 KB). `appRender.js` droneViews logic. `appDefault.js` `viewCamConfig:"DroneView"`. |
| Project data | JSON snapshots on S3: the model/scene graph (265 KB and 370 KB, 581 nodes with beds, baths, areas, type, renders), sales (15 KB: 94 units with `sku`, `priceMxn`, `status`; 91 available and 3 unavailable; MX$4.69M–14.61M) and forms (9 KB). | `…/0800ef67…/ssales/s/26a55886….json`, `…/sforms/s/d1e35a0f….json`, `…/62e60818…/s_2/s/42f048f9….json`, `/2.01.0092/js/twin.json` (120 KB; prices in 10 currencies **including ILS**). |
| Live updates | The app POSTs to a live endpoint every 10 s and a projects endpoint every 30 s. Snapshots are cached in localStorage and applied without a reload. | `https://p5wfdzg8uh.execute-api.us-east-1.amazonaws.com/Prod/v1/app/live` (about 3.9 KB each). `https://n3qydg3m0a.execute-api.us-east-1.amazonaws.com/Prod/v1/app/projects` (about 2.7 KB). |
| 2D images | Unit-type thumbnails ship as a JPG plus a separate JPG alpha mask. Gallery renders are JPG/PNG. | `…/a/{alone}/s_2/p/{id}/AssetImage.jpg` (45–52 KB) plus `AssetImageAlpha.jpg` (14–16 KB), ×13. |
| Map | Google Maps JS, satellite with default POIs. | DOM: "Map data ©2026 INEGI Imagery ©2026 Airbus, CNES / Airbus, Maxar", "Keyboard shortcuts". |
| Lead and contact | Forms are configured as `isThirdParty:true`, `baseUrl:"https://olaetower.mx/"`, `embed:true`, shown in an iframe. Their own form engine (with `unit_id` fields) exists, but those forms are marked deleted or inactive in this project. A Reserve form type exists in code (`FormReserve`) but is not configured here. | `sforms` JSON. `appApply.js` (`doReserveBtn` is disabled when no FormReserve exists). |
| Share and favourites | `shareon` popup with per-unit deep links. Favourites live in localStorage. | `shareon.min.js`. The `…_favs` key holds `{"favs":[1266]}`. |
| Analytics | GA4 `G-6FZD2TYYNJ` and Google Ads `AW-950833889`, with events `page_view` (project_slug, node_type, node_id, node_name), `button_click` and `camera_interact`. | Network log. |
| Other capabilities in code (not shown in this project) | WebXR immersive-vr and immersive-ar (the AR button appears only on supporting devices); stereo mode; `/studio` route for making renders and videos (camera, FOV, bloom, tone map and LOD set from the URL); `/download` and `/launch` routes for native apps; `ledsSP108E` settings that light an LED physical model in a sales centre; 4K/8K render outputs. | `appXR.js`, `app.js` (isSessionSupported), `Hauzd.js` (studio params), `twin.json` (ledsSP108E group). |
| Absent | No time-of-day or sun control, no sound, no compare, no brochure, no reservation or payment in this project. | UI checked (eyes). Code: no time-of-day in the UI layer; no audio requests. |

**Load and weight**

This machine: AMD iGPU, fast broadband, Israel to us-east-1.

- **Shell:** DOMContentLoaded 1.0 s, load 2.8 s; engine WASM in by about 3.7 s. Shell plus engine is 1.9 MB. The 3D stream starts about 5 s after the page opens, before any click: 62 MB by the first click and 122 MB by "I agree" in session d1.
- **Desktop cold start:** geometry about 6 s after agree, full materials about 17 s, drone backdrop (the finished look) about 21–23 s.
- **Phone profile:** grey model about 4.5 s after agree, still untextured at 20 s, and a 25 s download stall at 34 MB. It was finished by my next frame, at 93 s; the exact moment was not captured.
- **Session totals:**
  - fresh desktop, 15-minute walk: 811 requests, **659 MB** (612 MB of it `.ibf`)
  - long desktop session, 25 minutes: **1.0 GB** transferred, 865 MB unique
  - phone profile, 8 minutes: **532 MB**
  - streaming runs at about 50–185 MB per minute during use
- **nad-lan Rainbow, for contrast:** the whole desktop page is **6.4 MB** (268 requests), with the 3D at about **0.33 MB** (three.js r170 264 KB, `stage.js` 42 KB, OrbitControls/GTAO add-ons). DOMContentLoaded 1.8 s, load 3.2 s. The phone session with 3D interaction was 1.85 MB.

---

## 4. Every feature: is it cinematic, and how is it built

| Feature | Cinematic? | How it is built | Evidence |
|---|---|---|---|
| Language gate, then disclaimer gate | No, but the gates hide the preload | HTML popups; `.ibf` streaming starts behind them | eyes 01, 02; code |
| Intro establishing move | **Yes**: slow push-in, surroundings blurred (depth of field) | Engine camera animation after "I agree"; context blurred behind a sharp tower | eyes load frames, 03 |
| Photoreal tower in a real drone context | **Yes** | Textured model, baked lighting, tone mapping and bloom; drone 360 blended as the background; a separate `twinmap` pack for neighbouring buildings | eyes 03, 18; code |
| Orbit, zoom, turn buttons, compass | Eased; soft | Mouse drag, wheel, touch swipe and pinch; step-rotation buttons (`snapRotation` setting); zoom limits per scene (`minZoomMag`/`maxZoomMag`, `limDel*`) | eyes 04, 05, 36, 43, 44 |
| Hover highlight per unit | **Yes**: soft translucent fill plus pill | Per-unit zones in the engine; the pill is HTML projected from 3D | eyes 06, 08b |
| Select a unit, fly-to, card | **Yes**: about 1 s eased dolly | `?selRelAddr=Nivel14/Dpto1401`; HTML card; breadcrumb | eyes 07, 26a |
| Status colour on the whole facade | **Yes**: the building becomes a heat map | colorCode config plus the live sales JSON | eyes 24 |
| Filter chips light matching units | **Yes** | Filter config; the sidebar filters too | eyes 25 |
| Unit card fields and similar unit | No | HTML from the property definitions; one suggestion per card | eyes 07; code |
| Breadcrumb Project \ Floor \ Unit | No | HTML buttons (`addr_0…2`) | code |
| Keyplan (floor plate, pills, hover) and pitched stack | **Yes**: the camera drops to the plate | Same scene, camera preset; `isPitched=1` | eyes 08, 08b, 09 |
| 2D plan and 2D with dimensions | No | 2D plan asset (`asset2d`/`seq2d`) drawn in the engine canvas, with a dimensions overlay (`show2d`, `showDim`) | eyes 10, 11 |
| Furnished 3D top-down and dollhouse | **Yes**: smooth mode transitions | Same unit scene, different camera | eyes 12, 13 |
| First-person walk | **Yes** | Eye height 1.5 m; click-to-walk glide with a ring cursor; drag to look; URL keeps `tourPos`/`tourCamUV`; windows show the drone shot. No keyboard or wheel. | eyes 14–17b, 48, 49 |
| 360 drone views | **Yes** | 10 stacked photos at 7 m steps plus 1 aerial, with the tower composited in | eyes 18, 19, 50; code |
| Amenities | Partly: camera swing and fly to the podium | One "Amenities" node with a 3D plan, pitched view and walk; no per-amenity hotspots | eyes 20–20e |
| Idle attract movie | **Yes**: the strongest cinematic piece | 5-minute inactivity timer; auto camera tours of units and exterior; fades; logo and caption overlay | eyes 21a–d; code |
| Price list | No | HTML table with a frozen column, sortable, Request Quote per row; row click flies to the unit | eyes 22, 23, 23b |
| Location | No | Google Maps satellite with default POIs | eyes 27, 52 |
| Gallery | No | HTML grid by group and a lightbox; lazy with no placeholders | eyes 28a–30, 53 |
| Favourites | No | Heart adds a Favorites tab; localStorage | eyes 31, 32 |
| Share | No | shareon with a per-unit deep link; no link preview | eyes 33; code |
| Contact / Request Quote | No | The developer's homepage in an iframe; unit context lost | eyes 34, 35, 54 |
| WhatsApp | No | `wa.me` with a preset message and no unit | code |
| Fullscreen and sidebar collapse | No | Buttons | eyes 36 |
| Phone layout | – | Bottom tab bar, bottom-sheet card, same rail; lower render resolution | eyes 40–54 |
| AR/VR, LED model, Studio, native apps | – | In code, not shown here | code |
| Day/night, sound, compare, brochure, reserve | **Absent** in this project | – | eyes; code |

---

## 5. What nad-lan must build to be clearly above it (ranked)

Rules that apply to all items:
- **Location in code:** build inside `project-stage/<project>/` modules and never inside the frozen `showroom-engine` internals or the beam.
- **Honesty law:** unit data comes only from published sources, shown with a label. Unknown status is omitted, never invented.

1. **Unit-level picking on the facade (P0).**
   - **What:** split each floor ring into unit sectors from the published layout (units per floor × direction). Each sector is its own raycast target, as separate meshes or an instanced mesh with a per-instance colour attribute.
   - **States:**
     - idle: invisible
     - hover: translucent emissive fill of about 35% plus an HTML pill with the apartment number or type
     - selected: stronger fill, outline and pill
     - filtered-in: fill
     - unknown: hatched grey
   - **Test:** 60 fps on this iGPU; one-tap pick on a phone with a hit area of at least 44 px.
   - **Why:** this is Hauzd's core move (06, 07). nad-lan today picks floors only.
2. **One camera director with eased fly-to (P0).**
   - **What:** target, distance, azimuth and pitch, cubic ease-in-out over 0.9–1.2 s, interruptible.
   - **Presets:** establishing shot, unit close-up, floor plate, pitched floor, walk start, and a 4–6 s intro push-in on first view.
   - **Idle loop:** the same director drives an attract loop for `?present=1` kiosk and sales-office screens (Hauzd's movie, 21a–d).
3. **Unit card, URL state and deep links (P0).**
   - **Card:** a left panel on desktop and a bottom sheet on phones. Fields: apartment or type, rooms, m², balcony, floor, direction (compass), and a public price range where published.
   - **Deep links:** every view has a URL (`?u=…&mode=plan|dollhouse|walk|view&cam=…`).
   - **Link previews:** a server-rendered OG image per floor view and unit type. Hauzd has no preview at all.
   - **WhatsApp:** prefilled with project, floor, direction, unit or type, and the deep link. This beats Hauzd's context-free message and its iframe that loses the unit.
4. **Real view per height: a drone 360° column per flagship (P0 for flagships).**
   - **Capture:** a vertical column every 6–7 m, about 2 floors, from the first residential floor to the roof, plus one aerial. Geotag x, y, z and azimuth. Get the CAA permit and blur for privacy. The honest caption gives the capture date and height.
   - **Pipeline:** equirectangular photos converted to KTX2 cubemaps, 2K for phones and 4K for desktop.
   - **Engine:** pick the nearest height for the selected floor and crossfade in 400 ms.
   - **Where it shows:** in the "view from the floor" panel (upgrading today's Mapbox approximation, which stays as the labelled fallback) and later through the walk's windows. This is exactly Hauzd's mechanism (p01–p10).
5. **Plans rail with five modes (P1).**
   - **Modes:** 2D vector plan (SVG) with a dimensions toggle, furnished 3D top-down, pitched dollhouse, and walk, all on one rail. The camera stays continuous between modes.
   - **Assets:** one GLB per unit type (meshopt or Draco plus KTX2), at most about 3 MB, loaded on demand. The source is the published sales plans, labelled "לפי תוכניות שיווק".
6. **First-person walk (P1).**
   - **Movement:** a navmesh raycast for click-to-walk with a ring cursor and an eased glide; drag to look. Add what Hauzd lacks: WASD, arrows and wheel on desktop, tap-to-walk plus an optional gyroscope on phones.
   - **Views:** the windows show the drone image from item 4.
   - **Lighting:** baked lightmaps, or Gaussian splats of a real show apartment where one exists.
7. **Filters that paint the building, plus a sortable list (P1).**
   - **Chips:** rooms, floor range, direction, balcony and price band. Matching units light up on the facade and the rest fade.
   - **Table:** a frozen first column; a row click flies to the unit; an honest empty state.
   - **Data:** published data only.
8. **Full-screen theater mode (P0 UX).**
   - **Theater:** one button expands the 3D to 100vw × 100svh with overlay UI; Esc or Back returns to the article.
   - **Wheel:** zooms only inside the theater. Today the wheel scrolls the page.
   - **Phone:** a bottom tab bar and bottom sheet. The disclaimer caption collapses into an (i) chip so it never covers the model; today, caption plus floor card cover about half of the 3D on a phone (67).
9. **Visual fidelity pass (P1).**
   - **Materials:** glass with environment-map reflections, and real railings and balcony depth.
   - **Scene:** instanced vegetation, AgX or ACES tone mapping, subtle bloom, and depth of field on the context.
   - **Context:** either textured city context (photorealistic 3D tiles or block photogrammetry) or a deliberate premium stylised look. Today's beige boxes read as a sketch next to 03.
   - **Time of day:** keep GTAO and add a real sun path (sunrise to night, with lit windows at night). Hauzd has none, so this is an easy, visible win.
10. **Weight budget as a selling point (P0 guardrail).**
    - **Budget:** first interactive view at most 10 MB and 3 s on 4G; a whole session at most about 80 MB; progressive levels of detail; everything else lazy.
    - **Pitch:** contrast this openly in developer pitches with Hauzd's 600 MB per visit.
11. **Amenity hotspots (P1).** Pins on the pool, lobby, gym and roof that fly the camera there and open a card with a render, 360 or video. Only verified amenities; no inventing (Hauzd has one generic "Amenities" node).
12. **Neighbourhood layer inside the 3D (P1).** Bring the existing POI categories, nearby ₪/m² markers and future-plan footprints into the 3D scene as anchored labels, with walking-time rings. Hauzd offers only a Google map (27).
13. **A robust mode state machine plus this GPU regression harness (P0 quality).**
    - **State machine:** modes exterior ⇄ floor ⇄ unit ⇄ plan ⇄ walk ⇄ view, all reversible. Back goes one step, never to a gate. This avoids Hauzd bugs 37 and 38.
    - **Harness:** run the Playwright real-GPU harness from this study (desktop and phone) on every release, with a screenshot of every mode.
14. **Leads and analytics with context (P0 business).**
    - **Lead sheet:** stays inside the experience and carries floor, direction and unit plus the deep link.
    - **Analytics:** events per interaction (`unit_hover`, `unit_select`, `mode_change`, `view_open`, `lead_click`), feeding a developer report. Hauzd sends only `button_click` and `camera_interact`.

**Do not copy:**
- two gates before any 3D
- 600 MB streaming
- a homepage in an iframe for leads
- broken number formatting
- mixed languages
- no link previews

---

## 6. What the earlier notes got wrong or missed

**`competitor-profiles/hauzd.md` (20.8, marketing-site scrape)**
- **Time of day.** It said the twin has "time-of-day". **Not in Olae**: no UI and no time-of-day code in the web layer, only a post-processing "FX sun" setting. nad-lan's sunset/noon toggle is ahead here.
- **Filters.** It listed "Smart filters … price / bedrooms / orientation / view / availability". **Overstated**: Olae has only Status plus four bedroom-type chips. There is no price, direction or view filter.
- **Reservation and payment.** It said "Reservations + online payments inside the showroom". **Not seen**: the platform has a Reserve form type, but this project has none. Contact and quote are the developer's homepage in an iframe.
- **CRM sync.** It said "CRM/ERP-connected inventory". **Partly confirmed**: a live endpoint is polled every 10 s and price and status are per-unit data that can be updated live. Whether a CRM feeds it cannot be seen from outside.
- **Drone views.** It said "360° drone views … per-unit real view". **Confirmed, and the mechanism was missed**: a vertical column of 10 drone 360s every 7 m on the tower's own axis plus one aerial, composited behind the 3D model and shown through the walk's windows.
- **Israel.** It said "No evidence anywhere" of Hebrew or Israel. **Nuance**: the data model includes a price field in Israeli shekels (`priceIls`). The UI languages seen were only EN and ES.
- **What it missed entirely:**
  - the custom C++/WASM engine (not Unity)
  - hundreds of MB of streaming per visit
  - GPU-tiered texture builds in six formats
  - the idle attract movie
  - WebXR AR/VR hooks
  - LED physical-model control
  - the Studio mode for renders and videos
  - per-unit deep links for every view
  - favourites
  - GA events per camera move
  - no SEO or OG at all

**`competitor-profiles/hauzd-gap-analysis.md` (20.8, Palmanova)**
- **Canvas features.** Everything marked "[canvas]" was left unverified because nothing could be screenshotted. It is **now seen**, see sections 2 and 4.
- **Location.** It said "Location: map scene [canvas]". **Wrong for Olae**: it is an embedded Google Maps satellite view with default POIs, not a 3D scene.
- **Gallery.** It said "Gallery: renders [canvas]". **Wrong**: it is an HTML image grid with a lightbox, and it loads slowly.
- **Amenities.** It said "Amenities: dedicated amenity walk". **Partly**: the camera swings to the podium, and there is one amenities floor with a 3D plan, pitched view and walk. There are no per-amenity stops.
- **Similar units.** It said a "similar units carousel with 20+ alternatives". **Not here**: Olae shows one "similar unit" per card.
- **Info tab.** It listed an "Info" in-app story page. **Absent in Olae** (the header has no Info).
- **What it missed:**
  - **The facade is the interface.** Hover and select on each unit's segment, status colouring of the whole building, and filters that light the building.
  - **Fly-to.** A camera fly-to on every click.
  - **Five-mode plan rail.** One rail from plan to walk.
  - **The walk.** It is real-time 3D with click-to-walk, not panorama hops.
  - **Attract movie.**
  - **Numbers.** Load times and data weight.
  - **Bugs.** Stuck interior state, Back to the language gate, blank gallery, a Request Quote that loses the unit, broken decimals, Spanish leaking into English.
- **Still correct:** Hauzd's pages are invisible to Google, with an empty 1.3 KB shell, no description and no OG. That is still nad-lan's strategic wedge.

---

## 7. nad-lan Rainbow today vs Hauzd: where we are below (and above)

Checked live: `https://nad-lan.co.il/projects/rainbow-tel-aviv/?nlv=1`, desktop and phone, same GPU method. Screenshots 60–68.

**Below Hauzd today**
1. **Granularity.** We pick **floors, not units**. The hover card is the same generic text on every floor ("קומה 30 · בפרויקט דירות 2 עד 5 חדרים, לפי פרסומי השיווק"), with no apartment, area, price or status (62, 63). Hauzd picks each of 94 units with status colour (06, 24).
2. **Fidelity.** Our model is procedural massing: white rings, beige extruded boxes for the city, no textures (61). Hauzd shows a photoreal textured tower inside a real drone panorama (03).
3. **Stage.** Our 3D is a 1082×646 box in the middle of a scrolling page. The wheel scrolls the page instead of zooming, and there is no full-screen mode. Hauzd is full-screen with a dedicated UI.
4. **Plans.** We show no plans in the 3D. Hauzd has five modes: 2D, dimensions, 3D top-down, dollhouse, walk (10–13).
5. **Interior.** This page has no interior at all; the designer tool is on a separate page, `/tour/designer/`. Hauzd has a furnished first-person walk with real drone views in the windows (14–17b).
6. **View from the floor.** Ours is a Mapbox satellite camera at about 86 m, honestly captioned and draggable, but map-grade with labels and icons (64, 64b). Hauzd's is a real drone photograph from the tower's own position at that height (18, 16).
7. **List and filters.** We have no unit list and no filters on the 3D. Hauzd has a 94-row sortable price list and filter chips that paint the facade (22–25).
8. **Unit actions.** We have no favourites, compare or share per unit, and no deep link that reopens the exact view. Hauzd deep-links every state, even the walk position.
9. **Motion.** We have one floor fly-in, which is good (63), but no intro shot, no eased unit fly-to and no attract loop. Hauzd has all three (21a–d, 26a).
10. **Phone.** Our caption box plus the floor card cover about half of the 3D (67). Hauzd uses a bottom sheet and bottom tabs, so the model stays visible (45).
11. **Amenities.** We have none in 3D. Hauzd has a podium plan, pitched view and walk (20c–e).

**Above Hauzd today** (keep and advertise these)
- **Speed and weight:** 6.4 MB for the whole page and about 0.33 MB for the 3D, with no gate; the 3D was already rendered in the first screenshot, 8 s after navigation. Hauzd needs two gates, about 22 s to the finished image on desktop (longer on the phone profile) and 530–660 MB per visit.
- **Findable in Google:** the page is indexable Hebrew content (article, data table, FAQ, sources; 68). Hauzd is an empty shell.
- **Neighbourhood data:** categorised POIs with counts (education 17, parks 16, transport 16…), nearby ₪/m² markers, a future-plans layer, and a view cone on the map (64). Hauzd has only a default Google map.
- **Honesty:** captions everywhere, as the law requires. Hauzd shows one disclaimer at the gate, then numbers with broken decimals.
- **Languages:** 5 (HE/EN/FR/RU/AR) against 2.
- **Sunset/noon lighting toggle** (63b). Hauzd has none in this project.
- **Broker WhatsApp card and ecosystem tools:** quarter tour, earth flight and apartment designer.

---

## 8. Reproducibility and raw data

- **Harness:** a persistent Playwright driver with a file command queue: `driver.py` and `send.py`, with `dom.py`, `netsum.py`, `sheet.py` and `psheet.py` for analysis. It is in this session's scratchpad (`…/scratchpad/hauzd_work/`) and **is temporary**: move it to `nad-lan-co-il/tools/` if it becomes the release regression harness (item 13).
- **Raw logs** (network JSONL, CDP sizes, perf entries) and Hauzd's public JSON config are in the same scratchpad folder. They were not copied into the repo on purpose (they are third-party data); the findings above cite them.
- **Launch flags that give real GPU rendering headless:** `channel="chrome"`, `headless=True`, `--use-angle=d3d11 --ignore-gpu-blocklist --enable-gpu`. Verified renderer: `ANGLE (AMD, AMD Radeon (TM) Graphics … Direct3D11)`.
