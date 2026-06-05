# Guide C - Daily Money Dashboard

The dashboard is for daily operational direction. It is not board-grade accounting. Churn and NRR are directional until the system tracks expansion, contraction, reactivation, and cohorts at event level.

## Steps

1. Open WordPress admin.
   `[SCREENSHOT: wp-admin dashboard]`

2. Click NadLan Ops in the left admin menu.
   `[SCREENSHOT: NadLan Ops menu item highlighted]`

3. Scroll to the Autopilot panel.
   `[SCREENSHOT: Autopilot panel under the existing Ops grid]`

4. Read MRR.
   `[SCREENSHOT: Revenue card showing MRR]`
   MRR means estimated monthly recurring revenue from paid tiers and auction commitments.

5. Read Revenue 30d and Orders 30d.
   `[SCREENSHOT: Revenue 30d and Orders 30d rows]`
   These come from WooCommerce completed/processing orders where available.

6. Read MRR at risk.
   `[SCREENSHOT: MRR at risk row]`
   This is money tied to cards in dunning/retry state. Watch this while travelling.

7. Read Paid-tier cards, Billable cards, and Editorial premium.
   `[SCREENSHOT: Paid base card]`
   Billable cards should be real paying cards. Editorial premium means the site floated a card editorially; it is not cash.

8. Read New signups 7d and Activation 7d.
   `[SCREENSHOT: activation rows]`
   Activation is the percentage of new advertisers who publish a listing within seven days.

9. Read Leads 7d and Lead delivery.
   `[SCREENSHOT: lead volume and lead delivery rows]`
   Lead delivery should stay high. If it drops, paid customers may not receive inquiries.

10. Read AI deflection.
    `[SCREENSHOT: AI deflection row]`
    This only becomes meaningful after the AI concierge is correctly configured and logging quality events.

11. Read auction revenue, fill rate, average bid, and contests.
    `[SCREENSHOT: auction card rows]`
    These indicate whether advertisers are competing for premium exposure.

12. Open healthcheck as a quick phone-friendly status URL:

```text
https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
```

`[SCREENSHOT: healthcheck JSON on phone]`

## What To Watch While Travelling

- Version: must be `1.51.0`.
- `gi.in_dunning`: if rising, payments are failing.
- `business.mrr_at_risk`: if rising, money is in danger.
- `lead_delivery_rate_7d`: if low, advertisers are not getting value.
- `ai.escalations_7d`: if high, AI is not resolving.
- `auction.active_contests`: if zero, auction monetization is not yet active.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Autopilot panel missing | Business metrics module not loaded or wrong plugin version. | Check healthcheck version and plugin update status. |
| MRR is zero even after orders | Cards may be paid editorially without `paid_order_id`, or recurring not configured. | Check card meta and Settings -> NadLan GI. |
| NRR/churn looks strange | Current formula is directional single-snapshot logic. | Use it for daily warnings, not accounting reports. |
| AI deflection empty | AI quality log not populated or concierge not configured. | Fix AI setup first. |
| Auction numbers zero | No active auction bids or auction disabled. | Check Settings -> NadLan Auction. |
