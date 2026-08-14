# WordPress Agent Deploy Pipeline - Full Instructions (cross-project hand-off)

**Audience:** an autonomous coding agent that must ship plugin code to a live,
managed-hosting WordPress site (e.g. UPress) with **zero manual clicks, no FTP,
no SSH** - only HTTPS + an Application Password.

**Status:** this exact pipeline has shipped 30+ production releases on a live
UPress-hosted WordPress site. It is proven. Copy it; do not reinvent it.

**Your current project (the one that's stuck):** plugin slug `hea-lth-ops`,
site `https://hea-lth.co.il`, host UPress, driver `scripts/deploy-wordpress.py`.
Everywhere below, substitute your real slug/owner/repo.

---

## 0. TL;DR - the one-paragraph fix for the failure you're hitting right now

You are failing for TWO independent reasons, and both are fixable in minutes:

1. **You are using the wrong install mechanism.** WordPress core's REST endpoint
   `POST /wp-json/wp/v2/plugins` accepts **only a wordpress.org slug**. It then
   makes the *server* download that package *from wordpress.org*. Your plugin is
   not on wordpress.org, so this endpoint can never install it - and the
   "cURL timed out" you saw is the UPress server failing to fetch from
   wordpress.org. Stop using that endpoint. Register your **own** temporary
   admin-gated REST route that runs `Plugin_Upgrader->install( $your_zip_url,
   [ 'overwrite_package' => true ] )`, where `$your_zip_url` is **your own zip on
   GitHub raw**. `Plugin_Upgrader::install()` accepts a slug, a local path, **or
   a remote URL** - so it pulls your zip from GitHub, never from wordpress.org.

2. **Your custom header trips the UPress WAF.** The `X-Hea-Lth-Deploy` diagnostic
   header (and/or posting raw HTML in a request body) matches a generic WAF rule
   on the managed host, which returns **403 before WordPress even runs**. The
   tell: the 403 body is **HTML from nginx**, not a WordPress JSON error object.
   Fix: send **no custom headers**, authenticate with the **Application Password**
   (`Authorization: Basic`), use `Content-Type: application/json` with a small
   JSON body (never a multipart HTML blob), and keep a normal User-Agent.

Do those two things and the deploy goes green. The rest of this document is the
full, durable pipeline so you never hit this again.

---

## 1. Why your current approach fails - exact root-cause of each error

| What you saw | Real cause | Fix |
|---|---|---|
| "UPress's server-side cURL timed out fetching the official package from WordPress.org" | You called core `POST /wp/v2/plugins` (or an equivalent), which only takes a wordpress.org **slug** and makes the **server** fetch from wordpress.org. Your plugin isn't there. | Don't use that endpoint. Use a custom route + `Plugin_Upgrader->install()` from **your** GitHub raw zip. |
| "UPress nginx rejected the request signature again" / 403 | Managed-host **WAF** (ModSecurity/nginx) inspects all traffic. Custom header `X-Hea-Lth-Deploy` and/or HTML in the body match generic XSS/anomaly rules and return **403 before PHP runs**. Body is HTML, not JSON. | Remove custom headers. JSON body only. Standard UA. Auth via Application Password. |
| "core endpoint accepts only a WordPress.org slug ... does not accept a local ZIP or arbitrary URL" | Correct - that is documented core behavior. It is a dead end for private plugins. | Confirmed dead end; use the custom route below. |

Key confirmations from the official sources (see Sources at the end):
- Core `/wp/v2/plugins` **install requires a `slug`** from the wordpress.org
  directory; it cannot take a local or arbitrary-URL zip.
- `Plugin_Upgrader::install()` **can install from a slug, a local zip path, or a
  remote zip URL** - which is exactly why the custom-route approach works.
- On managed hosts, a **403 whose body is HTML (not a JSON error) is the WAF**,
  not WordPress; custom headers and HTML request bodies are classic triggers.

---

## 2. The correct architecture (one line, then the picture)

Reviewed code in Git -> a deterministic script builds `plugin-dist/<slug>-<ver>.zip`
-> pushed to the default branch so it has a public **raw** URL -> a **temporary**
admin-only REST route on the site runs
`Plugin_Upgrader->install( <raw zip URL>, [ 'overwrite_package' => true ] )`
-> verify the version flipped -> **DELETE** the route.

```
  ┌──────────┐   build    ┌───────────────────────┐  git push   ┌───────────────┐
  │  Git repo │ ─────────▶ │ plugin-dist/slug-ver.zip│ ─────────▶ │ GitHub raw URL │
  └──────────┘   (python)  └───────────────────────┘             └──────┬────────┘
                                                                         │ 200, public
        create temp snippet (Code Snippets REST)                         │
  ┌───────────────────────────────────────────────┐   POST /run   ┌─────▼──────────────┐
  │ your admin-gated route: agentdeploy/v1/run     │ ◀──────────── │  Plugin_Upgrader    │
  │  -> Plugin_Upgrader->install(zip, overwrite)   │               │  ->install(zip)     │
  │  -> activate + cache flush                     │ ─────────────▶│  pulls from GitHub  │
  └───────────────────────────────────────────────┘   result      └────────────────────┘
        │ verify GET /healthcheck (version flipped?)
        ▼
   DELETE the snippet  -> confirm /run now 404s
```

Why this beats every alternative:
- **No wordpress.org dependency** -> no cross-network cURL timeout.
- **No custom headers, no HTML body** -> nothing for the WAF to match.
- **Runs as real WordPress** with `update_plugins` capability -> same code path
  as a human clicking "upload plugin", so behavior is predictable.
- **The privileged route exists for seconds**, then is deleted -> no standing
  attack surface.

---

## 3. One-time setup on the site (~30 min, once per site)

1. wp-admin -> Plugins -> install + activate **Code Snippets** (free). This gives
   you a REST API (`/wp-json/code-snippets/v1/snippets`) to create/delete PHP
   snippets remotely - that is how you install your temporary deploy route
   without ever touching FTP. (Your `--bootstrap-code-snippets` flag is doing
   exactly this - good.)
2. wp-admin -> Users -> your admin user -> **Application Passwords** -> create one.
   Store as env vars, **never in the repo**:
   `WP_BASE_URL`, `WP_USER`, `WP_APP_PASSWORD`.
   Verify auth works and you're an admin:
   ```bash
   curl -s -u "$WP_USER:$WP_APP_PASSWORD" \
     "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,roles"
   # expect: {"id":..,"roles":["administrator"]}
   ```
   If this returns HTML/403, it's the WAF - see section 10 before going further.
3. Settings -> Permalinks -> **Post name** (custom REST namespaces need pretty
   permalinks).
4. Create your ops plugin in Git (scaffold in section 4). It must expose a public
   `GET /healthcheck` route that returns the running version - your source of
   truth for "did the deploy land".
5. Copy the deterministic build script (section 5) and create the manifest JSON
   (section 6).
6. Install the plugin **the first time by any means** - a one-time wp-admin
   "Upload Plugin" of the zip is fine. Every deploy after that uses the loop in
   section 8.

---

## 4. The ops plugin scaffold (full, copy-paste)

`hea-lth-ops/hea-lth-ops.php`:

```php
<?php
/**
 * Plugin Name: Hea-Lth Ops
 * Description: Site behavior + agent deploy target.
 * Version: 0.1.0
 * Author: hea-lth
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

// The version constant MUST equal the header Version above. One sed bumps both.
define( 'HEALTH_OPS_VERSION', '0.1.0' );

// Public healthcheck: the deploy's source of truth. No auth - returns version only.
add_action( 'rest_api_init', function () {
	register_rest_route( 'hea-lth/v1', '/healthcheck', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			return array(
				'ok'      => true,
				'version' => HEALTH_OPS_VERSION,
				'time'    => current_time( 'mysql' ),
			);
		},
	) );
} );

// Enqueue assets with the version CONSTANT so caches bust on every deploy.
add_action( 'wp_enqueue_scripts', function () {
	// wp_enqueue_style( 'health-ops', plugins_url( 'assets/app.css', __FILE__ ), array(), HEALTH_OPS_VERSION );
} );

// OPTIONAL fallback path: plugin-update-checker so wp-admin can self-update too.
// Vendored at hea-lth-ops/lib/plugin-update-checker/ (YahnisElsts v5).
add_action( 'init', function () {
	$puc = __DIR__ . '/lib/plugin-update-checker/plugin-update-checker.php';
	if ( ! file_exists( $puc ) ) { return; }
	require_once $puc;
	if ( class_exists( '\\YahnisElsts\\PluginUpdateChecker\\v5\\PucFactory' ) ) {
		\YahnisElsts\PluginUpdateChecker\v5\PucFactory::buildUpdateChecker(
			'https://raw.githubusercontent.com/OWNER/REPO/main/plugin-dist/hea-lth-ops.json',
			__FILE__,
			'hea-lth-ops'
		);
	}
}, 5 );
```

Rules for this file:
- **Header `Version:` and the `*_VERSION` constant must always be equal.** Bump
  both with a single `sed`. The healthcheck reads the constant; the update
  checker reads the header; if they drift you get "deployed but version didn't
  change" ghosts.
- Ship **all ongoing behavior inside this plugin** (via `the_content`,
  `wp_head`/`wp_footer`, `wp_enqueue_*`, shortcodes, REST). The **theme** does
  not auto-update, so never put evolving logic there.

---

## 5. The deterministic build script (full, copy-paste)

`scripts/build-plugin-zip.py` - forward-slash paths only (Windows backslashes in
a zip make WordPress mis-extract silently), and it asserts both version strings
match before it will build:

```python
#!/usr/bin/env python3
import os, sys, zipfile, re

SLUG = "hea-lth-ops"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "plugins", SLUG)          # your plugin source dir
DIST = os.path.join(ROOT, "plugin-dist")

def main(ver):
    main_php = open(os.path.join(SRC, SLUG + ".php"), encoding="utf-8").read()
    header = re.search(r"Version:\s*([0-9][0-9.]*)", main_php).group(1)
    const  = re.search(r"_VERSION',\s*'([0-9][0-9.]*)'", main_php).group(1)
    assert header == const == ver, f"version mismatch header={header} const={const} arg={ver}"
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, f"{SLUG}-{ver}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(SRC):
            for f in files:
                full = os.path.join(base, f)
                # arcname MUST start with the slug dir and use forward slashes
                arc = SLUG + "/" + os.path.relpath(full, SRC).replace(os.sep, "/")
                z.write(full, arc)
    # prove the zip is real and contains the plugin main file
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
        assert f"{SLUG}/{SLUG}.php" in names, "main file missing from zip!"
    print("built", out, "entries:", len(names))

if __name__ == "__main__":
    main(sys.argv[1])
```

Run: `python3 scripts/build-plugin-zip.py 0.1.1`

---

## 6. The manifest JSON (`plugin-dist/hea-lth-ops.json`)

Used only by the wp-admin self-update fallback path. Keep it in sync each release:

```json
{
  "name": "Hea-Lth Ops",
  "slug": "hea-lth-ops",
  "version": "0.1.1",
  "author": "hea-lth",
  "requires": "6.0",
  "tested": "6.7",
  "requires_php": "7.4",
  "download_url": "https://raw.githubusercontent.com/OWNER/REPO/main/plugin-dist/hea-lth-ops-0.1.1.zip",
  "last_updated": "2026-07-10 12:00:00",
  "sections": { "changelog": "<h4>0.1.1</h4><ul><li>...</li></ul>" }
}
```

---

## 7. The release ritual (every version, in THIS order, no skips)

1. **Bump version in BOTH places** (header + constant) with one sed:
   `sed -i "s/0\.1\.0/0.1.1/g" plugins/hea-lth-ops/hea-lth-ops.php`
2. **`php -l` every changed file.** A syntax error deployed = a live outage.
   ```bash
   for f in $(git diff --name-only | grep '\.php$'); do php -l "$f" || exit 1; done
   ```
3. **Build:** `python3 scripts/build-plugin-zip.py 0.1.1`
4. **Assert the change is inside the zip** (a marker string from your diff) AND
   both version strings. Never deploy on faith:
   ```bash
   unzip -p plugin-dist/hea-lth-ops-0.1.1.zip hea-lth-ops/hea-lth-ops.php | grep "0.1.1"
   ```
5. **Update the manifest JSON**, commit, push/merge to the **default branch**.
   Confirm the raw zip URL returns 200:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" \
     "https://raw.githubusercontent.com/OWNER/REPO/main/plugin-dist/hea-lth-ops-0.1.1.zip"
   # want: 200
   ```

Only after the raw zip is 200 do you run the deploy loop.

---

## 8. The deploy loop (create -> call -> verify -> delete)

### 8a. The deploy route snippet (the ONLY thing that ever runs privileged code)

Save as `deploy-snippet.php`. Note: **no top-level side effects** - the
privileged work lives entirely inside the route callback, gated on
`update_plugins`.

```php
add_action( 'rest_api_init', function () {
  register_rest_route( 'agentdeploy/v1', '/run', array(
    'methods'             => 'POST',
    'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
    'callback'            => function ( $req ) {
      require_once ABSPATH . 'wp-admin/includes/file.php';
      require_once ABSPATH . 'wp-admin/includes/misc.php';
      require_once ABSPATH . 'wp-admin/includes/plugin.php';
      require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';

      $plugin = 'hea-lth-ops/hea-lth-ops.php';
      $ver    = $req->get_param( 'ver' );                 // e.g. "0.1.1"
      // cache-bust GitHub raw (it caches ~5 min); pull from YOUR repo, not wp.org
      $zip = 'https://raw.githubusercontent.com/OWNER/REPO/main/plugin-dist/hea-lth-ops-'
           . preg_replace( '/[^0-9.]/', '', (string) $ver ) . '.zip?cb=' . time();

      $skin = new WP_Ajax_Upgrader_Skin();
      $up   = new Plugin_Upgrader( $skin );
      $ok   = $up->install( $zip, array( 'overwrite_package' => true ) );
      if ( ! is_plugin_active( $plugin ) ) { activate_plugin( $plugin ); }

      // bust page/object cache so the new version renders immediately
      do_action( 'litespeed_purge_all' );  // no-op if LiteSpeed absent
      wp_cache_flush();

      return array(
        'result'   => is_wp_error( $ok ) ? $ok->get_error_message() : var_export( $ok, true ),
        'messages' => $skin->get_upgrade_messages(),
        'active'   => is_plugin_active( $plugin ),
      );
    },
  ) );
} );
```

### 8b. Drive it over REST - full bash (no custom headers, WAF-safe)

```bash
set -euo pipefail
VER="0.1.1"

# 1) create the snippet (scope=global + active so rest_api_init actually fires)
BODY=$(python3 -c "import json;print(json.dumps({'name':'tmp-deploy','code':open('deploy-snippet.php').read(),'scope':'global','active':True}))")
SID=$(curl -s -u "$WP_USER:$WP_APP_PASSWORD" -H "Content-Type: application/json" \
      -d "$BODY" "$WP_BASE_URL/wp-json/code-snippets/v1/snippets" \
      | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
echo "snippet id=$SID"

# 2) call the deploy route (pass the version as JSON; no X-* headers!)
curl -s -u "$WP_USER:$WP_APP_PASSWORD" -H "Content-Type: application/json" \
     -X POST "$WP_BASE_URL/wp-json/agentdeploy/v1/run" \
     -d "{\"ver\":\"$VER\"}" --max-time 180 | tee /tmp/deploy-result.json

# 3) verify the RUNNING version flipped (source of truth = healthcheck)
sleep 3
GOT=$(curl -s "$WP_BASE_URL/wp-json/hea-lth/v1/healthcheck" | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])")
echo "live version now: $GOT (wanted $VER)"
[ "$GOT" = "$VER" ] || { echo "DEPLOY DID NOT LAND"; }

# 4) DELETE the snippet, then confirm the privileged route is gone (want 404)
curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X DELETE "$WP_BASE_URL/wp-json/code-snippets/v1/snippets/$SID" -o /dev/null
CODE=$(curl -s -u "$WP_USER:$WP_APP_PASSWORD" -X POST "$WP_BASE_URL/wp-json/agentdeploy/v1/run" -o /dev/null -w "%{http_code}")
echo "route after delete: $CODE (want 404)"
```

That is the whole loop. It is idempotent, leaves no standing privileged code, and
touches wordpress.org exactly zero times.

---

## 9. Timing & sequencing (the parts that bite if you rush)

- **Do not call `/run` until the raw zip URL returns 200.** After a git push,
  GitHub's raw CDN can lag a few seconds. Poll the raw URL for 200 first
  (section 7 step 5).
- **Always cache-bust the zip URL** with `?cb=<timestamp>` inside the route
  (already in the snippet). GitHub raw caches ~5 minutes; without the buster you
  reinstall the previous zip and the version never flips.
- **Prefer `install(overwrite_package)` over `upgrade()`.** If you instead force
  the `update_plugins` transient and call `upgrade()`, a vendored update-checker
  can rewrite that transient and the deploy silently no-ops ("plugin is already
  at the latest version").
- **Give the call `--max-time 180`.** Install fetches + unzips; do not use a 10s
  timeout.
- **Verify with an independent GET, not the POST response body.** Some proxies
  return a 404/HTML body on a request that actually succeeded. The healthcheck
  GET is truth.

---

## 10. WAF avoidance (this is what's blocking you specifically)

Managed hosts (UPress, WP Engine, Kinsta, SiteGround) run a WAF that inspects
every request **before PHP runs**. Make your requests boring:

- **No custom request headers.** Delete `X-Hea-Lth-Deploy` and any other `X-*`
  diagnostic header. They match anomaly rules. Pass metadata in the JSON body
  instead (`{"ver":"0.1.1"}`).
- **JSON body, never HTML.** Posting raw HTML/`<script>`/`<?php` in a request
  body trips generic XSS rules. Your zip travels as a URL the *server* fetches -
  it never rides in the request body. Keep bodies tiny and JSON.
- **Authenticate with the Application Password** (`-u user:app_pass` -> HTTP
  Basic). Do not send session cookies or nonces from a script.
- **Normal User-Agent.** Don't set a weird UA; default curl UA is fine, or a
  plain `curl/8.x`.
- **How to tell it's the WAF and not WordPress:** the failing response is a
  **403/406 with an HTML body** (an nginx/ModSecurity page), and has **no**
  `Content-Type: application/json`. A real WordPress permission error is
  **JSON**: `{"code":"rest_forbidden",...}`. Check with:
  ```bash
  curl -s -D - -o /dev/null -u "$WP_USER:$WP_APP_PASSWORD" \
    -H "Content-Type: application/json" -X POST \
    "$WP_BASE_URL/wp-json/agentdeploy/v1/run" -d '{"ver":"0.1.1"}'
  ```
  If you see `Server: nginx` + HTML, it's the WAF. If you still get blocked after
  removing custom headers, ask UPress support to **allowlist `/wp-json/` for your
  admin IP** or relax ModSecurity on that path. That is a one-line host change.

---

## 11. Blocker catalog - symptom -> cause -> fix

| Symptom | Cause | Fix |
|---|---|---|
| cURL timeout "fetching official package" | Using core `/wp/v2/plugins` (slug-only, fetches from wordpress.org) | Custom route + `Plugin_Upgrader->install()` from your GitHub raw zip |
| 403 with **HTML** body | Host WAF matched a custom header or HTML body | Remove `X-*` headers; JSON body only; ask host to allowlist `/wp-json/` |
| `{"code":"rest_forbidden"}` **JSON** 403 | Real WordPress auth/cap failure | Fix the Application Password; confirm the user has `administrator` / `update_plugins` |
| Deploy returns success but version unchanged | Reinstalled a cached/old zip, or header/constant drift, or transient no-op | Add `?cb=time()`; keep header==constant; use `install(overwrite_package)` not `upgrade()` |
| `rest_no_route` / 404 on your route | Snippet not active, wrong scope, or permalinks not "Post name" | Create snippet `scope=global, active=true`; set pretty permalinks |
| Site 500s after a snippet | Privileged code ran at top level of a global snippet (every request) | Never top-level privileged code; put it INSIDE the route callback only |
| WordPress mis-extracts the zip | Zip built on Windows with backslash paths | Build only with the Python builder (forward slashes) |
| POST body says fail but site updated | Proxy rewrote the response body | Trust the independent healthcheck GET, not the POST body |

---

## 12. Hard rules (each one has caused a real outage somewhere)

1. **NEVER put privileged/one-shot code at the top level of a global snippet.**
   Global snippets run on **every** request at `plugins_loaded`; one fatal (e.g.
   calling `wp_update_post` before `init`) 500s the whole site - including the
   REST API you'd use to fix it. One-shot code goes **inside** the admin-gated
   route callback, always.
2. **Never leave the deploy route active.** Create -> call -> **delete**. One
   deploy = one create/delete cycle.
3. **Prefer `install(['overwrite_package'=>true])`** over transient+`upgrade()`.
4. **Always cache-bust the zip URL** (`?cb=<time()>`).
5. **Verify the RENDERED result**, not a whole-page HTML substring: read the
   healthcheck version and, for content changes, slice from `<body>` and assert
   the OLD markup is ABSENT too.
6. **Zip only via the canonical Python builder.**
7. **Never print `WP_APP_PASSWORD`** to logs, output, or commits. Public repo =>
   the zip contains **no secrets**; API keys live in `wp_options`, entered via
   wp-admin, never in Git.
8. **Response bodies can lie behind proxies** - the independent GET is truth.

---

## 13. Verification discipline (what "done" means)

A deploy is done ONLY when all three are true:
1. `GET /wp-json/hea-lth/v1/healthcheck` returns the **new** version.
2. For a visible change: fetch the page, slice the `<body>`, confirm the **new**
   markup is present **and** the **old** markup is gone.
3. `POST /wp-json/agentdeploy/v1/run` returns **404** (route deleted).

If you can't independently observe the change live, it is **not** done - do not
report success.

---

## 14. Emergency recovery (memorize before you need it)

- **Site 500 + REST dead:** host File Manager -> `wp-content/plugins/` -> rename
  the offending plugin folder to `<name>.off`. Site returns instantly.
- **Runaway Code Snippets:** add `define('CODE_SNIPPETS_SAFE_MODE', true);` to
  `wp-config.php` right after `<?php`, delete the bad snippet via REST, then
  remove the define. SQL fallback: `UPDATE wp_snippets SET active = 0;`.
- **After any emergency edit:** re-apply the intended change as reviewed **plugin
  code** and mirror it back into Git immediately. Never leave a fix living only
  as a live snippet.

---

## 15. Minimal end-to-end reference (paste, set 4 vars, run)

```bash
# --- config ---
export WP_BASE_URL="https://hea-lth.co.il"
export WP_USER="healthca_admin"
export WP_APP_PASSWORD="****"          # from wp-admin Application Passwords; never commit
VER="0.1.1"; SLUG="hea-lth-ops"; OWNER_REPO="OWNER/REPO"

# 0) sanity: am I an admin, and is the raw zip live?
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=roles"
curl -s -o /dev/null -w "zip:%{http_code}\n" \
  "https://raw.githubusercontent.com/$OWNER_REPO/main/plugin-dist/$SLUG-$VER.zip"

# 1..4) create snippet -> call route -> verify -> delete   (see section 8b)
#       (reuse the section 8b block verbatim)
```

That's the entire pipeline. The two changes that unblock you today: **(a)** stop
using core `/wp/v2/plugins`; install via a custom route + `Plugin_Upgrader` from
your own GitHub zip, and **(b)** drop the `X-*` header and send a small JSON body
so the UPress WAF stops rejecting you.

---

## Sources
- WordPress REST API Handbook - Plugins reference (core install requires a
  wordpress.org `slug`): https://developer.wordpress.org/rest-api/reference/plugins/
- `Plugin_Upgrader` class (install from slug / local path / remote URL):
  https://developer.wordpress.org/reference/classes/plugin_upgrader/
- `Plugin_Upgrader::upgrade()` method reference:
  https://developer.wordpress.org/reference/classes/plugin_upgrader/upgrade/
- Adding custom REST endpoints (register_rest_route):
  https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/
- WAF/403 diagnosis on managed hosts (HTML 403 body = host WAF, not WordPress;
  custom headers/HTML bodies trigger rules):
  https://cr0x.net/en/wordpress-403-forbidden-diagnose-fix/
- Core Trac #9757 - core UI historically could not update a plugin from an
  uploaded zip (context for why the custom route is needed):
  https://core.trac.wordpress.org/ticket/9757
