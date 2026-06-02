# Codex Plugin Access & Deploy — the complete operator guide

> **Who this is for:** Codex (and any coding agent: Claude, Antigravity, Cowork-code)
> that needs to change the `nadlan-config` WordPress plugin and get the change LIVE on
> nad-lan.co.il. This is the single source of truth for the deploy pipeline. If another
> doc disagrees, this one wins for *deploy mechanics*; `nadlan-config-plugin.md` wins for
> *coding conventions*; `plugin-auto-update.md` is the historical "why".
>
> **The golden rule:** agents have **NO** WordPress admin, FTP, SSH, or cPanel access.
> The ONLY way code reaches the live site is **git → manifest on `main` → owner clicks
> "Update" in WP-admin**. Plan everything around that one channel.

---

## 0. TL;DR (the whole loop in 9 steps)

```
1. git fetch origin main && git checkout -b <branch> origin/main   # ALWAYS branch off main
2. edit plugins/nadlan-config/inc/<module>.php                      # your change
3. bump version in TWO places in plugins/nadlan-config/nadlan-config.php
4. php -l on every changed file  (MUST be clean)
5. rebuild plugin-dist/nadlan-config-<ver>.zip
6. update plugin-dist/nadlan-config.json (version + download_url + changelog + date)
7. git add -A && git commit && git push -u origin <branch>
8. open PR → squash-merge into main
9. tell the owner: WP-admin → Plugins → NadLan Config → Update to <ver>
```

If you only remember one thing: **a code change that is not (a) on `main`, (b) inside a
bumped `nadlan-config-<ver>.zip`, and (c) advertised by `nadlan-config.json` on `main`
WILL NOT reach the live site.** Editing the `.php` alone does nothing.

---

## 1. Coordinates — every location & link

| Thing | Exact location |
|---|---|
| **Repo** (public) | `https://github.com/The-new-ben/nad-lan-co-il` |
| **Default branch** | `main` |
| **Plugin source** | `plugins/nadlan-config/` |
| **Main plugin file** | `plugins/nadlan-config/nadlan-config.php` |
| **Modules** | `plugins/nadlan-config/inc/<name>.php` |
| **Update-checker lib** | `plugins/nadlan-config/lib/plugin-update-checker/` (vendored — never delete) |
| **Built ZIPs** | `plugin-dist/nadlan-config-<ver>.zip` |
| **Update manifest** | `plugin-dist/nadlan-config.json` |
| **Manifest URL the live site reads** | `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config.json` |
| **Healthcheck (live version probe)** | `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck` |
| **Live site** | `https://nad-lan.co.il` |
| **Sitemap** | `https://nad-lan.co.il/sitemap_index.xml` |
| **Coding conventions** | `skills/nadlan-config-plugin.md` |
| **This deploy guide** | `skills/codex-plugin-access-and-deploy.md` |

---

## 2. How the plugin is wired (so you change the right thing)

### 2.1 Module loader
`nadlan-config.php` ~line 25 has a single `foreach` array that `require_once`-loads every
module from `inc/`:

```php
foreach ( array( 'catalog-meta', 'claim', 'import', ... ,
    'directory', 'reviews', 'lead-ledger', 'ai-concierge', 'archive-grid',
    'calculators', 'catalog-shine' ) as $nadlan_mod ) {
    $f = __DIR__ . '/inc/' . $nadlan_mod . '.php';
    if ( file_exists( $f ) ) { require_once $f; }
}
```

**A new module is NOT loaded until its filename is added to this array.** Creating
`inc/foo.php` alone does nothing.

**Load order matters** when two modules hook the same action at the same priority, OR when
one calls a function defined by another at file-load time (rare — we guard everything).
The safer lever is the **hook priority**, not array order (e.g. `directory.php` intercepts
`/professionals/` on `template_redirect` priority **5**, `archive-grid.php` on **6**, so
directory wins).

### 2.2 Every module MUST follow this skeleton
```php
<?php
/** nadlan-config — <what it does> (vX.Y.Z) */
if ( ! defined( 'ABSPATH' ) ) { exit; }              // 1. hard exit if loaded directly

if ( ! function_exists( 'nadlan_foo_bar' ) ) {        // 2. guard EVERY function
    function nadlan_foo_bar() { ... }
}
add_action( 'init', 'nadlan_foo_bar' );               // 3. wire hooks at file scope
```
- **PHP floor is 7.4** (`Requires PHP: 7.4`). No `match()`, no named args, no enums,
  no constructor promotion, no first-class callable syntax. Arrow functions `fn()` are OK.
- Prefix everything `nadlan_` to avoid collisions.
- Escape output (`esc_html`, `esc_url`, `esc_attr`), sanitize input (`sanitize_*`,
  `wp_unslash`), nonce/cap-check writes. The repo is **public** and the site is live.

### 2.3 Version lives in TWO places — bump BOTH
In `nadlan-config.php`:
```php
 * Version: 1.34.0          // line ~5  (the header WP reads)
...
'version' => '1.34.0',      // line ~73 (healthcheck response)
```
If the header version is not **higher** than the installed version, WP will NOT offer the
update. The healthcheck string is what you verify against after deploy.

