# Competitor teardown: environmental hazards near a home

Read on 3.11.2026.

**How the Hebrew pages were read.**
- Raw HTML was fetched with curl, using a desktop Chrome user agent and Hebrew Accept-Language.
- The main content was sliced from the H1 or first H2 to the end of the article or FAQ.
- Words were counted by a script: Hebrew, Latin and number tokens. The download time of each page is recorded below.
- The script also counted tables, iframes and maps, FAQ schema, outbound links in the main content, and ₪ or ש"ח price patterns.

**Accuracy limits.**
- Net words are script counts of the slice, not estimates. Where the slice still includes navigation or teaser blocks, this is stated.
- World references were read with WebFetch or web search where curl failed. Those times are approximate, to the minute.

The 5 Hebrew pages are the most relevant pages that appeared in `serp.md`.

---

## Hebrew pages (top 5)

### 1. spectrum.fit, "מפת אנטנות סלולריות לפי כתובת"

- **URL:** https://www.spectrum.fit/מפת-אנטנות-סלולריות/
- **Read:** 19:54:45 UTC, HTTP 200.
- **Dates:** schema datePublished 2.8.2026, dateModified 5.9.2026.
- **Who:** a seller of cellular signal amplifiers. The page ends with an amplifier upsell and a "prices" link in the menu.

| Measure | Count or finding |
|---|---|
| Net words | **1,231** (slice includes about 10 words of top menu) |
| Tools | **1 own tool.** Antenna locator: city, then street and number (optional), plus "my location". Returns operator, generation (3/4/5G), distance and direction, site type, radiation-permit data with a PDF link, and a network recommendation. |
| Data tables | **1.** 24 largest cities, with antennas, of which 5G, and the 5G share. Example rows: Tel Aviv 895 / 359 / 40%; Jerusalem 719 / 310 / 43%; Haifa 341 / 171 / 50%. |
| Maps | **1 own interactive map** (plugin iframe) |
| Cited sources | Ministry of Environmental Protection database (monthly update) and Ministry of Communications, named. **0 outbound links** in the main content. |
| Prices | 0 on the page |
| Professionals directory | None |
| Languages | Hebrew only. The menu links a separate Russian amplifier page, not a translation. No hreflang. |
| FAQ | **11 questions, with FAQPage schema (11 Question objects).** They include "האם מסוכן לגור ליד אנטנה סלולרית?" and "מה המרחק הבטוח מאנטנה סלולרית?". |
| Israeli specifics | Rich. 8,768 sites as of August 2026 (8,368 active, 400 under construction). PHI 3,102, Pelephone 2,899, Cellcom 2,767. About 3,739 sites on 5G. Site types: ground mast 3,481, indoor small cell 1,614, rooftop mast 1,570, "sting" antenna 986, wireless access point 889, slanted antenna 226. iPhone Field Test code, dBm thresholds. |
| What is missing | Every hazard except cellular antennas: broadcast transmitters, power lines, transformer rooms, substations, industry, air, noise, fuel stations. No legal threshold in numbers; it only says "a few percent of the threshold". No measurement price, no certified testers, no home-buying angle (what to ask a seller or developer, value). Commercial bias, since the page sells amplifiers. |

### 2. cellular.wmh.co.il, Watch My Health, "אנטנות סלולריות ליד הבית"

- **URL:** https://cellular.wmh.co.il/
- **Read:** 19:54:46 UTC, HTTP 200.

| Measure | Count or finding |
|---|---|
| Net words | **40 in the static HTML.** The page is a JavaScript single-page app (one `/assets/index-….js` bundle). Its content cannot be read without rendering, so it is **partly blocked to our reading method**. |
| Tools | 1, per its own text and SERP snippet: map by address, filter by distance and infrastructure, "directions to the home". **Not verified working.** |
| Data tables | Not visible in static HTML |
| Maps | 1, claimed, not verified |
| Cited sources | States it is based on the Ministry of Environmental Protection's active-antenna database. No links. |
| Prices | 0 |
| Professionals directory | None visible |
| Languages | Hebrew |
| FAQ | None visible |
| Israeli specifics | Names Pelephone, Cellcom and PHI (Partner and HOT). States that "the map shows infrastructure, not reception measurement at home". |
| What is missing | Everything beyond antennas. Its content is invisible to crawlers that do not run JS, yet it ranks O4 for "בדיקת אנטנה סלולרית". |

