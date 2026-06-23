# Adopted Codex Goal Bundle Skill

> Converts a vague NadLan feature request into a bounded autonomous execution slice with objective, verification, progress, screenshots, and stop conditions.

## When to use this

- A request is too broad for direct coding.
- The owner says "goal", "mission", "work standalone", or "do not ask questions".
- The slice needs autonomous Codex execution without losing proof.

## Procedure

1. Write a one-sentence objective.
2. Define the public outcome and exact files likely to change.
3. Split into one slice only: showroom, homepage, listings, city page, admin war room, or release packaging.
4. Write acceptance criteria with proof:
   - command proof
   - desktop screenshot
   - mobile 390 screenshot
   - public-language scan
   - release artifact check when plugin code changes
5. Write stop conditions:
   - spending credits
   - live deploy
   - missing credentials
   - legal/public wording approval
   - contradictory source of truth
6. Update `skills/nadlan-autonomous-execution-master.md` if the goal creates a reusable workflow.

## NadLan adaptation

Do not create a new `/goal` if an existing app goal is active. Continue the active goal and record the working slice in `COORDINATION.md` or the PR body.

## Source basis

- Nathan Onn, `wp-spec-to-goal`: https://github.com/nathanonn/agent-skills
- OpenAI Codex best practices: https://developers.openai.com/codex/learn/best-practices
- Civil Learning Codex workflow: https://medium.com/coding-nexus/my-current-openai-codex-workflow-that-writes-clean-reliable-code-e2d7b5714e34

## Revision log

- 2026-06-23 - Created by Codex from external goal-bundle research.
