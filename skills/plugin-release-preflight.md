# Plugin Release Preflight

Use this skill before any NadLan Config plugin release is committed, merged, uploaded, or handed to
the owner for a WordPress update.

## Why

The live server was previously damaged by a plugin ZIP built with Windows/backslash archive paths.
On Linux/uPress those paths can become junk files or phantom plugin entries. A release also becomes
confusing when the plugin header, healthcheck, manifest, ZIP filename, or asset cache-busters do not
agree.

This skill is the release safety stop. If it fails, do not ask the owner to update the plugin.

## Required Commands

Run the canonical builder:

```bash
python scripts/build-plugin-zip.py <version>
```

Then run the verifier:

```bash
python scripts/verify-plugin-release.py <version>
```

The verifier checks:

- plugin header version,
- main healthcheck version,
- `inc/health.php` version,
- manifest version,
- manifest `download_url`,
- expected ZIP filename,
- ZIP CRC,
- zero backslash paths,
- every entry rooted at `nadlan-config/`,
- every plugin source file present inside the ZIP.

## Pass Criteria

The verifier must print JSON with:

```json
{
  "ok": true,
  "zip": {
    "backslash_paths": 0,
    "rooted": true,
    "crc": "ok"
  }
}
```

If the verifier fails, fix the package or version surfaces first. Do not merge, deploy, or tell the
owner to update.

## Notes

- Do not use Windows Explorer, PowerShell `Compress-Archive`, `tar.exe`, or ad-hoc ZIP commands for
  this plugin.
- Do not assume a GitHub merge updated production. Production changes only after the owner updates
  the plugin in WordPress and live `/wp-json/nadlan/v1/healthcheck` reports the new version.
- If PHP is unavailable locally, say so explicitly and leave `php -l` for the reviewer/deploy gate.

## Revision Log

- 2026-06-15 - Created by Codex after the 1.66.x ZIP-path incident. Pairs with
  `scripts/build-plugin-zip.py` and `scripts/verify-plugin-release.py`.
