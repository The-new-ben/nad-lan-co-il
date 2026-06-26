# Ashira V2 Preview Factory Gate

Date: 2026-06-26
Branch: `codex/ashira-showroom-v2-clean`

## Scope

This slice adds a repeatable screenshot-first QA gate for clean v2 showroom previews. It runs a
local HTTP server, opens the preview in Google Chrome through Playwright, captures screenshots at
desktop, tablet, mobile and Edge-mobile sizes, and writes a machine-readable report.

It does not contact WordPress, import a draft, publish content, build a plugin ZIP or deploy the
site.

## Command

```powershell
node scripts\qa-showroom-v2-preview.mjs --preview docs\previews\ashira-showroom-v2-preview.html --out docs\qa\screenshots\ashira-v2-preview-factory-gate --strict
```

Shortcut:

```powershell
npm run qa:showroom-v2-preview
```

## Screenshot Proof

Output folder:

`docs/qa/screenshots/ashira-v2-preview-factory-gate/`

Screenshots:

- `desktop-1440-initial.png`
- `desktop-1440-selected.png`
- `tablet-768-initial.png`
- `tablet-768-selected.png`
- `mobile-390-initial.png`
- `mobile-390-selected.png`
- `edge-mobile-390-initial.png`
- `edge-mobile-390-selected.png`

Report:

- `report.json`

## Gate Results

| Check | Result |
|---|---|
| Chrome screenshot pass at 1440 | PASS |
| Chrome screenshot pass at 768 | PASS |
| Chrome screenshot pass at 390 | PASS |
| Edge-mobile UA pass at 390 | PASS |
| Horizontal overflow | PASS, `0` |
| `model-viewer` registered | PASS |
| One `model-viewer` element | PASS |
| One H1 | PASS |
| Old `.nlps` / `.nlp3d` roots absent | PASS |
| Apartment cells present | PASS, `5` |
| Minimum tap target | PASS, desktop/tablet `54x46`, mobile `50x44` |
| Selected card overlaps facade | PASS, `false` |
| Visible Hebrew present | PASS |
| Mojibake visible | PASS, none |
| Internal wording visible | PASS, none |

## Honest Limits

- This proves the local clean v2 preview only. It is not proof that a WordPress post has been
  created or that the live site has changed.
- The GLB and facade remain prototype assets until official Ashira material is approved.
- The script is a pre-import factory gate. A separate live-page gate is still required after any
  WordPress import or deployment.
