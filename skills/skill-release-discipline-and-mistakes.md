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

## 0a. SESSION-START SYNC — run this every time, both agents, 60 seconds

Before reading the user's request, before writing any code, before opening any branch:

```bash
cd /path/to/your/ONE/canonical/checkout    # Codex: C:\Users\pro\nad-lan-co-il (NOT .codex-tmp)
git fetch origin main && git checkout main && git reset --hard origin/main

# A. CURRENT GIT STATE
echo "main HEAD: $(git rev-parse --short HEAD)"
echo "git version: $(grep -m1 'Version:' plugins/nadlan-config/nadlan-config.php)"

# B. CURRENT LIVE STATE (the only truth that matters for 'done')
curl -s https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck | python3 -c "import json,sys;d=json.load(sys.stdin);print('live version:',d.get('version'));print('live flags:',[k for k,v in d.get('project_3d',{}).items() if v is True][:6])"

# C. OPEN PRs (what the OTHER agent is doing)
# look at github.com/The-new-ben/nad-lan-co-il/pulls

# D. THE ONE SENTENCE
# "main is X. Live is Y. Open PRs touching project-3d.php: [list]. Real blocker right now: ___."
```

If `git version > live version`, **the next action is deploy, not more code.** Do not start a new feature on top of an undeployed stack — that is M0 + M6 compounded.

Both agents must paste this state at the **top** of any "what I'm going to do" message. If you can't paste it, you haven't synched.

---

## 0b. SYMMETRY CONTRACT — both agents are bound, not just Codex

This is not a Codex lecture. **Claude has made every one of these mistakes too** in this codebase. The contract is mutual:

| | Claude commits to | Codex commits to |
|---|---|---|
| One checkout | work only in `/home/user/nad-lan-co-il` | work only in `C:\Users\pro\nad-lan-co-il` (never `.codex-tmp`) |
| `project-3d.php` | edit it (owner per 2026-06-14) — but only after §0a | **never** edit it; propose via PR comment / spec |
| Theme files | propose via PR comment / spec | edit them (owner per 2026-06-19) |
| Pre-work | run §0a + grep main for what's already done before writing anything | same |
| Done | "merged" vs "deployed" — state which (M0/M8) | same |
| Verification | every integrity claim backed by a command pasted in the PR (M5) | same |
| Stop rule | when blocked on deploy, stop and say so (M6) — don't ship docs to look busy | same |
| Sync | post §0a state at the top of status updates | same |

Either agent calling out a violation by the other is welcome. The owner should not have to be the referee.

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

### M7 — Two agents editing one file *(superseded 2026-06-19)*
**Original problem:** Claude and Codex both edited `project-3d.php` and pushed to main → collisions, regressions, renumbering.
**Original rule (2026-06-14):** `project-3d.php` is owned by Claude.
**Updated rule (2026-06-19, owner decision):** Role split is now **Codex implements (incl. project-3d.php) · Claude reviews & merges**. To prevent the original collision pattern from returning, use the **two-key rule** and the **shared billboard** instead of file-level lock:
1. Implementer ≠ merger. Codex commits & pushes; Claude reviews & merges.
2. Both agents declare the file they're touching in `COORDINATION.md` §3/§4 BEFORE editing. If the other agent has it open, hold or split the work.
3. The mitigation that actually worked: see `COORDINATION.md` at repo root — the shared billboard.

### M11 — "Proof" that lives only in chat or a local file *(new — 2026-06-19)*
**What happened:** "I rebuilt the ZIP" / "screenshots look good" was reported, but the artifact was never in the repo so the other agent couldn't verify. M5 said *every integrity claim needs a command on the actual artifact*; this extends it: **every visual-change claim needs a screenshot committed to the repo** at a stable path (`docs/qa/screenshots/<run>/<viewport>.png`) — not pasted in chat, not on a Windows desktop. If it isn't in git, it didn't happen.
**Rule:** for any CSS / layout / copy / hierarchy change, the PR must include screenshots at **1440 / 768 / 390** committed under `docs/qa/screenshots/`, AND a healthcheck JSON committed under `docs/qa/healthcheck-<version>.json` after live deploy.
**Fix:** Codex (who has Chrome) captures and commits the screenshots. Claude verifies they exist in the PR before merging.

### M12 — Building a coordination framework instead of using the simplest one *(new — 2026-06-19, meta-mistake)*
**What happened (would have happened):** the temptation to write a complex multi-agent framework, a new state machine, custom MCP servers, etc.
**Rule:** Anthropic's own guidance — *"finding the simplest solution possible, and only increasing complexity when needed"* (Building effective agents, Dec 2024). Our solution is one Markdown file (`COORDINATION.md`) + the discipline skill + trunk-based merging. That's it. No new abstractions until that proven inadequate by measurement, not by feeling.

---

### M9 — Working in throwaway temp folders instead of the repo  *(the root cause of most chaos)*
**What happened:** work was done in `C:\Users\pro\Documents\websites\.codex-tmp\nadlan-rainbow-showroom-dna-1664\` — a hidden, disposable clone. Result: assets/QA/screenshots lived outside git, branches were cut from stale copies (→ M1/M2 regressions), commits were lost to branch-name reuse, and the owner couldn't find the files.
**Rule:** **If it's not committed to the repo, it does not exist.** Use ONE canonical, findable checkout — `C:\Users\pro\nad-lan-co-il` (NOT under `.codex-tmp`, NOT a per-task clone). Every durable artifact (project assets, payloads, QA screenshots, docs) goes in git under a stable path (`assets/projects/<slug>/`, `docs/qa/…`). Never report a "proof file" that lives only in a temp dir — commit it or it's not proof.
**Fix:** one repo, one working dir, everything in git.

### M10 — Forgetting the THEME has a different deploy path than the plugin
**What happened (new risk with theme-first):** presentation is moving from the plugin into the theme (repo root + `patterns/`, `assets/css|js/`, `functions.php`). The plugin deploys via the WordPress auto-updater (ZIP). **The theme deploys via `git pull` on the UPress server** — a *different* pipeline. Merging theme code to `main` puts **nothing** live until someone pulls on the server.
**Rule:** state the deploy path explicitly per change. Plugin change → "update plugin to vX". Theme change → "git pull on UPress server + clear cache". A theme PR with no server pull is M0 all over again. Keep a `THEME` vs `PLUGIN` label on every release note.

---

## 1b. ARCHITECTURE BOUNDARY (theme-first, decided 2026-06-19)
- **Plugin** = infrastructure only: CPTs, REST endpoints, lead capture, data contracts, sanitization, AI/payment/business logic, healthcheck. No page layout, no showroom CSS.
- **Theme** = all presentation: project-page layout, showroom pattern, responsive CSS/JS, article hierarchy, breadcrumbs.
- **Project folder** (`assets/projects/<slug>/`, committed) = unit data, source notes, model/facade/poster/tour assets, validated `showroom-payload.json`.
- **WordPress draft** = the editable CMS page, created from the committed payload.
- Rule: a presentation tweak must NOT require a plugin ZIP release (that's what poisoned the server). If you're editing the plugin to change how the page *looks*, stop — it belongs in the theme.

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
