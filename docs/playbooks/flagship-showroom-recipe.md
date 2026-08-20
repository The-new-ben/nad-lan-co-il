# THE FLAGSHIP SHOWROOM RECIPE

**Purpose:** any capable model (ChatGPT, Codex, Claude) follows this document and
produces a nad-lan.co.il flagship project page at the H Infinity standard —
pixel-by-pixel, law-by-law — with zero access to prior conversations.
First designated execution: **Einstein 18 (Hagag, Tel Aviv)**.

Written 2026-08-13 while hot, from the H Infinity build (live v1.72.201,
post 6548, `/projects/h-infinity-somail-tel-aviv/`). The reviewing agent
(Claude) quality-gates every recipe execution against the gates in §10.

---

## 1. What "done" means

A foreign investor who has never been to Israel opens the page on a phone and
can decide like they are buying a stock: what the tower is, who builds it,
what surrounds it, what they would see from their window, what is verified
fact vs. pending — all tappable, all visual-first, in their language.
The owner opens the page and his jaw drops. Nothing less.

Definition of done, mechanically:
- Engine showroom boots with a 3D model (real or honest-generic), hotspots
  spread with logic, working unit scene, window view surfaced by default.
- Every displayed fact is either sourced or explicitly labeled pending.
- Verified with REAL screenshots (looked at, not DOM-diffed) on desktop 1280
  and mobile 390, in Hebrew + English at minimum.

## 2. Non-negotiable laws (owner canon — violating any one fails the build)

1. **HONESTY:** unknown stays unknown. Never invent rooms, sqm, status,
   direction, prices, tours, or imagery. Statuses vocabulary:
   `available | reserved | sold | unknown` (missing/invalid → `unknown`).
   Zero values NEVER render ("0 rooms" is a data gap, not information).
   Generic imagery/models are allowed ONLY with the explicit label
   "הדמיה ראשונית להמחשה · בהמתנה לחומרי היזם".
2. **THE BEAM IS FROZEN.** The golden direction beam on the map (beam v3:
   view-up rotation, cone fixed up, map rotates, pitch 52, zoom 15.9,
   3D-buildings layer `nl-bld-3d`, N tick, landmark chips) is one of the
   owner's most valuable assets. You do not change its layout, logic,
   rotation, styling, or behavior. You may build AROUND it (overlay chips,
   content below) only if the mechanism is untouched, and you must check
   fleet-wide side effects before deploy.
3. **INTENT-FIRST DNA:** title + first paragraph = substantive article lead
   about the project (status, delivery, developer, facilities). Disclaimers
   BELOW the lead, never the opening text. Affordance labels state the
   ACTION ("לחצו להסתכל מהחלון"), not a bare data value.
4. **ADDITIVE LAW:** features are never removed or levelled down. If page A
   has something B lacks, B catches up. Discovery of built features
   (blinking chips, linked tools) outranks building new ones. Nothing
   floats — in-flow UI only (dialogs excepted).
5. **EXPAND, don't condense:** the showroom gets room. No squeezed strips.
   Everything tappable on mobile (44px minimum targets). Visual language
   over text.
6. **No em/en dashes** in site copy — plain "-" only. No AI-sounding
   phrasing.
7. **ENGINE pages get the SR-provided h1 — the body must NOT add an h1**
   (guides pages are the opposite). Exactly one h1 per page, always.
8. **Content split:** the agent collects exact Compass/Zillow-grade data and
   builds the page; the 5,000-word × 5-language article is produced by the
   owner's ChatGPT from a prompt the agent writes, delivered as ZIP, then
   integrated. Agent never writes the mega-article itself.
9. **VERIFICATION:** nothing is "done/verified" without a real screenshot
   that was actually looked at. DOM checks are progress, not proof.
   (See §10 for the full gate list.)

## 3. Phase A — Research dossier (before touching WordPress)

Collect and ANCHOR every fact to a source (developer site, madlan, official
press, municipality). Required minimum:
- Tower(s): floors, unit count, architect, status (planning/construction/
  occupancy), delivery estimate if published.
- Address + streets that bound the plot; the compound/district story.
- Developer: full name, public-company status (TASE ticker if any), track
  record projects (prefer ones already on nad-lan).
- 6-8 NAMED landmarks with real coordinates (park, sea, rail station,
  hospital, square, sibling towers) — these feed the beam ring.
