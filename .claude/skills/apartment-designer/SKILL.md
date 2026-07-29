---
name: apartment-designer
description: Maintain and extend the cinematic 3D apartment designer (experience/apartment-designer) - walk a sample apartment, style surfaces, leave notes for the developer, place furniture, and run the end-to-end MOCK buying flow. Use when the owner asks for designer upgrades, new rooms/materials/furniture, flow changes, or publishing it.
---

# Apartment Designer — the "design it, note it, order it" experience

One self-contained file: `experience/apartment-designer/index.html` (three.js 0.160 +
GSAP from CDN, procedural everything, zero asset downloads). Branches:
`claude/apartment-designer-v1` (tour + styling), `claude/apartment-designer-v2`
(adds notes, furniture, mock buy flow). NOT live, noindex, never linked from the
site until the owner says so. Production site ships from `claude/plugin-handoff`
— never touch it from here.

## 1. Architecture map (V2, top to bottom of the file)

- **Header comment** — research references + the 12-point interaction recipe.
  Keep updating it; it is the design law of the file.
- **CSS** — glass/gold luxury system on CSS vars (`--gold`, `--ink`, `--glass`).
  Blocks in order: shell/poster/topbar/dock, palette sheet + `#noteArea`,
  furniture (`#furnBtn`, `#furnBar`), buy flow (`#flow*`, `.fs/.fc` progress,
  `.fstep`, pay card, success, `#confetti`). All tap targets >=44px, RTL.
- **Markup** — `#stage` canvas, `#shell` loader, `#poster` entry, `#topbar`
  (brand + `#styleBtn` opens the flow), `#hint`, `#dock` (mood seg + `#furnBtn`
  + room bar), `#sheet` (swatches + note field), `#furnBar` toolbar, `#flow`
  (4 steps), `#confetti`, `#toast`, `#veil`, `#fallback`.
- **JS module** (single IIFE, try/catch to `#fallback`):
  - renderer/scene/PMREM; procedural canvas textures (wood/stone/terrazzo/
    deck/plaster/art).
  - `OPTS` — curated per-surface options (wall/floor/sofa/kitchen), `LOOKS`
    presets, `choices` state.
  - **`T` dict** — ALL V2 strings (notes/furniture/flow). EN path: ship a
    translated `T`. V1 strings are still inline Hebrew — accepted gap.
  - **`ELEMENTS`** — note-target registry: 4 design cats + 6 door/window ids,
    each `{label,anchor,[noteOnly],[door]}`. `notes{}`, `furniture[]`,
    `contact{}` state.
  - materials (shared `MeshStandardMaterial`s) then merged-geometry apartment
    shell; **doors/windows are separate meshes** (`doorLeaf, bathDoor,
    mamadDoor, balcDoor, winBed, winKit`) so they raycast individually.
  - exterior world (sky/sea shaders, instanced city), lights, `MOODS` +
    `applyMood` (sun/sky/sea/exposure/lamps tween together).
  - **rails**: `NODES` waypoint graph + `EDGES`/BFS `findPath`; `gotoRoom`
    glides a CatmullRom(centripetal .5); `LOOKS_AT` pano anchors; reduced
    motion cuts through `#veil`.
  - hotspots: `HOTSPOTS` (design rings, nav arrows, V2 `note` rings on
    windows/slider), sprite build + per-room refresh + pulse.
  - **V2 badges**: `syncBadge(id)` gold ✎ sprite at `ELEMENTS[id].anchor` or
    above a furniture item when `notes[id]` exists.
  - **V2 furniture**: `FURN` catalog (8 kinds; each `build()` returns a Group
    of <=2-3 merged meshes reusing shared materials — sofa follows the sofa
    fabric, lamp shade joins the mood lamp glow). `ROOM_RECTS` placement
    bounds + `fitSpot/clampSpot`; `placeFurn/moveFurn/deleteFurn/selectFurn`;
    gold `selRing` + `rotHandle` (drag rotates, `#fRotate` steps 45°);
    `FURN_LIMIT=12` protects the draw-call budget (<=140).
  - pointer: furniture grab/rotate beats camera-look; tap routing:
    placement tap -> sprite (nav/note/design) -> furniture -> noteId mesh ->
    design cat. `castAt` raycasts sprites+targets+furniture.
  - sheet: `openSheet(cat)` swatches + bound note field; `openSheet('furniture')`
    tray; `openNoteSheet(id)` note-only mode; notes flush on close.
  - **V2 flow state machine**: `FLOW_STEPS=['summary','details','pay','done']`,
    `setFlowStep/openFlow/closeFlow`. Summary rebuilds thumbnails via
    `snapRooms()` (4 offscreen renders, camera restored). `validateDetails`
    (name>=2, IL phone, optional email). Pay is a **MOCK** (`payment.simulated
    :true`, demo ribbon on every step, prefilled dummy card, nothing sent).
    `completeOrder` -> ref `NDL-xxxxxx`, `buildPayload`, `buildWa`, confetti.
  - **storage**: `nadlan-apt-designer-v2` (choices, mood, element notes,
    furniture incl. per-item note, contact), debounced autosave, v1-key
    migration, restore rebuilds furniture + badges.
  - entry film, resize/fov, tick (sea/curtains/motes/pulse/inertia),
    `window.__APT` QA hooks (calls/fps/goto/place/addFurn/note/flow/pay/
    payload/reset — everything scriptable headless).

