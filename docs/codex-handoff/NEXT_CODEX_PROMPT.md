# Paste This Into The Receiving Codex

You are taking over the NadLan WordPress repo on a new PC. Read this carefully and do not start coding before syncing.

Repo:

`https://github.com/The-new-ben/nad-lan-co-il`

Clone/use:

```powershell
git clone https://github.com/The-new-ben/nad-lan-co-il.git
cd nad-lan-co-il
git fetch origin main
git switch main
git reset --hard origin/main
```

Read first:

1. `AGENTS.md`
2. `docs/codex-handoff/HANDOFF.md`
3. `docs/codex-handoff/REPO_MAP.md`
4. `docs/codex-handoff/WIRING.md`
5. `docs/codex-handoff/WORK_LOG.md`
6. `docs/codex-handoff/AGENT_COLLABORATION.md`
7. `COORDINATION.md`
8. `skills/skill-release-discipline-and-mistakes.md`
9. `skills/project-page-premium-showroom-runbook.md`

Immediate goal:

Finish Stage 1 public trust cleanup verification. PR #211 and #212 are merged to main. Because they are theme changes, they are not live until the UPress server Git copy is pulled and cache is cleared. Do not start Dimri showroom work until this is verified.

Run checks:

```powershell
git log --oneline -8
git status --short --branch
gh pr list --state open --limit 25 --json number,title,headRefName,baseRefName,isDraft,mergeable,url
Invoke-RestMethod -Uri https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
php -l functions.php
node --check scripts\qa-stage1-public-trust.mjs
```

After UPress theme pull/cache clear, run:

```powershell
node scripts\qa-stage1-public-trust.mjs --phase final --out docs/qa/screenshots/stage1-public-trust-final
```

Expected output from you:

- State current `origin/main` SHA.
- State live plugin version from healthcheck.
- State whether PR #212 is visibly live after UPress pull.
- Commit final Stage 1 screenshots/report if generated.
- If final QA fails, list the exact visible leaks, console errors, and target files.
- Only then propose the next Dimri showroom slice.

Avoid:

- Do not commit secrets, `.env`, browser sessions, `node_modules`, or local cache.
- Do not use old `.codex-tmp` or repair worktrees.
- Do not manually build plugin ZIPs on Windows.
- Do not ship fake facades or silent fallbacks.
- Do not hide failures with CSS stacking.
- Do not claim visual work without committed screenshots at 1440, 768, and 390.
- Do not merge stacked PR #210 before #209 or without rebasing.

If blocked:

Write one concise escalation with:

- what you tried,
- exact command/error,
- why it blocks the next step,
- what unblocks it,
- whether it is theme deploy, plugin deploy, credential, or asset availability.

Do not keep producing new docs/scripts to look busy while a deploy or asset blocker is unresolved.
