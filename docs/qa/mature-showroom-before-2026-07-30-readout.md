# Mature showroom live BEFORE readout - 2026-07-30

## Outcome

The read-only Google Chrome baseline is regression-ready.

- Four mature project families were covered: DUO, Rainbow, Dimri Yama and Ashira.
- All 20 live language siblings advertised by the Hebrew pages were discovered from live hreflang or showroom language links.
- All 40 required project/language/viewport cases were captured.
- Viewports were exactly 1440x1000 and 390x844.
- All 40 documents returned HTTP 200.
- All 40 passed language, direction, self-canonical, exact live hreflang, one showroom root, model presence, trusted unit-selector presence and zero-horizontal-overflow checks.
- There were no first-party network failures and no first-party non-GET attempts.
- Ninety-six screenshots were preserved, totaling 31,691,019 bytes.
- The immutable evidence directory contains 98 hashed artifacts plus its SHA-256 manifest. Independent verification found zero missing or mismatched hashes.

## Strict console flag interpretation

The raw report labels all 40 static cases `baseline_defect` because the safety harness deliberately rejected third-party telemetry POSTs. Chrome emitted only this console message:

`Failed to load resource: net::ERR_BLOCKED_BY_CLIENT.Inspector`

No other console-error signature was observed. The guard blocked 176 third-party POST attempts:

- 52 to `https://www.google.com/g/collect`
- 52 to `https://www.google-analytics.com/g/collect`
- 40 to `https://events.mapbox.com/events/v2`
- 32 to `https://m.stripe.com/6`

These are deliberate read-only guard effects, not failed first-party assets or broken showroom interactions. All non-guard static assertions passed in every case. The JSON keeps the strict flag so the evidence is not softened after capture.

## Deep client-only journeys

Each family used a fresh context and its highest-scoring live language. No form was filled or submitted. WhatsApp, RFP, video-call and co-tour controls were not clicked.

| Project | Best live language | Unit selection and cinematic | Studio add, undo, persistence, clear | Unified map facilities, satellite, 3D | Model-to-map bearing | Window view turn and fullscreen |
|---|---|---|---|---|---|---|
| DUO | Russian | Passed | Passed | Passed | Passed | Passed |
| Rainbow | Hebrew | Passed | Passed | Passed | Passed | Passed |
| Dimri Yama | Hebrew | Passed | Passed | Passed | Passed | Passed |
| Ashira | French | Passed | Passed | Passed | Passed | Passed |

## Manual screenshot observation

The representative Rainbow Arabic mobile screenshot has correct Arabic page direction and an Arabic project headline, but visible showroom navigation and CTA labels remain in English. This is a pre-existing localization-quality issue preserved in the BEFORE image, not a UTOPIA regression. The interaction path itself remained functional.

## Evidence

- Raw report: `docs/qa/screenshots/mature-showroom-before-2026-07-30/report.json`
- Human summary: `docs/qa/screenshots/mature-showroom-before-2026-07-30/summary.md`
- SHA-256 manifest: `docs/qa/screenshots/mature-showroom-before-2026-07-30/artifact-manifest.sha256`
- Screenshots: `docs/qa/screenshots/mature-showroom-before-2026-07-30/*.png`
- Runner stdout: `docs/qa/mature-showroom-before-2026-07-30.stdout.log`
- Runner stderr: `docs/qa/mature-showroom-before-2026-07-30.stderr.log`

## Command

```powershell
node scripts/qa-mature-showroom-before-2026-07-30.mjs
```

The runner refuses to overwrite the immutable final baseline directory.
