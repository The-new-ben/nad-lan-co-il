# AGENTS.md

> **What this file is.** The contract every AI agent (Claude / Codex / Cowork /
> ChatGPT-via-browser / Gemini / any future tool) follows in this repository.
> Format: the [AGENTS.md open specification](https://agents.md/) — the
> Linux-Foundation-stewarded Markdown standard adopted by 60,000+ repos and all
> major AI coding tools since OpenAI shipped it with Codex CLI in August 2025.
> Plain Markdown, H2 sections, no schema, no special syntax.
>
> Read this FIRST. Every session. No exceptions.

---

## Project overview

This repository operates **nad-lan.co.il** — a Hebrew real-estate authority site
combining a directory of verified professionals + projects (sourced from
data.gov.il), money-pillar content (mortgage, tax, urban renewal, lawyer),
calculators, an AI concierge, and a tracked lead/commission ledger. The owner
also runs a network of sibling sites (legal portal, travel/relocation, regional
desks); see `skills/SKILLS-TREE.md` for the portable-DNA stamp used when opening
a new site.

The site runs **WordPress 7.0 / PHP 8.5** with a custom theme and the
**`nadlan-config`** plugin (this repo's `plugins/nadlan-config/`). Payments go
through **WooCommerce + Green Invoice (Morning)** gateway. The repo is **public**
— no secrets, no partner names, no client data, ever.

---

## Prime directive

**The repo is the source of truth.** Not the live WordPress site, not your local
memory, not your training data, not the last screenshot. If they disagree, the
repo (after a fresh `git fetch origin main`) wins.

A code change that is not (a) on `origin/main`, (b) inside a bumped
`plugin-dist/nadlan-config-<ver>.zip`, and (c) advertised by
`plugin-dist/nadlan-config.json` on `origin/main` — **does not affect the live
site**. Editing a `.php` file alone does nothing. See
[`skills/codex-plugin-access-and-deploy.md`](skills/codex-plugin-access-and-deploy.md)
for the 9-step ship loop and every pre-solved blocker.

---

## Mandatory reading at session start

In this exact order:

1. This file (`AGENTS.md`)
2. [`BACKLOG.md`](BACKLOG.md) — current priority queue + shipped log
3. [`skills/MAP.md`](skills/MAP.md) — categorised index of every skill
4. [`skills/site-state.md`](skills/site-state.md) — **last 6 dated blocks** only
5. Any specific skill named in the user's task (the MAP lists which to open
   when)

**Before changing the plugin**: also read
[`skills/codex-plugin-access-and-deploy.md`](skills/codex-plugin-access-and-deploy.md).
**Before publishing/renaming any page**: also read
[`skills/url-namespace-contract.md`](skills/url-namespace-contract.md).

---

## Setup, build, deploy

This repo has **no `npm install` / no `make` / no test harness yet** — the
plugin is plain PHP, the theme is plain PHP+CSS. The "build" is producing a ZIP.
The "deploy" is the owner clicking Update in WP-admin after a merge to `main`.

**Plugin ship loop** (canonical reference:
[`skills/codex-plugin-access-and-deploy.md`](skills/codex-plugin-access-and-deploy.md)):

```bash
git fetch origin main                                              # always branch off latest main
git checkout -b <agent>/<topic-version> origin/main
# edit plugins/nadlan-config/inc/<module>.php
# add new module to the foreach() loader in plugins/nadlan-config/nadlan-config.php
# bump version in BOTH places in plugins/nadlan-config/nadlan-config.php
fail=0; for f in $(find plugins/nadlan-config -name "*.php"); do php -l "$f" >/dev/null 2>&1 || { echo "FAIL $f"; fail=1; }; done
[ $fail -eq 0 ] && echo "ALL CLEAN"                                # MUST be clean
cd plugins && rm -f /tmp/nadlan-config-<ver>.zip && zip -rq /tmp/nadlan-config-<ver>.zip nadlan-config -x "*.DS_Store" && cd ..
cp /tmp/nadlan-config-<ver>.zip plugin-dist/nadlan-config-<ver>.zip
# update plugin-dist/nadlan-config.json (version + download_url + changelog)
# HARD GATE — verify each new module IS INSIDE the built zip:
unzip -p plugin-dist/nadlan-config-<ver>.zip nadlan-config/inc/<new-module>.php | grep -c '<unique-signature>'
git add -A && git commit -m "vX.Y.Z <summary>" && git push -u origin <branch>
# open PR → squash-merge → tell owner to click Update in WP-admin
```

The ZIP MUST have a top-level `nadlan-config/` folder. Always verify with
`unzip -l <zip> | head`.

**Multi-agent coordination**: see
[`skills/agent-coordination-protocol.md`](skills/agent-coordination-protocol.md).
Coordinate version numbers (`git show origin/main:plugin-dist/nadlan-config.json`
tells you the current version). Don't both edit the same `inc/` module in
parallel branches.

---

## Code style and conventions

- **PHP floor: 7.4** (`Requires PHP: 7.4`). No `match()`, no named args, no
  enums, no constructor promotion, no first-class callable syntax. Arrow
  functions `fn()` OK.
- **One capability per module file.** `inc/<topic>.php` does one thing. See
  [`skills/nadlan-config-plugin.md`](skills/nadlan-config-plugin.md) and
  [`skills/plugin-discipline.md`](skills/plugin-discipline.md).
- **Guard every function** with `function_exists()` and start every file with
  `if ( ! defined( 'ABSPATH' ) ) { exit; }`.
- **Prefix `nadlan_`** on every function, class, option, and post-meta key.
- **Escape output** (`esc_html`, `esc_url`, `esc_attr`), **sanitize input**
  (`sanitize_*`, `wp_unslash`), **nonce-check or cap-check every write**.
- **No public-facing internal language.** Public copy never mentions CRM, UTM,
  paid lead, supplier routing, money pages, revenue, or internal operating
  terms. See [`skills/copywriting-skill.md`](skills/copywriting-skill.md) and
  the forbidden-words list there.
- **Hebrew RTL** rules: use logical CSS properties (`inset-inline-start`, not
  `left`); use `direction: rtl`; see
  [`skills/design-rtl-hebrew.md`](skills/design-rtl-hebrew.md).
- **Slugs are Latin only.** Hebrew titles are fine; URLs are
  `[a-z0-9-]+`. See
  [`skills/url-namespace-contract.md`](skills/url-namespace-contract.md).

---

## Hard boundaries (do NOT do these)

1. **Never commit secrets.** No WP passwords, app passwords, API keys, partner
   names, closed prices, lead-buyer rates, customer data. See
   [`skills/security-public-repo.md`](skills/security-public-repo.md). The repo
   is public.
2. **Never expose tooling/internal terms in public copy** (CRM, UTM, paid lead,
   supplier routing, money pages, etc.). Customer-facing only.
3. **Never publish a page without checking** the URL namespace + cannibalization
   rules in [`skills/url-namespace-contract.md`](skills/url-namespace-contract.md).
4. **Never use a content type** without checking
   [`skills/wordpress-content-types.md`](skills/wordpress-content-types.md). Pages
   vs Posts vs CPT decisions are documented; do not improvise.
5. **Never edit another agent's open module** in a parallel branch. Coordinate
   first. The `inc/` modules have implicit ownership; ask before encroaching.
6. **Never claim a UI/behavior change is "live" without curl-verifying** the
   live HTML signature. After every plugin ship, fetch the live page and grep
   for the signature class/string that proves it. See the "honesty statement"
   section below.
7. **Never `git checkout <otherbranch> -- file`** on a branch where you already
   have working-tree edits to that file. It silently clobbers your edits and
   has shipped no-op commits twice. Use `cp` from a known-good copy instead.
8. **Stop and ask** if a task requires acting outside the repo (sending email,
   posting reviews, contacting partners, purchasing plugins, changing DNS).
   The owner approves these out-of-band.

---

## Honesty statement (non-negotiable)

This is canon across every agent that operates here. From
[`skills/honesty-statement.md`](skills/honesty-statement.md):

- **No flattery.** Tell the owner the truth even when uncomfortable.
- **Cite or flag.** If a claim is non-obvious, cite the source (URL, file path,
  live REST output). If you can't, say "I'm uncertain".
- **Verify, don't claim.** A UI/behavior claim without a curl verification is a
  lie. The `unzip -p ... | grep` "ZIP content gate" is mandatory before every
  merge.
- **Money truth.** Plumbing ≠ revenue. Be explicit about what earns ₪ today
  vs. what's wired but waiting on traffic/partners/etc.

---

## Adding knowledge (skills accumulation)

When you learn something worth keeping, follow
[`skills/ACCUMULATION.md`](skills/ACCUMULATION.md). Short version:

- **Portable method/pattern** → new file under `skills/<name>.md` + add row in
  `skills/MAP.md`.
- **One-shot outcome (audit, migration, launch)** → file under
  `docs/<YYYY-MM-DD>-<topic>.md`.
- **Current decision/task** → append to `BACKLOG.md`.
- **State change on live site** → append a dated block to
  `skills/site-state.md`.
- **New plugin module** → also add the filename to the `foreach()` loader in
  `plugins/nadlan-config/nadlan-config.php` and to
  `skills/SKILLS-TREE.md` (DNA branch).
- **Credentials / private values** → STOP. Public repo. Document only the env
  var name.

---

## Where common things live

| What | Path |
|---|---|
| Skills index (the map) | `skills/MAP.md` |
| Prime directive (you're reading it) | `AGENTS.md` |
| Backlog + shipped log | `BACKLOG.md` |
| Live situation report | `skills/site-state.md` |
| Access map (public-safe) | `HANDOFF.md` |
| Plugin source | `plugins/nadlan-config/` |
| Plugin deploy guide | `skills/codex-plugin-access-and-deploy.md` |
| URL/slug law | `skills/url-namespace-contract.md` |
| Portable DNA branches | `skills/SKILLS-TREE.md` |
| Skills accumulation protocol | `skills/ACCUMULATION.md` |
| Implementation logs / handoffs | `docs/<date>-<topic>.md` |

---

## Sources (research behind this AGENTS.md and the skills system)

These are the real specifications and best-practice sources we built on. Cite
them if you need to argue an approach.

- **AGENTS.md open specification** — the canonical spec this file follows:
  [agents.md](https://agents.md/),
  [particula.tech / explained](https://particula.tech/blog/agents-md-ai-coding-agent-configuration),
  [augmentcode.com / 2026 guide](https://www.augmentcode.com/guides/how-to-build-agents-md),
  [codersera.com / complete guide](https://codersera.com/blog/agents-md-complete-guide-2026/),
  [agentsindex.ai](https://agentsindex.ai/agents-md),
  [research paper on AGENTS.md impact](https://arxiv.org/pdf/2601.20404)
  (35–55% fewer agent bugs when detailed).
- **Claude Code Skills convention** — Anthropic's own skill structure (SKILL.md
  directory pattern, YAML frontmatter, description-as-trigger):
  [code.claude.com / skills docs](https://code.claude.com/docs/en/skills),
  [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en),
  [awesome-claude-skills (curated list)](https://github.com/ComposioHQ/awesome-claude-skills),
  [Nimbalyst / practical 2026 guide](https://nimbalyst.com/blog/claude-code-skills-guide/),
  [DEV / practical guide](https://dev.to/muhammad_moeed/claude-code-skills-a-practical-guide-for-2026-3f6p).
- **Lean-collection rule** (8–12 well-chosen skills > 60 vague ones; descriptions
  do the heavy lifting): synthesised from the Anthropic guide and the
  Composio/Nimbalyst pieces above.
- **Knowledge-as-Code pattern** — knowledge base as a normal repo (forkable,
  auditable, agent-readable via plain text):
  [knowledge-as-code.com](https://knowledge-as-code.com/),
  [Doc-Serve Agent Skill](https://medium.com/spillwave-solutions/empowering-ai-coding-agents-with-private-knowledge-the-doc-serve-agent-skill-8d9683534758),
  [Autonomous Code Documentation / augmentcode.com](https://www.augmentcode.com/guides/autonomous-code-documentation).
- **Source-code taxonomy of coding-agent architectures**:
  [arxiv.org / Inside the Scaffold](https://arxiv.org/pdf/2604.03515).

---

## Revision log
- 2026-06-03 — Rewritten to the AGENTS.md 2026 open spec (Claude). Added
  citations, the "Hard boundaries" list including the git-clobber rule and the
  ZIP-content gate, the skills accumulation pointer, and the location map.
  Triggered by owner observation that agents (including Codex) couldn't reliably
  find or extend skills. Pairs with the new `skills/MAP.md` and
  `skills/ACCUMULATION.md`.
- Earlier — Initial AGENTS.md drafted with prime directive + read order. Kept
  in git history.
