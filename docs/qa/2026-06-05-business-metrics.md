# v1.49.0 Business Metrics + Autopilot QA

Branch: `codex/business-metrics`

Scope: `plugins/nadlan-config/inc/business-metrics.php`, `plugins/nadlan-config/inc/ops-dashboard.php`, loader/version in `plugins/nadlan-config/nadlan-config.php`, plugin manifest/ZIP.

## What changed

- Added `nadlan_metrics_snapshot()` as a daily cached snapshot under `nadlan_metrics_snapshot_YYYYMMDD`.
- Added an Ops Autopilot panel through a new `do_action( 'nadlan_ops_after_grid' )` seam in `inc/ops-dashboard.php`.
- Added healthcheck `business` block: `mrr`, `net_churn`, `nrr`, `mrr_at_risk`, `active_paid`, `lead_volume_7d`.
- Added optional daily digest seam. It is disabled by default through `nadlan_metrics_digest_enabled` and can route to email/Slack through filters without storing secrets.
- Reads current main data safely and automatically uses future branch data when present:
  - `paid_tier`, `paid_order_id`, `campaign_end`, `dunning_state`, `gi_lapsed_at`.
  - `nadlan_gi_charge_log` from GAP3 if installed.
  - `nadlan_lead_log` from GAP2 if installed.
  - `auction_bid`, `auction_next_cycle_amount`, `_nadlan_auction_winner` from GAP7 if installed.
  - WooCommerce orders if `wc_get_orders()` exists.
- Keeps editorial premium separate from billable paid cards so showcase cards without billing evidence do not inflate MRR.

## Formulas

- MRR: billable paid-tier card monthly amount + winning auction next-cycle commitments.
- Billable paid card: `paid_order_id > 0`, recent `nadlan_gi_charge_log` paid event for the card, auction bid present, or a future `nadlan_metrics_card_is_billable` filter override.
- MRR at risk: active paid cards with `dunning_state=retrying`.
- Revenue churn: `lost_mrr_30d / month_start_mrr`.
- Net MRR churn: `(lost_mrr_30d - expansion_mrr) / month_start_mrr`, using current MRR expansion above the stored month-start MRR.
- NRR: `(start_mrr + expansion - lost_mrr_30d) / start_mrr`.
- Activation: new users in 7 days who have at least one published owned listing.
- Lead delivery: delivered owner route events divided by route attempts from `nadlan_lead_log`.
- AI deflection: read from `nadlan_ai_quality_stats()` when the AI hardening branch is installed.

First-run note: churn/NRR are `null` until the month-start MRR baseline option exists. The module stores it on first run and reports directional values after there is history.

## Manual QA

### Healthcheck after install

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=$(date +%s)" \
  | jq '.version,.business'
```

Expected:

- `.version` is `1.49.0`.
- `.business.mrr` is numeric.
- `.business.active_paid` is numeric.
- `.business.mrr_at_risk` is numeric.
- `.business.net_churn` and `.business.nrr` may be `null` on first run.

### Ops page

Open:

```text
/wp-admin/admin.php?page=nadlan-ops
```

Expected:

- Existing Ops cards still render.
- A new `Autopilot` section appears below the existing grid.
- Cards show Revenue, Paid base, Growth, Churn and NRR, and Auction.
- No public route is added.

### Package proof

```bash
tar -tf plugin-dist/nadlan-config-1.49.0.zip | head
tar -xOf plugin-dist/nadlan-config-1.49.0.zip nadlan-config/inc/business-metrics.php \
  | grep -E "nadlan_metrics_snapshot|healthcheck|nadlan_ops_after_grid|auction_revenue_mrr"
tar -xOf plugin-dist/nadlan-config-1.49.0.zip nadlan-config/nadlan-config.php \
  | grep -E "Version: 1.49.0|business-metrics|'version'             => '1.49.0'"
```

## 10-cycle checklist

- C1 Snapshot: `nadlan_metrics_snapshot()` returns one daily cached array.
- C2 Revenue: MRR uses billable paid tiers and auction commitments, not editorial premium alone.
- C3 Churn: revenue churn, net MRR churn, NRR, and MRR at risk are present and nullable when history is missing.
- C4 Activation: 7-day advertiser activation is computed from new users and owned published cards.
- C5 Leads: lead volume and delivery rate read `nadlan_lead_log` when GAP2 exists.
- C6 AI: AI deflection reads `nadlan_ai_quality_stats()` when GAP4/Track F exists, otherwise reports null.
- C7 Auction: auction commitment, fill rate, contests, and average winning bid read GAP7 meta when present.
- C8 Perf: all heavy work is behind a daily transient and daily option snapshot, not per-dashboard query loops on every page load.
- C9 Healthcheck: `business` block exposes the owner-critical metrics for external monitoring.
- C10 UX/copy: owner-facing Ops strings are concise, LTV:CAC is intentionally omitted until CAC is measured, and the PR adds no public route or theme change.

## Local checks

- `git diff --check`: run before PR.
- `php -l`: BLOCKED locally because `php` is not installed on this machine. Claude must run PHP lint in the WordPress/PHP sandbox before deploy.

## Caveats for Claude

- Current `main` does not include GAP2/GAP3/GAP7/AI-support yet. This module is intentionally defensive and returns zeros/nulls when those logs do not exist.
- The daily digest is opt-in. Claude or the owner should enable it with `nadlan_metrics_digest_enabled` and choose recipients through `nadlan_metrics_digest_recipients`.
- `project premier` defaults to ₪0 MRR because the current public package is a high-ticket project product, not confirmed monthly recurring. Override with `nadlan_metrics_mrr_project_premier` or `nadlan_metrics_tier_amounts` if the owner decides it is recurring.
- Editorial premium cards are counted separately as `editorial_paid_cards`, not included in MRR unless a paid order, recent GI paid event, auction bid, or filter proves billing.
