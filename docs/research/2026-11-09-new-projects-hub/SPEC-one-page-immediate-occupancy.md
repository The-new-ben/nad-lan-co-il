# /projects/ as the one page of the new-projects intent, with an immediate-occupancy finder (spec for Ben's approval, 9.11.2026)

Status: **proposal**. Nothing here is live. Ben decides; then design, data, build, release, proof, in that order.
Evidence:
- `israel/intent-overlap.md` (one intent: 3-6 shared Google results);
- `practitioners-one-page.md` (21 sourced practitioner items);
- `world/immediate-occupancy-tools.md` (20 sites, a 33-row matrix, 6 world-first candidates);
- `israel/keyword-map.md`, `israel/serp.md`, `israel/our-pages.md`.

## 1. The decision
- **One page:** `/projects/` owns פרויקטים חדשים, דירות מקבלן, דירות חדשות, דירות לאכלוס מיידי / אכלוס קרוב, על הנייר / פריסייל, דירות מקבלן במבצע, the budget forms and the city forms. No second URL on this intent, ever. The Tel Aviv immediate-occupancy URL stays a 301 (Ben, 9.11).
- **Every sub-intent gets a full section:** its own heading in both forms, a live count, a filter, a table, a map layer and a self-contained answer. This follows the practitioners (Zerodown, Amsive, Badush) and answers the risk that Yad2 wins "אכלוס מיידי" and "מבצע" with dedicated filtered URLs.
- **Informational phrases stay on the guides:** קניית דירה מקבלן, מה זה דירה על הנייר, איך עובד 20/80. The guides link to /projects/ with varied anchors, a few at a time, never sitewide in one day.

## 2. Synonyms and forms carried by the page (Ben's law, 9.11)
- **Immediate occupancy:**
  - core forms: אכלוס מיידי · לאכלוס מיידי · באכלוס מיידי · אכלוס קרוב · לאכלוס קרוב;
  - ready flat: מוכנה לכניסה · דירה גמורה · דירות מוכנות מקבלן · כניסה מיידית · מסירה מיידית;
  - after delivery: פרויקטים מאוכלסים · אחרי טופס 4 · מפתח ביד;
  - abbreviation: טופס 4 / תעודת גמר.
- **From a developer:** דירות מקבלן · דירה מקבלן · דירות חדשות מקבלן · יד ראשונה · ישירות מהקבלן · דירות קבלן · פרויקטים בשיווק · פרויקטים חדשים למגורים.
- **Stage:** על הנייר · פריסייל · פרי סייל · בבנייה · בשלד · לפני היתר · אחרי היתר · בשיווק.
- **Deals:** מבצע · מבצעי קבלנים · 20/80 · 10/90 · 15/85 · ללא הצמדה · פטור ממדד · דחיית תשלום · הלוואת קבלן · ריהוט מתנה.
- **Spellings and abbreviations:**
  - פרוייקטים / פרויקטים · משכנתא / משכנתה · דירת 4 חד׳ / 4 חדרים;
  - cities: ת״א · ר״ג · פ״ת · ראשל״צ · ב״ש;
  - fixed abbreviations: ממ״ד · יח״ד · מ״ר.
- **Budget:** עד מיליון · עד 1.2 מיליון · עד 1.5 מיליון · עד 2 מיליון · מיליון וחצי.
- **Where the forms go:** headings, the answer paragraph, filter labels, table headers, alt text, FAQ and schema. Always as natural sentences, never as a keyword list.

