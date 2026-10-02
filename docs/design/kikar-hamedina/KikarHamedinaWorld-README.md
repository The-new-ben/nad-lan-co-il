# KikarHamedinaWorld

**Design system version 104 (30.9.2026, the owner's order), HAD-375.** The Kikar Hamedina Towers page (`/projects/hamedina/`, `/projects/hamedina-en/`) is the flagship, built as ONE walkable, clickable 3D world of the whole area. It has to sell and rank.

**Where it comes from:**
- `docs/loop/KIKAR-HAMEDINA-LOOP.md`
- the research in `docs/research/2026-09-30-kikar-hamedina/`: `facts.md` (82 sources, 21 conflicts), `area.md`, `places.json` (1,245 places), `city-blocks.json` (1,102 buildings with heights), `serp-dna.md`, `feature-inventory.md` (83 features)

## The page, in order (PROJECT-PAGE-CHECKLIST, on every width, phones first)

1. **H1:** "מגדלי כיכר המדינה, תל אביב · Kikar Hamedina Towers".
2. **The answer paragraph (`.nl-lead`), 4-7 lines, sourced, keywords first.** It covers:
   - three turning towers of 40, 40 and 37 floors;
   - 453 apartments;
   - every floor turned 1.25°;
   - MYS Architects;
   - built by Electra and Ashtrom;
   - the frame completed on 23.4.2026, per the municipality's building-site record;
   - around a public park of about 40 dunam with an ecological pond;
   - three sourced deals on floors 38-39 at ₪9.58-10.63M (Globes 2.5.2025);
   - what the page lets you do.
3. **Buttons:**
   - **ייעוץ חינם** (WhatsApp, one tap)
   - **דירות למכירה במגדלים** (anchor to the for-sale section)
   - **סיור בעולם** (enters the 3D world)
4. **The stage, the world** (below).
5. **The view and the map**, attached under the stage: the floor view and the area map with the place registry.
6. **The facts:**
   - A sourced fact table.
   - Where sources disagree, the row shows both, e.g. "tower B: 37 floors, 157 m (Wikipedia, Ashtrom) · 40 floors, 158.2 m (the municipality's layer)".
7. **The tools:**
   - Deals and prices.
   - "When is it ready?".
   - The construction timeline.
   - Sun and shade.
   - For sale and for rent.
   - The square.
   - The park.
   - The FAQ.
8. **The article:** 5,000+ words, from the ChatGPT Pro prompt (P6), marketing tone and sourced.

## The world (the stage)

One scene, four ways in. A **poster** frame paints at once, from a pre-rendered image of the same scene. The 3D loads only when the visitor shows intent (a tap, or scrolling into it). Text and buttons paint in under 1 s on a phone.

| Mode | What the visitor does | Data |
|---|---|---|
| **Aerial** (default) | orbits the whole area; the three towers glow; tap anything | city-blocks.json (true heights), streets, greens, the square's ring |
| **Walk** | walks the square's ring, the park paths, the lake shore, and into the lobby entrance, at eye height; drag and joystick on a phone, WASD on desktop | the same scene, plus the park layout where sourced |
| **Tower** | picks tower A, B or C, then a floor (slider 1-40), then a facing; sees the view from the real eye height; turns the **sun clock** (season × hour) and watches light and shade on the facade and in the room | twist 1.25° × floor; eye height (floor − 1) × 4 + 1.6 m, provisional until sourced; the real sun path for 32.087°N |
| **Places** | filters (school, transport, parks, shops, health, cafés, sport, culture); taps a pin to see its card with walking minutes and source; draws the walking route from the ring | places.json (1,245), Mapbox walking minutes, GTFS bus lines (53 within 5 minutes), the Purple line's Ichilov station at 350 m, the Red line's Arlozorov at 859 m |

**Everything can be clicked and explained:**
- The towers, each floor, the lobby, the facilities (pool, gym, spa, treatment rooms, halls: "on one of the basement levels", per Ashtrom).
- The park, the lake, the school (north building) and the community centre (south building), per the municipal decision of 4.8.2021.
- The ring of stores, the stations, Ichilov, and the landmarks seen from the windows: the sea, Park HaYarkon, Azrieli, the Reading power station, Ramat Aviv.

**Honest labels:**
- The towers: "הדמיה להמחשה · גאומטריה מקומת הבסיס של העירייה + הסיבוב שפורסם (1.25° לקומה)".
- The interiors: "דירה לדוגמה".
- The unit mix is not published, so no apartment facts are invented.

**The engine.** ONE shared world module, `assets/project-stage/world/`, holds the twisted towers, the city blocks, places, sun and the walk. It is not a fifth 170 KB copy of stage.js. engine.js and the original map beam stay frozen. Later, the other projects can move onto the same module.

## The selling path

- The WhatsApp bar sends one tap with the source line: page, tower and floor when chosen.
- "For sale in the towers":
  - explains the resale market (about 250 landowner-sellers; at most 200-250 units expected, per Bizportal 2025);
  - shows dated, attributed asks;
  - routes to WhatsApp and to the pros network.
  - The site never presents itself as the broker (the Brokers Law exemption).
- The shared viewing room and the video call.
- The basket, only for items the site sells.

## Prices, only sourced

- **Deals (Globes 2.5.2025):** floor 38-39, 4 rooms, 140 m²:
  - ₪9.58M (4.2024)
  - ₪9.59M (5.2024)
  - ₪10.63M (12.2024, ₪75,913/m²)
- **Asks, each with its source and date:**
  - a 258 + 57 m² penthouse on floor 39 at ₪43M
  - 168 m² at ₪13.7M (29.1.2026)
  - 154 m² on floor 35 at ₪14.5M
- **The area:**
  - ₪67,747/m² (Madlan via ynet 19.7.2025)
  - deals near the square at ₪63-66K/m² (Tax Authority via ICE 28.4.2026)
- **Nothing is shown without a source and a date.**

## "When is it ready?"

A dated table of statements. No single date is invented:
- Ashtrom: 2026
- Globes 2023: 12.2026
- Electra and Wikipedia: 4.2027
- Bareket's CEO, 9.2025: "within two years"
- Bizportal: end of 2028
- The municipal site record: frame completed 23.4.2026

## FAQ (the 7 Google People-Also-Ask questions, each answered with a source)

- height
- prices
- who built it
- what Kikar Hamedina is
- what the project is
- cafés at the square
- kosher restaurants

A visible `<h2>שאלות נפוצות` plus FAQPage schema.

## SEO

- **Title (he):** "מגדלי כיכר המדינה תל אביב: מחירים, עסקאות, מפה ותלת ממד"
- **Title (en):** "Kikar Hamedina Towers Tel Aviv: Prices, Deals, Map & 3D"
- **Facts as short bullets and table rows:** Google's AI Overview leads both SERPs and cites fact bullets.
- **The rest:** hreflang he/en (fr/ru/ar later), BreadcrumbList, one map, one FAQPage.

## The look

- The house DNA: cream #FAF7F1, ink #1B1A17, gold #9C7A3C, terracotta #C2563A (money CTAs only), hairline #E2DCD0.
- The world is a premium architectural model: cream massing with ink edges, the three towers in glass-gold, the park a muted green, the lake a soft blue, soft real shadows.
- Never game-like, never gaudy. Touch targets are 44 px.
- The prototype renders (`docs/research/2026-09-30-kikar-hamedina/prototype/`) are attached in the preview once they are built.

## Checks at release

- `tools/content_first_check.py`: C3 and C4.
- `tools/source_audit.py`, before and after.
- `tools/wa_bar_audit.py`.
- The runner's H1 and ORDER checks.
- Live eyes at 390 and 1440, in Hebrew and English.
- The load budget: the lead in under 1 s on a mid phone; the 3D not in the first request.

## v104.15 (1.10, loop turn 24): on a tablet or a computer the city is framed below the floating panel

- **The finding (live 1.72.385, tablet 768 × 1024, aerial view):** the floating panel (top right on he/ar pages, top left on LTR pages) covers tower C's roof, so tower C has no name and no letter. On a phone the panel is docked under the stage, so the problem does not exist there.
- **The model: a lens shift, not a camera move.** The perspective's centre moves down until the towers' roofs clear the panel. The city is framed in the free area, while the canvas still runs behind the panel. This is the standard technique for 3D viewers with overlay panels: three.js `setViewOffset`, here as the same off-axis term the phone's bottom sheet already uses.
  - The camera, the orbit and the zoom stay where they were.
  - Taps and labels use the same projection, so they stay exact.
- **The design:**
  - **When:** in the aerial view, on stages of 720 px or wider, where the panel floats. It is computed once the camera has arrived (and on every resize), and it does not chase the user's orbit, so the city never slides while a finger moves.
  - **How much:** just enough that the highest roof under the panel sits 24 px below it, and never so much that the towers' bases leave the stage (48 px margin at the bottom).
  - Other views and phones: no shift.
- **Measured locally (the live page with the local world.js):**
  - Tablet 768 × 1024: towers named 2 → 3. The city moved down 99 px under the panel; the panel itself is untouched.
  - A click on each tower's body still opens that tower's card (A, B and C pressed).
  - Tablet landscape 1024 and desktop 1440: unchanged, all three named.
  - Phones: unchanged (no floating panel): every tower identified.
- **Two bugs caught before release:**
  - a repeated measurement left the lens unshifted;
  - the roof was measured at the tower's height instead of its label's anchor, 5 m higher, which put tower C's letter 3 px into the panel's padding.

## v104.16 (1.10, loop turn 25): on the en/fr/ru/ar pages "what's nearby" counts every place, as the Hebrew page does

- **The finding (live 1.72.386, computed with the world's own rules from places.json):** on the language pages the world LEFT OUT every place whose name exists only in Hebrew. So "N places within 12 minutes" understated what is around the towers:

| Category | he | en, fr, ru, ar (before) |
|---|---|---|
| Education | 94 | 10 |
| Community | 49 | 5 |
| Health | 35 | 6 |
| Parks and sport | 77 | 23 |
| Cafés and dining | 139 | 53 |
| Shops and services | 198 | 61 |
| Transport | 27 | 25 |

  The area map on the same page already counted them all, naming a Hebrew-only place by its kind ("School"). Two parts of one page disagreed.
- **The design: one name rule for the whole page, the area map's.** A place's name is chosen in this order:
  1. its name in the page's language;
  2. its English name;
  3. a name with no Hebrew letters;
  4. its kind in the page's language ("School", "École", "Школа", "مدرسة").

  Nothing is translated or transliterated.
  - The card of a place named by its kind shows its real name too: "Name in Hebrew: כיכר המדינה". It is set right-to-left, so a buyer can match it to the sign in the street.
  - The counts are now the same in every language.
  - Two places that share a kind word are told apart by their Hebrew names, so two different kindergartens nearby are never merged as one.
- **Real names in other languages** come only from sources: OpenStreetMap name tags (v104.8), and now a Wikidata step (a separate data notch, in progress).

## v104.17 (1.10, V2 loop turn 1, item V1): the page opens on choosing an apartment, and nothing scrolls inside the 3D

**The owner's order (1.10 evening):** open straight on choosing an apartment. No scroll-in-scroll on the phone or the PC. Cards that fade. The sun goes to the side. As few elements as possible over the 3D.

**Measured on live 1.72.387 (phone 390, PC 1440):**
- On the PC, the floating panel scrolls inside the stage (638 px tall, 803 px of content). The card does the same (933 px).
- Half of the floor panel is "sun and shade": day, sunset, night, four dates and an hour slider.
- On the phone, the eight directions are a strip that scrolls sideways inside the page.
- The direction cards carry sun hours, not apartment information.
- The floor view also labels the school, the lake and the park on the building's surroundings.

**The design:**
1. **The panel and the cards never float over the 3D, at any width (except full screen).**
   - On a stage of 900 px or wider they sit BESIDE the 3D, in a 340 px column.
   - That column belongs to the page's own scroll. The 3D stays sticky, so it stays in view while the page scrolls through the panel.
   - Below 900 px they sit under the 3D, as the phone dock already does.
   - Nothing scrolls inside anything.
2. **The world opens in the floor view** when it has apartments to show (today Kikar Hamedina), as numbered steps: **1 tower, 2 floor, 3 apartment by direction**. Then the example apartment (plan, 360, album). Prices and plans per apartment are V2 and V3.
3. **The directions are a grid,** four by two, at every width. No sideways strip. Each card shows the direction and its bearing, without sun hours.
4. **The sun goes to the side:** a closed fold, "שמש ושעות היום", at the end of the panel. It never opens by itself.
5. **The floor view labels only the towers and the floor.** The places stay in the aerial view and in "מה בסביבה".
6. **Cards that fade:** in full screen, where a card still floats over the 3D, it closes after 8 seconds without a touch, a hover or the keyboard inside it.

**Not changed:** the 3D engine, the tabs, the example apartment, the area map, the WhatsApp bar (its wording is V9, last).

## v104.18 (1.10, V2 loop turn 2, item V2): apartments by direction, from a computed floor plan

**The owner's order (1.10 evening):** choose an apartment by its direction, not only a floor. Compute the floor plan from the published deals ("four apartments are possible"). Decision information, few disclaimers, no source names on the page.

**Measured on live 1.72.388:** step 3 was eight compass buttons (a 4 x 2 grid). A buyer chose a direction, not an apartment. Nothing on the page showed how a floor divides, which apartment a window belongs to, or what size the apartments are.

**The computation:** world.json `model.plan`, kind "corner4". It says once on the page that it is schematic.
- The plate inside the glass line is about 850-900 m², taken from the municipal footprint (`model.plate`).
- 453 units over 117 floors is 3.9 a floor.
- The published sizes are 132-170 m², with 4-5 rooms. Four apartments of that size fill the plate round a round core; three or five do not.
- The listings' directions fall on this plan's corners at their floors: floor 35 "south-east" and a high floor "north-west". The plate turns 1.25° a floor, so the corners point to the cardinal directions low down and to the diagonals high up.
- The top floors hold larger penthouses (floor 39: 258 m² plus 57 m² outside). No official floor plan is public.

**The design:**
1. **Step 3 is the floor's plan.** It is a 148 px key plan, north up, turned with the floor: dragging the floor slider turns the plan. It shows four corner apartments round the spiral core, each quarter tappable and keyboard-reachable, with its direction in two short lines.
2. **A tap chooses the apartment.** The view from its corner opens; a small gold cone on the plan shows which way the window looks. In the 3D, "המגדל מבחוץ" shows only that apartment's glass on that floor in gold.
3. **Beside the plan:**
   - the apartment's name ("דירה פינתית צפון-מערבית");
   - the project's apartment sizes, labeled "מידע גלוי" (130–170 m² · 4–5 rooms), with the ranges kept in reading order in RTL;
   - under the plan, the three windows it looks out of (its two sides and its corner), as one row;
   - the window / outside switch as one row.
4. **The floor and the tower keep the apartment** nearest the same corner, and a window inside it.
5. **The WhatsApp source line names the apartment:** "… · דירה פינתית צפון-מערבית · מערבה". No unit number is ever invented.
6. **The example apartment (c30w) is the north-west corner apartment.** Its button shows on any of its three windows. The album says the side its pictures face.
7. **One line under the plan:** "תוכנית סכמטית: 4 דירות פינתיות בקומה טיפוסית". On the top two floors it reads "בקומות העליונות: דירות פנטהאוז גדולות יותר". The full basis is in "מה בתמונה להמחשה".

**Not changed:** the 3D engine and the beam; steps 1 and 2; the album; the area map; the WhatsApp bar (V9, last). The eight-direction grid stays for any world without a plan.

**Next (V3):** prices per apartment, from the deals' average and range, labeled "מידע גלוי".

## v104.19 (1.10, V2 loop turn 3, item V3): prices as public information, no source names on the page

**The owner's order (1.10):**
- Prices are the deals' average and range, labelled "מידע גלוי", with no source names.
- "מספיק עם הקרדיטים ומספיק עם המקורות" — enough credits and enough sources.

**Measured on live 1.72.389:**
- The page named news sources dozens of times (Globes, Mako, Bizportal and others): in the lead, in the price section ("לפי גלובס", a "המקור והתאריך" column) and in the sale section.
- The 3D panel showed no price for the chosen apartment.

**The design:**
1. **The 3D panel, once an apartment is chosen:** a block under the floor plan, headed by the "מידע גלוי" pill and "עסקאות בפרויקט".
   - The big line is the deals' range, "9.58–10.63 מיליון ₪", with "ממוצע 9.93 מיליון ₪" beside it.
   - Under it: "3 עסקאות · 4 חדרים, 140 מ״ר · קומות 38–39 · כ-71,000 ₪ למ״ר".
   - Then the towers' average: "כ-65,000 ₪ למ״ר · בקומות הגבוהות ובפנטהאוזים 80,000–150,000 ₪ למ״ר".
   - Numbers use each language's own format. Every number range keeps its reading order in RTL.
   - The data is in world.json `model.plan.deals`.
   - The sizes line loses its own pill; one "מידע גלוי" heads the block.
2. **The page (all five posts):**
   - **The lead:** no source in parentheses, and no "לפי רישום אתר הבנייה". Its last sentence is the page's new flow: "כאן בוחרים מגדל, קומה ודירה לפי כיוון, ורואים בהדמיה את הנוף מהחלונות שלה". The sun hours are no longer promised.
   - **The price section:** "מחירים ועסקאות · מידע גלוי". One paragraph gives the range, the average, the price per m² and the towers' average. The tables keep a "מתי" (date) column and no source column. One closing note: all prices are published public information, and an asking price is not a deal.
   - **The sale section:** its two inline source names are removed; the facts are unchanged.
3. **The sources stay in the repository** (facts.md), never on the page.

**Not changed:**
- The facts table's per-row source lines (the article rewrite, V7, replaces them).
- The FAQ.
- The WhatsApp wording (V9, last).

## v104.20 (2.10, V2 loop turn 4): the basket from the 3D world, and a page with no source names

**V4's first parity step: the basket.**
- The fleet's basket (BasketOne v86) was loaded on the Kikar page and heard the world's floor and direction, but it had no way in. Its button mounts on the fleet stage's steps and view band, which the world page lacks.
- Now, once an apartment is chosen, a terracotta button "לסל הדירה: המחיר המלא, הצוות והנציג" sits under its deals. Terracotta is the money action.
- The button opens the basket:
  - the apartment, named ("דירה לדוגמה · קומה 30 · דירה פינתית צפון-מערבית");
  - the steps;
  - a team of real professionals from the directory;
  - the full price with purchase tax, with a "מידע גלוי" price hint;
  - then the representative on WhatsApp, or the shared viewing room.
- Hebrew only, where the basket runs.

**The owner's law on the rest of the page: no source names.**
- **The quick facts** keep the facts and lose the "לפי ויקיפדיה ואשטרום" lines. The apartments' tile says the average size instead.
- **The deals block** has no source column on this page; its intro opens with "מידע גלוי". Every other project keeps its column.
- **The project card** no longer prints its "המקור: …" line.
- **The facts table, the timeline, the FAQ and the park and square sections** (all five languages) keep every fact and lose their attributions. When two figures were published, both remain, worded neutrally.
- **The stage's hint line** describes the page's flow (the floor plan, the deal prices, the view from the windows). It no longer promises the sun hours.
- **Kept:** the illustration's data line (the municipality's open GIS layers), as the data licence's attribution.

**The parity table** with DUO and Rainbow is in docs/loop/KIKAR-HAMEDINA-LOOP.md (V4). **Next gaps:**
- design styles inside the C30 album;
- the lobby and the basement pool and gym in 360, as labelled concepts;
- the building walk;
- parking (missing everywhere);
- the film.

## v104.21 (2.10, V2 loop turn 5, V4 step 2): design styles inside the example apartment

**The gap (the parity table):**
- DUO and Rainbow let a buyer switch design styles inside the 360. Kikar's C30 album had one look.
- The basket's "העיצוב" step said "הדירה מבפנים עוד לא זמינה בפרויקט הזה".
- Competitors in 2026: Zillow Showcase restyles rooms in curated styles and swipes between staged and unstaged views; Matterport is building the same into its 3D models.

**The design:**
1. **The living room's 360 offers the fleet's styles:** "כמו במסירה" (the room as rendered), "עץ חם", "בהיר" and "אבן".
   - They are rendered from the same Kikar scene, so the same window, the same sea and the same sun appear in each. Only the finishes and furnishing change (the studio kit).
   - The fleet's viewer shows its style panel: at the inline end on a wide screen, a strip over the switches on a phone.
   - Each style says "רעיון עיצוב להמחשה". No developer wording.
2. **The album's 360 tile** says how many styles it has ("סיור 360 בסלון · 3 סגנונות עיצוב").
3. **The basket:**
   - On a world page, "להיכנס לדירה ולבחור סגנון" takes the buyer to the example apartment and opens its 360 at once.
   - The chosen style returns to the basket ("העיצוב": "עץ חם, נבחר בתוך הדירה ב־360°").
4. **The album's size line** names no source.

## v104.22 (2.10, V2 loop turn 6, V4 step 3): the building's rooms in the example apartment's 360

**The gap (the parity table):** DUO and Rainbow walk from the apartment to the lobby and the facilities in one 360 viewer. Kikar showed the apartment only. Israeli competitors (Ashira, the shoreline towers) list long amenity menus but show no 360 of them.

**What is true:**
- The builder places the pool, the gym, the spa, the treatment rooms and the multi-purpose halls on one of the BASEMENT levels. So those rooms are drawn underground, with architectural light only: no window, no sky, never a roof pool.
- A lobby with a concierge desk is published. Tower C's ground floor sits in the renewed square, with the park and the pond around it.
- Everything else is an illustration, labelled once per room: the plans, the sizes, the finishes, the equipment.

**The design:**
1. **The album's gallery strip** gets one 360 tile per room after the apartment's pictures: "הלובי", "הבריכה", "חדר הכושר".
2. **The fleet's viewer (BuildingWalk v96) opens them as one building:**
   - the living room is "הדירה · קומה 30";
   - the rooms are its "בבניין" bar, so a tap walks between them;
   - a tile opens the viewer at its own room;
   - each room carries the "מתקן לדוגמה" chip and one line, e.g. "הבריכה, חדר הכושר והספא נמצאים באחת מקומות המרתף".
3. **Five languages.**

**Next:**
- the doors in the picture and the lift between floors (the full building walk, Maya's W1);
- parking, missing fleet-wide.

## v104.23 (2.10, V2 loop turn 7, V4 step 4): the building walk

**The gap:** DUO and Rainbow walk from the apartment's door to the lift and its floors. Kikar's rooms were reached only by a bar or a tile.

**The design (the fleet's BuildingWalk v96, every connection an illustration):**
1. **In the living room's 360**, "יציאה מהדירה · למעלית" stands in the picture at the hall door. The door was located in the render itself: yaw −128.2°, pitch −2.75°. The door is flush and painted like the wall, so the button is what shows where it is.
2. **The lift panel "לאן?"** (with "מעבר להמחשה") lists:
   - floor 30 (the example apartment, marked "אתם כאן" when you are in it);
   - the lobby (the entrance floor);
   - the pool and the gym (the basement level).
3. **In the lobby, the pool and the gym,** "למעלית" stands at their lift or entrance (located in their renders), so the walk goes both ways.
4. **Every word of the viewer is in the page's language:** the lift, "אתם כאן", "חזרה", and the floor on the apartment's place ("The apartment · Floor 30"). The shared viewer's Hebrew stays the default for DUO and Rainbow.

## v104.24 (2.10, V2 loop turn 8, V4 step 5): the spa and the car park

**The gap:** the published facilities include a spa with treatment rooms (one of the basement levels, with the pool and the gym) and the residents' underground parking, two spaces per apartment. Kikar's 360 had only the lobby, the pool and the gym, so the V4 table's "parking" row was empty on every page of the fleet.

**The design (illustrations, the same viewer, the same walk):**
1. **Two more rooms** in the example apartment's 360, rendered in the same design family as the pool and the gym (scripts/interior/kikar_facility.py, scenes spa and parking):
   - **הספא** ("ספא וחדרי טיפולים, באחת מקומות המרתף, ליד הבריכה וחדר הכושר"): a reception counter, loungers, treatment-room doors, a sauna's glass front, no window.
   - **החניון** ("קומות החניה מתחת לקרקע; שתי חניות לכל דירה"): a clean residents' level with a bronze-framed glass lift vestibule, storage-room doors, a few generic cars (no make, no plate, no number).
   - The number of parking levels is not stated, because the sources disagree (3 or 4).
2. **The walk reaches both rooms.** The lift panel now has six stops: floor 30, the lobby, the pool, the gym, the spa and the car park, whose sub-line reads "קומות החניה". In each room, "למעלית" stands at the room's door (located in the render: spa +135.0° / −3.0°, car park −138.4° / −4.7°). There is no inner scroll in the panel, on phone or PC.
3. **The album never leaves one tile alone on a row.** Nine tiles (4 of the apartment and 5 rooms) are laid out as three full rows of three, not 4 + 4 + 1. The rule is in example.js `stripCols`: use 3 columns when 4 would leave a single orphan and 3 would not.
4. **All five languages:** Spa / Parking, Spa / Parking, Спа / Паркинг, السبا / موقف السيارات.

## v104.25 (2.10, HAD-390, with Maya's QA; LOCAL until her QA passes): ConsultBand, the WhatsApp bar's own reserved space (FloatingClear v2)

**The gap (measured on the live 1.72.395, the apartment chosen, the whole page scrolled in steps):**
- **Phones (320 to 412, he and en):** the floating "ייעוץ חינם" bar covered:
  - the "מידע גלוי" deals box, up to 11,856 px²;
  - facts lines, up to 11,956 px²;
  - buttons and links, up to 11,706 px².

  The bar or the accessibility button covered something in 35 to 40% of the scroll steps.
- **768:** it also covered `.nlw-exlink` (10,322 px²) and facts cells.
- **1440:** the deals, the facts and `.nlw-exlink` are clean (0); a guides link is covered at a few steps.
- **Why the old rule failed:** it lifts the bar over the nearest free slot between buttons. Text is not an obstacle, so it parked on the price. A local try that made the price and the plan obstacles pushed the bar onto half of "היכנסו לדירה לדוגמה", where it would steal the tap. Rejected.

**The design: ConsultBand.** On pages with the 3D world (`#nlps .nlw`), up to 1023px wide:
1. **A band of its own at the foot of the screen.**
   - Full width, cream #FAF7F1, a hairline #E2DCD0 on top, a soft shadow upward. Its height is the bar's height plus 8px above and below, plus the phone's safe area.
   - Content passes under it as under a toolbar. Nothing sits on top of the reading area.
2. **The wide bar is unchanged:** green, the NadLan mark, "ייעוץ חינם" and its line, one tap to WhatsApp. It holds the band's end side, as wide as before and never wider than 360px.
3. **The accessibility button** sits in the band's start corner (its corner since 25.9), centred in the band height. It never rises over content, and the two never overlap.
4. **The page keeps the band's height at its end** (body padding), so the last line is always reachable above the band.
5. **No lifts on these pages.** The bar and the accessibility button never move up over content.
6. **The full-screen layers stay above the band as before:** the world's full screen, the album, the 360 viewer and the basket.
7. **From 1024px up:** unchanged. The bar floats in its corner (measured clean against the price, the facts and the example link).

**The acceptance test** (`band_probe.py`, Maya's matrix: 320/360/390/412/768/1440, he and en, with the apartment chosen):
- the whole page is scrolled from top to bottom;
- in the reading area (the screen above the band), the bar and the accessibility button cover 0 px² of the deals, `.nlw-exlink`, facts and controls;
- the bar and the accessibility button never overlap each other;
- the touch targets are at least 44px;
- the page's end is reachable;
- no page errors.

**Revision 2 (2.10 evening, after Maya's independent QA):**
- **Every width, desktop included.** Live at 1440x900, the floating bar took the centre of the apartment button `.nlw-btn--ex` (at y838, scrollY 224). The band now holds the bar on every world page.
- **The sticky 3D** of a wide stage ends above the band: height `clamp(440px, 100svh - 168px, 760px)`.
- **One owner for the floating layout: the CSS.** It sets `--nlcta-band:1` on the body. The bar's lift script and AccessibleCorner read that variable and stand still, so the two systems with fixed collision lists no longer decide alone.
- **Keyboard focus reveal.** `scroll-padding-bottom: calc(84px + safe area)` on the page. A native Tab from "המגדל מבחוץ" put the apartment button half under the band; now the browser scrolls it fully above the band. Touch scrolling is untouched: no jumps, no inner scroll.
- **The acceptance**, a route-swap on the live HTML (`scripts/qa/had-390/hit_probe.py`, `tab_probe.py`, `fleet_regress.py`):
  - the matrix: he and en at 320/360/390/412/768/1440, landscape 844x390, short 1366x640;
  - the states: before the choice, after the choice, after the album closes, with the accessibility panel open;
  - each CTA tested at 5 points.
- **The results:**

  | | Live 1.72.395 | Local |
  |---|---|---|
  | Points that missed their target | 762 | 0 (of 32,710) |
  | Elements behind the header or the band (counted separately, not as misses) | 1,021 | 1,054 |

  - Tab and Shift+Tab: 24 steps on 6 screens, every focus visible.
  - DUO and Rainbow: the band's scope is false. The journeys (choice, tour, basket, accessibility) behave the same live and local. The positions of the bar and the accessibility button match live vs local on desktop, and on the phone they differ only within the live-vs-live timing noise.

**Revision 3 (2.10 evening, HAD-390 R3, after Maya's SECOND verdict): the usable rect, in both directions.**
- **The finding:** at HE 844x390, 12 Tab then 12 Shift+Tab put the apartment button at y0-46, under the sticky header (which ends at 61). Revision 2 had a bottom padding and no top one.
- **The design:** on a 3D-world page, the usable rect runs from the sticky header's foot to the band's top. Every keyboard move (Tab, Shift+Tab, Escape back to a trigger, an in-page link) ends with the focused control fully inside it. There is no clipping exemption, at either edge.
- **The means, CSS only:** `html:has(.nlps-stage--world){scroll-padding-top: 77px}`. That is the tallest measured header (69px at 1366+; 61 at 768-1024; 57 at phones) plus 8px of air. When the admin bar sits above the header, it becomes 123px.
  - No auto-scroll script.
  - Touch and manual scrolling are untouched: scroll padding only steers the browser's own reveal.
- **The acceptance:**
  - Maya's sequence, plus the forward Tab, on 6 screens in he and en;
  - Escape from the album returns focus visibly;
  - the in-page links land in the usable rect;
  - a touch swipe moves the same distance as live;
  - DUO/Rainbow keep no scroll padding.
