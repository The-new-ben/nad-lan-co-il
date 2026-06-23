# Adopted Codex Visual Proof Loop Skill

> Requires real browser screenshots and visual analysis for every public UI change, especially WordPress showroom, listings, homepage, city pages, and admin war room.

## When to use this

- Any CSS, layout, component, image, or public text changes.
- Any Lovable design is ported to WordPress.
- The owner asks "show me", "screenshot", "prove", or "looks wrong".

## Procedure

1. Capture before screenshot when the issue is visual.
2. Make the code change.
3. Capture after screenshots:
   - desktop 1440 or 1280
   - mobile 390
   - Hebrew and English if relevant
   - critical states, not only the default state
4. Save screenshots inside the repo.
5. Write a visual QA note:
   - what changed
   - what passed
   - what failed
   - whether it is live, local, or injected-preview only
6. If a screenshot fails, fix the source and rerun. Do not explain it away.

## NadLan no-stacking check

When the visual fix depends on a late CSS override, stop. Remove or disable the old active source and make the new source primary.

## Source basis

- Composio webapp-testing recommendation: https://composio.dev/content/top-codex-skills
- Playwright screenshot docs: https://playwright.dev/docs/screenshots
- Existing NadLan screenshot skill: `handoff/shared-knowledge/skills/nadlan-screenshot-first-visual-qa.md`

## Revision log

- 2026-06-23 - Created by Codex from UI-testing skill research and owner screenshot rule.
