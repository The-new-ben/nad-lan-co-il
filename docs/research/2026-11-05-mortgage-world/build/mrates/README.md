# HAD-675 · three rate tools for /mortgage-calculator/ (local build, not deployed)

Built 5.11.2026 on the instruments engine (`core.js`, `core.css`) and the NLMG math of `tools/mortgage.js`. Hebrew, RTL, phones
first. Nothing under `plugins/` was edited; nothing was committed or deployed.

| id | title on the page | decisive number (opening example) |
|---|---|---|
| `mdecision` | החלטת הריבית והמשכנתא שלכם | ₪54 a month per quarter point (400,000 ILS prime, 22 years, prime -0.68) |
| `mreplay` | אם 2022 חוזרת | ₪6,201 peak in 5.2023 of the replay (from ₪5,428, +₪772; 1,000,000 ILS, 25 years, system mix 9.2026) |
| `mexit` | כמה תעלה היציאה | ₪209,765 interest + linkage + fee if exiting in 5 years; existing-loan mode: ₪15,908 on ₪956,994 |

## Files

- `mrates-common.js`: shared math (`window.NLMR`) and page parts (`NLMR.ui`). All payments, balances and fees go through NLMG
  (`pmt, scenario, track, mix, ef2nom, prepayFee, stream, pv`). Two extensions, no new amortization: a month-by-month CPI path
  (the linked track runs in real terms through `NLMG.track`, each month times the index ratio; exact for Spitzer), and the fee of a
  past loan (`NLMG.prepayFee` fed with the Bank of Israel average in force on the loan day and today's, as a one-bucket term table
  plus a `drop`).
- `mdecision.js`, `mreplay.js`, `mexit.js`: one tool each, `spec.custom(root, data)`. Each waits up to 6 s for NLMG and NLMR, so
  script order does not matter.
- `test_mrates.js`: `node docs/research/2026-11-05-mortgage-world/build/mrates/test_mrates.js` -> **50 of 50 passed**: the 5,428
  calibration (5,428.30, equal to `headlines.pay_1m_25y`), the Banking Order example (balance 956,993.98, fee 15,907.53 = lower of
  s.3(3) 17,686 and s.3(4) 15,908, equal to `headlines.prepay_fee`), the 2022 path (15 months 3.2022 to 5.2023, 10 hikes, BoI
  0.10% to 4.75%, CPI +6.00%, peak 6,200.56 in month 15, extra 772.26 = 749.49 prime + 22.77 CPI), the decision delta (54.26 ILS),
  the forecast ramp (-52.88 by 8.2027), and exit identities (price = interest + linkage + fee; no fee on prime, on a var5 change
  day, or at the end).
- `preview.html`: the three tools mounted exactly like the shortcode prints them (section.nli, div.nli-host with data-nli and
  data-nli-data, the PHP summary inside, the related links). Serve the repo root: `python -m http.server 47941 --bind 127.0.0.1`
  in `nad-lan-co-il`, open `/docs/research/2026-11-05-mortgage-world/build/mrates/preview.html`.
- `registry.php.txt`: the three `nadlan_nli_tools()` entries, plus a one-line change to the enqueue closure so an entry can name
  `'deps' => array( 'mortgage', 'mrates-common' )` (deps load first, once). `php -l` clean; the patched loop prints the order
  mortgage, mrates-common, mdecision, mreplay, mexit.
