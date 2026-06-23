# Codex Skills Research And Adoption Log

Date: 2026-06-23

Purpose: document the external Codex, WordPress, and agent-skill sources inspected, what each source says, and which NadLan skill was adopted from it. Raw public repos were cloned to a temporary research folder, inspected, and not copied wholesale into this repo. The committed skills below are adapted to NadLan.

## Downloaded public sources

| Source | Commit inspected | Notes |
|---|---:|---|
| `https://github.com/WordPress/agent-skills.git` | `aa735ea7111c7924ee988306bcef70439e17dec9` | Official WordPress agent skill pack. |
| `https://github.com/Automattic/agent-skills.git` | `48d4aa21d0da0e7bda1c7ac155fef2e16b87aa25` | Archived, moved to WordPress org. |
| `https://github.com/jorgerosal/wordpress-skills.git` | `8c964424d05ba34b3ea5641f7181d4c13829e06f` | WordPress review and triage skills for Claude and Codex. |
| `https://github.com/nathanonn/agent-skills.git` | `90e64e571a2f86a9ebd6d7bdd71117ae83ebca8e` | Goal-bundle skills for autonomous Codex workflows. |
| `https://github.com/willmot/wordpress-com-codex-skill.git` | `0d2fcbbef043e42cbcc5434270609687da023075` | WordPress.com MCP/OAuth/REST Codex skill. |
| `https://github.com/agentsmd/agents.md.git` | `d1ac7f063d20e70015ed6732664049ae4ba9d74e` | AGENTS.md standard examples. |
| `https://github.com/VoltAgent/awesome-agent-skills.git` | `85941348ed4df5efe81e93b1d1c37a5fe41e7cb7` | Agent skill index. |
| `https://github.com/heilcheng/awesome-agent-skills.git` | `de9056857eb0e96da833469d2ee3ac392058225d` | Multilingual agent skill index. |

## What people and sources say, and what we adopted

