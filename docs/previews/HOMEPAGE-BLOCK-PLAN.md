# NadLan Homepage — block-by-block build plan (the thing we follow)

Ground truth design target: `docs/previews/nadlan-homepage-target.html`
(live view: https://raw.githack.com/The-new-ben/nad-lan-co-il/main/docs/previews/nadlan-homepage-target.html)

We iterate on a PREVIEW (`docs/previews/nadlan-homepage-vN.html`), one block at a time.
Each round: I apply the block, regenerate the preview, render HE + EN screenshots, and report
files + links + what it wires to + chain of reaction. Only after the owner approves a block do
we WIRE it into the live system (theme pattern + CMS + engine), real data, no mock, no fallback.

## Standing rules
- Light, minimal-gold, premium. Architectural coil/line **sketches**, NO AI/photo images.
- Buyer intent first (buy an apartment / read real estate). NO bragging about features/languages.
- Real estate breadth: projects + listings + news + areas + tools + professionals (SEO signals).
- Rich info per asset (Zillow/Compass/Madlan-class), all wired to CMS when live.
- Full multilingual: the homepage renders fully in he/en/fr/ru/ar (not a string swap that goes nowhere).
- Coherent with the previous theme, the internal pages, the sitemap, the GLB/engine locations.

## Where the engines + assets live (so we never lose them)
- Homepage gallery engine (preview/theme): `assets/js/nadlan-showroom-engine.js` + data `assets/engine/projects.json`
- Homepage 3D models (GLB): `assets/engine/rainbow.glb`, `assets/engine/dimri.glb`, `assets/engine/ashira.glb`, posters `assets/engine/*-poster.*`
- Project-page showroom engine (plugin, CMS-wired): `plugins/nadlan-config/inc/showroom-engine.php` + `plugins/nadlan-config/assets/showroom-engine/` (engine.js, showroom.css, i18n.js, mapbox-init.js) + models in `plugins/nadlan-config/assets/showroom-engine/models/`
- Live homepage render: `functions.php` front-page filter -> `patterns/nadlan-home-showroom.php` (gated by the `nadlan_revenue_use_home_showroom` filter)
- Map: Mapbox (`nadlan_mapbox_token` WP option, already set live); coordinates per project (geo meta / projects.json)

## The blocks (in order)
1. **Language** (current) — full he/en/fr/ru/ar page render + working switcher (dir + every string). HE+EN complete; fr/ru/ar scaffolded for Cowork's translated content.
2. **Hero + search** — buyer promise + a real search affordance (area/type/rooms), sketch building art (no AI image).
3. **Project gallery selector** — switch Ashira/Rainbow/Dimri, real GLB 3D, real unit panel, the sun/orientation back, all wired to CMS.
4. **Price + comps** — real recorded transactions + non-binding range + source (already real for Ashira).
5. **Map + surroundings** — real Mapbox, correct coordinates (Cowork supplies), real POIs, sun arc.
6. **Project cards** — sketch thumbnails + rich facts.
7. **Area hubs** — Sde Dov / Ramat Aviv etc., wired to the area pages.
8. **Listings** — apartments for sale (needs `nadlan_property` content; Cowork creates).
9. **News / magazine** — Nadlan news (needs posts; Cowork creates).
10. **Tools** — calculators (wired to the existing calculator pages).
11. **Professionals teaser** — wired to the 2,711 directory.
12. **Footer mega-menu** — like the previous theme; sitemap-coherent.

## Wire-after-approval checklist (per block)
- Replace the matching section in `patterns/nadlan-home-showroom.php` (live homepage).
- Wire data to CMS (`nadlan_project` meta / queries), no static mock.
- Selectors stay anti-stack (one renderer, one band, one model per surface).
- Bump/deploy: theme via UPress git-pull; plugin via versioned ZIP + Update.
- Report files + links + chain.

## Status log
- Target saved: `docs/previews/nadlan-homepage-target.html` (PR #267).
- Block 1 (language): preview in progress.
