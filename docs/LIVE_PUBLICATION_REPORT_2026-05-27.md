# nad-lan.co.il Live Publication Report

Date: 2026-05-27
Owner: Codex acting as operator

## Live Changes

- Set `https://nad-lan.co.il/` to a static public homepage instead of the default WordPress blog feed.
- Published the first real-estate content hub pages through WordPress REST API.
- Replaced public-facing operating language with consumer-facing wording such as `פנייה`, `בדיקה`, `הכוונה`, and `גורם מקצועי`.
- Updated homepage internal links to the currently working plain WordPress page URLs because pretty permalinks are not resolving unique page content yet.

## Published URLs Verified

| Page | URL | Verification |
| --- | --- | --- |
| Homepage | `https://nad-lan.co.il/` | HTTP 200, unique homepage content, hero image present |
| Purchase tax | `https://nad-lan.co.il/?page_id=6` | HTTP 200, unique H1 |
| Mortgage adviser | `https://nad-lan.co.il/?page_id=7` | HTTP 200, unique H1 |
| Buying checklist | `https://nad-lan.co.il/?page_id=8` | HTTP 200, unique H1 |
| Buying apartment pillar | `https://nad-lan.co.il/?page_id=9` | HTTP 200, unique H1 |
| Investment apartment | `https://nad-lan.co.il/?page_id=10` | HTTP 200, unique H1 |
| Real-estate lawyer | `https://nad-lan.co.il/?page_id=11` | HTTP 200, unique H1 |
| New projects | `https://nad-lan.co.il/?page_id=17` | HTTP 200, unique H1 |
| Tabu extract check | `https://nad-lan.co.il/?page_id=18` | HTTP 200, unique H1 |

## Research Applied

- Google Search Central: people-first content, crawlable links, image SEO, and useful internal linking.
- Israel Tax Authority service pages for purchase-tax context.
- Bank of Israel mortgage comparison/transparency context.
- Gov.il land-registration extract service context.
- Competitor DNA target for the next improvement pass: Israeli real-estate marketplaces and service pages that lead with clear search intent, calculators, price context, city/property segmentation, professional trust, and short conversion paths.

## Critical Review

- This is a real public visibility upgrade, but it is not the final competitive standard.
- The homepage is now much better than the default WordPress state, yet still needs a custom branded theme, stronger logo, better above-the-fold trust proof, and mobile CTA polish.
- The published pages are useful first pages, but still too short versus top-ranking competitors. The next content pass should expand each page with more price ranges, examples, questions, updated official-source references, and comparison tables.
- Pretty permalinks currently return the homepage content instead of the unique page content. Until this is fixed, homepage links use working `?page_id=` URLs.

## Next Gap-Closing Tasks

1. Fix pretty permalinks so `/purchase-tax-calculator/`, `/mortgage-advisor/`, and similar URLs resolve to unique content.
2. Expand each published page to competitor-level depth.
3. Add structured FAQ blocks and schema where appropriate.
4. Add a real lead form to each page or a clear shared intake flow.
5. Replace the external hero image with an owned/generated asset uploaded to WordPress media.
