# Professionals' forum, version one: build notes (12.11.2026)

## Owner correction 12.11
The professionals in the directory were imported from public registers and did not ask to take part. Applied:
1. The forum window ("בפורום", tabs, contact buttons, owner controls) prints only on the profile of a professional who joined himself: a member row whose `pro_id` was set through his verified email (`nlf_pro_member()` in inc/pro-forum.php).
2. Every other profile gets only a neutral box: "מחפשים בעל מקצוע?", "פרסמו בקשה בפורום ובעלי מקצוע שהצטרפו יענו לכם.", button "פרסמו בקשה" (compose with kind=seek and the profession's category, no pro_id), then the dashed "זה הכרטיס שלכם?" box with "הצטרפות" (one-step entry) and "הסרת הכרטיס" (request form).
3. No mail of any kind goes to a professional who has not joined. The mail to "the email on record" was removed; the one direct-question mail goes to the joined member's own verified address only. Other notifications go only to members (followers).
4. REST `forum/topic` refuses a `pro_id` whose card has no linked member (HTTP 400, Hebrew message).
5. Phone and WhatsApp print only for a linked member who switched `show_phone` on himself.
6. Data model: `topics` got `need_profession` (category key), `need_city`, `status_seek` (open|closed). A new `seek` discussion fills them (`open`). No board UI yet.
Also because of this: the home lead line says "בעלי המקצוע שהצטרפו" instead of the board's "בלי מתווך באמצע" (honest, and does not insult the brokers who are members).

## What was built (new files only)
| File | Bytes | What |
|---|---|---|
| plugins/nadlan-config/inc/pro-forum.php | 81 KB | pure functions, gate, tables, members and session, the guard, moderation, mail, REST, addresses, search-engine tags, assets |
| plugins/nadlan-config/inc/pro-forum-render.php | 43 KB | home, discussion, professional window, neutral box, claim box, owner box, sheets, one-click link pages |
| plugins/nadlan-config/inc/pro-forum-admin.php | 10 KB | wp-admin "פורום" screen |
| plugins/nadlan-config/assets/proforum/forum.css | 19 KB | scoped under `.nlf` |
| plugins/nadlan-config/assets/proforum/forum.js | 24 KB | no library, unminified |
| plugins/nadlan-config/tests-local/pro-forum-test.php | 11 KB | CLI test of the pure functions |

Hebrew text is 2 bytes a character, so the PHP byte sizes look large.

## What the releaser must add (replaced after the review of 12.11.2026, see REVIEW.md)
One line appended at the END of the LIVE `inc/pro-network.php` (NOT the module list in `nadlan-config.php`):
`if ( file_exists( __DIR__ . '/pro-forum.php' ) ) { require_once __DIR__ . '/pro-forum.php'; }`
`pro-forum.php` itself requires `pro-forum-trades.php`, the render file and, in wp-admin only, the admin file. No manual step: the module writes its rewrite rules once per rules version on `wp_loaded` (option `nadlan_forum_rules`; skipped if a published page already owns `/forum/`) and creates its tables once per DB version (now 2). Options all default safely: `nadlan_forum_public` '0'. Probe for the runner: `GET /wp-json/nadlan/v1/forum/ping` always 200 `{"loaded":true,"public":false,"v":"0.1.0"}`.

## Every WordPress hook used
Actions: `init` (prio 1: ?forum=on/off cookie; prio 10: rewrite rules), `admin_init` (`nlf_install`; admin screen POST actions), `rest_api_init` (13 routes), `parse_query`, `template_redirect` (prio -100: `?nlf_act=` one-click pages; prio 1: render forum pages inside get_header/get_footer and exit), `wp_head` (prio 2: description and canonical only when Yoast is absent, JSON-LD), `wp_enqueue_scripts` (prio 30), `wp_footer` (prio 20: dialogs), `admin_menu` (prio 20), `litespeed_control_set_nocache` (fired).
Filters: `query_vars`, `posts_pre_query`, `redirect_canonical` (false on forum addresses only), `pre_handle_404`, `pre_get_document_title`, `wpseo_title`, `wpseo_opengraph_title`, `wpseo_metadesc`, `wpseo_opengraph_desc`, `wpseo_canonical`, `wpseo_opengraph_url`, `wpseo_json_ld_output` (off on forum pages only, the forum prints its own), `wp_resource_hints`, `litespeed_vary_cookies`, `the_content` (prio 40, singular nadlan_professional), plus the module's own `nadlan_forum_send_code` (SMS later) and `nadlan_forum_admin_email`.
REST (nadlan/v1/forum/): GET state, similar; POST code, enter, leave, topic, reply, thank, solve, follow, report, view, owner, request. Errors are HTTP 400.

## How the profile window is attached
No edit to professional-profile.php. A `the_content` filter at priority 40 (after the profile at 6 and its wpautop shield restore at 11) appends `<div class="nlf-card-zone">` for singular `nadlan_professional`, in the loop, main query, gate open. `nadlan_forum_card_window( $id )` is also public for other placements.

## Deviations from the brief, and why
- Home pagination is `?pg=2`, not `?p=2`: `p` is a WordPress core query variable (post id); it would turn the forum into a post query and trigger a canonical redirect.
- Canonical of the unfiltered home page 2 is its own address (`/forum/?pg=2`); filtered views point to `/forum/`.
- Admin approve/reject mail links open a page with one confirm button (POST). Mail scanners open links by themselves; a pure GET would approve or reject without the admin. Unsubscribe links act at once on GET (harmless).
- One-click pages live on the front page URL (`/?nlf_act=token`), not admin-post.php, so they work for people who are not logged in and with the gate closed.
- Extra tables `follows` and `requests`; extra columns `pro_notified`, `body_hash`, `ip_hash` on topics/replies.
- A discussion's author follows it automatically (every mail has the one-click stop link).
- Thanks and follow have their own ceiling (90 an hour per IP); the 20-an-hour ceiling counts content writes (topics, replies, reports, requests).
- Not built from the boards: the "14 כותבים עכשיו" and "כותב תשובה עכשיו" live signs (no real data), search button, bottom navigation, videos tab, endorsements tab, "עדכון שבועי" switch (column `digest` exists), "מאומתים קודם" sort, image/video/poll buttons in compose.
- Proof-of-work default is 14 bits (option `nadlan_forum_pow_bits`, 8 to 20): 16,384 digests took 129 ms in Node on this PC; a phone should take about 0.5 to 1.5 s.
- One session per member: a new code entry on another device ends the previous session.

## Tested here
- `php -l` on all PHP files: no syntax errors. `node --check forum.js`: ok.
- `php tests-local/pro-forum-test.php`: 89 passed, 0 failed (categories, link and phone guard, normalisation, length rules, duplicate window, Discourse limits, proof of work, challenge and form time signing, HMAC links, code hashing, expiry and tries, output escaping, house-law scan of the module files).
- The browser solver (Web Crypto) and PHP agree on the nonce for the same challenge.

## Not tested (no WordPress here)
Everything touching `$wpdb`, dbDelta, hooks, REST, cookies, templates, the theme, Yoast, LiteSpeed and mail. Specifically unverified: that `pre_handle_404` + `posts_pre_query` give a clean 200 page inside the theme and a normal 404 when closed; whether the theme header prints its own h1; Yoast's output on a non-WordPress address (title, canonical, robots); that LiteSpeed honours the no-cache and `litespeed_vary_cookies`; that `wp_update_post` to private/back triggers no unwanted side effects in other modules; dialogs, focus, 360 px layout and console in a real browser; real phone timing of the proof of work; that a `/forum` WordPress page does not already exist live (the rules are added at 'top').
