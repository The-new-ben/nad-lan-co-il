# Patterns users already know, and where one product solved it better

- Scope: Zoom, Google Meet, Microsoft Teams, Cisco Webex. Retrieved 2026-11-11, 21:20-22:40 UTC.
- Each pattern cites matrix rows (`B###` in `matrix.csv`). Those rows hold the URLs and evidence classes.
- A pattern is listed as "shared" only when at least three of the four show it with [DOC] or [IND] evidence. Where the evidence is thinner, the line says so.

## A. 34 shared patterns (a user arriving from any of the four expects these)

### Getting in
1. **A link is the invitation.** One tap or click on a URL; no code needs typing (B001).
2. **Guests do not need an account.** A name is enough (B002). Teams and Webex may add an email check or an "Unverified" label (B012).
3. **A preview before entering.** You see your own camera and check the mic before anyone sees you (B004-B005).
4. **Mic and camera state is chosen before entering, and can be remembered** (B006).
5. **A knock or lobby with a host who admits.** Admit, Deny and Admit all, with a visible alert to the host (B009, B013, B074).
6. **A fallback when the camera or mic is blocked.** The browser permission prompt comes first; a help path follows (B008).

### The bar
7. **One row of round or square buttons along an edge**, with mic first and camera second (B025-B026).
8. **The mic and camera buttons toggle and show state:** a slashed icon when off, often red (B039; colour is [OWN] except Webex [DOC]).
9. **The hang-up button is last and visually different**, in red (B029; colour [OWN]).
10. **"More" overflow.** Rare actions hide behind one button (B032).
11. **Share sits next to mic and camera on desktop**, and inside More on phones (B038, B087).
12. **On phones the controls hide, and a tap on the video brings them back** (B028).
13. **People and chat panels open on the side** (desktop) or **top-right** (Teams phone) (B036, B110).
14. **Device dropdowns hang off the mic and camera buttons** (B034).
15. **Keyboard shortcuts for mute and video, plus a shortcut list** (B043-B044, B161).
16. **Hold-to-talk while muted** (space or Ctrl+Space) on three of four (B045).

### The picture
17. **Two families of view:** a grid of everyone, or a speaker/focus view with a strip (B049-B052).
18. **The person speaking is highlighted** with a border, a ring or a sort order (B058).
19. **A name label on every tile** (B060).
20. **A muted icon on muted people** (B061).
21. **Pin is mine only; spotlight or stage is for everyone** (B054-B055).
22. **Self view is a small floating tile that can be moved, minimised or hidden** (B056-B057).
23. **When someone shares, the shared content takes the big area and faces shrink to a strip** (B069-B070).
24. **Phones show far fewer tiles:** 6 to 9 on one screen, then swipe or page (B050, B066).

### Working together
25. **Desktop remote control means asking and approving:** one controller at a time, the owner can take back control, and phones are excluded (B089-B092; Meet has none).
26. **Annotation over a share is a presenter-granted right:** the presenter allows others or keeps it to themselves (B093).
27. **A small common tool set:** pen, text, eraser or clear, pointer or arrow (B094).
28. **The presenter stays in charge of what everyone sees** (stage sync, Present mode, follow mode) (B055, B105).

### Talking without talking
29. **Raise hand, plus emoji reactions that float and fade** (B114-B118).
30. **Chat as a side panel, with a badge for unread messages** (B110, B113; badge [OWN]).

### Trouble
31. **A visible warning when the connection degrades** (bars, a banner or a pop-up), and the call keeps trying (B124-B125).
32. **A reminder when you speak while muted** (B128).
33. **Audio-only or low-data modes for weak networks or driving** (B046, B132).

### Leaving
34. **Leave versus End for everyone, and only the host or presenter can end for all**, usually via a second choice under the leave button (B146-B148).

## B. Ten differences where one product did it better, and why

| # | Problem | Best solver | What they do | Why it is better |
|---|---|---|---|---|
| 1 | Hanging up by accident | **Meet**, now copied by **Teams** | Leave sits far from mic/camera; the Teams redesign "separates Leave to reduce accidental exits" (B030). Zoom mobile went the other way and put End inside the toolbar (B026). | The most frequent action (mute) and the most destructive one (leave) never share a thumb zone. Microsoft's own change admits the old layout failed (B171). |
| 2 | A phone held upright | **Webex "Equal view"** | Portrait only: speaker on top, you below; when content is shared, content on top and speaker below (B053, B070). | The only documented layout designed for a vertical phone and not shrunk from desktop. It splits the screen into two clean halves. |
| 3 | Following one leader without losing freedom | **Teams Live Share LiveFollowMode** | Follow the presenter, take a temporary private view, resync with one action (B105). Zoom whiteboard Present mode locks viewers (B101). | Locking frustrates curious viewers, and free roaming loses the group. Follow plus escape plus resync keeps both. |
| 4 | Seeing who is drawing | **Teams** | Collaborative cursors show each person's name by default; anyone can turn them off (B095). | With 3 or more people drawing, unnamed ink is noise. Names make it a conversation. |
| 5 | Ink that does not pile up | **Meet** | Disappearing ink is on by default (B094). | Pointing gestures vanish; deliberate marks can still be kept. The canvas stays clean without a clear button. |
| 6 | A raised hand left up forever | **Meet** (and Teams) | The hand lowers itself when the person starts speaking; Cancel keeps it up (B117). Zoom keeps it up until lowered. | It removes a constant chore for hosts. |
| 7 | Talking while muted | **Webex** | After more than 60 s of silence, the reminder fires as soon as you speak. A spacebar hold talks without unmuting (B128, B045). | The 60-second rule targets the real failure (forgetting you are muted) without nagging people who mute and unmute often. Users complain about the Zoom and Meet pop-ups (B178). |
| 8 | A busy host leaving | **Zoom** "Assign and leave" / **Webex** automatic successor order | Pick the next host in one dialog; Webex falls back through a documented order (B078). | The meeting never dies because the organiser had to go. |
| 9 | Showing a physical object or a 3D model | **Webex iOS** | AR share of a .usdz 3D object: place, rotate, pinch, walk around. Live phone camera share with others annotating on it (B102-B103). | It is the only one of the four that treats 3D as shared content and not a screen picture. That is the closest match to our use case. |
| 10 | Weak phones and weak networks | **Webex** | Suggests audio-only when the battery is low, and has an audio-only mode (B132-B133). Zoom has bandwidth-coloured quality bars with published thresholds (B124). | Both act before the call breaks, instead of telling you after. |

Runner-up notes, not ranked:
- **Zoom waiting-room branding.** A branded waiting screen with logo, text and video (B010) turns dead waiting time into a branded moment.
- **Teams two-step share confirmation.** A two-step share and live previews (B038) prevent sharing the wrong window.
- **Meet join path.** Meet's iOS Safari path (B001) is now the lowest-friction phone join among the four.

## C. What none of the four does (our opening)
- **No mirrored right-to-left call bar.** Zoom has no Hebrew interface at all. Webex documents RTL only for text, and Meet has an RTL bug in sharing (B157-B158).
- **No reconnect timing is published.** Reconnect UX is not documented anywhere official (B126).
- **Phone-browser feature sets are cut down or missing.** Teams has none (B176, B179). Joining from a phone browser with full shared control does not exist in the four.
- **No product-level "pen" for a shared 3D object on phones**, except Webex AR on iOS (B103) and developer platforms such as Live Share or Collaborate mode (B079).
