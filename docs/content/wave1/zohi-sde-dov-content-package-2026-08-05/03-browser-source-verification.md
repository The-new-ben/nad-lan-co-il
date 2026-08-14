# ZOHI browser and source verification record

Research date: 5 August 2026  
Browser surface: the user's connected Google Chrome browser only  
Research market: Israel, with Tel Aviv-Yafo shown by Google from the connection's IP  
Scope: source verification and audit evidence only. No article, page, code, schema or media was changed.

## Why there is no separate `01-live-google-intent-ledger.md`

`cultural-intent-support.md` already contains the complete localized intent evidence needed for this package:

- the Chrome setup and location limitations;
- fourteen Google search URLs;
- thirty-two exact phrase records, eight each for English, French, Russian and Arabic;
- capture timestamps;
- culture-specific intent interpretation;
- project-first title and H1 recommendations.

Creating a second intent ledger would duplicate evidence and introduce a drift risk. `cultural-intent-support.md` is therefore the authoritative intent record for ZOHI. This file covers a different layer: the Hebrew live-page audit and factual source verification.

## Browser settings and evidence rules

- Google host: `google.co.il`
- Interface for factual source discovery: Hebrew
- Country parameter: `gl=il`
- Personalization parameter: `pws=0`
- Visible location signal: Tel Aviv-Yafo from the IP connection
- Direct-source rule: Google results were used to discover URLs, not to prove project claims.
- Chrome-only rule: a claim was accepted only when the target source was opened in the connected Chrome session and its relevant text was visible or programmatically exposed from that rendered tab.
- PDF rule: a PDF appearing in a Chrome PDF viewer counted as a successful load, but not as claim verification when the viewer exposed no readable document text.
- Conflict rule: later first-party product information controls current product wording; statutory material controls planning; dated media remains dated.

All times below use Israel time, UTC+3, unless stated otherwise.

## Direct verification matrix

| Source | Direct URL | Capture result | Capture time | Claim status |
|---|---|---|---|---|
| NadLan Hebrew ZOHI page | https://nad-lan.co.il/projects/zohi-sde-dov/ | Loaded; title, canonical, headings, rendered text, article links and JSON-LD captured | 02:52:51 | Valid evidence of what the current page publishes, not independent proof of its claims |
| Official ZOHI project site | https://www.zohi.co.il/ | Loaded; visible hero plus hidden accordion text and source markup inspected | 02:54:23 | Current first-party marketing evidence |
| Levinstein project URL | https://www.levinstein.co.il/פרוייקטים/פרויקט-שדה-דב/ | Loaded and redirected/canonicalized to official ZOHI site | 02:58:35 | Confirms the official project destination |
| Levinstein marketed-project archive | https://www.levinstein.co.il/project-stage/%D7%91%D7%A9%D7%99%D7%95%D7%95%D7%A7/ | Loaded; archive heading and ZOHI entry captured | 02:58:54 | Current first-party evidence for `בשיווק` category only |
| Globes planning report | https://www.globes.co.il/news/article.aspx?did=1001487655 | Loaded; headline, author, date, article body, canonical and NewsArticle data captured | 03:04:41 | Dated attributable evidence for the 2024 planning version |
| Mako launch report | https://www.mako.co.il/finances-real-estate/Article-1b581a9f8f40c91026.htm | Loaded in a fresh Chrome tab; headline, author, publication time, body, canonical and meta captured | 03:07:33 | Dated attributable evidence for January 2026 launch terms and configuration |
| RMI Eshkol plan PDF | https://apps.land.gov.il/IturTabotData/takanonim/telmer/5050215.pdf | Official PDF URL loaded; Chrome title `5050215.pdf`; document body exposed no text | 03:05:43 | Official source candidate, but no claim extracted from it in this run |
| Levinstein 2025 annual report on Maya | https://mayafiles.tase.co.il/rpdf/1730001-1731000/P1730141-00.pdf | Official PDF loaded in Chrome viewer; title identified; body and accessibility text empty | 02:57:30 | Official filing candidate, but no project claim extracted |
| Tel Aviv municipal sitemap lead | https://www.tel-aviv.gov.il/sitemap_adds.xml | Direct navigation failed with `net::ERR_BLOCKED_BY_CLIENT` | about 03:00 | Discovery lead only; no municipal claim accepted |
| Globes January 2026 result | https://www.globes.co.il/news/article.aspx?did=1001533129 | Google result was visible, but a later direct attempt resolved to a blank tab | about 03:05 | Rejected as direct claim evidence; overlapping launch facts are sourced to the successfully opened Mako report |

