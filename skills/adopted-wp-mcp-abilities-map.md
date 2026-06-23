# Adopted WordPress MCP And Abilities Map Skill

> Prevents agents from reinventing WordPress functionality by mapping available site, plugin, REST, MCP, and future Abilities API capabilities before building.

## When to use this

- A feature might already exist in a plugin, REST route, WP admin screen, or external account.
- The owner asks to connect WordPress admin, Lovable, GitHub, email, Drive, or a future content dashboard.
- Building an admin strategy room or contractor intake system.

## Procedure

1. Inventory existing repo modules and REST routes.
2. Inventory WordPress admin capabilities and plugin settings.
3. Check whether the feature is better expressed as:
   - existing plugin setting
   - REST route
   - admin page
   - MCP connector
   - future Abilities API description
4. Do not build custom functionality when a safer existing capability exists.
5. If a plugin capability is important, document it in an agent-readable file before asking agents to use it.

## NadLan adaptation

Before building the owner war-room dashboard, map:

- Lovable handoff reports
- Codex reports
- Claude reports
- release status
- keyword registry
- screenshot QA
- PR and branch state

Keep that map private to admin users.

## Source basis

- Tom Willmot WordPress.com MCP Codex skill: https://github.com/willmot/wordpress-com-codex-skill
- Joost de Valk on agent-ready plugins: https://joost.blog/agent-ready-plugins/
- OpenAI MCP guidance: https://developers.openai.com/codex/learn/best-practices

## Revision log

- 2026-06-23 - Created by Codex from MCP and agent-ready plugin research.
