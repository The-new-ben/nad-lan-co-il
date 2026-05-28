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

## Mortgage Adviser Page Expansion

Updated: 2026-05-28 01:32 Asia/Jerusalem

- Live page upgraded: `https://nad-lan.co.il/mortgage-advisor/`.
- Replaced the short 355-word draft-like content with a full consumer-facing guide of 2,035 words.
- Removed public internal wording such as `דראפט` and editor/source instructions.
- Added a realistic real-estate image, premium guide layout, sections on early financing checks, adviser role, preliminary approval, comparing bank offers, mortgage tracks, new-build purchases, investment apartments, preparation checklist, common mistakes, FAQ, and public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for financial/YMYL quality.
  - Bank of Israel “Equalizer” and mortgage comparison information, including the public note that these tools are informational and not personal advice.
  - Current competitor SERP review for Israeli mortgage-guide structure, with the public page written as original Hebrew content.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/mortgage-advisor/`.
- Rendered H1 count: 1.
- Word count: 2,035.
- Image count: 1.
- Blocked internal terms: none.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Screenshot:
  - `verification-screenshots/nadlan-mortgage-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This page now meets the portfolio minimum content gate and is live, but it still needs the same site-wide Nadlan header/footer/theme polish and later a real calculator or offer-comparison interface to compete with the strongest mortgage competitors.

## Real Estate Lawyer Page Expansion

Updated: 2026-05-28 01:52 Asia/Jerusalem

- Live page upgraded: `https://nad-lan.co.il/real-estate-lawyer/`.
- Replaced the short 329-word draft-like content with a full consumer-facing guide of 2,005 words.
- Removed public internal wording such as `דראפט` and editor/source instructions.
- Added a realistic real-estate image, premium guide layout, sections on rights and registration checks, Tabu extract, timing before signing, sale-contract checks, new-build purchases, investment apartments, first-contact checklist, common mistakes, FAQ, and public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for legal/financial YMYL quality.
  - Gov.il Land Registry extract page for official Tabu context: what the extract contains, when to check it, and why it is date-sensitive.
  - Current competitor SERP review for real-estate lawyer and apartment-purchase contract pages, rewritten as original Hebrew content.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/real-estate-lawyer/`.
- Rendered H1 count: 1.
- Word count: 2,005.
- Image count: 1.
- Blocked internal terms: none.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Screenshot:
  - `verification-screenshots/nadlan-lawyer-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This page now meets the portfolio minimum content gate and is live, but it still needs the same site-wide Nadlan header/footer/theme polish and later a real inquiry/profile flow for vetted real-estate lawyers.

## Investment Apartment Page Expansion

Updated: 2026-05-28 02:12 Asia/Jerusalem

- Live page upgraded: `https://nad-lan.co.il/investment-apartment/`.
- Replaced the short 349-word draft-like content with a full consumer-facing guide of 2,002 words.
- Removed public internal wording such as `דראפט` and awkward wording from the previous version.
- Added a realistic real-estate image, premium guide layout, sections on investment goals, yield calculation, purchase tax, mortgage and leverage, area/rental checks, legal and physical checks, investor worksheet, new-build investment, tenant management, exit planning, common mistakes, FAQ, and public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for financial/YMYL quality.
  - Israel Tax Authority official purchase-tax simulator for second/investment apartment tax planning.
  - Current competitor SERP review for Israeli investment-apartment guides, yield calculators, financing pages, and city-opportunity pages, rewritten as original Hebrew content.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/investment-apartment/`.
- Rendered H1 count: 1.
- Word count: 2,002.
- Image count: 1.
- Blocked internal terms: none.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Screenshot:
  - `verification-screenshots/nadlan-investment-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This page now meets the portfolio minimum content gate and is live, but it still needs the same site-wide Nadlan header/footer/theme polish and later real tools for yield calculation, property comparison, and professional inquiry.

## New Projects / Contractor Apartment Page Expansion

Updated: 2026-05-28 02:39 Asia/Jerusalem

- Live page upgraded: `https://nad-lan.co.il/new-projects/`.
- Replaced the short 309-word draft-like content with a full consumer-facing guide of 2,506 words.
- Removed public internal wording from both the page body and the WordPress excerpt, including old draft/commercial/lead language.
- Added a realistic construction/project image from Wikimedia Commons, premium guide layout, sections on developer checks, permits, Sales Law protections, payment schedule, construction index exposure, technical specification, delivery delays, purchase tax, mortgage planning, investment use case, warning signs, FAQ, and public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for financial/legal YMYL quality and people-first content.
  - Official `hoc-hamecher.moch.gov.il` Sales Law portal for buyer protections, the 7% threshold, voucher-book/payment route, bank guarantee/insurance protection, and timing of guarantees.
  - Current SERP and competitor review for contractor-apartment guides, including Madlan-style buyer-protection content and real-estate-law office pages that emphasize contract, permit, guarantee, indexation, delivery, specification, and registration checks.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/new-projects/`.
- Rendered H1 count: 1.
- Word count: 2,506.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: cleaned to public buyer-facing text.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 174,066 bytes.
- Screenshot:
  - `verification-screenshots/nadlan-new-projects-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This page now meets the portfolio minimum content gate and is live. It is stronger than the previous draft, especially on buyer protections and contract/payment checks.
- It still needs the same site-wide Nadlan header/footer/theme polish, and later a dedicated new-project inquiry flow with structured project fields such as city, rooms, budget, delivery range, permit status, and financing readiness.

## Buying Apartment Pillar Expansion

