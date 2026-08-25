# START HERE — Local GSC OAuth

This is the non-secret locator for the reusable Google Search Console login on
the owner's Windows computer. Future agents must read this before starting a
new GSC session.

## The two OAuth files

The actual files are stored locally, outside every repository:

```text
%USERPROFILE%\Documents\jus-tice-secrets\gsc\gsc-oauth-client.json
%USERPROFILE%\Documents\jus-tice-secrets\gsc\gsc-token.json
```

- `gsc-oauth-client.json` identifies the local Google OAuth Desktop app.
- `gsc-token.json` contains the reusable authorization and refresh token.
- Both files are protected with local NTFS permissions.
- Never print their contents, paste them into chat, add them to a ZIP, upload
  them, or commit them.

## Next-time startup

```powershell
$env:GSC_OAUTH_CLIENT_PATH="$env:USERPROFILE\Documents\jus-tice-secrets\gsc\gsc-oauth-client.json"
$env:GSC_TOKEN_PATH="$env:USERPROFILE\Documents\jus-tice-secrets\gsc\gsc-token.json"
cd "$env:USERPROFILE\Documents\ChatGPT-Work\justice-theme"
node tools/gsc/gsc-universal-pull.js --list-sites
```

If `--list-sites` works, the saved token is reusable and no Google login is
needed. If Google has revoked or expired the authorization, run the local OAuth
flow again; never request or share the secret in chat.

## Verified connection

- Last verified: 2026-08-25
- OAuth scope: `https://www.googleapis.com/auth/webmasters.readonly`
- NadLan property: `sc-domain:nad-lan.co.il`
- Permission at verification: `siteOwner`

The full commands and run history are in `README-GSC-CONNECTION.md`. Private
property listings and GSC data remain under `%USERPROFILE%\Documents\GSC-Data\`.
