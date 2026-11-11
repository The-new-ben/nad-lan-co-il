# Call design: "שיחת וידאו על הדירה" (the video call inside the apartment designer)

- Date: 11.11.2026. Status: design version A, waiting for the owner's choice of name and sign-off. Nothing here is built or released.
- Boards (source of truth for the look): `boards.html` in this folder, published privately at https://claude.ai/artifact/5nPXHJjrT72DFwD4gzRMZE, and as images in `boards/01-cover.png` ... `boards/12-components.png` (2640×1860 each).
- Replaces the look of the current dock in `plugins/nadlan-config/assets/designer/call.js` + `call.css` (square 52 px tiles in a top strip, one-row bar under them). Transport, LiveKit wiring and the pen/state sync stay; only the UI layer is rebuilt to this spec.
- Research inputs: `docs/research/2026-11-11-video-meeting-teardown/others/` and `.../big4/`.

## 1. Identity

**One line (as on board 1):** ink #0F2233 behind the video and the model, blueprint white and paper for panels, blueprint blue for action and live state, red only for leaving and for measurements, and six technical-pen colours, one per person. IBM Plex Sans Hebrew for the interface and IBM Plex Mono for numbers and time. Not the default because every colour and letter comes from the sheet on the drafting table (ink, paper, pen, dimension), not from a chat-app template.

Banned here (owner law 13.10.2026): cream, beige, brown, terracotta, gold; purple-blue gradients; Inter or Space Grotesk; emoji icons; rounded soft-shadow cards; near-black with one acid accent. Shapes: sharp corners, 2 px rules. The only round things are face discs (drawing "detail circles") and the speaking ring.

### Colour tokens

| Token | Hex | Use |
|---|---|---|
| `--ink` | #0F2233 | Surface behind video and 3D, header, text on paper |
| `--ink-2` | #16304A | Raised ink surface |
| `--ink-3` | #22405C | Hairlines on ink |
| `--graph` | #46596A | Secondary text on paper |
| `--mute` | #7A8B98 | Tertiary text, timestamps |
| `--sheet` | #F2F5F7 | Plan background, boards |
| `--paper` | #FFFFFF | Bar, sheets, cards, inputs |
| `--rule` | #C9D4DC | Dividers on paper |
| `--blue` | #1F5FA8 | Primary action, live dot, active toggle, focus ring |
| `--blue-2` | #D6E5F6 | Soft blue fill |
| `--red` | #B5302A | Leave / end for all / remove. Dimension lines. Nothing else |
| Live dot on ink | #5B9BE6 | The timer square and the reconnect spinner (blue lifted for contrast on ink) |

### Pen colours (one per participant, in join order)

| Order | Name | Hex |
|---|---|---|
| 1 (host) | כחול שרטוט | #1F5FA8 |
| 2 | ירוק | #1C7A4E |
| 3 | מגנטה | #B0307A |
| 4 | טורקיז | #0F7C8A |
| 5 | סגול | #5B4BB7 |
| 6 | גרפיט | #46596A |
| 7, 8 | repeat 1, 2 | same hex, the ring is dashed |

The pen colour appears in: the face-disc ring, the speaking ring, the name stamp stripe, the glow around furniture the person holds, the "X is moving" chip, the pointer and laser, the 3D view cone, the follow frame, the change list after the call. Never in buttons.

### Type

| Role | Face | Size / weight |
|---|---|---|
| Sheet title (sheets, end screen) | Plex Sans Hebrew | 20/700 (end screen 24/700) |
| Call header title | Plex Sans Hebrew | 15/600; sub line 12/400 |
| Body, list rows | Plex Sans Hebrew | 14-15/400-600 |
| Chip, toast | Plex Sans Hebrew | 13-14/600 |
| Bar label | Plex Sans Hebrew | 10.5/500 (desktop 12) |
| Name stamp | Plex Sans Hebrew | name 11/600, role 10/500; on-model tag 10.5/600 |
| Timer, dimensions, link, areas | Plex Mono | 13/500, `direction:ltr; unicode-bidi:isolate; tabular-nums` |
| Input text | Plex Sans Hebrew | 17 (stops iOS zoom) |

