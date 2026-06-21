# Codex Transfer Handoff - NadLan

Date: 2026-06-21
Repo: https://github.com/The-new-ben/nad-lan-co-il
Prepared from: `C:\Users\pro\Documents\websites\nad-lan-co-il-showroom-1680`
Current handoff branch: `codex/deep-handoff-2026-06-21`

## Current Objective

Continue the NadLan WordPress project safely from a different PC. The immediate work is not a new feature. It is to finish Stage 1 public trust cleanup on the live site, verify it with screenshots, then continue the Dimri Yama showroom work only after the trust layer is green.

Plain language objective:

1. Make public pages stop leaking WooCommerce/cart/debug/internal UI where they are not commerce pages.
2. Verify the merged theme fixes are live after a UPress Git pull and cache clear.
3. Only after that, continue Dimri/Rainbow showroom work with visual proof, no fake facades, and no silent fallbacks.

## Business And Product Context

NadLan is a Hebrew Israeli real-estate authority and marketplace site. It combines:

- real-estate content and SEO pages,
- professional and project directories,
- lead capture and routing,
- advertiser/payment rails,
- AI concierge,
- premium project pages with 3D/showroom experiences.

The owner wants Rainbow and Dimri Yama to become the replicable model for future project pages. The product promise is a buyer-facing showroom: project context, model/facade selector, apartment data, view/tour media, and a clean contact path to the developer or owner. The site must also look trustworthy to buyers, contractors, investors, and search engines. Public pages must not expose internal words such as funnel, CRM, debug, placeholder, cart fragments, or unfinished payment wiring.

## Current Verified State

Local Git inspected on 2026-06-21:

- `origin/main`: `8643e74` - `Dequeue Woo assets on public non-commerce pages (#212)`
- Live plugin healthcheck: `version: 1.68.2`
- WordPress live versions from healthcheck: PHP `8.5.5`, WordPress `7.0`
- Plugin health flags show `project_3d.enabled: true`, `model_viewer_ready: true`, `dimri_yama_concept_facade_v1682: true`, `fake_facade_grid_removed_v1681: true`
- Open active showroom PRs:
  - PR #209 - `Add facade engine QA tooling and geometry baseline`, branch `codex/facade-engine-standard-1683`, base `main`, mergeable.
  - PR #210 - `v1.68.3 Dimri showroom geometry containment`, branch `codex/dimri-geometry-fix-1684`, base `codex/facade-engine-standard-1683`, mergeable and stacked on #209.
- Recently merged:
  - PR #211 - Stage 1 public trust cleanup for non-commerce pages.
  - PR #212 - Follow-up dequeue of Woo assets on public non-commerce pages.

Important: PR #212 is merged to GitHub main, but a theme change does not become live until the UPress server Git copy is pulled and cache is cleared.

## What Has Already Been Done

### Plugin/showroom history

- `nadlan-config` plugin reached live version `1.68.2`.
- Project 3D/showroom runtime contains many feature flags and healthcheck fields.
- Silent fallbacks and fake CSS grid facades were identified as harmful and banned in skills.
- Dimri Yama currently has a concept facade fallback asset in `1.68.2`; owner judged the generated image ugly. Treat it as temporary or replace with official/decent render.
- Rainbow has been used as the prototype for 3D/showroom work.

### Stage 1 public trust cleanup

PR #211 merged:

- Removed public WooCommerce blocks/notices from non-commerce pages.
- Cleaned Join Pro public wording.
- Suppressed `More posts` on project/property/professional singles.
- Removed duplicate page-title H1 on `/join-pro/` and `/sitemap/`.
- Added/refined `scripts/qa-stage1-public-trust.mjs`.
- Committed baseline screenshots under `docs/qa/screenshots/stage1-public-trust-before/`.

After #211 live QA was run:

- `node scripts\qa-stage1-public-trust.mjs --phase after --out docs/qa/screenshots/stage1-public-trust-after`
- Result: `screenshots: 15`, `leakCount: 78`, `visibleLeakCount: 33`, `overflowCount: 0`, `consoleErrorCount: 3`
- This was improved from baseline (`visibleLeakCount: 120`, `consoleErrorCount: 9`) but not fully green.

PR #212 merged:

- Added a guarded non-commerce WooCommerce asset dequeue in `functions.php`.
- Preserves real commerce screens via `nadlan_revenue_is_commerce_screen()`.
- Local checks passed before merge: `php -l functions.php`, `node --check scripts/qa-stage1-public-trust.mjs`, `git diff --check`.

## What Is Partially Done

1. Stage 1 trust cleanup is merged but still needs live theme deployment and final proof.
2. Dimri showroom has tooling and geometry work in PR #209/#210, but these should not be merged blindly. They need review against current main and screenshot evidence.
3. The project-showroom engine is conceptually defined, but still not a complete factory. It needs reliable asset ingestion, facade authoring, interior tour fields, and stable QA.
4. Public trust cleanup may still show raw asset strings in HTML, even if visible leakage is gone. The final QA script should distinguish visible buyer-facing leaks from harmless asset references.

