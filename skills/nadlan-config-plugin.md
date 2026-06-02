# Plugin: `nadlan-config` — the lead-capture foundation

> **Notice to all agents:** this plugin is the runtime backbone of the lead-capture monetization model (`monetization-lawyer-angle.md`). When the theme's `functions.php` fails to load custom code (which happened in the 2026-05-28 sync), this plugin is the resilient fallback that keeps the CPT and lead handler alive. **Read before editing the theme `functions.php`.**

> **Deploy update, 2026-06-02:** the old manual upload/delete flow below is historical.
> The active deploy source of truth is now `skills/codex-plugin-access-and-deploy.md`:
> bump plugin version in two places, build `plugin-dist/nadlan-config-X.Y.Z.zip`, update
> `plugin-dist/nadlan-config.json`, merge to `main`, then the owner clicks Update in
> WP Admin. Editing PHP files alone does not affect the live site.

## What it does (current — v1.0.3)

1. Registers the **`nadlan_lead`** custom post type — private, admin-only, with `dashicons-money-alt`. Every public lead form submits to this CPT.
2. Registers a public **lead-form admin-post handler** at `admin_post(_nopriv)_nadlan_lead`. Validates nonce, sanitizes 11 fields (name, phone, email, goal, city, budget, timeline, message, source_url, utm_source, utm_campaign + a hashed IP), inserts a private `nadlan_lead` post with meta, emails `admin_email`, redirects with `?lead=received`. Bad nonce → `?lead=bad_nonce`.
3. Exposes a **`[nadlan_lead_nonce]` shortcode** that outputs the hidden nonce and action inputs for the form, so the Codex-built homepage form (raw HTML inside a Gutenberg block) can include them without PHP.
4. Exposes a **healthcheck REST endpoint**: `GET /wp-json/nadlan/v1/healthcheck` — returns plugin version, php_version, wp_version, and `cpt_present` boolean. Public, no auth. Used by any agent to confirm the plugin is loaded after a deploy.

That's it for v1.0.2. **Deliberately minimal** because earlier versions (mu-plugin v1.0.0, plugin v1.0.1 with Hebrew strings + lead-form handler + anonymous-function init + nested REST callbacks) failed to load on this WordPress 7.0 + UPress environment. Path-to-success was: strip everything → confirm load → add features back incrementally.

## Where it lives

- **Repo source of truth:** `plugins/nadlan-config/nadlan-config.php`
- **Live server:** `/wp-content/plugins/nadlan-config/nadlan-config.php`
- **NOT in:** the theme. NOT in `mu-plugins/`. Both alternatives were tried and failed on this host.

## Install / update flow

The owner installs / updates via standard WP admin upload, not via UPress Git. (UPress Git into `/wp-content/plugins/...` is possible in principle but adds a second sync target; we keep it simple.)

To ship a new version:
1. Agent edits `plugins/nadlan-config/nadlan-config.php` in the repo.
2. Bump the `Version:` header in the file's docblock.
3. Run `cd plugin-build && rm -rf nadlan-config && cp -r ../plugins/nadlan-config . && rm -f ../nadlan-config.zip && zip -r ../nadlan-config.zip nadlan-config/`. (The `plugin-build/` and `nadlan-config.zip` paths are gitignored — they are build artifacts only.)
4. Commit the source. Push to PR branch.
5. Send the ZIP to the owner via `SendUserFile`.
6. Owner: WP Admin → Plugins → installed plugins → **Delete** the existing NadLan Config → Plugins → Add New → Upload Plugin → choose the new ZIP → Install → Activate.
   - WP does NOT support uploading an update over an existing plugin. The old version must be deleted first OR the owner can manually overwrite files via UPress file manager (riskier — leaves stale files).
7. Owner reports back; agent verifies via `GET /wp-json/nadlan/v1/healthcheck` and checks the version field.

## Confirmed environment (verified 2026-05-28 via healthcheck)

- WordPress: **7.0** (Abilities API live as `wp-abilities/v1`)
- PHP: **8.5.5**

