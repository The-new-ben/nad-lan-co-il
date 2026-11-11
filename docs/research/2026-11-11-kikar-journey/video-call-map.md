# Kikar video call: how a tap becomes a room today (map for "tap opens live video at once")

11.11.2026, read-only research. Repo `C:\Users\777\nad-lan\nad-lan-co-il`, plugin `plugins/nadlan-config` (paths below are relative to the plugin unless they start with `docs/` or `scripts/`). Live version at research time: **1.72.656** (`/wp-json/nadlan/v1/health`).

Evidence classes: **live** = fetched from nad-lan.co.il now; **repo** = read in the repo file; **inferred** = reasoned from code, not run.

## 0. Repo vs live

| File | Repo vs live | How checked |
|---|---|---|
| `assets/project-stage/world/showroom.js` | identical | MD5 of live file = repo (live) |
| `assets/project-stage/world/cockpit.js` | identical | MD5 (live) |
| `assets/together/together.js`, `together.css` | identical | MD5 (live) |
| `inc/together.php` | **repo is behind live** | repo last commit 9c8b22c8 (28.9, 1.72.334); live mints tokens through the Supabase proxy since 1.72.463 (memory `nadlan-ashira-meeting-2026-10.md:53`, `docs/coordination/claude-codex.md:4373`). The proxy code is not in the repo. Live PHP was not read (that needs a bridge snippet, i.e. a write). |
| `assets/designer/call.js`, `call.css` | **not live** (HTTP 404) | curl (live). Repo has the committed file (06a66d68) plus uncommitted edits by another session (`git status`: call.js, call.css, studio.js, strings.js, inc/designer.php modified). |
| `/designer/call` REST routes | **not live** | `/wp-json/nadlan/v1` route index lists only `designer/save` and `designer/design/<id>` (live) |

Live facts:
- `GET /wp-json/nadlan/v1/room/available` → `{"ok":true,"now":false}`, header `Cache-Control: no-store` (live).
- Kikar page `https://nad-lan.co.il/projects/hamedina/?room=<dummy id>` prints `#nltg-root` cfg: `post: 8113, canRep: false, repNow: false, lk: true, lkLib: livekit-client@2.22.3` (live; a GET of HTML only, no room created). So LiveKit video is ON on live; only the "rep available" box is off.
- The Kikar page has one `id="nlsch"` (the booking band) and prints the `avail` URL into the cockpit config (live).

## 1. The TogetherRoom (inc/together.php, repo copy)

**Settings / options (names only):**
- `nadlan_tr_lk_url`, `nadlan_tr_lk_key`, `nadlan_tr_lk_secret` (direct LiveKit, together.php:38-48, saved at :752-759).
- `nadlan_tr_rep_now` = the wp-admin box "נציג זמין עכשיו" (Settings > חדר צפייה משותף), read by `nadlan_tr_rep_now()` together.php:50-52, saved :760, checkbox :774.
- `nadlan_tr_retention` (days, default 30) :53-58, :761-762.
- **Live only (not in repo):** `nadlan_tr_lk_proxy` (the Supabase function URL) and `nadlan_tr_lk_proxy_secret` (HMAC shared secret). Written by `scripts/together/wire_livekit.py:6, 42-43`. Function: `nadlan-room-token` in the courtai Supabase project (`scripts/together/wire_livekit.py:12-14`; source copy `scripts/together/edge/nadlan-room-token/index.ts`). It takes `{room, identity, role, name, ts, sig}`, checks HMAC over `room|identity|ts` within 5 minutes (index.ts:35-38), allows rooms matching `^nadlan-[a-z0-9-]{4,80}$` and roles `rep, buyer, partner, friend, designer, engineer, lawyer` only (index.ts:12, :36), returns `{url, token}` with a 2 h TTL (index.ts:39-41). The live `nadlan_tr_lk_ready()` evidently counts the proxy as "ready" (live cfg shows `lk:true`), but its exact code is unseen.

