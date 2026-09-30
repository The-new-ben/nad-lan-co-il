# Kikar Hamedina: the masterpiece loop (the state file)

**Owner order, 30.9.2026.** Build Kikar Hamedina as the tip of the pyramid, a project page never seen before:
- **The whole area** is mapped and built as ONE walkable 3D world: the three towers, the square's ring of buildings and shops, the park and the lake, the streets, and every key place around.
- **Everything is clickable and informative:** hotspots, facilities, the key places, and the view from the windows.
- **It sells:** a visitor lands, clicks, understands, and reaches a sale.
- **It brings traffic:** keywords and SERP DNA.
- **The article** is marketing, rich, with more detail than any site on Google, and never nerdy or negative.
- **Languages:** Hebrew and English first, then fr, ru and ar.
- **Before building:** check everything built for Rainbow, DUO, Dimri, Ashira and H Infinity, and forget nothing.

Every loop turn reads this file first, takes the first unchecked item, does it end to end, ticks it with its evidence, and writes the next step. Linear issue: see "Tracking" below.

## The recursive scaling rule (the owner, 30.9.2026: "recursive researching scaling up... non-compromising... web search every looping")

Every turn does ALL of these, not only the current phase:

1. **Research fresh.** Run several web searches, not deep research: new facts about the project (marketing status, prices published, delivery, the square's renewal), what competitors added, and the newest ways to build walkable 3D real-estate worlds and interactive sales pages. Every finding goes into the right file with its URL and date.
2. **Do the phase.** Take the first unchecked phase and do it end to end.
3. **Re-check the done phases.** A fact that changed is updated. A competitor that now has something we lack becomes a new item. A weak spot found anywhere becomes a new item. Nothing done is left at yesterday's level.
4. **Scale up.** Raise the bar by at least one notch every turn: a richer card, one more clickable place, a better view, a sharper sentence, a faster load, one more keyword covered. Write it under "Scale-up ledger" with its evidence.
5. **Write a sharper next step.** The next turn starts from it.

**No compromise:** no placeholder is shipped as final, no "good enough", no generic model passed off as the real one. What is not ready yet waits, labelled, and stays on the list.

## P9a (30.9, turn 12): LIVE as 1.72.371 (Design v104.1)

- **Runner 371, clean:**
  - 309 page checks OK; `[kh]` OK on all 5 pages;
  - the Hebrew post updated (its content-drift check matched 369's md5);
  - the record was written as it went; the bridge came down.
- **Live proof:**
  - `kh_first_screen_check.py` at 390, scroll 0 / 300 / 700, in 5 languages: **RESULT OK, the bar covers no button and no tab** (15 of 15 measures).
  - `content_first_check`: 0 failed across the fleet.
  - `source_audit`: GREEN. The diffs are explained: about 2.2 KB more on every page from the bar's new script, and the Russian page +1 style from the Cyrillic font link.
  - Looked at: he, ar, en and ru first screens.
- **New P9 items found by looking:**
  - (a) In Arabic, the bar rises above the three buttons and now sits over the lead's last lines. That is text, not a control, but it is the answer paragraph.
  - (b) The accessibility button (bottom corner) sits on the world's first tab in en and ru.

(the earlier plan, kept for the record:)

- **Design:** Claude Design v104.1 "KikarHamedinaFirstScreen" (artifact version 137), with before and after at 390, looked at.
- **What P9a prepared locally** (commit 6fc520c6):
  - **The phone's first screen.** The WhatsApp bar treats the hero buttons as controls and takes the nearest free place. The Kikar world starts 50 px lower, which leaves a 73 px lane for the bar.
    - Kikar, 5 languages: 10 overlaps (35,437 px²) → 0.
    - The fleet's pages: 12 → 0.
  - **The fixes:**
    - "1.25 מעלות" is written in words in Hebrew; a bidi isolate did not fix it in Chrome.
    - One "Mediterranean Sea" label instead of two.
    - Cyrillic from each font's own family, on the Russian page only.
    - "He Be'Iyar" in English.
  - **Day, sunset and night** in the floor view: night windows are labelled as illustration; draw calls unchanged; night is faster.
- **Runner 371:** it writes 3 files plus the Hebrew post's content, after a content drift check against 369's md5. The dry run was clean, and the release runs in the background.

## P8 RESULT (30.9, turn 10): LIVE as 1.72.370, fr/ru/ar

- **The pages:** /projects/hamedina-fr/ (post 8116), /projects/hamedina-ru/ (8117), /projects/hamedina-ar/ (8118). The Arabic title is in English, per the owner's 28.9 decision.
  - The world speaks 5 languages: `world.js` plus `hamedina/world-i18n.json`.
  - The P7.1 fixes are live: the WhatsApp refit on `load`, and verify_kh in the fleet's real order.
  - The Hebrew "המקור: … · עודכן" line is translated on every language page (`lang-pages.json`).
- **The runner (370)** ran in the background with no time limit, in one clean pass:
  - 309 page checks OK; `[kh]` OK on all 5 pages;
  - the record was written as soon as the files were in;
  - the bridge came down; no active bridge was left.
- **Live proof** (a real Chrome, 390 and 1440, fr/ru/ar and he):
  - one H1, the FAQPage, and 6 hreflang links each way;
  - the world opened by a real click, with its tabs in each language;
  - 0 console errors;
  - the WhatsApp message in the page's language carries the floor and the tower (for example "étage 30 · tour C").
- **Checks:**
  - `content_first_check`: 0 failed on all 5 pages.
  - `lang_pages_check hamedina`: 4 pages, 0 Hebrew left outside the article.
  - `source_audit`: GREEN on all.
- **What the audit found, and the fix:** the French page came out ORANGE "notice-above-article". The notice was right above the article, but French is longer than the 400-byte window measured from the notice's START. `tools/source_audit.py` now measures from the notice's END, and must be within 200 bytes. The controls (Rainbow, DUO, the Hebrew page) stay GREEN.
- **A new P9 item:** on the phone's first screen, the WhatsApp bar now clears the world's tabs but sits on the third hero button ("סיור וירטואלי בכיכר"). There is not enough room for both in that first frame, so this is a design decision for the P9 pass.

## P7 RESULT (30.9, turn 8): LIVE as 1.72.369

- **The pages:** https://nad-lan.co.il/projects/hamedina/ (post 8113) and https://nad-lan.co.il/projects/hamedina-en/ (post 8114). Featured image: attachment 8115.
- **Live proof** (a real Chrome, 390 and 1440, both languages):
  - one H1; the lead before the world on the phone;
  - FAQPage schema; hreflang he/en and x-default;
  - the world entered by a real click, with 4 tabs;
  - "קומה ונוף" gives tower C, floor 30;
  - 0 console errors;
  - one tap on WhatsApp sends "מקור: מגדלי כיכר המדינה… · פרויקט · קומה 30 · מגדל C".
- **Checks:**
  - `content_first_check.py`: 0 failed across the fleet.
  - `source_audit.py`: GREEN on both pages. The controls' diffs are explained: the home says 976 projects; the catalogue has one more card; Rainbow and H Infinity are about 400 bytes bigger from the wa-source facing line.
- **What went wrong and how it was closed:**
  - **The runner.** The shell's 590 s timeout stopped the runner in its second check round, after every file had been written and md5-verified and both posts read back 20/20.
    - The only failed check was the runner's own `[kh]` order expectation, and it was wrong: the fleet puts the notice and the article wrapper BEFORE the page's own sections (the checklist's C7).
    - Next runner: fix `verify_kh` to expect notice → article wrapper → sections, and run the release with a longer timeout, in the background.
  - **The bridge left behind.** Bridge 1009 was still active. `scripts/project-stage/bridge_sweep.py` (new) deactivated it.
  - **The release record.** `deploy-result-369.json` was written by hand from the pinned md5s. The public assets were re-checked live, all matching.
- **For the next release (P7.1):**
  - **(a) The phone's first screen.** The WhatsApp bar sits on the world's tabs until the first scroll. `conversion-cta.php` should refit on `window.load` too; this is fleet-wide.
  - **(b) The article** from the owner's ChatGPT run, into the empty `nadlan-project-article` wrapper.
  - **(c) `verify_kh`** as above.

## Scale-up ledger (newest on top)

- **1.10, turn 16.**
  - **Web:**
    - [Electra: completion April 2027](https://www.electra.co.il/en/electra_building/projects/kikar_hamedina_towers) and [Ashtrom: 2026](https://www.ashtromconstruction.co.il/en/projects/kikar-hamedina), both already in facts.md as a conflict;
    - [Globes EN 1001522524](https://en.globes.co.il/en/article-tel-avivs-kikar-hamedina-undergoes-transformation-1001522524), already there;
    - [OSM Wiki, Names](https://wiki.openstreetmap.org/wiki/Names): localized maps use name:<lang>, then name:en, then name.
    - **Re-check:** no contradiction.
  - **NOTCH (v104.8 → 1.72.379):** places named in the page's language from OpenStreetMap only.
    - The STRICT rule: the place's own OSM element, or a same-kind POI. Never a street, a parking lot, an area or a bare building. Never translated.
    - 30 places named (en 30, ru 3, ar 3), 12 of them within 10 minutes. 20 matches dropped as a different object, 9 ambiguous skipped.
    - Evidence: names-osm/ (README, matches.csv, the raw Overpass answer).
    - Live en: the transport, education and food names appear; the essentials and community names appear when those groups are switched on. 0 errors.
  - **Honest limit:** 304 places within 10 minutes still have Hebrew-only names (no name in any source). They keep their kind ("School").
  - **Deferred, with its reason:** `#nlps summary` in the a11y corner's and the WhatsApp bar's control lists. It is a 2-PHP-file live-text edit with pinned checks; it goes into the next PHP round.
  - **NEXT NOTCH:**
    - (1) 320 px world label density;
    - (2) the PHP round (`#nlps summary`, and the lead as a soft obstacle for the bar at 360 px);
    - (3) an owner-bar evening interior (a new render).

- **1.10, turn 15.**
  - **Web:**
    - [NN/G, bottom sheets](https://www.nngroup.com/articles/bottom-sheet/), [IxDF, progressive disclosure](https://ixdf.org/literature/topics/progressive-disclosure), [Lollypop, progressive disclosure 2026](https://lollypop.design/blog/2025/may/progressive-disclosure/);
    - prices: [Bizportal 20015974](https://www.bizportal.co.il/realestates/news/article/20015974), already in facts.md (S20); [Globes 1001481134](https://www.globes.co.il/news/article.aspx?did=1001481134), already there.
    - **Re-check:** no new fact contradicts the page.
  - **NOTCH (v104.7 → 1.72.378):** the long world card, organized.
    - The tower's own facts and the two actions come first. The facts about all three towers sit in a fold, closed on phones and open on desktop. Nothing is deleted.
    - Measured: the card is 1,077 → 489 px.
  - **FOUND ON THE WAY (a regression of 373, fixed here):** the green WhatsApp button in the phone's dock showed dark, underlined link text. The white-text rule was scoped to `.nlw`, and the dock sits outside it.
  - **Maya:** the owner is actively using the ChatGPT app (another thread), so the app was not driven. The update waits in claude-codex.md.
  - **NEXT NOTCH:**
    - (1) more named places at 320 px;
    - (2) generic en/ar names from OSM name:en/name:ar;
    - (3) a scan for other `.nlw`-scoped rules the dock may lose (done: only this one).
  - **Finding (live 378, element shot):** the floating accessibility button can sit on the card's last fold ("מה בתמונה להמחשה") in the dock at some scroll positions. P9c's corner script guards the world's controls, not the dock's. Next round: count the dock's summaries and buttons as controls.
  - **Transient:** 1 × HTTP 502 on /projects/ashira-sde-dov-en/ during 378's first check round; purge + second round OK; 3 × 200 after.

- **30.9 night, turn 14** (Opus 5.5).
  - **Web:**
    - [ynetnews: top Tel Aviv deals concentrate at District 4 / Kikar Hamedina and Sde Dov](https://www.ynetnews.com/real-estate/article/b11jju011zx) (context only);
    - [immobilier.co.il, Tel Aviv](https://www.immobilier.co.il/en/city/telaviv): asking prices of 4 rooms at ₪6.2-6.5M. These are ADS, not deals: never page facts;
    - [Tel Aviv Online on the renewed square](https://tlvonline.co.il/%D7%A9%D7%93%D7%A8%D7%95%D7%92-%D7%9B%D7%99%D7%9B%D7%A8-%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/): 560 new trees and heritage trees kept, already in facts.md from mako;
    - [Google Maps collision behavior](https://developers.google.com/maps/documentation/android-sdk/advanced-markers/collision-behavior): REQUIRED vs OPTIONAL markers;
    - [Mapbox label placement](https://docs.mapbox.com/help/dive-deeper/optimize-map-label-placement/).
    - The search engine's summary claims "occupancy early 2026"; it is unsourced and NOT used (facts.md keeps its sourced conflicts).
  - **Releases since turn 13, all live and verified:**
    - **1.72.373** (v104.3): one scroll on the phone, place icons, with Codex/Maya.
    - **1.72.374** (v104.4): Maya's QA fixes: no camera tilt, no icon overlap.
    - **1.72.375** (P9c, v104.2): the example apartment. The evening render was REJECTED as below the bar.
    - **1.72.376** (v104.5): the rest of Maya's QA:
      - map names from the opening zoom (the lazy RTL plugin);
      - world name+icon units with 44 px taps;
      - the desktop wheel;
      - the bar clears the floor slider.
      - The first run rolled back on stale pinned checks; the second passed.
  - **NEW NOTCH (this turn, v104.6 → 1.72.377):** the project becomes a REQUIRED mark on every area map (Google's collision model).
    - Its name shows under the page's own dot, and the places make room.
    - Where an HTML price chip covers it (Rainbow), the name steps back.
    - SEO tails are cut ("מגדלי DUO תל אביב").
    - Measured locally: Kikar and DUO show the name, Rainbow hides it (chips); 0 errors.
  - **NEXT NOTCH:**
    - (1) The long world card, 1,065-1,402 px on a phone (Maya): a summary with the main action first, then details by topic. Nothing deleted; Design first.
    - (2) The world's labels at 320 px: smarter placement (below, and to the side) so more places keep their names.
    - (3) Data: generic "School"/"مدرسة"/"Open" names in en/ar. Take names from OSM name:en/name:ar where they exist; never invent.

- **30.9 evening, turn 13** (new session, Opus 5.5). Web: [Ashtrom Industries on the project](https://www.ashtromindustries.co.il/en/projects/kikar-hamedina-industries), [the Ashtrom base-pile page](https://basepile.ashtromconstruction.co.il/en/projects/kikar-hamedina-base-pile), [ynetnews on the square's works](https://www.ynetnews.com/real-estate/article/r1w0etf111e) (background only, not page material), [off-plan 360 tours 2026](https://archeyes.com/off-plans-360-virtual-tours-how-it-can-help-to-market-pre-built-properties/).
  - **P9b's prototype is committed (3fc7f966).** It is an example apartment in tower C, floor 30, in Blender Cycles, with the real view at 117 m. It shows the twist on floors 20/30/38: the same window faces 278.1°, 265.6° and 255.6°.
  - **NEXT NOTCH (P9c):**
    - "היכנסו לדירה לדוגמה" inside the floor view, in the fleet's 360 viewer, with a gallery that follows the time of day, and the twist strip.
    - The Arabic first screen: the bar goes off the lead.
    - The accessibility button comes off the world's first tab.
    - Design v104.2 material; runner 373 chained after 372.
  - **Coordination:**
    - The parallel HAD-376 session was told to chain from 371 and report. Its message is queued.
    - Codex got a full status sync on HAD-373 and in the coordination file. Its scope ACK is pending.

- **30.9, turn 11** (web: [R2U interactive floor plans 2026](https://r2u.io/en/blog/interactive-floor-plan-real-estate/), [a luxury tower site with views at three times of day](https://www.6sqft.com/manhattan-view-condo-launches-full-website-touting-luxury-amenities-and-far-reaching-views/), [Madlan: 86 listings at the square](https://www.madlan.co.il/for-sale/%D7%9B%D7%99%D7%9B%D7%A8-%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91-%D7%99%D7%A4%D7%95-%D7%99%D7%A9%D7%A8%D7%90%D7%9C), [a Sotheby's high-floor 5-room listing](https://www.israelsir.co.il/property/5-room-apartment-kikar-hamedina-towers-tel-aviv/)).
  - The best 2026 sites render the actual sightline per floor, and show views at three times of day.
  - **NEW notches:**
    - (1) A day, sunset and night switch in the floor view, with night windows labelled as illustration (P9a).
    - (2) Example apartments whose window shows the REAL city from the world at the real height and facing. The twist means the same apartment faces a slightly different way on every floor, and the page SHOWS it (P9b).
  - **P9 started as two sub-agents:**
    - **P9a:** the small fixes (°1.25 bidi, "Mediterranean Sea" twice, a Cyrillic font), the phone's first screen (the bar vs the third hero button), the night view, and runner 371 prepared.
    - **P9b:** the interiors plan and a high-quality prototype of tower C, floor 30, facing west.

- **30.9, turn 9** (web: [Globes 1001481134](https://www.globes.co.il/news/article.aspx?did=1001481134), [ip-tlv](https://ip-tlv.com/properties/kikar-ha-medina-towers-project/?lang=en), [Evenis Group, a French agency](https://www.evenisgroup.com/en/property/ref-gs-18539-for-sale-4-rooms-kikar-hamedina-tel-aviv/), [Israel Property Hub](https://israelpropertyhub.com/property/for-sale-kikar-hamedina-tel-aviv-premium-apartment-in-a-new-luxury-project)).
  - **NEW FACT (Globes, data of 6.2024):** 148 units were sold in the neighbourhood over one year, at an average of ₪68,000/m², with an average deal of ₪5.66M. It goes into the area price line with its date.
  - **A MARKETING CLAIM, attributed only:** ip-tlv says "offered at about ₪55,000/m² vs a market of about ₪80,000/m²". Show it as their claim, or not at all.
  - **French demand exists:** a French-speaking agency lists 4-room apartments in the towers. That means P8 fr is worth the work.
  - **P8 started as a sub-agent:**
    - fr/ru/ar posts with a cultural rewrite, world strings in 5 languages, and SERP notes per language;
    - the P7.1 fixes (WhatsApp refit on load, verify_kh order);
    - a resilient runner 370 that writes its record as soon as the writes succeed and always takes the bridge down.

- **30.9, turn 6** (web: [Mako/N12 on the new square](https://www.mako.co.il/news-money/real_estate/Article-1b24331b3cec0a1026.htm), [tlvonline on the square's renewal](https://tlvonline.co.il/%D7%A9%D7%93%D7%A8%D7%95%D7%92-%D7%9B%D7%99%D7%9B%D7%A8-%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/), [project-tlv's timeline](https://project-tlv.info/buildings/kikar-hamedina/kikar-hamedina-project/)).
  - **VERIFIED (dog park):** the park has a dog garden, a play garden, lawns and tables, the ecological pond with paths and bridges, a boulevard with a bicycle path, three rows of trees including heritage trees, a running track and kiosks.
  - **The school (north):** fan-shaped, 3 upper floors, a green roof, an underground sports hall, and a field open to the public in the afternoons. It opened this school year.
  - **The community centre (south):** 5 floors, with a dance studio, art rooms, lecture halls and a multi-purpose hall.
  - All of these were sent to the world builder as clickable hotspots with sources.
  - **Timeline additions (project-tlv):** plan published 2013, approved 2015, permit application 2017, excavation permit 2018, tree transplanting 2019, committee approval 2021, permit 2022.

- **30.9, turn 5** (the prototype looked at; MYS read; Hebrew occupancy search: [Ashtrom](https://www.ashtrom.co.il/en/projects/kikar-hamedina), [Mako](https://www.mako.co.il/finances-real-estate/Article-cdd2b05daf37a91026.htm), [project-tlv](https://project-tlv.info/buildings/kikar-hamedina/kikar-hamedina-project/)).
  - **(1) The towers look like the real ones.** White slabs and white curtain walls per the architect, instead of a gold box. Gold now means "you chose this".
  - **(2) Hours of direct sun per facing.** Ray-tested against the real city blocks and shown per floor. No site in Israel shows this.
  - **(3) The phone's window view is framed on the view.** The prototype's phone frame was mostly sky.
  - **(4) The WhatsApp line carries tower and floor from the world**, through `window.__nlpsPick`.
  - **To verify next turn:** the dog park (Mako), and project-tlv's building timeline.

- **30.9, turn 3** (P1 facts, 82 sources; P3 live SERP with DataForSEO, about $0.01).
  - **(1) Win the AI Overview.** Google puts an AI Overview on top in Hebrew and English. The page states each fact as a short, sourced bullet or table row with the names Google uses. The FAQ answers the 7 People-Also-Ask questions word for word.
  - **(2) Deals table, sourced by floor and date.** The three Globes deals (floors 38-39) plus the area's ₪/m² for comparison. No competitor shows deals.
  - **(3) "When will it be ready?", answered honestly.** A dated table of what each party said (Ashtrom, Electra, Bareket, Globes, Bizportal), instead of one made-up date.
  - **(4) Our own construction timeline.** Dated milestones from public sources: the permit 12.2022, the first concrete 18.12.2022, the cores' rate, financing 9.2025, the school opening. This answers the video pack's "progress" intent.
  - **(5) Sales path.** A resale market of up to about 250 owners means the page leads with "for sale / for rent in the towers" (the Madlan intent) and routes to WhatsApp and brokers.

- **30.9, turn 2** (web search: [development sales sites 2026](https://vinode.io/), [unit finders](https://archicgi.com/interactive-real-estate-platform/), [3D visualization ROI 2026](https://intwopixel.com/blog/3d-real-estate-visualization-complete-guide), [the twist technique](https://medium.com/@crazypixel/geometry-manipulation-in-three-js-twisting-c53782c38bb) and [Cayan Tower's 1.2° per floor](https://en.wikipedia.org/wiki/Cayan_Tower)). The best off-plan sites in the world go tower → floor → unit, with view corridors, SUNLIGHT and distance to amenities.
  - **NEW for Kikar:**
    - **(1) Sun and shade per floor and facing.** The real sun path for Tel Aviv (32.09°N) by season and hour, on the turning towers. None of our pages has it; no Israeli competitor has it.
    - **(2) Performance budget.** Text and CTAs paint in under 1 s on a phone (a sub-second load is cited at 2× conversion). The 3D world loads after, on intent.
    - **(3) Twist geometry.** Each floor is a separate slab rotated 1.25° around the core. This is the Cayan method, and the floor slice and the 360 read the same angle.
  - **Not copied:** live availability and prices. They appear only where a source publishes them, since we never invent inventory.

- **30.9, turn 1.** The bar for the area world was raised: from "maps and places" to true-height buildings from the municipality's GIS (free), with photoreal options costed for the owner.
  - Next notch: the parcel geometry from govmap and the square's renewal plan.

## The laws (never broken)

- **G1, Claude Design first.** No visible code before a new design system version, published and looked at: artifact L9Nqz7Viv7K3MYeZrBc9s8, component "KikarHamedinaWorld".
- **Checklists:**
  - `docs/checklists/PROJECT-PAGE-CHECKLIST.md`: H1 → answer paragraph → CTAs → stage → view + map → facts → tools → article, on every width, phones first.
  - `docs/research/2026-09-24-rainbow-run/unit-layer-and-recipes.md`, section 3.
- **No invented facts.**
  - Every fact carries its source.
  - Conflicts are shown as conflicts, or the fact is omitted. The delivery date is 2026 per Ashtrom and 4.2027 per Wikipedia.
  - A price appears only if published, attributed and dated.
  - Example apartments are labelled "דירה לדוגמה".
  - Unknown means omitted on sales surfaces.
- **Frozen:** `engine.js` internals and the original map beam and cone.
- **Never:** EcoCity or Stricker, noindex, touching the sitemap, or printing secrets.
- **The URL word law:** run `tools/gsc/url_word_audit.py` before minting the slug. "kikar" is owned by /tel-aviv-plans/kikar-atarim/; "hamedina" is free.
- **Every release** goes through:
  1. the runner `scripts/project-stage/deployNNN.py`, with drift checks, backups, page checks and rollback;
  2. `tools/content_first_check.py`;
  3. `tools/source_audit.py`, before and after;
  4. a live check on phone and desktop, looked at;
  5. `tools/wa_bar_audit.py` on the new page;
  6. a Linear comment, a Notion row, and a Hebrew report with screenshots.
- **The WhatsApp bar** is on the page, and one tap opens WhatsApp. It is never hidden.
- **Don't stop to ask.** Owner questions go under "Waiting for the owner" and the loop moves on.
- **Grinding goes to a sub-agent.** Scraping, bulk research and long crawls go to a sub-agent with a self-contained prompt. This session does design, integration, verification and decisions.

## What we already know (sourced; research/kikar-hamedina-research.csv, 29.9)

| Fact | Value | Source |
|---|---|---|
| Towers | 3: two of 40 floors (towers A and C, 160 m) and one of 37 (tower B, 157 m); every floor turns 1.25° | Wikipedia; Ashtrom |
| Apartments | 453 | Wikipedia; Ashtrom; Globes 14.12.2022 |
| Parking | 1,620 (Globes: 906 for residents and 720 public) | Ashtrom; Wikipedia; Globes |
| Who builds | Electra Construction and Ashtrom, executing together; the developers are the landowners | Globes 14.12.2022; Wikipedia |
| Architect | Yaski Mor Sivan | Wikipedia; homeland |
| Facilities | pool, gym, spa, treatment rooms, multi-purpose halls; at ground level a public park with a lake, paths and play areas | Ashtrom; Globes |
| Timeline | permit and start of work 12.2022; completion 2026 (Ashtrom) vs 4.2027 (Wikipedia): a CONFLICT | Ashtrom; Wikipedia |
| Price | "from 10 million" for 4-5 rooms, from ONE marketing site: unverified, not to be used as fact | newhomesisrael |

**Monthly demand (DataForSEO, Israel):**
- כיכר המדינה תל אביב 390
- kikar hamedina towers 320
- מגדלי כיכר המדינה 260
- kikar hamedina 260
- פרויקט כיכר המדינה 170
- kikar hamedina tel aviv 140
- כיכר המדינה מגדלים 110
- כיכר המדינה מפה 90
- דירות להשכרה כיכר המדינה 90
- מגדלי כיכר המדינה למכירה 70
- פרויקט כיכר המדינה מחירים 50
- The bare "כיכר המדינה" (5,400) is mostly shopping intent.

**Who ranks today:** Ashtrom, Wikipedia, Globes, civileng, Madlan (88 resale listings), homeland (~550 characters), wxg, newhomesisrael.
- None of them has a map, an FAQ, a sourced price, a 3D model or floor views.
- Related searches: למכירה, מדלן, אדריכל, להשכרה, חנויות, תמונות.

## The phases (tick with evidence; the first unchecked is the next step)

- [x] **P0 DONE 30.9: `docs/research/2026-09-30-kikar-hamedina/feature-inventory.md`** (83 features in 11 groups, "forgotten or partial" list, a 17-step build recipe). What it means for the build:
  - **(a) No stage can turn a floor.** Each project's stage.js is a 164-182 KB copy of the same engine.
    - Kikar's 1.25° per floor touches the tower geometry, `floorPlan()`, the bearings, `nadlan_ps_unit_resolve()`, the slice, the sight lines and the 360.
    - A twist formula exists in `docs/playbooks/glb-gen-toha2-v2.py`.
    - Decision at P4: extract ONE shared stage engine rather than a fifth copy (engine.js stays frozen; this is the per-project stage layer).
  - **(b) Bearings are per project today.** Kikar needs a bearing per tower AND per floor, and direction words per tower.
  - **(c) The free world, option (a) of Q1, already exists.**
    - `build_city_*.py` reads Tel Aviv's building-height layer.
    - DUO's places.json already names the square's school, community centre and shops.
    - Option (b), Google photoreal through Cesium, exists as `inc/earth-experience.php`, but `/earth/` answers 401.
  - **(d) Rainbow text leaks when a config key is missing.** Tour words, `view_src`, `poster_alt`, `src_line`, the hard-coded 360 floors 25/10/36, the `living-25w-card.jpg` gate and `'25-'`: every key must be set for Kikar.
  - **(e) Adding a project is manual.** Edit the lists in `build_places.py`, `measure_eyes.py`, `stage_harvest.py`, `content_first_check.py`, `source_audit.py` and `nadlan_ps_unit_resolve()`.
    - Write the missing `project-page-factory` skill while doing it.
  - **(f) No price until it is sourced.** The deals table needs at least 2 sourced deals tied to a floor.
  - **(g) SEO specifics:**
    - the answer paragraph is the first paragraph of the content with 100+ characters;
    - the article goes in `nadlan-project-article`;
    - the FAQ schema comes only from a visible `<h2>שאלות נפוצות`;
    - language pages need `_nl_faq_schema`;
    - check read-only whether a Kikar catalogue post already exists.
  - **(h) Unreleased branch work Kikar depends on:** the docked card, the map landing, "מחיר מוערך", the per-unit request, `nadlan_ps_unit_resolve`, and bridge.js v101.2.
    - On the LIVE site the WhatsApp source line cannot carry the floor yet: only the unreleased bridge.js sets `window.__nlpsPick`.
  - **(i) The selling path stops at WhatsApp.**
    - There is no LiveKit key, so the shared room has no video.
    - The basket is Hebrew only; payments were never proven; a lost response duplicates a lead.
    - These are sales items for P7 and P9.
- [x] **P0 (the original task text) Recon of everything we built.**
  - Inventory every feature on Rainbow, DUO, Dimri, Ashira and H Infinity:
    - the stage, the floor slice, the building walk, the 360 rooms, the facilities pill and hotspots;
    - AreaLife maps with walking minutes and the view per floor band from real eye heights;
    - styles, the designer, the basket, the video call, the shared viewing room;
    - WhatsApp, the FAQ, schema, hreflang and the 5 languages;
    - the film and its player, the deals and price line, the official lot.
  - Read `docs/loop/FORGOTTEN-2026-09-28.md`, the Codex open items, and HAD-346.
  - Output: `docs/research/2026-09-30-kikar-hamedina/feature-inventory.md`, listing every feature with where it lives and "reuse / improve / new for Kikar".
- [x] **P1 DONE 30.9: `docs/research/2026-09-30-kikar-hamedina/facts.md`** (82 sources, 21 conflicts with both sides, gaps listed). What it means for the page:
  - **Sales reality.** There is no developer sales campaign: about 250 landowners resell through brokers, and at most 200-250 units are expected on the market.
    - The page sells through us (WhatsApp) and the brokers, never presenting the site as the broker (Brokers Law exemption).
  - **Sourced price material.**
    - Deals (Globes 2.5.2025): three 4-room 140 m² apartments on floors 38-39, ₪9.58M (4.2024), ₪9.59M (5.2024), ₪10.63M (12.2024, ₪75,913/m²). This is at least 2 deals tied to floors, so the deals table can go up.
    - Asks, dated and attributed: a floor-39 penthouse 258+57 m² at ₪43M; 168 m² at ₪13.7M (29.1.2026); 154 m² on floor 35 at ₪14.5M.
    - Area averages: ₪67,747/m² (Madlan via ynet 19.7.2025); deals near the square at ₪63K-66K/m² (Tax Authority via ICE 28.4.2026).
  - **The plan.**
    - תא/מק/2500/א (in force 24.6.2013): 77.743 dunam, block 6213, 28.94 dunam housing.
    - 507-0193490 (30.3.2018): traffic changes, the underground road cancelled.
  - **The team.** Architect MYS (competition, 2000); project management WXG; landscape T.M.A; structure Ben-Avraham.
    - Financing: Bareket with Clal and Migdal, about ₪2.05B (Globes 25.9.2025).
    - Execution: Electra and Ashtrom, ₪1.4B.
  - **The park.** About 40 dunam, a 1 m deep ecological pond, 560 new trees plus 36 kept, a 750 m running track, ₪150M of public works due by the end of 2027 (Mako 24.9.2026).
    - An 18-class school plus 6 special-education classes, an underground sports hall and a community centre. Mako says the school opened this school year.
  - **Commerce.** The project's own is only 3-4 kiosks; the 8,500 m² figure is the EXISTING shop ring around the square.
  - **The delivery date: shown as sourced statements, never one invented date.**
    - Ashtrom: 2026
    - Globes 2023: 12.2026
    - Electra and Wikipedia: 4.2027
    - Bareket's CEO, 9.2025: "within two years"
    - Bizportal: end of 2028
  - **Key conflicts that the model and the text must respect:**
    - Floors: 40/40/37 vs 42.
    - Heights: 160/160/157 vs 156.
    - Twist: 1.25° vs 2.5°. Use 1.25° (Wikipedia, WXG, MYS) and log the other.
    - Park size and lake size.
  - **Gaps:**
    - Units per tower and per floor, and the official unit mix.
    - Ceiling heights; floor plans; green standard; Form 4; an official marketer.
    - So there are no per-unit facts, and every interior is "דירה לדוגמה".
  - **Image rights.** No stock image (Alamy) on a sales page. Official renders only with permission.
- [x] **P1 (the original task text) Facts, deep.**
  - Official sources: the developers and landowners, Ashtrom, Electra, the architect's site, the Tel Aviv municipality (the square's renewal plan and the plan numbers), govmap for the parcel, Globes, Calcalist, TheMarker, Wikipedia.
  - Collect: unit mix and typologies, floors per tower, lobby and facilities, the commercial ring, the public park and lake, the parking split, the timeline, the marketing status, and published prices with dates.
  - Output: `facts.md`, with a source URL and date for every line and conflicts listed.
- [x] **P2 DONE 30.9.** Files: `places.json`, `city-blocks.json`, `sight-landmarks.json`, `area.md`, `eye-kikar-provisional.json`, `kikar-stage/quarter.json`, `kikar-stage/city.json`, and the build scripts `build_area_kikar.py` and `enrich_places_kikar.py`. `build_places.py` gained a `kikar` entry, and the four existing projects are unchanged.
  - **The plot centre** is 32.086758, 34.789776: the area-weighted centre of plan 2500ב's lots 101, 201-208 and 303 (47,846 m², municipal lots layer). OSM way 727196846 lies 11 m away.
  - **The towers**, from the municipal building layer:
    - A is 78 m south-west of the centre, B 78 m south-east, C 75 m north-east.
    - Permit addresses: ה' באייר 25, 45 and 65.
    - **NEW FACT:** the city's building-site record says the FRAME WAS COMPLETED on 23.4.2026.
    - **NEW CONFLICT:** the city lists all three at 40 floors and 160/158.2/160 m. The permit record notes 2 added floors for B. Wikipedia and Ashtrom say B has 37 floors and 157 m. Carry this into facts.md, and model B with the source shown.
  - **Places:** 1,245 within 1.5 km with walking minutes (182 within 5 minutes, 463 within 10, 843 within 15).
  - **Buildings:** 1,102 within 700 m with heights (1,075 from the city's 2019 survey, 23 from its surface model, 4 estimated and labelled).
  - **Also:** 95 towers of 70 m or more within 2 km, 349 street lines, 108 green areas, 20 landmarks and 68 skyline buildings of 100 m or more.
  - **Transport:**
    - Purple line, planned 2028: Ichilov station 350 m, about 2 minutes' walk.
    - Red line, running since 18.8.2023: Arlozorov 859 m.
    - Savidor rail station 852 m.
    - Green line (Ibn Gabirol) planned 2030.
    - 53 bus lines within 5 minutes (Ministry of Transport GTFS 8.9.2026).
  - **Distances:**
    - Weizmann 139 m, Namir 526 m, Ibn Gabirol 718 m, the Ayalon 804 m.
    - Ichilov 0.7-0.85 km.
    - Park HaYarkon's nearest edge 1,020 m, 13 minutes.
  - **Public buildings (municipal design decision 4.8.2021):** the north one is the school and the south one the community centre. OSM labels them differently.
  - **Provisional until P5:**
    - Walks start from the ring road, because the lobby doors are unknown.
    - Sight lines are computed from the plot centre, with eye height (floor − 1) × 4 + 1.6 m, and the towers are not yet obstacles.
  - **Not found:** the lake's outline, Park HaYarkon's gates, and the M1 metro stations.
  - **Defect found in the LIVE maps:** Rainbow, DUO, Dimri and Ashira compare unrotated places against buildings rotated 10-11°, so their "seen/hidden" labels are probably wrong. This is **HAD-376**, a separate task, offered to the owner as a one-click task.
- [x] **P2 (the original task text) The area.**
  - Run the place registry (`scripts/project-stage/build_places.py`: findplace.co.il + OpenStreetMap + Mapbox walking) for Kikar Hamedina.
  - Include: the square and its shops (the luxury ring), the parks (HaYarkon, the square's own park), schools and kindergartens, transport (roads, the light rail, buses), health, culture, sport, and cafés.
  - Add sight lines per floor band per tower, using real eye heights.
  - Output: `assets/project-stage/kikar/places.json` and `area.md`.
- [x] **P3 DONE 30.9: `docs/research/2026-09-30-kikar-hamedina/serp-dna.md`.**
  - **AI Overviews** lead both the Hebrew and the English results and cite short, sourced fact bullets.
  - **7 People-Also-Ask questions** become the FAQ; 12 related searches become sections.
  - **Titles** are decided, and so is the H1.
  - **URL** (url_word_audit 30.9): `/projects/hamedina/` and `/projects/hamedina-en/`. "kikar" and "towers" are taken; "hamedina" is free.
- [x] **P3 (the original task text) SERP and competitor DNA.**
  - GSC for the last 28 days, and DataForSEO within $5: keywords, People Also Ask, competitor page structure, intent.
  - Run the URL word audit and choose the slug.
  - Output: `serp-dna.md` and the slug decision.
- [x] **P4 DONE 30.9: Claude Design v104 "KikarHamedinaWorld" published** (artifact L9Nqz7Viv7K3MYeZrBc9s8, version 136) and looked at.
  - It holds the page order on a phone, the four ways into the world with real prototype renders, the twist, sun and shade, the sourced fact table, deals and prices, "when is it ready?", the FAQ and the honest labels.
  - The spec is copied at `docs/design/kikar-hamedina/KikarHamedinaWorld-v104-README.md`.
  - The prototype (`docs/research/2026-09-30-kikar-hamedina/prototype/`) holds:
    - 9,079 real buildings with heights;
    - 11,669 tree crowns from the city's 2024 canopy layer;
    - the towers built floor by floor with 1.25°;
    - the real sun, checked: sunsets 19:51 in June and 16:41 in December; shadows of 286 m at 13:00 on 21.12.
  - **Fixes carried to P5:**
    - The facade is WHITE slabs and white curtain walls per MYS (m-y-s.com/Kikar-Hamedina, read 30.9: "a repetitive system of floor slabs and white curtain walls", "each residential floor … sets back from the floor beneath and rotates in a circular movement"). Gold is the selection highlight only.
    - The phone's window view is framed on the view, not the empty sky.
    - Labels are bigger on phones.
- [x] **P4 (turn 4 note) IN PROGRESS (30.9).**
  - The spec is written: design system component `KikarHamedinaWorld/README.md`, v104. It covers:
    - the page order;
    - the world's four modes: aerial, walk, tower with the sun clock, places;
    - the shared engine module `assets/project-stage/world/`;
    - the selling path, prices (sourced only), "when is it ready?", the FAQ and SEO.
  - A sub-agent is building a LOCAL 3D prototype from the real data, with renders at 1440 and 390: aerial, street, window views, sun and shade, the twist. It lives in `docs/research/2026-09-30-kikar-hamedina/prototype/`.
  - Next: the preview.html with the renders, then publish design system v104, then look at it.
  - To verify: a "dog park" in the square's park (search 30.9, Mako article), and project-tlv.info's building page as a timeline source.
- [ ] **P4 (the original task text) Claude Design "KikarHamedinaWorld"**, a new design system version. It covers:
  - the page order per the checklist;
  - the walkable area world (walk and fly, and every place clickable with an info card);
  - the three turning towers on the real lot;
  - the hotspots, the facilities, and the window views per floor;
  - the unit layer (example apartments labelled);
  - the sales path (WhatsApp, the representative, the basket);
  - Hebrew and English.
  - Publish it and look at it.
- [x] **P5 DONE 30.9: the shared world module, local commits be03ba1e and 2be12a5d.**
  - **The files:**
    - `assets/project-stage/world/world.js` (140 KB, 43 KB gzip) and `world.css`.
    - `assets/project-stage/hamedina/world.json` (865 KB, 334 KB gzip), `places.json`, and posters (webp/jpg at 1600 and 800).
    - `scripts/project-stage/build_world_hamedina.py` and `poster_world_hamedina.py`.
    - A harness and 32 screenshots in `docs/research/2026-09-30-kikar-hamedina/world-shots/`.
  - **The API:** `mountWorld(el,{dataUrl,placesUrl,lang,i18n,onPick,poster,intent})`, with setMode, pickTower, setFloor, setFacing, setSun, sunHours, walkTo and more.
    - Events: `nl:floor` and `nl:facing`.
    - It sets `window.__nlpsPick`, so the WhatsApp line reads "קומה 30 · מגדל C".
  - **Performance:** 34-64 draw calls; 38-52 fps on desktop and 56 fps on the emulated phone (real phones not measured); ready in 1.0-1.6 s; about 0.73 MB on the wire, loaded on intent only.
  - **The world:**
    - 8 park hotspots with sources, marked "מיקום להמחשה".
    - Tower cards with both of B's versions.
    - Direct-sun hours for each of the 8 facings.
    - Window views naming the landmarks; street routes; Hebrew and English.
  - **Looked at, 30.9:** the quality is high.
  - **Fixes carried to P7:**
    - (1) The card's "ייעוץ חינם על מגדל X" button uses the WhatsApp green (#0F7A63), not terracotta, which is for money CTAs.
    - (2) The walk's start point: the near tower fills too much of the frame.
    - (3) `wa-source.php` should also print the facing (one line).
  - **Still open:** interiors and 360 per facing ("דירה לדוגמה"); which tower the Globes deals are in (unpublished); fr/ru/ar strings; a real-phone test.
- [x] **P5 (turn 5 note) IN PROGRESS.** A sub-agent is building the SHARED world module locally:
  - `assets/project-stage/world/world.js` and `world.css`, with the API `mountWorld(el, {dataUrl, placesUrl, lang, i18n, onPick})`. It sets `window.__nlpsPick` so the WhatsApp source line carries tower and floor.
  - The four modes: aerial, walk (joystick and WASD, collisions), tower (floor, facing, window view, sun clock, hours of direct sun per facing), places.
  - `assets/project-stage/hamedina/world.json`, built by `scripts/project-stage/build_world_hamedina.py`, about 1.5 MB loaded on intent.
  - A poster image; a test harness with screenshots at 1440 and 390; fps and bytes.
  - It does NOT touch engine.js, the existing stages or PHP.
- [x] **P6 DONE 30.9: `prompt-he.md` (110 KB) and `prompt-en.md` (86 KB).**
  - **The structure:**
    - 15 H2s in each language.
    - About 190 facts, 103 table rows and 23 conflicts, stated calmly.
    - A positive "איך קונים" section in 7 steps.
    - 12 FAQ entries: the first 7 are Google's People-Also-Ask questions, word for word.
    - Internal links: 28 in Hebrew and 23 in English, every one checked 200 and indexable on 30.9.
  - **The owner runs them:** attach the file in ChatGPT Pro, then paste the result back.
  - **Titles:** "ותלת ממד" / "& 3D" stay in the SEO titles. The site already uses "תלת ממד" in its menus; the body text keeps the language rules.
  - **Flags:**
    - The tax rules are copied from the verified H Infinity list and marked [לאישור הבעלים].
    - "Benini" has no source, so ChatGPT verifies it or says nothing.
    - No kashrut data: the text says to check the certificate at the place.
- [x] **P6 (turn 5 note) IN PROGRESS.** A sub-agent writes `prompt-he.md` and `prompt-en.md`: marketing and positive per the owner, sourced, with the 7 People-Also-Ask questions as the FAQ, and internal links checked for 200.
- [ ] **P5 (the original task text) The models.**
  - The three towers with the 1.25° turn per floor, heights 160/157 m, on the official parcel.
  - The square's ring and the park with the lake.
  - The surrounding blocks at the right heights (OSM heights, else floors × 3.2 m, labelled).
  - One world, walkable at street level and flyable, where every key place is clickable.
  - Interiors: example apartments and 360 rooms per facing, with views from the real floor heights.
- [ ] **P6, The article.**
  - A ChatGPT Pro prompt built from the SERP DNA: 5,000+ net words, marketing tone, positive, the richest facts, every fact sourced, Hebrew and English. It goes in the chat as a copyable block.
  - The owner runs it and the result goes in. The agent never writes the mega-article itself.
- [ ] **P7a PREPARED LOCALLY 30.9 (not released; the coordinator runs the runner).**
  - **The page:** a 'hamedina' entry in `nadlan_ps_config()` mounts the SHARED world module (`mountWorld`), no stage.js copy, no bridge.js; no tour, 360 or example apartments (no interiors yet); Hebrew and English words printed directly. The three deals (Globes 2.5.2025, floors 38-39, tower not published) and the area price line are in the config.
  - **How it ships:** `scripts/project-stage/hamedina_ps_patch.py` holds the change as 8 anchored hunks. The release copy is the LIVE base 65af09be + these hunks, so Batch 1/2 (branch only) is NOT released. `ps_identity_proof.py`: Rainbow, DUO, Dimri and Ashira, Hebrew and English, byte for byte the same (branch and release).
  - **P5 fixes done:** the card's consult button is WhatsApp green #0F7A63 (and stays white on the site's link styles); the walk starts on the ring's south side by Weizmann (tower C framed between A and B); `inc/wa-source.php` prints the facing ("קומה 30 · מגדל C · מערבה"). Also: the card's message names the tower or place; the English world shows no Hebrew-only places or lines.
  - **The content:** `docs/research/2026-09-30-kikar-hamedina/post-he.html`, `post-en.html` (the lead first, the facts table with conflicts as two versions, prices, for sale, "when", the timeline, the park, the square, transport, 12 FAQ with the 7 PAA first, the empty article wrapper). Copy gate: `scripts/project-stage/kikar_copy_gate.py`.
  - **SEO and posts:** `scripts/project-stage/hamedina_page_data.py` (titles, descriptions, meta, `_nl_faq_schema` for English); `scripts/seo/project_meta.py` has both.
  - **The runner:** `scripts/project-stage/deploy369.py`, generated by `gen_deploy369.py` from deploy368 (every file and both contents pinned by MD5). Not run.
  - **Local preview:** `scripts/project-stage/preview_hamedina.py`, 55 shots in `docs/research/2026-09-30-kikar-hamedina/p7-shots/` (looked at), content first C3/C4 pass at 390, 412 (Googlebot) and 1440 in both languages.
  - **Next:** the coordinator runs `python scripts/project-stage/deploy369.py --dry`, then without `--dry`; then content_first_check, source_audit (a baseline for the two new URLs), wa_bar_audit and live eyes.
- [x] **P7 DONE 30.9: live as 1.72.369.** See "P7 RESULT" above. Commits 0d594592, cfb26280 and 55ce22e3.
- [x] **P7 (the original task text) Build and release, Hebrew and English.**
  - The project post and config.
  - The stage `kikar/`, the places, the facilities JSON, the tour.
  - SEO: title, description, schema, FAQ, hreflang.
  - Check locally at 390 and 1440, then release through the runner. Run the content-first, source, WhatsApp and live-eyes checks.
- [x] **P8 DONE 30.9: LIVE as 1.72.370 (see "P8 RESULT").** fr, ru, ar (Arabic titles in English, per the owner's decisions of 28.9).
  - **PREPARED LOCALLY 30.9 (not released; the coordinator runs `scripts/project-stage/deploy370.py`, generated by `gen_deploy370.py`).**
    - SERP per language: `serp-fr.md`, `serp-ru.md`, `serp-ar.md` (DataForSEO about $0.46: French demand exists, "tours" reads as sightseeing in French; Russian in three spellings; Arabic-script demand near zero, so the English title fits).
    - Posts `post-fr.html`, `post-ru.html`, `post-ar.html` (15, 16 and 16 FAQ; `kikar_copy_gate.py` OK in five languages; `kikar_typo.py` for each language's spacing).
    - The world in five languages: `world.js` I18N fr/ru/ar + `hamedina/world-i18n.json` (the data's texts, keyed by the English); Hebrew-only names left out.
    - The page top: `hamedina_ps_patch370.py` (369's live text + 4 hunks); `ps_identity_proof370.py`: every existing page byte for byte the same.
    - P7.1: the pill measures again on load; `verify_kh` in the real C7 order for all five pages; the runner writes its record at once and always ends with the bridge down. Extra: the card's Hebrew source line now translates on language pages (`lang-pages.json`), the Russian pill no longer pushes its mark off a 360-390 px screen, Arabic degrees as a word.
    - Preview: `preview_hamedina.py --p8`, shots in `p8-shots/`, C3/C4 pass at 390, 412 (Googlebot) and 1440.
- [ ] **P9, IN PROGRESS (turn 11: P9a fixes + phone first screen + night view; P9b interiors). The masterpiece pass.** Every hotspot, every click, and every width, looked at. Then compare with every competitor page, and fix what is weaker.

## Tracking

- Linear: HAD-375 (https://linear.app/hadmaia/issue/HAD-375)
- Notion row: https://app.notion.com/p/3eaab55be7a18104afcbdf82347fe085

## Waiting for the owner

- **Q3, 30.9: who answers WhatsApp messages written in French, Russian and Arabic?** The fr/ru/ar pages send their visitors to the same number, and each message says which page it came from.

## P9 list (the masterpiece pass), gathered so far

- **Status 30.9 night.** DONE and live:
  - the phone flow (373/374/376);
  - place icons and names (373/376/377);
  - the example apartment by day and at sunset (375);
  - the degrees bidi, the sea named once and Cyrillic (371);
  - the Arabic first screen and the a11y corner (375).
- **OPEN, in order:**
  - (a) the long world card, organized, nothing deleted;
  - (b) 320 px label density;
  - (c) en/ar generic place names (data);
  - (d) M04/M05, two pointers and page pinch;
  - (e) a real-device check (the owner's iPhone);
  - (f) an evening interior at the owner's bar (a new render, not the rejected one);
  - (g) the twist's direction, from a source;
  - (h) the shared viewing room and the video call wired to the world;
  - (i) the article (the owner's ChatGPT run).

- **"1.25°" shows as "°1.25"** in right-to-left text on the live Hebrew page. Wrap it in `<bdi>` or put the degree sign inside an LTR span.
- **The window view names "Mediterranean Sea" twice**, in every language, the live pages included.
- **Cyrillic in the world falls back to system fonts**, because the site's fonts have no Cyrillic. Add a Cyrillic subset.
- **On an Arabic phone's first screen, the WhatsApp pill covers the third hero button.** Its avoid list does not include hero buttons; this needs a design decision.
- **Interiors and 360 per facing**, labelled "דירה לדוגמה", in the higher quality the owner asked for (28.9).
- **The article** from the owner's ChatGPT run.
- **The shared viewing room and the video call** are not wired to the world yet.

- **Q2, 30.9: the two article files** (`prompt-he.md`, `prompt-en.md`, sent to him in chat) run in ChatGPT Pro. He pastes the results back.
  - The page can go live without the article: the world, the sourced lead, facts, deals, "when is it ready?" and the FAQ are real content, not placeholders.
  - The article joins in the next release the moment it arrives.

- **Q1, 30.9: how photorealistic should the area world be?** The default is (a). (b) and (c) need his word because they cost money. The loop continues with (a).
  - **(a) Free, the default.** Tel Aviv municipality open GIS: building footprints and heights for every building ([opendata.tel-aviv.gov.il](https://opendata.tel-aviv.gov.il/en/Pages/Category.aspx); [OSM forum on the height layer](https://community.openstreetmap.org/t/using-gis-tel-aviv-for-buildings-heights/85546)). We build the blocks ourselves, in the house style, true to height.
  - **(b) Google Photorealistic 3D Tiles**, streamed into three.js through 3DTilesRendererJS ([Google overview](https://developers.google.com/maps/documentation/tile/3d-tiles-overview); [real-estate use](https://mapsplatform.google.com/resources/blog/helping-buyers-make-more-confident-real-estate-decisions-with-photorealistic-3d-tiles/)).
    - It needs a paid Google Maps Platform key and attribution, and its terms limit caching.
    - It is photoreal, and this is how Zillow-class sites show neighbourhoods.
  - **(c) A Gaussian-splat capture** of the square by drone ([real-estate guide 2026](https://www.utsubo.com/blog/gaussian-splatting-commercial-real-estate); [MapTiler GeoSplats](https://www.maptiler.com/geosplats/)).
    - It is the most real, and Zillow SkyTour and Apartments.com shipped it in 2025-26.
    - It costs about $2,000 to $50,000 and needs a flight permit.

## Log (newest on top)

- **30.9, turn 1:**
  - Created the state file.
  - Opened Linear HAD-375 and a Notion row.
  - P0 (inventory) and P1 (facts from web search) are running as sub-agents.
  - Web search: three ways to build the area world (see Q1). Tel Aviv's open GIS carries a height for every building, so a true-height free world is possible now.

- 30.9.2026: the loop was armed; this file was created from the owner's order and the 29.9 research.
