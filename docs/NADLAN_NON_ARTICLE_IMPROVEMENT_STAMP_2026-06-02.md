# Nadlan Non-Article Improvement Stamp - 2026-06-02

Codex stamp: 2026-06-02, live non-article maintenance block.

Scope: improve live Nadlan presentation, metadata hygiene, and reusable skills without writing new articles or changing article body content.

## Skills and Knowledge Read

- `portfolio-wordpress-seo-publisher`: live verification, no internal public language, excerpt hygiene.
- `premium-wordpress-site-chrome`: 5-7 core header routes plus CTA, premium footer, Hebrew font/menu discipline, mobile verification.
- `nadlan-real-estate-growth`: Nadlan public-language rules, money architecture, header/footer expectations, REST excerpt checks.
- `seo`: technical SEO, on-page quality, title/snippet hygiene, Core Web Vitals discipline.
- Active live theme skill export under `C:\Users\pro\AppData\Local\Temp\nadlan-live-theme-export-20260602\skills`, including strategy, copywriting, design, monetization, E-E-A-T, and WordPress content-type notes.

## Fresh Research Used

- Google Search Central: helpful, reliable, people-first content and title/snippet guidance.
- WordPress Developer Resources: REST API, block theme navigation/template-part behavior.
- web.dev: LCP, font, image, and Core Web Vitals implementation discipline.
- Nielsen Norman Group footer/navigation usability principles for keeping footer links useful, not dumped.

## Live Changes Applied

1. Header navigation fixed live through WordPress REST.
   - Target: `wp_navigation` post id `4`.
   - Before: 13 top-level/public labels, and after the first update the live `<nav>` rendered empty because the navigation post contained rendered `<li>` HTML instead of WordPress navigation block markup.
   - After: proper `wp:navigation-link` and `wp:navigation-submenu` block markup.
   - Visible desktop labels now verified: `קניית דירה`, `מכירת דירה`, `השקעה`, `משכנתא`, `משפט ומיסוי`, `כלים`, `אנשי מקצוע`, `בדיקת עסקה`.

2. Public REST excerpts cleaned for 23 pages.
   - Removed the malformed public prefix beginning `נח נכתב...`.
   - Replaced with short consumer-facing Hebrew excerpts only.
   - Article/page body content was not changed.
   - Maintenance script dry-run now reports zero remaining broken excerpts in the checked REST page set.

3. Mobile floating contact buttons improved live through the footer template part.
   - Target: `nadlan-revenue//footer`.
   - Before: right-side vertical stack covered RTL page content on mobile.
   - After: compact bottom-left mobile row with short labels, reserved bottom padding, and no horizontal overflow.

## Verification

- Desktop homepage live check:
  - URL: `https://nad-lan.co.il/`
  - HTTP: 200.
  - H1 count: 1.
  - Header labels: 8 verified.
  - Horizontal overflow: false.
  - Forbidden visible internal terms: none detected by rendered check.
  - Screenshot: `verification-screenshots/nadlan-20260602-home-desktop-v2-top.png`.

- Mobile homepage live check:
  - URL: `https://nad-lan.co.il/`
  - HTTP: 200.
  - H1 count: 1.
  - Horizontal overflow: false.
  - Responsive menu button visible.
  - Mobile FAB row verified visually.
  - Screenshot: `verification-screenshots/nadlan-20260602-home-mobile-fab-v4-top.png`.

- Representative page checks:
  - `https://nad-lan.co.il/commercial-real-estate/store-for-rent/` returned 200, one H1, no broken public byline prefix.
  - `https://nad-lan.co.il/investment/` returned 200, one H1, no broken public byline prefix.
  - `https://nad-lan.co.il/urban-renewal/tama-38-rights-obligations/` returned 200, one H1, no broken public byline prefix.

## Important Blockers and Gaps

1. `https://nad-lan.co.il/robots.txt` returns 404.
   - This is a technical SEO blocker.
   - The exported theme contains a `robots.txt`, but WordPress/theme files are not serving it at the domain root.
   - Next fix should be server/root-level robots or a plugin/theme virtual robots handler.

2. Active live theme is ahead of the local repo.
   - Live active theme: `nadlan-revenue`, version `1.1.0`.
   - Local repo theme files are older and should not be pushed blindly.
   - For future theme-code work, first align/export/selectively merge the live theme into the repo, then push to GitHub and pull in UPress File Manager.

3. Mobile homepage still has a heavy first viewport design language.
   - Header and floating controls improved, but homepage typography/hero/card rhythm still deserves a separate design pass.
   - Do not start that pass by writing articles.

## Scripts Added

- `scripts/nadlan-nonarticle-maintenance-20260602.mjs`
  - Dry-run/apply tool for `wp_navigation` block markup and public excerpt cleanup.

- `scripts/nadlan-mobile-fab-maintenance-20260602.mjs`
  - Dry-run/apply tool for mobile floating contact button CSS in the footer template part.

- `scripts/nadlan-live-spotcheck-20260602.mjs`
  - Live HTML spot-check for homepage/page status, H1 count, broken prefix visibility, and internal term scan.

## Non-Article Boundary

No new articles were written. No long-form page bodies were rewritten. Changes were limited to navigation markup, excerpts/snippets, footer mobile CSS, verification scripts, and knowledge documentation.

## Next Authorized Goals

1. Fix `robots.txt` 404.
2. Align live theme export with repo before any GitHub theme push.
3. Build a no-article improvement plan for homepage typography, footer symmetry, menu behavior, provider directory CMS fields, and revenue flow.
4. After user authorization, resume article/content body work using the cleaned public narrative rules.
