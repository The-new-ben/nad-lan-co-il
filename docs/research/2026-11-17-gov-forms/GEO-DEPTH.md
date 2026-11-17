# /forms/ : the layers built for AI engines (GEO / AIO) and for Google (17.11.2026)

Ben asked for GEO and AIO on top of SEO, built "deep, and prove it". Below, each layer is listed with what was built, why AI engines use it, and how it was checked.

| # | Layer | What was built | Why (the mechanism) | Check |
|---|---|---|---|---|
| 1 | Answer first | The page opens with a 60-word paragraph that answers the question. Every card opens with "what it is" in 2-3 sentences, before any details. | AI answers lift whole passages that work on their own. Google AI Overviews summarise top pages. | Read in page.html and in the cards. |
| 2 | Numbers with a source | A table "המספרים שחשוב לדעת": 16 statutory deadlines, thresholds and majorities (30 days, 45 working days, 108,500 ₪, 7%, 40%, 2/3 and 3/5, and more). Each has its section and an official link. | The Princeton GEO study (KDD 2024) measured citing sources at +40% visibility and statistics at +37%. Tables are lifted as they are. | test_h768_forms.php: one table row per fact. |
| 3 | Sources per item | 328 items, each with its own sources: law text, gov.il, Knesset, State Comptroller. Weak or partial sources carry a visible "אומת חלקית" label. | Engines prefer sources they can verify. A false number breaks trust. | Build script: an item with no source is dropped (0 dropped). |
| 4 | Headings in the searchers' words | Stage and section names come from the manual Google search: "טפסים לתחילת עבודות", "תעודת גמר", "שלבי היתר בנייה", "טפסי מיסוי מקרקעין". The questions copy "People also ask". | The query fan-out of AI Mode retrieves by the related phrasings. | KEYWORDS.md (two rounds, screenshots). |
| 5 | Deep schema | CollectionPage (about with 10 entities linked by sameAs to Hebrew Wikipedia, publisher, citation of up to 60 official sources, speakable), ItemList of DigitalDocument (each official form: contentUrl, publisher GovernmentOrganization, isBasedOn the official page), HowTo with the 11 stages, Dataset with a JSON download, and FAQPage. | Non-Google engines read structure. Entity linking places the page in the knowledge graph. | The test checks HowTo, Dataset, citation, about, FAQPage. |
| 6 | Machine-readable data | GET /wp-json/nadlan/v1/forms returns the whole map as JSON (stages, facts, items, sources), linked from the page head (rel="alternate" type="application/json"). | AI agents read JSON without rendering anything. | After release: HTTP 200 and the item count. |
| 7 | llms.txt | A "Forms and building approvals" section with a description, the count and the JSON link. | A reading list in the llms.txt convention that assistants read. | After release: the line appears in /llms.txt. |
| 8 | The official files | 145 files, byte-identical to gov.il, under the original file names. Each has a card with a clean name, which replaces the broken gov.il title (for example "מ ד ב ק ה" on 7002). | The "link inversion" effect (GSC help, Glenn Gabe 2024, Petrovic 2018), and a clean heading that beats the bare file. | media.json: 145/145 byte_check OK. |
| 9 | Access for crawlers | robots.txt allows everyone (GPTBot, ClaudeBot, PerplexityBot, Google-Extended are not blocked). The page is in the sitemap by default. | A blocked crawler means no citation. | robots.txt read 17.11.2026. |
| 10 | Freshness | dateModified, "עודכן / נבדק 17.11.2026" on the page and on every item. The JSON carries an updated date. | Engines prefer content with a date, and so does Ben's own llms.txt note ("quote the date with the number"). | On the page. |
| 11 | Internal links to our tools | Each stage links to our tools: registered-contractor check, construction-input-index calculator, delay-compensation calculator, inspection-period clock, purchase tax, arnona, Tabu extract. | Engines cite a hub with tools. Users get an action, not only reading. | All 17 links answered 200 on 17.11.2026. |
| 12 | Baseline for measurement | What AI shows today (manual Google 17.11): "טופס 7000" AI overview cites gov.il, Kol Zchut and easydo; "טופס 7002" cites gov.il, 2sign and hmercaz; "ביטול הערת אזהרה" cites gov.il. nad-lan is not cited. | Measured again in 2-4 weeks: does nad-lan appear among the citations? | Screenshots in screens/. |

## Left out on purpose
- Prices and fees with no official amount. Where the source does not give an amount, the item says so and points to the regulations.
- Invented "ranking" claims, and keyword stuffing (GEO: -10%).
- A request to Google to index the page (owner law). Only the sitemap is resubmitted.
