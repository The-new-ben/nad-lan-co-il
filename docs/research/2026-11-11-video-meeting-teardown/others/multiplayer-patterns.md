# Co-editing patterns: who does each one best, and what fits dragging furniture on a phone

Retrieved 2026-11-11, 21:05-21:27 UTC. Each pattern names the best example found and its source. The full source URL and retrieval time are in `matrix.csv` (area "5 Presence and co-editing"). Marks: [DOC] official docs, [VC] official company blog or marketing, [IND] independent source, [OWN] my own knowledge without a source today. "Fit" rates the pattern for our case: 2 to 8 people, a phone held upright, a plan view and a 3D view, furniture moved by touch.

| # | Pattern | Best example (source) | How it works | Fit for us |
|---|---|---|---|---|
| 1 | Pointer with name and colour | Google Docs [IND], tldraw [DOC], Figma [VC] | Cursor in the person's colour, with their name on it | **Must.** On a phone there is no hover, so show the last touch point for about 2 s and the dragged object. |
| 2 | Pointer coordinates in document space | Liveblocks: percentages of the container [DOC] | Positions survive different screen sizes | **Must.** Send plan coordinates in cm, never screen pixels. |
| 3 | Smooth remote motion | Liveblocks: spring interpolation [DOC] | Smooth on screen even when updates arrive slowly | **Must.** Updates at 15-20 Hz, drawn at 60 fps. |
| 4 | Fast path for pointers, safe path for commits | Canva: peer-to-peer WebRTC with a WebSocket fallback, duplicates dropped by client id. 3 updates per second at first, aiming for ~60 [VC] | Pointers take the cheap lossy path. State changes take the reliable path. | **Must.** LiveKit lossy channel for drag frames, reliable channel for the commit. |
| 5 | Binary messages | Canva: protobuf instead of JSON cut server CPU about 30% [VC] | Small packets | Should. A drag frame under 40 bytes. |
| 6 | Stack of present people | Liveblocks AvatarStack with "+N" [DOC], Spline panel at top right [DOC] | Shows who is here | Replaced by our face discs: the video is the presence. |
| 7 | Selection outline in the owner's colour | Liveblocks [DOC], Figma [VC], tldraw [DOC] | Others see what you hold | **Must.** The furniture glows in the holder's colour, with a name tag. |
| 8 | "X is editing" flag | Liveblocks typing flag, cleared on timeout or blur [DOC] | Short-lived intent | **Must.** A chip on the object: "Dana is moving the sofa". |
| 9 | Soft hold (lease) on an object | Liveblocks presence is advisory only [DOC]. Canva has element locks [DOC]. Onshape has no file locks [VC]. | A hold is taken when the finger lands and released on lift or timeout | **Must, our own design.** Request by RPC. Store as attribute `holding=id`. Heartbeat every 2 s, expires after 6 s [OWN design]. |
| 10 | Last writer wins, per property | Figma: the server keeps the last value for each property of each object [VC] | Simple and predictable | **Must**, applied when a hold ends. |
| 11 | Local edits win until the server confirms | Figma: incoming changes that conflict with unconfirmed local edits are discarded to stop flicker [VC] | No snap-back for the person dragging | **Must.** The sofa never jumps out from under your finger. |
| 12 | One authority per document | Figma: one server process per open document [VC] | Settles races | Should. The host's browser for the MVP, a small server worker later [OWN]. |
| 13 | Undo only your own changes | Figma's rule: undo, copy, then redo back to the present must leave the document unchanged [VC]. tldraw: remote changes never enter undo history [DOC] | Undo does not erase another person's work | **Must.** Per-person undo stack. If someone else moved the object since, undo is skipped with a toast. |
| 14 | Remote changes applied in one batch | tldraw `mergeRemoteChanges` [DOC] | One redraw per batch | Should. |
| 15 | Rejoin and replay | Figma: download a fresh document, reapply offline edits, resume [VC] | Survives dropped connections | **Must**, triggered by LiveKit `Reconnected`. |
| 16 | Follow a person's view | Figma, Pitch: tap the avatar [DOC]. tldraw [DOC]. Onshape follow mode [VC]. Gather [IND] | Your camera tracks theirs | **Must.** Tap a face disc to follow their camera in 3D or their view of the plan. |
| 17 | Follow frame | Figma: border in the presenter's colour plus a line of text [DOC]. tldraw: coloured border [DOC] | You always know you are being driven | **Must.** Coloured frame plus "Following Dana · tap to stop". |
| 18 | Following ends when you act | tldraw: stops on pan, zoom, page change or the leader leaving [DOC] | Never fights the user | **Must.** Any orbit gesture ends the follow. A "Back to Dana" chip appears. |
| 19 | Fit the leader's view on a different screen | tldraw: contains the leader's viewport and keeps your own aspect ratio [DOC] | A phone can follow a desktop | **Must.** In 3D, copy the camera position and target and keep your own field of view. |
| 20 | Eased camera with a final snap | tldraw: lerp factor 0.1-0.8, snaps under 2 px [DOC] | Smooth following | **Must.** |
| 21 | Show everyone, with a way out | Figma "Spotlight me" gives viewers a few seconds to say "Not now" [DOC]. Miro "Bring everyone to me" moves people once [IND]. Butter follow-me [VC] | The host brings all phones to one view | **Must.** Host-only "Show everyone", with a 3-second opt-out. |
| 22 | Ask someone to present | Figma "Ask to spotlight", accept or decline [DOC] | Turn-taking | Should. Client taps "Show me" on the agent. |
| 23 | Viewer count for the presenter | Figma [DOC] | The presenter knows who is with them | Should. "3 watching" on the host's disc. |
| 24 | Jump to a person without following | tldraw `zoomToUser`, with a short highlight [DOC] | "Where is she?" | Should. |
| 25 | Laser that fades | tldraw: the trail stays while you draw, then fades as one after 1200 ms, and can be cancelled at once [VC]. Works for read-only users too [VC] | Point without changing anything | **Must.** Long-press on the plan or a wall in 3D. Viewers can use it too. |
| 26 | Text bubble on the cursor | FigJam cursor chat: "/" opens it, typed live, fades 5 s after typing stops, nothing saved [DOC] | Quick text in the moment | Could. Better: a short note pinned to a 3D point and saved. |
| 27 | Show where others are looking in 3D | Spline: other users' pointers and labels show "the position they're viewing the scene from" [DOC] | Presence in 3D space | **Must, our signature.** A small camera cone in the person's colour in 3D, and a "you are here" dot on the plan. |
| 28 | Control modes in a guided tour | 3DVista Live Guided Tours: Party, Presentation and Silent modes, where guests request control [IND] | Who may drive | **Must, our own names:** Free, Guided, Show. |
| 29 | Video attached to the cursor | Pitch: each person's video circle travels with their cursor and pulses while they speak [VC] | Face and action are one object | Should, in the plan view on desktop. On a phone only while that person drags. |
| 30 | Comments pinned to objects | tldraw (licensed) [DOC], Onshape [VC] | Context survives the call | **Must.** "Too big?" pinned to the sofa, saved after the call. |
| 31 | Hide other people's pointers | Google Slides [IND]. Miro users ask for this [IND] | Less clutter | Should. "Hide hands" toggle. |
| 32 | Presence timeout | Yjs awareness: no update for 30 s means offline [DOC, read from a search extract] | Clears ghosts | Our holds: 6 s. Presence: follows LiveKit leave. |

## The flow for one furniture drag (recommended)
1. Finger lands on the sofa. The phone shows it lifted right away (optimistic) and sends an RPC `hold(sofa)` to the authority.
2. If granted, attribute `holding=sofa`. Everyone sees a glow in Dana's colour and the chip "Dana is moving the sofa".
3. If refused (Moshe already holds it), the sofa shakes gently under the finger and shows "Moshe is holding it". No snap, no error dialog.
4. While dragging: lossy `drag` messages at 20 Hz (id, x, y, angle, sequence number). Others spring-smooth toward each new position.
5. Finger lifts: reliable `commit` (id, final position, version + 1). The hold is released and the step is pushed onto Dana's own undo stack.
6. Network drops in the middle: the hold expires after 6 s and others see the sofa ease back to the last committed position.

Plan or 3D on a phone: drag on the plan, which is precise. Show the result in 3D. Allow direct moves in 3D only along the floor plane, with a long-press to pick up [OWN design judgement].
