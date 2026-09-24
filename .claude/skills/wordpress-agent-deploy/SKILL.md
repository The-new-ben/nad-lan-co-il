---
name: wordpress-agent-deploy
description: MANDATORY for any work on a WordPress site. The agent-driven deploy pipeline - ship plugin code to a live WordPress with zero manual clicks and no FTP/SSH, via a temporary admin-gated REST route running Plugin_Upgrader. Covers setup on a NEW site, the release ritual, the deploy loop, self-update wiring (plugin-update-checker), cache discipline, verification, and emergency recovery. Use whenever installing, updating, deploying, or hotfixing anything on a WordPress site.
---

# WordPress Agent Deploy Pipeline (the law for WordPress work)

Proven across 30+ production releases on nad-lan.co.il. Deep reference with
full reasoning: `docs/playbooks/agent-wordpress-deploy-pipeline-handbook.md`.
This skill is the operational contract every agent MUST follow.

## The architecture in one line
Reviewed code lives in Git -> a deterministic script builds `plugin-dist/<slug>-<ver>.zip`
-> pushed to the repo's default branch (public raw URL) -> a TEMPORARY admin-only
REST route on the site runs `Plugin_Upgrader->install($zip, ['overwrite_package'=>true])`
-> verify -> DELETE the route. The site also carries plugin-update-checker
pointed at a manifest JSON, so wp-admin/auto-update works as a fallback path.

## Reference implementation facts (clone these on a new site)
- Update library: **plugin-update-checker v5 (v5p6) by YahnisElsts**, vendored at
  `<plugin>/lib/plugin-update-checker/`, booted on `init` prio 5 with
  `PucFactory::buildUpdateChecker( MANIFEST_URL, __FILE__, '<slug>' )`.
- Manifest: `https://raw.githubusercontent.com/<OWNER>/<REPO>/main/plugin-dist/<slug>.json`
  with fields: `name, slug, version, author, homepage, requires, tested,
  requires_php, download_url, last_updated, sections{changelog}`.
- Primary update trigger: the agent's temp REST route (seconds after merge).
  PUC/wp-admin is the human-fallback path; WP's `auto_update_plugins` cron path
  works too (lands within <=12h) but keep it OFF for deliberate deploys.
- Cache handling after install, inside the same route: `do_action('litespeed_purge_all')`
  (no-op when absent) + `wp_cache_flush()`; plus every asset enqueued with a
  version CONSTANT that equals the plugin header version (never hardcode `?ver=`).
- Theme-level changes: the theme does NOT auto-update. ALL ongoing behavior
  ships inside the plugin via hooks (`the_content`, `wp_head`/`wp_footer`,
  `wp_add_inline_style/script`, shortcodes, REST). The theme stays static chrome.

## One-time setup on a NEW site (30 minutes)
1. wp-admin -> Plugins -> install + activate **Code Snippets** (free).
2. wp-admin -> Users -> your admin -> **Application Passwords** -> create one.
   Store as env vars (never in the repo): `WP_BASE_URL`, `WP_USER`, `WP_APP_PASSWORD`.
   Verify: `curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,roles"`.
3. Settings -> Permalinks -> "Post name" (custom REST namespaces need it).
4. Create the ops plugin in Git: main file with header `Version:` + a
   `<SLUG>_VERSION` constant (kept equal), a public GET `/healthcheck` REST route
   returning the version, and the vendored plugin-update-checker boot (facts above).
5. Copy `scripts/build-plugin-zip.py` from the handbook (deterministic zip,
   forward slashes only, asserts version sync). Create `plugin-dist/<slug>.json`.
6. Install the plugin the FIRST time by any means (wp-admin upload of the zip is
   fine). Every install after that uses the loop below.

## The release ritual (every version, in this order, no skips)
1. Bump the version in BOTH places (header + constant) with one sed.
2. `php -l` EVERY changed file. A syntax error deployed is an outage.
3. `python3 scripts/build-plugin-zip.py <ver>`.
4. Open the zip and ASSERT the changed code is inside it (marker string), plus
   both version strings. Never deploy on faith.
5. Update the manifest json (`version`, `download_url`, changelog). Commit,
   push/merge to the default branch. Confirm the raw zip URL returns 200.

## The deploy loop (create -> call -> verify -> delete)
Snippet PHP (the only thing that ever runs privileged code):
```php
add_action( 'rest_api_init', function () {
  register_rest_route( 'agentdeploy/v1', '/run', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
    'callback' => function () {
      require_once ABSPATH . 'wp-admin/includes/file.php';
      require_once ABSPATH . 'wp-admin/includes/misc.php';
      require_once ABSPATH . 'wp-admin/includes/plugin.php';
      require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
      $plugin = 'SLUG/SLUG.php';
      $zip = 'https://raw.githubusercontent.com/OWNER/REPO/main/plugin-dist/SLUG-VERSION.zip?nlcb=' . time();
      $skin = new WP_Ajax_Upgrader_Skin();
      $up = new Plugin_Upgrader( $skin );
      $ok = $up->install( $zip, array( 'overwrite_package' => true ) );
      if ( ! is_plugin_active( $plugin ) ) { activate_plugin( $plugin ); }
      do_action( 'litespeed_purge_all' ); wp_cache_flush();
      return array( 'result' => is_wp_error( $ok ) ? $ok->get_error_message() : var_export( $ok, true ),
                     'messages' => $skin->get_upgrade_messages(), 'active' => is_plugin_active( $plugin ) );
    },
  ) );
} );
```
Drive it over REST (Code Snippets API):
```bash
# create (scope global + active so rest_api_init fires)
SID=$(curl -s -u "$WP_USER:$WP_APP_PASSWORD" -H "Content-Type: application/json" \
  -d "$(python3 -c "import json;print(json.dumps({'name':'tmp-deploy','code':open('deploy-snippet.php').read(),'scope':'global','active':True}))")" \
  "$WP_BASE_URL/wp-json/code-snippets/v1/snippets" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
# call
curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X POST "$WP_BASE_URL/wp-json/agentdeploy/v1/run" --max-time 180
# verify version flipped
curl -s "$WP_BASE_URL/wp-json/SLUG/v1/healthcheck"
# DELETE the snippet, then confirm the route 404s
curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X DELETE "$WP_BASE_URL/wp-json/code-snippets/v1/snippets/$SID"
curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X POST "$WP_BASE_URL/wp-json/agentdeploy/v1/run" -o /dev/null -w "%{http_code}\n"  # want 404
```

