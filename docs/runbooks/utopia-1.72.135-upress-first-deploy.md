# UTOPIA 1.72.135 uPress-first deployment, rollback, and redeploy runbook

Date: 2026-07-30

Target: `https://nad-lan.co.il`

Plugin: `nadlan-config`

Live baseline: `1.72.134`

Candidate: `1.72.135`

This is the manual, fail-closed production procedure for the first UTOPIA
1.72.135 deployment. It covers recovery preparation, the WordPress upload and
replacement flow, the guarded five-language seed, public acceptance, the
complete AFTER regression, an actual rollback, and redeployment of the identical
candidate.

It does not authorize a different artifact, an in-place source edit, an old
deployment bridge, a Code Snippets workaround, or a change to shared showroom
code.

## Current decision

The candidate is frozen and locally validated. Production deployment remains
**NO-GO** until all of the following are true:

1. The owner is authenticated to the exact uPress production installation for
   `nad-lan.co.il`.
2. A fresh uPress database backup and a fresh files backup that includes
   `wp-content/uploads/` have completed.
3. The uPress restore interface shows both backups as selectable and restorable.
4. The owner has made and recorded the explicit decision about the 42 exposed
   backup-suffixed files described below.
5. A no-write maintenance window is active for the rollback and identical
   redeploy exercise.
6. Production still reports exactly `nadlan-config 1.72.134`.
7. The exact active plugin manifest still matches the recorded 1.72.134 server
   baseline.
8. The administrator used for the seed has `manage_options` and
   `unfiltered_html`.

The current uPress browser tab is at its login screen, and the required uPress
database backup is still pending. Do not upload or replace the plugin while
either condition remains unresolved.

The WordPress dashboard 404 is not a seed blocker. The following authenticated
admin surfaces have been verified:

| Surface | Verified result | Use |
|---|---:|---|
| `/wp-admin/plugins.php` | 200 | Plugin replacement, activation check, and fresh non-AJAX seed request |
| `/wp-admin/admin.php?page=file_manager_advanced_ui` | 200 | Emergency plugin-directory access |
| `/wp-admin/index.php` | 404 | Do not use; it is not required for this release |

The candidate registers its seed on `init`. It accepts any genuine non-AJAX
`is_admin()` request made by the current user when that user has
`manage_options` and `unfiltered_html`. Therefore, a fresh authenticated GET of
`/wp-admin/plugins.php` is the verified seed trigger after installation.
`admin-ajax.php`, REST, a public page, and a simulated admin context are not
substitutes.

## Frozen release identity

Deploy only this file:

```text
C:\Users\pro\nad-lan-utopia-release-1.72.135\plugin-dist\nadlan-config-1.72.135.zip
```

Its immutable identity is:

| Property | Required value |
|---|---|
| SHA-256 | `edf5644d5151d3e3302eb68598a48d68e2a66d4cc5f99f961bf150336d2d52b6` |
| Size | `3,862,340` bytes |
| ZIP entries | `231` |
| Root | `nadlan-config/` |
| Release source commit | `44a4c62a1c116f4474dad20d2a05f76c7cd1d207` |
| Artifact freeze commit | `89211d6d87082c06f3e70c028d96c7628ae56780` |
| ZIP CRC | clean |
| Unsafe, backslash, duplicate, missing, extra, or mismatched entries | `0` |

Do not rebuild, recompress, rename, patch, or source the candidate from another
checkout. Recompute its local SHA-256 immediately before selecting it in the
WordPress upload dialog. A mismatch of one byte stops the deployment.

The release verifier must pass against the frozen bytes:

```powershell
Set-Location 'C:\Users\pro\nad-lan-utopia-release-1.72.135'
python -B scripts\verify-plugin-release.py 1.72.135
(Get-FileHash -Algorithm SHA256 'plugin-dist\nadlan-config-1.72.135.zip').Hash.ToLowerInvariant()
(Get-Item 'plugin-dist\nadlan-config-1.72.135.zip').Length
```

Expected final two values:

```text
edf5644d5151d3e3302eb68598a48d68e2a66d4cc5f99f961bf150336d2d52b6
3862340
```

The source review or protected production-branch approval must refer to these
exact commits and this exact artifact hash. If landing or approving the release
changes the ZIP, the approval does not transfer to the new bytes.

## Verified live-server recovery artifact

