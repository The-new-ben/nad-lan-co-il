# Adopted WordPress Plugin Quality Gate Skill

> Adds a stronger pre-release quality checklist for NadLan plugin changes: architecture, WordPress APIs, Plugin Check, coding standards, release ZIP, and public behavior.

## When to use this

- Any plugin file changes.
- Any plugin ZIP or manifest changes.
- Any new endpoint, shortcode, admin page, asset, CPT, cron, or updater behavior.

## Gate

1. Locate the plugin main file and version surfaces.
2. Confirm the feature belongs in the plugin, not the theme.
3. Check architecture:
   - no heavy side effects at file load
   - hooks registered deliberately
   - admin code behind admin checks
   - public code escaped at output
4. Run PHP lint.
5. Run inline JS syntax check when JavaScript is embedded in PHP.
6. Build ZIP only with the guarded builder.
7. Run the release verifier.
8. If available, run Plugin Check or document why it was not available.
9. Screenshot affected public/admin surfaces.

## NadLan adaptation

This does not replace `skills/codex-plugin-access-and-deploy.md`. It strengthens the checklist and must be used with the no-stacking visual rule.

## Source basis

- WordPress agent skills: https://github.com/WordPress/agent-skills
- WordPress Plugin Handbook: https://developer.wordpress.org/plugins/
- Shahibur Rahman on Plugin Check: https://dev.to/shahibur_rahman_6670cd024/deep-dive-ensuring-wordpress-plugin-quality-with-plugin-check-pcp-59e9
- WordPress Coding Standards: https://github.com/WordPress/WordPress-Coding-Standards

## Revision log

- 2026-06-23 - Created by Codex from WordPress plugin skill and quality-gate research.
