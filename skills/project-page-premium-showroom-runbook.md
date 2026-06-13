# Project Page Premium Showroom Runbook

Use this skill when turning a real-estate project page into a flagship, replicable project showroom
for NadLan. The target is a buyer-ready, investor-search-ready, contractor-demo-ready page, not a
plain WordPress article.

## A. Source And Intent Research

1. Search Hebrew and English SERP for the project name, developer, neighborhood and price intent.
2. Open the official project site, developer page, compound/city page, Madlan/Yad2 if permitted,
   and news sources that report sales or construction milestones.
3. Record only public or licensed facts: developer, units, floors, amenities, status, notable
   public sales, price per sqm ranges, transport, parks and risks.
4. If numbers conflict, show the conflict. Example: developer marketing count vs municipal permit
   count. Truth-first is part of the NadLan brand.
5. Do not publish paid-source rows or subscription-only data until the owner approves the license
   and public wording.

## B. Page Assembly

1. One URL only, under `/projects/<latin-slug>/`.
2. Keep one visible H1.
3. Place the interactive model immediately after breadcrumbs and before the old static profile card.
4. Wrap the model with `<!-- nlp3d-start -->` and `<!-- nlp3d-end -->`.
5. Add a concise source-backed content block with:
   - buyer summary,
   - price/availability disclaimer,
   - project facts,
   - FAQ visible in the body.
6. Seed schema meta before `wp_head`, never on `the_content` render:
   - `amenities`,
   - `official_site_url`,
   - `price_range`,
   - `price_min`,
   - `price_max`,
   - `project_faq_json`.

## C. 3D And Buyer Interaction

1. Default view is the building selector, not the map.
2. The buyer can drag or tap angle controls to rotate/spin.
3. Clickable floors/units update the selected-unit card, facts, compare tray, sun insight and lead
   payload.
4. Map view is user-opened and lazy-loaded to control Mapbox costs.
5. Register Mapbox RTL text plugin before creating a map with Hebrew labels.
6. Drawings, floor plans and real inventory are optional CMS fields. If absent, show a clear request
   path instead of faking a plan.
7. Price can be:
   - official unit price,
   - explicit unit estimate,
   - project average per sqm estimate,
   - or `לפי פנייה`.
   Anything estimated must say `אומדן` and `לא מחייב`.

## D. Lead And WhatsApp Funnel

1. Every CTA must enter the same lead CPT and routing rails.
2. Site forms use `/nadlan/v1/lead`.
3. WhatsApp messages should use a secret-gated bridge such as `/nadlan/v1/wa-lead`; never rely on a
   click-to-chat link as the only funnel.
4. Always send `card_id` when known. If unknown, route to admin fallback and log attribution gap.
5. Lead payload should preserve unit, floor, sqm, building, timeline, budget, advisor and
   non-binding purchase intent.

## E. Browser QA Gate

Check real Chrome or Playwright at:

- 390px mobile,
- 760px tablet,
- 1440px desktop.

Pass criteria:

- no horizontal overflow,
- no raw JavaScript text visible,
- no page errors,
- 44px tap targets,
- building selector is visible quickly,
- drag changes model angle,
- unit click updates facts and card,
- view button opens map only on demand,
- Hebrew map labels are not reversed,
- floating buttons do not cover forms or footer,
- schema contains visible FAQ-aligned data.

## F. Deployment Reminder

After a PR is merged:

1. Pull/sync the uPress/server Git copy.
2. Trigger or upload the WordPress plugin update.
3. Hard refresh the page.
4. Check `/wp-json/nadlan/v1/healthcheck` for the new version and feature blocks.

GitHub merge alone does not update production.
