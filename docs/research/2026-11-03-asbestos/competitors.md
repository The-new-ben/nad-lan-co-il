# Competitor pages - asbestos (Israel + world references)

Read 3.11.2026, 17:40-18:20 UTC, in a real browser (Claude desktop browser pane), full rendered DOM. gov.il blocks scripted fetches (HTTP 403), so every page was read the same way for fairness.

**Method (same for every page).** Word count = words in the main content container (`article` / `main` / the element with the most paragraph text), with nav, header, footer, aside, share widgets and reference lists removed; Hebrew and Latin words and numbers counted as tokens. H2 list = every `h2` inside that container. Tools = interactive inputs that compute or look something up (contact forms are reported separately and do not count as tools). Data tables = `table` elements with data. Maps = embedded data maps (an office-location Google Map does not count). Cited sources = outbound links or footnotes to sources inside the content. Counts are rounded by nature; treat +/-10% as noise.

**Which Hebrew pages and why.** The top organic results across the 6 Hebrew SERPs (serp.md), skipping a Facebook post and thin contractor home pages: he.wikipedia (rank 1 on `אסבסט`), the Israel Cancer Association (rank 2), the MoEP asbestos site (rank 3 on `אסבסט`, rank 1 on `פינוי אסבסט` and `אסבסט בבניין`), the Tel Aviv municipality (ranks 4-5 on two SERPs), plus the three commercial pages Google's AI Overviews cite most (volta.solar, asbest.co.il price page, elm.co.il guide).

---

## 1. he.wikipedia - אזבסט
URL: https://he.wikipedia.org/wiki/%D7%90%D7%96%D7%91%D7%A1%D7%98
- Words: **~3,170** (includes infobox and table text).
- H2 (12): סוגי אזבסט · סיבי אזבסט ואבק אזבסט · שימושים · מחלות הנגזרות מחשיפה לאזבסט · משפט וחוק · סילוק אזבסט · ביקורת על תקנות חרם האזבסט · תחליפים מודרניים לאזבסט בבנייה · ראו גם · לקריאה נוספת · קישורים חיצוניים · הערות שוליים. H3: 12 (white/brown/blue asbestos, historical/current uses, asbestos as pollutant, diseases...).
- Tools: none. Data tables: 4 (mineral/infobox tables). Maps: none. Images: 17.
- Cited sources: 22 footnotes; 37 external domains linked.
- Languages: the article exists in 79 language editions.
- Israeli specifics: almost none ("ישראל" appears 2 times; no Western Galilee, no Nahariya factory, no Israeli numbers, no licensing, no prices).
- Missing: everything practical for an Israeli owner or buyer: what to do, who to call, licences, registry, permits, costs, grants, Israeli data, maps.

## 2. Israel Cancer Association - אסבסט והסיכון לסרטן
URL: https://www.cancer.org.il/articles/8255/ (dated 22.12.2024; professional advice: Dr. Eli Stern)
- Words: **~1,490**.
- H2 (8): סוגי אסבסט · האם אסבסט גורם סרטן? · סוגי הסרטן שנמצאו קשורים בחשיפה לאסבסט · הקשר בין עישון לסיכון תחלואה בסרטן מחשיפה לאסבסט · דרכי החשיפה · חקיקה בישראל · מצב האסבסט בישראל · דרכים להפחתת הסיכון. H3 include "המצב בגליל המערבי והמבצע לתיקון" and a short frontline-war paragraph.
- Tools: none (a site chat widget only). Data tables: 0. Maps: none. Images: 0.
- Cited sources: 2 outbound links, both gov.il; IARC/CDC named in text without links.
- Languages: Hebrew only.
- Israeli specifics: medium (law, Western Galilee stages, ~20 friable buildings, frontline mapping intent). Strongest health section in Hebrew (symptom list, smoking interaction, see a doctor).
- Missing: prices, grants, who to call, registry, how to check a home or a building, roofs, buyer angle, maps, numbers with dates (no incidence data for Israel).

