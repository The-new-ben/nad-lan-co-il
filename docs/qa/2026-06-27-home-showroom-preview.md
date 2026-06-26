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
npm run qa:home-showroom-preview
npm run qa:home-showroom-pattern
```

Expected:

- 4 Chrome screenshots: desktop, tablet, mobile, Edge-mobile UA.
- One H1.
- At least 5 language entries.
- 4 real language target sections.
- 4 buyer-path cards.
- At least 3 project cards.
- Project section visible in the first viewport.
- No horizontal overflow.
- No public internal wording.
- No mojibake.

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

- Desktop project section starts at 656.94px.
- Mobile project section starts at 863.22px, inside the first 900px viewport.
- Desktop buyer-path cards: 4.
- Desktop language target sections: 4.
- Minimum checked public tap target: 34px.
- Failures: 0.
- Pattern gate: PASS, `docs/qa/home-showroom-pattern-report.json`.
- Homepage template placement gate: PASS. `templates/home.html` now uses `nadlan-revenue/nadlan-home-showroom` and no longer uses the default blog/query-loop patterns.
- PHP lint: `patterns/nadlan-home-showroom.php` and `functions.php` clean.
- JS syntax: `assets/js/nadlan-showroom-engine.js`, `scripts/qa-home-showroom-preview.mjs`, and `scripts/qa-home-showroom-pattern.mjs` clean.

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
