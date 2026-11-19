# The ten common landlord jobs and how taps are counted (HAD-795, stage 3)

Chosen from the tree (docs/rentals/bom) by how often a landlord meets them: monthly money first, then repairs, then documents, then the yearly and end-of-lease jobs.

| Job | What done means | Tree node |
|---|---|---|
| J1 | See who has not paid this month | the list shows unpaid tenants for the current month | 05.01, 05.10 |
| J2 | Record a rent payment received | this month's rent for one tenant is marked paid (expected amount, today's date) | 05.01 |
| J3 | Send a tenant a payment reminder | a reminder leaves (or is ready in WhatsApp/e-mail with the text filled) | 05.02, 05.09 |
| J4 | Log a repair with a photo | a repair exists on the apartment with one photo attached | 06.02 |
| J5 | Send a professional to a repair | a professional is assigned to that repair and gets its details | 06.02, 06.16 |
| J6 | Close a repair with its invoice | the repair is marked fixed and an invoice file is attached | 06.02, 06.17 |
| J7 | Add a document to the apartment | a file (contract, receipt) is stored on the apartment | 03.04, 07.06 |
| J8 | Update the rent by the CPI | the new linked rent is computed and saved for the next month | 05.04, 08.03 |
| J9 | See the year's rental income for tax | a yearly total per apartment is shown or exported | 07.06, 07.07 |
| J10 | Start a renewal or record a notice of ending | a renewal offer or an ending notice is recorded with its date | 08.02, 09.01 |

## Counting rule (the same for every product, ours included)
- Start: the product's home screen after login (or the start of its public demo). End: the "done" state above is visible.
- Count every press on the screen: buttons, links, tabs, menu items, picker choices, toggles, a tap to focus a field, the file picker's choice, confirm dialogs. Do not count typed characters or scrolling.
- The fewest-press path a first-time user can find from what is on screen (no keyboard shortcuts, no search box typing unless it is the only way).
- A job the product cannot do = "cannot". A job behind a login or payment we could not pass = "not reachable" (never create an account, never pay, never solve a captcha).
- Record the date, the URL where it was run, phone (390 px) or desktop, and keep a screenshot of the done state.
