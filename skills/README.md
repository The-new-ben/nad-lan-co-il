# skills/ — The shared brain

Every agent (Claude, Codex, Antigravity, Cowork) reads from here before acting and writes back here after acting. This is not documentation _about_ the project; it _is_ the project's operating knowledge.

## Read order for a fresh session

**Mandatory before any work:**

1. `../AGENTS.md` — the contract between agents
2. `../HANDOFF.md` — technical access + current state (public-safe)
3. `agent-onboarding.md` — credentials handshake
4. `README.md` — this file
5. `cowork-briefing.md` (or your equivalent agent briefing) — condensed history + voice + guardrails
6. `site-state.md` — read the **last 6 blocks**, that is the live situation report
7. `strategy-master.md` — the full Hebrew SEO/business brief

**Before publishing content:**

8. `google-blueprint-workflow.md` — how we research a query before writing
9. `article-publishing-protocol.md` — how a ChatGPT article becomes a live page (THE checklist that 2026-05-29 skipped)
10. `copywriting-skill.md` — voice, forbidden phrases, em-dash ban
11. `internal-linking-hub-spoke.md` — the hub/spoke map + anti-cannibalization rules
12. `yoast-config.md` — required meta + Person schema

**Before shipping plugin or theme:**

13. `nadlan-config-plugin.md` — plugin lessons, one-capability rule
14. `codex-plugin-access-and-deploy.md` — **THE step-by-step deploy pipeline** (any agent: how to change the plugin and get it live; pre-solved blockers)
15. `plugin-auto-update.md` — self-hosted update channel
16. `agent-coordination-protocol.md` — UPress sync constraints

**Before creating or cloning a premium project showroom:**

17. `project-page-premium-showroom-runbook.md` — A-to-Z project page workflow: research, assets, CMS payload, QA, deploy
18. `skill-3d-model-pipeline.md` — GLB/poster/facade/unit-map pipeline and buyer-facing model rules
19. `skill-interactive-apartment-picker.md` — clickable apartment cells/polygons on the building
20. `skill-project-page-seo-and-assembly.md` — project SEO, schema fields, visible content blocks, international intent
21. `docs/2026-06-15-rainbow-template-v1-readiness-matrix.md` — current Rainbow clone-readiness state and exact gate

## Index (current as of 2026-05-30)

### Onboarding + contract

| File | Purpose |
|---|---|
| `../AGENTS.md` | Cross-agent contract; mandatory read/write protocol |
| `../HANDOFF.md` | Public-safe onboarding for a new agent; technical access map |
| `agent-onboarding.md` | Secure credential handshake; what lives where |
| `cowork-briefing.md` | Condensed history + voice + guardrails for Claude Cowork |
| `agent-coordination-protocol.md` | Rules for Codex/Antigravity/Claude/Cowork coexistence |
| `agent-tooling-strategy.md` | Which agent does what work |
| `original-prompt-2026-05-28.md` | The Laravel prompt that started the project |
| `honesty-statement.md` | Verified vs assumed vs needs-paid-data |
| `security-public-repo.md` | What MUST NEVER be committed (repo is public) |

### Strategy + monetization

| File | Purpose |
|---|---|
| `strategy-master.md` | Full Hebrew SEO/content/design/business brief; competitor DNA |
| `monetization-lawyer-angle.md` | Revenue model centered on owner's law practice |
| `lead-funnel.md` | Site-wide FAB + lead CPT + REST endpoint |
| `payments-woo-greeninvoice.md` | Self-registration directory: Free/Pro/Premier tiers |

### Content production (the new authoring loop)

| File | Purpose |
|---|---|
| `strategy-master.md` §13 | Google Blueprint workflow — manual SERP reverse-engineering → article spec → ChatGPT prompt |
| `internal-linking-hub-spoke.md` §"Article publishing protocol" | ChatGPT output → live page (10-step checklist) |
| `runbook-cowork-article-batch-v3.md` | **THE current master recipe (use this one)** — Drive-bridged architecture: owner runs ChatGPT in a Project, ChatGPT writes to Drive inbox, Cowork polls and publishes. 23-article queue (5 rewrites + 18 new). |
| `runbook-cowork-article-batch-v2.md` | SUPERSEDED by v3 |
| `runbook-cowork-article-batch.md` | SUPERSEDED by v2 - kept for history |
| `article-guide-design-pattern.md` | The `.nadlan-guide` green canonical design pattern (hero/cards/table/note/CTA). Owner-approved 2026-05-30. |
| `google-blueprint-workflow.md` (stub) | Folded into strategy-master.md §13; pointer only |
| `article-publishing-protocol.md` (stub) | Folded into internal-linking-hub-spoke.md; pointer only |
| `copywriting-skill.md` | Hebrew voice; forbidden AI phrases; em-dash ban (2026-05-29 owner-explicit) |
| `internal-linking-hub-spoke.md` | Pillar→spoke map; anti-cannibalization; idempotency markers |
| `spoke-prompts-short-rent-abroad.md` | System block + 7 country prompts for ChatGPT |
| `short-term-rentals-abroad.md` | Pillar source data + 7-country regulation research |
| `yoast-config.md` | Yoast meta requirements; Person schema for lawyer E-E-A-T |
| `skill-project-page-seo-and-assembly.md` | Project-page SEO replication standard: SERP, transactional title/meta, schema fields, FAQ, investor/international blocks |

