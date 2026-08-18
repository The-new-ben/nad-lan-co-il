# Drift Reconciliation — 2026-08-18 (SEO session 45acac5e)

## The problem
Production ran **1.72.212** while the recorded production branch `claude/sde-dov-experience-v1`
sat at **1.72.204** — 8 versions of drift accumulated by file-swap deploys (einstein-lab wave,
bak207→bak216 lineage on the server) that never landed in git. Zip-deploying the stale branch
would have rolled production back.

## The fix
Branch **`claude/production-truth-1.72.212`** (commit 2aa6b38) now holds a full ZipArchive
snapshot of the LIVE plugin directory (md5-verified transfer, health-confirmed 1.72.212),
plus tonight's `inc/project-lang.php` CTA-translation fix (deployed live via md5 swap, `.bakSEO3`).

**This branch is the deploy base going forward.** Cut work branches from it, not from
`claude/sde-dov-experience-v1` and not from `main`.

## Drift contents (204 → 212): 49 files changed, +10,293 / -37
New inc/ modules that existed only on the server until tonight:
- `inc/einstein-lab.php` — the einstein showroom-lab prototype (1.72.212 flagship)
- `inc/flagship-cotour.php`
- `inc/flagship-surface.php`
- `inc/project-image-batch.php`
- `inc/page-lang.php` — path-based page language variants (/ru/<slug>/): lang context,
  hreflang page clusters, chrome retranslation (this module auto-covered the new
  RU/FR estimator pages)
Plus asset waves (flagship-*, lab.*, registry.json) and this session's
`inc/directory.php` + `inc/city-hubs.php` (SEO wave 2).

Excluded from source control: 41 server-side `.bak*` rollback siblings (bak207–bak216,
bakSEO2) — they stay on the server only.

## Standing rules reaffirmed
- Live version truth: `GET /wp-json/nadlan/v1/health` — never trust a branch label.
- Before ANY plugin file edit: fetch the live file (uploads-copy snippet pattern), diff, edit on top.
- After swap deploys: mirror the change to git the same session (this file's branch).
