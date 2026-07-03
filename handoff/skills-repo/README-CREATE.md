# Create the shared skills repo (2 minutes, owner action needed)

My GitHub access in this session is scoped to nad-lan-co-il only, so I could
not create the new repository myself (403). Everything is prepared - the
`repo/` folder next to this file IS the complete repo content. Two ways:

## Option A - GitHub web (no terminal)
1. https://github.com/new -> name: `agent-skills` -> Private -> Create.
2. On the new repo page: "uploading an existing file" -> drag the CONTENTS of
   `handoff/skills-repo/repo/` (the `skills/` and `docs/` folders + README.md)
   -> Commit.

## Option B - terminal (one paste)
```bash
git clone https://github.com/The-new-ben/nad-lan-co-il
gh repo create The-new-ben/agent-skills --private
cd "$(mktemp -d)" && git init -b main
cp -r /path/to/nad-lan-co-il/handoff/skills-repo/repo/* .
git add -A && git commit -m "seed: shared agent skills library"
git remote add origin https://github.com/The-new-ben/agent-skills
git push -u origin main
```

## After it exists
- Give future agent sessions access to BOTH repos (when connecting a session,
  include `The-new-ben/agent-skills` in the repo scope). From then on I can
  push skill updates there directly.
- I will keep updating `.claude/skills/` in THIS repo in parallel, as ordered,
  and mirror changes into `handoff/skills-repo/repo/` so the bundle never
  goes stale until the real repo exists.
