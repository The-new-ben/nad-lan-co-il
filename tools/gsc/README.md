# GSC API Tool - Quick Start

## Credential Safety

`oauth-client.json`, `gsc-token.json`, app-password files and other credential JSON files must stay local and untracked.

Recommended local credential paths:
- OAuth client: `tools/gsc/oauth-client.json`
- OAuth token: `tools/gsc/gsc-token.json`

If a real OAuth client JSON was ever committed, create a new OAuth client in Google Cloud and delete or rotate the old one.

## First Time On A New PC

```bash
cd tools/gsc
npm install googleapis open
node gsc-pull.js
```

Browser opens, then log in with the Google account that has Search Console access and approve the read-only flow. Token saves locally. Next runs are automatic.

## After First Time

```bash
cd tools/gsc
node gsc-pull.js
```

No browser needed: token auto-refreshes.

## Family / Divorce First Export

Use this runner for the first controlled Family/Divorce upload risk check. It supports credential paths outside the repo and a safe dry run.

PowerShell:

```powershell
$env:GSC_OAUTH_CLIENT_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-oauth-client.json"
$env:GSC_TOKEN_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-token.json"
node tools/gsc/gsc-family-divorce-export.js --dry-run
node tools/gsc/gsc-family-divorce-export.js
```

Outputs save under `reports/gsc/family-divorce-YYYY-MM-DD/`.

One-command workflow after credentials are configured:

```powershell
$env:GSC_OAUTH_CLIENT_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-oauth-client.json"
$env:GSC_TOKEN_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-token.json"
.\tools\gsc\run-family-divorce-gsc-workflow.ps1 -DryRun
.\tools\gsc\run-family-divorce-gsc-workflow.ps1
```

This wrapper runs the focused export, builds the Family/Divorce GSC decision map, then rebuilds the protected URL owner-review packet for the same report date. Use `-SkipExport -OutputDir "reports\gsc\family-divorce-YYYY-MM-DD" -ReportDate "YYYY-MM-DD"` to rebuild decision files from an existing focused export without calling GSC again.

After the export, build the protected URL / cannibalization decision map:

```powershell
node tools/build-family-divorce-gsc-decision-map.mjs --gscDir="reports/gsc/family-divorce-YYYY-MM-DD" --reportDate="YYYY-MM-DD"
node tools/build-family-divorce-protected-url-review-packet.mjs --reportDate="YYYY-MM-DD" --input="reports/family-divorce-protected-url-decision-map-YYYY-MM-DD.csv"
```

Without `--gscDir`, the decision-map builder can use the older cached `reports/gsc/` CSVs as a baseline only. Treat that baseline as `NOT_FINAL` until the focused export is reviewed.

## Priority Cluster Export

Owner-facing command packet:

- `project-control/gsc-owner-execution-packet-2026-05-22.md`

Use the packet for the ordered owner flow: credential paths, preflight, dry run, read-only export, strict output validation, and the explicit no-public-change boundary.

Before the first real export, run the local preflight. It checks paths, local packages, Git hygiene and optional dry-run wiring without opening OAuth or calling GSC:

```powershell
$env:GSC_OAUTH_CLIENT_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-oauth-client.json"
$env:GSC_TOKEN_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-token.json"
.\tools\gsc\check-gsc-oauth-preflight.ps1 -RunPriorityDryRun
```

After owner OAuth setup, this runner executes the three upload-blocking focused exports in sequence:

- Family/Divorce
- Criminal Law
- Medical Malpractice

Dry run:

```powershell
.\tools\gsc\run-priority-cluster-gsc-exports.ps1 -DryRun
```

Full read-only export after credentials:

```powershell
$env:GSC_OAUTH_CLIENT_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-oauth-client.json"
$env:GSC_TOKEN_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-token.json"
.\tools\gsc\run-priority-cluster-gsc-exports.ps1
.\tools\gsc\check-priority-gsc-export-output.ps1 -WriteReport
```

Single cluster:

```powershell
.\tools\gsc\run-priority-cluster-gsc-exports.ps1 -Clusters family
.\tools\gsc\run-priority-cluster-gsc-exports.ps1 -Clusters criminal
.\tools\gsc\run-priority-cluster-gsc-exports.ps1 -Clusters medical
```

Review all generated decision maps before any CMS upload, URL migration, redirect, canonical/noindex, sitemap, taxonomy or internal-link action.

The validator is intentionally strict. It blocks missing focused export folders, missing required files, malformed CSV headers, empty page/query/protected-source exports and decision maps that still come from baseline cache/dashboard data instead of `FOCUSED_GSC_EXPORT`.

## Criminal Law First Export

Use this runner for the controlled Criminal Law upload risk check. It exports the five Criminal first-upload current URLs, protected/support pages, route-fallback candidates and Criminal query terms without changing the site.

PowerShell:

```powershell
$env:GSC_OAUTH_CLIENT_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-oauth-client.json"
$env:GSC_TOKEN_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-token.json"
.\tools\gsc\run-criminal-gsc-export.ps1 -DryRun
.\tools\gsc\run-criminal-gsc-export.ps1
```

