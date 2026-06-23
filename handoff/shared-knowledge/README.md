# NadLan Shared Knowledge

This folder is the shared memory surface for Codex, Lovable, Claude, and future agents.

Do not leave reusable project knowledge only in chat.

If an agent creates a rule, design decision, prompt, workflow, glossary entry, anti-cannibalization rule, or reusable implementation lesson, it must be committed here or in a dated subfolder under `handoff/`.

## Folder Contract

- `skills/`: reusable agent rules and skill-like workflows.
- `decisions/`: stable product, SEO, design, and technical decisions.
- `prompts/`: reusable prompts that should not be lost in chat.
- `glossary/`: public/private terminology, Hebrew/English naming, and banned/internal phrases.
- `indexes/`: inventories that point to reports, screenshots, branches, and datasets.

## Agent Rules

1. Read this folder before producing major strategy, design, SEO, or implementation work.
2. Add date, author/agent, source, and status to new files.
3. Do not overwrite another agent's work without preserving history.
4. If the rule is public-facing, remove internal language such as "money page", "war room", "KD", "contractor monetization", or "agent prompt".
5. If the rule affects SEO, include the anti-cannibalization target page and support-page relationship.
6. If the rule affects design, include mobile behavior and asset truth rules.
7. If the rule affects implementation, include WordPress file targets and acceptance tests.

## Replication Rule

The NadLan process must be reusable for future WordPress real-estate sites without depending on Lovable. The active reusable workflow is:

`handoff/shared-knowledge/skills/nadlan-3d-ai-replication-system.md`

Codex also has a local skill named `nadlan-3d-ai-replication` for bootstrapping the same process in future projects.

## Lovable-Specific Rule

Lovable should use this folder as project knowledge when possible. If Lovable creates reusable guidance, it should write it to:

`handoff/shared-knowledge/skills/`

or, for run-specific material:

`handoff/lovable/<run-name>/knowledge/`

Then commit and push it to GitHub. Do not keep it only in Lovable chat or `.lovable/`.
