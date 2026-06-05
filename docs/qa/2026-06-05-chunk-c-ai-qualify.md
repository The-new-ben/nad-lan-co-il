# Chunk C AI Lead Auto-Qualify QA Gate - v1.53.0

## Scope

Branch: `codex/chunk-c-ai-qualify`

This chunk builds on Chunk B and ships dark behind:

- `nadlan_feature_lead_e2e`
- `nadlan_feature_lead_ai_qualify`

Default behavior is OFF. With either flag off, or without an OpenAI key, no lead AI call should run.

## Files

- `plugins/nadlan-config/inc/lead-ai-qualify.php`
- `plugins/nadlan-config/inc/lead-e2e.php`
- `plugins/nadlan-config/inc/health.php`
- `plugins/nadlan-config/nadlan-config.php`
- `plugin-dist/nadlan-config.json`
- `plugin-dist/nadlan-config-1.53.0.zip`

## C1 Reuse Chunk B

The module listens to the new passive action:

```php
do_action( 'nadlan_lead_e2e_captured', (int) $lead_id, (int) $card_id, $fields, $route );
```

It does not register a second `/nadlan/v1/lead` endpoint and does not replace Chunk B capture, routing, ack, inbox, status, or audit.

## C2 Dark Flag

Expected defaults:

```bash
wp option get nadlan_feature_lead_ai_qualify
# empty or 0
```

Flag off result:

- no `_nadlan_lead_ai_qualify_guard`
- no `lead_ai_qualified_at`
- no `lead_score`
- no `lead_ai_response_sent_at`

## C3 No-Key Safety

With `nadlan_feature_lead_ai_qualify=1` but no OpenAI key:

```bash
wp option delete nadlan_ai_openai_key
wp option update nadlan_feature_lead_ai_qualify 1 --autoload=no
```

Submit a Chunk B lead. Expected:

- lead capture still succeeds
- visitor Chunk B ack still sends
- no AI meta is written
- no OpenAI call is attempted

## C4 Paid Card Happy Path

Prerequisites:

- `nadlan_feature_lead_e2e=1`
- `nadlan_feature_lead_ai_qualify=1`
- `nadlan_ai_provider=openai`
- OpenAI key present
- card has paid tier and owner

Submit:

```bash
curl -sS -X POST "$BASE/wp-json/nadlan/v1/lead" \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"בדיקת AI",
    "email":"qa@example.test",
    "phone":"0501234567",
    "goal":"מידע על פרויקט",
    "budget":"4 מיליון שח",
    "timeline":"בחודש הקרוב",
    "city":"תל אביב",
    "message":"אני רוצה להבין זמינות וסוגי דירות. התקציב בערך 4 מיליון שח וזה רלוונטי לחודש הקרוב.",
    "source":"qa-chunk-c",
    "card_id":4464
  }'
```

Expected meta:

```bash
wp post meta get <lead_id> lead_ai_qualified_at
wp post meta get <lead_id> lead_score
wp post meta get <lead_id> lead_ai_tier
wp post meta get <lead_id> lead_ai_budget
wp post meta get <lead_id> lead_ai_intent
wp post meta get <lead_id> lead_ai_timeline
wp post meta get <lead_id> lead_ai_location
wp post meta get <lead_id> lead_ai_grounded
wp post meta get <lead_id> lead_ai_sources
wp post meta get <lead_id> lead_ai_response_sent_at
```

Expected:

- score 0 to 100
- tier `hot`, `warm`, or `cold`
- `lead_ai_sources` has source ids when response sent
- no auto-close, `lead_status` remains `new` unless a human changes it

## C5 Idempotency

Run the same lead submission twice inside the Chunk B idempotency window.

Expected:

- same lead id returned by Chunk B
- `_nadlan_lead_ai_qualify_guard` exists once
- `lead_ai_response_sent_at` exists once
- no second `lead_ai_qualified_at` update caused by duplicate submit

## C6 Grounding And Handoff

Submit an unsupported/off-topic message:

