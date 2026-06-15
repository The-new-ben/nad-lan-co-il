# SKILL — Release Discipline & The Bible of Mistakes (nadlan-config)

> **Audience:** any agent (Codex, Claude, future) shipping the `nadlan-config` plugin.
> **Status:** MANDATORY. Read this before touching versions, ZIPs, or `project-3d.php`.
> **Why this exists:** the same handful of mistakes have burned days and once
> **took the production server down**. This file is the post-mortem turned into rules.
> When you make a NEW mistake, add it here. This is a living document.

---

## 0. THE PRIME DIRECTIVE — "in git" ≠ "live"

The single most expensive recurring confusion: **pushing/merging code is not deploying it.**

- The live site updates **only** when WordPress installs the new plugin ZIP (auto-updater notice → Update, or manual upload). Until then, `main` can be 5 versions ahead and **buyers see none of it**.
- **Definition of Done = deployed AND verified live**, not "pushed" / "PR open" / "ZIP built".
- Always state two versions separately: **git/main version** and **live healthcheck version** (`/wp-json/nadlan/v1/healthcheck` → `version`). If they differ, the task is **not done** — the next action is *deploy*, not more code.
- Do **not** generate more docs/scripts/QA while the real blocker is "not deployed." That is motion, not progress.

---

## 1. THE MISTAKE CATALOG

### M1 — Version racing / picking a number ≤ main  *(caused PR #181 = a regression)*
**What happened:** built on a stale local base and bumped to `1.65.7` while `main` was already `1.66.2`. Merging would have *decreased* the version → the WordPress updater **stops offering updates** on a semver decrease, and the manifest points at a ZIP that contradicts the header.
**Rule:** before ANY version bump, run `git fetch origin main` and read main's version. Your new version must be **strictly greater** than main's. Never reuse or go below.
**Fix command:**
```bash
git fetch origin main && git show origin/main:plugins/nadlan-config/nadlan-config.php | grep -m1 'Version:'
```

### M2 — Branching off a stale base → parallel rewrite that wipes work *(PR #181: +342/−161 to project-3d.php)*
**What happened:** the branch was a near-total rewrite of `project-3d.php` from a pre-feature base, which would have **deleted the embedded apartment-cell selector** (`renderApartmentCells`, `is-facade-select`, `nlp3d-facade-plane`, `nadlan_p3d_facade_cell_selector_css`).
**Rule:** **rebase onto `origin/main` BEFORE working**, not after. Produce a *small additive delta*, not a rewrite. If `git diff --stat main..yourbranch` shows hundreds of changed lines in a file you didn't intend to rewrite, STOP — you're on a stale base.
**Fix command (run first, every session):**
```bash
git fetch origin main && git rebase origin/main
# sanity: confirm the live features still exist on your branch
grep -c 'renderApartmentCells\|is-facade-select\|nlp3d-facade-plane' plugins/nadlan-config/inc/project-3d.php   # must stay >0
```