**How a visitor opens a room:**
1. A link to the project page with `?room=new` (built by the showroom/cockpit, see section 3, or the hero chooser together.php:720).
2. `nadlan_tr_request()` (:618-632) accepts `new` or a 12-char id only on a stage page; then `together.css` (:647-650) and `#nltg-root` cfg + `together.js` (:653-676) are printed.
3. `together.js` `boot()` (together.js:434-450): `?room=new` → `createRoom()` (:452-462) → `POST /nadlan/v1/room {post}`.
4. `POST /room` (together.php:365-391): project must be a published stage project (:372, `nadlan_tr_project_ok` :130-142); **visitor refused with 403 `no_rep` unless `nadlan_tr_rep_now()`** (:373); rate limit **4 rooms/hour/IP for visitors, 60 for reps** (:374, `nadlan_tr_rl` :165-175, fixed window transient keyed by IP); creates private post `nadlan_room` (:381-385); live transient `nltr_l_<room>` for 6 h idle (:386, :160-163); fires `do_action('nadlan_together_room_created', $room, $pid, 'rep'|'buyer')` (:387); returns `{room, join_url, file_url}` (:389).
5. On `no_rep`, together.js shows `showNotice(e_no_rep, withBook)` (together.js:455, :474-487): "אין כרגע נציג זמין…" + "לתאם מועד" (leave to `#nlsch`) + WhatsApp + back.
6. Otherwise `showJoin()` (together.js:528-575): name (required), role radio, camera/mic checkboxes (only when `CFG.lk`), the consent line, then `POST /room/token`.
7. `POST /room/token` (together.php:394-450): rate limit 30 per 10 min per IP (:401); role `rep` needs `edit_posts` (:407); name required, max 40 chars (:408-410); a closed room (no live transient) is reopened only by a rep, a visitor gets 410 `closed` (:411-415); max 12 people seen in the last minute (:426-427); returns `mode:'livekit'` + `url` + `token` (repo: signed locally by `nadlan_tr_lk_token` :282-296 as room `nadlan-<id>`; live: via the Supabase proxy) or `mode:'fallback'` (:441-447).
8. `enter()` (together.js:545-565) loads livekit-client from the CDN only now and connects (`LiveKitTransport` :1640ff), falling back to REST polling on failure (:561, :1670).

**`/room/available`** (together.php:593-601): public GET, returns `now = nadlan_tr_rep_now()` only, `no-store`. Nothing else (no presence, no hours).

## 2. `nadlan_together_room_created` and the owner mail

- Fires once at together.php:387 with `($room, $pid, $by)`. **It does not pass the join URL**; listeners rebuild it from the permalink.
- Listener (HAD-712, 1.72.643): inc/project-stage.php:2848-2862. Runs only for `$by === 'buyer'` and when `nadlan_omx_send` exists (:2852). Builds `get_permalink($pid)` + `?room=<id>` (:2855).
  - Subject: `שיחת וידאו עכשיו · <project title> · מבקר מחכה בחדר` (:2856).
  - Body (HTML, RTL): "a visitor opened a video room on <project>", a button "להיכנס לשיחה" with the join link, and a line that the link opens as the representative when signed in (:2857-2859); plain-text twin with the link (:2860).
  - Sent by `nadlan_omx_send($subj, $html, $text, 'room')` (:2861) → inc/owner-mail.php:267-276: recipient defaults to the site admin address option (`admin_email`), `wp_mail` HTML, header `X-NadLan-Mail: owner-room`, logged to option `nadlan_omx_log` (:277-281). No visitor name or contact in the mail.
- Today this mail can only fire while the box is ticked, because a visitor cannot create a room otherwise (together.php:373).

## 3. The Kikar showroom / cockpit call button today

**Showroom** (`assets/project-stage/world/showroom.js`, mounted by journey.js on Kikar):
- `callRow()` showroom.js:224-227: `CK.availNow` true → link `<path>?room=new`; else `#nlsch`. Label "שיחת וידאו עם נציג".
- Printed in the row under the map (:246). At mount it fetches `CK.avail` (= `/room/available`, set in inc/project-stage.php:1188) and, on `now === true`, re-renders the row with "שיחת וידאו עכשיו, עם נציג" (:256).
- Click: only analytics `showroom_call` (:218); the browser follows the href. So **available=false → jump to the booking band `#nlsch`; available=true → full page load of `?room=new` → TogetherRoom**.

**Cockpit** (`assets/project-stage/world/cockpit.js`, the apartment screen):
- `askAvail()` cockpit.js:56-60 fetches once per page (on `show()`, :270).
- `paintBar()` :245-251: `avail` → `?room=new` keeping `#dira=…`, label "שיחת וידאו עכשיו, על הדירה"; else `#nlsch`, label "שיחת וידאו על הדירה".
- Click handler :313: `avail` false → `preventDefault`, close the cockpit, smooth-scroll to `#nlsch`; true → navigation to `?room=new`.

**Which UI opens:** the TogetherRoom (`assets/together/together.js` + `.css`), full screen over the page. Not the designer's call.js. On Kikar there is no `bridge.js` (inc/project-stage.php:1049 comment, :1597 early return for `world`), so `window.__nlpsStage` is absent: the room should give video + notes but no shared 3D view (inferred, also noted in `docs/research/2026-11-11-kikar-journey/inventory-commerce-call.md:27-30`).

