# Slice 1: the live test with real data, and the proof that it leaves nothing behind (HAD-795)

Coordinator's condition (20.11.2026): a test apartment in the administrator account is allowed only if it leaves nothing behind, proven by a before and after snapshot. Touch no row this session did not create.

## What removal paths exist (read in the code, inc/rentals)
- `nlrm_delete()` (store.php:886) is a soft delete, and it refuses ledger rows ("the books are never deleted"). So a test payment cannot be removed by id.
- `POST /rm/erase` with `confirm=ERASE` (rest.php:448) deletes EVERY row of the owner in the eleven tables (properties, units, contacts, leases, ledger, tickets, docs, events, links, tasks, members) and unlinks the owner's document files. It is all or nothing for the account.
- Therefore the only complete path is erase-all, and it is acceptable ONLY while the account holds nothing but the test rows.

## Snapshot BEFORE (20.11.2026 about 09:20 IL, read-only, from the live app's own loaded data in the owner's Chrome, signed in as administrator)
properties 0, units 0, contacts 0, leases 0, ledger 0, tickets 0, tasks 0, docs 0, events 0, personal links 0; role owner; not the demo portfolio. Not readable from the app: the members table (the erase covers it; expected 0, no team feature is in use).
Totals: year income 0, open repairs 0, documents 0.

