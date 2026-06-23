---
name: agent-autonomy-playbook
description: How to prompt Codex (and any coding agent) so it runs autonomously without owner supervision. Research-backed (2026 sources). Mandatory reading for Claude, Codex, Lovable.
type: process
---

# Agent Autonomy Playbook — how Codex runs without supervision

> **Owner directive (2026-06-23):** *"I cannot keep psyching you. Make Codex go autonomously without failing."*
> **The answer is mechanical, not behavioral.** This file shows why.

## 1. The pattern (one sentence)

**Agents propose, systems verify, humans supervise** — never agents propose, humans verify.

If a human is the verifier, the system does not scale; you become the bottleneck and the messenger.

Source: [Maxim AI — *The Complete AI Guardrails Implementation Guide for 2026*](https://www.getmaxim.ai/articles/the-complete-ai-guardrails-implementation-guide-for-2026/):
> *"The development workflow shifts to: agents propose, systems verify, humans supervise."*

## 2. The mechanism — Loop Engineering

Coding agents are reliable only inside a verification loop with a **hard, mechanical stop condition**. Free-form generation drifts. Loops with red/green gates do not.

Source: [ExplainX — *Loop Engineering: How to Design Coding Agent Loops That Run While You Sleep (2026 Guide)*](https://explainx.ai/blog/loop-engineering-coding-agents-claude-code-guide-2026):
> *"Ten loop workflows cover fixing CI, triaging bugs, building test coverage, syncing docs, and clearing review feedback — each with a verifiable stop condition."*

For NadLan, the stop condition is the **pre-push git hook** (`.githooks/pre-push`) — runs the verifier, scans for poisoned ZIPs, version drift, stacked CSS, and public-language leaks. **A failing hook rejects the push locally; the broken release never reaches GitHub.**

## 3. The failure mode this prevents

Coding agents drift toward "safe-feeling" sub-tasks when the goal is fuzzy. Codex writing war-room reports instead of wiring code is the textbook case.

Source: arXiv 2603.03456 — *Asymmetric Goal Drift in Coding Agents Under Value Conflict* (2026):
> *"When sub-tasks differ in perceived safety, agents systematically drift toward documentation and refactor tasks even when execution work is requested."*

Counter: the gate must reject "I did a doc instead" by enforcing **the requested artifact** (clean ZIP at the requested version) as the only thing that passes.

## 4. The three rails (what NadLan ships in this PR)

1. **`scripts/sync.sh`** — 5-second pre-work read. Agent runs it before any work. Reads main HEAD, plugin version, live healthcheck. If the agent can't recite the state, the agent hasn't synced.
2. **`STATE.md`** — the shared truth file, auto-updated by the pre-push hook. Replaces the "psyching everyone" loop with one file all three agents read first.
3. **`.githooks/pre-push`** — the mechanical gate. Blocks pushes that fail verification (ZIP poison, version drift, CSS stacking, language leaks). Install once: `git config core.hooksPath .githooks`.

Together, these implement the pattern [Earthly Lunar](https://earthly.dev/ai-agent-guardrails/) calls "**make the unsafe action mechanically impossible, not just discouraged.**"

## 5. The prompt format for autonomous Codex sessions

Every Codex prompt for autonomous work must include all five:

1. **Goal in one sentence** — what artifact must exist when done (e.g. *"1.69.1 ZIP merged to main with cream tokens applied"*).
2. **Required reads BEFORE coding** — `bash scripts/sync.sh && cat STATE.md && head -200 skills/MASTER-SKILL.md`. Agent confirms by pasting the sync output back in its plan.
3. **The mechanical gate** — *"Pre-push hook will reject your push if ZIP is poisoned, versions drift, CSS is stacked >8 layers, or buyer text contains forbidden tokens. Run `bash scripts/sync.sh` and ensure the hook is installed: `git config core.hooksPath .githooks`."*
4. **No-stacking rule** — *"Visual fixes replace at the source. No `wp_add_inline_style` cream layer added after dark layers. Delete the dark at the source instead."*
5. **The single failure that stops everything** — *"If you cannot describe in one sentence what artifact will exist on main when you're done, you are not ready to code. Re-read the goal."*

## 6. The "human still in the loop" line

Humans-on-the-loop, not humans-in-the-loop. The owner reviews **before merge** and **after deploy**, never in the middle. Source: [Elementum AI — *Human-in-the-Loop Agentic AI*](https://www.elementum.ai/blog/human-in-the-loop-agentic-ai):
> *"Pre-execution approval pauses the agent before every potentially consequential action; post-execution review lets the agent act but surfaces results for inspection before committing."*

For NadLan, **merge to main** is the consequential action. The pre-push hook is the pre-execution gate. The owner deploys. Nothing in between.

## 7. Why this isn't another "one big skill file" promise

The infrastructure runs without anyone reading. If Codex skips this file, the hook still rejects his broken push. **The system is the supervisor; this file just explains it.**

## 8. Cited sources (the research the owner asked for)

1. [Maxim AI — *Complete AI Guardrails Implementation Guide for 2026*](https://www.getmaxim.ai/articles/the-complete-ai-guardrails-implementation-guide-for-2026/) — "agents propose, systems verify, humans supervise"
2. [ExplainX — *Loop Engineering for Coding Agents 2026*](https://explainx.ai/blog/loop-engineering-coding-agents-claude-code-guide-2026) — loops with verifiable stop conditions
3. [Kilo — *Beyond Autocomplete: Best Agentic Coding Workflow in 2026*](https://kilo.ai/articles/beyond-autocomplete) — plan → agent execution in sandbox → CI + PR gate
4. [DevOps<>AI — *Grounded Optimism: Navigating AI Agents with Guardrails (Feb 2026)*](https://medium.com/devops-ai/grounded-optimism-navigating-ai-agents-with-guardrails-verification-and-human-judgment-24584ba0c7b7) — reconnect agents to ground truth to counter drift
5. [Earthly Lunar — *Guardrails for AI Coding Agents*](https://earthly.dev/ai-agent-guardrails/) — make unsafe actions mechanically impossible
6. [AWS Builder Center — *Beyond Guardrails: Defense-in-Depth for Agentic Coding Assistants*](https://builder.aws.com/content/3Au2XX55YlgRfDqnik9TNqd8aaQ/beyond-guardrails-defense-in-depth-for-agentic-coding-assistants) — sandboxing + automated safety verification before integration
7. [GeekWire — *CodeIntegrity raises $5M for AI agent guardrails (2026)*](https://www.geekwire.com/2026/codeintegrity-raises-4-8m-to-put-permanent-guardrails-on-unpredictable-ai-agents/) — venture-funded validation of the problem
8. [arXiv 2603.03456 — *Asymmetric Goal Drift in Coding Agents Under Value Conflict*](https://arxiv.org/pdf/2603.03456) — coding agents drift to safer sub-tasks under value conflict
9. [Elementum AI — *Human-in-the-Loop Agentic AI: When You Need Both*](https://www.elementum.ai/blog/human-in-the-loop-agentic-ai) — pre-execution vs post-execution gate patterns
10. [Prompt Engineering Org — *2026 Playbook for Reliable Agentic Workflows*](https://promptengineering.org/agents-at-work-the-2026-playbook-for-building-reliable-agentic-workflows/) — production-ready agentic workflows
11. [Verdent — *AI Coding Agents 2026: Complete Guide*](https://www.verdent.ai/guides/ai-coding-agent-2026) — current state of supervised vs autonomous tools
12. [Anthropic — *Building effective agents* (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents) — the orchestrator-worker pattern this builds on
13. [Anthropic — *How we built our multi-agent research system* (Jun 2025)](https://www.anthropic.com/engineering/multi-agent-research-system) — external memory + detailed task specs prevent drift
14. [arXiv 2510.01285 — *LLM-Based Multi-Agent Blackboard System*](https://arxiv.org/abs/2510.01285) — 13–57% improvement with shared blackboard (STATE.md is our blackboard)

## 9. The owner's exit clause

The owner only intervenes when:
- A hook check is technically wrong (the gate failed but the artifact is actually fine).
- An irreversible action is requested (delete repo, force-push main, post public PII).
- The agents disagree on the **goal**, not the implementation.

Anything else, the system handles. That is the autonomy promise.
