# NadLan Showroom — Block Schema & Engine Contract (the DNA)

> Date: 2026-06-27. Owner-approved architecture. This is the durable source of truth
> that both Claude Design (front-end) and Claude Code / Codex (WordPress port) build
> against. It is a system, not a one-off page. Ashira is the first instance; every
> future project, listing and urban-renewal page fills the same schema.

## 0. Operating principles

1. **Modular.** Every block is independently toggleable per project. Removing a
   parameter is a one-flag change, never a redesign.
2. **Graceful collapse.** If a block's data is absent, the block hides cleanly. No
   empty box, no placeholder, no fake.
3. **No stacking.** One design system. Replace at the source. Never layer over a
   baked-in image or an old stylesheet.
4. **Real estate first.** Headlines, SEO and language are about buying apartments.
   The 3D is the moat, never the keyword.
5. **Two faces, one system.** Buyer-facing and contractor-facing are separated at the
   architecture level. The buyer never sees the contractor's technical layer.
6. **Data-driven.** Every block renders from the `window.NADLAN_SHOWROOM` payload.
   Concept visuals today, real GLB/BIM later by swapping one field.
7. **Honesty.** Concept models and facades are labelled illustrative. Non-binding
   price estimates only. No invented facts.

## 1. Project page — buyer-facing blocks (all modular)

| # | Block | Data source | Collapse rule |
|---|---|---|---|
| 1 | Language bar (HE/EN/FR/RU/AR) + reciprocal hreflang | system | always on |
| 2 | Hero / intent band: real-estate H1 + first paragraph above fold + key facts | project meta | hide facts row if absent |
| 3 | Showroom stage: air-world 3D building, spin animation, apartment polygon-select | GLB/concept + units | fall back to block 4 |
| 4 | Facade backup selector: labeled squares, direction, per-square data, contractor-ID ready | facade image + viewBox + unit polygons + direction | hide if no facade |
| 5 | Selected apartment panel (slide-out): rooms/sqm/floor/dir/view/plan/estimate/inquiry | unit | — |
| 6 | Inventory list (filterable, mirrors stage) | units | hide if none |
| 7 | Media: gallery / video / tour (click-to-load) | contractor-fed media | hide if none |
| 8 | The complete world (spokes): location+anchor, transport, education, facilities, area stats, nearby projects | shared spoke records | hide empty spokes individually |
| 9 | Investment / foreign-buyer module | per-language | hide per project |
| 10 | SEO article body (editorial rhythm, not wall of text) | per-language content | — |
| 11 | Inquiry / lead form -> `/wp-json/nadlan/v1/lead` | system | always on |
| 12 | Honesty / disclaimer band | system | always on |

## 2. Facade backup selector (block 4) — explicit spec

The facade is NOT scrapped. It is the deliberate fallback for mobile and for buyers
who struggle to select on the rotating 3D stage.

- Distinct squares per apartment, drawn from the payload `viewBox` + unit polygons.
- Each square shows direction (front / sea / city / back) and per-unit data.
- Built so a contractor-supplied facade identification (real per-unit mapping) can
  drop in later with no redesign — today the mapping is authored, tomorrow contractor-fed.
- Selecting a square drives the same selected-apartment panel (block 5) as the 3D stage.

## 3. Homepage blocks

1. Real-estate hero (buyer intent).
2. Project gallery / slider — addable cards (Rainbow, Ashira, future). Adding a project
   is a data entry, not a new design.
3. Area / region entry points (spokes as discovery surfaces).
4. List-with-us (contractor funnel).
5. SEO content.

## 4. Contractor-facing (separate — WordPress build; Claude Design designs UI only)

A login dashboard, never rendered to buyers:
- upload facade photo, GLB/BIM, video, gallery
- set units, prices, status, availability
- mark facade identification (per-unit mapping)
- preview the buyer page
Internal/technical language lives here only, never on a buyer surface.

## 5. Spokes are shared entities (the hub-and-spoke database)

A spoke (an area, a school, a transit line, an anchor like the Reading Tower) is one
record. Multiple projects point to it. Ashira and Rainbow both reference the same
"Sde Dov area" spoke. Change once, both update. Spokes can graduate into their own
pages (area pages, glossary, terms) — the same data, more surfaces.

Relationship model: `project  <->  area  <->  spoke (POI / stat / transit / school)`.

## 6. Engine contract (front-end <-> WordPress)

- The engine renders from `window.NADLAN_SHOWROOM` (a single project payload, a map of
  projects, or the raw repo payload shape). WordPress prints it before the component.
- Field correspondence is normalized (see `docs/showroom-engine-wiring.md`): `units` /
  `project_3d_units`, `model_glb` / `project_model_glb`, `poster` /
  `project_model_poster`, `position` / `hotspot_position`, `orbit` / `camera_orbit`,
  `plan`, `floor`, `rooms`, `sqm`, `dir`, `view`, `status`.
- Swap to official BIM/GLB by setting `project_model_glb` — no other change.
- Lead endpoint: `/wp-json/nadlan/v1/lead` (existing route).

## 7. Design tokens (locked)

`--cream:#FAF7F1; --ink:#1B1A17; --gold:#9C7A3C; --terracotta:#C2563A (accent/CTA only);
--sage:#7A8F6A; --border:#D9D2C4; --muted:#6B6457; --radius:0.25rem`.
Fonts: Hebrew -> Frank Ruhl Libre (headings) + Heebo (body); English -> Fraunces +
Inter Tight. Direction: cream editorial page with a dark immersive 3D theater as the
dramatic centerpiece. One soft shadow, 1px hairlines, generous whitespace, motion on
interaction. Editorial rhythm per `skills/article-guide-design-pattern.md` — not
headline-then-text boredom.

## 8. Keep vs scrap (decided)

- KEEP: the air-world 3D stage with apartment-select (the moat), the spin animation,
  the language pills, cream as the base, the facade as the backup selector.
- SCRAP/FIX: flat boring execution (cure = contrast + depth + editorial rhythm),
  baked-in-UI hero images, the dark-teal-vs-cream wobble (decision: cream page + dark
  3D theater).

## 9. Division of labor

- **Claude Design**: front-end look + interaction (blocks 1-12 design, facade clicker,
  3D polygon select, homepage gallery, language pages). Pushes to the handoff branch
  (section 10). Does not write final marketing/area content — placeholders only.
- **Claude Code / Codex**: port to WordPress, wire CMS fields, the spoke database, the
  contractor dashboard, Mapbox, leads, billing, hreflang output. Fill verified content.
  Gate every release with screenshots before the owner deploys.
- **Owner**: deploys, approves content, supplies contractor assets.

## 10. Where Claude Design pushes its output

Branch: `design/claude-design-showroom-engine`
Path: `handoff/claude-design/2026-06-27-showroom-engine/`
- `index.html` (or `home.html`) — homepage gallery
- `project.html` — Ashira project page (the template instance)
- `engine/` — the data-driven engine (HTML/CSS/JS)
- `screenshots/` — desktop 1280/1440 + mobile 390, HE and EN, per component
- `NOTES.md` — what each block maps to, what is placeholder, what is interactive

Claude Code pulls from that branch/path and ports into the WordPress theme + plugin.
