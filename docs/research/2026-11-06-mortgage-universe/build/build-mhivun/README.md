# New tool for /mortgage-calculator/: "עמלת היוון" (mhivun)

HAD-675, mortgage universe. Built 6.11.2026, **local only**: nothing deployed, nothing committed, no live write, no existing file
edited (`inc/instruments.php`, `mrates-common.js`, `mexit.js`, `mortgage.js`, `core.js`, `core.css` and the data files untouched).

The most complete capitalization-fee calculator we know of: a whole mortgage (up to 6 tracks), the fee of every track by the
Banking Order with the full step-by-step, partial prepayment split for the least fee, the fee in each of the next 24 months with
two scenarios, and a check of the bank's number. Search intent: "היוון משכנתא" (the fee), with "מחשבון עמלת היוון משכנתא",
"עמלת היוון בנק ישראל", "הפרשי היוון משכנתא", "פירעון חלקי" used naturally on the page.

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/mhivun.js` | The tool (id `mhivun`), Hebrew only, RTL. Pure math in `window.NLHV` (runs in node); the page part on `NLMR.ui` of mrates-common.js. |
| `build-mhivun/test_mhivun.js` | Node test, **67 assertions**, hand-worked closed forms written in the test (not NLMG). Last run: `test_mhivun.out.txt`. |
| `build-mhivun/preview.html` | Local mount exactly as the shortcode prints it (section.nli, nli-host, kicker, title, the PHP summary, related links) inside pane `#tool-hivun`; scripts in enqueue order: core.js, mortgage.js, mrates-common.js, mhivun.js. `?theme=1` adds the live theme stylesheets (read only). |
| `build-mhivun/verify.py` | Playwright (Chrome, headless) at 390x844 is_mobile and 1280x900, plus a phone pass under the live theme. Starts `http.server` on a free 127.0.0.1 port itself and stops it in `finally`. **154 checks.** Last run: `verify.out.txt`, `verify.json`, `shots/`. |
| `build-mhivun/registry.php.txt` | The `nadlan_nli_tools()` entry and the `nadlan_nli_summary('mhivun')` branch. `php -l` clean (PHP 8.3). |
| `build-mhivun/render_summary.php` | Renders the summary branch against the real data with WordPress stubs (copies of `nadlan_nli_mrates`, `nadlan_nli_mr_nom`, `nadlan_nli_mr_pmt`). Output: `summary.out.html` (also pasted into preview.html). |

Run from the repo root: `node docs/research/2026-11-06-mortgage-universe/build/build-mhivun/test_mhivun.js` and
`python docs/research/2026-11-06-mortgage-universe/build/build-mhivun/verify.py`.

## Results (6.11.2026, data built 5.11.2026, averages in force from 19.10.2026, CPI 9.2026, "today" = 11.2026)

* Node: **67 of 67**. Among them: 400 seeded single loans (all five tracks, dates 12.2021 to 10.2026, 5 to 30 years, 1% to 7%):
  `NLHV.mortgage([one row])` gives fee, balance and notice `===` `NLMR.feeExisting` (what mexit calls) with 0 mismatches, and
  `NLHV.feeFreq(..., 60)` returns the feeExisting object field by field in all 400. mexit's own example gives the same 15,908 on
  956,994 to the last digit (= `headlines.prepay_fee` of the data). The PHP summary is run and its numbers matched to the JS.
* Browser: **154 of 154** at 390 and 1280 and under the live theme. Pressed: the four "איך זה חושב" panels, the notice choice both
  ways, a track change with its cycle (every 2.5 years, every year), the term unit (months and back, 239 months), add row to 6 (the
  add button then disabled), remove twice, a bad month (13.2023) and a future one, the partial amount (200,000, 600,000, 9,000,000)
  and both modes, the 24-month table, the bank's number (a gap and a close one), copy (clipboard read back), WhatsApp (wa.me answered
  by a local stub, nothing left the machine), the case link (reopened in a new tab: same case), print (window.print counted). Every
  total checked against `NLHV` on the same values in the page. No console error or warning, no horizontal scroll, every visible
  button, input, select and summary at least 44 px, every input and select labelled, every group named, no long dash, no banned
  word, never a bare "₪0". Under the live theme: headings in ink, steps numbered, inputs in Plex Mono, buttons in Plex Sans Hebrew;
  the only console errors are the theme's own assets (filtered by URL, as in the mzakaut build).
* Screenshots looked at (eyes): `page-default-390/1280`, `card-steps-390`, `when-390/1280`, `partial-1280`, `partial-390`,
  `bank-gap-390`, `page-theme-390`. Fixed after looking: the scenario lines started at today's value and drew a false jump to next
  month (now they start next month); the cheapest-month label floated on the red line (now on its bar); month labels collided on
  the phone (every 6 months under 560 px); a "₪0" axis tick (now "0"); two amounts joined by a comma in the key sentence (now two
  sentences); a long no-fee reason crammed into the partial table (short reasons there); "₪2,084, ₪2,084 יותר" (now "במקום אפס");
  spacing in the 24-month section; and under the live theme the inputs had lost Plex Mono and the unit select had become a rounded
  grey pill (scoped `!important` rules for faces and flat boxes inside `.mhv`).

