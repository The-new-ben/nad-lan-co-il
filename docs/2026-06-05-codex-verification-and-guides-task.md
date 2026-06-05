# Codex Task — Verify v1.51.0 Will Not Break the Live Site + Write Owner Guides

**Status:** owner-critical. The owner is about to deploy consolidated v1.51.0 on the live site
(nad-lan.co.il) and will be TRAVELLING and unavailable. Your job is to make sure the update will
NOT collapse the system and CANNOT lock the owner out, then write beginner-level step-by-step
guides so the owner can connect the concierge and the recurring billing alone.

## HARD RULES
1. **Do NOT change the plugin mechanism / runtime behavior.** This is a VERIFICATION + DOCS task.
   You may only: read code, write docs/QA files, and (if you find a genuine lockout/fatal risk)
   raise it as a BLOCKED entry in codex-status.md with the exact line — do NOT silently patch.
2. If you DO find a real lockout or fatal-error risk, STOP and post it as `BLOCKED` with the file:line
   and the minimal safe fix proposed (for Claude to apply). Owner safety beats everything.
3. Plugin lane only for any proposed fix; DRAFT PR only; never merge; never push to main.
4. Be honest. If something is not autonomous, say so. No "looks good" without evidence.

## FIVE CYCLES OF VERIFICATION (do all five, document each in codex-status.md)

### Cycle 1 — LOCKOUT SAFETY (most important)
Prove the owner CANNOT be locked out of /wp-admin or the REST API by v1.51.0. Check every one:
- `inc/roles.php`: does `nadlan_roles_setup()` ever `remove_cap()` core caps from the
  administrator, or `remove_role('administrator')`, or strip `manage_options`/`read`/`edit_posts`
  from the admin? It must NOT. Confirm the migration only ADDS caps to administrator and only
  assigns nadlan_advertiser/nadlan_buyer to non-admins. Quote the exact lines.
- Could the role migration accidentally downgrade the OWNER's account (if the owner owns a card)?
  `nadlan_roles_assign_user()` uses `add_role()` (additive) — confirm it never `set_role()` /
  never removes administrator. Quote it.
- `map_meta_cap` filter (`inc/claim.php`): confirm it only GRANTS to verified owners and otherwise
  returns `$caps` unchanged — it can never DENY an administrator (admins satisfy every primitive).
- `inc/final-hardening.php` rate limiter: confirm it only applies to a fixed allowlist of PUBLIC
  POST routes and CANNOT throttle wp-admin, wp-login, or authenticated admin REST calls. Quote the
  route allowlist and the `route_is_limited()` logic.
- Any `register_uninstall_hook` must not fire on update/deactivate — confirm it's uninstall-only.
- Verify: if OpenAI key / GI secret are ABSENT, the plugin still loads and admin still works
  (graceful 503/empty, no fatal). Trace each entrypoint.
DELIVERABLE: a LOCKOUT-SAFETY table — each risk → PASS/FAIL → file:line evidence.

### Cycle 2 — FATAL / WHITE-SCREEN SAFETY (won't collapse the site)
- Confirm every new `inc/*.php` begins with `if ( ! defined( 'ABSPATH' ) ) exit;`.
- Confirm every new function is wrapped in `function_exists()` guards (no redeclare fatals when a
  gap's function also exists elsewhere — e.g. `nadlan_revenue_event`, `nadlan_deal_closed` are
  defined in BOTH greeninvoice-recurring.php AND placement-auction.php — confirm the guards make the
  second definition a no-op, no fatal).
- Confirm no `require` of a missing file; the loader uses `file_exists()` before `require_once`.
- Confirm no PHP 7.4 incompatibility (the plugin declares Requires PHP 7.4) — flag any 8.0+ only
  syntax (named args, enums, `str_contains` without polyfill, etc.).
- Confirm all REST routes register inside `rest_api_init` and all `add_action('init', …)` cron
  scheduling is idempotent (`wp_next_scheduled` guard).
DELIVERABLE: a FATAL-SAFETY checklist with file:line for each, plus the duplicate-function audit.