Spacing grid 4 · 8 · 12 · 16. Hairline 1 px, rule 2 px, focus ring 3 px blue with 2 px offset.

## 2. Phone frame (390×844 reference)

| Layer | y | Height | z-index |
|---|---|---|---|
| System status | 0 | 44 | (system) |
| Call header (ink) | 44 | 56 | 30 |
| Stage: model or plan | 100 | 634 (fills to the bar) | 0 |
| Face discs / pill | on stage | | 15 / 22 |
| Chips, inset, layout switch | on stage | | 21-22 |
| Control bar (paper) | 744 | 76 | 35 |
| Banners (reconnect, audio, weak) | top of stage | 46-60 | 36 |
| Toasts | | | 37 |
| Sheets and scrim | from bottom | | 45 / 50 |
| Home area | 810 | 34 + `env(safe-area-inset-bottom)` | |

Header: back chevron 44×44 (returns to the designer, call keeps running), title + sub line (apartment, rooms, m², floor), live box on the end side: blue square, Plex Mono timer, people icon + count. Height 56.

## 3. The three layouts and when each runs

The model never moves to make room for a face. Faces never reorder (join order). Layout switch: a 3-segment control (סיור · סידור · שיחה), 40 px tall, always in the same place on the stage edge; on desktop it sits in the header.

### A. סיור / Tour (default)
- When: on entry; while anyone leads or is followed; 5 s after the last furniture drop in B.
- Model fills the stage. Face discs float in a row at the top (inline-start), 52 px, 14 px gap, 44 px when more than 4 people; beyond 6 the row scrolls sideways with a "עוד 3" disc.
- My own disc: 40 px, draggable to any corner, collapses to a pill "אני" after 10 s, hideable from עוד.
- Follow: 3 px frame in the leader's pen colour around the stage + a tab at the bottom of the stage "עוקבים אחרי יואב | הקישו לעצור". Any orbit, pan or pinch stops following and shows the chip "חזרה ליואב" (44 px, thumb zone, bottom centre).
- Other people's 3D view cones in their colour (fill 28 %, 1.5 px edge, 18 px square at the eye point), drawn on the floor so they never hide furniture.
- Controls auto-hide after 4 s without a touch (never during a drag); one tap anywhere brings them back. Hint toast the first time: "הקישו על המסך כדי להחזיר את הכפתורים".

