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
