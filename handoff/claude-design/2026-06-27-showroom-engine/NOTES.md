# NadLan Showroom Engine — Handoff Notes (Claude Design → Claude Code)

Date: 2026-06-27 · Branch target: `design/claude-design-showroom-engine` ·
Path: `handoff/claude-design/2026-06-27-showroom-engine/`

This is a **CMS-ready, not CMS-wired** front end. Vanilla HTML/CSS/JS. Every value the
UI shows comes from **`window.NADLAN_SHOWROOM`** (`engine/data.js`) or an **i18n key**
(`engine/i18n.js`). Nothing user-visible is hardcoded in HTML or `engine.js`. To port:
print the same payload from PHP, replace the i18n tables with the theme's translation
function, and it renders identically. The 3D/facade/posters are generated **concept**
assets labelled illustrative; swap `model_glb` / `facade_image` for real developer assets
with no other change.

---

## 1. Files

```
home.html              home gallery (data-page="home")
project.html           project page (data-page="project") — the Ashira template instance
engine/
  tokens.css           locked design tokens (copy of repo nadlan-tokens.css; fonts via Google for the prototype)
  showroom.css         all component styles (cream page + dark theater), RTL-first, mobile-first
  i18n.js              window.NADLAN_I18N — HE+EN complete, FR/RU/AR scaffold (EN placeholders)
  data.js              window.NADLAN_SHOWROOM — projects, units, spokes, areas, config
  engine.js            the engine: renders all blocks + interactions from data+i18n
  models/
    {slug}.glb           generated concept building (tower + podium + sea + Reading Tower + context city)
    {slug}-poster.jpg    hero/poster image (shown until the 3D paints — no blank flash)
    {slug}-facade.jpg    front elevation for the facade backup selector (1000×1333, matches viewbox)
screenshots/           desktop + mobile, HE + EN proof captures
NOTES.md               this file
```

Load order in each HTML shell: `tokens.css`, `showroom.css`, model-viewer module,
then `i18n.js` → `data.js` → `engine.js`. The only hand-written markup is
`<div id="nl-root" data-page="…"></div>`.

---

## 2. Block schema → implementation (buyer-facing, all modular + graceful-collapse)

| # | Block | Status | Source | Collapse rule (implemented) |
|---|-------|--------|--------|------------------------------|
| 1 | Language bar (HE/EN/FR/RU/AR) | interactive | `config.languages`, i18n | always on; sets `<html lang/dir>` |
| 2 | Hero / intent (RE H1 + facts) | interactive | `project` meta + i18n | facts derive from units |
| 3 | 3D theater + apartment select | interactive | `model_glb` + `units` | poster-until-paint; falls back to block 4 |
| 4 | Facade backup selector | interactive | `facade_image` + `viewbox` + `units[].stage_*` | hidden if no `facade_image` |
| 5 | Selected apartment panel (slide-out) | interactive | `unit` | empty-state prompt until select |
| 6 | Inventory (filterable) | interactive | `units` | hidden if `units` empty |
| 7 | Media (gallery/video/tour) | placeholder/collapse | `gallery`,`video_url`,`tour_url` | shows "media empty" if none |
| 8 | The complete world (map + spokes + stats) | interactive | `area.map`,`area.spoke_groups`,`area.stats`,`order` | each spoke group hides if `items` empty |
| 9 | Investor / foreign-buyer | interactive | i18n (per-language) | static points; hide per project if desired |
| 10 | SEO article body | placeholder | `project.content[lang].seo_h/seo_p` | owner fills prose |
| 11 | Inquiry / lead form (money moment) | interactive | posts to `config.lead_endpoint` | always on; carries unit context |
| 12 | Honesty / disclaimer band | interactive | i18n; gated by `config.demo` | always on |

**Home blocks:** RE hero, project gallery (cards from `order`+`projects`), list-with-us
(contractor funnel), language bar. Area entry points reuse the same spoke data.

**Elevate features (interactive):** save/favorite (localStorage `nl_favs`), compare 2–3
(panel → compare tray), deep-link `?project=&unit=&lang=`, sticky inquire + WhatsApp on
scroll, keyboard/focus (hotspots & cards are buttons; Enter/Space select; Esc closes),
poster-until-paint (no blank flash), camera clamps (product orbit, never underneath).

---

## 3. DATA fields — `window.NADLAN_SHOWROOM` (engine/data.js)

> Right column = the repo `nadlan_project` / showroom-payload field it maps to
> (see `docs/showroom-engine-wiring.md`). The engine already normalizes both names.

### config
`brand_key` · `lead_endpoint` (→ `/wp-json/nadlan/v1/lead`) · `whatsapp` (digits, empty hides WA) ·
`phone` · `demo` (bool → disclaimer/badges) · `default_project` · `default_lang` ·
`languages[]` · `rtl_languages[]`

