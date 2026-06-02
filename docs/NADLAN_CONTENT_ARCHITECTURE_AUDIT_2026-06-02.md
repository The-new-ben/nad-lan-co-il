# Nadlan Content Architecture Audit - 2026-06-02

Codex stamp: 2026-06-02, audit-only block after the user allowed small corrections/additions but not full article writing.

No full articles were written. No live WordPress content was published in this block. The work was live crawling, visual verification, architecture analysis, recommendations, and skill preservation.

## Research and Skills Used

- Google Search Central, helpful people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search Central, SEO starter guide and site structure/internal links: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google Search Central, faceted navigation and crawl management: https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation
- Google Search Central, structured data introduction: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Google Search Central, generative AI content guidance: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- Local skills used: `nadlan-real-estate-growth`, `seo`, `seo-content`, `skill-creator`.
- Previous Nadlan knowledge read: Lovable competitor scan, money page briefs, live publication report, non-article maintenance stamp, pasted CloudCraft/Opus context.

## Evidence Collected

Raw evidence file: `docs/nadlan-content-audit-data-2026-06-02.json`

Audit crawler added: `scripts/nadlan-content-architecture-audit-20260602.mjs`

Fresh screenshots:

- `verification-screenshots/nadlan-audit-home-mobile-2026-06-02-top.png`
- `verification-screenshots/nadlan-audit-professionals-mobile-2026-06-02-top.png`
- `verification-screenshots/nadlan-audit-projects-mobile-2026-06-02-top.png`

Live inventory found:

| Surface | Sitemap count | REST count | Notes |
| --- | ---: | ---: | --- |
| Pages | 100 | 100 | Most long-form content lives here. |
| Products | 6 | 5 | WooCommerce exists but is not yet a strong visible revenue journey. |
| Glossary terms | 23 | 22 | Term pages sampled as strong, archive weaker. |
| Projects | 942 | 941 | Large generated entity set. |
| Professionals | 2,703 | 2,702 | Large generated entity set. |
| Product categories | 1 | n/a | Minor. |
| Term categories | 5 | n/a | Minor. |
| Custom hub sitemap | listed | n/a | `https://nad-lan.co.il/sitemap-nadlan-hubs.xml` timed out in the audit check. |

Technical crawl signals:

- `https://nad-lan.co.il/robots.txt` now returns HTTP 200 with `Allow: /` and the Yoast sitemap URL. The previous robots 404 is resolved.
- 185 sampled public URLs returned HTTP 200.
- Visible internal/private terms in sampled page text: 0.
- Multi-H1 pages in sample: 48. Main causes: professional profiles, archive templates, and one short-term rental page.
- Missing canonical in sample: 62. Main causes: sampled project and professional entity pages.
- Missing image alt in sample: 0 by crawler.

## Honest Verdict

The long-form guide layer is real now. Many money pages are above 2,000 Hebrew words and cover expensive user decisions: buying, selling, mortgage, purchase tax, valuation, lawyer checks, appraiser, broker, urban renewal, investment, commercial real estate, and luxury location price guides.

This is not yet a guaranteed 1-2 year competitor killer. With age and links, the content can win meaningful long-tail and mid-tail rankings, especially where official-source explanations and checklists are strong. It is not yet likely to beat Yad2/Madlan/Nadlan.gov-level results on the hardest terms because the site still lacks three things: unique data depth, directory/profile trust depth, and a premium homepage/directory experience that makes the whole ecosystem obvious.

My honest score today:

- Long-form guide content depth: 78/100.
- Hub/spoke clarity: 63/100.
- Directory/entity quality: 46/100.
- Homepage as revenue/navigation command center: 55/100.
- Googlebot crawl discipline: 58/100.
- AI/GEO answer readiness: 68/100.
- Revenue journey readiness: 52/100.

## User Journey

### Buyer Journey

Current good path: homepage -> buying guide -> checklist -> purchase tax/mortgage/property value/lawyer/appraiser.

Gap: the journey is article-heavy. It needs a clearer transaction dashboard: budget, city, apartment type, stage, risk flags, and next professional. The homepage should feel like "start a safe property decision" rather than only a guide index.

