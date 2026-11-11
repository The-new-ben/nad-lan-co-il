# Big-4 video meeting teardown: overview

Scope: Zoom, Google Meet, Microsoft Teams, Cisco Webex. Each is checked in a desktop browser, a phone browser and the phone app.
Retrieved: 2026-11-11, 21:20-22:40 UTC.
Method: read-only. Sources were official help centres, vendor posts, App Store listings, independent studies and forums. No accounts, no meetings joined, no downloads.
Builds on the earlier `../../2026-11-10-apartment-designer/call/zoom-teardown.md` and `livekit-mapping.md`. It deepens them and does not repeat them.
No page contained instructions addressed to an AI agent.

## Files
- `matrix.csv`: 184 behaviour rows in 10 chapters × 12 product-platform cells. Each row lists its source URLs, retrieval time and evidence classes.
- `screens.md`: each product screen by screen (join, desktop call, phone portrait call, invite, share and control, end).
- `patterns.md`: 34 shared patterns users already know, 10 places where one product solved it better, and gaps none of the four fills.
- `take-list.md`: what we build for a 2-8 person phone-first 3D apartment call, with priorities, what we explicitly do not take, and why.

## Self-check
- Rows: 184. Rows with at least one source URL: 183. The one row without a source is "new-message notice" (all [OWN]).
- Rows whose only evidence is [OWN]: 2 of 184 (1%). That is under the one-quarter cap.
- Cell tags: 562 [DOC], 67 [IND], 61 [OWN] (9% of tags). No [VC] tags were used, because vendor blog statements were treated as documentation.
- Distinct URLs: 123 http(s) sources, plus one pointer to the earlier HAD-706 file for facts carried over from that pass.
- 10 random URLs (seed 20261111) all returned HTTP 200 with matching page titles.
- Five claims re-read on the page: four confirmed (Webex shortcuts; Meet Android annotation limits; Teams Rate My Call 1 in 10 with thumbs replacing stars; Zoom "Hide Self View"). The fifth, a Teams Q&A page, says the web app is not supported on mobile devices but not that users are redirected; the matrix wording was corrected.

## The 12 patterns that matter most
1. A link is the invitation, and guests need no account.
2. A preview with a mic meter and camera check comes before anyone sees you.
3. One bar on the bottom edge, mic first, camera second.
4. Leave is last, red and set apart. Meet and the October 2026 Teams redesign separate it explicitly to stop accidental exits.
5. On phones, controls hide after a few seconds and a tap brings them back.
6. Rare actions live in "More".
7. A grid view and a speaker/focus view. Phones show 6-9 tiles per screen.
8. When someone shares, the content takes the big area and faces become a strip.
9. Pin is for me only; spotlight or stage is for everyone.
10. Self view is small and floating, and can be moved or hidden. Fatigue research supports hiding it.
11. Control of shared content is asked for and approved, one holder at a time, and the owner can take it back. On all four, pixel remote control is desktop-only.
12. The host chooses between leaving and ending for everyone, and can hand over the host role.

## Best-in-class moves worth rebuilding (our own words and design)
- Meet: leave far from mic and camera; raised hand lowers when you speak; disappearing ink by default.
- Teams: follow the presenter with a private escape and resync; names on collaborative cursors; two-step share confirmation.
- Webex: portrait "Equal view" (content on top, speaker below); AR 3D object sharing on iOS; audio-only offered when the battery is low; "you're muted" reminder only after more than 60 s of silence.
- Zoom: branded waiting room; "Assign and leave" host handover; quality bars with published thresholds.

## Priority-1 build list (details in take-list.md)
1. Join from the link in the phone browser: no app, no account, 3 taps or fewer, mic and camera off by default.
2. A preview with a level meter and a plain fix path for blocked permissions.
3. A bottom bar in right-to-left order with text labels, with Leave isolated at the far edge.
4. "The pen": one holder, request card with a 30 s timeout, rep can always take it back, holder's name shown on the object.
5. Follow the pen holder's 3D view, with a private peek and one-tap resync.
6. Phone portrait split: apartment about 70% on top, face strip below, small hideable self view.
7. Reconnect banner within 1 s, 30 s of retries, then rejoin. The design snapshot is re-pulled on reconnect.
8. Leave versus end for everyone, with automatic handover of pen and host.

## Gaps none of the four fills (our opening)
- No mirrored right-to-left call bar. Zoom has no Hebrew interface at all; Webex has RTL text only; Meet has an RTL sharing bug.
- No published reconnect timing.
- Phone browsers get a cut-down product or none (Teams).
- No phone-friendly shared "pen" on a 3D object, except Webex AR on iOS and developer platforms.

## Not verified
- Exact desktop bar order for Zoom, Teams and Webex. Only Meet documents it; the rest is [OWN].
- Leave-button colours on all four ([OWN]).
- Active-speaker styling for Meet, Teams and Webex ([OWN]). The Zoom detail comes from community answers.
- Reconnect wording and timing: forums only; no official page.
- Webex Join browser table: seen in a search-index snippet; the page returned "not found" on direct fetch.
- Two Webex iOS lines (picture-in-picture, accidental-end fix) come from release-note search results; the exact article was not pinned.
- Meet's 2025 phone bar change: the Android Authority page returned 403; the change is known from the search summary only.
- Teams mobile tile counts come from an older Microsoft page and may be stale. The Teams redesign's final position (top or bottom bar) is not stated.
- Zoom phone tile count per screen, Meet Android browser joining, Teams camera flip, Webex mobile bar order, and Webex post-call survey: not found.
- Many rows rely on search-engine summaries of the official page, not a full fetch. The `retrieved_utc` column marks them "(search summary)".
- Facts carried over from the 2026-11-10 pass were not re-fetched today; they are marked "prior HAD-706 pass".
