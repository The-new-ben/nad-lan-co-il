# Advertiser Monetization Research + v1.41.3 Media Kit

Date: 2026-06-03
Agent: Codex
Scope: project advertisers, claimed professionals, promoted property owners, billing/order handoff, Studio usage, reporting expectations.

## Honesty statement

The site already has serious revenue plumbing: WooCommerce + Green Invoice, tier products, project campaign product, claim flow, Studio, lead ledger, reviews, sponsored spot, and GA4 dataLayer events. The gap is not "can we imagine monetization"; the gap is making a paying customer feel guided after payment and giving them visible proof of value. This release improves that first customer-facing layer. It does not claim real revenue until orders, traffic, leads, and renewals are verified.

## Live baseline checked

- `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=codex` returned plugin `1.41.1`, WordPress `7.0`, PHP `8.5.5`.
- `/join-pro/` returned HTTP 200 with 159,324 bytes.
- `/projects/` returned HTTP 200 with 109,897 bytes.
- `/studio/` redirected unauthenticated users to WordPress login, which is correct for an owner-only editor.
- Healthcheck tier counts were `free=0`, `pro=0`, `premier=0`, so no paid-card data exists yet for proof of paying-customer behavior.

## Competitor research: patterns to steal

1. Zillow Premier Agent
   Source: https://zillow.zendesk.com/hc/en-us/articles/360000985228-Premier-Agent-FAQ
   Pattern: lead vetting, phone connection, share-of-voice routing, CRM inbox, and reporting for incoming leads / attempted / successful connections.

2. Homes.com advertising
   Source: https://www.homes.com/advertise/agents/
   Pattern: Listing Boost vs membership, top search placement, retargeting, Matterport, lead vetting, analytics reports, and post-checkout instructions to access reports.

3. Rightmove valuation products
   Source: https://www.rightmove.co.uk/press-centre/property-valuation-leads-to-agents-up-50-on-last-year/
   Pattern: AI-assisted agent response, seller-intent prediction, opportunity dashboard, valuation reports, and notification when a prospect views a report.

4. Zoopla agent products
   Source: https://www.zoopla.co.uk/press/releases/zoopla-delivers-record-number-of-valuation-leads-in-january-up-30-year-on/
   Pattern: seller-lead products positioned around tangible ROI, top-six local valuation placement, and data insights.

5. REA Audience Maximiser
   Source: https://help.realestate.com.au/hc/en-us/articles/44972749736601-A-guide-to-Audience-Maximiser-All-Packages
   Pattern: fixed packages with expected clicks, campaign duration, automated video ads from listing images, and tiered reach.

6. LoopNet / CoStar
   Source: https://www.loopnet.com/solutions/
   Pattern: explicit tier comparison: priority ranking, call tracking, logo/headshot in search, CoStar homepage placement, newsletter placements, retargeting, photo shoot, Matterport, video, drone.

7. Matterport real estate
   Source: https://matterport.com/industries/real-estate
   Pattern: 24/7 virtual open house, floor plans, room dimensions, AI-generated listing descriptions, defurnish/visualization, MLS-ready exports.

8. Houzz Pro local advertising
   Source: https://pro.houzz.com/for-pros/feature-advertising
   Pattern: project/budget targeting, premium local listing, finished-project showcase, photos selected for ads, notifications for new inquiries, service-area controls.

9. Yelp for Business / services
   Source: https://business.yelp.com/services/ and https://biz.yelp.com/support-center/article?articleNumber=000018229&l=en-US
   Pattern: claimed page, messages, calls, website clicks, page visits, and lead definitions that avoid obvious double counting.

10. Yad2 real estate
    Source: https://realestate.yad2.co.il/
    Pattern: Israeli users expect quick category depth, "publish ad" visibility, real-estate services, map search, mortgage advisors, appraisers, lawyers, and valuation tooling.

11. Madlan developers index
    Source: https://www.madlan.co.il/developers
    Pattern: project/developer trust layer; Nadlan must beat this with richer owner editing, claim path, data, and reports.

## Product decisions applied in v1.41.2

