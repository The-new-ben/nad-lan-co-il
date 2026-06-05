# Phased Plan — Infrastructure First, Then Solid Chunks (each gated + tested)

**Owner directive:** stop swallowing big blobs. Slice it. Lay infrastructure first so each later
slice can ship SAFELY (toggle off if bad, roll back fast, never lock the owner out). Do deep research
(>=5 cited sources per area) before building each. Push a solid chunk, test it, then the next.
Trip-safe before any reliance.

**Honest status going in (no spin):** v1.51.2 is on main but NOT proven live. OpenAI concierge code
is now correct but unverified on the site. Payments unproven until Morning IPN is configured + a real
small charge clears. The autonomous lead->money loop is NOT built. So: we build the rails to make
shipping safe, then prove one capability at a time.

---

## PHASE 0 — INFRASTRUCTURE (build this FIRST; it makes every later slice safe)
Each item is small, independently shippable, and gated. Research citations land from Claude's 4
background research streams (release-engineering, autonomous-loop, admin-control-plane, in-app-help).

- **0.1 Feature-flag layer.** Every NEW feature sits behind an option `nadlan_feature_<name>` that
  DEFAULTS OFF, with an admin toggle screen. We ship code "dark," then enable one feature at a time
  and watch. A bad feature is turned off in one click — no uninstall, no rollback needed.
  *Why first:* this is what lets us merge code without it going live until we choose.
- **0.2 Fatal-guard + canonical version.** Wrap each module `require` so a fatal in one module
  auto-disables that module (sets a flag) instead of white-screening the whole site; log it; surface
  in /health. Single source of truth for the version (no more 1.50.0 vs 1.51.x drift).
  *Why:* the owner can NEVER be white-screened by one bad feature while travelling.
- **0.3 Staging-first + rollback runbook.** Document/confirm a staging clone path; keep the prior
  ZIP; the SFTP folder-rename + wp-cli deactivate rollback; (optionally) WP Rollback plugin. A
  one-page "if it breaks" card.
- **0.4 Audit log.** Record every admin/operator change (who/what/when/old->new). Needed by the admin
  control plane (Phase E) and for trust. Bounded, no secrets.
- **0.5 Contextual-help framework.** A reusable help layer (field tooltips + step tours + WP Pointers)
  that every later feature plugs its guidance into — built once, used everywhere. Hebrew/RTL, a11y.

**PHASE 0 GATE (must pass before any feature chunk):** feature flags toggle a test feature on/off
live; killing a module doesn't white-screen; /health shows version + module status; rollback drill
performed on staging; audit log records a test change. Pass/fail table + exact URLs/curls + screenshots.

---

## SOLID CHUNKS (one at a time: build -> push -> QA gate -> staging test -> production enable)
Order chosen for value + safety. Each has a brutally concrete release gate (pass/fail, URLs, curls,
screenshots, blockers-that-must-be-fixed).

### CHUNK A — SAFETY PATCH (make current v1.51.2 safe & dark)
Put all 9 already-built tracks behind feature flags (default OFF), confirm lockout/fatal-safe, ship.
Nothing new goes live yet — this just makes the merged code controllable. **This is the "release
gate" the owner asked for before the blind install.**
GATE: every track flag OFF = behaves exactly like 1.42.8; flags individually ON = feature appears;
admin never locked out; rollback proven.

### CHUNK B — LEAD CAPTURE END-TO-END (owner's top priority: "lead and what's happened, end to end")
Prove: a real lead (web form first, WhatsApp second) -> lead record -> routed to the right paid
owner -> owner notified -> owner inbox shows it -> delivery logged -> (later) auto-acknowledged.
Web form path first (no external deps), then add WhatsApp inbound.
GATE: submit a real test lead; see it routed + logged + delivered; screenshots of each hop; failure
modes (no owner, free card) handled. 5-source research on lead autonomy + WhatsApp before building.

### CHUNK C — PAYMENTS + RECURRING BILLING PROVEN
Configure Morning recurring + signed IPN; run ONE real small charge; verify the IPN signature
(hex/base64), campaign_end extension, invoice issued by Morning, dunning on a forced failure.
GATE: a real (small) payment clears, invoice issued, IPN verified, access extended, charge-log row.
5-source research on Morning/WooCommerce invoicing + webhook security.

### CHUNK D — AI SUPPORT PROVEN (OpenAI concierge live)
Enable the flag, set the OpenAI key, prove grounded answers + sources-or-abstain + human handoff +
cost cap, with a real model call.
GATE: live chat answers from site content, abstains off-topic, hands to a human, spend visible.

### CHUNK E — ADMIN CONTROL PLANE (your new request)
Operator screen to change a client's LOCATION, references/links, PRIORITIES, and the internal
competition/placement (boost/pin/slots), every change audit-logged; safe impersonation rules.
5-source research on admin/RBAC/audit + safe impersonation before building.

### CHUNK F — CONTEXTUAL HELP EVERYWHERE (your new request)
Field-level popup guidance + step tours on every screen, friendly, Hebrew/RTL, dismissible. Plugs
into the Phase-0.5 framework. 5-source research on field-help/tours/WP-pointers before building.

### CHUNK G — AUTONOMOUS LOOP CLOSURE (last, hardest, owner-approval-gated)
WhatsApp auto-qualify + auto-respond within minutes, booking, and the deal/success-fee monetization
+ invoicing — the actual "lead -> money while I travel" circle. Built only after B/C/D are proven,
because it stacks on all of them. Owner-approval gate on anything that acts/charges/builds.

---

## How we work each chunk (the loop)
1. Claude deep-research the chunk (>=5 cited sources) + hand Codex the spec; Codex ALSO researches
   his side and posts findings.
2. Codex builds behind a feature flag (default OFF), DRAFT PR.
3. Claude reviews + EXECUTES tests, posts pass/fail.
4. Merge to main with the flag still OFF (dark).
5. Enable the flag on STAGING, run the concrete QA gate, capture screenshots.
6. Only when the gate is GREEN: enable on production.
7. Rollback drill confirmed for that chunk before moving on.

## Research status (Claude, in progress — citations land here)
- Release/deploy infrastructure (flags, staging, migrations, rollback, gates) — RUNNING
- Autonomous lead->money loop + WhatsApp end-to-end — RUNNING
- Admin control plane (change location/refs/priorities/competition, audit, impersonation) — RUNNING
- In-app contextual help (field tooltips, tours, WP pointers, onboarding) — RUNNING
Each will be appended with >=5 source URLs and concrete rules. Codex researches his side in parallel.
