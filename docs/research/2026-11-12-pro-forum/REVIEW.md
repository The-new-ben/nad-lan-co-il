# Professionals' forum: review before the hidden release (12.11.2026)

Reviewer: a review session (Opus 5.5), code only. Nothing was deployed, committed or run against the site.
Files touched: `inc/pro-forum.php`, `inc/pro-forum-render.php`, `inc/pro-forum-admin.php`, `assets/proforum/forum.css`,
`assets/proforum/forum.js`, `tests-local/pro-forum-test.php`, this file and `BUILD-NOTES.md`. `inc/pro-forum-trades.php` was read, not changed.
Line numbers below are of the files after the fixes (paths relative to `plugins/nadlan-config/`).

## Requirements

| requirement | status | file:line | note |
|---|---|---|---|
| 1a. Gate option `nadlan_forum_public` default '0' | ok | inc/pro-forum.php:321 | |
| 1b. Gate: ?forum=on, cookie nlf_gate, administrator | ok | inc/pro-forum.php:324 | `?forum=off` closes even with the cookie |
| 1c. Gate cookie set ONLY by ?forum=on | ok | inc/pro-forum.php:377 | the only `nlf_cookie( 'nlf_gate', '1'` call. Now HttpOnly too (JS never reads it) |
| 1d. /forum/ and /forum/<n>/ closed = real WordPress 404 | ok | inc/pro-forum.php:1475 | `pre_handle_404`: set_404 + status 404, theme 404 template (smart-404 body keeps the 404, its 301 list does not touch /forum/) |
| 1e. No forum HTML/CSS/JS on any other page while closed | fixed | inc/pro-forum-render.php:316, 539; inc/pro-forum.php:1622 | (1) `nadlan_forum_card_window()` is public and had no gate check: now returns '' while closed. (2) Any made-up `/?nlf_act=x` used to render a forum page with forum.css + forum.js + Google fonts for anyone; now a broken token with the gate closed falls through to the normal page (`nlf_act_takeover`), and a genuine one-click page loads the CSS only |
| 1f. REST routes answer 400 while closed | ok | inc/pro-forum.php:441, 783, 1090 | all 13 routes check the gate first; errors are `status 400` only |
| 1g. REST routes hidden from the public `/wp-json/` index | fixed | inc/pro-forum.php:1078 | `show_in_index => false` (the index listed `/forum/...` to anyone) |
| 1h. GET forum/ping: always 200, `{loaded, public, v}` only, no-cache | added | inc/pro-forum.php:1082 | coordinator's request; the only route that answers while closed |
| 1i. No-cache on every gated response | fixed | inc/pro-forum.php:359, 368, 374-385, 441, 446 | `nlf_nocache()` = nocache_headers + DONOTCACHEPAGE + `litespeed_control_set_nocache`, re-fired on `wp` (it was called at init priority 1, possibly before LiteSpeed Cache hooked the action; a raw X-LiteSpeed-Cache-Control header is overwritten by LiteSpeed at the end). Added: every request carrying `?forum=`, `nlf_gate` or `nlf_s` is no-cache on ANY page; a professional page with the gate open is no-cache at `template_redirect` priority 0 (before output; before the fix it was decided inside `the_content`, after headers may have gone, so a Varnish/CDN layer could have stored it); every REST answer (ok and error) is no-cache (LiteSpeed Cache can cache REST GETs: `state` carries the member's name and nonce) |
| 1j. Vary on the gate cookie (LiteSpeed) | fixed | inc/pro-forum.php:391, 397 | kept `litespeed_vary_cookies` (only reaches .htaccess when LiteSpeed Cache saves settings); added `litespeed_vary_curr_cookies` on forum addresses and professional pages so the public cached copy carries `X-LiteSpeed-Vary: cookie=nlf_gate,...` and a gated browser never gets it |
| 2a. No redirects | ok | inc/pro-forum.php:1472; inc/pro-forum-render.php:522, 534 | no wp_redirect / wp_safe_redirect / Location / 301 / 302 in the module (test scans the source). `redirect_canonical` is off on forum addresses only; template_redirect callbacks render and exit on the same URL; the act-page confirm form POSTs to the same URL. JS `location.assign` after posting is a client navigation, not a server redirect |
| 2b. No noindex/nofollow/robots changes | ok | tests-local/pro-forum-test.php | source scan test |
| 2c. Canonical: self for a discussion, /forum/ for filtered views | fixed | inc/pro-forum.php:1537, 1555, wp_head block | Yoast printed the canonical/description only if it called its filter for a virtual address; now the forum always prints its own and Yoast's are switched off on forum pages only (exactly one each). A home page past the last page (`?pg=999`) now points to /forum/ instead of itself (endless empty self-canonical pages). Unfiltered page 2 keeps its own canonical (builder's documented choice) |
| 3a. Non-member card: no window, phone, WhatsApp | ok | inc/pro-forum-render.php:420, 375, 382 | `the_content` prio 40: neutral box "מחפשים בעל מקצוע?" + "פרסמו בקשה" + "זה הכרטיס שלכם?" (הצטרפות / הסרת הכרטיס) unless `nlf_pro_member()` |
| 3b. Phone/WhatsApp only for a linked member who switched it on | ok | inc/pro-forum.php:716 | |
| 3c. REST refuses addressing a non-member | ok | inc/pro-forum.php:1206 | 400 with a Hebrew message |
| 3d. Every wp_mail and its recipient | ok | inc/pro-forum.php:950 (nlf_mail), 978, 995, 1016, 1119, 1323, 1414 | admin (pending, 3 reports, card request); followers = members' own verified address; direct question = the linked member's own verified address (opt-out link, `nl_forum_optout`); the code mail = the address the visitor typed. No mail ever reads `email`/`_nl_email` of a card as a recipient. Added a per-address day cap on code mails (6 a day, 3 an hour) so the entry form cannot flood a register professional's mailbox |
| 4a. SQL through prepare | fixed | inc/pro-forum.php:726 | `nlf_members()` interpolated (int) ids; now placeholders. ORDER BY of the home list comes from a fixed whitelist, LIMIT/OFFSET are (int); admin queries use fixed strings only |
| 4b. Output escaping, JSON-LD | fixed | inc/pro-forum.php:290, 1567, 1627 | `nlf_json_script()` (HEX_TAG + HEX_AMP + UNESCAPED_UNICODE + UNESCAPED_SLASHES) for the JSON-LD and the inline `window.NLF` (the latter had no HEX_TAG); test proves no `</`, `<` or `>` in the output |
| 4c. Nonces on REST writes and admin actions | fixed | inc/pro-forum.php:798, 1184; inc/pro-forum-admin.php:29-30 | per-session header nonce on all member writes; `leave` had none, now checked (JS retries once with a fresh one). Admin: `check_admin_referer` + `manage_options` |
| 4d. Admin screen capability | ok | inc/pro-forum-admin.php:64 | |
| 4e. Session token hashed; cookie HttpOnly + Secure + Lax | fixed | inc/pro-forum.php:344, 620 | SHA-256 stored only. Secure used `is_ssl()` alone, false when TLS ends at the host's proxy: now also true when the site address is https |
| 4f. Codes hashed, expiry, tries | ok | inc/pro-forum.php:246 | HMAC, 10 minutes, 5 tries |
| 4g. HMAC links: hash_equals, secret from wp_salt | ok | inc/pro-forum.php:197, 333 | |
| 4h. Rate limits on member AND ip_hash | fixed | inc/pro-forum.php:423, 783 | content writes and light actions counted per hashed IP and per member (before: per IP only); card requests per member and per IP |
| 4i. No user-controlled file paths | ok | | none |
| 4j. Proof of work single-use, signed, expiry | ok | inc/pro-forum.php:214, 791-792 | |
| 4k. JS: no innerHTML, no eval | ok | assets/proforum/forum.js | textContent / createElement only; test scans |
| 4l. Owner switches cannot publish a card the staff hid | fixed | inc/pro-forum.php:301, 1056 | before: "show" on a card an admin had made private published it. Now only a card the owner hid goes back, only to its stored status (`nlf_restore_status`, tested) |
| 4m. Card status change from a forum request | fixed | inc/pro-forum.php:1037 | `wp_update_post` ran for no logged-in user, so kses would strip the card's content HTML; kses is lifted for that one call; LiteSpeed is asked to purge the card |
| 5. Data honesty | ok | inc/pro-forum.php:283; inc/pro-forum-render.php | no sample data; every counter goes through `nlf_count_words` or `> 0` checks; empty states say so |
| 6a. No emoji, long dashes, banned words, "נחבר אתכם" | ok | tests-local/pro-forum-test.php | source scan |
| 6b. Buttons second person plural | ok | | imperatives are plural (כתבו, פרסמו, שלחו); the rest are nouns (שליחה, כניסה) |
| 6c. One h1 per forum page | open (live) | inc/pro-forum-render.php:133, 244, 575 | the module prints one; whether the theme header adds one on a virtual page can only be seen live |
| 7a. CSS/JS only on forum surfaces | ok | inc/pro-forum.php:1622 | forum pages, a genuine one-click page (CSS only), a professional page with the gate open (not a removed card) |
| 7b. Touch targets >= 44px, focus ring, aria-live, reduced motion | fixed | assets/proforum/forum.css:14, 42, 223; render:158 | focus ring now `!important` (the theme forces button styles) |
| 7c. 360px, no horizontal scroll | fixed | assets/proforum/forum.css:8, 134 | the trap field sat at `left:-9999px`: on a right-to-left page that scrolls sideways; now clipped in place. `overflow-wrap:anywhere` on every `.nlf` root (the card window and sheets did not have it; long words or links could overflow) |
| 8a. Loaded by one line at the END of inc/pro-network.php | fixed | inc/pro-forum.php:20-24, 1650-1652 | works at plugin-load time (only add_action/add_filter/is_admin/define at top level); loads trades, render and (wp-admin only) admin itself; double include is harmless (require_once + NADLAN_FORUM_VERSION guard). The live pro-network.php (docs/qa/live-read/20261112T172508Z) has no early return and no closing tag |
| 8b. Rewrite rules flushed once by the module | fixed | inc/pro-forum.php:307, 1430, 1445 | on `wp_loaded` (after every plugin's init, so a flush drops nobody's rules), guarded by option `nadlan_forum_rules` (version 1); stored before flushing so it never loops. If a published page/post already owns `/forum/`, no rule is added and nothing is flushed (the forum must never hide a live page); the admin screen says so |
| 9. Tables once per DB version | fixed | inc/pro-forum.php:462, 584, 590 | dbDelta only when the stored version differs; the version is stored only when all 8 tables exist (before: stored even if dbDelta failed); a failed attempt waits an hour; option autoloaded (read on every forum request). DB version 2 adds `members.trade` and `members.trade_other` |
| Trades (coordinator) | added | inc/pro-forum.php:1154, 1650; render:473-476; forum.js | a member who says "בעל מקצוע" picks a trade from `nadlan_forum_trades()` (key stored) or "תחום אחר" (free text, kept for admin review, shown only on the admin screen). The trade label shows next to his name, never a verified mark: no licence check was built ('reg' contractors/brokers/appraisers is for a later join check; lawyers 'review' get nothing until the owner decides) |

