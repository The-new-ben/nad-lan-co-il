# agent-skills - the shared skills library

One repo, every project, every agent. Skills here are the working contracts
that agents (Claude Code, Cowork, chat suites) load before touching a project.
The source of truth for a skill lives HERE; projects consume copies or
symlinks and may add project-specific overrides.

## What is inside

```
skills/
  wordpress-agent-deploy/SKILL.md   # the WordPress deploy pipeline law
  aesthetic-ownership/SKILL.md      # owner-mode critique + verified delivery
docs/
  agent-wordpress-deploy-pipeline-handbook.md  # deep reference (10 parts)
```

## How to consume

**Claude Code, one project** (skills auto-load from the repo):
```bash
# inside the project repo
mkdir -p .claude/skills
cp -r /path/to/agent-skills/skills/* .claude/skills/
```
Or keep it live with a submodule:
```bash
git submodule add https://github.com/The-new-ben/agent-skills .claude/skills-shared
# then copy or symlink the skills you want into .claude/skills/
```

**Claude Code, machine-global** (every project on the machine):
```bash
git clone https://github.com/The-new-ben/agent-skills ~/agent-skills
mkdir -p ~/.claude/skills
ln -s ~/agent-skills/skills/* ~/.claude/skills/
```

**Any other agent or chat** (Cowork, ChatGPT, custom suites): paste the
relevant SKILL.md body into the session/system prompt. The files are written
to work standalone.

## Rules of the library

1. A skill is a CONTRACT, not advice. Agents must follow it or say why not.
2. Update skills here first, then sync consuming projects. Projects may carry
   local project-specific skills (e.g. a design-DNA yardstick) that extend a
   shared one; the shared file stays generic where possible.
3. Every hard-won production lesson (outage, false positive, recovery drill)
   gets folded back into the relevant skill the same day it is learned.
4. No secrets, ever. Skills reference env vars and admin screens, never values.

## Provenance

Born on nad-lan.co.il (The-new-ben/nad-lan-co-il) after 30+ production
releases through the agent deploy pipeline. That repo keeps its own synced
copies under `.claude/skills/`.
