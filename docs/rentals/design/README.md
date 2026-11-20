# Rentals world: Claude Design boards (HAD-795, stage 4)

One board at a time, each shown to Ben before the next (coordinator order 20.11.2026).

| # | Board | Link | State |
|---|---|---|---|
| 1 | The home as an object: 1a the services drawing (fast mode), 1b the 3D model with the services through the walls | https://claude.ai/artifact/C1bAvy1rZEfkMab6FirUmk | 1a sent to Ben 20.11.2026; 1b added the same day on the coordinator's review; waiting for Ben's reaction |
| 2 | The tenancy timeline, handover to exit | | after board 1 |
| 3 | The five jobs over three taps + the index update that saves | | after board 2 |
| 4 | The landlord's first screen | | after board 3 |

## Board 1
- Sources: board1/*.dc.html + canvas.json (the published files). Renders: board1/board1-phones.png (home, part open, thumb zone), board1/Desk.png, board1/p1..p4 (a pressed run).
- Identity: the colour code of building-services drawings (cold water blue #1565c0, hot water red dashed #c62828, gas yellow #f5b800, electricity violet #6a3fc8) on a white drafting sheet with a 12 px grid and dark ink #14212b; the action colour is the site's sea blue #2f6f86. Faces: IBM Plex Sans Hebrew for text, IBM Plex Mono for dates and numbers. Not the default AI look: no cream, no brown, no gradient; every colour names a system.
- Measured in a browser at 390 x 844 (headless Edge, not a real phone): layer chip then a row then the part = 2 presses to a part from the list, 1 press from the drawing; primary action centre at 79% of the height on the home screen and 81% with a part open; 0 visible targets under 44 px.
- Legal sentences on the board: only s.25ח of the Rental and Lending Law as read in the statute text on 20.11.2026. For appliances the landlord left (fridge, oven, washing machine) the board points to the contract and states no rule; that wording waits for a lawyer.
- All data is an example and is labelled "דירה לדוגמה".

## Board 1b (added 20.11.2026 after the coordinator's review of 1a)
- What it is: the same screen and the same sheet as 1a, with the home drawn as a white 3D model by the apartment designer's own engine (space.js, three.js 0.170), walls ghosted and the four service runs in the 1a colours; one press switches to the 1a drawing, which is also the reduced-motion and weak-phone fallback.
- Harness (design lab, not site code): docs/design-lab/rentals-xray/ (xray.html, xray.js, space.lab.js = a lab copy of space.js with one export added, shoot.py, measure.py). Renders and the fly-in film: board1b/renders/. Board frames: board1/Home3d.dc.html, Part3d.dc.html, Film.dc.html. Pressed run: board1b/b1..b4 and board1b-phones.png.
- Measured (board1b/renders/measure.json): 474 KB in 13 requests (three.js 215 KB), 1.3 s to the first 3D frame, 2.8 ms of render work per frame, 306 draw calls, about 99k triangles. Desktop Chrome with a real GPU emulating a 390 x 844 phone, NOT a real phone; a mid phone was not measured.
- Pressed at 390 x 844 (headless Edge): the urgent part's pin = 1 press to the part; primary action centre at 81% of the height; the 3D / drawing switch at 48%; 0 targets under 44 px. A part inside the crowded wet cluster = 2 presses through the layer list.
- Not at the level yet (said on the board): the overview is pale, the appliance models are plain boxes, no soft corner shading; on the board the fly-in is a crossfade between two renders (the film shows the real one); the fast drawing on the board is the 1a apartment, not the engine's plan.
