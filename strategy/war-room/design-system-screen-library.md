# NadLan Design System And Screen Library

Date: 2026-06-23  
Scope: owner-readable and build-ready design specification. This is not runtime code.

## Purpose

This file converts the strategy, live evidence, Lovable prototype output, and current-site QA into a screen library that Codex can implement later without guessing. It does not claim that the production redesign is already built.

## External Product Evidence Used

- Zillow 3D Home: virtual tours and interactive floor plans are listing assets, not decoration. Source: https://www.zillow.com/3d-home/
- Zillow Showcase: elevated listing design, branding, search/map priority, and serious-buyer reach are treated as a paid premium listing product. Source: https://www.zillow.com/agents/showcase/
- Zillow SkyTour article: exterior and setting context matter, including angles, elevation, surroundings, and neighborhood connection. Source: https://www.zillow.com/news/zillow-showcase-brings-listings-to-life/
- Matterport: one capture can support 3D tours, floor plans, photos, and marketing assets. Source: https://matterport.com/
- Homes.com Matterport: digital twins and detailed floor plans create a more realistic touring experience. Source: https://www.homes.com/solutions/matterport
- JamesEdition real estate: luxury property discovery depends on curated global inventory, strong imagery, filters, trusted agents, and international orientation. Source: https://www.jamesedition.com/real_estate

## Brand Direction

Working public name: NadLan. Do not use a final Hebrew brand such as Nadlan Chacham until legal/domain and competitor checks are complete.

Visual position:

- Premium real-estate decision platform.
- Hebrew-first, with native English investor pages.
- Product and proof before marketing copy.
- Calm, serious, data-backed, not a decorative tech demo.

Logo and favicon direction:

- Mark: compact geometric building/floor plate plus map pin signal.
- Favicon: simple dark mark on warm paper background, readable at 32px.
- Avoid generic house icons and avoid an AI-themed name or robot mark.

## Design Tokens

Color tokens:

- `--nl-paper`: `#f7f1e8`, warm page background.
- `--nl-surface`: `#fffaf2`, panels and cards.
- `--nl-ink`: `#211915`, primary text.
- `--nl-muted`: `#746b63`, secondary text.
- `--nl-line`: `#ded2c3`, borders.
- `--nl-forest`: `#0f332c`, premium project/action surfaces.
- `--nl-gold`: `#a7793b`, emphasis, not dominant decoration.
- `--nl-danger`: `#8f2e24`, blockers and missing proof.
- `--nl-ok`: `#2f654f`, verified states.

Typography:

- Hebrew heading: high-contrast serif or equivalent Hebrew-capable display face.
- Hebrew body: clean sans-serif with strong numerals and form readability.
- English investor pages: native LTR rhythm, not mirrored Hebrew layout.
- No viewport-based font scaling. Use responsive layout, not fluid font-size formulas.

Spacing and shape:

- Cards: 4px to 8px radius only.
- Buttons: stable 44px minimum tap target.
- No nested UI cards except repeated item cards inside a page section.
- Dense operational surfaces should avoid oversized hero-only composition.

## Public Language Rules

Public UI must not expose internal terms such as implementation notes, file formats, ranking internals, or prompt language. If a state needs explanation, use buyer-facing Hebrew or English:

- Official asset: "חומר רשמי מהיזם".
- Concept asset: "הדמיה לבדיקה, לא חומר רשמי".
- Missing asset: "חסר חומר רשמי".
- Paid placement: "מיקום בתשלום" or legally reviewed equivalent.
- Estimate: "אומדן לא מחייב" with source note.

## Asset Truth System

Every visual or data asset must be classified before public use:

- official: approved by developer, owner, registry, or official source.
- concept: internal design or planning material, clearly labeled.
- reused: from existing site/repo, with source path.
- missing: needed but unavailable.
- broken: expected but failed to load.

This applies to project images, GLB models, facade/elevation assets, floor plans, apartment plans, map data, virtual tours, consultant profiles, logos, favicon, and Open Graph images.

## Screen Library

See `design-system-screen-library.csv` for the structured build table. The required surfaces are:

1. Brand system.
2. Homepage.
3. Listing search.
4. Listing detail.
5. Projects catalog.
6. Project page.
7. 3D showroom.
8. Professionals directory.
9. Tools and calculators.
10. International investor pages.
11. Contractor intake.
12. Admin war room.

## Implementation Gates

A screen is not accepted until:

- desktop and 390px screenshots are saved,
- no horizontal overflow is visible,
- no internal language leaks into public UI,
- asset-truth labels are correct,
- SEO owner page is known,
- required schema/canonical/noindex rules are documented,
- owner-facing screenshot review exists.

## What This Improves

This file closes part of the visual-design gap identified in `objective-completion-audit.csv`. It gives Codex a screen library and token layer to build from.

It does not complete the full redesign because real project assets, live trust fixes, and production implementation screenshots still remain.
