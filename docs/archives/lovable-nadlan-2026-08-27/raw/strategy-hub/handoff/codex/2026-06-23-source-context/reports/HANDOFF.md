# HANDOFF — onboarding for the next agent (Claude Cowork)

> **Read this first.** You are taking over the **NadLan** project (`נדל״ן חכם`, nad-lan.co.il) — a Hebrew/RTL Israeli real-estate WordPress site. This file is **public-safe**: it contains NO secrets. Credentials are environment variables (see §Credentials). After reading this, read the skills tree in the order under §Skills.

_Last handoff: 2026-05-29 by Claude Code (claude-opus-4-8)._

---

## 1. What this project is

A premium Hebrew real-estate **knowledge + tools + catalog** platform, monetized primarily through the owner's **law practice** (he is a practicing Israeli lawyer, NOT a broker) plus a professional directory (PMPro+Stripe, planned) and sponsored placements. Full strategy: `skills/strategy-master.md`. Monetization model: `skills/monetization-lawyer-angle.md`.

## 2. Repository

- **GitHub:** `The-new-ben/nad-lan-co-il` (PUBLIC repo — never commit secrets; see `skills/security-public-repo.md`).
- **Working branch:** `claude/charming-meitner-mwVEW` (all recent work is here).
- **`main`:** deploys to the live site via UPress Git. **Currently `main` is ~8 commits behind the working branch — PR #2 is open and UNMERGED.** Merging it is an owner action.
- The repo root **is the WordPress theme** (`nadlan-revenue`, a fork of Twenty Twenty-Five). The plugin lives at `plugins/nadlan-config/`. See `skills/theme-fork-decision.md`.

## 3. Credentials (how you get them — NO values in this file)

The live WordPress is reached via **WP REST API** using environment variables already configured in this platform environment:

| Env var | Meaning |
|---|---|
| `WP_BASE_URL` | `https://nad-lan.co.il` (public) |
| `WP_USER` | the WP admin username (an application-password user) |
| `WP_APP_PASSWORD` | the WordPress **Application Password** (SECRET — lives only in the environment, never in the repo) |

**If you (Cowork) run in the SAME platform environment, you inherit these automatically — no transfer needed.** Confirm with:
```
curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck"
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,name,roles"
```
If those return data, you're connected. If the env vars are empty, the owner must add them to your environment's secret config (see §Credential transfer in the chat handoff / `skills/agent-onboarding.md`).

## 4. The live site — what's deployed

