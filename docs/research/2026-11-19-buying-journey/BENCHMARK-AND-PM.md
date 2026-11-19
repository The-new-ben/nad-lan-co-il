# Buying journey, package 4 (HAD-788): world benchmark and product requirements

Date: 19.11.2026. Session: package 4 (Opus 5.5). Screenshots in `bench/`, taken on 19.11.2026: headless Chrome at 390 and 1440 wide
(`bench.mjs`), and the owner's Chrome at 1280 for the sites that block headless browsers (Tesla, Redfin, Damac). The deeper
26-product study from 11.11.2026 is `docs/research/2026-11-11-kikar-journey/benchmark-world.md`; its facts are cited, not re-checked.

## 1. Who is best at each part, and where we stood on 19.11.2026 (before)

| Part of the journey | Best in the world | Link, screenshot | What they do | nad-lan before this package |
|---|---|---|---|---|
| Configure, then one sticky order bar | **Tesla** | tesla.com/modely/design, `bench/tesla-chrome-1280.jpg` | Every choice updates one bottom bar: the car, the choices in one line, the price per month, one blue "Order Now". Three steps: design, summary, pay | Per-project drawer on Hebrew stage pages only; engine pages (DUO, Rainbow) have a separate 5-screen "build me an offer"; Kikar has a third flow |
| A bag that holds items from anywhere | **Apple Store** | apple.com/shop/buy-iphone, `bench/apple-bag-390.jpg`, `-1440.jpg` | One bag icon with a count in the header on every page; the bag lists every line, delivery and pickup, and one "Check Out" | No cross-project basket; the basket forgets you when you change project; not in ru/ar at all |
| Low-pressure first step, privacy said at the form | **Opendoor** | opendoor.com, `bench/opendoor-390.jpg` | "Takes 5 minutes", "Your information stays private", a counter of real customers | Privacy notice exists at forms; no time promise |
| Offer started online with a person behind it | **Redfin** | redfin.com/buy-a-home/offer, `bench/redfin-chrome-1280.jpg` | "Start an offer" online, an agent takes it from there | RFP document (he/en/fr), no ru/ar, not joined to the basket |
| Saved collections, "see it first" | **Compass** | compass.com, `bench/compass-390.jpg` | Collections shared with an agent; exclusive listings first | None |
| Reserve and pay a hold online | **Taylor Morrison**, Home Reservation System | blog.taylormorrison.com/home-buying/home-reservation-system/, `bench/taylor-chrome-1280.jpg` | "Add home to cart": lot, plan, options, finishes, review, then a refundable US$100 deposit with a 48 hour hold (11.11 study) | No reservation at all (gap 6) |
| Reserve off-plan in Dubai | **Emaar** (Vyom app: real-time availability, token payment, instant confirmation, 11.11 study); **Damac** | properties.emaar.com, `bench/emaar-1440.jpg`; damacproperties.com, `bench/damac-chrome-1280.jpg` | Filters by community, bedrooms, price; "Instant call" and WhatsApp in the header; token in the app | WhatsApp bar on every page; no token or reservation |
| Legal gate and documents | **Unlatch** (EU), **Yourkeys** (UK) | 11.11 study rows 14-15 (unlatch.com now redirects to a domain-sale page, 19.11) | Reservation documents, e-sign, ID checks, the conveyancer (lawyer) receives the file automatically | Nothing; no lawyer anywhere in the flow |

## 2. Product requirements I set for this package (my own PM list, Ben's "מוצר גמור")

1. One basket, "הסל שלי", in every project and every language (he, en, fr, ru, ar), right to left for he and ar. A count badge like Apple's; the basket remembers several projects at once.
2. Every way into the basket feeds the same store: the stage's floor and direction, package 3's shell slot, the engine's "build me an offer" buttons, the Kikar showroom, the designer (package 2), the rental plan (package 6). The old per-project baskets hand over to it, so nothing a buyer had collected is lost.
3. The order summary reads like a product order (Tesla, Apple): the apartment, the design, the services, the call, the price you typed and its purchase tax, with an edit link on every line, and the honest lines on what is not included.
4. Six services with real professionals where the directory has them, never a sample profile: mortgage, lawyer, interior design, inspection, moving, rental management.
5. A call booked inside the order: day, time window, phone, video or WhatsApp. Said as a request, never as a promise that someone already waits.
6. The RFP sent from the basket in all five languages, as a printable document with a reference number, an unguessable link, and a timeline that claims only what happened.
7. Reservation after the RFP: conditions and a deposit, three steps like Tesla. The conditions are marked "draft for a lawyer". The deposit is a simulation; no money moves; live charging does not exist in the code until Ben opens a provider and terms.
8. A lawyer gate: the reservation stops at "waiting for a lawyer". Only a user with the lawyer role ticks "אני עורך דין ומאשר", with licence number, and only then the buyer can continue. Administrators can see the queue but cannot approve (separation of duties). A switch lets Ben run the journey without the gate (the simulation he approved).
9. Privacy: the section 11 notice at the form itself, consent that names the recipients (the developer, the chosen professionals), no budget field, no personal data in events.
10. Brokers law: the site publishes and passes the request to the developer; no fee on a sale, no word presenting the site as a broker; a deposit, when real, goes to the developer's escrow only.
11. Events for package 5's developer report: basket_add, basket_remove, basket_open, rfp_open, rfp_send, call_book, reserve_start, reserve_request (no names, no phones, no typed text).
12. Phone first: a bottom sheet on the phone, a side panel on the desktop, 44 px touch targets, no scroll capture, keyboard and screen reader friendly.

## 3. After (to be filled with live evidence at the end)

See `AFTER.md` once the journey has been pressed on the live site.