- `summary.php.txt`: helper `nadlan_nli_mrates()` + three `nadlan_nli_summary()` branches; every number computed from the data.
  `php -l` clean and run on the 5.11.2026 data under UTC, Asia/Jerusalem, Kiritimati and Adak (identical output). They print:
  - mdecision: ריבית בנק ישראל: 3.25% מ־3.9.2026, ריבית הפריים 4.75%. ההחלטה הבאה של בנק ישראל: 23.11.2026. במסלול פריים של 400,000 ₪ ל־22 שנה, במרווח הממוצע של המשכנתאות החדשות (פריים פחות 0.68%, 9.2026), ההחזר הוא כ־2,296 ₪ בחודש, וכל רבע אחוז בריבית בנק ישראל מזיז אותו בכ־54 ₪. ...
  - mreplay: בין 14.4.2022 ל־25.5.2023 העלה בנק ישראל את הריבית 10 פעמים, מ־0.10% ל־4.75% ... ההחזר מגיע ל־6,201 ₪ בחודש ה־15, תוספת של 772 ₪ בחודש, מזה 749 ₪ מהפריים.
  - mexit: ... ופורע את כולה ב־11.2026, משלם עמלת היוון של כ־15,908 ₪ על יתרה של 956,994 ₪ ...
- `screens/`: headless Chrome screenshots at 375 and 1280, `opening-*` (the example) and `after-clicks-*` (mdecision on the whole
  mix, mreplay on Habeinleumi's mix at 2,000,000 ILS, mexit on "משכנתא שכבר יש לי"), per tool and full page.

## Integration (release engineer)

1. Copy the four `.js` files to `plugins/nadlan-config/assets/instruments/tools/`.
2. Ship `data/boi-mortgage-v2.json` as `assets/instruments/data/boi-mortgage.json` (same keys as live, plus `by_bank`, `prepay`,
   `flows`, `expect`, `headlines`). The live 16 KB file lacks `by_bank` and `prepay`; on it mreplay and mexit show the "data did
   not load" note and mdecision falls back to `tracks.prime` for the margin.
3. Apply `registry.php.txt` (entries + the `$files` line) and `summary.php.txt` (helper + branches).
4. On the page: `[nadlan_tool id="mdecision"]`, `[nadlan_tool id="mreplay"]`, `[nadlan_tool id="mexit"]`.

## Assumptions shown to the reader (all stated on the tool)

- Rates of by_bank are effective; converted with `NLMG.ef2nom` (r = (1 + e)^(1/12) - 1), the calibration's conversion.
- mdecision: only prime moves on decision day; var5 changes at its change day by its anchor; forecasts reach their value by
  8.2027 on the ramp of tools/mortgage.js (`rampMonths`, the Q3 2027 horizon of `forecast.rate_q3_2027`). No email alert or
  button is shown. The countdown line hides itself once `forecast.next_decision` is past (the date stays).
- mreplay: each month uses the BoI rate in force on its last day and that month's CPI (no known-index lag); prime = your rate +
  the change since 3.2022; var5 keeps its rate (change day is month 61); "variable not linked, not prime" is taken as var5.
- mexit: forecast path (prime to 3.0%, CPI 2.0%); the exit-day average = today's average for the period left minus the forecast
  fall of the policy rate (0.25), with "no change" (always 0 at average rates) and "-1%" beside it; operational fee counted once;
  0.1% short notice and the CPI fee shown apart. Existing loan: the 15th of the loan month picks the average in force; a variable
  loan's balance assumes today's rate from the start; before 11.2021 (start of `prepay.*.rows`) only s.3(3) can be tested.
  Presented as cost by horizon, no "best" mark.

## Checks done

- Language: no blacklisted words, no long dashes or spaced hyphens, no English in visible text (file names aside), no NaN.
- Layout: no horizontal page scroll at 375 or 1280; every control 44 px or taller; one survey-red underline per tool; wide
  tables become cards under 600 px; signed amounts isolated (LRI/PDI) so the sign stays left inside Hebrew.
- Interaction (headless Chrome): mode switches, horizon chips, bank chips, typing an amount and a month, an invalid month (error
  shown), and a `#mexit=` link reopening the same case.
- Not done: the built-in browser pane stayed at its tab cap (all tabs belonged to other sessions), so the pane was not used;
  the evidence is headless Chrome (`screens/`). Not checked inside the live theme.
