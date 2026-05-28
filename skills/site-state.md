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
