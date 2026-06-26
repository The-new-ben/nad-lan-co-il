# Home Showroom Preview QA, 2026-06-27

## Scope

This slice adds a verified homepage preview that places the multi-project showroom directly after the first hero/search band. It is intentionally not at the absolute top: the page first explains the buyer promise, then presents project comparison and apartment selection before long content.

## Research Anchors

- [Zillow](https://www.zillow.com/): homepage navigation centers buyer/renter/search tasks and property tools.
- [Rightmove](https://www.rightmove.co.uk/): homepage presents buy/rent/sold search paths plus valuation, guides and overseas paths.
- [Madlan](https://www.madlan.co.il/): Israeli homepage exposes sale/project/search links, popular city searches, prices and neighborhood/listing signals.
- [Google Search Central localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions): multilingual versions should become crawlable localized URLs with reciprocal `hreflang`; this preview only shows language entry points until full translated pages exist.

## Buyer-Language Decisions

- Public copy speaks to buyers, families and foreign investors.
- No public wording about internal systems, funnel language, CMS, strategy or monetization.
- The first screen includes: one H1, search fields, language entry points, and the multi-project project cards.
- The project engine reuses `assets/engine/projects.json` so Rainbow, Dimri Yama and Ashira remain one data source.

## Chrome Gate

Run:

```bash
npm run qa:home-seo-schema
npm run qa:home-chrome
npm run qa:home-showroom-preview
npm run qa:home-showroom-pattern
```

Expected:

- 4 Chrome screenshots: desktop, tablet, mobile, Edge-mobile UA.
- One H1.
- Premium header has at least 7 real-estate routes.
- Footer has at least 20 buyer, area, tool, language and legal links.
- At least 5 language entries.
- 4 real language target sections.
- 4 buyer-path cards.
- At least 3 project cards.
- Project section visible in the first viewport.
- No horizontal overflow.
- No public internal wording.
- No default theme chrome wording such as Blog, Shop, Patterns, Themes or WordPress credit.
- No mojibake.
- Homepage title, description and JSON-LD are present and buyer-facing.

## Result

Status: PASS.

Report:

- `docs/qa/screenshots/home-showroom-preview-2026-06-27/report.json`

Screenshots:

- `docs/qa/screenshots/home-showroom-preview-2026-06-27/desktop-1440-home.png`
- `docs/qa/screenshots/home-showroom-preview-2026-06-27/tablet-768-home.png`
- `docs/qa/screenshots/home-showroom-preview-2026-06-27/mobile-390-home.png`
- `docs/qa/screenshots/home-showroom-preview-2026-06-27/edge-mobile-390-home.png`

Measured:

- Desktop project section starts at 677.94px.
- Mobile project section starts at 757.25px, inside the first 900px viewport.
- Header routes: 7.
- Footer links: 23.
- Desktop buyer-path cards: 4.
- Desktop language target sections: 4.
- Minimum checked public tap target: 34px.
- Homepage SEO title length: 53.
- Homepage meta description length: 130.
- Homepage JSON-LD schema types: Organization, WebSite, SearchAction, WebPage, ItemList, ListItem.
- Homepage JSON-LD project list items: 3.
- Failures: 0.
- SEO/schema gate: PASS, `docs/qa/home-seo-schema-report.json`.
- Header/footer chrome gate: PASS, `docs/qa/home-chrome-report.json`.
- Pattern gate: PASS, `docs/qa/home-showroom-pattern-report.json`.
- Homepage template placement gate: PASS. `templates/home.html` now uses `nadlan-revenue/nadlan-home-showroom` and no longer uses the default blog/query-loop patterns.
- Premium header/footer patterns: PASS. `patterns/header.php` and `patterns/footer.php` now use explicit NadLan routes instead of a saved empty menu or default WordPress footer links.
- PHP lint: `patterns/header.php`, `patterns/footer.php`, `patterns/nadlan-home-showroom.php` and `functions.php` clean.
- JS syntax: `assets/js/nadlan-showroom-engine.js`, `scripts/qa-home-chrome.mjs`, `scripts/qa-home-showroom-preview.mjs`, `scripts/qa-home-showroom-pattern.mjs`, and `scripts/qa-home-seo-schema.mjs` clean.

Honesty note: this is a preview and QA standard, not a live homepage deployment. The language entries are visible navigation affordances; full multilingual SEO still requires separate translated pages and reciprocal `hreflang` once those pages exist.

## Theme Pattern

The verified composition now has a reusable theme pattern:

- `patterns/nadlan-home-showroom.php`

The pattern is content-only and does not duplicate the site header. The branch homepage template now places this pattern between the normal header and footer. The theme asset loader detects `data-nle-home-showroom` or the homepage template placement and enqueues:

- `assets/css/nadlan-showroom-engine.css`
- `assets/css/nadlan-home-showroom.css`
- `assets/js/nadlan-showroom-engine.js`

The engine reads project data from the pattern root via `data-nle-projects`, so the same project JSON remains the source of truth.

This is not deployed live. The next controlled step before production is a live-equivalent WordPress render check after the branch is installed or previewed in WordPress.
