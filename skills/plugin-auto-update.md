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

## SHIPPED 2026-05-28 — v1.2.0 self-hosted auto-update (Option B, adapted)

Because tool scope is restricted to the single repo (no separate plugin repo, no GitHub Releases API), we used PUC's **self-hosted JSON metadata** method instead of the GitHub-releases method — same end result for the owner.

- Vendored `YahnisElsts/plugin-update-checker` v5.6 at `plugins/nadlan-config/lib/plugin-update-checker/` (trimmed css/js/languages → 392K).
- Wired in `nadlan_config_boot_updater()` (init priority 5, try/catch guarded) pointing at:
  `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config.json`
- Committed `plugin-dist/nadlan-config.json` (version + download_url + changelog) and `plugin-dist/nadlan-config-1.2.0.zip` to the repo. The download_url is the raw.githubusercontent zip.

### How to ship a new plugin version FROM NOW ON (no owner ZIP upload)
1. Edit `plugins/nadlan-config/nadlan-config.php`, bump `Version:` (e.g. 1.2.1) and the healthcheck version string.
2. Build the zip: `rm -rf plugin-build/nadlan-config && mkdir -p plugin-build/nadlan-config && cp -r plugins/nadlan-config/. plugin-build/nadlan-config/ && (cd plugin-build && zip -rq ../plugin-dist/nadlan-config-1.2.1.zip nadlan-config/)`
3. Update `plugin-dist/nadlan-config.json`: set `version` to 1.2.1, `download_url` to the new zip path, update changelog + last_updated.
4. Commit + push to a PR branch → owner merges to `main` (so raw.githubusercontent serves the new files).
5. Within ~12h (or immediately if owner clicks "Check for updates"), WordPress shows "Update available" for NadLan Config. **Owner clicks Update. Done.**
6. Verify via `/wp-json/nadlan/v1/healthcheck` version field.

**This v1.2.0 is the LAST manual ZIP upload.** Confirmed by owner 2026-05-28.

Note: the raw.githubusercontent JSON only updates after the change is on `main` (merged PR). So plugin updates still ride the same merge-to-main flow as the theme — but the owner's action becomes a single in-WP "Update" click instead of delete+upload+activate.
