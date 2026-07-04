# Codex Local State Inventory and Handoff

Date: 2026-07-04
Machine path inspected: `C:\Users\pro\.codex`
Repo inspected: `C:\Users\pro\Documents\websites\nad-lan-co-il-pr2`

## Bottom Line

`C:\Users\pro\.codex` is not synced into this repo, and it must not be copied into GitHub as a raw folder.

That folder is the Codex desktop runtime, not project source. It contains credentials, browser/session state, logs, SQLite databases, generated caches, plugin caches, local attachments, and temporary files. Pushing it wholesale would leak private operational state and make the repository noisy and unsafe for other agents.

The correct handoff is:

1. Keep project knowledge, skills, designs, screenshots, and build instructions in the repo.
2. Keep local Codex runtime state out of the repo.
3. If a local attachment is useful, audit it first, sanitize it, and place it under a named `handoff/` or `docs/` path with a short README.

## What Is Already Synced in the Repo

After syncing `main`, the repo already tracks a large amount of shareable project material:

- `handoff/claude-design/`
  - mockups
  - generated screenshots
  - showroom engine prototypes
  - GLB assets
  - project page factory files
  - homepage design files
- `handoff/research/`
  - multilingual architecture notes
  - project data prompts
  - full-world enrichment prompts
- `docs/`
  - audits
  - marketing plans
  - playbooks
  - QA screenshots
  - specs
- `skills/`
  - release discipline
  - WordPress deployment
  - project showroom runbooks
  - SEO, content, monetization, visual QA, and plugin discipline

Ground truth checked:

- `git ls-files 'handoff/*' 'docs/*' 'skills/*'` returns 1,864 tracked files.
- `handoff/claude-design/2026-06-28-mockup/` is tracked.
- `handoff/claude-design/2026-07-02-factory-run/` is tracked.
- `handoff/claude-design/2026-07-03-project-page-factory/` is tracked.
- `handoff/research/` is tracked.
- `docs/playbooks/agent-wordpress-deploy-pipeline-handbook.md` is tracked.

## What Exists Only Locally in `.codex`

Top-level local runtime inventory:

| Path | What it is | Repo action |
| --- | --- | --- |
| `auth.json` | Codex/GitHub/auth runtime file | Never commit |
| `config.toml` | Local Codex configuration | Never commit without explicit redaction |
| `cap_sid` | Local session/capability state | Never commit |
| `.sandbox-secrets/` | Secret storage | Never commit |
| `logs_2.sqlite*` | Local logs, hundreds of MB | Never commit |
| `state_5.sqlite*` | Local app state | Never commit |
| `goals_1.sqlite*` | Local goal state | Never commit |
| `memories_1.sqlite*` | Local memory DB | Never commit |
| `sessions/` | Local conversation/session history | Never commit raw |
| `browser/` | Browser runtime state | Never commit |
| `plugins/` | Installed plugin cache | Never commit raw |
| `.tmp/`, `tmp/` | Temporary files | Never commit |
| `.sandbox-bin/` | Bundled/runtime binaries | Never commit |
| `attachments/` | Local pasted-text and uploaded-file cache | Audit before copying any single file |
| `generated_images/` | Local generated images | Audit before copying any single file |
| `skills/` | Local Codex skills | Usually do not copy wholesale; port useful project-specific knowledge into repo `skills/` |

Local directory size observations from the inspection:

- `sessions/`: 117 files, about 5.6 GB
- `plugins/`: 1,887 files, about 343 MB
- `.sandbox-bin/`: about 317 MB
- `.tmp/`: 6,057 files, about 128 MB
- `generated_images/`: 41 files, about 81 MB
- `attachments/`: 49 files, about 1.34 MB
- `skills/`: 93 files, about 0.63 MB

## Local Skills Compared With Repo Skills

Local Codex skill directories currently include:

- `.system`
- `courtai-legal-retrieval`
- `courtai-simulation-adapter`
- `courtai-source-intake`
- `nadlan-real-estate-growth`
- `portfolio-wordpress-seo-publisher`
- `premium-wordpress-site-chrome`
- `seo`
- `seo-content`
- `seo-page`
- `seo-visual`

The repo already has a broad project skill library under `skills/`, including the NadLan-specific release, showroom, SEO, monetization, visual QA, and WordPress deployment rules. Do not bulk-copy the local `.codex\skills` folder into the repo unless each skill is reviewed and intentionally converted into repo format.

Secret-pattern scan against local `.codex\skills` found no obvious live API keys. The matches were instruction text such as `OPENAI_API_KEY`, `secret`, `token`, and `password`, not actual credential values. Still, treat local skills as local tooling until intentionally ported.

## Existing Handoff Warning

The repo already contains captured browser artifacts under `handoff/claude-design/`. At least one old HTML snapshot contains WordPress admin-bar markup from an authenticated browsing session. Future agents must sanitize any browser HTML exports before committing them. Screenshots are usually safer than full logged-in HTML snapshots, but screenshots can still reveal private admin state and must be reviewed.

## Safe Handoff Rule for Future Agents

When an agent asks for "the Codex folder" or "all local context":

1. Do not copy `C:\Users\pro\.codex` wholesale.
2. Read the repo first:
   - `START-HERE.md`
   - `AGENTS.md`
   - `docs/playbooks/agent-wordpress-deploy-pipeline-handbook.md`
   - `skills/skill-release-discipline-and-mistakes.md`
   - `skills/project-page-premium-showroom-runbook.md`
   - `skills/skill-3d-model-pipeline.md`
   - `handoff/claude-design/2026-06-28-nadlan-master-spec.md`
   - `handoff/claude-design/2026-07-02-critical-report-and-full-spec.md`
   - `handoff/claude-design/2026-07-03-project-page-factory/README.md`
3. If local `.codex\attachments` has a missing prompt or zip, copy only that specific file after reviewing it.
4. Put reviewed artifacts under:
   - `handoff/<source>/<date>-<topic>/`
   - `docs/<topic>/`
   - `skills/<skill-name>.md`
5. Add a README explaining where the artifact came from, what it is for, and whether it is production-ready or reference-only.

## Answer to the Owner

No, the entire `.codex` folder is not synced to the repo.

Yes, the important project handoff material is now largely synced in the repo under `handoff/`, `docs/`, and `skills/`.

The missing part was a clear rulebook telling future agents what not to sync from `.codex`, where the shareable knowledge already lives, and how to safely promote any local attachment into the repo. This document is that handoff.

