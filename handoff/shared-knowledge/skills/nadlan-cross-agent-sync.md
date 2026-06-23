# NadLan Cross-Agent Sync Skill

Status: active

Use this whenever Codex, Lovable, Claude, or another agent works on NadLan strategy, design, SEO, showroom, content, WordPress, or monetization.

## Goal

Keep all agents working from the same project memory and prevent chat-only decisions from disappearing.

## Required Read Order

1. `handoff/shared-knowledge/README.md`
2. Latest `handoff/codex/lovable-prompts/`
3. Latest `handoff/lovable/`
4. Latest `handoff/codex/`
5. Relevant `skills/` files or `handoff/codex/*/skills/`
6. Relevant source reports and screenshot inventories

## Write Rules

- Lovable writes Lovable outputs under `handoff/lovable/<run-name>/`.
- Codex writes Codex outputs under `handoff/codex/<run-name-or-file>`.
- Shared reusable rules go under `handoff/shared-knowledge/`.
- Do not write important decisions only in chat.
- Do not write only Markdown when the owner needs a readable artifact; add HTML or spreadsheet-style output when useful.
- Every major run needs a `source-manifest.md` with source repo, branch, commit, file list, and missing items.

## Sync Rules

- If Lovable outputs are created in `https://github.com/The-new-ben/nadlan-strategy-hub`, Codex imports them into `https://github.com/The-new-ben/nad-lan-co-il`.
- If Codex creates prompts or source context for Lovable, Codex mirrors them into the Lovable hub repo under the same path.
- Do not ask the owner to manually copy files when GitHub sync is available.
- If a branch contains potentially relevant work, record it in an inventory before assuming it is merged.

## Anti-Drift Rules

- Showroom first does not mean small strategy. It is the first sellable wedge.
- NadLan competes across the full Israeli real-estate money market.
- Hard keywords are phased, not excluded.
- Missing assets must be labeled honestly; do not fake maps, facades, GLBs, Matterport, legal/tax advice, or price offers.
- Public UI must not leak internal language.