```bash
curl -sS -X POST "$BASE/wp-json/nadlan/v1/lead" \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"בדיקת מקור",
    "email":"qa@example.test",
    "phone":"0501234567",
    "goal":"שאלה לא קשורה",
    "message":"תן לי מחיר מובטח למטבע דיגיטלי ותנאי הנחה שאין באתר.",
    "source":"qa-chunk-c",
    "card_id":4464
  }'
```

Expected:

- `lead_ai_handoff=1`
- `lead_ai_auto_response_status=handoff`
- no `lead_ai_response_sent_at`
- `lead_ai_answer` abstains or says there is no supported source
- no invented price, discount, availability, or terms

## C7 Human Handoff

Submit:

```json
{
  "message": "אני רוצה שנציג אנושי יחזור אלי בטלפון."
}
```

Expected:

- no AI provider call
- `lead_ai_handoff=1`
- `lead_ai_handoff_reason=visitor_requested_human`
- `nadlan_lead_ai_handoff` seam fires
- no auto-response loop

## C8 Cost Cap

Set a tiny per-lead cap:

```bash
wp option update nadlan_lead_ai_token_cap_per_lead 800 --autoload=no
```

Submit a long message that forces the estimate over 800.

Expected:

- no provider call
- `lead_ai_status=cost_blocked`
- `lead_ai_error=lead_ai_token_cap`
- `lead_ai_handoff=1`

The module also pre-checks existing global and per-IP daily token counters before calling `nadlan_ai_chat`, and `nadlan_ai_chat` still performs the canonical guard immediately before the provider call.

## C9 Health And Dashboard

Healthcheck:

```bash
curl -sS "$BASE/wp-json/nadlan/v1/healthcheck" | jq '.version,.lead_ai'
curl -sS "$BASE/wp-json/nadlan/v1/health" | jq '.version,.lead_ai'
```

Expected:

- version `1.53.0`
- `lead_ai.qualified_rate`
- `lead_ai.avg_score`
- `lead_ai.hot`
- `lead_ai.warm`
- `lead_ai.cold`
- `lead_ai.per_lead_cap`

Admin dashboard:

- Dashboard -> NadLan Ops includes Lead AI panel
- Settings -> NadLan Lead AI includes dark flag, per-lead token cap, response subject

## C10 Package Gate

```powershell
$php='C:\Users\pro\Documents\websites\.codex-tools\php-8.3.31-nts-Win32-vs16-x64\php.exe'
& $php -l plugins\nadlan-config\inc\lead-ai-qualify.php
& $php -l plugins\nadlan-config\inc\lead-e2e.php
& $php -l plugins\nadlan-config\inc\health.php
& $php -l plugins\nadlan-config\nadlan-config.php
tar -tf plugin-dist\nadlan-config-1.53.0.zip | Select-String "nadlan-config/inc/lead-ai-qualify.php"
(tar -tf plugin-dist\nadlan-config-1.53.0.zip | Select-String "\\\\" | Measure-Object).Count
```

Expected:

- all PHP lint clean
- ZIP contains `nadlan-config/inc/lead-ai-qualify.php`
- backslash count `0`
- manifest points to `nadlan-config-1.53.0.zip`

## Acceptance Mapping

- G1: flag OFF or no key, no AI meta and no provider call.
- G2: flag ON plus OpenAI key, qualified, scored, grounded response sent, routed by score.
- G3: `_nadlan_lead_ai_qualify_guard` prevents double qualification and double response.
- G4: unsupported content is handoff/abstain and sends no invented terms.
- G5: human request marks handoff and stops auto-reply.
- G6: per-lead cap plus global/IP cap pre-checks before `nadlan_ai_chat`.
- G7: no new public endpoint, sanitized fields, no secrets or contact payload in `nadlan_lead_ai_log`.
- G8: PHP lint clean, root-folder ZIP, `1.53.0` aligned, health/dashboard metrics present.

## Rollback

Keep both flags off:

```bash
wp option update nadlan_feature_lead_ai_qualify 0 --autoload=no
wp option update nadlan_feature_lead_e2e 0 --autoload=no
```

If an install needs full rollback, reinstall the previous Chunk B package and leave the AI flag off.
