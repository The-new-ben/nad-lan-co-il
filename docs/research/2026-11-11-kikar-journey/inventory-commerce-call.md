# Kikar journey: inventory of call, commerce and payment code (11.11.2026, read-only)

Repo: nad-lan-co-il, branch claude/apartment-experience-b1 at cb4ad62f. Paths below are under plugins/nadlan-config/ unless stated.
Caveat: the repo is not the live site. The live together.php gets LiveKit tokens from the Supabase function nadlan-room-token
(option nadlan_tr_lk_proxy_secret, release 1.72.463, docs/coordination/claude-codex.md:4373). Neither this branch nor
origin/main contains that proxy code. Read live before any change (memory nadlan-kikar-showcase-had699).

## 1. The video call today

1. Cockpit opens (nl:facing from world.js:1964 / journey.js:133; cockpit.js:304). show() calls askAvail(); cockpit.js:58-59
   fetches C.avail = /wp-json/nadlan/v1/room/available (inc/project-stage.php:1188).
2. /room/available returns now = option nadlan_tr_rep_now (inc/together.php:593-600, 51). That option is ONE manual checkbox
   "נציג זמין עכשיו" in Settings > חדר צפייה משותף (inc/together.php:760, 774). Not presence, not a schedule.
3. paintBar (cockpit.js:232-237): now:true gives the link ?room=new (keeps #dira); otherwise '#nlsch', and the click scrolls to the
   scheduler band (cockpit.js:299).
4. ?room=new loads together.js (inc/together.php:653-676, only when nadlan_ps_current()). The visitor POSTs /room
   (inc/together.php:365-390): allowed only while rep_now=1, 4 rooms per hour per IP; creates the private post nadlan_room; fires
   do_action('nadlan_together_room_created') at :387.
5. NOBODY LISTENS to nadlan_together_room_created (grep: only the do_action). No mail, push, WhatsApp, SMS or owner-mail card.
   The visitor sees "הנציג עוד לא בחדר. אפשר לשלוח לו הודעה בוואטסאפ עם הקישור לחדר" (together.js:52, 769-770) and a
   wa.me button with the room link. So the only "ring" is the visitor sending a WhatsApp message by hand.
6. To answer, Ben must be logged in with edit_posts and open the same ?room=<id> (role rep, together.php:410). He learns the
   id only from that WhatsApp message or from the admin room list (together.php:795ff).
7. Third person: "הזמנת משתתף" copies or shares join_url (together.js:63-64, 104-105). They join with a name and a role
   (buyer, partner, friend, designer, engineer, lawyer; rep only for edit_posts). No sign-up.
8. At most 12 active participants (together.php:425, error 'full' 409). Rate limits: token 30 per 10 min per IP.
9. Shared: LiveKit video and audio; the leader's view ("עקבו אחריי") over the data channel about 10 times a second; notes pinned to points, kept
   in the room file (/room/file, ?file=1), sent on WhatsApp. The shared state needs window.__nlpsStage (together.js:300, 467), which
   only bridge.js sets. The Kikar world branch prints no bridge.js (project-stage.php:1049, 1597). So on Kikar the room
   should give video but no shared 3D view or anchors (inferred from code, not tested). No screen share (no setScreenShare*).
   No design sharing (the designer has getView/setView; HAD-706 is not built).
10. A room closes after 6 hours idle (transient). Rooms are deleted after the retention days (default 30).
11. #nlsch (inc/scheduler.php) books a WhatsApp video call. Email notices are OFF by default (nadlan_scheduler_notify_enabled=0,
    scheduler.php:237-246) and always logged. Bookings are mirrored into nadlan_lead.

Missing for "one tap rings Ben":
- (a) a listener on nadlan_together_room_created that alerts him. owner-mail nadlan_omx_send exists (inc/owner-mail.php:267); a WhatsApp or push channel does not.
- (b) real presence instead of a manual checkbox.
- (c) a rep-side "answer" link (signed, opens ?room=<id> as rep).
- (d) a timeout fallback to #nlsch.
- (e) the world branch exposing a stage-like handle for the shared view.
- (f) a video button in the Kikar hero, which has none today (project-stage.php:1211-1215).

How to test end to end without a visitor: use two browsers, one logged in with edit_posts and one private window. Tick rep_now on a
staging copy or locally (scripts/together/router.php + php_selftest.php; the memory records a proof with a local livekit-server 1.13.7).

## 2. Chain "apartment chosen -> holding fee"