The PHP 8.5 confirmation is critical: **all modern PHP syntax is safe to use**, including `str_ends_with`, `str_starts_with`, first-class callable syntax (`func(...)`), readonly properties, named arguments, match expressions, enums, constructor property promotion, etc. The "Requires PHP: 7.2" in the plugin header is a portability floor, not a feature ceiling — we can use anything PHP 7.4+ and not worry.

## Roadmap (incremental, only after each step verifies)

### v1.0.3 — lead-form handler (SHIPPED 2026-05-28)

Add back the `admin_post_nadlan_lead` / `admin_post_nopriv_nadlan_lead` handler so the public lead form on the homepage actually stores submissions. Specifically:
- `nadlan_config_handle_lead()` — wp_verify_nonce + sanitize + wp_insert_post + update_post_meta + wp_mail to admin_email.
- Sanitization helper `nadlan_config_clean( $key )`.
- All field meta keys: `name`, `phone`, `email`, `goal`, `city`, `budget`, `timeline`, `message`, `source_url`, `utm_source`, `utm_campaign`.

After install, test from the live homepage's form. Confirm a `nadlan_lead` post appears in WP admin AND the admin gets an email.

### v1.0.4 — Abilities API registrations (after v1.0.3 stable)

The owner's intent (recorded in `agent-tooling-strategy.md`) is for AI agents to introspect this site via `/wp-json/wp-abilities/v1/abilities`. Register `nadlan/get-pillars`, `nadlan/get-calculators`, `nadlan/get-cities`, `nadlan/get-lead-stats`.

**Important:** the earlier v1.0.0 attempt at registering abilities silently failed. Cause unknown — possibly the `wp_register_ability` signature on WP 7.0 differs from what I guessed (`label`, `description`, `input_schema`, `output_schema`, `execute_callback`, `permission_callback`). Before v1.0.4 ships:
1. Agent must inspect the WP 7.0 actual abilities-api source code, e.g. `https://github.com/WordPress/wordpress-develop/tree/trunk/src/wp-includes/abilities-api` or equivalent.
2. Verify the exact argument names and types.
3. Test by registering ONE ability first, confirm it appears at `/wp-abilities/v1/abilities`, then add the other three.
4. **Wrap in `try { ... } catch ( Throwable $e ) { error_log( ... ); }`** so a future API breaking change doesn't kill the entire plugin again.

### v1.0.5+ — incremental additions (no specific ETA)

- Custom REST endpoints for lead intake from external sources (Antigravity bot, Zapier webhook).
- Stats endpoints with `manage_options` permission gating.
- Webhook fan-out for new leads (mortgage broker partner, lawyer-owner intake CRM).
- Self-service `nadlan_professional` CPT for the directory monetization model (Phase 1 of `agent-tooling-strategy.md`).

Each version: ship minimum delta, verify via healthcheck, then plan the next slice.

## What to NEVER do in this plugin (lessons from failures)

These rules came from concrete observed failures. Don't repeat them.

1. **Don't ship multiple new features in one version.** v1.0.1 tried CPT + lead-form + abilities + Hebrew labels all at once → fatal on activation, no info about which part failed. v1.0.2 with just CPT loaded clean. Lesson: one capability per release until we have logging.

2. **Don't put Hebrew strings in code paths that fire during activation** until we know the host's encoding handling. The v1.0.2 strip removed Hebrew labels; the activation worked. Once we have logging in v1.0.3+, we can test Hebrew CPT labels carefully. Until then, keep CPT labels in English; they show only to admins anyway.

3. **Don't rely on `mu-plugins/` on this host.** Confirmed in v1.0.0 attempt: a file dropped into `/wp-content/mu-plugins/nadlan-config.php`, verified in the file manager, did NOT load. UPress may sandbox mu-plugins. Use regular plugins.

4. **Don't put runtime code into the theme's `functions.php`** beyond theme-specific setup. The theme can be swapped, broken, or partially synced (which happened on 2026-05-28). Logic that must survive theme changes belongs in this plugin.