### projects[slug]
| engine field | repo field | drives |
|---|---|---|
| `slug` | post slug | routing, deep-link |
| `area` | taxonomy/area ref | block 8 map+spokes |
| `building` | `building` | labels |
| `name_key` | (title → i18n key) | hero H1, cards, footer |
| `city_key` | meta | subtitles |
| `floors` | `project_floors` | hero fact, facade band count |
| `floor_height_m` | `project_3d_floor_height_m` | 3D hotspot Y |
| `viewbox` | `project_3d_viewbox` | facade frame aspect |
| `model_glb` | `project_model_glb` | 3D theater (**swap for real BIM/GLB here**) |
| `model_poster` | `project_model_poster` | hero image + poster-until-paint |
| `facade_image` | `project_3d_facade_images[].src` | block 4 backdrop |
| `default_orbit`/`default_target`/`frame_radius_m` | camera defaults | initial + reset framing |
| `orientation{west,south,east,north}` | `project_3d_environment_json.orientation` (→ i18n keys) | theater orientation pins |
| `concept` | `project_3d_demo` | illustrative labelling |
| `video_url`/`tour_url`/`gallery[]` | `project_3d_video_url`/`project_3d_tour_url`/media | block 7 |
| `content[lang]{tagline,hero_p,seo_h,seo_p}` | per-language post content | hero lede + SEO body (**owner fills**) |
| `units[]` | `project_3d_units` | everything unit-level |

### units[] (structured facts only; display strings composed via i18n)
`id` · `label` · `building` · `floor` · `rooms` · `sqm` · `balcony` · `dir` (enum→`dir_*`) ·
`status` (`available`/`reserved`/`sold` → `status_*`) · `recommended` · `view_key` (→ i18n) ·
`price_estimate_key` · `plan` (floor-plan url; empty → "coming") · `interior_url` · `tour_url` ·
`hotspot_position` (`hotspot_position`) · `hotspot_normal` (`hotspot_normal`) ·
`camera_orbit` (`camera_orbit`) · `stage_x`/`stage_y`/`stage_w`/`stage_h` (facade % box).

> **Concept-model note:** the generated GLB derives each hotspot's 3D point from
> `floor` + `dir` + `floor_height_m` (function `unitPos`), because the authored
> `hotspot_position` was for a different placeholder model. When real BIM arrives, set
> `model_glb` and the contractor's real `hotspot_position`/`camera_orbit`, and remove the
> derive step (or leave it as a fallback). The facade selector already uses the authored
> `stage_x/stage_y` directly.

### spokes[id] (shared hub-and-spoke records)
`id` · `type` · `icon` · `label_key` (→ i18n) · `geo{lat,lng}` (for real Mapbox port)

### areas[id]
`label_key` · `blurb_key` · `map{center{lat,lng},zoom,bbox{w,s,e,n},coast_x,project_pin{x,y},pins[{ref,x,y}]}` ·
`stats[{id,value,label_key}]` · `spoke_groups[{id,icon,label_key,items[spokeId]}]`

> **Map:** block 8 ships a **stylized SVG** map driven by `pins[].x/y` (% positions).
> Every pin/center also carries real `geo`/`bbox`/`center` lat-lng, so the WordPress port
> swaps in **Mapbox** using the same records with zero data changes. The owner asked for
> the real map experience — wire Mapbox GL in the port; pin data is ready.

### order[]
project slugs in catalog order (home gallery, footer, nearby-projects).

---

## 4. i18n keys — `window.NADLAN_I18N.langs[lang]` (engine/i18n.js)

`t(key, vars)` resolves `lang → en → he → key` and interpolates `{placeholders}`.
HE + EN complete. **FR / RU / AR are EN-placeholder scaffolds** (every slot present;
translators overwrite in place). Full key set:

