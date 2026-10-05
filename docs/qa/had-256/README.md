# HAD-256 · the owner listing journey · local build for QA

Status: **local only.** Nothing here is live, nothing is pushed, and nothing may be released on the strength of a
Playground (SQLite) run. Main is the only publisher. Results: `RESULTS.md` (generated) and `results.json` (raw).

| | |
|---|---|
| Worktree | `C:\Users\777\nad-lan\nad-lan-co-il\.claude\worktrees\agent-a61b211e083144352` |
| Branch | `worktree-agent-a61b211e083144352` (based on `6e9cf930`, the design + contract commit) |
| Builder's preview (hot code) | `node scripts/had-256/local/start.mjs after` -> http://127.0.0.1:9401/post-listing/ (`?lang=en` for English) |
| Base code 6e9cf930 (before) | `node scripts/had-256/local/start.mjs before` -> http://127.0.0.1:9411/post-listing/ |
| A pinned QA snapshot | `node scripts/had-256/local/start.mjs qa <commit> <port>` (immutable git-show copy, own data, qa.a / qa.b) |
| Draft photos outside the web root | `node scripts/had-256/local/start.mjs private` -> 127.0.0.1:9431 |
| Rollback drill | `python scripts/had-256/tests/test_rollback.py` (starts and stops its own site on 127.0.0.1:9421) |
| Tests | `cd scripts/had-256/tests && python run_all.py` (or one file: `python test_media.py`), then `python make_report.py` |

## Snapshots for QA (named commits; never updated in place)

| Name | Commit | Port | Doc |
|---|---|---|---|
| slice-1 | `d2b8f349` | 9402 | `QA-SNAPSHOT.md` (restarted once after the usage-limit stop on its own unchanged data: `bind-check-qa-9402-restart.txt`) |
| snapshot 2 (P0/P1 a-d fixed) | `c2e4cd31` | 9403 | `QA-SNAPSHOT-2.md` |
| snapshot 3 (everything below) | see `QA-SNAPSHOT-3.md` | 9404 | `QA-SNAPSHOT-3.md` |
| builder's latest | see `git log` | 9401 | not for QA |
| theme bench, snapshot 3 in the real theme + plugin | `2ce0a741` | 9405 | `THEME.md` (5.10) |
| theme bench, fix candidate owner-wizard 2.0.1 | `e28df264` | 9406 | `THEME.md` (not a QA snapshot) |

