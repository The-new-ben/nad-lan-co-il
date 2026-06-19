# COORDINATION.md — shared billboard between Claude and Codex

> **Audience:** Claude, Codex, owner. **Read FIRST every session.** This file is the *single shared truth*. If it isn't here, it isn't coordinated.
> **Update protocol:** append; don't overwrite. Sign every entry with: `agent · UTC time · commit SHA (if relevant)`. Last writer wins for the "NOW" section only — everything else is history.

---

## 0. Research grounding (why this file exists at all)

This billboard implements three patterns from published research:

1. **Orchestrator–Worker** (Anthropic, *Building effective agents*, Dec 2024): "a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results." We apply it as: **Claude = orchestrator/reviewer, Codex = worker/implementer.** Source: https://www.anthropic.com/engineering/building-effective-agents
2. **External memory + detailed task specs** (Anthropic, *How we built our multi-agent research system*, June 2025): "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries. Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information." This file IS the external memory. Source: https://www.anthropic.com/engineering/multi-agent-research-system
3. **Blackboard architecture** (Engelmore & Morgan, 1988; recently revived for LLMs — Liu et al., *LbMAS*, arXiv:2510.01285, Oct 2025): a shared knowledge structure all agents read/write. 2025 measurements: **13–57% relative improvement in end-to-end success** over baselines that lack a blackboard. Sources: https://arxiv.org/abs/2510.01285 · https://arxiv.org/pdf/2507.01701

Trunk-based discipline (Atlassian: https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development): "every developer must ensure that the main branch is in a deployable state and any merged changes were successfully integrated." We use this with one mainline (`origin/main`), short-lived branches, and the file-ownership table below.

**Bottom line, per Anthropic's own guidance:** simplest tool that works. One file. Two agents. Read it. Update it. Don't invent a framework.

---

## 1. ROLE SPLIT (updated 2026-06-19 by owner)

| Concern | Codex (Implementer) | Claude (Orchestrator + QA gate) |
|---|---|---|
| **Code edits** | ✅ writes them, including `project-3d.php` (M7 superseded — owner decision 2026-06-19) | reviews specs, comments on PRs, edits only on request |
| **Live browser / Chrome** | ✅ drives clicks, captures screenshots from Chrome integration | cannot — uses server-side HTTP probes only |
| **Spec / research** | reads spec, asks if unclear | ✅ writes the spec, cites references |
| **PR gate** (php -l, JS check, ZIP guard, version audit) | runs locally | ✅ re-runs before merge (M5: no claim without command) |
| **Merge to main** | ❌ never merges own PRs | ✅ merges after gate passes |
| **Live verification** (healthcheck, screenshots, page diff) | captures live screenshots, posts here | ✅ confirms healthcheck version, demands proof |
| **Deploy click** (plugin updater / server git pull) | owner-only action | owner-only action |

**Two-key rule:** implementer ≠ merger. Codex commits & pushes; Claude reviews & merges. No exceptions.

---

## 2. NOW (live state — both agents overwrite this section on update)

```
git main HEAD:  a1f1820  ·  plugin version: 1.67.5
live plugin:    1.67.4   ·  DEPLOY GAP — owner: update plugin in WP-Admin → 1.67.5
live theme:     Dimri assets serving 200 (verified 2026-06-19)
open PRs:       —
active branches:—
last live healthcheck: 2026-06-19 (Claude)
```

---

## 3. CODEX — Next 5–10 steps (Codex writes; Claude reviews inline as `> REVIEW (Claude):`)

Codex acknowledges cadence+CoT · 2026-06-19T17:48:19Z

> Template Codex pastes:
> ```
> ### Codex plan · UTC <time>
> Goal in one sentence: _______
> 1. [ ] step ...  (touches: <files>) (deploy-path: PLUGIN / THEME / NONE)
> 2. [ ] step ...
> ...
> 5. [ ] step ...
> Acceptance gate I will satisfy: <healthcheck flag / screenshot path / file presence>
> Blockers I see: <none / list>
> ```
> Claude then comments inline. Codex proceeds when Claude says `> APPROVED` or after 10 minutes if no blocker is flagged (own-the-assumption rule).

---

## 4. CLAUDE — Next 5 steps (Claude writes; Codex may flag)

*(empty — Claude fills before next session)*

---

## 5. BLOCKERS

*(format: `<agent> · UTC · one sentence · what unblocks it · owner of the unblock`)*

- Claude · 2026-06-19 · live plugin behind main (1.67.4 vs 1.67.5) · owner clicks Update in WP-Admin Plugins · owner

---

## 6. DONE (proof-backed log — append-only)

*(format: `UTC · agent · one line · commit SHA · proof: live URL / screenshot path / healthcheck JSON path`)*

