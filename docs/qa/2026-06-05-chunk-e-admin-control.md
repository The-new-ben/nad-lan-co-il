# Chunk E QA - operator admin control plane

Branch: `codex/chunk-e-admin-control`
Plugin version: `1.55.0`
Feature flag: `nadlan_feature_admin_control`, default `0`

## Scope

Chunk E ships a dark operator control plane for listing/card operations:

- validated editing of `city`, `lat`, `lng`, `references`, and `priority_weight`
- query-time placement overrides: `is_pinned`, `boost_multiplier`, `reserved_slot`, `promo_until`
- bounded admin audit log in `nadlan_admin_audit`
- safe time-boxed impersonation with read-only default
- `nadlan_manage_clients` capability and `nadlan_operator` role
- admin-control health metrics

The feature is inert while the flag is off.

## G1 - flag off

Expected:

- `nadlan_feature_admin_control=0`
- no `NadLan Ops -> בקרת לקוחות` submenu
- no `/nadlan/v1/admin-control/*` routes registered
- `nadlan_operator` role absent
- administrator does not receive `nadlan_manage_clients`

Manual checks:

```bash
wp option update nadlan_feature_admin_control 0
wp eval '$role=get_role("administrator"); var_dump($role ? $role->has_cap("nadlan_manage_clients") : null);'
curl -i https://example.test/wp-json/nadlan/v1/admin-control/cards
```

Pass condition:

- curl returns 404 or route-not-found
- custom cap is not present

## G2 - validated card edit

Enable:

```bash
wp option update nadlan_feature_admin_control 1
wp eval 'do_action("init"); echo get_role("administrator")->has_cap("nadlan_manage_clients") ? "cap\n" : "missing\n";'
```

REST write with a browser nonce:

```bash
curl -i -X POST "https://example.test/wp-json/nadlan/v1/admin-control/card/4464" \
  -H "Content-Type: application/json" \
  -H "X-WP-Nonce: $NONCE" \
  --cookie "$COOKIE" \
  --data '{"city":"תל אביב-יפו","lat":95,"lng":-190,"priority_weight":101,"references":[{"label":"מקור","url":"https://nad-lan.co.il/"}]}'
```

Pass condition:

- `lat` clamps to `90`
- `lng` clamps to `-180`
- `priority_weight` clamps to `100`
- `references[0].url` is sanitized through `esc_url_raw`
- each changed field writes an audit row with old and new values

## G3 - placement overrides compose

Set:

```bash
wp post meta update 4464 is_pinned 1
wp post meta update 4464 reserved_slot 1
wp post meta update 4464 boost_multiplier 2.5
wp post meta update 4464 priority_weight 80
wp post meta update 4464 promo_until "$(($(date +%s)+86400))"
```

Expected SQL composition:

- paid placement remains priority `20` in `directory.php`
- auction remains priority `25` in `placement-auction.php`
- admin-control prefixes at priority `27`
- geo remains priority `30`

Pass condition:

- final `ORDER BY` starts with reserved/pinned/weight expressions
- then keeps auction winner
- then keeps paid tier `premier > pro > free`
- no organic score/meta is mutated

## G4 - audit

Audit option:

```bash
wp option get nadlan_admin_audit --format=json | jq '.[0:5]'
```

Pass condition:

- every write has `actor`, `action`, `card_id`, `field`, `old`, `new`, `ts`
- log is capped at 2000 rows
- rows do not contain full card rows or secrets

## G5 - impersonation

Start:

```bash
curl -i -X POST "https://example.test/wp-json/nadlan/v1/admin-control/impersonate/start" \
  -H "X-WP-Nonce: $NONCE" \
  --cookie "$COOKIE" \
  --data "user_id=$TARGET_USER_ID"
```

Pass condition:

- only `manage_options` can start
- session expires within 30 minutes
- admin and frontend banners render
- advertiser-center and `/studio/mine` read as the target user
- writes remain blocked until `/impersonate/write-toggle`
- audit rows include `Impersonated By <operator_id>`

## G6 - RBAC

```bash
wp role list | grep nadlan_operator
wp cap list nadlan_operator | grep nadlan_manage_clients
wp cap list nadlan_operator | grep manage_options && exit 1 || echo "no manage_options"
wp cap list administrator | grep nadlan_manage_clients
```

Pass condition:

- `nadlan_operator` has `nadlan_manage_clients`
- `nadlan_operator` does not have `manage_options`
- administrator has `nadlan_manage_clients` while flag is on

## G7 - security

Checks:

- POST without `X-WP-Nonce` returns 403
- non-owner/non-admin cannot write a card they do not have `edit_post` on
- operator without `manage_options` cannot start impersonation
- URLs pass through `esc_url_raw`
- lat/lng/weight are clamped
- read-only impersonation blocks mutating `/nadlan/v1/*` routes except end/toggle

## G8 - package and health

Expected:

```bash
tar -tf plugin-dist/nadlan-config-1.55.0.zip | grep '\\' && exit 1 || echo "forward-slash paths"
tar -xOf plugin-dist/nadlan-config-1.55.0.zip nadlan-config/inc/admin-control.php | grep -c "nadlan_feature_admin_control"
curl -s https://example.test/wp-json/nadlan/v1/healthcheck | jq '.version,.admin_control'
curl -s https://example.test/wp-json/nadlan/v1/health | jq '.version,.admin_control'
```

Pass condition:

- ZIP entries use forward slashes
- ZIP contains `nadlan-config/inc/admin-control.php`
- header, healthcheck, `/health`, manifest, and ZIP are all `1.55.0`
- `admin_control` health block exposes enabled, audit count, operator role, overrides, impersonations, and cron state

## Local Codex environment note

This Windows shell does not have `php`, WSL, or Docker available, so Codex cannot run `php -l` locally. Claude must run the PHP lint gate before deploy. Codex still runs repository diff, manifest, and ZIP-content gates on this branch.
