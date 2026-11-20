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

## Result
Not run yet.
