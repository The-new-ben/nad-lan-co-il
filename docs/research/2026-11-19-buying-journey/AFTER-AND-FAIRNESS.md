# Buying journey (HAD-796, package 4): after the release, and the fairness declaration

Release 1.72.710, live since 19.11.2026 (second run, 0 failed rows of about 1,400). Follow-up 1.72.715 live since 19.11.2026 17:30 UTC (first run, deploy-result-715.json).

## 1. After: the same parts as the benchmark, measured on the live site

| Part | Best in the world (before table) | nad-lan after 1.72.710 | Evidence |
|---|---|---|---|
| One bag from anywhere | Apple: one bag, count in the header | "הסל שלי" in package 3's shell slot on every developer project page in he/en/fr/ru/ar, in the stage steps, and from the Kikar apartment screen's own bag button; a count badge; several projects in one basket; it follows the buyer to other pages once it holds something | live/B-desk-rainbow-gateon/01-basket.jpg, live/A-phone-kikar-gateoff/01-basket.jpg; runner rows on hamedina, hamedina-ru, rainbow-ar, duo, h-infinity, mortgage-calculator |
| Configure then summary | Tesla: sticky order bar, three steps | Three named steps (summary, request for proposal, reservation) with the step strip; every line of the summary has an edit link back to the basket | live/*/04-summary.jpg |
| Services | (none of the six benchmarked sites bundles services) | Six services in the order: mortgage, lawyer, interior design, inspection, moving, rental management; real directory professionals on Hebrew pages, never a sample profile | live/*/02-call.jpg |
| Call in the order | Emaar / Damac: instant call, WhatsApp | A day, a time window and a channel (phone, video, WhatsApp) saved inside the order, worded as a request | live/*/02-call.jpg |
| Price and tax | none in the six | The price the buyer typed, purchase tax recomputed on the server from the brackets in force (6,200,000 single home: 209,886) | B-desk-rainbow-gateon/21-certificate.jpg |
| Request for proposal | Redfin: start an offer online | Lead with the section 11 notice and consent at the form, then an order document with a reference (NL-XXXX-XXXX), printable, in the buyer's language, timeline of what happened only | live/*/07-sent.jpg, 08-doc.jpg |
| Reserve online | Taylor Morrison: refundable hold online | Reservation with five draft conditions stamped "draft for a lawyer", a lawyer gate, an example deposit that charges nothing, a confirmation with both stamps | A: 11-certificate.jpg (gate off, Ben's simulation); B: 10-after-reserve.jpg (waiting), 21-certificate.jpg (approved) |
| Lawyer in the flow | Unlatch / Yourkeys: the conveyancer gets the file | A lawyer role inside the site; the reservation stops until a lawyer user ticks "אני עורך דין ומאשר" with a licence number; the administrator sees the queue but cannot approve | live/gate-evhmpk.json: anonymous deposit 409, lawyer without the tick 400, lawyer with the tick 200; the administrator's call did not approve (405, status still waiting) |

Measured, not claimed: we did not run the same scenario inside Tesla, Apple, Redfin or Taylor Morrison accounts (no accounts, no payments; Redfin, Tesla and Damac block automated browsers). The "before" column is their public pages and the 11.11 study.

## 2. Live press test (19.11.2026, real taps on the live site, test identity only)

- A, phone 390, Kikar, gate OFF (Ben's simulation): opened through the page's own shared link, bag button on the apartment screen, three services, call, price, summary, request sent (NL-WBQ6-F99E), order page, reservation, "approved without a lawyer review (example run)", example deposit, confirmation. 13 screens in live/A-phone-kikar-gateoff/.
- B, desktop 1440, Rainbow, gate ON: shell slot, the same steps, request sent (NL-EVHM-PKZT), reservation stops at "waiting for a lawyer" with the deposit button locked; a test lawyer user (role nadlan_lawyer) approved with a licence number; the buyer's page then opened the example deposit and the confirmation. Screens in live/B-desk-rainbow-gateon/.
- Harness on live pages with the local files before the release: he phone and desktop, en, fr (DUO), ar (Rainbow), H Infinity desktop: no script errors.
- Content-first check after the release: Rainbow and H Infinity pass on phone and desktop. Kikar fails (paragraph at 2,622 px on a phone) with the cart switched ON and OFF alike: it predates this release (the full-screen showroom sits above the paragraph). Reported as a finding.
- Source audit after: the only differences are basket.js -> cart.js on project pages, and +2 small inline scripts (the cart's config and loader) on other pages.

## 3. Fairness declaration (signed: Claude, package 4 session, Opus 5.5, 19.11.2026)

Proven on the live site, with evidence in this folder:
- The basket, summary, request for proposal, order document, reservation, lawyer gate and example deposit work end to end on a phone (Kikar) and a desktop (Rainbow), in Hebrew.
- The gate refuses an anonymous deposit and a lawyer who did not tick the box, and opens only after a lawyer user's approval.
- No money moves: there is no payment-provider call in the code; the deposit is recorded as an example with charged = false.
- The config and the basket script are printed on Hebrew, Russian and Arabic project pages and on a non-project page (runner rows).

Not proven, or found broken:
- On Kikar, the apartment chosen through the shared link did not enter the basket in 1.72.710. Fixed in 1.72.715 and pressed live on a phone: the basket shows "קומה 24 · מגדל B · פונה למערב" (live/C-phone-kikar-dira-715/).
- The two test orders (NL-WBQ6-F99E, NL-EVHM-PKZT) and their leads were removed after 1.72.715 (the purge route now finds private orders); both order pages return 404. The lawyer gate is back on.
- English, French, Russian and Arabic were pressed in the harness (local files on live pages), not in the live press test after the release.
- The wp-admin lawyer desk was not opened in a browser: the approval was made through the same code path by REST with a test lawyer user. No screenshot of the desk.
- The administrator's refusal returned HTTP 405, not the 403 the code returns; the outcome (no approval) is proven, the cause of the 405 is not.
- Package 2's design order and package 6's rental plan entering the basket were tested only with fixtures in the harness, not with their live tools.
- Real professionals in the services row were not pressed in the live test (the test chose services without a named professional).

Not done, by design, and waiting for Ben:
- Real deposit amount, provider and live charging (option nadlan_cart_deposit_ils is empty; live charging does not exist in the code).
- The conditions are a draft for a lawyer (version "draft 1, 19.11.2026"). The real support team and terms are Ben's.
- A real lawyer user: none exists; the test lawyer user was deleted.
