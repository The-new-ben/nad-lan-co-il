# Chunk B Lead E2E QA Gate - v1.52.0

Branch: `codex/chunk-b-lead-e2e`

Scope: lead journey only. One feature flag, default off: `nadlan_feature_lead_e2e = 0`.

## What Changed

- New module: `plugins/nadlan-config/inc/lead-e2e.php`.
- Loader: `lead-e2e` added after `lead-routing`.
- Version aligned to `1.52.0` in plugin header, `/healthcheck`, `/health`, and manifest.
- Existing `/nadlan/v1/lead` REST endpoint remains the only lead intake route. When the flag is off, it follows the old code path. When the flag is on, it delegates to `nadlan_lead_e2e_capture()`.
- Existing `admin-post.php?action=nadlan_lead` handler follows the old path while off and delegates to the E2E capture while on.
- New authenticated route: `POST /wp-json/nadlan/v1/lead/status`.
- Advertiser Center inbox shows workflow status, ack state, response time, private note, and status update controls only when the feature is on and the current user is allowed to manage the lead.
- `lead_e2e` metrics appear in `/healthcheck`, `/health`, the daily metrics snapshot, and the Ops/Autopilot dashboard.

## 10-Cycle Checklist

| Cycle | Result |
|---|---|
| C1 reuse existing lead surfaces | Reuses `nadlan_lead`, `conversion-cta.php`, `nadlan_lead_route()`, `nadlan_lead_log`, and advertiser-center. No duplicate `/lead` route. |
| C2 visitor acknowledgement | Sends visitor ack once by email, calls `apply_filters('nadlan_lead_deliver', ...)`, records `ack_sent_at`, and exposes `do_action('nadlan_lead_ack', ...)`. |
| C3 status workflow | Adds `lead_status` values `new/contacted/won/lost`, nonce-protected REST status route, owner/admin cap check, and bounded `nadlan_lead_audit`. |
| C4 inbox upgrade | Shows status, ack state, response-time, status select, and private note for paid owned-card leads only. |
| C5 response-time | Records `lead_first_response_at` on the first non-new owner/admin action and computes minutes. |
| C6 fallback | No card, invalid card, unclaimed card, free tier, self-submission, or failed owner delivery falls back to admin notification and `lead_e2e_fallback_admin=1`. |
| C7 metrics | Adds `lead_e2e` block: `leads_7d`, `delivered_7d`, `ack_rate`, `avg_response_minutes`, `fallback_7d`, `by_status`, `audit_entries`. |
| C8 idempotency | Same card + contact + name inside the short window uses an atomic `add_option()` guard. This is intentionally global because `add_post_meta(..., unique=true)` is unique only per post, not across all leads. Duplicate returns the first `lead_id`, with no second ack/delivery. |
| C9 security | Inputs sanitized, `/lead/status` requires login + REST nonce + owner/admin cap, `/lead` and `/lead/status` are rate-limited 8/min/IP, and audit/event logs avoid contact payloads. |
| C10 hardening | PHP lint, root ZIP listing, manifest/version alignment, and this QA doc. |

## Acceptance Gates

Replace the placeholders before running:

```bash
BASE="https://nad-lan.co.il"
CARD_PAID="REPLACE_WITH_PAID_CARD_ID"
CARD_FREE="REPLACE_WITH_FREE_OR_UNCLAIMED_CARD_ID"
OWNER_COOKIE="cookies-owner.txt"
ADMIN_COOKIE="cookies-admin.txt"
OWNER_NONCE="REPLACE_WITH_WP_REST_NONCE_FROM_ADVERTISER_CENTER"
ADMIN_NONCE="REPLACE_WITH_WP_REST_NONCE_FROM_ADMIN"
```

### G1 - Flag OFF keeps today's behavior

```bash
wp option update nadlan_feature_lead_e2e 0
curl -s -X POST "$BASE/wp-json/nadlan/v1/lead" \
  -H "Content-Type: application/json" \
  --data "{\"name\":\"בדיקת כבוי\",\"phone\":\"0500000000\",\"goal\":\"בדיקה\",\"message\":\"flag off\",\"card_id\":$CARD_PAID}"
curl -s "$BASE/wp-json/nadlan/v1/healthcheck" | jq '.version,.lead_e2e.enabled'
```

Expected:

- Response shape remains the old `/lead` shape with `ok` and `lead_id`.
- No `ack_sent_at`, `lead_e2e_enabled`, or `lead_status` is written on the new lead.
- `lead_e2e.enabled` is `false`.

### G2 - Flag ON paid card full path

```bash
wp option update nadlan_feature_lead_e2e 1
curl -s -X POST "$BASE/wp-json/nadlan/v1/lead" \
  -H "Content-Type: application/json" \
  --data "{\"name\":\"בדיקת לקוח\",\"phone\":\"0501111111\",\"email\":\"lead-test@example.com\",\"goal\":\"פנייה לכרטיס בתשלום\",\"message\":\"בדיקת מסלול מלא\",\"card_id\":$CARD_PAID}"
curl -s "$BASE/wp-json/nadlan/v1/healthcheck" | jq '.lead_e2e'
```

Expected:

- Lead created with `lead_card_id=$CARD_PAID`, `lead_status=new`, `lead_e2e_enabled=1`.
- `lead_route_status=delivered_owner`.
- `ack_sent_at` exists once.
- `nadlan_lead_log` has a `delivered_owner` entry.
- Advertiser Center for the owner shows the lead and contact payload.