## Tests
- `php -l` on the four PHP module files and the test: no syntax errors (PHP 8.1 and 8.3).
- `php tests-local/pro-forum-test.php`: 115 passed, 0 failed (was 89). New: script-safe JSON, restore-status rules, rewrite step, one-click takeover, trade list (84 in 6 groups, reg values, search), no innerHTML/eval, no off-screen CSS, reduced motion, routes out of the index, ping shape, 400 only, no 301/302, trades file loaded.
- Note: the WinGet PHP 8.1 has no mbstring, so the test fatals there on `mb_substr`; run it with `C:\Users\777\tools\php-8.3\php.exe` (WordPress itself polyfills mb_substr).
- `node --check assets/proforum/forum.js`: ok.

## Still open (not fixed here)
1. Follower mails are sent inside the request that publishes a reply (up to 200 through SMTP). Fine at launch volume; move to a scheduled event before the forum is public.
2. Rate limits use `REMOTE_ADDR` like the site's other modules. If uPress puts a proxy in front, all visitors share one IP bucket (20 writes an hour site-wide). Check live.
3. When `nadlan_forum_public` becomes '1', every professional page becomes no-cache (the card zone depends on the session). A decision for the public launch, not for the hidden release.
4. `wp_update_post` on a card fires other modules' save hooks for a request with no logged-in user (builder's open item).