## 3. Rendered order (phones first; intent-first law)
1. **H1 (corrected on Ben's word, 9.11, built only from the words in Google's page-1 titles for "פרויקטים חדשים"):** פרויקטים חדשים ודירות חדשות בישראל.
   - **Where the words come from:**
     - Yad2 #1: "פרויקטים ודירות חדשות בתל אביב יפו - מעודכן ל-2026".
     - Madlan #2: "דירות ופרויקטים חדשים בישראל".
     - The municipality: "פרויקטים חדשים".
     - nadlan.com: "לוח דירות חדשות, פרויקטים חדשים ודירות קבלן".
   - **Title:** פרויקטים חדשים ודירות חדשות למכירה בישראל - מעודכן ל-2026.
   - **Each section's H2 comes from that sub-phrase's own SERP:**
     - דירות חדשות לאכלוס מיידי: Ashtrom's title and the related search;
     - לאכלוס קרוב: Yad2;
     - פרויקטים חדשים בשיווק: Dimri and the related search;
     - פרויקטים חדשים על הנייר: Galim and the related search;
     - פרויקטים חדשים במבצע: Yad2's deals hub;
     - פרויקטים חדשים עד 2 מיליון: the related search;
     - דירות חדשות למכירה מקבלן: nadlanmaster.
   - The first H1 I proposed was invented, and Ben rejected it.
2. **Answer paragraph, printed from live data with a "נבדק ב" date:**
   - how many projects are on the market, split by stage: לאכלוס מיידי · אכלוס קרוב · בבנייה · על הנייר ופריסייל;
   - how many show a "החל מ" price;
   - that next to each price we show what flats really sold for nearby.
3. **Buttons and search:** the existing search bar, plus stage chips with counts. **"לאכלוס מיידי (N)" comes first and is visually strongest.** Then budget, city, rooms, במבצע, קרוב אליי, and התראה.
4. **NEW: the immediate-occupancy finder**, the tool. Section 4 has the details.
5. The full market list for every stage. This is the existing table, raised above the catalog, with its chips kept in sync with the finder.
6. **City sections.** Each has an anchor and no new URL.
   - Tel Aviv comes first. It takes in everything of value from the retired page: its 27 projects, neighbourhoods, prices by room count, and the 3-project shortlist method.
   - Then, in order of search volume: Jerusalem, Petah Tikva, Rishon LeZion, Haifa, Ashdod, Netanya, Ramat Gan, Herzliya (linking to /herzliya-projects/), Beer Sheva, and so on.
   - Every city section is unique: counts by stage, price per m² from the Tax Authority, 3-5 projects, and a link to its filtered list. Never a template with the city name swapped (Lily Ray, Badush).
7. **על הנייר ופריסייל:** how much it saves and what the risk is. It links to the guide for the "what is it" side.
8. **Deals in shekels:** every 20/80 or furniture-gift offer gets a shekel value against a normal schedule. It links to /developer-deals/ for the explanation.
9. **Kept as they are:** timeline, payment, the 7 calculators, the checks, types, numbers, guides.
10. **The 975 urban-renewal compounds**, relabelled "מתחמי פינוי בינוי ותמ״א 38 בתכנון", moved below the buying list, and linked to /urban-renewal/.
11. **FAQ:** the hub's ~20 questions, plus the retired page's 11 without duplicates. The questions Google already quotes keep their exact wording.

## 4. The immediate-occupancy finder
**Heading:** "דירות לאכלוס מיידי ואכלוס קרוב: N פרויקטים מוכנים לכניסה", with a sub-line "נבדק ב-<date>".

**Controls:**
- time bands: מוכנה עכשיו · עד 6 חודשים · עד שנה · (על הנייר, linked to its section);
- region and city chips with counts; budget ceiling; rooms; developer; במבצע;
- view: רשימה / מפה.

**Card fields:** only known facts are printed; unknown fields are omitted.
- project · developer · neighbourhood and city · band badge plus the delivery month;
- rooms · "החל מ" price as published, with source and date;
- **next to the price:** the Tax Authority median for flats of the same rooms in the neighbourhood or city, with its period;
- **the deal in shekels:** what the 20/80 or the gift is worth against a normal schedule, with the method one click away;
- **the label check:** if "אכלוס מיידי" is marketed while the stated date is later, the card says so plainly, with both facts;
- "נבדק ב" plus the source link · buttons for details, compare (up to 3) and follow.

