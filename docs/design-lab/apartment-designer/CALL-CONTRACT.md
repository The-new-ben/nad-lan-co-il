# The shared call: contract for other pages (HAD-706)

Owner of the module: the apartment designer session (HAD-701). Files: `plugins/nadlan-config/assets/designer/call.js`, `call.css`.
Other pages (project pages, the Kikar showroom, a broker page) only wire it. They do not copy it and do not restyle it.
Design source: `docs/design-lab/apartment-designer/call-design/` (12 boards as PNG, `boards.html`, `call-design.md`).

## What is stable (will not change without a note in `docs/coordination/claude-codex.md`)

```js
import { joinCall, livekitTransport, callSheet, receivePlan } from '/wp-content/plugins/nadlan-config/assets/designer/call.js?v=<plugin version>';

const call = await joinCall(designer, {
  container,          // an element inside the designer's shadow root (studio.js makes it: a div.ndc-host)
  transport: livekitTransport({ url, token }),
  room,               // the 12-character room id from the site (a-z, 2-7)
  identity,           // the identity the token route returned
  name,               // what the others see
  role,               // 'host' for whoever opened the room, 'guest' for whoever joined from a link
  lang,               // 'he' | 'en'
  mode: 'open',       // everyone may change the design; 'pen' is the older one-holder rule
  share: () => ({ plan, title, unitLabel, mine }),   // the apartment a newcomer receives
  inviteBase,         // the address the invite link is built on (default: the current page)
  onLeave,            // called once when the call is over for this person
});
call.leave(); call.openPanel('invite'); call.follow(true);
```

New options may be added. Existing ones keep their names and meaning.

## The two site routes (same origin, POST, JSON, header `X-NL-Designer: 1`)

| Route | Body | Answer |
|---|---|---|
| `/wp-json/nadlan/v1/designer/call` | `{page, name}` | `{room}`; limits: 6 rooms an hour per address, a daily cap; the owner gets one mail per room |
| `/wp-json/nadlan/v1/designer/call/token` | `{room, name, role: 'host'|'guest', identity?}` | `{url, token, identity}`; up to 8 people in a room; `503 {error:'off'}` when LiveKit does not answer |

The token comes from the site's shared LiveKit project. A page never holds a key, and a token is never printed or stored.
Rooms last six hours. On LiveKit they are named `nadlan-dsg-<room>`.

## The easiest way to wire a page

Do not call `joinCall` yourself. Mount the studio and let it open the call:

```js
import { mountStudio } from '/wp-content/plugins/nadlan-config/assets/designer/studio.js?v=<plugin version>';
mountStudio(host, pick, { rest: '/wp-json/nadlan/v1/designer/', lang: 'he', call: true, onCall: (what, studio) => {} /* 'joined' | 'left' */ });
```

- `?room=<id>` on the page address joins that room (this is what the invite link carries).
- A page that wants its own "video call" button opens `/tour/designer/?project=<slug>&unit=<id>` and lets the visitor press the
  designer's own call button, or links straight to a room it opened with the first route: `/tour/designer/?room=<id>`.

## Data topics (LiveKit data messages, JSON, one object per message)

| Topic | Delivery | What |
|---|---|---|
| `sys` | reliable | hello / state for a newcomer |
| `design` | reliable | one design operation `{op, rev, by, g, at}`; applied through the designer's store |
| `design-snap` | reliable | the whole design for a late joiner |
| `plan` | reliable | the apartment plan in 4,000-character pieces |
| `view` | lossy | a camera position, about ten a second |
| `ptr` | lossy | a pointer on the plan and on the 3D |
| `chat`, `hand`, `pen` | reliable | messages, raised hands, the older one-holder rule |

A page that puts its own shared object into a call (the Kikar showroom's tower and floor, for example) uses its OWN topic name
with its own prefix (`kikar-…`) through `transport.publishData(topic, obj, {reliable})` and `transport.onData(fn)`. It never
writes to the topics above.

## What a wiring page must not do

- No second LiveKit connection on the same page; one room per call.
- No recording, and nothing personal in a data message (the design log carries a role, never a name).
- No change inside `call.js` / `call.css`: ask in the coordination file.

## Checks

- `docs/design-lab/apartment-designer/check-call.mjs`: the logic on a stand-in transport.
- `docs/design-lab/apartment-designer/check-call-live.mjs --room=<id>`: two separate Chromes against the real LiveKit, local pages.
- `docs/design-lab/apartment-designer/check-call-live.mjs --live [--page=/design-studio/]`: the live site, nothing replaced.
  Each run opens one room and sends the owner one mail: keep it to a few runs.
