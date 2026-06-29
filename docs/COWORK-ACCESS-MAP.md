# COWORK ACCESS MAP — read this first, every session

> For **Claude Cowork** (and any fresh agent: Codex, Gemini, ChatGPT-in-browser).
> This is the "where is everything and how do I touch it" map. Written plainly.
> If anything here disagrees with your local folder or your memory, **this file
> (after a fresh `git fetch origin main`) wins.** Last verified: 2026-06-29,
> live + repo both at plugin **v1.69.56**.

---

## 0. The one rule that prevents 90% of the disasters

**The GitHub repo, branch `main`, is the source of truth. Always pull it fresh first.**

```
git clone https://github.com/The-new-ben/nad-lan-co-il.git
cd nad-lan-co-il
git fetch origin main
git checkout main
git pull origin main
```

Why this matters: a previous agent worked from an **old downloaded snapshot
(v1.56.1)** and tried to "rebuild" against files that were 13 versions behind
live (v1.69.56). Everything it built was fiction, because it never pulled the
current repo. **Do not trust a `.zip` someone handed you, a `Downloads` folder,
or your training memory. Pull `main` and read the real files.**

How to know you are current: open `plugins/nadlan-config/nadlan-config.php`,
line ~6, and read `Version:`. Compare it to the LIVE site:
`https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck` → the `version` field.
They should match. If your local file is lower, you are on a stale copy — pull again.

---

## 1. What this project is (one paragraph)

`nad-lan.co.il` is a live, revenue-generating Hebrew real-estate website on
WordPress (host: UPress). It has two moving parts you can edit:
- **The theme** = the look/layout. In this repo it is the **repository ROOT**
  (the block theme `nadlan-revenue`).
- **The plugin** = the business brain. It is `plugins/nadlan-config/` (60+ PHP
  modules: projects, professionals directory, calculators, leads, billing,
  monetization, SEO, and the 3D showroom engine).

Keep business logic in the **plugin**. Keep look/layout in the **theme**. Never
move business logic into the theme.

---

## 2. WHERE EVERYTHING LIVES (exact paths in this repo)

### The theme (look & layout) — TWO parts, mind which one is active
The **active live theme is the child `themes/nadlan-platform-child/`** (Template:
`nadlan-revenue`). The **parent `nadlan-revenue` is the repo ROOT**. Because the child is
active, its files WIN: edit header/footer/home/project **templates and `theme.json` in the
child** (`themes/nadlan-platform-child/`), or the child overrides your change and it never
shows. Only edit the parent root for things the child does not override.
```
# PARENT (repo root) = nadlan-revenue
style.css            parent stylesheet header + base CSS
theme.json           parent block theme tokens
functions.php        parent PHP
parts/  patterns/  templates/  styles/    parent block parts/patterns/templates/variations

# CHILD (active live theme) = themes/nadlan-platform-child/
style.css            child header (Template: nadlan-revenue), v0.1.6
functions.php        presentation only (enqueues platform.css, body_class)
theme.json           child color/type/spacing overrides (these win site-wide)
assets/css/platform.css   the active site chrome (header/footer/home/article CSS)
```
NOTE: the showroom on project pages is rendered by the **plugin engine** (`#nl-root`),
independent of the theme. Do showroom work in `nadlan-config`, not the theme.

### The plugin (the business brain) = `plugins/nadlan-config/`
```
nadlan-config.php                  MAIN plugin file. Header "Version:" lives here (line ~6).
                                   Line ~25 is the module loader array — every inc/ file it loads.
inc/                               ALL the modules. Key ones:
  showroom-engine.php              <-- the 3D showroom: shortcode [nadlan_showroom_engine],
                                       the_content injection on nadlan_project, hreflang.
  project-3d.php                   the older project-3d showroom (legacy renderer).
  project-page-assembly.php        per-project SEO seeds (Rainbow etc.).
  directory.php                    professionals/projects premium directory renderer.
  archive-grid.php                 branded card grid for CPT archives.
  calculators.php, leads*, billing, auction, schema, sitemap... (the rest of the money machine)
  health.php                       healthcheck version mirror.
assets/showroom-engine/            THE DESIGN SYSTEM for the showroom (edit these for look):
  engine.js                        renders the whole showroom from data (vanilla JS).
  showroom.css                     the cream page + dark 3D theater styles.
  editorial.css                    the SEO article styling (.nadlan-project-article).
  tokens.css                       color/type tokens (cream/ink/gold/terracotta).
  i18n.js                          every UI string in he/en/fr/ru/ar.
  mapbox-init.js                   real Mapbox mount (only if a token is set).
  data.js                          fallback demo payload (used ONLY when no CMS project).
  models/                          .glb 3D models + posters + facade images.
lib/plugin-update-checker/         the library that powers "Update" in WP-admin.
```