## Only the live site can show
1. Closed gate, logged out: `/forum/` and `/forum/1/` answer 404 with the theme 404 page; the HTML of the home page, a professional page and the 404 contains none of: `nlf-card-zone`, `nlf nlf-win`, `nlf nlf-neutral`, `nlf nlf-claim`, `id="nlf-compose"`, `assets/proforum/`, `nlf-css`, `nlf-fonts-css`, `window.NLF=`.
2. `GET /wp-json/nadlan/v1/forum/ping` = 200 with the three keys; `GET /wp-json/nadlan/v1/forum/state` = 400; `/wp-json/nadlan/v1` index does not list `forum`.
3. LiteSpeed: a professional page answers with `X-LiteSpeed-Vary` containing `nlf_gate`; with the cookie, `X-LiteSpeed-Cache` is a miss and the response carries no-cache; after visiting with `?forum=on`, a second browser without the cookie still gets the public page (no forum markers). Same check for any Varnish/CDN layer uPress adds.
4. Gate open: `/forum/` answers 200 inside the theme, exactly one h1, a canonical and a description printed once (Yoast's off), title from the module, Yoast robots not set to noindex.
5. The rules option `nadlan_forum_rules` is written once after the first request; no live page owned `/forum/` (else the admin screen says so and the forum stays off that address).
6. Entry by code mail arrives (Brevo), the cookie is Secure, the trade picker appears for "בעל מקצוע".
7. 360 px phone: no sideways scroll on the forum home, a discussion, a profile with the card zone and the sheets; focus ring visible; dialogs return focus.
8. Owner switches on a test card: hide makes it private and the cached page disappears; show restores; content HTML unchanged.