### 3. afikil.co.il (Afik College news), "בדיקת אנטנות סלולריות ליד בית: מה לבדוק?"

- **URL:** https://afikil.co.il/real-estates/בדיקת-אנטנות-סלולריות-ליד-בית-מה-לבדוק/
- **Read:** 19:54:47 UTC, HTTP 200.
- **Dates:** published 7.5.2026, modified 28.6.2026.

| Measure | Count or finding |
|---|---|
| Net words | **1,244** in the slice. The slice includes several inline "related article" teaser blocks, so the article prose itself is lower. |
| Tools | 0. It has 1 audio player ("listen to the article") and 1 embedded YouTube video. |
| Data tables | 0 |
| Maps | 0 |
| Cited sources | **0 outbound links.** It says "the antenna map of the Ministry of Communications". That is a mix-up: antenna locations are published by the Ministry of Environmental Protection, while Communications publishes coverage. |
| Prices | 0 |
| Professionals directory | None. It has a lead form ("a professional adviser will call you back"). |
| Languages | Hebrew |
| FAQ | None |
| Israeli specifics | Weak. It is generic (WHO) and has no Israeli numbers or law. |
| What is missing | Data, sources, maps, every other hazard. **But it is the only page in the SERPs framed for real estate.** It has the sections "השפעת האנטנות על ערך הנדל"ן" and "ההשפעה הפסיכולוגית של חשש מאנטנות". It ranks O7 for "בדיקת אנטנה סלולרית". |

### 4. norad4u.co.il, "ללא קרינה בשבילך", "מפת אנטנות סלולריות ומשדרים אחרים"

- **URL:** https://www.norad4u.co.il/knowledge-h/cellphone-antennas/cellphone-antenna-maps/
- **Read:** 19:54:48 UTC, HTTP 200.
- **Dates:** published 10.11.2019, modified 30.9.2025.

| Measure | Count or finding |
|---|---|
| Net words | **791** (article scope) |
| Tools | 0 own. It explains how to switch on the antenna layer in GovMap and how to use Google Earth and Street View to judge line of sight to an antenna. |
| Data tables | 0 |
| Maps | **1 embedded** Google My Maps iframe, plus **5 links to govmap.gov.il** |
| Cited sources | Linked: govmap.gov.il ×5, sviva.gov.il ×1, idanplus.tv ×2 (TV transmitter sites) |
| Prices | 0 on the page. The site sells a "fast home radiation meter", which the page recommends. |
| Professionals directory | None |
| Languages | Hebrew |
| FAQ | None |
| Israeli specifics | GovMap layer instructions. A section on **radio and TV transmitter maps**, the only Hebrew page here covering broadcast transmitters. |
| What is missing | Balance. It claims the official measurements in the map "have no real practical value", which is an activist and seller stance. No other hazards, no data, no prices. |

### 5. midrag.co.il, Tip 5238, "בדיקת קרינה סלולרית"

- **URL:** https://www.midrag.co.il/Content/Tip/5238
- **Read:** 19:54:49 UTC, HTTP 200.
- **Dates:** published 26.10.2022, modified 15.5.2025.