- 2026-06-19 · Codex · 1.67.5 generic project copy fix shipped · `a1f1820` · proof: pending live verification (need owner deploy)
- 2026-06-19 · Codex · Dimri page metadata wired, modelViewers 0→1, 4 unit controls render · (post meta change, not commit) · proof: `docs/qa/screenshots/live-2026-06-19-rainbow-dimri-after-meta/dimri-after-click-1440.png`
- 2026-06-19 · Codex · interior-journey design doc committed · `a1f1820` · proof: `docs/design/2026-06-19-project-showroom-engine-interior-journey.md`
- 2026-06-19 · Claude · M9/M10 + architecture boundary added to discipline skill · `8f55939` · proof: `skills/skill-release-discipline-and-mistakes.md`
- 2026-06-19 · Claude · 1.67.4 duplicate-hero fix · `55bee8a` · proof: ZIP entry check, `nlp3d-intro-hero` absent
- 2026-06-19 · Claude · 1.66.1 poisoned-ZIP defused + builder guard · `92a7966` · proof: `scripts/build-plugin-zip.py` refuses backslash

---

## 7. PROOF STANDARD (M5 + new M11)

Every "done" claim above MUST cite at least one of:
- a **commit SHA on `origin/main`** (not a local commit), OR
- a **live URL with HTTP 200** + content excerpt, OR
- a **screenshot file path inside the repo** (`docs/qa/screenshots/…`) committed with the change, OR
- the **live healthcheck JSON** showing the new flag, committed as `docs/qa/healthcheck-<version>.json`.

"It compiled," "I rebuilt the ZIP," "PHP lint should pass" are **not proof.** Per skill M5.

For **visual changes** (CSS/layout/copy), a screenshot is **mandatory** — committed to repo, not posted in chat only. Per new skill M11.

---

## 8. SESSION-START COMMAND (both agents, every session)

```bash
cd <YOUR-ONE-CANONICAL-CHECKOUT>      # Codex: C:\Users\pro\nad-lan-co-il (NOT .codex-tmp, NOT *-repair)
git fetch origin main && git checkout main && git reset --hard origin/main
# 1) read this file
cat COORDINATION.md | head -120
# 2) read the discipline skill
head -80 skills/skill-release-discipline-and-mistakes.md
# 3) live state
curl -s https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck | python3 -c "import json,sys;d=json.load(sys.stdin);print('live version:',d['version'])"
# 4) git state
echo "main: $(git rev-parse --short HEAD) $(grep -m1 Version: plugins/nadlan-config/nadlan-config.php)"
# 5) IF the two versions differ -> next action is DEPLOY, not new code.
```

If you can't paste this state at the top of your status update, you haven't synched. Don't code yet.

---

## 9. ANTI-PATTERNS (the failures we paid for)

Cross-referenced to the discipline skill mistake catalog:

- Working in `.codex-tmp` / `-repair` / parallel folders → **M9**. The folder you can't show the owner is the folder where commits go to die.
- Bumping version below `origin/main` → **M1**. Always grep main first.
- Branching off a base older than `origin/main` → **M2**. Rebase first or your PR is a regression.
- Windows backslash ZIPs → **M3**. Use `scripts/build-plugin-zip.py`. Verify entries.
- "PHP lint should pass" without running it → **M4 + M5**.
- Theme PR with no server `git pull` follow-up → **M10**.
- More docs/scripts while real blocker is deploy → **M6**.
- Saying "deployed" when you mean "merged" → **M0 / M8**.
- Editing a file the other agent is also editing → **M7** (now mitigated by the two-key rule in §1, but file-level lock-in still preferred — declare it in §3/§4 first).

---

## 10. WHEN OWNER IS AWAY

- Codex follows §3 plan; if blocked, writes BLOCKED in §5 with what unblocks it; doesn't ship docs to look busy (M6).
- Claude reviews PRs as they come in; merges after gate; updates §6 DONE with proof; updates §2 NOW.
- Neither agent makes irreversible decisions (deploys, public-facing content publishes, destructive ops) without owner.
- Both agents stop and surface ambiguity rather than guess. Direct quote from Anthropic's research-system writeup: *"Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information."* When in doubt, ask in §5.

---

## 11. COMMUNICATION CADENCE — initiate, never block *(owner directive 2026-06-19)*

There is **no live socket** between Claude and Codex — the owner relays asynchronously. So classic heartbeat/timeout polling doesn't map directly; the rule that does is **graceful degradation + idempotency** (Maxim, *MAS reliability*; gossip-protocol literature): never hang waiting for the other agent.

