# v1.51.0 Owner Safety Verification

Scope: consolidated `nadlan-config` v1.51.0 on `origin/main`, including `plugin-dist/nadlan-config-1.51.0.zip`.

Verdict: no lockout or white-screen blocker found in the code path I inspected. Do not overread that as "fully autonomous" or "everything is polished". It means the owner should be able to update, keep wp-admin access, and roll back if needed.

Critical non-collapse findings to fix next:

1. Major functional gap: the OpenAI adapter exists in `inc/ai-provider.php`, but the visible concierge route and Settings page are still Anthropic-first in `inc/ai-concierge.php`. Because `ai-concierge.php` loads before `ai-provider.php`, it defines `nadlan_ai_key()` first, and the provider module cannot replace it. Result: a non-developer cannot turn on the live concierge with an OpenAI key from Settings -> NadLan AI. Fix direction: load `ai-provider` before `ai-concierge`, refactor `/nadlan/v1/concierge` and Studio AI copy to call `nadlan_ai_chat()`, and add OpenAI provider/key/cap fields to the Settings UI.
2. Minor monitoring bug: `inc/health.php` returns `"version":"1.50.0"` on `/wp-json/nadlan/v1/health`, while the canonical `/wp-json/nadlan/v1/healthcheck` returns `1.51.0`. Fix direction: read the plugin version from one shared source or bump the literal.
3. Cleanliness gap: the role migration does not skip administrators. It uses additive `WP_User::add_role()`, so it should not downgrade the owner or remove admin access, but an admin can gain `nadlan_advertiser` or `nadlan_buyer`. Fix direction: skip users with `manage_options` during migration unless the owner explicitly wants extra roles on admins.

## Plugin Mechanism Learned And Verified

| Mechanism | Evidence | Meaning |
|---|---|---|
| Plugin header version | `plugins/nadlan-config/nadlan-config.php:5` is `Version: 1.51.0`. | WordPress can see a higher version after the manifest updates. |
| PHP floor | `plugins/nadlan-config/nadlan-config.php:8` declares `Requires PHP: 7.4`. | New code must stay PHP 7.4 compatible. |
| Module loader | `plugins/nadlan-config/nadlan-config.php:25-29` loads module names from one `foreach`, checks `file_exists()`, then `require_once`s. | A new `inc/*.php` only runs if listed there; missing files are skipped, not fatal. |
| Consolidated modules in loader | `geo-search`, `roles`, `greeninvoice-recurring`, `ai-provider`, `placement-auction`, `business-metrics`, `health`, `final-hardening` all appear in `nadlan-config.php:25`. | v1.51.0 is not just the final-hardening branch; it is the consolidated branch. |
| Update mechanism | `nadlan_config_boot_updater()` at `nadlan-config.php:390-407` loads Plugin Update Checker only if the library exists and points it to `plugin-dist/nadlan-config.json`. | Runtime update path is GitHub manifest -> WP update screen -> owner clicks Update. |
| ZIP proof | `plugin-dist/nadlan-config-1.51.0.zip` contains the consolidated modules and no backslash paths. | The package should unzip correctly as `nadlan-config/`. |

## Cycle 1 - Lockout Safety

| Risk | Result | Evidence | Notes / Fix Direction |
|---|---|---|---|
| Administrator core caps stripped during setup | PASS | `roles.php:105-109` only calls `$admin->add_cap()` for custom listing caps. No `remove_cap()` appears in setup. | No evidence of `manage_options`, `read`, or `edit_posts` removal on update. |
| Administrator role removed | PASS | `roles.php:93` removes only `nadlan_advertiser`; `roles.php:133-134` removes custom roles only inside uninstall. | No `remove_role('administrator')`. |
| Owner/admin downgraded by migration | PASS for lockout, FAIL for "non-admin only" cleanliness | `roles.php:80-83` loops all users. `roles.php:73` uses `$user->add_role(...)`, not `set_role()`. | Additive role assignment should not remove admin. It does not skip admins, so add a future guard for users with `manage_options`. |
| `map_meta_cap` denies admin editing | PASS | `claim.php:190-214` returns `$caps` unchanged unless it grants verified owner access by returning `array('read')`. | It only grants. It does not inject a denial. Administrators still satisfy normal primitive caps. |
| Public POST rate limiter can throttle wp-admin/wp-login | PASS | `final-hardening.php:33-45` lists only specific REST route regexes. `final-hardening.php:69-79` runs only for REST `POST`, checks `get_route()`, and returns unchanged if not allowlisted. | No `/wp-admin`, `/wp-login.php`, or general admin REST route in allowlist. |
| Uninstall cleanup fires on update/deactivate | PASS | `roles.php:139-141` registers activation, uninstall, and admin-init setup separately. `register_uninstall_hook` only fires on uninstall, not update/deactivation. | Uninstall removes custom roles/caps by design. |
| Missing OpenAI key kills site/admin | PASS | `ai-provider.php:238-240` returns `WP_Error('nokey')`; `ai-concierge.php:151-153` returns a 503 JSON response if `nadlan_ai_enabled()` is false. | No fatal. Functional issue: OpenAI is not wired into the visible concierge route yet. |
| Missing Green Invoice IPN secret kills site/admin | PASS | `greeninvoice-recurring.php:300-305` returns 503 `not_configured` for `/gi-ipn` when secret is empty. | No fatal. Recurring billing simply does not process until configured. |

