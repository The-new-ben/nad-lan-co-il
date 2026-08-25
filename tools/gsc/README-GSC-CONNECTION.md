# Local GSC Connection — Non-Secret Handoff

Future agents: read `START-HERE-OAUTH.md`, this file, and `tools/gsc/AGENTS.md`
before running any GSC command. These documents contain paths and commands only;
they never contain credential contents.

## Repositories

- Justice tools: `%USERPROFILE%\Documents\ChatGPT-Work\justice-theme`
- NadLan site reference: `%USERPROFILE%\Documents\ChatGPT-Work\nad-lan-co-il`

## Local credentials

The reusable OAuth Desktop client and refresh token are outside every Git
repository:

- `%USERPROFILE%\Documents\jus-tice-secrets\gsc\gsc-oauth-client.json`
- `%USERPROFILE%\Documents\jus-tice-secrets\gsc\gsc-token.json`

They are restricted with local NTFS permissions. Never print, copy, commit,
upload, or embed either file. The OAuth scope must remain exactly:
`https://www.googleapis.com/auth/webmasters.readonly`.

Set the paths only in the current PowerShell session:

```powershell
$env:GSC_OAUTH_CLIENT_PATH="$env:USERPROFILE\Documents\jus-tice-secrets\gsc\gsc-oauth-client.json"
$env:GSC_TOKEN_PATH="$env:USERPROFILE\Documents\jus-tice-secrets\gsc\gsc-token.json"
```

The token can be reused on this computer until Google revokes it. Do not copy a
refresh token to another computer.

## List properties safely

```powershell
cd "$env:USERPROFILE\Documents\ChatGPT-Work\justice-theme"
node tools/gsc/gsc-universal-pull.js --list-sites
```

The private property registry is stored under
`%USERPROFILE%\Documents\GSC-Data\_registry\`. Never commit it. Choose a property
explicitly; the universal runner intentionally has no fallback.

## Last verified NadLan run

- Verified: 2026-08-25
- Exact property: `sc-domain:nad-lan.co.il`
- Permission at verification: `siteOwner`
- Requested dates: 2026-05-25 through 2026-08-25
- Final data returned: 2026-05-27 through 2026-08-23
- Output directory:
  `%USERPROFILE%\Documents\GSC-Data\nad-lan.co.il\2026-05-25_2026-08-25`

Reproduce the read-only pull:

```powershell
cd "$env:USERPROFILE\Documents\ChatGPT-Work\justice-theme"
node tools/gsc/gsc-universal-pull.js `
  --site="sc-domain:nad-lan.co.il" `
  --start="2026-05-25" `
  --end="2026-08-25" `
  --type="web" `
  --data-state="final" `
  --daily-shards `
  --resume `
  --output-dir="$env:USERPROFILE\Documents\GSC-Data\nad-lan.co.il\2026-05-25_2026-08-25"
```

Build the read-only content inventory and analysis:

```powershell
node tools/gsc/gsc-site-inventory.js `
  --output-dir="$env:USERPROFILE\Documents\GSC-Data\nad-lan.co.il\2026-05-25_2026-08-25"

node tools/gsc/gsc-nadlan-analysis.js `
  --run-dir="$env:USERPROFILE\Documents\GSC-Data\nad-lan.co.il\2026-05-25_2026-08-25"

node tools/gsc/gsc-nadlan-analysis.test.js `
  "$env:USERPROFILE\Documents\GSC-Data\nad-lan.co.il\2026-05-25_2026-08-25"
```

## Safety boundary

These tools read GSC, public WordPress REST, and XML sitemaps. They must not
change WordPress, Search Console, sitemaps, canonicals, robots, slugs, redirects,
content, taxonomies, or internal links. Every migration recommendation requires
manual approval.
