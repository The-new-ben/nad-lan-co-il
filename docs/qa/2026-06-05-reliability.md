# v1.50.0 Reliability + Health QA

Branch: `codex/reliability`

Scope: `plugins/nadlan-config/inc/health.php`, loader/version in `plugins/nadlan-config/nadlan-config.php`, plugin manifest/ZIP.

## What changed

- Added public `GET /wp-json/nadlan/v1/health`.
- Health endpoint probes:
  - DB: cheap `SELECT 1`.
  - Morning / Green-Invoice reachability: `nadlan_gi_health_url` option, default provider host, no secret sent.
  - OpenAI reachability: `nadlan_openai_health_url` option, default `/v1/models`, no secret sent. `401` is treated as reachable because it proves the API edge responded.
- Aggregate status is `ok`, `degraded`, or `fail`. Dependency outages return HTTP 200 with `status=degraded`, not a fatal response.
- Added `nadlan_log_event( $channel, $id, $status, $meta )`:
  - stable id, status, timestamp.
  - scrubs keys that look like secrets, tokens, auth, email, phone, card data, raw bodies, names, or IPs.
  - stores in bounded `nadlan_event_log` option with autoload false.
  - alert email only after a repeated high-severity threshold.
- Added heartbeat helper for cron hooks:
  - `nadlan_gi_reconcile`
  - `nadlan_gi_dunning_tick`
  - `nadlan_ao_daily_downgrade`
- Added healthcheck `reliability` block: `health_loaded`, `deps_ok`, `last_cron_run`, `last_cron_age`, `event_log_size`.
- Added a Site Health test reminding the owner to use real server cron and heartbeat URLs.

## Owner setup checklist

1. Add a real server cron for WordPress:

```php
define( 'DISABLE_WP_CRON', true );
```

Then hit `wp-cron.php` from the server on a fixed schedule, for example every 5 minutes.

2. Point an external uptime monitor at:

```text
https://nad-lan.co.il/wp-json/nadlan/v1/health
```

Use a 30 to 60 second interval for revenue-critical monitoring.

3. Configure heartbeat URLs as options if using BetterStack or another heartbeat monitor:

```text
nadlan_heartbeat_nadlan_gi_reconcile_url
nadlan_heartbeat_nadlan_gi_dunning_tick_url
nadlan_heartbeat_nadlan_ao_daily_downgrade_url
```

4. Optional provider probe overrides:

```text
nadlan_gi_health_url
nadlan_openai_health_url
```

Do not put secrets in these URLs unless the monitor vendor explicitly requires a tokenized heartbeat URL. The logger redacts URL-like secret keys, but secrets should still stay out of code.

## SLO

Target: `99.9%` availability for revenue-critical public journeys.

Alerting model:

- Page on symptoms users feel, not every low-level dependency cause.
- Use multi-window multi-burn-rate alerts when external monitoring supports it.
- For this low-traffic site, aggregate to user impact: homepage/catalog reachable, checkout path reachable, lead path reachable, health endpoint degraded/fail.
- Use ticket-level alerts for slow burn, owner page/email only after repeated high-severity events to avoid alert fatigue.

## Manual QA

### Health endpoint

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/health?cb=$(date +%s)" | jq .
```

Expected:

- HTTP code is `200`.
- `.version` is `1.50.0`.
- `.status` is `ok`, `degraded`, or `fail`.
- `.dependencies.db.status` is `ok` on a healthy site.
- If OpenAI or Morning is down, the response is still JSON with `status=degraded`.

### Healthcheck

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=$(date +%s)" | jq '.version,.reliability'
```

Expected:

- `.version` is `1.50.0`.
- `.reliability.health_loaded` is `true`.
- `.reliability.deps_ok` is boolean.
- `.reliability.last_cron_run` is numeric or `0`.

### Log scrub proof

In a PHP sandbox:

```php
nadlan_log_event( 'test', 'pii', 'fail', array(
  'email' => 'person@example.com',
  'phone' => '0500000000',
  'secret' => 'abc',
  'safe_count' => 3,
) );
var_export( end( get_option( 'nadlan_event_log', array() ) ) );
```

Expected:

- `email`, `phone`, and `secret` values are `[redacted]`.
- `safe_count` remains `3`.

### Package proof

```bash
tar -tf plugin-dist/nadlan-config-1.50.0.zip | head
tar -xOf plugin-dist/nadlan-config-1.50.0.zip nadlan-config/inc/health.php \
  | grep -E "nadlan_log_event|/health|nadlan_reliability_ping_heartbeat|site_status_tests"
tar -xOf plugin-dist/nadlan-config-1.50.0.zip nadlan-config/nadlan-config.php \
  | grep -E "Version: 1.50.0|health|'version'             => '1.50.0'"
```

## 10-cycle checklist

- C1 Endpoint: `GET /nadlan/v1/health` is public and returns structured JSON.
- C2 DB: cheap `SELECT 1` probe is present.
- C3 Dependencies: Morning and OpenAI probes use safe timeouts, `sslverify=true`, and no secrets.
- C4 Edge: dependency down returns degraded JSON, not a 500.
- C5 Logging: `nadlan_log_event()` stores stable id, status, timestamp, and scrubbed metadata only.
- C6 Retention: event log is bounded by count and retention days.
- C7 Alerts: high-severity owner email is thresholded and transient-deduped.
- C8 Cron: billing cron heartbeat helper records last run and optionally pings heartbeat URLs.
- C9 Site Health: owner sees a cron reliability note.
- C10 Ops doc: SLO target, external monitor, heartbeat, and server-cron steps are documented.

## Local checks

- `git diff --check`: run before PR.
- PHP-segment structural scan: run before PR.
- `php -l`: BLOCKED locally because `php` is not installed on this machine. Claude must run PHP lint in the WordPress/PHP sandbox before deploy.

## Caveats for Claude

- Current `main` may not include GAP3 recurring hooks yet. The heartbeat actions are harmless until those hooks fire.
- Green-Invoice and OpenAI probes only confirm reachability, not paid account entitlement.
- The healthcheck calls the same probe helper, so repeated monitoring should prefer `/health` and keep `/healthcheck` for deploy/version checks.
