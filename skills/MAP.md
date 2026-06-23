# SKILLS MAP — every file, where, why, when

> **Purpose.** One single page that answers, for **every** agent (Claude / Codex /
> Cowork / ChatGPT-via-browser / Gemini / human): *what skills exist, where they
> live, what each does, and when to open it*. Read this BEFORE doing any work.
>
> **Status keys:** ✅ ACTIVE (current source of truth) · 🟡 REFERENCE (still useful for
> background or pattern reuse) · 🟪 DNA (portable to other sites in the network) ·
> ⚠️ DEPRECATED (kept for history; do not act on without checking the active replacement)
>
> **Last updated:** 2026-06-23 (Codex). When you change a skill, append a Revision
> line at the bottom of THAT skill and update this MAP if the status changes.

---

## 0. The "first 10 minutes" reading list

If you have only 10 minutes (a fresh agent walking in), read these in this order:

1. **`/AGENTS.md`** ✅ — the prime directive: how agents work in this repo
2. **`/BACKLOG.md`** ✅ — what we're doing right now (newest decisions win)
3. **`skills/MAP.md`** ✅ — this file
4. **`skills/nadlan-autonomous-execution-master.md`** ✅ — autonomous loop, no-stacking rule, screenshots, release gates
5. **`skills/site-state.md`** ✅ — append-only situation report; **read the last 6 blocks**
6. **`skills/codex-plugin-access-and-deploy.md`** ✅ — the deploy pipeline (mandatory before any plugin change)
7. **`skills/honesty-statement.md`** ✅ — no-flattery + cite-or-flag policy
8. **`skills/url-namespace-contract.md`** ✅ — slug/URL rules (mandatory before publishing any page)
9. **`skills/copywriting-skill.md`** ✅ — voice, forbidden phrases, em-dash ban
10. **`skills/SKILLS-TREE.md`** ✅ — the portable DNA branches (for stamping new sites)
11. **`skills/ACCUMULATION.md`** ✅ — how to add/update a skill (when you learn something)

Everything else is on-demand by category below.

---

## 1. OPERATING SYSTEM (how agents act, coordinate, ship)

