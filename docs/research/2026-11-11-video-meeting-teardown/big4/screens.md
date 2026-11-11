# Screen by screen: Zoom, Google Meet, Microsoft Teams, Cisco Webex

- Retrieved: 2026-11-11, 21:20-22:40 UTC. Method: official help centres, vendor blogs and message-center posts, App Store listings, a few independent studies and forums. No account, no meeting joined, no install, nothing downloaded.
- Every line points to a row in `matrix.csv` (`B###`). That row carries the full source URL, retrieval time and evidence class.
- Evidence: [DOC] official documentation, [VC] vendor claim, [IND] independent (press, forum, study, store review), [OWN] my own knowledge with no source found today. "Unknown" means no source was found. It is not a guess.
- Positions are given for a left-to-right interface. None of the four documents a mirrored right-to-left call bar (B158).
- No page I read contained instructions addressed to an AI agent.

---

## 1. Zoom (Zoom Workplace 6.7 desktop, 7.x mobile)

### Before joining
- **Desktop browser:** the link opens a launch page that pushes the desktop app. Below it, "Join from your browser" opens the Web App, but only if the host allowed it [DOC] (B001). The user types a name [OWN] and enters a passcode with the meeting ID [DOC] (B017). That is about four steps to the call (B014).
- **Phone browser:** the Web App runs in mobile browsers. Gallery, chat, reactions, virtual background and captions work there. Sharing, annotation, whiteboard and remote control do not [DOC] (B001, B176).
- **Phone app:** the link opens the app [OWN]. Personal settings decide the starting state: "Show video preview", "Mute my microphone", "Turn off my video" [DOC] (B004, B006).
- **Waiting room:** off by default for instant meetings. Paid accounts can brand it: a title up to 64 characters, a logo, a 400-character description, an image or a muted video, with a desktop/mobile preview toggle [DOC] (B009-B010).

### In the call, desktop
- The toolbar is at the bottom [OWN]. Since 6.7 it shows only the most-used tools, and the rest sit under **More**. Users pin a tool by right-clicking it or dragging it. Host tools are grouped on the right [DOC] (B025, B033). The 6.7 update reset everyone's custom toolbar and the old layout could not be restored [IND] (B180).
- Settings open as one panel on the right [DOC] (B042).
- **Gallery** shows 25 or 49 tiles per screen and pages through up to 1,000 people. **Active Speaker** view and **Immersive View** are also available [DOC] (B049, B051, B063).
- The active speaker gets a yellow/green border that is always on, and there is no setting to remove it [IND] (B058, B181).
- "Hide Self View" hides your own tile; others still see you [DOC] (B057).
- "Ask me to confirm when leaving" is a setting [DOC] (B031).

### In the call, phone portrait (app)
- The toolbar sits at the bottom: Mute, Video, Chat, More. Since December 2025 End/Leave sits inside the toolbar. More opens a grid with reactions at the top [DOC] (B026, B032).
- The toolbar hides after a few seconds and returns on a tap, unless "Always show meeting controls" is on [DOC] (B028).
- Swipe left for gallery once 3 or more people are in the call. The phone tile count is not documented (B050). Swipe right for Safe driving mode: video off, tap to speak [DOC] (B046).
- Speaker and camera-flip icons sit in the top bar [OWN] (B040, B041).

### Invite and people
- The invite link can be copied to the clipboard automatically when a meeting starts [DOC] (B021). There is one host and any number of co-hosts. To leave without ending, the host taps End, then Leave meeting, picks a new host and taps "Assign and leave" [DOC] (B077-B078).

### Sharing and control
- On a phone app, one share menu covers screen, file, camera and whiteboard [DOC] (B087).
- Remote control is desktop to desktop only. Phones can neither request nor give it, and iPhones cannot receive it. One person controls at a time, and a new grant revokes the old one [DOC] (B089-B092).
- In whiteboard Present mode everyone is view-only and follows the presenter's viewport [DOC] (B101, B105).

### Ending
- Only the host can end the meeting for everyone [DOC] (B148). A short experience survey can follow; the account can disable it [IND] (B150).
- The interface is **not available in Hebrew**: 17 interface languages, and Hebrew is not among them [DOC] (B157).

---

## 2. Google Meet

### Before joining
- **Desktop browser:** no install. The green room shows a preview tile with device dropdowns. The mic bar moves when you speak, and "Test speakers" plays a sound. Then "Join now", or for a guest, type a name and "Ask to join" [DOC] (B001, B004-B005).
- **Phone browser:** since 23 June 2026, iOS users without the app are sent to Safari. They type a name and request entry [DOC] (B001). Android browser behaviour is not documented.
- **Phone app:** the link prefers the installed app [DOC]. App versions are supported for 6 months [DOC] (B023).
- **Host side:** a prompt offers Admit or Deny entry. With several people waiting: View all, then Admit all or Deny all [DOC] (B013, B074).

