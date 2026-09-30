# Agent Collaboration Handoff

## Agents Involved

### Codex

Role:

- Primary implementer.
- Runs local commands.
- Uses Chrome/Playwright/CDP screenshot tooling.
- Opens PRs.
- Should not self-merge when two-key review is active.

Recent Codex work:

- Stage 1 trust cleanup and follow-up (#211, #212).
- Dimri/Rainbow showroom iterations.
- QA scripts and screenshot evidence.

### Claude

Role in prior protocol:

- Reviewer/orchestrator/gatekeeper.
- Writes specs and merges after gate.
- Runs independent checks where possible.
- Often cannot use the same live Chrome/session, so Codex owns visual screenshots.

Recent Claude-related items:

- Reviewed/merged specs and plugin releases.
- Added release discipline/mistake rules.
- Identified and gated fake facade/silent fallback problems.
- Merged or reviewed recent PRs.

### Owner

Role:

- Product direction and final business judgement.
- May perform UPress server Git pulls and WordPress plugin updates.
- Provides official contractor/BIM/facade/interior assets when available.
- Decides whether generated concept assets are acceptable.

## Current Coordination State

Current source of truth:

- GitHub `origin/main` plus live healthcheck.
- Do not rely only on `COORDINATION.md` "NOW" because it can be stale.

Main now includes:

- PR #211 - public trust cleanup.
- PR #212 - non-commerce Woo asset dequeue.

Open PRs that matter:

- #209 - `Add facade engine QA tooling and geometry baseline`
  - branch `codex/facade-engine-standard-1683`
  - base `main`
  - mergeable when inspected.
  - Review before merging. It is likely the next showroom-engine foundation.
- #210 - `v1.68.3 Dimri showroom geometry containment`
  - branch `codex/dimri-geometry-fix-1684`
  - base `codex/facade-engine-standard-1683`
  - stacked on #209.
  - Do not merge before #209 or without rebasing.

Stale/risky PRs:

- #181, #186, #188, #163 and other old drafts are conflicting/stale.
- Treat them as historical, not merge-ready.

## Ownership Boundaries

The old hard file lock on `project-3d.php` was superseded. Current practical rule:

- Codex may implement plugin/theme code.
- Claude or another reviewer should gate/merge when two-key review is active.
- Declare touched files and deploy path before major changes.
- Avoid parallel edits to `project-3d.php`, `functions.php`, or plugin manifest/ZIPs.

Theme vs plugin:

- Theme presentation: repo root, templates, patterns, styles, `functions.php`.
- Plugin infrastructure/runtime: `plugins/nadlan-config/`.
- Project data/assets: `assets/projects/<slug>/`.

## Conflict Avoidance

1. Start every session with:
   ```powershell
   git fetch origin main
   git switch main
   git reset --hard origin/main
   git log --oneline -5
   ```

2. Check open PRs:
   ```powershell
   gh pr list --state open --limit 25 --json number,title,headRefName,baseRefName,isDraft,mergeable,url
   ```

3. Check live plugin:
   ```powershell
   Invoke-RestMethod -Uri https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
   ```

4. If `origin/main` and live disagree, deployment/verification may be the real next step.

5. Do not branch from old `.codex-tmp` or repair folders.

6. Keep each slice small:
   - one problem,
   - one deploy path,
   - one QA report.

7. Do not present baseline screenshots as proof of a fix.

## Open Coordination Issues

- The UPress theme pull/cache clear for PR #212 may still need to happen.
- Final Stage 1 trust screenshots are not yet committed.
- #209/#210 are open and should wait until Stage 1 final QA is green.
- The owner is unhappy with the Dimri concept facade image. Future work should not invest further in that exact image unless the owner accepts it as a temporary demo.
- A long-term facade engine should use real bitmap/render/elevation assets plus polygons. Do not invent another CSS-square facade.

## Links

- Repo: https://github.com/The-new-ben/nad-lan-co-il
- PR #212: https://github.com/The-new-ben/nad-lan-co-il/pull/212
- PR #211: https://github.com/The-new-ben/nad-lan-co-il/pull/211
- PR #209: https://github.com/The-new-ben/nad-lan-co-il/pull/209
- PR #210: https://github.com/The-new-ben/nad-lan-co-il/pull/210
- Live healthcheck: https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
- Dimri page: https://nad-lan.co.il/projects/dimri-yama-sde-dov/
- Rainbow page: https://nad-lan.co.il/projects/rainbow-tel-aviv/