---

## 3. The deploy pipeline — full commands

### 3.1 ALWAYS branch off `origin/main`  ⚠️ #1 blocker
We squash-merge PRs. After a squash merge, your old working branch **diverges** from main
and the next PR throws `405 merge conflict`. So every change starts fresh:

```bash
cd /path/to/nad-lan-co-il
git fetch origin main
git checkout -b claude/<short-topic> origin/main
```
If you already committed on a now-stale branch, **recreate**:
```bash
git fetch origin main
git checkout -b <newbranch> origin/main
git checkout <stalebranch> -- plugins/nadlan-config/ plugin-dist/   # bring just the files
```

### 3.2 Make the code change
Edit `inc/<module>.php`. If it's a NEW module, also add its name to the `foreach` array
in `nadlan-config.php` (§2.1).

### 3.3 Bump the version (both places)
```bash
OLD=1.34.0; NEW=1.35.0
sed -i "s/ \* Version: $OLD/ * Version: $NEW/"                  plugins/nadlan-config/nadlan-config.php
sed -i "s/'version'             => '$OLD'/'version'             => '$NEW'/" plugins/nadlan-config/nadlan-config.php
grep -n "Version:\|'version'" plugins/nadlan-config/nadlan-config.php | head   # verify both changed
```
(The spacing before `=>` in the healthcheck line is real — match it or the sed misses.)

### 3.4 Lint EVERYTHING (blocker if any file fails)
```bash
fail=0
for f in $(find plugins/nadlan-config -name "*.php"); do
  php -l "$f" >/dev/null 2>&1 || { echo "FAIL $f"; php -l "$f"; fail=1; }
done
[ $fail -eq 0 ] && echo "ALL CLEAN"
```
Never ship unless `ALL CLEAN`.

### 3.5 Build the distribution ZIP  ⚠️ #2 blocker — internal folder structure
The ZIP **must** contain a top-level `nadlan-config/` folder (WP unzips it into
`wp-content/plugins/nadlan-config/`). Build it by zipping the folder *from its parent*:
```bash
NEW=1.35.0
cd plugins && rm -f /tmp/nadlan-config-$NEW.zip && \
  zip -rq /tmp/nadlan-config-$NEW.zip nadlan-config -x "*.DS_Store" && cd ..
cp /tmp/nadlan-config-$NEW.zip plugin-dist/nadlan-config-$NEW.zip
# sanity: first entries must start with "nadlan-config/"
unzip -l plugin-dist/nadlan-config-$NEW.zip | head
```
Do NOT `zip` from inside `plugins/nadlan-config/` (that produces a rootless zip WP rejects).
The vendored `lib/plugin-update-checker/` is inside the folder, so it ships automatically.

### 3.6 Update the manifest `nadlan-config.json`  ⚠️ #3 blocker — must point at `main`
The live site only reads this file **on `main`**. It must advertise the new version AND a
`download_url` that resolves (the ZIP you just committed, on `main`):
```bash
NEW=1.35.0
python3 - <<PY
import json
p='plugin-dist/nadlan-config.json'
d=json.load(open(p,encoding='utf-8'))
d['version']='$NEW'
d['download_url']='https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config-$NEW.zip'
d['last_updated']='$(date -u +%Y-%m-%d\ %H:%M:%S)'
d['sections']['changelog']='<h4>$NEW</h4><ul><li>WHAT CHANGED — write it here.</li></ul>'+d['sections'].get('changelog','')
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('manifest now',d['version'])
PY
```
Fields that MUST be right: `version` (== header), `download_url` (exact ZIP filename on
`main`), `slug`/`name` (leave as-is). The `sections.changelog` is what the owner sees in
the WP update modal — prepend, don't overwrite history.

### 3.7 Commit, push, PR, merge
```bash
git add -A
git commit -m "vX.Y.Z <summary>

<body — what + why>

https://claude.ai/code/session_..."      # end with the session link if you have one
git push -u origin <branch>
```
Open a PR into `main` and **squash-merge** it. With `gh`:
```bash
gh pr create --base main --head <branch> --title "nadlan-config vX.Y.Z — ..." --body "..."
gh pr merge --squash --auto <num>     # or merge in the GitHub UI / via MCP tool
```
(Claude-side uses the GitHub MCP `create_pull_request` + `merge_pull_request` tools; Codex
can use `gh` or the API. Either is fine — the artifact on `main` is what matters.)

### 3.8 Verify it landed on `main` (don't trust the raw CDN immediately)
`raw.githubusercontent.com` caches ~5 min, so check git directly:
```bash
git fetch origin main
git show origin/main:plugin-dist/nadlan-config.json | python3 -c "import sys,json;print('manifest',json.load(sys.stdin)['version'])"
git ls-tree origin/main plugin-dist/ | grep "$NEW"   # ZIP present?
```

### 3.9 Hand off to the owner (the only human step)
The live site does NOT auto-deploy instantly. Tell the owner:
> **WP-admin → Plugins → NadLan Config → "Update now" to vX.Y.Z.**
> If it's not showing: **Dashboard → Updates → "Check again"** forces the check (WP caches
> update lookups ~12h), then Update.

