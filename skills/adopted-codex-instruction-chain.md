# Adopted Codex Instruction Chain Skill

> Keeps Codex behavior stable by front-loading command, done, escalation, and source-of-truth instructions in AGENTS.md and the NadLan master skill.

## When to use this

- A future agent must start reliably without owner supervision.
- Instructions are spread across chat, Lovable, Claude, and repo files.
- Codex is skipping commands, screenshots, or release gates.

## Required instruction order

1. Commands and verification first.
2. Definition of done second.
3. Escalation rules third.
4. Task-specific sections fourth.
5. Style preferences last.

## Verification

Ask the agent to summarize:

- build commands
- definition of done
- no-stacking rule
- screenshot requirement
- release gate

If it cannot repeat those rules, the instruction file is too verbose or not discovered.

## NadLan adaptation

The first reading list is:

1. `AGENTS.md`
2. `COORDINATION.md`
3. `BACKLOG.md`
4. `skills/MAP.md`
5. `skills/nadlan-autonomous-execution-master.md`

## Source basis

- OpenAI AGENTS.md docs: https://developers.openai.com/codex/guides/agents-md
- AGENTS.md standard: https://agents.md/
- Blake Crosley AGENTS.md patterns: https://blakecrosley.com/blog/agents-md-patterns

## Revision log

- 2026-06-23 - Created by Codex from AGENTS.md and instruction-chain research.
