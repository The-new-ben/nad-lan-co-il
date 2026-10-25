# /projects/ in en, fr, ru, ar: what exists, what Google does today, the safe plan

Read-only research, 25.10.2026, Opus 5.5 sub-agent. Nothing on the live site was changed. GSC was read only (no sitemap
submit, no URL inspection request, no indexing request).

Sources: the plugin code (`plugins/nadlan-config/inc/page-lang.php`, `project-lang.php`, `lang-pages.php`, `i18n.php`,
`directory.php`, `city-hubs.php`, `projects-hub.php`), the live Yoast sitemaps and the public REST page list (fetched
about 08:45 to 09:00 UTC, 10:45 to 11:00 Israel time), raw HTML of every page quoted below (same window), Search Console
query+page export for 25.7 to 23.10.2026, `tools/gsc/url_word_audit.py`, and the earlier package
`docs/content/new-projects-2026-08-07/` (intent map and hreflang map of the buyer guide family).

Scratch evidence (not in the repo): `C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\`
holds `gsc_qp.csv`, `gsc_page.csv`, `gsc_q.csv`, `probe1.json`, `sitemap_lang.json`, `rest_lang_pages.json`, `uwa_*.txt`.

---

## 0. Live-site alarm found during this research

From about 09:02 UTC (11:02 Israel) every URL on nad-lan.co.il returns **HTTP 500, the WordPress "critical error"
page**: `/`, `/projects/`, `/sitemap_index.xml`, `/wp-json/nadlan/v1/health`. Still 500 at 09:08 UTC. The page probes in
this report were taken before that (all 200 at the time). The timing matches the open
`RELEASE LOCK 1.72.513 (ProjectsHub ...)` in `docs/coordination/claude-codex.md` (another session, "Ashira session")
and the local `inc/projects-hub.php` saved at 11:01. This agent did not touch the site. It needs the releasing session or
the owner now.

---

## 1. Short answer

- **No language version of the catalog exists.** `/en/projects/`, `/fr/projects/`, `/ru/projects/`, `/ar/projects/`
  are 404 (Hebrew 404 page, `noindex, follow`). No other hidden catalog URL exists: the public REST list of every
  published child page under `/en/`, `/fr/`, `/ru/`, `/ar/` matches the sitemap one for one (44, 30, 30, 16 pages).
- **Google already sends foreign catalog searches to the Hebrew `/projects/`.** In 90 days about 840 English, Russian and French
  impressions with a catalog intent (plus 69 Italian and Portuguese) landed on the Hebrew catalog, at positions 55 to 78, with 0 clicks:
  "новостройки израиль" 213, "new projects israel" 167, "projet immobilier israël" 127, "new apartments israel" 101,
  "real estate developments in tel aviv" 60, "new apartments projects jerusalem israel 2026" 49,
  "off plan properties israel" 40. The language buyer guides (`/xx/new-projects/`) get almost none of it
  (`/ru/new-projects/` 13, `/en/new-projects/` 0).
- **So Google itself separates "catalog" from "buyer guide"** in every language, exactly as in Hebrew, where `/projects/`
  takes 1,220 impressions for "פרויקטים חדשים" and the Hebrew guide `/new-projects/` takes 0.
- **Safe URLs: `/en/projects/`, `/fr/projects/`, `/ru/projects/`, `/ar/projects/`**, as true translations of `/projects/`,
  in one hreflang cluster with `/projects/` (x-default = `/projects/`). They are the only slugs that are law-compliant
  and pair automatically. Any other slug (`/en/catalog/`, `/en/new-developments/`, `/ru/novostroyki/`) would be a new
  word set: a rival URL, or a head word another page already owns (`catalog` belongs to `/catalog/`).
- **Creating them is safe** if four conditions hold: a full, in-language translation of the hub (no Hebrew cards),
  two small code additions so the archive and the pages declare one cluster in both directions, titles that lead with
  the catalog intent (the guides stay "buyer guide"), and paced linking. Details and owner decisions are in sections 6 and 7.

---

## 2. How language URLs are built today (code)

| Shape | Where | Language set by | hreflang printed by | Notes |
|---|---|---|---|---|
| Language homes `/en/` `/fr/` `/ru/` `/ar/` | WP pages with slug = language code | `inc/i18n.php` (`wp` hook: slug in en/fr/ru/ar sets lang + `nadlan_is_lang_home`) | `inc/i18n.php` wp_head: he `/`, en, fr, ru, ar, x-default `/` | Body translated by the whole-string pass in `inc/lang-pages.php` |
| Pillar pages and guides `/xx/<path>/` | WP child pages under the language root page | `inc/page-lang.php` (top ancestor slug) | `inc/page-lang.php`: family key = page path minus the language prefix; members found with `get_page_by_path()` **as pages**; prints only if 2+ members **and the Hebrew member exists** | Used by `/xx/new-projects/`, `/xx/sde-dov/`, `/xx/north-tel-aviv/`, `/xx/guides/...` |
| Project pages `/projects/<slug>-en|fr|ru|ar/` | `nadlan_project` posts with a slug suffix | `inc/project-lang.php` | `inc/project-lang.php`: he = base slug, siblings by suffix, x-default he | 15 projects x 4 languages = 60 pages live |
| Query-string variants `?lang=en` | `/global/...`, `/site-map/`, `/my-rentals/`, `/urban-renewal/...` | each module | each module | Not used for the catalog: `/projects/?lang=en` returns the Hebrew page, canonical `/projects/` |

The catalog itself is **not a page**: `/projects/` is the `nadlan_project` post-type archive (`has_archive => 'projects'`
in `nadlan-config.php`), rendered by `nadlan_dir_project_page()` in `inc/directory.php` (template_redirect, then exit).
Its title is set there: "פרויקטים חדשים בישראל | דירות מקבלן לפי עיר ויזם | נדלן". Language siblings are excluded from the
catalog grid on purpose (`nadlan_no_lang_siblings`, owner audit 5.7.2026: they read as mixed-language duplicates).

Two technical consequences for the plan:

1. `/projects/` prints **no hreflang at all** today (checked in the raw HTML).
2. If `/en/projects/` were created as a child page today, `page-lang.php` would look for a Hebrew **page** at path
   `projects`, find none (it is an archive), and print **no cluster** on the new page either. Two small additions are
   needed (section 6.4).

---

## 3. Inventory of every language URL near "new projects" (live, before the outage)

### 3.1 Sitemap totals by language (Yoast, all child sitemaps)

| Language | URLs in sitemaps | Of which project pages `-xx` | Pages under `/xx/` |
|---|---|---|---|
| en | 60 | 15 | 45 (incl. 17 broker listing pages) |
| fr | 46 | 15 | 31 |
| ru | 46 | 15 | 31 |
| ar | 32 | 15 | 17 |

No `/xx/projects/` in any sitemap. Every published page found by REST is also in the sitemap (no orphans).

### 3.2 Pages about new projects, new apartments, buying from a developer, areas (status, title, H1, hreflang)

| URL | Status | Title | H1 | hreflang cluster |
|---|---|---|---|---|
| `/projects/` | 200 | פרויקטים חדשים בישראל \| דירות מקבלן לפי עיר ויזם \| נדלן | פרויקטים חדשים בישראל | **none** |
| `/new-projects/` | 200 | המדריך המלא לקנייה מקבלן ובדיקת פרויקט חדש \| נדלן | המדריך המלא לקנייה מקבלן: כך בודקים פרויקט חדש לפני שחותמים | he, en, fr, ru, ar, x-default = `/new-projects/` |
| `/en/new-projects/` | 200 | New-Build Projects in Israel: Foreign Buyer Guide | New-Build Projects in Israel: The Complete Foreign Buyer Guide | same 5 + x-default |
| `/fr/new-projects/` | 200 | Immobilier neuf en Israël : guide d'achat complet \| NadLan | Immobilier neuf en Israël : le guide complet pour acheter un appartement neuf | same |
| `/ru/new-projects/` | 200 | Новостройки в Израиле: полное руководство \| nad-lan | Новостройки в Израиле: как выбрать квартиру от застройщика | same |
| `/ar/new-projects/` | 200 | مشاريع سكنية جديدة في إسرائيل: دليل المشتري | مشاريع سكنية جديدة في إسرائيل: الدليل الكامل للمشتري | same |
| `/en/sde-dov/` | 200 | Sde Dov, Tel Aviv: New Projects, Prices and Apartments | Sde Dov, Tel Aviv: New Projects and Apartments for Sale | he `/sde-dov/` + en fr ru ar + x-default |
| `/fr/sde-dov/` | 200 | Sde Dov Tel Aviv : programmes neufs, prix et quartier | Sde Dov à Tel Aviv : programmes neufs et appartements à vendre | same |
| `/ru/sde-dov/` | 200 | Сде-Дов, Тель-Авив: новые проекты, цены и квартиры у моря | Сде-Дов в Тель-Авиве: новые проекты и квартиры на продажу | same |
| `/ar/sde-dov/` | 200 | Sde Dov, Tel Aviv: New Projects, Prices and Apartments (English title on the Arabic page) | same English H1 | same |
| `/en/north-tel-aviv/` (+ fr, ru, ar, + `rova-4/` children) | 200 | North Tel Aviv Real Estate: Neighborhoods, Projects, Prices | North Tel Aviv: Neighborhoods, New Projects and Apartment Prices | he `/north-tel-aviv/` + 4 + x-default |
| `/en/developer-deals/` | 200 | Israel Developer Deals 2026: 20/80, 10/90, Apartment Auctions ... \| NadLan | same | he `/developer-deals/` + en only + x-default |
| `/en/buy-property-in-israel/` | 200 | Buying Property in Israel from Abroad: A Family Home Guide | Buying a Family Home in Israel from Abroad | **none** (no Hebrew twin at `/buy-property-in-israel/`, it is 404) |
| `/en/guides/` (+ fr, ru, ar) | 200 | Buyer guides \| NadLan | Buyer guides | he `/guides/` + 4 + x-default |
| `/projects/hamedina-en/` | 200 | Kikar Hamedina Towers Tel Aviv: Prices, Deals, Map & 3D | Kikar Hamedina Towers, Tel Aviv | he + en fr ru ar + x-default (project cluster) |
| `/projects/hamedina-fr/` | 200 | Tours Kikar Hamedina à Tel Aviv : appartements, prix et 3D | Tours Kikar Hamedina, Tel Aviv | same |
| `/projects/hamedina-ru/` | 200 | Башни Кикар ха-Медина, Тель-Авив: цены, сделки, карта и 3D | Башни Кикар ха-Медина, Тель-Авив | same |
| `/projects/hamedina-ar/` | 200 | Kikar Hamedina Towers, Tel Aviv: Prices, Deals & 3D Map | Kikar Hamedina Towers, Tel Aviv | same |
| `/projects/rainbow-tel-aviv-en/` | 200 | Rainbow Tel Aviv \| Coastal Resort Living in Sde Dov \| NadLan | same | he + 4 + x-default |

All of these are self-canonical and `index, follow`. Projects that have all four language siblings (15): rainbow-tel-aviv,
utopia-sde-dov, gindi-vogue-sde-dov, meier-on-rothschild, park-bavli, recanati-residence, shikun-binui-sde-dov,
yoo-tel-aviv, zohi-sde-dov, the-park-bnei-brak, toha2-tel-aviv, duo-tel-aviv, hamedina, dimri-yama-sde-dov, ashira-sde-dov.

### 3.3 Probed and confirmed absent (404)

`/en/projects/`, `/fr/projects/`, `/ru/projects/`, `/ar/projects/`, `/projects-en/`, `/en/new-projects-israel/`,
`/en/new-developments/`, `/ru/novostroyki/`, `/en/catalog/`, `/en/projects-catalog/`, `/fr|ru|ar/buy-property-in-israel/`,
`/buy-property-in-israel/`, `/fr|ru|ar/developer-deals/`.

### 3.4 What the language homes link to for "projects" (raw HTML)

On `/en/`, `/fr/`, `/ru/`, `/ar/` (same pattern in all four):

- header "Projects" and "Choose a project" -> `/projects/` (Hebrew);
- "All projects", "New projects across Israel", "All new projects" -> `/projects/` (Hebrew);
- "Projects in Jerusalem / Tel Aviv-Yafo / Ramat Gan / Haifa / Netanya / Bat Yam / Petah Tikva / Herzliya / Holon /
  Givatayim" and the city tiles ("Jerusalem 197 projects", "Tel Aviv-Yafo 101 projects" ...) -> `/projects/?city=<Hebrew city>`
  (the Hebrew page);
- "New projects in Tel Aviv" -> `/new-projects/new-projects-tel-aviv/` (Hebrew);
- the three featured project cards -> the right language siblings (`/projects/hamedina-en/` etc.).

So about 25 links per home, with English, French, Russian or Arabic anchor text, point at the Hebrew catalog. These are the
natural first link slots for the language catalogs.

The language guides `/en/new-projects/` and `/ru/new-projects/` list eight projects that link to the **Hebrew** project
pages with **Hebrew** anchor text (for example "מגדלי DUO תל אביב - פרוייקט דואו אבן גבירול תל אביב" on the English
guide), although six of them have a sibling in the page language (duo, dimri-yama, ashira, rainbow, toha2, the-park).
This is an existing defect, independent of the catalog.

### 3.5 hreflang clusters declared today

| Cluster | Members |
|---|---|
| Homes | `/` `/en/` `/fr/` `/ru/` `/ar/`, x-default `/` |
| Buyer guide | `/new-projects/` + `/en|fr|ru|ar/new-projects/`, x-default `/new-projects/` |
| Areas | `/sde-dov/`, `/north-tel-aviv/`, `/guides/` and children, each with its 4 language twins |
| Projects | each of the 15 projects with its 4 suffix siblings |
| Developer deals | `/developer-deals/` + `/en/developer-deals/` |
| **Catalog** | **does not exist** (`/projects/` declares nothing) |

---

## 4. Search Console (sc-domain:nad-lan.co.il, 25.7 to 23.10.2026, read only)

Export: 9,599 query+page rows (Google hides rare queries, so real totals are higher). Foreign-script queries: Latin
5,023 impressions (26 clicks), Cyrillic 462 (0 clicks), **Arabic script 6 (0 clicks)**.

### 4.1 Catalog-intent demand by language, and where it lands today

Filter: queries about new projects / new apartments / developments / off-plan, excluding "how to buy", "foreigner",
"invest" and finance questions (those belong to guides).

| Language | Impressions | Landing on Hebrew `/projects/` | Landing elsewhere |
|---|---|---|---|
| English | 502 | **472** | `/` 16, `/urban-renewal/english-guide/` 5, `/en/` 3 |
| Russian | 258 | **232** | `/ru/new-projects/` 13, `/ru/` 11 |
| French | 301 | **133** | `/fr/` 139, `/site-map/` 18, `/premium/` 9 |
| Italian | 120 | 48 | **`/ar/` 72** |
| Portuguese | 60 | 21 | `/ar/` 29, `/` 10 |
| Arabic | 0 | 0 | 0 |

### 4.2 The queries (all 0 clicks)

| Query | Impr. | Avg pos. | Pages (impressions, position) |
|---|---|---|---|
| новостройки израиль | 222 | 69.7 | `/projects/` 213 @71.1, `/ru/new-projects/` 5 @18.2, `/ru/` 4 @58 |
| projet immobilier israël | 184 | 73.2 | `/projects/` 127 @75.6, `/fr/` 29 @46.6, `/site-map/` 18, `/premium/` 9 |
| new projects israel | 170 | 76.6 | `/projects/` 167 @77.3, `/en/` 2 @8.0 |
| new apartments israel | 101 | 78.6 | `/projects/` 101 |
| nuove costruzioni israele | 103 | | `/ar/` 60 @58.9, `/projects/` 43 @50.9 |
| appartement neuf israël | 89 | 37.4 | `/fr/` 89 |
| real estate developments in tel aviv | 68 | 61.3 | `/projects/` 60 @59.9, `/` 6 |
| lançamentos imobiliários israel | 60 | | `/ar/` 29 @43.5, `/projects/` 21 @34.7, `/` 10 |
| new apartments projects jerusalem israel 2026 | 49 | 54.8 | `/projects/` 49 |
| off plan properties israel | 44 | 79.1 | `/projects/` 40, `/` 3, `/en/` 1 |
| купить новостройку в израиле | 32 | 60.3 | `/projects/` 19 @65.2, `/ru/new-projects/` 8 @34.6, `/ru/` 3 |
| new projects | 24 | 62.3 | `/projects/` 24 |
| programme neuf israël | 21 | 52.6 | `/fr/` 21 |
| tel aviv real estate developments | 19 | 75.2 | `/projects/` 13, `/` 5 |
| nuovi progetti immobiliari israele | 17 | | `/ar/` 12, `/projects/` 5 |
| property developments israel | 7 | 62.9 | `/projects/` 7 |
| programme neuf tel aviv | 4 | 59.5 | `/projects/` 4 |
| new projects tel aviv / projects in tel aviv / new development israel / new building projects in jerusalem | 1 to 3 each | 47 to 81 | `/projects/` |

Guide-intent queries go to guides, not to the catalog: "buying apartment in israel from usa / uk / abroad" 153 and
"how to buy an apartment in israel" 131 land on `/en/buy-property-in-israel/`; "buying property in israel as a foreigner"
35 on `/buy-property-israel-foreign-buyers/`; "israel investment property for americans" 84 on
`/buying-real-estate-israel-foreign-investor/`. Brand searches go to the right sibling: "kikar hamedina towers" 26
(`/projects/hamedina-en/` 14 @17.3), "rainbow building tel aviv" (`-en` @11.7), "yoo tower tel aviv" (`-en` @11.0).

### 4.3 Hebrew control: the same split already works

| Query | `/projects/` | Hebrew guide `/new-projects/` |
|---|---|---|
| פרויקטים חדשים | 1,220 impr. @32.5 | 0 |
| פרויקטים חדשים בישראל | 212 @27.2 | 0 |
| דירות מקבלן | 529 @29.9 | 0 |
| דירות חדשות מקבלן | 351 @50.2 | 0 |

Page totals in the period: `/projects/` 24,474 impressions, 7 clicks, position 44.0; `/new-projects/` 171 impressions,
position 13.2.

### 4.4 The existing language pages (page totals, 90 days)

| Page | Clicks | Impr. | Pos. |
|---|---|---|---|
| `/en/` | 23 | 1,361 | 10.9 (mostly brand: "madlan" 151, "nadlan israel" 51, "nadlan" 45) |
| `/ru/` | 16 | 522 | 30.9 |
| `/fr/` | 14 | 369 | 23.2 (incl. "appartement neuf israël" 89, "projet immobilier israël" 29, "programme neuf israël" 21) |
| `/ar/` | 0 | 237 | 43.6 (Italian/Portuguese new-build queries and Hebrew brand typos, no Arabic queries) |
| `/en/buy-property-in-israel/` | 1 | 735 | 58.1 |
| `/en/new-projects/` | 0 | 74 | 6.5 (one visible query: "build a home in israel from abroad") |
| `/ru/new-projects/` | 1 | 32 | 16.8 |
| `/fr/new-projects/` | 0 | 3 | 54.3 |
| `/ar/new-projects/` | 0 | 4 | 8.8 |
| `/en/sde-dov/` | 0 | 36 | 7.7 |
| Project siblings, best: `/projects/rainbow-tel-aviv-en/` 5 / 290, `/projects/duo-tel-aviv-en/` 3 / 230, `/projects/ashira-sde-dov-en/` 5 / 217, `/projects/toha2-tel-aviv-en/` 2 / 136, `/projects/gindi-vogue-sde-dov-en/` 8 / 80 | | | |
| Language totals (all language URLs) | en 60 clicks / 5,118 impr. (59 pages); ru 28 / 965 (37); fr 27 / 626 (34); ar 1 / 363 (23) | | |

Reading: the guides are not competing for the catalog head terms today; Google gives that intent to the Hebrew catalog and
cannot rank a Hebrew page well for an English or Russian searcher. A language catalog in the same hreflang cluster is the
page Google is missing.

---

## 5. URL word law (tool runs, 25.10.2026, 4,595 live URLs)

| Token | URLs holding it | What it means |
|---|---|---|
| `projects` | 1,050 | Owned by `/projects/` (and every `/projects/<slug>/`); also in the `/new-projects/` family, `/herzliya-projects/`, `/sde-dov-luxury-projects-2026/` |
| `new` | 62 | The `/new-projects/` family and the guides (`/guides/new-apartment-*`, `/guides/new-project-*`) |
| `catalog` | 1 | `/catalog/` (the 3D catalog): **taken** |
| `en` (and fr, ru, ar) | 0 | The tool's stop list removes language codes: a language prefix is **not a word** |
| `novostroyki`, `developments`, `projets`, `proekty`, `mashari` | 0 | Free, but see below |
| `new-projects` | n/a | The tool splits on hyphens, so this is the two tokens above. (The last runs also failed on HTTP 500 when the site went down.) |

How the law reads for a translation of the same page:

- `/en/projects/` has the token set {projects}: the **same set as `/projects/`**, with no word repeated inside the URL.
  The site already treats `/<lang>/<same path>/` as the same page in another language: `page-lang.php` builds the family
  by stripping the prefix, and `/en/new-projects/`, `/en/sde-dov/`, `/en/guides/<x>/` all mirror their Hebrew paths. Under
  that reading `/xx/projects/` is the owner of "projects" speaking another language, not a new owner.
- Any other slug is a **new word set**: `/en/catalog/` collides with `/catalog/`; `/en/new-developments/` or
  `/ru/novostroyki/` are free words but would be fresh URLs with no Hebrew twin, unpaired by the code, and in practice
  rivals of both `/projects/` and `/xx/new-projects/`. Not recommended.
- The owner should confirm this reading once (section 7), because the law's wording ("a new URL never re-uses a head word an
  existing URL already owns") could be read literally against `/en/projects/`.

---

## 6. The safe plan

### 6.1 URLs and clusters

| Language | Catalog (new) | Buyer guide (exists) |
|---|---|---|
| he | `/projects/` (archive, untouched title) | `/new-projects/` |
| en | `/en/projects/` | `/en/new-projects/` |
| fr | `/fr/projects/` | `/fr/new-projects/` |
| ru | `/ru/projects/` | `/ru/new-projects/` |
| ar | `/ar/projects/` | `/ar/new-projects/` |

Two separate hreflang clusters, never mixed:

- Catalog cluster: he `/projects/`, en, fr, ru, ar, **x-default `/projects/`** (every other cluster on the site uses Hebrew
  as x-default; keep it consistent).
- Guide cluster: unchanged.

Each language pair mirrors the Hebrew pair that GSC shows already works (catalog takes the head term, guide takes "how to
buy"). That is what makes the two pages strengthen each other instead of competing.

### 6.2 Intent split and titles (drafts, to be finalised after the per-language SERP read in 6.6)

| Language | Catalog title (mirrors the Hebrew title) | Catalog H1 | GSC phrases to carry in title, H1, lead and section heads | Guide stays |
|---|---|---|---|---|
| en | New Projects in Israel \| New Apartments by City and Developer \| NadLan | New Projects in Israel | new projects israel, new apartments israel, real estate developments in tel aviv, new apartments projects jerusalem, off plan properties israel, property developments israel | "New-Build ... Foreign Buyer Guide" |
| fr | Projets immobiliers neufs en Israël \| Appartements neufs par ville et promoteur \| NadLan | Projets immobiliers neufs en Israël | projet immobilier israël, appartement neuf israël, programme neuf israël, programme neuf tel aviv | "Immobilier neuf en Israël : guide d'achat complet" |
| ru | Новостройки в Израиле \| Проекты по городам и застройщикам \| NadLan | Новостройки в Израиле: все проекты | новостройки израиль, купить новостройку в израиле, квартиры от застройщика | "Новостройки в Израиле: полное руководство" (overlap, see 6.7) |
| ar | مشاريع جديدة في إسرائيل \| شقق من المقاول حسب المدينة والمطوّر \| NadLan | مشاريع جديدة في إسرائيل | no Arabic demand in GSC; vocabulary from the 7.8 intent map: مشاريع سكنية جديدة في إسرائيل، شقق جديدة للبيع، شقق من المقاول | "مشاريع سكنية جديدة في إسرائيل: دليل المشتري" (overlap) |

Cross-links (contextual, with intent-specific anchors):

- catalog -> guide, once in the lead and once in the "what to check before you sign" section: anchor in the "buyer guide /
  how to check a project" sense.
- guide -> catalog: anchor in the "all new projects in Israel by city and developer" sense; replace the guide's eight
  Hebrew-anchored links to Hebrew project pages with the language siblings and one catalog link.
- catalog -> the 15 project siblings in its language (cards), `/xx/sde-dov/` and `/xx/north-tel-aviv/` from the Tel Aviv
  section, `/xx/guides/` from the guides section; en only: `/en/developer-deals/` (payments section) and
  `/en/buy-property-in-israel/` (foreign-buyer question).
- back-links: language home "All new projects / New projects across Israel" -> `/xx/projects/`; the home's city links
  -> `/xx/projects/#<city>` (fragment, no new URLs); `/xx/sde-dov/`, `/xx/north-tel-aviv/` -> `/xx/projects/`.

