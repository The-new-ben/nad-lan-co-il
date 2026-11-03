# Garden apartments in Tel Aviv: what nad-lan.co.il already has

**Checked on 2026-11-03. Read-only; nothing was changed.**

## 1. Search Console

**Pull:** `gsc_api.py query --site sc-domain:nad-lan.co.il --start 2026-08-03 --end 2026-11-02 --dimensions query,page`. It returned 9,817 query-and-page rows, with 99,851 impressions and 128 clicks in those rows. Rows with anonymised queries are not included in a query-level pull, so these totals are lower than the property's real totals.

The raw file is `scratchpad/garden/gsc_qp.csv`. I filtered rows whose query contains "גן", "garden", "גינ" or "חצר".

| Group | Rows | Distinct queries | Impressions | Clicks |
|---|---|---|---|---|
| **Garden-apartment intent (דירת גן / דירות גן / garden)** | **0** | **0** | **0** | **0** |
| Ramat Gan, the city (kept separate) | 144 | 106 | 1,126 | 1 |
| עוגן / עוגני קרקע (glossary, engineering) | 8 | 7 | 312 | 0 |
| דיור מוגן (assisted living, Migdalei HaYam) | 25 | 25 | 109 | 0 |
| Project and place names containing גן, גינה or חצר | 18 | 16 | 68 | 0 |
| גינדי (the developer) | 15 | 10 | 47 | 0 |
| Gan Yavne, the city | 8 | 7 | 29 | 0 |

**The site has no Search Console presence for any garden-apartment query.** No page ranks, not even on page 9.

Project and place names in the list:

| Query | Our page | Impressions | Position |
|---|---|---|---|
| מחירון דקל גינון | /glossary/מחירון-דקל-לבנייה-ותשתיות/ | 40 | 22.8 |
| גן ריינבו תל אביב | /projects/rainbow-tel-aviv/ | 4 | 19 |
| שמשיה לגינה מרכזית מול צדית מה עדיף ולמה? | /sde-dov/parks/ | 3 | 8.7 |
| חצר אנג'לו יפו, and חצר אנג'לו | /projects/ and /properties/ | 3, 1 and 1 | 53 to 93 |
| גינת בילטמור | /projects/ | 1 | 55 |
| ישגב על הגן | /projects/ | 1 | 63 |
| גינות דוד, and גינות דוד בני ברק | /projects/ | 1 and 1 | 47 and 76 |
| איפה יש דירות חדשות בנווה אביבים קרוב לגן צורי? | /projects/ashdar-einstein/ | 1 | 4 |
| דמרי נווה גן, פרויקט נווה גן בני ברק, נווה מגן החדשה | /projects/ | 1 to 3 | 40 to 67 |

Ramat Gan city queries are listed separately because they are not garden intent. The pages that take them:

| Page | Impressions |
|---|---|
| /city/רמת גן/projects/ | 336 |
| /city/רמת-גן/projects/ | 297 |
| /projects/ | 210 |
| /city/רמת-גן/ | 119 |
| /ramat-gan-apartment-prices/ | 35 |
| /projects/הגפן-8-10-רג/ | 32 (the only click) |

**Finding, reported only:** two URL spellings of the Ramat Gan projects page, with a space and with a hyphen, both get impressions for the same query. For "פרויקטים חדשים ברמת גן" that is 150 impressions at position 28.3 against 149 at 21.3. Two URLs on one query is cannibalisation. It is reported as found; how to handle it is Ben's decision.

**Related context in the same pull:** queries containing ממד or ממ"ד have 8 rows and 25 impressions, none about garden flats. Queries containing פנטהאוז have 2 rows and 9 impressions. Queries containing קרקע (66 rows, 951 impressions) are about land zoning (ייעוד קרקע), soil anchors, land lawyers and Sde Dov plots, not ground-floor flats.

## 2. URL ownership (`tools/gsc/url_word_audit.py --token`)

The tool reads the live sitemap (4,649 URLs) and splits each path on `/ - _ . +`.

| Token | URLs | Who holds it |
|---|---|---|
| garden | 4 | /global/project/garden-residence-jvc-dubai/, /global/project/bang-tao-garden-villas-phuket/, /global/project/porta-romana-garden-milan/, /properties/baka-jlm-garden-4r-demo/. All are project names or a demo listing; **no hub owns "garden"** |
| gardens | 1 | /global/project/sky-gardens-jvc-dubai/ (a project name) |
| gina, ginat, ganim, yard | 0 | |
| gan | 8 | all Ramat Gan: 6 commercial pages, /investment/ramat-gan-investment-apartment/, /ramat-gan-apartment-prices/ |
| apartments | 8 | /luxury-apartments-israel-guide/, /luxury-apartments-israel-guide-he/, /affordable-apartments-israel-2026/, /property-value/luxury-apartments-tel-aviv/, /real-estate-lawyer/sale-of-apartments-law/, /investment/apartments-for-investment/, /athens-apartments/, /global/project/lion-apartments-paphos/ |
| apartment | 106 | price pages per city (/tel-aviv-apartment-prices/ and others), guides, investment pages |
| tel / aviv | 80 / 92 | city qualifiers on many pages, including the sibling /tel-aviv-penthouse-prices/ and /tel-aviv-luxury-apartment-prices/ |
| sale | 38 | commercial and listing pages |
| tel-aviv | 0 | the tool splits on hyphens, so "tel" and "aviv" are counted separately |