An authenticated direct download of the active 1.72.134 plugin directory is
already preserved outside the repository:

| Property | Recorded value |
|---|---|
| Archive | `nadlan-config-live-1.72.134-server-directory.zip` |
| SHA-256 | `30f562f2bd3b42fdc4150d8f10c26e13a75ddffc3e01a46068fde659dd228245` |
| Size | `3,081,950` bytes |
| Entries | `259` |
| CRC | clean |
| Unsafe or duplicate entries | `0` |
| Sorted content-manifest SHA-256 | `3c5df5b9c2a8e2199eba79d0a1a77dab92ded468d57ea7c15201a621c432cfd3` |
| Header and runtime constant | `1.72.134` |

All 217 files from authoritative live source commit
`064567a50466c3c1245f1abcc4e699144949492d` are present on the server.
Eight raw-byte differences reduce to zero substantive differences after newline
normalization.

This exact server archive is the primary plugin-directory rollback artifact.
The local `nadlan-config-1.72.134-source-reconstruction.zip` is secondary
recovery only. It must not replace the exact server archive in this procedure.

The exact plugin archive is necessary but not sufficient. The release also
changes WordPress posts, options, attachment records, and a file under uploads.
A fresh uPress database backup and a fresh files/uploads backup are mandatory.

## Owner decision required for 42 exposed extras

The active server directory also contains 42 files that do not exist in the
authoritative 1.72.134 source:

- 38 PHP backup files
- 3 JavaScript backup files
- 1 CSS backup file

Every one has a backup-style suffix. At least one sampled file is publicly
downloadable over HTTP. This is a wider production defect that has been
surfaced, not altered.

A standard WordPress whole-plugin replacement may remove these 42 extras when
it replaces the `nadlan-config` directory. That would be a change beyond the
UTOPIA file set even though it would also remove exposed backup material.
Before installation, the owner must record one of these two decisions:

```text
APPROVED: replace nadlan-config with the exact 1.72.135 ZIP, accepting that the
standard replacement may remove the 42 recorded backup-suffixed extras. Preserve
the exact 1.72.134 server archive for rollback and evidence.
```

or:

```text
DECLINED: do not deploy 1.72.135. Prepare a separate reviewed plan for the 42
backup-suffixed extras before replacing the plugin.
```

If the decision is declined, unclear, or not recorded, stop. Do not copy the 42
files into the candidate, reinsert them after replacement, merge directories by
hand, or silently convert this release into a cleanup release.

After installation, inventory the active directory again and record whether the
42 extras remain. Do not claim that UTOPIA removed or preserved them unless the
post-install inventory proves it.

## Prohibited deployment paths

The following paths are not permitted:

- Do not run the old 1.72.133 driver or bridge.
- Do not adapt `scripts/deploy-utopia-1.72.133.py`.
- Do not load `deploy/utopia-1.72.133-bridge.php`.
- Do not create a temporary Code Snippets route.
- Do not use `admin-ajax.php` to imitate a seed.
- Do not use a nonce-bearing URL as a deployment mechanism.
- Do not fetch the artifact from an anonymous GitHub raw URL. The repository is
  private and anonymous raw requests return 404.
- Do not put a GitHub token, WordPress password, cookie, nonce, or uPress
  credential in a URL, command line, source file, screenshot, or audit record.
- Do not deactivate and delete the active plugin before upload.
- Do not extract files individually over the active directory.
- Do not rebuild 1.72.135 after approval.
- Do not proceed if production advances beyond the recorded 1.72.134 baseline.

The preferred and approved ingress path is WordPress:

```text
Plugins > Add New Plugin > Upload Plugin > Install Now > Replace current with uploaded
```

If that authenticated upload flow is unavailable, rejects the package, or does
not present an unambiguous replacement confirmation, stop. Do not improvise a
bridge or a partial File Manager copy during the production window.

## Evidence record

Create a private deployment record before the first live write. It must contain:

- deployment ID and UTC start time
- operator, owner approver, and QA reviewer
- target host `https://nad-lan.co.il`
- live baseline version and health response hash
- candidate filename, size, SHA-256, source commit, and freeze commit
- exact server plugin archive SHA-256 and manifest SHA-256
- fresh uPress database backup reference
- fresh uPress files/uploads backup reference
- fingerprints of the opaque uPress references for any shareable audit
- restore-interface proof for both backups
- recorded owner decision about the 42 extras
- no-write window start and end times
- initial install, seed, acceptance, rollback, and redeploy timestamps
- cache-purge timestamps
- post-install and post-rollback active-directory manifests
- final health, five URLs, AFTER report, screenshots, and reviewer decision

