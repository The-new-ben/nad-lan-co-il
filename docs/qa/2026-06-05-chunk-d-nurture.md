# Chunk D Automated Lead Nurture QA Gate - v1.54.0

Branch: `codex/chunk-d-nurture`  
Base: `codex/chunk-c-ai-qualify`  
Module: `plugins/nadlan-config/inc/lead-nurture.php`

## Scope

Chunk D adds an email-only follow-up cadence for Chunk B E2E leads, using Chunk C scoring when present. It ships dark behind `nadlan_feature_lead_nurture`, default `0`.

The flow reuses:

- `nadlan_lead_e2e_captured` to schedule only after a real E2E capture.
- `lead_status` from Chunk B for stop conditions.
- `lead_score` / `lead_ai_tier` from Chunk C for hot/warm/cold cadence.
- `nadlan_lead_deliver` for the email channel.
- `nadlan_lead_ai_handoff` for immediate stop.

Out of scope stays out: no SMS, no WhatsApp, no auto-close, no new deal logic.

## Implementation Summary

- New dark flag: `nadlan_feature_lead_nurture`, default off.
- New admin page: Settings -> NadLan Lead Nurture.
- New scheduled hook: `nadlan_lead_nurture_send_touch`.
- Hourly safety tick: `nadlan_lead_nurture_tick`.
- New public unsubscribe route: `GET /wp-json/nadlan/v1/nurture/unsubscribe?lead=&token=`.
- Signed-token unsubscribe (`secret.hmac` using WordPress salts), rate-limited 8/min/IP.
- Bounded audit option: `nadlan_lead_nurture_log`, capped at 1500 rows and no message body, email, phone, or name.
- Health metrics: `lead_nurture.scheduled`, `sent`, `stopped_by_reason`.
- Ops dashboard panel: scheduled, sent, active, stopped, stopped-by-reason.

## C1-C10 Build Cycles

- C1 capture seam: schedule starts from `nadlan_lead_e2e_captured` only, priority 40, after Chunk C priority 20.
- C2 dark launch: `nadlan_lead_nurture_enabled()` requires nurture flag ON and E2E ON.
- C3 cadence: warm/hot schedule day 1, 3, 7, 14, then monthly; cold schedules lighter day 7, 14, monthly.
- C4 idempotency: send guard uses unique post meta `_nadlan_lead_nurture_sent_<step>`.
- C5 stop conditions: status contacted/won/lost, reply meta/action, AI handoff, unsubscribe.
- C6 consent: every body gets `{{unsubscribe}}`; code appends the URL if an admin removes the token.
- C7 security: unsubscribe is token-authenticated, sanitized, and rate-limited; no secrets or PII in logs.
- C8 metrics: healthcheck, `/health`, metrics snapshot, and Ops panel expose nurture status.
- C9 packaging: module added to loader, version bumped to 1.54.0, manifest and ZIP rebuilt.
- C10 handoff: this doc plus PR body tell Claude exactly how to execute G1-G8.

## Manual Gate

Set variables:

```bash
SITE="https://nad-lan.co.il"
AUTH="user:app-password"
CARD_ID=4464
NONCE="<wp_rest_nonce_when_testing_browser_session>"
```

### G1 - Flag OFF means no nurture scheduling

```bash
curl -u "$AUTH" -X POST "$SITE/wp-json/wp/v2/settings" \
  -H "Content-Type: application/json" \
  -d '{"nadlan_feature_lead_e2e":"1","nadlan_feature_lead_nurture":"0"}'

curl -s -X POST "$SITE/wp-json/nadlan/v1/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"בדיקת נרטור כבוי","phone":"0501111111","email":"off@example.test","message":"מבקש מידע","card_id":4464}' \
  | tee /tmp/chunkd-off.json
```

Expected:

- Lead is created by Chunk B.
- `lead_nurture_state` is empty.
- `lead_nurture_scheduled_steps` is empty.
- No `nadlan_lead_nurture_log` scheduled row for this lead.

WP-CLI proof:

```bash
LEAD_ID=$(jq -r '.lead_id' /tmp/chunkd-off.json)
wp post meta get "$LEAD_ID" lead_nurture_state
wp post meta get "$LEAD_ID" lead_nurture_scheduled_steps
```

### G2 - Flag ON schedules day 1/3/7/14 and due touches send

```bash
wp option update nadlan_feature_lead_e2e 1
wp option update nadlan_feature_lead_nurture 1

curl -s -X POST "$SITE/wp-json/nadlan/v1/lead" \
  -H "Content-Type: application/json" \
  -d '{"name":"בדיקת נרטור פעיל","phone":"0502222222","email":"on@example.test","message":"מבקש מידע בחודש הקרוב","card_id":4464}' \
  | tee /tmp/chunkd-on.json

LEAD_ID=$(jq -r '.lead_id' /tmp/chunkd-on.json)
wp post meta get "$LEAD_ID" lead_nurture_state
wp post meta get "$LEAD_ID" lead_nurture_scheduled_steps --format=json
```

Expected for warm/default lead:

- `lead_nurture_state=active`.
- scheduled steps include `day1`, `day3`, `day7`, `day14`, `monthly_1`.

Force a due send:

```bash
wp eval "do_action('nadlan_lead_nurture_send_touch', $LEAD_ID, 'day1');"
wp post meta get "$LEAD_ID" _nadlan_lead_nurture_sent_day1
wp post meta get "$LEAD_ID" lead_nurture_last_step
```

Expected:

- `_nadlan_lead_nurture_sent_day1` exists.
- `lead_nurture_last_step=day1`.
- audit log contains one `sent` row for `day1`.

### G3 - Idempotency, double cron does not double-send

