# Claude Access Handoff - NadLan

Date: 2026-06-29

This file is the practical access map for Claude/Cowork/any agent working on `nad-lan.co.il`.
Use it before touching code. The main risk is working from the wrong local folder or stacking a new visual layer over an old one.

## 1. Correct Local Repository

Use this folder:

```text
C:\Users\pro\Documents\websites\nad-lan-co-il-pr2
```

This is the current GitHub-synced repository on `main`.

Do not use this older folder for current rebuild work:

```text
C:\Users\pro\Documents\websites\nad-lan-co-il
```

That folder is an old dirty branch snapshot and caused confusion because it can look weeks behind production.

GitHub remote:

```text
https://github.com/The-new-ben/nad-lan-co-il.git
```

Current known merged head after the no-stack child theme slice:

```text
0d69bd5 feat: stabilize NadLan platform child chrome
PR: https://github.com/The-new-ben/nad-lan-co-il/pull/248
```

## 2. Current Live State

Live site:

```text
https://nad-lan.co.il/
```

Live healthcheck:

```text
https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
```

Current live plugin version verified from healthcheck:

```text
nadlan-config 1.69.56
```

The public homepage currently loads theme assets from:

```text
wp-content/themes/nadlan-platform-child/
wp-content/themes/nadlan-revenue/
```

The homepage safe band marker is present:

```text
data-nlpo-home-projects
```

## 3. Deployment Model

The repo is the source of truth.

Theme code reaches live by syncing/pulling the GitHub repo on the UPress server or by uploading a theme ZIP in WordPress admin.

Plugin code reaches live through:

```text
plugin-dist/nadlan-config.json
plugin-dist/nadlan-config-<version>.zip
```

WordPress plugin updates are driven by the manifest download URL inside:

```text
C:\Users\pro\Documents\websites\nad-lan-co-il-pr2\plugin-dist\nadlan-config.json
```

Never hand-upload random plugin folders. Always use a clean ZIP with forward slash paths.

## 4. Live Admin Access

The owner keeps Chrome logged in.

Use real Chrome for verification and WordPress admin work.

Typical admin URLs:

```text
https://nad-lan.co.il/wp-admin/
https://nad-lan.co.il/wp-admin/themes.php
https://nad-lan.co.il/wp-admin/plugins.php
https://nad-lan.co.il/wp-admin/edit.php?post_type=nadlan_project
```

If an existing Chrome tab cannot be controlled, open a new Chrome tab and navigate to the admin URL. Do not assume lack of access just because one tab is stale.

Do not print cookies, nonces, secrets, or tokens in chat.

## 5. Important Current Files

Plugin business engine. Keep business logic here:

```text
plugins/nadlan-config/nadlan-config.php
plugins/nadlan-config/inc/showroom-engine.php
plugins/nadlan-config/inc/project-3d.php
plugins/nadlan-config/inc/project-page-assembly.php
plugins/nadlan-config/inc/directory.php
plugins/nadlan-config/inc/archive-grid.php
plugins/nadlan-config/assets/showroom-engine/engine.js
plugins/nadlan-config/assets/showroom-engine/showroom.css
plugins/nadlan-config/assets/showroom-engine/editorial.css
plugins/nadlan-config/assets/showroom-engine/i18n.js
plugins/nadlan-config/assets/showroom-engine/mapbox-init.js
```

Presentation/orchestration helper plugin:

```text
plugins/nadlan-platform-orchestrator/nadlan-platform-orchestrator.php
plugins/nadlan-platform-orchestrator/inc/shortcodes.php
plugins/nadlan-platform-orchestrator/inc/helpers.php
plugins/nadlan-platform-orchestrator/inc/content-gaps.php
```

Currently active child presentation theme:

```text
themes/nadlan-platform-child/style.css
themes/nadlan-platform-child/functions.php
themes/nadlan-platform-child/theme.json
themes/nadlan-platform-child/assets/css/platform.css
themes/nadlan-platform-child/parts/header.html
themes/nadlan-platform-child/parts/footer.html
themes/nadlan-platform-child/templates/home.html
themes/nadlan-platform-child/templates/archive-nadlan_project.html
themes/nadlan-platform-child/templates/single-nadlan_project.html
```

Parent theme:

```text
themes/nadlan-revenue/
```

Design/spec handoff:

```text
handoff/claude-design/2026-06-28-nadlan-master-spec.md
handoff/claude-design/2026-06-28-agent-build-prompt.md
handoff/external-agent-packages/2026-06-28/
```

Key uploaded packages are archived here:

```text
handoff/external-agent-packages/2026-06-28/nadlan-platform-child-theme.zip
handoff/external-agent-packages/2026-06-28/nadlan-platform-orchestrator-plugin.zip
handoff/external-agent-packages/2026-06-28/nadlan-complete-platform-solution.zip
handoff/external-agent-packages/2026-06-28/NadLan_Ashira_Factory_Run_mockup.zip
handoff/external-agent-packages/2026-06-28/REVIEW-AND-SOLUTION.md
```

## 6. QA Evidence Already Produced

Renderer inventory:

```text
docs/rebuild-nadlan-2026-06-29/renderer-inventory.md
```

Rollback doc:

```text
docs/rebuild-nadlan-2026-06-29/ROLLBACK.md
```

Baseline screenshots and report:

```text
docs/qa/screenshots/platform-rebuild-2026-06-29/00-baseline/
```

Live deployed child theme QA:

```text
docs/qa/screenshots/platform-rebuild-2026-06-29/03-live-after-child-0.1.6/
```

Post-merge sanity QA:

```text
docs/qa/screenshots/platform-rebuild-2026-06-29/04-post-merge-sanity/
```

QA script:

```text
scripts/qa-platform-child-live.mjs
```

Run it from the correct repo:

```powershell
cd C:\Users\pro\Documents\websites\nad-lan-co-il-pr2
node scripts/qa-platform-child-live.mjs docs/qa/screenshots/platform-rebuild-2026-06-29/<new-folder>
```

## 7. What Must Not Be Done

Do not activate old rescue theme.

Do not activate the rejected bridge plugin as a replacement for the site.

Do not create another `[nadlan_showroom_engine]`.

Do not create a parallel lead endpoint.

Do not duplicate hreflang output.

Do not move CPTs, leads, billing, directory, calculators, or project data into the theme.

Do not stack a new homepage band over the existing one.

Do not stack another showroom over `#nl-root`.

Do not edit live database content without export/meta backup.

Do not claim success without real Chrome screenshots.

## 8. Renderer Rules

Before changing a public surface:

1. Screenshot current page.
2. Count the renderers.
3. Identify the file/hook/shortcode responsible.
4. Disable or bypass the old layer first.
5. Prove selector count changed.
6. Add the new implementation once.
7. Prove exactly one implementation.

Core selectors:

```js
document.querySelectorAll('#nl-root').length
document.querySelectorAll('.nlv2-showroom').length
document.querySelectorAll('.nlp3d').length
document.querySelectorAll('[data-nlpo-home-projects]').length
document.documentElement.scrollWidth > window.innerWidth + 2
```

Known current healthy expectation on checked pages:

```text
Homepage: data-nlpo-home-projects = 1, #nl-root = 0, .nlv2-showroom = 0, .nlp3d = 0
Ashira HE/EN: #nl-root = 1, .nlv2-showroom = 0, .nlp3d = 0
```

## 9. Recommended Next Step

Do not rebuild blindly.

First do an emergency read-only audit from the correct repo:

```powershell
cd C:\Users\pro\Documents\websites\nad-lan-co-il-pr2
git fetch origin main
git status --short --branch
git log --oneline -5 origin/main
node scripts/qa-platform-child-live.mjs docs/qa/screenshots/platform-rebuild-2026-06-29/claude-current-audit
```

Then compare screenshots against the Cloud Design target and decide:

- If the current child theme is acceptable as a temporary stable layer, continue with small surgical fixes.
- If the owner wants a true clean rebuild, create `themes/nadlan-premium/` side by side, but do not activate it live until screenshots pass.

## 10. Plain Truth For Claude

If your workspace shows `nadlan-config` around `1.56.x`, you are in the wrong folder or stale checkout.

The current repo and live site are at `nadlan-config` `1.69.56`.

The correct local working folder is:

```text
C:\Users\pro\Documents\websites\nad-lan-co-il-pr2
```

Start there.