Needed small additions:

- Add "where are you in the transaction?" entry points on homepage and buying pages.
- Make the form outcome clearer: estimate, checklist, professional match, or project inquiry.
- Add a visible "official checks" route: Tabu, planning, tax, mortgage approval, inspection.

### Seller Journey

Current good path: selling guide -> pricing apartment -> property value -> lawyer/tax/broker.

Gap: not enough direct seller tools. The seller needs valuation, tax exposure, pricing plan, marketing plan, broker/no-broker comparison, and document checklist.

Suggested content opportunities:

- Seller preparation hub: documents, valuation, tax, listing, negotiation.
- "How to price an apartment before listing" as a tool-backed page.
- "Selling inherited property" and "selling after divorce/separation" as high-intent legal/tax pages.
- "Capital gains before selling: decision tree" as a visual guide.

### Investor Journey

Current good path: investment hub -> investment apartment -> yield/cashflow/leverage/company/Airbnb/short-term-rental country pages.

Gap: there are two strong investment hubs that can overlap if not clearly separated:

- `/investment/`: broad strategy hub for real-estate investment in Israel.
- `/investment-apartment/`: deal-check page before buying one investment apartment.
- `/investment/apartments-for-investment/`: asset selection and location choices.

Required architecture rule: each investment page needs one parent job, one primary query family, and cross-links that explain "continue to" rather than competing for the same phrase.

Suggested content opportunities:

- "Best cities for investment apartment in Israel: data method and risks".
- "Small apartment vs larger apartment for investment".
- "New project vs second-hand apartment for investment".
- "Short-term rental vs long-term rental in Israel".
- "Investor due diligence checklist before signing".

### Professional/Provider Journey

Current good path: homepage links to professionals; `join-pro` exists; 2,702 professional URLs are exposed.

Major gap: the live `/professionals/` URL behaves like a thin archive with about 466 words and two H1s. The REST page inventory contains a stronger 2,113-word `/professionals/` page, but the live URL appears to be occupied by the archive template. This means the stronger guide content may be hidden from users and Google at the exact commercial directory route.

Required correction:

- Either merge the strong guide content into the archive top, or move the guide to a separate canonical URL such as `/choosing-real-estate-professionals/` and make `/professionals/` a proper directory landing page.

Suggested content opportunities:

- City/profession landing pages only where useful: real-estate lawyer in Tel Aviv, appraiser in Herzliya, broker in Ramat Hasharon, construction inspector in new projects.
- Professional profile upgrade blocks: license/source, specialties, service area, languages, typical documents reviewed, questions to ask, review/update date, and verified public-source note.
- Provider monetization pages: professional profile upgrade, project listing, featured placement, verified badge. Keep public wording trust-first, not internal monetization language.

## Googlebot Journey

### Strong Signals

- Robots file is now valid.
- Main sitemap index is live.
- 100 pages and many long-form guides are crawlable.
- Most sampled guide pages return 200 and have one H1.
- Internal public wording has been cleaned in the sampled text.

### Weak Signals

1. Custom hub sitemap timeout.
   - `https://nad-lan.co.il/sitemap-nadlan-hubs.xml` is listed but timed out.
   - Fix or remove it from the sitemap index. A stale/unresponsive sitemap is a trust and crawl reliability issue.

2. Archive/template H1 duplication.
   - `/professionals/`, `/projects/`, `/properties/`, and many professional profiles show multiple H1s.
   - Professional profiles often repeat the same name twice as H1.

3. Missing viewport meta on archive templates.
   - Homepage has `<meta name="viewport" content="width=device-width, initial-scale=1" />`.
   - `/professionals/` and `/projects/` did not expose a viewport meta tag in the HTML check.
   - The headless verifier rendered these archive pages as a 980px wide layout on mobile.

4. Missing canonical on custom entity pages.
   - 62 sampled URLs lacked a canonical. Grouping showed 43 professionals and 19 projects.
   - This is especially important because the project/professional pages are large generated sets.

5. Thin indexable archives.
   - `/projects/`: about 185 rendered words, two H1s.
   - `/properties/`: about 68 rendered words, two H1s.
   - `/catalog/`: visually and semantically not yet strong enough for a marketplace hub.

