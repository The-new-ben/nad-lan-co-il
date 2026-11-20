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
