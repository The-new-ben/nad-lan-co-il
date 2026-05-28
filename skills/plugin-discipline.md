# Plugin Discipline

> **Notice to all agents:** the owner explicitly does not want plugin sprawl. Every new plugin is a future maintenance burden, a future security surface, and a confusion point for the next agent who doesn't know why it's there. Default answer to "should we install X?" is **no**. Justify each one against this file before installing.

## Currently installed (as of 2026-05-28)

Active:
- **Yoast SEO** (v27.7) — SEO, schema, sitemap. Kept. Configuration in `yoast-config.md`.
- **Google Site Kit** (v1.179.0) — GSC, GA4, PageSpeed, AdSense integration. Kept. Currently: site-verification + search-console + pagespeed-insights connected; Analytics/AdSense/TagManager NOT connected.

Inactive:
- **AI Provider for OpenAI** (v1.0.3) — purpose unclear, not active. Owner decision: delete or keep dormant. Default action: leave inactive until owner decides.
- **Akismet** — anti-spam. Owner can activate when comment spam becomes an issue (currently comments may be off site-wide).
- **Hello Dolly** — stock WordPress default. Useless. Safe to delete; not urgent.

## When to install a new plugin — checklist

A new plugin clears the bar ONLY if all of these are true:

1. The capability is genuinely needed for a documented strategy item (cite the skill file + section).
2. Cannot be done in ~50 lines of PHP added to this theme's `functions.php`.
3. Active maintenance: last release within 6 months, >50K active installs, security history clean.
4. License-compatible (GPL or compatible).
5. Owner approves the cost (if paid).
6. Doesn't duplicate something an existing plugin can do.
7. Documented in this file with: why it was added, who added it, what the next agent should know.

If any of these fails: do not install. Add the gap to `site-state.md` as an open issue instead, or write it in-theme.

## Plugins the strategy doc tempts us to install — currently DECLINED

| Plugin | Strategy doc reasoning | Why declined for now |
|---|---|---|
| **Redirection** (Yoast Premium or free Redirection plugin) | Required before any URL change | We are NOT changing URLs. The owner endorsed flat-URL discipline. Decline until a real URL change is approved. |
| **WP Rocket / FlyingPress** | Caching for Lighthouse targets | UPress (managed Israeli WP host) ships its own caching layer. Don't double-cache. Decline until UPress's cache proves insufficient. |
| **Cloudflare** | CDN, security | UPress's edge already handles this. Decline. |
| **Wordfence / iThemes Security** | Security hardening | UPress runs security at the host level. Adding a heavy plugin layer slows the site for marginal benefit. Decline until a specific threat appears. |
| **Gravity Forms / WPForms** | Lead forms | Our own `nadlan_lead` CPT + handler in `functions.php` does the job for the basic intake form. Re-evaluate when we need conditional logic, multi-step, or webhook fanout. |
| **Paid Memberships Pro + Stripe** | Self-service professional directory | Phase 1 of the self-service vision (`agent-tooling-strategy.md`). Real cost (PMPro Pro tier + Stripe fees). Owner approves BEFORE installation. |
| **WPML / Polylang** | Multilingual (English investor microsite) | Only if/when we ship `/en/` for foreign-Jewish investors. Decision deferred. |
| **Git Updater** | Repo→site sync of theme/plugins | UPress's native Git management (the screenshot the owner sent) supersedes this. Decline — use UPress's native flow. |
| **AI Provider for OpenAI** | (already installed, inactive) | Owner decision. Either delete or keep dormant. Don't activate without understanding what it does. |
| **WP All Import / Export** | Bulk import / export of pages | Codex on local PC writes pages directly via WP REST. Don't need import plugin. |
| **Custom Post Type UI** | CPT registration via admin UI | We register CPTs in code via `functions.php`. Decline; "code-defined CPT" is the strategy. |
| **ACF (Advanced Custom Fields)** | Custom fields for property/project | Tempting. Adds a real dependency. Defer until the `nadlan_property` CPT is actually built. When that day comes, consider the free version only. |

## Plugin removal protocol

To delete a plugin:
1. Confirm no theme code calls its functions.
2. Confirm no published page or block depends on it.
3. Document the removal in `site-state.md`.
4. Owner deactivates → tests site → if OK, deletes.

## Open TODOs for next agent

- [ ] Owner: decide whether to keep `AI Provider for OpenAI` (inactive) or delete it. Currently dormant; no harm in leaving.
- [ ] When the inquiry-form needs more than basic intake (e.g., file upload for proof of bar admission for the professional directory), revisit Gravity Forms.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7)._
