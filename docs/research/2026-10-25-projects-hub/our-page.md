# /projects/ on nad-lan.co.il: inventory of our own page (25.10.2026)

Read-only research for the projects-hub upgrade. Nothing on the live site or in the repo was changed; this file is the only output.
**Constraint from the owner: the `<title>` must not change.**

Evidence classes used below:
- **raw**: raw HTML fetched with curl (browser user agent, `?z=<timestamp>` cache-buster) at 07:35 UTC, 25.10.2026.
- **dom**: positions measured in a real browser (the built-in browser pane, at 1440x900 and 375x812). No screenshot was reviewed, so this is not "eyes".
- **code**: read from the repo or from the saved live snippet copy.
- **rest**: public WordPress REST and plugin REST routes.
- **gsc**: Search Console API, read only, 25.7 to 23.10.2026 (90 days), property `sc-domain:nad-lan.co.il`.

Live plugin version during the research: **1.72.512** (`/wp-json/nadlan/v1/health`, status ok).

---

## 0. The short version

- The page is a PHP-rendered catalog. It is **not a WP page and not an option**. `inc/directory.php` renders the whole page on `template_redirect` and then calls `exit`.
- A live Code Snippets snippet, **#661 "x-catalog-plus"**, rewrites that output through an output buffer. It adds the search bar, the map, the sidebar price map, the card enrichment, the body copy (H2s, price table, city links, FAQ) and the ItemList and FAQPage JSON-LD.
- The repo's `inc/catalog-plus.php` is only a stale 6.9 mirror of that snippet. The live code is the snippet.
- Title is `פרויקטים חדשים בישראל | דירות מקבלן לפי עיר ויזם | נדלן`. The H1 is `פרויקטים חדשים בישראל`. Canonical is self, robots is `index, follow`, and there is **no hreflang**.
- The page shows 24 cards out of **976** catalog projects. Of those, 942 are pinui-binui compounds (mostly in statutory planning), 19 are new-build and 5 are tama 38.
- **1,036** projects are published in total: 976 in the catalog plus 60 language siblings, which are 15 projects x en/fr/ru/ar.
- There is no `/en|fr|ru|ar/projects/`; all four return 404.
- In the last 90 days GSC shows 24,474 impressions, 7 clicks and an average position of 44. The head queries are `פרויקטים חדשים` (1,220 impressions, position 32.5), `פרויקטים חדשים בתל אביב`, `דירות מקבלן` and `דירות חדשות בתל אביב`.
- Main defects, detailed in section 7:
  - `/projects/page/N/` serves the same 24 cards as page 1 and is self-canonical.
  - og:title and the schema name read `ארכיון NadLan Projects - נדלן`.
  - The prose says "18 ערים", but 78 cities are in the data.
  - The prose says verified projects are marked, but `verified_at` is empty on all projects.
  - Be'er Sheva is missing from the city lists.
  - There is a stray `</a>` in the grid.
  - The page has no links to the `/new-projects/` family.

---

## 1. What the live page shows

### 1.1 Head (raw)

