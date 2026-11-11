# How each product splits a phone screen between faces and content

Retrieved 2026-11-11, 21:00-21:27 UTC. Sources are in `matrix.csv` (area "3 Phone layout with shared content"). Marks: [DOC], [VC], [IND], [OWN] as in the matrix.

| Product | Faces and content on a portrait phone | Source class |
|---|---|---|
| WhatsApp | The current speaker is highlighted and shown first. On leaving the app the call shrinks to a floating picture-in-picture window (iPhone since version 23.3.77). One how-to says it can be dragged to a corner or off the edge. Screen sharing includes audio. | [VC] blog; [IND] press and a low-quality how-to |
| FaceTime | In a web browser: grid toggle, highlighted speaker, full-screen button, flip camera. No screen sharing or SharePlay on the web. In the app, SharePlay syncs content while faces float above it [OWN for the app layout]. | [DOC] |
| Telegram | Tap a video to make it full screen. A pinned video stays in focus as people join. Tablet: grid and participant list side by side. Desktop: whoever shares is pinned automatically. Camera and screen can be shared together. | [VC] |
| Discord | Activities are web apps in an iframe inside the call on desktop, mobile and web. The pages I read do not document how they are laid out on a phone. Watching a stream: tap the name. | [DOC] / [IND] |
| Slack Huddles | Up to 2 people share at once. Drawing on a share works only in the desktop app. On a phone, sharing is in the three-dots menu. | [DOC] |
| Signal | Desktop: Grid, Sidebar and Speaker views. Phone layout not documented. | [VC] |
| Whereby | `floatSelf` puts the self view at the bottom right and `autoHideSelfView` hides it. Picture-in-picture button. No screen share in phone browsers. | [DOC] |
| Jitsi | Tile view or the active speaker. On a phone it pushes the app over the web. | [DOC] / [IND] |
| LiveKit kit | GridLayout shows 1x2 on a phone narrower than 560px. Screen share pins focus and puts the others in a carousel. | [DOC] source code |
| Around (closed 31.3.2025) | Floating heads in resizable circles, with AI that keeps the face centred, and a "campfire" circle mode. | [IND] |
| Pitch | A video circle travels with each person's cursor on the canvas and pulses while they speak. They chose not to use a grid. | [VC] |
| Gather | Video appears when avatars come close and fades as they move apart. A spotlight tile reaches the whole room. | [IND] / [DOC] |
| Butter | Spotlight enlarges some people and shrinks the rest. Each agenda block can set the layout. | [VC] search extract (the updates site refused connection when re-checked) |
| 3DVista Live Guided Tours | Video call inside a virtual tour on desktop and mobile. Guests can follow the host or take control. The screen split is not documented. | [IND] |
| Figma, tldraw, Spline | No video built in. Presence is cursors plus a coloured follow frame, and the canvas stays full screen. | [DOC] |

## What the market converges on
1. Content takes the screen. Faces become small round, draggable or collapsible elements (Around, Pitch, WhatsApp picture-in-picture).
2. The speaker is shown with a ring or highlight, not by moving tiles around (WhatsApp, FaceTime web, Pitch pulse, LiveKit `useVisualStableUpdate`).
3. Pinning beats automatic switching. The shared thing does not lose focus when someone joins (Telegram, LiveKit auto-pin).
4. The self view is optional and small (Whereby `autoHideSelfView`). The Stanford self-view fatigue finding is [OWN] here: their page refused the fetch.

## Three recommended layouts for an apartment call on a portrait phone

**Layout A: "Tour" (default, when someone is leading: the host or a person being followed)**
- The 3D view or plan fills the screen from the top to just above the control bar.
- Faces: a horizontal strip of round discs (44px) floating over the top edge of the model. The speaker's disc gets a pulse ring. The self view is hidden after 10 s.
- The person being followed gets a coloured frame and a text line: "Following Dana · tap to stop".
- Use when the agent walks the client through rooms, or anyone follows anyone.

**Layout B: "Arrange" (someone is dragging furniture)**
- The plan from above fills the screen. 3D shrinks to a 30% inset window that can be swapped with a tap.
- Faces collapse to a single pill ("4 people · Dana speaking"). Whoever is dragging gets their 28px face disc on the object they hold, as in Pitch's cursor video.
- Controls hide after 4 s of no taps, but never during a drag.
- Use from the first touch on furniture until 5 s after the last one is put down.

**Layout C: "Talk" (deciding, money, questions)**
- Faces grow into a 2x2 grid in the top half (LiveKit 1x2 for 2 people). The model shrinks to a still in the bottom half that keeps its state; tap it to return to A.
- Use when the host switches to "discussion", when nobody has touched the model for 60 s and someone is speaking, or on "voice only" (the faces become initials).

Switching: automatic between A and B, by the person's own touch or the host's control. C is a manual button plus the idle rule. The model never moves to make room for a face.
