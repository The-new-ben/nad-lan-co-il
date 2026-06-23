# Live Rainbow model selection QA - 2026-06-23

Scope: verify the live Rainbow Tower showroom after plugin 1.69.2 was installed through WordPress admin.

Result: pass.

What was tested:
- Opened the live Rainbow showroom in Chrome.
- Confirmed the plugin assets were running version 1.69.2.
- Clicked an apartment selector on the actual model area.
- Verified the selected unit state changed to `unit-24-nw`.
- Verified the model camera moved to `camera-orbit: 24deg 61deg auto`.
- Verified the model camera target moved to `camera-target: -6 80 5`.
- Verified the selected-unit card became visible.
- Verified no sampled public-language leak was detected in the selected view.

Evidence files:
- `01-live-1692-before-click.json` - DOM and runtime state before the click.
- `02-live-1692-after-click.json` - DOM and runtime state after the click.
- `03-live-1692-windows-screen-after-click.png` - visible Windows-level screenshot after the live click.

Note: the Chrome extension screenshot API produced blank cream screenshots for this model-viewer stage during this run. The Windows-level screenshot is the visual proof file for the live browser state.