### G3 - Idempotent duplicate

Run the same G2 curl again within 15 minutes.

Expected:

- Response includes the first `lead_id` and `idempotent=true`.
- No second `nadlan_lead` post.
- No second `ack_sent_at`, owner delivery, or admin fallback.

### G4 - Status workflow and audit

```bash
curl -s -X POST "$BASE/wp-json/nadlan/v1/lead/status" \
  -b "$OWNER_COOKIE" \
  -H "Content-Type: application/json" \
  -H "X-WP-Nonce: $OWNER_NONCE" \
  --data "{\"lead_id\":REPLACE_LEAD_ID,\"status\":\"contacted\",\"note\":\"בדיקת תגובה\"}"

curl -s -X POST "$BASE/wp-json/nadlan/v1/lead/status" \
  -b "$OWNER_COOKIE" \
  -H "Content-Type: application/json" \
  -H "X-WP-Nonce: $OWNER_NONCE" \
  --data "{\"lead_id\":REPLACE_LEAD_ID,\"status\":\"won\"}"
```

Expected:

- First response sets `lead_first_response_at`.
- `lead_status` changes `new -> contacted -> won`.
- `nadlan_lead_audit` includes `old_status/new_status` rows for both transitions.
- Non-owner cookie returns 403.
- Admin cookie + nonce can update the same lead.

### G5 - Free/unclaimed fallback

```bash
curl -s -X POST "$BASE/wp-json/nadlan/v1/lead" \
  -H "Content-Type: application/json" \
  --data "{\"name\":\"בדיקת נפילה למנהל\",\"phone\":\"0502222222\",\"email\":\"fallback-test@example.com\",\"goal\":\"כרטיס לא בתשלום\",\"message\":\"fallback\",\"card_id\":$CARD_FREE}"
```

Expected:

- Lead created and attributed to the card.
- `lead_route_status=fallback_admin`.
- `lead_e2e_fallback_admin=1`.
- Admin notification is sent.
- Free/non-owner account does not see the contact payload in Advertiser Center.

### G6 - Metrics and response time

```bash
curl -s "$BASE/wp-json/nadlan/v1/healthcheck" | jq '.lead_e2e'
curl -s "$BASE/wp-json/nadlan/v1/health" | jq '.version,.lead_e2e'
```

Expected:

- Version is `1.52.0`.
- `lead_e2e.leads_7d >= 1`.
- `ack_rate` is non-null after a lead with email.
- `avg_response_minutes` is non-null after the status update.
- `by_status` includes counts for `new`, `contacted`, `won`, `lost`.

### G7 - Security

```bash
curl -s -i -X POST "$BASE/wp-json/nadlan/v1/lead/status" \
  -H "Content-Type: application/json" \
  --data "{\"lead_id\":REPLACE_LEAD_ID,\"status\":\"won\"}"
```

Expected: unauthenticated status update returns 401/403.

Rate-limit proof:

```bash
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST "$BASE/wp-json/nadlan/v1/lead/status" \
    -b "$OWNER_COOKIE" \
    -H "Content-Type: application/json" \
    -H "X-WP-Nonce: $OWNER_NONCE" \
    --data "{\"lead_id\":REPLACE_LEAD_ID,\"status\":\"contacted\"}"
done
```

Expected: request 9 or 10 returns `429` from the shared public POST limiter.

Log proof:

- `nadlan_lead_audit` contains IDs, status, timestamp, note-present flag, and note length only.
- `nadlan_event_log` contains route status and ack status only.
- Contact data remains on the private lead post, not in bounded option logs.

### G8 - Build and package

Local checks performed by Codex:

```powershell
C:\Users\pro\Documents\websites\.codex-tools\php-8.3.31-nts-Win32-vs16-x64\php.exe -l plugins\nadlan-config\inc\lead-e2e.php
C:\Users\pro\Documents\websites\.codex-tools\php-8.3.31-nts-Win32-vs16-x64\php.exe -l plugins\nadlan-config\nadlan-config.php
tar -tf plugin-dist\nadlan-config-1.52.0.zip | Select-String "nadlan-config/inc/lead-e2e.php"
tar -tf plugin-dist\nadlan-config-1.52.0.zip | Select-String "\\\\"
```

Expected:

- `php -l` clean for every changed PHP file.
- ZIP contains `nadlan-config/inc/lead-e2e.php`.
- ZIP contains no Windows backslash paths.
- `plugin-dist/nadlan-config.json` points to `nadlan-config-1.52.0.zip`.

## Rollback

Because the feature flag defaults off, the first rollback is:

```bash
wp option update nadlan_feature_lead_e2e 0
```

If the plugin itself fails after installation, use the standard plugin rollback path:

1. WP Admin -> Plugins -> deactivate NadLan Config.
2. If wp-admin is unavailable, rename `wp-content/plugins/nadlan-config` to `nadlan-config-disabled` in the host file manager.
3. Reinstall the previous ZIP from `plugin-dist/nadlan-config-1.51.2.zip`.

## Known Limits

- WhatsApp inbound and AI auto-qualification are deliberately out of scope. The seams are present: `nadlan_lead_ack` and `nadlan_lead_qualified`.
- This chunk does not create payment logic. It proves the lead loop after a card already has a paid tier.
- Status route intentionally requires a REST nonce. Application-password curl without a browser nonce should fail.
