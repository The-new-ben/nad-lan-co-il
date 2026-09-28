# nad-lan.co.il: work started, promised or planned and not finished (audit of 28.9.2026)

**The owner's order (28.9.2026):** go back and find everything forgotten, not completed, started and not continued, across the repo and everything else.

**The audit was read-only.** Nothing in Linear, Notion, git or the site was changed. This file is the only thing written.

**Sources scanned:**
- Linear, team Hadmaia: every open nad-lan issue (the project "nad-lan.co.il — חדר מלחמה" and the unassigned nad-lan issues), plus the ones closed in the last 7 days. That is 64 open issues and 18 closed ones, each read with its description and comments.
- Notion "מרכז הבקרה של הפרויקטים": 49 open rows (נכס = נדל״ן or שדה דב), plus the "פעולה הבאה" of 63 rows closed since 21.9.
- The repo (branch `claude/production-truth-1.72.212`, HEAD f392e1f0, the same as origin):
  - docs/loop/SITE-LOOP.md and docs/coordination/claude-codex.md;
  - docs/handoff/ and the September receipts;
  - `git status`, the unmerged branches and the worktrees;
  - TODO/FIXME in plugins/nadlan-config.
- The memory folder: the handoff file, the owner decisions of 28.9, and the buying-journey vision.
- The owner board: artifact Sot2mJCpiWSiEwEwMtErxL, version of 28.9 19:10.
- Quick live checks, all read-only: health, /projects/, /properties/, /developers/, /film/, and the Rainbow and The Park pages.

## Summary

| Group | Rows | Blocked by the owner | Nobody blocks |
|---|---|---|---|
| Started and not finished | 18 | 4, partly | 14 |
| Promised to the owner and not delivered | 14 | 6, fully or partly | 8 |
| Waiting for the owner | 8 | 8 | 0 |
| Ideas and found gaps never started | 12 | 3 | 9 |
| **Total** | **52** | **21** | **31** |

Out of the 9 asks the owner made on 28.9 (listed at the end), **only 2 have a real Linear issue**:
- the full buying process (HAD-358);
- the H Infinity article (HAD-357).

**Only 1 has its own Notion row:** the buying journey, together with the shared room. The other 7 exist only in the chat, the memory and the owner board.

**What stands out:**
1. **Nobody has ever paid on the site, as far as the records show.** The 17.9 diagnosis found no order ever placed. On 28.9 the Morning gateways were found switched on, but a real purchase was never made end to end. **No leads were recorded in the last 7 days:** live health, 28.9, lead_e2e.leads_7d = 0.
2. **The owner asked for four things on the evening of 28.9 that nobody has recorded as tasks:**
   - the floor card that covers the 3D model;
   - a better Hebrew voice;
   - the commercial spaces on the model;
   - walking inside the building.
3. **A privacy exposure with no owner decision needed has not been started for 5 days:** HAD-262. Each professional's email and owner fields are open in the public REST API.
4. **The Linear records lag behind the site.** Seven open issues are done or moot. Three issues serve as release logs (HAD-297, HAD-346, HAD-358), so their leftovers have no issues of their own.
5. **No TODO or FIXME was added in plugins/nadlan-config in the last 30 days.** The only three (claim.php:13, lead-drip.php:8, saved-search.php:13) date from 13.8.

## Started and not finished

