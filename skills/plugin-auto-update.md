# Plugin Auto-Update — the path to "click Update inside WP"

> **Notice to all agents:** the owner raised the upload friction problem (delete → upload → activate every version). This skill documents the honest options and the recommended path.

## The honest reality

There are three real options. Anything else is wishful thinking.

### Option A — UPress Git for the plugin folder
UPress's "ניהול GIT" feature clones one repo into one folder. We already use it for the theme (`/wp-content/themes/nadlan-revenue/`). For the plugin we'd need a **second sync target** pointing at `/wp-content/plugins/nadlan-config/` — but the SAME repo, AND it would clone the repo root into the plugin folder (not the `plugins/nadlan-config/` subfolder).
- **Limitation**: UPress git doesn't do sparse checkout.
- **Workarounds**: a separate plugin-only repo, OR a structure trick where the plugin lives at repo root in a dedicated repo.
- **Verdict**: clean if owner is OK maintaining a second small repo. Status: NOT RECOMMENDED — adds repo sprawl for one small file.

### Option B — "Plugin Update Checker" library (RECOMMENDED)
Vendor the standard `yahnis-elsts/plugin-update-checker` library (~300 KB, GPL-2.0, used by thousands of WP plugins). Wire it to a **GitHub Releases** feed.
- After this lands once: **WordPress shows "Update available" in your Plugins screen** any time we tag a new GitHub Release. **You click "Update" once. Done.** No upload, no delete-and-reinstall, no ZIP shipping.
- Update notes appear from the GitHub release body.
- Rollback: WordPress shows the previous version in the changelog if needed.
- Cost: one extra ~300 KB of vendored code; the library is rock-stable.

### Option C — "One big plugin" (NOT recommended)
Bundling more code doesn't reduce upload friction; it just delays it. Same delete+upload+activate cycle. **Rejected.**

## Recommended path

**Option B** in plugin v1.2.0 (next release). Roughly:
1. Vendor `plugin-update-checker` into `plugins/nadlan-config/plugin-update-checker/`.
2. Wire it to `https://github.com/The-new-ben/nad-lan-co-il/releases`.
3. From then on: when we want to ship a new version, the agent creates a GitHub Release tagged `nadlan-config-1.2.x` with the ZIP attached. WordPress sees it and offers Update.
4. Owner clicks Update once. Verified via `/wp-json/nadlan/v1/healthcheck`.

## Open TODOs

- [ ] Owner approves vendoring `plugin-update-checker` (free GPL, no recurring cost).
- [ ] Build v1.2.0 with the checker wired up.
- [ ] Document the GitHub Release workflow in `nadlan-config-plugin.md` (the agent creates the release; owner just clicks Update).

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8)._
