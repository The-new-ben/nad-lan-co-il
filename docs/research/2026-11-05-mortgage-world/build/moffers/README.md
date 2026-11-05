# moffers: "שלוש הצעות, טבלה אחת" (HAD-675, built 5.11.2026)

A new tool for https://nad-lan.co.il/mortgage-calculator/ on the NadLan Instruments engine (custom surface). Built locally
only: nothing under `plugins/` was changed, nothing deployed or committed. The release engineer integrates it.

## What it does

Every mortgage approval in principle (אישור עקרוני) must show three uniform baskets, Bank of Israel directive 451, circular 2694
(31.1.2022, in force 31.8.2022), addendum 5. **Verified** in `docs/research/2026-10-26-upgrades/u1-mortgage-calculator/dna.md`
section 6 and in the data key `baskets.list`:

| Basket | Mix |
|---|---|
| סל אחיד 1 | 100% fixed, not linked (קל"צ) |
| סל אחיד 2 | 1/3 fixed not linked + 1/3 prime + 1/3 variable every 5 years, **CPI-linked** (`var5_cpi`) |
| סל אחיד 3 | 1/2 fixed not linked + 1/2 prime |

(The brief's sentence "variable unlinked/ CPI" for basket 2 is imprecise: the source and the data both say CPI-linked.)

**Inputs** (2 or 3 approvals, a tab per approval, "+ הצעה שלישית"):
- the bank, from the 7 banks in `by_bank.banks` (plus "בנק אחר"); until a bank is picked the approval is called "בנק א׳", "בנק ב׳", "בנק ג׳";
- the loan amount and the term of the approval;
- per basket: ריבית כוללת חזויה, סך התשלומים הצפוי, ההחזר החודשי הגבוה הצפוי, ההחזר הראשון (any may be left empty);
- optional, per approval: the bank's own proposed mix (track, share, rate, years; up to 6 tracks).

Impossible numbers are flagged under the field and left out of the comparison (total below the loan, interest outside 0 to 20%,
term outside 1 to 30 years); doubtful ones are only flagged (highest payment below the first, total above highest x months).

**Outputs**
1. **One normalized table.** Per basket, the approvals side by side, the cheapest marked (green tag and cell), and the gap
   "היקרה פחות הזולה" for every figure. The headline (the one survey-red underline) is the gap in shekels over the loan in the
   basket chosen in "הסל להשוואה" (opens on basket 2, as on the design board), with the gap in the highest monthly payment.
   Normalization: approvals for different amounts are scaled to the first approval's amount (payments of a fixed mix are
   proportional to the principal; the overall interest is a rate and is not scaled). When the terms differ, the cheapest is
   the lowest overall interest, not the lowest total (a 20-year and a 30-year total are not comparable); the page says so.
   Phones (< 720 px): one card per basket (the chosen one), each bank a block with the four figures; wide: the full table.
2. **Each approval against that bank's own Bank of Israel average** ("קו המשווה", `by_bank.latest`, September 2026): the bank's
   average overall interest next to each basket's typed interest, the gap in points, and where the chosen basket sits between
   the cheapest and the dearest of the five large banks (a dot ladder with the five large banks, all banks, any smaller bank
   picked, and the approvals). With a mix typed: per track, the offered rate, the bank's average for that track (effective as
   published, converted to nominal with `12 x ((1 + r)^(1/12) - 1)`, the same conversion as `tools/mortgage.js`), its share of
   the bank's credit, the gap and its monthly shekel effect (Spitzer, no CPI, no rate change). With no bank picked, or
   "בנק אחר", the reference is all banks, and the page says why. The wording states that a bank average depends on that bank's
   mix and clients, and is not an offer; for Bank of Jerusalem it adds its CPI-linked share against all banks.
3. **Negotiation text** (Hebrew, first person singular, polite, facts only): addressed to the dearest approval in the chosen
   basket by default, selectable. It contains only typed numbers and official averages with their month (no computed gaps,
   no advice wording). Copy button "העתקת הנוסח".
