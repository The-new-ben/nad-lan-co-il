# Kikar Hamedina showcase: every visitor feature built for the project pages (10.11.2026)

This updates `docs/research/2026-09-30-kikar-hamedina/feature-inventory.md` (30.9.2026, 83 rows). Read-only pass: no code
edited, nothing deployed, no server touched beyond plain public GET requests.

- **Rows:** `features.csv`, 142 features. Columns: what the visitor sees, the code, the switch, the marker, yes/no for each
  checked live page, other evidence, status, who it was built for, and buyer value from 1 to 5.
- **Live evidence:** fetched 10.11.2026 with a desktop Chrome User-Agent. Every page served plugin `ver=1.72.630`.
- **Pages checked:**
  - /projects/hamedina/ (8113) and its English sibling /projects/hamedina-en/ (from hreflang);
  - /projects/rainbow-tel-aviv/, /projects/duo-tel-aviv/, /projects/dimri-yama-sde-dov/, /projects/ashira-sde-dov/;
  - /projects/h-infinity-somail-tel-aviv/ and /sde-dov/.
- **Extra pages used as evidence:**
  - Kikar: /projects/hamedina-fr/, -ru/, -ar/, `?room=new` and `?advisor=on`;
  - other projects: /projects/ashira-sde-dov-en/, /projects/gindi-vogue-sde-dov/, /projects/aurelia/, /projects/utopia-sde-dov/,
    /projects/einstein-tower/;
  - tools: the tool pages named in the CSV;
  - routes: /tour/sde-dov/, /tour/somail/, /tour/designer/, /earth/, assets/walk/ashira/ and assets/walk/kochav/;
  - the English guide /en/buy-property-in-israel/.
- **Repo:** branch `claude/apartment-experience-b1`, HEAD d7bf7034.
- **Not proven by HTML:** client-side features are proven by two things together: the page loads the script, and the live
  script contains the feature's string.
  - Kikar uses `world.js` and `example.js`; the other stages use `bridge.js`.
  - Those live scripts were downloaded and compared with the repo.

## Counts

| Status | Features |
|---|---|
| On Kikar: 22 only there, 34 also elsewhere, 4 inside the world album or with a limit | 60 |
| Live elsewhere only (other project pages, tool pages, routes, one guide page) | 53 |
| Built but live nowhere (off, not printed, branch-only, or not found on the checked pages) | 12 |
| Prototype only (labs, Codex worktrees, untracked local files, private artifacts, sales kit) | 16 |
| Removed or broken (/earth/) | 1 |

## 1. Features live elsewhere but missing on Kikar, ranked by value to a buyer

Kikar already leads the fleet in several features (rows F01-F13, E10-E13, B04): the one-world 3D, the tower → floor →
apartment-by-direction pick, the turning key plan, the window view, the sun clock, the walk on the square, the deals in the
apartment card, the 4-style 360, the twist strip, and the car-park 360. The gaps are below.

