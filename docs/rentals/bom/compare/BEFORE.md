# Rentals world: the world comparison, BEFORE (HAD-795 stage 3, 20.11.2026)

Measured before any design or build of package 6. The same table is re-measured after the build (stage 7).

## 1. Coverage of the 76 parts of a rented home (score out of 152)

2 = a working feature, 1 = partly, 0 = absent on the vendor pages read, ? = could not tell (counted 0). Evidence per cell: coverage.csv. Products found by search (queries in coverage-summary.md); 14 global, 7 Israeli.

| Product | Country | Total /152 | Parts fully covered (2) |
|---|---|---|---|
| Rentila | France | 72 | 19 |
| DoorLoop | US | 70 | 23 |
| Arthur Online | UK | 67 | 20 |
| Landlord Studio | UK | 67 | 15 |
| immocloud | Germany | 60 | 17 |
| Hemlane | US | 56 | 18 |
| AppFolio | US | 54 | 16 |
| TenantCloud | US | 54 | 15 |
| Dira360 (best Israeli) | Israel | 46 | 12 |
| nad-lan today | Israel | 80* | 9 |

\* Not comparable: nad-lan's score is derived from the tree's own leaf status (any "partly" leaf gives 1), and most of what "works" is the administrators-only version 2. **The honest reading: nad-lan fully covers 9 parts; the leaders fully cover 19 to 23.** Full table with every product and per-branch scores: coverage-summary.md.

**Parts no product in the world fully covers (26 of 76):** house rules; brokers and the fee; discrimination limits; handover date and documents; after the handover; arnona; every appliance and system branch except electricity, gas, the house committee and the yearly calendar (structure, plumbing, hot water, AC, kitchen, laundry, mamad, pests); wear vs damage; warranty and invoices; all four tax-track parts; debts after the exit; and five of the seven long-view parts (wear over years, wear reserve, selling with a tenant, sale-day tasks, ending the business). This is the open ground: the home as an object and the Israeli tax and exit paths.

**Only Israeli products touch:** setting the price (rent estimates: DiffeRent, Dira360, WeCheck) and collecting applicant details with consent (Dira360). No Israeli product fully covers CPI linkage, arnona, the house committee or any tax track.

## 2. Taps for the ten common jobs (TEN-JOBS.md; every press counts, typing does not)

| Job | nad-lan v2 (local lab of the live admin code) phone / desk | nad-lan public demo phone / desk | Dira360 public demo | Global leaders |
|---|---|---|---|---|
| J1 who has not paid | 0 / 0 | 0 / 0 | 1 | not reachable |
| J2 record a payment | 2 / 2 | cannot (read-only demo) | cannot | not reachable |
| J3 payment reminder | 2 / 2 | 2 / 2 | cannot | not reachable |
| J4 repair with a photo | **8 / 8** | cannot | cannot | not reachable |
| J5 send a professional | **5 / 5** | cannot | cannot | not reachable |
| J6 close a repair with its invoice | **6 / 6** | cannot | cannot | not reachable |
| J7 add a document | **5 / 5** | cannot | cannot | not reachable |
| J8 update rent by the CPI | 3 / 3, computes only, no save | 2, computes only | cannot | not reachable |
| J9 the year's income for tax | **4** / 3 | cannot | cannot | not reachable |
| J10 renewal or ending notice | 2 / 2 | cannot | cannot | not reachable |

**Over three taps today: J4, J5, J6, J7 and J9 on a phone; J8 cannot save.** Main causes (taps-v2/summary.md): attaching a file is a second sheet after saving; the file picker costs 2 presses; the repair form focuses the wrong first field; the repair card must be opened before assigning; Reports sit behind "עוד" on phones.

**What could not be run (said plainly):** no global or Israeli leader could be counted. DoorLoop, RentRedi and AppFolio offer only guided slide tours that cannot be driven; Buildium's tour is a video behind a form; Stessa and Landlord Studio have videos only; Baselane and Hemlane have booking forms; TurboTenant and TenantCloud have no public tour; Avail refused the browser; MyHome answered 402; Beyti's site is down. We never opened an account, paid, filled a demo form or solved a captcha. The phone counts are a 390 px browser emulation, not a real phone.

## 3. What this means for the design (input to stage 4)

1. The ten jobs: five are over three taps today. Fixes are structural (a file attached in the same sheet, a camera-first repair, assign from the repair row, Reports one tap from the home on phones, a CPI "apply" button).
2. The open ground nobody covers is exactly Ben's order: the home as an object (systems and appliances with who pays by law), the Israeli tax tracks and the exit path.
3. Fair comparison rule for stage 7: the same jobs, the same counting rule, the same products; competitors stay "not reachable" unless a drivable public demo appears.
