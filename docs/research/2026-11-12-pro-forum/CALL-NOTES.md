# Forum video calls: build notes and the contract for the forum module (12.11.2026)

Nothing here is deployed, committed or wired yet. New files only; no existing file was edited.

## Files

| File | Bytes | What |
|---|---|---|
| plugins/nadlan-config/inc/pro-forum-call.php | 34,324 | pure functions, the switches table, LiveKit token, rooms and invites, 4 REST routes, the one-click "no more call mails" page, the page config and script tags |
| plugins/nadlan-config/assets/proforum/call.js | 31,161 | ES module: call pills, entry sheet, full-screen call, in-forum notice, the member's switches |
| plugins/nadlan-config/assets/proforum/call.css | 10,949 | scoped `.nlfc-*` |
| plugins/nadlan-config/tests-local/pro-forum-call-test.php | 10,529 | CLI test of the pure part: 85 passed, 0 failed |

Hebrew text is two bytes a character, so the byte sizes look large.

## The one line the forum module adds

At the very END of `inc/pro-forum.php` (after the line that requires `pro-forum-render.php`, so every `nlf_*` function exists):

```php
if ( file_exists( __DIR__ . '/pro-forum-call.php' ) ) { require_once __DIR__ . '/pro-forum-call.php'; }
```

Nothing else is required. The file creates its table once (`{prefix}nadlan_forum_callpref`, option `nadlan_forum_call_db`), on
`admin_init` or on the first call route. Owner switches: option `nadlan_forum_call` (`'0'` turns every route off, default on)
and `nadlan_forum_call_day_cap` (default 40).

## Buttons: the forum may print them, or not

**Without any forum change** call.js adds a "שיחת וידאו" pill (44 px, `nlf-pill nlfc-pill`) into `.nlf-acts` of:
- the newest live reply (`article#r<id>`) of every member the signed-in member may call, when he opened the discussion;
- the discussion's own card (`.nlf-op .nlf-acts`), to call the person who opened it, when he answered it.
The list comes from `window.NLFCALL.targets` (`[{with, reply, name, label}]`), computed server-side by the same predicate as the route.

**If the forum prefers to print its own buttons** (for example on a seek board card), any element with these attributes works,
and call.js then adds no pills of its own:

```html
<button type="button" class="nlf-pill" data-nlf-call="<topic id>" data-nlf-with="<member id>"
        data-nlf-name="<display name>" data-nlf-label="<trade label>">שיחת וידאו</button>
```

`data-nlf-name` / `data-nlf-label` are optional (used only when the member is not in `targets`). Print it only when
`nlfc_can_call()` says '' (or simply for the ids in `nlfc_page_targets( $topic, nlf_me() )`), else the press ends in a 400 message.

**The member's own switches** ("אפשר לפנות אליי בשיחת וידאו מתוך דיון", "לשלוח לי מייל כשמזמינים אותי לשיחה"): call.js fills any
`<div data-nlf-callpref></div>` the forum prints (for example inside `nlf_owner_box()` or the member bar). Without one, it adds a
"שיחות וידאו" link to `.nlf-mebar` that opens the two switches in a sheet. Both switches start OFF for every member.

## Forum functions this file relies on (read, never changed)

`nlf_gate_open`, `nlf_me`, `nlf_nonce_for` (header `X-NLF-Nonce`), `nlf_install`, `nlf_topic`, `nlf_t`, `nlf_members`, `nlf_author`,
`nlf_topic_url` (its `$hash` argument carries `call=<room>`), `nlf_mail`, `nlf_link_token` / `nlf_link_read` / `nlf_key`
(action `cmo` for the stop-mail link), `nlf_ip_hash`, `nlf_nocache`, `nlf_surface`, `nlf_rendering`, `$GLOBALS['nlf_topic']`,
`$GLOBALS['nlf_act_page']`, `nlf_json_script`, `nlf_ver`; REST `GET nadlan/v1/forum/state` (the page nonce) and forum.js's
delegated `[data-nlf-enter]` (the entry sheet when a visitor opens a call link before signing in).
If the forum renames any of these, the call routes answer 400 "שיחות וידאו לא זמינות כרגע" (each one is `function_exists`-checked
where the forum may be absent).