| Measure | Count or finding |
|---|---|
| Net words | **635** in the article slice (857 including the block of city links) |
| Tools | 0. It has a search input for the directory. |
| Data tables | 0 |
| Maps | 0. It has 5 YouTube iframes. |
| Cited sources | 0 outbound links |
| Prices | **Yes.** A standard apartment costs 500 to 800 ₪ including VAT, and the price rises with size. An office or building costs about 1,200 ₪. A cellular and an electrical test are usually done in the same visit. |
| Professionals directory | **Yes.** The section "בודקי קרינה מוסמכים במידרג", with reviews, plus city pages (Tel Aviv, Jerusalem, Ramat Gan, Petah Tikva, Rishon LeZion, Holon, Haifa, Givatayim, Herzliya and more). The individual tester cards are not in the static HTML, so they were not counted. |
| Languages | Hebrew |
| FAQ | **4 questions, with FAQPage schema (4 Question objects)** |
| Israeli specifics | "Only a certified radiation tester" may test. Filed under "טיפים נוספים בקונים דירה" (home-buying tips). |
| What is missing | No map, no address check, no official thresholds, no hazards beyond cellular and electrical. Thin prose. |

### Also read (useful but not in the top 5)

**tnuda.org.il, "אנטנות סלולריות"**
- URL: https://www.tnuda.org.il/אנטנות-סלולריות
- Read 19:54:50 UTC. Published 31.1.2016, modified 2.9.2018. National information centre on non-ionizing radiation.
- **4,193 net words, 3 tables**, no map or tool, no FAQ schema; it has an "I have a question" form.
- It has the **Israeli thresholds in numbers**:
  - in long-stay areas (homes, offices) exposure from transmitters must not exceed **10% of the ICNIRP level**;
  - in short-stay areas (pavements, roads) it must not exceed **30%**;
  - permits are valid from 1 to 25 years under the Non-Ionizing Radiation Regulations of 2009.
- The site's menu offers Hebrew, English and Arabic.
- The content is 7 to 8 years old.

**tiber.co.il/Home/Antenna**
- Read 19:54:51 UTC.
- 1,242 words, an address tool, **14-question FAQ schema**, GovMap. Intent: reception and choosing a carrier, not health.

**kamazeole.co.il/cellular-reception-checker**
- Read 19:54:52 UTC.
- 692 words. An address tool that counts active sites per network in a radius and shows the nearest site and generations. Source: the ministry dataset on data.gov.il.
- It has a privacy line: the address is used only for geocoding through GovMap or OpenStreetMap and is not stored.

**bedikat-krina.co.il, "בדיקת אנטנה סלולרית"**
- Read 19:54:51 UTC. Dated 17.3.2025.
- 397 words, a service page, no prices.

**ynet, "אתר חדש ימצא לכם מפגעים ליד הבית"**
- URL: https://www.ynet.co.il/articles/0,7340,L-4345026,00.html
- Read 19:54:53 UTC. Publication date not captured.
- About 1,000 words. It describes "סביבתי", a GIS site by Adam Teva V'Din and Tel Aviv University.
- Its layers were cellular antennas, air monitoring, factory emission standards, quarries and threats to open space. Contaminated land, pirate waste sites and pesticide spraying were left out for lack of data.
- **This is proof that the multi-hazard idea existed in Israel, but it is not what ranks today.**

---

## World references

