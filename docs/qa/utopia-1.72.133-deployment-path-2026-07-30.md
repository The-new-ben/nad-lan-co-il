# UTOPIA 1.72.133 deployment-path audit

Date: 2026-07-30  
Scope: deployment-path and rollback audit. The local release verifier and update metadata were corrected after the initial audit; the frozen candidate and plugin runtime were not changed. No production write, upload, plugin install, database change, GitHub push, or deployment was performed.

## Decision

**NO-GO until WordPress administrator authentication and host-level recovery access are available.**

The frozen 1.72.133 candidate is structurally safe and matches the frozen release worktree. Production still reports `nadlan-config 1.72.132`. The current task environment has no authenticated WordPress write path, and installing the plugin alone will not run the guarded UTOPIA content seed. A real authenticated `wp-admin` request is required after installation.

| Gate | Result | Evidence / limit |
|---|---:|---|
| Production baseline | PASS | Public health endpoint reports `nadlan-config 1.72.132`, WordPress 7.0.2, PHP 8.5.5. |
| Candidate frozen | PASS | Candidate lineage was audited at `29cb84cf01b490730701d62119bbef6df101c848`; the subsequent verifier and manifest correction did not change the ZIP or plugin runtime. |
| Candidate ZIP structure | PASS | 231 files, one `nadlan-config/` root, no unsafe paths, no duplicate entries, CRC passes, all 231 entries match the frozen worktree byte-for-byte. |
| Candidate immutable hash | PASS | SHA-256 `5BE7A071233C8A67425408B80BE517DC76119C673C431517EED240684E321E5B`; 3,859,424 bytes. |
| Reconstructed rollback ZIP | CONDITIONAL | 217 files, safe root/path structure, no duplicates, CRC passes, header and constant are `1.72.132`. It has the same file-path set as exact live-source commit `f20db56c7f04b23d302d0779d502f95ded07a6dd`, but raw-byte comparison found 195 differences. These may include checkout line-ending transformations, but that was not normalized/proven before the audit stopped. It is not accepted as an exact live-directory backup. |
| Rollback ZIP hash | RECORDED | SHA-256 `4B47ECE263822D79E4D70740EA1740C9B34D7608CCBC7B80639801328968B1B5`; 2,583,030 bytes. |
| Canonical verifier | PASS | The verifier now resolves the two recognized `NADLAN_CONFIG_VERSION` health expressions, still rejects unknown expressions, and still requires every version surface, update URL, ZIP entry, root, and CRC check to pass. The stale `1.72.110` update manifest was aligned to `1.72.133`. |
| WordPress authentication | BLOCKED | `WP_BASE_URL`, `WP_USER`, and `WP_APP_PASSWORD` are absent. Protected REST endpoints return 401. |
| Host recovery access | UNPROVEN | UPress/File Manager or equivalent recovery login was not available in this task. |
| GitHub transport | BLOCKED | Repository is private; anonymous raw/archive URLs return 404. Production cannot safely fetch the ZIP from a private GitHub URL. |
| Protected release governance | FAIL | No repository runner, release workflow, required checks, or usable branch protection was found. `main` is stale/diverged from the production-source branch and must not be used as the immediate release base. |

## Frozen artifacts

- Candidate: `plugin-dist/nadlan-config-1.72.133.zip`
  - SHA-256: `5BE7A071233C8A67425408B80BE517DC76119C673C431517EED240684E321E5B`
  - Size: 3,859,424 bytes
  - 231 files, including the five localized UTOPIA article payloads
  - Safe ZIP root, no traversal/backslash paths, no duplicates, CRC clean
  - Byte-identical to the frozen worktree at audit time
- Reconstructed source rollback: `plugin-dist/nadlan-config-1.72.132.zip`
  - SHA-256: `4B47ECE263822D79E4D70740EA1740C9B34D7608CCBC7B80639801328968B1B5`
  - Size: 2,583,030 bytes
  - Same 217-path inventory as `f20db56c7f04b23d302d0779d502f95ded07a6dd`
  - Not a copy of the package currently installed on the server
  - Not proven byte-identical to the live directory; use only as secondary recovery

The primary rollback artifact must be a server-side copy of the currently active `nadlan-config` directory captured immediately before installation, with a recorded directory digest. Capture a scoped database backup at the same gate.

## Canonical local build and verification

The repository's guarded builder is:

```powershell
python scripts/build-plugin-zip.py
```

It sorts paths, creates a single `nadlan-config/` root, rejects unsafe paths, and performs a CRC check. It preserves filesystem modification times through `ZipFile.write()`, so it is not fully reproducible byte-for-byte across checkouts.

The intended verifier is:

```powershell
python scripts/verify-plugin-release.py 1.72.133
```

The initial run failed because the verifier only understood quoted health-version literals even though both health responses now use `NADLAN_CONFIG_VERSION`. The verifier was corrected to resolve only the bare constant and the guarded `defined(...) ? NADLAN_CONFIG_VERSION : 'unknown'` expression. Legacy numeric literals remain supported, and unknown expressions fail closed.

That correction exposed a separate release-metadata defect: `plugin-dist/nadlan-config.json` still advertised `1.72.110`. Its version, download URL, date, and changelog were aligned to the frozen `1.72.133` package. The manifest schema has no candidate hash or size fields, so none were invented. Five focused parser tests pass, and the full command now returns `ok: true` with 231 entries, zero backslash paths, one valid root, and a clean CRC. The candidate remains 3,859,424 bytes with SHA-256 `5BE7A071233C8A67425408B80BE517DC76119C673C431517EED240684E321E5B`.

