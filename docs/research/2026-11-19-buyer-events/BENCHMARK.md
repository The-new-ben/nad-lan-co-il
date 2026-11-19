# Buyer events and the developer report: world benchmark (HAD-791, 19.11.2026)

Question: who in the world best shows a developer or seller "what buyers did", and where nad-lan stands.
Sources read 19.11.2026 (vendor pages and practitioner forums; vendor claims marked as such). Screenshot: shots/b1-zillow-listing-performance.jpg
(the in-app browser pane was hidden, so the other pages were read as text, not photographed; see the fairness note at the end).

| Who | Link | What they give the seller / developer | Inside the 3D / tool? | Funnel to a call? | Shareable link / export | Gap vs us before | After this package |
|---|---|---|---|---|---|---|---|
| Matterport (built-in Space Statistics) | matterport.com, practitioner thread wegetaroundnetwork.com/topic/1731 | impressions, visits, unique visitors per space | No: practitioners call it shallow; rooms and tags need third parties | No | No automatic send to clients (forum) | They count loads only | We count floor, direction, view, designer, payment check, basket, call, RFP per project |
| CAPTUR3D / Mattertraffic (Matterport add-ons) | wegetaroundnetwork.com/topic/9927 | heat map of rooms and scan points, time per room, tag clicks, CSV | Yes (rooms, tags) | No | CSV | Strong inside the tour, blind to the sales step | We join the 3D choices to the call and the lead on one visit |
| Zillow Listing Showcase, Listing Performance (Apr 2025) | grow.zillow.com/showcase-performance | views, saves, shares since live, buyer geography (state, city), compare to similar listings, pre-live interest, email stats | No (listing level) | No | "Share Report" PDF for the seller | Best seller-facing report in the world, but listing-level | We match geography (country) + saves + shares, and add the floor/view/payment steps and a live signed link (not a PDF that goes stale) |
| Spacio (Lone Wolf) | spacio.lwolf.com | post-open-house summary for sellers: sign-ins, activity, feedback, branded | No (physical open house) | Sign-in is the lead | Report to seller | Physical only | Same idea online, on every project page |
| Lasso CRM (ECI) | ecisolutions.com/products/lasso-crm | traffic, appointments and sales per community, daily traffic email, month-end rollup, funnel stages, custom reports | No (CRM side) | Yes (appointment kept → sale) | Dashboards, emails | Starts at the lead; blind before it | We give the developer the part before the lead: what the buyer chose before he asked |
| PostHog / Amplitude (event design) | posthog.com/docs/product-analytics/best-practices | object_action names, fixed verb list, properties, funnels | n/a | Funnels | n/a | Our names were ad hoc per module | Contract uses object_action (floor_select, view_open, rfp_send), fixed verbs, an allow list of properties |

## Where we stand after the package (honest)
- Ahead of every row above on one thing: the 3D choices, the tools and the call sit on ONE first-party visit, and the developer gets the funnel per project with real counts, by language and device, through a signed link that never goes stale and can be revoked.
- Behind Zillow on: comparison with similar listings (we do not compare projects to each other in the developer report: no invented baselines), email stats, a PDF (we give a printable page and CSV).
- Behind CAPTUR3D on: a heat map inside the tour (we record choices, not paths).
- Behind Lasso on: what happens after the lead (appointment kept, sale). That is the developer's CRM; we stop at the lead.

## Sources
- https://www.wegetaroundnetwork.com/topic/1731/omg-statistics-are-in-my-matterport-workshop
- https://www.wegetaroundnetwork.com/topic/9927/captur3d-detailed-analytics-and-heat-map-for-your-matterport-3d-tours/
- https://grow.zillow.com/showcase-performance , https://zillow.mediaroom.com/2025-04-15-Zillows-listing-performance-feature-gives-agents-deeper-market-insights-sellers-value
- https://spacio.lwolf.com/
- https://ecisolutions.com/products/lasso-crm , https://www.casestudies.com/company/lasso-crm/case-study/hunter-quinn-homes-customer-case-study
- https://posthog.com/docs/product-analytics/best-practices
