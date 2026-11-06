# Mortgage 2.0 v2 (round M, HAD-675, 6.11.2026): six delta rows closed, local only

File changed: `plugins/nadlan-config/assets/instruments/tools/mortgage.js`
- before: md5 `c99f393d90c41582c453cad6a9900acd`, 102,125 bytes (byte-identical to live; kept here as `orig-mortgage.js`)
- after: md5 `8cd8308ea03537f0edeb7af208c0adf9`, 122,709 bytes

Nothing deployed, nothing committed or pushed, no live writes, no new URLs, nothing sent to a server. No other repo file was edited.
The delta rows are in `../delta.md`, section (c).

## What changed (all additive)

With the new controls untouched, every payment, total, text, chart and the case link are the same as v1 (checked in node on 25
mix x scenario pairs and in the browser block by block against the live file).

| Row | What the visitor sees | How |
|---|---|---|
| C1 | Under each rate field (full width, under the rate row): "הריבית ב־7 הבנקים, ספטמבר 2026: מ־4.47% (דיסקונט) עד 5.96% (ירושלים) נומינלית, ובריבית אפקטיבית מ־4.56% עד 6.13%. מקור: קו המשווה של בנק ישראל." | `NLMG.band(D, track)`: by_bank latest, the 7 banks (the "system" row left out). The file's rates are effective; the field is nominal for a monthly payment, so the line shows both (nominal by `ef2nom`, as every other rate of the tool). Only for fixed_nl, fixed_cpi, prime, var5_cpi (var_cpi), var5_nl (var_nl_other). The eligibility loan gets no line; data without by_bank gives no line. |
| C2 | On the two variable tracks only: "תדירות שינוי הריבית" (כל שנה, כל שנתיים, כל 2.5 שנים, כל 5 שנים, כל 10 שנים), default 5 years. A chosen frequency shows in the track name ("משתנה כל שנתיים, צמודה"), a results line, the copied text, the formula note, the case link. | `track()`: the var5 reset month is `(m - 1) % freq === 0` instead of `% 60`. Read first: in v1 the reset path of the scenario is `sc.reset(m)`, which is non zero only for "עלייה של 2%" and "שינוי משלכם"; the Bank of Israel forecast and market expectations move the prime track only (the tool says so). That is kept, so: with no shock the payments are identical on every frequency; with a shock it lands at the first change month (every 2 years: month 25; a shock from month 40, yearly: month 49). The moat "same period" average follows the frequency; the Banking Order fee runs to the next change day, and a yearly change has no capitalization fee (`fees.no_cap_fee_if_change_within_months` = 12). |
| C3 | "התקופה בכל מסלול: בשנים / בחודשים". In months, each track takes 48 to 360 months ("מסלול 1: תקופה בין 48 ל־360 חודשים." otherwise). | The state stays in years (months / 12); the math was already monthly (`N = round(years x 12)`), so 250 months is a 250 payment schedule. Years mode keeps its v1 check. |
| C5 | "הורדת לוח הסילוקין (CSV)" in the share bar (next to copy, WhatsApp, link, print, all kept) and inside the schedule section. | `NLMG.csv(R, names)`, a Blob in the browser, file `mortgage-schedule.csv`: UTF-8 with BOM, CRLF, comma separated. One row per month: month, then for each track and for the total: payment, principal (payment less interest; below zero in a full grace or balloon month, when interest joins the balance), interest, CPI linkage added to the balance that month, balance at month end. A prepayment is not a payment row; the balance includes it (as the on-screen schedule says). Sample: `sample-schedule-*.csv`. |
| C9 | "שלושה תרחישים זה לצד זה": היום, תחזית בנק ישראל, תרחיש מחמיר. Each: first payment, highest payment with its year, total paid. | `NLMG.three(rows, D, opts)`: today = no prime path and no shock, the CPI as chosen; forecast = the policy rate to `forecast.rate_q3_2027` on the prime track by the middle of Q3 2027 (the same ramp as v1) with CPI `forecast.inflation_4q`; stress = the v1 "+2% בכל המסלולים" check (`scen({all: 2})`, the `st2` of v1, checked equal to the original file's own result). |
| C14 | "הסלים האחידים לסכום שלי" (a toggle): your mix and the three uniform baskets of directive 451 on your loan and term, four cards with first, highest (and year), total; the lowest total in green. | `NLMG.baskets(D, loan, years, rateOf, sc)`: Spitzer, one term (track 1's, the convention of the existing compare button), each track at the rate typed for it in the mix, else the Bank of Israel average; on the page's scenario. Checked equal (first, highest, total) to mexit's math, `NLMR.mathRows(NLMR.basketRows(...))` of `tools/mrates-common.js`, in node and in the page. |

Version note added at the top of mortgage.js in the existing style. Style: id-scoped CSS with `!important` where the theme fights,
IBM Plex Sans Hebrew for text, IBM Plex Mono for numbers, the given palette (ink #12202A, mute #5E6A75, line #D3DCE2, sea #2F6F86,
sea deep #1F4B5C, ground #F6F8F9; the stress card top line uses the tool's existing warning red #C42550). The scenario and basket
cards share rows through CSS subgrid so their values line up; on phones the amounts scale with the screen and never wrap.

## Tests

- `node test_mortgage_v2.js`: **56/56 passed**. v1 unchanged on 5 mixes x 5 scenarios (deep equality of every `mix()` array and
  total), solveLoan and prepayFee unchanged; C1 min/max equal by_bank latest for all 5 tracks, none for zakaut or without by_bank,
  Hebrew month; C2 the change month for each of the 5 frequencies, shock timing, same payments without a shock, fee rules; C3 48,
  250, 301, 360 months; C5 BOM, 301 lines, 21 columns, header names, sums per month; C9 the three definitions (stress equal to v1);
  C14 equal to the mexit basket math; no en or em dash in the file; no blacklisted word in the 192 added or changed lines (the one
  "כדאי" is the v1 status text kept word for word).
- `python verify.py` (Chrome headless, channel chrome, server on 127.0.0.1:47963 stopped at the end): **63/63 passed** on 390x844
  and 1280x900: the default state of v2 equals the live v1 in 14 blocks (answer, lines, status, stress, rules, legend, moat, schedule,
  charts, formula, strip, hints, case link, numbers); every feature above in the real page; the CSV download read back from disk;
  the case link reopens months + frequency; no console errors; no horizontal scroll; the 5 new controls are 44 px and labelled.
  Results in `verify-results.json`, screenshots in `shots/` (default, each feature, both widths).

## Left out, and why

- English: `/en/mortgage-calculator/` mounts only `mquick` (checked in the saved public source of 6.11), and the `mortgage` tool has
  no `en` block in `inc/instruments.php`, so it always renders Hebrew. No English labels were needed; no English mount to shoot.
- The existing method and grace-type selects measure 42 px inside their 44 px box; they are v1 controls and were left as they are.
  The new frequency select uses an inside outline instead of a border, so it is a full 44 px with the same look.
- CSV of the mix comparison table (delta C5 also mentions it): not in this brief; the schedule CSV only.
- The Bank of Israel forecast still moves only the prime track (v1 rule). Applying it to variable tracks at their change months would
  change v1 results for visitors who pick the forecast today, so it was not done.
- Not verified: the live page itself (the theme around the tool, the site header), Safari and Firefox (subgrid has a safe fallback),
  and Excel opening the CSV (BOM and UTF-8 checked in bytes only).
- Release: copy mortgage.js as is; no PHP change is needed. After a release, run the public source audit and the content-first check
  on /mortgage-calculator/ as the project rules require.
