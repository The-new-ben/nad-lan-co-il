# A0b - Gap Audit

## Executive Diagnosis

NadLan has many strong pieces, but not yet a single execution machine. The recurring failure has been jumping from idea to plugin/theme implementation without a completed keyword/page/design/build registry.

The project needs a controlled sequence:

1. Trust cleanup.
2. Keyword and page ownership.
3. Visual product board.
4. Listing/product specs.
5. Project showroom source/asset pipeline.
6. Implementation backlog.
7. Build only one P0 slice at a time.

## Gap Matrix

| Area | Current state | Target state | Gap | Priority |
|---|---|---|---|---|
| Public trust | PR #211/#212 merged, final live proof pending | No public internal/Woo/debug leakage | Needs UPress pull + final screenshots | P0 |
| Homepage | Existing WordPress homepage, not yet final portal shell | Search/map/projects/tools/trust above fold | Needs visual board and route ownership | P0 |
| Keywords | Seed lists and prior reports | 1500-3000 keyword universe | Missing metrics and full ownership | P0 |
| Canonical pages | Implicit and scattered | One canonical owner per keyword | Missing registry | P0 |
| New projects | Strong business direction | Projects hub + city/project pages + showroom | Needs page architecture | P0 |
| Project showroom | Plugin runtime exists, uneven UX/assets | Official/concept/missing states, no fake claims | Asset pipeline, geometry, mobile, tour | P0 |
| Listings | Directory/CPT pieces exist | Map/list marketplace | Missing app UX and supply thresholds | P1 |
| Professionals | Imported records, profession imbalance | Normalized professional marketplace | Taxonomy and trust state weak | P1 |
| Design | Multiple ad hoc slices | Unified data-rich product system | Need gallery and tokens | P1 |
| CRM/leads | Lead routes exist | SLA, assignment, dashboard, analytics | Need operating model | P0/P1 |
| i18n | Intent exists | Hebrew first, EN/FR/RU/AR bridge | No architecture | P2 |
| QA | Some scripts and screenshots | Required gates per PR | Needs consistent enforcement | P0 |

## Trust Gaps

- Confirm PR #212 is live after UPress theme pull.
- Verify no public mini-cart/cart/checkout text on non-commerce pages.
- Verify `/professionals/` console error is gone or documented.
- Verify sitemap placeholders are gone.
- Verify no `More posts`, comments UI, or template English on project/professional pages.
- Verify one visible H1 per key page.

## SEO Gaps

- No verified volume/KD/CPC for many target keywords.
- No top-100 money term SERP reverse engineering.
- No canonical page registry with forbidden keywords.
- No faceted navigation/noindex law for buy/rent/projects/pros/listings.
- No programmatic SEO thresholds for city/neighborhood/street pages.
- No GSC cannibalization export.

## UX/Product Gaps

- No final component gallery for the portal.
- No map/list listing product.
- No developer dashboard shell.
- Project cards need official/concept/missing state consistently.
- Showroom still depends on inconsistent assets.
- Need clear mobile containment and state handling.

## 3D/Showroom Gaps

- Official BIM/GLB assets mostly missing.
- Real per-unit apartment geometry missing.
- Official facade/elevation assets missing for most projects.
- Concept facades can be used only with clear concept labels.
- Interior tour path requires real Matterport/360/iframe/media URL.
- Mapbox works for locator/POI; credible high-floor view may require Cesium/Google Photorealistic 3D Tiles evaluation.

## Monetization Gaps

- Packages exist conceptually, but dashboard/SLA/CRM proof is incomplete.
- Project Premier needs clear deliverables, pricing, onboarding, and asset requirements.
- Professional Pro/Premier needs better taxonomy and value proof.
- Lead quality needs funnel and attribution reporting.
- Outreach needs legal review before automation.

## Immediate Blockers

1. Stage 1 final live proof pending after UPress pull.
2. No official facade/BIM asset pipeline.
3. Keyword/page registry missing.
4. Visual product board missing.
5. CRM operating model incomplete.

## Do Not Build Yet

Do not build new public pages or showrooms until the page registry and visual/product board exist. The only exception is a surgical trust fix with screenshot QA.
