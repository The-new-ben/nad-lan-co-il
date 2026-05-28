# Interactive Widgets — calculators, sitemap, premium footer

> **Notice to all agents:** four interactive widgets were deployed live to nad-lan.co.il on 2026-05-28 via REST. **They are stored in the DB as page/template-part content**, not in the theme files (footer is a "custom" override of the theme's template part). Use these patterns; do not duplicate.

## What was deployed

### 1. Mortgage Calculator (`/mortgage-calculator/`)
- **Repo source:** `assets/widgets/mortgage-calculator.html`
- **Deployed via:** PREPENDED to the existing page content (Codex's article remains below)
- **Marker:** `data-nlc="mortgage-v1"`
- **Features:**
  - 3-track Israeli mortgage mix: קל"צ, פריים, משתנה
  - Per-track inputs: סכום + ריבית + תקופה
  - Live calculation: total amount, monthly payment, total interest, total cost
  - Stacked bar showing track contribution to monthly payment
  - **Stress test** checkbox (+2% to all rates) — Israeli regulation requires this for new mortgages
  - Heebo font, brand palette (gold accent #D89B3C, trust blue #0E3A8A), cream background
  - Fully RTL, responsive (collapses to 1-col on mobile)
  - Vanilla JS, no dependencies, no external requests
- **Why it's a differentiator:** Israeli sites (Semerenko, israelmortgagecalculator.com) require email-gates; bank calcs handle single-track only. Ours is open + 3-track + stress-test + no friction.

### 2. Purchase Tax Calculator (`/purchase-tax-calculator/`)
- **Repo source:** `assets/widgets/purchase-tax-calculator.html`
- **Deployed via:** PREPENDED
- **Marker:** `data-nlc="ptx-v1"`
- **Features:**
  - 2026 brackets baked in (verified, frozen until 2028 per חוק ההסדרים)
  - דירה יחידה: 0% to 1,978,745 → 3.5% to 2,347,040 → 5% to 6,055,070 → 8% to 20,183,565 → 10%
  - משקיע: 8% to 6,055,070 → 10%
  - **Visual bracket bar** with marker showing where the user's price falls (the killer feature — Israeli SERP law firms have plain calcs only)
  - Per-bracket breakdown showing slice × rate = sub-tax
  - Gradient blue result tile with big tax number + % of property
  - Toggle: single vs investor
- **Why it's a differentiator:** SERP for "מס רכישה 2026" is owned by law firms with plain text-based calcs. The visual bracket bar with live marker is leagues better UX.

### 3. Dynamic HTML Sitemap (`/sitemap/`)
- **Repo source:** content embedded in `docs/wp-state/page-sitemap.html`
- **WP page id:** 336
- **Marker:** `data-nlc="sitemap-v1"`
- **Features:**
  - **Self-updating** — fetches `/wp-json/wp/v2/pages?per_page=100` on page load and renders cluster cards
  - Hard-coded cluster topology (8 clusters: buying, selling, invest, mortgage, tax, renewal, pros, cities)
  - Cornerstone pages get a gold "פילר" tag, calculator pages get a green "כלי" tag (detected from Yoast meta + slug match)
  - Live search box filters across all titles
  - 4-card stats strip: total pages, clusters, tools, pillars
  - Orphan page detection — pages not in any cluster get a "שאר העמודים" card
  - Updates "last updated" timestamp on every render
  - Premium cards with hover lift + shadow
  - Mobile-responsive grid
- **Yoast meta description** set on the page during creation
- **Why it's better than ordinary:** truly dynamic (not a static list), searchable, organized hierarchically, premium UX.

### 4. Premium Footer (site-wide)
- **Repo source:** `docs/wp-state/template-part-footer.html` (saved DB state)
- **WP template part:** `nadlan-revenue//footer`, source=`custom` (DB override of theme file)
- **Layout:** 4 columns + bottom bar:
  - Brand col: nadlan חכם heading + tagline + uppercase trust line
  - תחומי תוכן: 7 pillar links
  - כלים אינטראקטיביים: 5 calculator links
  - מיסוי ומשפט: 4 legal/tax + sitemap link
  - Separator bar
  - Bottom: copyright + disclaimer
- **Style:** dark contrast bg (#0F1B2D), accent-1 gold uppercase section headings, accent-5 cream body text
- **Why premium:** matches Rightmove/Zillow-style 4-col footer with brand block on the right (RTL). Old footer was empty default.

## Update / extend protocol

### To update a calculator widget:
1. Edit `assets/widgets/<name>.html` in the repo
2. Bump the data-nlc marker version (e.g. `mortgage-v1` → `mortgage-v2`)
3. The injection script must REMOVE the v1 block before prepending v2 (current script skips if marker present — needs enhancement for true updates)
4. For now: easiest path is via WP admin → edit the page → delete the old widget block → paste the new one. OR run a small REST script that strips between `<!-- wp:html -->` markers matching the old data-nlc and prepends the new one.

### To update the sitemap clusters:
- Edit the `CLUSTERS` array in the JS (inside the wp:html block of page id 336)
- Source-of-truth lives in the DB, mirrored in `docs/wp-state/page-sitemap.html`

### To update the footer:
- POST new content to `/wp-json/wp/v2/template-parts/nadlan-revenue//footer`
- Mirror in `docs/wp-state/template-part-footer.html`

## Constraints respected
- No new plugins (everything via REST + content blocks)
- No external services (no Google Fonts CDN, no map APIs, no analytics SDKs)
- No Hebrew article writing (UI labels only — ~50 short strings total per widget)
- Lawyer/Person schema deferred — owner not ready to be publicly signed as lawyer
- All widgets are vanilla JS — no React/Vue/jQuery dependencies

## Open TODOs (next session)
- [ ] Build **Buy-vs-Rent calculator** (NYT-style, viral potential — gap in IL market)
- [ ] Build **Affordability reverse calc** (Zillow-style "what can I afford given my income")
- [ ] Build calculators for the remaining 3 calculator pages (property-value-estimator, investment-property-cashflow-calculator, apartment-purchase-cost-calculator) — current page is just Codex's article
- [ ] Add **Cap Rate / Cash-on-Cash / IRR** to investment cashflow calc
- [ ] Premium header upgrade (current header is bare logo + nav; competitors have search-box + CTA)
- [ ] **Map widget** with neighborhood price overlays (Trulia-style; using OSM tiles, no Mapbox key needed)
- [ ] Compose shareable PNG/PDF report from calculator state (EstatePass-style — viral / E-E-A-T)

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Sources: see WebSearch citations in commit message + skill content for US/UK competitor research._

## Update 2026-05-28 (claude-opus-4-8) — Buy-vs-Rent break-even visualizer + logo header

### Buy-vs-Rent break-even ("the wow")
- **Live at `/buy-vs-rent/`** (page id 343). Repo source: `assets/widgets/buy-vs-rent.html`.
- The globally-viral NYT-style tool, ABSENT in the Hebrew market (verified gap). Decision-stage → highest-value lead moment → CTA links to `/real-estate-lawyer/`.
- Computes 30-year cumulative NET cost of buying (mortgage interest + maintenance 1% + ~8% purchase costs − equity/appreciation) vs renting (rent rising with market − alt-investment return on the would-be down payment). Finds the **break-even year** where the two lines cross.
- Animated inline SVG dual-line chart with a dashed gold break-even marker, live recompute on every input change. Vanilla JS, no deps. Uses the live luxury CSS tokens (`--font-serif`, `--gold-600`, `--ink-900`), so it inherits the design system automatically.
- Marker: `id="nbvr"`. Added to the כלים submenu in nav id 4.
- **Honest limitation**: uses conservative fixed assumptions (25y Spitzer mortgage, 1% maintenance, 8% one-time purchase costs, rent rises at appreciation rate, ignores selling costs). Documented in the widget's note. A future v2 could expose these as advanced inputs and add a "sensitivity" band.

### Logo header (the "internal pages show only a link" fix)
- The header template part (`nadlan-revenue//header`) used `wp:site-title` (plain text) — so internal pages showed a text link, not a logo.
- **Overridden live via REST** (`source: custom`) with a brand lockup: inline-SVG **monogram seal** (נ in a gold double-circle, the "old-house" double-rule) + serif wordmark "נדל״ן חכם" + tagline "ידע · כלים · החלטות" + a **pulsing gold dot** (CSS `@keyframes nlpulse`, respects `prefers-reduced-motion`, hidden detail the owner requested to "attract the eye").
- Keeps the curated block navigation (ref 4). Slim, cream bg, hairline bottom border.
- Repo mirror: should be saved to `docs/wp-state/template-part-header.html` (TODO next commit).
- **Note**: this is a DB `custom` override — it does NOT live in the theme file `parts/header.html`. If the theme is re-synced, the override persists (DB wins over theme file for customized parts). But for repo-source-of-truth, mirror it.