| # | What | Source | Started | What is left | Size | Blocked by |
|---|---|---|---|---|---|---|
| 1 | The apartment designer loses the chosen apartment, and Codex's two lab pieces are not integrated: the UnitCut section cut and the designer adapter | HAD-346 items 1 and 4; HAD-221; docs/coordination/claude-codex.md:33-72 and 74-118; Notion "ריינבו: מעצב הדירה לא יודע איזו דירה נבחרה" (הבא) and "ריינבו: גובה הנוף תוקן... ביקורת על הניסוי של Codex" (פעיל); worktree `worktrees/codex-rainbow-unit-lab-2026-09-27` (labs/ and scripts/labs/ uncommitted) | 27.9 | A design version that keeps the unit visible and names the generic example honestly. One real saved-design/lead/RFP contract (today the editor's "הבקשה בדרך ליזם" has no backend). Codex's 98% tap-grid proof at 390 px. The read-only `stage.internals()` hook. The lazy `cut.js` after the paper-volume redesign | L | nobody (Codex's evidence) |
| 2 | The RFP path: the studio choices never reach `/nadlan/v1/rfp`, and `sanitize_key()` strips ':' from unit ids | HAD-329; claude-codex.md:157-161 | 27.9 | Review Codex's `labs/unit-journey/unit-contract.md`. Store the studio choices in `inc/rfp.php`. Give the id its own sanitiser or map it explicitly to `32-w` and the engine's `unit_id` | M | nobody |
| 3 | Stage accuracy: sun, lobby, pool, balconies | HAD-358 comment of 28.9 14:52; memory handoff (353); HAD-295; Notion "nad-lan 1.72.352-353" (next action "תיקון שמש השקיעה") | 25.9 / 28.9 | The "sunset" preset puts the sun at 208°/16°, which is wrong for late September. DUO's lobby glass is drawn at 6 m; the developer says about 7 m. A lounger stands inside DUO's toddler pool (z −6.0). Rainbow's balconies are drawn as waves around the tower, 0.7-3.6 m deep; the design plan says at most 2 m and not all around. Check that against the permit (HAD-295); the stage, the slice and the 360 renders all use this shape | S + M | nobody; HAD-295's final shape is the owner's design call |
| 4 | Dimri Yama, Ashira and DUO are not at Rainbow's level inside the building | Owner board table, 28.9; HAD-364 follow-ups; HAD-358; Notion "1.72.337 – נכנסים למתקנים בריינבו" (next action "חדרי מתקנים לדואו, דמרי ימה ואשירה") | 28.9 | Dimri and Ashira: no apartment 360, no facility rooms (the 360 buttons on their facility cards are inert), and no deals by floor. DUO: no balcony 360 and no design styles. Styles exist only on Rainbow's floor 25 | L | nobody |
| 5 | H Infinity has no 3D stage | HAD-356 (the rest after DUO, Dimri and Ashira); Notion "1.72.336" (next action "במה לאינפיניטי") | 28.9 | A stage on the shared engine. Source the height (187 m has no source) and put the low building on its real side | M | nobody |
| 6 | The language pages are not finished (EN/FR/RU/AR) | HAD-361; HAD-363 follow-ups; Notion "1.72.338" and "1.72.350-351" rows; memory handoff (338, 350) | 28.9 | They still use the old theme header, a sideways strip on phones (checked live 28.9: rainbow-tel-aviv-en has no `nlhp-top`). The browser dictionary is 17 KB gzip; trim it. The film, the steps rail, the deals table and the basket are still left out. The shared room was never tested there. /ar/'s footer touches the edge at 390 px | M | nobody |
| 7 | The home, what is left of H1.3b | HAD-297; SITE-LOOP.md row H1; Notion "עמודים פנימיים קלים ב-18.7 KB (1.72.283)" and "ריינבו: ראש העמוד..." (25.9) | 25.9 | The language homes still use the skin renderer, so the site has two home renderers. Critical CSS and fonts (FCP about 3.0 s is the limit). The map band prints about 14 KB inline and its data is 356 KB. City names on the language homes and the English footer need checking (the board says the RU footer is fixed) | M | nobody |
| 8 | DUO's data (research of 28.9) | HAD-365; Notion "דואו: נתוני מכירות, מע״מ, מועד השלמה וטבלת עסקאות" (הבא); memory handoff (341) | 28.9 | Item 5, the facilities wording: the pool on the lobby roof or in the wellness complex; the ~7 m lobby; the 300 m² gym only with its source; the Green Line link on floor −1; the penthouse pools on floors 49-50. Check that the floor-18 asking price of ₪12.5M is never shown as a deal. Memory says the 4 language pages got the Q2 2026 figures in 341, while Linear says open: confirm, then close | S-M | nobody |
| 9 | What is left of Rainbow | SITE-LOOP.md rows R6 and R8; HAD-296, HAD-290, HAD-292, HAD-293 | 25.9 | R6 part 2 is parked: the opening flight, the sun path with soft shadows, haze and tower detail. Noon light and a bedroom. Clickable existing buildings and more places. R8: the Tax Authority's full deals list, a price-range chip, and the deals table in 5 languages | M | nobody |
| 10 | The 16 Hauzd gaps (HAD-186): 14 boxes unticked, though several are live | HAD-186; competitor-profiles/hauzd-gap-analysis.md | 20.8 | Re-tick what is live (slice, basket, 360, facilities). Real gaps: a sorted table of all units, filters that mark units on the building, a plan and keyplan per type (needs the developer's plans), similar units, favourites, a developer dashboard, live price and status | L | nobody (the plans come from the developer) |
| 11 | The broker platform, what is left | HAD-258; HAD-246 rows 16-25; HAD-252; HAD-229; docs/receipts/RECEIPT-BROKER-OFFER-2026-09-23.md:81; RECEIPT-BROKER-DROP-2026-09-23.md:63-68 | 23.9 | Move the 3 broker snippets into the plugin (about 320 KB read on every uncached request). The drop engine prints images without srcset. An empty ~150 px band on broker sites. Hebrew posters in the English galleries (L09, L04) and a ~200 px gap at the top of the English pages. "מדלן" is still in the source JSON: receipt 1.72.238 says the live pages have 0, while HAD-252 still says 55. About 100 inactive tmp-* snippets, leftover page-id CSS, and the `.nlx` class clash | M | nobody (deleting the snippets needs the owner's OK) |
| 12 | Listings, what is left | HAD-347 | 27.9 | Meital's 11 listings have lat/lng 0, so there are no map pins; geocode them. Rename the `.nlpl` class prefix, which the placement card shares. The signed-in "my listings" view was never looked at | S-M | nobody |
| 13 | SEO and copy fixes left over | HAD-298; HAD-301; HAD-366; HAD-287; HAD-288; docs/receipts/RECEIPT-SEO-GAPS-1.72.235-236-2026-09-24.md:48; SITE-LOOP.md:209 | 23-28.9 | /projects/ still says "ב־18 ערים", from the query's LIMIT 18 (live, 28.9). i18n.php still holds "קטלוג התלת ממד" (tour_catalog) and "מהמערכת" (rc_kicker). The about page's title says "נדל"ן חכם", and the deal-check title ends in "נדלן - נדלן". FIRST's "בקו ראשון לים" is unverified. Template titles over 60 characters promise "בחירה מהבניין"; Dimri's title is 79 characters. Zohi's developer name lacks the gershayim. Aurelia shows "חסרות קואורדינטות". The Somail tour's "כ־257 דירות" has no source. The /earth/ layer returns 401. The surroundings text has "תכנית ל'", "find-place" and bare permit numbers. Check CTR in Search Console in mid-October (HAD-366) | M | nobody |
| 14 | HubSpot: site leads do not reach the CRM | HAD-220; Notion "HubSpot לכל הלידים + וואטסאפ" (ממתין לאישור); live health 28.9 | 17.9 | The plugin that sends every site lead to HubSpot form e4ee7f00 was never built. Live health shows 0 leads in 7 days, so also check that the forms deliver at all | M | nobody for the build; the plan and the footer are row 39 |
| 15 | The August war-room engineering items, untouched since 20.8 | HAD-187, HAD-188, HAD-196, HAD-203, HAD-206, HAD-183 | 20.8 | HAD-187: the language pages lost units and posters. It was probably overtaken by 338/348; verify and close. HAD-196: Akirov took 25 s; a warm load today took 0.8 s; measure a cold load. HAD-206: the 3D integrity items (USDZ 404 with an AR button, copy that oversells, Einstein's 28 fake floor pins). HAD-188: The Park's poster; its page has no model today, so it is probably moot. HAD-203: the technical SEO bundle (the Hebrew city-filter canonical, the home JSON-LD pointing to a Dimri 404, merging the schema @id, the og/{id}.svg 404, an h1 on /catalog/ and /buy-vs-rent/). HAD-183: SIX-8 is frozen and not in today's fleet | M | nobody; HAD-203's noindex and sitemap parts need the owner's explicit order (law of 3.9) |
| 16 | Repo hygiene | HAD-253; HAD-287; `git status` of 28.9 | 23.9 | **Not tracked in git:**<br>• `.claude/skills/language-dna/`, `docs/design-lab/`, `docs/content/plate-factory-2026-08-28/`, `tools/deals/`, `plate-factory-2026-08-28.bundle` and `inc/skin-a.php.v11.bak`;<br>• **27 Rainbow `*-card.jpg` renders** in assets/project-stage/rainbow/tour/ (floors 10 and 36, and the 25 n/e/s styles). They return 404 live, so they were rendered but never shipped;<br>• scripts/interior/_renders/, 207 live-backup files and 24 speed JSONs.<br>**The project CLAUDE.md** still says 1.72.210, branch claude/sde-dov-experience-v1 and C:\Users\pro.<br>**7 codex/* branches and worktrees** from 27-28.8 are unmerged, 4 of them EcoCity: retire them.<br>**handoff/ecocity-takedown-2026-08-30/media-backup/** holds EcoCity media: never commit it and never republish it.<br>**The local origin ref is from 20.8.** The remote itself matches HEAD | S | nobody |
| 17 | Reviews and "In Review" statuses | HAD-247, HAD-249, HAD-251, HAD-257, HAD-259; closed HAD-229, HAD-254, HAD-255, HAD-256 | 23-24.9 | No Fable review is recorded for the Opus 5.5 work of 23-24.9, and the session-boot law asks for one. HAD-247 still waits for the owner's look on a phone. Close what is live | S | nobody (the owner's look for HAD-247) |
| 18 | The owner board and memory need this list | Owner board "סריקת משימות שנשכחו" (הבא בתור) | 28.9 | Put this list on the board and open the Linear issues and Notion rows marked "none" below. This audit did not write them, by order | S | nobody |

## Promised to the owner and not delivered

| # | What | Source | Started | What is left | Size | Blocked by |
|---|---|---|---|---|---|---|
| 19 | **The floor card covers the 3D model** when a floor is clicked | memory nadlan-owner-decisions-2026-09-28 (evening); owner board "הכרטיס מסתיר את הדגם" (הבא בתור). **No Linear issue, no Notion row** | 28.9 | All of it: a design version first, then the card docks to the side, folds to a strip or drags, on desktop and phone. Consult Codex | M | nobody |
| 20 | **The video call** in the shared room (LiveKit) | HAD-358 comment 28.9; Notion "עיצוב: חדר צפייה משותף (77)..." (פעיל, דחוף); owner board q-livekit; memory decisions | 28.9 | The room is live without video, because the `nadlan_tr_lk_*` options are empty. Ask Codex whether jus-tice has a key; if not, the owner opens an account and pastes the key. Then: a push alert to the representative when a buyer opens a room, an "admit" step, the room must not cover the WhatsApp pill, and the "נציג זמין עכשיו" toggle | S after the key; M for the alerts | **owner (the key)** |
| 21 | **The Hebrew narration of the films** is poor | commit bf47b440; owner board q-films; memory decisions; Notion rows "1.72.331" and "1.72.335" (only in the next action). **No Linear issue** | 28.9 | Replace edge-tts he-IL-AvriNeural with the better voice work from jus-tice and Hadmaya (through Codex), or ElevenLabs. Hebrew first, then EN/FR/RU. The narrated cut is not on the site; the silent film is live | M | nobody (find where the ElevenLabs key is) |
| 22 | **The developers' film** | commits 3c91dd38 and f848765b; scripts/project-video/out/nadlan-developers_*.mp4 (rendered 28.9 18:06); Notion "nad-lan 1.72.352-353" (next action "הסרט ליזמים"); owner board. **No Linear issue** | 28.9 | 50 s, no narration, on the board for approval. /developers/ and /film/ still play the August `nadlan-developer-film-hq.mp4` (checked live). After the OK: upload it, swap it on both pages, and add a voice track (row 21) | S | **owner (approval)** |
| 23 | **The DUO film** | HAD-358; Notion "1.72.331" and "1.72.333" (next actions); memory handoff 353 "Next". **No dedicated issue or row** | 28.9 | The data is ready (scripts/project-video/data/build_duo.py, duo-tel-aviv.json) but it was never rendered; there is no DUO file in out/. The owner wants DUO for the Africa Israel meeting | M | nobody |
| 24 | **The H Infinity article in 5 languages**, and its language pages | HAD-357; memory decisions (the article method); owner board "המאמר של אייץ׳ אינפיניטי" (running, research stage). **No Notion row** | 28.9 | Research: Google's results and suggested searches, and the DNA of 4-5 competitors, per language. Then at least 5,000 net words through ChatGPT Pro in the owner's Chrome. Each language is rewritten, not translated, for buyers from abroad. The EN/FR/RU/AR pages do not exist (404); run the URL word audit first | L | nobody (the ChatGPT run happens in the owner's Chrome, driven by the agent) |
| 25 | **"One project that has it all": Rainbow** | memory decisions (19:00); owner board table (four rows "חסר"); HAD-221 as the umbrella. **No dedicated issue or row** | 28.9 | The developer's floor plans (row 36). The facilities exist behind the legend chip "מתקנים בפרויקט", but the owner did not find them: make them discoverable. The commercial spaces mapped and clickable on the model (developers love it). Walking continuously inside the building | L | nobody; the plans come from the developer via the owner |
| 26 | **The full buying process**, self-serve up to the legal line | HAD-358 (10 build boxes unticked); HAD-364 follow-ups; HAD-184; Notion "עיצוב: חדר צפייה משותף (77) ומסע הקנייה וסל הדירה (78)" and "1.72.340"; owner board q-pay; memory nadlan-buying-journey-vision | 28.9 | The reservation request, a file number, a personal apartment-file page and a requests screen for the team (designed, DS v93, not built). Services paid through WooCommerce + Morning for what the site itself sells. The independent lawyer pool (never "our lawyer"). Explain down payments in plain words. The basket on the language pages. Real professionals in the six slots (there are none today). The steps bar at the top. ₪/$/€ and index linkage in the full price. "הבית שלי" | L | **owner** (approve the approach, the legal line, the lawyers' model); the build is nobody's |
| 27 | **The interior 360 quality** must be much higher (Rainbow's styles are low; DUO must be better) | memory decisions; HAD-358; Notion "1.72.335" (next action "רהיטים אמיתיים (ממתין לאישור הורדה)"); owner board q-codex | 28.9 | Real furniture: the download of CC0 models waits for his OK. Build on Codex's graphics results; where they are is unknown. Better lighting and materials | L | **owner** (OK to download; where Codex's results are) |
| 28 | **Consulting and brainstorming with Codex** ("Astra"): voice, the LiveKit key, the card, graphics and marketing | memory decisions; owner board "התייעצות עם קודקס" (running). **No Linear issue, no Notion row** | 28.9 | No answer is recorded yet in claude-codex.md or in the repo. Collect it, write it into the coordination file, and bring the owner the breakthroughs in Hebrew | S | nobody |
| 29 | **Proposals he approved, not built** | owner board "הצעות"; memory decisions. **No Linear issue, no Notion row** | 28.9 | "קומה מול הים": ads that land on the floor and side in the model, with 360, per project and language. The developer report: floors and sides buyers chose, real numbers only, a tool for the Africa Israel meeting. The professionals network as the social seed. The WhatsApp deal alert: explain how it works; it needs WhatsApp Business. Also his standing ask: new proposals in Hebrew every time | M each | nobody (the WhatsApp alert needs a Meta business number: owner) |
| 30 | **The showroom as a template for the fleet and the premium projects** | SITE-LOOP.md:208 (owner order 28.9), rows S1 and P1 | 24-28.9 | The skill `project-page-factory` (S1) was never created. Stages for UTOPIA, Einstein Tower and SIX-8 (P1). Then the premium projects | L | nobody |
| 31 | **The competitor research for the home** was never run | HAD-297 plan step 2; SITE-LOOP.md row H1 | 25.9 | ChatGPT deep research on the home pages of Yad2, Madlan, Homeless, Onmap, Zillow and Rightmove. It never started, because the owner's Chrome was hidden | S | nobody |
| 32 | **Aurelia Sports** ("the next thing", owner 3.9) | HAD-221 description; Notion "אורליה: לאתר עבודה שננטשה" (הבא, low); memory handoff 1.9 and 3.9 | 1.9 | Gate 3 (filling the studio) never started, and there has been no activity since 7.9. Map what stopped and where | M | nobody |

## Waiting for the owner

| # | What | Source | Started | What is left | Size | Blocked by |
|---|---|---|---|---|---|---|
| 33 | **Payments proven end to end, and the prices** | HAD-184 (all boxes open); HAD-257; Notion "קופה: Pro יוצא 0 בגלל קופון firstmonth..." (ממתין לאישור); owner board q-devprice | 20.8 | The Morning API key in wp-admin. Pro is ₪349 (ruled 28.9), but the firstmonth coupon brings it to ₪0 with no card saved, and there is no recurring charge. His OK for a ₪1 live test (as of 17.9 no order was ever placed). The price of the developers' 3D product | S for him, M for the fix | **owner** |
| 34 | **Demo content**: 7 demo listings (4951-4957) and 15 demo professionals with invented ratings in the schema | HAD-248 (Urgent, untouched); HAD-219; Notion two rows (ממתין לאישור) | 23.9 | They are labelled "לדוגמה" since 1.72.292-298 but still published. His word to move them to draft; first replace the 4 links to them on the home | S | **owner** |
| 35 | **Meital Katzir** | HAD-217; HAD-252; HAD-229; HAD-255; Notion rows: "מיניסייט מיטל קציר", "תיבת נכסים למתווכים", "רשת בעלי מקצוע", "תיאום סיור ביומן", "סרטון נכסים לכל מתווך" | 17.9 | Send her the drop link and the firgun link. Ask her for the calendar link and a written OK on the copy, the photos and the prices. Ask whether every listing is exclusive, and whether L04 and L05 are one property. The vertical video for her WhatsApp status. Optional: RU/FR for her 11 listings | S | **owner** |
| 36 | **The Rainbow developer's marketing data** (Israel Canada) | SITE-LOOP.md:221; docs/handoff/2026-09-25-rainbow-floor-answers-HANDOFF.md:104; HAD-221 | 25.9 | Apartments left, price lists and the plans per side. When they arrive, they go on the floor card as published, with the source | S for him, M to place | **owner** |
| 37 | **Legal and privacy** | HAD-259; HAD-347; HAD-358; Notion "מדיניות פרטיות ותנאי שימוש..." (ממתין לאישור) | 24.9 | A lawyer reviews /privacy/ (8103) and /terms/ (8104). The listings' distance chip sends the visitor's IP to ipwho.is: keep it, switch to the browser's location, or drop it? The lawyers' ethics model for the basket | S | **owner** |
| 38 | **Corrections to his own texts** | SITE-LOOP.md:216; Notion "1.72.329" | 28.9 | The H Infinity article says "DUO 510 apartments", while DUO's page says 668. (HAD-340, the 459/480 sentence, was fixed on 27.9 on his word; checked live on 28.9, the sentence is gone. Linear still says Backlog) | S | **owner** |
| 39 | **Small rulings** | SITE-LOOP.md:222; HAD-346; HAD-356; HAD-266; HAD-263; HAD-267; HAD-260; HAD-220; HAD-368 | 23-28.9 | 1. /tour/designer/ ends in a demo checkout with a card form marked "(דמו)".<br>2. Do paying developers' video calls go to the developer's own representative?<br>3. The /tour/* pages have noindex and no canonical; only he decides.<br>4. /properties/ slugs with a city name vs the URL word law.<br>5. The AI token cap: 200K → 1M a day, at most ~$5 a day.<br>6. Permanent deletion of 8 test media items.<br>7. His OK for an SMTP test mail; two SMTP plugins are active.<br>8. The paid HubSpot plan and the business address for the email footer.<br>9. DataForSEO and Meshy: payment and keys (mostly jus-tice). | S | **owner** |
| 40 | **Decisions from August never answered** (close them or ask once) | HAD-191, 192, 193, 194, 197, 198, 200, 202, 204, 207; Notion "ניקוי קניבליזציה בשדה דב" and "מיזוג שתי כפילויות שדה דב" (ממתין לאישור since 28.8) | 20.8 | **Still open:**<br>• the empty heading "מימון, ייעוץ ועיצוב": fill it or remove it (still live on The Park, 28.9);<br>• GO for the 3 mega-articles;<br>• the facilities standard;<br>• Einstein's "33,000";<br>• the re-crawl word;<br>• the voice recording (probably replaced by row 21);<br>• peek-card, roofs, tool anchor;<br>• the Sde Dov duplicates merge.<br>**Moot:** the gh ssh key, since pushes work (the remote matches HEAD). The EcoCity and Africa Israel story and the DUO forensic are frozen by his word, and EcoCity was taken down | S | **owner** |

## Ideas and found gaps never started

| # | What | Source | Started | What is left | Size | Blocked by |
|---|---|---|---|---|---|---|
| 41 | **Professionals' records are open in the public REST API**: email, owner_user_id, claim_status, promo fields | HAD-262 (High) | 23.9 | All of it: count the affected cards, then filter with rest_prepare or unregister the fields | S-M | nobody |
| 42 | The site's hierarchy abroad: one /global/ hub with country pages, the block editor for nadlan_intl, the Dubai article (7625) linked | HAD-218 | 17.9 | All 6 items | L | nobody |
| 43 | A strong residential page on broker fees | HAD-264 (Search Console: "דמי תיווך" 215 impressions at position 46, 0 clicks) | 23.9 | All of it; run the URL word audit first | M | nobody |
| 44 | French and Russian broker directories, and the owner wizard in both languages | HAD-265 | 23.9 | All of it | M | nobody |
| 45 | Import brokers from the register | HAD-250; Notion "מתווכים במדריך: דגימה מאזורי יוקרה" | 23.9 | Rescoped on 24.9 to a sample from luxury areas; 120 are listed already | M | owner (sitemap and scope) |
| 46 | **Recruiting developers** | Notion "מודל הכנסה בלי תיווך ותוכנית פנייה לכל היזמים" (הבא, 24.9); HAD-195; memory nadlan-developer-recruitment-strategy | 20.8 / 24.9 | A revenue model with subscriptions and advertising only, a list of developers by size, a package per developer built on the search numbers, and the first 10 messages. Launch only on his word | M | nobody (the launch is the owner's) |
| 47 | Notion ideas of 24.9, never started | Notion rows (הבא) | 24.9 | A list of ideas for the young and for kids. Award-level design research and a 3D city demo for Sde Dov. The buyer's journey mapped with screenshots and drop-off measured. A WhatsApp "share to" door without Meta. A video and a calendar per broker. The property page: a small drawing that marks the floor at once, the full 3D on click | S-M each | nobody |
| 48 | The board's new proposals of 28.9 | Owner board "הצעות" (חדש) | 28.9 | Buyers from abroad: currency, purchase tax for non-residents, foreign mortgage, remote signing. Comparing two apartments. Sun and shade per apartment. A recorded tour in 5 languages. The buyer's personal area | M each | nobody |
| 49 | Codex's open business tracks | claude-codex.md:72 and :132 | 28.9 | The failed listing-publication path, the stale lead/task email, a professional graph from evidenced work, unit campaigns on the existing advertiser/orders rails (no fifth payment rail) | M | nobody |
| 50 | The old tour and generation tracks | HAD-185, HAD-199, HAD-201 | 20.8 | Image generation for the fleet through the owner's ChatGPT. GLB buildings in the aerial tour. A tour factory for developers. A broker form that makes a tour. Personal WhatsApp tours. A live guided tour. 10 renewal terms in the glossary, and merging the double "עסקת קומבינציה". The 4-minute film | L | nobody |
| 51 | Codex's Notion rows of 28.8-1.9, stale | Notion rows (אחראי קודקס/ג׳מיני): "אתר המיפוי הישראלי בחמש שפות", "בניית חתך אנכי של שדה דב", "מודל ישויות", "מפת כתובות", "מנגנון מקורות", "תמונות שיתוף 1200×630", "תור פלטות ליזמים גדולים", "עוגן מצב קבוע", "דנ״א שפה ומותג" | 28.8-1.9 | No activity since 1.9. Re-scope or close | S | owner (whether to keep them) |
| 52 | The May SEO plan (the old theme approach) | HAD-113 | 26.5 | Obsolete; close it | S | nobody |

**Checked and not items:**
- SITE-LOOP.md:169, "only a couple of pins" on the home map: corrected by 1.72.303-306 (961 of 975 projects have a place).
- The 404s of /projects/bnei-dan-54-56/, /projects/stricker-13-brandeis-14/ and /echo-city/: the deliberate EcoCity takedown.
- The WhatsApp pill on /tour/* and the '+' encoding (HAD-346 comments): fixed in 1.72.323-326.
- The 401 that live health shows for OpenAI: the probe is unauthenticated, so this is expected (inc/health.php:160).

## The owner's asks of 28.9: which have an issue or a row

| Ask | Linear | Notion | Row here |
|---|---|---|---|
| The video call with LiveKit (key missing) | only a comment on HAD-358 | inside the row "עיצוב: חדר צפייה משותף (77)..." | 20 |
| Hebrew narration quality | **none** | only in next actions (1.72.331, 1.72.335) | 21 |
| A project with everything (Rainbow: floor plans, clickable facilities, commercial spaces on the model, walking inside) | HAD-221 as the umbrella only; **none** for the commercial spaces or walking inside | **none** | 25, 36 |
| The floor card covering the 3D model | **none** | **none** | 19 |
| The full buying process | **HAD-358** (+ HAD-364 step 1 done, HAD-184 payments) | **row "עיצוב: ... מסע הקנייה וסל הדירה (78)"** | 26, 33 |
| The developers' film | **none** | only a next action (1.72.352-353) | 22 |
| The DUO film | only comments on HAD-358 | only next actions (1.72.331, 1.72.333) | 23 |
| The H Infinity articles in 5 languages | **HAD-357** | **none** | 24 |
| Brainstorming with Codex | **none** | **none** | 28 |
| (also 28.9) Interior quality, real furniture | a line in HAD-358 | only a next action (1.72.335) | 27 |
| (also 28.9) More proposals, approved proposals | **none** | **none** | 29, 48 |

## Record hygiene (not work, but the records mislead)

**Linear issues that are done or moot but still open:**
- HAD-340: fixed 27.9; checked live.
- HAD-299: /properties/?listing_type=rent has the H1 "דירות להשכרה" (checked live).
- HAD-344: all its next items are done.
- HAD-332: only a page that does not exist is left.
- HAD-251: the menu item is live.
- HAD-249: close after the review.
- HAD-188: The Park has no model on the page now.

**Other Linear records:**
- HAD-195 still points to HAD-183 as the DUO card; HAD-183 is SIX-8.
- HAD-297, HAD-346 and HAD-358 are running release logs. Their leftovers (rows 1, 7 and 26) need issues of their own.

**Notion rows that are stale:**
- "ריינבו: לחיצה על קומה עונה מיד" (הבא): live since 1.72.278-279.
- "ריינבו: להחזיר את הפרויקט עם תלת-ממד... לשיווק יחד עם מיטל" (ממתין לאישור): live since 1.72.255.
- "מפת פערים 23.9 לילה": its next action says Linear is full; the plan was upgraded on 24.9.
