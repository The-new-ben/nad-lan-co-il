# Lovable Locked Build Scope

Date: 2026-06-23

Status: approved by Codex, ready for owner to tell Lovable to start.

## Scope

Single Lovable run in the TanStack Start project, estimated 45-65 credits.

War Room dashboard and Dubai/Cyprus/Greece/Thailand coded landings are deferred to a later run. They must be outlined and remain phased, not excluded.

## Deliverables

1. Interactive showroom prototype.
2. Listings page with magazine cards and ranking hierarchy.
3. Sitewide IA: navigation, homepage, breadcrumbs, city hubs, guide hub, professionals teaser.
4. Cream Luxury / editorial-bright design system.
5. Nadlan3D working brand direction with `.ai` positioning.
6. All output committed to `https://github.com/The-new-ben/nadlan-strategy-hub` on `main`.
7. All Lovable output appended under `handoff/lovable/2026-06-23-war-room-sync/`.

## Design System

Adopt the existing `luxury-design-system.md` direction, with one brighter editorial accent:

- base: cream `#FAF7F1`, ink `#1B1A17`, muted gold `#9C7A3C`
- accent: terracotta `#C2563A`, only for CTAs, Featured badge, and hover states
- hairlines: 1px borders
- radii: 0-4px
- layout: generous whitespace, large hero type, asymmetric grids
- tokens: HSL/OKLCH semantic variables in `src/styles.css`
- mobile-first: verified at 390px, no horizontal overflow, bottom sheet for unit details

Hebrew font correction:

- Hebrew display: Frank Ruhl Libre or another Hebrew-capable editorial serif
- Hebrew body/UI: Heebo or another Hebrew-capable clean sans
- English display: Fraunces allowed for LTR/English
- English body/UI: Inter Tight allowed for LTR/English

Fraunces and Inter Tight must not be the accidental fallback for Hebrew UI.

## Brand

Working direction: `Nadlan3D`.

- Wordmark: Nadlan + 3D depth treatment
- English tagline: `Real Estate, Rendered Real`
- Hebrew tagline: Hebrew equivalent to "real estate you can see before you buy"
- `nadlan3d.com` and `nadlan.ai` are prototype positioning only
- no legal/domain/social availability claim
- report must include availability-risk notes and at least three alternative names
- SVG logo component, not raster

## Showroom Prototype

Route:

`/showroom/$projectId`

Required asset-truth modes:

1. Rainbow: real GLB/model-viewer mode.
2. Dimri Yama: facade-first fallback mode, clearly labeled as concept/fallback.
3. Empty/missing asset state: premium contractor upload CTA.

Required UI:

- sticky project identity header
- visual stage
- floor/unit selector rail
- unit drawer or bottom sheet
- buyer journey strip
- footer dock: WhatsApp, Call, Save, Compare, Share
- non-binding CTA
- AI floor-plan placeholder with permanent illustrative watermark
- contractor upload portal stub, UI only

AI floor-plan fallback must never be presented as official.

## Listings Page

Route:

`/listings`

Required:

- magazine cards with hero render and floor-plan thumbnail
- project name, location, price-range chip
- badges: 3D, AI tour, Premium, Verified
- mini-stats: rooms range, sqm range, units left
- hover/tap interaction
- CTA: View showroom
- sticky sort/filter bar
- empty, loading, and error states

Ranking hierarchy:

1. paid tier
2. asset completeness
3. engagement
4. freshness
5. location boost

Paid tier must be transparent with visible labels such as Featured, Sponsored, or Promoted.

Data is mock-only for this run, with schema documented for the WordPress port.

## Sitewide IA

Routes:

- `/`
- `/listings`
- `/showroom/$projectId`
- `/cities/$city`
- `/guides`
- `/professionals`
- `/about`
- `/contact`

Global components:

- Nadlan3D nav
- HE/EN toggle
- WhatsApp button
- breadcrumbs on non-home routes
- footer with hub links and legal links
- mobile floating WhatsApp + AI concierge CTA

Each route needs unique `head()` metadata:

- title
- description
- Open Graph fields
- canonical
- hreflang HE/EN

Open Graph image only on leaf routes.

## Language

- Hebrew default.
- English complete enough for international investors.
- HE/EN toggle in nav and showroom.
- Real RTL/LTR behavior.
- centralized strings in `src/lib/i18n/{he,en}.ts`.
- AR/RU/FR are future backlog, no stubs this run.

## Required Handoff Outputs

Append to:

`handoff/lovable/2026-06-23-war-room-sync/`

Required files:

- `reports/02-showroom-prototype.md`
- `reports/03-listings-ia.md`
- `reports/04-brand-nadlan3d.md`
- `reports/05-fallback-floorplan-spec.md`
- screenshots for mobile 390px and desktop
- updated `source-manifest.md`

Required shared skills:

- `handoff/shared-knowledge/skills/nadlan-editorial-bright-tokens.md`
- `handoff/shared-knowledge/skills/nadlan-listings-ranking.md`
- `handoff/shared-knowledge/skills/nadlan-magazine-card.md`

If Lovable internally renames the token skill to `nadlan-cream-luxury-tokens.md`, keep the owner-requested filename as well or add a clear redirect note.

## Acceptance Gates

- 390px mobile: no horizontal scroll, bottom sheet works.
- HE RTL renders with Hebrew-capable fonts.
- EN LTR toggle works, hreflang present.
- Featured/Sponsored/Promoted labels visible.
- Floor-plan watermark present plus contractor CTA.
- Rainbow real GLB loads.
- Dimri facade fallback renders.
- Empty asset state shows.
- All four reports committed.
- Three shared skills committed.
- Screenshots committed in handoff folder.
- `source-manifest.md` updated by appending, not by wiping prior context.

## Deferred

- War Room dashboard: one-paragraph future-run outline only.
- Dubai/Cyprus/Greece/Thailand coded landings: deferred, not excluded.
- Hard markets and hard keywords: phased, not excluded.

## Credit Guardrail

If consumption crosses roughly 55 credits mid-build, Lovable must pause and report:

- what is done
- what remains
- estimated incremental credits

## Out Of Scope For This Run

- Lovable Cloud/backend
- real GLB upload pipeline
- WhatsApp ingestion
- payments
- Supabase
- AI Elements package
- server functions
- real AI floor-plan generation

## Codex Position

Approve this scope. It is specific enough to produce a useful prototype for Codex to port into WordPress later.

Critical watchpoints for Codex after Lovable commits:

- check actual mobile screenshots
- check Hebrew font rendering
- check that the GLB is real and not replaced by a fake placeholder
- check that source-manifest was appended safely
- check that paid ranking labels are visible
- check that the reports include enough implementation detail for `plugins/nadlan-config/inc/project-3d.php`
