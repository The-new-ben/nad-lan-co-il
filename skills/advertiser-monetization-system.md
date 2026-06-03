# Advertiser Monetization System

> Use this when building or auditing a self-serve advertiser journey: claim or create a card, choose a paid package, pay, edit/upload media, receive inquiries, see performance, and renew or upgrade. Portable DNA for directory, marketplace, legal, travel, health, and real-estate sites.

## When to use this

- A customer pays to publish or promote a listing, project, profile, service page, or sponsored placement.
- The site needs a dashboard, post-checkout next step, campaign report, or upgrade path.
- A competitor scan shows "advertising" but the product lacks concrete deliverables.

## The standard

1. Sell a concrete artifact, not vague visibility.
   - Artifact: profile, project page, listing, article, microsite, verified badge, top placement.
   - Position: where it appears.
   - Duration: how long it runs.
   - Reporting: what proof the customer gets.

2. The first paid minute must feel premium.
   - Order confirmation explains what happens next.
   - Customer can reach a center/dashboard immediately.
   - If the promoted entity does not exist yet, the customer gets a setup/request path.

3. The advertiser center is mandatory.
   - Owned assets.
   - Completion checklist.
   - Edit/upload button.
   - Public preview.
   - Views, inquiries, reviews.
   - Orders and package status.
   - Upgrade and renewal CTAs.

4. Reporting is part of the product.
   - Minimum: views, inquiries, reviews, completion score, campaign period, product purchased.
   - Stronger: source/channel, top pages, search queries, response time, valid/invalid inquiry status.
   - Never promise traffic that cannot be measured or delivered.

5. Billing truth must be visible internally and accurate publicly.
    - If the gateway is one-charge only, sell annual/fixed-duration products or document manual standing-order follow-up.
    - Do not describe a package as automatic recurring unless automatic rebilling is actually active.
    - A one-time paid tier must have an expiry job. Without downgrade automation, the first payment becomes permanent access and revenue leaks.
    - Reuse the existing entitlement field that ranking/gating already reads. Do not invent a parallel campaign status that paid placement code cannot see.

6. Media is the premium surface.
   - Require hero image, gallery, map pin, description, contact, and relevant proof.
   - For real estate: floorplan, video, 3D tour, developer logo, project status, units, delivery/planning data.
   - AI assist is a helper, not a substitute for verification.

7. Lead quality matters more than raw lead count.
   - Track valid contact method, intent, source, entity, and status.
   - Replace/refund invalid deliverable leads if that is part of the offer.
   - Avoid shared-lead ambiguity unless it is disclosed.

## v1.41.2 Nadlan implementation

- Code module: `plugins/nadlan-config/inc/advertiser-center.php`
- Order bridge: `plugins/nadlan-config/inc/advertiser-orders.php`
- Route: `/advertiser-center/`
- Alias route: `/advertiser-dashboard/`
- Shortcode: `[nadlan_advertiser_center]`
- WooCommerce hook: post-payment next-step panel for products 476, 477, 489, 490.
- Paid activation hook: `woocommerce_payment_complete`.
- Paid tier mapping: product 476 -> `pro`, 477 -> `premier`, 489 -> `premier` on `nadlan_project`, 490 -> `pro` on `nadlan_property`.
- Card-level paid metadata: `paid_tier` plus `campaign_end`, `paid_order_id`, `paid_product_id`.
- Daily cron: `nadlan_ao_daily_downgrade` returns expired `pro`/`premier` cards to `paid_tier=free`.
- Healthcheck keys: `advertiser_center`, `advertiser_order_bridge`.
- Research log: `docs/2026-06-03-advertiser-monetization-research-and-center.md`

## Editorial premium showcase pattern

For owner-approved editorial showcase cards, it is valid to set `paid_tier=premier` without `paid_order_id`. That distinguishes a manually curated demonstration listing from a paid campaign: the order-expiry cron only downgrades cards with a positive `paid_order_id`, so editorial showcases do not auto-expire or create fake revenue attribution. Document the reason in the PR/body notes, keep `claim_status=verified` when premium public surfaces are expected, and never treat the missing `paid_order_id` as a billing bug for explicitly marked editorial showcases.

## What not to do

- Do not sell "exposure" without a time period and report.
- Do not hide the next step after checkout.
- Do not create a beautiful Studio editor that customers cannot find after paying.
- Do not count all leads as valuable; define valid inquiries.
- Do not expose internal labels such as CRM, paid lead routing, UTM, or money page in public copy.

## Revision log

- 2026-06-03 — Created by Codex after the Nadlan advertiser-center build and competitor scan. Captures the reusable monetization/product standard for future site work.
- 2026-06-03 — Tightened the order bridge around the owner steer: `paid_tier` stays the source of truth; `campaign_end` + daily downgrade cron prevent permanent access from one-time payments.
- 2026-06-04 — Documented the editorial premium showcase pattern: `paid_tier=premier` can be valid without `paid_order_id` when the owner explicitly marks a curated example card as editorial, not paid.
