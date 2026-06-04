# GAP 3 — Recurring billing: DECISION = Option B (true auto-renew)

Owner decision 2026-06-04: **Option B — true auto-renew** (not annual+reminder).

## Feasibility: CONFIRMED ✅
The live payment gateway **Morning (Green Invoice) for WooCommerce** supports
recurring subscriptions + tokenized auto-renew. Evidence from the plugin's
official changelog (wordpress.org/plugins/wc-gateway-greeninvoice/):

- v1.6.0 (2024-08-14) — "Added support for WooCommerce Subscriptions"
- v1.6.1 — "WooCommerce Subscriptions trial days"
- v2.3.5 (2025-12-02) — "Improved WooCommerce Subscriptions integration"
- v2.3.6 (2025-12-28) — "Added support for replacing a token for existing subscriptions"

## Hard requirement (PURCHASE — owner action)
The Morning gateway integrated against the **official WooCommerce Subscriptions**
extension (the woocommerce.com product, ~$199/yr). The free alternatives
(wpswings/subscriptions-for-woocommerce, YITH free) are NOT what Morning hooks —
do not use them for this gateway.

Prerequisites:
1. Buy + install official **WooCommerce Subscriptions** (~$199/yr). [OWNER]
2. Morning account Basic/Extra + Digital Payments add-on. [ALREADY HAVE]

## Implementation plan (Codex, after the plugin is installed)
1. Convert ad SKUs 476/477/489/490 from `simple` → `subscription` products
   (or add subscription variants) with billing periods:
   - 476 Pro pro: monthly (₪349/mo, first month free retained as trial)
   - 477 Premier: monthly (₪749/mo)
   - 489 project campaign: keep as 180-day or make a 6-month renewing term
   - 490 property ad: 60-day or monthly per owner preference
2. Rewire `plugins/nadlan-config/inc/advertiser-orders.php`:
   - Replace the one-time `woocommerce_payment_complete` activation (line 103)
     with subscription lifecycle hooks:
       woocommerce_subscription_status_active   → set paid_tier (activate)
       woocommerce_subscription_status_on-hold  → grace (keep tier briefly)
       woocommerce_subscription_status_expired
       woocommerce_subscription_status_cancelled → downgrade to free
   - Keep the existing daily `nadlan_ao_daily_downgrade` cron as a SAFETY NET
     only (in case a webhook is missed), but the subscription status becomes
     the source of truth.
   - `campaign_end` becomes the subscription's next-payment/end date.
3. Idempotence: the existing guard (paid_order_id === order_id) must extend to
   renewal orders — each renewal is a new order on the same subscription;
   activate on every renewal, downgrade only on terminal statuses.
4. Advertiser Center: show subscription status + next billing date + a
   "manage/cancel subscription" link to /my-account/subscriptions/.

## QA (must pass before customer outreach)
- Buy 476 as a subscription → tier=pro, subscription active, next-payment set.
- Force a renewal (WP-CLI `wp wc subscription` or wait) → tier stays pro,
  new order created, no double-charge, no downgrade.
- Cancel the subscription → at period end tier downgrades to free.
- Refund a renewal → tier handling stays correct.
- All verified in docs/2026-06-04-e2e-revenue-qa-script.md Part 2 (extended).
