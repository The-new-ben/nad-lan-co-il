# Advertiser Monetization Flow: Current State And Gap Map

Date: 2026-06-04
Scope: Nadlan advertiser journey, paid listing/project/professional activation, reporting, billing handoff, and QA gates.
Mode: docs-only. No plugin code, no new public route, no version bump.

## Executive Read

The core monetization spine is now materially further along than the older readiness docs suggest.

Live evidence from 2026-06-04:

- `https://nad-lan.co.il/join-pro/` returns `200` and is the canonical public pricing/packages page.
- `https://nad-lan.co.il/advertiser-center/` returns `302` for logged-out users, which is correct for a logged-in advertiser center.
- `https://nad-lan.co.il/advertise/` returns `404`, which is correct while the URL decision is parked. Do not create or merge a second public advertiser route without Claude and owner sign-off.
- `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck` returns plugin version `1.41.2` and reports:
  - `advertiser_center.route = https://nad-lan.co.il/advertiser-center/`
  - `advertiser_center.products = [476,477,489,490]`
  - `advertiser_order_bridge.activation_hook = woocommerce_payment_complete`
  - `advertiser_order_bridge.uses_paid_tier = true`
  - card meta: `campaign_end`, `paid_order_id`, `paid_product_id`
  - `advertiser_order_bridge.daily_downgrade_cron = true`
  - durations: `476=30`, `477=30`, `489=180`, `490=60`
- `/join-pro/` source includes Google Site Kit / Google tag output and Product JSON-LD for the main paid products I observed.

The next phase is no longer "invent the system." It is: verify every customer path, align the public offer copy with the actual one-time billing/duration logic, finish the no-card attach/create path, improve advertiser reporting, and make the visual shell premium.

## Competitor Pattern: What World-Class Platforms Sell

The best advertiser products do not sell vague "exposure" by itself. They sell one or more of:

1. A durable asset: a listing page, profile, project mini-site, gallery, 3D tour, or sponsored article.
2. Guaranteed position for a fixed duration.
3. A measurable action: lead, click, call, save, inquiry, or checkout.
4. A dashboard/report that proves delivery.
5. A managed upsell path: better media, higher position, larger audience, or more reporting.

| Source | URL | Lesson for Nadlan |
| --- | --- | --- |
| Zillow Premier Agent | `https://premieragent.zillow.com/products/advertising/` | The product is not just a profile. It is an acquisition system with leads, response expectations, and reporting. For Nadlan, Pro/Premier must show leads, views, response state, and next action. Curl got `403`, so treat this as a public official URL to review in browser. |
| Zillow Showcase | `https://www.zillow.com/z/showcase-listing/` and `https://www.zillowgroup.com/news/zillow-showcase-brings-listings-to-life/` | Premium listings use richer media and immersive context. A premier Nadlan project cannot be an emoji card plus text. It needs gallery, location, amenities, schema, and a visible showcase treatment. Curl got `403`, so browser review is required for exact UI. |
| Rightmove products | `https://www.rightmove.co.uk/this-is-rightmove/our-products/` | Listing-depth products are clear when they specify placement, visibility, and product ladder. Nadlan should state product duration and placement, not just "promotion". |
| Rightmove advertise | `https://www.rightmove.co.uk/this-is-rightmove/advertise-with-us/` | Media sales should separate audience proposition from product mechanics. Nadlan's canonical path is `/join-pro/`; any media-kit expansion must not duplicate that URL intent. |
| REA Ignite | `https://ignite.realestate.com.au/` | Reporting and campaign tools are part of the paid product, not a bonus. Nadlan's advertiser center should evolve from best-effort counters to campaign-period reports. |
| REA agent | `https://agent.realestate.com.au/` | Agent tooling is sold as a professional operating system. Nadlan should make advertisers feel they have a control center, not only a checkout receipt. |
| LoopNet / CoStar | `https://www.loopnet.com/advertise/` and `https://www.costargroup.com/about-us/brands/loopnet` | Commercial property advertisers expect high-intent audience, filters, asset pages, and serious lead capture. Curl got `403`; use browser or sales pages for UI review. |
| Apartments.com | `https://www.apartments.com/advertise/` | Property ads sell package tiers plus audience delivery. For Nadlan, package tiers must match the actual `paid_tier` and `campaign_end` behavior. Curl got `403`; browser review required. |
| Houzz Pro | `https://www.houzz.com/pro` | Professionals buy a business profile, portfolio, reviews, lead handling, and business tools. Nadlan professional advertisers need profile completion, photos, reviews, lead attribution, and renewal prompts. |
| Homes.com advertise | `https://www.homes.com/advertise/agents/` | Agent advertising is moving toward profile ownership plus leads and attribution. Curl got `403`; use browser review for exact current copy. |
| Yad1 / Yad2 | `https://www.yad2.co.il/yad1` and `https://www.yad2.co.il/realestate/forsale` | Israel's mainstream real-estate portals normalize project marketing and paid listing placement. Nadlan must compete on trust, content quality, and advertiser reporting, not traffic volume yet. |
| Madlan developers | `https://www.madlan.co.il/developers` | Developer/project credibility comes from concrete facts, project inventory, city context, and data confidence. Nadlan project cards and profiles need developer facts and source caveats. |
| GA4 ecommerce docs | `https://developers.google.com/analytics/devguides/collection/ga4/ecommerce?client_type=gtag` | Purchase, item, and campaign events should be measurable. Nadlan should eventually send product id, card id, tier, campaign duration, and checkout source as structured events. |
| Bing Webmaster | `https://www.bing.com/webmasters/about` | Bing matters for search visibility and AI/search surfaces. Advertiser reporting should eventually include Google and Bing visibility, not only internal views. |
| Israeli consumer disclosure sources | `https://www.gov.il/he/departments/the_consumer_protection_and_fair_trade_authority/govil-landing-page` and `https://www.gov.il/he/pages/influencers-opinion-leaders` | Sponsored/benefit-driven content needs clear disclosure. Curl got `403`, so verify in browser/legal review before public copy, but keep the disclosure requirement as a product invariant. |