Updated: 2026-05-28 02:52 Asia/Jerusalem

- Live page upgraded: `https://nad-lan.co.il/buying-apartment/`.
- Replaced the short 304-word draft-like pillar page with a full consumer-facing guide of 2,057 words.
- Removed public internal wording from both the page body and WordPress excerpt, including old draft/pillar language.
- Added a realistic residential construction image, premium guide layout, buyer journey sections, total-cost planning, mortgage approval, city/neighborhood checks, price comparison, rights/document checks, physical/building checks, purchase-type comparison table, lawyer role, buying timeline, common mistakes, FAQ, and public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for people-first YMYL pages.
  - Bank of Israel mortgage guidance around standardized preliminary approval and comparing mortgage offers.
  - Israel Tax Authority purchase-tax simulator context for transaction-cost planning.
  - Gov.il / Land Registry context for checking registration and rights documents before signing.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/buying-apartment/`.
- Rendered H1 count: 1.
- Word count: 2,057.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: cleaned to public buyer-facing text.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 174,066 bytes after replacing a broken 404 image URL caught during verification.
- Screenshot:
  - `verification-screenshots/nadlan-buying-apartment-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This page now meets the portfolio minimum content gate and is live. It is now a real central buyer pillar instead of a navigation draft.
- The content hierarchy is stronger because it links into checklist, mortgage, purchase tax, Tabu, lawyer, new projects, and investment pages. The next gap is to expand the checklist page and then move the temporary page-level style/chrome into a durable theme/header/footer implementation.

## Apartment Buying Checklist Expansion

Updated: 2026-05-28 03:00 Asia/Jerusalem

- Live page upgraded: `https://nad-lan.co.il/apartment-buying-checklist/`.
- Replaced the short 341-word draft-like checklist with a full consumer-facing guide of 2,109 words.
- Removed public internal wording from both the page body and WordPress excerpt, including old draft/commercial/professional-routing language.
- Added a realistic construction/residential image, premium guide layout, sections on purchase purpose, total budget, mortgage approval, rights documents, contract checks, physical apartment checks, building/surroundings checks, transaction-type checks, red flags, negotiation and final price, document folder, post-signature tracking, FAQ, and public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for people-first YMYL pages.
  - Bank of Israel mortgage transparency guidance around standardized preliminary approval and comparing offers.
  - Israel Tax Authority purchase-tax simulator and official transaction-cost context.
  - Gov.il / Land Registry context for checking rights and registration documents before signing.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/apartment-buying-checklist/`.
- Rendered H1 count: 1.
- Word count: 2,109.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: cleaned to public buyer-facing text.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 174,066 bytes.
- Screenshot:
  - `verification-screenshots/nadlan-buying-checklist-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This page now meets the portfolio minimum content gate and is live. It supports the main buying-apartment pillar with a practical checklist rather than a thin summary.
- The next content gap is likely `tabu-extract-check`, because it is tightly linked to both the buying guide and the checklist. The design gap remains site-wide header/footer/theme polish.

## Tabu Extract / Rights Check Expansion

Updated: 2026-05-28 03:10 Asia/Jerusalem

- Live page upgraded: `https://nad-lan.co.il/tabu-extract-check/`.
- Replaced the short 329-word draft-like page with a full consumer-facing guide of 2,109 words.
- Removed public internal wording from both the page body and WordPress excerpt, including old draft/commercial language.
- Added a realistic residential image, premium guide layout, sections on what a Tabu extract is, what appears in the extract, ownership/right checks, mortgages, warnings, liens, attached parking/storage, when a Tabu extract is not enough, RMI rights approval, new-build cases, common gaps, house-registration documents, seller questions, repeated extract timing, mismatches, document prep for lawyers, FAQ, and public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for people-first YMYL pages.
  - Gov.il official Land Registry service for producing a land-registration extract.
  - Gov.il Ministry of Construction and Housing registration-status service, which distinguishes Tabu extract production from other registration-status inquiries.
  - Gov.il / Israel Land Authority rights-approval service, including the distinction between RMI-managed property and property registered in the Land Registry.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/tabu-extract-check/`.
- Rendered H1 count: 1.
- Word count: 2,109.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: cleaned to public buyer-facing text.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 174,066 bytes.
- Screenshot:
  - `verification-screenshots/nadlan-tabu-extract-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This page now meets the portfolio minimum content gate and is live. It is an important trust page because it anchors the buying/checklist/lawyer cluster in official registration-source logic.
- It still needs a future interactive rights-check intake flow, but the public page no longer exposes internal draft language and now gives a real buyer a usable framework before contacting a lawyer.

## Selling Apartment Pillar Publication

Updated: 2026-05-28 03:24 Asia/Jerusalem

