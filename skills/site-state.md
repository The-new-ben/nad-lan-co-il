# site-state.md — Living snapshot of nad-lan.co.il

> **Notice to all agents:** this file is append-mostly. Each session adds a dated block at the bottom. Read the **last 5 blocks** before starting work — they are your situation report. Do not rewrite history.

## Latest known state (as of 2026-05-28)

### Domain & hosting
- Domain: `nad-lan.co.il`. Live. SSL: assumed valid (not verified this session).
- Host: **UPress** (Israeli managed WordPress host). Deploys from this GitHub repo (the-new-ben/nad-lan-co-il).
- The repo → live-site sync mechanism is UPress GitHub integration (owner-managed). **Do not push secrets — they sync.**

### WordPress
- Active theme: **`nadlan-revenue`** (this repo's custom theme). Status: confirmed by owner; footer reportedly still shows fallback to a Twenty-Twenty-X theme footer — likely template fallback bug, needs investigation.
- WP-Admin access: owner-only this session. No agent has direct WP REST access in this Claude session.

### Plugins
- **Yoast SEO**: installed, **unconfigured**. Defaults active. No GSC/Bing verification. See `yoast-config.md`.
- Other plugins: unknown to this session. Codex or next agent must inventory and append.

### Content
- Codex previously generated content as WordPress **Pages** (not Posts, not CPTs). Quantity and quality not audited yet.
- No spoke articles as Posts yet.
- No CPTs registered other than the theme's own `nadlan_lead` (defined in `functions.php:25-38`).

### Branding
- Logo: owner uploaded a newly generated logo to Yoast (organization logo). Dimensions and source: not verified.
- No favicon confirmation.
- Footer: reportedly still showing default WP footer credit. Theme's `footer.php` exists; needs check that it's actually rendering.

### SEO / discoverability
- Google Search Console: **not opened** for this domain (owner-confirmed 2026-05-28).
- Bing Webmaster Tools: **not opened**.
- Likely indexed pages: unknown; no GSC report.
- Sitemap: Yoast default sitemap exists at `/sitemap_index.xml` but not submitted anywhere.

### Analytics
- Google Analytics 4: not confirmed installed.
- No alternative analytics (Plausible/Matomo) confirmed.

### Partnerships / monetization
- Zero partnerships signed.
- The owner is a practicing Israeli lawyer — primary monetization is the owner's own law practice. See `monetization-lawyer-angle.md`.
- No mortgage broker, no appraiser, no developer relationship active.

### Image assets
- Repo: `assets/images/` directory does not yet exist.
- Owner's PC: `C:\Users\pro\.codex\generated_images` — contains mixed-project images, not inventoried. See `image-pipeline.md` for the inventory protocol.

### Skills tree (this file's family)
- Created 2026-05-28 in this session: `AGENTS.md`, `skills/README.md`, `skills/strategy-master.md`, `skills/honesty-statement.md`, `skills/security-public-repo.md`, `skills/agent-coordination-protocol.md`, `skills/wordpress-content-types.md`, `skills/yoast-config.md`, `skills/image-pipeline.md`, `skills/monetization-lawyer-angle.md`, `skills/copywriting-skill.md`, `skills/visual-design-skill.md`, `skills/original-prompt-2026-05-28.md`, `skills/site-state.md` (this file), `docs/research/serp-snapshots-2026-05.md`.

---

## Session log (append below)

### 2026-05-28 — Claude Code (claude-opus-4-7) — research brief task
- Read: pre-existing `docs/OPERATING_PLAN.md`, `README.md`, theme files in repo root.
- Did: created the `skills/` tree from scratch. Authored 14 skill/research files. No theme changes, no plugin changes, no WordPress changes, no deploy. Commit and push at end of session.
- Why: owner requested a research-only deep brief + persistent skills for multi-agent coordination (Claude, Codex, Antigravity).
- Touched: `AGENTS.md` (new), `skills/*` (new directory), `docs/research/serp-snapshots-2026-05.md` (new). No edits to `functions.php`, `front-page.php`, `style.css`, `header.php`, `footer.php`, `index.php`.
- Skills updated: all of the above are new this session.
- Web research performed in-session: 4 live Google searches via WebSearch — for "נדלן להשקעה", "מחשבון משכנתא", "דירות למכירה בתל אביב yad2 madlan", and "מס רכישה 2026 מדרגות". Results captured in `docs/research/serp-snapshots-2026-05.md`.
- Next agent should: read `AGENTS.md`, then `skills/README.md`, then `skills/strategy-master.md`, then `skills/monetization-lawyer-angle.md`. Then attack the open TODOs at the bottom of each skill file. Highest-priority next actions: (1) owner opens Google Search Console + Bing Webmaster Tools, (2) Codex inventories `C:\Users\pro\.codex\generated_images`, (3) Codex audits existing Pages on the live site and produces `docs/research/content-audit-YYYY-MM-DD.md`.

### (next agent block goes here)

---
_File maintained by all agents. Created 2026-05-28 by Claude Code (claude-opus-4-7)._

### 2026-05-28 (afternoon) — Claude Code (claude-opus-4-7) — theme fork + Abilities API
- Read: prior session block; `AGENTS.md`; the owner's uploaded `twentytwentyfive.archive.zip`; `strategy-master.md`; `visual-design-skill.md`; `wordpress-content-types.md`.
- Did:
  - Forked Twenty Twenty-Five (v1.5, from the owner's UPress server) into this repo root.
  - Bulk-renamed every identifier: `twentytwentyfive_` → `nadlan_revenue_`, text domain `'twentytwentyfive'` → `'nadlan-revenue'`, package + slug references throughout 14 PHP files.
  - Replaced `style.css` header with NadLan Revenue metadata (still GPL-2.0+).
  - Replaced `theme.json` color palette (10 brand colors: gold #D89B3C, trust blue #0E3A8A, cream #FAF8F4, positive green, negative red, etc.). Added Heebo as first fontFamily with Hebrew-friendly fallback stack. Switched body typography to Heebo, 400 weight, line-height 1.65.
  - Appended to `functions.php`: `nadlan_lead` CPT, lead-form admin-post handler (with sanitization + nonce + meta storage + admin email), and four WP 7.0 Abilities API registrations: `nadlan/get-pillars`, `nadlan/get-calculators`, `nadlan/get-cities`, `nadlan/get-lead-stats`.
  - PHP lint clean. theme.json valid JSON.
  - Removed old classic-theme placeholder files (header.php, footer.php, front-page.php, index.php) — the block theme replaces them via `parts/header.html`, `parts/footer.html`, `templates/*.html`.
- Why: owner instructed full theme fork (not child theme) for simple mental model. Next agent doesn't have to reason about parent inheritance. WP 7.0 Abilities API lets any AI agent introspect what nad-lan can do without reading source.
- Touched: repo root (added ~150 T25 files + customizations); `skills/theme-fork-decision.md` (new); `skills/abilities-api.md` (new); `skills/plugin-discipline.md` (new); `skills/site-state.md` (this entry).
- Discovery results captured this session (call out): site is on **WordPress 7.0**; active theme was `twentytwentyfive` (now ready to be replaced by `nadlan-revenue` after sync); 42 pages published by Codex covering pillars + calculators + 11 city/neighborhood pages; 0 posts (just hello-world); 1 media item; Google Site Kit shows `search-console` + `site-verification` + `pagespeed-insights` **connected** (contradicts earlier session's note that GSC wasn't opened); plugins are minimal (Yoast + Site Kit active; Akismet + Hello Dolly + AI Provider for OpenAI inactive).
- Skills updated: theme-fork-decision (new), abilities-api (new), plugin-discipline (new), site-state (this entry).
- Next agent / OWNER should:
  1. In UPress → Git management: set path to `/wp-content/themes/nadlan-revenue/`, clone URL `https://github.com/The-new-ben/nad-lan-co-il.git`, branch `claude/charming-meitner-mwVEW` (PR #1). Click שכפול פרויקט.
  2. In WP Admin → Appearance → Themes → activate "NadLan Revenue".
  3. Visually verify homepage and a few pillar pages. Block content is theme-agnostic — expect the palette+typography to shift to ours; structure should be intact.
  4. If anything breaks, switch back to Twenty Twenty-Five (still installed) in WP Admin. Zero data loss.
  5. After visual confirmation: merge PR #1 to `main`, then change UPress Git branch to `main`.

### 2026-05-28 (evening) — Claude Code (claude-opus-4-7) — post-activation verification
- Read: prior block. Owner reported manual file-manager upload (UPress Git only supports `main` branch, which doesn't yet contain the fork — PR #1 unmerged).
- Did: REST verification via WP REST API.
- Findings:
  - **Active theme: `NadLan Revenue` v0.1.0** — partial state. The version `0.1.0` indicates an OLD style.css landed on the server, not the v1.0.0 from the fork commit.
  - Pages: 42, unchanged. **No content loss.** Sample pages (home, mortgage-calculator, real-estate-lawyer, buying-apartment, tel-aviv-apartment-prices) all retain full Hebrew content (17K-25K chars each).
  - Block templates / parts: rendering correctly — homepage screenshot confirmed by owner.
  - **functions.php NOT loaded**: `/wp/v2/types/nadlan_lead` returns 404; `/wp-abilities/v1/abilities` shows only the 4 core+Yoast abilities, none of our `nadlan/*` ones.
  - Diagnosis: the file-manager upload landed the T25 base (templates, parts, theme.json, assets — enough for block rendering) but kept the OLD repo-root `style.css` and `functions.php` (pre-fork placeholders). Probably because the owner sourced from `main` branch which lacks the fork commits.
  - Plugins / media unchanged.
  - Color note: live homepage shows green-dominant branding because Codex's blocks use the `accent-3` slug, which our theme.json maps to `#0E7C57` (positive green). Not a bug — a brand-fit decision to revisit. Original strategy in `visual-design-skill.md` had trust-blue dominant.
- Recommended owner action documented in chat:
  1. Merge PR #1 to `main` on GitHub (one click on the green "Merge pull request" button at https://github.com/The-new-ben/nad-lan-co-il/pull/1).
  2. UPress → ניהול GIT, branch `main`, re-clone to `/wp-content/themes/nadlan-revenue/` — overwrites partial files with the complete fork.
  3. Verify by visiting `/wp-json/wp-abilities/v1/abilities` — should list 8 abilities including the 4 `nadlan/*` ones.
- Lessons captured for the protocol:
  - UPress Git only supports the `main` branch. Document this in `agent-coordination-protocol.md` as a hard constraint.
  - When the owner does a manual file-manager upload, partial states are likely. Always run REST verification after any sync.
  - Going forward: I push to PR branch → owner clicks "Merge pull request" → UPress Git syncs from main. Owner does not need to know any Git commands; only the merge button click.
- Open / blocked: until functions.php is loaded, the lead form, the CPT, and the Abilities API extensions don't exist. This blocks any next-agent work that depends on `nadlan_lead` or `nadlan/*` abilities.

### 2026-05-28 (night) — Claude Code (claude-opus-4-7) — mu-plugin fallback + handoff
- Final state of this session:
  - PR #1 (theme fork) was **merged to main**. Confirmed via git log.
  - UPress Git synced from main, cache cleared by owner.
  - **`style.css` and `theme.json` on the server ARE the new fork** (verified via direct fetch: header v1.0.0, palette contains `#D89B3C`/`#0E3A8A`/`#0E7C57`/`#FAF8F4`, theme.json contains "Heebo").
  - **`functions.php` on the server is NOT loading our appended additions.** Verified by REST: `nadlan_lead` CPT returns 404 from `/wp/v2/types/nadlan_lead`; abilities list still shows only the 4 core+Yoast entries, none of `nadlan/*`. Possible causes: UPress Git silently skipped functions.php, file permissions blocked the overwrite, or PHP opcache persisted older bytecode.
  - **Mitigation committed to PR branch as `mu-plugins/nadlan-config.php`** (single 6.5 KB file, PHP-lint clean, GPL-2.0+). It contains: the `nadlan_lead` CPT, the lead-form handler, and the four `nadlan/*` Abilities API registrations. mu-plugins auto-load regardless of theme state, so this bypasses the functions.php issue entirely.
  - **Owner was instructed to manually drop that one file into `/wp-content/mu-plugins/` via the UPress file manager.** As of session end, REST verification did NOT detect it loaded. Either the upload didn't complete, or UPress's mu-plugins path is non-standard.

### Handoff to next agent (Claude resumed, Codex June 2+, or any other)

1. **First action:** run REST verify (`python3 /tmp/v2.py` from previous session, or equivalent: hit `/wp/v2/themes?status=active`, `/wp/v2/types/nadlan_lead`, `/wp-abilities/v1/abilities`, `/wp/v2/pages?per_page=1` for X-WP-Total).
2. **If `nadlan_lead` CPT is now registered and abilities list has 8 entries**, including `nadlan/*`: the mu-plugin upload succeeded between sessions. Proceed to Phase 1 of the monetization plan (`monetization-lawyer-angle.md`).
3. **If still NOT registered**, the mu-plugin was never received OR the path is wrong. Ask the owner:
   - Did the file `/wp-content/mu-plugins/nadlan-config.php` get uploaded to the server? Verify in UPress file manager.
   - If yes: try a Site Health check in WP admin to see if mu-plugins are being scanned. The standard WP path is `wp-content/mu-plugins/<file>.php` at the root of that folder (not in a subfolder; mu-plugins are NOT recursive).
   - If UPress uses a custom mu-plugins path (some hosts override `WPMU_PLUGIN_DIR`), that path is needed.
4. **Alternative fallback if mu-plugins is blocked**: convert the file into a regular plugin (add `Plugin Name:` header and ZIP it for one-click upload via Plugins → Add New → Upload Plugin in WP admin). The file already has the right header — just zip the folder and provide to owner.

### What is BLOCKED until functions.php OR mu-plugin work

- Lead-form submissions (no `admin_post_nadlan_lead` handler → form would error)
- The Abilities API extension (next agents can't discover what nad-lan can do)
- Visible `NadLan Leads` admin menu (no CPT)

### What is UNBLOCKED and ready for next-agent work (no PHP dependency)

- Yoast configuration via REST API (titles, social, breadcrumbs, Person schema for the lawyer-owner). See `skills/yoast-config.md`.
- Content pipeline: Codex (returning June 2) writes spoke articles per `skills/strategy-master.md` keyword clusters.
- Image pipeline: `image-pipeline.md` protocol exists; Codex inventories `C:\Users\pro\.codex\generated_images` next session.
- Google Search Console: already connected via Site Kit. Next step is to verify sitemap submission and look at first index data.
- Site state, plugin discipline, theme-fork rationale, copywriting rules, visual design, abilities-API spec — all in `skills/`. Read before acting.

### Files committed this session

Commits on `claude/charming-meitner-mwVEW` (= PR #1, merged to main):
- `5621b78` Bootstrap skills/ tree (initial skills, strategy, monetization, agent protocol, SERP research)
- `ac7b351` Fork Twenty Twenty-Five into nadlan-revenue: brand palette, Heebo, Abilities API
- `af840ed` site-state + protocol: post-activation verification; UPress Git branch=main constraint
- `30ac21b` Add nadlan-config mu-plugin: CPT + Abilities API independent of theme
- (this commit) site-state.md handoff

### Owner tone at session end
Owner reported being tired and concerned about token usage ($43.07 / $50 monthly Claude budget, 86%). Next session: be minimal in chat, batch operations, do not re-explain rationale that's already in skills/. Read site-state.md last 3 blocks first.

### 2026-05-28 (late night) — Claude Code (claude-opus-4-7) — nadlan-config plugin LIVE
- **Outcome: lead-capture foundation is alive.** After three failed attempts (mu-plugin v1.0.0 didn't load, plugin v1.0.1 with Hebrew + lead handler + abilities had fatal on activation), the stripped v1.0.2 (CPT + healthcheck only) loaded successfully.
- **Verified via** `GET /wp-json/nadlan/v1/healthcheck`:
  - `plugin`: nadlan-config
  - `version`: 1.0.2
  - `cpt_present`: **true**
  - `php_version`: **8.5.5** (much newer than the conservative 7.2 floor; all modern PHP is safe)
  - `wp_version`: **7.0** (Abilities API namespace confirmed)
- **Live URL for any agent to test:** `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck`
- New skill: `skills/nadlan-config-plugin.md` — documents the plugin's purpose, install/update flow, roadmap, the five "never do this" rules, and how to verify loaded.
- Theme `functions.php` issue is now MOOT — the lead-capture lives in the plugin, theme can be anything.
- Next agent should: ship v1.0.3 (add lead-form handler back), then v1.0.4 (abilities — after verifying `wp_register_ability` signature in WP 7.0 source).

### 2026-05-28 (very late night) — Claude Code (claude-opus-4-7) — v1.0.4 live, REST work session
- **Plugin v1.0.4 activated successfully.** Healthcheck confirms `cpt_present: true`, `lead_handler_loaded: true`, PHP 8.5.5, WP 7.0. This is the stable baseline; owner instructed no more uploads unless absolutely needed.
- v1.0.3 had failed activation — the bisect (v1.0.4 = v1.0.3 minus shortcode + plus function_exists guards) succeeded. Cause was either the shortcode itself OR a function-name collision from not deleting v1.0.2 first. Unproven which; future plugin updates must add `function_exists` guards defensively.
- **Critical finding for revenue:** the homepage at id=2 has **zero `<form>` tags**. The pretty lead-capture-looking fields Codex built are styled Gutenberg blocks that don't submit anywhere. Verified by reading raw page content via REST. No `nadlan_nonce`, no `admin-post.php` reference, no `nadlan_lead` action. **The homepage currently captures zero leads.**
- **Path to fix the homepage form:** needs ONE more plugin upload (v1.0.5) adding a `[nadlan_lead_form]` shortcode that renders a complete working `<form>` with embedded nonce + action. Owner was told this and given the choice (A: ship v1.0.5 now, B: defer). At session end the choice was pending.
- **Yoast REST limitation discovered:** the `_yoast_wpseo_metadesc` meta key is NOT exposed for REST writes by Yoast SEO Free. Attempted to write 28 templated Hebrew meta descriptions for all the calculator + pillar + professional + city pages; WP returned 200 but the meta did not persist (silent ignore of non-whitelisted private meta). To bulk-write Yoast descriptions via REST, one of:
  - Add a small `register_meta` filter in nadlan-config plugin (requires v1.0.5)
  - Upgrade to Yoast Premium (paid)
  - Edit each page in WP admin manually
- **Timezone now set to Asia/Jerusalem** (verified via PUT to `/wp/v2/settings` with field `timezone`).
- **Confirmed via REST that all 42 of Codex's pages still have empty Yoast meta descriptions.** Major SEO miss — affects organic CTR. Highest-impact no-plugin-upload work for next session: write a `register_meta` exposing `_yoast_wpseo_metadesc` and `_yoast_wpseo_title` for REST in v1.0.5, then bulk-set descriptions.

### Open issues by priority for next agent

1. **Homepage form**: decide v1.0.5 (shortcode-based form) OR defer. If we want leads, this must happen.
2. **Yoast meta descriptions × 42 pages**: blocked on either v1.0.5 register_meta or Yoast Premium.
3. **Yoast Person schema for the lawyer-owner**: needs owner's full Hebrew name + bar number. Configure via Yoast UI manually (not via REST in free version).
4. **Sitemap submission to GSC**: Site Kit shows GSC connected; sitemap auto-submits via Yoast's default sitemap. Verify in GSC dashboard.
5. **Nav menu**: zero menus registered. Block themes can use the Navigation block in Site Editor; not strictly needed via classic menus.
6. **Cornerstone marking in Yoast**: mark pillar pages (buying, selling, investment, urban-renewal, real-estate-lawyer, real-estate-tax-advisor, mortgage-calculator, purchase-tax-calculator) as cornerstone in Yoast UI.

### What WAS accomplished this session (chronological)
- Skills tree bootstrapped (16 files including strategy, monetization, copywriting, visual design, agent protocol).
- Twenty Twenty-Five forked to nadlan-revenue (palette + Heebo + abilities API in functions.php, though functions.php failed to load).
- Plugin journey: mu-plugin failed → v1.0.1 plugin failed → v1.0.2 minimal succeeded → v1.0.3 failed → v1.0.4 succeeded with lead handler.
- Timezone fixed to Asia/Jerusalem.
- 16 skill files committed for cross-agent persistence.
- All work pushed to PR #1 (merged) + branch `claude/charming-meitner-mwVEW` (active).

### 2026-05-28 (deep night) — Claude Code (claude-opus-4-7) — hub-spoke implementation
- **Pillars → Spokes sweep:** added "מדריכים קשורים" related-articles block to all 11 pillars (buying-apartment, selling-apartment, investment-apartment, mortgage-calculator, real-estate-tax-advisor, real-estate-lawyer, urban-renewal, commercial-real-estate, new-projects, professionals, tel-aviv-apartment-prices). 63 new outgoing internal links.
- **Spokes → Pillar back-links + sibling links:** 30 spoke pages got back-link blocks (cream-bg group with "חלק מהמדריך" + "ראה גם" siblings). 30 pillar back-links + ~60 sibling links.
- **Homepage Tools strip:** 5 calculators linked from home.
- **Total new internal links this session: ~153.**
- **Idempotency markers** in place: `<!-- nadlan-hub-related-v1 -->`, `<!-- nadlan-spoke-backlink-v1 -->`, `<!-- nadlan-tools-strip-v1 -->`. Future agents read these before re-running.
- **Skill created:** `skills/internal-linking-hub-spoke.md` documents cluster maps, primary-pillar map, markers, anchor discipline, and TODOs.
- **Verified:** sitemap reachable at `/sitemap_index.xml` (4 sub-sitemaps).
- **Confirmed blocked (Yoast Free REST):**
  - `_yoast_wpseo_metadesc` (descriptions) — silent ignore on REST writes
  - `_yoast_wpseo_is_cornerstone` (cornerstone flag) — same
  - Both unblocked by v1.0.5 plugin update (owner approval gate)
- **Site Kit search-console data endpoint** returned 404 for `/google-site-kit/v1/modules/search-console/data/searchanalytics` — needs correct path; defer to next session.
- **Timezone:** confirmed Asia/Jerusalem (set earlier this session via PUT to /wp/v2/settings).

### 2026-05-28 (continued, claude-opus-4-8) — technical SEO + curated navigation
- Read: prior blocks, internal-linking-hub-spoke.md, strategy-master.md §3.
- **Technical-SEO audit via live HTML (good news):**
  - Canonicals are `https` on home + pillar pages (Yoast). robots meta = `index, follow, max-image-preview:large`. og:url https. BreadcrumbList schema present (Yoast emits it). Site is fully indexable.
  - `home` = https (correct, public-facing). `siteurl` (`url`) = http — minor inconsistency, causes sitemap to list http URLs (Google 301-follows to https; low harm). **Deliberately NOT changed** — flipping siteurl on a managed host (UPress edge SSL) risks an admin redirect-loop, not worth it for marginal benefit. Owner can fix in UPress → Settings → General → Site Address if desired.
  - robots.txt returned 404 to my fetch — worth a later look but Google finds the sitemap via Site Kit/GSC.
  - Yoast schema on /real-estate-lawyer/ = WebPage + Organization + BreadcrumbList + WebSite + ImageObject. **Missing Article + Person/Attorney** — Pages emit WebPage (Posts emit Article). This is the documented reason the strategy wants spokes as Posts eventually. Lawyer E-E-A-T Person schema still needs owner's full name + bar number + Yoast author config.
- **Curated navigation deployed (high value):** replaced the auto `<!-- wp:page-list /-->` (which dumped all 42 flat pages) on nav id=4 with a curated pillar-first menu:
  - Top level: קניית דירה, מכירת דירה, דירה להשקעה, [submenu] משכנתא ומימון, [submenu] מיסוי ומשפט, [submenu] כלים, התחדשות עירונית, דירה מקבלן, אנשי מקצוע
  - 23 curated links total. Site-wide nav links to every pillar from every page = strong internal linking + clean UX + hierarchy signal.
  - Old nav content backed up in this log: `<!-- wp:page-list /-->`. To revert: PUT that string to /wp/v2/navigation/4.
  - Saved current nav markup to `docs/wp-state/navigation-4.html` for version control.
- Homepage still renders HTTP 200 with new nav labels present.

### 2026-05-28 (continued) — template fixes + breadcrumbs + v1.0.5 ready
- **Bug fixed (repo):** earlier theme-fork sed renamed pattern slugs only in `.php` files; all `.html` templates/parts still referenced `twentytwentyfive/*` patterns that no longer exist under that name. Fixed every `.html` in templates/ + parts/ to `nadlan-revenue/*`. parts/header.html + parts/footer.html were affected (used on every page). Verified all referenced patterns resolve. **Requires owner theme re-sync (UPress Git pull from main) to apply on live.** Live header currently renders OK regardless (synced state internally consistent), so no live breakage — this is a correctness fix for the next sync.
- **Visible breadcrumbs added** to templates/page.html + templates/single.html (yoast-seo/breadcrumbs block above title). Requires (a) owner theme re-sync AND (b) Yoast breadcrumbs enabled in SEO → Search Appearance → Breadcrumbs. Harmless if disabled (renders nothing).
- **Plugin v1.0.5 BUILT and ZIP ready (NOT yet installed — owner decides):** adds `register_post_meta` exposing `_yoast_wpseo_metadesc`, `_yoast_wpseo_title`, `_yoast_wpseo_focuskw`, `_yoast_wpseo_is_cornerstone` for REST writes (edit_posts gated). Unblocks the two biggest remaining on-page levers: bulk meta descriptions (42 empty) + cornerstone marking (11 pillars). PHP lint clean. Source in plugins/nadlan-config/. If owner installs: next agent runs the desc-writing script (template Hebrew descriptions already designed in /tmp/work2.py logic — see strategy/copywriting skills for tone).

### Decision pending for owner
1. **Install plugin v1.0.5?** One delete-old + upload-new cycle. Payoff: I then write all 42 Yoast meta descriptions + mark 11 cornerstones via REST in one batch. Biggest remaining on-page SEO win.
2. **Re-sync theme from main (UPress Git pull)?** Applies: pattern-ref consistency fix + visible breadcrumbs. Then enable Yoast breadcrumbs in Search Appearance.

### 2026-05-28 (continued) — v1.0.5 installed, 41 meta descriptions + 11 cornerstones LIVE
- Owner installed plugin v1.0.5. Healthcheck confirms version 1.0.5.
- **register_post_meta worked** — Yoast meta keys now writable via REST.
- **Wrote 41/42 Yoast meta descriptions** (hand-written Hebrew, 150-160 chars, copywriting-skill tone: fact + benefit + soft CTA, no AI markers, no forbidden internal terms). Verified persisted per-page during write; confirmed rendering live on mortgage-calculator + real-estate-lawyer (`<meta name="description">`).
  - 1 page skipped (no mapping — likely a sample/privacy page; check & fill if it's a real page).
- **Marked 11 pillars as cornerstone** (`_yoast_wpseo_is_cornerstone=1`): buying-apartment, selling-apartment, investment-apartment, mortgage-calculator, real-estate-tax-advisor, real-estate-lawyer, urban-renewal, commercial-real-estate, new-projects, professionals, purchase-tax-calculator.
- Note: REST collection query with `_fields=...,meta` returns 400 (WP quirk); query meta per-page instead. Documented so next agent doesn't trip on it.
- The full description text per slug is in /tmp/desc.py logic this session; if regeneration needed, the DESC dict pattern is reproducible from page titles + copywriting-skill.

### On-page SEO status after this session
- ✅ 41 pages: unique Hebrew meta descriptions (was 0)
- ✅ 11 cornerstone pillars marked
- ✅ 153 internal hub-spoke links
- ✅ curated pillar-first navigation (site-wide)
- ✅ https canonicals, index/follow, BreadcrumbList schema
- ✅ visible breadcrumbs in templates (pending theme re-sync + Yoast breadcrumbs toggle)
- ⏳ Article/Person schema on legal pages (needs owner name+bar # OR Posts migration)
- ⏳ featured/OG images (Codex, from PC image folder)
- ⏳ content depth on thin pages (Codex)

### 2026-05-28 (continued, claude-opus-4-8) — interactive widgets shipped
- **4 widgets deployed live** (all via REST, no plugin uploads, no external services, no paid APIs):
  1. **Mortgage calculator** on /mortgage-calculator/ — 3-track Israeli mix (Kalatz/Prime/Variable) + stress test +2% + visual bar. Vanilla JS, ~7.3 KB. PREPENDED above Codex's article. Marker data-nlc="mortgage-v1".
  2. **Purchase tax calculator** on /purchase-tax-calculator/ — 2026 brackets baked in, visual bracket bar with live position marker, side-by-side first-vs-investor. ~7.4 KB. Marker data-nlc="ptx-v1".
  3. **Dynamic HTML sitemap** at NEW page /sitemap/ (id=336) — self-updating via fetch to /wp-json/wp/v2/pages, organized by 8 clusters, search-filterable, cornerstone & tool tags, premium cards, mobile-responsive. Yoast meta desc set.
  4. **Premium footer** site-wide — 4-col (brand/pillars/tools/legal) + bottom bar, dark contrast bg, gold section headings, RTL. Override of theme's footer template part (source=custom in DB).
- **Web research conducted before building** (3 WebSearch queries — US/UK competitor tools, Zillow/Redfin/Trulia heat maps, Israeli mortgage tools). Documented gap: NYT-style buy-vs-rent + visual bracket sim + reverse affordability are missing from IL SERP. Sources cited in commit.
- **New skill:** skills/interactive-widgets.md documents all 4 widgets, markers, update protocol, US/UK research basis, and TODO roadmap for next session.
- **Repo state mirror:** docs/wp-state/template-part-footer.html and docs/wp-state/page-sitemap.html now hold the live versions for version control.
- **Lawyer Person schema explicitly deferred** per owner — not ready to be publicly signed as lawyer.

### 2026-05-28 (continued) — Lovable design prompt authored
- Owner wants a $1M-quality theme and prefers Lovable for the visual design pass.
- Authored `docs/lovable-prompt.md`: a world-class, exhaustive Lovable prompt + a follow-up "export portable CSS" prompt + a porting checklist for Claude/Codex.
- Workflow established: Lovable designs → outputs framework-agnostic CSS + tokens → Claude/Codex port into the WordPress block theme (theme.json + style.css + template parts + widgets). We do NOT ship Lovable's React; we extract its visual decisions.
- The prompt bakes in: luxury design language (Sotheby's/Christie's/The Agency/Compass caliber), RTL Hebrew, Frank Ruhl Libre headings + Heebo body, warm-minimal ink/cream/gold palette, all page types, the calculator tools, components library, and demands exact tokens/CSS.
- Fonts already bundled locally (assets/fonts/frank-ruhl-libre + heebo); Lovable's @font-face points at those theme paths.
- Status: brand assets (serif logo/favicon/OG) staged in repo + luxury-design-language.md skill committed. The earlier cartoon-house logo (media id 338/340) is still wired live as site_logo/site_icon — REPLACE after the Lovable direction is locked. Full theme.json/CSS rewrite deferred until Lovable output (or owner approval of provisional luxury direction) lands.

### 2026-05-28 (late) — Claude Code (claude-opus-4-8) — Lovable design system received + translated to skills
- Owner ran Lovable round 1 and delivered `nadlanchachamdesignsystem.md` (715 lines): full luxury design system with competitor DNA (Sotheby's, Christie's, The Agency, Compass, Luxury Presence), WCAG-verified color palette, full type scale (desktop + mobile), 7-section homepage, article + calculator + city + professionals page specs, full components library, micro-interactions matrix, monogram logo spec, self-critique with 3 fixes applied, honesty statement.
- **Source archived** at `docs/design/lovable-output-2026-05-28.md` (authoritative).
- **Translated to 6 new skills** + 1 master:
  - `skills/luxury-design-system.md` — master skill, tokens, hard rules, deprecation log
  - `skills/design-page-patterns.md` — homepage, article, calculator, city/neighborhood, professionals
  - `skills/design-components.md` — buttons, inputs, cards, tables, tabs, accordion, breadcrumb, pagination, badges, tooltips, lead form, toasts, header, footer, 404
  - `skills/design-micro-interactions.md` — full motion matrix + animated underline + tab slide + drawer stagger
  - `skills/design-logo-mark.md` — wordmark + monogram seal + lockups + tagline `ידע. כלים. החלטות.` + rejected cartoon-house cleanup
  - `skills/design-rtl-hebrew.md` — consolidated RTL rules with logical-property cheat sheet
  - `skills/design-monetization-surfaces.md` — NEW per owner request: sponsored articles, sponsored listings, sponsored map pins, in-article capsules, partner strip, directory Pro/Premier tiers, reserved ad slots, cookie disclosure, CMS schema readiness
- **Deprecated** `skills/luxury-design-language.md` (provisional) and `skills/visual-design-skill.md` §palette+typography (corporate blue) with in-file notices pointing to the new system.
- **Lovable Prompt #2 authored** at `docs/lovable-prompt-2.md`. Closes 7 gaps: blog index, search results, lead-form variations, neighborhood explicit spec, map widget full UI, listing card full state spec, MONETIZATION SURFACES (per owner addendum), plus three artifact gaps that unblock the WordPress port: GAP 4 CSS bundle, GAP 5 theme.json fragment, GAP 6 Gutenberg block-pattern markup for homepage sections P1–P10.
- **Inconsistencies resolved (Lovable's values now canonical):**
  - Gold: `#9C7A3C` (was provisional `#B08D57`)
  - Cream: `#FAF7F1` + `#F3EEE3` (was `#F7F4ED`)
  - Ink: `#1B1A17` + `#2E2B26` + `#5C564D` (was `#1A1A1C`)
  - Hairlines: `#E2DCD0` + `#C9C0AE` (was `#E5E1D8`)
  - Logo: monogram נ in 1px gold double-circle "seal" (cartoon-house version REJECTED — media ids 338/340 still on live; pending cleanup)
- **Tokens are documented, palette is set; the actual CSS / theme.json port to the live theme is gated on the second Lovable round** producing the CSS bundle + theme.json fragment + block patterns.
- No live-site changes this session beyond the skills tree update.
