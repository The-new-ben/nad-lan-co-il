# Pro forum: design boards (HAD-726)

Claude Design canvas (private to the owner's account): https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC

Direct play links, one per board (checked in Chrome on 12.11.2026):

| Board | Link |
|---|---|
| 1 Feed (forum home) | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-15dd8cd198dd |
| 2 Discussion | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-c759609e9e9b |
| 3 Writing + one-step entry | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-66cf255f67dc |
| 4 Professional card with the forum window | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-313eea0da738 |
| 5 Profile, with self removal | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-30956c1cee26 |
| 6 Short video | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-6cf9c7c09f6e |
| 7 Register record, did not join | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-58d15d1850f4 |
| 8 Requests board | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-865a35ba9eb1 |
| 9 One request with offers | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-fde3ab2ac9c0 |
| 10 Join as a professional (84 trades) | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-7263a67f9d7e |
| 11 Finished work, kudos, reactions, endorsements | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-55b5dafaa761 |
| 12 Video call from a request | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-bb1592bc109b |
| 13 Ben's control panel (desktop) | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-2e771e05cb9f |
| 14 The forum on desktop | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-fd91350171f7 |
| 15 The forum inside every professional card (12.11 night) | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-2d348d6ecb35 |
| 16 Video call with a shared board on a plan, phone | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-a4cfe6e39e88 |
| 17 The shared board on desktop, numbered notes | https://claude.ai/artifact/6pVfLsFgiNgMWDDWK6XhkC#play-657d7a78a665 |

## Identity: the building site's notice board

- Ground: cold concrete white `#F2F4F5`. Surface `#FFFFFF`. Asphalt ink `#101820`, second ink `#3A4650`, muted `#5B6770`, hairline `#D5DBDF`.
- Action: the site's sea blue `#2F6F86` (keeps the forum inside Skin A).
- New and live: raspberry `#B0144F` on `#FBE9F0` (text `#8C0F3E`). Used only for what is new, unanswered or happening now, and for the one "publish" button.
- Confirmed and verified: `#1B4D33` on `#EAF4EF`. Danger: `#B3261E`.
- One cool tint per profession, always with the profession's name beside it: contractor `#DCE6F2/#1D3B66`, lawyer `#EBDDF0/#4A1D5E`, appraiser `#DCEFE3/#1B4D33`, mortgage `#DDE3FB/#1E2F8F`, designer `#E7E1FA/#43308F`, broker `#D9EEF0/#0E4A57`, developer `#E3E6E8/#22303A`.
- Faces: Rubik (headings, numbers) and Assistant (text, the site's body face).
- Why it is not the default look: no cream, beige, gold or serif; the colour comes from the professions themselves, not from decoration.

## Files

- `boards/` : PNG renders of the six boards (rendered from the board markup with headless Chrome at 2x; the canvas itself was also opened and looked at in Chrome).
- `canvas-source/` : the `.dc.html` sources and `canvas.json` as published.

Every name and number on the boards is sample content for the design and is marked "דוגמה לעיצוב". Nothing here is live.

## The shared board (boards 16 and 17): a site drawing sheet

- Drawing paper #F7F9FA with a fine grid, walls in ink #101820, a title block in the corner as on a real plan.
- One colour per person on marks, cursor and video frame: raspberry #B0144F, sea #2F6F86, site green #2E7D5B, marking yellow #E8B400.
- Faces: Rubik for numbers and measures, Assistant for text.
- Why it is not the default look: the language comes from a work sheet and red-pen markups on a plan, not from a generic whiteboard.
- Owner, 12.11.2026 night: only Claude Design, nothing that looks cheap. The first board.js screenshot (built before these boards) was rejected; code follows boards 15 to 17.

## Boards 18 and 19 (18.11.2026)

- Board 18, "a forum member opens an own card, and a visible video call": `canvas-source/MyCard.dc.html`, image `boards/board-18-*.png`. Built in 1.72.698 (inc/pro-forum-card.php). Checked on the live site with two test members: 9 of 9 (`docs/research/2026-11-18-arena/live-card-698/`).
- Board 19, "a video room every visitor sees, from the press to the invitation": `canvas-source/VideoRoom.dc.html`, image `boards/board-19-video-room-everyone-sees.png`. Parts: the band on the forum home, the row in every discussion and card, the lobby, "מי מצטרף?" (link, WhatsApp, share, discussion members, lock), what the invited person sees. Built in 1.72.699. Same palette and faces as the rest (ground #F2F4F5, ink #101820, raspberry #B0144F for what is live, sea #2F6F86 for actions; Rubik and Assistant). Why it is not the default look: the room is drawn as a notice on the building site's board with numbered steps in the site's own raspberry, not as a generic meeting tile.
- Lesson of 18.11: the first run on the live site showed the shared board white with invisible buttons, because its class `nlfb` belonged to the feature bar and the site skin paints that class. The prefix is `nlfsb` since 1.72.700. A board is checked on the live site, never only in a local lab.
