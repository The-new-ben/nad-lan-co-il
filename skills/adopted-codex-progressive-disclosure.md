# Adopted Codex Progressive Disclosure Skill

> Keeps large workflows usable by routing Codex to the one relevant reference file instead of loading every report, skill, and handoff at once.

## When to use this

- A task mentions many topics but only one surface is being changed.
- A skill file is becoming too large.
- Codex is missing important rules because context is crowded.

## Routing table

| If the task is about | Read first |
|---|---|
| Showroom visual port | `handoff/lovable/2026-06-23-war-room-sync/data/nadlan-tokens.css` and `handoff/shared-knowledge/skills/nadlan-showroom-design-rules.md` |
| Plugin release | `skills/codex-plugin-access-and-deploy.md` and `skills/adopted-wp-release-agent-gate.md` |
| Public copy | `skills/copywriting-skill.md` |
| SEO/cannibalization | `skills/internal-linking-hub-spoke.md` and `skills/url-namespace-contract.md` |
| Security | `skills/adopted-wp-security-threat-gate.md` |
| Performance | `skills/adopted-wp-performance-gate.md` |
| Visual proof | `skills/adopted-codex-visual-proof-loop.md` |

## Rules

- Use one primary skill plus only the references needed for the slice.
- Do not paste massive instructions into public pages or PR descriptions.
- If a rule becomes repeatable, move it into a skill and add it to the routing table.

## Source basis

- OpenAI Codex skills: https://developers.openai.com/codex/skills
- Box Codex skill article: https://blog.box.com/teaching-ai-agents-work-your-content-building-box-skill-openai-codex
- WordPress agent-skill principles: https://github.com/WordPress/agent-skills

## Revision log

- 2026-06-23 - Created by Codex from progressive-disclosure research.
