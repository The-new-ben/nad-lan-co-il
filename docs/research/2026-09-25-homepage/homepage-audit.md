# The homepage today: data and a live audit (25.9.2026, H1 step 1)

**Why now:** the owner moved the homepage first on 25.9.2026 (the board's order override; Linear HAD-297).

## Google Search Console (API, 25.6 to 22.9.2026, 90 days)

- **The whole site:** 1,101 clicks, 137,877 impressions, CTR 0.80%, average position 28.6.
- **The homepage:** 638 queries, **2 clicks**, 2,473 impressions. Its top queries rank far down:
  - "נדלן": 182 impressions, position 55;
  - "מידע נדלן": position 43;
  - "דירות חדשות": position 82;
  - "פרויקטים חדשים": position 79;
  - "מרכז הנדלן": position 26.5;
  - "פרויקטים חדשים מחירים": position 25.1.
- **The head terms across the whole site** (the exact term, or with one more word):

| Term | Impressions | Clicks | Average position | Pages that compete for it |
|---|---|---|---|---|
| פרויקטים חדשים | **12,771** | 1 | 38.7 | **103** |
| דירות חדשות | 3,888 | 0 | 46.4 | 74 |
| נדלן | 3,325 | 4 | 51.5 | 90 |
| מחשבון משכנתא | 2,206 | 1 | 54.2 | 1 |
| פרויקטים חדשים בתל אביב | 1,174 | 0 | 45.8 | 7 |
| נדל"ן | 634 | 0 | 50.2 | 37 |
| דירות למכירה | 299 | 0 | 29.8 | 15 |
| דירה למכירה | 179 | 2 | 22.8 | 5 |
| מחירי דירות | 77 | 0 | 30.1 | 23 |

- **Reading the table:**
  - The biggest demand is "פרויקטים חדשים", and 103 of our pages split it between them.
  - The homepage and the catalogue (/catalog/) both try to rank for it, and neither ranks.
  - The homepage should own the portal's broadest term ("נדל"ן", with its forms) and hand the projects' demand to one hub, through clear internal links.
- **Hygiene:** the homepage with the membership plugin's parameters (`/?pms_user=0&pms_action=pms_delete_user&…`) appears in Google for "דירות למכירה". That is a finding to record; noindex needs the owner's word.

## The live page

**Search basics**

- **Title** (55 characters): "נדלן - דירות למכירה, פרויקטים חדשים ומחירי דירות בישראל".
- **h1:** one, "פרויקטים חדשים, דירות למכירה ומחירי דירות בכל הארץ".
- **Meta description:** it promises "בדקו זמינות דירות לפי קומה ונוף". We have no availability for most projects, so it goes against the honesty law.

**Sections, links and markup**

- **Sections:** 12 h2 sections (the home v2 renderer, `nlhv2`, with 6 mega-menu panels):
  - new projects in Tel Aviv;
  - new listings;
  - prices and calculators;
  - where buyers look;
  - where the market goes;
  - news and guides;
  - professionals;
  - the building's project room;
  - the live projects map;
  - the rental management;
  - tours, map, rent and urban renewal;
  - an English section.
- **Internal links:** 116 unique.
- **Schema:** Organization, WebSite with SearchAction, ItemList, WebPage.
- **Text:** about 1,258 visible words.

**Weight and speed**

- **Size:** 244 KB of HTML, of which the head is **107 KB**.

**Speed on a mid Android** (4x CPU, Slow 4G, two runs):

| Measure | Result |
|---|---|
| First contentful paint | 3.95 s and 4.25 s |
| Largest contentful paint | **17.0 s and 17.7 s**: the hero image, nadlan-hero-israel-coastline-v2.jpg, 1400 x 1049 |
| Layout shift | 0.097 |
| Requests | 52 |
| Transferred | 2.3 MB |

- **Why it matters:** Google counts a largest paint over 4 s as poor. The hero image is also what the owner called "not premium".

## What follows (the H1 plan)

1. Competitors' homepages: a ChatGPT deep research in the owner's Chrome.
2. The homepage v2 in Claude Design: the portal kept (mega menus, search, listings, projects, prices, tools, guides, professionals), with a premium hero of our own that paints in under 3 s.
3. The SEO copy plan from the table above.
4. The build, in releases.
