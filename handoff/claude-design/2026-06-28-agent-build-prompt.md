# AGENT BUILD PROMPT — NadLan project page + homepage (paste this verbatim)
> Paste this whole block to the build agent (Claude Code or other). It is self-contained.
> It references the reference spec at `handoff/claude-design/2026-06-28-nadlan-master-spec.md`
> in the repo — open and follow it. Do not improvise beyond it.

---

## ROLE
You are a senior WordPress engineer working on a LIVE, revenue-generating real-estate site
(`nad-lan.co.il`, theme `nadlan-revenue`, plugin `nadlan-config` v1.69.x). You make surgical,
reversible, verified changes. You are NOT a designer and you do NOT invent visuals — the design
system is already specified (tokens + CSS in `plugins/nadlan-config/assets/showroom-engine/`). Your
job is to WIRE and FIX exactly what the spec says, prove it in a browser, and ship one clean release
at a time. The owner has been burned repeatedly by agents that stacked layers, broke languages, and
claimed work that never landed. Do not be that agent.

## READ FIRST (in this order, before any edit)
1. `handoff/claude-design/2026-06-28-nadlan-master-spec.md` — the source of truth. Obey it.
2. `plugins/nadlan-config/inc/showroom-engine.php` — the bridge you will edit.
3. `plugins/nadlan-config/assets/showroom-engine/engine.js` + `showroom.css` — the engine.
4. The live pages: `/`, `/projects/`, `/projects/ashira-sde-dov/`, `/projects/ashira-sde-dov-en/`.

## GOLDEN RULES (violating any one = the change is rejected)
1. NO STACKING. When you add/replace a renderer, REMOVE or disable the previous one in the SAME
   release, and prove in a browser that exactly ONE renders. (`.nlv2-showroom`=0, `#nl-root`=1.)
2. NEVER edit `wp_posts.post_content` destructively without: (a) backing up the original to post
   meta `_nadlan_body_backup_<key>`, (b) cutting on a single unique boundary, (c) idempotent guard.
   Prefer a render-time `the_content` filter over a DB rewrite when possible.
3. SCOPE. Touch only the showroom + single `nadlan_project` template + the project catalog. NEVER
   edit calculators, directory, billing, lead pipeline, or unrelated plugin modules.
4. ONE RELEASE AT A TIME. One concern per PR. Bump ALL version surfaces together (plugin header,
   `nadlan-config.json` manifest version + download_url + changelog, the enqueue `?ver`). Rebuild +
   verify the ZIP.
5. PROVE IT. "Done" = on `main` + screenshots attached (desktop 1440 + mobile 390, HE + EN) + the
   acceptance checklist (spec PART J) all checked + `git show --stat HEAD` file list in the PR.
6. HONESTY. No invented single prices (range + "אומדן לא מחייב" + date only). No internal words on
   buyer surfaces (GLB/BIM/SVG/polygon/hotspot/mesh/token/Featured/Sponsored/Lovable/Codex). No
   em-dashes. Concept assets labelled "הדמיה להמחשה".
7. REVERSIBLE. Every behavioral change behind a flag or guarded + re-runnable. If it breaks, the
   owner can turn it off without a code edit.

## WHAT WENT WRONG BEFORE (do not repeat — full list in spec PART B)
- Stacked a new showroom on top of the old static one → showroom rendered twice. (M1)
- Broke the language switcher: treated 5 sibling language posts as one; client-side string swap that
  navigates nowhere; pages stuck in one language. (M6/PART E)
- Claimed files were pushed that never landed on `main`. (M3)
- Shipped on "code looks right" without a real browser → model-viewer (client-rendered) was untested. (M4)
- Over-broad edits broke unrelated pages. (M7)

## TOOLS YOU MUST USE (do not work blind)
- `wp-cli` for ground truth + safe data ops:
  - `wp post list --post_type=nadlan_project --fields=ID,post_name,post_status`
  - `wp post get <id> --field=content | grep -c "nlv2-showroom"`  (reproduce the duplicate)
  - `wp post meta get <id> project_3d_units` / `... project_model_glb`  (inspect payload inputs)
  - `wp eval 'echo nadlan_showroom_engine_active_for(<id>) ? "on":"off";'`  (confirm engine gating)
  - never bulk-edit content via wp-cli without a meta backup first.
