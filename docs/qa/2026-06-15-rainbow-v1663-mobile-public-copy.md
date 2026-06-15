# Rainbow v1.66.3 Mobile Containment And Public Copy QA

## Scope

This is a surgical patch only. It does not redesign the Rainbow showroom and it does not change the
project data model. It fixes four verified live/template failures:

1. The 390px and Edge-mobile showroom root is shifted outside the viewport.
2. After selecting an apartment on mobile, the model scene collapses to a 2px strip.
3. The live Rainbow body still contains old internal public wording such as lead panel / leads.
4. The rendered social image URL is same-site HTTP instead of HTTPS.

## Live Baseline Before Patch

Command:

```bash
node scripts/qa-project-showroom-visual.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --out docs/qa/screenshots/rainbow-v1-surgical-before --strict
```

Result:

- Passed: 0
- Failed: 4

Measured failures:

| Viewport | Failure |
| --- | --- |
| desktop-1440 | public text contains internal wording |
| tablet-768 | public text contains internal wording |
| mobile-390 | showroom cropped; public text contains internal wording |
| edge-mobile-390 | showroom cropped; public text contains internal wording |

Key metrics from the live page before this patch:

| Metric | Value |
| --- | --- |
| mobile root before selection | x 183.5, width 362, right 545.5 on a 390px viewport |
| mobile scene before selection | height 483.6 |
| mobile scene after selection | height 2 |
| desktop pick count | 6 |
| desktop apartment-cell count | 6 |
| model-viewer defined | true |
| visible H1 count | 1 |

Screenshots are saved under:

`docs/qa/screenshots/rainbow-v1-surgical-before/`

## Fix Summary

1. Reinstates the mobile edge correction by allowing `--nlp3d-mobile-nudge` to affect the showroom
   root. A late mobile `transform:none!important` was cancelling the JavaScript correction.
2. Adds a selected-state mobile guard so `.nlp3d-scene` keeps a real height after the apartment
   card opens.
3. Adds a one-shot Rainbow public-copy cleanup that replaces old internal wording with buyer-facing
   inquiry language.
4. Adds `project_page_assembly.rainbow_public_copy_v1663` to healthcheck so the live seed can be
   verified after deployment.
5. Normalizes same-site Yoast/dynamic `og:image` and `twitter:image` URLs to HTTPS.
6. Aligns plugin header, healthcheck, manifest, ZIP and showroom cache-busters at 1.66.3.

## Local Package Checks

ZIP build:

```bash
python scripts/build-plugin-zip.py 1.66.3
```

Observed result:

```text
OK nadlan-config-1.66.3.zip entries=130 backslash=0 rooted=True crc=ok
```

JavaScript syntax checks:

```bash
node --check scripts/qa-project-showroom-visual.mjs
node --check scripts/qa-project-showroom-live.mjs
node --check scripts/build-project-showroom-payload.mjs
node --check scripts/import-project-showroom-payload.mjs
```

Observed result: all passed.

PHP lint was not run locally because this Windows shell does not have a `php` binary available.
Reviewer should run `php -l` on the changed PHP files before deploy.

## Post-Deploy Gate

After merge and plugin update:

1. Pull or sync the UPress server Git copy.
2. Update NadLan Config to 1.66.3.
3. Clear UPress cache.
4. Open `/wp-json/nadlan/v1/healthcheck`.
5. Confirm:

```json
{
  "version": "1.66.3",
  "og_image": {
    "https_normalizer": true
  },
  "project_page_assembly": {
    "rainbow_public_copy_v1663": true
  }
}
```

6. Rerun:

```bash
node scripts/qa-project-showroom-visual.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --out docs/qa/screenshots/rainbow-v1663-after --strict
```

Expected live improvements:

- mobile root starts near x 0 and right edge stays inside the viewport;
- mobile scene remains at least 380px high after apartment selection;
- public text no longer contains internal wording;
- rendered `og:image` uses `https://`;
- no new console errors;
- one visible H1 remains;
- apartment cells and model-viewer remain present.

## Honest Risk Note

This patch stabilizes the current Rainbow template. It does not solve the larger product question:
the final selector should use apartment-shaped cells embedded into a facade or a true per-unit GLB,
not abstract marker dots. That work belongs in a separate, carefully gated product slice.
