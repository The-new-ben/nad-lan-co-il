# mbudget: "כמה דירה זה קונה, ואיפה" (HAD-675)

Panel 1 of the approved mortgage design board (`Tools.dc.html`), built for https://nad-lan.co.il/mortgage-calculator/ as a custom
surface on the NadLan Instruments engine. Local build only: nothing under `plugins/` was edited, nothing deployed or committed.

## What it does
In under a minute the household types net income, equity and buyer type (optional: existing loans, share of income, term). It gets:

1. **The highest home price that passes both Bank of Israel limits**: payment to income (the share they pick, capped at
   `rules.pti_max` = 50%) and LTV by buyer type (`cost.ltv`: single 75%, additional 50%, oleh 75%, foreign 50%), with purchase tax
   (`ptax.json` brackets, oleh cap included) and the lawyer (`cost.lawyer.from` 0.5% + VAT 18%) paid from the equity.
   The solver is the existing `window.NLAF.compute` from `tools/afford.js`, unchanged. It gets one equivalent nominal rate that
   reproduces the blended first payment of the five tracks in the Bank of Israel system mix of the latest month
   (`by_bank.latest.table`, row `system`, 9.2026; monthly rate = (1+e/100)^(1/12)-1). Since PV and PMT are linear in the loan, the
   equivalent rate gives exactly the blended payment for any loan size. The one decisive number (the max price) has the survey red
   2px underline. Every other figure is in mono, and a formula line with the real numbers and a source line sit under the result.
2. **Where**: every city in `homes.payments.rows` (24 cities, plus Israel as a reference line) where the official median deal price
   for 3, 4 or 5 rooms is at or under the max price. Each row shows the city, median, quarter, and *this household's* first payment
   at that median: the loan it needs after equity, tax and lawyer, times the same blended payment per million. A room picker shows
   the count per size (default 4 rooms). When none fits, it names the cheapest city for that size.
3. **Homes on the site**: GET `/wp-json/nadlan/v1/near-finder` (public, read only, cached 5 min; demo, sold and rented are already
   excluded server side). It keeps listings with `deal === 'sale'`, a published `price > 0`, `price <= max`, and a link on
   nad-lan.co.il. Up to 6 are shown, closest to the budget first, with a "see all" link to https://nad-lan.co.il/properties/.
   **Projects are not shown**: the endpoint has no home price for projects (849 projects, only `psqm`, filled on 6 of them), and
   the honesty law says unknown = omitted. If the endpoint fails or times out (9 s), parts 1 and 2 stay and a plain line plus the
   see all link replace part 3.

Plus copy, WhatsApp and print, the "דוגמה" badge until the first edit, and `data-nli-set` support (for example `track`).

## Inputs and defaults (the example on the board)
Income 22,000 ₪, equity 600,000 ₪, single home, loans empty ("אין"), share 33%, term 25 (20 / 25 / 30).
Result: **max ₪1,926,000**, loan ₪1,337,436, first payment ₪7,260, binding limit = income. With 4 rooms, the cities are Eilat,
Haifa, Ashkelon and Beer Sheva (1-3.2026), the same as the board.

## Sources and dates (every number shown comes from these or from the inputs)
| What | File and key | As of |
|---|---|---|
| Track rates and mix, system average | `boi-mortgage.json` `by_bank.latest` (BoI TamInt010.xls) | 9.2026, published 20.10.2026 |
| PTI cap 50% | `boi-mortgage.json` `rules.pti_max` (directive 329) | 30.6.2026 |
| City medians, 3/4/5 rooms | `boi-mortgage.json` `homes.payments.rows`, src `homes.medians.src` (Tax Authority via nadlan.gov.il) | quarter per row (1-3.2026 mostly, Israel 4-6.2026), read 26.10.2026 |
| LTV by buyer, VAT, lawyer % | `cost.json` | checked 21.10.2026 |
| Purchase tax brackets | `ptax.json` | in force from 16.1.2025, checked 26.10.2026 |
| Homes for sale | `near-finder` endpoint, field `updated` | live |

## Files
- `mbudget.js`: the tool. Pure logic in `window.NLMB` (`perMillion`, `eqRate`, `solve`, `cities`, `listings`, `html.*`), no DOM needed. Scoped CSS `#nlmb-css`, reusing the engine's classes (`nli__panel`, `nli__f`, `nli__in`, `nli__seg`, `nli__lines`, `nli__bar`, `nli__note`, `nli__share`, `nli__eg`).
  **afford.js dependency**: when `window.NLAF` is missing, the tool loads `afford.js` from its own folder with the same `?ver`.
  I checked this on a scratch copy laid out like `tools/`: afford.js was fetched and the result rendered. So the registry needs no
  extra key, though the release can still enqueue afford before mbudget.