## 2. RFP payload contract (what "the developer receives")

`__APT.payload()` after a completed mock order:

```json
{ "type":"nadlan-apartment-designer-rfp", "version":2, "demo":true,
  "ref":"NDL-XXXXXX", "ts":"ISO",
  "unit":{"project":"רובע שדה דב · תל אביב","model":"דירת 4 חדרים · דירת דוגמה",
          "view":"נוף לים","disclaimer":"הדמיה להמחשה בלבד — ..."},
  "mood":"sunset",
  "palette":[{"cat":"wall","label":"צבע הקירות","pick":"חול חם","idx":1},...],
  "furniture":[{"id":"f1","kind":"armchair","label":"כורסה","room":"סלון",
                "x":-1.2,"z":-1.9,"ry":0.79}],
  "notes":[{"el":"door-entry","label":"דלת הכניסה","text":"..."}],
  "contact":{"name":"","phone":"05XXXXXXXX","email":""},
  "payment":{"simulated":true,"line":"מקדמת עיצוב — סימולציה",
             "amountILS":2500,"charged":false} }
```

Consumers (future real backend / WhatsApp bridge) must treat `demo:true` as
non-binding. Keep the shape backward-compatible; bump `version` on change.

## 3. How to extend

- **Room**: add `NODES` position + `LOOKS_AT` anchor + `EDGES` links + room
  chip button + `ROOM_ORDER`; add geometry via the `B/RB/CYL/P` helpers into
  the shared material arrays; add a `ROOM_RECTS` rect for furniture; add
  hotspots; add `T.roomNames` + `rectRoom` mapping; check `fovBias`.
- **Material option**: append to `OPTS[cat].items` ({n,hex} or {n,canvas,rep});
  3-6 options max per surface (conversion law); floor needs a texture in
  `floorTexs` (index-aligned). New surface cat = OPTS entry + mesh userData.cat
  + hotspot + apply branch in `applyChoice` + ELEMENTS entry.
- **Furniture kind**: add to `FURN` ({label,r,badgeY,build}) + `FURN_KINDS` +
  a `furnThumb` case. Build with `LB/LRB/LC/LS` into `fParts(mat,[geos])`,
  <=3 meshes, reuse shared materials. Keep the 8-item tray curated — swap,
  don't grow.
- **Note target**: separate mesh + `userData.noteId` in `initTargets` +
  `ELEMENTS` entry (anchor = badge position) + optional `note` hotspot ring.
- **Flow step**: extend `FLOW_STEPS`, a `.fstep` section, `#flowBar` node,
  `T.flowTitles`. Keep the demo ribbon visible on every step; the honest
  "no real charge" badges are owner law, not decoration.

## 4. Publish (when the owner says ship)

Upload `index.html` to wp-uploads exactly per the **quarter-experience skill,
section 3** (uPress specifics: temporary Code Snippets mime-override snippet,
`POST /wp/v2/media`, copy-over-canonical trick because WP suffixes duplicates,
purge LiteSpeed + healthcheck after). Compress `preview.png` to ~55KB for any
teaser embed (same skill, section 4). Keep `noindex` until the owner approves
public linking.

## 5. Next session must know (continuity contract)

- Owner laws: substance in chat; publish, don't hand off; benchmark against
  the world's best (god-mode skill); honest gaps stated every report.
- The mock flow is intentionally RECKLESS end-to-end per the owner ("like
  buying a car online; the RFP comes after the payment step") — blockers/
  legal gating come later; NEVER wire real payments without explicit owner
  approval and a compliance pass.
- Verify gate before any push: full flow (design->note->furniture->summary->
  details->mock pay->success->reload restore), 375px viewport, `?rm=1`
  reduced motion, ZERO console errors, `__APT.calls()<=140`,
  `node --check` on the extracted module.
- Honest gaps as of V2: V1 strings not yet in `T`; no undo for furniture
  delete; furniture ignores collisions with fixed furniture (simple rect
  bounds only); per-room thumbnails skip on WebGL context loss; no real
  backend — payload lives in the browser + WhatsApp text only.
