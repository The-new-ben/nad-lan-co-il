# v1.51.0 Finish-Line QA Index

Branch: `codex/final-hardening`

This index ties together the gap PRs and the owner prerequisites. Draft PRs stay draft until Claude reviews and deploys.

## Gap QA docs and PRs

| Area | Branch / PR | QA doc | Status |
| --- | --- | --- | --- |
| GAP 5 geo search | `codex/gap5-geo-search`, PR #76 | `docs/qa/2026-06-05-gap5-geo-search.md` | Draft delivered, Claude verified geo plus auction ordering composition |
| GAP 6 roles | `codex/gap6-roles`, PR #80 or later branch history | `docs/qa/2026-06-05-gap6-roles.md` | Draft delivered, Claude verified role setup |
| GAP 3 recurring | `codex/gap3-recurring`, PR #83 | `docs/qa/2026-06-05-gap3-recurring.md` | Draft delivered, Morning signature blocker cleared |
| GAP 7 placement auction | `codex/gap7-placement-auction`, PR #85 | `docs/qa/2026-06-05-gap7-placement-auction.md` | Draft delivered, co-deploy depends on GAP5 order fix |
| AI support hardening | `codex/ai-support-hardening`, PR #89 | `docs/qa/2026-06-05-ai-support.md` | Draft delivered, Claude approved decision logic |
| Business metrics | `codex/business-metrics`, PR #91 | `docs/qa/2026-06-05-business-metrics.md` | Draft delivered, Claude approved with directional-accounting caveat |
| Reliability | `codex/reliability`, PR #93 | `docs/qa/2026-06-05-reliability.md` | Draft delivered, pending Claude health/logger tests |
| Seams + final hardening | `codex/final-hardening` | this file | Current PR |

## Owner prerequisites before deploy sequence

- Set `nadlan_gi_ipn_secret`.
- Point Morning recurring webhook at `/wp-json/nadlan/v1/gi-ipn`.
- Create and paste Morning recurring links for each paid tier.
- Decide recurring cycle days for Pro, Premier, Project Premier, and Property Pro.
- Confirm auction slot count, reserve price, and bid increment.
- Configure real server cron if `DISABLE_WP_CRON` is enabled.
- Configure uptime monitor for `/wp-json/nadlan/v1/health`.
- Configure heartbeat URLs for `nadlan_gi_reconcile`, `nadlan_gi_dunning_tick`, and `nadlan_ao_daily_downgrade`.
- Configure OpenAI key and confirm the AI provider in the deployed GAP4/AI support branch.

## Final hardening in this PR

- Adds `inc/final-hardening.php`.
- Adds shared rate limiting for current public POST routes:
  `/lead`, `/claim`, `/saved-search`, `/review-submit`, `/concierge`, `/concierge-lead`,
  `/referral/route`, `/referral/<token>/accept`, `/referral/<token>/status`, and auction bids.
- Adds future seams:
  - `do_action( 'nadlan_after_lead_closed', $lead_id )`
  - `do_action( 'nadlan_search_executed', $args, $user_id )`
  - `apply_filters( 'nadlan_real_estate_listing_jsonld', $data, $post_id )`
  - `apply_filters( 'nadlan_card_jsonld', $data, $post_id, $type )`
  - `do_action( 'nadlan_card_jsonld_ready', $data, $post_id, $type )`
- Adds WP privacy exporters and erasers for lead data and future AI logs.
- Stops echoing the stored Anthropic key back into the admin password field.
- Stores replacement Anthropic keys with `autoload=false`.
- Pins `sslverify=true` on current-main Anthropic calls.
- Centralizes the Anthropic messages URL behind `nadlan_anthropic_messages_url`.

## Known deferred items

- Reviews after closed lead: seam exists as `nadlan_after_lead_closed`; review invitation workflow is deferred.
- Saved searches and alerts: seam exists as `nadlan_search_executed`; alert productization is deferred.
- Native geo POINT migration: deferred until the meta-model search is proven at traffic scale.
- Full ChartMogul-grade expansion/contraction/reactivation accounting: deferred. Business metrics currently label churn and NRR as directional, not board-grade accounting.
- Cross-branch endpoint hardening: GAP3/GAP5/GAP7 endpoints are hardened in their own draft branches where they exist. This PR hardens current-main public POST routes only.

## Manual QA

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=$(date +%s)" | jq '.version,.hardening'
```

Expected after deploy:

- `.version` is `1.51.0`.
- `.hardening.loaded` is `true`.
- `.hardening.rate_limit_routes` is at least `10`.
- `.hardening.privacy_hooks` is `true`.

Package proof:

```bash
tar -xOf plugin-dist/nadlan-config-1.51.0.zip nadlan-config/inc/final-hardening.php \
  | grep -E "nadlan_after_lead_closed|nadlan_search_executed|wp_privacy_personal_data|rest_pre_dispatch"
tar -xOf plugin-dist/nadlan-config-1.51.0.zip nadlan-config/inc/ai-concierge.php \
  | grep -E "sslverify|nadlan_ai_anthropic_key|value=\\\"\\\""
```

## Local checks

- `git diff --check`: run before PR.
- PHP-segment structural scan: run before PR.
- `php -l`: BLOCKED locally because `php` is not installed on this machine. Claude must run PHP lint in the WordPress/PHP sandbox before deploy.
