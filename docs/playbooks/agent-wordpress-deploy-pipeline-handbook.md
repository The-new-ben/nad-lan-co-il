# The Agent-Driven WordPress Deploy Pipeline - Complete Portable Handbook

**What this is.** A battle-tested method for letting an AI agent (Claude Code, or
any REST-capable automation) deploy plugin code to a live WordPress site with
**zero manual "Update" clicks and no FTP/SSH**, on hosts where you only have
wp-admin + an application password. Built and proven on nad-lan.co.il across
30+ releases. This handbook is host-agnostic: it works on UPress, WP Engine,
SiteGround, Kinsta, Cloudways, or any standard WordPress.

**Who it is for.** A developer or agent setting up the same loop on a *different*
WordPress site. Copy this file into that repo and follow it top to bottom.

**The one-sentence idea.** Your reviewed plugin code lives in Git; a build script
zips it; you push the zip to a public URL (GitHub raw); then a **temporary**
admin-only REST route on the site runs WordPress's own `Plugin_Upgrader` against
that zip and deletes itself. The repo stays the source of truth; only the deploy
*trigger* moves from a human to the agent.

---

## PART 0 - The mental model (read this first)

Clicking "Update" in wp-admin is nothing but WordPress running `Plugin_Upgrader`
in an authenticated admin request. Any actor with the `update_plugins` capability
can run the exact same class. So the pipeline is:

```
[Git repo]  --build-->  [plugin-<ver>.zip]  --push-->  [GitHub raw URL]
     |                                                        |
     |                                                        v
     |                                        [temp REST route on the site]
     |                                          runs Plugin_Upgrader->install()
     |                                                        |
     v                                                        v
[source of truth]                              [live site now runs new code]
```

Four properties make it safe and repeatable:

1. **Ephemeral privilege.** The privileged deploy route exists only for the
   seconds of one deploy: create it, call it, delete it. Never leave it live.
2. **Idempotent install.** `install($url, ['overwrite_package'=>true])` is the
   "Upload Plugin -> Replace current with uploaded" path. It ignores version
   comparison, so re-running is harmless and downgrades/rollbacks work the same.
3. **Verify before trusting.** WordPress puts the site in maintenance mode for
   ~2-5s during the swap and rolls back on failure; you still verify a health
   endpoint + the changed page after every deploy.
4. **Cache-bust everything.** GitHub raw caches ~5 min; browsers cache assets by
   `?ver=`; hosts add page caches. Each layer has an explicit buster.

---

## PART 1 - Prerequisites & the stack

### 1.1 What the target site needs

| Requirement | Why | How to get it |
|---|---|---|
| WordPress 6.x+ | REST API + application passwords are core | Already there |
| An **administrator** user | `update_plugins`, `install_plugins` caps | Existing owner account, or a dedicated deploy admin |
| **Application Password** for that user | Bearer auth for REST without the login cookie | wp-admin -> Users -> Profile -> Application Passwords -> "Add New" |
| **Code Snippets** plugin (free) | Runs arbitrary PHP on the site incl. a REST route, without file access | wp-admin -> Plugins -> Add New -> search "Code Snippets" -> Install -> Activate |
| Your plugin's code in Git | Source of truth; produces the zip | This repo |
| A public URL that serves the zip | The upgrader downloads from here | GitHub raw (default), or any HTTPS URL |
| `pretty permalinks` ON | Custom REST namespaces need non-plain permalinks | Settings -> Permalinks -> "Post name" |

### 1.2 Optional but recommended plugins

| Plugin | Role | Notes |
|---|---|---|
| **WP Mail SMTP** | Reliable transactional mail | Recovery-mode emails + your app's mail |
| **File Manager Advanced** | Emergency file access from wp-admin | Your rescue hatch if a deploy breaks admin |
| **WP Adminer** or Adminer | Raw SQL from wp-admin | Emergency option-flip / cleanup |
| A caching plugin (LiteSpeed, WP Rocket…) | Perf | You will purge it in the deploy route |

### 1.3 The credentials (store these OUTSIDE the repo)

For an agent, put these in environment variables, never in a committed file:

```
WP_BASE_URL="https://example.com"
WP_USER="deploy_admin"
WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"   # the app password, spaces ok
```

In Claude Code on the web: repository -> Environment settings -> Environment
variables. Locally: a `.env` that is `.gitignore`d. **Never print the password to
logs or chat.** Verify auth without leaking it:

```bash
curl -s -u "$WP_USER:$WP_APP_PASSWORD" \
  "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,name,roles"
# expect your user with "administrator" in roles
```

---

## PART 2 - Prepare the plugin repo

### 2.1 Layout

```
your-plugin/
  your-plugin.php            # main file with the header + a version constant
  inc/                       # modules, each guarded by function_exists / ABSPATH
  assets/
plugin-dist/                 # build output: the zips + a manifest json
scripts/
  build-plugin-zip.py        # the canonical builder (below)
```

### 2.2 Single source of version truth

In your main plugin file, define the version in EXACTLY these places and keep
them in lockstep (the build script asserts it):

```php
<?php
/**
 * Plugin Name: Your Plugin
 * Version: 1.0.0
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

/* Cache-busting constant - MUST equal the header Version. Enqueue every asset
   with this, never a hardcoded string (a frozen ?ver= once pinned browsers to
   a month-old script for weeks). */
if ( ! defined( 'YOURPLUGIN_VERSION' ) ) {
    define( 'YOURPLUGIN_VERSION', '1.0.0' );
}

// example enqueue:
// wp_enqueue_script( 'yourplugin-app', $url . 'assets/app.js', array(), YOURPLUGIN_VERSION, true );
```

Add a **healthcheck REST route** so you can verify the live version in one call.
This is the single most useful thing you can build for the pipeline:

```php
add_action( 'rest_api_init', function () {
    register_rest_route( 'yourplugin/v1', '/healthcheck', array(
        'methods'             => 'GET',
        'permission_callback' => '__return_true', // read-only, safe to be public
        'callback'            => function () {
            return array(
                'plugin'      => 'your-plugin',
                'version'     => YOURPLUGIN_VERSION,
                'php_version' => PHP_VERSION,
                'wp_version'  => get_bloginfo( 'version' ),
            );
        },
    ) );
} );
```

### 2.3 The canonical zip builder (`scripts/build-plugin-zip.py`)

This exists because ad-hoc `zip` commands on Windows poison archives with
backslash paths that WordPress silently mis-extracts. Use ONE deterministic
builder on every project:

```python
#!/usr/bin/env python3
"""Build a WordPress-installable plugin zip, deterministically.
Usage: python3 scripts/build-plugin-zip.py 1.0.0
Produces plugin-dist/your-plugin-<ver>.zip with a single top-level folder
'your-plugin/' and FORWARD-SLASH paths only. Asserts the version is in sync."""
import os, sys, zipfile, re

PLUGIN_DIR  = "your-plugin"          # the folder that becomes the plugin
MAIN_FILE   = "your-plugin/your-plugin.php"
OUT_DIR     = "plugin-dist"
EXCLUDE     = {".git", ".DS_Store", "node_modules", "__pycache__"}

def main():
    ver = sys.argv[1]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    # 1. assert version is in sync in the main file (header + constant)
    src = open(MAIN_FILE, encoding="utf-8").read()
    assert re.search(r"Version:\s*" + re.escape(ver), src), "header version mismatch"
    assert ("'" + ver + "'") in src, "constant version mismatch"
    # 2. build
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"{PLUGIN_DIR}-{ver}.zip")
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dns, fns in os.walk(PLUGIN_DIR):
            dns[:] = [d for d in dns if d not in EXCLUDE]
            for fn in fns:
                if fn in EXCLUDE:
                    continue
                p = os.path.join(dp, fn)
                arc = p.replace(os.sep, "/")            # force forward slashes
                z.write(p, arc)
                n += 1
    # 3. self-verify
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        assert all("\\" not in x for x in names), "backslash in archive!"
        assert any(x == MAIN_FILE for x in names), "main file missing!"
    print(f"OK {os.path.basename(out)} entries={n} backslash=0 rooted=True")

if __name__ == "__main__":
    main()
```

### 2.4 The update manifest (`plugin-dist/your-plugin.json`)

Optional but lets wp-admin show "update available" too. Keep it updated by the
release script:

```json
{
  "name": "Your Plugin",
  "slug": "your-plugin",
  "version": "1.0.0",
  "download_url": "https://raw.githubusercontent.com/OWNER/REPO/main/plugin-dist/your-plugin-1.0.0.zip",
  "requires": "6.5",
  "tested": "6.8",
  "requires_php": "7.4",
  "sections": { "changelog": "<h4>1.0.0</h4><ul><li>Initial.</li></ul>" }
}
```

---

## PART 3 - The release ritual (every version, in order)

