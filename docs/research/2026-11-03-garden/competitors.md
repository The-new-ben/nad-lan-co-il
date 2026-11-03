# Garden apartments in Tel Aviv: competitor pages read in full

**Read on 2026-11-03, 17:36 to 17:45 UTC.**

- **Plain fetch:** curl with a browser user agent, saved in `scratchpad/garden-dl/` and parsed by `scratchpad/garden/html_text.py`.
- **Madlan and Yad2:** both refuse a plain fetch. Madlan answers 403 with a "Just a moment…" check; Yad2 shows a Radware "Verifying your browser" page. No check was bypassed. Both pages were then read in the owner's Chrome ("gmktec") as ordinary public pages, with no login, through DOM text extraction.
- **Word counts:** all visible text on the page, navigation included, unless "main" is stated.

These were chosen as the most relevant pages because they rank in the five SERPs (serp.md).

## 1. Madlan: דירות גן למכירה בתל אביב יפו

URL: https://www.madlan.co.il/garden-apartments-for-sale/תל-אביב-יפו-ישראל

- **Title:** "דירת גן למכירה בתל אביב יפו - 755 דירות מחכות לך | מדלן". **H1:** "דירות גן למכירה בתל אביב יפו". **H2:** "755 דירות גן למכירה".
- **Listings:** 755 in Tel Aviv-Yafo city, 16 result pages. Each card shows the asking price, rooms, floor, built m², street, neighbourhood and badges (broker, exclusive, "Top10 במדד המתווכים"). Developer project cards are mixed in ("פרויקט במבצע", PRESALE, and "150,000 ש"ח לעיצוב הבית").
- **Filters:**
  - Main bar: price, rooms, property type, a toggle for new project / broker / private, and sort.
  - "More filters" panel: deals ("מד מדלן" good-price flag, recent price drop, projects on promotion); features (parking, elevator, balcony, **ממ"ד**, ממ"ק, shelter, AC, storage, accessible, bars); who sells (private, broker, developer); condition (5 levels); built m² range; floor range.
  - There is **no garden-size filter**, and no garden m² on the cards.
- **Price data:** none on this page. No average, no price per m², no closed deals. Madlan does have address pages ("מידע על כתובות" in the menu), but this page does not link deal data to garden flats.
- **Map:** none on page load (no map element detected).
- **Tools:** saved-search alert ("יצירת התראה"), the good-price flag, a price-drop filter, and mortgage promotions mixed into the list.
- **Article:** none about garden flats. A "יעניין אותך לדעת…" strip has 30 generic article and podcast teasers (Neve Sha'anan, Yad Eliyahu, a mortgage guide, among others).
- **Internal links:** 2, 3, 4 and 5-room pages for Tel Aviv (generic, not garden), "דירות עם ממ״ד למכירה בתל אביב יפו", plus neighbourhood and street garden pages that rank separately (Hadar Yosef 116, Neve Tzedek 117, Kfar Shalem 108, Ramat HaHayal 110, מח"ל street 7).
- **Schema:** BreadcrumbList and ItemList.
- **Words:** about 1,668 visible (almost all listing cards and teasers).
- **Data quality seen:** a listing at "111,111 ₪" (מח"ל 24, 240 m²) is live in the list, and Google's AI Overview quotes it.
- **Missing:** closed-deal prices, ₪ per m², garden size, any explanation of what a garden flat is or how to check one (Tabu attachment of the garden, building permits), a garden + ממ"ד combined page, a street price table, and an unmixed new vs second-hand comparison.

## 2. Yad2: דירות גן למכירה בתל אביב והסביבה

URL: https://www.yad2.co.il/realestate/forsale/tel-aviv-area?property=3

- **Title:** "דירות גן למכירה בתל אביב והסביבה | אלפי מודעות חדשות בכל יום". **H1:** "דירות גן למכירה בתל אביב והסביבה".
- **Listings:** "931 תוצאות" for the Tel Aviv **area**. That area includes Holon and Ramat Gan, so the city figure is not shown. Cards show the asking price, street, neighbourhood, rooms, floor, m² and badges: ממ"ד, "ירד ב-100,000 ₪", exclusive.
- **Filters:**
  - Property types (garden is one of them).
  - With photo, with price, price dropped, 3D tour.
  - Features: elevator, balcony, AC, bars, accessible, renovated, furnished, **ממ"ד**, exclusive, building shelter, ממ"ק.
  - 5 condition levels, 4 permit stages, entry date, built m² ("מ״ר בנוי"), free text.
  - There is **no garden-size filter**.
- **Price data:** none (no medians, no per-m² figures for resale).
- **Map:** yes.
- **Tools:** saved alert, a price-drop flag, a 3D-tour filter.
- **Article:** none. About 2,629 words in total, all listings and menus.
- **Missing:** a Tel Aviv city-only count, deal prices, garden size, any guidance text.

## 3. Yad2 / Yad1: דירות גן חדשות בתל אביב והסביבה

URL: https://www.yad2.co.il/yad1/newprojects/tel-aviv-area?propertyType=garden

- **Title:** "דירות גן חדשות בתל אביב והסביבה - מעודכן ל-2026". **H1:** the same.
- **Listings:** developer project cards. The page states no total. Examples:
  - מעבר לכיכר, Jabotinsky 133-137: from ₪3,930,000.
  - קיציס תל אביב, Hadar Yosef: from ₪39,000 per m².
  - מרים החשמונאית 2-4-6: from ₪6,035,800.
  - BLOCH 10: from ₪6,150,000.
  - Also INFINITY TOWER, לב בבלי, and Ramat Gan, Givatayim and Bat Yam projects.
- **Filters:** area, rooms, and room-specific URLs such as minRooms=3&maxRooms=3, which rank for "דירת גן 3 חדרים בתל אביב".
- **Price data:** "from" prices per project only.
- **Map:** yes.
- **Article:** a generic Yad1 footer paragraph (about 979 words in total on the page).
- **Missing:** how many garden units each project has, garden sizes, any deal data, any ממ"ד information.

## 4. Habait-halavan: דירות גן למכירה בתל אביב (broker blog)

URL: https://www.habait-halavan.co.il/דירות-גן-למכירה-בתל-אביב/

- **Title:** "דירות גן למכירה בתל אביב | תיווך הבית הלבן", published 22.4.2025. It has **no H1**.
- **Structure:** H2 "דירות גן למכירה בתל אביב – מגורים בלב העיר עם תחושת טבע ופרטיות", "כיצד לבחור דירת גן למכירה בתל אביב?", and a sales closing block. H3s cover why they are in demand, where they are (Old North and Ramat Aviv, the centre, renewing south), defining your needs, checking the garden (registered in the Tabu, private and not shared, electricity and water), and professional support.
- **Listings, filters, price data, map, tools:** none.
- **Words:** about 888 visible; the body text is roughly 600 to 700 words. Schema: WebPage and BreadcrumbList.
- **Why it ranks:** it is the only article-style page on page 1, and the AI Overview cites it.
- **Missing:** every number, any listing, any area-level data.

## 5. Israel Sotheby's: דירת גן בצפון תל אביב (tag page)

URL: https://www.israelsir.co.il/property_tags/דירת-גן-בצפון-תל-אביב/

- **H1:** "דירת גן בצפון תל אביב".
- **Listings:** 2, both shown in USD and ₪:
  - Garden flat with a private pool in Kochav HaTzafon, 5 rooms, 220 m² built, ₪19,000,000.
  - Garden flat in Savyonei Ramat Aviv, 233 m² built, ₪11,900,000.
- **Filters, data, map:** none.
- **Words:** 55 in main, 347 in total. Schema: CollectionPage.
- **Missing:** everything except the two cards. It feeds the AI Overview's "up to 19 million" figure.

## 6. Home Stories: 4 דירת גן למכירה בתל אביב (broker list)

URL: http://www.home-stories.co.il/areaProperties.aspx?city=תל אביב&action=מכירה&prp=דירת גן

- **Listings:** 4:
  - Hadar Yosef, 4 rooms, ground floor: ₪4,190,000.
  - Habima, 4 rooms: ₪6,900,000.
  - New North, project under construction, 4 rooms: ₪8,100,000.
  - Shabazi (Neve Tzedek), 6 rooms, floor 1: ₪9,890,000.
- **Filters:** a search form (neighbourhood, rooms, maximum price, property type).
- **Words:** about 615 visible, mostly form options.
- **Missing:** data and content.

## Scoring

Scale: 0 = absent, 1 = weak, 2 = good, 3 = best seen.

| Page | Listings | Filters | Price data by street | Map | Tools | Article depth | ממ"ד filter | Garden size data | Total |
|---|---|---|---|---|---|---|---|---|---|
| Madlan, TLV garden for sale | 3 (755) | 3 | 1 (street listing pages exist; no prices or deals) | 0 (none on load) | 2 (alert, good-price flag, price drop) | 0 | 3 | 0 | **12** |
| Yad2, TLV-area garden for sale | 3 (931, area) | 3 | 0 | 3 | 2 (alert, price drop, 3D) | 0 | 3 | 0 | **14** |
| Yad1, new garden projects TLV | 2 (projects) | 2 | 1 ("from" prices, one per-m²) | 3 | 1 | 0 | 0 | 0 | **9** |
| Habait-halavan article | 0 | 0 | 0 | 0 | 0 | 1 (about 650 words, no numbers) | 0 | 0 | **1** |
| Israel Sotheby's tag | 1 (2) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **1** |
| Home Stories list | 1 (4) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **2** |
| **nad-lan.co.il today** | 0 (no real TLV garden listing) | 0 (no garden page) | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

## Strongest competitor and its gap

**The strongest is Madlan.** It ranks on all 5 SERPs with neighbourhood, street and single-address pages; it holds the largest Tel Aviv city inventory (755); it has a ממ"ד filter; and it is cited in every AI Overview that was read. Yad2 scores higher on map and area inventory, but it does not cover Tel Aviv city as such and it has no neighbourhood depth in these SERPs.

**What every competitor lacks:**

- **Closed-deal prices for garden flats.** No page publishes the Tax Authority garden deals (248 rows for Tel Aviv-Yafo, 2001 to 2024-08). The AI Overview has to build its price answer from asking prices, including a "111,111 ₪" placeholder.
- **Garden size.** No filter, no card field, no ₪ per garden m².
- **A garden + ממ"ד answer.** That SERP is Facebook posts and single-address pages.
- **Rooms × garden × Tel Aviv.** Google shows generic 3-room and rent pages.
- **Guidance with numbers.** The only article (habait-halavan) has no data.
- **Ground floor against the building.** No one shows how ground-floor prices compare with the rest of the neighbourhood (our proxy table in garden-deals.md).
