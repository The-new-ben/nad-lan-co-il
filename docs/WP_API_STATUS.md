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
| 7 | `mortgage-check` | draft | Mortgage adviser qualification |
| 8 | `buying-checklist` | draft | Buyer checklist lead magnet |
| 9 | `buying-apartment` | draft | Pillar page for buying an apartment |
| 10 | `investment-apartment` | draft | Investment apartment lead capture |
| 11 | `real-estate-lawyer` | draft | Real-estate lawyer service intent |

These are intentionally drafts. Before publishing, add richer Hebrew content, source references, internal links, schema checks, and active calculators/forms.
