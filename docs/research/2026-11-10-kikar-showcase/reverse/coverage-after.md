# Coverage after the apartment cockpit (HAD-699, 10.11.2026)

Same 221 features as features.csv. Only features the cockpit implements AND that were checked in a local headless browser run (phone 390 and desktop 1440, scratchpad kikar/local/cockpit_test.mjs) change status. Not live yet: the cockpit ships behind ?kikar=next first.

| | before | after |
|---|---|---|
| present / partial / absent (of 211 that apply) | 66 / 68 / 77 | 76 / 66 / 69 |
| coverage, partial = half | 47.4% | 51.7% |
| weighted by buyer value | 53.2% | 58.5% |
| the 56 features that matter most (4-5): present / partial / absent | 27 / 17 / 12 | 33 / 16 / 7 |

## What changed, and how it was checked

| id | feature | before → after | what the cockpit does |
|---|---|---|---|
| F058 | Monthly service / common charges as a field | partial → present | maintenance fee field, 4,000-5,000 per Maariv, editable |
| F059 | Payment calculator split with HOA dues line | absent → present | cockpit price section: mortgage, arnona and maintenance lines and one monthly total |
| F077 | Inline mortgage calculator with editable deposit, rate and term | partial → present | financing %, years and rate are editable inputs with visible defaults |
| F078 | Monthly payment line next to the price | absent → partial | the monthly line is in the cockpit, not yet beside the page headline price |
| F142 | Personal buyer link or QR code | absent → partial | a link per choice, no QR yet |
| F154 | Instant call with sales from the project page | absent → present | cockpit asks /room/available; when a representative is on, the main button opens ?room=new (the shared video room) |
| F157 | Deep link per apartment | absent → present | #dira=<tower><floor>-<bearing> in the address; opening it picks the same tower, floor and direction |
| F159 | Compare units side by side | absent → present | save, pick another, the decide section shows both side by side |
| F161 | Share sheet with copy link and messaging apps | absent → present | navigator.share on phones, copy to clipboard elsewhere; the visitor chooses what goes in, no personal details |
| F168 | Save to wishlist (heart) | partial → present | save up to three apartments on the device |
| F169 | Share a link to the exact viewpoint | absent → partial | the link reopens the apartment and facing, not the camera angle |
| F215 | Sticky bottom reserve bar on mobile | partial → present | the cockpit action bar stays at the bottom: video call, WhatsApp, save |
| F218 | Section anchor tabs | partial → present | the section index is always visible in the cockpit and jumps to each section |

Honest limit: about half of the enumerated features are still partial or missing. The largest remaining gaps: real floor plans with room sizes, current listings with dated asking prices on the tower, photographed (not rendered) views, noise and environment data, travel time to the buyer's own places, an empty apartment and a ruler in the 360 (the walk lab has a laser measure, not live).

## Cockpit v2 (the same evening, after Ben's "the cockpit of his life")

The panel became a full-screen apartment app: the rendered view from that apartment on top, nine tiles (the view across floors
and directions, inside in 360 with four styles, the designer opened for that unit, the plan, the facilities in 360, price and
cost, the neighbourhood with walking directions, the project film, compare and send), the video call fixed at the thumb. The
journey (tower, floor, view) ends in it. Checked in headless Chrome on the local harness (phone 390x844, desktop 1440x900: every
tile opens and comes back, 0 script errors) and on the real gated page with these files served in place (phone 390x844, 0 errors).

| id | feature | before → after | why |
|---|---|---|---|
| F018 | Media chips on the hero (photos, video, 3D, plan, street view) | partial → present | the apartment's home screen opens view, 360, plan, facilities 360 and film from one grid |

Not counted, on purpose: F029 (finish packages with their price): the designer is linked per unit, but it shows no package
prices; F019 (video per residence line): the film is for the whole project. Coverage moves from 51.7% to 51.9% (partial = half);
the honest gaps listed above are unchanged.