## Hard rules (violations have caused real outages)
0. **THE LINT GATE IS A CHAIN, NOT A LINE (outage 2026-07-12).** `php -l` printed
   a parse error and the deploy STILL ran, because lint / build / deploy were
   separate lines in one Bash call - the failure did not stop the sequence, and
   the site went down hard (every WP entry point 500s; with outbound mail dead
   the WP recovery email never arrives - there is NO self-service recovery).
   The ONLY acceptable shape is one `&&` chain from lint to the deploy call:
   `php -l a.php && php -l b.php && build && assert-zip && upload && deploy`.
   Additionally: extract the changed file(s) FROM the built zip and `php -l`
   them again before upload - the zip is what ships, not the working tree.
   Root cause that day: an apostrophe in a CSS comment that lived inside a
   single-quoted PHP string. Watch every apostrophe near PHP strings.
1. **NEVER top-level privileged code in a global snippet.** Global snippets run
   on EVERY request at plugins_loaded; one fatal (e.g. `wp_update_post` before
   `init`) 500s the whole site including the REST API you'd fix it with.
   One-shot code goes INSIDE an admin-gated route callback, always.
2. **Never leave the deploy route active.** Create, call, delete - one deploy.
3. **Prefer `install(overwrite_package)`** over forcing the `update_plugins`
   transient + `upgrade()`: vendored PUC rewrites that transient and the deploy
   silently no-ops ("plugin is at the latest version").
4. **Always `?nlcb=<time()>` on the zip URL** - GitHub raw caches ~5 minutes.
5. **Verify the RENDERED BODY, not whole-HTML substrings.** Head assets contain
   your class names; slice from `<body>` and also assert the OLD markup is ABSENT.
6. **Zip only via the canonical Python builder** - ad-hoc Windows zips poison
   paths with backslashes and WordPress mis-extracts silently.
7. **Never print `WP_APP_PASSWORD`** to output/logs/commits. Public repo = the
   zip must contain no secrets; keys live in wp-options, entered via wp-admin.
8. Response bodies lie behind some proxies (404 body on a successful write) -
   truth is the independent GET verification, always. On nad-lan (uPress nginx)
   the "404 after a successful write" is WordPress's 403 masked by nginx: the
   post row was already inserted, then a protected meta key was refused. Retrying
   makes duplicates. Fix at the source: refuse in `rest_pre_insert_{type}` (before
   the insert) with a non-403 code (HAD-249, 24.9.2026).
9. **A rollback never deletes a file that live code may require (outage
   24.9.2026, about 2 minutes of HTTP 500 on every URL, HAD-247).** After you
   restore the old source of a caller, OPcache can keep serving the NEW compiled
   caller; if the rollback deletes the new file it `require_once`s, every request
   fatals, and the purge call that would reset OPcache dies on the same fatal.
   Order: restore -> `opcache_invalidate()` each restored file -> `opcache_reset()`
   -> check a page; leave the unused new file on disk. Load optional companions
   with `@include_once`, never `require_once` behind `file_exists()` (with
   opcache.enable_file_override the guard answers from the cache).
10. **Two sessions, one live plugin**: patch shared files (nadlan-config.php) on
    the LIVE text by anchors with a compare-and-swap on the live md5, swap other
    files only when live == git HEAD, announce every deploy to the other session,
    and never ship a whole-plugin zip from a shared working tree (it carries the
    other session's unfinished files). Runners: `scripts/owned-rule/deployowned.py`,
    `scripts/had-247/deploy232.py`.
11. **Post-deploy checks match printed markup, never bare class names.** Class
    names also sit inside the page's inline CSS/JS, so "must not contain
    nlps-cover" hit the gallery's own script and fired the rollback in rule 9.
    Match `<figure class="nlps-cover"` exactly as printed.
12. **A `the_content` filter that prints SVG or structured HTML runs after
    wpautop (priority 11 or later).** Below 10, wpautop writes `</p>` inside
    `<svg>` and `<br />` between inline buttons: the drawing dies silently (the
    listing facade showed an empty box with "87654321" from the day it was built).
13. **On Windows, patch PHP as bytes.** Python text mode writes CRLF; git stores
    LF, so a live-vs-git md5 compare fails on identical content. Write with
    `open(p, 'wb')` and compare with line endings normalised.
14. **One bridge route per run** (a random namespace): a bridge snippet left
    active by a failed run keeps answering the old route with the old token.

## Emergency recovery (memorize before you need it)
- Site 500 and REST dead: host File Manager -> `wp-content/plugins/` -> rename the
  offending plugin folder to `<name>.off` -> site returns instantly.
- Runaway Code Snippets specifically: add `define('CODE_SNIPPETS_SAFE_MODE', true);`
  to wp-config.php right after `<?php`, rename the folder back, delete bad
  snippets via REST, remove the define. Or SQL: `UPDATE wp_snippets SET active=0;`.
- After recovery: re-apply the intended change as reviewed plugin code, never as
  another live snippet. Mirror any emergency edit back into Git immediately.