Keep credentials and authorization headers out of the record. If a screenshot
shows account details, backup secrets, cookies, nonces, or personal data, redact
it before it enters the retained evidence set.

## Gate 1 - Start the no-write maintenance window

An actual database and uploads restore can discard writes made after the
baseline snapshot. The rollback exercise must therefore run in a controlled
no-write window.

1. Confirm the owner-approved start time and a recovery operator who will remain
   available until final redeploy passes.
2. Use the host's supported maintenance or write-freeze process so no posts,
   leads, form submissions, comments, orders, media, options, or other WordPress
   writes can be accepted from the baseline backup through final acceptance.
3. Keep authenticated uPress and WordPress recovery access available.
4. Confirm there is no concurrent WordPress deployment, plugin update, content
   edit, backup restore, or cache operation.
5. Record the UTC start time and the mechanism used.

If a true no-write window cannot be guaranteed, do not perform the rollback
exercise and do not call the deployment complete.

## Gate 2 - Prove current production has not advanced

Use fresh, cache-busted reads.

1. Request:

   ```text
   https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?nlcb=<unique-UTC-value>
   ```

2. Require the plugin version to be exactly `1.72.134` and dependencies to be
   healthy.
3. In `/wp-admin/plugins.php`, require `nadlan-config` to be active and displayed
   as 1.72.134.
4. Download the active `wp-content/plugins/nadlan-config/` directory again
   through authenticated File Manager.
5. Build the same sorted per-entry content manifest and require:

   ```text
   3c5df5b9c2a8e2199eba79d0a1a77dab92ded468d57ea7c15201a621c432cfd3
   ```

6. Capture the current status, final URL, and body hash for all five UTOPIA
   routes and the mature comparison set before installation.

If the health version, plugin header, authoritative file inventory, any file
content, or the server manifest has changed, production has advanced. End the
window without installing. Rebase UTOPIA on the new live source, reserve a new
release version, rebuild, revalidate, and obtain a new approval. Never force
1.72.135 over a newer live release.

## Gate 3 - Create and prove uPress recovery

In the authenticated uPress account, select the exact production installation
serving `nad-lan.co.il`. Verify the domain and environment twice before creating
or restoring anything.

1. Create a fresh full database backup.
2. Create a fresh files backup that explicitly includes:
   - `wp-content/plugins/nadlan-config/`
   - `wp-content/uploads/`
   - any host metadata required for a complete files restore
3. Wait for both jobs to reach a completed state. "Queued", "running", or a
   downloaded archive without a restore record is insufficient.
4. Open the uPress restore interface and prove that both completed backups are
   listed, selectable, and associated with the correct production site.
5. Record their timestamps and opaque references in the private deployment
   record. Store only fingerprints in shareable evidence.
6. Verify enough free space exists for the active plugin, uploaded package,
   exact plugin backup, files/uploads backup, and temporary replacement copy.
7. Keep the previously verified exact server plugin archive available outside
   WordPress and outside the directory being replaced.

The WordPress File Manager database-access probe produced a critical error and
is not a database recovery path. Do not substitute it for the uPress database
backup and restore control.

If either backup cannot be restored from the visible uPress interface, stop
before uploading the candidate.

## Gate 4 - Verify the administrator and upload surface

1. Open `/wp-admin/plugins.php` in the authenticated browser.
2. Require HTTP 200, the real Plugins screen, the expected production domain,
   and no login redirect.
3. Confirm that the current account has `manage_options` and
   `unfiltered_html`. Use an authenticated, read-only capability check or the
   site's trusted administrator record. Do not infer both capabilities merely
   from seeing the admin bar.
4. Open `Plugins > Add New Plugin > Upload Plugin`.
5. Confirm the upload limit exceeds 3,862,340 bytes.
6. Keep authenticated File Manager open in a separate recovery tab.
7. Reconfirm the exact local candidate SHA-256 and size.

The seed also refuses AJAX. The final trigger must be a normal full-page request
to `/wp-admin/plugins.php`.

## Last-chance prewrite checklist