| # | Feature (CSV id) | Where it is live | Why a Kikar buyer wants it |
|---|---|---|---|
| 1 | ProjectToolkit: total cost, construction-index indexation, purchase tax and late-delivery compensation, preset for the project, with the result share bar: copy, WhatsApp, print (C01-C06, A21) | Rainbow, DUO, Dimri, H Infinity, Gindi Vogue and the radius pages | An off-plan buyer of a 10-million-shekel apartment with a 2026-2028 delivery needs exactly these four. Kikar's content has no `[nadlan_project_kit]` shortcode. It is the only result-sharing feature on project pages. |
| 2 | A link that reopens the chosen apartment (`?unit=`) (D03) | Rainbow, DUO, Dimri, Ashira (`keepUnit` in the live bridge.js) | Buyers send the choice to a partner. world.js keeps no address state, so a chosen tower, floor and apartment cannot be shared. |
| 3 | The room as delivered (empty) vs furnished (E03) | Rainbow (floor 25 living room), Ashira (floors 10 and 25 plus the balconies) | Kikar's base picture is already furnished ("העיצוב המקורי"). There is no empty apartment. |
| 4 | 360 across floors and directions, with balcony 360 (E01) | Rainbow 24 scenes; Ashira floors 10, 25 and 34 × 4 directions; DUO 4 | Kikar has one example apartment: tower C, floor 30, west. |
| 5 | The view from the floor on a real satellite map, the "what is that way" list with walking minutes, and place names inside the 360 windows (D06, D07, E06) | Rainbow, DUO, Dimri, Ashira (names in the windows: Rainbow and DUO) | Kikar's window view is massing from GIS data, not real imagery. Its places list is by category, not by the chosen window. |
| 6 | Free walk into the building: between the buildings, the lobby, the facilities, the apartment (E07) | Ashira (assets/walk/ashira/index.html) | Kikar's walk stays outside on the square. The facilities are reached as separate 360 jumps. |
| 7 | Monthly-cost tools: mortgage by tracks, "from contract to keys" (mkeys), repayment capacity (afford), Tel Aviv arnona, value estimate (pval) (C07-C10) | Tool pages only, on no project page | The monthly cost of a 140 m² Tel Aviv home is the question after the price. Kikar shows only the finance line. |
| 8 | How-to film and video-call demo film in the side rail (E08) | Ashira (English with captions) | It shows a hesitant buyer how to use the page and what the video call looks like. |
| 9 | Hero film button with its length, plus VideoObject structured data (A09, A19) | Rainbow (hero button); Rainbow, DUO, Dimri (VideoObject) | Kikar has two films, but only as sections lower on the page, and no VideoObject. |
| 10 | Floor card link to the apartment designer (D10, H09) | Rainbow, DUO, Dimri, Ashira (/tour/designer/) | Design intent. The live link drops the chosen unit; branch v102 fixes this (L10). |
| 11 | Facility pins on the model with "ask about this facility" on WhatsApp (D09) | Rainbow, DUO, Dimri, Ashira | Kikar's facilities sit underground and appear only in the album. There is no per-facility question. |
| 12 | Deal rows that jump to their floor, and a sold deal named in the floor card (B03, B05) | Rainbow, DUO | Kikar's three published deals carry no tower (`n=0`), so this needs data first. |

**Also missing on Kikar:**
- **The English page** has none of these Hebrew-only modules:
  - the deals table;
  - the basket;
  - RadiusPrices;
  - the price-alert window;
  - the professional slot;
  - the facility chips.
- **AggregateOffer price schema** (A20): only Rainbow has it, and the AI-citation research tied it to the pages ChatGPT
  quotes.
- **ProjectFacts** with linked sources and a "checked on" line (B10).
- **The NeighbourCompare spotlight** (B11).
- **The showroom engine** (I01, Aurelia: 2D studio with SI 1918 clearances, "בנו לי הצעה", compare, favourites). It runs on
  the frozen engine and is not meant for stage pages.

## 2. Features built but live nowhere

Ranked by buyer value. Paths are in the CSV.

1. **Plan Studio (L01).** It shows Ashira's four published building-E plans. The buyer taps a room and sees the 3D building
   and apartment, the window view with distance, the facility 360s, and WhatsApp. It is a private artifact:
   https://claude.ai/artifact/363bRm1N5CsXXc1jG4PWZx. The format could be reused for Kikar once plans exist.
2. **The walkthrough 3D lab (L07).** A continuous walk: park → lobby → clubs → lift → pool, spa and parking → floors 1 to 40
   → apartment, with styles, curtains and a laser measure. It was built for Kikar and Ashira, lives in
   `C:\Users\777\nad-lan\walkthrough-3d-lab\`, and is not in git.
3. **BuildingLife facility navigation (L03).** Photo cards under the stage open the facility 360s and keep the chosen unit.
   It also adds a DUO gym node and a tower-aware basket. It sits uncommitted in Codex worktree
   `codex-kikar-duo-experience-2026-10-09`.
4. **Ashira round-3 interiors (L02).** E-plan living rooms, balconies and the master bedroom on floors 5, 10 and 15, plus
   cinema, kids and club rooms. The files are untracked. The live `ashira/tour/walk.json` and `views.json` answer 404.
5. **Branch bridge v101/v102 (L10).** The floor card docked under the stage, +/− zoom, the map landing with the unit line and
   "חזרה לבניין", the designer opened with the unit, and `window.__nlpsPick` on the stage pages. Repo bridge.js is 55 KB and
   the live one is 39 KB; the live file has 0 hits for `__nlpsPick`, `cardHost` and `nlps-mapsum`.
6. **The designer remembering each apartment and sending furniture and notes in the request (L05), and the UnitCut section
   cut (L04).** Both are labs.
7. **Higher-quality CC0 interior furniture (L06).** A lab that waits for the owner's OK on the downloads.
8. **ConsultSheet (H03).** An editable WhatsApp message with chips. No `#nlcta-sheet` was found on any checked page.
9. **The Hebrew how-to film (E09).** `ashira/howto-he.mp4` answers 200 (4.28 MB), but no checked page uses it.
10. **The "מחיר מוערך" label on map price chips (B12).** It exists only on the branch.
11. **First-person interior from unit data (I05) and the area price line (A26).** Their CSS loads, but no element was found
    on the checked pages.
