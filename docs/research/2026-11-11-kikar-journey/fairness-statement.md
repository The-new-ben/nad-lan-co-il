# Fairness statement: the Kikar HaMedina purchase journey (HAD-712, 11.11.2026)

Ben's order: before building, check everything we already built, check the best sites in the world, and say plainly what is taken
from where. Nothing below is invented; every line points at a file, a live page or a URL.

## 1. What was checked, and how

| What | How | Where the evidence is |
|---|---|---|
| Ashira, DUO, Rainbow, Dimri and Kikar as a phone visitor (390 x 844, touch) | Headless Chrome driven step by step on the LIVE pages: landing, the stage, a tap on the tower, the floor card, "the view and the map", the basket, the specific-apartment inquiry | `evidence/*.jpg`, `evidence/*.mjs` (the scripts that produced them) |
| The stage code of the four older pages and Kikar | Read with file:line by an Opus agent | `inventory-stage.md` |
| The video room, the basket, RFP, payments, the home film | Read with file:line by an Opus agent | `inventory-commerce-call.md` |
| 26 products in the world that sell or reserve a new apartment online, 35 scored parameters, the Israeli law on holding fees, usability studies | Public pages only, each row labelled "saw it" or "their documentation" | `benchmark-world.md` |
| Thumb and gaze rules for a property buyer on a phone | The 36 sourced rules of the buyer-gaze-ux skill | `docs/research/2026-11-10-kikar-showcase/ux/` |

Not checked: real analytics counts (no export exists in the repo), a real phone in the hand, the 3D selectors of the world's
products (their viewers need a real browser session; the benchmark used their documentation), the live `together.php` (the repo
copy is behind the live one).

## 2. What already worked on our own pages, and is taken as is

| Taken | From | Evidence |
|---|---|---|
| One tap on the tower chooses the floor; the floor lights up on the building; a card opens at the thumb | Ashira, DUO, Rainbow (`assets/project-stage/ashira/stage.js:1072-1359`) | `evidence/06-mouse-a.jpg`, `13-picked-min.jpg` |
| The floor card: the facing in words, three actions (enter the apartment, the view and the map, design) and "לקבלת תוכניות ומחירים" for THIS apartment | `bridge.js:157-166, 305-312, 606-611` | `evidence/06-mouse-a.jpg`; the WhatsApp text read live: "…לדירה בקומה 22 בפרויקט אשירה שדה דב, לכיוון הים" |
| The numbered steps strip under the model (1 floor, 2 view and map, 3 inside, 4 design) that moves by itself after each step | the stage pages | `evidence/06-mouse-a.jpg` (step 2 lit after the pick) |
| The beam: a cone on the map from the building towards what the apartment faces, the map turning that way | `bridge.js:754-782` (`showBeam`) | `evidence/14-nlpjx-unimap.jpg` |
| "The view from this floor" beside the map, with the list of what lies that way | `bridge.js` | `evidence/08-view.jpg` |
| The apartment basket: building, apartment, design, team (designer, lawyer, appraiser), price; "send the basket", "a shared viewing room" | `inc/basket.php`, `basket.js` (live on Ashira, DUO, Rainbow; loaded on Kikar with no button) | `evidence/10-basket.jpg` |
| The apartment's identity in the address (`?unit=`) and in the WhatsApp pill | `inc/cta-sheet.php:146-148` | `inventory-stage.md` |
| Door hotspots between 360 rooms | `tour.js` (Ashira, DUO, Rainbow) | `inventory-stage.md` |
| Facility pins and neighbour pins on the model, tappable from outside | `ashira/stage.js:1815-1977` | `evidence/02-tour-open.jpg` |
| The video room (LiveKit): invite by link, up to 12 people, roles, "follow me", notes | `inc/together.php` | `inventory-commerce-call.md` |
| Payments in ILS: WooCommerce with Morning (card, Bit, Google Pay, Apple Pay) | live, verified 7.11 (HAD-678) | `inventory-commerce-call.md` |
| Kikar's own apartment screen (nine tiles), the 96 window views, the 48 living rooms in 360, the real Blender city | this session's releases 1.72.636 to 1.72.642 | the live page |

## 3. What Kikar lost when it moved to its own model (mine to own)

1. The beam on the map under the model.
2. Choosing the apartment on the building itself; on phones Kikar shows a picture, a slider and a list.
3. The steps strip, so the visitor no longer sees what comes next.
4. The basket button (the script is loaded and even records the apartment, but nothing opens it).
5. The apartment in the WhatsApp message and in the address.
6. Room to room in 360, and facilities and neighbours tappable from outside.

## 4. What is new, because nobody has it (not us, not the 26 products)

| New | Why it is needed | Evidence that it is missing elsewhere |
|---|---|---|
| EACH tower turns on its own (a photoreal turntable of 24 Blender frames per tower, the real city around it) | Ben's order; three towers hide one another in one model | `inventory-stage.md` (a): "exists nowhere"; benchmark white space: "No product turns a 3D tower separately per building" |
| A pulse on the next thing to tap, at every step, that stops once the visitor acts | Ben's order; no stage page has any | `inventory-stage.md` (d); NN/g: contextual signposting beats tutorials, a permanent pulse competes with the task |
| A map ATTACHED to the model on the phone, the beam moving while the finger moves | on phones the old map sits far down the page | `inventory-stage.md` (c) |
| One tap that really reaches the owner: an alert with an "answer" link | today nothing alerts anyone (`together.php:387` fires an event nobody listens to) | `inventory-commerce-call.md` 1.4 |
| The whole flow on one phone screen sequence: tower, apartment, map, inside, design, basket, hold | benchmark white space: nobody documents it | `benchmark-world.md` |

## 5. Patterns taken from the world (rebuilt by us, no code or asset copied)

| Pattern | Seen at | How we rebuild it |
|---|---|---|
| A small, fully refundable hold with a clock | Taylor Morrison ($100, 48 hours) | the last step of the basket; amount, clock and refund in plain words inside the panel |
| Refund terms in plain words with dates | St Modwen | the same panel, not a separate legal page |
| Saying exactly when the unit is held | Mirvac | "held only after the payment succeeds" |
| A running total that changes with every choice, then an itemised review | Taylor Morrison | the basket's price step already does half of it |
| A 2D floor list beside the 3D | Cockburn and McKenzie; Spark | a floor stepper beside the turntable |
| Tap a room on the plan to jump into its 360 | iGUIDE | the plan tile and the door hotspots |
| The view from the unit's own balcony | Volume Vision, 3DEstate | already live on Kikar (96 window views, 48 living rooms) |

## 6. What only the owner can decide (found, not hidden)

1. The holding fee. Our own recorded rule says the site never charges the buyer and never presents itself as a broker; since 9.3.2025
   the broker ethics regulations forbid a broker to collect "דמי רצינות"; whether a site that is not a broker may hold a third
   party's money is not answered by any source found. Ben said on 11.11.2026 that he approves the purchase flow to the end and takes
   responsibility. The flow is built to the payment step; the legal form of the fee (who holds it, what it is called, the refund
   rule) is his to set before real money is taken.
2. WhatsApp wording is his by his own rule; the apartment-specific text reuses Ashira's approved sentence.
3. Availability for video calls is a manual box in wp-admin today; real "ringing" needs him to choose where the alert goes.
