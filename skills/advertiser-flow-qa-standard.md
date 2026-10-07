# Advertiser Flow QA Standard

Use this skill when testing or specifying a paid advertiser journey for Nadlan or another marketplace site.

## Non-Negotiables

- The public package URL must be canonical. For Nadlan today, use `/join-pro/`. Do not create `/advertise/`, `/media-kit/`, or `/pricing/` without URL sign-off.
- The entitlement source of truth is `paid_tier`.
- Paid orders may add only explicit campaign/order metadata: `campaign_end`, `paid_order_id`, `paid_product_id`.
- Paid activation happens on the real paid hook, not a thank-you page view. For Nadlan, that is `woocommerce_payment_complete`.
- One-time campaigns must expire. A paid placement without expiry is a revenue leak.
- Trial/editorial showcase states must not be wiped by paid-order expiry jobs.
- Purchases without card context must be surfaced and attachable. Never silently drop paid intent.
- Paid public and internal screens must support the same premium promise. Raw sprite IDs, stock/fake people imagery, default WordPress controls, or abandoned empty cards can undermine the sale even when billing works.

## The Journey To Prove

1. Discover the package from normal navigation.
2. Understand what is sold: asset, placement, duration, reporting, and next step.
3. Claim or create the relevant card.
4. Edit the card in Studio.
5. Upload media.
6. Pay.
7. Activate the right tier on the right card.
8. Show campaign dates and proof in the advertiser center.
9. Attribute leads exactly to the card.
10. Renew, upgrade, or downgrade correctly.

## Evidence Required

For a production claim, gather:

- public URL status checks
- browser screenshots at desktop and 390px mobile
- order id and order notes
- product id
- card id and post type
- `paid_tier`
- `campaign_end`
- `paid_order_id`
- `paid_product_id`
- lead id and `lead_card_id`
- Studio save/upload proof
- report/dashboard screenshot
- expiry cron proof

## Failure Classes

Blocker:

- paid order does not activate the correct card
- paid order activates the wrong card
- no-card order disappears
- expired paid campaign never downgrades
- trial/editorial card is downgraded by paid cron
- checkout cannot complete
- advertiser cannot reach their card after payment

Major:

- package copy conflicts with actual duration/billing
- card can be upgraded but cannot be edited
- lead count uses fuzzy matching
- reporting does not show campaign period or leads
- mobile flow has horizontal overflow or hidden CTA
- public page looks non-premium enough to undermine the advertiser sale
- public package metadata conflicts with actual billing duration or implies traffic guarantees

Minor:

- labels are unclear but the path works
- empty states are awkward but not blocking
- report needs better wording
- visual polish remains after core flow passes

## Source Lessons

- Zillow/REA/Rightmove style products sell media, position, action, and reporting.
- Houzz-style professional tools sell profile completion, proof, reviews, and leads.
- Israeli project/listing advertisers expect concrete packages and clear disclosure.
- Before traffic is proven, sell controlled deliverables and reporting, not guaranteed exposure.

## Stop Rule

If a test reveals a missing public route decision, missing module ownership decision, payment gateway issue, or legal/sponsored-disclosure decision, stop and document the gap. Do not invent routes or patch plugin modules without Claude and owner sign-off.