## Worked examples (all in the test)

**1. mexit's example, one loan.** 1,000,000 ₪ fixed not linked from 11.2024, 25 years, 4.88%, repaid 11.2026: 24 paid, 276 left,
balance 956,994, fee **15,908** (exactly feeExisting).

**2. The opening example** (labelled on the page): 1,400,000 ₪ from 7.2023 in four tracks, repaid in 11.2026 (40 payments made).

| Track | Balance today | Average used (in force) | The two calculations of s.3 | Fee |
|---|---|---|---|---|
| 1. קבועה לא צמודה, 500,000, 300 months, 5.30% | 464,966.66 (payment 3,011.01) | today 20_25: 4.788% eff = 4.6860% nominal (19.10.2026); loan day 20_25: 5.022% = 4.9100% (12.7.2023) | value at today's avg 491,158.16, at the loan-day avg 481,359.21; s.3(3) = 491,158.16 - 464,966.66 = **26,191.49**; s.3(4) = 491,158.16 - 481,359.21 = **9,798.95**; lower = s.3(4) | 9,798.95 x 0.8 (3 years in 7.2026) = **7,839.16** |
| 2. פריים, 450,000, 4.15% | 413,327.45 | none | none (rate changes at an unknown date, s.4) | **none, said so** |
| 3. משתנה צמודה, every 5 years, 300,000, 4.20% | 275,708.60 x CPI 9.2026 / 7.2023 = 1.0822 = 298,377.86 | today le5: 3.501% = 3.4460%; loan day le5: 3.921% = 3.8523% | 20 payments of 1,749.77 to the change day 7.2028, the last with the balance (285,539.65); s.3(3) 3,556.04, s.3(4) 1,921.57 | 1,921.57 x 0.8 = **1,537.26** |
| 4. קבועה צמודה, 150,000, 240 months, 3.90% | 132,363.63 x 1.0822 = 143,246.80 | today 15_20: 3.455% = 3.4015%; loan day 15_20: 3.995% (above 3.90%, so s.3(4) does not apply) | s.3(3) = 148,714.23 - 143,246.80 = 5,467.43 | 5,467.43 x 0.8 = **4,373.94** |

Whole mortgage: balance **1,319,918.77**, capitalization fee **13,750.36**, operational fee up to 60 (once), 0.1% short notice
1,319.92, CPI fee if repaid on the 1st to 15th 302.07 on the two linked tracks (shown, not in the total). Total to pay off with the
notice: 1,335,049.

**3. Partial prepayment.** 200,000: all to prime (no fee), payment down 1,167.45 a month, interest saved to the end 103,536.82; the
split by balances would cost 2,083.52. 600,000: prime closed (413,327) and 186,673 to track 3 (fee per shekel 0.52%, against 1.69%
on track 1 and 3.05% on track 4): fee **961.75** against 6,250.55 by balances; payment down 3,507.39, interest saved 311,922. In
"קיצור התקופה" mode: prime closed (260 months), track 3 shorter by 187 months, 355,594 saved. The partial fee is the full fee times
the share repaid (NLMG.prepayFee with share = a/B gives the same number, asserted).

**4. The next 24 months** (averages unchanged / 0.5 lower / 0.5 higher): today 13,750; 12.2026 13,597 / 37,322 / 127; the fee falls
each month to **10,849 in 6.2028, the cheapest month, 2,901 less than today**. In 7.2028 it rises to 12,051 although tracks 1 and 4
reach 5 years (30%) and track 3 has its change day (no fee that month): tracks 1 and 4 move to a lower-average remaining-term column
(15_20 4.739%, 10_15 3.242%). From 8.2028 track 3 is counted again at today's rate (15,333). The page says all of this in "החודשים
שבהם משהו משתנה" and under the chart; the fee is very sensitive to the averages (a 0.5 point fall almost triples it).

**5. Other change cycles.** var not linked, every 2.5 years, 300,000 from 1.2024 at 5.20%: 26 payments to the change day 1.2029,
columns 1_5, fee 3,180.12. Every year: no capitalization fee (s.4). Every 2 years from 11.2024, repaid 11.2026: the change day, no
fee. Every 10 years from 11.2021: 60 payments to 11.2031, loan-day column 5_10.

**6. Zero-fee reasons.** 3.00% from 1.2022: today's average is not lower ("noavg"). 5.00% from 12.2021: s.3(3) = 11,936 but the
loan-day average was 3.36%, below today's, so s.3(4) = 0 and the fee is 0 ("orig"). 4.80% from 1.2024: the loan-day average 5.235%
was above the rate, so only s.3(3): 4,931.