## Cycle 2 - Fatal / White-Screen Safety

| Check | Result | Evidence |
|---|---|---|
| New module ABSPATH guards | PASS | `geo-search.php`, `roles.php`, `greeninvoice-recurring.php`, `ai-provider.php`, `placement-auction.php`, `business-metrics.php`, `health.php`, and `final-hardening.php` all have `if ( ! defined( 'ABSPATH' ) ) { exit; }` in the first 10 lines. |
| New functions guarded | PASS | Static scan found 132 functions across the eight consolidated modules and no unguarded named function declarations. |
| Duplicate function collision | PASS | `greeninvoice-recurring.php:8-18` defines `nadlan_revenue_event()` and `nadlan_deal_closed()` behind `function_exists()`; `placement-auction.php:8-12` also guards `nadlan_revenue_event()`. |
| Missing require fatal | PASS | Loader uses `file_exists()` before `require_once` at `nadlan-config.php:26-29`; updater library also checks `file_exists()` and `class_exists()` at `nadlan-config.php:390-395`. |
| PHP 7.4 static compatibility | PASS by static grep, not by local lint | I found no `match`, `enum`, `readonly`, nullsafe `?->`, `str_contains`, `str_starts_with`, or `str_ends_with` usage in the consolidated modules. Local `php -l` is blocked because PHP is not installed on this machine. Claude already executed lint during PR review; rerun lint before live deploy anyway. |
| REST routes registered under `rest_api_init` | PASS | Examples: `/near` at `geo-search.php:221-287`, `/gi-ipn` at `greeninvoice-recurring.php:321-327`, `/auction/bid` at `placement-auction.php:284-291`, `/health` at `health.php:202-208`. |
| Cron scheduling idempotent | PASS for new modules | `greeninvoice-recurring.php:390-400` uses `wp_next_scheduled()` before scheduling dunning/reconcile; `business-metrics.php:453-458` uses `wp_next_scheduled()` before daily digest. |

## Cycle 3 - Post-Update Smoke Test Plan

Run these immediately after the owner clicks Update.

| Order | Test | Expected | Failure Symptom | Immediate Rollback |
|---|---|---|---|---|
| 1 | Open `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=<timestamp>` | JSON contains `"version":"1.51.0"` plus `gi`, `ai`, `roles`, `business`, `hardening`, `auction`, and `geo` blocks. | Version is old, route 404, or JSON is invalid. | If old version: update did not apply. If 500: deactivate plugin or restore prior ZIP. |
| 2 | Open `/wp-admin` while logged in as owner | Normal dashboard loads. This triggers one-time `admin_init` role setup. | White screen, fatal, redirect loop, or owner cannot access dashboard. | Rename `wp-content/plugins/nadlan-config` to `nadlan-config-disabled` via hosting file manager/SFTP. |
| 3 | Logged-out browser: `/`, `/projects/`, `/professionals/` | Pages render, no white screen, footer/header present. | 500, blank page, broken header/footer. | Deactivate plugin in wp-admin if accessible; otherwise folder rename rollback. |
| 4 | `GET /wp-json/nadlan/v1/near?lat=32.0853&lng=34.7818&radius_km=25&type=project` | JSON with `ok:true`, `count`, and `results` array. Empty array is acceptable if no nearby cards have coords. | 500 or PHP error. 422 means the URL was malformed. | Do not rely on geo UI; rollback only if it causes broader errors. |
| 5 | `POST /wp-json/nadlan/v1/gi-ipn` with no signature | 503 `not_configured` if no secret, or 401 `bad_signature` if a secret exists. It must not be 500. | 500 fatal. | Deactivate plugin or restore prior ZIP; recurring IPN is unsafe until fixed. |
| 6 | WP Admin -> Settings -> NadLan AI and Settings -> NadLan GI | Both forms render. Secret fields are blank; text says configured/not configured. | Fatal/white screen in settings page. | Deactivate plugin if settings page blocks admin. |
| 7 | Optional monitoring: `/wp-json/nadlan/v1/health` | Should return JSON status. Known caveat: current code reports `"version":"1.50.0"`. | 500. | Monitoring should use `/healthcheck` for version until fixed. |

## Cycle 4 - Data And Reversibility

v1.51.0 writes options and meta but does not bulk delete live content on update.

Options written:

