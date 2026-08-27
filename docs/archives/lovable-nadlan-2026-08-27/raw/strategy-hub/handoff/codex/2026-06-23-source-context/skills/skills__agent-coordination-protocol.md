# Agent Coordination Protocol

> **Notice to all agents:** the owner has been burned by agents overwriting each other's work. This file specifies the minimum coordination behaviour. If you cannot follow it, stop and ask.

## Handoff log lives in `site-state.md`

Every agent appends a dated block when finishing a task. Format is specified in `../AGENTS.md`. Read the last 5 blocks of `site-state.md` before starting; they are your situation report.

## Branch discipline

- Default working branch for Claude Code sessions invoked via the web/CLI: `claude/charming-meitner-mwVEW` (per harness configuration).
- Codex CLI on the owner's PC: works on whatever branch the owner checks out. **Codex should pull `main` (or the active feature branch) before starting and push before stopping.**
- Antigravity: same rule as Codex.
- Owner merges to `main` when satisfied; `main` deploys to UPress / nad-lan.co.il.

**No agent rebases or force-pushes branches another agent has been on without confirming with the owner.** Diverging history will silently overwrite work.

## "I touched the live site" rule

If you made any change directly inside WordPress admin (installed a plugin, edited Yoast settings, created a page, uploaded media, changed a permalink), you owe TWO writes in the repo before ending the session:
1. A dated block in `site-state.md` describing the change.
2. Either (a) a new commit that mirrors the change in code where possible (theme tweak, content as code) OR (b) a `skills/` update describing the WP-side configuration for the next agent to know.

A live-site change with no repo trace is a contract violation under `AGENTS.md`.

## "I made code changes locally" rule

Commit and push before the session ends. Uncommitted work in an ephemeral container is gone the moment the container reclaims. Commit even imperfect work-in-progress on a feature branch — the next agent can rebase or clean up.

## How to disagree with prior agents' work

You may disagree with what Codex or a prior Claude session did. That's fine. The protocol for changing course:

1. Read the relevant skill file. Understand the intent.
2. If you still disagree, **do not silently rewrite the skill**. Add a section at the bottom:
   ```
   ## Revision YYYY-MM-DD — <agent name>
   The previous guidance to do X was based on assumption Y. Updated guidance:
   do Z because <evidence>. Old guidance remains above for context until
   the owner confirms the change is permanent.
   ```
3. Implement Z. Document in `site-state.md` what you changed and why.
4. Flag to the owner in your reply that there's a revision the previous agent (Codex) should see next time.

## Communication that crosses agents

The owner cannot relay full context between sessions. So any cross-agent message must live in the repo:
- "Codex, please regenerate the hero image at 1600×900 webp" → leave it as a TODO at the bottom of `image-pipeline.md` with a date.
- "Next Claude session, please verify Yoast schema fired" → leave it as a TODO at the bottom of `yoast-config.md`.
- Do not bury TODOs inside long prose. Put them under a `## Open TODOs for next agent` heading.

## What is out of scope for autonomous action

Do not, without explicit owner approval:
- Email or call any third party (broker, lawyer, developer).
- Publish content to the live site (even drafts can leak if scheduled).
- Install a paid plugin or sign up for a paid SaaS.
- Change the domain, SSL, or DNS.
- Migrate the WordPress database.
- Touch any other domain the owner mentioned (legal portals, wife's site).

## What is in scope for autonomous action

- Editing code in the repo on a feature branch.
- Drafting and committing skill files.
- Doing web research and writing it into `docs/research/`.
- Cleaning up the repo, fixing lint, fixing broken markdown.
- Proposing a plan and waiting for approval before applying.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7)._

## Revision 2026-05-28 — UPress Git branch constraint

**UPress's "ניהול GIT" feature only supports the `main` branch.** It will not clone from a PR branch like `claude/charming-meitner-mwVEW`. This is a hard constraint we have to work around.

Implications:
- To deploy any change from a PR branch, the owner must first **merge the PR to `main` on GitHub** (one click on the green "Merge pull request" button), then have UPress Git pull from `main`.
- For testing without affecting the live site: owner can either (a) merge to main on a Friday evening and rollback Sunday if bad, or (b) manually download specific files via the file manager. Both work.
- Agents must keep `main` deployable. Don't push half-finished work to main directly. Use PR branches for work-in-progress, merge to main only when ready to deploy.

## Revision 2026-05-28 — Manual file-manager uploads cause partial states

When the owner uploads files via UPress's file manager (rather than UPress Git), partial syncs are very possible — only the files they happened to drop in get updated; everything else stays at the previous version. This was observed in the 2026-05-28 theme activation, where `style.css` and `functions.php` ended up at an older version than the rest of the theme.

**Protocol:** after any non-Git sync (file manager, FTP, etc.), the next agent MUST run REST verification before assuming anything is deployed. Confirm:
- Active theme version matches the expected version (`/wp/v2/themes?status=active`).
- Key CPTs registered (`/wp/v2/types/<cpt_slug>`).
- Custom Abilities API registrations visible (`/wp-abilities/v1/abilities`).
- Page count and a few page content lengths haven't changed.

Document findings in `site-state.md`.