| Reference | URL | Read | What it does | Counts or notes |
|---|---|---|---|---|
| **US EPA EJScreen** | https://www.epa.gov/ejscreen | 19:55:24 UTC | **HTTP 404, removed.** Per search results, EPA pulled public access on 5.2.2025. | Status checked by search at about 19:57 UTC. Sources: [Wikipedia](https://en.wikipedia.org/wiki/EJScreen), [EDGI](https://envirodatagov.org/?p=11456), [Waste Dive](https://www.wastedive.com/news/a-year-after-ejscreen-shut-down-researchers-envision-better-tools/818552/) |
| **EJScreen reconstruction (PEDP)** | https://screening-tools.com/epa-ejscreen | about 20:00 UTC, WebFetch | "Initial reconstruction" of EPA EJScreen v2.3, by Public Environmental Data Partners. Today it looks up indicators and index percentiles **by block group**; "more functionality" is promised. | Landing prose about 75 words. Indicators, languages and cost are not stated on the landing page. Per search, Social Explorer and others also rebuilt it, and a lawsuit over the removal was dismissed on 13.3.2026 ([Harvard EELP tracker](https://eelp.law.harvard.edu/?p=8168)). |
| **UK, Groundsure** | https://www.groundsure.com/ | about 19:57 UTC, WebFetch (curl got 867 KB of script-heavy HTML with no readable text) | Paid address reports: **Avista** ("our most comprehensive environmental, mining and climate risk report"), **Insight** (Enviro, Geo and Map Insight), Geology & Projects, Review (commercial). A **free "Groundsure Insights"** tier with open data, OS mapping, drawing tools and risk alerts. ClimateIndex™ risk model. More than 1.6 million historical OS maps digitised. | **Prices not shown.** The homepage names no specific hazards (flood, radon, power lines, masts). Some menu text is placeholder. |
| **UK, Ofcom** | not read | – | – | Not fetched (budget); no claim made |
| **Australia, ARPANSA** | https://www.arpansa.gov.au/understanding-radiation/radiation-sources/more-radiation-sources/mobile-phone-base-stations | 19:55 UTC (curl) and about 19:57 UTC (WebFetch) | **Blocked: timed out twice** | – |
| **Australia, RFNSA** | https://www.rfnsa.com.au/ | 19:54:58 UTC, HTTP 200 | Search mobile base stations by keyword, **near address**, or postcode. Each site page has an **exact-location map, a compliance certificate, a site EME (exposure) report**, carrier contacts (emergency, access, general), and **community-consultation details** for new sites and upgrades. **Email alerts by postcode** for changes and new proposals. Markers: P = proposed, C = in consultation; active and proposed technologies are marked separately. It links the **AMTA RF Assessors Supplier List**, a professionals directory. Run by AMTA for the Mobile Carriers Forum. | About 703 words of static help text. It is the closest world model to what Israel lacks: a per-site exposure report plus subscriptions plus a list of assessors. |
| **Canada, ISED** | https://ised-isde.canada.ca/site/spectrum-management-system/ | about 19:57 UTC, search only, not read in full | Spectrum Management System: search of radio authorizations and a downloadable site-data file. Tower siting follows the public-consultation circular CPC-2-0-03. A third-party ArcGIS mirror of the site data is updated twice a year. **An official public map of antenna sites was not confirmed.** | Sources: [ISED SMS](https://ised-isde.canada.ca/site/spectrum-management-system/), [ArcGIS mirror](https://services.arcgis.com/wjcPoefzjpzCgffS/ArcGIS/rest/services/Spectrum_Licences_Site_Data/FeatureServer) |
| **Israel, ministry ArcGIS dashboard "דשבורד אנטנות סלולריות"** | https://www.arcgis.com/apps/dashboards/361fb3cf9857422b8bab4a908fb2ae2b (metadata read from the item JSON) | about 20:00 UTC, WebFetch | Public dashboard, owner account "yigalm", built by Systematics on the ministry's open dataset data.gov.il/dataset/antennaactive. Created 8.11.2018, modified 22.6.2026. | Licence field: "לצרכי הדגמה בלבד" (demonstration only). It is cited in 3 AI Overviews. |
| **Israel, GovMap environment layer** | https://govmap.gov.il/sviva | not read (JS app) | Cited by the AI Overview as "the official antenna map" | `govmap` is searched 90,500 times a month |
| **Israel, Ministry of Communications coverage per address** | https://www.gov.il/he/pages/10042024_1 | 19:55:25 UTC | **Blocked (HTTP 403)** | Cited in the AI Overview for "מפת אנטנות סלולריות" |
| **Israel, air.sviva.gov.il** | https://air.sviva.gov.il/ | not read | Live monitoring map and AQI, cited in the AI Overview for "זיהום אוויר" | – |

---

## Scoring

