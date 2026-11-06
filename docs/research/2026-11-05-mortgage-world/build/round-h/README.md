# Round H (HAD-675): "מהחוזה למפתח", the 7th tool of /mortgage-calculator/

Local only. Nothing deployed, nothing committed, no live write. Built 6.11.2026 from the design board `Keys.dc.html`.

## What was built

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/mkeys.js` | The tool (id `mkeys`), Hebrew only, RTL. Pure logic in `window.NLMK`. On an English mount (`NI.langOf(root) === 'en'`) it draws nothing. |
| `build/round-h/test_mkeys.js` | Node test: indexation.js + mquick.js + mkeys.js with a fake window, on the two real data files. |
| `build/round-h/preview.html` | Local mount, exactly like the shortcode prints it (`section.nli > div.nli-host[data-nli="mkeys"]`), repo scripts in deps order. `?theme=1` adds the live theme stylesheets (read only). |
| `build/round-h/verify_h.py` | Playwright (Chrome, headless) pass: every chip and field, at 390x844 (is_mobile) and 1280x900, plus a phone pass under the live theme. |
| `build/round-h/shots/` | Screenshots (list below). `verify-h.json` and `test_mkeys.out.txt` hold the last runs. |

### Not touched (needed before release)

1. `inc/instruments.php` registry entry, to add next to `mexit`:
   ```php
   'mkeys' => array(
       'name' => 'מהחוזה למפתח: התשלומים, ההצמדה והמשכנתא', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · דירה מקבלן',
       'desc' => 'לקונים דירה מקבלן: כל תשלום לפי התאריך שלו, ההצמדה למדד תשומות הבנייה לפי חוק המכר, מה יוצא מההון העצמי ומה נמשך מהמשכנתא, הריבית עד המסירה בשלוש דרכי גרייס, וההחזר המלא אחרי קבלת המפתח, בתמהיל ובריבית הממוצעים של כל הבנקים לפי בנק ישראל.',
       'deps' => array( 'indexation', 'mquick' ),
       'data' => array( 'boi-mortgage.json', 'cbs-200010.json' ),
   ),
   ```
   The data order does not matter: mkeys finds each file by its shape (`by_bank` / `id 200010`).
2. A server summary in `nadlan_nli_summary()` for readers without scripts (no-JS text). The preview carries a sample sentence with the worked example numbers below.
3. The 7th chip of the switcher on the page: `<button type="button" data-sw="tool-keys" aria-controls="tool-keys">מהחוזה למפתח</button>` and a pane `<div class="nlmx-pane" id="tool-keys">` with `[nadlan_tool id="mkeys"]`. The copy button links to `#tool-keys`, so the pane id should be exactly that.

## The math

Inputs (opening values): price 2,000,000; equity 600,000; signing = today; delivery = signing + 36 months (follows the signing date until the reader types a delivery date); plan "לפי שלבים"; grace "משלמים ריבית"; 25 years; annual index change = `NLIX.trailing()`.

1. **Plan and linkage: NLIX, not re-implemented.** `NLIX.schedule(kind, sign, delivery)` gives the payments (kinds `end`, `stages`, `thirds`); `NLIX.compute({price, sign, delivery, share, floor: true, rows}, cbs, annual)` gives each payment's linkage. `share` = 50 (the legal maximum) for a contract from 7.7.2022, 100 for an older one (the upper bound, said on the page). A payment dated after the contractual delivery (a very short build) is moved to the delivery date before NLIX runs. Nothing in NLIX's API blocked anything.
2. **Funding.** Payments in date order; equity pays each payment plus its linkage until it runs out; the rest is drawn.
3. **Rate.** `by_bank`, bank `system`, latest month: shares normalized, monthly rate per track `(1 + e)^(1/12) - 1`; before the keys the mix-weighted monthly rate `rm = Σ share × r`.
4. **Grace.** A draw in month m bears interest for months m+1 through the delivery month (`n` months; a draw on the delivery date bears none).
   * משלמים ריבית: interest paid monthly, `cumulative draws × rm`; total `Σ draw × rm × n`; balance at the keys = the draws.
   * הריבית נצברת: balance `Σ draw × (1 + rm)^n`.
   * החזר מלא מיד: each draw starts its own Spitzer schedule per track over the term; payment after a draw = `cumulative draws × payPer1`; balance at the keys = what is left of each schedule after `n` payments.
5. **After the keys.** `balance × NLMQ.payPer1(by_bank, 'system', last month, term)` (mquick.js). In "החזר מלא מיד" it is the sum of the draws' own payments, which is `draws × payPer1` (the same headline as partial with constant rates; what differs is the balance at the keys and what was paid before).
6. **Financing share.** The largest sum owed (draws, or the balance with capitalized interest in full grace) / contract price; above 75% underlined in #C42550 with the directive 329 sentence.

### Worked example (real data: Bank of Israel `by_bank` 9.2026, CBS 200010 latest 9.2026)

2,000,000 ₪, equity 600,000 ₪, signed 6.11.2026, delivery 6.11.2029, "לפי שלבים", 25 years.

* Known index on 6.11.2026: 9.2026 = 104.0 (base). Annual change for unpublished months: 104.0 / 100.4 (9.2025) - 1 = 3.586%.
* All-banks mix 9.2026: fixed not linked 30.675% at 4.7162%, prime 26.482% at 4.1477%, variable not linked 35.034% at 4.425%, variable CPI 3.385% at 3.28%, fixed CPI 4.424% at 3.2641%. `rm` = 0.35548% a month. `payPer1(25)` × 1,000,000 = 5,428 (the mquick calibration).