| Status | File | Purpose | When to open |
|---|---|---|---|
| ✅🟪 | `/AGENTS.md` | Prime directive, source-of-truth rule, mandatory read/write protocol | Every session start |
| ✅🟪 | `/HANDOFF.md` | Public-safe access map (URLs, credentials *references*, not values) | When you need to know how to authenticate or where things live |
| ✅🟪 | `/BACKLOG.md` | Living priority queue + shipped log | Every session start AND end |
| ✅🟪 | `skills/agent-onboarding.md` | Secure credential handshake; what env vars and app passwords exist | Once at session start to confirm auth |
| ✅🟪 | `skills/agent-coordination-protocol.md` | Multi-agent sync rules; how Claude/Codex/Cowork avoid stepping on each other | Before starting work parallel to another agent |
| ✅🟪 | `skills/agent-tooling-strategy.md` | Which agent does what (Codex = orchestration; Cowork = content; Claude = code) | When deciding to delegate vs do |
| ✅🟪 | `skills/nadlan-autonomous-execution-master.md` | Master autonomous execution loop: no stacking, screenshots, release gates, Lovable sync, cross-site replication | Every NadLan implementation session |
| ✅🟪 | `skills/adopted-codex-goal-bundle.md` | Turns broad owner requests into one bounded autonomous slice with verification and stop conditions | When the task is broad, urgent, or must run standalone |
| ✅🟪 | `skills/adopted-codex-instruction-chain.md` | Checks AGENTS/project guidance, done definition, commands, and escalation rules | Before starting long autonomous work or changing repo conventions |
| ✅🟪 | `skills/adopted-codex-progressive-disclosure.md` | Loads only the relevant reports, skills, and references instead of flooding context | When many handoff reports or skills exist |
| ✅🟪 | `skills/adopted-codex-visual-proof-loop.md` | Screenshot-first UI proof loop with public-language and no-stacking checks | Any visible page, component, or responsive change |
| ✅🟪 | `skills/adopted-wp-playground-verification.md` | WordPress runtime verification using Playground or wp-env style feedback loops | Before trusting plugin or theme behavior without live deploy |
| ✅🟪 | `skills/adopted-wp-plugin-quality-gate.md` | Plugin quality gate: packaging, i18n, version surfaces, Plugin Check mindset | Any plugin release or ZIP artifact |
| ✅🟪 | `skills/adopted-wp-security-threat-gate.md` | Security gate for input, output, REST, AJAX, SQL, uploads, nonces, capabilities | Any code touching user input or permissions |
| ✅🟪 | `skills/adopted-wp-performance-gate.md` | Performance gate for route-scoped assets, duplicate CSS/JS, queries, and REST calls | Any public page or asset-loading change |
| ✅🟪 | `skills/adopted-wp-accessibility-rtl-gate.md` | Accessibility plus Hebrew RTL gate | Any public UI, mobile, focus, contrast, or Hebrew layout change |
| ✅🟪 | `skills/adopted-wp-release-agent-gate.md` | Separates implementation, verification, packaging, deploy, and rollback responsibilities | Before release PRs or production-bound packages |
| ✅🟪 | `skills/adopted-wp-rest-api-contract-gate.md` | REST API schema, permission, validation, and consumer contract gate | Any REST endpoint or API consumer change |
| ✅🟪 | `skills/adopted-wp-mcp-abilities-map.md` | Maps existing plugin/admin/MCP capabilities before inventing new code | Before adding automation, admin surfaces, or AI integration |
| ✅🟪 | `skills/honesty-statement.md` | No flattery, cite-or-flag, refusal to claim without verification | Any time you're tempted to make a confident claim — re-read it |
| ✅🟪 | `skills/security-public-repo.md` | What NEVER goes into the public repo (secrets, partner names, prices, client data) | Before committing any new file |
| ✅🟪 | `skills/ACCUMULATION.md` | Protocol for adding/updating skills (this file's sibling) | When you've learned something worth keeping |
| ✅ | `skills/site-state.md` | Append-only dated situation report — the live narrative of the project | Read last 6 blocks at session start; APPEND at session end |
| 🟡 | `skills/original-prompt-2026-05-28.md` | The owner's original mission statement | Read once at onboarding for context |

## 2. PLUGIN: nadlan-config (the engine; lives in `plugins/nadlan-config/`)

| Status | File | Purpose | When to open |
|---|---|---|---|
| ✅🟪 | `docs/codex-onboarding-and-mission-brief.md` | **THE one-shot onboarding** — repo access, every feature/module/REST endpoint, user journeys, coding examples, the Last-Mile Contract anti-premature-completion checklist | Paste-to-Codex (or any new agent) at session start |
| ✅🟪 | `skills/codex-plugin-access-and-deploy.md` | **THE deploy pipeline** — 9-step ship loop, every blocker pre-solved, multi-agent etiquette | **MANDATORY** before touching any plugin code |
| ✅🟪 | `skills/nadlan-config-plugin.md` | Plugin lessons + one-capability-per-module rule + coding conventions | Before writing a new `inc/<module>.php` |
| ✅🟪 | `skills/plugin-discipline.md` | What belongs in a plugin module vs the theme | Architectural decisions |
| ✅🟪 | `skills/plugin-auto-update.md` | How the self-hosted update channel works (plugin-update-checker + manifest) | If the updater misbehaves |
| ✅🟪 | `skills/SKILLS-TREE.md` | Sorts every skill + every code module into 6 portable DNA branches | When opening a NEW site in the network |

## 3. SEO + CONTENT ENGINE

| Status | File | Purpose | When to open |
|---|---|---|---|
| ✅🟪 | `skills/url-namespace-contract.md` | **THE slug / URL rules** — Latin-only, one-concept-one-URL, namespace map, pre-publish collision check | **MANDATORY** before publishing/renaming any page |
| ✅🟪 | `skills/copywriting-skill.md` | Voice, em-dash ban, forbidden phrases (no internal/CRM language in public copy) | Before drafting any public Hebrew copy |
| ✅🟪 | `skills/article-publishing-protocol.md` | Publish checklist for long-form articles | When publishing a guide/pillar/spoke |
| ✅🟪 | `skills/article-qa-audit.md` | QA gate before going live (word count, H1, links, schema) | After draft, before publish |
| ✅🟪 | `skills/article-guide-design-pattern.md` | Layout pattern for guides/pillars | Designing a new long-form page |
| ✅🟪 | `skills/google-blueprint-workflow.md` | How to research a SERP before writing | Before scoping any keyword target |
| ✅🟪 | `skills/internal-linking-hub-spoke.md` | Pillar/spoke/glossary linking law + anti-cannibalization | When mapping a new content cluster |
| ✅🟪 | `skills/authority-eeat-program.md` | E-E-A-T expert authorship (the owner is a RE lawyer = built-in advantage) | When deciding bylines / expert quotes |
| ✅ | `skills/content-encyclopedia-glossary-plan.md` | Glossary architecture + term selection | Before adding glossary terms |
| ✅ | `skills/wordpress-content-types.md` | When to use Page vs Post vs CPT | Any new content type decision |
| ✅ | `skills/yoast-config.md` | Required meta + Person schema | Per-page SEO settings |
| ✅ | `skills/strategy-master.md` | nad-lan SEO/business master strategy (Hebrew) | Strategic decisions about keyword targeting |
| ✅ | `skills/nadlan-seo-content-design-monetization-rulebook.md` | The rulebook (Hebrew) | Strategic alignment check |
| 🟡 | `skills/lovable-competitor-blueprint-2026-06.md` | Competitor teardown (Madlan / Yad2 / Nadlanmaster) | Strategic moves vs competitors |
| 🟡 | `skills/nadlanmaster-anatomy-and-attack.md` | Specific competitor breakdown | Opportunity hunting |
| 🟡 | `skills/short-term-rentals-abroad.md` | Foreign STR cluster brief | If working that cluster |
| 🟡 | `skills/spoke-prompts-short-rent-abroad.md` | 7 ChatGPT prompts for the STR cluster | Same |
| 🟡 | `skills/properties-catalog.md` | Property data model | When working on `nadlan_property` CPT |
| 🟡 | `skills/proptech-adoption-roadmap.md` | Industry adoption notes | Background |

## 4. DESIGN SYSTEM

| Status | File | Purpose | When to open |
|---|---|---|---|
| ✅🟪 | `skills/design-rtl-hebrew.md` | RTL + Hebrew-specific rules (logical properties, fonts) | All design work for nad-lan / jus-tice / hea-lth (any Hebrew site) |
| ✅🟪 | `skills/design-components.md` | Component library spec | Building/changing UI components |
| ✅🟪 | `skills/design-page-patterns.md` | Standard page layouts | New page template |
| ✅🟪 | `skills/design-implementation.md` | How design tokens land in code | Implementation handoff |
| ✅🟪 | `skills/design-micro-interactions.md` | Hover/focus/loading micro-animation specs | Polish pass |
| ✅🟪 | `skills/design-monetization-surfaces.md` | Sponsored slots, ad reservations, upgrade CTAs | When adding revenue surfaces |
| ✅🟪 | `skills/luxury-design-language.md` + `luxury-design-system.md` | Brand voice and tokens (gold/ink/cream palette) | Any brand decision |
| ✅🟪 | `skills/design-logo-mark.md` | Logo + favicon spec | Per-brand output |
| ✅🟪 | `skills/visual-design-skill.md` | Visual judgment heuristics | When making aesthetic calls |
| ✅🟪 | `skills/accessibility-israel-is5568.md` | Israeli accessibility law compliance | Required on every IL site |
| ✅🟪 | `skills/image-pipeline.md` | Image generation + optimization pipeline | When attaching images |
| ✅🟪 | `skills/interactive-widgets.md` | Calculator/widget component patterns | Building interactive tools |
| ✅🟪 | `skills/project-3d-sales-experience.md` | Interactive project showroom standards: building-first, unit picker, map/sun/lead seams | Before changing any project 3D or apartment-selection page |
| ✅🟪 | `skills/project-page-premium-showroom-runbook.md` | A-to-Z repeatable project page runbook: research, assembly, schema, 3D, WhatsApp funnel, QA, deploy | Before cloning Rainbow quality to another project |
| 🟡 | `skills/theme-fork-decision.md` | When to fork the theme vs extend the plugin | Architectural decision |

## 5. MONETIZATION + REVENUE

| Status | File | Purpose | When to open |
|---|---|---|---|
| ✅🟪 | `skills/payments-woo-greeninvoice.md` | **LIVE** Woo + Green Invoice (Morning) gateway; products 476/477/489/490; the recurring-billing caveat | Before touching anything that handles ₪ |
| ✅🟪 | `skills/lead-funnel.md` | Funnel design pattern | Designing a new capture surface |
| ✅🟪 | `skills/advertiser-monetization-system.md` | Self-serve advertiser journey: pay, activate `paid_tier`, expire paid access, edit, upload, report, renew | Building paid listings/projects/profiles |
| ✅🟪 | `skills/customer-value-spec.md` | What the customer actually pays for (the "asset, position, duration") | Designing pricing/packaging |
| ✅🟪 | `skills/monetization-readiness-and-adsales.md` | Ad-sales readiness checklist | Before pitching sponsorships |
| ✅ | `skills/monetization-lawyer-angle.md` | RE-lawyer-specific lead angle (owner is the expert) | When pitching legal-leg leads |
| ✅ | `skills/listings-auction-directory-architecture.md` | Directory + claim funnel + auction engine architecture | Architectural reference for the engine |
| ✅ | `skills/directory-listings-project-plan.md` | nad-lan rollout plan for the directory | Sequence/priority reference |

## 6. CALCULATORS + DATA APIS

| Status | File | Purpose | When to open |
|---|---|---|---|
| ✅ | `skills/abilities-api.md` | Where the calculator JS lives and how it talks to the plugin | When changing any calculator |

## 7. RUNBOOKS for Cowork (content publishing + QA)

| Status | File | Purpose | When to open |
|---|---|---|---|
| ✅🟪 | `skills/qa-journey-testing.md` | **THE Cowork end-to-end QA script** — 5 personas (incl. "Rainbow Project" advertiser), journey charters, session-report template, acceptance bar, fix→re-run loop. Reports land in `docs/qa/`. | Running any QA / smoke-test pass before or after a release |

### (content publishing runbooks below)

| Status | File | Purpose | When to open |
|---|---|---|---|
| ✅ | `skills/runbook-cowork-FULL-OPERATOR-v3.2.md` | The current Cowork operator runbook | Cowork sessions |
| ⚠️ | `skills/runbook-cowork-article-batch-v3.md` | Older article-batch runbook | Reference only — superseded by FULL-OPERATOR |
| ⚠️ | `skills/runbook-cowork-article-batch-v2.md` | Older still | Reference only |
| ⚠️ | `skills/runbook-cowork-article-batch.md` | Original | Reference only |
| ✅ | `skills/cowork-briefing.md` | Condensed history + voice + guardrails for Cowork | Send to a fresh Cowork session |
| ✅ | `skills/cowork-prompt-business-readiness.md` | Cowork business-readiness checklist prompt | Specific business-side ops |
| ✅ | `skills/cowork-prompt-ga4-sitekit.md` | Cowork prompt for GA4 + Site Kit work | Analytics work |

## 8. DOCS folder (`/docs/*` — implementation logs + handoffs)

These are point-in-time documents, not living skills. Read them if their topic is current.

| File | What it is |
|---|---|
| `docs/glossary-slug-migration-2026-06-02.md` | Record of the 22 glossary slug renames + 301 mapping |
| `docs/AGENT_HANDOFF_NADLAN_CONFIG_1_35_ARCHIVE_SEO_2026-06-02.md` | Codex's 1.35 handoff (PR closed; partial ideas absorbed into later versions) |
| `docs/NADLAN_CONTENT_ARCHITECTURE_AUDIT_2026-06-02.md` | Codex's content audit (sharp findings; still relevant) |
| `docs/NADLAN_CHATGPT_SERP_BLUEPRINT_WORKFLOW_2026-06-02.md` | SERP blueprint workflow Codex wrote |
| `docs/OPERATING_PLAN.md` | Cross-site operating plan (multi-site portfolio) |
| `docs/PRODUCTION_LAUNCH_PLAN.md` | Production launch plan |
| `docs/MONEY_PAGE_BRIEFS.md` | Money-page briefs |
| `docs/CRM_AUTOMATION.md` | CRM automation notes |
| `docs/master-plan-and-sequencing.md` | Master sequencing |
| `docs/cowork-*.md` | Specific Cowork mission prompts |
| `docs/contract-audit-*.md` + `competitive-research-contract-audit.md` | Contract / TOS / refund audits |
| `docs/lovable-prompt*.md` | Lovable prompts shipped to designers |
| `docs/listings-questions.md` | Open listing questions |
| `docs/lawyer-profile-template.md` | Template for a lawyer profile |

## 9. ⚠️ DEPRECATED / superseded (kept for history, do not act on)

- **Hebrew glossary slugs** — superseded by Latin slugs per `docs/glossary-slug-migration-2026-06-02.md`.
- **runbook-cowork-article-batch.md / v2 / v3** — use `runbook-cowork-FULL-OPERATOR-v3.2.md` instead.
- **"PayPlus" references** anywhere — wrong. Production stack is Green Invoice / Morning, see `payments-woo-greeninvoice.md`.

## 10. Where Codex must look for THIS site, in one paragraph

The repo root contains `AGENTS.md` (prime directive), `BACKLOG.md` (priority queue + shipped log),
`README.md` (project intro), `HANDOFF.md` (public-safe access). All knowledge lives under `skills/`
as flat `.md` files and under `docs/` as implementation logs. The plugin source is `plugins/nadlan-config/`
with the deploy pipeline documented in `skills/codex-plugin-access-and-deploy.md`. The portable DNA
(reusable on the owner's other sites) is mapped in `skills/SKILLS-TREE.md`. The URL/slug rules are in
`skills/url-namespace-contract.md`. To add a new skill, follow `skills/ACCUMULATION.md`. **No special
tooling is required — `git`, `cat`, and `grep` are all an agent needs to read everything.**

---

## Revision log
- 2026-06-23 - Codex added the adopted Codex and WordPress skill pack from external research: goal bundle, instruction chain, progressive disclosure, visual proof, Playground verification, plugin quality, security, performance, accessibility, release, REST, and abilities-map gates.
- 2026-06-03 — Created (Claude). Built after web research of the AGENTS.md open spec, Claude Code
  skills convention, and Knowledge-as-Code pattern (see AGENTS.md "Sources" section for citations).
  Categorises the 61 existing skill files + 20 docs into 9 functional sections, marks ACTIVE vs
  REFERENCE vs DEPRECATED, and lists the 10-minute reading order. Pairs with new
  `skills/ACCUMULATION.md` (protocol for adding/updating skills) and the upgraded `AGENTS.md`.
