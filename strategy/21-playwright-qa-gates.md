# Playwright QA Gates

Required viewports:
- Desktop: 1440x1100.
- Tablet: 768x1024.
- Mobile: 390x844.

Required pages:
- `/`
- `/projects/`
- `/projects/dimri-yama-sde-dov/`
- `/projects/rainbow-tel-aviv/`
- `/projects/ashdar-einstein/`
- `/professionals/`
- `/join-pro/`
- `/sitemap/`
- `/property-value-estimator/`
- `/for-sale/` if it exists.
- `/for-rent/` if it exists.
- One city/project route if it exists.

Public trust gate:
- No public WooCommerce cart/notifications outside commerce pages.
- No coming soon.
- No QA/debug/internal text.
- No placeholder sitemap.
- No `More posts`, `Leave a reply`, or template English.

Mobile gate:
- `document.documentElement.scrollWidth <= innerWidth + 2`.
- No fixed card blocking content.
- CTA is reachable and readable.

Project showroom gate:
- No fake facade.
- Concept/official/missing state is clear.
- No unit cells without facade asset and mapping.
- Mapbox error is visible if broken.
- Tour button disabled or absent when no URL exists.
- GLB missing/broken state is visible.
- Lead payload includes project/unit context where known.

SEO gate:
- Title, meta, H1, canonical, breadcrumbs, and schema are present and not contradictory.
- Noindex is applied to pages that are not ready.

Output:
- PASS/BLOCK.
- Screenshots list.
- Failed assertions.
- Exact URL.
- Exact selector/text.
- Recommendation to Codex.