- Facilities list (pool/gym/lobby/retail...) — only what is published.
- What is NOT known: floorplans? unit mix? prices? Write the unknowns into
  the dossier explicitly — they define what the page must label pending.

Store the dossier in `docs/content/<project-slug>/dossier-start.md`.
H Infinity worked example: `docs/content/somail-flagship/dossier-start.md`.

## 4. Phase B — The card (post type `nadlan_project`)

Create the post (Hebrew base, slug without language suffix; language
variants share the slug + `-en`/`-fr`/`-ru`/`-ar`). Then seed EXACTLY these
metas (engine contract, from `inc/showroom-engine.php`):

| Meta key | Type / example (H Infinity) | Notes |
|---|---|---|
| `city` | `תל אביב יפו` | canonical city name — also the eyebrow fallback |
| `building` | free text | optional building descriptor |
| `num_floors` | `52` | int |
| `project_floors` | `52` | engine floors source; else max unit floor |
| `num_units` | `242` | TOTAL homes in project — feeds honest hero stat |
| `developer_name` | `קבוצת חג'ג'` | |
| `lat` / `lng` | `32.0846` / `34.7818` | decimal degrees |
| `geo_confidence` | `address-approx` | `city` DISABLES window view (honesty gate); use `address-approx` or better only when coords are truly the plot |
| `project_hero_eyebrow` | `מתחם סומייל · לב תל אביב` | per-project truth; empty → `city` meta → i18n default |
| `project_subtitle` | one-line tagline | hero lede |
| `project_model_glb` | uploads URL of the GLB | empty → honest generic standard-residential.glb + `model_generic:true` chip |
| `project_model_generic` | `1` when the GLB is a massing model, not developer geometry | renders the honesty chip |
| `project_model_poster` | poster SVG/JPG uploads URL | 3D loading frame |
| `project_3d_image` | same or marketing hero | hero/opening image |
| `project_3d_facade_images` | JSON `[{"src":"..."}]` | first src = facade for stage tiles; EMPTY facade collapses the stage → always provide poster+facade or the honest-concept state |
| `project_3d_floor_height_m` | `3.35` | window-view altitude + hotspot math |
| `project_3d_viewbox` | optional SVG viewBox | legacy stage |
| `project_facilities` | `בריכה,חדר כושר,מועדון דיירים,מסחר` | comma list, published facts only |
| `project_3d_video_url` / `project_3d_tour_url` | real URLs only | NEVER an invented tour |
| `project_3d_avg_price_per_sqm` + `project_3d_price_source_note` + `project_price_updated` | only with a real source | else omit — engine shows honest pending |
| `project_comps_json` / `project_faq_json` / `project_interior_panoramas` | JSON metas | real data only |
| `nl_unit_scene_v2` | `on` | enables the unit journey v2 |
| `project_env_landmarks` | see §6 | beam landmark ring |
| `project_3d_units` | see §5 | the units array |
| `project_tier` / `project_featured` | monetization ordering | leave default on new builds |

**Yoast:** focus keyword = "<project> <city>", meta title ≤ 60 chars with
brand tail, description with status + differentiator. Body: see §8.

## 5. Phase C — Units JSON (`project_3d_units`)

When the developer publishes no unit mix (normal for pre-sale towers), seed
ONE unit per floor, honest-empty, with hotspots spread by golden angle:

```python
import json, math
FLOORS = 52           # residential floors
FLOOR_H = 3.35        # project_3d_floor_height_m
BASE_Y = 10.0         # engine hotspot origin offset (podium)
units = []
for n in range(1, FLOORS + 1):
    az = math.radians((137.5 * n) % 360)   # golden-angle spread, no stacking
    r = 16.0                                # ~tower radius in meters
    units.append({
        "id": f"floor-{n:02d}",
        "floor": n,
        "status": "unknown",   # HONESTY: not "available"
        "dir": "",             # unknown direction stays empty
        "rooms": 0,            # zeros never render (engine law)
        "sqm": 0,
        "hotspot": {
            "x": round(r * math.sin(az), 2),
            "y": round(BASE_Y + (n - 0.5) * FLOOR_H, 2),
            "z": round(r * math.cos(az), 2),
        },
    })
print(json.dumps(units, ensure_ascii=False))
```