```bash
# 1. bump version in the two places (header + constant). One sed does both:
sed -i "s/ \* Version: 1\.0\.0/ * Version: 1.0.1/; \
        s/'YOURPLUGIN_VERSION', '1\.0\.0'/'YOURPLUGIN_VERSION', '1.0.1'/" \
        your-plugin/your-plugin.php

# 2. LINT every changed PHP file BEFORE building. This gate has saved production
#    from a fatal more than once (an apostrophe in a single-quoted string).
php -l your-plugin/your-plugin.php
for f in your-plugin/inc/*.php; do php -l "$f" | grep -v "No syntax errors" || true; done

# 3. build the zip
python3 scripts/build-plugin-zip.py 1.0.1

# 4. VERIFY THE FEATURE IS INSIDE THE ZIP (never deploy blind). Assert the actual
#    code you changed is present in the archive, plus the version:
python3 - <<'PY'
import zipfile
z = zipfile.ZipFile("plugin-dist/your-plugin-1.0.1.zip")
main = z.read("your-plugin/your-plugin.php").decode()
assert "Version: 1.0.1" in main and "'1.0.1'" in main
# assert your changed marker, e.g.:
# assert "my_new_function" in z.read("your-plugin/inc/feature.php").decode()
print("ZIP VERIFIED")
PY

# 5. update the manifest json (version + download_url), then commit + push to the
#    default branch so the raw URL serves the new zip:
git add -A && git commit -m "release 1.0.1" && git push
```

Merge to the branch your raw URL points at (usually `main`). Now the zip is live
at its GitHub raw URL. Confirm:

```bash
curl -sI "https://raw.githubusercontent.com/OWNER/REPO/main/plugin-dist/your-plugin-1.0.1.zip" | head -1
# expect HTTP 200 (may lag ~5 min behind the push - the cache-buster below handles it)
```

---

## PART 4 - The deploy route (the heart of the pipeline)

### 4.1 The snippet code

This is the PHP you put in a **temporary** Code Snippets snippet. It registers an
admin-only REST route that runs the upgrader. Replace the two ALL-CAPS values:

```php
add_action( 'rest_api_init', function () {
    register_rest_route( 'yourdeploy/v1', '/run', array(
        'methods'  => 'POST',
        // ONLY someone who could click "Update" in wp-admin can call this:
        'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
        'callback' => function () {
            require_once ABSPATH . 'wp-admin/includes/file.php';
            require_once ABSPATH . 'wp-admin/includes/misc.php';
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
            require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';

            $plugin_file = 'your-plugin/your-plugin.php';   // folder/mainfile
            // cache-buster (?nlcb=) dodges GitHub raw's ~5-min CDN cache:
            $zip = 'https://raw.githubusercontent.com/OWNER/REPO/main/plugin-dist/your-plugin-VERSION.zip?nlcb=' . time();

            $skin = new WP_Ajax_Upgrader_Skin();
            $upgrader = new Plugin_Upgrader( $skin );
            // install() with overwrite_package = the "Upload -> Replace" path.
            // This is BETTER than the transient + upgrade() dance (see gotcha #1).
            $ok = $upgrader->install( $zip, array( 'overwrite_package' => true ) );

            if ( ! is_plugin_active( $plugin_file ) ) {
                activate_plugin( $plugin_file );
            }

            // OPTIONAL: purge caches in the same request so changes are instant.
            if ( function_exists( 'do_action' ) ) { do_action( 'litespeed_purge_all' ); }
            if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }

            return array(
                'result'   => is_wp_error( $ok ) ? ( 'ERR:' . $ok->get_error_message() ) : var_export( $ok, true ),
                'messages' => $skin->get_upgrade_messages(),
                'active'   => is_plugin_active( $plugin_file ),
            );
        },
    ) );
} );
```

### 4.2 Create -> call -> delete, over REST (no browser needed)

Code Snippets exposes a REST API at `wp-json/code-snippets/v1`. The full deploy
in bash:

