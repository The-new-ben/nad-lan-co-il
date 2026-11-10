# The apartment designer engine: architecture (HAD-703)

11.11.2026. Parent task HAD-701. Research this is built on: `docs/research/2026-11-10-apartment-designer/` (reverse: 78 measurable parameters and the white space; seo: intents, headings and slug; inventory: what we own).

This document fixes the shape of the engine before anything is built for the site. The working proof is the spike in `docs/design-lab/apartment-designer/spike/`. Nothing here is live.

## 1. The decision in one paragraph

One apartment is **one model**, and the plan and the 3D interior are two drawings of it. The model is two JSON documents: `nadlan-apartment` (the facts of the layout, written by us or the developer) and `nadlan-unit-design` (what one buyer changed). A design changes **only through operations** (move a piece, move a partition, set a finish). Every operation passes the rules first, then both views redraw the part that changed. The same operations are the undo stack, the decision log, the bill of quantities' input and, later, the messages of the shared video call. Nothing is kept twice, so the plan, the 3D, the spec sheet and the price can never disagree.

The old designer failed exactly here (inventory, section 4): an invented flat with no plan, and two design formats in two frames with no transform between them.

## 2. What the spike proved (measured 11.11.2026)

`node check-spike.mjs` presses the page like a phone user in headless Chrome over CDP: touch events at 390×844, device pixel ratio 2.625, on this machine's GPU (AMD Radeon, Direct3D 11). Receipt and screenshots: `spike/evidence/`. Core checks without a browser: `node test-model.mjs` (24 of 24).

| What | Result |
|---|---|
| Press checks (drag on the plan, drag in 3D, partition, blocked rules, floor finish, walk, undo, desktop) | 24 of 24 pass |
| Plan drawn, phone, cold cache | 0.27 s (slow 4G, 1.6 Mbps and 150 ms: 0.89 s) |
| First 3D frame, phone, cold cache | 1.70 s (slow 4G: 2.85 s) |
| Weight of the first 3D view | 345 KB in 17 requests (three.js 0.170.0 is most of it; a project page already holds that file) |
| A change on the plan reaches the 3D picture | 1.7 ms of work at the median, 1.9 ms at p95, 3.0 ms worst of 120; always shown in the next display frame |
| Moving a partition (rooms, areas, walls and floors rebuilt) | 5.0 ms median, 6.1 ms p95 |
| Render work per frame while orbiting | 1.4 ms median, 2.7 ms p95, 59 draw calls |
| The model alone (derive rooms from the wall graph, node) | 0.29 ms |

For scale: the first interior 3D view of the products we could open cost 12 to 21 MB (white-space item 10), and the target we set there is 4 s, 5 MB and 60 requests.

**What this does not prove yet.** (1) It ran on a desktop GPU with a phone-sized screen, not on a phone; headless Chrome also capped the display at 30 frames a second, so frame rate is reported as work per frame, not as fps. Real numbers need a mid-range Android and an iPhone (rubric section 7). (2) The spike has four small generated textures and box furniture. Real materials and furniture models add weight; the budget in section 8 is the limit they must fit in. (3) The room rule values (2.60 m, 8 m²) are placeholders marked "to be verified" inside the data.

## 3. The two documents

Schemas: `apartment.schema.json`, `design.schema.json` (JSON Schema 2020-12). The spike's example and a design written by the store both validate.

**Frame, everywhere:** centimetres, origin at the plan's top-left, x to the right, y down, rotation in degrees clockwise. 3D is the same frame in metres: X = x, Z = y, Y up. A piece at `rot` degrees on the plan has `rotation.y = -rot` in three.js. There is no second frame.

### 3.1 `nadlan-apartment` v1: the layout

- `nodes` (corners) and `walls` between them, each wall with a thickness and a **kind**: `facade`, `structural`, `mamad`, `shaft`, `partition`, `divider` (a line between two open spaces, no wall), `rail`. Only a partition can ever move.
- `openings` on a wall: door, window, sliding door or a plain opening, measured from the wall's a-end, with sill and head heights.
- `rooms` are **not outlines**. A room is a name, a type and one point inside it. The model finds the closed spaces of the wall graph and gives each the room whose point it contains. Outlines, areas and clear sizes are always computed. When a partition goes, two rooms become one space by themselves.
- `rules` with their source, `fixed` things (columns, shafts, drains), `view` (what the windows see), `source.kind` (`sales-plan`, `derived`, `schematic`, `example`) and its Hebrew label. The label is printed on every screen and every export.
- `geometry_revision`: changes when geometry changes. A design belongs to one revision.

