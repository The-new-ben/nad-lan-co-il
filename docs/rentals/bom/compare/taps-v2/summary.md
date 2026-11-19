# Rentals app v2: taps for the ten landlord jobs (HAD-795, stage 3)

Run 2026-11-20 on the LOCAL lab copy (http://127.0.0.1:47914/docs/design-lab/rentals/app.html?lang=he#/today, sample portfolio, mock server), Hebrew, Edge via Playwright. Phone = 390x844 touch, desktop = 1440x900. Counting rule: TEN-JOBS.md (every press, including field focus, file-picker press and choice; no typed characters, no scrolling). Script: `count_v2.py`; paths and checks: `taps-v2.csv`; done-state screenshots: `shots/`. All 20 runs ended in the done state and passed their data check, except J8 (computed only, see below).

| Job | Phone 390 | Desktop 1440 |
|---|---|---|
| J1 See who has not paid | 0 | 0 |
| J2 Record a rent payment | 2 | 2 |
| J3 Send a payment reminder | 2 | 2 |
| J4 Log a repair with a photo | 8 | 8 |
| J5 Send a professional to a repair | 5 | 5 |
| J6 Close a repair with its invoice | 6 | 6 |
| J7 Add a document to the apartment | 5 | 5 |
| J8 Update the rent by the CPI | 3 (computes only, no save) | 3 (computes only, no save) |
| J9 Year's rental income for tax | 4 | 3 |
| J10 Renewal offer / ending notice | 2 | 2 |

Paths (labels as pressed): J2 סימון ששולם > שמירה. J3 תזכורת בוואטסאפ > שליחה בוואטסאפ. J4 תקלות > תקלה חדשה > (focus title) > שמירה > הוספת תמונה > (file field) > (file picker choice) > שמירה. J5 פתיחה > בחירת בעל מקצוע > שמירה > שליחה לבעל המקצוע > שליחה בוואטסאפ. J6 פתיחה > טופלה > הוספת תמונה > (file field) > (picker choice) > שמירה. J7 הוספה > העלאת מסמך > (file field) > (picker choice) > שמירה. J8 כספים > הצמדה למדד > בדיקת הצמדה עכשיו. J9 (phone: עוד >) דוחות > פתיחה > פתיחה. J10 הצעת חידוש > שליחה בוואטסאפ.

## Over 3 taps
J4 (8), J6 (6), J5 (5), J7 (5), and J9 on phone (4). J9 on desktop is exactly 3.

## Cannot be done
No job is fully "cannot". One is partial: J8. The app computes the linked rent (5,900 to 6,056) in a sheet that has no save or apply button. The linkage rule feeds future charges by itself (rm-core.js `N.mx.amount`, next step 1.9.2027), so "saved for next month" is not an action the landlord can take or confirm. Counted as 3 taps for the computation only.

## Why the extra taps
- **File picker = 2 presses every time** (press the file field, then choose in the system picker). It is inside J4, J6 and J7, so 2 of their 5 to 8 taps are the picker alone.
- **Two-step attach**: a repair or document is first saved, then opened, then the file is attached in a second sheet (J4: create repair, card opens, add photo, then a separate save). Photo and invoice share one button labelled "add photo" and save as kind "other"; labelling it "invoice" or "contract" costs +2 more (select, choose).
- **Field focus**: J4 needs 1 tap to focus the title (the first field of the form, the apartment list, is the one auto-focused).
- **Drawer and card depth**: J5 and J6 start by opening the repair card (1), then act inside it. J5 is assign (open form, save) and then a separate dispatch step (send link, send), because sending needs the vendor assigned first.
- **Send is its own press** (J3, J5, J10): the message is ready after the first press, but nothing leaves or is logged until the second.
- **Phone navigation**: Reports sit behind "עוד" (+1 on J9). Year picker opens as a form that needs its own "פתיחה" (J9).
- **Defaults help but can mislead**: forms preselect the first apartment, first vendor (a plumber for a boiler fault), first lease; picking another costs +2 (J4, J5, J7).
- **Confirm dialogs**: none occurred in these paths (a confirm only appears when closing a repair that has a cost).
- **Zero and one-press wins**: J1 is on the home screen without a press; J2 is 2 because the form is prefilled (tenant, amount, today). A tenant-reported payment is 1 press (אישור התשלום).