### In the call, desktop
- One bottom bar, always visible [DOC] (B024-B025):
  - **Left:** the meeting code, plus a clock when the window is maximised.
  - **Middle:** mic, camera, captions, raise hand, present, more, hang-up.
  - **Right:** meeting details, people, chat and activities.
  The leave button is placed "away from the camera and mic buttons" [DOC] (B030). Icons carry no text labels; hovering shows the name [DOC] (B027).
- **Layouts:** Auto is the default. Tiled shows up to 49 tiles (16 by default), plus Spotlight and Sidebar. "Hide tiles without video" is an option [DOC] (B048-B052, B062).
- **Self view:** in a one-to-one call it floats bottom-right. With 3 or more people you choose floating or a grid tile, and the choice is saved. It can be dragged to any corner. Crop settings change only your own view [DOC] (B056, B064).
- A shared presentation is pinned automatically. You can unpin it to a tile or mute its audio [DOC] (B069).

### In the call, phone portrait (app)
- **iPhone:** up to 8 tiles. Tap the screen to show the controls [DOC] (B050, B028).
- Each tile has a More options menu with Pin and Full screen. You can pinch to un-crop a tile, and minimise your own floating video [DOC] (B054, B064-B065).
- In 2025 emoji reactions moved into the bottom bar, raise hand moved into the overflow menu, and the iOS hang-up button moved to the right [IND] (B026, B118).
- "Switch camera" is on the bottom bar (B041). On-the-Go audio-only mode is under More [DOC] (B046).
- Whoever shares is pinned automatically. Pin someone else to swap them in [DOC] (B070).

### Sharing and control
- The app shares via More > Share screen > Start sharing [DOC] (B087). Meet has **no remote control** (no doc found) (B089).
- **Annotation:** pen, stickers, text and disappearing ink, which is on by default. Only the presenter and the co-annotators they appoint can draw. On Android only pen, eraser and trash are available, and an Android presenter cannot appoint co-annotators [DOC] (B093-B094).

### Chat, hand, ending
- **Raised hand** lowers itself when you start speaking. Tap "Cancel" to keep it up [DOC] (B117).
- **Ending:** the host chooses "End meeting for all" or "Leave meeting". On a phone the options read "End the call" and "Just leave the call" [DOC] (B147).
- **Lone participant:** the call ends after 10 minutes idle plus 2 minutes with no response [DOC] (B144).
- **Hebrew:** the App Store lists Hebrew [DOC] (B157). A known issue: Hebrew/Arabic windows shared from Windows can appear mirrored [DOC] (B158).

---

## 3. Microsoft Teams

### Before joining
- **Desktop browser:** "Continue on this browser" or "Join on the Teams app", then the pre-join screen with a mic toggle (remembered for next time), background effects and an audio choice: Computer, Phone, Room or Don't use audio. Then "Join now" [DOC] (B001, B004, B006-B007).
- **Phone browser:** a Microsoft Q&A moderator says "Teams for Web is not supported on mobile devices". Another reply suggests "Join on the web instead", so the answers conflict [IND] (B001, B179).
- **Phone app:** the link opens the store if the app is missing. Then allow mic, "Join as a guest", type a name, "Join meeting" [DOC] (B014).
- **Lobby:** a guest who is not admitted within 30 minutes is removed. The host sees an Admit / View lobby notification (Ctrl+Shift+Y), and labels next to names: Unverified, Email verified or External [DOC] (B011-B013).

### In the call, desktop
- **Current documentation:** the bar is across the top with a timer. Camera, Mic and Share stay fixed. Chat, People, Raise hand, React, View, Controls, Notes, Rooms, Copilot and Apps can be pinned, unpinned or reordered. Leave has a dropdown with "End meeting" for presenters [DOC] (B024-B025, B029).
- **Redesign (MC1317197), worldwide mid-to-late October 2026:**
  - Core controls are centred, with mic, camera and share grouped together.
  - Leave is set apart "to reduce accidental exits".
  - Less-used actions move into a reorganised More menu.
  - A new share panel adds live previews, tabs and a two-step confirmation.
  - Personalisation persists per device and does not sync.
  - On by default; admins cannot turn it off [DOC] (B030, B033, B038, B047).
- **Layouts:** Large gallery shows up to 49 on screen (100 in total). Presenter layouts: Content only, Standout, Side-by-side, Reporter. "Pin for me" is local only. Spotlight pins a video for everyone, but not in Large gallery [DOC] (B049, B051, B054-B055).

### In the call, phone portrait (app)
- **Bottom:** Camera and Mic bottom-left, Speaker bottom-middle, More and Leave bottom-right. **Top-right:** Chat and People. Tap the centre to show the controls [DOC] (B026, B028).
- More contains Reactions, Chat, People, Share, Views, Background effects and Start recording [DOC] (B032).
- **Gallery:** 8 featured videos plus 15 to scroll. Large gallery shows 10 at once on newer phones (older page) [DOC] (B050).
- Press and hold a video to pin it [DOC] (B054). A camera-flip control was not found in the docs (B041).

