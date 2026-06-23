# STATE.md — current ground truth

> **Audience:** Claude, Codex, Lovable, owner. Read FIRST. Update on every push.
> **Source of truth ranking:** this file > COORDINATION.md > anyone's memory.
> **Auto-updated by:** `.githooks/pre-push` (on successful push). Manual edits allowed but the hook will overwrite the auto-managed fields on next push.

---

## NOW (auto-managed; do not hand-edit the values below — the hook rewrites them)

```
git main HEAD       : 8643e74
plugin version (git): 1.68.2
live plugin version : 1.68.2
plugin in-sync      : YES
last push           : 2026-06-23 · Claude · sync infra
active release      : 1.69.1 (Codex implementing — cream tokens applied to dark showroom)
open blocker        : none
```

## What's happening (hand-managed, short)

- **Codex**: applying Lovable's `nadlan-tokens.css` cream skin to the showroom → bumping to **1.69.1** → ZIP → verifier → PR.
- **Lovable**: delivered `handoff/lovable/2026-06-23-war-room-sync/data/nadlan-tokens.css` (verified vanilla CSS, all tokens, 8 `@font-face` rules, HE/EN/RTL, component→pattern map). Not blocked on anything.
- **Claude**: gating Codex's 1.69.1 PR when it lands. Built sync infra in this commit so future packaging mistakes are blocked by the git pre-push hook, not by Claude eyeballing claims.
- **Owner**: not in the loop until 1.69.1 PR is gate-passed → review → deploy plugin update.

## Next gate (the only thing that matters)

When Codex pushes 1.69.1: pre-push hook auto-verifies all 6 version surfaces + ZIP cleanliness. If hook passes → safe to merge. If hook fails → Codex fixes locally, push is rejected before reaching GitHub.

---

## How to use this file (for every agent, every session)

**Before any work**, run:
```bash
bash scripts/sync.sh
```
This prints the current state in 3 seconds. If you can't read this state, you haven't synced — don't code yet.

**After any push**, the pre-push hook (`.githooks/pre-push`) auto-rewrites the NOW block. Install once with:
```bash
git config core.hooksPath .githooks
```
After that, every `git push` runs the verifier first. A broken release (poisoned ZIP, version drift, lint fail) is **rejected by git locally** — it never reaches GitHub.

---

## Why this file exists (one line)

The owner shouldn't be the messenger between agents. This file is.
