# NadLan Ashira Factory Run ZIP Intake

Date: 2026-06-26
Source file: `C:\Users\pro\Downloads\NadLan Ashira Factory Run.zip`
Inspection path: `%TEMP%\nadlan-ashira-factory-run-inspect`

## Verdict

Yes, this ZIP helps, but not as production code.

Use it as:

- visual reference for the showroom direction;
- asset reference for the kind of hero/facade image the owner likes;
- interaction reference for embedded apartment cells on a real-looking facade;
- reminder that the buyer-facing page needs language chips, inventory state, unit facts, plan/view/tour tabs and an environment section.

Do not import it as-is because:

- `Rainbow Showroom.dc.html` is an inline-style generated prototype, not maintainable WordPress/theme code;
- `support.js` is generated prototype runtime, not a product JS file;
- the prototype uses Rainbow-specific assets and copy, while Ashira needs its own public-source facts and assets;
- importing the HTML directly would recreate the same stacking/maintenance problem the v2 reset is meant to stop.

## Useful ZIP Contents

| File | Use | Notes |
|---|---|---|
| `assets/projects/rainbow-tel-aviv/tower-clean.jpg` | Strong visual reference | 902x916, 1.6 MB. High-quality tower/facade image with highlighted apartments. New to this checkout. Useful as a design reference, not Ashira content. |
| `assets/projects/rainbow-tel-aviv/rainbow-showroom-hero-v1664.jpg` | Existing visual reference | Already exists in repo. Wide hero with 3D/model/apartment-picker messaging. |
| `screenshots/01-qa.png` and `screenshots/panel.png` | UI reference | Shows the desired facade-embedded apartment cells and selected-unit panel hierarchy. |
| `assets/projects/rainbow-tel-aviv/plans/*.svg` | Plan-tab pattern | Good reference for how the selected apartment card can show plans. |
| `Rainbow Showroom.dc.html` | Prototype anatomy only | Inline styles and generated templating. Extract ideas only. |
| `support.js` | Do not use | Generated runtime for the prototype. Not suitable for production WordPress theme. |

## Design Lessons To Carry Into Ashira v2

1. A real-looking facade image makes apartment selection understandable immediately.
2. Apartment cells should sit on the building, not float beside it.
3. The selected-apartment panel should show floor, rooms, sqm, balcony, view and status before the form.
4. The tabs `תכנית`, `מבט`, `סיור` are the right buyer sequence.
5. The environment section belongs below the selector, with public district facts.
6. Language chips are useful, but the first v2 build can keep language pages as separate URLs until a multilingual architecture is selected.

## Action For Clean v2

Build Ashira with new `.nlv2-*` theme assets and use this ZIP only as a visual reference. Do not copy the inline HTML or generated runtime. If any image is copied later, store it under a clearly named reference folder or the correct project asset folder with source notes.
