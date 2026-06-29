# Renderer Inventory

Date: 2026-06-29

Purpose: identify every known public renderer family before any new platform change. The golden rule for this run is: disable or remove the old layer, prove it is gone, then enable the new layer and prove exactly one exists.

## Active And Historical Renderer Families

| Renderer family | Evidence selector or marker | Main locations found | What it outputs | Status | Disable/proof rule | Owner-facing risk |
| --- | --- | --- | --- | --- | --- | --- |
| Showroom engine | `#nl-root`, `nadlan_showroom_engine` | `plugins/nadlan-config/inc/showroom-engine.php`, `plugins/nadlan-config/assets/showroom-engine/` | Current factory showroom engine for project pages. | Intended canonical path for new project pages. | On new showroom pages, require `#nl-root = 1`. | If combined with old layers, the user sees duplicated showrooms and broken hierarchy. |
| Legacy static v2 showroom | `.nlv2-showroom`, `data-nlv2-showroom` | `assets/css/nadlan-showroom-v2.css`, `assets/js/nadlan-showroom-v2.js`, preview docs and old post bodies | Static/baked project showroom markup. | Legacy, must not render on factory pages. | On new showroom pages, require `.nlv2-showroom = 0`. | Causes stacked duplicate showroom and language/content mismatch. |
| Legacy project 3D | `.nlp3d` | `plugins/nadlan-config/inc/project-3d.php`, many docs and old Rainbow/Dimri work | Older model/facade/apartment selector system. | Functional legacy path. Use only where factory engine is not active. | On a page using factory showroom, require `.nlp3d = 0` unless deliberately gated as legacy. | CSS debt and old facade/model layers can overlap new engine. |
| Old project showroom | `data-nlps-showroom` | `assets/js/nadlan-project-showroom.js`, Dimri docs | Earlier project showroom implementation. | Legacy. | Require no `data-nlps-showroom` on factory pages. | Adds another selector implementation and can compete with the current engine. |
| Home/project gallery band | `[data-nlpo-home-projects]` | `plugins/nadlan-platform-orchestrator/inc/shortcodes.php`, `nadlan-platform-orchestrator.php` | Homepage/project catalog band from the platform orchestrator. | Present but off by default unless option or `?nlpo_preview=1`. | Homepage should have either `0` or exactly `1`, never more. | If enabled by both template and filter, homepage gets duplicate bands. |
| Legacy home engine config | `data-nle-home-showroom`, `data-nle-engine-config` | `assets/js/nadlan-showroom-engine.js` | Older standalone home/showroom engine config. | Historical/prototype. | Do not use as a second homepage renderer. | Can create a parallel home showroom with separate state. |

## Hard Findings From Current Search

- `plugins/nadlan-platform-orchestrator/nadlan-platform-orchestrator.php` keeps `nlpo_auto_insert_home_band` defaulted to `0`.
- `?nlpo_preview=1` is the safe preview path for the homepage project band.
- `[data-nlpo-home-projects]` is emitted by the orchestrator shortcode in `plugins/nadlan-platform-orchestrator/inc/shortcodes.php`.
- The public homepage already has one editorial project showcase in the body (`.nlux-showcase`), but it is not marked with `[data-nlpo-home-projects]`.
- The first safe homepage move is to mark the existing showcase at render time, not append another project band.

## Acceptance Checks To Use In Browser

```js
{
  nlRoot: document.querySelectorAll('#nl-root').length,
  oldNlv2: document.querySelectorAll('.nlv2-showroom').length,
  oldP3d: document.querySelectorAll('.nlp3d').length,
  homeBand: document.querySelectorAll('[data-nlpo-home-projects]').length
}
```

## Release Rule

No implementation PR may add a renderer path until the report for that PR proves the old path count is zero or intentionally gated off on the same page.
