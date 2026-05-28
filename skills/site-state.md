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
