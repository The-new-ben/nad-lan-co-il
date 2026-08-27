# Agent Onboarding — credential handshake for a new agent (Cowork / Codex / Antigravity)

> **Notice:** this skill explains HOW a new agent gets the access it needs — securely, given the repo is public. The owner asked to "hand over all credentials" to Claude Cowork. The honest, secure answer is below: secrets live in the environment, not in text.

## The mental model

There are exactly **three** access surfaces. None of the secret values belong in the repo or in chat.

| Surface | What it is | How a new agent gets it |
|---|---|---|
| **WordPress REST** | `WP_BASE_URL`, `WP_USER`, `WP_APP_PASSWORD` env vars | Same platform environment → inherited automatically. New environment → owner re-enters them in the environment's secret config. |
| **GitHub repo** | `The-new-ben/nad-lan-co-il` | The platform provides git access to the agent's session (proxied). The agent does NOT need a PAT pasted; the platform handles auth. Scope is the one repo. |
| **wp-admin (browser) / UPress panel / Stripe** | Manual-click surfaces | Owner-held logins. A Cowork agent with browser tools uses the owner's logged-in browser session OR the owner provides those logins directly to that agent's secure input — NEVER via the repo. |

## Credential transfer to Claude Cowork — the recommended path

**Best case (same environment):** Start the Cowork session on the **same platform environment** that has `WP_USER` / `WP_APP_PASSWORD` / `WP_BASE_URL` configured. Cowork inherits them. Zero transfer. Verify with the healthcheck curl in `HANDOFF.md §3`.

**If Cowork is a fresh environment:** the owner adds three secrets to that environment's configuration (the platform's env-var / secret UI):
- `WP_BASE_URL` = `https://nad-lan.co.il`
- `WP_USER` = the admin app-password username
- `WP_APP_PASSWORD` = a **fresh** Application Password (see rotation below)

**Never** paste `WP_APP_PASSWORD` into a chat message, a commit, an issue, or any file in the repo.

## Rotate the Application Password (recommended NOW)

The current app password was pasted in plaintext in chat during earlier sessions — treat it as **compromised**. The owner should:
1. WP admin → **Users → (your profile) → Application Passwords**.
2. **Revoke** the old one (the one currently in the environment).
3. **Create a new** Application Password named e.g. `cowork-2026`.
4. Put the new value into the environment secret config (NOT chat/repo).
5. Old sessions stop working; new agent uses the fresh one. Clean cut.

This is good hygiene regardless of which agent continues.

## What the new agent should verify on first run

```bash
# 1. WordPress reachable + plugin alive
curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck"
# 2. Auth works (should show id, name, roles incl. administrator)
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,name,roles"
# 3. Git: confirm scope + branch
git remote -v ; git branch -a
```

If #1 and #2 return JSON, the handshake is complete and the agent can read/write content via REST.

## What lives where (the map)

- **Repo source of truth:** `The-new-ben/nad-lan-co-il`, branch `claude/charming-meitner-mwVEW`.
- **Theme on server:** `/wp-content/themes/nadlan-revenue/` (synced from repo `main` via UPress Git).
- **Plugin on server:** `/wp-content/plugins/nadlan-config/` (uploaded by owner; auto-updates from `plugin-dist/` after v1.2.0).
- **Live site:** `https://nad-lan.co.il` (host: UPress, WordPress 7.0, PHP 8.5.5).
- **Owner-held logins (NOT in repo):** WP admin, UPress panel, Google Site Kit/Search Console, (future) Stripe, ChatGPT (for spoke writing).

## Owner-action surfaces a REST agent cannot do (needs Cowork's browser tools or owner)

- Installing third-party plugins (PMPro, Stripe gateway).
- Merging GitHub PRs to `main`.
- UPress "ניהול GIT" pull button.
- Stripe account + API keys.
- Yoast settings that aren't REST-writable (some schema/Person fields).

Cowork (with manual-click tools) can do several of these that a pure-REST agent (like the previous Claude Code) could not — which is why the owner is migrating.

---
_Created 2026-05-29 by Claude Code (claude-opus-4-8) for the Cowork handoff._

