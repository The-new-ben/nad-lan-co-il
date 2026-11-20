# Rentals world: Claude Design boards (HAD-795, stage 4)

One board at a time, each shown to Ben before the next (coordinator order 20.11.2026).

| # | Board | Link | State |
|---|---|---|---|
| 1 | The home as an object: 1a the services drawing (fast mode), 1b the 3D model with the services through the walls | https://claude.ai/artifact/C1bAvy1rZEfkMab6FirUmk | 1a sent to Ben 20.11.2026; 1b added the same day on the coordinator's review; waiting for Ben's reaction |
| 2 | The tenancy timeline, handover to exit | https://claude.ai/artifact/UnXWjYcZPJnARhMLhafL1C | sent to Ben 20.11.2026 (the coordinator said not to wait for his reaction to board 1) |
| 3 | The five jobs over three taps + the index update that saves | https://claude.ai/artifact/UnXWjYcZPJnARhMLhafL1C#page-b3 (a second page of the board 2 canvas) | sent to Ben 20.11.2026 |
| 4 | The landlord's first screen, "היום", in three states | https://claude.ai/artifact/UnXWjYcZPJnARhMLhafL1C#page-b4 (third page of the same canvas) | sent to Ben 20.11.2026 |

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

## Board 2 (20.11.2026)
- The lease as a ruler: twelve month ticks, a needle on today, paid months filled with ink, the option-notice month hatched; under it the axis top to bottom, one row per thing that happens; the sheet always stands on the next thing due with one sentence and one primary action; previous / next buttons walk the whole axis with one thumb.
- Frames: board2/Main (interactive), After (rent marked received), Thumb, Full (the whole axis, handover to the return of the security), Desk. Renders: board2/board2-phones.png, Desk.png, Full.png, t1..t3 (a pressed run).
- Pressed at 390 x 844 in headless Edge (not a real phone): what is due next = 0 presses; mark the rent received = 1 press (v2 today: 2); primary action centre at 81% of the height, previous / next at 60%; 0 targets under 44 px.
- Legal sentences: only the statute's own words, read 20.11.2026: s.25ז(ג) use instructions by handover, s.25ח(ב) 30 days from the tenant's demand, s.25יב option notices 90 / 60 days and a reasonable time without an option, s.25י(ה) security back within 60 days or when the debts are paid, whichever is later. No tax date (the Tax Authority's two pages disagree). Index linkage shown "by the contract".
- Navigation gains a fifth tab, "השכירות"; board 1's frames still show four and take it at build.

## Board 3 (20.11.2026)
- Frames (board3/src): Flows (a phone that plays all six flows with a live press counter), FlowsThumb, Counts (before and after with the structural change per job), FlowsDesk. Renders: board3/board3-phones.png, Counts.png, FlowsDesk.png, f1..f5 (the pressed run).
- Counts, before (v2 measured in the local lab, compare/BEFORE.md) -> after (pressed on the board's own screen at 390 x 844 in headless Edge; not a built product, not a real phone): repair with a photo 8 -> 3; send a professional 5 -> 2; close a repair with its invoice 6 -> 3; add a document 5 -> 3; the year's income 4 -> 1; index update: computes only -> saved in 2. In the three camera flows two of the three presses are the phone's own camera (shutter, use photo); the camera on the board is a drawing.
- Structural changes: camera first and save without a form; the open repair's actions sit on the first screen's card; the last professional used is preselected and choose + send is one step; close + attach is one action with the file kind known from the context; the document kind is asked after saving; the yearly total heads the money tab; the index sheet has a save button.
- Sending to a professional opens the landlord's own WhatsApp; nothing is sent automatically. The professional, the index numbers and the amounts are examples.

## Board 4 (20.11.2026)
- The landing screen as a drawing sheet: the home drawing on top with a title block beside it (the date and one sentence that says what is waiting), the part that needs attention lit and the rest dimmed; under it the lease ruler with the needle on today and the index month hatched; then everything anchored from the bottom: recent activity, the main card with its actions in the thumb zone, the fixed camera row, the five-tab navigation with icons. Square corners and ink lines instead of white rounded cards.
- Three states: something urgent (20.11, the open boiler fault), something due soon (28.11, rent in three days and a reminder the landlord set), a quiet day (8.12: money, repairs and documents all in order, plus one suggestion for a spare moment: photograph a missing model plate, BOM leaf 06.01.02).
- Frames (board4/src): Today, TodaySoon, TodayQuiet, TodayThumb, TodayDesk, Plan (the board 1a drawing with a mood prop). Renders: board4/board4-phones.png, TodayDesk.png, TodayThumb.png.
- Measured at 390 x 844 in headless Edge (not a real phone): what is waiting = 0 presses; the urgent card's buttons at 79% of the height (35% on board 3's first frame, which this screen replaces); the camera row at 88%; due-soon buttons at 71% and 78%; every button 48 px or more.
- Board 3's counts are unchanged: the same buttons, lower on the screen.
