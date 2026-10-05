# HAD-256 · release package (snapshot 3, code `2ce0a741`)

For main, the only publisher. Owner (Ben) approved the release on 5.10.2026. **Maya's independent QA has not run on
snapshot 3**, the MySQL proof below has not run yet, and the theme bench found items that need a decision first
(`THEME.md`, "Before the release"). Nothing here was run against nad-lan.co.il except anonymous public GETs of
`/post-listing/`, a broker page, a listing and their stylesheets (reference copies in `theme/live-ref/`).

## What changes on the live site

Two Code Snippets. No plugin file, no theme file, no page, no option, no database schema.

| Live snippet | Change | Base (live now) SHA-256 of the snippet body | After |
|---|---|---|---|
| `x-owner-wizard` (id **707**) | replaced WHOLE by `owner-wizard.php` 2.0.0 | `f04dbbf8d99d6eaf89d2b8a272f5d8e529f91b6fe97030ca9b22930083a5f9d4` (1.0.0 = `6e9cf930`; equals the live read of 3.10, `docs/qa/live-read/20261003T205055Z/snippet-707.php`) | `14acb521b9cf5d76e8b6daa555eb6d8c69eaab2b4ed7314707c0c3ccedd040b4` |
| `x-broker-drop` (id: find by name) | exactly the 8 HAD-256 hunks | `e7736ef75fdf176ee759273af2c2a74f31a39215c7dd0a29cccc595bb68232b9` (1.1.3 = `6e9cf930`; **not read live by this line**: the runner must compare) | `fb081ee5e3a07bf2c5bd474bbe0abe36e69aa4bc81ce6bace00026ae1491d441` |