## What Is Not Done

- Final post-#212 live screenshots.
- Confirmation that `/professionals/` no longer logs the `@wordpress/interactivity` module error after #212 is live.
- A real Dimri Yama official facade/elevation render.
- A real Dimri Yama BIM/GLB with apartment-level geometry.
- A polished generated facade engine accepted by the owner.
- A completed Home.com/Matterport-style apartment interior journey.
- Foreign-language versions for Dimri or Rainbow.
- A clean one-shot project factory that can create a new project end-to-end from one data file and assets.
- Cleanup/closure of stale draft PRs and old `.codex-tmp` worktrees.

## Exact Next Steps

Priority order:

1. Sync to current main:
   ```powershell
   git fetch origin main
   git switch main
   git reset --hard origin/main
   ```

2. Deploy current theme main to UPress:
   - This is a theme change, not a plugin update.
   - Pull the UPress server Git copy for the active theme.
   - Clear UPress/site cache.

3. Run final Stage 1 trust QA:
   ```powershell
   node scripts\qa-stage1-public-trust.mjs --phase final --out docs/qa/screenshots/stage1-public-trust-final
   ```

4. Inspect `docs/qa/screenshots/stage1-public-trust-final/report.json`:
   - no visible mini-cart/cart/checkout/debug leakage on home, Join Pro, sitemap, professionals, or Dimri project page,
   - no horizontal overflow,
   - console errors reviewed and explained,
   - one visible H1 on target pages,
   - no `More posts` on project singles.

5. If final QA is green, commit the final screenshots/report on a small docs branch and open a PR.

6. Only after Stage 1 final QA is green, review PR #209 and #210:
   - #209 should be first because #210 is stacked on it.
   - Do not merge #210 without #209 unless it is rebased.
   - Check whether they touch plugin versions, ZIPs, generated assets, or theme only.
   - Require screenshots at 1440/768/390 and real DOM checks.

7. Continue Dimri showroom only in small slices:
   - Mapbox/view broken state or working state,
   - model camera containment,
   - facade docking/geometry,
   - selected-apartment card,
   - lead payload,
   - interior tour/media panel.

## Known Blockers, Risks, And Assumptions

Blockers:

- UPress theme Git pull/cache clear is required before #212 can be verified live.
- Real official Dimri Yama facade/BIM assets are not available in this repo.
- Some open PRs are stale/conflicting and should not be used as source without rebasing.

Risks:

- Plugin ZIP packaging has previously broken the live server due to Windows backslash paths. Always use `scripts/build-plugin-zip.py`.
- Theme changes and plugin changes have different deploy paths. Mixing them creates false "done" claims.
- Old worktrees under `.codex-tmp` and `*-repair` may be stale; do not use them as source of truth.
- The repo is public. Never commit secrets, raw API keys, app passwords, cookies, browser profiles, paid-source rows, or private client data.

Assumptions:

- The next Codex can access the GitHub repo.
- The next Codex may not have this thread, so this packet is self-contained.
- Live WordPress admin/UPress access may exist in Chrome on the original PC, but should not be assumed on a different PC unless the owner grants it.

## Decisions Made And Why

- Stage 1 public trust cleanup comes before more Dimri showroom work because a buyer must trust the site before the product UI matters.
- Theme presentation changes deploy through UPress Git pull, not WordPress plugin updater.
- Plugin changes deploy through the `nadlan-config` update ZIP and healthcheck.
- No fake facades: generated or prototype assets must be clearly labeled as concept/illustrative.
- No silent fallbacks: if a model, facade, Mapbox view, tour, or image fails, show a visible missing/error state.
- Screenshot-or-it-did-not-happen: visual work needs committed screenshots at 1440, 768, and 390 widths.

## Do Not Change Without Asking

- Do not commit secrets or session data.
- Do not manually build plugin ZIPs on Windows.
- Do not merge stale plugin PRs that reduce version numbers or reintroduce old `project-3d.php` code.
- Do not ship a fake CSS/SVG grid and call it a real facade.
- Do not hide failures behind old tower/facade fallbacks.
- Do not start broad Dimri/Rainbow redesign work until #212 is live and final Stage 1 QA is green.
- Do not work from `.codex-tmp` or old repair clones.
- Do not publish or noindex pages without checking SEO intent and owner expectations.

## Definition Of Done For The Immediate Handoff Objective

The next Codex has succeeded when:

1. It syncs to `origin/main` and confirms live plugin healthcheck.
2. It verifies #212 is live after UPress theme pull/cache clear.
3. It runs final Stage 1 public trust QA and commits screenshots/report.
4. It updates `COORDINATION.md` or a new QA doc with exact results and remaining risks.
5. It does not touch Dimri showroom code until trust QA is resolved.

## Suggested First Prompt For Receiving Codex

See `docs/codex-handoff/NEXT_CODEX_PROMPT.md` for a paste-ready prompt.