### Deploy artifacts = `plugin-dist/`
```
nadlan-config.json                 the UPDATE MANIFEST. Holds the version + download_url +
                                   changelog. WP-admin reads this to show "Update available".
nadlan-config-1.69.56.zip          the actual installable plugin ZIP (one per version).
```

### Docs, handoff, tooling
```
AGENTS.md            the rules every agent follows. READ FIRST.
START-HERE.md        orientation (note: keep its version line current).
BACKLOG.md           priority queue + shipped log.
skills/              68+ skill files (copywriting, design, deploy process, SEO).
docs/                specs, research, QA evidence, this file.
handoff/             external deliverables + the design mockups + the verdicts
                     (handoff/external-agent-packages/2026-06-28/REVIEW-AND-SOLUTION.md).
scripts/build-plugin-zip.py        builds the versioned ZIP.
scripts/verify-plugin-release.py   checks all version surfaces + ZIP integrity.
```

---

## 3. THE LIVE SITE — how to look at it (read-only)

Base URL: `https://nad-lan.co.il`

You can READ the live site from a terminal with `curl` (this works through the
proxy). You do this to learn the *real* current state — not to change anything.

```
# 1) Plugin version + system health (your "is my code live yet?" check)
curl -s https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck | python3 -m json.tool

# 2) Read a project's real content (all 5 Ashira language posts exist as separate posts)
curl -s "https://nad-lan.co.il/wp-json/wp/v2/nadlan_project?slug=ashira-sde-dov&_fields=id,slug,title,content"

# 3) Fetch a rendered page's HTML (to count renderers / check stacking)
curl -s https://nad-lan.co.il/projects/ashira-sde-dov/ -o /tmp/ashira.html
```

Key pages to know:
```
/                                  homepage (the נדל"ן hub: calculators, guides, directory)
/projects/                         project catalog
/projects/ashira-sde-dov/          Ashira (Hebrew)   + -en / -fr / -ru / -ar siblings
/projects/rainbow-tel-aviv/        Rainbow
/wp-admin/                         WordPress admin (owner login only)
/wp-admin/options-general.php?page=nadlan-features   feature flags switchboard
```

REST endpoints that exist:
```
GET  /wp-json/nadlan/v1/healthcheck     version + module status (public)
POST /wp-json/nadlan/v1/lead            the ONE lead endpoint (do not create a second one)
GET  /wp-json/wp/v2/nadlan_project       read project posts + content + meta
```

---

## 4. HOW CODE ACTUALLY REACHES LIVE (the deploy model)

There are TWO different paths. Mixing them up is a classic mistake.

### A. The THEME (repo root) deploys by git pull
The host (UPress) pulls `main`. So a theme change is live once it is merged to
`origin/main` and the host pulls. (The owner / host triggers the pull.)

### B. The PLUGIN deploys by a versioned ZIP + manifest (owner clicks Update)
Editing a `.php` file and merging is **NOT enough** for the plugin. To ship a
plugin change you must, in ONE release:
1. Edit the code under `plugins/nadlan-config/`.
2. **Bump every version surface to the same new number** (e.g. 1.69.56 → 1.69.57):
   - `plugins/nadlan-config/nadlan-config.php` header `Version:`
   - the `'version' =>` line in that same file's healthcheck array
   - `plugins/nadlan-config/inc/health.php` `'version'`
   - the `?ver` cache-busters in `inc/showroom-engine.php` (the enqueue lines)
   - `plugin-dist/nadlan-config.json` → `version` AND `download_url` (the zip name)
3. Build the ZIP:   `python3 scripts/build-plugin-zip.py 1.69.57`
4. Verify it:       `python3 scripts/verify-plugin-release.py 1.69.57`  (must print `"ok": true`)
5. Commit on a branch, open a PR to `main`, merge.
6. The owner opens **WP-admin → Plugins → "Update available" → Update**. THAT is
   the moment it goes live. Then re-check the healthcheck reports the new version.
   If it still shows the old number, it is PHP opcache: WP-admin → Plugins →
   Deactivate "NadLan Config" → Activate again.

**Rule: a plugin code change that is not on `origin/main` AND inside a bumped
`nadlan-config-<ver>.zip` AND advertised by `nadlan-config.json` does nothing to
the live site.**

---

## 5. WHAT ACCESS YOU HAVE (and don't)

YOU CAN:
- Read + write the **GitHub repo** (`The-new-ben/nad-lan-co-il`) — via the GitHub
  tools/MCP or plain `git`. Develop on a branch, open a PR, merge to `main`.
- **Read the live site** read-only via `curl` to the URLs in section 3.
- Run `php -l`, `node --check`, the build/verify Python scripts locally.

YOU CANNOT (from the code environment):
- Directly edit the live WordPress database, run `wp-cli` on the server, or SSH in.
- Load the live site in a headless browser here (the proxy blocks it — you get
  `ERR_CONNECTION_CLOSED`). **Live screenshots must be taken by the QA agent on
  the owner's real Chrome.** Do not fake screenshots.