- **brand/langs:** `brand` `brand_sub` `lang_he` `lang_en` `lang_fr` `lang_ru` `lang_ar` `city_tlv`
- **projects:** `proj_ashira_name` `proj_rainbow_name` `proj_dimri_name`
- **dirs:** `dir_west` `dir_east` `dir_north` `dir_south` `dir_south-west` `dir_north-west` `dir_south-east` `dir_north-east`
- **status:** `status_available` `status_reserved` `status_sold`
- **orientation:** `orient_sea` `orient_reading` `orient_district` `orient_district_north`
- **views:** `view_sea_reading` `view_district` `view_sea_court` `view_urban` `view_garden` `view_sea` `view_park` `view_coast` `view_court` `view_promenade`
- **composition:** `apt_word` `rooms_label` `floor_label` `sqm_unit` `unit_short` `price_on_request`
- **nav:** `nav_projects` `nav_areas` `nav_guides` `nav_list`
- **hero:** `hero_eyebrow` `hero_cta_primary` `hero_cta_secondary` `fact_floors` `fact_homes` `fact_from_floor`
- **theater:** `theater_eyebrow` `theater_title` `theater_hint` `view_3d` `view_facade` `legend_available` `legend_reserved` `legend_sold` `loading_model`
- **facade:** `facade_title` `facade_sub`
- **panel:** `panel_prompt` `panel_floor` `panel_rooms` `panel_sqm` `panel_balcony` `panel_view` `panel_dir` `panel_status` `panel_price` `tab_plan` `tab_view` `tab_tour` `plan_coming` `view_coming` `tour_coming` `btn_inquire` `btn_save` `btn_saved` `btn_compare` `btn_compared` `btn_share` `btn_close` `link_copied`
- **inventory:** `inventory_title` `inventory_sub` `filter_all` `filter_available` `filter_3` `filter_4` `filter_5` `results_count`
- **media:** `media_title` `media_empty` `media_gallery` `media_video` `media_tour`
- **world:** `world_eyebrow` `world_title` `world_sub` `map_title` `map_project_here` `spoke_transport` `spoke_education` `spoke_facilities` `spoke_anchor` `spoke_reading_tower` `spoke_beach` `spoke_light_rail` `spoke_yarkon_park` `spoke_school` `spoke_commercial` `spoke_road` `stat_plan` `stat_units` `stat_dunams` `stat_residents` `area_sde_dov` `area_sde_dov_blurb` `nearby_projects`
- **investor:** `investor_title` `investor_sub` `investor_pt_process` `investor_pt_legal` `investor_pt_finance` `investor_cta`
- **seo:** `seo_eyebrow`
- **inquiry:** `form_title` `form_sub` `form_name` `form_phone` `form_email` `form_submit` `form_submitting` `form_success` `form_error` `form_consent` `form_unit_ctx` `form_no_unit` `whatsapp_cta` `sticky_cta`
- **compare:** `compare_title` `compare_empty` `compare_clear` `compare_inquire`
- **disclaimer/badges:** `demo_badge` `disclaimer_title` `disclaimer_text`
- **home:** `home_hero_eyebrow` `home_hero_title` `home_hero_sub` `home_search_area` `home_search_type` `home_search_cta` `home_gallery_eyebrow` `home_gallery_title` `home_gallery_sub` `card_explore` `card_units` `home_areas_title` `home_areas_sub` `home_list_title` `home_list_sub` `home_list_cta`
- **footer:** `footer_tagline` `footer_rights` `footer_col_projects` `footer_col_areas` `footer_col_company` `footer_col_langs`

---

## 5. Lead payload (POST `config.lead_endpoint`)

```json
{ "source":"showroom_engine", "project_slug","project_title","lang",
  "name","phone","email",
  "unit","floor","rooms","sqm","direction","status",
  "message" }
```
Carries the selected unit context. On no backend it shows the local thank-you (prototype).
Wire to the existing `/wp-json/nadlan/v1/lead` route — straight swap.

---

## 6. Multilingual / hreflang

Per `docs/plans/2026-06-27-ashira-multilingual-architecture.md`: **no plugin, one page per
language under `/projects/`**. The reciprocal hreflang set (he/en/fr/ru/ar + x-default) is
included in `project.html` **as an inert HTML comment** — it must stay inert until every
language page exists on its final URL and passes QA. Claude Code emits it server-side from
the publication manifest at publish time. Language switch here is client-side for preview;
production serves separate crawlable URLs.

---

## 7. Concept vs real (honesty)

- **Generated, illustrative:** `{slug}.glb`, `{slug}-poster.jpg`, `{slug}-facade.jpg`,
  the stylized SVG map. All labelled `הדמיה להמחשה` / "Illustrative"; disclaimer band ships.
- **Placeholder text (owner fills):** `content[lang].hero_p/seo_h/seo_p`, `area_*_blurb`,
  FR/RU/AR translations. Marked with `⟦…⟧`.
- **Real / structured:** all unit facts, statuses, directions, floor counts, area stats
  (sourced public Sde Dov figures — verify before publish), spoke records, coordinates.
- No internal/engineering words appear on any buyer surface. No em-dashes. No invented
  prices (estimate-on-request only).

---

## 8. Implementation notes for the port

- **model-viewer + RTL:** the stage is forced `direction: ltr` (`.nl-stage`) — without it,
  model-viewer mirrors hotspot X in an RTL document. Keep this in the port.
- **Framing:** camera radius is in **meters** (`frame_radius_m`) because the scene includes
  large sea/ground planes; `%` radius would shrink the tower. `min/max-camera-orbit` clamp
  the polar angle so the building is never seen from underneath (product orbit).
- **Poster-until-paint:** `#nl-poster` covers the stage until model-viewer fires `load`,
  then fades. Prevents the known blank-flash on load.
- **Accessibility:** hotspots/cards are real buttons with aria-labels; Enter/Space select;
  Esc closes the panel; `:focus-visible` ring from tokens; `prefers-reduced-motion` honored.
- **Performance:** one GLB + one poster per project (~100–200 KB GLB, ~80–100 KB jpg).
  Self-host fonts in production (tokens.css note).
