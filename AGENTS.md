# AGENTS.md — Read this before you touch anything

This repository is operated by multiple AI agents (Claude Code, Codex CLI, Antigravity, possibly others) on behalf of a single human owner. Coordination is mandatory. Drift between agents has already cost work in past sessions. This file is the contract.

## The Prime Directive

**The repo is the source of truth. Not the live WordPress site, not your local memory, not your training data, not the last screenshot.**

Before any action:
1. Read `skills/README.md`
2. Read `skills/site-state.md` (current known state of the live site)
3. Read the specific skill(s) relevant to your task

After any action that changes the live site, the repo, plugins, or content:
1. Update `skills/site-state.md` with a dated entry: who you are, what you did, why, where.
2. If you learned something new, create or extend a skill file under `skills/`.
3. Commit with a message that names the skill you read and the skill you updated.

## Who is who

- **Claude Code (claude.ai/code, web/CLI)** — used for strategy, skill authoring, code review, and high-stakes edits. Expensive. Used sparingly by the owner.
- **Codex CLI** — primary content/code generator. Runs on the owner's Windows PC. Has direct file system access including `C:\Users\pro\.codex\generated_images`. Does most of the production work.
- **Antigravity** — possibly used. Treat as equivalent to Codex for protocol purposes.
- **The owner** — a practicing Israeli lawyer (`עורך דין`). Not a real estate broker. Operates multiple legal portals. This is the highest-priority commercial domain.

## Hard rules

1. **Never commit secrets.** No WordPress passwords, no application passwords, no API keys, no partner names, no lead-buyer pricing. See `skills/security-public-repo.md`. This repo is public.
2. **Never make direct WordPress REST API changes that bypass the repo.** Every change to the live site must trace back to a commit. If you fixed something live without committing, you broke the contract.
3. **Never delete another agent's skill file.** Extend, deprecate, or supersede with a clear note. Knowledge accumulates; it never gets erased.
4. **Never publish public copy that contains internal SEO terms.** See the forbidden-words list in `skills/copywriting-skill.md`.
5. **Never use a content type without checking `skills/wordpress-content-types.md`.** Pages-vs-Posts-vs-CPT decisions are documented; do not improvise.
6. **Stop and ask** if a task requires acting outside the repo (sending email, posting reviews, contacting partners, purchasing plugins). The owner approves these out-of-band.

## When you finish a task

Append to `skills/site-state.md`:

```
### YYYY-MM-DD HH:MM — <agent name>
- Read: <skill files you read>
- Did: <what you actually changed>
- Why: <which goal from skills/strategy-master.md this serves>
- Touched: <repo paths, WP areas, plugins>
- Skills updated: <skill files you created or edited>
- Next agent should: <one-line handoff>
```

If you skip this, the next agent will redo or undo your work. That is the failure mode this file exists to prevent.

---
_Maintained by: any agent. Last structural change: 2026-05-28 by Claude Code (claude-opus-4-7)._
