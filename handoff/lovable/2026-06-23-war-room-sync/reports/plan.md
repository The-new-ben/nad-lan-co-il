## Goal

Stay in advisor mode. No code in this Lovable project, no writes to WordPress. Produce a complete, opinionated redesign + business brief for `nad-lan.co.il` — concept, showroom UX (Dimri Yama + Rainbow Tel Aviv + a 3rd pilot), monetization (advertiser-funded), foreign-buyer engagement, lead handling, and SEO money pages — grounded in:

- repo code (`plugins/nadlan-config`, `assets/projects/*`, `assets/js/nadlan-project-showroom.js`)
- live site shape (already screenshotted: home, `/project/dimri-yama/`, `/project/rainbow-tel-aviv/`)
- existing reports (`report-3a-real-semrush.md`, `rest-api-map.md`, `repo-inventory.md`, `advisor-notes.md`)
- competitor benchmarks (Zillow.com, OnTheMarket, JamesEdition, Daft.ie, Madlan, Yad2, Homeless)

Everything ships as markdown under `.lovable/reports/` — your team takes it to the WordPress repo as the implementation source-of-truth.

## Deliverables (8 new reports)

```text
.lovable/reports/
├─ 00-strategy-brief.md            # one-pager: thesis, target users, what we are vs what we're not
├─ 01-showroom-redesign.md         # the core piece: 3D + units + interior + view, mobile-first
├─ 02-design-system.md             # brand, type, color, icons, favicon set, RTL/LTR, dark/light
├─ 03-content-architecture.md      # IA, URL map, hierarchy of money pages vs supporting content
├─ 04-monetization-playbook.md     # contractor packages, placements, offers, auction, pricing
├─ 05-foreign-buyer-engine.md      # EN/FR/RU/ZH funnels, trust, currency, tax, concierge
├─ 06-lead-ops.md                  # routing, SLA, scoring, WhatsApp/email, CRM hooks via REST
└─ 07-seo-money-pages.md           # exact URL templates + on-page recipe per page type
```

Plus updates to `advisor-notes.md` after each report so context survives across chats.

## 01 — Showroom redesign (the heart of the request)

Three pilots side-by-side: **Dimri Yama, Rainbow Tel Aviv, + a 3rd we pick together** (Dimri Yama already has the richest payload; Rainbow has the real GLB and richest `environment.json`; the 3rd should be a counter-example — e.g. boutique low-rise or urban-renewal — to prove the template generalizes).

### Concept (one line)
"Pick a floor → pick a unit → step outside the window → step inside the apartment" — in a single page, in under 10 seconds, on a phone with one thumb.

### Critique of current state (from screenshots + JS)
- Hero card looks premium on desktop, but on mobile the gold/dark glass card stacks awkwardly and CTA hierarchy is unclear.
- Showroom uses 4 tabs (plan / tour / view / contact) that today only swap a paragraph of placeholder Hebrew copy — no real interactivity wired between unit-grid → 3D model → interior tour → exterior view.
- `<model-viewer>` is loaded but unit hotspots (`hotspot_position`, `camera_orbit` in `unit-map.json`) aren't actually driving the camera on click.
- Lead form sends a rich payload (good) but offers no price, no availability calendar, no FX (₪/$/€), no language toggle, no "save & share" — kills foreign-buyer intent.
- Two anomalies in `rest-api-map.md` (project-showroom 401, offers 404) silently break server-rendered showroom + offers placement.