12. **The advisor and avatars:**
    - the AI advisor HAD-680 (K01) is off: `?advisor=on` on Kikar prints nothing;
    - the talking face 0.2.0 (K02) is local only;
    - the small avatar HAD-682 (K03) is live only on /en/buy-property-in-israel/, not on any project page.
13. **The rest:**
    - the Kikar film cuts uploaded but not shown (G04, per the memory note, not checked in the media library);
    - the DUO modular preview (I07);
    - the LOI form (H12);
    - listing offers (H13, flag off);
    - the Kochav real-photo layer (L08);
    - the untracked Rainbow style cards (L09);
    - the parked opening flight (L11);
    - Aurelia's community options (L12);
    - the EcoCity and Lovable branches (L13, L14);
    - the Ashira journey film (G05, sales kit only).

## 3. Broken or wrong things noticed (with evidence)

1. **On Rainbow, DUO, Dimri and Ashira, the chosen floor and direction never reach the WhatsApp message.**
   - inc/wa-source.php reads `window.__nlpsPick`, and only the unreleased branch bridge.js sets it: 0 hits in the live
     file, 3 in the repo.
   - This was open on 30.9 and is still open.
   - Kikar is not affected, because world.js sets it.
2. **On Kikar, the shared viewing room cannot share the 3D world view.**
   - `together.js` takes the building view from `window.__nlpsStage` (line 300), which only bridge.js sets (line 69 of the live file).
   - world.js never sets it, so a `?room=` session on Kikar can share the 360 (through `window.__nlTour`, set by tour.js)
     but not the tower, floor and camera.
   - This is code evidence; it was not tested in a live room.
3. **The live designer link drops the unit.** The live bridge.js does `location.href = DESIGNER` with
   `DESIGNER = '/tour/designer/'` and no parameters.
4. **Kikar has two films but no VideoObject**, and no AggregateOffer despite its sourced deals. Rainbow has both.
   Grep `"VideoObject"` and `"AggregateOffer"` in the page HTML.
5. **Ashira has no FAQPage JSON-LD**: no `"@type":"FAQPage"` in its page HTML.
6. **/earth/ now answers 404**; on 30.9 it answered 401.
7. **ConsultSheet, live on 29.9, is no longer printed.** Nothing named `nlcta-sheet` or `nlcs-` appears on any checked page.
   Whether this was a deliberate removal is unknown.
8. **The repo is not the live truth for several project files.**
   - The live `inc/project-stage.php` carries the price guide (`#nlpg`, rendered by `scripts/project-stage/price_guide/`)
     and the Ashira how-to rail (`.nlps-howto`). The repo copy has neither.
   - Live and repo differ in `bridge.js`, `tour.js`, `expert-advisor/advisor.js` and `ashira/facilities.json`.
   - These files are byte-identical live and in the repo: `world.js`, `example.js`, `hamedina/world.json`, `together.js`,
     `basket.js`, `booking.js`, `trail.js`, `price-alert.js`, `slice.js`, `arealife.js`, and the Rainbow, DUO and Dimri
     `facilities.json`.
   - **A Kikar rebuild must start from the live files.** See the memory note nadlan-repo-not-live-files.
