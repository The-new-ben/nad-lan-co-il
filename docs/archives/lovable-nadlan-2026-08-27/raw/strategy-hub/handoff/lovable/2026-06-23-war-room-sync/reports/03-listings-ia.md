# Report 03 — Listings + Sitewide IA

Sync date: 2026-06-23

## Sitewide IA

| Route                       | Purpose                                       | File                                  |
|-----------------------------|-----------------------------------------------|---------------------------------------|
| `/`                         | Homepage — hero, 3 featured cards, value strip| `src/routes/index.tsx`                |
| `/listings`                 | Magazine grid + filter/sort + ranking note    | `src/routes/listings.tsx`             |
| `/showroom/$projectId`      | Interactive showroom (see report 02)          | `src/routes/showroom.$projectId.tsx`  |
| `/cities/$city`             | City hub (TLV, Haifa, Jerusalem, Ashdod, …)   | `src/routes/cities.$city.tsx`         |
| `/guides`                   | Editorial hub stub                            | `src/routes/guides.tsx`               |
| `/professionals`            | Professional hub stub                         | `src/routes/professionals.tsx`        |
| `/about`                    | Brand statement + prototype disclaimer        | `src/routes/about.tsx`                |
| `/contact`                  | Demo form                                     | `src/routes/contact.tsx`              |

Global chrome (root layout): `SiteHeader` (Nadlan3D mark + nav + HE/EN toggle) and `SiteFooter`.

### Head meta rules applied
- Every leaf route owns its own `title`, `description`, `og:title`, `og:description`, `og:url`, and `<link rel="canonical">`.
- `og:image` set **only on the leaf** showroom route (per the `head-meta` rules — root layout is image-free so it doesn't override leaf previews).
- `hreflang` alternates declared for HE / EN on every shareable route. EN query convention is `?lang=en` (real switch is client-side via `LangProvider`; the alternate URLs are documented so Codex can move to subdirectories or subdomains without rewriting routes).
- Organization JSON-LD on root.

## Listings page

`/listings` magazine grid. Each card is a `MagazineCard` (see skill `nadlan-magazine-card`).

### Filter / sort bar
- City (derived from data, language-aware)
- Rooms (3/4/5/6)
- "Complete listings only" toggle (≥ 0.75 completeness)
- Order is the ranking hierarchy (below), applied after filters

### Ranking hierarchy (canonical — also in skill `nadlan-listings-ranking`)
1. **Paid tier** (`featured` > `promoted` > `standard`) — always wins ties
2. **Asset completeness** (GLB present, plan present, photos, price, rooms)
3. **Engagement** (mock CTR proxy)
4. **Freshness** (`updated_at` desc)
5. **Locality boost** (city affinity)

### Transparency labels (owner guardrail #5)
- `Featured` badge on the card (terracotta accent)
- `Promoted` badge (ink/inverted)
- Paid placements (featured & promoted) always also carry a `Sponsored` chip
- A standing transparency `<aside>` at the bottom of the listings page explains the order in both languages

## Mock data → real data migration path

`src/lib/projects.mock.ts` is intentionally shaped to mirror the `nadlan/v1/projects` WordPress REST endpoint:

```ts
{ id, slug, name_he, name_en, city_he, city_en, developer,
  status, paid_tier, priceFromILS, rooms, asset_state, model_url,
  hero_image, plan_image, completeness, engagement, updated_at,
  city_boost, units, tagline_he, tagline_en }
```

Codex can port this 1:1 — same field names — when wiring real data.

## Deferred (outlined only this run)

### War Room dashboard (future)
A single-page operator console: live ranking board, paid-tier overrides, asset-state queue (which projects need a GLB or a real plan), engagement spikes, contractor onboarding pipeline, AI-generated-plan governance log. Expected addition: ~25–40 credits in its own run. Will sit at `/war-room` behind an auth gate (Lovable Cloud + role check via `has_role`).

### Country landings (Dubai, Cyprus, Greece, Thailand)
Phased — not excluded. Each is a landing + listings grid in its own locale. Order: Cyprus (lowest legal friction for Israelis) → Greece (golden visa) → Dubai (highest demand, hardest market) → Thailand. ~20 credits per pair.

### Hard markets / hard keywords
Phased per ambition guardrail — not removed from strategy.

