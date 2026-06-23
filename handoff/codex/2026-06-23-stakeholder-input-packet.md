# Stakeholder Input Packet

Date: 2026-06-23

Purpose: collect the business, asset, and technical facts needed from the relevant decision-maker, advisor, contractor contact, or technical partner before NadLan turns the showroom into the contractor-facing product.

This is not a blocker for design work. It is the checklist that prevents expensive wrong assumptions while Codex and Lovable continue the showroom redesign.

## 1. Outcome Needed From The Call

After the call, NadLan should know:

- which showroom model is realistic for the first contractor demo
- which assets exist now and which must be requested from contractors
- how leads and commissions should be routed
- whether the implementation should stay inside the current WordPress plugin path or require a separate service
- what must be ready before showing the product to a contractor

## 2. Project And Asset Questions

Ask the relevant stakeholder:

1. Which project should be the first serious contractor demo: Rainbow, Dimri Yama, an urban-renewal pilot, or another project?
2. For that project, do we have a real GLB/3D model, or only facade/photo/plans?
3. Do we have official facade renders from the contractor or only concept art?
4. Do we have floor plans per floor and per unit?
5. Do we have coordinates for every project and, if possible, for each building entrance?
6. Do we have unit-level data: floor, rooms, sqm, balcony, direction, price, availability, view, parking, storage, and delivery date?
7. Do we have Matterport, Cupix, drone, panorama, interior render, or apartment-tour URLs?
8. Are there legal restrictions on showing price, availability, view, or renderings?
9. What asset quality is acceptable for a contractor demo, and what is embarrassing enough that we should hide it?
10. What exact contractor asset checklist should NadLan request before publishing a premium showroom?

## 3. Showroom Product Questions

Ask the relevant stakeholder:

1. What is the minimum impressive flow for a contractor demo?
2. Should the first demo emphasize 3D building, view from apartment, interior tour, map surroundings, AI advisor, or lead conversion?
3. What is the best order on mobile: visual first, unit selector, map/view, plan, interior, lead?
4. Should AI be visible to the public immediately, or start as a gated concierge/lead assistant?
5. What comparison features matter most: price, sqm, floor, direction, view, delivery, payment terms, or financing?
6. What should happen when assets are missing: hide project, show concept fallback, or show asset-intake state?
7. What contractor-facing proof would make a developer pay?

## 4. Business And Monetization Questions

Ask the relevant stakeholder:

1. Who pays first: contractor, buyer, professional, or partner broker?
2. What are the contractor packages: basic listing, premium showroom, lead package, exclusive project, foreign-buyer package?
3. Does NadLan expect referral fees, advertising fees, success fees, subscription, or hybrid?
4. Who owns a lead after it comes in?
5. What lead fields are mandatory before routing?
6. What is the SLA for contacting a serious buyer or investor?
7. Should WhatsApp be the main lead path, or should serious investors go through form plus concierge?
8. What professionals should be monetized first: lawyers, mortgage advisors, appraisers, inspectors, architects, interior designers, tax advisors, property managers?
9. What is the rule for avoiding conflicts of interest when recommending professionals?
10. What should be shown publicly and what should stay internal/admin-only?

## 5. SEO And Market Scope Questions

Ask the relevant stakeholder:

1. Which categories must NadLan win first: new projects, urban renewal, city pages, neighborhood pages, foreign buyers, professionals, or investor guides?
2. Are any topics legally or commercially sensitive?
3. Which Israeli competitors should be treated as direct SEO/product benchmarks?
4. Which commercial pages must exist even if they are hard to rank?
5. Which outbound investment markets matter now: Cyprus, Dubai/UAE, Greece, Thailand, or others?
6. For outbound markets, does NadLan have partners or should the site start with research, guides, and lead qualification?
7. What languages matter first: Hebrew, English, French, Russian, Arabic, Chinese?
8. What is the editorial approval process before publishing AI-assisted content?

## 6. Technical WordPress Questions

Ask the relevant stakeholder:

1. Should the showroom stay in the existing `nadlan-config` plugin, or should it become a separate plugin/module?
2. What custom post types are final: projects, units, compounds, professionals, guides, cities, neighborhoods, destination countries?
3. Which data should live in WordPress meta, which in JSON assets, and which in an external service?
4. Who will maintain Mapbox tokens, geocoding, coordinates, and map styling?
5. Is a multilingual plugin already chosen, or should Codex evaluate WPML/Polylang/custom routing later?
6. Is there an existing CRM, email, WhatsApp, or lead-management destination?
7. Should leads be stored in WordPress first, sent to email/WhatsApp, pushed to CRM, or all three?
8. What security/privacy constraints apply to buyer leads?
9. What caching/CDN constraints exist on UPress?
10. What performance target is acceptable for 3D on mobile?

## 7. Decisions The Stakeholder Can Change

| Stakeholder answer | Build impact |
| --- | --- |
| Real GLB exists | Build model-first unit hotspot flow. |
| Only facade/plans exist | Build facade-first premium fallback, no fake 3D. |
| Matterport/Cupix exists | Add interior-tour tab and deep link flow. |
| No Mapbox token | Build not-ready map state and admin token checklist. |
| Contractor pays first | Prioritize contractor package dashboard and showroom readiness score. |
| Buyer lead funnel pays first | Prioritize qualification, WhatsApp, concierge, and CRM flow. |
| Outbound markets are strategic now | Add country/city/project taxonomy and foreign partner intake. |
| Professionals are strategic now | Add professional vertical pages and referral routing rules. |
| WP plugin path is approved | Implement inside `plugins/nadlan-config/inc/project-3d.php` and related assets. |
| Separate product service is needed | Design API boundary before heavy implementation. |

## 8. Call Summary Template

Paste answers here after the call.

```text
Date:
Participants:

Best first demo project:
Available assets:
Missing assets:
Asset restrictions:

Main buyer flow:
Main contractor pitch:
Lead routing decision:
Monetization decision:

SEO categories to prioritize:
Outbound countries:
Professional verticals:
Languages:

Technical direction:
WordPress/plugin decision:
CRM/WhatsApp/email decision:
Mapbox/data decision:
Performance/caching notes:

Immediate next actions:
Owner decisions still needed:
```

## 9. Current Codex Recommendation Before The Call

Continue the design/prototype run now. Do not wait for the call.

For implementation, use the current WordPress plugin renderer as the first target:

- `plugins/nadlan-config/inc/project-3d.php`
- `assets/css/nadlan-project-showroom.css`
- `assets/projects/rainbow-tel-aviv/`
- `assets/projects/dimri-yama/`

Do not fake assets. Use Rainbow as the model-first technical reference, Dimri as the concept/facade fallback, and the urban-renewal pilot as the low-asset mode.