```bash
# --- A. create the snippet (scope 'global' + active so its rest_api_init fires) ---
CODE=$(cat deploy-snippet.php)      # the PHP from 4.1, as a file
PAYLOAD=$(python3 -c "import json,sys; print(json.dumps({'name':'tmp-deploy','code':open('deploy-snippet.php').read(),'scope':'global','active':True}))")
SID=$(curl -s -u "$WP_USER:$WP_APP_PASSWORD" -H "Content-Type: application/json" \
  -d "$PAYLOAD" "$WP_BASE_URL/wp-json/code-snippets/v1/snippets" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo "snippet id: $SID"

# --- B. call the deploy route (basic auth as the app-password admin) ---
curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X POST "$WP_BASE_URL/wp-json/yourdeploy/v1/run" --max-time 180
# success => messages array ends with "Plugin updated successfully."

# --- C. verify the live version flipped ---
curl -s "$WP_BASE_URL/wp-json/yourplugin/v1/healthcheck" \
  | python3 -c "import sys,json; print('live:', json.load(sys.stdin).get('version'))"

# --- D. DELETE the snippet (never leave the privileged route live) ---
curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X DELETE "$WP_BASE_URL/wp-json/code-snippets/v1/snippets/$SID" \
  -o /dev/null -w "deleted: %{http_code}\n"     # expect 204

# --- E. confirm the route is gone ---
curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X POST "$WP_BASE_URL/wp-json/yourdeploy/v1/run" \
  -o /dev/null -w "route after delete: %{http_code} (want 404)\n"
```

That is the entire loop. Deploy = create, call, verify, delete. Every time.

---

## PART 5 - Verification: never trust the response body alone

Some proxies/CDNs return an nginx 404 body even when the write succeeded. Truth
is always the *effect*, checked independently:

```bash
# health endpoint says the new version:
curl -s "$WP_BASE_URL/wp-json/yourplugin/v1/healthcheck" | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])"
# the changed page returns 200:
curl -s -o /dev/null -w "%{http_code}\n" "$WP_BASE_URL/the-changed-page/?cb=$(date +%s)"
# homepage still 200 (nothing broke):
curl -s -o /dev/null -w "%{http_code}\n" "$WP_BASE_URL/"
```

**Golden rule learned the hard way: verify the RENDERED PAGE BODY, not whole-HTML
substrings.** Enqueued CSS/JS in `<head>` contain your class names, so a "marker
present" grep can pass while the visible page is unchanged (a theme filter was
overriding our content for a full day before we caught it). Slice from `<body>`
and also assert the OLD markup is ABSENT:

```bash
curl -s "$WP_BASE_URL/" | python3 -c "
import sys; f=sys.stdin.read(); b=f[f.find('<body'):]
print('new present:', 'my-new-marker' in b)
print('old absent :', 'old-marker' not in b)"
```

---

## PART 6 - Gotchas (each one cost real debugging here)

1. **Prefer `install(overwrite_package)` over the transient+`upgrade()` dance.**
   If your plugin bundles a plugin-update-checker library, its
   `pre_set_site_transient_update_plugins` filter can rewrite the forced update
   transient before the upgrader reads it, giving "plugin is at the latest
   version" and deploying nothing. `install` skips version comparison entirely.
2. **GitHub raw caches ~5 minutes.** Always append `?nlcb=<time()>` to the zip
   URL inside the route. Without it you deploy the previous zip.
3. **Windows-zipped archives poison paths.** Always use the Python builder in
   Part 2.3; assert no backslashes in `namelist()`.
4. **A `single-use` snippet activated via REST may not execute its code.** Use
   `scope:"global"` + `active:true` and an explicit REST route you call yourself,
   so you get the upgrader messages back and aren't deploying blind.
5. **NEVER put one-shot privileged code at the TOP LEVEL of a global snippet.**
   Global snippets run on EVERY request at `plugins_loaded`; a fatal there (e.g.
   calling `wp_update_post()` before `init`) takes the whole site down, including
   the REST API you'd use to remove it. One-shot code goes INSIDE an
   admin-gated REST route callback, always. (This is how we once 500'd
   production - see Part 7.)
6. **Lint before build, always.** `php -l` every changed file. A syntax error
   deployed is an outage.
7. **Assert the feature is inside the zip before deploying**, not just the
   version. A patch script that dies mid-run can bump the version but skip the
   feature.
8. **Pretty permalinks must be on** or custom REST namespaces 404.

---

## PART 7 - Emergency recovery (write this down BEFORE you need it)

If a deploy or a bad snippet takes the site to HTTP 500 and the REST API is down:

**Plan A - rename the plugin folder (foolproof).** In the host's File Manager,
go to `wp-content/plugins/` and rename the offending plugin folder (e.g.
`code-snippets` -> `code-snippets.off`). WordPress skips it and the site returns
instantly. Nothing is deleted.

**Plan B - safe-mode a runaway Code Snippets.** Add to `wp-config.php` right
after `<?php`:
```php
define( 'CODE_SNIPPETS_SAFE_MODE', true );   // loads the plugin but runs no snippets
```
Then delete the bad snippet via REST and remove the line.

