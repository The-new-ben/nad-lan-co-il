# Work Log - Current Transfer Context

## Before This Handoff

The project went through a long Rainbow and Dimri showroom cycle. The important lessons are now encoded in `skills/skill-release-discipline-and-mistakes.md` and `skills/project-page-premium-showroom-runbook.md`:

- GitHub merge is not deployment.
- Theme deploy and plugin deploy are different.
- Never hand-build plugin ZIPs on Windows.
- Do not ship fake facades or silent fallbacks.
- Visual claims need committed screenshots.
- Old `.codex-tmp` and repair worktrees caused stale-base regressions and should be avoided.

## Stage 1 Public Trust Cleanup

Supervisor directed the next work order:

1. Public trust cleanup first.
2. Dimri/project showroom second.
3. QA proof with screenshots at 1440, 768, 390.
4. Commit each slice separately.

### PR #211

PR #211 merged at `1046722`:

- Stage 1 public trust cleanup for non-commerce pages.
- Added/updated `scripts/qa-stage1-public-trust.mjs`.
- Added baseline screenshots under `docs/qa/screenshots/stage1-public-trust-before/`.
- Theme source changes in `functions.php`.

### After #211 live QA

Command run:

```powershell
node scripts\qa-stage1-public-trust.mjs --phase after --out docs/qa/screenshots/stage1-public-trust-after
```

Observed result:

```json
{
  "phase": "after",
  "outDir": "docs/qa/screenshots/stage1-public-trust-after",
  "screenshots": 15,
  "leakCount": 78,
  "visibleLeakCount": 33,
  "overflowCount": 0,
  "consoleErrorCount": 3
}
```

Interpretation:

- Visible leakage improved from 120 to 33.
- Console errors improved from 9 to 3.
- Overflow stayed at 0.
- Still not green, because Woo block/cart assets and a WordPress interactivity module error remained.

### PR #212

Branch:

`codex/stage1-trust-asset-cleanup-2026-06-21`

Commit:

`b1a3d9a51a08586d846e0651c21549cd7c7d300c`

PR:

`https://github.com/The-new-ben/nad-lan-co-il/pull/212`

Merged:

`8643e7448ab34eb533ff852415daa32c6338f049`

What changed:

- Added guarded Woo asset/script dequeue in `functions.php`.
- Only affects non-commerce public pages.
- Preserves cart, checkout, account, shop, product pages, and product taxonomies through `nadlan_revenue_is_commerce_screen()`.
- Updated `COORDINATION.md`.
- Committed after-#211 QA screenshots/report.

Checks run before PR #212:

```powershell
php -l functions.php
node --check scripts\qa-stage1-public-trust.mjs
git diff --check
```

Result:

- All passed locally.

Remaining after #212:

- Needs UPress theme Git pull.
- Needs cache clear.
- Needs final live QA screenshots.

## Handoff Creation

Handoff created on branch:

`codex/deep-handoff-2026-06-21`

Started from:

`origin/main` at `8643e7448ab34eb533ff852415daa32c6338f049`

Inspection performed:

- `git status --short --branch`
- `git rev-parse --show-toplevel`
- `git remote -v`
- `git log --oneline --decorate`
- `git worktree list`
- `gh pr list --state open`
- `gh pr view 212`
- live healthcheck via `Invoke-RestMethod https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck`
- top-level guidance reads: `AGENTS.md`, `README.md`, `START-HERE.md`, `COORDINATION.md`, `package.json`
- key skills/scripts reads:
  - `skills/skill-release-discipline-and-mistakes.md`
  - `skills/nadlan-config-plugin.md`
  - `skills/project-page-premium-showroom-runbook.md`
  - `scripts/build-plugin-zip.py`
  - `scripts/qa-stage1-public-trust.mjs`
  - `plugins/nadlan-config/nadlan-config.php`
  - `plugins/nadlan-config/inc/health.php`
  - `plugin-dist/nadlan-config.json`

Important finding:

- Live plugin is `1.68.2`.
- Main is now `8643e74`.
- Stage 1 code PR #212 is merged.
- Theme deployment may still be pending on UPress.
- PR #209 and PR #210 are open and related to facade/showroom engine work.

## Failed Or Risky Attempts Learned From

- Old backslash-path ZIPs caused a phantom plugin problem on Linux/UPress. Use `scripts/build-plugin-zip.py`.
- CSS stacking and `!important` layers caused repeated mobile/facade overflow confusion. Fix source, not just another override.
- Fake facades made the owner lose trust. Use real images/renders/polygons, or show a visible missing/illustrative state.
- "Merged" was repeatedly confused with "live". Always say which.
- Screenshots posted in chat are not durable proof. Commit them under `docs/qa/screenshots/`.
- Old `.codex-tmp` and repair worktrees are stale and should not be used as source.

## User Instructions That Matter

- Be honest; do not claim work is done without proof.
- Do not ask for permissions as a way to avoid work. Use available tools, and escalate only when truly blocked.
- If blocked, prepare a clear escalation for the supervising ChatGPT/owner instead of stopping silently.
- Use screenshots for every visual claim.
- Use external references/examples for product design decisions.
- Do not leak internal language into public pages.
- Do not stack new fake layers over broken old layers.
- Make project pages replicable for future projects.
- Keep everything documented in repo skills/runbooks.

## Immediate Next Log Entry Expected

After UPress theme pull/cache clear, run:

```powershell
node scripts\qa-stage1-public-trust.mjs --phase final --out docs/qa/screenshots/stage1-public-trust-final
```

Then commit the final screenshots/report and update the coordination log with the result.