### 3.2 `nadlan-unit-design` v2: the buyer's changes

- `geometry.walls`: partition id to its distance from the base position (absolute, so applying it twice changes nothing).
- `finishes`: surface key (`floor:living`) to a catalogue key, only where it differs from the base specification.
- `items`: pieces with `sku`, `x`, `y`, `rot` and a **status** badge: `base`, `upgrade`, `credit`, `decor`, `ai`.
- `notes`, and `log`: one line per finished gesture with who did it.

Version 1 documents (`inc/rfp.php`, `nadlan_rfp_clean_design`) stay readable. Their `plan2d` layer is already in this frame. Their `space3d` layer (metres from the centre, radians) converts only when the geometry revision is known: `x = cx + 100·x`, `y = cy + 100·z`, `rot = -ry·180/π`. Designs of the old invented flat (`sdedov-sample-2026-07`) are kept as they are and not converted: that flat is not any real unit.

## 4. The core (`model.js`)

No DOM and no three.js: it runs in the browser, in node tests and on the server side of the call.

- `derive(apartment, design)`: effective corners, walls, openings and rooms. A window or door keeps its place in the building when the corner beside it moves.
- `createStore(apartment, design)`: `apply(op, {by, gesture})`, `undo()`, `redo()`, `on(listener)`. A drag is one gesture: one undo step and one log line, however many moves it sent.
- Operations today: `item.add`, `item.move`, `item.rot`, `item.remove`, `finish.set`, `wall.shift`. Next: `opening.move` (interior doors), `partition.add`, `partition.remove`, `note.add`, `item.swap`.
- **Rules run before the change** and answer with a code and one Hebrew sentence the buyer sees:
  - a wall that is not a partition never moves (the sentence names why: façade, structure, safe room);
  - a partition slides only along the walls it meets, never out of a corner;
  - it cannot reach a window or a door; it cannot make a room narrower or smaller than the rule allows.
- `quantities(store)`: floor area per finish, room sizes, piece counts, and which rooms differ from the base specification. A pure function of the model, so the bill of quantities cannot drift from the picture.

## 5. The two views

Both subscribe to the store and never keep geometry of their own.

