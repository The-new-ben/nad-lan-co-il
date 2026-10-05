# Technical audit, nad-lan.co.il (HAD-435, crawl of 5.10.2026)

## How the crawl was done (and what was not possible)

- **Screaming Frog did not run.** The CLI refused to start headless: "Could not locate licence file ...
  C:\Users\777\.ScreamingFrogSEOSpider\licence.txt" (the CLI needs a paid licence; the free GUI mode is 500 URLs and
  interactive). No licence is listed in the tools registry. Log: scratchpad `sf1/sf1.log`.
- **Replacement: a polite stdlib Python crawler** (4 workers, 0.15 s pause per request, no redirect following inside a
  fetch, robots.txt respected: only the two `pms_` disallows exist). It started at the home page, followed every internal
  link breadth-first (link depth), then fetched every sitemap URL the links never reached. **4,638 URLs fetched =
  100% of the 4,528 sitemap URLs + 110 linked URLs.** Query-string URLs (`?city=`, `?lang=`, `?listing_type=`) were
  recorded as links but not crawled. Rendering: raw HTML (no JavaScript), which is what Google's first wave sees and
  what the public-source law audits.
- Outputs (`data/crawl/`): `tech-summary.json`, `onpage-issues.csv`, `internal-links-to-non200.csv`, `orphans.csv`,
  `canonical-issues.csv`, `hreflang-issues.csv`, `noindex-pages.csv`, `sitemap-non200.csv`, `indexable-not-in-sitemap.csv`,
  `redirects.csv`, `gsc-pages-not-200.csv`. Sitemap snapshot: `data/sitemap-urls.csv` (17 child sitemaps).
- GSC URL Inspection (read-only) on 10 URLs; GSC sitemap status read.

## Findings ranked by traffic impact

