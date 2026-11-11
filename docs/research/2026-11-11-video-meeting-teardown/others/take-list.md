# Take list: what we take, from where, the bar to meet, and how we rebuild it as our own

Priority 1 = needed for the first public call. 2 = within a month. 3 = later.
"Bar" = the measurable level to reach. Sources are in `matrix.csv`. We rebuild ideas, not looks: no copied icons, wording, colours or layouts.

Design rule for every item (owner law 13.10.2026): no cream, gold or terracotta, and no default "AI look". Proposed identity for the call layer: **architectural blueprint**. Ink navy #0E1B2C with drafting cyan #27B3E6 and a safety-orange mark #FF5A1F for "held" objects. Faces Heebo (Hebrew) and IBM Plex Sans (Latin). Why it is not the default: the palette comes from architects' sheets and site safety markings, the world of the apartment itself. Final approval goes through Claude Design.

| # | Take | From | Bar | Our rebuild (words in Hebrew UI) | Priority |
|---|---|---|---|---|---|
| 1 | Two taps from the WhatsApp message to seeing the apartment | FaceTime web, WhatsApp call links | Open link, then one "כניסה" (Enter) tap. Name prefilled. Camera off, mic asks on first tap | Our own entry card over the live model preview, not a device-test page | 1 |
| 2 | Name only, never an account, for guests | Jitsi, FaceTime web, Whereby | 0 sign-up fields | One field: "איך לקרוא לך?" (What should we call you?) | 1 |
| 3 | Audio unlock button | LiveKit `StartAudio` | Never a silent call on iOS | Full-width strip: "הקישו כדי לשמוע" (Tap to hear) | 1 |
| 4 | Join as a listener when permission is refused | Whereby `deny_device_permission` (they emit the event; the fallback is ours) | 100% of refusals still enter | "נכנסת בלי מיקרופון" (You joined without a microphone) + a "how to allow" sheet for iOS and Android | 1 |
| 5 | Custom phone control bar | LiveKit `TrackToggle`, `DisconnectButton` | 5 primary buttons, each at least 44px, Hebrew label under the icon, right-to-left order | Mic · Camera · Follow · Point · Invite, leave on the far end | 1 |
| 6 | Round face discs with a speaker ring, no reordering | Around floating heads, Pitch pulse, LiveKit `useVisualStableUpdate` | Order never changes. Ring shows within 300 ms of speech | Discs ringed in the person's colour | 1 |
| 7 | Adaptive stream + dynacast + simulcast | LiveKit SDK | Phones publish at most 360p; a collapsed strip uses 0 kbps video | Settings only | 1 |
| 8 | Follow a person's view, with a frame, ended by touching | Figma, tldraw, Pitch, Onshape | Gap under 150 ms on Wi-Fi. Any gesture ends the follow | "עוקבים אחרי דנה · הקישו לעצור" (Following Dana · tap to stop) + "חזרה לדנה" (Back to Dana) chip | 1 |
| 9 | Host summons everyone, with an opt-out | Figma Spotlight, Miro, Butter | 3 s "לא עכשיו" (Not now) | Host button: "כולם אליי" (Everyone to me) | 1 |
| 10 | Soft hold on furniture + glow in holder's colour + "X is moving" | Liveblocks selection and typing patterns; locks are ours | Hold answered within 200 ms. Never two people holding one object | "דנה מזיזה את הספה" (Dana is moving the sofa) chip; gentle shake on refusal | 1 |
| 11 | Local edits win until confirmed | Figma | 0 snap-back under the finger in a 2-phone test | Engine rule | 1 |
| 12 | Lossy frames for drags, reliable commit | Canva pointers, LiveKit data | Drag frames ≤ 40 B, 20 Hz; commit in 1 reliable packet | Engine rule | 1 |
| 13 | Per-person undo | Figma, tldraw | My undo never removes another person's move | "בטל את שלי" (Undo mine) | 1 |
| 14 | Invite during the call over WhatsApp | FaceTime "Share Link", Slack copy link | Share sheet opens in 1 tap | "הזמנה בוואטסאפ" (Invite on WhatsApp) + copy + QR for a second phone in the same room | 1 |
| 15 | Reconnect without losing the model | LiveKit `Reconnecting`/`Reconnected`, Figma replay | The model stays usable offline; re-sync in under 3 s | Thin bar: "מתחברים מחדש…" (Reconnecting…) | 1 |
| 16 | Layouts A/B/C (see phone-layouts.md) | Synthesis | The model never yields to a face | Our own | 1 |
| 17 | Laser pointer on the plan and in 3D | tldraw lasers | Fades 1.2 s after lift; viewers can point too | Long-press = "כאן" (Here) pulse | 2 |
| 18 | Other people's view cones in 3D | Spline (pointer shows the viewing position) | Visible at 10 m, never blocking furniture | A small cone in each person's colour | 2 |
| 19 | Control modes Free / Guided / Show | 3DVista Party/Presentation/Silent (our own names) | Host switches in 1 tap | "חופשי · מודרך · הצגה" (Free · Guided · Show) | 2 |
| 20 | Notes pinned to furniture, saved after the call | tldraw comments, Onshape | 100% survive the call | Pin with text | 2 |
| 21 | After-call summary card | Slack huddle notes; ours | Opens within 5 s of leaving; one-tap WhatsApp share | Before and after plan + list of changes + notes | 2 |
| 22 | Chat saved into the design file | LiveKit chat is not persisted (gap) | Someone who joins late sees the history | — | 2 |
| 23 | Connection badge only when poor | LiveKit `data-lk-quality` | Hidden when good | Dot on the disc | 2 |
| 24 | Voice-only mode | Jitsi audio-only, Whereby event | One tap; the model stays live | "קול בלבד" (Voice only) | 2 |
| 25 | Detect the in-app browser | Gap in every source | WhatsApp webview detected 100% | "פתחו בכרום/ספארי" (Open in Chrome/Safari) | 2 |
| 26 | Video bubble riding the dragger's pointer (desktop) | Pitch | — | Disc beside the held object | 3 |
| 27 | AI face crop for small discs | Around | Face fills 70% of the disc | — | 3 |
| 28 | Reactions pinned to an object | Signal burst, Slack reactions, placed in 3D by us | — | Heart over the sofa | 3 |
| 29 | Hebrew decision summary | Slack AI notes | Reviewed by a person | — | 3 |
| 30 | "Option B" copy of the layout | Onshape branching | — | "גרסה ב׳" (Version B) | 3 |

## Explicitly NOT taking
- Screen share on phones: no browser API (MDN, Whereby). Pixels are the wrong medium; we sync state.
- An equal-tile grid as the default (LiveKit `VideoConference`, Jitsi tile view): it kills the model.
- Pages that test devices or connectivity before entry (Whereby `precallCeremony`): friction on a phone.
- Proximity audio and avatars walking around (Gather): a gimmick for 2 to 8 people.
- Hard locks that need "unlock" (Canva-style element lock): holds release themselves.
- Hand raising and breakout rooms: meeting tools, not for viewing an apartment.
- Recording by default: privacy exposure (lead privacy is the site's biggest risk). Only on explicit consent, if ever.
- Pushing an app install (Jitsi, Riverside): we stay browser-only.
- Any copied names, icons or text: "Spotlight", "Huddle", "Party mode", "Campfire" are not used.
