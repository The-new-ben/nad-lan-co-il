# Owner live alerts and live screen: plan (HAD-791 follow-up, Ben's voice note 20.11.2026)

Status: PLAN ACCEPTED by the coordinator 20.11.2026 with three changes (below). Build only after the coordinator has seen the
Claude Design board and shown it to Ben. Board: https://claude.ai/artifact/7fdnJgxn8scFBeM63vyD9e

Coordinator's changes (they override the sections below):
1. Until phone push or the Telegram bot is on, MAIL is the fallback for every visit that reaches an instant event: one mail per
   visit on its first instant event (not only money steps), under the burst rule. Once push or Telegram works, mail goes back to
   money steps only.
2. The first alert of a visit names the page by its human name and where the visitor came from, in Hebrew, readable in the
   phone's notification line without opening anything ("ריינבו תל אביב · הגיע מגוגל").
3. The board shows the lock-screen notification, the live screen with visits in different states, and the one-time setup steps
   (Allow, Add to Home Screen, the Telegram bot) as pictures. Rentals names accepted; the privacy sentence stays non-blocking.

## 1. What the owner gets today (read from the code, 20.11.2026)
- Instant mail with a lead card for every form lead, concierge question and price-window sign-up (owner-mail.php, HAD-687).
- Instant "מבקר חם" mail only on listing pages (post type nadlan_property): a WhatsApp or phone tap, or a visitor who returns on
  another day. At most 6 a day, one per visitor and listing per week (owner-morning.php nadlan_om_hot).
- The morning mail at 08:00: leads, listing views per listing, technical notices.
- The visit trail (nlTrack, mine) records project pages, 3D, floors, view, designer, mortgage, basket, call, RFP and language on
  every page, but it only shows up in wp-admin "מסלולי ביקור" and the developer report. It never alerts.

Missing: no alert for anything on a project page (3D, floor, apartment, view), the designer, the basket, a video call or the rentals
tool; no message that reaches his phone apart from mail; no live screen; no way to keep his own phone out when he is not signed in.

## 2. What alerts at once, what goes to the digest
Instant (the first one in a visit opens the alert):
- Entered a project's 3D (stage opened, tour, floor chosen), chose an apartment, opened the view
- Opened the designer, added to the basket, started a video call, asked for a reservation or an RFP
- Opened the rentals tool, signed up there, added a property (names below)
- Left details (the lead card mail stays as is; the alert of that visit links to it)
Digest (morning mail plus the live screen only): page views without a step, the mortgage check, language changes, a change of
direction, scroll depth, opening other tools.

One visit = ONE alert that updates. The visit id already exists. The first instant step sends one message; every later step in the
same visit EDITS that message (Telegram editMessageText) or replaces it (web push with the same tag), as a growing line:
"ריינבו · טלפון · עברית · מגוגל: קומה 13 → נוף מערב → דירה 4 חד׳ → סל". Mail cannot be edited, so mail goes out once per visit, and
only for a money step (basket, call, RFP, reservation, details).
Excluded: robots (the existing check plus no event without a real press), signed-in staff (already), and his own phone through a
"זה הטלפון שלי" switch on the live screen that marks the device (localStorage), so his own visits never alert.
Guard: if more than 40 visits alert within an hour (a burst or a bot), new ones go to a single summary message until it calms down.

## 3. Channel to his phone (all free)
- Mail: works today, no change.
- Web push to his own phone (recommended first): needs nothing from him except opening the private live screen on his phone once
  and tapping "allow". On an iPhone, first "Add to Home Screen" (iOS 16.4 or later). The keys are made on the site; the only
  carriers are Apple's or Google's push service, and the content is encrypted end to end.
- Telegram bot (option, the best "one message that updates"): he opens @BotFather in Telegram, creates a bot (2 minutes), pastes the
  token himself into wp-admin, and presses Start on the bot. The agent never sees the token.
- WhatsApp is not offered: alerts sent by a business through the WhatsApp Cloud API are paid per message.

## 4. The live screen
One private page behind a signed link (the same signing as the developer report; revocable; not linked from anywhere; no change to
indexing rules). Newest first, one strip per visit (project, device, language, source, the steps as a line, minutes ago), the
money steps in a strong colour, refresh every 10 seconds, one thumb on a phone. Claude Design board before code:
- Palette: signal white #F4F6F8, ink #0D1B2A, cobalt #1E4FD6 (3D and project steps), teal #0B7A6F (money steps), signal red
  #D2352A (a live visit in the last 2 minutes), rule #B8C4CF.
- Faces: IBM Plex Sans Hebrew for words, IBM Plex Mono for times and counts.
- Why not the default look: the form is taken from air-traffic flight-strip boards (one strip per visit, moving down as it ages), not
  cards on cream; it is the same family as the developer report, so the owner's two screens read as one product.

## 5. Privacy
Only what the visit trail already records; no new field, no IP, no name for anonymous visitors. Showing the record to the site owner
is the site's own use, which the live notice already covers ("not sold and not passed to anyone"). For signed-in landlords in the
rentals tool, the alert shows the account's display name only (their own account with the site). One question for the lawyer in
HAD-797: whether the notice should add one plain sentence "the site's operator may see the activity in real time". Not blocking.

## 6. Rentals event names (for the rentals session, through nlTrack; proposal)
rent_open, rent_signup, rent_property_add, rent_lease_add, rent_tenant_invite, rent_doc_add, rent_pay_mark, rent_repair_open.
Instant: rent_signup, rent_property_add, rent_lease_add, rent_tenant_invite. Digest: the rest.

## Build and release (after the coordinator reads this)
inc/owner-live.php (new, loaded from visit-trail.php like dev-report.php): the alert hook after nadlan_vt_store (sent after the
response is finished, never slowing the visitor), web push (VAPID, aes128gcm with openssl), the optional Telegram sender, the signed
live screen and its feed route, the admin settings. trail.js: the "my phone" switch. Tests in build/, one release through the queue,
source audit before and after, Rainbow and H Infinity spot check, and a live proof with a real press and a real alert on his phone.