**Plan C - flip it off in the database.** In Adminer/phpMyAdmin:
```sql
UPDATE wp_snippets SET active = 0;         -- adjust table prefix
```

**Plan D - WordPress recovery email.** Core emails a recovery-mode link to the
admin address on a fatal; open it, deactivate the plugin, done.

After recovery: remove the offending snippet via REST, re-verify every page,
then re-apply the intended change the SAFE way (as reviewed plugin code, not a
live snippet).

---

## PART 8 - Making it scale

### 8.1 One site, many releases
The loop above is already the steady state: 30+ releases shipped this way with
zero manual clicks. Keep a scratch `deploy-snippet-<ver>.php` per release so the
create step is a one-line `sed` from the last one.

### 8.2 Many sites (fleet)
Parameterize the three env vars per site and loop:

```bash
for site in siteA siteB siteC; do
  export WP_BASE_URL WP_USER WP_APP_PASSWORD   # from a per-site secrets store
  ./deploy.sh "$PLUGIN_ZIP_URL" "$PLUGIN_FILE" "$VERSION"
done
```
Keep a `sites.json` (base URL + which plugin/version each runs) OUT of the repo.
The deploy route code is identical per site; only the zip URL/plugin-file differ.

### 8.3 A permanent (vs temporary) deploy route
For a fleet you may want a stable route instead of create/delete each time. If
so, harden it: require a **shared secret header** compared with `hash_equals()`
in addition to `current_user_can`, rate-limit it, and log every call. Ship it as
part of a tiny dedicated "ops" plugin, not a snippet. The temporary-route method
in Part 4 is strictly safer for a single site; only go permanent when the
create/delete overhead actually hurts.

### 8.4 CI/CD instead of an agent
The same route works from GitHub Actions: on push to `main`, build the zip,
commit it (or attach to a release), then `curl` the deploy route with the app
password stored as an Actions secret. The agent and CI are interchangeable
callers of the same route.

### 8.5 The real upgrade: WP Pusher / Git-based deploy
If the host allows installing WP Pusher (or the host has native Git deploy, as
some panels do), that replaces this pipeline with `git push -> auto-install`,
including for **themes** (which have no `Plugin_Upgrader` path). This handbook's
method is for hosts where you only have wp-admin + REST; graduate to Git-deploy
when the host supports it.

---

## PART 9 - Security boundaries (do not skip)

1. **There is usually no staging.** Every deploy lands on production. Re-verify
   health after every mutating call; if it fails, deactivate the change first
   (`POST wp-json/wp/v2/plugins/<plugin> {"status":"inactive"}`), do not stack a
   second change hoping to fix the first.
2. **The app password is full-admin.** Treat raw-DB and raw-file tools as
   deliberate-session tools, not always-on automation. Rotate the app password
   to a dedicated least-privilege deploy admin when possible, and revoke it the
   moment a session that used it ends.
3. **Git is the source of truth.** The route is for the deploy gap, not for
   making changes that should have been commits. If you ever hotfix live via a
   snippet, mirror it back into the repo immediately - "if it's not committed, it
   doesn't exist."
4. **Never leave the deploy route active** and never commit secrets. The route
   is created, used, and deleted within one deploy.
5. **Public repo?** The zip URL is public, so the zip must contain no secrets -
   keys live in wp-admin options / wp-config, never in shipped code.

---

## PART 10 - Copy-paste quickstart (TL;DR)

```
1. Install Code Snippets on the target site; create an app password for an admin.
2. Put your plugin in Git with a version constant + a /healthcheck route + the
   Python zip builder (Parts 2.2-2.3).
3. Set WP_BASE_URL / WP_USER / WP_APP_PASSWORD as env vars (never in the repo).
4. Release: bump version (2 places) -> php -l -> build zip -> assert feature in
   zip -> update manifest -> git push to main (Part 3).
5. Deploy: create the temp snippet with the route (Part 4.1) -> POST the route ->
   verify healthcheck version + rendered body (Parts 4.2, 5) -> DELETE the
   snippet -> confirm 404 (Part 4.2 D/E).
6. If anything 500s: rename the plugin folder in File Manager (Part 7 Plan A).
```

That is the whole pipeline. Everything else in this handbook is the reasoning and
the scars behind those ten lines.

---
_Authored from the working pipeline on nad-lan.co.il (skills/agent-direct-wordpress-access.md
is the site-specific short reference; this file is the portable, host-agnostic version)._
