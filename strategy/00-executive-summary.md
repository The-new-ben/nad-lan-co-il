# Executive Summary

NadLan should move from an experimental/technical site into a premium, credible, measurable commercial real-estate portal.

Core thesis:
- The goal is not easy long-tail SEO. The long-term target is the hardest and most profitable Israeli real-estate demand: apartments for sale/rent, new projects, urban renewal, mortgage/tax/legal intent, professionals, and paid B2B supply.
- Traffic is not enough. Public trust, product maturity, reliable data, project showroom credibility, and commercial funnels must mature together.
- The immediate P0 is trust, not feature expansion.

Current verified state:
- `origin/main` includes PR #212: non-commerce WooCommerce asset dequeue.
- Live plugin healthcheck reports `nadlan-config` version `1.68.2`.
- The #212 theme change still needs UPress theme Git pull and cache clear before final proof.
- Live probes still show WooCommerce asset handles on public non-commerce pages until that deployment happens.

North star:
- A Hebrew RTL real-estate authority site combining listings, new projects, verified professionals, calculators, buyer guides, AI answers, and B2B monetization.
- New project pages should feel like a premium digital showroom: real project context, official or clearly labelled concept media, selectable units, map/view layer, interior/tour media when available, and direct lead path.

Non-negotiables:
- No silent fallback.
- No fake facade.
- No dead buttons.
- No public internal/debug/QA language.
- No public WooCommerce cart/notification leakage outside commerce flows.
- No claims based on unverified Semrush/GSC/legal data.

Execution order:
1. Finish Stage 1 public trust final verification.
2. Capture external strategy evidence from Lovable/Semrush/GSC. `NEEDS_VERIFICATION`
3. Build a small implementation slice, not a broad redesign.
4. Commit visual proof for every buyer-facing change.