### 6.3 What each language catalog must contain

- A real translation of the Hebrew hub, same sections as `/projects/` (from `inc/projects-hub.php`): projects in marketing
  with prices and payment terms; new projects in Tel Aviv; new-apartment prices by city (Tax Authority medians,
  `assets/instruments/data/value.json`); what is in the catalog; from permit to keys; how payment works (schedule,
  index linkage, 20/80); calculators; what to check before signing; new build vs urban renewal vs TAMA 38 vs presale; the
  market in numbers; projects by city; guides; FAQ; official sources. Same numbers, same dates.
- The same catalog data, in the page language: the 15 projects with full translated pages as cards linking to their
  siblings; the "in marketing" table from `data/projects-market.json` (566 projects; names stay as the developer
  publishes them, many already in Latin letters; cities and developers through the name dictionary); per-city counts with
  translated city names. Unknown names are shown as published, never as Hebrew strings in the language UI. A project
  without a language page links to its Hebrew page and says so ("page in Hebrew").
- Language-specific search phrases from section 4.2 in title, H1, lead and headings (not stuffed).
- Correct `lang` and `dir` (ar = rtl), self-canonical, Yoast meta description in the language, ItemList/FAQ schema in the
  language, breadcrumb Home (`/xx/`) > Projects.
- Note for the build: `inc/lang-pages.php` keeps the body (`entry-content`) of a non-project language page untouched, so
  the catalog body must be rendered in the language by its own code; the dictionary pass will only translate the chrome.