4. **Advisor**: "העתקת הטבלה" (the table as text) and a plain link "לשלוח את הטבלה ליועץ משכנתאות" to
   https://nad-lan.co.il/mortgage-advisor/ (the page exists: `inc/professional-profile.php` links it as "האם צריך יועץ משכנתאות").
   No form.

Share bar: "העתקת התוצאה" (the table + a link that reopens the case), "הדפסה או שמירה כקובץ", "קישור שפותח את אותם מספרים"
(`#moffers=` state, same pattern as `#mortgage=`). **No WhatsApp button and no WhatsApp wording**: the approved design board
(Tools.dc.html panel 2) shows "העתקת התוצאה · הדפסה · קישור למקרה" only, and Ben's rule is that WhatsApp wording is his.

## How it relates to `tools/mortgage.js` (`#bank-offer-check`)

`bank-offer-check` takes ONE offer, track by track, against the **system-wide** averages (SDMX by track and the BoI
average-by-term files), turns the gap into shekels for that mix and places the loan among last month's mortgages. moffers does
not repeat that: it compares **2 or 3 approvals** on the **uniform baskets** (like for like across banks), and each bank against
**its own** published average (TamInt010, a source `mortgage.js` does not read). Suggested placement on the page: directly after
the Mortgage 2.0 tool, with a line in `bank-offer-check` pointing to it ("יש לכם שני אישורים או יותר? השוו אותם בטבלה אחת"); that
line is a change to `mortgage.js`, left to the release engineer.

## Sources (every number on the page comes from these or from the visitor, with its date)

| Data key | Source | As of |
|---|---|---|
| `by_bank` (rates, IRR, mix per bank) | Bank of Israel, Banking Supervision, "השוואת ריביות - הלוואות למטרת מגורים", `TamInt010.xls` sheets L01/L02, linked from https://www.boi.org.il/information/bank-paymnts/financial-education/campaigns/boi-equator/mortgage/ | month 2026-09, file 20.10.2026, retrieved 5.11.2026 |
| `baskets` | Directive 451, circular 2694, addendum 5 (via dna.md section 6, read 25.10.2026) | 31.1.2022, in force 31.8.2022 |
| `tracks` (basket track names), `policy.prime` (prime in the mix hint) | Bank of Israel (SDMX), as in the live file | policy 5.11.2026 |

Data file used: `docs/research/2026-11-05-mortgage-world/data/boi-mortgage-v2.json` (will ship as `data/boi-mortgage.json`
with the same keys; the tool needs `by_bank`, `baskets`, `tracks`, `policy`, `built`).

Example (marked "דוגמה" until a number is typed): two approvals for 1,200,000 ₪ over 25 years, computed by me with Spitzer,
constant rates (bank A: 4.85 / 4.45 / 3.35; bank B: 4.70 / 4.25 / 3.20 nominal) and the BoI 2.0% inflation forecast on the
linked third of basket 2. Not a real approval; realistic against the September 2026 averages.

## Files

| File | What |
|---|---|
| `moffers.js` | The tool. Pure logic on `window.NLMO` (check, clean, normalize, compare, bankRef, place, trackCmp, letter, tableText, example); the surface registers `moffers` with `spec.custom`. Scoped CSS (`.nlo`, injected once as `#nlo-css`), engine classes reused (panel, title, strip, form fields, seg, answer, lines, note, doc, share, eg). QA handle: `NLMO.ui` (state, last, paint, rebuild, link). |
| `test_moffers.js` | `node test_moffers.js [data.json]`: 17 tests. |
| `preview.html` | The shortcode markup with core.css/core.js and the v2 data. |
| `registry.php.txt` | The `'moffers'` entry for `nadlan_nli_tools()` in `inc/instruments.php` (after `'mortgage'`). |
| `summary.php.txt` | The `nadlan_nli_summary()` branch: one paragraph with the all-banks overall interest, the five large banks' range and the three baskets, all from the data. |
| `screenshot-375.png`, `screenshot-1280.png` | Full-page captures (headless Chrome; the 375 one through a 375 px frame, since the headless window will not go below about 500 px). |

