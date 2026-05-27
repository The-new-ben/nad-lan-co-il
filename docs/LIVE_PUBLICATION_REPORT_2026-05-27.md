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

## Live Homepage Navigation Polish

Updated: 2026-05-28 00:59 Asia/Jerusalem

- Researched crawlable/internal links and WordPress menu behavior before editing:
  - Google Search Central link best practices: internal links should be crawlable `<a href>` elements with concise, descriptive anchor text.
  - WordPress Theme Handbook navigation menus: WordPress can fall back to generated page menus when a custom location is not properly assigned, which explains the long page-title menu behavior.
  - Nielsen Norman Group/footer-navigation research remains the trust/navigation reference for keeping footer and site chrome clear instead of keyword-dumped.
- Added a live, crawlable homepage navigation strip under the H1 with short public labels: `קנייה`, `השקעה`, `מקבלן`, `משכנתא`, `מס רכישה`, `טאבו`, `עורך דין`.
- Sanitized the inline homepage style block. WordPress auto-inserted paragraph tags inside the style block after blank lines, which made later CSS visible in HTML but not parsed by the browser. The style block now avoids blank-line paragraph injection.
- Added a repeatable headless Chrome verifier: `scripts/verify-nadlan-home.mjs`.

### Live Verification

- Live URL verified: `https://nad-lan.co.il/`.
- Desktop check: 1366px viewport, no horizontal overflow, one visible H1, page navigation visible, custom footer visible, hero visible, first image loaded.
- Mobile check: 390px viewport, no horizontal overflow, one visible H1, navigation wraps cleanly into compact rows, no cut labels.
- Blocked internal terms check passed: no `SEO`, `CRM`, `לידים`, `כוונת חיפוש`, `מסלולי כסף`, `מוניטיזציה`, or `ספקים` in rendered public text.
- Final screenshots:
  - `verification-screenshots/nadlan-home-nav-wrap-desktop-2026-05-28-top.png`
  - `verification-screenshots/nadlan-home-nav-wrap-desktop-2026-05-28-footer.png`
  - `verification-screenshots/nadlan-home-nav-wrap-mobile-2026-05-28-top.png`
  - `verification-screenshots/nadlan-home-nav-wrap-mobile-2026-05-28-footer.png`

### Honest Gap Statement

- This is a real visible live improvement, not a draft, and it was verified on the public homepage.
- The active Twenty Twenty-Five header still does not expose a proper desktop menu in the theme header. The page-level nav solves the user-facing/crawlable route issue on the homepage now, but the durable fix is still to move the header/nav/footer into the production theme and pull it through UPress Git management.
- Next competitive gap for Nadlan: expand the existing live pillar pages to 2,000-3,000 Hebrew words each and replace placeholder city links with real city/neighborhood hubs.

## Purchase Tax Page Expansion

Updated: 2026-05-28 01:19 Asia/Jerusalem

- Live page upgraded: `https://nad-lan.co.il/purchase-tax-calculator/`.
- Replaced the short 380-word draft-like content with a full consumer-facing guide of 2,037 words.
- Removed public internal wording such as `דראפט` and editor/source instructions.
- Added a realistic real-estate image, a premium guide layout, official Tax Authority bracket table, preparation checklist, mortgage connection, lawyer/checklist internal links, FAQ, and a public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for finance/YMYL quality.
  - Israel Tax Authority official purchase-tax simulator and official apartment brackets from 16.1.2025 to 15.1.2028.
  - Bank of Israel mortgage context as a planning connection for purchase-tax affordability.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/purchase-tax-calculator/`.
- Rendered H1 count: 1.
- Word count: 2,037.
- Image count: 1.
- Blocked internal terms: none.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Screenshot:
  - `verification-screenshots/nadlan-purchase-tax-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This page now meets the portfolio minimum content gate and is live, but it still needs the full site-wide Nadlan theme/header/footer deployment so every pillar page shares the same premium chrome as the homepage.
