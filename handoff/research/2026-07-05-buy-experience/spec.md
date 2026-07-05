# Buy experience: research verdict + screen spec (2026-07-05)

Deep-research pass over Amazon, Booking, Wolt/DoorDash, Uber/Gett, Tesla/NIO
configurators, StockX, Zillow contact flows, EasySend progressive forms.

## Ten transferable patterns
1. Stored-profile one-click (Amazon): returning buyer = one tap from 3D unit to RFP.
2. "You won't be charged yet" (Booking): put "חינם, ללא התחייבות, ללא תשלום" under every CTA.
3. Total-price transparency, estimate-labeled (Booking + FTC 2025): running estimated
   total incl. upgrades and advisor fee ranges, always tagged "אומדן בלבד".
4. Configure > Summary > Reserve (Tesla): 3D unit is the hero; "בנו לי הצעה" is the
   zero-payment reserve step.
5. Choice-framed upsells: finish levels, designer bundle, furniture interest = the
   referral-revenue engine; chosen, never pre-checked.
6. Name-your-terms intent capture (StockX): budget bracket + timeline turn a browser
   into a qualified counterparty.
7. Staged live tracker (Wolt): RFP stages - generated > sent to contractor > viewed >
   proposal received.
8. Motion during waiting (Uber/Gett): animate the RFP traveling to each professional.
9. Progressive profiling, 2-3 fields per step (EasySend): name + WhatsApp first,
   everything else after value is delivered. WhatsApp OTP doubles as opt-in.
10. "What happens next" confirmation + 5-minute-response SLA promise.

## Screen-by-screen (v1)
1. Unit panel CTA "בנו לי הצעה" + reassurance line. Premium developer tier = richer
   media, verified badge, priority.
2. Configure, one decision per screen, all skippable, running estimate pinned:
   finish level (3 cards) > designer bundle (before/after) > advisors (lawyer,
   mortgage, inspector; fee ranges; never pre-checked) > furniture interest.
3. Contact: first name + WhatsApp (2 fields), WhatsApp OTP; email optional framed as
   "לאן לשלוח את המסמך"; budget/timeline optional "improves your proposals".
   Per-recipient consent checkboxes (Israeli privacy law). Guest-first.
4. Dispatch animation (5-8s, skippable, real backend events): analyzing > document
   ready > flying to contractor > advisors light up. Footer: response SLA.
   The waiting moment showcases advisor profiles = marketplace sells itself.
5. RFP shown inline + PDF by email + link by WhatsApp. Developer branding on premium
   docs. Printed disclaimers: estimates only, not an offer, subject to contract and
   developer spec (מפרט מכר), 30-day validity.
6. Status timeline page (persistent WhatsApp link): sent > viewed > proposal >
   advisor responded > meeting. WhatsApp pings per stage; 48h nudge; cross-sell
   advisors not yet chosen.

## RFP document contents
Header: RFP ID, date, validity, channel prefs, consent record, estimate disclaimer.
Unit: project, developer, building, floor, unit, rooms, net/gross sqm, balcony,
parking, storage, orientation, floor plan + 3D snapshot.
Configuration by trade: finish selections, upgrade deltas, designer scope, furniture
interest, special requests (accessibility, ממ"ד use).
Buyer intent: budget bracket, equity range, pre-approval status, occupancy date,
decision window, purpose.
Requested response + response-by date.
Per-advisor annexes, data-minimized (each sees only what they need).

Build order: (1) CTA + configure + contact + lead wiring into existing
nadlan/v1/lead + ledger; (2) RFP generator (AI document) + dispatch animation;
(3) status timeline + WhatsApp pings; (4) professionals upgrade feeds the advisor
cards (profiles, response times, ratings).