## Live Hebrew page capture

### Head and index signals

- URL: https://nad-lan.co.il/projects/zohi-sde-dov/
- Title: `ZOHI זוהי שדה דב - לוינשטין מבנה אלייד · תצוגת פרויקטים`
- Canonical: self-referencing
- Robots: index and follow
- Language: Hebrew
- Direction: RTL
- Visible H1 count: one
- First project-name heading: an H2 before the H1
- H1 rendered top: approximately 7,600 pixels below the page start
- Article length: approximately 23,100 characters and 3,935 words
- Article external links: only a `mailto:` correction/contact link

### Captured page claims requiring source review

The early showroom layer published 12 floors, four apartments to choose from, four available units, four detailed demo apartments, a price range of NIS 79,200 to NIS 100,800 per sqm and an average asking price of NIS 90,000 per sqm.

The article later said that no unit-level price information had been provided and that a price-per-square-metre range should not be invented. It also presented 20/80, launch status, about NIS 1.5 billion expected revenue, a rooftop pool and lot 110 as if they were current project facts without source links or dates.

The page emitted four JSON-LD blocks. The custom FAQ data stated 12 floors and about NIS 90,000 per sqm, while its four questions did not match the nine visible article FAQ questions. The `ApartmentComplex` data encoded lot 110 as a postal street address. These observations are fully assessed in `existing-page-audit.md`.

## Official project-site verification

The official site initially exposed only its hero copy through visible text because the project detail sits in accordions. The rendered source text was therefore inspected directly from the same Chrome tab, without switching browser surfaces.

The following current first-party content was found:

- residential project positioning in Sde Dov, Tel Aviv;
- modern Bauhaus design and relatively low construction compared with the neighborhood;
- a private urban garden of about 2.8 dunams;
- shared workspaces;
- 230 apartments;
- current published mix of 2 to 6 rooms plus penthouses;
- 3 metre ceilings in the apartment product copy;
- gym, yoga area and residents' lounge;
- Galor Fishbein Architects;
- Tal Goldschmidt Fish for architecture and interior design;
- Levinstein, Metropolis and Mivne in the developer section;
- explanation that Metropolis leads Allied Real Estate's residential arm.

The following terms were searched in the official rendered source text and were not found as current textual claims:

- 20/80;
- 2030;
- floor count;
- exact building count;
- current price;
- current availability;
- permit stage;
- pool.

Pool-related asset filenames were present. An asset filename is not treated as equivalent to current buyer-facing text or a sale specification.

## Dated source reconciliation

### August 2024 planning report

The directly opened Globes article tied planning lot 110 to Allied, Levinstein and Mivne, 230 homes, a 4.6 dunam lot and Galor Fishbein Architects. It described a four-building version with two 16-storey and two 9-storey buildings. At that publication date, the design-and-development plan was described as a step before a building permit and subject to conditions.

This source is accepted for planning history and the lot designation. It is not accepted as the current building configuration or current permit status.

### January 2026 launch report

The directly opened Mako article reported that early marketing was opening and described:

- 230 apartments plus commercial space on 4.6 dunams;
- two 15-storey towers with 66 apartments each;
- one 7-storey building above commerce;
- an internal garden of about 3 dunams;
- a shared level on the lower building with a pool, gym and lookout;
- about 80 apartment types, studios through 5.5 rooms and penthouses;
- NIS 70,000 to NIS 100,000 per sqm at launch;
- 20 percent at signing and the balance at occupancy during early marketing;
- expected occupancy in the second half of 2030;
- site works reported as having begun;
- expected revenue of about NIS 1.5 billion attributed to the companies.

All of these remain January 2026 reporting. They do not become current August 2026 offers, inventory, construction verification or contractual commitments.

### Resolution applied

- Current apartment mix: official 2 to 6 rooms plus penthouses.
- Current garden wording: official about 2.8 dunams.
- Current stage: Levinstein category `בשיווק`.
- Current building count: not published in the first-party text inspected.
- Historical configuration: January 2026 three-building report, if dated and attributed.
- Superseded configuration: August 2024 four-building planning version.
- Current price, 20/80, availability, delivery and construction: not verified as current.

## Google source-discovery ledger

The following exact Hebrew factual queries were run in Google Israel through the connected Chrome browser:

| Approximate Israel time | Query | Purpose | Result disposition |
|---|---|---|---|
| 02:53 | `ZOHI זוהי שדה דב לוינשטין מבנה אלייד 230` | Entity and first-party discovery | Led to official site and secondary results |
| 02:55 | `לוינשטין מטרופוליס מבנה משיקות זוהי 230 דירות בריכה 20/80` | Launch report discovery | Led to attributable January 2026 reporting |
| 02:56 | `site:mayafiles.tase.co.il שדה דב מגרש 110 230 לוינשטין מבנה אלייד` | Official filing discovery | Led to Maya/TASE report PDF |
| 02:56 | `לוינשטין שדה דב 230 יחידות דוח תקופתי 2025 מגרש` | Filing and company-report discovery | Found annual-report candidate and secondary snippets |
| 02:58 | `site:levinstein.co.il זוהי שדה דב` | Official developer verification | Found project redirect and marketed archive |
| 02:59 | `site:tel-aviv.gov.il "מגרש 110" "אשכול" שדה דב` | Municipal lot record | Found sitemap lead only |
| 02:59 | `"מגרש 110 שדה דב המ5854.pdf"` | Exact municipal file discovery | Filename found in snippet; underlying file unresolved |
| 02:59 | `site:tel-aviv.gov.il/PRDocs/ "מגרש 110 שדה דב"` | Direct municipal document discovery | No matching result |
| 03:00 | `site:land.gov.il 230 יחידות שדה דב לוינשטין מבנה אלייד` | RMI planning source | Broad result risked mixing central-district plan with Eshkol |
| 03:00 | `site:apps.land.gov.il מתחם אשכול שדה דב תכנית מגרש 110` | Correct Eshkol statutory source | Found plan 3001 and supporting official planning documents |
| 03:03 | `"230 יח"ד ובית ספר" שדה דב 27 באוגוסט 2024` | Exact planning article | Direct Globes article opened successfully |
| 03:04 | `site:globes.co.il ZOHI שדה דב 27 בינואר 2026 לוינשטין מטרופוליס מבנה` | Second-source launch cross-check | Result visible; direct page not accepted due blank-tab result |

The localized buyer-intent queries in English, French, Russian and Arabic are not repeated here. They are preserved with exact URLs and timestamps in `cultural-intent-support.md`.

## Verification blockers and their publication effect

### RMI PDF text unavailable in Chrome

The official Eshkol plan PDF loaded, but Chrome exposed no document text. Effect: the plan is retained as an official planning-context source, but no exact ZOHI lot, floor, address or permit claim is extracted from it.

### TASE/Maya report text unavailable in Chrome

The annual report loaded from the official filing host but exposed no text. Effect: it remains a candidate source. It may appear in the final source list only if a specific page is verified before publication. It supports no number in the current fact contract.

### Municipal page blocked

The municipal sitemap request failed with a client-blocked error. A Google snippet showed a promising file name, but the underlying content could not be inspected. Effect: no municipal permit status or postal address is asserted.

### Direct second Globes launch article unresolved

The Google result surfaced a January 2026 Globes article, but a direct attempt did not produce an inspectable page. Effect: no claim is sourced to that result. The successfully opened Mako article is the dated launch source.

### No current first-party commercial documents

The inspected official site and developer archive did not provide a current unit schedule, price list, delivery term or payment sheet. Effect: all four language articles must use unpublished/currently unverified wording for those fields.

## Evidence integrity checks

- No search-result snippet is used as the sole support for a locked claim.
- No PDF is cited for a specific fact when its text was not exposed.
- No current term is inferred from a January 2026 launch report.
- No planning lot is normalized into a street address.
- No apartment demo fixture is accepted as inventory.
- No 2024 and 2026 building configurations are merged.
- No current price estimate is generated.
- The same locked fact values apply to all four target languages.

## Files produced by this audit

- `00-source-ledger.md`: source hierarchy, locked multilingual fact contract, conflict resolutions, rejected claims and exact final source order.
- `existing-page-audit.md`: rendered Hebrew page, semantic, factual, trust and structured-data audit.
- `03-browser-source-verification.md`: this direct Chrome verification record.
- `cultural-intent-support.md`: pre-existing authoritative localized intent ledger. It was not modified.

No `01-live-google-intent-ledger.md` was created because the cultural brief already fully covers that evidence layer.

## Final browser handling

All tabs opened or reused for this ZOHI source run are to be finalized together after artifact validation. No browsing is required for the writing stage unless a new volatile claim is introduced or one of the blocked official documents becomes directly readable.