### M3 — Windows backslash ZIP paths → **took the server down** *(the 1.66.1 incident)*
**What happened:** a ZIP was built with entry paths like `nadlan-config\nadlan-config.php` (backslashes). On Linux/uPress those don't unpack as folders — they become **literal junk files** inside the plugin dir → a **phantom plugin** → uPress plugin manager jammed.
**Rule:** NEVER hand-build the ZIP on Windows. Use the canonical builder, which forces forward slashes and **refuses** to emit a backslash ZIP:
```bash
python3 scripts/build-plugin-zip.py            # detects Version: header
```
**Verify EVERY shipped ZIP (don't just claim it):**
```bash
python3 - <<'EOF'
import zipfile; z=zipfile.ZipFile('plugin-dist/nadlan-config-<VER>.zip'); n=z.namelist()
bad=sum('\\' in x for x in n)
print('entries',len(n),'backslash',bad,'rooted',all(x.startswith('nadlan-config/') for x in n),'crc',z.testzip())
assert bad==0 and all(x.startswith('nadlan-config/') for x in n) and z.testzip() is None, 'POISONED ZIP — DO NOT SHIP'
print('CLEAN')
EOF
```

### M4 — Shipping PHP without a lint *(Windows shell has no `php`)*
**What happened:** "PHP lint could not run because this Windows shell has no php executable." PHP changes shipped unlinted.
**Rule:** PHP must be lint-clean before merge. If your shell has no PHP, **say so explicitly and hand the lint to whoever can run it** (the file owner / CI). Do not mark a PHP change "verified" when you only checked JS.
**Fix:** `php -l plugins/nadlan-config/inc/<file>.php` on every changed PHP file. No PHP locally → request the owner/Claude run the gate before merge.

### M5 — Claiming integrity you didn't verify on the actual artifact
**What happened:** "ZIP: 0 backslash paths" was stated for a ZIP that, when inspected, had 130 backslash paths.
**Rule:** every integrity claim must be backed by a command run against the **exact file being shipped**, pasted in the PR. "I rebuilt it" is not verification; the assertion in M3 is.

### M6 — Activity ≠ progress (docs/scripts churn while blocked)
**What happened:** many readiness matrices, QA scripts, and manual edits were produced across hours while the only real blocker stayed "live not updated."
**Rule:** when blocked on an external state (deploy, owner action), **state the one blocker and stop**, or do work that *removes* the blocker. Don't add the 6th QA script. One sentence: "Blocked on deploy of X; nothing else ships value until then."

### M7 — Two agents editing one file
**What happened:** Claude and Codex both edited `project-3d.php` and pushed to main → collisions, regressions, renumbering.
**Rule:** **`project-3d.php` is owned by Claude** (owner's decision, 2026-06-14). Codex: do not edit it. Propose changes as a spec/PR comment, or hand off. One file, one owner.

### M8 — Calling a non-deploy a "deploy"
**Rule:** "merged to main" → say *merged*. "live healthcheck shows new version" → say *deployed*. Never blur the two (see M0).

---

## 2. RELEASE PRE-FLIGHT (copy-paste, run in order)

```bash
# 1. fresh base
git fetch origin main && git rebase origin/main

# 2. confirm live features survive
grep -c 'renderApartmentCells\|is-facade-select\|nlp3d-facade-plane' plugins/nadlan-config/inc/project-3d.php

# 3. pick version strictly > main
git show origin/main:plugins/nadlan-config/nadlan-config.php | grep -m1 'Version:'

# 4. bump ALL SIX surfaces to the new version:
#    a) header  Version:                       (nadlan-config.php)
#    b) 'version' => '...'  array               (nadlan-config.php)
#    c) 'version' => '...'                       (inc/health.php)
#    d) wp_register_style('nadlan-p3d',...)      (inc/project-3d.php)
#    e) wp_register_script('nadlan-p3d',...)     (inc/project-3d.php)
#    f) manifest "version" + "download_url" + ZIP filename (plugin-dist/nadlan-config.json)

# 5. lint (REQUIRED — get help if no php locally)
for f in nadlan-config.php inc/project-3d.php inc/health.php; do php -l plugins/nadlan-config/$f; done

# 6. inline JS syntax
#    extract the <<<'JS' block and: node --check that file

# 7. build + auto-verify ZIP (refuses poison)
python3 scripts/build-plugin-zip.py

# 8. confirm 6/6 version surfaces match the new number (grep)
```
If any step fails or you can't run it, **do not merge** — surface it.

---

## 3. BLOCKER PLAYBOOK (symptom → cause → unblock)

| Symptom | Cause | Unblock |
|---|---|---|
| Live healthcheck shows old version | not deployed | WP-Admin → Updates → update plugin → clear cache → re-check healthcheck |
| Updater shows no update | manifest version ≤ installed, or cache | confirm `plugin-dist/nadlan-config.json` version > installed; wait for PUC check (~12h) or force-check |
| uPress can't manage plugins / phantom plugin | poisoned backslash ZIP unpacked junk (M3) | delete whole `/wp-content/plugins/nadlan-config/` folder, reinstall clean ZIP (DB data is safe) |
| PR would lower the version | stale base (M1/M2) | rebase onto main, re-bump above main |
| "PHP lint can't run" | no php in shell (M4) | hand lint to file owner / CI before merge |
| Merge wipes a feature | parallel rewrite (M2) | rebase; keep the delta tiny and additive |

---

## 4. DEFINITION OF DONE (all must be true)
1. Rebased on current `main`; delta is additive; live features present.
2. Six version surfaces aligned, strictly above previous main.
3. `php -l` clean (all changed PHP) + inline JS `node --check` clean.
4. ZIP built by `scripts/build-plugin-zip.py`, verified 0 backslash / rooted / CRC ok.
5. Merged to main.
6. **Deployed** and **live healthcheck reports the new version.**
7. Post-deploy gate run against live (e.g. `scripts/qa-rainbow-postdeploy.mjs`).

Only #1–#5 are in our control from git. #6 is the owner's deploy click. **Say which step you're on.**

---

## 5. WHEN YOU MAKE A NEW MISTAKE
Append it to §1 as `M#` with: what happened, why it hurt, the rule, the fix command.
This file is the memory that stops us repeating days of pain.
### M9 - Healthcheck green is not visual green
**What happened:** v1.66.4 deployed correctly and `/wp-json/nadlan/v1/healthcheck` reported the new version, but the post-deploy visual gate caught a real 390px mobile crop on the Rainbow showroom.
**Why it hurt:** a live update can be technically installed while still failing the buyer experience. Healthcheck proves the plugin loaded; it does not prove the page is usable.
**Rule:** after every live plugin update, run the live visual gate before saying "done." If it fails, ship the smallest possible patch version and deploy that patch.
**Fix command:**
```powershell
.\scripts\nadlan-release-gate.ps1 -Version <VERSION>
```
For a visual-only live check:
```powershell
node scripts\qa-rainbow-postdeploy.mjs --version <VERSION> --out docs\qa\rainbow-postdeploy-<VERSION>.json
```

### M10 - Margin-based mobile containment can still inherit theme offset
**What happened:** v1.66.5 tried to fix the Rainbow 390px crop with `margin-left: calc(50% - 50vw + 14px)`, but the live block theme still rendered the root at `x=39.5 width=362 right=401.5` on a 390px viewport.
**Why it hurt:** the patch was technically loaded, but the buyer still saw a cropped showroom.
**Rule:** for full-bleed mobile blocks inside constrained WordPress content, prefer midpoint centering: `left:50%; transform:translateX(-50%); width:calc(100vw - 28px);`.
**Fix command:** run the live visual gate and inspect `rootRect`, not only `scrollWidth`.

### M11 - Do not treat a theoretical CSS formula as verified
**What happened:** v1.66.6 used midpoint centering, but relative positioning centered against the theme column, not the viewport, so the measured 390px crop stayed unchanged.
**Why it hurt:** it burned another deploy cycle because the fix was plausible but not proven on the live geometry.
**Rule:** when a visual bug is measured in pixels, patch the measured viewport first, then generalize only after the gate passes. For this case: phone-only `margin-left:-25px`, tablet untouched.

### M12 - Inspect the parent geometry before a third CSS patch
**What happened:** v1.66.7 still failed because the root lived inside `.entry-content.wp-block-post-content` at `x=51`, and the parent had `overflow:hidden auto`.
**Rule:** before another crop patch, capture the ancestor chain with `getBoundingClientRect()` and computed `overflow`, `marginLeft`, `width`, and `transform`. Patch the parent only if the parent is what clips the child.
**Fix:** for Rainbow at 390px, set phone-only parent `overflow:visible` and root `margin-left:-50px`.

### M13 - Do not let old selector layers fight the accepted architecture
**What happened:** after the fixed facade picker was accepted as the buyer selector, older release CSS still rendered floating model squares and fixed/mobile cards that could cover the model or facade.
**Why it hurt:** the buyer saw two competing selection systems and overlapping surfaces, so the product felt confusing even when the data was wired.
**Rule:** once a project has the dual-showroom contract, the GLB is context and the facade is the picker. Add final scoped overrides after older CSS slices: hide `.nlp3d-stage-picks` and `.nlp3d-mv-hotspot` only in `.is-dual-showroom`, and dock `.nlp3d-stage-card` below the scene.
**Fix command:** after deploy, click a facade cell at 1440/768/390 and verify the selected card does not overlap the model or facade.