### Sharing and control
- **Desktop:** Request control, Give control, Take back, Release control. The screen-reader path is Shift+Ctrl+Space then "Cancel control". Phones cannot give or take control [DOC] (B089-B091, B167).
- **Annotation** runs on Microsoft Whiteboard [DOC] (B093-B099):
  - The presenter picks "Everyone can annotate" or "Only I can annotate"; others press Request.
  - Collaborative cursors show names by default.
  - The presenter can "interact with the background" to scroll under the ink.
  - "Save a snapshot" keeps the annotations; "Clear my annotations" removes them.
  - Phones can annotate when the presenter shares from a desktop.
- **Live Share** offers follow-the-presenter with a private escape and resync. Microsoft's own example is a presenter driving the camera on a 3D model for everyone [DOC] (B103, B105).

### Ending
- **Rate my call** pops up after about 1 call in 10. Thumbs are replacing stars. There is no way to switch it off [DOC/IND] (B150-B151).

---

## 4. Cisco Webex (Webex App, Suite meeting platform)

### Before joining
- **Desktop browser:** on Windows or Mac the browser may push the desktop app; "Join from this browser" stays in the web app. Linux and ChromeOS open the web app directly. A preview window checks mic and camera, then Join. Signed-in users skip the lobby [DOC] (B001, B004).
- **Phone browser:** "Webex Join" works in Safari or Chrome on iPhone (iOS 15.2+) and in Chrome 81+ on Android. iPhone Safari has no fullscreen button [DOC; the page returned "not found" when fetched directly] (B016, B065).
- **Phone app:** audio choices are Use Internet for audio, Call me, Call in, or Don't connect audio [DOC] (B007). The iOS app joins muted by default [IND] (B006).
- **Lobby:** the waiting person can press "Notify host". The host sees a red dot above Participants. Waiting people are grouped Internal, External or Unverified, with Let in, Remove and Move to Lobby [DOC] (B009, B012-B013).

### In the call, desktop
- **Controls:** Mute (dropdown: Audio options), Stop video (dropdown: Video options), Share content, Record, Participants, Chat, Apps, Layout, More, and "Leave meeting or End meeting for all". Exact order is [OWN] (B025).
- **Meeting Info** at the top offers "Copy meeting link" [DOC] (B036, B072).
- **While sharing:** controls move to a top bar, and a floating window shows all videos [DOC] (B069, B107).
- **Grid:** the active speaker is highlighted and pages can be navigated. "Stage" can be synced by the host; attendees cannot change it [DOC] (B055, B058, B066).
- **Self view** can sit in the grid, float in a corner, or be hidden [DOC] (B056-B057).

### In the call, phone portrait (app)
- **Layouts** [DOC] (B050-B053, B070):
  - **Grid:** up to 9 tiles on iPhone, 6 on an Android phone.
  - **Equal view** (phones, portrait only): active speaker on top, your self view below. When content is shared, the content goes on top and the speaker below.
  - **Focus view:** content full screen with the speaker minimised.
  - **Stack view** (tablets only): a stage with 6 thumbnails.
- **Video:** a green dot shows when your camera is on. Video > "Swap camera" switches front and back [DOC] (B041).
- **Battery and data:** the app suggests audio-only mode when the battery is low [DOC] (B133). If anyone joins with narrow-band audio, everyone's wide-band audio drops without warning [DOC] (B137).
- **Muted while talking:** you get a reminder to unmute. After more than 60 seconds of silence, a reminder appears as soon as you start talking [DOC] (B128).

### Sharing and control
- **Share from iPhone:** More > Share Content > Share Screen > Start Broadcast. A red clock icon shows you are live [DOC] (B087, B107).
- **Share the camera:** zoom works and others can annotate the live view [DOC] (B102).
- **AR 3D share (.usdz):** place, rotate with two fingers, pinch to resize, walk around it [DOC] (B103).
- **Annotation tools:** Undo, Draw, Text, Eraser with four clear options, Arrow/laser, Border, Save to gallery [DOC] (B094, B097-B098).
- **Remote control:** on desktop, unanswered requests time out after 30 seconds. iPhone users must switch it on in Settings first. You cannot annotate while you are controlling [DOC] (B089-B100).
- **Camera gestures:** hold the gesture until the animation plays [DOC] (B116).

### Ending
- The host chooses "End meeting for all" or "Leave meeting". If the host leaves without choosing a successor, the role passes in a set order: alternate host, signed-in presenter, signed-in attendee, then the others. On mobile the role is assigned automatically [DOC] (B078, B147).
- Meetings are capped at 24 hours. Chat closes but is saved; it cannot be downloaded [DOC] (B112, B155).
- **Hebrew:** one of 33 interface languages. Right-to-left text works on Windows, Linux and Mac; mobile is not stated [DOC] (B157-B158).

---

## Gaps that apply to all four
- **Reconnection timing** (how long each product keeps trying) is not documented by any of them (B126). Reconnect wording comes only from forums (B125).
- **Exact desktop bar order:** only Meet documents it.
- **Leave button colour:** not documented by any of the four; red is [OWN] (B029).
- **Phone-browser screen layouts:** none of the four documents them.
- **A mirrored (RTL) call bar:** none of the four documents one.