Read-only artifact checks:

```powershell
git status --short --branch
git rev-parse HEAD
Get-FileHash -Algorithm SHA256 plugin-dist\nadlan-config-1.72.132.zip
Get-FileHash -Algorithm SHA256 plugin-dist\nadlan-config-1.72.133.zip
python scripts\verify-plugin-release.py 1.72.133
```

## Exact owner authentication action

Before any production write, the owner must:

1. Confirm that UPress/File Manager or equivalent host-level recovery login works and can restore the active plugin directory even if WordPress fails.
2. In `wp-admin`, create a fresh WordPress Application Password for an administrator with `update_plugins`, `manage_options`, and `unfiltered_html`.
3. Inject these values into the secure Codex task environment, not chat, source files, logs, or Git:

```text
WP_BASE_URL=https://nad-lan.co.il
WP_USER=<administrator username>
WP_APP_PASSWORD=<fresh application password>
```

4. Keep a real authenticated `wp-admin` browser session available. The application password is suitable for protected REST checks, but the UTOPIA seed is guarded by `is_admin()` and should not be assumed to run from a REST request.

After secure injection, verify identity and capabilities read-only at:

```text
GET /wp-json/wp/v2/users/me?context=edit&_fields=id,roles,capabilities
```

Do not paste the password into chat and do not embed a GitHub token in a URL, snippet, or plugin option.

## Safest go-live sequence

1. **Freeze and identify**
   - Require the exact candidate SHA-256 above and a clean immutable candidate commit descending from `f20db56`.
   - Record public health, the five UTOPIA routes, mature comparison projects, and the active plugin version before mutation.

2. **Create recoverable backups**
   - Put a deployment lock in place.
   - Copy the currently active server plugin directory to a timestamped server-side backup and record its digest.
   - Capture a scoped database journal/snapshot covering UTOPIA posts, post meta, terms, attachment/upload state, and UTOPIA release/manifest options.
   - Prove the host recovery login can reach both backups.

3. **Install the exact frozen artifact**
   - Upload the ZIP bytes through an adapted, capability-gated temporary deployment bridge or another authenticated WordPress/host path.
   - Verify the uploaded bytes against candidate SHA-256 before extraction.
   - Install `nadlan-config/nadlan-config.php`; do not use an anonymous GitHub URL because the repository is private.

4. **Run the UTOPIA seed**
   - With the owner/agent logged into the real WordPress admin, load one benign authenticated `wp-admin` page.
   - The new plugin's guarded admin `init` migration should create/update the five localized pages, attachment/upload, metadata, terms, and release options.
   - A plugin-install REST response alone is insufficient because it starts under the old plugin and REST is not `is_admin()`.

5. **Verify dynamic completion**
   - Confirm option `nadlan_utopia_release_v172133` is exactly `1`.
   - Confirm the stored UTOPIA manifest and five published posts have the expected slugs, project identity, canonical URLs, language links, and content hashes.
   - Confirm the media attachment exists and the uploaded file hash matches.
   - Confirm HE, EN, FR, RU, and AR routes return 200 and render the intended page.
   - Run browser acceptance on desktop/mobile, keyboard operation, console/network errors, links, media, apartment/showroom controls, map/view direction, and mature-project regression pages.

6. **Exercise rollback before declaring success**
   - While 1.72.133 code is still loaded, invoke and verify `nadlan_utopia_restore_backup()` through a temporary capability-gated recovery route, verified WP-CLI/admin recovery action, or restore the scoped database journal.
   - Restore the exact server-side pre-release plugin directory backup. Use the reconstructed 1.72.132 ZIP only if the exact server copy is unavailable and the owner explicitly accepts its provenance limitation.
   - Flush caches and verify health is back to 1.72.132, the four newly localized routes return to their prior state, the Hebrew page is restored, and mature projects remain unchanged.

7. **Redeploy the same candidate**
   - Reinstall the same candidate bytes with SHA-256 `5BE7...E5B`.
   - Trigger the admin seed again and repeat dynamic, browser, SEO, multilingual, media, showroom, map, and regression checks.

8. **Cleanup**
   - Delete the temporary deployment/recovery snippet or bridge.
   - Prove its REST route returns 404.
   - Remove temporary uploaded packages only after recovery evidence is retained.
   - Release the lock and record final health, artifact SHA, screenshots, console/network results, and rollback/redeploy evidence.

## Required bridge adaptation

A robust base64 package-upload/rollback driver exists locally in the Complete99 runner and is a useful pattern, but it is not safe to run unchanged. Before use it must be adapted and tested for:

- host `nad-lan.co.il`
- plugin slug `nadlan-config`
- plugin path `nadlan-config/nadlan-config.php`
- UTOPIA-scoped database/content backup and restore
- explicit UTOPIA seed execution and dynamic verification
- no Complete99-specific robots, health, option, or content mutations

The candidate's approximately 3.86 MB raw size fits that driver's 8 MB raw limit, but WordPress/PHP request-size limits must still be checked.

## Hard stops

- No WordPress administrator application password in the secure environment
- No proven host-level recovery access
- No exact server-side active-plugin backup and scoped database backup
- No tested UTOPIA-specific deployment/rollback bridge
- No proof that the post-install admin seed completed
- Any artifact hash other than the frozen SHA-256 recorded above
- Any plan that fetches the private GitHub artifact anonymously or exposes a GitHub credential
- Any plan that merges/deploys from stale `main` merely to satisfy a nominal branch policy

Until these gates are satisfied, retain the release as a frozen local candidate and do not install it on production.
