# HAD-256 · pinned QA snapshot 2 `qa-c2e4cd31` on port 9403

Maya's second instance. The builder does not reset, reseed, restart or update it. Snapshot 1 (`d2b8f349`) stays on
9402, untouched (restarted once after the usage-limit stop on its own unchanged data, see
`bind-check-qa-9402-restart.txt`). A newer slice gets 9404.

| | |
|---|---|
| Served commit | `c2e4cd31` (the shipped modules are byte-identical to `c1f84401`; c2e4cd31 adds results and tests only) |
| URL | http://127.0.0.1:9403/post-listing/ (English: `?lang=en`) |
| Start command (from the worktree root) | `node scripts/had-256/local/start.mjs qa c2e4cd31 9403` |
| Where it lives | `scripts/had-256/local/.runtime/qa-c2e4cd31/`: `snapshot/` (git-show copies of the commit, read-only), `site/` (its own WordPress + SQLite), `site/wp-content/mail-sink/` (its own mail sink) |
| Builder's site | http://127.0.0.1:9401 (hot, not for QA) |

## What changed since snapshot 1 (and is in this one)

P0 public media: a public copy of an owner's photo exists only while its listing is committed as `publish`.
The owner build writes the page as a non-public draft, commits the status with ONE fenced UPDATE (a run that lost the
lock cannot publish, hold or unpublish), and copies the photos only after `publish`; leaving `publish` (remove, hold,
draft, from any door including wp-admin) deletes every public copy BEFORE the status row changes; a view repairs a
published listing whose copies a dead run did not finish; a daily sweep removes stray copies.
P1: another account's local queue and the 1.x `nlow-draft` text are never listed, read, shown, imported or deleted
(the per-account neutral line is shown on every screen); a tab whose account changed is cleared at once (a no-data
ping between tabs, plus focus / visibility / back-forward checks against the server), the signed-in page is sent with
`Cache-Control: no-store`; the "sign in to another account" link is escaped once and returns to the journey.
Also: L08 exactly-once by a database-enforced claim (unique option_name) with fencing tokens; IP rate buckets keep a
string identity; draft photos sealed at rest and optionally outside the web root (NL_OWNER_PRIVATE_DIR); EXIF
orientations 1-8 applied (GD, else Imagick, else the photo is refused).

Known in this snapshot (fixed on 9401 after it, will come in snapshot 3): on phones the site's floating bar lifts
150 px over the fields above a form button (its own "clash" rule) and can cover a field; input placeholders use the
browser grey (4.41:1); disabled buttons are drawn at 60 % opacity (3.1:1, exempt under WCAG but unreadable).

## SHA-256 of the served files (LF bytes, as committed)

| File | SHA-256 |
|---|---|
| plugins/nadlan-config/inc/owner-wizard.php (2.0.0) | `33d692eaaef3d47e6a36af6cd13b6ea3a8506df2807754dc0ab51f53036e422b` |
| plugins/nadlan-config/inc/broker-drop.php (1.1.4) | `dff44c897230e0699496d2fa6fac000ce9e80bf4bfb6238e0ea18c878cf6cacd` |
| scripts/had-256/local/mu-plugins/nlj-bench.php (bench only) | `4c6fc232280525df519985e4d1031b9da55ddfd645704bad246d0a2fbfeb641e` |
| scripts/had-256/local/loopback.cjs (bench only) | `18b709a6adf6322ab1b0b8ffe570978b0e7b5592a8149fd468664c821ea225b4` |
| plugins/nadlan-config/inc/funnel.php (unchanged) | `abd78bf84f201eab6f4dbea96859a2041b38420ffb24ce6ddb203e5f0c68b54c` |
| plugins/nadlan-config/inc/auth.php (unchanged) | `5fb12b7ac8450483160d0cdfb250c28fcab01851f4142b464b5d35502965b9f7` |
| plugins/nadlan-config/inc/property-owner.php (unchanged) | `fa5060a76bac479039c97116be451fc6214548a108da97c3034f27d319a5f756` |
| plugins/nadlan-config/inc/conversion-cta.php (unchanged) | `a55a9d27ce5696e05d3348013794a3893e0d2da1e4dcb2a21d0aa5125a22a7de` |

## Socket proof

`docs/qa/had-256/bind-check-qa-9403.txt`: every listening socket of the QA-2 process (PID 5528) is on 127.0.0.1;
192.168.0.143:9403 is refused; 9402 is still listening on 127.0.0.1 (PID 21284).

## Accounts (local-only synthetic test credentials)

| Account | Email | Password | Role |
|---|---|---|---|
| QA user A | qa.a@example.test | `QA-Local-A-2026!` | subscriber |
| QA user B | qa.b@example.test | `QA-Local-B-2026!` | subscriber |
| QA admin | qa.admin@example.test | `QA-Local-Admin-2026!` | administrator |

Mail (recovery links): `scripts/had-256/local/.runtime/qa-c2e4cd31/site/wp-content/mail-sink/*.json`, or
`GET http://127.0.0.1:9403/?rest_route=/nlj-test/v1/mail`.

## Resetting ONLY this instance

`POST http://127.0.0.1:9403/?rest_route=/nlj-test/v1/reset` (127.0.0.1 callers only). Touches only
`.runtime/qa-c2e4cd31/site/`.

## Real vs stubbed

As in QA-SNAPSHOT.md (real modules + WordPress core in Playground/SQLite; stubbed post types, compliance rules copied,
no i18n so the bar says "לפרטים נוספים", AI off, outbound HTTP blocked, mail to the sink, Twenty Twenty-Five theme,
wptexturize off as on the live site). Production theme integration is not verified on the bench. SQLite is not MySQL.
