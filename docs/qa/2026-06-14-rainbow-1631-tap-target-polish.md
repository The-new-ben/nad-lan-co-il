# Rainbow v1.63.1 Tap-Target Polish QA

Scope: `plugins/nadlan-config/inc/project-3d.php`, plugin version metadata, manifest and ZIP.

## What changed

- Facade apartment selection now uses a larger transparent SVG hit rectangle as the only accessible
  control.
- The visible facade polygon is visual-only, so the QA scanner no longer sees thin 12px-high unit
  outlines as buttons.
- Decorative tower floor bands are no longer focusable controls. Only floors with selectable units
  remain interactive.
- Selectable tower floors render as 44px hit targets while keeping a thin architectural floor-band
  visual.
- Small showroom controls are forced back to at least 44px after the later mobile CSS overrides.

## Local proof

```powershell
node -e "const fs=require('fs'); const s=fs.readFileSync('plugins/nadlan-config/inc/project-3d.php','utf8'); const m=s.match(/\$js = <<<'JS'\r?\n([\s\S]*?)\r?\nJS;/); if(!m) throw new Error('inline JS not found'); new Function(m[1]); console.log('inline JS ok', m[1].length);"
```

Result: `inline JS ok 48140`.

```powershell
rg -n "1\.63\.1|tap_target_min_px|pointBox|nadlan_p3d_showroom_v1631_a11y_css|is-selectable" plugins/nadlan-config/nadlan-config.php plugins/nadlan-config/inc/project-3d.php
```

Result: markers present in header, healthcheck, inline CSS and JS.

## Gates for Claude / deploy

- `php -l plugins/nadlan-config/nadlan-config.php`
- `php -l plugins/nadlan-config/inc/project-3d.php`
- ZIP root must start with `nadlan-config/`.
- ZIP must contain `nadlan-config/inc/project-3d.php` with markers:
  `nadlan_p3d_showroom_v1631_a11y_css`, `pointBox`, `tap_target_min_px`.
- Live DOM after deploy:
  - no horizontal overflow at 1440 and 390,
  - no visible PHP/JS error text,
  - model-viewer rail still reports ready,
  - no `.nlp3d [role="button"]` target below 44px except hidden/offscreen nodes.

## Local blocker

This Windows shell still has no `php` binary, so PHP lint must run in Claude/deploy gate.