### Design system

| File | Purpose |
|---|---|
| `luxury-design-system.md` | Lovable round 1 — tokens, type, components, palette |
| `luxury-design-language.md` | Sister doc — design language overview |
| `design-page-patterns.md` | Page-level Gutenberg patterns |
| `design-components.md` | Component spec |
| `design-micro-interactions.md` | Motion + interaction rules |
| `design-logo-mark.md` | Logo + monogram spec |
| `design-rtl-hebrew.md` | RTL Hebrew + CSS logical properties |
| `design-monetization-surfaces.md` | Sponsored placements + CTA surfaces |
| `design-implementation.md` | Source → theme-file mapping; post-sync verification |
| `visual-design-skill.md` | DEPRECATED — superseded by luxury-design-system.md tree |
| `image-pipeline.md` | How to handle Codex-generated images |

### Plugin + WordPress

| File | Purpose |
|---|---|
| `nadlan-config-plugin.md` | Plugin journey v1.0.0→v1.2.1; one-capability rule; lessons |
| `codex-plugin-access-and-deploy.md` | **Complete deploy operator guide** — locations, links, the 9-step ship loop, obstacle→solution table, multi-agent etiquette. Start here to change the plugin. |
| `plugin-auto-update.md` | PUC self-hosted JSON; ship workflow |
| `plugin-discipline.md` | Mandatory guards (function_exists, no Hebrew in activation, no mu-plugins) |
| `theme-fork-decision.md` | Why we forked Twenty Twenty-Five instead of child theme |
| `wordpress-content-types.md` | Page vs Post vs CPT decisions |
| `abilities-api.md` | WP 7.0 Abilities API usage |
| `interactive-widgets.md` | Vanilla JS calculator widgets |
| `project-page-premium-showroom-runbook.md` | A-to-Z premium project showroom workflow |
| `skill-3d-model-pipeline.md` | 3D showroom asset/CMS pipeline: GLB, poster, facade, unit data, payload validation |
| `skill-interactive-apartment-picker.md` | Apartment selector standard: cells/polygons on the building, not abstract dots |
| `properties-catalog.md` | nadlan_property CPT + MapLibre archive |

### Living log

| File | Purpose |
|---|---|
| `site-state.md` | Append-only situation report; read the last 6 blocks first |

## Rule: skills are append-mostly

You may:
- Add new skills (only if the topic genuinely is not covered elsewhere).
- Add new sections to existing skills.
- Add dated revision notes at the bottom of a skill.
- Mark sections as DEPRECATED with a reason.

You may not:
- Delete a skill file.
- Silently rewrite a section without a revision note.
- Move strategy into a chat reply and skip writing it here.

## Rule: every action emits a skill or a state update

If a task taught you something reusable (a Yoast quirk, a plugin conflict, an RTL gotcha, a SERP shift, a Cowork failure mode), that goes into the relevant skill. If a task only changed the site, that goes into `site-state.md`. If both, do both.

## Rule: cross-reference, do not duplicate

A skill that covers a topic also covered elsewhere should _link to the other skill_, not repeat its content. Single source of truth per topic. The cross-reference map:

- Voice rules → `copywriting-skill.md`
- Link map → `internal-linking-hub-spoke.md`
- Meta requirements → `yoast-config.md`
- Plugin guards → `plugin-discipline.md`
- Design tokens → `luxury-design-system.md`
- Live state → `site-state.md`

If you find yourself writing about one of these in another skill, replace your text with a `→ see [skill]` pointer.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7). Reindexed 2026-05-30 to cover all 35+ skills + add the publishing workflow loop._

_Revised 2026-06-15 by Codex: added the premium project-showroom reading path and linked the 3D
model pipeline, apartment picker, project SEO assembly skill, and Rainbow readiness matrix so the
next Sde Dov project starts from reusable skills instead of improvisation._