| Link | Status | Where | Used on |
|---|---|---|---|
| Pick tower/floor/facing | EXISTS | world.js:1955-1964, cockpit.js:249-252 (#dira=A30-262) | Kikar |
| Price/cost calculator, share text | EXISTS | cockpit.js (scrPrice; share at :285-297) | Kikar |
| Save/compare (localStorage) | EXISTS | cockpit.js:279-283 | Kikar |
| Design the apartment | PARTLY | assets/designer/designer.js:25 mount(), onSend/onCall hooks :138-139; only plans/example-4r.json; inc/designer.php and its REST routes not built; wired to no page (commit 0b289fcc) | none |
| Basket (unit, style, team, price+tax) | PARTLY | inc/basket.php, assets/basket/basket.js; listens to nl:facing (:47); its openers (.nlps-steps, #nlps-view-cta, hero-video, :398-406) are absent on the world branch | stage pages (Rainbow, DUO, Ashira...); on Kikar loaded with no opener |
| Team of pros | PARTLY | GET /basket/pros (basket.php:43); room roles designer/engineer/lawyer | stage pages |
| Lead | EXISTS | /nadlan/v1/lead | all |
| RFP document | PARTLY | inc/rfp.php:215 create, :334 render; needs lead id+key (:111-120) and a unit id in meta project_3d_units or in nadlan_ps_unit_resolve (rfp.php:241), which is NOT DEFINED anywhere in the repo; design v1 accepted (:130) | showroom engine pages (buyflow.js:246, studio.js), e.g. utopia-sde-dov |
| Cart for the unit | MISSING | the Woo cart is used only for ad products (advertise-tiers.php:567-578) | - |
| Holding fee product/order | MISSING | no deposit or holding code; basket.js:348 says money for the apartment goes only to the escrow account | - |

Data that travels today: the cockpit carries tower, floor and bearing (#dira). The basket carries floor, bearing, unit?, label, style, team, typed
price, buyer type and lawyer fee (localStorage only). There is no unit id on Kikar, no price per unit, and no design in any server record.

## 3. Payments

WooCommerce (ILS) with Morning/GreenInvoice gateways (card, Bit, Google Pay, Apple Pay), live. Checkout was verified on test
order 8808 (7.11, HAD-678) with tools/checkout/checkout_check.py and cancel_test_order.py. Products: 475, 476 (349/month), 477 (749),
489 (3,990), 490 (299), 5403 (199). The Morning business is an exempt dealer (receipts only, no VAT).

Stripe: only a webhook signature verifier in inc/greeninvoice-recurring.php:54-82 and the Paid Member Subscriptions plugin's Stripe JS. This plugin has
no Stripe checkout for a product. The pattern for tying a product to a card is the advertiser order bridge, inc/advertiser-orders.php (product to card meta).

A "holding fee for unit X" would need:
- a Woo product (or a Morning payment link);
- cart item data: project, unit, floor, facing;
- order meta and refund rules;
- a link to the lead and the RFP;
- above all, a legal decision (see section 5).

## 4. Films

Home band (inc/home-v3.php:712-732): the file comes from the option nadlan_home_video_url. Its live value is not in the repo; the 27.9 handoff names
uploads/2026/07/nadlan-promo-v2.mp4, 38 s. The promised steps are 1 בוחרים קומה, 2 הנוף והמפה, 3 נכנסים לדירה,
4 מעצבים את הדירה, with a CTA to Rainbow. No script for promo-v2 was found.

Developer film v3 (/marketing/#film, docs/sales/developer-film-v3/SCRIPT.md): the buyer searches in his own language, then lands in the 3D stage,
picks a floor, sees the view, furnishes and leaves notes, sees prices and the neighbourhood, books a live video call in the page with one tap,
arrives as a lead who already chose, and the team escorts him to a signed contract.

## 5. Legal and privacy already written

- Brokers Law s.2(c): never present the site as a broker; never charge the buyer anything; fixed fees only (memory nadlan-brokers-law-exemption).
- Sale Law: apartment money goes only to the project escrow against a guarantee (basket.js:348; memory nadlan-buying-journey-vision).
- Privacy Amendment 13: the s.11 notice is required at the point of collection, and the notice on the form is still the top open exposure. Developers are
  independent controllers, and spam consent does not transfer (memory nadlan-lead-privacy-obligations).
- Room: not recorded; the call is with NadLan's team, not the developer; changes are subject to the developer's approval (together.php:27-28).
- ConsultSheet stores nothing (cta-sheet.php). Saving a design must not need contact details (ARCHITECTURE.md 10b).
- Morning: exempt dealer, so never quote "+ VAT". Collecting money for others needs the owner's legal and tax decision.
