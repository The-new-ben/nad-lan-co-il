# NadLan repo inventory

Source: `github.com/The-new-ben/nad-lan-co-il` @ `main` — 1,070 files total.

This is a **WordPress block theme + companion plugin**, not a JS app. No React/Next/build pipeline.

## Top-level shape

| Path | Role |
| --- | --- |
| `style.css`, `style.min.css`, `theme.json`, `functions.php` | WordPress block theme entry. `functions.php` enqueues the showroom CSS/JS and theme glue. |
| `parts/` (7) | Block-theme template parts (header, footer, etc.). |
| `templates/` (8) | Block-theme page templates. |
| `patterns/` (109) | Block patterns — site sections (hero, banners, CTAs, project-showroom pattern incl. `project-showroom-dimri-yama.php`). |
| `styles/` (32) | Block-theme `styles/colors`, `styles/typography`, `styles/sections`, `styles/blocks` variations. |
| `plugins/nadlan-config/` (132) | **The real product code.** Custom REST API (`nadlan/v1`), CPTs, lead engine, AI features, ads/auction, studio uploads, etc. |
| `plugin-dist/` (132) | A built/distributed mirror of `plugins/nadlan-config`. Treat `plugins/` as the source of truth and `plugin-dist/` as an artefact. |
| `assets/` (176) | Theme-level CSS/JS/fonts/images + per-project payloads under `assets/projects/<slug>/` (3D `.glb`, plans, SVGs, showroom JSON) and design references under `assets/premium*/`. |
| `docs/` (273) | Long history of specs, audits, research, QA scripts. Dates from 2026-06-03 onward. Some specs are aspirational — see `docs-vs-reality.md`. |
| `docs/qa/` (186) | The bulk of docs — per-feature QA notes. |
| `scripts/` (20) | Repo housekeeping / build helpers (PowerShell `assemble-nad-lan-kit.ps1` at root, plus `scripts/`). |
| `skills/` (80), `skills-templates/` (1) | Internal agent skill docs used by the team (not WP runtime). |
| `assemble-nad-lan-kit.ps1`, `START-HERE.md`, `AGENTS.md`, `BACKLOG.md`, `COORDINATION.md`, `HANDOFF.md` | Team workflow / agent handoff docs. |

## Plugin code map — `plugins/nadlan-config/inc/`

Single plugin, no OOP framework — flat `inc/*.php` files, each `add_action('rest_api_init', …)` or `add_filter` based. Grouped by concern:

**Content model & catalog**
- `catalog-meta.php`, `catalog-shine.php`, `cards-render.php`, `archive-grid.php`
- `compounds.php`, `compound-map.php`, `city-hubs.php`
- `media.php`, `og-image.php`, `pricing-schema.php`, `schema.php`, `term-faq-schema.php`

**Projects / showroom**
- `project-3d.php` (registers `/project-showroom/<id>` REST + 3D config)
- `project-page-assembly.php`

**Directory (professionals)**
- `directory.php` (registers `/directory` and `/projects` REST)
- `directory-assets.php`, `profile-extras.php`, `preferred-partners.php`

**Search / discovery**
- `autocomplete.php` (`/suggest`), `geo-search.php` (`/near`), `map.php` (`/map`)
- `ai-features.php` (`/nl-search`), `compare.php` (`/compare`), `facets.php`, `saved-search.php`

**AI**
- `ai-provider.php`, `ai-features.php`, `ai-concierge.php` (`/concierge`, `/concierge-lead`)
- `lead-ai-qualify.php`

**Leads**
- `conversion-cta.php` (`/lead`), `whatsapp-lead-ingestion.php` (`/wa-lead`)
- `lead-e2e.php` (`/lead/status`), `lead-drip.php`, `lead-nurture.php`, `lead-routing.php`, `lead-ledger.php` (referrals), `lead-inbox.php`

**Monetization / advertisers**
- `advertiser-center.php`, `advertiser-orders.php`, `featured-upsell.php`, `sponsored-spot.php`
- `placement-auction.php` (`/auction/bid`), `auction.php` (`auctions/v1/*`)
- `offers.php` (`/offers`, `/offers/leading/<card>`)
- `tiers.php`, `greeninvoice-recurring.php` (`/gi-ipn` — billing webhook)

**Studio (owner-facing media manager)**
- `studio.php`, `studio-rest.php` (8 routes under `/studio/*`)
- `owner-config-rest.php` (`/owner/whatsapp`, `/owner/partners`)
- `claim.php` + `claim-prompt.php` (`/claim`), `reviews.php` (`/review-submit`)

**Ops / admin / health**
- `admin-control.php` (6 routes under `/admin-control/*`)
- `health.php` (`/health`), top-level `nadlan-config.php` registers `/healthcheck`
- `ops-dashboard.php`, `business-metrics.php`, `feature-flags.php`, `roles.php`, `final-hardening.php`, `import.php` (`/import-enrich`, `/import-run`), `avm-deals.php` (`/deals-ingest`, `/avm`), `sitemap-ping.php`, `ga4-events.php`

**Misc**
- `breadcrumbs.php`, `calculators.php`, `contextual-help.php`, `conversion-cta.php`, `esign.php`, `glossary.php` (`/glossary-publish`) + `glossary-autolink.php`, `homepage.php`, `listings-ux.php` (`/favorite`), `nearby-poi.php`, `premium-ui.php`, `social-proof.php`, `lead-drip.php` (`/drip-optout`), `lead-nurture.php` (`/nurture/unsubscribe`), `lead-ledger.php` (`/referral/*`)

**Third-party**
- `lib/plugin-update-checker/` — bundled YahnisElsts PUC v5.6, used for GitHub-based plugin updates. Not our code.

## Theme-level JS/CSS

- `assets/js/nadlan-accessibility.js`, `nadlan-premium-revenue.js`, `nadlan-project-showroom.js`
- `assets/css/editor-style.css`, `nadlan-premium-revenue.css`, `nadlan-premium-sitewide.css`, `nadlan-project-showroom.css`
- Per-project payloads under `assets/projects/<slug>/` (e.g. `dimri-yama`, `rainbow-tel-aviv`): `model.glb`, `showroom-payload.json`, `unit-map.json`, `view-layer-config.json`, `material-intake-template.json`, plans/, source-notes, QA.

## CPTs and taxonomies (live, from `/wp-json/wp/v2/types`)

Custom post types: `nadlan_property`, `nadlan_project`, `nadlan_professional`, `nadlan_auction`, `nadlan_term`.
Taxonomies: `nadlan_city`, `nadlan_compound`, `nadlan_profession`, `nadlan_term_cat`.
Standard: `post`, `page`, plus WooCommerce `product` + `product_cat` / `product_tag` / `product_brand`.

## Live runtime versions (from `/wp-json/nadlan/v1/healthcheck`)

- Plugin `nadlan-config` **v1.68.2**
- PHP 8.5.5, WP 7.0
- All four core CPTs/taxes present, auction CPT + bids table present
- AI provider: OpenAI (key present, daily caps 30k / global 200k)

## Notable observations

1. **`plugin-dist/` duplicates `plugins/nadlan-config/`.** Edit only one; reconcile via build step if both diverge.
2. **No automated tests in the repo.** QA is doc-based under `docs/qa/`.
3. **No Composer / no PSR autoload.** Plugin uses flat `require` includes.
4. **Update channel = GitHub** via Plugin Update Checker — installed site pulls releases from this same repo.

