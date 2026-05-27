# nad-lan.co.il Live Publication Report

Date: 2026-05-27
Owner: Codex acting as operator

## Live Changes

- Set `https://nad-lan.co.il/` to a static public homepage instead of the default WordPress blog feed.
- Published the first real-estate content hub pages through WordPress REST API.
- Replaced public-facing operating language with consumer-facing wording such as `פנייה`, `בדיקה`, `הכוונה`, and `גורם מקצועי`.
- Saved WordPress permalink settings to `Post name`, which fixed clean page URLs.
- Updated homepage internal links back to clean SEO URLs after live verification.

## Published URLs Verified

| Page | URL | Verification |
| --- | --- | --- |
| Homepage | `https://nad-lan.co.il/` | HTTP 200, unique homepage content, hero image present |
| Purchase tax | `https://nad-lan.co.il/purchase-tax-calculator/` | HTTP 200, unique H1 |
| Mortgage adviser | `https://nad-lan.co.il/mortgage-advisor/` | HTTP 200, unique H1 |
| Buying checklist | `https://nad-lan.co.il/apartment-buying-checklist/` | HTTP 200, unique H1 |
| Buying apartment pillar | `https://nad-lan.co.il/buying-apartment/` | HTTP 200, unique H1 |
| Investment apartment | `https://nad-lan.co.il/investment-apartment/` | HTTP 200, unique H1 |
| Real-estate lawyer | `https://nad-lan.co.il/real-estate-lawyer/` | HTTP 200, unique H1 |
| New projects | `https://nad-lan.co.il/new-projects/` | HTTP 200, unique H1 |
| Tabu extract check | `https://nad-lan.co.il/tabu-extract-check/` | HTTP 200, unique H1 |

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
- Pretty permalinks were broken immediately after publication, returning the homepage instead of unique page content. This was fixed by saving WordPress permalink settings to `Post name`; the clean URLs now return the correct H1s.

## Next Gap-Closing Tasks

1. Expand each published page to competitor-level depth.
2. Add structured FAQ blocks and schema where appropriate.
3. Add a real lead form to each page or a clear shared intake flow.
4. Replace the external hero image with an owned/generated asset uploaded to WordPress media.
5. Add Search Console sitemap submission/recrawl once the content depth pass is complete.

## Lovable Competitor Skill Pass

Updated: 2026-05-28 00:20 Asia/Jerusalem

- Used Lovable on the existing SEO Navigator project with a research-only prompt for `nad-lan.co.il`.
- Lovable UI proof: `Used 9 tools`; saved file `nadlan-seo-business-design-skill.md`.
- Local copy saved to `docs/NADLAN_LOVABLE_COMPETITOR_SKILL_2026-05-27.md`.
- Reusable Codex skill created and validated: `C:/Users/pro/.codex/skills/nadlan-real-estate-growth/SKILL.md`.
- Competitors scanned/reported by Lovable: `yad2.co.il/realestate`, `madlan.co.il`, `nadlan.gov.il`, Homeless/WinWin/Yad1, MyPlace, Onmap, Nadlanmaster, IFRSConsulting, Meitav, Lazyinvestor.
- Lovable-reported competitive signals: Yad2 around 3.21M monthly organic traffic, Madlan around 192K, homepage traffic share around 36-37% for the major marketplaces, `מחשבון משכנתא` as the largest tool opportunity, and `נדלן להשקעה` as a weaker/dominatable SERP opening. These are internal Semrush/Lovable research leads and must not be published as public claims without independent verification.

## Live Homepage Polish From Skill

Updated: 2026-05-28 00:40 Asia/Jerusalem

- Rebuilt the live homepage through WordPress REST API. This was a direct public content/CSS change, so UPress Git pull was not required for this block.
- Live URL: `https://nad-lan.co.il/`
- Replaced public internal wording such as `כוונת חיפוש` with buyer-facing language.
- Reduced the live homepage to one visible H1: `נדלן חכם: קנייה, מכירה והשקעה עם נתונים`.
- Hid the default WordPress/Twenty Twenty-Five footer and inserted a custom trust/navigation footer with real estate paths.
- Added a premium first viewport: compact brand mark, data/tool entry, buyer/investor/tax CTAs, realistic Tel Aviv skyline image, and clear professional-check narrative.
- Desktop screenshot: `verification-screenshots/nadlan-home-lovable-polish-headless-2026-05-28.png`.
- Mobile CDP screenshot: `verification-screenshots/nadlan-home-lovable-polish-mobile-cdp-2026-05-28.png`.

### Live Verification

- HTTP/live page: `https://nad-lan.co.il/` returns the updated homepage.
- Rendered H1 count: 1 visible H1.
- Blocked public terms check: no `SEO`, `CRM`, `לידים`, `כוונת חיפוש`, `מסלולי כסף`, `תנועה מסחרית`, or `מוניטיזציה` found in rendered public text.
- Default footer: hidden; custom footer visible.
- Mobile CDP metrics: viewport width 390, scroll width 390, one H1, no blocked terms.

### Honest Gap Statement

- This is a real visible upgrade, but it is still an interim REST/content-layer homepage. The stronger long-term fix is to activate/sync the dedicated `NadLan Revenue` theme on production through UPress Git pull and then move this homepage/chrome into theme files.
- Homepage depth is suitable for a hub, but the competitive pages still need full 2,000-3,000 word expansions.
- The current city links are placeholders to existing published pages. Next pass should create real city/neighborhood hubs and connect them to transaction/source data.
