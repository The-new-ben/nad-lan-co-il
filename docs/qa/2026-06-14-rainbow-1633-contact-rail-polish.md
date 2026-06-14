# Rainbow v1.63.3 Contact Rail Polish QA

## Scope

Stacked on top of PR #165 / v1.63.2. This is a narrow showroom polish slice for the owner-observed problem where the floating WhatsApp, call, accessibility and AI controls visually compete with the 3D product stage.

## What changed

- While a `.nlp3d-premium` showroom is visible, `project-3d.php` adds `body.nadlan-p3d-stage-active` through `IntersectionObserver`.
- In that state, the floating contact controls become a compact left-edge rail instead of a wide panel over the building.
- The rail keeps reachable controls:
  - 52px tap targets.
  - keyboard focus support.
  - hover/focus labels.
  - safe-area offsets for mobile browsers.
  - `prefers-reduced-motion` support.
- When the buyer scrolls away from the showroom, the normal floating controls return.

## Files

- `plugins/nadlan-config/inc/project-3d.php`
- `plugins/nadlan-config/nadlan-config.php`
- `plugin-dist/nadlan-config.json`
- `plugin-dist/nadlan-config-1.63.3.zip`

## Local gates

Run before PR:

```powershell
git diff --check
node --check <extracted project-3d inline JS>
tar -tf plugin-dist/nadlan-config-1.63.3.zip | Select-String '\\'
tar -xOf plugin-dist/nadlan-config-1.63.3.zip nadlan-config/inc/project-3d.php | Select-String 'floating_action_rail_v1633|nadlan-p3d-stage-active|nadlan_p3d_showroom_v1633_contact_css'
```

Expected:

- ZIP root is `nadlan-config/`.
- No backslash paths.
- Version/header/manifest/ZIP aligned at `1.63.3`.
- Healthcheck after deploy reports `project_3d.floating_action_rail_v1633=true`.

## Live DOM gate after deploy

Check Rainbow at 1440px and 390px:

- Single H1 remains true.
- No horizontal overflow.
- No raw PHP/JS/class leak.
- Showroom is first visible product surface.
- Floating controls do not cover the central building/model interaction area.
- Hover/focus on the rail reveals labels.
- Keyboard Tab can reach the rail controls.
- Reduced motion does not animate the rail.

## Honest boundary

This does not wire the GLB model into Rainbow. That still requires PR #163 to merge and the CMS payload to be applied after the server Git pull. This patch only improves the floating-control behavior around the showroom experience.
