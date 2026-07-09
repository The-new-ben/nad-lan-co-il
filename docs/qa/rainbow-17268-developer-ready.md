# Rainbow 1.72.68 Developer-Ready Gate

## Scope

One reversible Rainbow-only composition behind `nadlan_showroom_composed_v2`. The release keeps
the existing SEO article, lead/RFP rails, theme, catalog, calculators, directory, and deployment
pipeline intact.

## Buyer Benchmarks Used

- Zillow new-construction content guidance: complete community media, plans, and buyer details.
- Zillow plan/community pages: price, plan, tour, nearby context, and contact in one journey.
- Yad1 new-project catalog/project pages: availability-led browsing, plans/gallery, nearby places,
  developer identity, and inquiry.

## Preview Proof

- One `#nl-root`, zero legacy showroom roots, one H1.
- Project breadcrumb is first, not buried in article content.
- Project progress retained inside the journey with estimated handover wording.
- Stable packaged Rainbow GLB plus six same-origin plan/drawing files.
- Model/facade switch, unit select, filters, compare, RFP, and studio exercised in Chrome.
- HE/EN/FR/RU/AR labels and text direction verified; no raw translation keys.
- 390px: no horizontal overflow, selected unit returns to model, drawer max height 72%, close target
  44 by 44 pixels.
- SEO article preserved and composed headings forced above paragraphs.

Screenshots:

- `docs/qa/screenshots/rainbow-17268/before-live-top.png`
- `docs/qa/screenshots/rainbow-17268/preview-he-mobile-390.png`
- `docs/qa/screenshots/rainbow-17268/preview-he-mobile-selected-390.png`

## Reversal

Run:

```powershell
$env:NADLAN_WP_USER='<user>'
$env:NADLAN_WP_APP_PASSWORD='<application-password>'
node scripts/rainbow-composition-meta.mjs --rollback
```

The script restores the committed pre-release metadata backup for all five Rainbow sibling pages.
Code rollback is the normal plugin downgrade; no post body is rewritten.

## Live Gate (pending deploy)

- Healthcheck `1.72.68`.
- Packaged GLB and all plan URLs return HTTP 200.
- Model load, rotate, facade, panel, plan, view, tour, filters, compare, RFP, studio, inquiry, and
  language navigation rechecked in live Chrome.
- One H1, one project progress tracker, one breadcrumb, no duplicate project-card/price/map/social
  fragments, no page errors, no horizontal overflow.