## 3. Ministry of Environmental Protection (MoEP) asbestos site - gov.il
Hub: https://www.gov.il/he/departments/topics/asbestos (plus the linked pages below). Treated as one multi-page competitor because Google ranks the hub and the AI Overviews cite its sub-pages.
- Words: hub ~300 words of links and news; content lives in sub-pages: FAQ **~1,660** (https://www.gov.il/he/pages/asbestos_faq, updated 09.04.2025); public guide, 4 tabs (updated 02.09.2025); what is asbestos (updated 19.03.2025); law page (updated 11.09.2024); Western Galilee page, 3 tabs (updated 19.03.2025); friable page; implementation-report news (02.12.2025). Estimated total across these pages: roughly 5,000-6,000 words (not counted page by page).
- H2-equivalents: the hub is a link list (guides, legal info, publications, policy, FOI, registry, landfills, labs, services, news). Content pages use tabs and accordions rather than H2s.
- Tools: **yes** - searchable registry of licence holders (filter by licence type; 453 results on 3.11.2026), list of landfill sites, list of laboratories, two online services (licence application; work notification / permit / final report). The guide has a 9-row "who to contact for which work" table.
- Data tables: the who-to-contact table; registry results (cards). No price tables.
- Maps: **none published on the site** (the Western Galilee layer lives only on data.gov.il / ArcGIS, see map-data.md; the 2025 report says a Gaza-envelope roof layer is "expected" on govmap).
- Cited sources: it is the primary source; links to Nevo for the law, PDFs, zip and docx project files, a Google Drive folder of air-sampling results.
- Languages: Hebrew, English, Arabic (hub has language switch; English guide pages exist, dated 21.09.2025).
- Israeli specifics: the most complete (law, licences, registry, landfills, Western Galilee, hotline *6911, grants as news items).
- Missing: one readable path for a homeowner or buyer; prices (MoEP says it is "not involved in market prices"); a map; the low-income help procedure was not published on the site in 2023 (Knesset report); grant information scattered across news items; no buyer / TAMA / pinui-binui guidance; no municipal rule summary.

## 4. Tel Aviv-Yafo municipality - אסבסט
URL: https://www.tel-aviv.gov.il/Residents/Environment/Pages/Asbestos.aspx (no date shown)
- Words: **~176**.
- H2: none in content; 2 bold sub-heads (survey in renovation licence request; dismantling / demolition).
- Tools: none. Tables: 0. Maps: none. Cited sources: 1 (link to the MoEP licence list).
- Languages: Hebrew page (site has other languages, not this content).
- Israeli specifics: high but local - survey mandatory before renovation in buildings built up to 31.12.2000; even under 50 m² needs a licensed contractor (stricter than the national exemption); city inspects public buildings only; hotline 106.
- Missing: almost everything beyond those rules.

## 5. volta.solar - פירוק אסבסט: כל המידע והשלבים לפינוי גג אסבסט (solar company content)
URL: https://volta.solar/knowledge-center/... (modified 24.08.2026)
- Words: **~1,340**.
- H2 (10): מה זה אסבסט? · מהו גג אסבסט? · פירוק אסבסט: האם זה מסוכן? · פינוי ופירוק אסבסט: מי, מתי ואיך? · כל השלבים בדרך לפינוי גג אסבסט והפיכתו לגג סולארי · האם אפשר לפנות אסבסט לבד? · אמצעי הזהירות בפירוק אסבסט · פינוי גג אסבסט: כמה זה עולה? · לסיכום · שאלות ותשובות.
- Tools: none (a 14-field lead form). Tables: 0. Maps: none. Images: 7.
- Cited sources: 0 outbound links.
- Price info: one figure in text ("~650 ₪ per m² for roofs under 50 m²", undated, unsourced).
- Israeli specifics: low-medium (mentions the 2011 law, MoEP; claims "obligation to remove existing asbestos within 10 years", which the AI Overview repeats - for asbestos-cement this is not what the law says; the 10-year duty was for friable asbestos).
- Missing: sources, dates, the registry, grants, health detail, maps, buyer angle. Cited by Google's AI Overview on 5 of 6 Hebrew queries anyway.

## 6. asbest.co.il - פינוי אסבסט מחיר 2026 – מחירון מעודכן למ״ר + מחשבון (contractor)
URL: https://asbest.co.il/%D7%A4%D7%99%D7%A0%D7%95%D7%99-%D7%90%D7%A1%D7%91%D7%A1%D7%98-%D7%9E%D7%97%D7%99%D7%A8/ (published 24.07.2022, modified 22.10.2026)
- Words: **~1,650**.
- H2 (13): עלויות ניקוי והתקנה מראש · מחירון בסיסי לפינוי אסבסט 2026 · מחירון החלפת גג: איסכורית ופאנל מבודד · מחירון בדיקות וייעוץ · משך העבודה הכרוך בפינוי אסבסט · פינוי אסבסט כולל גם עלויות הטמנה · המיקום הגיאוגרפי משפיע על מחיר פינוי · מחירי בסיס לפי גודל השטח · טבלת מחירים מפורטת · גורמים המשפיעים על המחיר · מחשבון מחירי הסרת אסבסט · תהליך הסרת האסבסט · שאלות נפוצות.
- Tools: **a price calculator** (3 inputs). Data tables: **4 price tables**. Maps: only an office-location Google Map (not data).
- Cited sources: 1 outbound link (gov.il). Prices are the site's own, no source or method.
- Israeli specifics: medium (2026 prices, law mention).
- Weakness: the size table is internally inconsistent (up to 50 m² "300 ₪/m², minimum 15,000 ₪" vs 51-100 m² "60 ₪/m²"); no public benchmark; no grants; no registry. This is the page Google's price AI Overview quotes.

## 7. ELM - סקר אסבסט, פירוק ופינוי: המדריך המלא (environmental consultancy)
URL: https://www.elm.co.il/asbestos-survey-removal/ (modified 07.07.2026)
- Words: **~2,160**.
- H2 (9): אסבסט צמנט מול אסבסט פריך: ההבחנה שקובעת הכל · החוק למניעת מפגעי אסבסט ואבק מזיק, התשע"א-2011 · מתי חובה לבצע סקר אסבסט · מי מורשה לגעת באסבסט: בעלי הרישיון בשרשרת · תהליך קבלת אישור עבודת אסבסט, שלב אחר שלב · עלויות: סדרי גודל ומה משפיע עליהם · אכיפה ועונשין: מדרג שמגיע עד מאסר · אסבסט בקרקע: כשהמפגע אינו על הגג אלא מתחתיו · איך ELM מלווה פרויקטים עם אסבסט.
- Tools: none (contact form). Tables: 1. Maps: none. Cited sources: 0 outbound links.
- Israeli specifics: the best commercial legal summary (licence chain, permit steps, 2024 exemptions, survey in demolition / urban renewal, soil asbestos).
- Weakness: fines quoted as 50,000 / 400,000 ₪ (individual) - the law text on Nevo now shows 60,900 / 243,610 / 487,220 ₪; survey-before-demolition claim has no cited regulation; costs only as "tens to hundreds of ₪ per m²"; no grants, no data, no map.

---

## World reference pages

## 8. US EPA - Asbestos
URL: https://www.epa.gov/asbestos (last updated 08.10.2026)
- Words on the hub: **~180**; it is a hub of 27 internal links in 9 H2 blocks: EPA Bans Ongoing Uses of Asbestos · Learn About Asbestos · Protect Your Family · Building Owners and Managers · School Buildings · Asbestos Professionals · Key Information · Related Topics · EPA Asbestos News.
- Tools / directories: **State Asbestos Contacts, EPA Regional Contacts, Find Labs**, hire-a-professional guidance, renovation and demolition requirements, schools programme, vermiculite guidance. Tables / maps on the hub: none.
- Cited sources: internal (it is the regulator). Languages: English on the hub.
- Lesson for us: audience doors (family / building owners / schools / professionals) and a contacts directory are the core, not prose length.

## 9. UK HSE - Asbestos
URL: https://www.hse.gov.uk/asbestos/
- Words on the hub: **~140**; 9 H2 doors: Introduction to asbestos safety · Duty to manage asbestos in buildings · A worker's guide to asbestos safety · Asbestos essentials task sheets · Locations of asbestos and taking the right action · Licensable work with asbestos · Frequently asked questions · Publications · REACH exemption certificates. Email subscription box.
- Tools: task sheets per trade; "locations of asbestos" image-led guide (where it hides in a building and what to do). Tables / maps on hub: none.
- Lesson for us: the "where asbestos hides in a building + the right action" visual is the gold standard for identification intent; "duty to manage" maps to Israel's public-place duties (section 8).

## 10. Australia ASEA - Asbestos Safety and Eradication Agency
URL: https://www.asbestossafety.gov.au/
- Words on the homepage: **~430** (no H2s; card layout). Navigation exposes: understanding asbestos, identification/removal/disposal, **the dangers of asbestos cement roofs**, liabilities and insurance, extreme weather and disaster events, **National Asbestos Exposure Register**, finding asbestos in the home / workplace / environment, guidance for householders, landlords, trades, local government, surveys, **asbestos-cement water and sewer pipes**, facts and figures, National Strategic Plan 2024-30 with progress reports, import/export, **Find a local disposal facility** (by state).
- Tools: **Asbestos Product Guide** (image catalogue of products with years, uses and brand names), disposal-facility finder, exposure register. Languages: **translated factsheets** ("Think Twice About Asbestos").
- Lesson for us: a product guide with photos and years, a disposal finder, a disaster page (fire / storm / missile damage maps directly onto Israel's war hazards), and an exposure register idea.

---

## Scoring table (proof-of-superiority baseline)

Scale for the qualitative columns: 0 = none, 1 = mention, 2 = useful, 3 = complete and sourced. Numbers in brackets are the raw counts behind the score.

| Page | Words (main) | Tools | Data tables | Maps | Cited sources | Price info | Authority directory | Israeli specifics |
|---|---:|---|---|---|---|---|---|---|
| he.wikipedia אזבסט | ~3,170 | 0 | 2 (4 tables, minerals) | 0 | 3 (22 footnotes) | 0 | 0 | 1 |
| Israel Cancer Association | ~1,490 | 0 | 0 | 0 | 1 (2 links) | 0 | 0 | 2 |
| MoEP site (multi-page) | FAQ ~1,660; set ~5-6k est. | 3 (registry search, landfill and lab lists, online permit services) | 2 (who-to-contact table) | 0 | 3 (primary) | 0 | 2 (registry, landfills, labs; no unit-by-city lookup) | 3 |
| Tel Aviv municipality | ~176 | 0 | 0 | 0 | 1 (1 link) | 0 | 1 (hotline 106) | 2 (local only) |
| volta.solar guide | ~1,340 | 0 (lead form) | 0 | 0 | 0 | 1 (one figure, unsourced) | 0 | 1 |
| asbest.co.il price page | ~1,650 | 2 (price calculator) | 3 (4 price tables, unsourced) | 0 | 0 (1 link) | 2 (rich but inconsistent, own prices) | 0 | 1 |
| elm.co.il guide | ~2,160 | 0 | 1 (1 table) | 0 | 0 | 1 (orders of magnitude) | 1 (mentions registry) | 2 |
| US EPA hub | ~180 (hub) | 2 (state/regional contacts, find labs) | 0 | 0 | n/a (regulator) | 0 | 3 | 0 (US) |
| UK HSE hub | ~140 (hub) | 2 (task sheets, locations guide) | 0 | 0 | n/a (regulator) | 0 | 2 (licensing) | 0 (UK) |
| Australia ASEA | ~430 (home) | 3 (product guide, disposal finder, exposure register) | 0 | 0 | n/a (regulator) | 0 | 2 (disposal by state) | 0 (AU) |
| **nad-lan target (plan, not yet built)** | 5,000+ he / ~3,000 en | 4-5 (see brief.md) | 3 (dated, sourced) | 2-3 (Western Galilee layer + landfills + registry by district) | 3 (every number linked + dated) | 3 (public benchmark + labelled commercial ranges) | 3 (255 authorities -> 57 environmental units; MoEP districts; registry) | 3 |

**Fair reading.** No single Hebrew page combines the law, the registry, prices, grants, health, a map and the property-buyer angle. MoEP has the data but no reader path and no prices; the commercial pages have prices and calculators but no sources and visible errors; Wikipedia has depth but no Israel. No Israeli page embeds any map. The world regulators win on structure (audience doors, directories, product/location visuals, disposal finders, disaster guidance), not on word count - their hubs are under 500 words. Our "superiority" claim should therefore be measured on tools, sourced data tables, map, directory and Israeli specifics, with word count as a supporting figure only.