- One URL per language: no `/xx/projects/page/2/`, filters by script on the same page, parameters canonical to the clean URL.

### 6.4 Code needed (small, additive, not done here)

1. `inc/page-lang.php`, family builder: when the family key is `projects`, the Hebrew member is
   `get_post_type_archive_link( 'nadlan_project' )` instead of a page lookup (today the lookup returns nothing and no
   cluster would print).
2. A wp_head emitter on `is_post_type_archive( 'nadlan_project' )` (first page, no filters) that prints the same cluster,
   so the return tags exist on `/projects/` too. Same transient and the same "published members only" rule.
3. A render path for the four pages (shortcode or a template hook on those paths) that reuses the hub's data functions;
   the archive hooks (`nadlan_cp_is_catalog()`, `projects-hub.php` filters) key on the archive and do not run on a page.
   Touch the Hebrew hub's code as little as possible.

### 6.5 Canonical, sitemap, indexing

- Every catalog self-canonical. No cross-language canonical. `/projects/` stays self-canonical, title untouched.
- Sitemap: Yoast adds published pages to `page-sitemap.xml` by itself; nothing to change. After release, a passive resubmit
  of the existing sitemap is allowed; **no "Request indexing"** (owner law 22.10; ignore step 8 of the 7.8 publishing
  sequence, which predates that law).