Immediately before selecting "Install Now", all boxes must be true:

- [ ] Owner approved the exact 1.72.135 artifact hash.
- [ ] Owner recorded the decision about possible removal of the 42 extras.
- [ ] Live health is still exactly 1.72.134.
- [ ] Active plugin content-manifest SHA-256 is still `3c5df5...32cfd3`.
- [ ] Exact server plugin archive SHA-256 is still `30f562f2...228245`.
- [ ] Fresh uPress database backup is complete and visible in Restore.
- [ ] Fresh uPress files/uploads backup is complete and visible in Restore.
- [ ] Exact 1.72.134 plugin archive is available outside the active directory.
- [ ] No-write window is active.
- [ ] File Manager recovery tab is authenticated.
- [ ] `/wp-admin/plugins.php` is authenticated and returns 200.
- [ ] Seed user has `manage_options` and `unfiltered_html`.
- [ ] Local candidate is 3,862,340 bytes with SHA-256 `edf5644d...d2d52b6`.
- [ ] No other deployment or update is running.

Any unchecked item stops the release.

## Initial installation through WordPress

1. In `Plugins > Add New Plugin > Upload Plugin`, select only:

   ```text
   nadlan-config-1.72.135.zip
   ```

2. Select `Install Now`.
3. Require WordPress to identify the existing `nadlan-config` destination and
   present the standard replacement comparison.
4. Verify the screen distinguishes current 1.72.134 from uploaded 1.72.135.
5. Select `Replace current with uploaded`.
6. Wait for the request to complete. Do not refresh during extraction or
   replacement.
7. Require a success result and return to the Plugins screen.
8. Require `nadlan-config` to remain active and display 1.72.135.

Do not click an unrelated plugin action. Do not deactivate, delete, or reinstall
from the WordPress directory.

If the replacement reports an error, the plugin disappears, the active version
is ambiguous, or the site returns 500, stop acceptance and follow the recovery
section. An installer success message is not deployment proof.

## Trigger and verify the guarded UTOPIA seed

The replacement request may load new code at a different point in its lifecycle.
Always use a separate fresh request for the seed.

1. After replacement completes, make one normal authenticated full-page GET:

   ```text
   https://nad-lan.co.il/wp-admin/plugins.php
   ```

2. Wait for the response to finish. Do not use AJAX and do not repeatedly
   refresh if it is slow.
3. If the request times out or errors, inspect release-control state before
   making another admin request.
4. Through the authenticated database viewer, identify the real WordPress table
   prefix. Run read-only queries only.

Successful release-control state is:

```text
nadlan_utopia_release_v172135          = "1"
nadlan_utopia_release_v172135_manifest = present and valid
nadlan_utopia_release_v172135_run      = absent
nadlan_utopia_release_v172135_error    = absent
nadlan_utopia_release_v172135_hold     = absent
nadlan_utopia_release_v172135_lock     = absent
```

Example read-only query, after replacing `<table_prefix>` with the exact prefix:

```sql
SELECT option_name, option_value
FROM <table_prefix>options
WHERE option_name IN (
  'nadlan_utopia_release_v172135',
  'nadlan_utopia_release_v172135_manifest',
  'nadlan_utopia_release_v172135_run',
  'nadlan_utopia_release_v172135_error',
  'nadlan_utopia_release_v172135_hold',
  'nadlan_utopia_release_v172135_lock'
)
ORDER BY option_name;
```

The successful result has exactly the completion row and manifest row. The four
run/error/hold/lock rows must not exist.

Do not require the internal UTOPIA backup option to be absent and do not delete
it manually. It is recovery material.

The stored manifest must contain:

- schema-compatible release data for `1.72.135`
- five post IDs keyed by `he`, `en`, `fr`, `ru`, and `ar`
- Hebrew post ID `4749`
- five exact article hashes:
  - HE: `fdc161bc1c760ec28baebaebf529daf1f84d36d02641419e52e1ed88e1fc1da9`
  - EN: `a7cb8b69c50a9cc5bb1f2370bd22871589ddb68bf45c2651421a070eda903fe5`
  - FR: `d344bafb736b0f56aaa4a5a0f1db59007556632c170983edb2a7f3c489fcbb51`
  - RU: `a004900d6e9dff39fa626ea04be3e65db0f95e962c567badc3309a75db5412ea`
  - AR: `9793250681d45fe6c34d1b480755488d3fb606b06fdfa24ca22657ece854248b`
