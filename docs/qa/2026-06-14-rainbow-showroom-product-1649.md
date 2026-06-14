# Rainbow showroom product QA - v1.64.9

## Scope

v1.64.9 is a buyer-decision-card polish slice on top of v1.64.8 mobile containment.

The owner feedback was that the showroom is close, but the apartment selection still does not feel
like a clear product-shopping moment. This slice keeps the existing 3D/model-viewer/selectUnit
plumbing and improves the selected-apartment moment without changing the lead endpoint or CMS data
contract.

## Fix

- Selected apartment card now renders buyer-facing tags from unit data:
  - recommended,
  - availability/status,
  - view,
  - price-estimate context.
- The selected card gets status-aware visual treatment through `data-status` and `data-recommended`.
- The card note explains the buyer's next step:
  - estimated price stays non-binding,
  - reserved unit asks the buyer to verify availability,
  - sold unit points to comparison/alternate selection,
  - available unit points to developer contact.
- Active stage apartment markers now set `aria-pressed="true"`.
- Healthcheck flag: `project_3d.buyer_card_v1649`.

## Public-Copy Guard

No public string in this slice uses internal terms such as lead, funnel, CRM, supplier, monetization
or implementation wording.

## Local Package Gate

Required before shipping:

- ZIP: `plugin-dist/nadlan-config-1.64.9.zip`
- ZIP integrity: clean
- ZIP root: `nadlan-config/`
- Backslash paths: 0
- Inline project-3D JavaScript: `node --check` clean
- PHP lint: not run locally because this Windows shell does not have `php`

## Live Gate Required After Plugin Update

- Healthcheck reports `version: 1.64.9`
- Healthcheck reports `project_3d.mobile_edge_guard_v1648: true`
- Healthcheck reports `project_3d.buyer_card_v1649: true`
- 390px mobile: showroom left edge is inside the viewport
- 390px mobile: tap visible apartment marker opens selected-apartment card
- 390px mobile: selected card shows tags and non-binding price wording
- 1440px and 768px: no horizontal overflow, one H1, no console errors

## Live Status During Build

Production still reported `version: 1.64.6` while this package was prepared, so the buyer-card
change is not live until the WordPress plugin updater installs 1.64.9.