After they update, confirm live:
```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=$RANDOM" \
  | python3 -c "import sys,json;print('LIVE version:',json.load(sys.stdin)['version'])"
```

---

## 4. Obstacle → solution table (pre-solved blockers)

| Symptom | Cause | Fix |
|---|---|---|
| PR gives `405 merge conflict` | Branch diverged after a prior squash-merge | Recreate branch off `origin/main` (§3.1) |
| Owner updated but sees no change | Manifest still on old version, or ZIP missing on `main` | Verify §3.8; ensure both `version` bumped + ZIP committed |
| WP shows no "Update available" | Header version not higher, or manifest cached | Confirm header bumped; owner → Dashboard → Updates → Check again |
| WP update fails "could not unzip" | ZIP has no top-level `nadlan-config/` folder | Rebuild zipping from `plugins/` parent (§3.5) |
| `download_url` 404 on update | URL filename ≠ committed ZIP, or not on `main` yet | Match filename exactly; merge to `main` first |
| Fatal error after update / white screen | A module fatal'd (syntax or calling undefined fn) | You skipped `php -l`. Every module is `function_exists`-guarded + `ABSPATH`-guarded; restore + re-lint. Owner can deactivate via WP-admin or rename the folder via host file manager to recover |
| New module not running | Not added to the `foreach` array | Add filename to array in `nadlan-config.php` (§2.1) |
| Raw manifest shows old version | GitHub CDN cache (~5 min) | Check `git show origin/main:...` instead (§3.8) |
| Two features fight on same archive | Both hook same action/priority | Set explicit hook priorities (lower = earlier) |
| Recurring billing "doesn't charge monthly" | Green Invoice gateway is one-charge | Sell annual products, or owner sets Morning standing order — see `payments-woo-greeninvoice.md` |
| Need to roll back | Bad version shipped | Bump a NEW higher version that reverts the change + reship (forward-only; WP won't "downgrade" via the checker). For emergencies the owner deactivates the plugin in WP-admin. |
| Agent can't click "Update" | Agents have no WP-admin | This is by design — always hand the final click to the owner (§3.9) |

---

## 5. What agents CAN and CANNOT touch

**CAN (via git):** any file under `plugins/nadlan-config/`, the dist ZIP + manifest,
skills, theme files in the repo.

**CAN (via REST, if holding the app password — data only, not code):**
`GET /wp-json/nadlan/v1/healthcheck`, the standard `wp/v2/*` content endpoints, and the
plugin's own public REST routes (`/nadlan/v1/directory`, `/projects`, `/review-submit`,
`/referral/*`, `/concierge`, `/lead`). These read/write **content**, never plugin code.

**CANNOT:** WP-admin UI, plugin activation/update click, FTP/SSH/cPanel, the server
`robots.txt`, DB direct access. Anything here is an **owner action** — list it explicitly
when you hand off.

---

## 6. Multi-agent etiquette (Codex + Claude + Cowork on the same plugin)

- **One version number per merge.** If two agents bump to the same version in parallel,
  the second PR conflicts. Coordinate: check the current `main` version first
  (`git show origin/main:plugin-dist/nadlan-config.json`), bump to the next integer.
- **Never edit the same module in two open branches.** Pick non-overlapping modules.
- **Always branch off the latest `origin/main`** so you include the other agent's merged work.
- **Write what you shipped to `BACKLOG.md`** (root) and the shipped-log there, so the next
  agent sees it.
- **Conventions live in `skills/nadlan-config-plugin.md`; deploy mechanics (this file).**

---

## 7. Quick reference card (paste-ready)

```bash
# ── nadlan-config ship loop ──────────────────────────────
REPO=/path/to/nad-lan-co-il; cd $REPO
OLD=$(git show origin/main:plugin-dist/nadlan-config.json | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])")
NEW=<set-next-version>
git fetch origin main && git checkout -b ship/$NEW origin/main
# ... edit inc/<module>.php (+ add to foreach if new) ...
sed -i "s/ \* Version: $OLD/ * Version: $NEW/" plugins/nadlan-config/nadlan-config.php
sed -i "s/'version'             => '$OLD'/'version'             => '$NEW'/" plugins/nadlan-config/nadlan-config.php
for f in $(find plugins/nadlan-config -name "*.php"); do php -l "$f">/dev/null||echo "FAIL $f"; done
cd plugins && zip -rq /tmp/n.zip nadlan-config -x "*.DS_Store" && cd ..
cp /tmp/n.zip plugin-dist/nadlan-config-$NEW.zip
# update plugin-dist/nadlan-config.json (version, download_url, changelog) — see §3.6
git add -A && git commit -m "v$NEW ..." && git push -u origin ship/$NEW
# open PR → squash-merge → tell owner to click Update → curl healthcheck
```

---

## Revision log
- 2026-06-02 — Created (Claude). Pipeline as of plugin v1.34.0: WooCommerce + Green
  Invoice payments, directory/reviews/lead-ledger/ai-concierge modules live. Auto-update
  via vendored plugin-update-checker reading the manifest on `main`.