- Live page published: `https://nad-lan.co.il/selling-apartment/`.
- Added a new missing commercial pillar for sellers, instead of reworking an already-passing page.
- Published as a public consumer-facing Hebrew guide of 2,208 words.
- Added the seller page to the live homepage page-level navigation as `מכירה`, so the page is reachable from the public site hierarchy and not only by direct URL.
- Added a realistic residential image, premium guide layout, and sections on pre-sale planning, price setting, rights documents, Tabu / rights checks, capital-gains tax and possible municipal improvement levy, advertising, buyer qualification, negotiation, contract topics, selling while buying, handover, common mistakes, FAQ, internal next-step links, and a public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for people-first YMYL pages.
  - Gov.il Israel Tax Authority Form 7000B page for sale/purchase declaration context, online filing context, and the 30-day declaration timing note.
  - Gov.il Land Registry extract page for Tabu document content and pre-sale/pre-purchase use.
  - Yad2 seller-guide competitor result for seller workflow DNA: pricing, preparation, ad quality, visits, and broker/self-sale decision points.
  - Real-estate-law competitor result patterns for seller legal DNA: rights checks, mortgage removal, tax planning, payment schedule, and final registration documents.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/selling-apartment/`.
- Rendered H1 count: 1.
- Word count: 2,208.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean buyer/seller-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 182,681 bytes.
- Homepage hierarchy check: `https://nad-lan.co.il/` returns HTTP 200 and contains both `/selling-apartment/` and visible `מכירה`.
- Homepage mobile nav check: page-nav labels now include `קנייה`, `מכירה`, `השקעה`, `מקבלן`, `משכנתא`, `מס רכישה`, `טאבו`, `עורך דין`.
- Screenshots:
  - `verification-screenshots/nadlan-selling-apartment-mobile-clean-2026-05-28-top.png`
  - `verification-screenshots/nadlan-home-selling-nav-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new seller pillar is published, verified, and linked from the homepage.
- It improves Nadlan's money architecture by adding the missing seller side of the marketplace: pricing, tax, rights, lawyer, buyer qualification, and handover.
- The durable site-wide gap remains the same: the block-theme header and footer still need a proper theme-level implementation through GitHub plus UPress pull. The homepage page-level navigation is working and verified, but it is still a bridge until the real site chrome is completed.

## Urban Renewal / Pinui Binui Pillar Publication

Updated: 2026-05-28 03:33 Asia/Jerusalem

- Live page published: `https://nad-lan.co.il/urban-renewal/`.
- Added a high-value missing Nadlan pillar for owners and buyers evaluating `התחדשות עירונית`, `פינוי בינוי`, and project risk before signing.
- Published as a public consumer-facing Hebrew guide of 2,088 words.
- Added the urban-renewal page to the live homepage page-level navigation as `התחדשות`, so it is reachable from the public homepage hierarchy.
- Added a realistic urban-renewal image, premium guide layout, and sections on renewal types, owner organization, majority/consent logic, developer checks, appraiser and feasibility questions, buyers evaluating a building with renewal potential, warning signs, agreement terms, document preservation, FAQ, internal next-step links, and a public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for people-first YMYL pages.
  - Gov.il Governmental Urban Renewal Authority declaration service, including requirements such as planning, local authority position, agreements, and special majority references.
  - Gov.il Governmental Urban Renewal Authority appraiser-appointment service, including the public concept of appraiser review for owners evaluating the feasibility of a proposed transaction.
  - Gov.il tenant inquiries commissioner page, especially trust/fairness duties and complaint handling around urban-renewal organizers.
  - Tel Aviv municipal urban-renewal page for public-facing process DNA: transparency, routes, rights, timetable expectations, public space, infrastructure, and resident participation.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/urban-renewal/`.
- Rendered H1 count: 1.
- Word count: 2,088.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean owner/buyer-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 260,775 bytes.
- Homepage hierarchy check: `https://nad-lan.co.il/` returns HTTP 200 and contains both `/urban-renewal/` and visible `התחדשות`.
- Homepage mobile nav check: page-nav labels now include `קנייה`, `מכירה`, `השקעה`, `מקבלן`, `התחדשות`, `משכנתא`, `מס רכישה`, `טאבו`, `עורך דין`.
- Screenshots:
  - `verification-screenshots/nadlan-urban-renewal-mobile-clean-2026-05-28-top.png`
  - `verification-screenshots/nadlan-home-urban-renewal-nav-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new urban-renewal pillar is published, verified, and linked from the homepage.
- It improves Nadlan's money architecture by adding a high-value owner/developer/lawyer/appraiser topic cluster that can later support professional listings and inquiry tools.
- The page meets the minimum content and live verification gates. The remaining gap is a future interactive intake/checklist flow for owners and buyers, plus the same durable theme-level header/footer work through GitHub and UPress pull.

## Property Value / Apartment Valuation Pillar Publication

Updated: 2026-05-28 03:44 Asia/Jerusalem

- Live page published: `https://nad-lan.co.il/property-value/`.
- Added a high-value missing Nadlan pillar for sellers, buyers, investors, mortgage borrowers, and future appraiser/professional workflows.
- Published as a public consumer-facing Hebrew guide of 2,044 words.
- Added the valuation page to the live homepage page-level navigation as `שווי דירה`, so it is reachable from the public homepage hierarchy.
- Added a realistic residential image, premium guide layout, and sections on valuation basics, transaction comparables, differences between asking price and closing price, apartment/building/neighborhood factors, adjustment logic, when to use a real-estate appraiser, quick estimates versus formal valuation, seller use case, buyer use case, investor use case, common mistakes, FAQ, internal next-step links, and a public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for people-first YMYL pages.
  - Gov.il / Israel Tax Authority real-estate information database service for actual transaction-comparison context.
  - CBS housing-price publication pages for official apartment-price index and average-price context.
  - Current valuation/appraiser competitor pages for commercial DNA: transaction comparison, property features, appraisal role, bank/mortgage need, and price-range framing.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/property-value/`.
- Rendered H1 count: 1.
- Word count: 2,044.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean buyer/seller/investor-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 174,066 bytes.
- Homepage hierarchy check: `https://nad-lan.co.il/` returns HTTP 200 and contains both `/property-value/` and visible `שווי דירה`.
- Homepage mobile nav check: page-nav labels now include `קנייה`, `מכירה`, `שווי דירה`, `השקעה`, `מקבלן`, `התחדשות`, `משכנתא`, `מס רכישה`, `טאבו`, `עורך דין`.
- Screenshots:
  - `verification-screenshots/nadlan-property-value-mobile-clean-2026-05-28-top.png`
  - `verification-screenshots/nadlan-home-property-value-nav-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new valuation pillar is published, verified, and linked from the homepage.
- It improves Nadlan's money architecture because valuation is a bridge topic for sellers, buyers, investors, mortgage checks, appraisers, and future property-value tools.
- The page meets the minimum content and live verification gates. The remaining opportunity is to build a real calculator/intake experience later, and to move the temporary page-level homepage nav into durable theme-level header/footer chrome through GitHub and UPress pull.

## Commercial Real Estate Pillar Publication

Updated: 2026-05-28 03:54 Asia/Jerusalem

- Live page published: `https://nad-lan.co.il/commercial-real-estate/`.
- Added a high-value missing Nadlan pillar for investors and business owners evaluating offices, shops, clinics, warehouses, logistics space, and other income-producing commercial assets.
- Published as a public consumer-facing Hebrew guide of 2,083 words.
- Added the commercial real-estate page to the live homepage page-level navigation as `מסחרי`, so it is reachable from the public homepage hierarchy.
- Added a realistic commercial-district image, premium guide layout, and sections on commercial property types, gross versus net yield, tenant and lease checks, legal/use checks, Tax Authority transaction data as a comparison source, financing, owner-occupier purchases, vacancy risk, appraiser/comparable checks, professional team, warning signs, FAQ, internal next-step links, and a public non-advice boundary.
- Research used before editing:
  - Google Search Central helpful content guidance for people-first YMYL pages.
  - Gov.il / Israel Tax Authority real-estate information database service for actual transaction-comparison context.
  - Commercial real-estate competitor pages around offices, shops, warehouses, yield, tenant strength, lease terms, management fees, financing, and professional checks.
  - Current commercial-property investment guides that emphasize net yield, cap-rate-style thinking, vacancy risk, lease review, and area demand.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/commercial-real-estate/`.
- Rendered H1 count: 1.
- Word count: 2,083.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean investor/business-owner-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 163,354 bytes.
- Homepage hierarchy check: `https://nad-lan.co.il/` returns HTTP 200 and contains both `/commercial-real-estate/` and visible `מסחרי`.
- Homepage mobile nav check: page-nav labels now include `קנייה`, `מכירה`, `שווי דירה`, `השקעה`, `מסחרי`, `מקבלן`, `התחדשות`, `משכנתא`, `מס רכישה`, `טאבו`, `עורך דין`.
- Screenshots:
  - `verification-screenshots/nadlan-commercial-real-estate-mobile-clean-2026-05-28-top.png`
  - `verification-screenshots/nadlan-home-commercial-nav-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new commercial-real-estate pillar is published, verified, and linked from the homepage.
- It improves Nadlan's money architecture because commercial property supports investor leads, legal review, appraiser needs, financing needs, management services, and future professional listings.
- The page meets the minimum content and live verification gates. The remaining opportunity is to build a commercial-property intake/calculator flow later, and to move the temporary page-level homepage nav into durable theme-level header/footer chrome through GitHub and UPress pull.

## Professionals Directory / Real Estate Experts Pillar Publication

Updated: 2026-05-28 04:08 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/professionals/`.
- Published as a public consumer-facing Hebrew guide of 2,136 words.
- Added the professionals page to the live homepage page-level navigation as `מקצוענים`, so it is reachable from the public homepage hierarchy.
- Added a realistic commercial-district image, premium guide layout, and sections on why professional help matters, lawyer/appraiser/mortgage-adviser/broker/inspection roles, how to choose a professional, timing by transaction stage, warning signs, coordination between multiple professionals, questions to ask before hiring, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph: real-estate professional directory pages must explain user value first, support lawyers/appraisers/mortgage advisers/brokers/inspectors/tax advisers, include trust fields, and keep commercial operations private.
- Research used before editing:
  - Google Search Central helpful content guidance for people-first pages and E-E-A-T: `https://developers.google.com/search/docs/fundamentals/creating-helpful-content`.
  - Gov.il Land Registry extract service for document/risk context: `https://www.gov.il/he/service/land_registration_extract`.
  - Gov.il / Ministry of Justice disciplinary page for licensed real-estate professionals such as appraisers and real-estate brokers: `https://www.gov.il/he/Departments/units/disciplinary-prosecution`.
  - Live competitor SERP review around real-estate transaction teams, lawyer/appraiser/mortgage adviser coordination, and professional trust pages. The public content is original and adapted to Nadlan's brand.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/professionals/`.