- **Plan (`plan2d.js`)**: SVG in centimetres. Walls drawn by kind the way a working drawing does (solid ink for structure, hatching for the safe room, hollow for partitions, blue for the ones that may move), door swings, glass lines, room names with computed areas, sizes in dimension red while a wall is dragged. Touch: drag a piece, drag a blue partition, tap a room. Every wall answers a touch: a fixed wall says why it is fixed.
- **3D (`space3d.js`)**: three.js, renders only when something changed. All walls of a build are one mesh (the cut tops carry the plan's ink through vertex colours), floors come from the same room outlines, pieces are placed from the same x, y and rot. Two cameras: from above with the walls cut at 118 cm, and walking at eye height with full walls, a ceiling, tap-to-walk and wall collision. A piece can be dragged in 3D too; the plan follows.
- **Linked**: the 3D camera is drawn on the plan (where you stand, what you see); dragging it walks you. A selection in one view is the selection in the other. The split between the views can be resized.
- **Loading order**: the plan needs no 3D library and paints first; `space3d.js` and three.js are requested after it.
- Handle for the shared room, same as the 360 tour: `getView()`, `setView(v)`.

## 6. The module on the site

Files (plugin `nadlan-config`): `assets/designer/core.js`, `plan.js`, `space.js`, `spec.js`, `room.js` (call), `designer.css`; server `inc/designer.php`.

```js
const designer = await NadlanDesigner.mount(host, { project: 'ashira', unit: 'E-4A-10', lang: 'he', mode: 'full' });
designer.on('change', fn); designer.getDesign(); designer.getView(); designer.setView(v); designer.destroy();
```

- `GET /wp-json/nadlan/v1/designer/plan?project=&unit=`: the `nadlan-apartment` for that unit. The server resolves the unit exactly as `inc/rfp.php` does and never guesses a neighbour.
- `GET /wp-json/nadlan/v1/designer/catalog?project=`: finishes and pieces allowed for that project.
- Saving: the existing lead and request path (`/nadlan/v1/lead`, then `/nadlan/v1/rfp`), with `nadlan_rfp_clean_design` extended to version 2. No new place for personal details; none in `localStorage`.
- Hosts: a full-screen sheet opened from a project page (the Kikar cockpit's design tile, the stage step "מעצבים את הדירה", the floor card), and the centre of the future "עיצוב דירה" page. It loads on tap only, so the host page's first paint does not change. It reuses the stage's three.js URL (`three@0.170.0` in the import map), which a project page has already downloaded.
- Every public entry stays behind a switch until Ben approves.

## 7. Where plans come from (honestly)

Only Ashira has real plans already redrawn (four types). Utopia (7 PDFs) and SIX-8 (2 drawings) need tracing. The rest of the 1,087 projects have none.

1. **Sales plans**: a staff tracing tool (draw walls over the plan image, mark kinds and openings) writes `nadlan-apartment` with `source.kind = sales-plan`. The Plan Studio's room polygons (HAD-543) convert as a starting point.
2. **Derived**: drawn by us from published facts (the Kikar typical floor). Label: derived.
3. **Schematic**: generated from room count and area, replacing the four separate generators we have today. Label: example layout.
4. **The buyer's own plan** on the public page: upload and trace, later image-to-plan with a stated tolerance (white-space item 8).

## 8. Budgets the build must hold (mid phone)

| Budget | Limit |
|---|---|
| Plan drawn | 1.0 s on IL-4G |
| First 3D frame | 4 s on IL-4G, 8 s on slow 4G |
| Transferred until the first 3D frame | 5 MB, 60 requests |
| A change reaches the other view | work under 8 ms at p95, shown in the next frame |
| Draw calls | 150 |
| Textures in memory | 64 MB (KTX2, 1K by default, 2K on demand) |
| Host page | LCP and CLS unchanged with the designer embedded |

Detail streams in after the first frame: plain colours, then textures, then furniture models (GLB with meshopt), each replacing a box of the true size.

## 9. How the other tasks plug in

- **HAD-704 graphics and video**: PBR materials and light probes on the same meshes; the real window view as the backdrop outside the glass (`hamedina/views/`, per tower, floor and side); a "render" button (progressive path tracing in the browser where the device allows, measured first); the Blender pipeline reads the same two JSON documents to render a hero picture and a film of the buyer's own design; a walkthrough recorded in the browser.
- **HAD-705 catalogue and spec**: a catalogue record carries supplier, price, VAT basis, capture date, valid-until and installation; a price without fresh provenance is shown as an estimate. The spec sheet is `quantities()` plus the catalogue, laid out room by room, each line marked base, upgrade, credit or decor with its difference in shekels. AI generation returns operations, not a picture, so its result obeys the same rules and stays editable.
- **HAD-706 co-design**: operations travel on a reliable `design` topic of the existing TogetherRoom (LiveKit), with a REST fallback. Each carries its author and the design revision; the last writer wins per target; one person holds the pen and can hand it over; "follow me" sends `getView()` ten times a second. The call ends by saving the design and its log. `nadlan_tr_clean_state()` must accept the real unit ids first.
- **HAD-707 page**: mounts the same module with an example layout and the upload path.
- **HAD-708 integration**: the six link sources of the old designer point at the module; `/tour/designer/` keeps answering 200.

## 10. Which measured parameters this decides

From `reverse/features.csv`: the 2D-3D link group (L01 to L05), P06 structural rules, K02, K05 and K07 (co-editing, control, decision log), S02 to S04 (bill of quantities, spec, difference from the base), T01 and T04 (honesty badges, one data source), F04, F05 and M06 (first 3D view, weight, phone), A01 to A03 (Hebrew, right to left). Our own product is scored only by live tests (rubric section 5), so each of these needs its test before it counts.

## 11. Open points

- Real-phone measurements (an Android and an iPhone in hand).
- The legal source of the room-size rules before any buyer sees them as fact.
- Each developer's structural layer and allowed options: without them a project's rules are only the generic ones.
- Meshy credits for furniture models (ask before spending).
- The weights survey of the rubric (section 4 there) before any public "above everyone" sentence.
