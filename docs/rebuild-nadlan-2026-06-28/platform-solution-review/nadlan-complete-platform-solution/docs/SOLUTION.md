# NadLan complete platform solution

This solution is not another replacement theme and not another duplicate showroom plugin. It is a two-layer platform package:

1. `NadLan Platform Child` theme: presentation layer only. It keeps `nadlan-revenue` as the parent and uses WordPress templates, theme.json and CSS to apply the premium design language across the site.
2. `NadLan Platform Orchestrator` plugin: glue layer only. It does not replace `nadlan-config`. It delegates the project showroom to the existing `nadlan_showroom_engine` when available, provides safe catalog and interior shortcodes, scans language and content gaps, and keeps optional homepage insertion off until screenshot QA approves it.

## Why this architecture

The live site already has the revenue CMS, calculators, professionals directory, leads, billing and `nadlan-config`. The failed theme package replaced that system and reduced the site to a demo. The failed bridge plugin duplicated hooks and shortcodes already owned by `nadlan-config`. This package avoids both failures.

## Files

- `theme/nadlan-platform-child.zip`: upload as a theme only when the parent theme `nadlan-revenue` is installed.
- `plugin/nadlan-platform-orchestrator.zip`: upload as a plugin after `nadlan-config` is active.
- `content/ashira/*.md`: multilingual Ashira content drafts for HE, EN, FR, RU, AR.
- `docs/QA-CHECKLIST.md`: mandatory browser and screenshot gates.
- `docs/CONTENT-MODEL.md`: CMS fields and language rules.

## Rollout order

1. Staging backup.
2. Install plugin, keep homepage auto band off.
3. Install child theme, do not activate on live until staging screenshots pass.
4. Verify `/`, `/projects/`, one existing project, one professional page, one calculator page, one lead flow.
5. Add Ashira multilingual content posts if missing.
6. Confirm hreflang is emitted by `nadlan-config` and not duplicated.
7. Enable homepage project band only after visual approval.
8. Promote to live with rollback to parent theme and plugin deactivation ready.

## Hard rules

- Do not activate any standalone replacement theme that ignores `nadlan-config`.
- Do not register `nadlan_showroom_engine` in any new plugin.
- Do not emit duplicate hreflang if `nadlan-config` already emits it.
- Do not strip `<main class="nlv2-showroom">` bluntly. Preserve the article.
- Do not invent single prices. Use a range or collapse the block.
- Do not expose internal words on public buyer pages.
- Do not ship without real Chrome screenshots.