- Rendered H1 count: 1.
- Word count: 2,136.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean buyer/seller/investor-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 163,354 bytes.
- Homepage hierarchy check: `https://nad-lan.co.il/` returns HTTP 200 and contains both `/professionals/` and visible `מקצוענים`.
- Homepage mobile nav check: page-nav labels now include `קנייה`, `מכירה`, `שווי דירה`, `השקעה`, `מסחרי`, `מקבלן`, `התחדשות`, `משכנתא`, `מס רכישה`, `טאבו`, `עורך דין`, `מקצוענים`.
- Screenshots:
  - `verification-screenshots/nadlan-professionals-mobile-clean-2026-05-28-top.png`
  - `verification-screenshots/nadlan-home-professionals-nav-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new professionals pillar is published, verified, and linked from the homepage.
- It improves Nadlan's business architecture because professional selection is the bridge between buyers, sellers, investors, lawyers, appraisers, mortgage advisers, brokers, engineers, and future verified profile pages.
- The page meets the minimum content and live verification gates. The next competitive gap is to build the actual structured professionals index and profile CMS, then move the temporary page-level homepage navigation into durable theme-level header/footer chrome through GitHub and UPress pull.

## Real Estate Appraiser Supporting Professional Page

Updated: 2026-05-28 04:20 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/real-estate-appraiser/`.
- Published as a public consumer-facing Hebrew guide of 2,212 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `שמאי מקרקעין`, so the new page is attached to the content hierarchy instead of living as an orphan URL.
- Added a realistic commercial-district image, premium guide layout, and sections on what a real-estate appraiser does, when to use one before buying, selling, mortgage approval, investment, commercial property, urban renewal, private houses/land, documents to prepare, fee factors, private appraisal versus bank appraisal, warning signs, city/neighborhood questions, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for appraiser pages: use official licensing/registry anchors, distinguish private appraisal from bank appraisal, and make the document checklist practical.
- Research used before editing:
  - Gov.il appraiser registry service and licensing conditions: `https://www.gov.il/he/service/registration_in_land_appraisal_registrar`.
  - Gov.il / Israel Land Authority appraisal unit for government appraisal practice and appraisal use cases: `https://www.gov.il/he/departments/Units/unit-appraisal`.
  - Gov.il Land Registry extract service for Tabu document context: `https://www.gov.il/he/service/land_registration_extract`.
  - Gov.il / Ministry of Justice disciplinary page for licensed real-estate professionals: `https://www.gov.il/he/Departments/units/disciplinary-prosecution`.
  - Live competitor SERP review around Israeli appraiser pages, valuation pages, mortgage-related appraisal, improvement levy, commercial property, and urban renewal. The public content is original and adapted to Nadlan's brand.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/real-estate-appraiser/`.
