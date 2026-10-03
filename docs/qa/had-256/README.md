# HAD-256 · the owner listing journey · local build for QA

Status: **work in progress, local only.** Nothing here is live and nothing here may be released on the strength of
a Playground (SQLite) run. Main is the only publisher.

| | |
|---|---|
| Worktree | `C:\Users\777\nad-lan\nad-lan-co-il\.claude\worktrees\agent-a61b211e083144352` |
| Branch | `worktree-agent-a61b211e083144352` (based on `6e9cf930`, the design + contract commit) |
| Snapshot for QA | see "Snapshots" below (named commit hashes; the code under test is the commit, not the folder) |
| Preview | `node scripts/had-256/local/start.mjs after` then http://127.0.0.1:9401/post-listing/ |
| Before (base code 6e9cf930) | `node scripts/had-256/local/start.mjs before` then http://127.0.0.1:9402/post-listing/ |
| Both | `node scripts/had-256/local/start.mjs` (add `--fresh` to reinstall the sites) |

## Snapshots

| Name | Commit | What is in it |
|---|---|---|
| slice-1 | (this commit, see `git log -1 -- docs/qa/had-256/README.md`) | account (open, existing email, sign in, recovery reply) + details + the draft saved in the account and resumed after a reload, on real WordPress |

## What is real and what is stubbed

**Real** (the code that would ship, running inside WordPress Playground 3.1.56, WordPress 7.1.2, PHP 8.3, SQLite,
6 worker threads, driven over HTTP and by a real Chrome through Playwright):
`plugins/nadlan-config/inc/owner-wizard.php` (new 2.0.0), `broker-drop.php` (1.1.4 hunks), `funnel.php`, `auth.php`,
`property-owner.php`, `conversion-cta.php` (the site's floating WhatsApp pill), WordPress core (users, REST, nonces,
cookies, posts, meta, options, password reset).

**Stubbed by the bench** (`scripts/had-256/local/mu-plugins/nlj-bench.php`, never shipped):
- the `nadlan_property` / `nadlan_professional` post types (same public args as `nadlan-config.php`, without the listing capability map);
- the plugin's own `[nadlan_listing_wizard]` shortcode (replaced by x-owner-wizard, as on the live site);
- `nadlan_compliance_scan` (the rules of `inc/ai-features.php`, copied);
- `nadlan_i18n` is not loaded, so the floating pill shows its built-in fallback words ("לפרטים נוספים") instead of the live "ייעוץ חינם";
- theme: Twenty Twenty-Five, NOT the NadLan theme. Production theme integration (the real header, footer, skin
  and page template of /post-listing/) is **not verified on the bench** and stays a separate check on the live
  site; a form inside the bench theme is not "site integration". Fonts load from Google Fonts for the screenshots;
- AI: off (`NADLAN_DISABLE_AI`), and every outbound HTTP request from PHP is blocked (logged to `wp-content/nlj-blocked-http.log`);
- mail: every email is written to `wp-content/mail-sink/*.json` (pre_wp_mail); nothing is sent;
- data: synthetic only (`scripts/had-256/local/seed.json`: dana / yoav / bench admin, all `@example.test`; "שכונת הדוגמה, תל אביב יפו").

**What SQLite in Playground cannot prove** (needs the live MySQL, by main, before any release): the exact
`INSERT IGNORE` / compare-and-swap row counts of MySQL, lock behaviour under the live PHP worker model, LiteSpeed
caching, the live theme, real outbound mail delivery (auth.php notes the site had no working outbound mail on
12.7.2026: password recovery depends on it), and the live server's image library (GD/Imagick) for orientation and HEIC.

## Bench safety

- Loopback only. The Playground CLI has no bind option (`server.listen(port)` binds every interface), so
  `scripts/had-256/local/loopback.cjs` is preloaded through `NODE_OPTIONS` and pins every `listen()` of the bench
  processes to 127.0.0.1. Proof: `docs/qa/had-256/bind-check-after.txt` (all 7 sockets of the bench process on
  127.0.0.1; the machine's LAN address 192.168.0.143:9401 is refused; 127.0.0.1:9401 answers 200).
  Maya confirmed the same independently (9401 on 127.0.0.1, PID 29564).
  Correction: the very first bench runs today (a 9455 probe and the first 9401 run, before 01:15) were bound to all
  interfaces; they were stopped and are not used for any result.
- The test-only routes (`nlj-test/v1/*`: reset, fault, state, mail) and every fault hook live only in the bench
  mu-plugin. `grep -rn "nlj-test\|nlj_fault\|nlj_reset\|NLJ_VARIANT" plugins/` finds nothing. The shipped code only
  fires `do_action( 'nl_drop_checkpoint', ... )`, which nothing listens to on the live site.

## Results so far (slice-1)

Command: `cd scripts/had-256/tests && python smoke_slice1.py` (needs the after bench running).

| Check | Result | Label |
|---|---|---|
| Open an account (new synthetic email) signs in and lands on the details step | pass | real WordPress + Chrome |
| Typing saves to the account: the status line goes "נשמר במכשיר הזה" then "נשמר בחשבון" with the time | pass | real WordPress + Chrome |
| A reload without the draft address offers "יש לכם טיוטה שמורה"; "המשך" restores deal, city, neighbourhood, rooms | pass | real WordPress + Chrome |
| An email that already has an account: the error sits under the field, the name and email stay, "כניסה עם המייל הזה" carries the email to the sign-in tab | pass | real WordPress + Chrome |
| A wrong password: one neutral message, the input stays | pass | real WordPress + Chrome |
| No JavaScript errors on these screens | pass | real WordPress + Chrome |

Screenshots: `docs/qa/had-256/shots/after/slice1-*.png` (390 px, Hebrew).

The full L01-L17 table, the before/after runs and the contrast table follow in later snapshots.