Release package (main only): `RELEASE.md`, `scripts/project-stage/had256_release.py`. MySQL proof kit (open item 1):
`mysql-claim-check.php` (dry run on the SQLite bench: `mysql-claim-check.sqlite-dryrun.json`, all 44 checks pass; the
MySQL run itself is main's, once, on the live database).

## What was built

**owner-wizard.php 2.0.0** (the Code Snippet 707 "x-owner-wizard" text; the whole file is new, see "For main" below):
- The journey of the approved design v5: account (open, sign in, recovery with one neutral answer), the saved draft
  to continue (delete = WordPress trash, only after the server confirms; restore from "deleted items"), details,
  photos, preview (not public, not indexed: REST, no-store, noindex), publish, published, My listings (edit, price,
  sold / let, remove = trash and publish again), promotion switched off (no price, no checkout, no payment route).
  Hebrew RTL first, English LTR (`?lang=en`). One primary action per screen, 44 px targets, visible focus, errors
  beside the field with a linked summary, the input kept.
- The draft is a server entity owned by one user: a private `nadlan_drop` with `nl_draft_v=2` and one meta row
  `nl_draft` {rev, fields, photos (refs in order; the first is the cover), step, saved_at}. Explicit fields: deal,
  type, city, neighbourhood, rooms, size, floor, price, description, display name, phone, phone consent, owner
  statement. No street field. Saves carry the revision they started from; the server swaps the row only if it still
  holds that text (one UPDATE), else 409 with the server version: the screen shows the difference and lets the owner
  load the other version or keep this one (and go back to the one that was here).
- Honest save states: saved on this device / saving / saved in the account (with the server's time) / no connection /
  save failed + retry with a countdown / open elsewhere (conflict) / sign in again / storage blocked.
- The local queue: one key per user and draft (`nlow:v2:u<uid>:d<id>`), never another account's, nothing secret (the
  phone is not stored), storage errors shown. The 1.x `nlow-draft` text and other accounts' keys are never listed,
  read, shown, imported or deleted. A neutral line on every screen: drafts are kept per account, with a "sign in to
  another account" link.
- An account change in another tab clears this page at once (a no-data ping between tabs, and focus / visibility /
  back-forward checks that ask the server who is signed in); the signed-in page is sent `Cache-Control: no-store`.
- Publish: draft id + a client request key; a retry returns the same result (`replayed`), the same key with another
  revision is refused (409). The owner listing is built by `nl_owner_build` under x-broker-drop's lock: one post per
  drop claimed by the unique option `nl_pub_<drop>_he`, written as a non-public draft, then the status committed by
  ONE UPDATE that requires the run's own lock row (a run that lost the lock can never publish, hold or unpublish), and
  only then the public photo copies. Copy = the plain template + the owner's own words: no model call, so the preview
  is the page.
- Photos: per-file answers (413 too big, 415 not an image / HEIC this server cannot clean, 422 corrupt or cannot be
  turned upright, 401 session, 429, 5xx, timeout), retry of the failed file only, removal during upload, a refresh
  keeps what the server took. Draft photos are cleaned (EXIF / XMP / IPTC / PNG text / WebP EXIF+XMP out, orientation
  2-8 applied to the pixels by GD or Imagick, else refused), then sealed at rest (libsodium secretbox, key from the
  site's auth salt) under `uploads/nl-private/<keyed dir>/` or outside the web root with `NL_OWNER_PRIVATE_DIR`, and
  shown only to their owner through `admin-ajax.php?action=nl_owner_img`. Public copies exist only while the listing
  is published (made after the publish commit; deleted BEFORE a listing leaves `publish`, from any door).
- Quotas: abuse counters for attempts (saves 600/h, publish tries 30/h, photos 90/h, drafts 30/day, sign-up and
  recovery 5/h per address with a string identity), apart from unique publishes (8 a day, counted once per listing,
  only after it exists). A validation failure never costs a publish. The 5-active cap is kept.
- Kept: media ownership checks, `nadlan_compliance_scan` (a hit holds the listing as pending and mails the admin),
  the 410 answers of the first wizard's doors, the broker redirect (`who=broker`), the 5-active cap, sold / let.
  The 1.x `/owner/submit` now tells an open 1.x page to refresh (410) instead of creating a new drop; `/owner/build`
  still builds a 1.x drop (under the lock).
- Phone: published only with the consent box (unchecked by default). Without it the listing has no number, no
  WhatsApp and no call link (checked on the published HTML: no `wa.me`, no `tel:`).

**broker-drop.php 1.1.4** (the shared engine; small, delimited hunks, see "For main"):
build lock with fencing tokens, one claimed listing per drop and language (database-enforced), the fenced commit of
`nl_result` / `nl_state`, the photo cleaner (also used by the broker photo door for every type, HEIC excepted).

## What is real and what is stubbed

**Real**: the modules that would ship (`owner-wizard.php`, `broker-drop.php`) and their neighbours `funnel.php`,
`auth.php`, `property-owner.php`, `conversion-cta.php` (the site's floating bar `#nlcta`, real markup and CSS), inside
WordPress Playground 3.1.56, WordPress 7.1.2, PHP 8.3.33 with GD 2.3.3 (JPEG/PNG/WebP) and Imagick (no HEIC),
libsodium, SQLite, 6 PHP workers; driven over HTTP and by a real Chrome (Playwright, headless, fresh profiles).

**Stubbed by the bench** (`scripts/had-256/local/mu-plugins/nlj-bench.php`, never shipped):
the `nadlan_property` / `nadlan_professional` post types (same public args, no capability map); the plugin's own
`[nadlan_listing_wizard]`; `nadlan_compliance_scan` (rules copied from `inc/ai-features.php`); `run_wptexturize`
off (as `inc/final-hardening.php` does on the live site); no `nadlan_i18n`, so the bar reads "לפרטים נוספים" (live:
"ייעוץ חינם"); the theme is Twenty Twenty-Five, NOT the NadLan theme: **production theme integration (header, footer,
skin, the real page template of /post-listing/) is not verified on the bench**; AI off and every outbound HTTP request
from PHP blocked; mail to `wp-content/mail-sink/*.json`; synthetic accounts and listings only.

**What SQLite in Playground does not prove** (main, on MySQL, before any release): the row counts of `INSERT IGNORE`,
the conditional `UPDATE ... WHERE ... AND EXISTS (SELECT ... FROM wp_options ...)` and the compare-and-swap on MySQL
(they are standard SQL and behave the same on MySQL InnoDB, but they were run on SQLite here); lock behaviour under the
live PHP-FPM / LiteSpeed worker model; LiteSpeed page and object caching (the code purges the listing and image URLs and
reads its locks past the object cache, but no LiteSpeed was on the bench); the live theme; real outbound mail
(auth.php notes the site had no working outbound mail on 12.7.2026: recovery depends on it); the live server's GD /
Imagick (a server without either refuses rotated photos rather than storing them sideways).

## Results (summary; the full table is RESULTS.md)

Every row was run on real WordPress (Playground) unless it says otherwise; no row is marked passed on a mock.
- L08 exactly-once: AFTER, every fault proven to have fired (bench fault log or the killed answer): parallel requests
  (same key, different keys), kills at every step of both paths (the journey's `nl_owner_build` and the engine's
  `nl_drop_build` via the 1.x door), a run paused right after each check (fence) and before its write, past the TTL,
  while a second run takes over; and a stale run whose draft was moved into a hold cannot publish it. BEFORE
  (6e9cf930): the same listing sent twice = 2 drops; 4 parallel builds of one drop = 4 public listings; a crash
  between the listing row and its meta + a rebuild = a second public listing; validation failures spent the publish
  quota (the valid send got 429).
- P0 public photos (Maya R1): 19 checks, none exposes a photo before a committed publish (validation, hold, admin
  test, kills at 9 points before the commit, 3 after it, a fenced-out run), revocation on remove / hold, restore on
  publishing again, a crash between withdraw and status write leaves no public copy.
- Privacy: two accounts on one browser (B never touches A's queue or the 1.x text; recorder on every localStorage
  call), the stale tab (cleared by the ping alone while in the background, 0.02 s after focus), another account and
  anonymous against every door with real and guessed ids (72 requests, all refused, nothing leaked).
- Layout (L14): 13 screens x 5 widths x 2 languages: 1,610 controls focused, none covered by the site's floating bar or
  left off screen; 3,889 text nodes, none under 4.5:1 (3:1 large) on computed colours; no horizontal overflow, every
  control 44 px, a visible focus ring, no JavaScript error (`CONTRAST.md`).
- Rollback (L17): new code -> base code 6e9cf930 on the same data (the 1.0 tool works, the 2.0 listing renders, the 2.0
  drafts are kept, no fatal) -> new code again (the open draft resumes with its photos).
- Findings fixed along the way, on real WordPress: the publish exposed a public photo before a successful publish (P0,
  Maya R1); a held listing lost its Latin address (WordPress empties a pending post's slug for a user who cannot
  publish); on phones the site's bar lifted 150 px over the fields; browser-grey placeholders 4.41:1; failed photo tiles
  clipped their buttons at 320 px; the 1.0 page's inline script broke under wptexturize on the bench only (the live site
  turns texturize off; the bench now does too).
- BEFORE findings (6e9cf930, same bench): a corrupt JPEG is accepted and stored; recovery on wp-login.php says "There is
  no account with that username or email address" (enumeration); the text queue is one origin-wide key (another tab's
  last keystroke wins silently; photos are lost on reload); there is no English page; the same listing sent twice is two
  drops; 4 parallel builds of one drop are 4 public listings; validation failures spend the publish quota.

## Open risks and things not done (honest list)

1. **Remaining check-then-write window (L08, partial guarantee).** Exactly-once creation is enforced by the database
   (one claim row per drop and language), the status commit and `nl_result` / `nl_state` are atomic with the fence.
   The other writes of a build (title, meta, page HTML, photo copies) are check-then-write: a run that stalls longer
   than the lock TTL (420 s) right after a check and then resumes can make that ONE write on the single claimed post,
   with the values of its own (older) revision. It can never create a second listing, never change the status, never
   commit a result. A later save or publish rewrites it.
2. **Public photo revocation and caches.** Public copies are deleted before a listing leaves `publish` and the image
   URLs are purged from LiteSpeed; a CDN or a browser may still hold a copy it already fetched.
3. **Recovery mail on the live site** depends on working outbound mail (see above). Not verifiable on the bench.
4. **Theme integration**: run on 5.10 (`THEME.md`, 127.0.0.1:9405, the real themes, plugin and snippets): one H1,
   header, footer, bar and accessibility button, contrast, targets, overflow all pass; **Shift+Tab puts controls under
   the live sticky header on every width (snapshot 3 fails this)**: fixed in candidate 2.0.1 (`e28df264`), not in
   snapshot 3. Copy and ?lang=en wrapper findings are listed there for Maya and Ben.
5. **HEIC**: refused on any server whose Imagick cannot read HEIC (the bench's cannot); a real HEIC decode was not run.
6. **The phone keyboard** (L14 on a device) and Safari were not run; headless Chrome only.
7. **Snippet 699 / the broker sign-up** and the broker `/drop/<token>/` page UI were not run end to end; the broker
   REST door + the shared engine were.
8. **AI copy for owners is off in 2.0** (the preview must equal the page). If the owner wants model-written copy back,
   it should be an explicit "suggest wording" step the owner approves (decision for Ben).
9. **Draft photo storage path on the live host**: sealed at rest wherever stored; `NL_OWNER_PRIVATE_DIR` (a folder
   outside public_html) is supported and tested on the bench but not set by default (the live path is main's choice).
10. **Auth salt rotation** makes unpublished draft photos unreadable (published ones are ordinary media by then).
11. **Playground flake**: the first request after an idle spell sometimes answered `rest_no_route` for the bench's own
    test routes; the bench helper repeats that call. No product route was affected in any run.

## For main: the exact changes to reconcile with the live text

- `owner-wizard.php`: replaced as a whole (1.0.0 -> 2.0.0). Base = snippet 707 = `6e9cf930` (LF SHA-256
  `f1ce0fcc…`). Everything 1.0 did is either kept (same function names `nl_owner_pseudo`, `nl_owner_from_listing`,
  `nl_owner_rate`, `nl_owner_phone`, `nl_owner_listings`, `nl_owner_rest_photo/submit/build/listings/update`,
  `nl_owner_shortcode`, `nl_owner_css`, `nl_owner_js`, the healthcheck key `owner_wizard`) or answered honestly (410).
- `broker-drop.php`: hunks only, all marked `HAD-256` (base LF SHA-256 `1f47d450…`):
  1. `NL_DROP_VERSION` 1.1.3 -> 1.1.4;
  2. before `nl_drop_build`: the lock / fence / claim block (`NL_DROP_LOCK_TTL`, `NL_Drop_Fenced`, `nl_drop_lock_*`,
     `nl_drop_fence*`, `nl_drop_fenced_meta`, `nl_drop_claim_read`, `nl_drop_orphan`, `nl_drop_claim_post`) and the
     new `nl_drop_build` wrapper; the old body is now `nl_drop_build_locked`;
  3. in `nl_drop_build_locked`: the listing insert replaced by claim + `wp_update_post`; the twin insert replaced by
     claim + update; fence calls before meta / render; `nl_result` / `nl_state` written by `nl_drop_fenced_meta`;
     the result `state` read from the post status;
  4. `nl_drop_rest_build`: a busy answer (409) when another run holds the lock;
  5. `nl_drop_strip_gps` replaced by the cleaner block (`nl_drop_tiff_orientation`, `nl_drop_exif_orientation`,
     `nl_drop_gd_orient`, `nl_drop_reorient`, `nl_drop_jpeg_strip`, `nl_drop_png_strip`, `nl_drop_webp_strip`,
     `nl_drop_clean_image`) with `nl_drop_strip_gps` kept as a wrapper for the broker door.
  `git diff 6e9cf930 -- plugins/nadlan-config/inc/broker-drop.php` shows them exactly.
- No other plugin file changed. The bench mu-plugin, `loopback.cjs`, `start.mjs` and the tests never ship:
  `grep -rn "nlj-test\|nlj_fault\|nlj_reset\|NLJ_VARIANT" plugins/` finds nothing.

## Bench safety

- Loopback only: the Playground CLI has no bind option, so `loopback.cjs` (NODE_OPTIONS preload) pins every
  `listen()` of the bench processes to 127.0.0.1. Proofs: `bind-check-after.txt`, `bind-check-qa-9402*.txt`,
  `bind-check-qa-9403.txt` (every socket on 127.0.0.1, the LAN address refused). The very first runs on 3-4.10 (a 9455
  probe and the first 9401 run, before 01:15) were bound to all interfaces; they were stopped and no result uses them.
- No live writes, no push, no secrets, no paid AI, no real mail, synthetic data only. No firewall or system setting
  was changed.
- Full-page screenshots draw the fixed bar where it sits on the first screen, so in a tall shot it can look as if it
  covers a field further down; the elementFromPoint test (each control focused and scrolled into view) is the proof.