- Rendered H1 count: 1.
- Word count: 2,212.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean buyer/seller/investor-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 163,354 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/real-estate-appraiser/` and visible `שמאי מקרקעין`.
- Screenshot:
  - `verification-screenshots/nadlan-appraiser-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting professional page is published, verified, and linked from the professionals hub.
- It deepens the professional/directory architecture because valuation connects sellers, buyers, mortgage borrowers, investors, commercial-property checks, and future appraiser profiles.
- The page meets the minimum content and live verification gates. The next gap is still a structured professional-profile CMS and a durable theme-level header/footer implementation through GitHub plus UPress pull.

## Real Estate Broker Supporting Professional Page

Updated: 2026-05-28 04:30 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/real-estate-broker/`.
- Published as a public consumer-facing Hebrew guide of 2,273 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `מתווך נדל״ן`, so the new page is attached to the content hierarchy.
- Added a realistic commercial-district image, premium guide layout, and sections on broker role, seller use case, buyer/renter use case, written brokerage order, brokerage fees, exclusivity, choosing a broker, warning signs, seller preparation, property-visit behavior, fee-dispute prevention, broker as part of the transaction team, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for broker pages: explain licensing, written orders, fees, exclusivity, and dispute prevention without attacking brokers or exposing internal commercial operations.
- Research used before editing:
  - Gov.il broker license and registry service: `https://www.gov.il/he/service/realtor_license`.
  - Gov.il broker-law exam/source material for written brokerage-order requirements and fee entitlement context: `https://www.gov.il/BlobFolder/news/exam_24112024/he/part2.pdf`.
  - Current consumer/competitor pages around brokerage fees, exclusivity, and buyer/seller expectations.
  - Current news/regulatory discussion around broker ethics and consumer complaints, used as a private research signal for trust concerns and not copied into public claims.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/real-estate-broker/`.
- Rendered H1 count: 1.
- Word count: 2,273.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean buyer/seller/renter-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 163,354 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/real-estate-broker/` and visible `מתווך נדל״ן`.
- Screenshot:
  - `verification-screenshots/nadlan-broker-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting broker page is published, verified, and linked from the professionals hub.
- It deepens the future directory architecture because brokers are a natural provider category for buyers, sellers, renters, commercial property, city pages, and future profile pages.
- The page meets the minimum content and live verification gates. The next gap remains structured professional-profile CMS plus durable theme-level header/footer implementation through GitHub and UPress pull.

## Home Inspection / Building Engineer Supporting Professional Page

Updated: 2026-05-28 04:43 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/home-inspection/`.
- Published as a public consumer-facing Hebrew guide of 2,079 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `בדק בית`, so the new page is attached to the content hierarchy.
- Added a realistic construction image, premium guide layout, and sections on what home inspection means, when to order it, inspection report scope, resale apartment checks, new-contractor handover, private-house checks, engineer/inspector selection, document preparation, cost factors, what to do after the report, limits of non-destructive inspection, negotiation use, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for home-inspection pages: explain the physical check, state non-destructive inspection limits, connect findings to lawyer/appraiser/contractor steps, and keep the page practical.
- Research used before editing:
  - Gov.il Ministry of Construction complaint/defect channel for contractor-related defects and public escalation context: `https://www.gov.il/he/service/complaint-about-constractor`.
  - Official Sales Law / contractor-apartment buyer protection context from the Ministry of Construction Sales Law portal: `https://www.gov.il/he/pages/hok_hamecher`.
  - Live competitor pages around בדק בית, engineer inspection, new-apartment handover, dampness, systems, reports, and pricing. The public content is original and adapted to Nadlan's brand.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/home-inspection/`.
