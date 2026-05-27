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
- Needs cleanup: `https://nad-lan.co.il/wp-json/...` currently returns the front-end HTML instead of JSON.

Until the pretty REST route is fixed, automation should use the `?rest_route=` form.

## Draft money pages created

| ID | Slug | Status | Intent |
| --- | --- | --- | --- |
| 6 | `purchase-tax-calculator` | draft | Purchase tax calculator lead capture |
| 7 | `mortgage-advisor` | draft | Mortgage adviser qualification |
| 8 | `apartment-buying-checklist` | draft | Buyer checklist lead magnet |
| 9 | `buying-apartment` | draft | Pillar page for buying an apartment |
| 10 | `investment-apartment` | draft | Investment apartment lead capture |
| 11 | `real-estate-lawyer` | draft | Real-estate lawyer service intent |
| 17 | `new-projects` | draft | New-project / contractor apartment lead capture |
| 18 | `tabu-extract-check` | draft | Tabu extract / ownership check education and legal-routing lead |

These are intentionally drafts. Before publishing, add richer Hebrew content, source references, internal links, schema checks, and active calculators/forms.

Updated: 2026-05-27. Draft IDs 7 and 8 were normalized from `mortgage-check` and `buying-checklist` to the production slugs above. Draft IDs 17 and 18 were created as the missing production-priority pages from `docs/MONEY_PAGE_BRIEFS.md`.

## Draft content upgraded

Updated: 2026-05-27 04:53 UTC

The eight draft money/pillar pages were upgraded through the WordPress REST API with conversion-focused Hebrew draft copy, official-source notes, qualification tables, CRM-ready CTAs, stronger internal linking, and no-guarantee legal/tax/mortgage/investment guardrails. All eight remain `draft`.

See `docs/WP_DRAFT_UPDATE_LOG.md` for the full operational log.