6. Large generated entity inventory before unique value.
   - 2,702 professionals and 941 projects are valuable for revenue, but profile/project pages around 280-420 words look templated.
   - That can be useful for users if filtered well, but it is not yet a strong answer page for Google.

## AI/GEO Journey

AI systems need extractable, attributed, specific answers. The strongest guide pages already have a good base: headings, tables, official-source references, and long explanatory sections.

Gaps:

- Many pages still need concise "answer blocks" near the top: price range, what to check, documents needed, who to consult, and official sources.
- Entity pages need stable facts: city, professional type, license/source, services, contact path, last verified date.
- Project pages need unique project facts: city, street, status, plan source, developer, risk checklist, nearby guides, and public documents where available.
- Homepage needs a clearer entity map: guides, tools, professionals, projects, glossary, city/price guides.

AI-readiness principle: every important page should answer one clear question in the first screen and then prove it with structure, sources, and internal links.

## Content Architecture Assessment

### Pillars That Look Strong

- Buying apartment.
- Selling apartment.
- Investment.
- Mortgage calculator/advisor/refinance.
- Purchase tax and real-estate tax.
- Property value and valuation estimator.
- Real-estate lawyer.
- New projects.
- Urban renewal.
- Commercial real estate.
- Premium/luxury price guides.

### Pillars Needing Better Parent Hubs

- Mortgage needs a true `/mortgage/` hub. Today homepage points strongly to the calculator, but the cluster includes advisor, refinance, insurance, rates, repayment capacity, and reverse mortgage.
- Price guides need a visible `/price-guides/` or stronger `/property-value/` hub that maps city/neighborhood/luxury guides and prevents same-looking price pages from drifting.
- Professionals need a real directory hub that does not hide the stronger guide page behind a thin archive.
- Projects need a better `/projects/` hub with city/status/type segmentation.
- Glossary needs an improved archive, even though individual term pages are strong.

### Cannibalization Risks

These are not fatal, but they need explicit page jobs:

- `/investment/`, `/investment-apartment/`, `/investment/apartments-for-investment/`, yield, leverage, Airbnb, and short-term-rental pages.
- `/property-value/` and `/property-value-estimator/`.
- `/mortgage-calculator/`, `/mortgage-advisor/`, `/mortgage-refinance/`, `/mortgage-calculator/mortgage-interest-rates/`, and repayment capacity pages.
- `/real-estate-tax-advisor/`, purchase tax calculator, purchase tax first home, purchase tax investor, capital gains pages.
- Tel Aviv price guide variants: base Tel Aviv, luxury, penthouse, seafront, Neve Tzedek.

Rule to apply: each cluster should have one parent hub, one primary query target per page, and descriptive internal links that show why the next page is different.

## Glossary Findings

The individual glossary terms sampled are strong: 200 status, one H1, and around 2,900 rendered words. The cards did not redirect to the wrong root in the sample; links pointed to `/glossary/{term}/`.

The archive is weak in a different way:

- Title is default-like: "Archive NadLan Glossary".
- H1 is archive-like rather than user-facing.
- It repeats generic headings such as definition/practical meaning/common mistake across many terms.
- Each term appears linked more than once on the archive.

Recommendation: keep term pages indexable if they remain high quality, but redesign `/glossary/` as an entity map:

- Search/filter by topic: tax, legal, planning, mortgage, investment, project.
- Alphabetical index.
- "Popular before signing" section.
- Internal links from every term to 2-4 real decision guides.
- Breadcrumb and canonical discipline.

## Homepage Findings

Homepage positives:

- One H1.
- Clean mobile screenshot, no horizontal overflow.
- Clear counts for professionals, terms, projects.
- Public language is consumer-facing.

Homepage gaps:

- No visible hero image or property/data visual in the audit screenshot.
- It reads like a clean guide/tool entry, not yet a premium real-estate intelligence product.
- It should better expose the full ecosystem: guides, tools, price/city data, professionals, projects, glossary.
- Header labels were not detected by the verifier, likely because mobile menu is collapsed and not opened in this script. Still, the first viewport should show stronger category direction.