- Add `/advertiser-center/` and `/advertiser-dashboard/` as logged-in customer routes.
- Add `[nadlan_advertiser_center]` shortcode as a fallback for any WordPress page.
- Show owned cards/projects/properties from `owner_user_id`.
- Show completion score: title, description, city/address, contact, photos, map, video/tour, verified ownership, and project-specific developer/status fields.
- Show views from `view_count`, reviews from `reviews_count`, photos from `photos_csv`/thumbnail, and best-effort identified inquiries from `nadlan_lead`.
- Show recent WooCommerce orders for the logged-in customer.
- Show product upgrade paths for products 476, 477, 489, 490.
- Add a WooCommerce thank-you panel for paid products so the order-received page tells advertisers what to do next.
- Add a My Account dashboard link to the advertiser center.
- Add healthcheck metadata for the new route and product ids.
- Add `inc/advertiser-orders.php` to preserve `card_id` through WooCommerce checkout and activate the existing `paid_tier` meta on `woocommerce_payment_complete`.
- Do not create a parallel campaign status field. Card-level paid state is only `paid_tier` plus `campaign_end`, `paid_order_id`, and `paid_product_id`.
- Add a daily downgrade cron so expired one-charge campaigns return `paid_tier` to `free` instead of becoming permanent paid placements.
- Add an Advertiser Center fallback for paid orders that were not connected to a card at checkout.

## Product decisions applied in v1.41.3

- Add `inc/advertise.php` with `/advertise/` and `[nadlan_advertise]` as the public media-kit and package-truth surface.
- Present package deliverables as artifact + duration + reporting instead of vague "exposure".
- Show an honest audience snapshot from current site data: professionals, projects, properties, recent leads, and internal tracked views.
- Wire public CTAs directly to WooCommerce products 476, 477, 489, and 490.
- Publish core advertiser policies on the page: no traffic guarantees in Phase 0, fixed campaign duration, sponsored-content disclosure, and make-good for missed placement.

## Ten more issues to handle next

1. Replace remaining vague monthly "exposure" copy with asset + position + duration + reporting copy everywhere outside `/advertise/`.
2. Resolve recurring billing truth: annual products vs Morning standing order vs custom recurring integration.
3. Add a real advertiser report generator: PDF/email monthly summary with views, inquiries, reviews, completion score, campaign dates, and next recommended action.
4. Add a "request project setup" form or draft-project wizard for customers who pay for product 489 before a project CPT exists.
5. Add verified media checklist: hero images, gallery minimum, floorplan, video, 3D tour, map pin, developer logo.
6. Add advertiser-facing lead quality states: new, contacted, valid, invalid/replaced, closed.
7. Add customer notifications: after payment, after first edit, weekly missing-fields reminder, monthly report.
8. Add advertiser terms page/PDF before selling sponsored articles at scale.
9. Add visual QA for `/advertise/` and `/advertiser-center/` on mobile after the owner updates to v1.41.3.
10. Decide whether admins should have a real all-advertisers dashboard separate from the customer-facing center.
11. Add source-of-truth campaign metrics from GA4/Search Console when authenticated reporting is available.
12. Add an automated test fixture for paid orders with `card_id` so the tier activation and downgrade logic can be regression-tested without a real charge.
13. Add operational monitoring for the daily downgrade cron so expired paid tiers cannot silently stay paid.

## QA notes for this release

The code can be linted and ZIP-gated before merge. Full end-to-end production QA still requires an owner/plugin update and, for the full paid journey, either a test payment path or explicit permission for a real charge/refund. After update, rerun Journey 2 from `skills/qa-journey-testing.md` with focus on:

- `/join-pro/` to product 489 checkout.
- Order-received page shows the new next-step panel.
- `/advertiser-center/` redirects unauthenticated users to login.
- Logged-in advertiser sees owned cards and Studio links.
- A claimed card with missing photos shows the missing-fields chips.
- A project advertiser can reach `/studio/?id=<project_id>` from the center.
- Paid order with `card_id` activates `paid_tier` through `woocommerce_payment_complete`, not through `woocommerce_thankyou`.
- Paid activation writes only `campaign_end`, `paid_order_id`, and `paid_product_id` on the card.
- Daily downgrade cron returns expired `pro`/`premier` cards to `paid_tier=free`.
- `/advertise/` renders for public users, shows honest current metrics, and every package CTA lands in the expected WooCommerce cart flow.