- **Theme:** `nadlan-revenue` v1.1.0, luxury design system live (Frank Ruhl Libre serif + Heebo, warm ink/cream/gold palette). Tokens + components: `skills/luxury-design-system.md` + `docs/design/lovable-output-round-2.md`.
- **Plugin:** `nadlan-config` **v1.2.0 active** (lead REST endpoint, IndexNow auto-ping, catalog CPTs, self-hosted auto-updater). **v1.2.1 is built and committed** (`plugin-dist/nadlan-config-1.2.1.zip`) but NOT yet uploaded — owner paused the plugin-upload cycle. v1.2.1 fixes: Site Kit generator suppression, property meta for REST, healthcheck IndexNow log. See `skills/nadlan-config-plugin.md` + `skills/plugin-auto-update.md`.
- **Pages:** ~45 (42 Codex pillars/calculators/cities + new `/short-term-rentals-abroad/` pillar id 345, `/catalog/` id 359, `/buy-vs-rent/` id 343, `/sitemap/` id 336).
- **Catalog:** `nadlan_property` CPT live with 5 seed properties (ids 360-364). Their meta (price/lat/lng) is **empty until v1.2.1 is active** (v1.2.0 doesn't register property meta for REST). `/catalog/` page has the MapLibre archive widget.
- **Contact funnel:** site-wide floating FAB — WhatsApp (`wa.me/972525101555`), tel, and a lead-modal posting to `POST /wp-json/nadlan/v1/lead`. See `skills/lead-funnel.md`.

## 5. Deploy / sync model (how changes go live)

- **Content/pages/template-parts/CPTs/settings:** edit live directly via WP REST (no sync needed). This is how most work is done.
- **Theme files (style.css, theme.json, patterns, templates):** commit → owner merges PR to `main` → owner clicks UPress "ניהול GIT" pull on `/wp-content/themes/nadlan-revenue/`. UPress only syncs the `main` branch.
- **Plugin:** v1.2.0+ has a self-hosted auto-updater. To ship a new version: bump header, build `plugin-dist/nadlan-config-X.Y.Z.zip`, update `plugin-dist/nadlan-config.json`, commit, owner merges to main → WP shows "Update available" → owner clicks Update. (Owner has paused this for now.)

## 6. Honest status scorecard (2026-05-29)

| Item | Status |
|---|---|
| Luxury design system live | DONE |
| Logo + pulsing-dot header, WhatsApp/tel/lead FAB | DONE |
| Short-rent pillar (deep article + recommender + comparison) | DONE |
| `/catalog/` + MapLibre + 5 seed properties | PARTIAL (meta blocked on v1.2.1) |
| Calculators (mortgage, purchase-tax, buy-vs-rent) | DONE |
| Sitemap (clean, fresh-sorted) | DONE |
| IndexNow auto-ping | PARTIAL (works; proof endpoint needs v1.2.1) |
| Auto-updater | PARTIAL (works after PR #2 merged) |
| PMPro + Stripe self-registration | PLANNED (`skills/payments-woo-greeninvoice.md`) |
| Spoke articles (7 countries) | PROMPTS READY (`skills/spoke-prompts-short-rent-abroad.md`) — owner writes via ChatGPT |
| Real photography | BLOCKED (Codex, `skills/image-pipeline.md`) |

## 7. Immediate next actions for the new agent

1. Confirm REST connectivity (§3 curl commands).
2. Read the skills tree (§8).
3. With owner: decide whether to merge PR #2 (unblocks auto-updater) and resume v1.2.1 (unblocks catalog meta).
4. When owner sends a spoke article → publish per `skills/spoke-prompts-short-rent-abroad.md` checklist.
5. Build the PMPro+Stripe flow when owner installs PMPro (`skills/payments-woo-greeninvoice.md`).

## 8. Skills — read in this order

1. `AGENTS.md` (the cross-agent contract)
2. `skills/README.md` (index)
3. `skills/site-state.md` (living log — read the **last 6 blocks**; this is the real situation report)
4. `skills/strategy-master.md`, `skills/monetization-lawyer-angle.md`
5. `skills/luxury-design-system.md` + its sisters (`design-page-patterns`, `design-components`, `design-micro-interactions`, `design-logo-mark`, `design-rtl-hebrew`, `design-monetization-surfaces`)
6. `skills/nadlan-config-plugin.md`, `skills/plugin-auto-update.md`
7. `skills/properties-catalog.md`, `skills/lead-funnel.md`, `skills/payments-woo-greeninvoice.md`
8. `skills/agent-coordination-protocol.md`, `skills/security-public-repo.md`, `skills/image-pipeline.md`
9. `skills/spoke-prompts-short-rent-abroad.md`

## 9. Hard rules (do not break)

- **Never commit secrets** (repo is public).
- **Never put runtime code in the theme `functions.php`** — it has failed to load before; use the plugin.
- **Plugin: one capability per version, function_exists-guarded, no Hebrew in activation paths** (`skills/nadlan-config-plugin.md` lessons).
- **RTL Hebrew everywhere, no AI-tell phrases, no em-dashes** in user-facing copy (`skills/copywriting-skill.md`).
- **Update `skills/site-state.md` after every session.**

---
_This file is public-safe. The only secret (`WP_APP_PASSWORD`) is never written here — it lives in the environment. If credentials must be re-issued, the owner generates a fresh Application Password in WP admin → Users → profile → Application Passwords and puts it in the new environment's secret config._