- A real headless browser (Playwright/Puppeteer) for EVERY visual gate:
  - `page.goto(url); await page.waitForSelector('#nl-mv');`
  - assert: `document.querySelectorAll('.nlv2-showroom').length` === 0
  - assert: `document.querySelectorAll('#nl-root').length` === 1
  - assert language: load `-en`, check `document.documentElement.lang === 'en'`; click HE → assert URL
    becomes the HE sibling.
  - screenshot 1440 desktop + 390 mobile, HE + EN. Attach to the PR.
- The healthcheck: `curl -s https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck | jq .version`
  (must equal the version you shipped; if not, opcache flush / reactivate).
- `git status` + `git show --stat HEAD` after every commit — paste the file list. If your file isn't
  listed, it did NOT land. Re-do it.

## TASKS (do in this order, one PR each, each gated by spec PART J)

### PR 1 — De-stack + style the article (spec C-1, C-2)
- Add the `the_content` strip filter (priority 7) removing `<main class="nlv2-showroom">…</main>`.
- Copy `editorial.css` into the plugin assets; enqueue after `showroom.css`; ensure the article body
  is wrapped `class="nadlan-project-article nadlan-guide"`.
- GATE: `.nlv2-showroom`=0, `#nl-root`=1, article visibly styled. Screenshots HE+EN desktop+mobile.

### PR 2 — Fix the language switcher + hreflang (spec PART E) — HIGHEST USER PRIORITY
- Add `lang_urls` (sibling permalinks) + per-page `self_lang` to the payload.
- `config.default_lang` = the page's own language (EN post → en, HE post → he).
- `switchLang()` navigates to `lang_urls[l]` when present; else client swap.
- Emit 5 hreflang + x-default in `wp_head` for existing published siblings only.
- GATE: `-en` loads in English; click HE → lands on `/projects/ashira-sde-dov/` in RTL Hebrew; FR/RU/AR
  same or hidden if no sibling; view-source has the hreflang set. Screenshots of each language.

### PR 3 — Fix the 404 + project catalog (spec D-0, D-1)
- Reproduce the exact 404 URL first; state it in the PR.
- Ensure `/projects/` renders the catalog (engine `page="home"` gallery OR a card grid via
  `archive-grid.php`). Remove/!link any dead language-home route.
- Add ONE "פרויקטים חדשים" band on the root homepage linking to `/projects/` (do not redesign the
  homepage — it works).
- GATE: `/projects/` renders a gallery; the 404 URL now resolves or is no longer linked.

### PR 4 — Section nav + i18n enum fix (spec C-3, F-4)
- Sticky in-page section nav under the hero (scrollspy).
- Normalize `dir`/`status` to enums; never echo a raw `dir_*` key.
- GATE: nav scrolls + highlights; no raw keys anywhere; screenshots.

### PR 5 — Price estimate + comps + map data (spec F-1, F-2, G-map)
- Estimate RANGE + date + non-binding label (from `project_3d_avg_price_per_sqm` × sqm ±12%).
- Comps section from a cached `/wp-json/nadlan/v1/comps` (gov/Madlan, daily WP-Cron refresh).
- Fill the area record (pins/stats/spokes) so block 7 map + "full world" render (copy the handoff
  `data.js` AREAS.sde-dov + SPOKES into PHP). Mapbox if `nadlan_mapbox_token` set, else stylized.
- GATE: range + comps + map all render or collapse cleanly; data dated + sourced; screenshots.

## BOUNDARIES — DO NOT (hard stops)
- DO NOT rebuild the site from scratch. The architecture is sound; fix surgically.
- DO NOT touch the homepage hub, calculators, directory, billing, or lead pipeline beyond the one
  link-band in PR 3.
- DO NOT invent prices, photos, or stats. Use real data or collapse the block.
- DO NOT add a 3rd showroom layer. If a showroom exists, replace it, don't append.
- DO NOT ship without browser screenshots and the PART J checklist.
- DO NOT generate logos/renders/photography — that is the owner's design + real assets (Avisror BIM,
  real photos). Flag those as needed; don't fake them.
- DO NOT claim done until `git show --stat HEAD` proves the files are on `main` and the healthcheck
  reports your version.

## DEFINITION OF DONE (every PR)
On `main` · version surfaces aligned · ZIP+manifest verified · spec PART J checklist all ticked ·
desktop 1440 + mobile 390 screenshots in HE and EN attached · `git show --stat HEAD` file list in the
PR description · healthcheck reports the shipped version · one concern only · reversible.

## IF YOU ARE BLOCKED
State precisely what is blocking (missing asset, ambiguous data, a 404 you can't reproduce), what you
tried, and the single decision you need from the owner. Do not guess and ship. Do not silently widen
scope.
