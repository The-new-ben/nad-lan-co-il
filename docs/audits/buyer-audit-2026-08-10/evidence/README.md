# Live-audit evidence

This directory contains read-only browser captures from 10 August 2026, the scripts that produced them, and portable sanitized JSON copies.

## What to review

- `screenshots/`: every current selected-floor tool on ToHa2 and THE PARK at mobile and desktop viewports.
- `current-*.png`: page-state overview captures.
- `*-visible-text.txt`: rendered text snapshots used to inspect language, terminology and disclosure placement.
- `sanitized/*.json`: structured measurements and observations safe for the handoff ZIP.
- `*.mjs`: reproducibility helpers. They are evidence tools, not product code.

The raw JSON files created by the probes are deliberately not shipped in the final ZIP because live Mapbox requests can expose a public browser token and ephemeral request identifiers. Run `node sanitize-evidence.mjs` after a fresh capture and review the resulting `sanitized/` files before sharing.

## Reproduction requirements

Use Node.js with the `playwright` package and a compatible Chromium installation in an isolated audit folder. For example, after your organization approves live read-only testing:

1. Install Playwright in that audit folder.
2. Install its Chromium browser.
3. Run one probe at a time from the extracted package root.
4. Do not submit contact, appointment, RFP, WhatsApp or share actions.
5. Store fresh raw output only in the local `evidence/` directory; sanitize it before transfer.

The scripts derive their output directory from their own location and contain no workstation-specific path. They target the public URLs listed in source. Because a live site changes, a rerun is new evidence and must carry a new timestamp; it does not retroactively alter this package’s findings.

Emulated viewport results are not a substitute for the physical-device gates in `migration-and-qa.md`.

