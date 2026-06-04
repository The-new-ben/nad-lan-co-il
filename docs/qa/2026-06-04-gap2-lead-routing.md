# GAP 2 QA - Lead routing to paying card owners

Branch: `codex/gap2-lead-routing`  
Plugin target: `nadlan-config` `1.42.9`  
Scope: plugin only. No theme files, no new public routes, no secrets.

## What I Read

- `docs/2026-06-04-master-architecture-build-bible.md`, especially GAP 2 and the 10-cycle method.
- `docs/2026-06-04-codex-implementation-spec.md`, GAP 2 baseline and copy/QA rules.
- `AGENTS.md`, `BACKLOG.md`, `skills/MAP.md`, last blocks of `skills/site-state.md`.
- `skills/codex-plugin-access-and-deploy.md`.
- `skills/copywriting-skill.md`.
- `skills/advertiser-monetization-system.md`.
- Runtime files inspected: `inc/conversion-cta.php`, `inc/advertiser-center.php`, `inc/ops-dashboard.php`, `inc/owner-config-rest.php`, `inc/lead-drip.php`, `nadlan-config.php`.

## Build Summary

- New module: `plugins/nadlan-config/inc/lead-routing.php`.
- Loader: added `lead-routing` to the `foreach` module loader.
- Version bump: plugin header and healthcheck moved from `1.42.8` to `1.42.9`.
- REST path: `/nadlan/v1/lead` now calls `nadlan_lead_route()` after `lead_card_id` is stored.
- Legacy form path: `admin_post_nadlan_lead` also calls `nadlan_lead_route()` after `lead_card_id` is stored.
- Advertiser Center: adds an owner-facing `הפניות שקיבלתי` panel, querying exact `lead_card_id` only for the current user's paid cards.
- Ops: `NadLan Ops` gets an `Autopilot - advertiser delivery` card from `nadlan_lead_log`.
- Healthcheck: adds `lead_routing.loaded`, `lead_routing.log_entries`, and `lead_routing.last_7_days`.

## 10-Cycle Checklist

| Cycle | Result |
|---|---|
| C1 foundation | `nadlan_lead_route()` resolves lead, exact card, `owner_user_id`, and `paid_tier`. It delivers only for `pro`/`premier`. |
| C2 idempotence | `lead_route_attempted=1` prevents duplicate emails/log spam when the same lead is routed twice. |
| C3 security + authority | Card validation requires existing `nadlan_professional`, `nadlan_project`, or `nadlan_property`. Advertiser Center lead details query only cards owned by the current user and only paid tiers. |
| C4 edge cases | No card, invalid card, unclaimed card, free card, self-submission, missing/deleted owner, and `wp_mail=false` all degrade to a stored status instead of fatal. |
| C5 observability | Writes lead meta: `lead_route_status`, `lead_route_reason`, `lead_route_attempted_at`, `lead_routed_to_owner`, `lead_routed_owner_user_id`, `lead_routed_at` on success. Also writes bounded option log `nadlan_lead_log`. |
| C6 automation | Both current REST leads and legacy admin-post leads route automatically after card attribution. Existing admin email remains the fallback notification. |
| C7 premium UX + Hebrew copy | Owner email and center panel use `פנייה`, not the internal word. No raw dumps. Contact links use `tel:` and `mailto:`. |
| C8 full journey | Visitor submits on paid card -> lead is stored -> owner email sends -> lead appears in Advertiser Center -> Ops dashboard shows the route. Free/unclaimed cards continue to admin fallback. |
| C9 deterministic QA proof | PHP lint and ZIP content gates listed below. Live POST was not run from Codex because it would create real leads and potentially email real users. |
| C10 adversarial hardening | Existing `/lead` rate limit remains 8/hour/IP. Router is idempotent, validates card type again, and caps `nadlan_lead_log` at 500 entries. |

## Manual QA Commands for Claude Sandbox

Use controlled test users and cards only.

```bash
# Paid card path, logged-out visitor.
curl -s -k -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"בודק","phone":"0500000000","email":"qa@example.com","card_id":<PRO_OR_PREMIER_CARD_ID>,"goal":"בדיקת מסירה","message":"בדיקת GAP 2"}'
```

Expected:
- JSON includes `ok:true`.
- `lead_route_status=delivered_owner`.
- `lead_routed_to_owner=1`.
- Owner receives one email.
- Re-running `nadlan_lead_route(<lead_id>, <card_id>, ..., "qa")` returns `idempotent:true` and does not send a second email.
- `/advertiser-center/` for the owner shows the inquiry in `הפניות שקיבלתי`.
- `NadLan Ops` Autopilot card increments `delivered to owner`.

```bash
# Free/unclaimed card path.
curl -s -k -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"בודק","phone":"0500000000","card_id":<FREE_OR_UNCLAIMED_CARD_ID>,"goal":"בדיקת fallback"}'
```

Expected:
- Owner does not receive contact details.
- Existing admin email receives the fallback notification.
- `lead_route_status=fallback_admin`.
- `lead_routed_to_owner=0`.
- Free-card owner does not see contact payload in the Advertiser Center detailed inbox.

## Local Verification

To be filled after final lint and ZIP gate in this branch:

```text
PHP lint: ALL CLEAN
ZIP structure: bad_paths=0, first entry nadlan-config/nadlan-config.php
ZIP signature count: lead_routing_signatures=37
ZIP loader/version gate: loader_has_lead_routing=True, zip_version_header=True, zip_healthcheck_version=True
Live healthcheck before merge/update: nadlan-config 1.42.8
```

## Non-Claims

- I did not run a live POST from Codex because it would create production records and may send real email. The route is designed for Claude to verify with controlled sandbox users/cards.
- This PR does not add WhatsApp/SMS delivery. It exposes the `nadlan_lead_deliver` filter so a future channel can be added without rewriting the routing boundary.
