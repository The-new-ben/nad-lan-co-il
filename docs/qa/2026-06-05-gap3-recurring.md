# GAP 3 recurring QA - v1.46.0

Branch: `codex/gap3-recurring`  
Scope: plugin lane only, `plugins/nadlan-config/**` and `docs/**`  
Implementation track: free Green Invoice / Morning signed IPN rail from the runbook steps 43-68.

## What changed

- Added `inc/greeninvoice-recurring.php`.
- Added `POST /nadlan/v1/gi-ipn` with `permission_callback => __return_true`; authentication is the HMAC signature.
- Added `nadlan_gi_verify( $raw, $sigHeader, $secret, 300 )`:
  - parses `t=...,v1=...`
  - rejects timestamps outside a 300 second replay window
  - verifies `hash_hmac( 'sha256', $t . '.' . $raw, $secret )`
  - uses `hash_equals()`
- Reads the raw request body before JSON parsing.
- Rejects bad/missing signature before any business logic.
- Requires an event id and stores processed ids in bounded `nadlan_gi_charge_log`.
- Parses refs shaped as `card_<id>_user_<uid>_tier_<tier>`.
- Validates the card exists, is a Nadlan listing CPT, tier is `pro|premier`, and the ref user matches `owner_user_id` when ownership is present.
- On `paid`, extends `campaign_end`, reaffirms `paid_tier`, clears dunning state, fires `nadlan_subscription_renewed`, and logs a generic `nadlan_revenue_event( 'subscription_paid', ... )` seam.
- On `failed`, sets `dunning_state=retrying`, `dunning_since`, and `dunning_tier`.
- Adds daily `nadlan_gi_dunning_tick` with 2, 4, 7, and 14 day notice hooks, 27 day grace, then downgrade to free plus `nadlan_subscription_lapsed`.
- Adds daily `nadlan_gi_reconcile`, using `nadlan_gi_api_key` and `nadlan_gi_reconcile_url` with `sslverify => true`.
- Adds Settings -> NadLan GI for IPN secret, API key, cycle days, Morning recurring links, reconciliation URL, and a charge log table.
- Secret values are never echoed back into HTML.
- Healthcheck reports `gi.recurring_loaded`, `gi.charges_30d`, `gi.in_dunning`, and `gi.lapsed_30d`.

## Simulated IPN curl

Set the secret in Settings -> NadLan GI first. Replace the `card_<owned-card-id>_user_<owner-user-id>` placeholders with a real card and its owner, then run this from a shell that has `openssl`.

```bash
SECRET='replace-with-the-configured-secret'
BODY='{"id":"evt_gap3_paid_001","status":"paid","ref":"card_<owned-card-id>_user_<owner-user-id>_tier_premier","amount":749}'
TS=$(date +%s)
SIG=$(printf "%s.%s" "$TS" "$BODY" | openssl dgst -sha256 -hmac "$SECRET" -binary | xxd -p -c 256)
curl -i -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/gi-ipn" \
  -H "Content-Type: application/json" \
  -H "X-GI-Signature: t=$TS,v1=$SIG" \
  --data "$BODY"
```

Expected:

```json
{"ok":true,"event_id":"evt_gap3_paid_001","status":"paid","action":"extended","card_id":123}
```

Run the same curl again with the same body and signature inside the replay window.

Expected:

```json
{"ok":true,"idempotent":true,"event_id":"evt_gap3_paid_001"}
```

## Edge tests

| Case | Request | Expected |
| --- | --- | --- |
| Missing secret | IPN before `nadlan_gi_ipn_secret` is set | `503 not_configured` |
| Bad signature | Correct body, wrong `v1` | `401 bad_signature`, no side effects |
| Replayed old event | `t` older than 300 seconds | `401 bad_signature`, no side effects |
| Duplicate event id | Same event id twice | second response is idempotent and does not extend twice |
| Unknown ref | `ref=bad` | `422 bad_ref` |
| Unknown card | `card_999999_user_1_tier_pro` | `422 bad_card` |
| Owner mismatch | card owner is not ref user | `422 owner_mismatch` |
| Failed then recovered | `failed` event then new `paid` event | dunning clears and tier is restored |
| Missed IPN | paid charge appears through reconciliation | `nadlan_gi_reconcile` applies the missing extension |
| Card replaced | old ref points to missing/wrong card | rejected, no silent activation |
| Order stopped | dunning reaches day 27 | `paid_tier=free`, `dunning_state=lapsed` |

## C1-C10 checklist

- C1 scope: plugin/docs only, no theme files.
- C2 versioning: plugin header, healthcheck, manifest, and ZIP bumped to `1.46.0`.
- C3 loader: `greeninvoice-recurring` added after `advertiser-orders`.
- C4 edge cases: listed above.
- C5 security: signature verified before JSON business logic; secret never logged or echoed.
- C6 idempotency: event id is stored in `nadlan_gi_charge_log`; duplicates return 200 with no side effects.
- C7 lifecycle: paid extends, failed enters dunning, recovered clears dunning, lapsed downgrades.
- C8 performance: handler work is small; reconciliation and dunning run daily; log is bounded while keeping all entries younger than three days.
- C9 copy: admin-only labels, no public marketing copy added.
- C10 seams: emits `nadlan_subscription_renewed`, `nadlan_subscription_lapsed`, and generic `nadlan_revenue_event`.

## Local verification

Local PHP is not installed in this Windows environment, so `php -l` could not run here. Claude should run:

```bash
find plugins/nadlan-config -name '*.php' -print0 | xargs -0 -n1 php -l
```

Static gates to run before review:

```bash
rg -n "register_rest_route\\( 'nadlan/v1', '/gi-ipn'|hash_hmac|hash_equals|sslverify' => true|nadlan_gi_dunning_tick|nadlan_gi_reconcile|nadlan_subscription_renewed|nadlan_subscription_lapsed|nadlan_revenue_event" plugins/nadlan-config/inc/greeninvoice-recurring.php
rg -n "nadlan_gi_ipn_secret|nadlan_gi_api_key" plugins/nadlan-config/inc/greeninvoice-recurring.php
```

Manual secret check:

- Confirm the settings page shows only `Configured` / `Not configured` for `nadlan_gi_ipn_secret` and `nadlan_gi_api_key`.
- Confirm `nadlan_gi_charge_log` stores event id, timestamp, ref, card id, tier, status, action, and amount only.

## Source note

- Morning API docs confirm API access uses OAuth/Bearer tokens and callback/webhook notifications exist: https://developers.morning.co/
- Morning's legacy Apiary payment docs mention `X-Data-Signature` HMAC-SHA256 over the received body. This PR implements the runbook-required `t=...,v1=...` replay-window format. If Morning cannot emit that exact format, Claude should decide whether to adapt the verifier or place a tiny signed-webhook adapter in front of this endpoint.
