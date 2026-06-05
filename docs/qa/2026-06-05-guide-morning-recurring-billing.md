# Guide B - Turn On Automatic Recurring Billing With Morning

Important truth: the plugin does not create Morning standing orders by itself. The owner must do the Morning account work manually. The plugin receives signed Morning events, extends `campaign_end`, keeps `paid_tier`, logs charges, and handles dunning/lapse.

## What You Need Before Starting

- Access to the Morning / Green Invoice account.
- A real card/listing ID in WordPress.
- The owner user ID for that card/listing.
- The tier: `pro` or `premier`.
- A shared IPN secret that exists both in Morning/webhook settings and Settings -> NadLan GI.

The reference string must look like:

```text
card_<card_id>_user_<user_id>_tier_<pro-or-premier>
```

Example:

```text
card_4464_user_12_tier_premier
```

## Steps In Morning

1. Log into Morning.
   `[SCREENSHOT: Morning dashboard after login]`

2. Create a recurring charge / standing order link for Pro.
   `[SCREENSHOT: Morning recurring charge setup for Pro]`

3. Set the amount for Pro.
   `[SCREENSHOT: amount field, for example 349 ILS if owner confirms that price]`

4. Add the reference field in the exact pattern `card_<id>_user_<uid>_tier_pro`.
   `[SCREENSHOT: Morning reference/external id field]`

5. Save/copy the Pro recurring payment link.
   `[SCREENSHOT: copied Pro payment link]`

6. Repeat for Premier with `tier_premier`.
   `[SCREENSHOT: Morning Premier recurring payment link]`

7. In Morning webhook/IPN settings, add this webhook URL:

```text
https://nad-lan.co.il/wp-json/nadlan/v1/gi-ipn
```

`[SCREENSHOT: Morning webhook URL field]`

8. Set the webhook signature/secret in Morning. Save the exact same secret for the WordPress step.
   `[SCREENSHOT: Morning webhook secret/signature field, secret hidden]`

9. Confirm Morning sends the `X-Data-Signature` header, or another supported header listed in the code.
   `[SCREENSHOT: Morning webhook signature header documentation/settings]`

## Steps In WordPress

1. Open WordPress admin.
   `[SCREENSHOT: wp-admin dashboard]`

2. Go to Settings -> NadLan GI.
   `[SCREENSHOT: Settings menu with NadLan GI highlighted]`

3. Set Signature scheme to `Morning X-Data-Signature`.
   `[SCREENSHOT: signature scheme dropdown set to Morning]`

4. Paste the IPN secret into the IPN secret field.
   `[SCREENSHOT: IPN secret password field, value hidden]`

5. Optional: paste Morning API key for reconciliation.
   `[SCREENSHOT: API key field, value hidden]`

6. Keep cycle days at `31` unless the owner decides a different cycle.
   `[SCREENSHOT: Pro and Premier cycle days fields]`

7. Paste the Pro Morning recurring link into the Pro link field.
   `[SCREENSHOT: Pro Morning recurring link field]`

8. Paste the Premier Morning recurring link into the Premier link field.
   `[SCREENSHOT: Premier Morning recurring link field]`

9. Click Save settings.
   `[SCREENSHOT: Settings saved notice]`

10. Open healthcheck:

```text
https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=<current-time>
```

`[SCREENSHOT: healthcheck gi block]`

11. Confirm `gi.recurring_loaded:true` and `gi.sig_scheme:"morning"`.
    `[SCREENSHOT: gi.recurring_loaded and gi.sig_scheme]`

12. Send a Morning test event or make the first real low-risk recurring charge.
    `[SCREENSHOT: Morning test event or first charge status]`

13. Go back to Settings -> NadLan GI and look at Charge log.
    `[SCREENSHOT: Charge log table with date, ref, tier, status, action]`

14. Confirm the related card has `paid_tier=pro` or `paid_tier=premier` and a future `campaign_end`.
    `[SCREENSHOT: WordPress card custom fields paid_tier and campaign_end]`

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `/gi-ipn` returns 503 `not_configured` | No IPN secret saved in Settings -> NadLan GI. | Paste the same secret used in Morning and save. |
| `/gi-ipn` returns 401 `bad_signature` | Secret mismatch, wrong signature scheme, wrong header, or body changed before signing. | Confirm `Morning X-Data-Signature`, copy secret again, and verify Morning signs the raw body. |
| No charge log row | Event did not reach WordPress, bad JSON, missing event id, or bad reference. | Check Morning delivery log and verify reference pattern exactly. |
| Charge log row exists but campaign not extended | Ref does not point to an existing card, tier not `pro`/`premier`, or owner mismatch. | Fix reference in Morning and send a new event. |
| Card goes into dunning | Morning sent failed/declined status. | Resolve payment in Morning; a later paid event should clear dunning and extend the campaign. |
| Owner expects project/property recurring links | Current GI settings UI exposes Pro and Premier only. | Add product-specific recurring fields later if the owner wants separate recurring rails for project/property packages. |