## Current Nadlan Product Map

Authoritative current live state comes from `/join-pro/`, plugin healthcheck, and the pending/merged 1.41.2 code path now reported live.

| Product | Current behavior | Card type | Tier outcome | Duration | Notes |
| ---: | --- | --- | --- | ---: | --- |
| 476 | Professional Pro | `nadlan_professional` | `paid_tier=pro` | 30 days | Product copy must not imply automatic monthly rebilling unless Morning standing order is configured. |
| 477 | Professional Premier | `nadlan_professional` | `paid_tier=premier` | 30 days | Premium visual treatment still depends on catalog redesign. |
| 489 | Project campaign | `nadlan_project` | `paid_tier=premier` | 180 days | This is the flagship developer offer. Needs project create/attach path and reporting. |
| 490 | Promoted property | `nadlan_property` | `paid_tier=pro` | 60 days | `/join-pro/` copy said monthly in the fetched source. Align with actual one-time/duration behavior. |

Entitlement source of truth:

- `paid_tier` remains the only ranking/gating source.
- Paid order bridge adds only `campaign_end`, `paid_order_id`, and `paid_product_id`.
- Activation is on `woocommerce_payment_complete`.
- Expiry is controlled by `nadlan_ao_daily_downgrade`.
- Expiry guard requires `paid_order_id > 0`, preserving editorial/trial use cases.

## Canonical URL Rule

`/join-pro/` is the live packages/pricing page. The parked `/advertise/` branch must not merge until Claude and the owner decide whether there should be one public URL or two. Current live `/advertise/` returning `404` is acceptable and should stay that way for now.

Do not create:

- `/advertise/`
- `/media-kit/`
- `/pricing/`
- another public package page

without explicit URL decision sign-off.

## Target End-To-End Advertiser Journey

### Flow A: Existing professional claims and upgrades

1. Professional finds card in `/professionals/`.
2. Professional claims card.
3. Owner verifies claim or system verifies according to policy.
4. Card enters trial/free state using existing `paid_tier` contract.
5. Advertiser opens `/advertiser-center/`.
6. Advertiser clicks Studio for completion, photos, map, video, contact fields.
7. Advertiser chooses Pro or Premier from `/join-pro/` or center.
8. Checkout carries `card_id`.
9. Payment complete activates `paid_tier`, `campaign_end`, `paid_order_id`, `paid_product_id`.
10. Advertiser center shows active period, profile completion, leads, views, orders, renew/upgrade action.
11. Daily cron downgrades only expired paid-order campaigns.

### Flow B: Project advertiser starts without an existing card

1. Marketing manager reaches `/join-pro/`.
2. Buys product `489` without `card_id`.
3. Order is stored but not silently dropped.
4. `/advertiser-center/` surfaces the unlinked order.
5. Advertiser can attach to an owned existing `nadlan_project`, claim one, or create/request a new project card.
6. Activation happens only after card ownership/type is valid.
7. Studio opens for images, facts, map, amenities, status, and content completion.
8. Project becomes `paid_tier=premier` for 180 days.
9. Report shows campaign period, views, leads, public URL, completion score, and next recommended action.

Current live/pending system appears to cover steps 2-4 and attach-to-owned-card. The self-service "create/request new project card after no-card purchase" path still needs QA and may need product work if no usable create path exists.

### Flow C: Editorial showcase

