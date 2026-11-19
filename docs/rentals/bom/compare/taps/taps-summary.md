# Tap count, ten landlord jobs, public demos only (HAD-795, stage 3)

Run 2026-11-20 in the built-in browser. Rule: TEN-JOBS.md in the parent folder. No account, no payment, no form, no captcha. Raw rows: taps.csv. Screenshots: shots/.

How to read the words
- A number = presses from the start of the public demo to the visible done state.
- cannot = a demo we could drive freely exists, and it has no such control. It says nothing about the logged-in product.
- not reachable = no usable public demo for that product, or the only public tour is a fixed slide sequence we cannot drive (so no job can be performed). It does not mean the product lacks the job.

## Counts (phone 390 px / desktop). Only two products could be driven at all.

| Job | nad-lan demo | Dira360 demo | DoorLoop | RentRedi | AppFolio | all other products |
|---|---|---|---|---|---|---|
| J1 unpaid this month | 0 / 0 | 1 / 1 | not reachable | not reachable | not reachable | not reachable |
| J2 record payment | cannot | cannot | not reachable | not reachable | not reachable | not reachable |
| J3 payment reminder | 2 / 2 | cannot | not reachable | not reachable | not reachable | not reachable |
| J4 repair with photo | cannot | cannot | not reachable | not reachable | not reachable | not reachable |
| J5 send a professional | cannot | cannot | not reachable | not reachable | not reachable | not reachable |
| J6 close repair + invoice | cannot | cannot | not reachable | not reachable | not reachable | not reachable |
| J7 add a document | cannot | cannot | not reachable | not reachable | not reachable | not reachable |
| J8 CPI rent update | cannot (2 taps compute, no save) | cannot | not reachable | not reachable | not reachable | not reachable |
| J9 yearly income | cannot | cannot | not reachable | not reachable | not reachable | not reachable |
| J10 renewal or ending notice | cannot | cannot | not reachable | not reachable | not reachable | not reachable |

Evidence: nad-lan = live public demo (https://nad-lan.co.il/my-rentals/, section "הדגמה חיה"); Dira360 = clickable demo with sample data on https://www.dira360.co.il/; DoorLoop, RentRedi, AppFolio = guided tours, desktop only (phone not run).

## Products that could not be reached, and why
- DoorLoop: public Arcade tour of about ten fixed slides (dashboard, late fees, maintenance requests, reports...). Nothing can be performed. Dashboard slide shows an Outstanding Balances widget as a picture only.
- RentRedi: public Storylane tour, 17 Next steps. Clicking the app itself does nothing. It shows a Late total on the payments widget, maintenance requests, receipt photo to expense, and a Schedule E report (15 Next presses to reach), all as slides.
- AppFolio: four Navattic tours about AI features for property managers; none is one of the ten jobs. Only the maintenance-performer tour was opened and stepped two screens.
- Buildium: "Take a tour" is a 7-minute video behind a form; trial needs an account.
- Stessa and Landlord Studio: Vimeo videos only. I did not watch them frame by frame, so there is no "video count".
- Baselane and Hemlane: demo pages are call or webinar booking forms.
- TurboTenant, Avail, TenantCloud: no tour or demo link found. TurboTenant and TenantCloud block plain fetches; the browser pane refused avail.co, so Avail was checked by plain fetch only.
- WeCheck: screening, guarantees, loans, mortgages; no landlord portfolio demo. LeaseLink: free contract wizard and a 30 second silent video, not a management app (wizard not run). MyHome: listings portal, answered HTTP 402 to a plain fetch. Beyti: site did not respond from this machine.

## Fastest per job
- J1: nad-lan 0 taps (list on arrival), then Dira360 1 tap (one tenant, sample illustration). The nad-lan list shows overdue apartments, not strictly this month.
- J3: nad-lan 2 taps, the only product measured.
- J2, J4 to J10: no product could be measured, so no fastest product exists. This table says nothing about who is faster in a logged-in app.

## nad-lan demo, per job
| Job | Phone | Desktop | Why |
|---|---|---|---|
| J1 | 0 | 0 | "הפעולה הבאה שלי" and chip "3 בפיגור" visible on arrival (phone: below the 3D model, scrolling not counted) |
| J2 | cannot | cannot | payment-month buttons disabled in the demo |
| J3 | 2 | 2 | apartment hotspot, then "תזכורת בוואטסאפ" (wa.me link with the tenant phone and the 11/2026 text filled; link read, not followed) |
| J4 | cannot | cannot | no add-repair control, no photo input |
| J5 | cannot | cannot | link goes to the professionals directory, nothing assigned to a repair |
| J6 | cannot | cannot | no close-repair control, no invoice upload |
| J7 | cannot | cannot | document file is a disabled checklist, no upload |
| J8 | cannot | cannot | computes the new rent (8,073 from 7,800 and index 112.4 over 108.6) after 2 taps, but no save and the CPI select is disabled |
| J9 | cannot | cannot | monthly total and a tax estimate only; no yearly income per apartment |
| J10 | cannot | cannot | list says "contract ended - renew or close" but no way to record an offer or notice |

The page itself says renewal and ending, auto CPI, year picker, document upload and similar are in managers' preview and not yet open to all owners. The nad-lan "cannot" rows are the public demo's limit; the logged-in app was not tested.

## Limits of this run (plain)
- Only the apartment-7 panel of the nad-lan demo was driven; the other apartments use the same panel.
- Desktop was the pane's default 1024 by 768, not a wide monitor. The phone width was set to 390 through the pane's viewport emulation, not a real phone.
- Screenshots were taken by the browser tool and converted to PNG. J2, J5, J6, J9, J10 "cannot" rows share the J4-J7 screenshot of the panel (nadlan-J4-J7-cannot-*), and the "cannot" rows of Dira360 have no own shot beyond dira360-J1-*.
- Guided tours (DoorLoop, RentRedi, AppFolio) were not run on phone.
