# Adopted WordPress Playground Verification Skill

> Uses WordPress Playground or wp-env style local verification when a plugin or theme change needs a real WordPress runtime before live deployment.

## When to use this

- A change needs a real WP install but must not touch production.
- A new plugin, theme, block, or admin workflow needs browser proof.
- A future site in the network needs repeatable local setup.

## Procedure

1. Prefer an existing repo-local verification harness if present.
2. If none exists, define a Playground or wp-env plan:
   - mount plugin or theme
   - create sample data
   - enable debug mode
   - login to admin if needed
   - run browser checks
3. Use Playwright to verify public and admin routes.
4. Save screenshots and logs to repo.
5. Do not replace the existing guarded plugin ZIP release gate.

## NadLan adaptation

For this repo, the immediate release gate remains `scripts/build-plugin-zip.py` plus `scripts/verify-plugin-release.py`. Playground is an additional runtime proof when we add admin war-room features or new site replication.

## Source basis

- Brandon Payton quote and WordPress News: https://wordpress.org/news/2026/01/new-ai-agent-skill/
- WordPress Playground agent skill docs: https://wordpress.github.io/wordpress-playground/guides/agent-skill-wp-playground/
- Fellyph Cintra Blueprint skill article: https://make.wordpress.org/playground/2026/04/02/teach-your-coding-agent-to-write-wordpress-playground-blueprints/

## Revision log

- 2026-06-23 - Created by Codex from WordPress Playground agent-skill research.
