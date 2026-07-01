# NAD-LAN — START HERE (orientation for any agent: Cowork / Claude / Codex)

One folder, everything you need to work on nad-lan.co.il. Assembled from the public repo
The-new-ben/nad-lan-co-il (branch main). Re-run assemble-nad-lan-kit.ps1 anytime to refresh.

## What this project is
nad-lan.co.il = Hebrew real-estate authority portal + marketplace. WordPress (UPress hosting),
block theme `nadlan-revenue` (this repo root) + plugin `nadlan-config` (plugins/nadlan-config/,
60+ modules). Revenue: paid listing tiers (free/pro/premier), paid placement, placement auction,
leads routed to paying owners, recurring billing via Morning (Green Invoice), AI concierge (OpenAI).

## Live state right now
- Plugin deployed: **v1.69.56** (verify, don't trust this line — check:
  https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=NOW ). If your local
  `plugins/nadlan-config/nadlan-config.php` shows a LOWER version, you are on a
  stale snapshot — run `git fetch origin main && git pull`. Full map: `docs/COWORK-ACCESS-MAP.md`.
- Six revenue features are deployed DARK behind flags. Master switchboard:
  https://nad-lan.co.il/wp-admin/options-general.php?page=nadlan-features
- Settings pages: nadlan-ai | nadlan-lead-e2e | nadlan-lead-ai | nadlan-lead-nurture |
  nadlan-gi-recurring | nadlan-placement-auction | nadlan-cta  (all under options-general.php?page=)
- Theme deploys via UPress git pull of main. Plugin deploys via the self-update manifest
  plugin-dist/nadlan-config.json -> owner/Cowork clicks Update in wp-admin/plugins.php.

## ⭐ DEPLOY WITHOUT THE OWNER CLICKING "UPDATE" (new 2026-07-01, proven live)

The owner no longer has to click "Update" for plugin releases. An agent with the
`WP_APP_PASSWORD` (admin) can trigger WordPress's own updater directly and push a release
live itself. Full, repeatable method + the exact code: **`skills/agent-direct-wordpress-access.md`**
(section "⭐ Agent-driven plugin deploy"). Four direct-access tools (Code Snippets, Vibe AI/MCP,
File Manager, WP Adminer) are installed live for this. Flow now: write code -> merge to main
-> agent triggers deploy -> verify live (healthcheck version + changed page + homepage 200).
Repo stays source of truth; only the deploy *trigger* moved from owner to agent. Rollback =
same call pointed at the previous ZIP. (Still open: the child theme has no direct path yet —
see docs/research/ on WP Pusher.)

## Read in this order
1. README.md + AGENTS.md + HANDOFF.md (project + agent rules)
2. handoff/antigravity/2026-07-01-mega-master-handoff/MEGA_MASTER_HANDOFF.md (brand vibe,
   buyer journey, sketch-first 3D strategy, monetization, the child-theme/UPress deploy mess
   — read the reconciliation note at the top first, it flags where this doc disagrees with
   decisions already made elsewhere in the repo)
3. docs/2026-06-11-owner-assessment-and-roadmap.md (current truth + P1-P5 priorities)
4. docs/agent-comms/claude-codex-channel.md (the durable agent coordination log; Claude-owned)
   + docs/agent-comms/codex-status.md (Codex-owned)
5. skills/copywriting-skill.md + skills/design-rtl-hebrew.md (non-negotiable style rules)
6. The spec for whatever you're building (see map below)

## Folder map
- skills/        68 skill files: copywriting, design system, RTL/Hebrew, EEAT program, SEO,
                 agent coordination protocol, plugin deploy process, monetization specs.
                 REUSABLE ON OTHER SITES (e.g., the Justice legal portal).
- docs/          Specs + research (all cited): finish-line spec, revenue+autonomous architecture,
                 lead-funnel best practices, offers feature spec, listing+3D spec, phased
                 infrastructure plan, research appendix (58 src), owner guides (AI key, Morning
                 billing, money dashboard, rollback).
- docs/qa/       17 QA gate docs (per-chunk acceptance evidence).
- docs/agent-comms/  The bidirectional agent channel + status files.
- plugins/nadlan-config/  The plugin source (the money machine).
- plugin-dist/   Versioned ZIPs + self-update manifest.

## Hard rules (apply to every agent)
- Public repo: NEVER commit secrets. Keys live in WP options / Google Keep only.
- Ship features DARK behind nadlan_feature_* flags (default off). Claude gates + deploys.
- Hebrew/RTL, copywriting-skill rules (no em-dash, no internal/dev words on public surfaces,
  benefit-led marketing language only).
- One change-set = one branch = draft PR. Never push main directly (Claude merges after the gate).

## Current mission queue
P1 ACTIVATE money machine (Cowork prompt delivered to owner) -> P2 content cannibalization fixes
-> P3 EEAT rollout (reviewer end-of-article + cross-site Person schema with the Justice portal)
-> P4 content diversification (glossary 100+) -> P5 listings level-up + Rainbow 3D picker +
offers feature (specs in docs/, cited).