- Rendered H1 count: 1.
- Word count: 2,079.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean buyer/new-apartment-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 174,066 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/home-inspection/` and visible `בדק בית`.
- Screenshot:
  - `verification-screenshots/nadlan-home-inspection-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting inspection/engineer page is published, verified, and linked from the professionals hub.
- It deepens the future directory architecture because inspection engineers connect buyer safety, new-project handover, resale-apartment negotiation, contractor defects, and future provider profiles.
- The page meets the minimum content and live verification gates. The next gap remains structured professional-profile CMS plus durable theme-level header/footer implementation through GitHub and UPress pull.

## Real Estate Tax / Tax Adviser Supporting Professional Page

Updated: 2026-05-28 04:52 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/real-estate-tax-advisor/`.
- Published as a public consumer-facing Hebrew guide of 2,221 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `מיסוי מקרקעין`, so the new page is attached to the content hierarchy.
- Added a realistic commercial-district image, premium guide layout, and sections on purchase tax, capital-gains/betterment tax, municipal improvement levy, transaction reporting and approvals, buyer/seller/investor questions, documents to prepare, when to involve a lawyer or tax adviser, inheritance/gift/investment cases, special transactions, common mistakes, integration with mortgage/appraisal/contract, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for real-estate-tax pages: separate the tax types clearly, use official Tax Authority/municipal anchors, connect tax to registration and cashflow, and avoid personal tax conclusions.
- Research used before editing:
  - Israel Tax Authority Form 7000 declaration page and 30-day transaction declaration context: `https://www.gov.il/he/service/real-estate-tax-7000`.
  - Israel Tax Authority buyer/seller guide for real-estate rights: `https://www.gov.il/BlobFolder/generalpage/guide-for-seller-right-in-land/he/Guides_knowrightinland_2022.pdf`.
  - Tel Aviv municipal improvement-levy public explanation as a local authority example: `https://www.tel-aviv.gov.il/Residents/Assets/Pages/ImprovmentTax.aspx`.
  - Current competitor pages around 2026 real-estate taxation, purchase tax, capital-gains/betterment tax, improvement levy, inheritance, gifts, and investment apartments. The public content is original and adapted to Nadlan's brand.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/real-estate-tax-advisor/`.
- Rendered H1 count: 1.
- Word count: 2,221.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean buyer/seller/investor-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 163,354 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/real-estate-tax-advisor/` and visible `מיסוי מקרקעין`.
- Screenshot:
  - `verification-screenshots/nadlan-real-estate-tax-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting real-estate-tax page is published, verified, and linked from the professionals hub.
- It deepens the future directory architecture because tax advice connects buyers, sellers, investors, real-estate lawyers, appraisers, mortgage advisers, and future professional profiles.
- The page meets the minimum content and live verification gates. The next gap remains structured professional-profile CMS plus durable theme-level header/footer implementation through GitHub and UPress pull.

## Construction Supervisor / Engineering Supervision Supporting Professional Page

Updated: 2026-05-28 05:03 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/construction-supervisor/`.
- Published as a public consumer-facing Hebrew guide of 2,042 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `מפקח בנייה`, so the new page is attached to the content hierarchy.
- Added a realistic construction image, premium guide layout, and sections on what a construction supervisor does, when supervision is useful, the difference between home inspection and ongoing supervision, new-contractor apartments, urban-renewal tenant supervision, private construction/major renovation, choosing a supervisor, agreement scope, reports, documents to prepare, conflict-of-interest checks, cost factors, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for construction-supervisor pages: explain supervision versus point-in-time inspection, cover contractor apartments/private construction/urban renewal, define report scope, and make conflict-of-interest checks explicit.
- Research used before editing:
  - Official new-apartment buyer guide with Sales Law inspection/warranty context: `https://www.gov.il/BlobFolder/guide/new_apartment_buyer/he/documents_chok_hamecher_madrich-lerochesh-dira.pdf`.
  - Official Sales Law / contractor-apartment buyer protection context from the Ministry of Construction Sales Law portal: `https://www.gov.il/he/pages/hok_hamecher`.
  - Live competitor pages around tenant-side construction supervision, urban-renewal supervision, engineering supervision, scope, reports, and selection criteria. The public content is original and adapted to Nadlan's brand.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/construction-supervisor/`.
- Rendered H1 count: 1.
- Word count: 2,042.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean owner/new-apartment-facing text, no old internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 174,066 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/construction-supervisor/` and visible `מפקח בנייה`.
- Screenshot:
  - `verification-screenshots/nadlan-construction-supervisor-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting construction-supervision page is published, verified, and linked from the professionals hub.
- It deepens the future directory architecture because construction supervisors connect buyers of new apartments, owners in urban-renewal projects, private builders, renovation clients, inspection engineers, and future provider profiles.
- The page meets the minimum content and live verification gates. The next gap remains structured professional-profile CMS plus durable theme-level header/footer implementation through GitHub and UPress pull.

## Public Excerpt Cleanup / Hidden Internal Language Remediation

Updated: 2026-05-28 05:27 Asia/Jerusalem

