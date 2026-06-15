# Rainbow v1.66.3 Readiness Check

Date: 2026-06-15  
Branch: `codex/rainbow-v1-surgical`  
Target PR: runtime surgical patch for NadLan Config `1.66.3`  
Live production during this check: `1.66.2`

## Package Preflight

Command:

```powershell
python scripts\build-plugin-zip.py 1.66.3
```

Result:

- OK `nadlan-config-1.66.3.zip`
- entries: 130
- backslash paths: 0
- rooted under `nadlan-config/`: true
- CRC: ok

Release verification:

```powershell
python scripts\verify-plugin-release.py 1.66.3
```

- plugin header: `1.66.3`
- main healthcheck version: `1.66.3`
- `inc/health.php` version: `1.66.3`
- manifest version: `1.66.3`
- manifest download URL points to `nadlan-config-1.66.3.zip`
- every plugin source file is present in the ZIP
- no extra ZIP entries
- key runtime files are present in ZIP:
  - `inc/project-page-assembly.php` with `rainbow_public_copy_v1663`
  - `inc/og-image.php` with Yoast OpenGraph/Twitter HTTPS normalizer
  - `inc/project-3d.php` with mobile containment, stage-card and model-viewer markers

Package status: ready for review/deploy from a ZIP-safety perspective.

## Live Structural QA On Production 1.66.2

Command:

```powershell
node scripts\qa-project-showroom-live.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464
```

Result:

- passed: 23
- failed: 0
- live version: `1.66.2`
- one H1
- model-viewer exists
- model-viewer script tag is `type="module"`
- model-viewer hotspots exist
- selected-apartment action card exists
- buyer inquiry and contractor request forms exist
- SEO title and meta are transaction-led

Interpretation: the structural contract is healthy on live `1.66.2`, but this is not enough to call
Rainbow template-ready.

## Live Visual QA On Production 1.66.2

Command:

```powershell
node scripts\qa-project-showroom-visual.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv
```

Result:

- passed viewports: 0
- failed viewports: 4

Failures:

- desktop 1440: public text contains internal wording
- tablet 768: public text contains internal wording
- mobile 390: showroom cropped and public text contains internal wording
- Edge mobile 390: showroom cropped and public text contains internal wording

Important measured mobile symptom:

- root right edge: `545.5` on a `390` px viewport
- stage right edge: `534.5` on a `390` px viewport

Interpretation: live `1.66.2` still has the user-visible failures that the owner reported. This is
the evidence that the goal is not yet complete on production.

## Template Gate On Production 1.66.2

Command:

```powershell
node scripts\qa-project-template-gate.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464 --min-version 1.66.3 --strict
```

Result:

- passed: 20
- failed: 5
- informational: 1
- template_ready: false

Failures:

1. live plugin version is `1.66.2`, below required `1.66.3`
2. `project_page_assembly.rainbow_public_copy_v1663` is not live
3. `og:image` is still HTTP
4. public visible text still contains internal words
5. visual Chrome showroom gate was not run inside the template gate

Interpretation: the public page is not yet a replicable template source. PR `1.66.3` is expected to
close the first four failures after deployment; then the visual gate must be rerun.

## Next Safe Action

1. Review and merge the `1.66.3` runtime patch only if the package preflight stays green.
2. Pull/sync the UPress server Git copy.
3. Update NadLan Config to `1.66.3`.
4. Clear UPress cache.
5. Verify `/wp-json/nadlan/v1/healthcheck` reports `version: 1.66.3`.
6. Rerun:

```powershell
node scripts\qa-rainbow-postdeploy.mjs --version 1.66.3 --out docs/qa/rainbow-postdeploy-1.66.3.json

# Or run the individual gates:
node scripts\qa-project-showroom-live.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464
node scripts\qa-project-showroom-visual.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv
node scripts\qa-project-template-gate.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464 --min-version 1.66.3 --visual --strict
```

Do not clone Rainbow to another Sde Dov project until the template gate is green.
