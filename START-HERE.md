# NAD-LAN — START HERE (orientation for any agent: Cowork / Claude / Codex)

One folder, everything you need to work on nad-lan.co.il. Assembled from the public repo
The-new-ben/nad-lan-co-il (branch main). Re-run assemble-nad-lan-kit.ps1 anytime to refresh.

## What this project is
nad-lan.co.il = Hebrew real-estate authority portal + marketplace. WordPress (UPress hosting),
block theme `nadlan-revenue` (this repo root) + plugin `nadlan-config` (plugins/nadlan-config/,
60+ modules). Revenue: paid listing tiers (free/pro/premier), paid placement, placement auction,
leads routed to paying owners, recurring billing via Morning (Green Invoice), AI concierge (OpenAI).

## Live state right now
- Plugin deployed: v1.56.1 (check: https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=NOW )
- Six revenue features are deployed DARK behind flags. Master switchboard:
  https://nad-lan.co.il/wp-admin/options-general.php?page=nadlan-features
- Settings pages: nadlan-ai | nadlan-lead-e2e | nadlan-lead-ai | nadlan-lead-nurture |
  nadlan-gi-recurring | nadlan-placement-auction | nadlan-cta  (all under options-general.php?page=)
- Theme deploys via UPress git pull of main. Plugin deploys via the self-update manifest
  plugin-dist/nadlan-config.json -> owner/Cowork clicks Update in wp-admin/plugins.php.

## Read in this order
1. README.md + AGENTS.md + HANDOFF.md (project + agent rules)
2. docs/2026-06-11-owner-assessment-and-roadmap.md (current truth + P1-P5 priorities)
3. docs/agent-comms/claude-codex-channel.md (the durable agent coordination log; Claude-owned)
   + docs/agent-comms/codex-status.md (Codex-owned)
4. skills/copywriting-skill.md + skills/design-rtl-hebrew.md (non-negotiable style rules)
5. The spec for whatever you're building (see map below)

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
