# LiveKit: what the official kit gives us, and what we must build

Retrieved 2026-11-11, 20:58-21:22 UTC. Evidence: [DOC] = LiveKit docs or the `livekit/components-js` source on GitHub (main branch, read 21:02 UTC). [OWN] = my own knowledge, no source today.

Sources:
- Components index: https://docs.livekit.io/reference/components/react/
- Prefab source: https://raw.githubusercontent.com/livekit/components-js/main/packages/react/src/prefabs/ (ControlBar.tsx, PreJoin.tsx, VideoConference.tsx)
- Grid rules: https://raw.githubusercontent.com/livekit/components-js/main/packages/core/src/helper/grid-layouts.ts
- SDK: /home/client/connect/, /tracks/subscribe/, /tracks/advanced/, /data/packets/, /data/rpc/, /state/participant-attributes/, /events/ (all under https://docs.livekit.io)

## 1. The kit, piece by piece

| Piece | What it does | What we can style or set | What is missing for us |
|---|---|---|---|
| `LiveKitRoom` | Holds the connection and gives context to everything inside [DOC] | `data-lk-theme`, className | Nothing. Use it, or the newer Session API [DOC connect]. |
| `PreJoin` (prefab) | Local camera and mic preview before joining, with no server connection. Returns the choices to `onSubmit` [DOC] | `defaults`, `persistUserChoices`, `onValidate`, `onError`, labels (`joinLabel` default "Join Room", `userLabel` "Username") [DOC source] | No message when permission is refused: errors only go to `onError` [DOC source]. No Hebrew text, no right-to-left layout. Requires a username, which we prefill. The full-screen layout does not fit our flow. **We build our own page and use the hooks `usePreviewTracks` and `usePersistentUserChoices`.** |
| `ControlBar` (prefab) | Mic (with device menu), camera (with device menu), screen share, chat, settings, leave, plus `StartMediaButton` [DOC source] | `controls` keys: microphone, camera, chat, screenShare, leave, settings. `variation`: minimal, verbose or textOnly. `saveUserChoices` (default true) | Fixed set and order. Below 760px (1000px when chat is open) it shows icons only [DOC source]. No follow, point, invite or "voice only" buttons. **We build our own bar from `TrackToggle`, `DisconnectButton` and `StartAudio`.** |
| `TrackToggle` | One toggle for one source, with the state exposed as attributes | className, `data-lk-*` | None. Use as is. |
| `DisconnectButton` | Leave the room | className | Has no "end for everyone" option. That needs a server API call [OWN]. |
| `StartAudio` / `StartMediaButton` | Shows only when the browser blocks audio until a tap, then hides itself [DOC] | label | **Must keep.** iOS Safari blocks audio until the user taps. |
| `MediaDeviceMenu` / `MediaDeviceSelect` | Pick a device | className | Rarely needed on a phone. |
| `GridLayout` | Tiles of equal size. Pages when the grid is full. `useVisualStableUpdate` stops tiles from jumping [DOC] | `tracks`, children | On a portrait phone narrower than 560px it shows at most 1x2. The 2x2 grid needs 560px [DOC source]. **A grid is the wrong layout for us**: the apartment model must be large. |
| `FocusLayout` / `FocusLayoutContainer` / `CarouselLayout` | One tile in focus plus a carousel of the rest. `VideoConference` uses this when something is pinned [DOC source] | `trackRef`, `onParticipantClick` | Reuse `CarouselLayout` as our strip of faces. The "focus" slot becomes the 3D canvas, which is not a track. |
| `ParticipantTile`, `ParticipantName`, `TrackMutedIndicator`, `ConnectionQualityIndicator`, `AudioVisualizer`, `BarVisualizer` | Parts of a tile [DOC] | Plain HTML, so className and style work. State is exposed through attributes such as `data-lk-quality` = unknown, poor, good or excellent [DOC style] | Tiles are rectangles. For round face discs we use `VideoTrack` with our own wrapper. |
| `Chat` (prefab), `ChatEntry`, `useChat` | Text chat to everyone in the room at the moment it is sent [DOC] | `messageFormatter` (+ encoder and decoder on `VideoConference`) | **Not persisted** [DOC]. Anyone who joins later sees nothing. We save chat to the design file. |
| `VideoConference` (prefab) | Full meeting: grid, focus on a shared screen, chat, settings modal. Pins the first screen share automatically. Shows a placeholder tile when a camera is off [DOC source] | chat encoder, decoder and formatter; `SettingsComponent` (alpha) | A reference to learn from, not our product. |
| `ConnectionStateToast`, `ConnectionState` | Toast while reconnecting | className | Translate to Hebrew. |
| `RoomAudioRenderer` | Plays all remote audio | none | Use as is. |

Hooks worth using [DOC index]: `useTracks`, `useParticipants`, `useSpeakingParticipants`, `useIsSpeaking`, `useConnectionQualityIndicator`, `useConnectionState`, `useDataChannel`, `useRpc`, `useParticipantAttributes`, `useLocalParticipantPermissions`, `useFacingMode`, `usePreviewTracks`, `usePersistentUserChoices`, `useSwipe`, `usePagination`, `usePinnedTracks`, `useKrispNoiseFilter`, `useIsRecording`, `useTranscriptions`.

Styling [DOC style]: import `@livekit/components-styles`, then override the `--lk-*` CSS variables (for example `--lk-accent-bg`, `--lk-danger`) and target `[data-lk-*]` attributes. The docs say prefabs are "not intended for extension": use them as they are or as a blueprint.

Right-to-left: none of the component docs I read mention RTL. We must mirror layout order ourselves and keep the media icons unflipped. This is an inference from missing documentation.

## 2. SDK behaviours to switch on

| Behaviour | What it does [DOC] | Our setting |
|---|---|---|
| Adaptive stream | Watches the size and visibility of each video element, asks the server for the matching layer, and pauses hidden elements. JavaScript needs `track.attach()` | **On.** Small face discs then download small video, and a collapsed strip downloads nothing. |
| Dynacast | Pauses simulcast layers nobody watches. `dynacast: true` | **On.** |
| Simulcast | On by default in every SDK. Presets h720, h540, h360, h180 | Phones publish at most h360, with layers h180 and a smaller one [OWN]. |
| SVC (VP9 or AV1, L3T3_KEY) | Switches layers without waiting for a keyframe | Keep VP8 for iOS Safari until tested [OWN]. |
| `setVideoQuality(LOW)` | Caps the quality received from one track | Faces in the strip. |
| `setEnabled(false)` | Stops bytes without renegotiating | When the user collapses the face strip. |
| `autoSubscribe` off + `setSubscribed` | Subscribe only to chosen tracks | Not needed for 2 to 8 people. |
| Reconnect | First resumes (WebSocket reconnect and ICE restart). If that fails, does a full reconnect, which others see as a leave and a rejoin, and tracks are republished. Events: `Reconnecting`, `Reconnected`, `Disconnected` | Hide "left" and "joined" toasts for gaps under 10 s. Keep the 3D scene usable offline and re-sync on `Reconnected`. |
| Disappearing participant | Without `disconnect()`, a participant vanishes after 15 s | Release a person's hold on furniture within the same window. |
| Connection quality | `ConnectionQualityChanged`. The value `Lost` arrives before the timeout | Show a small badge only when quality is poor or lost. |
| Active speakers | `ActiveSpeakersChanged`, `IsSpeakingChanged`, `audioLevel` | Pulse ring on the speaker's face disc. Never reorder faces. |
| Audio RED | Redundant audio. LiveKit recommends turning it on | On. |
| Network path | ICE/UDP, then TURN/UDP 3478, then ICE/TCP, then TURN/TLS. LiveKit Cloud provides TURN/TLS | Nothing to do on Cloud. |

## 3. Data: what goes where

| Channel | Limit [DOC] | Use in the designer |
|---|---|---|
| `publishData` lossy | Sent once, no order. Keep at or under 1300 bytes (the MTU is 1400) | Pointer and laser at 15 Hz, camera pose at 5 Hz, drag frames at 20 Hz (plan coordinates in cm, binary). |
| `publishData` reliable | In order, retransmitted (best effort, not buffered on the server). Up to 15 KiB per packet | "Object committed" (id, position, rotation, version), chat, reactions. |
| `topic` + `destinationIdentities` | Any string topic. Send to the whole room or to named people | Topics: `ptr`, `cam`, `drag`, `commit`, `chat`, `note`. Full sync goes only to someone who just joined. |
| RPC (`performRpc`) | 15 KiB payload, default 10 s timeout, error codes 1400-1505 | "May I take the sofa?" sent to the authority, which replies granted or held by Dana. |
| Participant attributes | 64 KiB across all keys. Change event fires. Needs `canUpdateOwnMetadata` | `holding=<objectId>`, `following=<identity>`, `color`, `role`. These clear themselves when the participant leaves. |
| Participant metadata | 512 KiB | Not needed. |
| Full snapshot | Larger than 15 KiB | Over HTTP from WordPress, never through the data channel. |

## 4. What the kit does not give (we build it)
1. Holds on objects, conflict rules and per-user undo. LiveKit is transport only.
2. Following another person's camera and the "show everyone" summon.
3. Pointer and laser on the plan and in 3D.
4. Face strip and floating face disc layouts sized for a portrait phone.
5. Hebrew and right-to-left text and order.
6. Saved chat and an after-call summary.
7. Detecting the WhatsApp or Facebook in-app browser and offering "open in Chrome or Safari" [OWN].
8. Screen share on phones: the browser API is not available there [DOC MDN, Whereby]. Not needed, because each phone renders the model itself.