| # | Person/source | What they say | NadLan adoption |
|---:|---|---|---|
| 1 | OpenAI Codex docs | Skills package instructions, resources, and optional scripts so Codex can follow workflows reliably. Clear descriptions matter for automatic selection. Source: https://developers.openai.com/codex/skills | `adopted-codex-progressive-disclosure.md` |
| 2 | OpenAI Codex best practices | Repeatable work should become skills. Keep each skill scoped to one job and add scripts only when reliability improves. Source: https://developers.openai.com/codex/learn/best-practices | All adopted skill files remain small and single-purpose. |
| 3 | OpenAI AGENTS.md docs | Codex reads AGENTS.md before work and layers global plus project guidance. Source: https://developers.openai.com/codex/guides/agents-md | `adopted-codex-instruction-chain.md` |
| 4 | AGENTS.md project | AGENTS.md is a predictable place for build commands, test commands, code style, and security considerations, used across many agents. Source: https://agents.md/ | `adopted-codex-instruction-chain.md` |
| 5 | Blake Crosley | Put build and test commands first, define done explicitly, add escalation rules, and test whether the agent can recite the instructions. Source: https://blakecrosley.com/blog/agents-md-patterns | `adopted-codex-instruction-chain.md` |
| 6 | WordPress contributors | WordPress agent skills teach assistants WordPress patterns and help avoid outdated patterns, security misses, block deprecation errors, and ignored repo tooling. Source: https://github.com/WordPress/agent-skills | `adopted-wp-plugin-quality-gate.md`, `adopted-wp-rest-api-contract-gate.md`, `adopted-wp-performance-gate.md` |
| 7 | Brandon Payton, WordPress contributor | AI agents work better with a clear feedback loop. The wp-playground skill lets agents test WordPress code while iterating. Source: https://wordpress.org/news/2026/01/new-ai-agent-skill/ | `adopted-wp-playground-verification.md` |
| 8 | Fellyph Cintra | The blueprint skill prevents common schema mistakes because the agent reads a structured reference before writing Blueprints. Source: https://make.wordpress.org/playground/2026/04/02/teach-your-coding-agent-to-write-wordpress-playground-blueprints/ | `adopted-wp-playground-verification.md` |
| 9 | Jorge Rosal | WordPress skills for Claude and Codex cover plugin architecture, security audits, accessibility, testing, release engineering, WP-CLI, Playground, PHPStan, and severity-based output. Source: https://github.com/jorgerosal/wordpress-skills | `adopted-wp-security-threat-gate.md`, `adopted-wp-accessibility-rtl-gate.md`, `adopted-wp-release-agent-gate.md` |
| 10 | Nathan Onn | Goal skills turn rough WordPress specs into GOAL.md, VERIFY.md, and PROGRESS.md for autonomous Codex execution. Source: https://github.com/nathanonn/agent-skills | `adopted-codex-goal-bundle.md` |
| 11 | Tom Willmot | WordPress.com skill verifies site and post access before write workflows and has REST fallback when MCP write tools are unavailable. Source: https://github.com/willmot/wordpress-com-codex-skill | `adopted-wp-mcp-abilities-map.md` |
| 12 | Joost de Valk | Plugins should not be black boxes for agents. AGENTS.md plus ability schemas can tell agents what a plugin already does before they invent duplicate functionality. Source: https://joost.blog/agent-ready-plugins/ | `adopted-wp-mcp-abilities-map.md` |
| 13 | Composio | Webapp-testing is easy to justify because UI work needs real user-flow verification, not code generation and hope. Source: https://composio.dev/content/top-codex-skills | `adopted-codex-visual-proof-loop.md` |
| 14 | Box developer blog | A routing table plus progressive disclosure keeps skills focused; guardrails must be explicit, tested, and use exact fallback conditions. Source: https://blog.box.com/teaching-ai-agents-work-your-content-building-box-skill-openai-codex | `adopted-codex-progressive-disclosure.md` |
| 15 | Varun Dubey | Reliable agents need a scoped purpose, constrained tool access, explicit exit conditions, and hard constraints. Source: https://vapvarun.com/custom-ai-agents-wordpress-plugin-development-repo-tour/ | `adopted-wp-release-agent-gate.md` and master skill updates |
| 16 | Shahibur Rahman | Plugin Check supports WP Admin and WP-CLI, and checks i18n, security, performance, and accessibility for plugin quality. Source: https://dev.to/shahibur_rahman_6670cd024/deep-dive-ensuring-wordpress-plugin-quality-with-plugin-check-pcp-59e9 | `adopted-wp-plugin-quality-gate.md` |
| 17 | unicodeveloper | Codex skills are reusable SKILL.md behaviors and AGENTS.md carries project-level instructions. Source: https://medium.com/@unicodeveloper/9-must-have-skills-for-codex-in-2026-b5124b375eec | Master skill source context |
| 18 | Civil Learning | Codex should be guided like a fast junior developer: slow down, understand, plan, then build. Source: https://medium.com/coding-nexus/my-current-openai-codex-workflow-that-writes-clean-reliable-code-e2d7b5714e34 | `adopted-codex-goal-bundle.md` |

## Skills added to the repo

1. `skills/adopted-codex-goal-bundle.md`
2. `skills/adopted-codex-instruction-chain.md`
3. `skills/adopted-codex-progressive-disclosure.md`
4. `skills/adopted-codex-visual-proof-loop.md`
5. `skills/adopted-wp-playground-verification.md`
6. `skills/adopted-wp-plugin-quality-gate.md`
7. `skills/adopted-wp-security-threat-gate.md`
8. `skills/adopted-wp-performance-gate.md`
9. `skills/adopted-wp-accessibility-rtl-gate.md`
10. `skills/adopted-wp-release-agent-gate.md`
11. `skills/adopted-wp-rest-api-contract-gate.md`
12. `skills/adopted-wp-mcp-abilities-map.md`

## Adoption decision

We did not copy third-party skills blindly. The NadLan repo already has local constraints: public-language hygiene, no CSS stacking, two-key plugin release gate, UPress deployment reality, RTL Hebrew, Lovable sync, and screenshot proof. The adopted skills translate external patterns into those constraints.

## Revision log

- 2026-06-23 - Created by Codex after owner requested deep Codex-skill research, at least ten sources, and adoption into the NadLan master workflow.