### T1. 893 of 1,037 project pages are orphans (reachable only through the XML sitemap) - HIGH
- 1,002 sitemap URLs have **no internal link** from any page reachable from the home page; 893 are `/projects/...`,
  64 professionals, plus /catalog/, /north-tel-aviv/bavli/ (212 impressions), /north-tel-aviv/shchunat-lamed/,
  /north-tel-aviv/old-north/, /construction-engineering-guide/ (the owner's 10.9K-word article),
  /property-value/luxury-apartments-tel-aviv/, /buy-vs-rent/, /projects/ashdar-einstein/.
- Cause (verified): /projects/ and each `?city=` / `?project_type=` view print about 25 project links in HTML and no
  crawlable pagination (the owner's no-pagination rule), so most of the 1,037 projects are never linked.
- Impact: orphan project pages still earned 6,509 impressions and 180 clicks in the property's life (676 of them
  have impressions). They are the "names" traffic engine (gsc-baseline.md) and they rank on sitemap discovery alone.
- Fix without pagination: (1) a server-rendered "all projects by city" index (e.g. on /site-map/ or a collapsed
  section at the foot of /projects/: plain links, no JavaScript); (2) a "more projects in {city}" block of 6 links on
  every project page; (3) developer pages in the professionals directory link to their projects.

### T2. Money pages with almost no internal links - HIGH
| page | inlinks | depth | why it matters |
|---|---:|---:|---|
| /urban-renewal/map/ | **1** | 2 | #6 click page, owns "מפת התחדשות עירונית" (pos 11) |
| /sde-dov/merkaz/ | 1 | 2 | |
| /new-projects/north-tel-aviv-new-projects/ | 1 | 2 | owner of "פרויקטים חדשים בצפון תל אביב" ($18/click) |
| /herzliya-projects/ | 4 | 3 | the only city projects page left |
| /projects/hamedina-en, -fr, -ru, -ar | **5 each** | 2 | language switcher + one image only |
| /sde-dov/prices/ | 7 | 2 | Google's preferred page for "דירות למכירה בשדה דב" |
| /new-projects/new-projects-tel-aviv/ | 12 | 1 | owner of "פרויקטים חדשים בתל אביב" (320/mo, $10.18); last crawled 11.8 |
| /luxury-tel-aviv/ | 17 | 3 | owner of "דירות יוקרה בתל אביב" |
| /projects/duo-tel-aviv/ | 23 | 2 | #2 click page |
| /real-estate-appraiser/, /home-inspection/ | 35 / 43 | 2 | $8.6 / $14 CPC words |

Sitewide links exist (header/footer, ~4,400 pages) for /projects/, /sde-dov/, /investment/, the tools, Rainbow,
Dimri Yama and Kikar, but several **anchors are not the money word**:
- /projects/hamedina/ is linked sitewide as "כיכר המדינה" (the square: 5,400 searches of place intent) instead of
  "מגדלי כיכר המדינה".
- /real-estate-lawyer/ is linked 4,220 times as "בדיקה משפטית" and 82 times as "עורך דין מקרקעין".
- /projects/dimri-yama-sde-dov/ is linked 4,425 times as "Dimri Yama" (Latin); Hebrew demand is "דמרי שדה דב" ($17.51).
- Glued anchor texts in the raw HTML: "כל הפרויקטים976" (/projects/) and
  "סיור וירטואלי · הדמיה להמחשהריינבו תל אביב: ..." (Rainbow). A space or separate element is missing.

### T3. Kikar Hamedina language pages: two of four not in Google - HIGH (for HAD-433)
URL Inspection 5.10: /projects/hamedina/ indexed (crawled 1.10); -fr indexed (4.10); -ar indexed (1.10);
**-en "URL is unknown to Google"; -ru "Discovered - currently not indexed"**. All five are in the sitemap with a
complete hreflang cluster and x-default. Cause: 5 internal links each. Fix: links from /en/, /ru/ homes and their
"new projects" pages, from the English/Russian flagship project pages (duo-en, rainbow-en, ...), and from the luxury
and Tel Aviv price pages. A "Request indexing" is a GSC write: the owner's word.

### T4. Broken internal links: 83 dead targets, 233 linking pages - MEDIUM-HIGH (easy)
All fixable by correcting the href (no redirects needed). Top items (`internal-links-to-non200.csv`):
| dead target | status | linked from | correct target (likely) |
|---|---|---:|---|
| /cities/תל-אביב-יפו/ | 410 | 45 language project pages (-en/-fr/-ru/-ar template) | /tel-aviv-apartment-prices/ or the TLV projects page |
| /mortgage-ltv-ratio/ | 404 | 26 (city price + investment city templates) | /mortgage-calculator/mortgage-ltv-ratio/ |
| /city/תל-אביב-יפו/projects/ | 410 | 18 /tel-aviv-plans/ pages | /new-projects/new-projects-tel-aviv/ |
| /mortgage-interest-rates/ | 404 | 10 | /mortgage-calculator/mortgage-interest-rates/ |
| **/reverse-mortgage/, /mortgage-repayment-capacity/** | 404 | 4 each, **including /mortgage-calculator/ itself** | /mortgage-calculator/reverse-mortgage/ ... (the parent-to-child money link from the 25.8 plan is broken) |
| /apartments-for-investment/, /real-estate-yield/, /bank-guarantee-purchase/ | 404 | /investment/ and children | /investment/... paths |
| 11 office price pages (/tel-aviv-office-prices/ ...) | 404 | /apartment-prices/ | /commercial-real-estate/... paths |
| /real-estate-lawyer/sale-deed-apartment/, /apartment-sale-contract/, /power-of-attorney-real-estate/ | 404 | lawyer cluster | correct /real-estate-lawyer/... paths |
| /short-term-rentals-{country}/ (6) | 404 | the short-term-rentals cluster | /short-term-rentals-abroad/... |
| 8 English article slugs (/transfer-money-to-israel-property/, /invest/, /pros/appraiser/, /tools/...) | 404 | English author/category archives, /buy-property-israel-foreign-buyers/ | unpublished English pages: remove or point to existing ones |
| /investment/income-producing-properties/ | 301 to a .jpg | /commercial-real-estate/office-for-sale-tel-aviv/ | an attachment URL; link the article instead |

### T5. Titles, H1s and meta - MEDIUM (money pages first)
Counts on 4,528 indexable pages: title > 70 chars 142 (96 projects), title < 25 chars 149 (121 glossary),
duplicate titles 32, duplicate H1 156 (mostly same-name professionals, natural), multiple H1 14, meta missing 43,
H1 mixing Hebrew and Latin 54.
Money-relevant ones:
- **/property-value-estimator/** (our #1 click page, 5,894 impressions/90d): title "מחשבון שווי דירה - נדלן" (23 chars)
  misses "הערכת שווי דירה" (590/mo) and "בחינם" (590/mo).
- **Project titles lead with Latin names and run long**: "GINDI VOGUE שדה דב - פרוייקט גינדי ווג, תל אביב יפו -
  מחירים, דירות ובחירה מהבניין | נדלן" (89), YOO (101), Park Bavli (86), Ashdar Einstein (92), FIRST שדה דב (77).
  Hebrew searches use "גינדי", "דמרי", "פארק בבלי". Put the searched Hebrew name first, keep the Latin brand second,
  stay under ~60 characters.
- /sde-dov/ title "שדה דב: כל הפרויקטים, המחירים והדירות למכירה | המדריך המלא" competes with /sde-dov/prices/
  (cannibalization.md A).
- 121 glossary titles are "{term} - נדלן" (the glossary has 19.5K impressions at pos 29; e.g. "יועץ איטום" 620
  impressions where "יועץ איטום מוסמך" has a $23 CPC). A short descriptor helps CTR.
- /global/* (9 pages) and /site-map/ print the site name "נדלן" as an extra H1 (multiple H1s); template issue.
- /properties/ has no meta description and shares its title with another listing page.

### T6. Hreflang - LOW
1,189 pages carry hreflang. Among crawled pairs: **no missing return links, no non-200 targets**, x-default present
on the flagship clusters (Kikar's five pages are a complete cluster). 46 alternates are `?lang=en|ar` URLs on
/global/*, /site-map/, /my-rentals/, /my-renewal/: they are self-canonical but their HTML says `lang="he-IL" dir="rtl"`.
Note (owner decision 28.9, not a defect): Arabic pages carry English titles (e.g. /projects/hamedina-ar/).

### T7. Sitemap coverage - LOW
- 4,528 sitemap URLs, **all return 200**, none canonicalised elsewhere. GSC: sitemap index downloaded 5.10, 0 errors.
- 22 sitemap URLs are noindex (the demo professionals and properties, which the owner keeps as the listings seed, 25.8).
  The sitemap and the robots meta disagree; the owner decides whether they leave the sitemap.
- 23 indexable pages are **not in the sitemap**: /global/ and 8 country pages (1,314 impressions in 90 days),
  /site-map/, /my-renewal/, /my-rentals/, /advertiser-center/, /studio/, paginated archives.
- /sitemap/ now answers 301 to /site-map/ (the 25.8 duplicate is resolved).

### T8. Canonicals, redirects, robots - OK
- No canonical conflicts. 8 pages without a canonical are noindex tool/tour pages (/tour/sde-dov/, /tour/somail/,
  /earth/*, /compare/, /studio/, /advertiser-center/). `?city=` views carry a canonical to /projects/.
- Only 2 internal redirects (/my-appointments/ to login; the .jpg above). No chains. http to https is a single 308.
- robots.txt: `Allow: /`, two `pms_` disallows, sitemap line. Nothing blocks money pages.
- GSC pages with 20+ impressions in 90 days that are not 200: 88, all the purged /city/ (410) and `?city=`
  URLs (expected).

### T9. Thin pages - LOW-MEDIUM
46 indexable non-professional pages have under 300 words of main content (`onpage-issues.csv`, flag thin<250w plus the
summary list): glossary stubs (/glossary/dayar-sarvan/ 224 words, /glossary/shamai-pinui-binui/ 268), /post-listing/,
/about/, /contact/, /buy-vs-rent/ (253, duplicate of /buy-or-rent/), /urban-renewal/check/ (131), /developers/ (286),
about 12 project pages of ~275 words (e.g. /projects/שער-צפון-מער-רמלה/, 11 clicks: thin but earning, keep and enrich).
/sde-dov-luxury-projects-2026/ has 437 words against a 5,525-word hub (merge candidate).

### T10. Depth and speed - MEDIUM (measure in GSC Core Web Vitals, not pulled here)
- Link depth from home: 0:1, 1:70, 2:467, 3:231, 4:98, 5:217, 6:644, 7:1,077, 8:556, 9+:103, unreachable: 1,091.
  Money hubs sit at depth 1-2 except /herzliya-projects/ and /luxury-tel-aviv/ (3).
- From this machine: median TTFB 853 ms; median HTML 226 KB (heavy inline payload on every page); /projects/ took
  5.2 s and 325 KB; a few professional pages took 6-55 s (outliers worth a server-log look).

## Fix list in order (all read-only findings; each change is a release under the owner's process)

1. Fix the 83 broken hrefs (T4), starting with the two templates (language project pages -> /cities/..., price and
   investment pages -> /mortgage-ltv-ratio/) and /mortgage-calculator/'s own child links.
2. Link the orphans (T1): an all-projects-by-city index + "more projects in {city}" on project pages.
3. Give the money pages their links and the money anchors (T2): /urban-renewal/map/, /sde-dov/prices/, TLV and North TLV
   project pages, the Kikar language pages, the lawyer anchor, Hebrew Dimri anchor, the glued anchors.
4. Retitle the estimator and the Latin-first project pages (T5).
5. Add /global/ and its 8 country pages to the sitemap; fix the double H1 template on /global/* and /site-map/.
