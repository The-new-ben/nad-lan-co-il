# Advisor session notes

Running log so context survives across chats. Newest at top.

## 2026-06-22 — redesign plan approved, reports 00 + 01 drafted

User approved the 8-report plan. Picked **urban-renewal / תמא 38** as the 3rd pilot (Dimri Yama and Rainbow Tel Aviv locked). Slug still TBD — needs pick from existing WP catalog.

Drafted:
- `00-strategy-brief.md` — thesis, target users, what we are / aren't, sequencing.
- `01-showroom-redesign.md` — full UX spec: 4-layer mobile-first showroom, exact JS wiring spec for hotspots/orbit, contractor-kit schema, performance budgets, per-pilot notes, monetization slots, WP eng checklist.

Key unblockers for the WP team (not us):
1. `nadlan-project-showroom.js` never reads `hotspot_position` / `camera_orbit` from `unit-map.json`. ~30 lines to wire. Spec in §4 of report 01.
2. `/wp-json/nadlan/v1/project-showroom/<id>` returns 401 — confirm intent or fix.
3. `/wp-json/nadlan/v1/offers` returns 404 despite registration in `inc/offers.php:113`.
4. Dimri Yama `model-prototype.glb` is an 8KB stub — replace before contractor pitch.
5. `plugin-dist/` vs `plugins/nadlan-config/` drift — confirm which is deployed.

Next reports queued: 02 design-system, 03 content-architecture, 04 monetization-playbook, 05 foreign-buyer-engine, 06 lead-ops, 07 seo-money-pages.

## 2026-06-22 — session bootstrap

**Mode:** read-only advisor. No code changes to this Lovable project. No writes to WordPress. No Cloud/Supabase. All findings live in `.lovable/reports/`.

**Sources connected:**
- GitHub: `The-new-ben/nad-lan-co-il@main` (1,070 files, public).
- Live REST: `https://nad-lan.co.il/wp-json/` — namespaces `nadlan/v1`, `auctions/v1`, plus stock WP/Woo/Yoast/Jetpack/GSK.

**Plugin / WP versions on prod:** `nadlan-config 1.68.2`, PHP 8.5.5, WP 7.0.

**First-pass deliverables in this folder:**
- `repo-inventory.md` — area-by-area code map.
- `rest-api-map.md` — every `nadlan/v1` + `auctions/v1` route → handler file:line + live probe result.

**Open questions for next turn (no action taken — flagged for you):**
1. `GET /nadlan/v1/project-showroom/<id>` returns **401** unauthenticated. The 3D showroom spec implies public read. Intentional gate (e.g. nonce-only) or regression?
2. `GET /nadlan/v1/offers` returns **404 `rest_no_route`** even though `inc/offers.php:113` registers it. Either (a) `offers.php` isn't being `require_once`d in `nadlan-config.php`, (b) a feature flag short-circuits the load, or (c) `plugin-dist/` (deployed) diverges from `plugins/` (source). Worth checking next.
3. `/nadlan/v1/map` returned `count: 0` — no listings on prod or a default scoping issue?
4. `plugin-dist/` mirrors `plugins/nadlan-config/`. Confirm which one is actually deployed and whether one is generated from the other.
5. If you want me to verify authenticated routes (`/studio/mine`, `/admin-control/cards`, `/project-showroom/<id>`), provide an Application Password — I'll store it via `add_secret`, never echo it, and only GET.

**Pending reports (will draft on request):**
- `content-model.md` — drill into `nadlan_property` / `nadlan_project` / `nadlan_professional` field shapes by probing `wp/v2/<cpt>` and cross-reading `catalog-meta.php`.
- `docs-vs-reality.md` — reconcile the `docs/2026-06-*` specs (offers, 3D, multilingual, lead AI) against what's actually wired in the plugin.