- `test_mbudget.js`: `node docs/research/2026-11-05-mortgage-world/build/mbudget/test_mbudget.js` (uses the real afford.js and data).
- `fixtures/near-finder-2026-11-05.json`: trimmed snapshot of the endpoint (all 16 listings, 5 projects) for the offline test.
- `preview.html`: the shortcode markup. Serve the repo root (`python -m http.server 57833` in `nad-lan-co-il`) and open `/docs/research/2026-11-05-mortgage-world/build/mbudget/preview.html`.
- `registry.php.txt`: the `nadlan_nli_tools()` entry (data: `boi-mortgage.json`, `ptax.json`, `cost.json`). php -l clean, related URLs all 200.
- `summary.php.txt`: the `nadlan_nli_summary()` branch. php -l clean. With the v2 data it prints:
  "לפי התמהיל הממוצע של כל הבנקים ב־9.2026 (בנק ישראל), משכנתא של 1,000,000 ₪ ל־25 שנה מתחילה בהחזר של 5,428 ₪ בחודש. משק בית עם הכנסה נטו של 22,000 ₪ בחודש, החזר של 33% מההכנסה והון עצמי של 600,000 ₪ יכול לקנות דירה יחידה עד 1,926,000 ₪, כולל מס רכישה ועורך דין; דירת 4 חדרים במחיר החציוני נכנסת בסכום הזה ב־4 ערים מתוך 24: אילת, חיפה, אשקלון ובאר שבע (רשות המסים, עסקאות 1-3.2026)."
  With the live (old) `boi-mortgage.json` it prints nothing.
- `screenshot-375.png` (full page, 2x) and `screenshot-1280.png` (full page).

## Test results (5.11.2026)
`OK 148 passed, 0 failed`:
- calibration: 1,000,000 over 25 years = **5,428.30** (matches `payment_per_1m` 5,428.3 and an independent track by track sum); the equivalent rate R satisfies NLAF.pv(5,428.30, R, 300) = 1,000,000;
- two limits on 5 cases (single payment bound, single equity bound, additional with loans and 30 years, foreign at 50% and 20 years, oleh): payment ≤ income × share − loans, loan ≤ LTV × price, equity ≥ price − loan + tax + lawyer, +1,000 fails; the 50% cap holds (65% gives the 50% answer); loans above the payment give no mortgage;
- city filter: every shown median ≤ max, none missing (pair by pair), Israel kept apart, medians and quarters equal the data, each payment re-derived, each loan passes both limits;
- listings: sale only, published price only (8424 and 7633 have none and never show), price and link exactly as the endpoint, no project, at most 6, off-site links dropped;
- no invented number: every ₪ amount, percent and date in the rendered text (aria labels and share text included) traces to an input, a data file or the model; no long dash, no spaced hyphen, no blacklisted word, no ₪0.

Browser (built-in pane, 375 and 1280): no horizontal scroll at 375 (scrollWidth 375), controls ≥ 44 px (the only smaller targets
are inline source links inside text and the engine's related links), no console errors besides the deliberate failure test. I
typed into equity (600,000 → 900,000 → max ₪2,216,000, the Ofakim listing at ₪2,000,000 appeared), picked 30 years
(₪2,345,000, tax ₪12,819 checked by hand), tapped 5 rooms and "הראו לי את הדירות האלה" (it scrolls to the homes). The
endpoint failure path still shows parts 1 and 2. In the example case **no home on the site** is at or under ₪1,926,000 (the
cheapest priced sale listing is ₪2,000,000), and the tool says so.

## Open questions and not verified
1. **Data file**: the tool and the summary need `data/boi-mortgage.json` with the v2 keys. The live file (16,808 bytes) does not have them yet. The local plugin copy was replaced with v2 at 22:22 by someone else, md5 equal to `boi-mortgage-v2.json`. With the old file the tool shows "הנתונים לא נטענו" and the summary is empty.
2. **Payload**: near-finder weighs about 390 KB (849 projects), fetched once per page view after the first paint. A `?deal=sale` or a lighter route would help. That is a server change for the release engineer.
3. **Projects**: if Ben wants new projects in part 3, the endpoint needs a real published "from" price per project. Until then none are shown.
4. Not verified: on the live page (theme CSS, sticky header, the live CSP), and the copy and WhatsApp buttons (clipboard not tried). There is no English version (the tool is Hebrew only).
5. The lawyer uses the low end of the cost.json range (0.5% + VAT), the same as afford's default. Appraiser, inspection and broker are not counted, also the same as afford.
