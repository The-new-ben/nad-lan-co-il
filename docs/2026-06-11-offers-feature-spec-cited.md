# "הצעות מחיר" — Non-Binding Home Offers Feature Spec (cited, 12 sources)

Owner directive: best-in-class offers feature, NOT a binding auction. Researched against Openn
(AU), iamsold MMoA (UK), Final Offer + Indigo (US), auction-theory evidence, and Israeli law.

## Model decisions (with evidence)
- TRANSPARENCY: per-listing setting `sealed | leading_amount | full_open`. Default = leading_amount
  ("יש הצעה מובילה מעל X") — captures the open-auction price effect (sealed bids fetch 1.2-9.6%
  LOWER prices: Chow/Hafalir/Yavas, Real Estate Economics) while letting a private seller stay sealed.
  (https://onlinelibrary.wiley.com/doi/10.1111/1540-6229.12035 , https://www.finaloffer.com/how-it-works)
- WINDOW: offer window with countdown that EXTENDS +24h on each new leading offer (anti-sniping;
  Openn final-stage pattern). (https://www.openn.com/en-au/how-it-works-for-buyers)
- QUALIFICATION: seller approves each buyer before the offer goes live (Openn registration gate);
  SMS OTP identity; optional financing-doc upload for a "מאומת" badge (Final Offer "Buying Power").
- NOTIFICATIONS: new offer→seller; counter→buyer; "הצעה חדשה קיימת"→all registered buyers (even
  without amounts, per Final Offer); window-closing-24h; connected (phones exchanged, with consent).
- EVERYTHING NON-BINDING until a lawyer-drafted contract offline. UI labels the offline close as
  "התמחרות אצל עורך הדין" — digitizing an accepted Israeli custom. (https://elkayamlaw.co.il/...)

## LEGAL (owner is a lawyer — final call is his; this is the risk map)
חוק המתווכים תשנ"ו-1996: תיווך = "הפגשה בתמורה... לשם התקשרותם בעסקה" (§2 license required; §14 fee
conditions). MITIGATION: (a) offers explicitly non-binding; (b) platform passes contact details only,
never negotiates/prices/attends; (c) revenue = FLAT listing/advertising fee paid regardless of
outcome — NO success fee (the יד2/מדלן advertising-fee theory). Not a statutory safe harbor; avoid
the word "תיווך" in UI; T&C declare an advertising board. Privacy: explicit consent before sharing
buyer phone; SMS = transactional only (חוק התקשורת §30א).
(https://www.nevo.co.il/law_html/law00/72991.htm , https://www.nevo.co.il/law_html/law00/229640.htm)

## Monetization (success-fee-free)
1. Flat/featured listing fee (sellers, upfront, outcome-independent). 2. Premium seller dashboard
subscription. 3. Buyer-lead packages to LICENSED brokers (they handle any תיווך under their own §9
engagement). 4. Later: partner-lawyer + mortgage-advisor leads. NEVER a % of price.

## MVP build spec (WordPress, flag nadlan_feature_offers default off)
- CPT `nadlan_offer` (admin-only UI). Meta: property_id, buyer_user_id, amount, financing
  (cash|preapproved|pending), occupancy_date, date_flexibility_days, conditions[], message,
  anonymous handle ("מציע #N"), phone_verified_at, consent_share_contact.
- Statuses: pending_review → live → countered ⇄ revised → connected | declined | withdrawn | expired.
- Listing settings: offers_enabled, transparency_mode, min_offer, offer_window_end (auto-extend), asking_price.
- REST nadlan/v1: POST /properties/{id}/offers (OTP + rate limit + honeypot); GET (seller full /
  buyer filtered by transparency); PATCH /offers/{id} (revise/withdraw | approve/decline/connect);
  POST /offers/{id}/counter; GET /me/offers.
- Seller dashboard: sortable comparison table (amount/financing/conditions/date), counter modal,
  "חבר בינינו" reveals phones to both sides (with consent) + notifies.
- Cron: window expiry + closing-soon digests. Full audit log of transitions.
- Reuses: lead delivery channel, signed-token pattern (Chunk D), audit pattern (Chunk E), rate-limit.

Sources: Openn how-it-works + pricing; iamsold fees; Final Offer how-it-works; Inman review; Indigo
PR; Nevo חוק המתווכים + תקנות אתיקה 2024; Chow et al. RE Economics; Athey/Levin/Seira; elkayamlaw
התמחרות; thebusinessprofessor sealed bids. (Full URLs in the research transcript.)
