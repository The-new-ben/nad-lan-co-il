# Take list: a call where 2 to 8 people look at an apartment in 3D and move furniture together, phone first

- Inputs: `matrix.csv` (184 rows, Zoom / Meet / Teams / Webex), the earlier HAD-706 files `../../2026-11-10-apartment-designer/call/zoom-teardown.md` and `livekit-mapping.md` (LiveKit API names, limits and costs are there; not repeated here).
- Rule for every item: we take the **behaviour** a user already knows, and we rebuild it in our own words, shapes and colours. We copy no icon, string, layout grid or brand colour.
- Bar = the minimum quality line, taken from the best of the four.
- Priority: 1 = build first, 2 = next, 3 = later or optional.
- Design identity, stated per the owner's design law: palette from architectural drawing sets. Blueprint ink, a cold concrete grey, and one signal colour taken from surveying marks; no cream, brass or terracotta. Hebrew face Assistant or Heebo for the interface (both by choice for their legible Hebrew numerals and true RTL metrics), Latin IBM Plex Sans for dimensions. Not a default because the call reads as a drafting table, not a chat app. Final faces and colours belong to the Claude Design pass.

## Priority 1: the eight to build first

| # | Component | Taken from (rows) | Bar to meet | How we rebuild it, in our own words and design |
|---|---|---|---|---|
| 1 | **Join from the link in the phone browser, no app, no account** | Meet iOS Safari path, Webex Join, Zoom web app (B001, B002, B014, B016) | Meet/Webex: a guest types a name and is in after 2-3 taps | One screen in RTL Hebrew. The 3D apartment is already loaded behind a frosted panel, so the guest sees the home before any face. Fields: name (prefilled if known), mic and camera switches **off by default**, and a "כניסה לשיחה" button inside the thumb zone. Target: link to first face in **3 or fewer taps**. |
| 2 | **Preview with a live mic meter and a camera check, and a plain fix-it path when permission is blocked** | Meet green room, Teams pre-join, Webex preview (B004-B005, B008) | Meet: the mic bar moves, a test sound plays, devices can be switched | A small self tile plus a moving level line drawn like a survey measurement. If permission is denied, show a picture of the exact browser control for iOS Safari or Android Chrome and a "continue without camera" option. Never a dead end. |
| 3 | **A bottom bar on phones, with Leave set apart from mic and camera** | Meet (leave far from mic), Teams redesign, Teams mobile edges (B024-B030) | Meet: leave "away from the camera and mic"; Teams: the core trio grouped | RTL order starting at the right edge: mic, camera, **"עט" (pen)**, people, more. Leave is a separate shape at the far left edge in the signal colour, with a gap. Text labels under the icons (Hebrew), 48 px targets. Controls stay visible while someone holds the pen (no auto-hide during editing) and fade after 4 s otherwise. A tap brings them back. |
| 4 | **The pen: one holder, ask, give, take back, visible to all** | Zoom/Teams/Webex remote control (B089-B092), Teams named cursors (B095), Teams Live Share 3D example (B103) | Teams: Request, approve, Take back, Release; Zoom: one controller at a time | It is not screen control. It is shared app state: only the holder's furniture moves count. "בקשת עט" sends a request card to the holder with Give/Not now buttons that time out after 30 s (Webex rule). The holder's name rides on a coloured ring around their tile and on the moving object. The host (sales rep) can always take the pen back. LiveKit topic `pen` per livekit-mapping.md. |
| 5 | **Follow the driver, peek privately, snap back** | Teams LiveFollowMode, Zoom whiteboard Present mode (B105) | Teams: follow, private view, resync | By default everyone's 3D camera follows the pen holder. Dragging the view starts a private look, shown by a slim strip "את/ה מסתכל/ת לבד · חזרה למבט המשותף" with one tap to resync. |
| 6 | **Phone portrait layout that shares the screen between the apartment and the faces** | Webex Equal view and Focus view, Meet auto-pin of the share (B053, B069-B070) | Webex: content on top, speaker below, portrait only | The 3D apartment takes about 70% of the top. Below it, a strip of round faces: the speaker is larger, and the rest scroll sideways. Self view is the smallest tile at the strip's end, hideable (fatigue research, B172). A tap on a face swaps it into a large float for 5 s. Up to 8 people: 3-4 faces visible, the rest scroll. |
| 7 | **Reconnect that keeps the design** | Zoom quality bars, Webex rejoin, LiveKit Reconnecting/Reconnected (B124-B127) | No official timing anywhere, so set our own: banner within 1 s of Reconnecting; keep trying 30 s; then a rejoin button | A thin banner in Hebrew: "החיבור חלש, ממשיכים לנסות". The furniture state stays local. On Reconnected, pull a fresh `design-snap` so nothing is lost. Per-person signal dots on tiles in three steps. |
| 8 | **Leave versus end, and the host can hand over** | Meet "Just leave" vs "End for all", Zoom "Assign and leave", Webex successor order (B146-B149) | Zoom: pick the next host in one dialog | A guest gets one tap and a confirm. The rep gets a two-choice sheet: "לצאת, השיחה ממשיכה" or "לסיים לכולם". If the rep leaves, the pen and host role pass automatically to the designer, then the buyer (Webex-style order). The design state is saved to the apartment record, not to a call log. |

