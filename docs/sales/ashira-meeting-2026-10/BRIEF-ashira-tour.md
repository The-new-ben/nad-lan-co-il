# Task: Ashira gets the same in-building journey as Rainbow and DUO (360 example apartments + facilities + building walk). LOCAL ONLY.

Repo root: C:\Users\777\nad-lan\nad-lan-co-il. Blender 5.2 is installed (`blender -b --factory-startup --python ...`).
Write only: scripts/interior/ashira_*.py, scripts/interior/render_ashira.py, scripts/interior/_renders/ashira/**,
plugins/nadlan-config/assets/project-stage/ashira/tour/** (new folder), docs/sales/ashira-meeting-2026-10/tour/REPORT.md + contact sheets.
Do NOT edit stage.js, bridge.js, project-stage.php, facilities.json or any live file; no deploy, no runner, no network uploads.
Rules: every image is an ILLUSTRATION (same caption policy as Rainbow/DUO); no downloaded/third-party assets or textures; no
real Ashira interior is claimed; the engine and the map beam are frozen. CPU Cycles with FIXED threads (other agents share the machine).

## Follow the proven pipeline exactly
Study, then mirror: scripts/interior/duo_world.py, duo_interior.py, duo_facility.py, render_duo.py, cut_tour.py, studio_kit.py
(and rainbow_interior.py / rainbow_facility.py for balconies and views by floor and direction). Mirror the OUTPUT the live page
already consumes for Rainbow and DUO: look at plugins/nadlan-config/assets/project-stage/rainbow/tour/ and .../duo/tour/
(file names like living-<floor><dir>.jpg/-2k.jpg/-card.jpg/.webp, balcony-<floor><dir>..., fac-<name>-c...; examples.json /
scenes json). Produce the identical set of sizes and formats so wiring later is data-only.

## Ashira facts (sources: plugins/nadlan-config/inc/project-stage.php Ashira block, assets/project-stage/ashira/*.json)
- Lot 101, Eshkol compound, Sde Dov, Tel Aviv. Municipal plan approved 12.5.2024: tower 35 floors (~137 m), mid-rise 16, two
  low buildings 8 each; 406 homes (202 in the tower). The world model and coordinates: reuse ashira/city.json and quarter.json
  (the same footprints the 3D stage draws) so views from each floor match the stage's geometry and the sea direction.
- Facilities the developer markets (illustrate, label "מתקן לדוגמה"): indoor semi-Olympic pool (basement), children's pool,
  jacuzzi, spa with salt room and collagen light therapy, dry and wet sauna, gym, yoga/wellness, private cinema, children's
  activity room, residents' lounge, bar and workspace, lobby. Use the facility list/positions in ashira/facilities.json.

## Scope (minimum parity with Rainbow)
1. Example apartment, tower: floors 10, 25 and 34 x four directions (w = sea, n, e, s): living room 360 + balcony 360 with the
   real-direction view built from the world model. 4096x2048 masters, then the derived sizes.
2. Facilities 360: lobby, indoor pool hall, spa (salt room visible), gym, residents' lounge/club, cinema, children's room.
3. Design styles in the living room like Rainbow (as-delivered, warm wood, light, stone) for at least floor 25 west.
4. Building walk data: which door leads where (apartment -> elevators -> lobby / pool / spa / gym / club), in the same JSON
   shape Rainbow/DUO use, saved under ashira/tour/ (not wired).

## Quality bar (the owner: "uncontested")
Interiors must be clearly better than the DUO/Rainbow sets: realistic proportions, daylight from the true sun side, materials
without default grey, no floating furniture, no blown windows, sea visible from west floors 25/34. Probe the camera rays
(the scripts' *_PROBE pattern) to prove the view direction. Render a low-res pass first, check, then the masters.

## Proof to deliver (docs/sales/ashira-meeting-2026-10/tour/)
- contact-sheet-apartments.jpg, contact-sheet-facilities.jpg, contact-sheet-styles.jpg (labelled tiles).
- side-by-side.jpg: the same scene type for Ashira vs Rainbow vs DUO.
- REPORT.md: scenes rendered, samples/time, the probe results per direction, known limits, the exact file list with sizes.
Work autonomously to the end; if time runs short, finish floor 25 (4 directions) + lobby + pool + spa first, report the rest as pending.