**Map:**
- the existing Mapbox map gets an "אכלוס מיידי" layer;
- pin colour by band, from the site's planning palette;
- the neighbourhood price layer stays underneath;
- pins sit at the project address. If no address is published, the pin goes at the neighbourhood with the label "מיקום לפי שכונה". Never a guessed spot.

**Calculator, "דירה גמורה או על הנייר: כמה זה שווה לכם בשקלים":**
- it is fed by the card: the project's delivery month, the local rent for that room count (editable), and the construction-cost index the buyer avoids (annual rate and source, editable);
- the payment schedule is editable (normal, 20/80, 10/90);
- the result is the shekel gap between entering now and waiting, line by line: rent, indexation, mortgage timing, delay risk under the sale law.

**Follow:**
- an alert when a followed project moves to near or immediate occupancy, or its date slips;
- it reuses the consent-based alert path (HAD-684); phone or email, and only with consent.

**Checklist, "דירה גמורה: מה בודקים לפני שחותמים":**
- טופס 4 / תעודת גמר (shown only where a public source exists);
- בדק בית; רישום הבית המשותף;
- the warranty clock (the existing tool);
- parking and storage; the specification against what was built.

## 5. Data (the part that makes it real)
- **The source:** `data/projects-market.json`, read 25.10.2026. It has 85 rows in immediate or near occupancy (67 + 18), across 30 cities, 51 of them priced, and 0 coordinates.
- **Before launch, every row is checked by hand**, against the developer's own page first and the portal second. Each row records:
  - date checked, source URL, address, delivery month, price from, rooms;
  - deal text and its expiry;
  - whether the label agrees with the date.
- **Rows that cannot be confirmed are left out.**
- **The address becomes coordinates**, with the method recorded. A row with no address gets the neighbourhood with a label.
- **Tax Authority data already on the site:** the price per m² for each city and neighbourhood, and the median for each room count. Each figure is printed with its period.
- **Rent by city and room count:** the source must be named before the calculator ships. If no source can be named, the user types the rent and we suggest no default.

## 6. Search signals
- **Title and meta are printed from live counts.** Example title: "פרויקטים חדשים ודירות מקבלן: N לאכלוס מיידי, מחירים ועל הנייר | נדלן". The final wording is checked against kw_guard.
- **Schema:**
  - ItemList for the ready projects;
  - FAQPage;
  - Dataset for the market table, with dateModified;
  - BreadcrumbList.
- **Internal links:** the guides, project pages and price pages link with varied exact and synonym anchors, added a few at a time.
- **Keyword guard:** update the owners in `docs/seo/protected-keywords.json` (אכלוס מיידי, דירות לאכלוס מיידי, דירות מוכנות מקבלן → /projects/).
- **Watch:** Search Console page-level at 2 weeks and at 1 month (`tools/seo/cluster_map.py`). Every change goes in the Notion change log.

## 7. Proof (what we may claim, from `world/immediate-occupancy-tools.md`)
**Safe:** the first finder we could find that does all of the following:
- values each developer deal in shekels;
- prices the cost of waiting from each project's own delivery month, local rent and the construction-cost index;
- alerts when a project moves to occupancy;
- checks the immediate label against the stated date.

Also safe: the first Israeli finder with time bands, a structured delivery month and a check date on every row, in four languages.

**Not safe:** first ready filter (NewHomeSource, Yad2, SeLoger), first delivery tracker (FAM Dubai), first ready-versus-paper calculator (stand-alone tools exist).

**Recheck before any public claim:** the sites that blocked the research tools.

## 8. Order of work (each step reported to Ben, logged, reversible)
1. **Ben approves** this spec and the visual design. The design comes first, by house law.
2. **Data:** check the 85 rows by hand, with sources and dates.
3. **Build:** the finder, the calculator, the map layer and the new order. Local tests, the language DNA check and the content-first check.
4. **Release** through the token-bridge runner, with source audit before and after. Press it live on phone and desktop.
5. **Merge the retired page's Tel Aviv content** and the FAQ.
6. **Proof table** against the world.
7. **Watch** at 2 weeks and 1 month.
