# HAD-256 · pinned QA snapshot `qa-d2b8f349` (slice-1) on port 9402

This instance is Maya's. The builder does not reset, reseed, restart or update it. A newer slice gets a NEW port
(9403, 9404, ...), announced in this file's successors; 9402 stays on `d2b8f349`.

| | |
|---|---|
| Served commit | `d2b8f349` (snapshot "slice-1") |
| URL | http://127.0.0.1:9402/post-listing/ (English: `?lang=en`) |
| Start command (from the worktree root) | `node scripts/had-256/local/start.mjs qa d2b8f349 9402` |
| Where it lives | `scripts/had-256/local/.runtime/qa-d2b8f349/` (git-ignored): `snapshot/` = the committed files (read-only), `site/` = its own WordPress + SQLite, `site/wp-content/mail-sink/` = its own mail sink |
| Builder's site (hot, changes all the time) | http://127.0.0.1:9401 - not for QA |

## How the snapshot was made (immutable, never the working tree)

`start.mjs qa d2b8f349` lists every file of `plugins/nadlan-config/inc/`, `scripts/had-256/local/mu-plugins/` and
`scripts/had-256/local/loopback.cjs` at that commit (`git ls-tree -r d2b8f349 ...`) and writes each one with
`git show d2b8f349:<path>` into `snapshot/`, then the files were set read-only. No checkout, no index change.
Playground mounts `snapshot/plugins/nadlan-config/inc` as `wp-content/nlj-code` and `snapshot/.../mu-plugins` as
`wp-content/mu-plugins`.

SHA-256 of the served files (LF bytes, as committed):

| File | SHA-256 |
|---|---|
| plugins/nadlan-config/inc/owner-wizard.php (changed: 2.0.0) | `926f41fdd6fc51ac581e168779ce8fb4fd07765f29cfbf67b0f1f4da8dbcb21c` |
| plugins/nadlan-config/inc/broker-drop.php (changed: 1.1.4 hunks) | `b7487625b30bf2332df145831e3ba6c4aa375a4f85e0d509136f671dd78e0962` |
| scripts/had-256/local/mu-plugins/nlj-bench.php (bench only, never shipped) | `024563c67e6b5fe2a6424830d8bf6c69404a36443e2bf4d26e6128e6dffcfffb` |
| scripts/had-256/local/loopback.cjs (bench only) | `18b709a6adf6322ab1b0b8ffe570978b0e7b5592a8149fd468664c821ea225b4` |
| plugins/nadlan-config/inc/funnel.php (unchanged) | `abd78bf84f201eab6f4dbea96859a2041b38420ffb24ce6ddb203e5f0c68b54c` |
| plugins/nadlan-config/inc/auth.php (unchanged) | `5fb12b7ac8450483160d0cdfb250c28fcab01851f4142b464b5d35502965b9f7` |
| plugins/nadlan-config/inc/property-owner.php (unchanged) | `fa5060a76bac479039c97116be451fc6214548a108da97c3034f27d319a5f756` |
| plugins/nadlan-config/inc/conversion-cta.php (unchanged) | `a55a9d27ce5696e05d3348013794a3893e0d2da1e4dcb2a21d0aa5125a22a7de` |

`ow_server.php`, `ow_js.js` and the other `scripts/had-256/local/.runtime/*` files are the builder's scratch parts;
they are not served and not committed. What runs is `owner-wizard.php`, which the parts are assembled into.

## Socket proof (loopback only)

`docs/qa/had-256/bind-check-qa-9402.txt`: every listening socket of the QA bench process (PID 18656) is on
127.0.0.1 (9402 and its six worker ports); the machine's LAN address 192.168.0.143:9402 is refused. The Playground
CLI has no bind option; `loopback.cjs` is preloaded through NODE_OPTIONS and pins every `listen()` to 127.0.0.1.
No firewall or Windows setting was changed.

## Accounts and fixtures (local-only synthetic test credentials, never a real person's)

| Account | Email | Password | Role |
|---|---|---|---|
| QA user A | qa.a@example.test | `QA-Local-A-2026!` | subscriber |
| QA user B | qa.b@example.test | `QA-Local-B-2026!` | subscriber |
| QA admin | qa.admin@example.test | `QA-Local-Admin-2026!` | administrator |

Pages: `/post-listing/` (the journey), `/terms/`, `/privacy/` (placeholders). `users_can_register` is on, so new
synthetic accounts can be opened from the journey (use `@example.test` addresses). Sign-in for an existing account:
the journey's "כבר יש לי חשבון" tab. Mail: every email (recovery links included) is a JSON file in
`scripts/had-256/local/.runtime/qa-d2b8f349/site/wp-content/mail-sink/`, also listed by
`GET http://127.0.0.1:9402/?rest_route=/nlj-test/v1/mail`.

## Resetting ONLY this QA instance

`POST http://127.0.0.1:9402/?rest_route=/nlj-test/v1/reset` (from this machine; the route answers only to a
127.0.0.1 caller). It deletes this site's submissions, listings, attachments, locks, claims, rate counters and mail
files, deletes non-seed non-admin users, and resets the three QA accounts to the passwords above. It touches only
the SQLite file under `.runtime/qa-d2b8f349/site/`; 9401 and 9411 have their own.

## Real WordPress vs stubbed

Real (inside WordPress Playground 3.1.56, WordPress 7.1.2, PHP 8.3, SQLite, 6 workers): the six nadlan-config
modules above, WordPress core (users, REST, nonces, cookies, posts, meta, options, password reset).
Stubbed by the bench mu-plugin: the nadlan_property / nadlan_professional post types (same public args, no
capability map), the plugin's own wizard shortcode, `nadlan_compliance_scan` (rules copied from ai-features.php),
`nadlan_i18n` absent (the floating pill shows "לפרטים נוספים", the live text is "ייעוץ חינם"), AI off, outbound
HTTP blocked, mail to the sink, Twenty Twenty-Five theme (the NadLan theme, header, footer and page template are NOT
on the bench; production theme integration is a separate check). SQLite is not MySQL: row counts of INSERT IGNORE
and the conditional UPDATEs must be confirmed on MySQL before any release.

## What slice-1 covers, and what it does not

Covered (and passing on the builder's run, see README): open an account, an existing email keeps the input and
offers sign-in, a wrong password gets one neutral message, details save to the account (status line), a reload
resumes the draft.

Known in `d2b8f349` and fixed after it (so they WILL show on 9402):
- publish fails with `empty_content` (the claimed placeholder post had an empty title; fixed in the next slice);
- the floating bar can cover a link or field under it (Maya's L14 finding; scroll padding for focus added after);
- the full L01-L17 runs, before/after and the contrast table are not part of this slice.
