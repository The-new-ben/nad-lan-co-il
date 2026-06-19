# Dimri Yama Showroom Preview QA

Local preview:

`http://127.0.0.1:8765/docs/previews/dimri-yama-showroom-preview.html`

## What Was Checked

- Desktop 1440px: poster, intro, 3D context area, facade picker, selected apartment card, tabs, buyer form, and article hierarchy render in one coherent showroom flow.
- Tablet 768px: model and facade stack cleanly in the captured viewport.
- Mobile pass: `scripts/dimri-cdp-mobile-qa.mjs` runs Chrome through DevTools device metrics at a true 390px viewport. It reported `clientWidth=390`, `scrollWidth=390`, `overflow=0`, 4 unit cells, and the buyer form present.
- Mobile journey pass: the same script selected B-15, filled the preview-only form, submitted it, and confirmed the message carries the selected apartment context.
- The model is present as context only. Apartment selection happens on the static facade, which matches the owner decision.
- Public copy is buyer-facing and avoids internal words such as funnel, CRM, SEO, or leads.
- The selected-apartment buyer form is present in the theme pattern and sends selected unit context to the shared `/nadlan/v1/lead` endpoint when used on WordPress.

## Screenshots

- `docs/qa/screenshots/dimri-yama-preview/desktop-1440-v9.png`
- `docs/qa/screenshots/dimri-yama-preview/tablet-768-v9.png`
- `docs/qa/screenshots/dimri-yama-preview/mobile-390-cdp-v1.png`
- `docs/qa/screenshots/dimri-yama-preview/mobile-390-cdp-form-v1.png`

## Honest Status

This is a local prototype preview, not a live deployment. It proves the intended Dimri Yama product structure and mobile-safe layout before production code is touched. It still needs official project assets before a public page can be presented as official: BIM/GLB, approved facade/elevation, plans, inventory, availability, prices, and contractor contact details.

Chrome CLI note: the simple `--window-size=390` screenshot mode rendered the CSS viewport as 476px and cropped the output image to 390px. That made the earlier raw mobile screenshot conservative and visually cropped. The CDP mobile pass above is the trustworthy 390px check.