## Procedure (to run in one sitting, in the owner's Chrome as administrator)
1. Re-read the counts. If ANY is not 0, stop: Ben or someone added data; do not create and do not erase; tell the coordinator.
2. Create through the app's own screens or its own adapter: property "דירת בדיקה, למחיקה", one unit, one contact "שוכר בדיקה", one lease with index linkage (a base index entered by hand).
3. Run for real: (a) the new landing screen's "לצלם תקלה" with a small generated test image = `POST /rm/today/repair`; (b) "לחשב לפי המדד" then "לאשר את שכר הדירה החדש" = `POST /rm/today/index-confirm`; (c) "התקבל" once = `/rm/pay`. Record every response and the id of every row created. Press each in Hebrew, then check the English strings on the same screens.
4. Re-read the counts and confirm they equal exactly the rows created (no stranger rows). If a stranger row exists, stop and report; do not erase.
5. `POST /rm/erase` with `confirm=ERASE` (the app's Settings has the same action). Re-read the counts: every one 0, totals 0; check the test photo's document URL answers 404 or 403.
6. Write the before, during and after table here, and send it to the coordinator.

## Result (run 20.11.2026, one sitting of about 12 minutes, the owner's Chrome, signed in as administrator, live 1.72.722)

| Table | Before | With the test rows | After the erase |
|---|---|---|---|
| properties | 0 | 1 (id 1, "דירת בדיקה, למחיקה") | 0 |
| units | 0 | 1 (id 1) | 0 |
| contacts | 0 | 1 (id 1, "שוכר בדיקה") | 0 |
| leases | 0 | 1 (id 1, index-linked) | 0 |
| ledger | 0 | 4 (three rent charges the engine made for Sep to Nov, one payment, id 4) | 0 |
| tickets | 0 | 1 (id 1) | 0 |
| docs | 0 | 1 (id 1, the test photo) | 0 |
| events (as the app loads them) | 0 | 3 (index_confirmed, money, doc_new; all by the administrator) | 0 |
| tasks, personal links | 0 | 0 | 0 |

Safeguards as run: counts all 0 right before creating; every row checked to belong to the test property, unit and lease right before erasing ("only mine" true, counts exactly as expected); `POST /rm/erase` answered 200 `{"erased":true}`; the app reloaded on the empty "ברוכים הבאים" screen with every count 0; the test photo's address answers 404 after the erase (403 before: it is not public). The members table cannot be read from the app; no member was created.

What the routes returned with real data:
- `POST /rm/today/repair` (through the screen's own camera input, a generated 8 x 8 PNG): a repair "תקלה חדשה, עם תמונה" (ticket 1, status new) with its photo (doc 1, kind photo) in one request; the landing screen switched to the open-repair state ("יום 1 מתוך 30 · לתקן עד 20.12.2026") and listed it under "נעשה לאחרונה". No console errors.
- `POST /rm/today/index-confirm` (called directly, see the defect below): 200 with a journal event `index_confirmed` (lease 1, start month 2027-01, base 100, applied 101.9, old 780000, new amount per the contract rule); the same call again returned the SAME event id (no double write); a wrong amount was refused with 409 "הסכום לא מתאים לחישוב לפי החוזה". The ledger count did not change.
- "התקבל" on the tenancy ruler (the existing `/rm/pay`): one press, one payment row of 7,800, September shown "שולם במלואו", open debt 15,600.

Defects and gaps seen:
1. The index confirmation could not be reached from the screen in this state: "לחשב לפי המדד" is offered only when the screen decides an update is due, so with an overdue rent and an open repair there was no button. The route is proven, the press is not. Fix: an index row on the tenancy screen that is always reachable for an index-linked lease.
2. With no parts recorded the title block says "עוד לא הוספתם מכשירים ומערכות לדירה" and offers "להוסיף תוכנית"; correct, but there is no one-press way to add the first part from there.
3. Desktop: the inner scrollbar on the system-icons row (seen earlier in the sample portfolio).
Not measured on a real phone. The English strings were not pressed in this sitting.

## Second sitting (20.11.2026, live 1.72.725): the index button and the one-press part with REAL data
Coordinator's yes of 20.11 with one hard stop (any row in the account before creating = stop; Ben's data is never erased). One sitting, the owner's Chrome, signed in as administrator; the machine's screen is 538 px tall, so the layer was pressed at a 60% page zoom.

| Table | Before | With the test rows | After the erase (fresh load from the server) |
|---|---|---|---|
| properties | 0 | 1 (id 2, "דירת בדיקה, למחיקה") | 0 |
| units | 0 | 1 (id 2) | 0 |
| contacts | 0 | 1 (id 2, "שוכר בדיקה") | 0 |
| leases | 0 | 1 (id 2, 1.9.2025 to 31.8.2027, 7,800, index-linked every 12 months) | 0 |
| ledger | 0 | 15 (the rent charges the engine made, Sep 2025 to Nov 2026; no payment) | 0 |
| tickets, docs, tasks, personal links | 0 | 0 | 0 |
| events (as the app loads them) | 0 | 1 (index_confirmed, id 13, lease 2) | 0 |

Safeguards as run: all counts 0 right before creating (and not the sample); before erasing the page was reloaded from the server and every row checked to be the test's own (one property, unit, contact and lease by id and name, all 15 ledger rows on lease 2, the one event on lease 2); the erase ran inside the same check; a fresh load after it shows 0 everywhere and the welcome screen. No document or photo was created in this sitting.

What was pressed, with real numbers:
- The tenancy screen showed the line "עדכון המדד של 1.9.2026 לא אושר" with its button. Press 1 opened the sheet: rent today 7,921, base index 103.5, latest index 105.1, rent from 1.9.2026 7,921, "מספרי המדד מהלשכה המרכזית לסטטיסטיקה". Press 2 ("לאשר את שכר הדירה החדש") made ONE call to /rm/today/index-confirm and wrote the journal event (base 103.5, applied 105.1, old 780000, new 792058, start month 2026-09); the ledger stayed at 15 rows; the sheet said "אושר: שכר הדירה מ-ספטמבר 2026 הוא 7,921 ₪. נרשם ביומן הדירה."; the line then read "אין עוד עדכון עד סוף החוזה".
- With real data the sheet and the engine AGREE: the engine's own charges from September 2026 are 7,920.59 and the sheet's new rent is 7,920.58. The 8,042 beside 8,034 seen in the sample portfolio is a mismatch of the sample's numbers only.
- A home with nothing recorded: one press on the "דוד מים" tile saved it (one call to /rm/save), no form; the row then showed the part and the add tile.

Seen and not fixed:
1. With an unpaid charge OLDER than the twelve months the ruler shows (here September 2025), the bottom sheet of the tenancy screen points at that month and says "עדיין אין חיוב לחודש הזה" although the charge exists; the ruler itself is right. It needs the ruler to show, or at least name, a debt from before its window.
2. Not measured on a real phone.


## Third sitting (20.11.2026, live 1.72.728): sample people carry no phone
Coordinator's order of 20.11 (a defect fix, not the board 5 build). Found by the film capture round: sample people carried phones shaped like real mobile numbers (050-000-0xxx), and the app turns every stored phone into a wa.me / tel: link, in the PUBLIC demo of version 1 and in the sample portfolio of version 2. Nobody pressed the WhatsApp button on the old build.

What changed: sample people carry no phone and no e-mail (data, server answer, stored sample, seed); human names stay and each wears "(דוגמה)" / "(example)"; in a sample a WhatsApp press shows the wording with a copy button and opens nothing; real accounts keep the real links.

| Check on the live site | Result |
|---|---|
| `/wp-json/nadlan/v1/rental-demo` he and en | 4 homes, `tenant_phone` empty on all, no phone-shaped number, names marked |
| Public demo as a visitor (built-in browser, not signed in), he | home "דירה 7": phone box empty, no wa.me / tel: / mailto: link inside the rentals block, the reminder press shows "היי משפחת לוי (דוגמה), תזכורת ידידותית..." with "העתקת הנוסח" and the note that nothing is sent |
| Public demo as a visitor, en | the three tenants: phone empty, wording shown, "Copy the wording", no link |
| `lab_sample_people_v1.py` on the live site (headless, visitor, he+en, 1280 and 390 wide) | 12/12 |
| Sample portfolio as administrator (owner's Chrome) | 10 people, none with phone or e-mail, each name marked; 10 screens and 23 cards with every tab: no chat, call or mail link from the app |
| A real press on a sample tenant's WhatsApp button (people list) | the sheet "הודעה לדנה כהן (דוגמה)": text box, "רישום ביומן", "העתקה", the note; both controls are buttons; the press wrote one line in the in-memory sample journal; no tab opened |
| The administrator's own account tables | 0 rows in all nine before the release and after the sitting (fresh load from the server) |

Left as it is, said plainly: on the English page of the public demo the names and addresses are still Hebrew (only the mark is English); the site-wide WhatsApp bar and the site's info mail address are on the page as on every page; the old numbers remain in repo archives no visitor is served (design previews, source snapshots). Not measured on a real phone.