- Roles: `nadlan_roles_version`.
- Green Invoice: `nadlan_gi_charge_log`, `nadlan_gi_sig_scheme`, `nadlan_gi_ipn_secret`, `nadlan_gi_api_key`, `nadlan_gi_cycle_days_pro`, `nadlan_gi_cycle_days_premier`, `nadlan_gi_link_pro`, `nadlan_gi_link_premier`, `nadlan_gi_reconcile_url`.
- AI: `nadlan_ai_tokens_today_YYYYMMDD`, `nadlan_ai_usage_YYYYMM`, `nadlan_ai_total_tokens`, `nadlan_ai_total_msgs`, `nadlan_ai_last_error`, `nadlan_ai_quality_log`.
- Auction: `nadlan_auction_enabled`, `nadlan_auction_quality_floor`, `nadlan_auction_slots_default`, `nadlan_auction_reserve`, `nadlan_auction_increment`, `nadlan_auction_enabled_categories`, `nadlan_auction_slot_overrides`.
- Metrics/reliability: `nadlan_metrics_snapshot_YYYYMMDD`, `nadlan_metrics_mrr_start_YYYYMM`, `nadlan_event_log`, `nadlan_reliability_last_cron_*`, heartbeat URL options if the owner sets them.
- Public rate limits/transients: `nadlan_postrl_*`, `nadlan_geo_near_*`, `nadlan_ai_daily_*`, auction rank transients.

Post meta written:

- Recurring billing: `paid_tier`, `campaign_end`, `dunning_state`, `dunning_since`, `dunning_tier`, `dunning_notice_day`, `gi_last_paid_at`, `gi_lapsed_at`.
- Auction: `auction_bid`, `auction_area`, `auction_category`, `auction_bid_at`, `auction_next_cycle_amount`, `auction_proration_policy`, `_nadlan_auction_winner`, `auction_rank`, `auction_clearing_price`.
- Lead routing/privacy/seams: `lead_route_*`, `_nadlan_after_lead_closed_fired`, erased lead contact fields during privacy erasure.

Reversibility:

1. Normal rollback: WP Admin -> Plugins -> deactivate `NadLan Config`.
2. Safer forward rollback: merge/release a higher version that reverts the bad module, then owner clicks Update.
3. Locked-out rollback: hosting file manager or SFTP -> rename `wp-content/plugins/nadlan-config` to `nadlan-config-disabled`.
4. WP-CLI rollback if available: `wp plugin deactivate nadlan-config`.
5. Restore previous package if needed: upload/reinstall the last known good ZIP or deploy a forward rollback version.

Irreversible-ish action:

- The role migration runs once behind `nadlan_roles_version` and adds roles with `add_role()`. It does not remove admin. It is still a data change, so if cleanliness matters later, run a cleanup migration that removes `nadlan_buyer` / `nadlan_advertiser` from administrators only.

## Cycle 5 - Autonomy Truth Audit

This is not yet a fully autonomous, owner-zero-touch, lead-to-money-to-invoice closed circle.

| Link | Status | Evidence / Truth |
|---|---|---|
| Lead captured | GREEN | Lead CPT and REST lead capture exist, including `/nadlan/v1/lead` and `nadlan_lead` storage. |
| Lead routed to owner/paid card owner | YELLOW | `lead-routing.php` stores routing meta and can email paid card owners, but it is email routing, not autonomous sales handling. |
| Lead auto-qualified by AI | YELLOW/RED | AI concierge exists, but current live route is Anthropic-first and not OpenAI-wired. It can answer/chat only after a key is configured and does not fully qualify/score leads into a pipeline by itself. |
| Lead auto-responded and followed up until close | RED | Drip/lead modules exist, but no closed-loop autonomous follow-up agent that negotiates, books, confirms, and closes without owner. |
| Booking/appointment closed automatically | RED | No verified booking engine or calendar-confirmed close path in v1.51.0. |
| Subscription money taken automatically | YELLOW | Green Invoice IPN rail exists, but owner must manually configure Morning recurring links, webhook URL, IPN secret, signature scheme, and correct reference pattern. |
| Invoice issued automatically | YELLOW | Morning can issue invoices after the owner configures recurring charges in Morning. The plugin does not create the Morning standing orders by itself. |
| Deal/success fee charged | RED | `nadlan_deal_closed` and `nadlan_revenue_event` seams exist, but the success-fee/deal-cut engine is not built. |
| Owner-zero-touch end to end | RED | Still needs owner setup, Morning setup, partner/lead business decisions, and human handling for closing/deals. |

## Enhancement / Fix Backlog From This Verification

1. Fix AI wiring before telling the owner "OpenAI concierge is on": provider settings UI, loader order, and endpoint refactor to `nadlan_ai_chat()`.
2. Update `/wp-json/nadlan/v1/health` version to `1.51.0` or remove hardcoded version.
3. Skip administrators during roles migration or add a cleanup task to remove extra custom roles from admins.
4. Add visible healthcheck "ready to travel" flag that summarizes: version correct, admin role version set, GI secret present, AI key present, crons scheduled, last cron heartbeat.
5. Add a Morning test-event button in Settings -> NadLan GI so owner does not hand-build a signed payload.
6. Add a real "owner is travelling" dashboard tile: failed IPNs, dunning cards, AI errors, lead delivery failures, and plugin version.
