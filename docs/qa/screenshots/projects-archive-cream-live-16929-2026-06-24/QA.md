# Projects Archive Cream Skin QA

Date: 2026-06-24  
Live plugin version: 1.69.29  
URL checked: https://nad-lan.co.il/projects/

## Result

Pass for this slice. The live Projects archive now uses the cream editorial skin instead of the old dark archive hero. The mobile viewport is contained at 390px with no horizontal overflow.

## Evidence

- `desktop-1280.png`
- `mobile-390.png`
- `chrome-public-projects.png` - deployment evidence from the logged-in Chrome session. This image includes the WordPress admin bar, so it is not used as the clean public screenshot.
- `results.json`

## Checks

- Live healthcheck reports `nadlan-config` version `1.69.29`.
- WordPress admin updater downloaded `plugin-dist/nadlan-config-1.69.29.zip` and reported successful installation.
- Desktop width: `1280`, scroll width: `1280`.
- Mobile width: `390`, scroll width: `390`.
- Hero background computed as cream gradient: `#FAF7F1` to `#F3EEE3`.
- Hero and H1 color computed as ink: `#1B1A17`.
- Visible text scan found no banned internal terms from the QA list.
- Visible text scan found no em dash.

## Honest Limitations

- This release changes the archive visual skin only. It does not solve the broader image quality problem across all project cards.
- Rainbow uses a real project image. Several other project cards still reuse generic-looking luxury or tower imagery and need a later real-asset pass.
- The public card provenance `data.gov.il` is still visible. That is source transparency, not an internal work term, but it should be reviewed in the next content polish pass.