**Waiting state inside the room:** with LiveKit on (live), `renderTiles()` hides `UI.peopleBox` (together.js:729-730), so the "הנציג עוד לא בחדר" line and the WhatsApp button (:767-770) are shown **only in fallback mode**. A LiveKit visitor waiting alone sees just his own tile, no "waiting" message, and no timeout (inferred from code). There is no timer anywhere that offers booking after a delay.

**Rep side:** the owner opens the mail link signed in. `showJoin()` preselects role `rep` only when `CFG.canRep && ST.created` (together.js:532); a rep arriving from the mail has `ST.created = false`, so the radio defaults to **buyer** unless a saved role exists. He must tap "נציג" by hand (inferred from code; the mail text promises "opens as the representative").

## 4. HAD-706: the designer call (assets/designer/call.js)

What it is (call.js:1-20): a video call module for the apartment designer: tiles, mic/camera/flip/screen share, an "invite people" panel with copy link + WhatsApp (call.js:385-420), chat, raised hand, pointer, "follow me", and design sync over the LiveKit data channel. A line "השיחה לא מוקלטת" (`noRec`, call.js:52, shown in the dock :147). Layout: on phones a strip above the designer, on wide screens a side column (`layout()` :174-180).

Exports:
- `joinCall(designer, opts)` :113 — **requires a mounted designer** (`designer.store`, a shadow root containing `.nd`, :119-121). Not usable without the designer.
- `livekitTransport({url, token})` :617 — generic LiveKit transport (loads `livekit-client@2.22.3`, :22, :635).
- `callSheet(container, {mode:'start'|'join', onGo, onClose, lang})` :727 — the start/join card: name field, one big button, "camera and mic open only after you allow them", error strings incl. `off`, `full`, `gone`, `rate`, and a waiting line `empty` "עוד אין אף אחד בשיחה…" (:711-725). Needs a container inside a shadow root for its CSS (`ensureCss` :104-109 loads `call.css` next to the module).
- `receivePlan(tr, o)` :771 — designer-specific (the apartment plan from the people in the call).
- No globals; ES module only. Strings: Hebrew and English only (no fr/ru/ar), unlike together.js (5 languages).

How it is mounted / connected: `assets/designer/studio.js:55-135` imports `./call.js` on demand; rooms and tokens come from **its own** routes `POST /nadlan/v1/designer/call` and `/designer/call/token` (inc/designer.php:575-745), **not** from the TogetherRoom routes. Designer rooms are transients `nldsg_call_<id>` (:617, :680), LiveKit room `nadlan-dsg-<id>` (:696), roles `host`/`guest` (:717), max 8 people (:726), rate 6 rooms/hour/IP + daily cap option `nadlan_designer_call_day_cap` default 80 (:671-676), token 20 per 10 min (:710). Opening a room mails the owner via `nadlan_dsg_call_mail` (:648-663) with the typed name and the link.

Risks for reuse:
- inc/designer.php signs tokens locally with `nadlan_tr_opt('lk_key'/'lk_secret')` (:593-599, :686-700). On live, LiveKit runs through the Supabase proxy; if the direct key/secret options are empty there, the designer call answers `off` or signs an unusable token once deployed (inferred; live option values unseen). And the proxy rejects roles `host`/`guest` (edge index.ts:12, :36).
- Evidence: `docs/design-lab/apartment-designer/call-evidence/receipt.json` — 35 passed, 0 failed, **transport "mock (BroadcastChannel, one browser)"**, 11.11.2026 21:11 UTC; screenshots c1-c9 in the same folder. Commit message 06a66d68: "proven only on the mock". Not proven on real LiveKit, not live.

Verdict: from the showroom, reuse is realistic only for `callSheet` (the start card look) and `livekitTransport`; `joinCall` is tied to the designer. The TogetherRoom is already live with real LiveKit on Kikar and is the shorter path.

## 5. What blocks "a visitor's tap always opens a room"