When real unit data exists (ToHa2 pattern), fill `rooms`, `sqm`, `dir`
(FULL word keys only: `north northeast east southeast south southwest west
northwest` as `north / north-east / east / south-east / south / south-west /
west / north-west` - the engine KNOWN_DIRS accepts these full forms or the
Hebrew labels, NEVER single letters; a `dir:"w"` seed left the SIX-8 beam
dead until 20.8.2026), real `status`, optional `balcony`,
`plan` (floorplan URL), `tour_url`. NEVER pad missing fields with guesses.

## 6. Phase D — Landmarks (`project_env_landmarks`)

Max 8, each with REAL coordinates and per-language labels:

```json
[
  {"lat": 32.0805, "lng": 34.7818,
   "label": {"he": "כיכר רבין", "en": "Rabin Square"}},
  {"lat": 32.0851, "lng": 34.7825,
   "label": {"he": "מגדלי DUO", "en": "DUO Towers"}}
]
```

The engine computes true bearings + distance bands (≤600m / ≤1800m / else)
for the beam ring. Empty meta = no ring — never invent a landmark.

## 7. Phase E — The GLB (massing model)

Use the pure-python glTF writer pattern in
`docs/playbooks/glb-gen-h-infinity.py`. Laws:
- SEG=64 ellipse segments, per-quad UNSHARED vertices, **NO normals**
  (client computes flat normals — byte-identical result, smaller file),
  uint16 indices, single buffer, single mesh.
- Parameterize: floors, floor height, ellipse radii top/bottom (taper),
  podium floors × height, crown height, secondary building offset.
  H Infinity: RX0/RZ0 15.5/12.5 → 14/11.5, FLOOR_H 3.35, POD 2×5.0,
  CROWN 6.0, boutique 9×7 at +24m east, 680KB / 23,104 tris.
- Budget: < 1MB, < 30k tris. Upload to WP media, set `project_model_glb`,
  set `project_model_generic=1` (it is massing, not developer geometry).