1. Owner/editor creates a showcase project, such as Rainbow Tel Aviv.
2. Card may use `paid_tier=premier` without `paid_order_id`.
3. Daily downgrade cron must not expire it because the trial/paid-order guard is `paid_order_id > 0`.
4. Internal note must identify it as editorial showcase, not a paid campaign.

This is correct architecture, not a leak.

## Gap Map

| Gap | Severity | Evidence | Required next move |
| --- | --- | --- | --- |
| No-card project purchase needs full QA | Blocker | Order bridge has unlinked-order handling, but the actual user journey from paid product `489` to a live/owned project card still needs browser QA. | Run Journey 2 with a test user/order. If no project create/request path exists, Claude should add one after sign-off. |
| Public offer copy vs billing reality | Blocker | Green Invoice/Morning gateway is one-time. Order bridge uses fixed durations. `/join-pro/` source showed monthly language for product 490. | Audit `/join-pro/` wording against actual duration and renewal model. Replace automatic-monthly implications with one-time campaign duration or explicit Morning standing-order language. |
| Advertiser reporting is still thin | Major | Advertiser center reports `view_count`, exact `lead_card_id` inquiries, reviews, photos, orders. It does not yet prove Google/Bing/search exposure or campaign-period deltas. | Define report v1: campaign dates, page views, card views, leads, CTA clicks, source, completion score, public URL, next recommendation. |
| Visual premium is pending | Major | Current catalog/profile shell still uses the older card system; PR #36 documents the premium redesign target. | Claude implements premium catalog/profile shell after reviewing PR #36. |
| Legal disclosure policy must be productized | Major | Sponsored/benefit-driven content needs visible disclosure. Existing docs say this, but public terms/disclaimer need review. | Add/verify advertiser terms and sponsored-content disclosure language before selling sponsored articles at scale. |
| `/join-pro/` Product schema may be incomplete | Major | Fetched source showed Product JSON-LD for 476, 477, 489; I did not observe 490 in the truncated match output. | Confirm 490 schema appears or update schema after Claude review. |
| Measurement events need product/card ids | Major | Google tag is present, but event coverage for add-to-cart, checkout, purchase, card_id, tier, source is not proven. | Add GA4 event contract and verify in debug mode: view pricing, choose package, add to cart, begin checkout, purchase, open center, upload photo, submit lead. |
| Renewal lifecycle is basic | Major | Cron downgrades expiry. Renewal reminders, "expiring soon", and post-expiry reactivation copy are not proven. | Add center/email states: active, expiring in 7 days, expired, renew, upgrade. |
| Mobile advertiser center is unverified | Major | `/advertiser-center/` redirects logged out, so authenticated mobile layout still needs browser QA. | QA at 390px and desktop with real advertiser account. |
| Terms for no traffic guarantee | Major | Pre-traffic sites should not guarantee impressions/views. | Public product copy should commit to asset, placement, duration, and reporting, not guaranteed traffic unless a make-good system is approved. |
| Create/upload image flow needs hard testing | Major | Studio exists, but the demanding project advertiser expects image upload, gallery, map, video, amenities. | QA Studio with project card: upload images, set map pin, save, reload, view public profile. |
| Admin all-advertisers view remains a question | Minor | Advertiser center has `?all=1` admin sample mode, not a full sales/ops dashboard. | Decide whether owner needs an admin advertiser operations dashboard after customer flow is stable. |

## Minimum Release Acceptance Bar

The advertiser system is not "production complete" until the following are proven with current live state:

1. `/join-pro/` is the only public package URL and its copy matches the actual products/durations.
2. Logged-out `/advertiser-center/` redirects to login.
3. Logged-in advertiser sees owned cards and unlinked paid orders.
4. Buying with `card_id` activates the correct card on `woocommerce_payment_complete`.
5. Buying without `card_id` does not silently drop; the center offers attach/create/request path.
6. Expired paid orders downgrade to `free`, but editorial showcase/trial cards without `paid_order_id` are not wiped.
7. Lead attribution counts exact `lead_card_id` matches only.
8. Studio edits persist: description, city/address, phone/email, photos, map, video/tour where supported.
9. Advertiser center shows campaign dates, views, inquiries, orders, and next action.
10. Mobile 390px journey has no horizontal overflow or hidden CTAs.

## What I Could Not Verify In This Pass

- I did not log in as an advertiser or complete a WooCommerce payment. A real end-to-end paid order test still needs a test customer and owner-approved payment/gateway mode.
- I did not alter `/join-pro/` copy or plugin code because the current lane is docs-only and plugin changes require Claude sign-off.
- Several competitor/sponsor/legal source URLs return `403` to curl. They should be reviewed in a normal browser before exact public copy is finalized.