"Snippet body" = what Code Snippets stores: the file without the opening `<?php` and the whitespace after it
(deploydrop.py's `re.sub(r"^\s*<\?php\s*", "", php, count=1)`), UTF-8, LF. The repo files as committed (LF, with the tag):

| File | Version | SHA-256 |
|---|---|---|
| `plugins/nadlan-config/inc/owner-wizard.php` | 2.0.0 | `9fcafd9d0e6b134c360b383df4622b8919a54d3bf06713706e4d377cddf892bd` |
| `plugins/nadlan-config/inc/broker-drop.php` | 1.1.4 | `dff44c897230e0699496d2fa6fac000ce9e80bf4bfb6238e0ea18c878cf6cacd` |

`x-broker-join` (699), `x-skin-a` (638) and every other snippet stay as they are (the theme bench ran 699 and 638 beside
the new code: no clash, no PHP notice from them).

## The module: `scripts/project-stage/had256_release.py`

Generated from git by `scripts/had-256/make_release.py` (never edited by hand), in the style of `perf_427.py`:
`RELS = ["snippet:x-broker-drop", "snippet:x-owner-wizard"]`, `apply(rel, txt)` returns the new snippet body or raises
`SystemExit`:
- `snippet:x-broker-drop`: refuses a text that already has 1.1.4 (`NL_DROP_VERSION 1.1.4` or `nl_drop_lock_acquire`);
  warns when the live text is not the 1.1.3 base; applies `HUNKS` in file order, each old block found **exactly once**
  at its turn, else `SystemExit("... hunk N anchor is there K times")`.
- `snippet:x-owner-wizard`: refuses 2.0.0 already there; refuses any live text that is not the 1.0.0 base (drift);
  returns `owner_code()`, read from `git show 2ce0a741:plugins/nadlan-config/inc/owner-wizard.php` and checked
  against `OWNER_NEW_SHA256` (the commit is in the shared repository of this worktree; keep the branch
  `worktree-agent-a61b211e083144352` or merge it before the run).
- CRLF in, CRLF out (the hunks are matched on LF).
- `python scripts/project-stage/had256_release.py` proves it: base + package == snapshot 3 for both, a second apply stops.
  Output on 5.10: `x-broker-drop e7736ef75fdf -> fb081ee5e3a0 (8 hunks), snippet 707 f04dbbf8d99d -> 14acb521b9cf`.

The 8 hunks (`git diff 6e9cf930 2ce0a741 -- plugins/nadlan-config/inc/broker-drop.php`): version 1.1.3 -> 1.1.4 (@30);
the lock / fence / claim block and the `nl_drop_build` wrapper, the old body renamed `nl_drop_build_locked` (@2023,
+201); the listing claimed and written by `wp_update_post` instead of inserted, fences before content and meta (@2053);
the language twin claimed the same way (@2123); the fence before the page render and the result state read from the
post status (@2150); `nl_result` / `nl_state` committed through `nl_drop_fenced_meta` (@2165); the photo cleaner block
with `nl_drop_strip_gps` kept as a wrapper (@2189, +208); the busy answer 409 in `nl_drop_rest_build` (@2286).

## How main runs it (the deploy415 / deploydrop.py pattern; no runner was run by this line)

1. **Gates.** Release lock + in-flight guard as for every runner (`nadlan-release-concurrency`, `nadlan-runner-inflight-guard`);
   `GET /wp-json/nadlan/v1/health`; public-source audit before (`tools/source_audit.py` on `/post-listing/`,
   `/brokers/meital-katzir/`, `/properties/nofei-yam-3-rooms-balcony-for-rent/`).
2. **MySQL proof first** (open item 1), STAGED since the one-piece kit answered an nginx 404 on live (5.10):
   `claim-proof-stage1.php` (`/wp-json/nadlan-h256c/v1/s1`: `{"steps":["hello"]}` first, then all reads),
   `claim-proof-stage2.php` (`/s2`, single connection, `"groups"` to bisect), `claim-proof-stage3.php` (`/s3`, the
   second connection only), one temporary snippet at a time. Answers are one base64 field `b64` unless `"enc": 0`.
   **Stop unless stage 2 says `"all_pass": true` with every `cleanup.*` 0.** Stage 3 is wanted, not required (see
   the hypothesis in the 5.10 report: a host guard may refuse a raw second connection from snippet code).
3. **Bridge up** (the usual `x-tmp-…-ops-<ts>` snippet with a fresh token; ops `lint_code` and `purge` as in deploy415).
4. **Read live.** `GET /wp-json/code-snippets/v1/snippets` -> the row named `x-broker-drop` (its id); `GET /707`.
   Save both bodies to `docs/qa/had-256/live-backup/<name>.<stamp>.live` (the rollback source). Stop unless 707 is
   `f04dbbf8…` and active, and `x-broker-drop` is `e7736ef7…` and active (any other hash = drift: diff it first).
5. **Build + lint.** `new_bd = apply("snippet:x-broker-drop", live_bd)`, `new_ow = apply("snippet:x-owner-wizard", live_ow)`;
   assert `fb081ee5…` / `14acb521…`; `ops({"lint_code": new_bd})`, `ops({"lint_code": new_ow})` (PHP on the server).
6. **Private photo folder** (below): decide and, if used, define `NL_OWNER_PRIVATE_DIR` BEFORE step 7.
7. **Write, engine first.** `PUT /<bd id> {"name":"x-broker-drop","code":new_bd,"scope":"global","active":false}`,
   `PUT /<bd id>/activate`, `GET` back: SHA `fb081ee5…` and active. Then the same for `/707` (`x-owner-wizard`,
   `14acb521…`). Engine first: 1.1.4 keeps every 1.1.3 function name and signature the 1.0 wizard calls
   (`nl_drop_build( $drop, $b )`), while 2.0 refuses to run without 1.1.4 (`"engine": false`). The pair 1.0 + 1.1.4 was
   NOT drilled on the bench (L17 rolled both back together); it exists only between the two writes. Between `PUT` and
   `activate` a snippet is off for one request (deploydrop.py's known window).
8. **Purge**: `ops({"purge": 1})` (LiteSpeed all + object cache + OPcache).
9. **Checks** (anonymous, `?nlv=<ts>` cache-buster, then once without it), below. Then eyes: `/post-listing/` and
   `?lang=en` at 390x844 and 1440x900 in the owner's Chrome.
10. **Bridge down** (deactivate, delete, route 404), source audit after, receipt, Linear HAD-256 + Notion row.

## Check strings for the runner

`/post-listing/` (anonymous):
- need: `<section class="nlj alignfull" id="nlj-app" dir="rtl" lang="he" data-v="2.0.0">` · `<style id="nlj-css">` ·
  `<script id="nlj-js">` · `"engine":true` · `"v":"2.0.0"` · `<h1 class="wp-block-heading">פרסום נכס למכירה או להשכרה, בחינם</h1>`
  (and exactly one `<h1` in the body) · `id="nlhp-top"` · `class="nlpc-site-footer"` · `id="nlcta"` · `id="nla11y-btn"` ·
  `<meta name='robots' content='index, follow` (indexing is the owner's: unchanged)
- never: `id="nlow-gate"` · `nlowg-go` · `"engine":false` · `nadlan-pwiz` · `nlj-test` · `nlj_fault` · `NLJ_VARIANT` ·
  `had256probe` · `>nl-drop-` · `Fatal error` · `Warning:` · `noindex`

`/post-listing/?lang=en`: need `<section class="nlj alignfull" id="nlj-app" dir="ltr" lang="en" data-v="2.0.0">` ·
`List your property, owner to buyer` · `"lang":"en"` · `"engine":true`; never: the same list as above.

`/brokers/meital-katzir/` and `/en/brokers/meital-katzir/` (x-broker-drop renders them): need HTTP 200, exactly one
`<h1`, `class="nlb-lcard"` as many times as before the release (11 on 5.10 in both), `id="nlhp-top"`; never
`Fatal error`, `nl_drop_fenced`, `>nl-drop-`.

`/properties/nofei-yam-3-rooms-balcony-for-rent/` (an existing listing): need 200, one `<h1`,
`3 חדרים עם מרפסת של 20 מ״ר ו-2 חניות, נופי ים`, `class="nlx-plate"`, `wa.me/972523631582`; never `Fatal error`, `>nl-drop-`.

Doors: `GET /wp-json/nadlan/v1/healthcheck` -> `owner_wizard.version` `2.0.0`, `engine` true, `sealed` true;
`broker_drop.version` `1.1.4` · `POST /wp-json/nadlan/v1/listing-submit` (anonymous) -> 410 `nl_owner_moved` ·
`POST /wp-json/nadlan/v1/owner/draft` (anonymous) -> 401 · `GET /drop/000000000000000000000000/` -> 404.
(All of these answered so on the theme bench, 127.0.0.1:9405.)

## The private photo folder

Draft photos are cleaned, sealed (libsodium secretbox, key from the auth salt) and stored per owner under a keyed folder.
Default: `wp-content/uploads/nl-private/<hmac>/` with a deny-all `.htaccess` and empty `index.php` (the bytes are
ciphertext either way). Recommended: a folder **outside the web root**, if the host allows it:

```php
// wp-config.php, above "That's all, stop editing!" (uPress file manager, after a backup of wp-config.php)
define( 'NL_OWNER_PRIVATE_DIR', dirname( ABSPATH ) . '/nl-private' );
```

Before setting it, one bridge op should prove: `wp_mkdir_p()` works there, `is_writable()`, `realpath()` is not under
`ABSPATH`, and `open_basedir` allows it. If not, keep the default and prove instead that
`https://nad-lan.co.il/wp-content/uploads/nl-private/.htaccess` answers 403 (LiteSpeed honours `.htaccess`). Decide
before the first 2.0 upload: moving it later strands the drafts already stored (the path is not migrated). Rotating
the auth salt makes unpublished draft photos unreadable (published photos are ordinary media).

## Rollback

1. `PUT /707` with the saved 1.0.0 body, activate, read back `f04dbbf8…` (the page answers with the 1.0 gate again).
2. Then `PUT /<bd id>` with the saved 1.1.3 body, activate, read back `e7736ef7…`. (Owner first: 2.0 on 1.1.3 shows
   the "engine" message; the end state 1.0 + 1.1.3 is the L17 drill.)
3. `ops({"purge": 1})`; check `/post-listing/` has `id="nlow-gate"` and no `id="nlj-app"`; broker pages as above.
4. What stays (inert under 1.0, resumed by a re-release; the L17 drill on the bench): 2.0 drafts (`nadlan_drop`
   private, `nl_draft_v` 2), owner listings published by 2.0 (they render under 1.0), options `nl_pub_*`,
   `nl_att_*`, `nl_owner_ck_*`, sealed photos in the private folder. Nothing is deleted by a rollback.
5. A fatal right after a write: Code Snippets' safe mode (`?snippets-safe-mode=1` in wp-admin) or the uPress file
   manager; then step 1-3.

## Before the release: blockers and decisions (honest list)

1. **Maya's QA of snapshot 3 has not run.** Nothing here is acceptance.
2. **MySQL proof not run** (open item 1). The kit ran on the SQLite theme bench only (dry run: 44/44, clean-up 0,
   anonymous 401, wrong token 403: `mysql-claim-check.sqlite-dryrun.json`). No local MySQL / MariaDB / Docker / WSL
   exists on this machine, so the first MySQL run is main's, on the live database. Expect `same_value_update_rows` 0
   there (MySQL counts changed rows; the code handles it) and `meta_value_compare_ignores_case` true (a `_ci` collation;
   harmless, every save bumps `rev`).
3. **Snapshot 3 fails the theme bench on Shift+Tab** (`THEME.md`): controls scrolled up to land under the live sticky
   header (WCAG 2.4.11), every width, he and en. Fixed in candidate `e28df264` (owner-wizard 2.0.1, +12/-7 lines): the
   same theme suite passes 32/32 on 127.0.0.1:9406 (2,448 focus events, none covered).
   Releasing 2.0.1 instead: `python scripts/had-256/make_release.py --snap e28df264` rewrites the module pinned to it
   (x-broker-drop is the same; snippet 707 body `0affcdd05fc0faf8af0cf3f0e6623a0d7479516a5e4f6ac698c9d0953f43846b`, file
   `68609da31337ac832be825a7366bff06b510ebd664894d9d94c30b465ab20345`; proven by its self-check), and the need-strings read
   `data-v="2.0.1"` / `"v":"2.0.1"`. Maya would then QA 2.0.1 (a fourth snapshot), not 3. main and Ben decide.
4. **Page copy and the English wrapper** (`THEME.md`, "Seen on the screenshots"): "WhatsApp and call buttons" promised
   unconditionally (page 4958 + the plugin's "how it works"), two "how it works" boxes, ?lang=en inside a Hebrew page.
   Copy is Ben's; none of it is in this package.
5. **The stale-write window** (README open risk 1): a run that stalls longer than the lock TTL (420 s, 7 minutes) right
   after a fence check and then resumes can make ONE check-then-write on the single claimed post (title, meta, page
   HTML or photo copies) with its own older revision. It can never create a second listing, change the status or commit
   a result; the next save or publish rewrites it. Closing it fully needs every write fenced inside the database.
6. **HEIC**: refused where Imagick cannot read HEIC (the bench's cannot); the live server's Imagick/GD were not probed.
   A cheap pre-check for the runner: one bridge op returning `Imagick::queryFormats('HEI*')`, `gd_info()` and
   `function_exists('sodium_crypto_secretbox')` (2.0 refuses rotated photos without GD/Imagick and needs libsodium to
   seal; the healthcheck's `sealed` must be true).
7. **Cached copies**: public photo copies are deleted before a listing leaves `publish` and purged from LiteSpeed;
   a CDN or a browser may still hold one it already fetched. The signed-in page is `no-store`; the anonymous
   `/post-listing/` stays cacheable (purge it after the write and after a rollback).
8. **Recovery mail** depends on the live site's outbound mail (auth.php noted none on 12.7.2026): not verifiable here.
9. **The 1.0 + 1.1.4 pair** exists for the seconds between the two writes; it was not drilled (see step 7 above).
