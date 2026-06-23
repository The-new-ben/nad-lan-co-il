# Adopted WordPress REST API Contract Gate Skill

> Keeps NadLan REST endpoints safe, documented, permissioned, schema-shaped, and testable before public or admin features rely on them.

## When to use this

- Adding or changing `register_rest_route`.
- Changing lead intake, listing data, project data, AI concierge, contractor uploads, admin war room, or public search APIs.

## Gate

1. Define route namespace and method.
2. Define input schema and validation.
3. Define permission callback.
4. Public read endpoints must still document why they are public.
5. Write endpoints so responses are stable and typed.
6. Sanitize request params.
7. Escape only at output, not in stored response data.
8. Add or update API map docs.
9. Test success, invalid input, unauthorized, and empty-state responses.

## NadLan adaptation

The future war-room dashboard should read internal reports through admin-only APIs. It must not expose strategy reports, keyword data, agent logs, or monetization language publicly.

## Source basis

- WordPress agent skills `wp-rest-api`: https://github.com/WordPress/agent-skills
- WordPress REST API handbook: https://developer.wordpress.org/rest-api/
- Jorge Rosal WordPress REST skill pack: https://github.com/jorgerosal/wordpress-skills

## Revision log

- 2026-06-23 - Created by Codex from WordPress REST API skill research.
