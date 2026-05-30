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
14. `plugin-auto-update.md` — self-hosted update channel
15. `agent-coordination-protocol.md` — UPress sync constraints

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
| `payments-pmpro-stripe.md` | Self-registration directory: Free/Pro/Premier tiers |

### Content production (the new authoring loop)

| File | Purpose |
|---|---|
| `google-blueprint-workflow.md` | Manual SERP reverse-engineering → article spec → ChatGPT prompt |
| `article-publishing-protocol.md` | ChatGPT output → live page (10-step checklist) |
| `copywriting-skill.md` | Hebrew voice; forbidden AI phrases; em-dash ban (2026-05-29 owner-explicit) |
| `internal-linking-hub-spoke.md` | Pillar→spoke map; anti-cannibalization; idempotency markers |
| `spoke-prompts-short-rent-abroad.md` | System block + 7 country prompts for ChatGPT |
| `short-term-rentals-abroad.md` | Pillar source data + 7-country regulation research |
| `yoast-config.md` | Yoast meta requirements; Person schema for lawyer E-E-A-T |

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
| `plugin-auto-update.md` | PUC self-hosted JSON; ship workflow |
| `plugin-discipline.md` | Mandatory guards (function_exists, no Hebrew in activation, no mu-plugins) |
| `theme-fork-decision.md` | Why we forked Twenty Twenty-Five instead of child theme |
| `wordpress-content-types.md` | Page vs Post vs CPT decisions |
| `abilities-api.md` | WP 7.0 Abilities API usage |
| `interactive-widgets.md` | Vanilla JS calculator widgets |
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