### Proposed UX (mobile-first, 4 layers)
1. **Building layer** — full-bleed `<model-viewer>` with auto-orbit on idle; sticky bottom sheet "בחר דירה" (CTA). Sun simulator and view-from-balcony toggle are icon-pills on the right rail (thumb-reachable).
2. **Floor layer** — tap building → sheet expands to a vertical floor selector (numbers 1–N) + a tiny isometric facade hint. Each floor shows availability dots (green/amber/grey) by line (N/S/E/W).
3. **Unit layer** — tap floor → grid of units on that floor (line × type), each chip shows rooms · sqm · dir · status. Tap = camera orbits to the unit's hotspot (use the `hotspot_position` / `camera_orbit` already in payload).
4. **Inside the apartment** — unit detail drawer with 3 tabs: **תכנית** (SVG plan from `drawings.json`), **סיור פנים** (Matterport/Cupix iframe — provided by contractor), **מבט מהדירה** (panorama placeholder, replaced when contractor supplies real renderings). Persistent CTA strip: "אני מעוניין · WhatsApp · שמירה".

### What the contractor feeds (kit you sell them)
A single ZIP per project — schema goes in `02-design-system.md` and matches what's already in `assets/projects/<slug>/`:

- `model.glb` (≤ 20MB, draco-compressed)
- `poster.webp` (hero)
- `unit-map.json` (id, floor, line, rooms, sqm, dir, view, hotspot, price, status, plan URL, tour URL, view URL)
- `drawings.json` (floor plans SVG/PDF)
- `environment.json` (district context + neighbor projects)
- `view-layer-config.json` (sun, time of day, season)
- `material-intake-template.json` (what we still need from them)

Until they feed real assets, we keep clearly labeled prototype data — the payloads already enforce a `source_note` / `availability` disclaimer field. We honor that. No fake prices.

### Performance budgets
- GLB ≤ 20MB, served from CDN, draco + meshopt
- LCP ≤ 2.5s on 4G mid-range Android, INP ≤ 200ms
- `<model-viewer>` `reveal="interaction"` + low-res poster first
- Lazy-load Matterport iframe only after user taps "סיור פנים"

## 02 — Design system

- **Type**: pair a Hebrew display (Heebo / Frank Ruhl Libre) with a tighter Latin display for EN (e.g. Söhne / GT America) — current site is too uniform.
- **Color**: deepen the navy/gold scheme into a real token set (`--surface-glass`, `--surface-deep`, `--accent-gold`, `--accent-gold-quiet`, `--status-available/reserved/sold`). Status colors are the missing primitive.
- **Icons**: custom 24px set for floor / unit / view / sun / WhatsApp / save / share / FX — current pages use generic Unicode.
- **Favicon set** + `og:image` recipe per page type (project, listing, professional, area-info) — today `<title>` and OG are inherited from theme defaults on many pages (confirmed in earlier scan).
- **RTL/LTR**: per-language locale, not per-element flipping; mirrored icons for direction-sensitive glyphs.

## 03 — Content architecture (URL map)

Hierarchy answers your "money pages first, listings/professionals down":

```text
/                                    home — money-keyword hub
/projects/                           new-projects index (the showroom feed)
/projects/<slug>/                    showroom (Dimri Yama, Rainbow, …)
/for-sale/<city>/                    P0 money page — mirrors madlan template
/for-rent/<city>/                    P0 — lowest KD per Report 3A
/area-info/<hood>/                   compounding-authority pages (neighborhood data)
/new-projects/<city>/                KD-0 across the board per Report 3A
/guides/<topic>/                     editorial money articles (תמא 38, מחיר למשתכן tracker, …)
/professionals/<profession>/<city>/  pros directory — kept, demoted in nav
/listings/<id>/                      individual listings — kept, deep, not surfaced in main nav
```

The home nav surfaces money pages first (Projects, For-Sale by City, New Projects, Area Info, Guides) and pushes Professionals + Listings into a secondary menu.

## 04 — Monetization playbook (so contractors pay you)

Three SKUs, all built on REST endpoints that already exist (`offers`, `placement-auction`, `featured-upsell`, `advertiser-orders`, `tiers`, `greeninvoice-recurring`):

