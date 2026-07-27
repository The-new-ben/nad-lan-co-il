# Handoff — NadLan Old Site Roast

## Deliverable

- [`2026-07-27-nadlan-old-site-roast-he.md`](2026-07-27-nadlan-old-site-roast-he.md) — full Hebrew product, visual, business, content, SEO, multilingual and advertiser roast.
- [`2026-07-27-nadlan-review-index.md`](2026-07-27-nadlan-review-index.md) — single reading index connecting this audit to the competitor research, specifications, marketing plan and five visual previews.

## Scope

Audited the main public page/template families rather than manually opening every database row:

- Homepage, desktop and mobile.
- Site map and navigation.
- Project, property and professional archives.
- Representative project detail: Rainbow Tel Aviv.
- Representative property and professional detail behavior.
- Advertise / paid-placement surfaces.
- Global investments and foreign-buyer path.
- Urban renewal, calculators, glossary/content architecture.
- English, French, Russian and Arabic home experiences.
- Relevant local source evidence for search, verification labels, paid ranking, generic media, demo inventory, pricing duration and view measurement.

## No-change statement

No production code, WordPress content, settings, permissions, users, API credentials or live data were changed. This delivery adds documentation and screenshot evidence to the repository only.

## Primary evidence

Repository screenshots:

- [`01-home-desktop-viewport.png`](qa/screenshots/nadlan-old-site-roast-2026-07-27/01-home-desktop-viewport.png)
- [`01-home-mobile-top.png`](qa/screenshots/nadlan-old-site-roast-2026-07-27/01-home-mobile-top.png)
- [`nadlan-live-home-desktop-top.png`](qa/screenshots/nadlan-old-site-roast-2026-07-27/nadlan-live-home-desktop-top.png)
- [`nadlan-live-home-project-cards.png`](qa/screenshots/nadlan-old-site-roast-2026-07-27/nadlan-live-home-project-cards.png)
- [`nadlan-live-home-listings.png`](qa/screenshots/nadlan-old-site-roast-2026-07-27/nadlan-live-home-listings.png)
- [`nadlan-live-home-3d-showcase.png`](qa/screenshots/nadlan-old-site-roast-2026-07-27/nadlan-live-home-3d-showcase.png)
- [`nadlan-live-home-professionals-international.png`](qa/screenshots/nadlan-old-site-roast-2026-07-27/nadlan-live-home-professionals-international.png)
- [`nadlan-live-projects-catalog-top.png`](qa/screenshots/nadlan-old-site-roast-2026-07-27/nadlan-live-projects-catalog-top.png)
- [All homepage and Rainbow evidence](qa/screenshots/nadlan-old-site-roast-2026-07-27/)

Verified public facts at audit time:

- Homepage: 987 projects, 2,726 professionals.
- Project archive: 971 projects.
- Advertise page: 965 projects, 2,723 professionals.
- Property archive: 7 records; inspected item URLs contain `-demo`.
- Rainbow: “6 apartments to choose” while the product source states the model and units are illustrative and not live inventory.
- `/en/`, `/fr/`, `/ru/`, `/ar/`: document language remained `he-IL`; English, French and Russian remained RTL.
- Homepage search for “תל אביב” produced `/properties/?q=...` and displayed a Jerusalem result.

## Evidence caveats

- WordPress admin-bar appearance was excluded from public design criticism.
- The repeated Hero visible in a full-page stitched screenshot was excluded as a screenshot artifact.
- Count discrepancies may be caused by cache, language siblings or different query definitions; the criticism is that the visitor sees no definition or timestamp.
- Legal content dated 2024 was not declared legally wrong; the criticism concerns visible freshness and verification in a 2026 product.
- No claim was made that every one of the hundreds of records was individually opened.

## Recommended next decision

Before design or code changes, the owner should approve:

1. The primary homepage product and audience.
2. The truth-label system: verified, official-source, owner-claimed, illustrative and demo.
3. The minimum complete card/project-page standard.
4. The advertiser product contract and measurement standard.
5. Whether International Buyers is a real operated service or a future concept.

No implementation should begin without owner approval.