| Date | Payment | Linkage | From equity | Drawn | Monthly interest after it |
|---|---|---|---|---|---|
| 11.2026 | 20%, 400,000 | none (s.5ג) | 400,000 | 0 | |
| 06.2027 | 15%, 300,000 | 3,114 | 200,000 | 103,114 | 367 |
| 01.2028 | 15%, 300,000 | 6,293 | 0 | 306,293 | 1,455 |
| 09.2028 | 15%, 300,000 | 10,008 | 0 | 310,008 | 2,557 |
| 04.2029 | 15%, 300,000 | 13,330 | 0 | 313,330 | 3,671 |
| 11.2029 | 20%, 400,000 | 22,295 | 0 | 422,295 | (keys) |

* Linkage until delivery **55,040 ₪** (all projected; nothing after 9.2026 is published yet).
* משלמים ריבית: interest until delivery **57,809 ₪**, mortgage at delivery 1,455,040 ₪, share 72.8%, **ההחזר המלא אחרי המפתח 7,898 ₪**.
* הריבית נצברת: capitalized 59,716 ₪, balance 1,514,756 ₪, share 75.7% (flagged), payment 8,223 ₪.
* החזר מלא מיד: paid to the bank before the keys 88,276 ₪ of which interest 56,808 ₪, balance at the keys 1,423,572 ₪, payment 7,898 ₪.
* Same case with equity 400,000: share 82.8%, flagged.

## Test results

* `node test_mkeys.js`: **54/54 passed** (`test_mkeys.out.txt`). Covers the six requested checks: (a) 20/80 after 7.7.2022, first 20% linked part 0 and "בלי הצמדה", the 80% half linked, total equal to NLIX.compute; (b) equity = price with a flat index: no draws, headline "לא צריך משכנתא" (never "0 ₪"); (c) partial interest = cumulative draws × rm on every row, total = Σ draw × rm × n; (d) full grace balance 1,514,756 > draws 1,455,040, equal to Σ draw × (1 + rm)^n; (e) payment = balance × payPer1 within 1 ₪ for 20/25/30 years in partial and full, and draws × payPer1 in immediate; (f) the 75% flag on and off. Plus funding identities, equity-first order, old-law contract, 8 validation messages, and a wording scan of 240 generated strings (no long dashes, no banned words, no NaN).
* `python verify_h.py` (served on 127.0.0.1:47971, server stopped after): **120/120 passed** (`verify-h.json`). At both widths: the headline equals NLMK.compute on the form's values after every chip (3 plans, 3 grace choices, 3 terms) and every field (price, equity, signing date moving the untouched delivery, a typed delivery staying, index 5% and -1%); the 75% underline in #C42550; validation messages for empty price, equity above price, delivery before signing, empty dates, empty index change; "לא צריך משכנתא"; copy to the clipboard and the prompt fallback; no console errors or warnings; no horizontal scroll (`scrollWidth - innerWidth = 0`); every button and input at least 44 px tall; every input labelled, every chip group named; running sentences in IBM Plex Sans Hebrew, numbers in IBM Plex Mono. Under the live theme stylesheets (phone): heading, list, chips, inputs and the timeline text keep their own style.

## Screenshots (`build/round-h/shots/`)

`mkeys-default-390.png`, `mkeys-default-1280.png`, `page-default-390.png`, `page-default-1280.png`, `mkeys-grace-full-{390,1280}.png`, `mkeys-grace-immediate-{390,1280}.png`, `mkeys-plan-2080-{390,1280}.png`, `mkeys-plan-203050-{390,1280}.png`, `mkeys-over75-{390,1280}.png`, `mkeys-index-negative-{390,1280}.png`, `mkeys-error-price-{390,1280}.png`, `mkeys-error-delivery-{390,1280}.png`, `mkeys-no-mortgage-{390,1280}.png`, `mkeys-after-all-{390,1280}.png`, `mkeys-theme-390.png`.

## Open questions

1. **Financing share basis.** Now: the largest sum owed / price (in full grace the capitalized balance, so 600,000 equity is flagged at 75.7% there but not in partial at 72.8%). Directive 329 measures the loan at approval; keep, or use the draws only?
2. **Contracts before 7.7.2022.** Linked in full (upper bound) with a sentence saying so. Add a "החלק המוצמד" field instead?
3. **Index floor.** Inherited from indexation's default (`floor: true`: a falling index does not lower the price). It only matters for past months.
4. **Interest timing.** Month granularity: a draw bears interest from the next month through the delivery month. Banks count from the release day; the difference is part of a month per draw.
5. **Grace limits.** Banks cap grace length and amount; no official number was found in the data files, so nothing is shown. Add one if a source is chosen.
6. **Equity.** The typed equity is assumed to go to the developer only; purchase tax and lawyer come on top (mbudget and mready already handle them).
7. **Currency sign in the headline** follows mquick exactly (`<bdi>7,898 ₪</bdi>`, sign to the right of the digits). A change would be a shared one for both tools.

Not verified: a real phone (iOS date picker, clipboard), the WordPress enqueue path with `deps` (the registry was not edited), the English page (the tool draws nothing there by design).