| Tier        | Price/mo (proposed) | What contractor gets |
|-------------|---------------------|------------------------|
| **Verified** | ₪ — (free)         | Listed in `/projects/`, basic card, lead capture |
| **Premium**  | ₪ 4–8K            | Full 3D showroom, sun sim, view layer, top-of-city placement, English page, WhatsApp routing |
| **Lighthouse** | ₪ 15–25K        | Premium + homepage hero rotation, foreign-buyer concierge package, retargeting pixel, monthly analytics PDF |

Plus a **placement auction** for "פרויקטים חדשים <city>" KD-0 pages (Report 3A) — contractors bid for one of 3 hero slots per city; uses the existing `placement-auction` endpoint.

## 05 — Foreign-buyer engine

This is currently absent. Build:

- `/en/`, `/fr/`, `/ru/`, `/zh/` mirrors of money pages (start with `/en/projects/<slug>/`).
- FX widget (₪ → $ / € / £ / ¥) inline on every price line — disclaimer the rate is indicative.
- Tax/legal explainer per persona (Aliyah buyer, non-resident investor, returning Israeli) — guide pages double as money-page anchors.
- Concierge intake: name, country, budget USD, intent (own/invest/Aliyah), timeline — routes to a human via existing `concierge-lead` endpoint with a `foreign_buyer=true` flag.
- Trust assets: video walkthroughs, contractor verification badge ("Premier · פרופיל מאומת" badge already on Rainbow — extend system-wide).

## 06 — Lead ops

- Single payload schema across showroom, generic CTA, WhatsApp, concierge (already roughly aligned in `nadlan-project-showroom.js` — formalize it).
- Routing rules: `unit + project + intent → owner` via `owner-config-rest.php`; foreign-buyer → concierge desk; ambiguous → round-robin to verified pros in city.
- SLA: 24h auto-reply with reference number (already in JS), 4h human response on Premium+.
- Scoring: budget × timeline × source → hot/warm/cold; surface in `admin-control/cards`.
- Drip + WhatsApp re-engagement using existing `lead-drip`, `lead-nurture`, `wa-lead`.

## 07 — SEO money pages (per Report 3A)

Concrete on-page recipe per template (title pattern, H1, intro block, FAQ schema, internal links, ad-slot placement, JSON-LD type). Sequenced by KD:

1. Rent-by-city (KD ≤ 22, ~20,920 vol/mo addressable)
2. New-projects-by-city (KD 0, lower vol but $2–5 CPC and direct contractor-monetization fit)
3. Area-info per neighborhood (compounding authority play)
4. Guides (תמא 38, מחיר למשתכן tracker, פינוי בינוי)
5. Sale-by-city (KD 50, last — needs authority earned from 1–4)

## Anomalies to flag for the WP team (not fixed by us)

1. `GET /nadlan/v1/project-showroom/<id>` → 401 unauth. Either intentional gate or regression — confirm.
2. `GET /nadlan/v1/offers` → 404 despite registration in `inc/offers.php:113`. Likely missing `require_once` or feature flag short-circuit.
3. `plugin-dist/` vs `plugins/nadlan-config/` divergence — confirm which is deployed.
4. `nadlan-project-showroom.js` doesn't drive `<model-viewer>` camera from `hotspot_position` / `camera_orbit` — wiring exists in data, missing in JS.

## What I need from you to start

Pick the 3rd pilot project (Dimri Yama and Rainbow Tel Aviv are locked) so report 01 has three real worked examples. Options I see in the repo / live site:

- a boutique low-rise (different mass, proves template scales down)
- an urban-renewal / תמא 38 project (different buyer persona)
- a peripheral-city large project (different price tier, foreign-investor angle)

Tell me which one (or name another), and I'll draft `00-strategy-brief.md` + `01-showroom-redesign.md` first, then the rest in order.

## Out of scope (still)

No React build here, no Lovable Cloud, no WordPress writes, no app-password use, no calls to billing/Woo. Pure advisor output as markdown reports.
