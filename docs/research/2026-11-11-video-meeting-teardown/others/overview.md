# Overview: phone call apps, browser video, and co-editing tools (part 2 of 2)

Date: 11.11.2026. Sources read 20:58 to 21:27 UTC (read-only: help centres, developer docs, GitHub source, company blogs, press, forums). No account opened, no call joined, nothing downloaded. Zoom, Meet, Teams and Webex are covered by the other agent.

## Files
- `matrix.csv`: 229 behaviour rows × 25 products, plus a takeaway for nad-lan in each row. A cell reads: what happens [type] URL @UTC time.
- `livekit-components.md`: what our supplier's kit gives ready-made, what is missing, and which SDK settings to turn on.
- `multiplayer-patterns.md`: 32 co-editing patterns and the recommended drag flow for furniture.
- `phone-layouts.md`: how each product splits a phone screen, and three layouts for us.
- `take-list.md`: 30 items to take (priorities 1 to 3), and a list of what we do not take.

## Evidence classes
- [DOC] official documentation, help centre or source code
- [VC] the vendor's own blog, marketing or case study
- [IND] independent source: press, forum, reseller, review
- [OWN] my own knowledge, no source today
- "(search-extract)": the fact came from a search engine's extract of the cited page, not a full read of it. Weaker, but still traceable.

## Counts (self-check)
- Rows: 229. Rows with at least one source URL: 226. Rows that include an [OWN] cell: 7 (3%). Rows that are [OWN] only: 3. The limit was 25%.
- Unique source URLs: 88.
- Random check of 10 URLs (seed 1111, run about 21:30 UTC): 9 answered HTTP 200. `updates.butter.us` refused the connection (ECONNREFUSED). Its 2 cells are marked search-extract and should be treated as unverified. The content of the other 9 had already been read in full earlier and supports the cells.

## Main findings
1. The market puts content first on phones. Faces become small circles or picture-in-picture (Around, Pitch, WhatsApp). The speaker gets a ring, and tiles do not reshuffle.
2. No phone browser can share its screen (MDN, Whereby, FaceTime web). Our edge: every phone renders the 3D itself, and we sync state, not pixels.
3. Guided 3D tours with video exist only as add-ons (Matterport partners, 3DVista). Nobody combines video, live furniture editing, and the phone browser in one product. That gap is ours.
4. The best co-editing ideas come from Figma (last writer wins, local edits shown at once), tldraw (follow, laser, per-user undo) and Spline (in 3D, a person's pointer shows where they are looking from). Nobody documents a self-releasing hold on a 3D object. We design that ourselves.
5. The LiveKit kit gives us transport, tracks, adaptive bandwidth, reconnect events, speaking state and data channels (lossy at 1300 B or less, reliable at 15 KiB or less, RPC with a 15 KiB payload and a 10 s timeout). Its ready-made pieces (PreJoin, ControlBar, GridLayout, VideoConference) are desktop meeting UI with no right-to-left support. On a portrait phone the grid shows at most 1x2. We use the hooks and build our own face strip and control bar.
6. LiveKit chat is not saved. A late joiner sees nothing. We save chat with the design.
7. No product I read documents right-to-left, Hebrew or in-app-browser support for its call UI. We must design and test those ourselves.

## Not verified (state plainly)
- Phone layouts for Discord Activities, Signal, Messenger and Slack on a phone: not documented in the pages read.
- WhatsApp in-call controls and FaceTime app gestures: [OWN] or a low-quality how-to.
- Miro help and Discord support pages blocked direct reading (403). Their facts come from search extracts and forum threads.
- How Stanford's self-view fatigue research applies: [OWN]. The page blocked reading (403).
- Enscape, Shapespark host tours and Canva "is editing" labels: no official source found.
- WhatsApp call-link expiry: sources conflict (30 days or 90 days).
- No page I read contained instructions aimed at an AI agent.

## Retrieval-time note
Times are per source fetch (accurate to about 5 minutes). Some pages were read in one batch, so their rows share a timestamp.
