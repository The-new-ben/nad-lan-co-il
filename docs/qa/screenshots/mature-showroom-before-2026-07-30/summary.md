# Mature showroom live baseline - BEFORE - 2026-07-30

Read-only Google Chrome baseline for DUO, Rainbow, Dimri Yama and Ashira across advertised HE/EN/FR/RU/AR siblings at 1440x1000 and 390x844.

- Matrix captured: 40/40
- Static health clean: 0/40
- Pre-existing static defects: 40
- Capture errors: 0
- Deep project families: 4/4
- First-party non-GET attempts: 0
- Regression-ready BEFORE evidence: YES

Regression-ready means the BEFORE evidence can be compared after UTOPIA work. Missing or broken live capabilities remain explicitly classified and are never counted as passes.

## Static matrix

| Project | Language | Viewport | HTTP | Root | Model | Unit selectors | Overflow | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| DUO | he | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | he | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | en | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | en | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | fr | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | fr | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | ru | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | ru | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | ar | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| DUO | ar | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Rainbow | he | desktop | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | he | mobile | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | en | desktop | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | en | mobile | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | fr | desktop | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | fr | mobile | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | ru | desktop | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | ru | mobile | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | ar | desktop | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Rainbow | ar | mobile | 200 | 1 | 1 | 18 | 0 | baseline_defect |
| Dimri Yama | he | desktop | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | he | mobile | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | en | desktop | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | en | mobile | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | fr | desktop | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | fr | mobile | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | ru | desktop | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | ru | mobile | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | ar | desktop | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Dimri Yama | ar | mobile | 200 | 1 | 1 | 12 | 0 | baseline_defect |
| Ashira | he | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | he | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | en | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | en | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | fr | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | fr | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | ru | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | ru | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | ar | desktop | 200 | 1 | 1 | 15 | 0 | baseline_defect |
| Ashira | ar | mobile | 200 | 1 | 1 | 15 | 0 | baseline_defect |

## Deep client-only paths

| Project | Language | Capability | Classification |
|---|---:|---|---|
| DUO | ru | trusted_unit_selection_cinematic | passed |
| DUO | ru | apartment_studio | passed |
| DUO | ru | unified_map | passed |
| DUO | ru | model_to_map_bearing | passed |
| DUO | ru | window_view | passed |
| Rainbow | he | trusted_unit_selection_cinematic | passed |
| Rainbow | he | apartment_studio | passed |
| Rainbow | he | unified_map | passed |
| Rainbow | he | model_to_map_bearing | passed |
| Rainbow | he | window_view | passed |
| Dimri Yama | he | trusted_unit_selection_cinematic | passed |
| Dimri Yama | he | apartment_studio | passed |
| Dimri Yama | he | unified_map | passed |
| Dimri Yama | he | model_to_map_bearing | passed |
| Dimri Yama | he | window_view | passed |
| Ashira | fr | trusted_unit_selection_cinematic | passed |
| Ashira | fr | apartment_studio | passed |
| Ashira | fr | unified_map | passed |
| Ashira | fr | model_to_map_bearing | passed |
| Ashira | fr | window_view | passed |

## Safety boundary

The runner allowed GET requests only. It did not fill or submit forms and did not click WhatsApp, RFP, video-call or co-tour controls. Every blocked request is preserved in the JSON report.

## Re-run command

```powershell
node scripts/qa-mature-showroom-before-2026-07-30.mjs
```