Recommended homepage model:

1. Search/decision console: "What are you trying to do?"
2. Three user paths: buy, sell, invest.
3. Tool row: mortgage, purchase tax, valuation, deal checklist.
4. Market data row: price guides by city/neighborhood/luxury.
5. Professional directory row: lawyer, appraiser, broker, inspector, mortgage adviser.
6. Projects row: new projects and urban renewal by city.
7. Authority row: official sources, editorial policy, update process.

## Small Corrections Allowed Now

These are not full article writing:

1. Fix duplicate H1 in custom archive/profile templates.
2. Add viewport meta to custom archive templates.
3. Add or restore canonical tags on project and professional entity pages, or noindex low-value generated pages until enriched.
4. Fix the `/professionals/` route conflict so the strong professional guide content is not hidden.
5. Rename default archive titles: avoid "Archive NadLan Projects" and "Archive NadLan Glossary" in public titles.
6. Strengthen thin archives with short intro, filters explanation, trust language, and links to relevant guides.
7. Fix `sitemap-nadlan-hubs.xml` timeout or remove it from sitemap index.
8. Add small source/update blocks to directories and profiles.
9. Add glossary archive search/categories and remove duplicate card links.
10. Hide/noindex WooCommerce utility pages if they are not meant to rank: cart, checkout, account, shop.

## Suggested New Content and Content Assets

No articles were written in this block. These are recommended targets.

### Highest Revenue Priority

- Mortgage hub: `/mortgage/`
- Price guide hub: `/price-guides/`
- Professionals directory hub route fix: `/professionals/`
- Projects by city/status hub: `/projects/{city}/`
- Urban renewal by city: `/urban-renewal/{city}/`
- Professional city pages: lawyer/appraiser/broker/inspector/mortgage adviser by city, only for useful cities.

### Buyer Content

- First apartment buying hub.
- New project purchase checklist with bank guarantee and delivery delay checks.
- Apartment inspection checklist before contract.
- Tabu, shared house, warning note, lien, and easement guides.
- Buying with parents/help from family.

### Seller Content

- Seller document checklist.
- How to price an apartment before listing.
- Selling inherited property.
- Selling after divorce/separation.
- Selling apartment with mortgage still open.
- Betterment levy before sale by city/asset type.

### Investor Content

- Best cities for investment apartment in Israel with transparent data method.
- New project vs second-hand apartment for investment.
- Small apartment vs family apartment yield comparison.
- Short-term vs long-term rental in Israel.
- Company purchase vs private purchase decision tree.
- Investor tax checklist before signing.

### Directory and Social-Network Content

- Verified professional profiles with service areas, specialties, public-source/license notes, reviews, questions to ask, and last verified date.
- Professional comparison pages: appraiser vs inspector, lawyer vs tax adviser, broker vs buyer representative.
- Project comparison pages by city and stage.
- Review/request journey pages: "ask three professionals", "compare offers", "prepare documents".
- Provider education pages: how professionals join, verification process, profile upgrade, project listing.

### AI/GEO Assets

- Short answer blocks for every main guide.
- Tables with official-source citations.
- "Last reviewed" and "source checked" boxes.
- FAQ content as page content, not necessarily FAQ schema for Google rich results.
- Glossary term snippets linked into relevant guides.

## Next Work Plan

1. Fix template-level issues first: viewport, H1 duplication, archive titles, canonical/noindex strategy.
2. Resolve the `/professionals/` route conflict.
3. Decide index/noindex rules for generated project/professional pages.
4. Redesign homepage as a real-estate decision console.
5. Build a parent hub map for mortgage, price guides, professionals, projects, investment.
6. Only then resume full article writing.

## Final Honesty Statement

The site has moved from draft-stage content to a real content base. The long-form guides are no longer the main weakness. The main weakness is that the site now exposes a large database and many routes without enough template, canonical, hierarchy, and directory-product discipline. If those structural issues are fixed and the entity pages are enriched with trust and unique data, the site can become a serious SEO/revenue asset. If they are not fixed, Google may see the strongest articles as good isolated pages while treating the large directory layer as boilerplate.