- model SHA-256
  `ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24`
- model triangle count `21416`
- the exact reviewed runtime-asset hashes

Verify the five records are published `nadlan_project` posts with these exact
slugs and identities:

| Language | Slug | Identity marker |
|---|---|---|
| Hebrew | `utopia-sde-dov` | `nadlan-utopia:lot-103:base-4749:he` |
| English | `utopia-sde-dov-en` | `nadlan-utopia:lot-103:base-4749:en` |
| French | `utopia-sde-dov-fr` | `nadlan-utopia:lot-103:base-4749:fr` |
| Russian | `utopia-sde-dov-ru` | `nadlan-utopia:lot-103:base-4749:ru` |
| Arabic | `utopia-sde-dov-ar` | `nadlan-utopia:lot-103:base-4749:ar` |

For each post, require:

- published status
- exact self-canonical in `_yoast_wpseo_canonical`
- exact reviewed article content
- expected language and direction
- the verified UTOPIA identity marker
- the same verified concept attachment as featured media

If completion is absent, the manifest is wrong, or any run/error/hold/lock row
exists, do not clear options or force another seed. Preserve the state, capture
the error evidence, and restore the complete baseline bundle.

## Verify installed plugin bytes and the 42-extra outcome

After a successful seed:

1. Download the active `wp-content/plugins/nadlan-config/` directory through
   authenticated File Manager.
2. Build a sorted per-entry hash manifest.
3. Require every one of the 231 candidate ZIP entries to be present and
   byte-identical to the frozen candidate.
4. Require the header and runtime constant to be 1.72.135.
5. Inventory any files beyond the 231 candidate entries.
6. Record specifically whether the 42 former backup-suffixed extras are absent
   or still present.

Any candidate-file mismatch is a failed installation. Additional unexpected
files are not silently accepted. Preserve the inventory and stop for review.

## Cache purge

Use the authenticated uPress cache-control surface to purge the site/page cache
and CDN cache after:

1. initial install and seed
2. baseline rollback
3. final identical redeploy and seed

Record each purge and its UTC time. Always verify with fresh cache-busted
requests after the purge. A cached 1.72.135 header or asset URL is not proof that
the active plugin and database state are correct.

## Five-language public acceptance

After seed and cache purge, all five exact URLs must return 200 without a
redirect:

```text
https://nad-lan.co.il/projects/utopia-sde-dov/
https://nad-lan.co.il/projects/utopia-sde-dov-en/
https://nad-lan.co.il/projects/utopia-sde-dov-fr/
https://nad-lan.co.il/projects/utopia-sde-dov-ru/
https://nad-lan.co.il/projects/utopia-sde-dov-ar/
```

Public health must report:

- plugin version `1.72.135`
- healthy dependencies
- UTOPIA release `1.72.135`
- five languages enabled
- model asset validated
- `official_model=false`
- `model_kind=independent_concept`
- `model_triangles=21416`
- building mode enabled
- empty apartment inventory

For every language page, verify:

- one correct self-canonical
- a reciprocal unique hreflang target for HE, EN, FR, RU, and AR
- `x-default` pointing to Hebrew
- no conflicting canonical or hreflang target
- correct `<html lang>` and `dir`; HE and AR are RTL, EN/FR/RU are LTR
- language-specific title and meta description with UTOPIA and Tel Aviv first
- the correct buyer-facing opening and project facts
- the localized shared non-affiliation notice appears once, before the showroom
- one H1 and the nine expected H2 sections
- article length remains above 5,000 useful words:
  - HE 6,539
  - EN 7,442
  - FR 9,304
  - RU 7,762
  - AR 6,777
- all source links are real and reachable
- the six intended internal links are present and point to the mortgage
  calculator, purchase-tax calculator, contractor-purchase guide, Tel Aviv city
  page, and the other reviewed internal destinations
- no broken images, scripts, styles, plans, or model request
- no unexpected console error, uncaught exception, mixed-content request, or
  failed first-party network request

Verify the showroom truth contract:

- the GLB response is 309,148 bytes with SHA-256
  `ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24`
- the model renders as 21,416 triangles and 14 meshes
- all four building-level selections work with mouse, keyboard, and touch
- building selection updates only verified building facts
- seven published sample-plan groups and 29 published plan references are
  represented as examples, not inventory
