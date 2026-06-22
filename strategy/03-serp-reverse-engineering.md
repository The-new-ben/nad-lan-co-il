# SERP Reverse Engineering War Room

Status: operating manual. This file defines how to turn "we need more SEO" into a ranked, verified, page-by-page search plan.

## Principle

Do not write a page because a keyword sounds important. Build a page only after the SERP proves one of these:

1. The query has clear commercial or legal value.
2. Current ranking pages are thin, outdated, generic, or not local enough.
3. NadLan can add a defensible edge: lawyer E-E-A-T, project-specific data, original tools, better UX, source-cited tables, or foreign-buyer localization.

## Required SERP Capture

For every priority query, capture the following in a committed note under `strategy/serp-notes/<query-slug>.md` or in the keyword CSV:

| Field | Required value |
|---|---|
| Query | Exact user query, in Hebrew or target language |
| Locale | Israel Hebrew by default; note if English/French/Russian/Arabic |
| Date checked | YYYY-MM-DD |
| Search mode | Chrome incognito or external SEO tool |
| Top 10 organic URLs | URL, title, meta, content type |
| SERP features | Ads, map pack, PAA, videos, images, snippets |
| Competitor page types | Portal, developer page, law firm, bank, blog, gov, project page |
| Content depth | Estimated word count, tables/tools/media present |
| Trust signals | author, date, sources, legal license, data source |
| Missing answers | what the top 10 do not answer well |
| NadLan angle | why our page deserves to exist |
| Page decision | create, improve, merge, noindex, or avoid |

If the search volume, CPC, or KD came from Semrush/GSC and is not independently rechecked, mark it `NEEDS_VERIFICATION`. Do not invent metrics.

## Competitor Patterns Confirmed By Research

Sources checked for the project-showroom pattern:

- Render Vision 3D Apartment Viewer: interactive building navigation, filters, comparison, and real-time availability are treated as a sales platform, not just a visual.
- Zillow 3D Home and Zillow Interactive Floor Plans: virtual tour + floor plan package is positioned as shareable listing media that helps buyers understand layout.
- Homes.com Matterport: buyer experience is a digital twin with detailed floor plans.
- Mapbox Real Estate: maps are used for property listings, rentals, and market insights, not only as decorative maps.
- Parallel Select: facade selector with availability colors and filter-driven apartment state.
- DIGBY Apartment Selector: active areas on a 3D rendered project image, with floor plans, images, and sales data per unit.
- Interactive Real Estate WordPress plugin: uploaded building renders/floor plans + clickable maps + callback lead flow.

Sources checked for Dimri Yama facts:

- Dimri official pages state the complex has four buildings, green landscape, internal garden, leisure facilities, spacious balconies, western facade with wave-like balconies, sea views, and floors A 38, B 8, C 15, D 8.
- SdeDov.co.il describes DIMRI YAMA as a beachfront Sde Dov project with four buildings, planning by Ranni Ziss Architects and design by Kelly Hoppen CBE.
- BuyItInIsrael and other public project pages reinforce the luxury/coastal positioning.
- Nadlan Center / Globes / JPost sources contain financial and development context that may be useful, but public legal/commercial reuse requires `LEGAL_REVIEW` and source/date citation.

## SERP Reverse Engineering Matrix

| Cluster | Example query | Current likely winner type | NadLan attack angle | Page action |
|---|---|---|---|---|
| New projects | פרויקטים חדשים בתל אביב | Portals, developers | rich project pages + buyer tools + lawyer trust | Create hub and project spokes |
| Sde Dov | רובע שדה דב | news, portals, developer pages | district pillar with every project, facts, map, buyer guide | Strengthen existing `/sde-dov/` |
| Project name | דמרי ימה שדה דב | official developer, portals | project page with buyer selector + cited data + contact | Improve project page |
| Price intent | דמרי ימה מחיר | thin snippets, broker pages | source-cited non-binding price range + disclaimer | Add price section |
| Foreign buyer | Tel Aviv new development foreign buyer | broker/law firms | English/French/Russian/Arabic legal + project guide | Create i18n pages |
| Purchase tax | מס רכישה 2026 | law firms, gov | lawyer-authored guide + calculator + CTA | Maintain pillar/tool |
| Mortgage | מחשבון משכנתא | banks/tools | real-estate journey calculator + lead routing | Build/upgrade tool |
| Urban renewal | פינוי בינוי תל אביב | law firms/news | lawyer-owned urban renewal knowledge base | Build pillar |
| Professionals | עורך דין נדלן תל אביב | law firms/directories | directory + owner legal authority + verification | Redesign professionals |
| Listings | דירות למכירה בתל אביב | Yad2/Madlan | do not fight head-on first; use niche/quality pages | Build later |

## Batch SERP Work Plan

### Batch A - P0 pages already connected to revenue

1. Homepage - primary query set: נדלן, nad-lan brand, real estate Israel.
2. Sde Dov hub - primary query: רובע שדה דב.
3. Rainbow project - primary query: Rainbow Tel Aviv / ריינבו תל אביב.
4. Dimri Yama project - primary query: DIMRI YAMA שדה דב / דמרי ימה.
5. Purchase tax pillar/tool - primary query: מס רכישה 2026.
6. Mortgage calculator/tool - primary query: מחשבון משכנתא.
7. Join Pro / professionals - primary query: פרסום נדלן / אינדקס בעלי מקצוע נדלן.

### Batch B - P1 expansion

1. City pages for Tel Aviv, Ramat Gan, Givatayim, Jerusalem, Netanya.
2. Neighborhood pages for Sde Dov, Ramat Aviv, Park Bavli, Florentin, Neve Tzedek.
3. Foreign buyer guides in EN/FR/RU/AR.
4. Urban renewal legal hub.
5. Project/developer profiles.

### Batch C - P2 programmatic

1. Neighborhood price pages.
2. Project comparison pages.
3. Investor yield pages.
4. School/transport/environment pages.
5. Glossary pages.

## SERP Output Template

```md
# SERP Note - <query>

Date:
Locale/device:
Primary intent:

## Top 10
| Rank | URL | Type | Title/meta summary | Strength | Gap |
|---|---|---|---|---|---|

## PAA / Related Searches

## Required sections for our page

## Differentiators NadLan must add

## Sources allowed

## Decision
Create / improve / merge / noindex / avoid.
```

## Hard Rules

- Do not copy competitor text.
- Do not use paid database rows publicly unless licensing and legal approval are explicit.
- Every number needs source + date.
- Do not target the same source-of-truth keyword with two live pages.
- If the page is a project showroom without official media, label assets as concept or show missing state.