- Poster: generate a matching SVG (tower silhouette + gold sky) so the
  stage NEVER boots empty — an empty facade/poster collapses the theater
  to a black strip (H Infinity's first shipped defect — never again).

## 8. Phase F — What the engine gives you FREE once metas are right

Do NOT rebuild these; they key off the data:
- SR-h1 + hero with truthful eyebrow chain (meta → city → i18n).
- Honest homes stat: counts `status==="available"`; zero available → shows
  `units_total` as "דירות בפרויקט". Degenerate "high floors" stat hides
  itself when it duplicates the floors stat.
- Floor-BAND inventory: >24 units collapse into decade bands (50-52 /
  40-49 / ...), penthouse band first, only the active band renders,
  44px chip targets, true total in the results line.
- Unit scene v2: beam v3 (FROZEN, see §2.2) + landmark ring + honest
  "כיוון בבדיקה" states + gold "נוף מהחלון" chip pulsing on the beam
  (pulse ×3, `prefers-reduced-motion` honored).
- Window view: known bearing → free-camera at true floor altitude
  (pitch 86, drag to look around). Unknown bearing → HONEST 360° panorama
  from the real floor height, slow orbit (0.12°/2 frames, stops on touch/
  keys/hidden tab) + caption "כיוון החלון המדויק בבדיקה מול היזם — מוצג
  מבט פנורמי 360° מגובה הקומה". `geo_confidence: city` → no map at all
  (honest fallback text).
- Zero-honesty rendering on every fact strip/card (rooms/sqm/balcony only
  when > 0).
- Status dots + vocabulary, favorites, compare, recent strip, deeplinks
  (`?unit=floor-30&lang=en`), 5-language i18n (he/en/fr/ru/ar — HE+EN
  strings mandatory for new keys, others fall back).

If a feature above is missing on the new page, the DATA is wrong — fix
metas, do not fork the engine.

## 9. Phase G — Content blocks (body)

Structure (engine renders the showroom; body carries the article):
1. Article lead (intent-first, §2.3): what/where/who/status/delivery.
2. Non-affiliation disclaimer AFTER the lead.
3. "מה אפשר לעשות כאן" action chips (tappable anchors into the showroom).
4. Area/streets block: `מתחם X: הסביבה, הרחובות ומה שמסביב` — named
   streets, distances, transit (light-rail stations), landmark story.
5. Developer block: track record + public-company status; link the
   developer's other nad-lan pages.
6. NO h1 anywhere in the body. No em/en dashes. He first; EN/FR/RU/AR
   variants via the owner's ChatGPT flow (§2.8) on suffixed slugs.

## 10. Phase H — Design language (the pixels)

- Tokens (from `tokens.css` / engine css): ink `#11130f`-family darks,
  cream page background, gold spectrum `#c9a34f → #f4df9d` (gradients),
  chip gold `#f3d98c`, borders `rgba(243,217,140,.35-.55)`, dark glass
  `rgba(10,15,12,.82)` + `backdrop-filter: blur(6px)`.
- Chips/pills: radius 999px, min-height 36px (44px for primary/mobile),
  600-700 weight, 12.5-14px.
- Pulse pattern (attention without nag): box-shadow ring keyframes,
  2.2s ease-in-out, **3 iterations only**, disabled under
  `prefers-reduced-motion: reduce`.
- RTL: logical properties (`inset-inline-*`) EXCEPT stage tiles anchored to
  photos — those use physical left/top on purpose (photos don't mirror).
- Hebrew UI strings live in `i18n.js` per language block — never hardcoded
  in markup.

## 11. Phase I — Deploy pipeline (uPress WordPress, no FTP)

1. Auth: DPAPI-decrypt the app password JSON
   (`.codex-secrets/wordpress-app-passwords/nad-lan.co.il.json`,
   CurrentUser scope) → `Basic` header in `NLWP_AUTH` env. NEVER print it.
2. Bump `Version:` header + `NADLAN_CONFIG_VERSION` in
   `plugins/nadlan-config/nadlan-config.php` (they must match).
3. Lint: `node --check` every touched JS, `php -l` every touched PHP.
4. Ship via the proven script pattern (`scratchpad/deploy200.py` lineage):
   zlib+base64 payloads → WP media → temp snippet (name prefix `x-`,
   NEVER `tmp-`) registers `nlagent/v1` swap+probe routes → file swap with
   `.bakNNN` + MD5-in/MD5-written verify → probe (header AND constant) →
   `litespeed_purge_all` + `wp_cache_flush` + `opcache_reset` → deactivate+
   delete snippet + delete payload media.
5. Script cloning law: regenerate by full rewrite or careful sed; verify
   the `# -*-` header survived (a naive replace once beheaded the script
   → silent empty runs).
6. Transient 502s mid-deploy happen; files may still be written — re-probe
   before re-running, and sweep leftover `x-` snippets.

## 12. Phase J — QA gates (all must pass before "done")

- [ ] REAL screenshots, looked at: hero, showroom, unit scene, window
      view, inventory bands — desktop 1280 + mobile 390, he + en.
- [ ] Exactly one h1 (strip `<style>` blocks + comments before counting).
- [ ] Hebrew values in embedded JSON verified with the ESCAPED needle
      (`json.dumps(v, ensure_ascii=True)`) or key names — raw Hebrew
      text-search against page HTML lies.
- [ ] Client-rendered text claims proven ONLY by screenshot.
- [ ] Console clean on load + after opening each tool.
- [ ] Deeplink `?unit=floor-NN` boots into the unit scene.
- [ ] Every status/fact on screen traceable to dossier source or labeled
      pending. Zero invented values.
- [ ] Fleet regression: open ToHa2 (75 rich units) + one sde-dov page —
      inventory, beam, window view intact. A defect seen once is suspected
      fleet-wide; fix at the root, not per page.
- [ ] Mobile: every control reachable and tappable, nothing floats,
      nothing squeezed.
- [ ] The beam behaves EXACTLY as before your change (§2.2).

## 13. Worked example — H Infinity seed values (copy the shape, not the facts)

Post 6548, slug `h-infinity-somail-tel-aviv`. 52 floors + 7-floor boutique,
242 units total, arch' פרופ' משה צור, between ז'בוטינסקי/אבן גבירול/בן גוריון,
facilities בריכה/חדר כושר/מועדון דיירים/מסחר, status: under construction.
Landmarks: Rabin Sq 32.0805/34.7818, TLV City Hall, Ichilov, Yarkon Park,
Savidor Central, DUO Towers 32.0851/34.7825. Units: 52 × honest-unknown per
§5 with 137.5° spread. GLB per §7 exact parameters. Eyebrow
`מתחם סומייל · לב תל אביב`. Every one of these came from the dossier —
Einstein 18 gets ITS OWN dossier first (§3).

---

*Recipe author: Claude Fable 5, from the live H Infinity build. The
reviewing agent gates every execution of this recipe against §12 with real
screenshots before anything is called done.*