- no exact apartment stack, official BIM, availability, view cone, apartment
  facing, or floor-specific window view is invented
- the apartment inventory remains honestly empty
- the model and four concept images are identified as independent concepts, not
  official sales renderings
- map location is presented as the planning-lot centroid, not an apartment or
  postal-address guarantee
- controls, language switcher, plan links, media, and map remain usable on
  desktop and mobile

Capture desktop and mobile screenshots before interaction and after each
material showroom state. Keep the public page free of internal QA language,
operator notes, and deployment disclaimers.

## Full read-only AFTER regression

Run the AFTER gate from the validated QA checkout that contains the immutable
BEFORE evidence and `scripts/qa-utopia-after-regression.mjs`. Do not move,
rewrite, or regenerate the BEFORE directory.

First validate the runner and live preflight:

```powershell
node scripts\qa-utopia-after-regression.mjs --self-test
node scripts\qa-utopia-after-regression.mjs --expected-version 1.72.135 --preflight-only
```

Then run the full visible Chrome capture:

```powershell
node scripts\qa-utopia-after-regression.mjs --expected-version 1.72.135 --headed
```

The runner is read-only. It blocks non-GET browser requests and must not fill or
submit a lead, contact, design, or sales form.

Require an exit code of zero and retained evidence for:

- UTOPIA in five languages at desktop and mobile sizes
- all 10 UTOPIA language/viewport cases
- the exact model hash and public release state at both start and end
- DUO, Rainbow, Dimri Yama, and Ashira
- all 20 mature-project language siblings
- all 40 mature desktop/mobile cases
- all 20 deep mature journeys
- trusted unit selection and cinematic transition where mature projects support
  them
- apartment studio/design flow
- unified map
- model-to-map bearing
- window view
- console, network, link, image, map, and model checks
- immutable BEFORE hash verification
- start/end health and route stability

Review the generated BEFORE/AFTER screenshots side by side. A human reviewer
must record that mature project layout and behavior remain equivalent, with no
unexpected change caused by UTOPIA. A green summary without the screenshot
review is not enough.

If a wider pre-existing defect is observed, record it separately. Do not repair
shared code during this UTOPIA deployment.

## Mandatory rollback exercise

The first manual replacement path is not production-proven until an actual
restore and identical redeploy pass. Keep the no-write window active.

After initial installation, seed, five-language acceptance, and the first full
AFTER pass:

1. Record the current 1.72.135 health, database completion state, installed
   plugin manifest, uploads inventory, and screenshot evidence.
2. In uPress, select the exact pre-release database backup and the exact
   pre-release files/uploads backup recorded for this deployment.
3. Restore both as one controlled recovery operation. Do not expose the site
   between the database and files halves.
4. If the host files restore does not restore the plugin directory exactly,
   restore the exact server plugin archive with SHA-256
   `30f562f2bd3b42fdc4150d8f10c26e13a75ddffc3e01a46068fde659dd228245`.
5. Purge all uPress site/CDN caches.
6. Independently require:
   - public health is back to 1.72.134
   - active plugin header and runtime constant are 1.72.134
   - active plugin content-manifest SHA-256 is
     `3c5df5b9c2a8e2199eba79d0a1a77dab92ded468d57ea7c15201a621c432cfd3`
   - the five UTOPIA route statuses and hashes match the captured pre-release
     baseline
   - the pre-release database and uploads state is restored
   - DUO, Rainbow, Dimri Yama, and Ashira still match immutable BEFORE behavior
7. Preserve the rollback evidence. Do not end the maintenance window.

If either the database or files/uploads restore fails, do not continue to
redeploy. Keep writes blocked, preserve all recovery material, and escalate to
uPress recovery support.

## Redeploy the identical candidate

After the baseline rollback is independently proven:

1. Recompute the candidate hash and size again.
2. Require the same exact values:

   ```text
   edf5644d5151d3e3302eb68598a48d68e2a66d4cc5f99f961bf150336d2d52b6
   3862340
   ```

3. Repeat the standard WordPress
   `Add New Plugin > Upload Plugin > Replace current with uploaded` flow.
4. Do not rebuild or reuse a browser-cached upload under a different name.
5. Require the plugin to be active at 1.72.135.
6. Make a fresh full-page authenticated GET to `/wp-admin/plugins.php`.
7. Re-run every release-control, manifest, post, media, and active-directory
   verification.