### B. סידור / Arrange
- When: automatically from the first touch on any furniture (mine or anyone's) until 5 s after the last drop.
- Plan fills the stage (sheet background, 50 cm grid, walls in ink, areas in mono). 3D shrinks to an inset 150×128 (about 30 %) at the bottom inline-end corner, with a swap button 30×30; tapping swaps plan and 3D.
- Faces collapse to one pill (40 px): stacked 24 px minis + "4 בשיחה · מיכל מדברת". Tap opens the faces row.
- Held furniture: fill 14 % of the holder's colour, 4 px stroke, outer glow rectangle 16 cm out, rotate handle, a 28 px face disc of the holder riding on the object, chip "דנה מזיזה את הספה". The last committed position is a dashed outline. Distances to the nearest walls in red dimension lines with mono values (1.40, 0.45).
- Refused hold: the object shakes (3 cycles, 4 px, 240 ms) and a toast "יואב מחזיק את הארון. נסו שוב בעוד רגע." No error dialog.
- "בטל את שלי" (undo mine) appears as a small toast button bottom-start after my first move; undo never removes another person's change (skipped with a toast if someone moved it since).

### C. שיחה / Talk
- When: the user taps שיחה; or automatically when nobody touched the model for 60 s and someone is speaking; and in voice-only (faces become initials).
- Top 380 px: 2×2 grid of face tiles (4 people), 2 rows stacked (2 people) with "לסדר זה לצד זה" toggle; tile speaking frame 3 px in pen colour; name stamp bottom inline-end; mute badge top inline-start.
- Bottom 254 px: the model, live, same state; label "הדגם נשמר כמו שהוא"; button "חזרה לדגם" (40 px) returns to A at the same camera.
- Voice only: 96 px detail discs with the initial in pen colour on white, speaking ring stays.

## 4. Components (sizes, states, behaviour)

### Face disc ("detail circle")
- Sizes: 28 (on a held object), 44 (5+ people), 52 (phone), 72 (desktop strip), 96 (talk, voice only).
- Ring: 2 px pen colour + 2 px ink separation. Speaking: 3 px pen colour + 3 px ink + 2 px pen colour at 55 % (pulse). Ring appears within 300 ms of speech start, fades 800 ms after silence.
- States: normal; speaking; muted (20 px white square badge, mic-off icon, ink border, bottom inline-start); camera off (white disc, initial in pen colour); weak connection (ink badge with signal icon, top inline-start, only when poor or lost); reconnecting (greyscale 75 %); host (small "מארח" tag top inline-end).
- Name tag under the disc on the model: 17 px, ink fill, 4 px stripe in pen colour on the start side.
- Tap: sheet with three choices: "לעקוב אחרי מיכל" (primary), "לקפוץ אליה פעם אחת", "תמונה גדולה" (5 s float). Long-press = big picture directly.

### Name stamp
22 px tall, 1.5 px border, 3 px pen-colour stripe at the start, two cells: name 11/600 | role 10/500. Ink version on video, paper version on paper.

### Control bar (phone)
- Paper, 2 px ink top rule, height 76 + 34 home area. RTL order from the right edge: מיקרופון, מצלמה, מעקב, הצבעה, הזמנה, עוד; then 8 px gap, 2×44 px rule, 8 px gap; then יציאה.
- Cell: at least 50×60 px, icon 24 px (2 px stroke, square caps), label 10.5/500 under it.
- States: default (ink icon on paper); off (ink fill, white icon, label changes: "מושתק", "כבויה"); active (blue fill: "עוקבים", הצבעה on); blocked (hatched, label "חסום"/"חסומה"); unread count (16 px blue square, top inline-end of עוד); mic level (3×14 px bar beside the mic, green fill to level).
- Press: ink 12 % fill, 80 ms. Focus: 3 px blue ring.
- יציאה: 56×56, red fill, white handset + label "יציאה". Guest: tap → short confirm. Host: sheet with "לצאת, השיחה ממשיכה" (sub: who becomes host) / "לסיים לכולם" (red) / "ביטול".
- Muted reminder: only after 60 s of silence while muted, when speech is detected; ink toast above the mic "אתם מושתקים. מדברים?" with "להפעיל מיקרופון" / "לא"; at most once a minute.

### עוד (more) sheet
הודעות (with unread count, saved with the design) · משתתפים · קול בלבד (switch) · החלפת מצלמה · להסתיר את התמונה שלי (switch) · בטל את שלי · host only: מי מזיז = חופשי / מודרך / הצגה; כולם אליי; סיום לכולם.

### Chips, pill, banners, toasts
- Chip: 32 px, fill pen colour, white 13/600, 24 px mini face with 2 px white ring at the start. Outline variant (white fill, 2 px pen-colour border) for "חזרה ליואב" and labels on 3D.
- Pill: 40 px, paper, 2 px ink border.
- Banners: full width at top of stage. Reconnecting = ink, 2 px blue bottom rule, spinner, mono counter. Audio unlock = blue, 60 px, centred "הקישו כדי לשמוע". Weak = paper, 2 px ink bottom rule, link "להחזיר וידאו".
- Toast: paper, 2 px ink border, 14/600; dark variant ink with white border.

### Sheets, buttons, fields
- Sheet: paper, 2 px ink top rule, padding 18/16, title 20/700, sub 14 graph.
- Button: 52 px (secondary 44), 2 px border, 16/600. Primary blue, neutral paper, dark ink, danger red.
- Field: 52 px, 2 px ink border, text 17, focus 3 px blue ring.
- Switch: 48×28, 2 px border, square knob 18; on = blue fill, knob at end.

### Pointer and laser
Long-press on the plan or on a wall in 3D. Pulse "כאן" in pen colour (dot 22 cm + rings at 44 and 70 cm on the plan), trail 10 cm wide; the trail stays while the finger is down and fades out as one 1.2 s after lift. Chip "מיכל: כאן". Listeners without a mic may point. Never saved.

### "כולם אליי" (host summons)
Card centred over a scrim: 64 px countdown ring (blue, 5 px) with mono "3", title "יואב רוצה להראות לכולם את המטבח", sub "עוברים למבט שלו בעוד 3 שניות", two equal buttons "לעבור עכשיו" / "לא עכשיו". Who declined gets a chip to join later; the host disc shows "3 צופים".

### Invite sheet
"הזמנה בוואטסאפ" (primary, first), link field in mono with an inline "העתקה" button that turns into "הועתק" for 2 s, QR 25×25 for a second phone in the same room. Link is valid for this call only. Full at 8: "השיחה מלאה, 8 מתוך 8".

### People list (host)
Rows 60 px: 40 px disc, name + role + what they do now, more button 44 px. Host actions: להשתיק, לעקוב, להוציא (inline confirm, red, "הוא יוכל לחזור רק בקישור חדש. מה שהזיז נשאר בעיצוב."). The host can mute, never unmute someone.

### Entry
- Starter: sheet over the model, 96 px self preview + live mic meter (14 bars, green to level) + "דברו, והקו זז. כך יודעים שישמעו אתכם.", name prefilled, camera and mic switches, "להתחיל שיחה", fine print "השיחה לא מוקלטת. הדפדפן יבקש רשות למצלמה ולמיקרופון רק כשתלחצו."
- Invited: tap 1 = WhatsApp link card (shows the apartment, not faces or logos); tap 2 = entry card over the live model, who is already inside, one field "איך לקרוא לך?", camera off by default, mic asked on entry, "כניסה". No device-test page, no lobby.
- Permission refused: enter as listener. Toast "נכנסת כמאזין. שומעים ורואים הכול, ואפשר להצביע ולהזיז רהיטים." + "איך לאשר מיקרופון" sheet with iPhone and Android steps, buttons "ניסיתי, לבדוק שוב" / "להמשיך כמאזין". Bar shows mic and camera blocked (hatched).

### Trouble states
| State | Trigger | UI |
|---|---|---|
| Weak connection | quality poor for 10 s | Auto voice only, white banner "החיבור חלש. עברנו לקול בלבד כדי שהשיחה תמשיך." + "להחזיר וידאו"; signal badge only on the affected disc |
| Reconnecting | `Reconnecting` event, within 1 s | Ink banner "מתחברים מחדש…" + mono counter; faces greyed; toast "הדירה ממשיכה לעבוד. השינויים שלכם יישלחו כשנחזור."; no leave/join toasts for gaps under 10 s; after 30 s "להתחבר שוב" |
| Audio blocked (iOS) | `StartAudio` needed | Blue 60 px banner "הקישו כדי לשמוע", gone after the tap |
| Low battery | below 20 %, once per call | Sheet "הסוללה ב־15%" + "לעבור לקול בלבד? כך השיחה תחזיק יותר. הדירה ממשיכה לעבוד כרגיל." / "קול בלבד" / "להמשיך עם וידאו" |

### End of call
Summary screen within 5 s: mono meta line (time, length, people), "השיחה הסתיימה. העיצוב שמור אצלכם.", before/after plan thumbnails, change list by person with pen-colour dots, pinned notes, "לשלוח את הסיכום בוואטסאפ" (primary), "להמשיך לעצב לבד", fine print "השיחה לא הוקלטה. נשמרו רק התוכנית, השינויים וההודעות." Continue alone returns to the designer at the same plan with toast "השיחה הסתיימה. כל השינויים נשמרו בעיצוב שלכם." One quiet question next day: "השיחה עזרה לכם?" with two buttons.

### Desktop 1440×900
Header 56 (title, layout switch, live box). Face strip 120 px over the centre: 72 px discs + stamps, self view 150×96 draggable in the strip corner. Centre: plan 42 % + 3D 58 %. While someone drags, a 56 px face disc rides next to the object on the plan with the chip. Side panel 340 px on the left (inline-end): tabs משתתפים / הודעות, people list, messages saved with the design, input "כתבו הודעה". Bar 80 px under the centre: mic, camera | follow, point, invite, more | leave (red, 52 px, with label). Shortcuts: M mic, V camera, F follow, Space to talk while muted.

### Timings
| Item | Value |
|---|---|
| Speaking ring appears | ≤ 300 ms |
| Controls hide | 4 s idle, never during a drag |
| Self disc collapses | 10 s |
| "Everyone to me" opt-out | 3 s |
| Laser fade | 1.2 s after lift |
| Hold answer | ≤ 200 ms; heartbeat 2 s; expires 6 s |
| B back to A | 5 s after last drop |
| A/B to C automatic | 60 s no touch + someone speaking |
| Follow lag | ≤ 150 ms on Wi-Fi; ease 0.1-0.8, snap under 2 px |
| Reconnect banner | ≤ 1 s; rejoin button after 30 s |
| Copy confirmation | 2 s |
| Reduced motion | no pulse, no shake, no ease; state changes only |

## 5. Strings (Hebrew / English)

| Key | Hebrew | English |
|---|---|---|
| product.default | שיחת וידאו על הדירה | Video call about the apartment |
| header.sub | דירת {n} חדרים · {m2} מ״ר · קומה {f} | {n}-room apartment · {m2} m² · floor {f} |
| bar.mic / muted / blocked | מיקרופון / מושתק / חסום | Mic / Muted / Blocked |
| bar.cam / off / blocked | מצלמה / כבויה / חסומה | Camera / Off / Blocked |
| bar.follow / on | מעקב / עוקבים | Follow / Following |
| bar.point | הצבעה | Point |
| bar.invite | הזמנה | Invite |
| bar.more | עוד | More |
| bar.leave | יציאה | Leave |
| layout.tour / arrange / talk | סיור / סידור / שיחה | Tour / Arrange / Talk |
| follow.frame | עוקבים אחרי {name} · הקישו לעצור | Following {name} · tap to stop |
| follow.back | חזרה ל{name} | Back to {name} |
| follow.sheet | לעקוב אחרי {name} / לקפוץ אליה פעם אחת / תמונה גדולה | Follow {name} / Jump to her once / Large picture |
| hold.chip | {name} מזיז/ה את {object} | {name} is moving the {object} |
| hold.refused | {name} מחזיק/ה את {object}. נסו שוב בעוד רגע. | {name} is holding the {object}. Try again in a moment. |
| undo.mine | בטל את שלי | Undo mine |
| pill.people | {n} בשיחה · {name} מדבר/ת | {n} in the call · {name} speaking |
| point.chip | {name}: כאן | {name}: here |
| point.hint | לחיצה ארוכה על התוכנית או על קיר מצביעה. הקו נעלם לבד. | Long-press the plan or a wall to point. The line fades by itself. |
| summon.title | {name} רוצה להראות לכולם את {room} | {name} wants to show everyone the {room} |
| summon.sub | עוברים למבט שלו בעוד {s} שניות | Switching to his view in {s} seconds |
| summon.go / no | לעבור עכשיו / לא עכשיו | Go now / Not now |
| muted.nudge | אתם מושתקים. מדברים? | You're muted. Talking? |
| muted.on / no | להפעיל מיקרופון / לא | Turn mic on / No |
| controls.hint | הקישו על המסך כדי להחזיר את הכפתורים | Tap the screen to bring the buttons back |
| start.title | שיחת וידאו על הדירה | Video call about the apartment |
| start.sub | מזמינים את מי שצריך ומעצבים יחד את דירת {n} החדרים. כולם רואים את אותה תוכנית בזמן אמת. | Invite whoever you need and design the {n}-room apartment together. Everyone sees the same plan live. |
| start.meter | דברו, והקו זז. כך יודעים שישמעו אתכם. | Speak and the line moves. That's how you know they'll hear you. |
| start.name | איך לקרוא לך? | What should we call you? |
| start.go | להתחיל שיחה | Start the call |
| start.fine | השיחה לא מוקלטת. הדפדפן יבקש רשות למצלמה ולמיקרופון רק כשתלחצו. | The call is not recorded. The browser asks for camera and mic only when you tap. |
| join.title | להצטרף לשיחה על הדירה | Join the call about the apartment |
| join.sub | {host} מזמין אותך. נכנסים עם מצלמה כבויה, ומפעילים כשרוצים. | {host} invited you. You join with the camera off and turn it on when you like. |
| join.inside | {a} ו{b} כבר בפנים | {a} and {b} are already inside |
| join.go | כניסה | Join |
| listen.toast | נכנסת כמאזין. שומעים ורואים הכול, ואפשר להצביע ולהזיז רהיטים. | You joined as a listener. You hear and see everything, and you can point and move furniture. |
| perm.title | לאשר מיקרופון בטלפון | Allow the microphone on your phone |
| perm.ios | לוחצים על Aא בשורת הכתובת, הגדרות האתר, מיקרופון: לאפשר. | Tap Aa in the address bar, Website settings, Microphone: Allow. |
| perm.android | לוחצים על המנעול ליד הכתובת, הרשאות, מיקרופון: לאפשר. | Tap the lock next to the address, Permissions, Microphone: Allow. |
| perm.retry / listen | ניסיתי, לבדוק שוב / להמשיך כמאזין | I tried, check again / Continue as a listener |
| invite.title | להזמין לשיחה | Invite to the call |
| invite.sub | מי שמקבל את הקישור נכנס מהדפדפן, בלי הרשמה. הקישור עובד רק לשיחה הזאת. | Whoever gets the link joins from the browser, no sign-up. The link works for this call only. |
| invite.wa | הזמנה בוואטסאפ | Invite on WhatsApp |
| invite.copy / copied | העתקה / הועתק | Copy / Copied |
| invite.qr | טלפון שני באותו חדר | A second phone in the same room |
| invite.msg | {host} מזמין אותך לשיחת וידאו על דירת {n} חדרים בקומה {f}. רואים את הדירה ומעצבים יחד, בדפדפן, בלי הרשמה. {url} | {host} invites you to a video call about a {n}-room apartment on floor {f}. See the apartment and design together, in the browser, no sign-up. {url} |
| invite.full | השיחה מלאה, 8 מתוך 8 | The call is full, 8 of 8 |
| people.title | בשיחה | In the call |
| people.remove.q | להוציא את {name} מהשיחה? | Remove {name} from the call? |
| people.remove.sub | הוא יוכל לחזור רק בקישור חדש. מה שהזיז נשאר בעיצוב. | He can only come back with a new link. What he moved stays in the design. |
| people.remove / mute / follow | להוציא / להשתיק / לעקוב | Remove / Mute / Follow |
| more.chat | הודעות | Messages |
| more.chat.sub | נשמרות עם העיצוב | Saved with the design |
| more.voice | קול בלבד | Voice only |
| more.flip | החלפת מצלמה | Switch camera |
| more.hideself | להסתיר את התמונה שלי | Hide my picture |
| more.mode | מי מזיז: חופשי · מודרך · הצגה | Who moves: Free · Guided · Show |
| weak.banner | החיבור חלש. עברנו לקול בלבד כדי שהשיחה תמשיך. | The connection is weak. We switched to voice only so the call continues. |
| weak.video | להחזיר וידאו | Bring video back |
| reconnect.banner | מתחברים מחדש… | Reconnecting… |
| reconnect.toast | הדירה ממשיכה לעבוד. השינויים שלכם יישלחו כשנחזור. | The apartment keeps working. Your changes will be sent when we're back. |
| reconnect.retry | להתחבר שוב | Reconnect |
| audio.unlock | הקישו כדי לשמוע | Tap to hear |
| battery.title | הסוללה ב־{p}% | Battery at {p}% |
| battery.sub | לעבור לקול בלבד? כך השיחה תחזיק יותר. הדירה ממשיכה לעבוד כרגיל. | Switch to voice only? The call will last longer. The apartment keeps working as usual. |
| battery.voice / keep | קול בלבד / להמשיך עם וידאו | Voice only / Keep video |
| leave.host.title | לצאת מהשיחה? | Leave the call? |
| leave.host.sub | אתם המארחים. אפשר לצאת ולתת לאחרים להמשיך, או לסיים לכולם. | You're the host. You can leave and let the others continue, or end it for everyone. |
| leave.keep | לצאת, השיחה ממשיכה | Leave, the call continues |
| leave.keep.sub | {name} תהיה המארחת | {name} becomes the host |
| leave.end | לסיים לכולם | End for everyone |
| leave.cancel | ביטול | Cancel |
| end.title | השיחה הסתיימה. העיצוב שמור אצלכם. | The call has ended. Your design is saved. |
| end.before / after | לפני / אחרי | Before / After |
| end.share | לשלוח את הסיכום בוואטסאפ | Send the summary on WhatsApp |
| end.alone | להמשיך לעצב לבד | Keep designing on your own |
| end.fine | השיחה לא הוקלטה. נשמרו רק התוכנית, השינויים וההודעות. | The call was not recorded. Only the plan, the changes and the messages were saved. |
| end.toast | השיחה הסתיימה. כל השינויים נשמרו בעיצוב שלכם. | The call has ended. All changes were saved to your design. |
| end.ask | השיחה עזרה לכם? | Did the call help you? |
| model.kept | הדגם נשמר כמו שהוא | The model is kept as it is |
| model.back | חזרה לדגם | Back to the model |
| desk.chat.input | כתבו הודעה | Write a message |

Hebrew copy rules: no em dash, no exclamation marks, no technical words, no other products' names except WhatsApp as the share channel. Gendered verbs follow the participant's name where known; otherwise use the plural.

## 6. What we took from the research and how we rebuilt it (fairness declaration)

We took behaviours users already know. No icon, string, colour, layout grid or name was copied. All icons are drawn by us (2 px square-cap line set), all words are ours in Hebrew, all colours come from the drafting identity above.

| Component | Pattern source in the research | What is different here |
|---|---|---|
| Two taps from WhatsApp to inside | FaceTime web, WhatsApp call links, Meet iOS Safari path (others take-list 1; big4 B001, B002) | Entry card sits over the live apartment model, not a camera page; one field; camera off by default |
| Name only, no account | Jitsi, FaceTime web, Whereby (others 2; big4 B002) | "איך לקרוא לך?" prefilled; no email check, no "unverified" label |
| Preview with a live mic meter | Meet green room, Teams pre-join, Webex preview (big4 B004-B005) | Inside the start sheet, not a separate page; 14-bar line, plain sentence instead of a test sound |
| Join as listener when permission is refused | Whereby `deny_device_permission` event (others 4; big4 B008) | Full listener can still point and move furniture; exact iPhone and Android steps; never a dead end |
| Audio unlock | LiveKit `StartAudio` (others 3) | Full-width blue strip "הקישו כדי לשמוע" |
| Bottom bar with leave separated | Meet leave far from mic, Teams redesign (big4 B024-B030, difference 1) | Mirrored RTL order (none of the four has an RTL bar, big4 C); rule + gap before a red square leave; text label under every icon |
| Controls hide and return on tap | All four on phones (big4 B028) | 4 s, never during a drag, first-time hint |
| Small, movable, hideable self view | Whereby `floatSelf`/`autoHideSelfView`, fatigue research (others; big4 B056-B057, B172) | Self is a 40 px disc that collapses to "אני" after 10 s |
| Speaking ring, no reordering | WhatsApp, Pitch pulse, LiveKit `useVisualStableUpdate` (others 6) | Ring in the person's pen colour as a drawing "detail circle"; join order fixed |
| Round faces over content | Around floating heads, Pitch, WhatsApp PiP (others phone-layouts) | Three named layouts A/B/C with automatic switching rules; the model never yields |
| Portrait split for decisions | Webex Equal view (big4 difference 2) | Layout C: faces top, live model bottom with "חזרה לדגם" |
| Follow with frame, stop on touch | Figma, tldraw, Pitch, Onshape, Teams LiveFollowMode (others 8, 16-20; big4 difference 3) | Frame + bottom tab in the leader's pen colour; "חזרה ליואב" chip; camera copied, my field of view kept |
| Host summons everyone with opt-out | Figma spotlight, Miro, Butter (others 9, 21) | "כולם אליי" with a 3 s countdown ring and two equal buttons; decliners get a join-later chip |
| Soft hold + glow + "X is moving" | Liveblocks presence and typing flag (others 10; multiplayer 7-9) | Self-releasing hold on 3D furniture (2 s heartbeat, 6 s expiry) designed by us; shake on refusal; holder's face rides the object |
| Local edits win until confirmed | Figma (others 11) | Engine rule, unchanged visually: the sofa never jumps under the finger |
| Per-person undo | Figma, tldraw (others 13) | "בטל את שלי" |
| Laser that fades | tldraw laser, Meet disappearing ink (others 17, 25; big4 difference 5) | Long-press on plan or wall, "כאן" pulse in pen colour, 1.2 s fade, listeners may point |
| View cones in 3D | Spline viewing position (others 18, 27) | Floor cone in pen colour that never hides furniture |
| Control modes | 3DVista modes (others 19, 28) | Our names: חופשי · מודרך · הצגה, host only, inside עוד |
| Invite during the call | FaceTime Share Link, Webex copy link (others 14; big4 13) | WhatsApp first with a prewritten Hebrew message, inline copy confirmation, QR for a second phone in the same room |
| Reconnect keeps the model | LiveKit Reconnecting/Reconnected, Figma replay (others 15; big4 7) | Banner within 1 s, model stays usable, changes queued, rejoin after 30 s |
| Weak network and battery | Webex low-battery and audio-only, Zoom bars (big4 difference 10) | Act first (auto voice only) with one tap back; battery offer once per call |
| Muted reminder | Webex 60 s rule (big4 difference 7) | Same rule, our wording, once a minute at most |
| Leave vs end for all, host handover | Meet, Zoom assign-and-leave, Webex successor order (big4 8, difference 8) | Two-choice sheet with the next host named (designer, then buyer) |
| Chat saved with the design | LiveKit chat is not persisted (others 22) | Messages live in the design file; late joiners see history |
| After-call summary | Slack huddle notes (others 21) | Before/after plans, changes by person in pen colours, WhatsApp share, continue alone |
| Connection badge only when poor | LiveKit `data-lk-quality` (others 23) | Badge on the disc only when poor or lost |

Not taken: equal-tile grids as default, device-test pages, lobby for normal calls, recording by default, app-install pushes, screen share on phones, hard locks, raise hand and breakouts, host remote-unmute, vendor names ("Spotlight", "Huddle", "Party mode", "Campfire") and their icons or colours.

## 7. Open for the owner
1. The product name: שולחן משותף / בדירה יחד / חדר תכנון (default until then: שיחת וידאו על הדירה).
2. Whether layout C may switch on by itself after 60 s idle, or only by hand.
3. Host order when the rep leaves (designer then buyer is proposed).
4. The one quiet "did it help" question the next day: yes or no.
