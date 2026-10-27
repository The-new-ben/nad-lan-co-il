# TOOLS-LOG: Kochav HaTzafon mini penthouse, apartment 43 (architect's plan to luxury visuals)

Date: 27.10.2026. Everything is local, under `docs/sales/kochav-ph/plan/`. Nothing was published, uploaded to a site, or committed.
Every visual carries the caption "הדמיה על פי תוכנית האדריכל": inside the SVG plans, as a badge in the web component, and stamped on the
publish-ready copies in `renders/labelled/`. No visual carries a dimension, a number in metres or m2, or a scale bar (checked by script:
zero digits in any visible text of the two SVGs and of the web page). No city and no skyline in any of our images; one AI pass that
painted a sea horizon was rejected (below).

Paths are relative to `docs/sales/kochav-ph/plan/`. Machine: Windows 11, AMD Ryzen 7 7730U (CPU rendering, no GPU render device).

## 1. Tools, commands, times, costs, outputs

| # | Tool | What it did | Exact command / script | Time (27.10) | Duration | Cost | Output |
|---|------|-------------|------------------------|------|------|------|--------|
| 1 | Python 3.11.9 + Pillow 12.3 + NumPy 2.4 | Grid crops of the raster, plain and in a 45-degree rotated frame, to read the drawing; a line-profile "snapper" that measures each wall face on the raster | `python tools/crop.py x0 y0 x1 y1 scale step out.png`, `python tools/crop45.py s0 s1 d0 d1 scale step out.png`, `python tools/snap.py D1 3115 700 1600 50` (about 60 measurements) | 13:35-14:00 | ~25 min | 0 | the face constants written into `trace/build_trace.py` |
| 2 | Python + Shapely 2.2 | Builds the trace: 50 wall bands, 20 openings (doors with hinge and swing, windows with sill, sliders), 18 rooms with Hebrew and English names and polygons, terrace, 2 pergolas + 2 posts, 39 furniture/fixture items as drawn, footprints; draws the check overlay on the raster | `python trace/build_trace.py` | 14:00, rebuilt after each fix | 2 s | 0 | `trace/plan.json`, `trace/overlay.png` (full size), `trace/overlay-small.png` |
| 3 | Python (SVG writer); Microsoft Edge headless via Playwright 1.62 for previews (so the Google fonts load) | Luxury 2D plan in Hebrew and English; every room is `<g id="room-...">` with a highlight layer | `python svg/build_svg.py`; `python tools/shot.py svg/plan-lux.svg svg/plan-lux-preview.png 2000 2000 1` | 14:05-15:00 | 1 s + 10 s | 0 | `svg/plan-lux.svg`, `svg/plan-lux-en.svg`, `svg/plan-lux-preview.png`, `svg/plan-lux-en-preview.png` |
| 4 | Blender 5.2.1 LTS, Cycles CPU, OpenImageDenoise | 3D model built from `plan.json` (walls cut at 1.2 m for the cut-away views, full height + roof for the terrace view; window sills, black-framed glass sliders, open door leaves as the swings are drawn, stone curb + frameless glass rail, louvred aluminium pergolas with only the two drawn posts; furniture as drawn; beds); procedural materials matched to the real photos | first pass: `sh blender/render_all.sh` (log `blender/render_all.log`); final pass after the Gemini fixes: `sh blender/render_all.sh` (log `blender/render_all-2.log`); single view: `blender -b --python blender/plan3d.py -- --view dollhouse --samples 128` | final: dollhouse 14:59:19-15:02:55, topdown 15:02:55-15:08:16, terrace 15:08:16-15:18:57 | 205 s, 317 s, 636 s | 0 | `renders/dollhouse-iso.png` 2400x1600, `renders/topdown.png` 2400x2400, `renders/terrace.png` 2400x1600 |
| 4b | Blender (test renders) | Camera, light and material tests at 30-50 % size, 16-32 samples | same script with `--scale 30 --samples 16 --out renders/_test/...` | 14:11-14:58 | 5-35 s each | 0 | `renders/_test/*.png` |
| 5 | Blender (no render) | Projects every room's label point into the dollhouse camera, for the web hotspots | `blender -b --python blender/plan3d.py -- --view dollhouse --hotspots` | 14:22 | 15 s | 0 | `renders/dollhouse-hotspots.json` |
| 6 | ChatGPT image `gpt-image-2.5-sunburst`, images/edits (same call as `film/gen_photoreal.py`; key read inside the script, never printed) | Realism pass on our Blender renders; the prompt forbids any change of geometry and any added object | `python gpt/edit_photoreal.py <in> <out> --no-fidelity [--prompt-file ...]` | see section 2 | 33-35 s per call | see section 2 | see section 2 |
| 7 | Nano Banana `google/gemini-nano-banana-2.1` via OpenRouter (same route as `nano/nano_plan.py`; key read inside the script, never printed) | The same realism pass, image to image, for comparison | `python gpt/nano_edit.py <in> <out> [--prompt-file ...]` | see section 2 | 13-14 s per call | see section 2 | see section 2 |
| 8 | Python (Pillow, NumPy) | Side by side + edge overlay + edge-distance score (share of the AI image's edges within 3 px / 8 px of a Blender edge, at 1200 px width) | `python tools/compare.py <orig> <ai> <side-by-side> <edges> "A" "B"` | 14:26-15:22 | 3 s | 0 | `renders/compare-*.png`, `renders/_test/edges-*.png` |
| 9 | Web component (plain HTML/CSS/JS, no library) + Edge via Playwright | Interactive plan built from the SVG and the hotspots; scripted test: tap a room, chips, 3D toggle, double-tap zoom, keyboard Enter, 44 px targets, console errors | `python web/build_web.py`; `python tools/test_web.py`; `python tools/shot.py web/plan.html web/shots/plan-390.png 390 844 2 --full` (and 1280) | 14:31-15:12 | seconds | 0 | `web/plan.html`, `web/img/*`, `web/shots/*.png` |
| 10 | Gemini `gemini-3.8-flash-high` through the Antigravity CLI | Two critique rounds (section 3) | `agy -p "$(cat gemini/prompt-1.txt)" --model gemini-3.8-flash-high --add-dir <plan>/gemini --mode plan --print-timeout 20m --output-format text > gemini/answer-1.txt` (round 2: `prompt-2.txt`, `answer-2.txt`) | 14:50-14:56; 15:21-15:25 | 3 + 3 min | Google quota of the CLI, no card charge | `gemini/answer-1.txt`, `gemini/answer-2.txt` |
| 11 | Edge via Playwright | Stamps the caption on publish-ready copies | `python tools/label.py` | 15:27 | 15 s | 0 | `renders/labelled/*.jpg` |

## 2. Every paid image call (from `gpt/calls.log`)

gpt-image cost is an estimate from the usage the API returns, priced at the published gpt-image-1 rates (text in $5/M, image in $10/M,
image out $40/M), because the price sheet of the 2.5 model is not on file. Nano Banana cost is the `usage.cost` OpenRouter returns.

| Time | Model | Input -> output | Usage | Cost | Decision |
|------|-------|-----------------|-------|------|----------|
| 14:25 | gpt-image-2.5-sunburst | dollhouse, with `input_fidelity=high` | refused, 400 (parameter not supported) | $0 | no image |
| 14:25 | gpt-image-2.5-sunburst | dollhouse (first Blender pass) -> `renders/dollhouse-iso-photoreal-v1-REJECTED-added-rug.png` | 368 text + 1,536 image in, 1,372 out | ~$0.072 | **rejected**: it added a rug under a bedroom bed |
| 14:27 | gemini-nano-banana-2.1 | dollhouse (first Blender pass) -> `renders/dollhouse-iso-nano.png` (1264x848) | 3,134 tokens | $0.0399 | **not used**: geometry kept (92 % of edges within 8 px) but floors turned into veined marble and the white built-in wardrobes into oak; lower resolution |
| 14:52 | gpt-image-2.5-sunburst | dollhouse (first pass), prompt v2 (no added rugs, wardrobes stay white) | 399 + 1,536 in, 1,372 out | ~$0.072 | superseded by the final Blender pass |
| 15:03 | gpt-image-2.5-sunburst | final dollhouse -> `renders/dollhouse-iso-photoreal.png` (1536x1024) | 399 + 1,536 in, 1,372 out | ~$0.072 | **accepted**: 93.6 % of edges within 8 px, median offset 1 px, nothing added, island not rotated; `renders/compare-photoreal.png` |
| 15:19 | gpt-image-2.5-sunburst | final terrace -> `renders/terrace-photoreal-v1-REJECTED-sea-horizon.png` | 280 + 1,536 in, 1,372 out | ~$0.072 | **rejected**: painted a sea horizon behind the railing (a view we cannot vouch for) |
| 15:20 | gemini-nano-banana-2.1 | final terrace -> `renders/terrace-nano.png` | 3,039 tokens | $0.0397 | **rejected**: sea horizon band, milky glare over the right glass |
| 15:21 | gpt-image-2.5-sunburst | final terrace, prompt v2 (plain sky only) -> `renders/terrace-photoreal.png` (1536x1024) | 311 + 1,536 in, 1,372 out | ~$0.072 | **accepted**: 83.6 % of edges within 8 px, median 1 px, no horizon, nothing added; `renders/compare-terrace-photoreal.png` |

Coordinator's earlier Nano Banana calls (theirs, logged in `nano/LOG.md`): 13:53 nano-banana-2.1 top $0.0406, nano-banana-2.1 iso $0.0405, gemini-3-pro-image iso $0.1404.

**Spend, all tools:** gpt-image ~$0.36 (5 images, estimate) + Nano Banana mine $0.08 + Nano Banana coordinator $0.22 = **about $0.66** of the 4 USD ceiling.

## 3. Gemini critique and what was done with it

Inputs: `gemini/inputs/` (round 1: plan, renders 02-07, real-photo sheet 08, the coordinator's n1-n3) and `gemini/inputs2/` (round 2: the final renders).
Round 1, first attempt 14:50:32-14:52:50 returned nothing: Gemini tried to run a shell command, which headless plan mode refuses
(`gemini/answer-1.err`). I did not switch on `--dangerously-skip-permissions`; I put the exact file paths in the prompt and told it to use only
its file viewer. Round 1 proper: 14:53:17-14:56:27. Round 2: 15:21:38-15:24:55.

| Gemini point | Checked against | Action |
|---|---|---|
| R1: the SVG plan matches the plan, zero numbers, USE | plan, script check | kept |
| R1: geometry, island orientation, terrace and pergolas of 02/05/06 match the plan | overlay | kept |
| R1: "the sofas are parallel, the plan draws an L" | the plan draws the two sofas at right angles; ours are at right angles (see `renders/topdown.png`) | **rejected**, a misreading of the oblique view |
| R1: "two random brown strips; the walnut TV wall is missing" | photos DX9wx4ziADM_02, DZp43r5DIou_04: walnut slats with a stone panel on the wall the sofa faces, which is where ours was | **fixed the reading**: the slat wall now runs along that whole wall section with a narrower full-height stone panel |
| R1: floors washed out; deck too cold, the photos show warm wood-look | photos DZp43r5DIou_07, DX9wx4ziADM_03 | **fixed**: warmer greige stone tiles, warm wood-look deck |
| R1: facade flat white with drawn lines | photo DZp43r5DIou_07 (light grey granite panels) | **fixed**: granite tone with speckle and deeper joints |
| R1: armchairs read as plain cylinders | photo DV6aYANjLBm_01 (rust tub chairs) | **fixed**: one rounded shell, cushion, curved back |
| R1: glass without reflections; flat studio light | | **fixed**: IOR 1.5 with stronger specular; warm sun, fill reduced |
| R1: add bar stools, terrace furniture, planters, curtains | the plan does not draw them; broker's rule: furniture only as drawn | **rejected** (offered to the broker as an option) |
| R1: Nano pass 04 "invented a wardrobe block in the hallway" | the architect draws two built-in wardrobes there, back to back | **rejected** as a geometry claim; true that Nano re-skinned them in oak and made the floor veined marble, so 04 is not used |
| R1: n1, n2, n3 REJECT (building core drawn as a private staircase, other floors' balconies built as terraces, extra pergola, furniture and plants added; n3 replaced the island with a U-shaped kitchen) | own check | agreed |
| R2: fixes landed (floors, deck, facade, chairs, light) | final renders | kept |
| R2: "the dining table is glued to the end of the island, 6 seats; the plan has it parallel" | the plan draws the table across the end of the island, with 8 chairs; ours is the same | **rejected** |
| R2: "the en-suite lost its bathtub", "the laundry nook was merged", "a maintenance-cradle setback is missing" | the plan: the bathtub is in the family bathroom (ours has it), the en-suite has a shower (ours has it), the laundry is enclosed (ours is), no cradle is drawn | **rejected** (hallucinated) |
| R2: "the terrace view lacks the real Tel Aviv skyline and sea" | broker's rule: no views | **rejected on purpose** |
| R2: walnut wall not visible in the terrace view | camera geometry: that wall sits just outside the right edge of the frame | left as is (stated in the report) |
| R2: terrace gpt-image pass (06b) is clearly better than Nano (06c); 06c has a milky glare | own check | agreed: 06b accepted, 06c rejected |

## 4. Measurement notes (trace)

- Internal proportion scale: 157.5 raster px per metre, cross-checked on five of the architect's dimensions (hall 446, bedroom depth 301, main bedroom 393 and 402, closet 395: all within 1.5 %). It only gives the 3D model real proportions and never appears in a visual.
- The living wing sits at 45 degrees; its walls were measured in a rotated frame (s = x + y, d = x - y), so each 45-degree face is one constant.
- `trace/overlay.png` puts the trace on the raster (walls red, openings blue, parapets orange, rooms tinted, furniture outlined).

## 5. Fidelity decisions

- Furniture: only what the architect drew (L sofa group, two armchairs, rectangular coffee table, dining table with eight chairs, island with the hob, counter with the sink, tall units, two built-in wardrobes, bathroom fixtures, washer, water heater, AC unit) plus beds (not drawn; staging, stated on the page). No bar stools, no terrace furniture, no plants, no curtains, no TV.
- Pergola posts: only the two squares drawn on the plan. Louvres run parallel to the living-room wall.
- Rooms the plan does not name: the 45-degree room by the lobby is "חדר נוסף" (it is the fifth room); the room reachable only from the main bedroom is "חדר ארונות". Both are flagged `label_source: inferred` in `plan.json`.
- Floors follow the real photos, not the brief's guess: large light stone tiles in the living space and kitchen (the photos show stone, not wood), light oak in bedrooms and hall, grey tiles in wet rooms, warm wood-look deck outside.
- The other floors' balconies drawn on the sheet ("גוזטרא בק'10", "מרפסת ק'5") and the building's stair/lift core are not part of the apartment and are not modelled; the core is a flat grey block in the 2D plan, for orientation only.
- Room photos in the web component: only where the photo certainly shows that room (living DX9wx4ziADM_02, kitchen DZp43r5DIou_01, dining DZp43r5DIou_04, terrace DX9wx4ziADM_03, family bathroom DX9wx4ziADM_05). The nursery photos (DZp43r5DIou_10, DX9wx4ziADM_04) are not attached to any bedroom, because the plan does not tell which bedroom it is.