8. Purge uPress site/CDN caches.
9. Re-run five-language public acceptance.
10. Re-run the full headed AFTER regression and human side-by-side review.

Only the second, identical deployment can become the final live state.

## Failure and emergency recovery

### Failure before replacement

Stop with production unchanged. Preserve the backups and evidence. Do not create
a bridge or try another artifact.

### WordPress replacement error while admin and uPress still work

Keep the no-write window active. Inspect the active plugin version and files
without making another replacement attempt. Restore the paired uPress
database/files backup and the exact plugin archive as needed, purge caches, and
prove 1.72.134 before ending the incident.

### Site, admin, or REST returns 500

Use authenticated uPress File Manager:

1. Rename only `wp-content/plugins/nadlan-config` to a deployment-specific
   `.off` name.
2. Restore the exact saved 1.72.134 server directory.
3. Restore the paired pre-release database and files/uploads backup.
4. Purge caches.
5. Verify 1.72.134 health and baseline routes.

Do not delete the failed directory until recovery evidence is complete. Do not
edit PHP live to repair the release.

### Seed request fails or times out

Do not keep refreshing `plugins.php`. Read the completion, manifest,
run/error/hold/lock state first. Preserve the exact state and error. Do not
delete release-control options by hand. Use the paired rollback bundle or a
separately reviewed recovery action.

### Candidate health succeeds but content is incomplete

Treat this as a failed release. Plugin health proves code loading, not the
database seed. Restore the paired baseline and investigate offline.

### Cached pages disagree with authoritative state

Purge through uPress, use unique cache-busting values, and re-read. If
authoritative plugin, database, and body evidence still disagree, stop. Do not
accept asset query strings or a cached health response as proof.

### Production advances during the window

Stop immediately. If no candidate write occurred, end safely with the new live
state untouched. If a candidate write already occurred, use the deployment's
paired backups to return to the exact recorded baseline, then investigate the
concurrent change. Never overwrite the advance blindly.

## Completion gate

UTOPIA 1.72.135 is live only when every item below is proven:

- [ ] Owner approved the exact candidate and the 42-extra decision.
- [ ] Fresh uPress database and files/uploads backups are complete and
      restorable.
- [ ] Exact 1.72.134 plugin archive and manifest are retained.
- [ ] Initial replacement used only the exact frozen ZIP.
- [ ] Initial installed candidate entries match the ZIP byte-for-byte.
- [ ] Seed completion is `1` and the manifest is exact.
- [ ] Run, error, hold, and lock options are absent.
- [ ] Five published language posts and the concept upload are verified.
- [ ] Five public URLs return 200 with correct canonical and hreflang data.
- [ ] Model, plan, media, map, and apartment-inventory truth checks pass.
- [ ] Initial full AFTER regression and side-by-side review pass.
- [ ] Paired database/files/uploads rollback restores exact 1.72.134 state.
- [ ] Identical candidate SHA-256 is reverified before redeploy.
- [ ] Final seed and active-directory verification pass.
- [ ] Final five-language acceptance passes.
- [ ] Final full AFTER regression and side-by-side review pass.
- [ ] Cache is purged and fresh reads prove 1.72.135 at the end.
- [ ] No bridge, snippet, staged package, credential, nonce, or temporary
      recovery route was introduced.
- [ ] The 42-extra post-install outcome is recorded without an unreviewed
      follow-up mutation.
- [ ] The no-write window is ended only after final acceptance.

Retain the exact candidate, exact baseline plugin archive, uPress backup
references, database/files restore proof, initial and final AFTER evidence,
screenshots, hashes, and decision log until the owner accepts the deployment.
Do not delete recovery material merely because the final page looks correct.

The final handoff must include these five live URLs:

- `https://nad-lan.co.il/projects/utopia-sde-dov/`
- `https://nad-lan.co.il/projects/utopia-sde-dov-en/`
- `https://nad-lan.co.il/projects/utopia-sde-dov-fr/`
- `https://nad-lan.co.il/projects/utopia-sde-dov-ru/`
- `https://nad-lan.co.il/projects/utopia-sde-dov-ar/`

It must also link the final AFTER report, the immutable BEFORE evidence, the
side-by-side screenshot review, the rollback/redeploy record, and the
non-secret artifact and server-backup manifests.