```bash
wp eval "do_action('nadlan_lead_nurture_send_touch', $LEAD_ID, 'day1'); do_action('nadlan_lead_nurture_send_touch', $LEAD_ID, 'day1');"
wp eval '$log=get_option("nadlan_lead_nurture_log",[]); $n=0; foreach($log as $r){ if(($r["lead_id"]??0)=='"$LEAD_ID"' && ($r["step"]??"")==="day1" && ($r["status"]??"")==="sent") $n++; } echo $n;'
```

Expected: `1`. Duplicate fires may log `skipped: duplicate`, but never another `sent`.

### G4 - Stop conditions

Status stop:

```bash
wp post meta update "$LEAD_ID" lead_status contacted
wp post meta get "$LEAD_ID" lead_nurture_state
wp post meta get "$LEAD_ID" lead_nurture_stop_reason
```

Expected: `stopped`, `status_contacted`.

Reply stop:

```bash
NEW_LEAD=<active_lead_id>
wp post meta update "$NEW_LEAD" lead_replied_at "$(date +%s)"
wp post meta get "$NEW_LEAD" lead_nurture_stop_reason
```

Expected: `reply`.

AI handoff stop:

```bash
AI_LEAD=<active_lead_id>
wp post meta update "$AI_LEAD" lead_ai_handoff 1
wp post meta get "$AI_LEAD" lead_nurture_stop_reason
```

Expected: `ai_handoff`.

Unsubscribe stop is covered in G6.

### G5 - Score-gated cadence

Hot:

```bash
HOT=<lead_id>
wp post meta update "$HOT" lead_score 85
wp post meta update "$HOT" lead_ai_tier hot
wp eval "nadlan_lead_nurture_schedule_for_lead($HOT, 4464, [], []);"
wp post meta get "$HOT" lead_nurture_scheduled_steps --format=json
```

Expected: includes `day1`, `day3`, `day7`, `day14`, `monthly_1`.

Cold:

```bash
COLD=<lead_id>
wp post meta update "$COLD" lead_score 20
wp post meta update "$COLD" lead_ai_tier cold
wp eval "nadlan_lead_nurture_schedule_for_lead($COLD, 4464, [], []);"
wp post meta get "$COLD" lead_nurture_scheduled_steps --format=json
```

Expected: lighter cadence, `day7`, `day14`, `monthly_1`; no `day1` or `day3`.

### G6 - Unsubscribe link

```bash
UNSUB=<active_lead_id>
URL=$(wp eval "echo nadlan_lead_nurture_unsubscribe_url($UNSUB);")
curl -i "$URL"
wp post meta get "$UNSUB" lead_nurture_state
wp post meta get "$UNSUB" lead_nurture_stop_reason
wp post meta get "$UNSUB" lead_nurture_unsubscribed_at
```

Expected:

- HTTP 200.
- `lead_nurture_state=stopped`.
- `lead_nurture_stop_reason=unsubscribe`.
- `lead_nurture_unsubscribed_at` exists.
- Later scheduling attempts do not re-activate the lead.

### G7 - Security

Bad token:

```bash
curl -i "$SITE/wp-json/nadlan/v1/nurture/unsubscribe?lead=$UNSUB&token=bad"
```

Expected: HTTP 403.

Rate limit:

```bash
for i in $(seq 1 10); do curl -s -o /dev/null -w "%{http_code}\n" "$SITE/wp-json/nadlan/v1/nurture/unsubscribe?lead=$UNSUB&token=bad"; done
```

Expected: at least one HTTP 429 after repeated attempts.

Log safety:

```bash
wp option get nadlan_lead_nurture_log --format=json | grep -E "email|phone|message|body|token|name" && echo "FAIL" || echo "PASS"
```

Expected: `PASS`.

### G8 - Packaging and health

```powershell
$php='C:\Users\pro\Documents\websites\.codex-tools\php-8.3.31-nts-Win32-vs16-x64\php.exe'
Get-ChildItem plugins\nadlan-config -Recurse -Filter *.php | ForEach-Object { & $php -l $_.FullName }

tar -tf plugin-dist\nadlan-config-1.54.0.zip | Select-String "^nadlan-config/inc/lead-nurture.php$"
(tar -tf plugin-dist\nadlan-config-1.54.0.zip | Select-String "\\").Count
tar -xOf plugin-dist\nadlan-config-1.54.0.zip nadlan-config/inc/lead-nurture.php | Select-String "nadlan_feature_lead_nurture|nadlan_lead_nurture_send_touch|nurture/unsubscribe"
```

Expected:

- PHP lint clean.
- ZIP contains `nadlan-config/inc/lead-nurture.php`.
- Backslash count is `0`.
- Header, `/healthcheck`, `/health`, and manifest show `1.54.0`.

Health proof after deploy:

```bash
curl -s "$SITE/wp-json/nadlan/v1/healthcheck" | jq '.version,.lead_nurture'
curl -s "$SITE/wp-json/nadlan/v1/health" | jq '.version,.lead_nurture'
```

Expected:

- version `1.54.0`
- `lead_nurture.scheduled`, `lead_nurture.sent`, `lead_nurture.stopped_by_reason`.

## Notes for Claude

- The unsubscribe route is public by design because email recipients are not logged in. Authorization is the per-lead signed token, plus 8/min/IP rate limiting.
- Reply stop is represented by either `do_action('nadlan_lead_replied',$lead_id)` or setting `lead_replied_at`, `lead_reply_received_at`, or `lead_has_reply`. A later inbound email or WhatsApp chunk should write one of those.
- When the feature flag is off, status and AI-handoff hooks do not write nurture metadata unless the lead already has nurture state. This protects G1.
