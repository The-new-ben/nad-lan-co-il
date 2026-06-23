# Adopted WordPress Security Threat Gate Skill

> Security review gate for NadLan WordPress plugin, theme, REST, AJAX, upload, admin, and public-form changes.

## When to use this

- Any public form, REST endpoint, AJAX handler, file upload, admin action, SQL, or user data path changes.
- Any AI, concierge, or contractor intake feature.
- Any monetization, lead routing, or payment-adjacent work.

## Three-pillar gate

1. Sanitize and validate input early.
2. Authorize actions with nonces and capabilities where required.
3. Escape output late, at the point of rendering.

## Search checks

- `register_rest_route` without permission callback.
- `$_GET`, `$_POST`, `$_REQUEST` without sanitize and `wp_unslash`.
- `$wpdb` calls without `prepare`.
- `echo` of variables without escaping.
- `wp_ajax_nopriv` without explicit public-intent review.
- upload handling without WP upload APIs and MIME checks.
- `eval`, `shell_exec`, dynamic include, raw unserialize.

## NadLan adaptation

Foreign-investor and contractor-intake surfaces will collect high-value contact data. Treat those as sensitive even when not legally defined as financial forms.

## Source basis

- Jorge Rosal WordPress security review skill: https://github.com/jorgerosal/wordpress-skills
- WordPress sanitizing docs: https://developer.wordpress.org/apis/security/sanitizing/
- WordPress plugin handbook security sections: https://developer.wordpress.org/plugins/

## Revision log

- 2026-06-23 - Created by Codex from WordPress security skill research.