1. **PHP availability gate**: together.php:373 (`no_rep` 403 unless `nadlan_tr_rep_now`). Box is off on live (`now:false`).
2. **JS gate**: showroom.js:225 and cockpit.js:247/:313 send to `#nlsch` unless `/room/available` says `now:true`; the hero chooser together.php:736 likewise.
3. **Rate limits**: 4 visitor rooms/hour/IP (together.php:374), 30 tokens/10 min/IP (:401), 12 people/room (:427). No daily site-wide cap on visitor rooms (the designer has one, designer.php:672-676). Every visitor room = one `nadlan_room` post + one owner mail, so opening the gate needs a cap.
4. **Name required** before entering (server together.php:408-410, client together.js:556): the join card is one more step; it also carries the consent line and is the user gesture for camera/mic permission, so it should stay but can be prefilled.
5. **Privacy/consent text in code**: together.js:49 (+ en :90 etc.) "not recorded, notes kept in the apartment file, NadLan team, independent, not on behalf of the developer, changes subject to developer approval" shown on the join card (:551). Header comment together.php:26-27 fixes these words. Camera/mic are opt-in checkboxes (:549-550). Lead-form privacy obligations (memory `nadlan-lead-privacy-obligations.md`) apply if a "leave a time" form collects a phone; the existing booking band `#nlsch` (inc/scheduler.php) already handles that.
6. **Rep reach**: mail only, to the admin address; it fires only for buyer rooms (project-stage.php:2852). No push/WhatsApp/SMS channel. The rep must be signed in on the device that opens the link, and must switch the role radio to "נציג" (together.js:532).
7. **No waiting UX in LiveKit mode** (together.js:729-730) and no timeout.
8. **Live together.php is not in the repo**: any PHP change must start from the live file (pull via the bridge, back up, hash), or the proxy token path will be lost.

## Minimal change for: tap opens a room, advisor gets the link, after ~1 minute offer to leave a time

Scope to Kikar first (project `post 8113`, dir `hamedina`) so Rainbow, DUO, Ashira and the hero chooser keep today's behaviour.

**PHP, inc/together.php (pull the LIVE file first; line numbers are the repo's):**
1. `POST /room` callback, line 373: replace `if ( ! $rep && ! nadlan_tr_rep_now() )` with a gate that also lets visitors in when the project is open for instant calls, e.g. new helper `nadlan_tr_open_now( $pid )` = `nadlan_tr_rep_now() || in_array( post_name, (array) get_option( 'nadlan_tr_open_projects', array( 'hamedina' ) ) )`.
2. Same callback, after line 374: add a site-wide daily cap for visitor rooms (copy designer.php:672-676: transient `nltr_day_<Ymd>`, option `nadlan_tr_day_cap`, default ~40) so the open gate cannot flood posts and mails.
3. `/room/available`, line 597: accept `?post=<id>` and return `now` = `nadlan_tr_open_now( $pid )` (keep `no-store`). With no `post` it stays `nadlan_tr_rep_now()`, so the hero chooser (:709, :736) on other projects is unchanged.
4. Line 387: pass the join URL to listeners: `do_action( 'nadlan_together_room_created', $room, $pid, $by, add_query_arg( 'room', $room, get_permalink( $pid ) ) )` (optional; project-stage.php:2855 already rebuilds it).

**JS, showroom and cockpit (repo = live):**
5. inc/project-stage.php:1188: append `?post=<id>` to the `avail` URL (`add_query_arg( 'post', $id, rest_url( 'nadlan/v1/room/available' ) )`). Then showroom.js:256 and cockpit.js:56-60 get `now:true` on Kikar and the existing code builds `?room=new` (showroom.js:225, cockpit.js:247) with no further JS change. (Alternative without PHP step 3: make `callRow()` showroom.js:224-227 and `paintBar()` cockpit.js:245-247 always use `?room=new`, and drop the `!avail` branch at cockpit.js:313.)

**JS, together.js (repo = live):**
6. `showJoin()` line 532: default role `rep` whenever `CFG.canRep` (not only `ST.created`), so the owner opening the mail link signed in enters as the representative in one tap. Optionally prefill the visitor's name field (:533-534) so the card is consent + one button.
7. `enter()` after the transport starts (~line 565): for a non-rep who created the room (`ST.created`), start a 60 s timer; on expiry, if no rep is present (LiveKit: `T.peopleList().some(p => p.role === 'rep')`; fallback: `ST.people.some(p => p.role === 'rep' && p.on)`, as at :767), show a small card reusing `showNotice`'s parts (:474-487): "הנציג עוד לא הגיע. אפשר להמשיך לחכות, או לקבוע זמן" with buttons "לתאם מועד" → `leave(true, '#nlsch')` (:1510), WhatsApp with `joinUrl()` (:405, :770), and "להמשיך לחכות" (closes the card). Cancel the timer when a rep joins. Add the strings in all five language blocks (next to `waitRep` at :52, :93, :134, :175, :216).
8. Also show the "waiting for the representative" line in LiveKit mode (today hidden by :729-730), e.g. as an overlay on the visitor's own tile until a rep tile appears.

**Owner notice (inc/project-stage.php:2851-2862):** already sends the link at once for buyer rooms; no change needed beyond an optional "the visitor will be offered a booking after one minute" line. Note it goes to the admin e-mail only.

**Release checks:** live room create on Kikar from a phone (visitor) + owner joining from the mail signed in; `/room/available?post=8113` → `now:true`, without `post` → unchanged; Rainbow/H-Infinity spot-check; source_audit before/after; content_first_check on Kikar.