| Item | Live value |
|---|---|
| `<title>` | `פרויקטים חדשים בישראל \| דירות מקבלן לפי עיר ויזם \| נדלן` (do not change) |
| meta description | `כל הפרויקטים החדשים ודירות מקבלן בישראל בקטלוג אחד. חיפוש לפי עיר, יזם וסטטוס, ומידע מסודר על כל פרויקט לפני הפגישה עם היזם.` |
| canonical | `https://nad-lan.co.il/projects/` (self) |
| robots | `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` |
| hreflang `<link rel="alternate">` | **none**. Only the header language switcher anchors carry `hreflang` attributes, and they point to the homes `/`, `/en/`, `/fr/`, `/ru/`, `/ar/` |
| rel next | `https://nad-lan.co.il/projects/page/2/` (see finding F1) |
| og:title | `ארכיון NadLan Projects - נדלן` (Yoast's post-type-archive default; differs from `<title>`; see F2) |
| og:image | `/wp-content/uploads/2026/09/og-default-1200x630-1.jpg` (the site default) |
| html lang / dir | `he-IL`, rtl. Body classes include `post-type-archive-nadlan_project nl-skin-a nlpc-platform nlpc-project-archive` |
| feed | `/projects/feed/` (200) |

### 1.2 Heading outline (raw, in source order)

```
H1  פרויקטים חדשים בישראל
H4  מפת מחירים: ₪ למ"ר לפי עיר               (sidebar)
H4  ערים מובילות                             (sidebar)
H3  x 23 project names + 1 sponsored slot "הציגו את הפרויקט שלכם כאן"   (cards)
H2  פרויקטים חדשים בישראל: מה יש בקטלוג
H2  דירה חדשה מקבלן: מה בודקים לפני שחותמים
H2  בנייה חדשה, פינוי בינוי ותמ"א 38: מה ההבדל לקונה
H2  מחירי דירות חדשות לפי עיר
H2  פרויקטים חדשים לפי עיר
H2  שאלות על פרויקטים חדשים ודירות מקבלן
(H3 '+p.title+' sits inside a JS template for the map card; it is not rendered text)
```

Card H3 order on page 1 (sort "featured" = paid tier, then menu_order, then date):
1. DUO
2. Rainbow
3. כיכר המדינה
4. Aurelia Sports
5. SIX-8 הרברט סמואל
6. H Infinity
7. (sponsored slot)
8. ToHa2 (offices)
9. THE PARK (offices, Bnei Brak)
10. שער צפון רמלה
11. הגנה/סלוודור
12. אחד העם 33-35
13. צאלים/האילנות
14. מעלה געתון
15. נתיב חבצלת
16. ביאליק שמעוני
17. בן צבי
18. הסתדרות
19. העצמאות
20. אאורה פיבקו בת ים
21. YOO
22. מגדל מאייר
23. מגדלי המרינה הרצליה
24. אקירוב
25. פארק בבלי

### 1.3 Sections in rendered order (raw + dom)

| # | Section | Content | Desktop 1440 top (px) | Phone 375 top (px) |
|---|---|---|---|---|
| 1 | Header | Sticky `nlhp-top`: logo, mega menu "פרויקטים חדשים" (cities with counts linking to `/projects/?city=…`, types, areas, virtual tours), language switcher | 0 | 0 |
| 2 | Hero card | Crumbs `בית › פרויקטים`, then H1 | H1 169 | H1 119 |
| 3 | Lead | `976 פרויקטים בקטלוג: 942 מתחמי פינוי בינוי, 19 פרויקטים בבנייה חדשה ו־5 פרויקטי תמ״א 38, לפי עיר, יזם וסטטוס. בעלי דירות בבניין ישן? המדריך המלא להתחדשות עירונית` (link to `/urban-renewal/`) | 227 | 191 |
| 4 | Intro | `מחפשים דירה חדשה מקבלן? כאן בודקים כל פרויקט לפני הפגישה עם היזם: סטטוס בנייה, יחידות, מיקום וכל מה שחשוב לדעת לפני שמתקדמים.` | 312 | 338 |
| 5 | Type pills | הכל / תמ״א 38 (5) / פינוי בינוי (942) / בנייה חדשה (19) | 419 | 506 (the row is 555px wide and scrolls inside itself) |
| 6 | Search bar | Fields: project or developer (free text), city (18 cities with counts), status (בתכנון/בהיתרים/בשיווק/בבנייה/הושלם), type, size (from 20/50/100/300 units), sort; plus "קרוב אליי" and "הצגת פרויקטים" buttons. A hidden legacy search form is also in the source | 475 | 569 (353px tall) |
| 7 | Map thumbnail | Mapbox static 240x240 with an overlay "מפת מחירים ופרויקטים · מחיר למ״ר על כל פרויקט · לחיצה פותחת" and a "פרויקטים לידי" pill; opens a full-screen map (`#map`) fed by REST `nadlan/v1/project-map` | 475 (left column) | 936 |
| 8 | Count and sort bar | `976 פרויקטים`, chips, sort select | 810 | 1291 |
| 9 | **Card grid** | 24 cards: 4 columns on desktop, 1 on phone. The sponsored slot is after card 6 | first card 883 | first card **1,365** |
| 10 | Sponsored slot | "מקודם · פנוי / הציגו את הפרויקט שלכם כאן / ₪3,990 לקמפיין", linking to `?add-to-cart=489&ref=ss` and `/join-pro/` | 1,692 | 5,180 |
| 11 | "הצגת עוד" | Loads 24 more cards through REST `nadlan/v1/projects-plus` (JS only) | 5,781 | 14,944 |
| 12 | Sidebar | Price map: 12 cities by ₪/m² as bars (TLV 52,856 … Haifa 18,807), "חציון עסקאות, רשות המסים"; then "ערים מובילות" (12 city buttons). These are JS filter buttons, not links | right column, 810 | moved **below the grid**, 15,024 |
| 13 | Prose box (`section.nlcp-body`) | The six H2s with paragraphs, a 6-item checklist, links to the developer-buying guide, `/buying-apartment/` and `/purchase-tax-calculator/` | 5,933 | 15,853 |
| 14 | Price table | 12 cities. Columns: projects in catalog, ₪/m², 4-room median, deals, period. Each city name links to `/projects/?city=…` | 6,729 | 17,331 (scrolls sideways inside its box) |
| 15 | City chips | 14 links `פרויקטים חדשים ב<עיר> <n>` to `/projects/?city=…` | 7,391 | 18,018 |
| 16 | FAQ | 5 `<details>` questions | 7,586 | 18,740 |
| 17 | Footer | Brand line, links (כל הפרויקטים, Ashira, Rainbow, Dimri Yama, mortgage calculator, purchase tax, buying guide, legal check, professionals, Sde Dov, about), tools row, legal | 7,951 | 19,048 |
| 18 | Legal notice | `nl-legal`: an independent site, not official, names for identification only | after footer | after footer |
| 19 | Floating WhatsApp pill `#nlcta` | "לקבלת מחירים, תוכניות והטבות · מענה בוואטסאפ" (fixed) | fixed | fixed |

Document height: 8,638px on desktop and 20,422px on the phone. There is no horizontal page scroll on the phone (scrollWidth 375).

**Card anatomy (raw):**
- An image with alt `<title> · הדמיה להמחשה`.
- A type badge.
- The H3 name and the city.
- A stats list: units and developer, or units and status.
- Up to 4 facility chips (`nlfc`, spans that deep-link to `/premium/?fac=`).
- A facts list: neighbourhood, floors, buildings, occupancy year or "שנת תוקף התוכנית", developer, architect.
- A price-context line: `מחיר למ"ר ב<עיר>: X ₪ · ברחוב <רחוב>: Y ₪ / N עסקאות, period · רשות המסים`.
- "לצפייה בפרויקט".
- Outside the anchor, a `<details>` "עוד פרטים על …": city, address, units, facts, city ₪/m², 3/4/5-room medians, street ₪/m², a source note, and "לעמוד הפרויקט".

### 1.4 Counts (raw + dom)

| Metric | Value |
|---|---|
| Project cards | 24 (`article.nlcp-card`), plus 1 sponsored slot |
| Visible words, rendered | **~2,125** on desktop and 2,104 on the phone (`innerText`; closed details are excluded) |
| Words in source text | 3,860 in the whole body (including collapsed "עוד פרטים" and FAQ answers); 3,290 from hero to FAQ; **785** in the prose section |
| `<a href>` in body | ~211; 136 unique internal URLs; 77 unique paths |
| Links in the content region (hero to FAQ) | 83 links, 46 unique. Breakdown below |
| `<img>` in body | 28. Breakdown below |
| Main JSON-LD blocks | 3 (section 1.5) |

Links in the content region:
- 24 project pages, each linked twice (card and "לעמוד הפרויקט").
- 14 `/projects/?city=` links.
- `/urban-renewal/` (x2).
- `/buying-new-apartment-developer-2026-negotiation/`, `/buying-apartment/`, `/purchase-tax-calculator/`.
- `/join-pro/` and the add-to-cart 489 link from the sponsored slot.
- The home crumb and `#map`.

Images:
- 24 card images from uploads, lazy-loaded, with alt text.
- 1 Mapbox static thumbnail, eager, with the public `pk.` token in the URL.
- 2 Rainbow posters in the mega menu.
- 1 inside a JS template.
- No `fetchpriority` or preload hint anywhere.

### 1.5 JSON-LD (raw)

1. **Yoast graph** (`class="yoast-schema-graph"`, in the head):
   - `CollectionPage` with `@id` `https://nad-lan.co.il/projects/`, **name `ארכיון NadLan Projects - נדלן`**, inLanguage `he-IL`, isPartOf `#website`, breadcrumb `@id` `/projects/#breadcrumb`.
   - `ImageObject` `#primaryimage`, `WebSite`, `Organization`.
2. **BreadcrumbList** with `@id` `https://nad-lan.co.il/projects/#breadcrumb`: בית › פרויקטים. It comes from `inc/breadcrumbs.php`. Since the 1.72.512 fix, the Yoast pointer resolves to it.
3. **`class="nlcp-schema"`** (end of body, from snippet 661), a `@graph` with two nodes:
   - `ItemList` named `פרויקטים חדשים בישראל`, numberOfItems **976**, itemListOrder Descending. It has **24** `ListItem`s (position, url, name, image), matching the 24 visible cards.
   - `FAQPage` with **5** questions:
     1. מה נחשב פרויקט חדש מקבלן?
     2. מה ההבדל בין דירה חדשה מקבלן לדירה יד שנייה?
     3. איך בודקים פרויקט חדש לפני שחותמים?
     4. מה ההבדל בין בנייה חדשה, פינוי בינוי ותמ"א 38?
     5. איפה רואים מחירים של דירות חדשות?

There is no `SoftwareApplication`, `Place`, `Residence` or `Offer` on the archive.

### 1.6 URL variants (raw)

| URL | Status | What it serves |
|---|---|---|
| `/projects/?city=ירושלים` | 200 | Same title and H1. Cards are filtered server-side (total 197). **Canonical goes to `/projects/`** (`inc/city-hubs.php:142-147`; no city hub page exists, so it falls back to the archive root) |
| `/projects/page/2/` | 200 | **The same 24 cards as page 1** (identical URL list). Canonical is self (`/projects/page/2/`), `index`, with rel prev and next. `/page/41/` and `/page/42/` also answer 200. See F1 |
| `/projects/?project_type=tama38` | 200 | Filtered; GSC shows 27 impressions |
| `/city/<עיר>/projects/` (old hubs) | **410** | smart-404 "Gone". Still had GSC impressions in the last 90 days (F12) |

### 1.7 Search Console, last 90 days (gsc)

`/projects/` had **24,474 impressions, 7 clicks, CTR 0.03%, average position 44.0**.

Filtered views:

| URL | Impressions | Clicks | Average position |
|---|---|---|---|
| `?city=באר שבע` | 590 | 0 | 35 |
| `?city=תל אביב-יפו` | 478 | 0 | — |
| `?city=בת ים` | 163 | 0 | — |
| `?city=נתניה` | 130 | 0 | — |

Top queries for `/projects/`:

| Query | Impressions | Average position |
|---|---|---|
| פרויקטים חדשים | 1,220 | 32.5 |
| פרויקטים חדשים בתל אביב | 588 | 42.0 |
| דירות מקבלן | 529 | 29.9 |
| פרויקטים חדשים תל אביב | 495 | 37.9 |
| דירות חדשות בתל אביב | 482 | 43.4 |
| דירות חדשות מקבלן | 351 | 50.2 |
| פרויקטים חדשים במרכז | 344 | 37.7 |
| פרויקטים בתל אביב | 339 | 48.3 |
| דירה חדשה מקבלן | 329 | 33.3 |
| דירות חדשות | 319 | 52.8 |
| דירות חדשות למכירה | 312 | 45.0 |
| פרויקטים חדשים בצפון הישן תל אביב | 255 | 41.8 |
| דירות מקבלן בתל אביב | 250 | 40.2 |
| новостройки израиль | 213 | 71 |
| פרויקטים בבניה | 213 | 34.8 |
| פרויקטים חדשים בישראל | 212 | 27.2 |
| פרויקטים חדשים על הנייר | 179 | 34.2 (1 click) |
| פרויקטים חדשים מחירים | 160 | 28.6 |
| new projects israel | 167 | 77 |
| projet immobilier israël | 127 | 75.6 |
| obra nueva israel | 122 | 55.3 |

Foreign-language demand lands on the Hebrew archive.

---

## 2. Which code builds it

### 2.1 Where the content lives

- **Hardcoded PHP strings**, in two places:
  - The plugin file `plugins/nadlan-config/inc/directory.php` holds the page shell, H1, lead, pills, sidebar cities and grid.
  - **Code Snippets snippet #661 "x-catalog-plus"** on live (global scope, active) holds the search bar, map, price sidebar, card enrichment, body copy, FAQ and schema.
- **Not** an option, **not** a WP page, and **no** shortcode content.
- Dynamic data comes from:
  - postmeta, through the facets transient `nadlan_dir_projfacets_v3` (1 hour);
  - `uploads/nadlan-skin/deals-context-v1.json`, through the transient `nadlan_cp_deals_v1` (6 hours);
  - the option `nadlan_mapbox_token`;
  - REST `nadlan/v1/project-map`.
- **Repo versus live:**
  - The plugin repo HEAD is the 1.72.511 commit. Live 1.72.512 differs only in `inc/breadcrumbs.php`.
  - The repo `nadlan-config.php` header still says 1.72.372, because the version bump is applied to the live text only.
  - `inc/catalog-plus.php` and `inc/catalog-plus-map.php` are **not loaded by the plugin**: they are absent from the module list at `nadlan-config.php:33`. They are 6.9.2026 mirrors made by `scripts/skin-a/pull_live_snippets.py`.
  - The newest saved copy of the snippet is `docs/qa/had-460/snippet-661/snippet-661-pg-20261007T125758.json` (82,620 B, md5 `91f1d077c43fd2623258f4f341af59b6`, HAD-460, 7.10.2026). Seven distinctive live strings were checked and all are present in it.
  - Before editing, re-read the live snippet with `python scripts/project-stage/snippet_read.py 661`. It writes to `docs/qa/live-read/`, so it was not run here.

### 2.2 Element to code map

**Plugin, `plugins/nadlan-config/inc/directory.php` (repo = live):**

| Element | Lines | Notes |
|---|---|---|
| Whole-page render and `exit` | 1052-1057 | `template_redirect` priority 5 → `nadlan_dir_project_page()`. Kill switch `NADLAN_DISABLE_DIRECTORY` (1054) falls back to `themes/nadlan-platform-child/templates/archive-nadlan_project.html`, which is an empty `<main>` |
| **`<title>`** | 1028-1035 | `pre_get_document_title`, priority 20. **Keep exactly.** A comment there records the 2026-07-11 de-cannibalisation (renewal terms moved to `/urban-renewal/`) |
| Meta description | 1036-1040 | `wpseo_metadesc` 25; only when Yoast has none |
| Archive title | 1023-1027 | `get_the_archive_title` |
| Viewport meta | 1042-1050 | |
| Single-H1 guard | 24-40 | Demotes the theme-compat header h1 |
| Crumbs | 1089 | |
| **H1** | **1090** | |
| **Lead** (live counts) | 1091-1097 | |
| **Intro** | **1098** | |
| Legacy search form | 1099-1103 | Hidden by snippet CSS (snippet line 421 / mirror 406) |
| Type pills | 1104-1114 | Types at 812-822; counts from facets at 981-995. The city facet is capped by `LIMIT 18` at 989 |
| Drone band | 1116 | Retired on the catalog; the snippet's buffer cuts it out |
| Sidebar "ערים מובילות" | 1119-1127 | |
| Count and sort bar | 1129-1140 | |
| **Card grid** | **1141** | Query at 830-861: lang siblings excluded at 836-840 and 863-870; featured = paid-tier boost at 140-168. Card renderer 878-970; cards HTML plus the filter `nadlan_dir_cards_html` at 972-979 |
| "הצגת עוד" and base JS | 1142, 1146 | `nadlan_dir_js` / `nadlan_dir_css` in `directory-assets.php` |
| Base REST `nadlan/v1/projects` | 1002-1021 | |

**Snippet #661 (live). Lines are in the 7.10 copy; the stale repo mirror `inc/catalog-plus.php` is given for comparison:**

| Element | Snippet lines | Mirror lines |
|---|---|---|
| Output buffer that injects everything | 494-539 | 478-524 |
| Search bar (`#nlcp-bar`) | 377-397 | 361-380 |
| Map thumbnail and full map | 586-771 (thumb 611-622, shell 623-634, assets 635-771) | `inc/catalog-plus-map.php` |
| Sidebar price map (`nlcp-pricemap`) | 335-354 | 320-339 |
| Card enrichment | 126-212 (facts 126-143, context line 144-154, "עוד פרטים" 155-181, enrich 182-212) | 115-196 |
| Status filter REST `nadlan/v1/projects-plus` | 214-257 | 198-241 |
| **Body copy**: H2s, checklist, price table, city chips, FAQ markup | **295-334** (H2s at 303, 306, 316, 318, 321, 323; FAQ markup 324-328) | 280-319 |
| **FAQ data** (5 Q&A) | **284-294** | 269-279 |
| Price table | 265-283 | 250-268 |
| City link URL | 259-264 | 244-249 |
| **ItemList and FAQPage JSON-LD** (`class="nlcp-schema"`) | **355-374** | 340-359 |
| Healthcheck marker `catalog_plus` | 578 | 563 |
| City price page helper `nadlan_cp_price_page()` | 1-12 | not in mirror |

Notes on the snippet:
- The output buffer runs on `template_redirect` priority 1 and anchors on:
  - `<div class="nldir-pills">` … `</header>` for the search bar and map thumbnail;
  - `<aside class="nldir-side">` for the price map;
  - `<script id="nldir-js">` for the body copy;
  - `</body>` for the assets, the map shell and the schema.
- It also swaps `data-rest` to `projects-plus`.
- In the card facts, "שנת תוקף התוכנית" applies to renewal plans; "אכלוס משוער" applies only to years 2024-2040.
- The city link URL uses a `city/<slug>/projects` WP page when one exists, otherwise `/projects/?city=`. None exists, so all links fall back.
- `nadlan_cp_price_page()` maps 23 cities to `/<city>-apartment-prices/`. **The archive does not use it.**

**Other files that touch the archive:**

| Element | File:line |
|---|---|
| Sponsored slot (after card 6) | `inc/sponsored-spot.php:22-75` (`nadlan_ss_inject` on `nadlan_dir_cards_html`) |
| Facility chips on cards | `inc/facility-chips.php`, called from `directory.php:956-961` |
| Canonical of `?city=` views | `inc/city-hubs.php:142-147` (`wpseo_canonical`) |
| BreadcrumbList and Yoast pointer | `inc/breadcrumbs.php:51` (archive crumb) plus the 1.72.512 `nadlan_breadcrumbs_id()` / `wpseo_schema_webpage` |
| Body class `nlpc-project-archive` | `themes/nadlan-platform-child/functions.php:46-58` |
| Header (`nlhp-top` mega menu) | `inc/home-v3.php:184` and the `render_block` filter at 796-809 |
| Footer | `themes/nadlan-platform-child/parts/footer.html` |
| WhatsApp pill `#nlcta` | `inc/cta-start.php:26` (project and archive branch) |
| Legal notice | `inc/legal-notice.php` |
| CPT registration | `plugins/nadlan-config/nadlan-config.php:263-270`. The label `NadLan Projects` is the source of Yoast's og:title and CollectionPage name |
| Project meta registration | `inc/catalog-meta.php:68-108` |
| REST privacy (address and phone hidden) | `inc/rest-privacy.php:21-24` |
| Map pins REST `nadlan/v1/project-map` | `inc/drone-map.php:77` |

### 2.3 Injection points for an upgrade (code)

- **Snippet 661's output buffer** is the established "additive layer". It has four string anchors (listed above), it fails open, and turning the snippet off reverts it.
- **Filters:**
  - `nadlan_dir_cards_html` (cards HTML, server and REST);
  - `nadlan_cp_query_args` (extra meta_query);
  - `nadlan_geo_card_distance`;
  - `get_the_archive_title`;
  - `wpseo_metadesc`, `wpseo_canonical`, `wpseo_schema_webpage`;
  - `pre_get_document_title`: **do not touch (title freeze)**.
- **No shortcode or WP page is rendered on the archive.** An `[nadlan_tool id="…"]` printed into the archive would only show its static summary:
  - `inc/instruments.php:207-213` (`nadlan_nli_page_ids()`) looks only at `is_singular()` post content.
  - So the engine CSS and JS (223-237) and the `SoftwareApplication` JSON-LD (471-484) would not load.
  - Embedding live tools needs an archive hook in `instruments.php`, for example a filter on the page ids, or an explicit enqueue from the archive code.
  - The instrument JSON-LD can also add a second `FAQPage`; keep one per page.

---

## 3. Languages (raw + code)

| URL / item | Live status |
|---|---|
| `/en/projects/` | **404** (smart-404 page "העמוד הזה כבר לא כאן", `noindex, follow`, Hebrew) |
| `/fr/projects/` | **404** |
| `/ru/projects/` | **404** |
| `/ar/projects/` | **404** |
| `/en/projects-in-israel/` | 404 |
| hreflang on `/projects/` | none |
| `/en/`, `/fr/`, `/ru/`, `/ar/` homes | 200, with a full hreflang cluster (he, en, fr, ru, ar, x-default). Their "Projects in X", TAMA 38 and "evacuate-rebuild" links go to the **Hebrew** archive (`/projects/?city=<Hebrew>`, `?project_type=…`) |
| `/en/new-projects/` (and fr/ru/ar) | 200. The foreign-buyer guide family, with hreflang to `/new-projects/` (`inc/page-lang.php`) |
| Project language siblings | 60 posts: 15 projects x en/fr/ru/ar at `/projects/<slug>-<lang>/`. The 15 are hamedina, toha2-tel-aviv, the-park-bnei-brak, zohi, yoo, shikun-binui, recanati, park-bavli, meier, gindi-vogue, utopia, duo, dimri-yama, rainbow and ashira. hreflang comes from `inc/project-lang.php:102-105`. They are excluded from the catalog |

How language routing works:
- Language pages are WP pages under the `/en|fr|ru|ar/` root pages (`inc/page-lang.php:24-34`, `is_page()` only), or project slug suffixes (`inc/project-lang.php:33-45`).
- `inc/lang-pages.php:23-38` (the server-side dictionary translation) runs only on project language pages and on singular or front language pages. **It never runs on an archive.**
- So no language archive exists today. Building one means either new WP pages (for example `/en/projects/`) that render the catalog in a language mode, or a language mode of `nadlan_dir_project_page()`.
- The token `projects` is already held by `/projects/`, the `/new-projects/` family, `/herzliya-projects/` and `/sde-dov-luxury-projects-2026/` (`url_word_audit.py --token projects`). Check the URL word law before minting.

---

## 4. Data available to power tools on this page

### 4.1 Counts (rest)

- Published `nadlan_project`: **1,036** (`X-WP-Total`). That is 976 catalog posts plus 60 language siblings. The catalog count 976 is the facets total (`directory.php:990`; it excludes siblings and private unit journeys).
- Type, base 976:

  | Type | Projects |
  |---|---|
  | pinui_binui | 942 |
  | new_build | 19 |
  | tama38 | 5 |
  | blank | 4 |
  | `new` | 2 |
  | `משרדים ומסחר` (ToHa2, THE PARK) | 2 |
  | urban_renewal | 2 |

- Source: `urban_renewal` 947 (mavat import), `editorial` 10, other free-text sources 19.
- **78 distinct cities**:

  | City | Projects |
  |---|---|
  | ירושלים | 197 |
  | תל אביב יפו | 77 |
  | רמת גן | 76 |
  | חיפה | 44 |
  | נתניה | 40 |
  | בת ים | 37 |
  | פתח תקוה | 37 |
  | הרצליה | 25 |
  | חולון | 25 |
  | גבעתים | 24 |
  | חדרה | 21 |
  | ראשון לציון | 19 |
  | רמלה | 17 |
  | אשדוד | 17 |
  | קרית אונו | 17 |
  | נהריה | 15 |
  | יבנה | 15 |
  | **באר שבע** | **14** |
  | רחובות | 14 |
  | טירת כרמל | 14 |
  | לוד | 13 |
  | כפר סבא | 12 |
  | … | … |

  City strings are not uniform (for example `einstein-tower` has `תל אביב-יפו`).

### 4.2 Project meta fields and fill rate (code + rest; base 976 projects)

Meta is registered in `inc/catalog-meta.php:68-108` and is **exposed** in `/wp/v2/nadlan_project` (73 keys; `address` and `phone` are removed by rest-privacy).

| Field | Meaning | Filled | Share |
|---|---|---|---|
| `city` | city | 973 | 99% |
| `project_type` | type | 972 | 99% |
| `project_status` | status (17 raw values, see below) | 963 | 98% |
| `num_units` | housing units | 964 | 98% |
| `lat` / `lng` | coordinates | 962 | 98% |
| `source` (+ `source_url`, `source_id`) | provenance (mavat links for renewal) | 969 | 99% |
| `completion_year` | occupancy year, or plan-validity year on renewal | 548 | 56% (range 1968-2030; mostly 2019-2025, plan years, not occupancy) |
| `neighborhood` | neighbourhood | 22 | 2% |
| `developer_name` | developer | 25 | 2% (all 19 new-build have it) |
| `num_floors` | floors | 20 | 2% |
| `project_3d_avg_price_per_sqm` | developer's ₪/m² | 8 | 1% |
| `project_3d_units` | unit inventory JSON | 15 | 2% |
| `price_min` / `price_max` | price from / to | 2 / 1 | 0% (e.g. dimri-yama 3,750,000; rainbow 5,500,000) |
| `project_price_updated` | price date | 2 | 0% |
| `gush` | land registry block | 2 | 0% |
| `verified_at` | registrar check | **0** | 0% |
| `photos_csv` | photos | 0 | 0% (images are featured thumbnails) |
| Also registered | `contractor_name`, `architect_name`, `helka`, `num_buildings`, `website`, `video_url`, `tour3d_url`, the `project_*_json` blobs, `is_demo`, `reserved_slot`, `promo_until` | sparse | |

Not in the data at all: rooms per project, a structured delivery date for new-build, or sale-stage flags beyond `project_status`.

`project_status` values:

| Value | Projects |
|---|---|
| תכנית מאושרת לפני מימוש | 334 |
| תכנון סטטוטורי | 262 |
| תכנית מאושרת - אחרי רישוי | 176 |
| תכנון ראשוני | 115 |
| תכנית מאושרת במימוש | 54 |
| בשיווק | 5 |
| construction | 3 |
| בבנייה / בהקמה | 2 each |
| planning, בתכנון, בהיתר בנייה, permits, `2025` | 1 each |
| blank | 13 |

Some values are padded with about 250 trailing spaces.

### 4.3 Three live samples (rest, `?slug=…&_fields=id,slug,title,meta`)

| id | slug | title | Filled meta |
|---|---|---|---|
| 4893 | duo-tel-aviv | מגדלי DUO תל אביב - פרוייקט דואו אבן גבירול תל אביב | developer אפריקה ישראל מגורים, city תל אביב יפו, neighbourhood מתחם סומייל, new_build, 668 units, 54 floors, lat 32.085698 / lng 34.782856, source editorial (status, year and price all empty) |
| 4890 | yoo-tel-aviv | מגדלי YOO פארק צמרת - מגה יוקרה בעיצוב פיליפ סטארק | developer קבוצת חבס, תל אביב יפו, פארק צמרת, new_build, 300 units, lat/lng, editorial |
| 5589 | צאלים-האילנות | צאלים/האילנות | city יקנעם עילית, pinui_binui, status תכנון סטטוטורי, 210 units, source urban_renewal, source_url mavat …/2005450336/310, source_id 8001390 |

The default query (`?per_page=3`) returns the hamedina-ar, -ru and -fr siblings, with meta translated into each language.

### 4.4 Other data sources

**Live and server-side:**
- `uploads/nadlan-skin/deals-context-v1.json`. The live file is byte-identical to `tools/deals/deals-context-v1.json` (md5 `e5a1f395…`, generated 6.9.2026, 20 cities). Builder: `tools/deals/build_deals_context.py`.
  - Per city: `psqm_all`, `psqm_new`, `deals_24m`, `price_by_rooms` 3/4/5, `psqm_by_year`, and `streets`.
  - Periods differ by city. Jerusalem is **9.2022 to 9.2024**; TLV is 10.2023 to 10.2025.
- REST `nadlan/v1/project-map` (`inc/drone-map.php:77`): 962 pins with id, lat/lng, title, url, city, conf, units, psqm and status.
  - Location precision (`conf`): 512 compound-verified, 334 parcel-centroid-verified, 112 city-level.
  - Only 8 pins carry psqm.
- `uploads/nadlan-skin/tlv-neighborhoods-psqm.geojson` (TLV neighbourhood polygons with ₪/m², used by the full map; builder `tools/deals/build_tlv_neighborhoods.py`) and `project-surroundings-v1.json`.
- REST `nadlan/v1/pinkas`: the contractors register.

**`plugins/nadlan-config/assets/instruments/data/`:**

| File | What it holds |
|---|---|
| `value.json` | Tax Authority closed deals, medians by rooms per city and neighbourhood, quarter 1-3.2026, 23 cities with `yoy4` and the city price page path. **Newer than deals-context** |
| `ptax.json` | Purchase tax brackets, tracks |
| `boi-fx.json` | Bank of Israel representative rates |
| `boi-rate.json` | Bank of Israel rate and prime, as of 21.10.2026 |
| `cbs-200010.json` | Construction inputs index |
| `cbs-120010.json` | CPI |
| `cost.json` | Lawyer, broker, appraiser, LTV, VAT |
| `nrm.json` | Non-resident mortgage |
| `dira.json` | Discount-apartment lotteries, data.gov.il, updated 16.8.2026, 264 KB |
| `pinkas-meta.json` | Contractor register stats, 17.8.2026 |
| `arnona-tlv.json` | TLV arnona order 2026 |
| `condo.json` | Condo documents |
| `greece*.json` | Greece tools |
| `sde-dov-soil.json` | Sde Dov soil surveys |

**`plugins/nadlan-config/data/`:**
- `pinkas-register.php`: 17,874 registered contractors as of 17.8.2026; contractor number, branches, levels, cities.
- `register-facts.json`: contractor branches and levels as of 28.9.2026.

There is no neighbourhood data outside TLV, apart from the `value.json` neighbourhood medians.

### 4.5 Calculators and tools (`plugins/nadlan-config/assets/instruments/tools/`, embedded with `[nadlan_tool id="…"]`; registry in `inc/instruments.php:17-195`)

| id (file) | One line | Host page today | Fit for /projects/ |
|---|---|---|---|
| `indexation` | Construction-inputs index linkage of a developer apartment, payment by payment (Sale Law s.5ג) | `/new-projects/construction-input-index/` | high |
| `delay` | Compensation for late delivery of a new apartment (Sale Law s.5א) | `/new-projects/contractor-delay-compensation/` | high |
| `ptax` | Purchase tax, every track (2026 brackets) | `/purchase-tax-calculator/` | high |
| `pcost` | Total cash a buyer really needs (tax, fees, equity versus LTV cap) | `/apartment-purchase-cost-calculator/` | high |
| `afford` | Which home a household can buy (payment-to-income plus equity limits) | — | high |
| `pval` | What an apartment is worth: neighbourhood or city median by rooms (`value.json`) | — | high (city price context) |
| `prime` | The Bank of Israel rate in shekels on a prime track | — | medium |
| `cpi` | CPI linkage (amounts, linked rent) | `/cpi-calculator/` | low |
| `warranty` | Sale Law inspection and warranty clock from handover | — | medium |
| `pinkas` (`pinkas.js`) | Search the official contractors register | `/pinkas-hakablanim/` | high (the "check the contractor" step) |
| `sivug` (`pinkas.js`) | Contractor classification table: what each level may build | `/pinkas-hakablanim/` | medium |
| `dira` | Discount-apartment (מחיר למשתכן) lottery odds by city | `/dira-behanacha/` | medium (link, not embed) |
| `nrm` | Israeli mortgage for a buyer abroad (English) | — | for a language archive |
| `arnona` | TLV arnona 2026 | — | low |
| `condo`, `condomaj` (`condo.js`) | Condo documents and majority | lawyer pages | low |
| `soilmap`, `pfas`, `soilask` | Sde Dov soil map, lab reading, question letter | `/sde-dov/contamination/` | low (Sde Dov only) |
| `grbuy`, `grgv`, `gryield`, `grmap`, `grbudget`, `grisrael` | Greece | `/prices-greece/` | no |

Remember the archive caveat in 2.3: the tool assets load only on singular pages today.

---

## 5. Related pages that /projects/ should link to and must not cannibalise (raw, live 25.10)

| URL | `<title>` | H1 | hreflang | Links to /projects/ |
|---|---|---|---|---|
| `/new-projects/` | המדריך המלא לקנייה מקבלן ובדיקת פרויקט חדש \| נדלן | המדריך המלא לקנייה מקבלן: כך בודקים פרויקט חדש לפני שחותמים | he/en/fr/ru/ar/x-default | 3 |
| `/new-projects/new-projects-tel-aviv/` | פרויקטים חדשים בתל אביב: מחירים, אכלוס והשוואת דירה מקבלן \| nad-lan | פרויקטים חדשים בתל אביב: מחירים, אכלוס והשוואה לפני חתימה | — | 2 |
| `/new-projects/north-tel-aviv-new-projects/` | פרויקטים חדשים בצפון תל אביב: השוואת דירה מקבלן \| nad-lan | פרויקטים חדשים בצפון תל אביב: איך להשוות דירה מקבלן לפני חתימה | — | 2 |
| `/new-projects/presale-apartment/` | דירת פריסייל 2026: מחיר אמיתי ו-20/80 \| nad-lan | דירת פריסייל 2026: מחיר אמיתי, 20/80 ובדיקות לפני חתימה | — | 2 |
| `/new-projects/purchasing-group/` | קבוצת רכישה 2026: סיכונים, מיסוי והבדל מרכישה מקבלן | מהי קבוצת רכישה ולמה היא שונה מרכישה מקבלן | — | 2 |
| `/new-projects/construction-input-index/` | מדד תשומות הבנייה 2026: דירה מקבלן וחישוב הצמדה | מדד תשומות הבנייה 2026: דירה מקבלן, תיקון 9 וחישוב הצמדה (tool `indexation`) | — | 2 |
| `/new-projects/contractor-delay-compensation/` | איחור במסירת דירה מקבלן 2026: פיצוי לפי חוק המכר | איחור במסירת דירה מקבלן 2026: פיצוי, חוק המכר ומה עושים (tool `delay`) | — | 2 |
| `/herzliya-projects/` | פרויקטים חדשים בהרצליה והמרינה - על הנייר ויוקרה \| נדל״ן חכם | פרויקטים חדשים בהרצליה והמרינה - על הנייר, יוקרה ופיתוח | — | 2 |
| `/sde-dov/` | שדה דב: פרויקטים ודירות למכירה ברובע החדש \| המדריך המלא | רובע שדה דב: פרויקטים ודירות למכירה | full cluster | 2 |
| `/sde-dov/prices/` | מחירי דירות בשדה דב - מחיר למ״ר, טבלאות השוואה וסקירת שוק \| נדל"ן חכם | מחירי דירות בשדה דב | full cluster | 2 |
| `/sde-dov-luxury-projects-2026/` | רובע שדה דב: הריביירה החדשה של תל אביב יוצאת לדרך - נדלן | (same) | — | 2 |
| `/north-tel-aviv/` | צפון תל אביב - שכונות, פרויקטים ומחירים \| נדל״ן חכם | צפון תל אביב - מדריך האזור, השכונות, הפרויקטים והמחירים | full cluster | 2 |
| `/dira-behanacha/` | דירה בהנחה: הסיכוי לזכות בהגרלה בכל עיר, מהנתונים הרשמיים | דירה בהנחה: מה הסיכוי לזכות בהגרלה, בכל עיר (tool `dira`) | — | 2 |
| `/developer-deals/` | מבצעי קבלנים 2026: 20/80, 10/90, מכרזי דירות וההנחות שבאמת שוות כסף - נדלן | (same) | he/en/x-default | 2 |
| `/urban-renewal/` | התחדשות עירונית: המדריך המלא לבעלי דירות \| תמ״א 38 ופינוי בינוי \| נדלן | התחדשות עירונית: מה בודקים לפני שחותמים | — | 2 |
| `/urban-renewal/map/` | מפת התחדשות עירונית: פרויקטים ומתחמי פינוי בינוי לפי עיר \| נדלן | מפת ההתחדשות העירונית: כל פרויקטי פינוי בינוי בישראל | — | 2 |
| `/premium/` | הקטלוג הפרימיום - פרויקטים עם בחירת דירה בתלת ממד \| נדלן - נדלן | הקטלוג הפרימיום - פרויקטים עם בחירת דירה בתלת ממד | — | 2 |
| `/apartment-prices/` | מחירון הדירות של ישראל: כל הערים והמספרים במקום אחד | מחירון הדירות של ישראל | — | 2 |
| `/tel-aviv-apartment-prices/` (and 22 other `/<city>-apartment-prices/`) | מחירי דירות בתל אביב 2026: חציון לפי חדרים, עסקאות ומגמה \| נדלן | מחירי דירות בתל אביב לפי אזורים ושכונות | — | 2 |
| `/purchase-tax-calculator/` | מחשבון מס רכישה 2026: סימולטור לכל קונה ומדרגות המס | חישוב מס רכישה על דירה: מדרגות 2026, מסלולים ומועד תשלום (tool `ptax`) | — | 2 |
| `/mortgage-calculator/` | מחשבון משכנתא 2026: החזר חודשי, ריבית ותמהיל \| nad-lan | מחשבון משכנתא 2026: החזר חודשי ועלות כוללת | — | 2 |
| `/apartment-purchase-cost-calculator/` | מחשבון קניית דירה 2026: כל עלויות רכישת הדירה, גם מקבלן \| nad-lan | מחשבון קניית דירה: כמה כסף צריך באמת כדי לקנות דירה? (tool `pcost`) | — | 2 |
| `/pinkas-hakablanim/` | פנקס הקבלנים: בדיקת קבלן רשום לפי שם, מספר, עיר וסיווג | בדיקת קבלן רשום: חיפוש בכל הקבלנים בפנקס הרשמי (tools `pinkas`, `sivug`) | — | 2 |
| `/buying-apartment/` | קניית דירה בישראל 2026: בדיקות לפני חתימה \| nad-lan | קניית דירה בישראל: מדריך בדיקות לפני חתימה | — | 3 |
| `/buying-new-apartment-developer-2026-negotiation/` | קונים דירה מקבלן ב-2026? כללי המשא ומתן השתנו לטובתכם - נדלן | (same) | — | 3 |
| `/developers/` | ליזמים ולחברות בנייה - נדלן | שכבת שיווק דיגיטלית לפרויקטים שלכם (B2B) | — | 2 |
| `/city/<עיר>/projects/` | **410 Gone**; the old ghost hubs were deleted | — | — | — |

**What /projects/ links to today**, counting the whole page including header and footer (raw):

| Linked (count) | Not linked |
|---|---|
| `/urban-renewal/` (3), `/purchase-tax-calculator/` (2), `/apartment-purchase-cost-calculator/` (2), `/sde-dov/`, `/mortgage-calculator/`, `/apartment-prices/`, `/premium/`, `/tel-aviv-apartment-prices/`, `/new-projects/construction-input-index/` (1 each; mostly header or footer) | `/new-projects/`, `/new-projects/new-projects-tel-aviv/`, `/new-projects/presale-apartment/`, `/new-projects/north-tel-aviv-new-projects/`, `/new-projects/contractor-delay-compensation/`, `/herzliya-projects/`, `/north-tel-aviv/`, `/dira-behanacha/`, `/developer-deals/`, `/urban-renewal/map/`, `/pinkas-hakablanim/`, `/developers/` |

**Ownership and cannibalisation notes (gsc, 90 days):**
- `/projects/` already collects most head-term impressions:
  - `פרויקטים חדשים בתל אביב`: 588 on `/projects/` versus 97 on the dead TLV hub.
  - `פרויקטים חדשים בצפון הישן תל אביב`: 255.
  - `פרויקטים חדשים בתל אביב ליד הים`: 185.
- `/new-projects/new-projects-tel-aviv/` leads `פרויקטים חדשים למגורים` (185 versus 111 on `/projects/`). Keep TLV-specific copy there and link to it, rather than rewriting it into the hub.
- `/herzliya-projects/` owns `איזה פרויקטים חדשים יש בהרצליה` (160 versus 19 on `/projects/`).
- `/new-projects/` is the "how to buy from a developer" guide. `/projects/` is the catalog and comparison intent. Keep the hub's copy on the catalog and comparison side, and send the buying-process depth to the guide family.
- Note also that `/new-projects/north-tel-aviv-new-projects/` repeats "new" and "projects" in one URL. That is a pre-existing breach of the word law; it must not be renamed (no-redirect law).

---

## 6. Release pattern (code: `scripts/project-stage/make_deploy512.py`, `ashira_512.py`, `deploy512.py`)

1. **Build.** Edit the PHP file locally. A `make_deployNNN.py` script diffs git HEAD against the edit into minimal hunks, each anchored on enough unchanged lines to be unique. It writes `ashira_NNN.py` (`RELS` + `HUNKS` + `apply()`, which refuses any anchor that does not occur exactly once) and generates `deployNNN.py` from the previous runner: version strings, rollback targets, and the CHECKS list of URLs with `?tNNN=1` cache-busters plus must-contain and must-not-contain strings.
2. **Pre-flight.** `deployNNN.py` refuses to run if another release is in flight (`deploy-result-*.json`; one runner at a time, with lock lines in `docs/coordination/claude-codex.md`). It requires `/wp-json/nadlan/v1/health` to be ok. It creates a one-run token bridge (a temporary `x-` Code Snippet REST route). Through the bridge it reads the **live** file, applies the hunks to the live text, and lints the result with `php -l` locally and with `token_get_all` on the server. It saves live backups.
3. **Write.** Every file is put with an MD5 guard: the old md5 must match, and the new md5 is read back and verified. `.bakNNN` siblings are kept. The plugin `Version` and `NADLAN_CONFIG_VERSION` are bumped on the live text of `nadlan-config.php`. Then it purges: opcache, LiteSpeed purge-all and `wp_cache_flush`.
4. **Verify or roll back.** It waits until health reports the new version, then runs the page checks. On failure it purges and checks a second time. Any remaining failure restores every file from backup automatically. The bridge is deleted and swept in `finally`, and `docs/qa/…/deploy-result-NNN.json` is the record.
5. **For this page specifically:**
   - The H1, lead, grid and title live in the plugin (`inc/directory.php`) and go through steps 1-4.
   - The body copy, FAQ, schema, search bar and map live in **Code Snippets #661**. Change it with the `scripts/project-stage/edit_snippet_661*.py` pattern: read the live code (`snippet_read.py 661`), apply one exact anchor, run `php -l`, write an md5 backup JSON, `PUT /code-snippets/v1/snippets/661`, read it back, run live checks, and roll back automatically. The runners from deploy460 onward carry a snippet-661 restore in `rollback()`.
   - Alternatively, port the snippet into a plugin file in a planned release.
   - Around every release, run `python tools/source_audit.py` before and after (raw view-source snapshots) and `python tools/content_first_check.py`, and spot-check `/projects/rainbow-tel-aviv/` and `/projects/h-infinity-somail-tel-aviv/`.

---

## 7. Findings (report only: no redirect and no indexing change is proposed; those are the owner's calls)

**F1. Pagination duplicates.**
- `/projects/page/2/` serves the same 24 cards as page 1 (raw: identical card URL lists).
- It is self-canonical and `index`, with rel prev and next. `/page/41/` and `/page/42/` also answer 200.
- Cause: the renderer reads `$_GET['paged']` (`directory.php:1069`) and ignores the `/page/N/` query var. Yoast still prints `rel=next`.
- GSC shows no impressions on these URLs in 90 days.

**F2. og:title and schema name.**
- og:title and the Yoast `CollectionPage.name` are `ארכיון NadLan Projects - נדלן`, Yoast's archive default built from the CPT label at `nadlan-config.php:263-266`.
- The `<title>` is the custom one from `directory.php:1032`. Aligning the og or schema name would not touch `<title>`.

**F3. "18 cities" is wrong.**
- The prose says `ב־18 ערים` (snippet line 304). 18 is the facet cap (`LIMIT 18`, `directory.php:989`). The data has **78** cities.

**F4. A claim with no data behind it.**
- The prose says `הקטלוג מסמן פרויקטים שאומתו מול הרשם` (snippet line 308 / mirror 293).
- `verified_at` is empty on all 976 projects, and no card shows such a mark.

**F5. Be'er Sheva is missing.**
- Be'er Sheva has 14 projects but falls outside the 18-city cap. It is absent from the city select, the price map, the table and the city chips, although the prose names it.
- GSC, 90 days: `?city=באר שבע` had 590 impressions (position 35); `פרויקטים חדשים בבאר שבע` had 122 on `/projects/` plus 110 on the `?city=` view.

**F6. Stale price table with no links to the price pages.**
- The table and card context come from deals-context (generated 6.9.2026). Periods are mixed: Jerusalem 9.2022 to 9.2024, TLV 10.2023 to 10.2025.
- `value.json` already holds 1-3.2026 medians for 23 cities, and city price pages exist (`/<city>-apartment-prices/`).
- The table links only to `/projects/?city=`. No `city/<slug>/projects` page exists, so `nadlan_cp_city_hub_url()` falls back.

**F7. Stray `</a>`.**
- A stray `</a>` closes the grid in both the server HTML and the REST HTML (51 closes against 50 opens).
- Cause: `inc/sponsored-spot.php:61-68` explodes on `</a>` and re-appends `</a>` to the trailing `"\n"` part.

**F8. Heading hierarchy.**
- H1 is followed by the sidebar H4s ("מפת מחירים", "ערים מובילות"), then the card H3s, then the prose H2s. There is no H2 above the grid.

**F9. Catalog make-up.**
- 96.5% of the catalog (942 of 976) is pinui-binui compounds in planning. Page 1 is curated new-build.
- Two office projects (ToHa2, THE PARK, type `משרדים ומסחר`) sit in a residential "דירות מקבלן" catalog. Their type badge is suppressed as "אחר".

**F10. Loose status data.**
- `project_status` has 17 raw values; some are padded with spaces, some are English keys, one is a year.
- The "בשיווק" filter returns 5 projects, all in Sde Dov.
- The "בבנייה" group also matches `במימוש`, which means a plan in implementation (snippet status groups at lines 87-97).
- `completion_year` on renewal projects is the plan-validity year, not occupancy.

**F11. No links to the sibling pages.**
- `/projects/` has no in-body links to the `/new-projects/` family, `/herzliya-projects/`, `/north-tel-aviv/`, `/developer-deals/`, `/dira-behanacha/`, `/urban-renewal/map/`, the city price pages or `/pinkas-hakablanim/` (see the table in section 5).
- `/new-projects/` links to `/projects/` three times.

**F12. Dead city hubs still get impressions.**
- The old `/city/<עיר>/projects/` URLs answer **410** but still drew GSC impressions in the last 90 days:

  | Old hub | Impressions |
  |---|---|
  | תל אביב יפו | 1,070 |
  | ראשון לציון | 731 |
  | אשקלון | 432 |
  | קרית אונו | 399 |
  | הרצליה | 352 |
  | רמת גן (two spellings) | 338 + 297 |
  | חיפה | 326 |
  | בת ים | 322 |
  | כפר סבא | 253 |

- City-level demand ("פרויקטים חדשים ב<עיר>") currently has no living owner page except `/projects/` and its `?city=` views, which are canonical to `/projects/`.

**F13. Duplicate filter controls.**
- The source holds a hidden legacy `.nldir-search` form plus the pills plus the `#nlcp-bar` form, so two inputs are named `q` and two are named `city`.
- The sidebar city buttons are JS buttons, not crawlable links.

**F14. The grid starts low on phones.**
- On the phone the first card is at **1,365px** (about 1.7 screens). Above it are the lead, the intro, the pills, a 353px search bar and a 300px map thumbnail. On desktop the first card is at 883px.
- The sidebar (price map, top cities) drops below all 24 cards on the phone, at 15,024px.

**F15. Instruments do not load on the archive.**
- They load only on singular pages (`inc/instruments.php:207-213`). Embedding a live calculator on `/projects/` needs a code change there first. See 2.3.

**F16. Repo drift.**
- `inc/catalog-plus.php` and `inc/catalog-plus-map.php` are 6.9 mirrors. The live snippet 661 is newer.
- The repo plugin header reads 1.72.372 while live is 1.72.512.
- Always build hunks on the **live** text: snippet via `snippet_read.py`, plugin files via the deploy bridge read.

**F17. Mapbox token in the HTML.**
- The static map URL carries the public `pk.` token. It is public by design, but it is exposed in the HTML; restrict it by URL in the Mapbox account if not already done.
