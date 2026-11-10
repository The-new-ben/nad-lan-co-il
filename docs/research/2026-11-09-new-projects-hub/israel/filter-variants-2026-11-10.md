# Filter variants of one listing page: how Yad2 and Madlan do it, and what it costs (10.11.2026)

Owner question, 10.11.2026: Yad2 wins budget searches with versions of one page whose title changes with the filter. How does
that not hurt them (cannibalisation)? Decision for now: sections on one page. This note is the evidence behind that decision.

## What was read (owner's Chrome, rendered pages, 10.11.2026 about 19:10)

| URL | Title | H1 | Canonical | Robots |
|---|---|---|---|---|
| yad2.co.il/yad1/newprojects/tel-aviv-area | פרויקטים ודירות חדשות בתל אביב והסביבה - מעודכן ל-2026 | פרויקטים ודירות חדשות בתל אביב והסביבה | itself | follow, index |
| …/tel-aviv-area?maxPrice=1500000 | …עד 1,500,000 ₪ - מעודכן ל-2026 | …עד 1,500,000 ₪ | itself, with the parameter | follow, index |
| …/tel-aviv-area?maxPrice=1200000 (a value typed by hand) | …עד 1,200,000 ₪ - מעודכן ל-2026 | …עד 1,200,000 ₪ | itself, with the parameter | follow, index |
| madlan.co.il/projects-for-sale/תל-אביב-יפו-ישראל | דירות ופרויקטים חדשים בתל אביב יפו \| מדלן | דירות ופרויקטים חדשים למכירה בתל אביב יפו | itself | index,follow |

Other facts read the same hour:
- **Yad2 opens some filters and closes many.** Its robots.txt blocks crawling of about 40 filter parameters on property pages
  (parking, balcony, elevator, floor, furniture, square metres, renovated, text search, sort order, pagination and more). The
  price ceiling (`maxPrice`), the area and the city are not blocked. So the indexable versions are the ones people search.
- **Any price value becomes an indexable page.** `maxPrice=1200000` is not a page Yad2 links to; typing it still returns its
  own title, H1 and self-canonical.
- **The versions are near copies.** Five of the first six project cards on the 1.2 million version are also among the first six
  on the 1.5 million version.
- **Google already mixes them.** For "דירות חדשות עד 1.2 מיליון" Google ranks Yad2's 1.5 million version of the general sale
  listing in first place, not a 1.2 million version (two readings, 15:20 and 17:35). The exact page exists and is indexable, and
  Google shows another one. That is the confusion the owner asked about, visible on the market leader.
- **Madlan uses places only.** Its indexable versions are path pages for a city or a neighbourhood, each with its own title, H1
  and self-canonical, linked from a city list on every page. No budget version was found.

## Our own pages today

| URL | Title and H1 | Canonical | Robots |
|---|---|---|---|
| /projects/?city=חיפה | same as /projects/ | /projects/ | index, follow |
| /projects/page/2/ | same as /projects/ | itself | index, follow |
| /projects/?status=… | same as /projects/ | /projects/ | noindex, follow |

Our city filter says "I am a copy of /projects/". That is the safe setting: it cannot compete with the main page. It also means
it cannot win a city search on its own. Finding only: page 2 and later are indexable with the same title and H1 as page 1.

## What practitioners say (not Google)

Sam Underwood, "Faceted Navigation" (Ahrefs blog, updated 7.2.2025; reviewed by Joshua Hardwick and Patrick Stox):
- Filters are "notorious for creating URLs with duplicate content en masse"; the damage he lists is keyword cannibalisation,
  "dilution of ranking signals into multiple URLs", index bloat and wasted crawling.
- The test for opening a filter page is search demand: "would a user ever search in Google for something that precise?"
- A filter page that is opened needs: its own canonical, no noindex, plain internal links from a second path, a place in the
  sitemap, a readable address, its own title, description and headings, and "unique written content".
- A canonical tag is a suggestion: Google may ignore it when the pages are not real copies or when the site links to them.
- On one audited site he found 39 non-indexable URLs for every indexable one.
The other guides found (Search Engine Land, Oncrawl, Search Engine Journal, StudioHawk, Salt) give the same rule: open only the
filter combinations with real search demand, give each a unique title and content, close the rest.

## Answer to the owner's question

1. It does hurt. The versions are near copies, and Google picks one of them, sometimes the wrong one, as it does today for 1.2 million.
2. Yad2 can afford it: its authority lets even a near copy reach first place, and it closes the long tail of filters in robots.txt
   so only searched filters are open.
3. For a site with our authority, a dozen near copies of /projects/ would each be weaker than the one page, and each would share
   the same 564 rows. The practitioners' conditions for opening a filter page (unique content, own links, own sitemap entry) are
   real work per page.
4. So for now: one page, one title, a section and a short answer for each searched filter (released in 1.72.632). Re-check in
   Search Console after two weeks and after a month.
5. If the sections do not move a searched filter, the next candidate is ONE opened version with real unique content, the place
   version first (a city or Tel Aviv neighbourhood, as Madlan does), never a price ladder of near copies. That would be an
   indexing decision for the owner, taken with the page-level data.

Limits: one day; rendered pages, not raw HTML; the combined-filter version and Madlan's price filter were not read.