**Rules:**
1. **Both initiate. Neither waits silently.** If you have a unit of work and a safe default, do it and log it. Don't poll "is the other agent done yet."
2. **Never block on the other agent for a *reversible* action** (a branch, a draft, a screenshot). Act on the documented safe default, leave a reconciliation note in §5, move on.
3. **Always require the second key for *irreversible* actions** — merge to main, deploy, publish content, destructive ops. These wait for the other agent / owner. (Two-key rule, §1.)
4. **Heartbeat = a timestamped line.** On starting and finishing any unit, append to §6 DONE (finished) or §3/§4 (starting). That line IS your "I'm alive" signal. Silence with no line = treat as stalled.
5. **Don't re-ping faster than one work cycle.** Consensus literature calibrates election timers to **2–2.5× the commit interval** to avoid thundering-herd ([MultiPaxos](https://arxiv.org/pdf/2405.11183)); analogously, don't re-ask a question you already posted until a full cycle passed — read §5 first, the answer may already be there.
6. **Review window:** when Codex posts a §3 plan, Claude reviews at next sync. If Claude hasn't flagged a blocker and the change is reversible, Codex proceeds and owns the assumption. Claude still gates + merges (two-key).

## 12. CHAIN-OF-THOUGHT DISCLOSURE — mandatory in every update *(owner directive 2026-06-19)*

Every status update, PR body, and §6 DONE entry MUST carry a short **REASONING** block so the other agent and owner can audit decisions and catch drift early:

```
REASONING
- SAW:     the evidence I observed (command output / screenshot path / healthcheck field)
- THOUGHT: why that evidence led to my conclusion
- DID:     the action I took, and why this approach over the alternative(s)
- CHECKED: how I verified it worked (the exact command / live URL / committed screenshot)
```

This is not optional narration. "I fixed X" without SAW/CHECKED is rejected at review (ties to M5/M11). If you can't fill CHECKED with a real artifact, the work isn't done.

## 13. OPEN DEFECTS — live Dimri/Rainbow (Claude, 2026-06-19, evidence-based)

Verified from live HTML of `/projects/dimri-yama-sde-dov/` (server-side; Codex must confirm visually + console):

1. **Floating buttons stacked** — `11` `position:fixed` elements; lead FAB + AI bot (`#nlai`) + WhatsApp(×2) all anchored to one corner at `bottom:10/18/20/62/145/205/207/273px`, `left:10px`. On mobile this is an overlapping tower. → Collapse into ONE expandable action rail (single FAB → expands). `compact_floating_actions_v1672` did not fully solve it on this page.
2. **Mapbox present but not rendering** — assets ARE there (`3` mapbox-gl script refs, token present, `5` `nlp3d-view-map` els) → it's a **runtime** failure, not a missing-asset failure. Codex (Chrome): capture console errors — likely token rejected (401), or container has 0 height, or it only inits behind a broken "live view" toggle.
3. **Model "weird spin"** — `model-prototype.glb` is an 8.5 KB generated *massing box*, not a real building; `auto-rotate` on a crude box looks wrong, and it tumbles because polar (vertical) orbit isn't locked. → Constrain orbit to azimuth-only + lock `min/max-camera-orbit` polar to a single angle, OR drop auto-rotate, until a real GLB exists. This is a placeholder-asset problem first, a config problem second.
4. **Facade not user-practical** — SVG prototype facade; `48` cells render but the mapping to a believable building face is weak. → Needs a real elevation image with traced polygons, or much better cell geometry. Same honest limit as Rainbow: 2.5D facade until BIM.

---


- Anthropic — *Building effective agents* (Dec 2024): https://www.anthropic.com/engineering/building-effective-agents
- Anthropic — *How we built our multi-agent research system* (Jun 2025): https://www.anthropic.com/engineering/multi-agent-research-system
- Liu et al. — *LLM-Based Multi-Agent Blackboard System for Information Discovery in Data Science* (arXiv:2510.01285, Oct 2025): https://arxiv.org/abs/2510.01285
- *Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture* (arXiv:2507.01701, Jul 2025): https://arxiv.org/pdf/2507.01701
- *CodeCRDT: Observation-Driven Coordination for Multi-Agent LLM Code Generation* (arXiv:2510.18893, Oct 2025): https://arxiv.org/pdf/2510.18893
- Atlassian — *Trunk-based Development*: https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development

---

## 14. ACTIVE SPECS (Codex implements; Claude provides)

- **2026-06-19 — 3D camera lock + facade dismissible + CMS wiring** → `docs/design/2026-06-19-camera-orbit-and-facade-dismiss-spec.md` · target version **1.67.6** · Codex builds, Claude reviews/gates/merges. Owner verbatim citations in §1 of the spec.
- *(M11 reminder: PR must include screenshots at 1440 / 768 / 390 under `docs/qa/screenshots/v1676-camera-facade/`.)*
- **2026-06-19 — Functional facade (polygons not squares, compounds, click→views+info)** → `docs/design/2026-06-19-functional-facade-polygons-compounds-spec.md` · target **1.68.0** · research-cited (Interactive Real Estate, Render Vision, VisEngine). Sequence: after 1.67.6.
- Engelmore & Morgan, *Blackboard Systems* (1988) — classic foundation; see also Hayes-Roth, *A blackboard architecture for control* (1985).