## Priority 2

| # | Component | From | Bar | Our build |
|---|---|---|---|---|
| 9 | Speaking-while-muted reminder | Webex (B128) | Reminder only after more than 60 s of silence | A small Hebrew note over the mic button: "מדבר/ת? המיקרופון כבוי". It shows once per minute at most and can be dismissed. |
| 10 | Pointer and disappearing ink on the plan or 3D | Meet disappearing ink, Teams laser, Webex arrow/laser (B094, B104) | Meet: ink fades by default | A long-press draws a fading line in the person's colour. Strokes vanish after 3 s unless "keep" is tapped. Lossy topic `pointer`. |
| 11 | Raise hand and quick reactions | Meet auto-lower, Zoom ~10 s fade (B115-B117) | The hand lowers itself on speaking | Replace "raise hand" with "**אני רוצה את העט**" (pen request = hand). Reactions are limited to the 4 that matter for a home: like, not this, question, price? |
| 12 | Waiting screen with the apartment | Zoom branded waiting room (B010) | Logo, title, text, media | While knocking, the guest sees the apartment name, floor and a slow turntable of the model. The rep admits with one tap from a top banner. |
| 13 | Invite and copy link from the call | Webex Copy meeting link, Zoom auto-copy (B021, B072) | One tap | A "הזמנה" sheet: WhatsApp share first (Israeli default, owner's WhatsApp laws apply), then copy link. Short-TTL token per invite (livekit-mapping.md). |
| 14 | Back/front camera flip to show a real room | Meet Switch camera, Webex Swap camera, Webex camera share (B041, B102) | One control | A flip control inside the camera sheet. The rep can show the real site from the back camera into a tile. |
| 15 | Audio-only and weak-phone mode | Webex low-battery suggestion, Meet On-the-Go (B132-B133) | The product suggests it | When the battery is under 20% or quality is Poor for 10 s, offer "רק קול, הדירה נשארת". Video stops, 3D sync continues. |
| 16 | Admit, remove, mute (rep only) | All four host tools (B074-B084) | Admit all, remove, mute | Rep-only menu on a tile: mute, remove, take pen. Server-side through together.php per livekit-mapping.md. |

## Priority 3

| # | Component | From | Our build |
|---|---|---|---|
| 17 | Hebrew live captions | Zoom/Meet/Teams support Hebrew (B159) | Only with the owner's word on cost (needs an agent plus STT; livekit-mapping.md). |
| 18 | Post-call one-tap rating | Teams thumbs, Duo good/bad (B150) | Thumbs up/down shown to **every** user once. On down, offer 4 reasons. No nagging (B182). |
| 19 | Save a snapshot of the design with marks | Teams snapshot, Webex save to gallery (B097) | "שמירת מצב" stores the layout plus marks to the apartment record and sends the buyer a link. |
| 20 | Gesture reactions | Webex/Meet camera gestures (B116) | Skip on phones (CPU); maybe desktop later. |

## What we explicitly do not take, and why

| Not taken | Seen in | Why not |
|---|---|---|
| Pixel remote control of someone's screen | Zoom, Teams, Webex (B089) | Desktop-only everywhere, excludes phones, and is the wrong model: everyone already runs the same 3D, so we pass state, not pixels. |
| Screen sharing as the main way to show the apartment | All four | It doubles bandwidth and freezes the 3D into a picture. Each phone renders the model itself. Screen share stays a desktop extra at most. |
| An app install, or a "use the app" push on phones | Teams (no phone browser), Zoom launch page (B001, B179) | The top complaint pattern. Our users arrive from a property page on a phone. |
| 25/49-tile galleries, Together/Immersive scenes | Zoom, Teams, Meet (B049, B063) | At 2-8 people the apartment is the star; faces are a strip. |
| Ending on a toolbar button next to mic | Zoom mobile 2025 change (B026) | It goes against the accidental-exit evidence (B171). |
| Always-on active speaker border with no off switch | Zoom (B181) | A thin speaking ring that fades is enough; ours must not flash over the model. |
| A forced post-call survey every time, or one that cannot be switched off | Teams (B151, B182) | It irritates. One quiet thumbs question, shown once. |
| Host remote-unmute of a buyer | Zoom "ask to unmute", Webex blocks (B143, B174) | A buyer must always own their mic (trust, privacy). The rep may mute, never unmute. |
| Polls, breakouts, Q&A, Slido, whiteboard apps | Zoom, Meet, Webex (B122) | Not needed for a home decision with 2-8 people. |
| Copying any vendor string, icon or colour ("Assign and leave", Meet's red handset, Teams purple) | All | The fairness declaration requires our own words and design. We keep only the behaviour. |
| A self view that is always large | All defaults | Fatigue research (B172): ours is small, movable and hideable from the first second. |