- The pages go live indexable (no noindex without the owner's order), so they must be complete on the day they are
  published: QA in a private preview first, publish only finished pages.

### 6.6 Before the brief (owner research law 3.10)

Per language: declare the 1 to 5 owned intents (drafts in 6.2), read the top 4 or 5 catalog competitors in full by hand
(for example immobilier.co.il, shukshuk.co.il/en/projects, israrealty.co.il/ru, immoneuf.co.il, developer catalog pages),
record related questions and whether an AI answer is shown. The 7.8.2026 intent map is 2.5 months old and was written for
the guides, not for a catalog. The translated hub copy is long-form text: under constitution law 8 it goes to the owner's
ChatGPT as a prompt, not written by an agent. Layout: Claude Design first (design-first law), LTR mirror plus Arabic RTL.

### 6.7 Risks and how each is handled

| Risk | Evidence | Handling |
|---|---|---|
| Catalog vs buyer guide cannibalisation | Today the guides get almost no catalog-intent impressions (EN 0, RU 13 of 258); Hebrew split proven (1,220 vs 0) | Mirror the Hebrew pair; catalog titles lead with inventory words, guides keep "guide"; two separate clusters; intent-specific anchors |
| Exact title overlap in RU and AR | RU guide title starts "Новостройки в Израиле"; AR guide "مشاريع سكنية جديدة في إسرائيل" | Ship the catalog as above; watch GSC per query for 4 to 6 weeks; if both pages show for the same query, narrow the guide title toward "how to buy" (owner's word, it is a published page) |
| Language homes overlap | `/fr/` already ranks @37 for "appartement neuf israël" and its title is "Appartements neufs et projets immobiliers en Israël"; `/ru/` title "Новостройки и квартиры в Израиле" | Home links prominently to the catalog; home titles unchanged now. Hebrew precedent: `/projects/` 1,220 vs `/` 42 for "פרויקטים חדשים" |
| Thin or mixed-language page | ~980 Hebrew catalog projects, only 15 translated; owner audit 5.7 on garbled mixed cards | Full translated hub + in-language data; never Hebrew strings in the language UI; Hebrew-only projects labelled |
| Broken or one-way hreflang | `/projects/` declares nothing; `page-lang.php` cannot pair an archive | The two hunks in 6.4; verify both directions in raw HTML of all five URLs |
| URL word law reading | `/en/projects/` shares {projects} with `/projects/` | Owner confirms the "translation = same owner" reading; no other slug |
| Mass change in one day | Header "Projects" link and sibling breadcrumbs sit on ~140 language pages | Day 1: four pages, the two hunks, links from the four homes and four guides only. Later days, one language at a time: header nav on language pages, then the 15 siblings' "All new projects" and breadcrumb |
| Arabic has no demand | 6 Arabic-script impressions site-wide in 90 days; `/ar/` receives Italian and Portuguese queries | Build `/ar/projects/` for a complete cluster at the same quality, expect little traffic; or publish en, ru, fr first and ar later (owner's choice) |
| Shared hub code mid-release | Site down at the time of writing during release 1.72.513 | Build the language path after 1.72.513 is stable; reuse its data functions, do not fork the Hebrew hub |

### 6.8 Verdict

Safe to create, with `/en/projects/`, `/fr/projects/`, `/ru/projects/`, `/ar/projects/` and only those, as full translations
in one cluster with `/projects/`. It removes no page, changes no existing slug, needs no redirect, no noindex and no
indexing request. It gives Google a native-language page for searches it already sends to the Hebrew catalog (about 840
English, Russian and French impressions in 90 days at positions 55 to 78, 0 clicks). No ranking is promised.

---

## 7. What the owner must approve

1. The URL reading: `/xx/projects/` is the translation of `/projects/`, the same owner of "projects" in another
   language (yes / no).
2. Which languages and when: recommended en, ru, fr first (they have the demand), ar the same day or later.
3. The day-1 scope (four pages, the two hreflang hunks, links from the four homes and the four guides), and that the header
   link and project-sibling links move later, one language per day.
4. The translation route for the hub copy: prompts to his ChatGPT (law 8), after the per-language SERP read.
5. Later, only if GSC shows overlap: narrowing the titles of `/ru/new-projects/` and `/ar/new-projects/` toward "buyer guide".

Side findings to log (not part of this change): `/en/new-projects/` and `/ru/new-projects/` link to Hebrew project pages
with Hebrew anchors although language siblings exist; the language homes link city tiles to the Hebrew catalog with
Hebrew query strings; `/ar/sde-dov/` serves an English <title> and H1, and the WordPress titles of `/ar/north-tel-aviv/`, `/ar/north-tel-aviv/rova-4/` and `/ar/sde-dov/prices/` are English too; Italian and
Portuguese new-build searches (180 impressions) land on `/ar/`.