## REST (nadlan/v1/forum/call/...), all errors HTTP 400 with a Hebrew message

| Route | Body | Answer |
|---|---|---|
| POST `open` | `{topic, with}` or `{topic, with, room}` | `{room, topic, title, topic_url, with:{id,name,label}}` |
| POST `token` | `{room}` | `{url, token, identity, room, topic, title, topic_url, me, others:[{id,name,label,identity}]}` |
| GET `status` | none, or `?room=` | `{invites:[{room,topic,title,from,label,url}], pref:{video,mail}}` or `{exists, joined, title, from, mine, topic_url}` |
| POST `pref` | `{video?: 0/1, mail?: 0/1}` | `{pref, message}` |

Every route, in this order: forum gate (closed and no gate cookie and not admin = 400 "הדף לא נמצא"), the module switch, a signed-in
member (session cookie `nlf_s`), the forum's per-session nonce header, member status ok; POSTs also refuse a cross-site
`Sec-Fetch-Site` or a foreign `Origin`. No proof-of-work: a call needs a session, and the room caps below bound it.

Who may call whom (`nlfc_can_call`, tested on fixtures): the discussion is live; both people wrote in it (live posts only); one of
the two is the person who opened it (two repliers cannot call each other); the other side's status is ok and his video switch is on.
"הזמינו עוד מישהו" adds a member to an open room under the same rule (up to 4 people a room, 20 invites a day per member).