- Live public WordPress excerpts were cleaned for four older Nadlan pages that still contained early internal wording even though the visible bodies had already been upgraded:
  - `https://nad-lan.co.il/real-estate-lawyer/`
  - `https://nad-lan.co.il/investment-apartment/`
  - `https://nad-lan.co.il/mortgage-advisor/`
  - `https://nad-lan.co.il/purchase-tax-calculator/`
- Each excerpt is now short public-facing Hebrew that explains the reader benefit without internal operating language.
- Saved a repeatable skill lesson in the Codex portfolio knowledge graph: always inspect `excerpt.rendered` after publishing or rewriting, because old excerpt text can leak into feeds, REST, theme cards, social snippets, or future search snippets.
- Research checked before this cleanup:
  - Google people-first content guidance: `https://developers.google.com/search/docs/fundamentals/creating-helpful-content`.
  - WordPress REST page endpoint behavior was verified operationally through the live `/wp-json/wp/v2/pages` response.

### Live Verification

- REST excerpt verification: all four affected pages now return clean public Hebrew excerpts.
- `https://nad-lan.co.il/real-estate-lawyer/`: quality gate passed, 2,101 words, one H1, one image, no blocked internal terms.
- `https://nad-lan.co.il/investment-apartment/`: quality gate passed, 2,098 words, one H1, one image, no blocked internal terms.
- `https://nad-lan.co.il/mortgage-advisor/`: quality gate passed, 2,131 words, one H1, one image, no blocked internal terms.
- `https://nad-lan.co.il/purchase-tax-calculator/`: quality gate passed, 2,133 words, one H1, one image, no blocked internal terms.

### Honest Gap Statement

- This was not a new page publication, but it was a real live public cleanup: four existing live pages no longer expose old internal language through WordPress excerpts.
- It directly fixes the type of issue Ben flagged earlier: public pages must speak only to buyers, sellers, borrowers, investors, and property owners.
- Remaining gap: continue excerpt/meta checks across every older page and move durable header/footer improvements into the synced theme with UPress Git pull verification.

## Architect / Building Permit Supporting Professional Page

Updated: 2026-05-28 05:31 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/architect-building-permit/`.
- Published as a public consumer-facing Hebrew guide of 2,340 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `אדריכל והיתר בנייה`, so the new page is attached to the content hierarchy.
- Added a realistic architecture/plans image, premium guide layout, and sections on what an architect does, architect versus interior designer, permit basics, choosing an architect, registration/licensing checks, proposal scope, buying before renovation, large renovations, urban renewal, documents to prepare, warning signs, cost factors, efficient collaboration, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for architect/building-permit pages: separate design, permit, engineering, legal, appraisal, and supervision roles; cover documents, proposal scope, consultants, warning signs, and no guarantee of permit approval.
- Research used before editing:
  - Official engineer/architect registration context from gov.il: `https://www.gov.il/he/service/registration-of-engineers-and-architects`.
  - Official Planning Administration / licensing-permit context around `רישוי זמין`, permit applications, and the role of an application editor.
  - Live competitor pages around architect selection, building permits, renovation planning, cost factors, permit scope, and questions to ask. The public content is original and adapted to Nadlan's brand.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/architect-building-permit/`.
- Rendered H1 count: 1.
- Word count: 2,340.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean owner/buyer/renovator-facing text, no internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 89,809 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/architect-building-permit/` and visible `אדריכל והיתר בנייה`.
- Screenshot:
  - `verification-screenshots/nadlan-architect-mobile-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting architect/building-permit page is published, verified, and linked from the professionals hub.
- It deepens the future directory architecture because architects connect buyers of renovation properties, private builders, owners seeking extensions, urban-renewal residents, commercial-property users, appraisers, lawyers, engineers, and construction supervisors.
- The page meets the minimum content and live verification gates. The next gap remains a structured provider-profile CMS and a durable theme-level header/footer implementation through GitHub and UPress pull.

## Property Management Supporting Professional Page

Updated: 2026-05-28 05:39 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/property-management/`.
- Published as a public consumer-facing Hebrew guide of 2,113 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `ניהול נכסים`, so the new page is attached to the content hierarchy.
- Added a realistic building image, premium guide layout, and sections on what property management includes, when it fits owners/investors, broker versus management company, choosing a company, management contract scope, tenant/contract/guarantees, maintenance, performance checks, pricing models, remote owners, warning signs, quarterly owner review, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for property-management pages: explain tenant screening, lease coordination, guarantees, rent collection, maintenance, reporting, vacancy handling, renewals, repair approval thresholds, and owner reporting cadence.
- Research used before editing:
  - Gov.il lease-registration context: `https://www.gov.il/he/service/registration_of_a_lease`.
  - Tel Aviv public rental-contract guidance: `https://www.tel-aviv.gov.il/Residents/Assets/Pages/rent.aspx`.
  - Live competitor pages around management companies, apartment management, investor services, maintenance, rent collection, owner reporting, pricing, and remote owners. The public content is original and adapted to Nadlan's brand.

### Live Verification

- First quality gate caught a useful issue: the first version was clean but only 1,974 words, below the 2,000-word minimum. The page was expanded before reporting.
- Final quality gate: passed.
- URL: `https://nad-lan.co.il/property-management/`.
- Rendered H1 count: 1.
- Word count: 2,113.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean owner/investor-facing text, no internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 163,354 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/property-management/` and visible `ניהול נכסים`.
- Screenshot:
  - `verification-screenshots/nadlan-property-management-mobile-clean-2026-05-28-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting property-management page is published, verified, and linked from the professionals hub.