- See secrets. Keys/tokens live in WP options (e.g. `nadlan_mapbox_token`,
  `nadlan_whatsapp_e164`) — set by the owner in WP-admin, never committed.

So your loop is: **edit in the repo → ship via the deploy model → ask the QA
agent (or owner) to verify live with screenshots.**

---

## 6. THE THREE LAYERS THAT ARE NOW ALL IN THE REPO (updated 2026-06-29)

Earlier these were live-only experiments. They are now committed and tracked on
`origin/main`, so the repo IS the source of truth for them. Verify with
`git ls-tree -r --name-only origin/main | grep platform`.
- `plugins/nadlan-config/` — the business brain + the showroom engine. Source of truth.
- `plugins/nadlan-platform-orchestrator/` (v0.1.3) — a companion plugin. Anti-stack
  safe: namespaced `nadlan_platform_*` shortcodes; `[nadlan_platform_showroom]`
  DELEGATES to `nadlan_showroom_engine_shortcode()`; its `the_content` filter is
  `is_front_page()` only and OFF by default (`nlpo_auto_insert_home_band`). It does
  NOT register `nadlan_showroom_engine` and emits NO hreflang.
- `themes/nadlan-platform-child/` (v0.1.6) — the active live theme, a real child of
  `nadlan-revenue` (presentation only; `functions.php` only adds body_class + marks
  the existing homepage showcase, it does not rewrite content).

So the live theme is `nadlan-platform-child` (child of `nadlan-revenue`), not the
bare parent. The showroom on project pages is still rendered by the plugin engine
(`#nl-root`), independent of which theme is active — so engine work happens in
`nadlan-config` regardless. Do not add a second showroom in the theme or orchestrator.

---

## 7. THE NON-NEGOTIABLE RULES (anti-stack + honesty)

1. **One renderer per surface.** A project page must have exactly ONE showroom
   root (`#nl-root` = 1, `.nlv2-showroom` = 0). Before adding a renderer, remove
   or disable the old one and PROVE it with selector counts.
2. **Never register a second `nadlan_showroom_engine` shortcode.** It already
   exists in `inc/showroom-engine.php`. A duplicate = stacking.
3. **One lead endpoint** (`/wp-json/nadlan/v1/lead`). Never a second.
4. **One hreflang set.** `showroom-engine.php` already emits it on project pages.
5. **Never blank/destroy `post_content`** without a meta backup. (A blunt strip
   once ate the article; the current filter keeps the article — keep it that way.)
6. **No fake data:** no invented single prices (show a range + "אומדן לא מחייב" +
   date), no fake AI photoreal images, no `/#english` hash links (each language
   is a real crawlable post).
7. **No internal words on public surfaces** (GLB, BIM, mesh, hotspot, token,
   Codex, Lovable, Featured, Sponsored). **No em dash** in public copy.
8. **Honesty:** never claim "done" without evidence. If you cannot verify live,
   say so and hand it to the QA agent. Repo is public — never commit secrets.

---

## 8. CURRENT STATE (2026-06-29)

- Live + repo `main`: plugin **v1.69.56**.
- The showroom engine is live on the **Ashira** project pages (all 5 languages),
  de-stacked (the old static showroom is removed at render, the SEO article is
  kept and styled). Language switch navigates to real sibling posts; hreflang is
  emitted. Map is the stylized fallback until a Mapbox token is set.
- The visual TARGET is `handoff/claude-design/2026-06-28-mockup/Ashira Target
  Mockup.dc.html` (the NADLAN-branded page with section nav + price/comps + clean
  map). The live page is not yet matching it on two pieces:
  **section nav** and **price-range + comps + real map** — those are the next
  work, inside `nadlan-config`'s engine, against real data.
- Blocking inputs only the owner can provide: Mapbox token, WhatsApp number,
  real Avisror BIM (true model), real photos.

---

## 9. YOUR FIRST 10 MINUTES (checklist)

1. `git clone` / `git fetch origin main` → `git pull`. Confirm you are current.
2. Open `plugins/nadlan-config/nadlan-config.php` line ~6, read `Version:`.
3. `curl .../healthcheck` → confirm it matches. Now you know live = repo.
4. Read `AGENTS.md`, then this file, then the task's spec.
5. For showroom work, read `inc/showroom-engine.php` + `assets/showroom-engine/*`.
6. Make changes on a **branch**, never commit to `main` directly.
7. For a plugin change: bump all version surfaces, build + verify the ZIP.
8. Open a PR. After merge, tell the owner to click Update, and ask the QA agent
   for live screenshots (desktop 1440 + mobile 390, HE + EN).
9. End every change with an **anti-stack statement**: the selector counts proving
   one renderer, and what old layer you removed.
10. If blocked, say exactly what is blocking and the single decision you need.
```
```
