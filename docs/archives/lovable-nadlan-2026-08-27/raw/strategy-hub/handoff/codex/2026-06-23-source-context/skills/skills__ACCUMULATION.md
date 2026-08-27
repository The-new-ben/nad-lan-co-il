# SKILLS ACCUMULATION — the protocol

> **Purpose.** A precise, low-friction protocol any agent (Claude / Codex / Cowork /
> human) follows when they learn something worth keeping. The goal: **knowledge
> compounds, nothing is lost, and the next agent finds it in under 60 seconds.**
>
> This file IS the policy. If you change the policy, update this file + the
> Revision log at the bottom + a one-line note in `BACKLOG.md`.
>
> Based on real best practices for agent-readable knowledge (sources cited in
> `AGENTS.md`): the AGENTS.md open standard (OpenAI, Aug 2025), Claude Code's
> Skills convention (Anthropic, 2025-26), and the Knowledge-as-Code pattern.

---

## 1. The "what to do when you learn X" decision tree

```
You learned something. Choose ONE bucket:
├── It's a portable METHOD/PATTERN (reusable on other sites/projects)
│      → write/extend a skill under skills/<name>.md and add to MAP §1-7
├── It's a one-shot OUTCOME (a migration, an audit, a launch)
│      → write a dated implementation log under docs/<YYYY-MM-DD>-<topic>.md
├── It's a CURRENT decision or open task
│      → append to BACKLOG.md (P0/P1/P2/P3/P4/P5)
├── It's something that HAPPENED (state change on the live site)
│      → append a dated block to skills/site-state.md
├── It's a brand-new code module
│      → ship the module + update skills/SKILLS-TREE.md (DNA branch) + the
│        loader in plugins/nadlan-config/nadlan-config.php
└── It's a credentials / private value
      → STOP. The repo is public. Never commit. Document only the env-var name.
```

If you can't pick one bucket, default to **`docs/<date>-<topic>.md`** + a one-line
pointer in `BACKLOG.md`. We'd rather over-capture into docs/ than lose the lesson.

---

## 2. How to WRITE a new skill (the file)

Every skill is a flat Markdown file at `skills/<kebab-name>.md`. The naming
convention: short, kebab-case, no version suffix unless replacing a versioned
predecessor. Example: `url-namespace-contract.md`, NOT `URL_Namespace_v2.md`.

### Minimum viable skill template

```markdown
# <Skill title — what it lets the reader do>

> One-paragraph summary in italics or blockquote: WHAT this is, WHO it's for
> (Claude / Codex / Cowork / human?), and WHEN to open it. This is what every
> other agent skims first.

## When to use this

Three bullet points max. Be specific. Vague triggers = skill never fires.

## The rules / steps / data

The actual content. Numbered steps for procedures. Tables for reference data.
Code blocks for commands. Keep it ≤ 300 lines unless it's a runbook.

## What NOT to do

Counter-examples. The land mines.

## Revision log
- YYYY-MM-DD — Created/changed by <agent>. Reason.
```

### Quality rules (lifted from best practice)
- **Description first.** The first sentence has to be specific enough that any
  agent skimming the MAP knows whether to open this. "Helps with payments" is
  too vague. "WooCommerce + Green Invoice (Morning) gateway: products 476/477,
  the one-charge limitation, how to ship a new SKU" is right.
- **One topic per file.** If you find yourself writing "Part 2 about X" — that's
  a new skill, not a section.
- **Cite-or-flag.** If a claim is non-obvious, cite the source (a URL, a file
  path with line numbers, or the live REST/healthcheck output that proves it).
  No claims without evidence — see `skills/honesty-statement.md`.
- **Mark portability.** If portable across sites, tag with 🟪 DNA in the MAP.

---

## 3. How to REGISTER the new skill (make it discoverable)

A skill that isn't indexed is invisible. Two updates are mandatory after writing
a new skill file:

1. **`skills/MAP.md`** — add a row in the correct section (1-7). Pick a status
   marker (✅ ACTIVE / 🟡 REFERENCE / 🟪 DNA / ⚠️ DEPRECATED). Write the
   "When to open" column tersely (≤ 15 words).
2. **`BACKLOG.md` shipped log** — append a one-liner so the next agent reading
   the backlog sees what changed.

If the skill is **portable DNA** (reusable on the owner's other network sites):
3. **`skills/SKILLS-TREE.md`** — add a row in the right branch with a reuse note.

If the skill describes a NEW workflow that should be the default for an existing
type of work, also:
4. **`AGENTS.md`** — add a one-line pointer in the relevant section so it's
   triggered by the prime-directive read.

---

## 4. How to UPDATE an existing skill

- **Never delete content.** Mark the old section "Superseded YYYY-MM-DD" and keep
  it, OR move it to a "Historical" section at the bottom.
- **Always append a Revision line** at the bottom (date + agent + what + why).
- If the change is significant enough that other skills cross-reference the old
  behavior, do a `grep -r` for the old skill name across the repo and update
  cross-references in the same commit.
- If the file becomes too long (> 500 lines) — split it into two files and add
  a cross-link section.

---

## 5. How to RETIRE a skill (deprecate, don't delete)

When a skill is genuinely superseded:

1. Add a banner at the top of the old file:
   ```
   > **⚠️ DEPRECATED YYYY-MM-DD** — superseded by [skills/<new>.md](./...). Kept for history.
   ```
2. Mark it `⚠️ DEPRECATED` in `skills/MAP.md` section 9.
3. Do **NOT** `git rm` it. Old skills are git-blame anchors; deletion erases the
   reasoning behind earlier decisions.

---

## 6. Where things live (the canonical map)

| Path | What goes there |
|---|---|
| `/AGENTS.md` | Prime directive. Edit only when the protocol itself changes. |
| `/BACKLOG.md` | Living priority queue + shipped log. Append every session. |
| `/HANDOFF.md` | Public-safe access map. Edit when access changes. |
| `/README.md` | One-paragraph project intro for humans landing here. |
| `skills/MAP.md` | Categorised skills map. Update on every new/deprecated skill. |
| `skills/ACCUMULATION.md` | This file. The protocol. |
| `skills/SKILLS-TREE.md` | Portable-DNA tree for stamping new sites. |
| `skills/site-state.md` | Append-only dated situation report. Append every session. |
| `skills/<name>.md` | Reusable skills (methods, rules, conventions). |
| `docs/<date>-<topic>.md` | One-shot logs, audits, handoffs, migrations. |
| `plugins/nadlan-config/inc/<module>.php` | Plugin code modules (one capability each). |

---

## 7. Network-DNA stamp (for the owner's other sites)

When opening a new site in the network (legal portal, travel/relocation, etc.),
the **portable DNA** branch of `skills/SKILLS-TREE.md` lists exactly what to copy.
The bootstrap order is documented there. **Never** clone site-specific keyword or
data files; **always** carry the operating-system + plugin-engine + design-system
skills.

---

## 8. The 60-second discovery test (every skill must pass)

A new agent walks in cold. They run:

```
cat AGENTS.md
cat skills/MAP.md
```

That's it. If your new skill isn't findable from MAP within 60 seconds, the
indexing failed — fix MAP, not the skill. **An unindexed skill does not exist.**

---

## Revision log
- 2026-06-03 — Created (Claude). Codifies the protocol that was previously
  implicit. Triggered by owner observation that agents (including Codex)
  couldn't reliably find/extend skills. Built on three real best practices:
  the AGENTS.md open spec, Anthropic's Claude Code Skills convention, and the
  Knowledge-as-Code pattern. Sources in `AGENTS.md`.

