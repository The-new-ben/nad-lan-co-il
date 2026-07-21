# Current Repository Gap Inventory

## Scope

Read-only repository evidence as of base commit `f16ca096b67a2e2077c7479c4e2e8ef33819b8eb`. No live WordPress state is asserted unless a current probe exists. Historical reports remain labelled historical until rechecked.

## What is already substantial

- WordPress block theme with NadLan color and typography tokens.
- Project, property, professional, city and compound content graph.
- Public project catalog and REST surfaces.
- Map/nearby/search suggestions.
- Save, saved-search and compare.
- Lead, concierge and WhatsApp ingestion paths.
- Developer claim and Studio editing/upload routes.
- Rich project 3D data contract and protected import/export route.
- Placement, sponsorship and commercial modules.
- HE/EN/i18n infrastructure and extensive research/design history.

The problem is therefore not “there is no product.” It is the gap between system depth and visible, consistent, rights-cleared project presentation.

## Repo-verified visual/content gaps

| Gap | Repository evidence | User-facing risk | Spec response |
| --- | --- | --- | --- |
| Archive card media depends on a featured image | `plugins/nadlan-config/inc/archive-grid.php:98-102` | Image-less cards recreate the amateur/unfinished feeling | Approved hero is a public-card gate; dignified missing state only outside featured surfaces |
| Facility chips currently render for properties, not projects | `plugins/nadlan-config/inc/archive-grid.php:107-119` | Project cards lose the useful badges the owner remembers | Add an approved project amenity taxonomy/field contract before implementation |
| Homepage media helper can exhaust poster, featured image and `photos_csv` and return empty | `plugins/nadlan-config/inc/home-v2.php:23-31` | Empty rails/blocks even when the layout expects imagery | Query only eligible visual-complete projects; collapse band or use truthful neutral state |
| Rainbow amenities exist mainly in narrative copy | `docs/rainbow-tel-aviv-flagship-listing.md:80-95` | No reliable card/filter facility system | Structure facilities with evidence, state and icon mapping |
| Existing project packages are prototypes | `assets/projects/*/source-notes.md` | Model/plans/images can be mistaken for official inventory | Visible illustrative states and developer material intake gate |
| Exact model taps are not exact window/unit geometry | multiple June 24 QA records under `docs/qa/screenshots/` | Overpromising 3D damages diligence trust | Level-based 3D contract; official per-unit geometry required for exact selection |

## Strong internal canon to preserve

The most useful prior structural source is the July 2 CMS-driven portal system:

- `docs/plans/2026-07-02-master-reset-homepage-projects.md`
- `handoff/claude-design/2026-07-02-homepage/homepage-spec.md`
- `handoff/claude-design/2026-07-02-critical-report-and-full-spec.md`
- `docs/research/2026-07-03-project-page-competitive-teardown.md`

It already identifies the need for a dense institutional homepage, real image posters, search-first identity, market/area/tool/editorial/professional/international bands and CMS-managed ordering. The owner’s July 21 direction strengthens this canon and supersedes older showroom-first/sparse rules.

## Superseded internal directions

- June positioning that NadLan should not resemble a listings board and should not compete on inventory.
- NadLan3D as the master public brand.
- Full apartment picker or live model as the homepage identity.
- Site-wide sketch/procedural art as the primary asset layer.
- Old navy/gold-heavy treatment and oversized prototype radii.
- Night map as an unquestioned first-viewport opener if it suppresses real project imagery and search.

Useful parts of those documents—honesty, source-aware 3D, editorial story, RTL and premium restraint—remain.

## Historical/live claims that must be rechecked

- Any count of projects, properties, professionals, transactions or pages.
- July 2 observations about the exact live homepage bands or language duplicates.
- June REST/version anomalies.
- Current plugin/theme version on production.
- Current application-password/REST write access.
- Current live search, save, compare, form, map and Studio behavior.
- Current prices, project lifecycle, handover and contact details.

The user instructed that WordPress admin navigation use clicks rather than direct URL entry because the hosting/security plugin can block straight paths. A future approved implementation/access audit should follow that rule. This research package does not navigate or mutate WordPress.

## Missing inputs, not missing code

The largest presentation blockers are content/rights/governance inputs:

- approved official hero/card thumbnails and galleries;
- developer logos and reuse permission;
- official plans/specifications;
- current price/availability/handover policy;
- structured amenity evidence;
- named sales contacts and language capability;
- English commercial review;
- source dates and re-verification owners;
- official unit/BIM/GLB mapping for exact 3D selection.

Adding more frontend code before these inputs exist would not solve the “empty amateur portal” problem.

## Safe next audit after owner approval

1. Click through wp-admin from the already authenticated session.
2. Inventory active theme/plugin versions, CPT counts and media completeness without writing.
3. Test public cards and project pages at desktop/mobile.
4. Test current public GET endpoints; do not perform REST writes.
5. Check application-password capability/status without creating/revoking anything unless separately approved.
6. Select the launch cohort and produce a project-by-project missing-material list.