- It deepens the future directory architecture because property management connects investors, owners, rental apartments, commercial property, brokers, lawyers, tax advisers, maintenance professionals, and future recurring service profiles.
- The live check initially failed the word-count minimum, and I corrected it before reporting completion. The next gap remains structured provider profiles plus durable theme-level header/footer implementation through GitHub and UPress pull.

## Mortgage / Home Insurance Supporting Professional Page

Updated: 2026-05-28 05:54 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/mortgage-home-insurance/`.
- Published as a public consumer-facing Hebrew guide of 2,493 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `ביטוח משכנתא ודירה`, so the new page is attached to the content hierarchy.
- Added a realistic Israeli business/residential skyline image, premium guide layout, sections on mortgage insurance, life insurance, building insurance, home contents, bank requirements, independent insurance choice, policy comparison, rental/investment apartments, documents to prepare, renewal checks, common mistakes, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for mortgage/home-insurance pages: separate bank-required mortgage cover from wider home cover, explain beneficiary/bank approval issues, compare price only after matching coverage, cover rental-property context, and always verify WordPress excerpts.
- Research used before editing:
  - Kol Zchut mortgage-insurance public guide: `https://www.kolzchut.org.il/he/ביטוח_משכנתא`.
  - Ministry of Finance / `האוצר שלי` apartment-insurance comparison guide: `https://haotzarsheli.mof.gov.il/Subject/Pages/Choosing-Apartment-Insurance.aspx`.
  - Bank Hapoalim mortgage life/building insurance page: `https://www.bankhapoalim.co.il/he/mortgage/building-insurance-and-life-insurance`.
  - Discount Bank mortgage-insurance guide and current competitor pages around mortgage insurance, home insurance, policy comparison, exclusions, service, and claims. The public content is original and adapted to Nadlan's brand.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/mortgage-home-insurance/`.
- Rendered H1 count: 1.
- Word count: 2,493.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean buyer/borrower-facing text, no internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 163,354 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/mortgage-home-insurance/` and visible `ביטוח משכנתא ודירה`; duplicate CTA was caught and removed before reporting.
- Screenshot:
  - `verification-screenshots/nadlan-mortgage-home-insurance-mobile-clean-2026-05-28-v2-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting mortgage/home-insurance page is published, verified, and linked from the professionals hub.
- The first mobile screenshot showed the image too low in the first viewport and the hub temporarily had a duplicate button; both issues were corrected before reporting completion.
- It deepens the future directory architecture because insurance connects mortgage borrowers, homeowners, investors, property managers, lawyers, mortgage advisers, and future insurance-professional profile pages.
- The page meets the minimum content and live verification gates. The next gap remains structured provider profiles plus durable theme-level header/footer implementation through GitHub and UPress pull.

## Renovation Contractor Supporting Professional Page

Updated: 2026-05-28 06:09 Asia/Jerusalem

- Live page published and verified: `https://nad-lan.co.il/renovation-contractor/`.
- Published as a public consumer-facing Hebrew guide of 2,382 words.
- Linked from the existing professionals hub at `https://nad-lan.co.il/professionals/` with the public label `קבלן שיפוצים`, so the new page is attached to the content hierarchy.
- Added a realistic Israeli construction image, premium guide layout, and sections on renovation before/after buying, contractor registry checks, preparing a scope, comparing quotes, cost factors, contracts, architects/supervisors, rental/investment renovation, warning signs, project conduct, FAQ, internal next-step links, and a public non-advice boundary.
- Saved a new repeatable skill lesson in the Codex portfolio knowledge graph for renovation-contractor pages: connect renovation to property economics, use official registrar anchors, compare quotes only after matching scope, define payment milestones, avoid operational wording such as supplier language, and always verify excerpts.
- Research used before editing:
  - Ministry of Construction contractor registrar: `https://www.gov.il/he/departments/units/contractors_registrar_and_head_of_sales_laws_moch`.
  - Official contractor registry: `https://www.gov.il/apps/moch/rasham/home`.
  - Current renovation-guide and price-guide competitors around contractor selection, quote comparison, payment milestones, reserves, materials, defects, and handover.

### Live Verification

- Quality gate: passed.
- URL: `https://nad-lan.co.il/renovation-contractor/`.
- Rendered H1 count: 1.
- Word count: 2,382.
- Image count: 1.
- Blocked internal terms: none.
- WordPress excerpt: clean owner/buyer/investor-facing text, no internal wording.
- Mobile 390px rendered check: no horizontal overflow, one H1, public terms clean.
- Image URL check: Wikimedia image returns `image/jpeg` and `Content-Length` 174,066 bytes.
- Professionals hub hierarchy check: `https://nad-lan.co.il/professionals/` returns HTTP 200 and contains both `/renovation-contractor/` and visible `קבלן שיפוצים`.
- Screenshot:
  - `verification-screenshots/nadlan-renovation-contractor-mobile-clean-2026-05-28-v2-top.png`

### Honest Gap Statement

- This is a real live publication, not a draft: a new supporting renovation-contractor page is published, verified, and linked from the professionals hub.
- The first mobile verifier caught the word `ספקים`; even though it was used in an ordinary renovation context, I removed it before reporting to keep Ben's public/private language standard strict.
- It deepens the future directory architecture because renovation contractors connect old-apartment purchases, rental upgrades, property-management maintenance, home inspection, architects, construction supervisors, appraisers, brokers, and future contractor-profile pages.
- The page meets the minimum content and live verification gates. The next gap remains structured provider profiles plus durable theme-level header/footer implementation through GitHub and UPress pull.
