# Research and build notes

## Decision

The correct rescue path is a plugin bridge, not a replacement theme. The prior theme-only artifact narrowed the site to a few project pages. This bridge keeps the existing content system and adds a project showroom, shortcodes, styling, hreflang and lead capture.

## Scope

- Preserve existing homepage and content.
- Preserve existing listings, professionals, calculators, guides and monetization.
- No destructive DB rewrite.
- One showroom layer only.
- Project pages remain crawlable and content-rich.
- Each language remains a separate URL, with sibling navigation and hreflang.

## Research anchors used

- Google Search Central localized versions and hreflang guidance.
- WordPress Shortcode API.
- WordPress REST API custom endpoints.
- model-viewer documentation for web-based 3D display.
- Pannellum as a future free interior-tour option.

## Known live-site work still required

- Upload to staging or a backup-safe live slot.
- Confirm the exact live CPT/meta field names.
- Confirm whether the existing NadLan lead pipeline should receive a duplicate lead event.
- Replace sample comps with the existing NadLan government/Madlan data pipeline.
- Confirm real assets for Ashira/Rainbow/Dimri and real URL slugs.
