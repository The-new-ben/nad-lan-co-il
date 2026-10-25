# Tel Aviv-Yafo Municipality - "פרויקטים חדשים" (new neighbourhoods)

- URL: https://www.tel-aviv.gov.il/Residents/Development/Pages/NewNeighborhoods.aspx
- SERP: #6 for "פרויקטים חדשים", #3 for "פרויקטים חדשים תל אביב" (serp.md, 25.10.2026). Cited in Google's AI overview ("projects in Tel Aviv and the centre").
- Retrieved: 25.10.2026 07:34 UTC curl (SharePoint + Angular, partly client-rendered) and 07:40 UTC rendered in the owner's Chrome (gmktec) for the tiles. DataForSEO instant_pages was blocked (status 571). Raw: `raw/tlvgov.html`.
- Title: `פרויקטים חדשים | עיריית תל אביב-יפו`
- Meta description: information about new neighbourhoods planned within Tel Aviv-Yafo and contact details for the planning and building division.
- H1: `פרויקטים חדשים` (two h1 tags in source: one mobile, one desktop).
- Visible words: main content ~475 (intro ~60, two promo blocks ~160, podcast block ~170); the page is 3,900+ words only because of the mega-menu.

## Heading outline (rendered, main area)
- h1 פרויקטים חדשים
  - h3 tiles (14): התחדשות התחנה המרכזית / התחדשות עירונית בפלורנטין / התחדשות עירונית בשכונת לבנה / התחדשות עירונית בשכונת רמת הטייסים / התחדשות שכונות ניר אביב, נווה חן ונווה אליעזר / התחדשות שכונת כפיר / עיר כיכר ים / צפון מערב - 3700 / קירוי איילון / רובע שדה דב / שדה דב - שיתוף ועדכון הציבור / שוק הכרמל / תכנון ופיתוח שכונת נאות אפקה ב' / תכנית לאיחוד וחלוקה (רה-פרצלציה) בשכונת התקווה
  - (server HTML also carries) h2 שדה דב, h2 תוכנית צפון מערב העיר 3700
- h2 רוצים לשמוע עוד? / h3 שכירות הוגנת / h3 פארק המסילה ומרחב ציבורי / h3 דיור בר השגה
- h3 האגף לתכנון העיר (contact)
- h2 האם דף זה עזר לך?

## Sections in order
1. Breadcrumb + left sub-navigation listing every new-neighbourhood page (adds Neve Avivim and Yad Eliyahu to the tiles).
2. Two-sentence intro: planning in areas not available before, mixed use, open space, green building, public buildings.
3. "News flashes" (מבזקים) widget - empty at retrieval.
4. Tile grid of 14 planning areas, each linking to a dedicated municipal page.
5. Promo blocks: Sde Dov (airport closure to free land for thousands of units) and North-West plan 3700 (new district along the northern shore).
6. Municipal podcast episodes (fair rent, Park Hamesila and public space, affordable housing).
7. City Planning Division contact card (phone, fax, address, online request) + page-feedback widget.

## Data points published
- Sde Dov: 2010 government decision to close the airfield to build thousands of housing units; mixed residential, employment, retail, hotels, public space.
- Plan 3700 (North-West): new urban quarter along the northern coastline.
- Planning areas named: Central Bus Station renewal, Florentin, Livne, Ramat Hatayasim, Nir Aviv / Neve Chen / Neve Eliezer, Shkhunat Kfir, Kikar Yam city, North-West 3700, Ayalon roofing (Kiruy Ayalon), Sde Dov quarter + public participation, Carmel Market, Neot Afeka B, Hatikva re-parcellation, Neve Avivim, Yad Eliyahu.
- No prices, no developers, no project-level listings, no dates.

## Tools / interactive
- Site search, page feedback (yes/no + text), GIS maps link in footer, accessibility. No filters, map, calculator or alerts on this page.

## Structured data
- None (no JSON-LD, no microdata). og:type website.

## FAQ questions
- None.

## Internal linking
- ~688 unique internal links (mega-menu dominated). Content links: 14 tiles + 16 side-nav planning pages + policy pages (TAMA 38 municipal policy, master plan, urban renewal, Rova plan pages via nav).

## Judgement
- Ranks on pure authority: the government entity for the city, a matching title ("פרויקטים חדשים"), and the official source for the plans every other page talks about (Sde Dov, 3700, renewal neighbourhoods).
- It satisfies the "what is being built in Tel Aviv" informational slice of the intent, which is why Google keeps it in the top 3 for the Tel Aviv query and quotes it in the AI overview.
- Weaknesses: no listings, no prices, almost no text, JS-dependent tiles, no schema, tile order is alphabetical not by buyer relevance.
- Lesson: our hub should cover the official planning layer (Sde Dov, 3700, renewal neighbourhoods, Kikar Yam, Ayalon roofing) and cite/link the municipal pages as sources, then add what the city cannot: which marketed projects sit inside each plan, prices and stage.