The same rubric is used for every page: 12 criteria, each scored 0, 1 or 2, so the maximum is 24.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Net words | under 500 | 500–1,500 | over 1,500 |
| Address tool | none | links or embeds others' tools | own working tool |
| Data tables | none | 1 | 2 or more |
| Maps | none | embedded or linked | own interactive |
| Cited sources | none | named, not linked | linked official sources |
| Prices | none | one figure | ranges by case |
| Professionals directory | none | – | yes |
| Languages | 1 | 2 | 3 or more |
| FAQ | none | under 5 questions | 5 or more with schema |
| Hazard breadth | 1 hazard | 2–3 | 4 or more |
| Israeli specifics | generic | some | rich numbers or law |
| Real-estate framing | none | a mention | central |

| Page | Words | Tool | Tables | Maps | Sources | Prices | Pros | Langs | FAQ | Hazards | IL | RE | **Total /24** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| spectrum.fit | 1 | 2 | 1 | 2 | 1 | 0 | 0 | 0 | 2 | 0 | 2 | 0 | **11** |
| midrag.co.il | 1 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 1 | 1 | 1 | 1 | **9** |
| tnuda.org.il (also read) | 2 | 0 | 2 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | **8** |
| norad4u.co.il | 1 | 1 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | **7** |
| cellular.wmh.co.il | 0 | 2* | 0 | 2* | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | **6*** |
| afikil.co.il | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | **3** |
| RFNSA, Australia (world reference) | 1 | 2 | 0 | 2 | 2 | 0 | 2 | 0 | 0 | 0 | – | 0 | **9 of 22** (Israeli column not applicable) |

\* Claimed by the page; not verified, because the content is JavaScript only.

**Strongest Hebrew competitor: spectrum.fit (11 of 24).** It has its own address tool, a 24-city table, an 11-question FAQ with schema, fresh dated numbers, and it is cited in all 3 antenna AI Overviews. Its weak points are a single hazard, no prices or professionals, no legal thresholds in numbers, no home-buying angle, and an amplifier-seller bias.

---

## The gap we can own

These are facts from the reads above, not page copy.

1. **One address, every hazard.** No ranking Hebrew page covers more than 1 to 2 hazard types. Nobody puts cellular antennas, broadcast transmitters (only norad4u touches them), high-voltage lines, transformer rooms and substations, industry and emissions, air quality by city, aircraft noise and fuel stations around one address. The multi-hazard idea existed ("סביבתי", ynet) but is not what ranks today.
2. **The home-buyer's decision.** The only real-estate-framed page (afikil) scores 3 of 24. Its value section has no data and no sources. Nobody explains what to ask the seller or developer, what to check before signing, or how a hazard relates to price.
3. **Israeli thresholds in plain numbers.** The ministry rule (10% of ICNIRP for long stays, 30% for short stays, permits of 1 to 25 years) sits only on a 2016 to 2018 page (tnuda). spectrum.fit only says "a few percent of the threshold".
4. **Air pollution by city as a real table.** "זיהום אוויר בישראל לפי ערים" (1,000 a month) has **no AI Overview** and no ranking page with an actual city table. Google shows old news items, council pages and a PDF.
5. **Measurement prices plus certified testers, tied to the map.** Only midrag has prices (500 to 800 ₪ for an apartment, about 1,200 ₪ for a building) and a directory. No page connects "there is an antenna or transformer near your address" to "here is what a certified test costs and who does it". The CPCs ($19.16, $9.56, $8.18) show the money is in exactly that handoff.
6. **The RFNSA model, missing in Israel.** There is no per-site page in Israel that combines the exposure report, permit, distance and direction with a "notify me" subscription for new antennas near an address. Australia has it; Israel has a dashboard the ministry labels "demonstration only".
7. **Languages.** Every Hebrew competitor is Hebrew-only; only tnuda's site menu offers English and Arabic. Nad-lan already runs language pages, and new immigrants and foreign buyers have no source in their own language.
8. **Winning the AI Overview citation.** The AI cites dated, numbered facts plus an FAQ, as it does with spectrum.fit's "8,768, August 2026". To be cited, the page needs counts, thresholds, dates and named sources in clean text, plus FAQ schema. It must not hide them in a JavaScript-only app, which is the weakness of cellular.wmh.co.il.