## Server summary (rendered 6.11.2026, `summary.out.html`)

"עמלת היוון היא עמלת הפירעון המוקדם ... הממוצעים שבתוקף מ־19.10.2026 (נתוני 9.2026, ריבית שנתית אפקטיבית): בקבועה לא צמודה
4.607% לתקופה של מעל 10 ועד 15 שנים ו־4.788% למעל 20 ועד 25 שנים; בצמודה למדד 3.242% ו־3.365%. למשל, הלוואה קבועה לא צמודה של
500,000 ₪ שנלקחה ב־7.2023 ל־25 שנה בריבית 5.30%, ונפרעת כולה ב־11.2026: היתרה 464,967 ₪, הממוצע לתקופה שנותרה 4.788% (ביום
ההלוואה 5.022%), ועמלת ההיוון כ־7,839 ₪ ..." Every number is read from boi-mortgage.json at render time; the example is computed in
PHP with the same steps as feeExisting and equals the JS (test section 9). "Now" in PHP is the data build month.

## How mhivun decides (readings to confirm)

1. **Operational fee once per payoff**, not per track ("עד ₪60, פעם אחת"). The Order's text was not reopened for this; if a bank
   charges it per sub-loan the total differs by up to 60 per track (the bank-check reasons do not claim either way).
2. **Change cycles other than 5 years.** `NLMR.feeExisting` is fixed to 60 months, so `feeFreq` repeats its steps with the cycle
   FQ: the next change day at `FQ * ceil(el / FQ) + 1`, the loan-day average column of `min(FQ/12, term)` years (5 years in
   feeExisting), and FQ passed to `NLMG.prepayFee` as `t.freq`, which already gives no capitalization fee when FQ is 12 or less
   (`fees.no_cap_fee_if_change_within_months`). With FQ = 60 it is byte-identical to feeExisting (asserted). The loan-day column for
   2, 2.5 and 10 year cycles is our reading of s.4 / s.7(a).
3. **After a change day inside the 24 months** the new rate is unknown, so the track is counted at today's rate (said on the page).
4. **Scenarios** move every remaining-term column of both files by 0.5 point from next month; the loan-day averages stay.
5. **Balance**: Spitzer at today's rate from the start month (feeExisting's rule; on prime and variable tracks as if today's rate
   ran from the start), linked tracks x CPI latest / CPI of the start month. No grace, no past partial prepayments, no equal
   principal: the bank-check section lists these as usual reasons for a gap.
6. **The least-fee split** sorts tracks with no fee by rule first, then by fee per shekel, ties to the higher rate; the fee is
   linear in the amount, so this is exactly optimal. Interest saved is in today's shekels (no future CPI, today's rate on prime and
   variable tracks).
7. **The CPI fee** (repaid on the 1st to 15th) is shown per linked track and in the lines, not added to the total.
8. **Source labels** for the two Bank of Israel pages (`circulars/cir2103/` as "חוזר הפיקוח על הבנקים לחישוב העמלה" and
   `information/interestrates/` as "שיעורי ריבית") were written without opening the pages; confirm the titles.
9. **Keywords**: "עמלת היוון" and "היוון משכנתא" were not run through the keyword guard / URL word audit; this is a tool pane on
   /mortgage-calculator/ (no new URL), but the owner page for the head term should be confirmed before release.
10. **The example rates** (5.30%, 4.15%, 4.20%, 3.90% from 7.2023) are typed example values, not Bank of Israel averages; the page
    labels the whole opening case as an example.

## Release steps (not done)

1. Paste `registry.php.txt` part (1) after 'mexit' in `nadlan_nli_tools()` and part (2) after the 'mexit' branch of
   `nadlan_nli_summary()`; ship `tools/mhivun.js` (no new data file).
2. Add the chip and pane to the switcher of /mortgage-calculator/ (`tool-hivun`, markup in the snippet header). Placement and the
   chip wording are the owner's call.
3. After release: source audit of the raw HTML, content_first_check, the press-through in the owner's Chrome, spot-check rainbow and
   h-infinity, a Linear note on HAD-675 and the Notion row.

## Design

The instruments system as is: steel-blue ink on form-paper white, tokens `--nli-*` (ink #12202A, sea-deep #1F4B5C, sea #2F6F86,
survey red #C42550 only for the answer underline, a gap and the "averages lower" scenario, open green #4F9A5C for the cheapest month
and a close match), IBM Plex Sans Hebrew for text and IBM Plex Mono for every figure. Why it is not the default look: it reads as a
bank payoff ledger, each track a ruled card with its own track colour on the edge, a numbered calculation sheet under each, a
24-column fee strip with the discount and change days marked under the axis, no cream, no gold, no gradient of ours, no emoji. All
new CSS is scoped to `.mhv` (style id `mhv-css`), with `!important` only where the live theme restyles inputs, selects, buttons,
headings and lists.