The full wrapper now runs the read-only export and then builds the Criminal decision maps for the same report date:
- `reports/criminal-gsc-decision-map-YYYY-MM-DD.csv`
- `reports/criminal-protected-url-decision-map-YYYY-MM-DD.csv`
- `reports/criminal-cannibalization-decision-map-YYYY-MM-DD.csv`
- `reports/criminal-gsc-decision-map-YYYY-MM-DD.json`

Manual commands:

```powershell
node tools/gsc/gsc-criminal-export.js --dry-run
node tools/gsc/gsc-criminal-export.js
node tools/build-criminal-gsc-decision-map.mjs --gscDir="reports/gsc/criminal-law-YYYY-MM-DD" --reportDate="YYYY-MM-DD"
```

Outputs save under `reports/gsc/criminal-law-YYYY-MM-DD/`:
- `criminal-law-pages.csv`
- `criminal-law-query-page.csv`
- `criminal-law-cannibalization.csv`
- `criminal-law-protected-sources.csv`
- `criminal-law-summary.json`

Review the export before any Criminal clean-slug migration, redirect, canonical, noindex or sitemap decision.

Without `--gscDir`, the Criminal decision-map builder can use the readiness dashboard and older cached GSC CSVs as a baseline only. Treat that baseline as `NOT_FINAL` until the focused Criminal export is reviewed.

## Medical Malpractice First Export

Use this runner for the controlled Medical Malpractice upload risk check. It reads the latest `medical-malpractice-readiness-dashboard-YYYY-MM-DD.csv` to scope the primary pillar, protected/support pages, route candidates and boundary exclusions.

PowerShell:

```powershell
$env:GSC_OAUTH_CLIENT_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-oauth-client.json"
$env:GSC_TOKEN_PATH="C:\Users\janana\Documents\jus-tice-secrets\gsc-token.json"
.\tools\gsc\run-medical-malpractice-gsc-export.ps1 -DryRun
.\tools\gsc\run-medical-malpractice-gsc-export.ps1
```

The full wrapper runs the read-only export and then builds Medical Malpractice decision maps for the same report date:
- `reports/medical-malpractice-gsc-decision-map-YYYY-MM-DD.csv`
- `reports/medical-malpractice-protected-url-decision-map-YYYY-MM-DD.csv`
- `reports/medical-malpractice-cannibalization-decision-map-YYYY-MM-DD.csv`
- `reports/medical-malpractice-gsc-decision-map-YYYY-MM-DD.json`

Manual commands:

```powershell
node tools/gsc/gsc-medical-malpractice-export.js --dry-run
node tools/gsc/gsc-medical-malpractice-export.js
node tools/build-medical-malpractice-gsc-decision-map.mjs --gscDir="reports/gsc/medical-malpractice-YYYY-MM-DD" --reportDate="YYYY-MM-DD"
```

Outputs save under `reports/gsc/medical-malpractice-YYYY-MM-DD/`:
- `medical-malpractice-pages.csv`
- `medical-malpractice-query-page.csv`
- `medical-malpractice-cannibalization.csv`
- `medical-malpractice-protected-sources.csv`
- `medical-malpractice-summary.json`

Review the export before any Medical Malpractice clean-slug migration, redirect, canonical, noindex, sitemap, taxonomy or internal-link decision.

Without `--gscDir`, the Medical Malpractice decision-map builder uses the readiness dashboard as a baseline only. Treat that baseline as `NOT_FINAL` until the focused Medical Malpractice export is reviewed.

## Output

Reports saved to `reports/gsc/`:
- `performance-pages.csv`: all pages with clicks/impressions/position for 12 months.
- `performance-queries.csv`: all queries for 12 months.
- `query-page-combined.csv`: query and page pairs for 3 months.
- `cannibalization-report.csv`: queries competing across multiple pages.

## Sites Available

All sites owned by the authenticated Google account in Google Search Console.

To change the target site, edit `SITE_URL` at the top of `gsc-pull.js`.

## Token File

`gsc-token.json` is created locally and listed in `.gitignore`. Never commit it.

## Universal Multi-Site Pull

For a reusable, exact-property, read-only export, read
[`README-GSC-CONNECTION.md`](README-GSC-CONNECTION.md) first and use
`gsc-universal-pull.js`. The runner never falls back to another property and
supports full-range pagination, daily shards, resume checkpoints, controls,
reconciliation, a run manifest, and SHA-256 hashes.

The NadLan analysis workflow uses these additional read-only tools:

- `gsc-site-inventory.js` — public WordPress REST and XML sitemap inventory.
- `gsc-nadlan-analysis.js` — multi-URL query classification and migration inventory.
- `gsc-nadlan-analysis.test.js` — numerical, ordering, and safety QA.

Raw GSC data, property registries, tokens, and generated reports belong outside
the repository. Do not commit or publish them.