9. **The area price line (`nl-areaprice`) prints on no checked page.** Its CSS ships, but it needs 5 or more deals in
   `wp_nadlan_deals`, and the near-alerts header says that table is empty.

## 4. The exact markers, so the check can be repeated

1. **Fetch the pages.** Use a normal browser User-Agent and save each page as `<name>.html` in one folder:

   ```bash
   UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
   for p in hamedina:projects/hamedina/ hamedina-en:projects/hamedina-en/ rainbow:projects/rainbow-tel-aviv/ \
            duo:projects/duo-tel-aviv/ dimri:projects/dimri-yama-sde-dov/ ashira:projects/ashira-sde-dov/ \
            hinf:projects/h-infinity-somail-tel-aviv/ sdedov:sde-dov/; do
     curl -s -L -A "$UA" -o "${p%%:*}.html" "https://nad-lan.co.il/${p#*:}"; done
   ```

2. **Fetch the live scripts into `js/`.** Name each file after its path with `/` replaced by `_`, for example
   `project-stage_world_world.js`. Fetch `project-stage/world/world.js`, `project-stage/world/example.js` and
   `project-stage/bridge.js` from `https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/`.
3. **Run the check:** `python -I check_markers.py <that folder> <output folder>`. It rewrites `features.csv` with the
   yes/no columns.
4. **How the marker column reads:**
   - **A regex on the page HTML.** Attribute markers like `id="nlrp"` and `class="nlpf` only count real elements; the inline
     CSS on every page also names the prefixes.
   - **`<script> + <file> "<string>"`.** The page must load the script, and the live script must contain the string.
   - **Data-driven rows** (E04, E05, E06, B05) come from the live `facilities.json` and config:
     - Rainbow: 360 rooms pools, club and lobby, plus a walk;
     - DUO: pool, lobby and club, plus a walk;
     - Ashira: 7 rooms and no walk;
     - Dimri: none.
5. **The main markers:**

   | What | Marker |
   |---|---|
   | The world (Kikar) | `project-stage/world/world.js` |
   | A stage page | `project-stage/<dir>/stage.js` + `project-stage/bridge.js` |
   | Price guide | `id="nlpg"` |
   | Deals table | `id="nlps-deals"` |
   | Floor-linked deal rows | `data-nlps-floor` |
   | RadiusPrices | `id="nlrp"` |
   | ProjectToolkit | `id="nlkit"` |
   | Tools (and their JSON-LD) | `assets/instruments/core.js` (`id="nadlan-nli-ld"`) |
   | ProjectFacts | `id="nlfx"` |
   | NeighbourCompare | `class="nlnb"` |
   | Basket | `nadlan-basket-cfg` |
   | Price alert | `id="nlnu"` |
   | Video-call booking | `id="nlsch"` |
   | Room chooser | `id="nadlan-together-chooser"` |
   | The room | `together/together.js` on `?room=new` |
   | Film dialog | `id="nlfilm"` |
   | Kikar films | `id="nlws-film"`, `id="nlws-facilities"` |
   | 360 card | `id="nlps-tour"` |
   | Styles | `living-NN<d>-warm` |
   | Empty room | `bare-thumb` |
   | Ashira walk | `walk/ashira/index.html` |
   | How-to rail | `class="nlps-howto` |
   | Satellite view | `id="nlps-view"` |
   | "What is that way" | `id="nlps-near"` |
   | Unit deep link | bridge.js `keepUnit` |
   | Slice | bridge.js `openSlice` |
   | Hero actions | `data-nlps-ev="hero-wa|hero-pick|hero-world|hero-sale|hero-video|hero-film|slot|walk|howto"` |
   | Schema | `"@type":"FAQPage"`, `ApartmentComplex`, `"VideoObject"`, `"AggregateOffer"` |
   | The pick in WhatsApp | world.js `__nlpsPick` (stage pages: bridge.js `__nlpsPick`, absent live) |

6. **What the marker check does not prove:**
   - that a feature works when pressed: no clicks were made;
   - that a room carries video;
   - the media library contents;
   - the language siblings of Rainbow, DUO, Dimri and Ashira (only the Ashira English page and Kikar's four siblings were
     fetched).
