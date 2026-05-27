# NadLan WordPress API Status

Updated: 2026-05-26

## Access

- Site URL: `https://nad-lan.co.il`
- WordPress user: `nadlvzld_admin`
- App password name: `Codex API 2026-05-26`
- Secret storage: local Windows DPAPI encrypted file outside the repo:
  `C:\Users\pro\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json`

Do not commit app passwords or plaintext credentials.

## SSL

uPress SSL/TLS is installed and active. This was required before WordPress would allow Application Password creation.

## REST behavior

- Working REST route style: `https://nad-lan.co.il/?rest_route=/wp/v2/...`
- Pretty REST route verified after permalink flush: `https://nad-lan.co.il/wp-json/` returns JSON.

Automation can keep using the `?rest_route=` form because it is explicit and stable, but public/internal content links should use clean page URLs.

## Published content pages

| ID | Slug | Status | Intent |
| --- | --- | --- | --- |
| 2 | `home` | publish | Static homepage and content hub |
| 6 | `purchase-tax-calculator` | publish | Purchase tax estimate and professional-check page |
| 7 | `mortgage-advisor` | publish | Mortgage adviser qualification page |
| 8 | `apartment-buying-checklist` | publish | Buyer checklist page |
| 9 | `buying-apartment` | publish | Pillar page for buying an apartment |
| 10 | `investment-apartment` | publish | Investment apartment evaluation page |
| 11 | `real-estate-lawyer` | publish | Real-estate lawyer service-intent page |
| 17 | `new-projects` | publish | New-project / contractor apartment fit page |
| 18 | `tabu-extract-check` | publish | Tabu extract / ownership-check page |

Updated: 2026-05-27 13:31 UTC. The homepage is now a static page and the first eight content pages are public. WordPress permalink settings were saved to `Post name`, and verification confirmed HTTP 200 responses, unique clean URLs for the inner pages, and no visible operating-language leak in the checked public text.

Updated: 2026-05-27. Draft IDs 7 and 8 were normalized from `mortgage-check` and `buying-checklist` to the production slugs above. Draft IDs 17 and 18 were created as the missing production-priority pages from `docs/MONEY_PAGE_BRIEFS.md`.

## Public content upgraded

Updated: 2026-05-27 04:53 UTC

The eight money/pillar pages were upgraded through the WordPress REST API with conversion-focused Hebrew copy, official-source notes, qualification tables, consumer-facing CTAs, stronger internal linking, and no-guarantee legal/tax/mortgage/investment guardrails. All eight were later made public after public-language cleanup.

See `docs/WP_DRAFT_UPDATE_LOG.md` for the full operational log.