### Cycle 3 — SMOKE TEST PLAN (what to click after Update Now, in order)
Write the exact ordered smoke test the owner (or Claude) runs immediately after Update Now, with
the EXPECTED result for each and what a FAILURE looks like:
1. `/wp-json/nadlan/v1/healthcheck` → expect `"version":"1.51.0"` + blocks gi/ai/roles/business/
   hardening/auction/geo. (If version is still 1.42.8 → update didn't apply.)
2. Load `/wp-admin` → expect normal dashboard (this triggers the one-time role migration).
3. Load the homepage, `/projects/`, `/professionals/` logged-out → expect normal render (no white
   screen, footer present).
4. `/wp-json/nadlan/v1/near?lat=32.0853&lng=34.7818&radius_km=25&type=project` → expect JSON list.
5. POST `/wp-json/nadlan/v1/gi-ipn` with no signature → expect 401 or 503 (NOT 500).
6. Open Settings → NadLan AI and Settings → NadLan GI → expect the forms render, no stored secret
   shown.
For EACH: the failure symptom + the immediate rollback (deactivate plugin / restore 1.50 ZIP).

### Cycle 4 — DATA & REVERSIBILITY
- List every option/meta v1.51.0 writes (roles version flag, gi options, ai options, auction meta,
  metrics snapshot, event log). Confirm none overwrite or delete existing live data destructively.
- Confirm the update is REVERSIBLE: what exactly does the owner do if something breaks? (Deactivate
  via wp-admin; if locked out, deactivate via SFTP rename of the plugin folder, or `wp plugin
  deactivate nadlan-config` via WP-CLI). Write the rollback runbook.
- Confirm the role migration is the ONLY irreversible-ish action and that it's idempotent + only
  adds roles.

### Cycle 5 — AUTONOMY TRUTH AUDIT (the owner's real question)
Answer, with evidence from the code, HONESTLY: is this a fully autonomous, owner-zero-touch,
"lead → handled → monetized → invoiced" closed circle? Map each link of the chain to the code that
exists or is MISSING:
- Lead captured? (yes — conversion-cta / lead CPT)
- Lead auto-qualified + auto-responded (no human)? (MISSING — only routed/emailed)
- Lead → booked/closed automatically? (MISSING)
- Money taken automatically? (subscriptions: YES via Morning standing order IF configured; deal/
  success-fee: MISSING)
- Invoice issued automatically? (subscriptions via Morning: YES if configured; otherwise MISSING)
- Owner-zero-touch end to end? (NO — state exactly which links need a human or are unbuilt)
Produce a one-screen "closed-circle gap map": GREEN (works hands-off after config) / YELLOW (works
but needs owner setup) / RED (not built). Do NOT inflate. The owner is travelling and will rely on
this being truthful.

## OWNER GUIDES (write these as separate docs, beginner level, screenshots)
Audience: a non-developer who does not know this system. Each guide is numbered steps, one action
per step, with a screenshot slot for every step. Because you cannot log into the live production
WP, mark each screenshot as `[SCREENSHOT: <what to capture on the live site>]` so the owner or
Claude captures the real one — annotate with the exact menu path and field names from the code so
the description is accurate. Include a Troubleshooting section per guide (symptom → cause → fix).

Guide A — "Turn on the AI concierge" (connect OpenAI):
  step-by-step: where in wp-admin (Settings → NadLan AI), paste key, save, verify via healthcheck
  `ai.provider=openai` + a test message, what "no key" looks like, cost cap fields, how to read
  today's spend. Troubleshooting: 401 from OpenAI, empty answer, "not configured".

Guide B — "Turn on automatic recurring billing" (Morning / הוראת קבע):
  step-by-step with the manual parts CLEARLY flagged: (1) in Morning, create a recurring charge
  link per tier (THIS IS MANUAL IN MORNING — owner does it in their Morning account), (2) copy the
  IPN secret into Settings → NadLan GI, (3) paste the per-tier links, (4) in Morning set the webhook
  to POST to `/wp-json/nadlan/v1/gi-ipn`, (5) confirm signature scheme = Morning, (6) send a test /
  first real charge and verify the charge log row + `campaign_end` extended. Troubleshooting: 401
  bad_signature (hex vs base64), 503 not_configured, no charge log row, dunning states.
  Be explicit about EVERY step the owner must do INSIDE Morning that this plugin cannot do for them.

Guide C — "Daily money dashboard" (read the autopilot):
  where the Ops Autopilot panel is, what each number means (MRR, churn, NRR, MRR-at-risk, leads, AI
  deflection, auction), and which numbers to watch while travelling. State the directional-not-
  board-grade caveat.

Guide D — "If something breaks while I'm away" (rollback):
  the Cycle-4 rollback runbook in plain language, including the SFTP folder-rename method for the
  worst case (locked out), and the one phone-friendly URL to check (healthcheck).

## STAY-ON-WATCH (owner instruction)
At the END of your verification, append a directive in codex-status.md addressed to Claude that
explicitly asks Claude to REMAIN in continuous watch mode (re-arm the repo monitor every cycle,
never drop the watch), to subscribe to any new PRs you open, and to re-verify on every push. The
owner does not want Claude to stop watching.

## OUTPUT
- All five cycles documented in codex-status.md (or linked QA docs).
- Guides A-D as docs/qa/2026-06-05-guide-*.md.
- A single BLOCKED entry if you find any lockout/fatal risk, with the proposed minimal fix for
  Claude to apply (do NOT patch the mechanism yourself).
- The honest closed-circle gap map (Cycle 5).
Do NOT modify plugin runtime code. Verification + docs only.
