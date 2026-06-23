# Adopted WordPress Release Agent Gate Skill

> Separates implementation from release packaging so Codex does not mix feature coding, version bumping, artifact building, PR proof, and deployment claims.

## When to use this

- A plugin version is about to ship.
- A ZIP, manifest, cache-buster, or health version changes.
- A PR is being prepared for review.

## Release-only scope

Allowed:

- version surfaces
- cache-busters
- manifest
- ZIP built by guarded builder
- verifier output
- changelog or PR summary
- screenshots and QA report

Not allowed:

- new feature logic during final packaging
- hand-built ZIPs
- deploy claims without live proof
- merging own PR when the two-key gate is active

## Gate

1. Confirm implementation commits are done.
2. Bump all version surfaces.
3. Build ZIP with guarded builder.
4. Run verifier.
5. Inspect ZIP safety.
6. Capture screenshots.
7. Push and open PR.
8. Wait for gate review.

## Source basis

- Varun Dubey on scoped WordPress agents and exit conditions: https://vapvarun.com/custom-ai-agents-wordpress-plugin-development-repo-tour/
- OpenAI hooks docs: https://developers.openai.com/codex/hooks
- Git hooks reference: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
- Existing NadLan release discipline: `skills/skill-release-discipline-and-mistakes.md`

## Revision log

- 2026-06-23 - Created by Codex from WordPress release-agent research and NadLan ZIP failures.