## Tests and checks (evidence class)

- **code**: `node test_moffers.js` 17/17: basket definitions in the data; latest month 2026-09 and the five large banks (min
  הבינלאומי 4.748, max מזרחי טפחות 5.1613, all banks 5.0949); normalization (equal amounts, scaled amounts where the raw-dearer
  approval wins after scaling); cheapest and gaps on the example (basket 2: 36,212 ₪ and 131 ₪); ties; different terms by the
  overall interest; a basket typed in one approval only; dropped and flagged numbers; placement among the five large; the
  effective-to-nominal conversion equals `mortgage.js`; the negotiation text in 5 cases contains only typed or official numbers
  (every digit run checked), no gap figures, no advice wording, no long dash; the table text; a source scan of every Hebrew
  string for the language-dna blacklist, spaced hyphens, long dashes and any WhatsApp element.
- **code**: `php -l` on both PHP fragments inside a harness (PHP 8.3), and the summary run on the real data. Output:
  "...של ספטמבר 2026 הייתה 5.09% בכל הבנקים, ובחמשת הבנקים הגדולים בין 4.75% (הבינלאומי) ל־5.16% (מזרחי טפחות)..."
- **eyes** (built-in browser pane, served by `python -m http.server` from the repo root): 375 px and 1280 px looked at section by
  section. Fixed during the pass: clipped rate cells in the mix rows, misaligned input pairs, a squeezed dot ladder on phones,
  mono font on Hebrew words, direction of figures inside Hebrew sentences, the phone cards showing at 1280, the letter section
  losing focus on its select, a `prompt()` fallback that threw where prompt is unsupported.
- **code** (DOM in the pane): no horizontal overflow at 375 (scrollWidth 375) or 1280; every control of the tool at least 44 px
  high; real clicks and typing: bank pick renames the tab and moves every section to that bank's average; "+ הצעה שלישית" and
  typing its basket 2 (a too-low total is flagged and excluded, the corrected one enters the ladder); basket switch moves the
  headline (35,818 ₪ for basket 3), the phone card and the ladder; the three copy buttons copy the letter, the table and the
  table with the case link (clipboard stubbed, the pane blocks it); the case link reopens banks, numbers, mix and basket.
- **unverified**: the real site page (theme CSS around `.nli`), print layout, VoiceOver/TalkBack.

## Integration (for the release engineer)

1. Copy `moffers.js` to `plugins/nadlan-config/assets/instruments/tools/moffers.js`.
2. Add the `registry.php.txt` entry and the `summary.php.txt` branch to `inc/instruments.php`.
3. Ship the v2 data as `data/boi-mortgage.json` (the tool shows "הנתונים לא נטענו" without `by_bank`).
4. Place `[nadlan_tool id="moffers"]` on /mortgage-calculator/ after the Mortgage 2.0 tool (no new URL). Run `kw_guard.py` on
   the H2 "השוואת הצעות משכנתא: שלוש הצעות, טבלה אחת" and the content-first check after the release.

## Open questions

1. Is the "ריבית כוללת חזויה" printed on an approval exactly the measure behind the Supervision's per-bank IRR? Both follow the
   directive 451 formula per the BoI notes, but I did not see a real approval form. Needs one approval (any bank) to confirm the
   four printed lines, including whether "ההחזר הראשון" is printed per basket (dna.md names three figures).
2. WhatsApp: left out per the approved board. If Ben wants the engine's standard "שליחה בוואטסאפ" here, it is his word.
3. Banks outside the TamInt010 list (for example Yahav or Massad, if offered under their own names) fall back to "all banks" via
   "בנק אחר". Should those names map to their parent group (Mizrahi-Tefahot, First International)?
4. Finding outside this tool: `core.js` (share bar) and `tools/mortgage.js` call `window.prompt` in the clipboard-failure path
   without a guard; in a browser without `prompt()` this throws an uncaught error. moffers guards it.
5. The September 2026 averages move monthly (around the 20th); all text follows the data, nothing is hard-coded except the
   example approvals.