## 3. Keyword guard (`tools/seo/kw_guard.py`, `docs/seo/protected-keywords.json`, built 2026-10-26)

- **"דירת גן למכירה" is a protected term, owner `/properties/`** (volume 210, KD 0, tier C, and "not seen in Search Console"). A new garden hub may not lead its title or H1 with "דירת גן למכירה". It may only carry it as a qualified phrase after its own topic.
- **Tests run on the candidate texts:**
  - H1 "דירות גן בתל אביב: מחירים, עסקאות ודירות למכירה": **WARN**, because "דירות למכירה" is protected with owner /properties/ (tier A, 5,400 a month).
  - Title "דירת גן בתל אביב — מחירי עסקאות לפי שכונה, רחוב וחדרים": **OK**.
  - Slug `tel-aviv-garden-apartments`: **OK**.
- **Other protected owners that matter here:**

| Term | Owner |
|---|---|
| דירות למכירה בתל אביב | city page (HAD-602, later) |
| דירות להשכרה בתל אביב | none |
| מחיר למטר, מחירי דירות | /apartment-prices/ |
| פנטהאוז למכירה, דירות 3 / 4 חדרים למכירה | /properties/ |
| דירות חדשות בתל אביב | /projects/ |

## 4. Listings on the site (WordPress REST, public)

- **Post types** (`/wp-json/wp/v2/types`): the listing type is `nadlan_property` (rest base `nadlan_property`). The others are `nadlan_project`, `nadlan_professional` and `nadlan_term`.
- **Search:** `/wp-json/wp/v2/nadlan_property?search=גן&per_page=50` returned 13. Only one is a garden flat: id 4957 `baka-jlm-garden-4r-demo`, "דירת גן 4 חדרים בבקעה, ירושלים — גינה של 45 מ״ר", **a demo** (is_demo true), in Jerusalem. The other 12 matched on other words.
- **All public listings** (`X-WP-Total: 25`). By property type and deal type:

| Property type / deal | Count |
|---|---|
| apartment / rent | 10 |
| apartment / sale | 6 |
| cottage / sale | 2 |
| penthouse / rent | 2 |
| penthouse / sale | 2 |
| villa / sale | 1 |
| **garden / sale** | **1**: 4957, Jerusalem Baka, demo |
| **garden / rent** | **1**: 4956, Haifa Carmel, demo |

- **Real Tel Aviv garden listings: 0.** Under the honesty law, the two demo garden listings must never appear on a sales surface.
- **Listing fields available today** (meta on `nadlan_property`): listing_type, **property_type (with the value `garden` already in use)**, price, price_per_sqm, rooms, floor, total_floors, size_sqm, balcony_sqm, parking, elevator, ac, **protected_room** (the ממ"ד flag), storage, street, building_number, lat/lng, city, neighborhood, condition, entry_date, renovated_year, direction, arnona_monthly, vaad_bayit_monthly, tour_url, video_url, floorplan_url, photos_csv, highlights_csv, is_demo, status, broker ids (nl_broker_id), hreflang twins, sponsor and promo fields.
- **Missing for garden flats:** garden m² (there is a balcony m² field but no garden m² field), garden registered or attached in the Tabu, private pool, and a garden duplex or lower-floor flag.

## 5. Existing pages a garden hub would sit next to (live sitemap, 2026-11-03)

- **Prices:** /tel-aviv-apartment-prices/, /tel-aviv-penthouse-prices/ (sibling pattern: H1 "מחירי פנטהאוזים בתל אביב", about 2,021 words in main, 12 H2s with an FAQ), /tel-aviv-luxury-apartment-prices/, /tel-aviv-seafront-apartment-prices/, /apartment-prices/.
- **Area:** /north-tel-aviv/ (and its sub-pages), /tel-aviv-plans/, /investment-apartment/tel-aviv-investment-neighborhoods/.
- **Features:** /guides/new-apartment-mamad/ (in 5 languages).
- **Listings and projects:** /properties/, /projects/, /new-projects/new-projects-tel-aviv/, /city/תל אביב יפו/projects/.
