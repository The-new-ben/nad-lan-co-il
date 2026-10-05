# HAD-256 · pinned QA snapshot 3 `qa-2ce0a741` on port 9404

Maya's third instance: the code every result in `RESULTS.md` (run 2) was produced on. The builder does not reset,
reseed, restart or update it. 9402 (`d2b8f349`) and 9403 (`c2e4cd31`) stay as they are. A newer slice gets 9405.

| | |
|---|---|
| Served commit | `2ce0a741` |
| URL | http://127.0.0.1:9404/post-listing/ (English: `?lang=en`) |
| Start command (from the worktree root) | `node scripts/had-256/local/start.mjs qa 2ce0a741 9404` |
| Where it lives | `scripts/had-256/local/.runtime/qa-2ce0a741/`: `snapshot/` (git-show copies, read-only), `site/` (own WordPress + SQLite), `site/wp-content/mail-sink/` |

## New since snapshot 2

- The site's floating bar stays at its resting place on the journey (the site's own `--nlcta-band` switch; on phones
  its "clash" lift used to put it 150 px up, over fields), the page keeps measured room below the last control, and a
  focused control is scrolled above the bar (also when a phone keyboard resizes the screen).
- Placeholders #59636d (5.9:1), disabled buttons drawn solid (7:1); failed photo tiles no longer clip their buttons at 320 px.
- A held owner listing keeps its Latin address (WordPress empties the slug of a pending post saved by a user who cannot
  publish; found by L13).
- The bench mirrors the live site's `run_wptexturize` off and seeds the page with a classic shortcode; a synthetic
  broker route for the broker-door regression; the image-library report route.

## SHA-256 of the served files (LF bytes, as committed; the tested working tree has the same hashes)

| File | SHA-256 |
|---|---|
| plugins/nadlan-config/inc/owner-wizard.php (2.0.0) | `9fcafd9d0e6b134c360b383df4622b8919a54d3bf06713706e4d377cddf892bd` |
| plugins/nadlan-config/inc/broker-drop.php (1.1.4) | `dff44c897230e0699496d2fa6fac000ce9e80bf4bfb6238e0ea18c878cf6cacd` |
| scripts/had-256/local/mu-plugins/nlj-bench.php (bench only) | `4058645b5dfde720d7e42ceaddf762203a807fc2ae187ebd6a61fbabe4103666` |
| scripts/had-256/local/loopback.cjs (bench only) | `18b709a6adf6322ab1b0b8ffe570978b0e7b5592a8149fd468664c821ea225b4` |
| funnel.php / auth.php / property-owner.php / conversion-cta.php | unchanged, same hashes as in QA-SNAPSHOT-2.md |

## Socket proof

`bind-check-qa-9404.txt`: every socket of the QA-3 process (PID 21740) on 127.0.0.1; 192.168.0.143:9404 refused;
9402 and 9403 still listening on 127.0.0.1.

## Accounts, mail, reset, real vs stubbed

As in `QA-SNAPSHOT-2.md`: qa.a@example.test / `QA-Local-A-2026!`, qa.b@example.test / `QA-Local-B-2026!`,
qa.admin@example.test / `QA-Local-Admin-2026!` (local-only synthetic test credentials). Mail:
`.runtime/qa-2ce0a741/site/wp-content/mail-sink/`. Reset only this instance:
`POST http://127.0.0.1:9404/?rest_route=/nlj-test/v1/reset`. Real modules + WordPress core on Playground/SQLite;
stubs, theme and SQLite limits as listed in README.md.
