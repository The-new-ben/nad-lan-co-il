# skills/ — The shared brain

Every agent (Claude, Codex, Antigravity) reads from here before acting and writes back here after acting. This is not documentation _about_ the project; it _is_ the project's operating knowledge.

## Read order for a fresh session

1. `../AGENTS.md` — the contract between agents
2. `README.md` — this file
3. `site-state.md` — what is true about the live site right now
4. `strategy-master.md` — the full Hebrew strategy brief (the deliverable)
5. `monetization-lawyer-angle.md` — owner is a lawyer; this changes everything
6. `agent-coordination-protocol.md` — how we don't run over each other
7. The specific skill for your task (e.g. `wordpress-content-types.md`, `yoast-config.md`, `image-pipeline.md`)

## Index

| File | Purpose | Owner-readable? |
|---|---|---|
| `strategy-master.md` | The full Hebrew SEO/content/design/business brief | Yes (he) |
| `honesty-statement.md` | What's verified vs assumed vs needs-paid-data | Yes |
| `monetization-lawyer-angle.md` | Revenue model rebuilt around the owner being a lawyer | Yes |
| `agent-coordination-protocol.md` | Rules for Codex/Antigravity/Claude coexistence | No (internal) |
| `wordpress-content-types.md` | When to use Page vs Post vs CPT | No |
| `yoast-config.md` | Target Yoast configuration + current status | No |
| `image-pipeline.md` | How to handle `C:\Users\pro\.codex\generated_images` | No |
| `copywriting-skill.md` | Hebrew tone, voice, forbidden words | No |
| `visual-design-skill.md` | Colors, typography, components | No |
| `security-public-repo.md` | What MUST NEVER be committed (repo is public) | No |
| `original-prompt-2026-05-28.md` | The Laravel prompt that triggered this brief | Yes |
| `site-state.md` | Living snapshot, append-only log | Yes |

## Rule: skills are append-mostly

You may:
- Add new skills.
- Add new sections to existing skills.
- Add dated revision notes at the bottom of a skill.
- Mark sections as DEPRECATED with a reason.

You may not:
- Delete a skill file.
- Silently rewrite a section without a revision note.
- Move strategy into a chat reply and skip writing it here.

## Rule: every action emits a skill or a state update

If a task taught you something reusable (a Yoast quirk, a plugin conflict, a Hebrew RTL CSS gotcha, a SERP shift), that goes into the relevant skill. If a task only changed the site, that goes into `site-state.md`. If both, do both.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7) during the "research brief" task._