5. **Don't add a plugin activation hook** (`register_activation_hook`) until we've tested logging. If the activation hook errors, WP shows "fatal error" with no detail. Lazy-init via `init` hook is safer.

6. **Don't add anonymous functions to `add_action` until you're sure** the host's PHP setup handles them. They DO work on PHP 8.5.5, but if a future host migration drops PHP version, anonymous funcs are harder to debug.

## How a future agent verifies the plugin is loaded

```
curl https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
```

If returns JSON with current version → loaded.
If returns 404 → not loaded. Check WP Admin → Plugins → is it active?
If returns 500 → fatal error. Owner must check WP error log or deactivate the plugin via file rename in file manager.

## Open TODOs

- [ ] Ship v1.0.3 — add lead-form handler. Test with the homepage's existing form. Verify a `nadlan_lead` post is created on submission.
- [ ] Research the actual `wp_register_ability` signature on WP 7.0 BEFORE shipping v1.0.4.
- [ ] After v1.0.4 ships and works, remove the four `wp_register_ability` calls from the theme's `functions.php` — they belong here, not in the theme. (The theme's copy isn't even loading right now, so this cleanup is just hygiene.)

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7) after the v1.0.2 activation succeeded._

## Revision 2026-05-28 late night — v1.0.4 LIVE

v1.0.3 failed activation with no diagnostic info. The bisect step v1.0.4:
- Removed: the `[nadlan_lead_nonce]` shortcode
- Added: `function_exists` guards around every function declaration

v1.0.4 activated cleanly. Healthcheck confirms `lead_handler_loaded: true`, `cpt_present: true`, PHP 8.5.5, WP 7.0.

**Open question:** unproven whether v1.0.3 failed because of the shortcode OR because of a function-name collision from v1.0.2 not being fully deleted first. Future versions should keep the `function_exists` guards regardless.

## v1.0.5 — planned changes (NOT YET SHIPPED, owner approval gate)

Adds two capabilities the homepage actually needs to capture leads:

1. **`[nadlan_lead_form]` shortcode** — renders a complete working `<form>` element. Inside: action=admin-post.php, hidden nonce + action fields, all 8 input fields (name, phone, email, goal, city, budget, timeline, message) with Hebrew labels, submit button. CSS-light; styling via theme palette. The form is the conversion mechanism for the lead-capture monetization model.

2. **REST-write registration for Yoast meta keys**:
   ```php
   register_meta( 'post', '_yoast_wpseo_metadesc', array(
       'show_in_rest'      => true,
       'single'            => true,
       'type'              => 'string',
       'auth_callback'     => function() { return current_user_can('edit_posts'); },
   ) );
   register_meta( 'post', '_yoast_wpseo_title', array( /* same */ ) );
   ```
   Unblocks bulk REST writes of Yoast meta descriptions (currently 42 pages × empty = major SEO miss). After v1.0.5, an agent can iterate all pages and write Hebrew descriptions via REST.

**Owner approval required** because v1.0.5 means another plugin delete + upload + activate cycle. Trade-off: one more upload buys the lead-capture form AND unlocks bulk Yoast description writes.


## v1.3.0 (2026-05-31) - robots.txt + wptexturize disable
- `robots_txt` filter: serves User-agent rules + `Sitemap: /sitemap_index.xml`. Respects the "discourage search engines" toggle. CAVEAT: only works if the web server routes /robots.txt to index.php. Live /robots.txt currently returns nginx 404 (request not reaching WP) - after deploy, verify; if still 404, the host must add `location = /robots.txt { try_files $uri /index.php?$args; }` or drop a physical robots.txt.
- `nadlan_config_disable_texturize()`: removes wptexturize from the_content/the_title/excerpt/etc. Root-fix for the en-dash AI-tell (wptexturize converted ' - ' to '–' at render). Prevents future regressions site-wide.
- Deploy: server `git pull` (plugin-build/ is gitignored; tracked copy is plugins/nadlan-config/). Bumped header + healthcheck version to 1.3.0 - verify via /wp-json/nadlan/v1/healthcheck.