Limits (own transients `nlfc_rl_*`, separate from together.php `nltr_rl_*` and designer.php `nldsg_rl_*`): 8 new rooms a UTC day per
member, 8 per hashed IP (the forum's `nlf_ip_hash`), 40 for the whole forum. Refused requests do not count. Tokens 30 per 10 minutes
per member, status 300 an hour, switches 60 an hour, call mails at most 6 a day per receiver.

## The token source, and why it is safe

`nlfc_lk()` calls designer.php's `nadlan_dsg_call_lk()` when it is loaded, else reads together.php's settings the same way
(`nadlan_tr_opt`): a local LiveKit key if the site has one, otherwise the shared project's edge function. `nlfc_grant()` is
designer.php's `nadlan_dsg_call_grant()` request with the room `nadlan-frm-<12 a-z2-7>` instead of `nadlan-dsg-<id>`:
`HMAC-SHA256(room|identity|time)` under the stored proxy secret, role `buyer` for the opener and `friend` for the others,
8-second timeout. The edge function serves `nadlan-*` rooms only, which this name satisfies. The designer's own grant function
could not be called directly because it hard-codes the `nadlan-dsg-` prefix. The secret is read at request time inside PHP,
never printed, stored or sent to the page; the page gets only `{url, token}` for its own identity in a room it belongs to.
Nothing in this work read any key file.

## The notification and the mail

There is no in-forum notification table, so the "forum notification" is a short list per member (transient, 15 minutes, 5 at most)
that `GET call/status` returns. call.js polls it every 25 s while a forum page is visible and shows a card:
"<name · trade> מזמין אתכם לשיחת וידאו על <title>" with "כניסה לשיחה" / "לא עכשיו".
The mail goes only when the invited member switched "לשלוח לי מייל" on: subject "<name> מזמין אתכם לשיחת וידאו על <title>", the link
`/forum/<id>/[?forum=on]#call=<room>` (the room travels in the fragment, never to a server log), and a one-click stop link
`/?nlfc_stop=<signed token>` (turns the mail switch off at once). The site owner gets no mail about calls. Nothing is recorded.

## Reuse of the designer call: what blocked a clean reuse

- `joinCall(designer, opts)` cannot run without the apartment designer: both modes read `designer.store`, `designer.space`,
  `getView/setView`, `getDesign`, `toast`, `ready3d`, and mount into the designer's shadow root (`.nd`). A stub would have to fake a
  3D space and a design store, so the forum uses only `livekitTransport({url, token})` from the same file (imported on the first
  press, no static imports in call.js, so nothing else loads) and draws its own screen from the approved board `Call.dc.html`.
- `callSheet()` is reusable in shape but its words are about the apartment ("שיחת וידאו על הדירה", "מעצבים יחד"), it expects a
  container inside a shadow root for its CSS, and its sheet names the visitor (the forum already knows the name), so the forum
  draws its own entry sheet with the same behaviour (camera and mic OFF, preview and level line only when switched on).
- `nadlan_dsg_call_grant()` hard-codes `nadlan-dsg-`; replicated with `nadlan-frm-` (see above).
- Suggestion for the designer session (coordination file, not done here): a `prefix` option on the grant, and a `strings` option on
  `callSheet`, would let other pages reuse both without copying.

## What call.js draws (from Call.dc.html and the teardown take-lists)

Entry: a bottom sheet on phones (centred card on wide screens) with the request title, the other person's trade, camera and mic
switches OFF, a preview and a moving level line only after a switch is on, "השיחה לא מוקלטת", and a plain message when the browser
refuses (join without camera or mic, allow later). Call: full screen, dark job-site screen; the request pinned at the top with
the duration; the other person's initials, name and trade; self view bottom corner, mirrored only for the front camera; mic,
camera, flip (phones only, enabled when the camera is on, `facingMode` switch via the transport), more (voice-only, "not
recorded"), end set apart in red; "הקישו כדי לשמוע" when the browser blocks sound; reconnecting and left/joined notices;
56 px controls with Hebrew labels, aria-label and aria-pressed, Escape closes only the menu, Tab stays inside the dialog.
End returns to the discussion: the overlay closes, `#call=` is removed, focus returns to the button (or to the discussion's
heading); a call joined from another forum page goes to the discussion's address.

## Not built, and why

- "צלמו תמונה לבקשה" is hidden: no forum route accepts an image (BUILD-NOTES: image buttons in compose were not built). The button
  exists in the call screen and shows when `NLFCALL.photo` is set; wiring it needs a forum image route (owner decision: storage,
  moderation, privacy of a photo of someone's home).
- No ringing or push to a phone that is not on the forum: the invited member sees the notice when on a forum page, or the mail.
- No "end for everyone": with two people, leaving ends the call; the other side sees "יצא/ה מהשיחה".

## Tested here

- `php -l` both PHP files: no syntax errors. `php tests-local/pro-forum-call-test.php`: 85 passed (room and identity format,
  `nadlan-frm-` prefix, day window and keys, the 8/8/40 caps, the permission predicate on fixture discussions including pending
  replies, two repliers, video off, blocked member, hidden discussion, targets, same-site headers, Hebrew messages, mail wording,
  invites pruning, house rules: no 403, no owner mail, no recording, innerHTML only for constant icons, no emoji, no wheel/touch capture).
- `node --check call.js`: ok; importing the module in Node without a window: ok (it stays idle).

## Not tested (needs WordPress, LiveKit and two phones)

Everything touching `$wpdb`, dbDelta, transients, REST, cookies, the nonce, mail and the theme; the edge function's answer for a
`nadlan-frm-` room (it is expected to serve every `nadlan-*` room, as designer.php's comment says, but no live request was made);
the call screen in a real browser (layout at 360-390 px, iOS Safari autoplay and audio unlock, camera flip on a real phone,
permission refusal paths, reconnect), and the pills' placement inside the live forum cards. Before release: two Chromes on a
gated forum page, member A (opened a discussion) and member B (replied, switched video on), then a real phone.
