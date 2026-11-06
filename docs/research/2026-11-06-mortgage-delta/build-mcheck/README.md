# mcheck: "בדיקת משכנתא לפני חתימה" (HAD-675, built 6.11.2026, LOCAL ONLY)

Spec: `../presign.md` (sections 2 to 6), context `../delta.md` and `../inventory.json`. Nothing was deployed, nothing written to
the live site, nothing committed, and `plugins/nadlan-config/inc/instruments.php` was not edited.

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/mcheck.js` | The tool (new). Pure logic on `window.NLMC`, the page part on the instruments engine (`NadLanInstruments.register('mcheck', { custom })`, started through `NLMR.ui.start`) |
| `build-mcheck/registry.php.txt` | The `nadlan_nli_tools()` entry (name, cat, kicker, desc, deps, data, related) and the `nadlan_nli_summary()` branch. Linted with PHP 8.3 and rendered against the real data file in a scratch harness |
| `build-mcheck/test_mcheck.js` | Node test on the real data and the real tool scripts with a fake `window` |
| `build-mcheck/preview.html` | Local mount exactly like the shortcode prints it, scripts in the `deps` order; `?theme=1` adds the live theme CSS (read only) |
| `build-mcheck/verify.py` | Playwright, Chrome headless, 390x844 and 1280x900; starts `python -m http.server 47971 --bind 127.0.0.1` and stops it; writes `screens/` and `verify.json` |

Reused, not copied: `NLMG` (mortgage.js: mix, scenario, prepayFee, stream, pv, bucket, pmt), `NLMR` (mrates-common.js:
exitScenario, bankMix, replayPath, replay, parseMonth, mDiff, and the page parts `NLMR.ui`), `NLMO` (moffers.js: bankRef, place,
trackCmp, clean, normalize, compare, names, ef2nom), `NLMQ.fullCost` (mquick.js). Declared deps: `mortgage, mrates-common, moffers,
mquick`. New math, small: the overall rate of a cash flow (`irrOf`, a diagnostic used by the tests only; row 7 is never recomputed) and
the capitalization fee of a variable track that changes every 2, 2.5, 7 or 10 years (`capFee`: the formula of `NLMG.prepayFee`, which
knows only every 5 years, with that track's own change day; fixed and every-5-years tracks call `NLMG.prepayFee` itself, and the
test proves the 7-year fee equals `NLMR.exitAt`, the mexit engine, to the agora).

## What the reader types (451, addendum 6)

Header: bank (the 7 banks of קו המשווה + "בנק אחר"), approval date, guarantors yes/no, price, buyer type (single, replacement,
investment, reduced price), new or second hand, delivery month (new only), requested loan. Four baskets with a switcher (one basket
per screen): quick mode = row 3 (term in months) and rows 7 to 11; one tap opens every basket's tracks: row 1 name (fixed not
linked, fixed CPI, prime, variable not linked / CPI with change every 1, 2, 2.5, 5, 7, 10 years, eligibility loan), 2 amount, 3
months, 4 method + grace (proposed basket only, as the form), 5 rate, 6 anchor + margin + frequency, 12 interest-difference fee
yes/no; plus "מידע נוסף": reservation or option fee seen, new lien yes/no. The reader's context (optional): net income, other loan
payments, equity, years to exit, eligibility yes / no / not checked, life and structure quotes, arnona and committee. Optional:
up to two other banks' uniform baskets (rows 3, 7 to 11). No name, ID, phone or email field. Mode 2: the final documents (date,
loan, fees, guarantors, a new insurance requirement, the tracks), with "copy from the proposed basket" so only changes are typed.

## The 28 checks: all in

| # | In? | How it flags |
|---|---|---|
| 1 Validity | yes | 24 days (12 with no new lien); red expired, amber under 5 days, info otherwise; also shown as a strip above the summary |
| 2 Completeness | yes | red when a basket was not typed (text says "if it is missing on the approval too"), the exemptions in the rule |
| 3 Uniform form | yes | amber: term not 120/180/240/300/360, mix not the definition (shares within 1 point), variable not every 5 years. The mix part needs the tracks |
| 4 Totals | yes | red: tracks do not add up to the requested loan (tolerance max(1,000, 0.1%)); red: loan + equity below the price; info: what is left for tax and lawyer |
| 5 LTV | yes | red above `rules.ltv[buyer]`; reduced price: equity vs 100,000 / 60,000 from `rules.reduced` |
| 6 Payment to income | yes | (row 8 + other loans) / income: red > 50%, amber > 40% (`rules.pti_*`); uniform baskets' range shown |
| 7 Variable share | yes | red above two thirds, per basket with tracks (basket 2 at exactly 2/3 passes) |
| 8 Term | yes | red above 30 years, per basket and per track |
| 9 IRR vs the bank (קו המשווה) | yes | info only: gap to the bank's own 9.2026 figure, all banks, the big-5 range (`NLMO.bankRef / place`) |
| 10 Rate per track | yes | proposed basket: bank and all-banks average per track (effective to nominal), the term-file average for fixed tracks, the gap a month and over the track (`NLMO.trackCmp`); amber when 0.1 above both |
| 11 Across banks | yes, with an optional other approval | `NLMO.clean / normalize / compare` per uniform basket, cheapest named; info |
| 12 Recompute rows 8 to 10 | yes, full rows | on the BoI Research forecast (`NLMR.exitScenario`); the text says banks use the 451 forecasts; amber when row 8 differs by over 3% |
| 13 Highest payment | yes | row 9 and its month, PTI at the peak, +1% on every variable track, and the 2022 to 2023 replay (`NLMR.replay`, boi-rate + CPI files); amber if a peak passes 50% |
| 14 Fees | yes | red on a reservation / option fee (451 s.8); row 11 per basket, proposed vs uniform, vs other banks; not checked when row 11 is empty |
| 15 File opening fee | yes, info | the bank tariff; Kol Zchut's "up to 360 ₪" attributed and called unsourced |
| 16 Early repayment | yes | amber when row 12 says "yes" on prime / yearly / eligibility; fee at the reader's horizon (capitalization, operational, 0.1% notice); amber when 50%+ fixed meets a fee |
| 17 Balloon, bullet, grace | yes | amber with the lump sum and its month (`NLMG.track` lump) and the grace type |
| 18 Linkage | yes | linked share, payment and balance after 5 years at the 2.0% forecast vs no CPI |
| 19 Variable mechanism | yes | amber when anchor or margin is missing, or prime rate ≠ prime + margin; first change month; the 451 sentence on the anchor |
| 20 Guarantors | yes | amber with two questions |
| 21 Insurance rights | yes, info | 451 s.11 rules; up to 30,000 ₪ when the loan is that small; not before delivery for a new home; CMA links |
| 22 Full monthly cost | yes, info | `NLMQ.fullCost`; empty quotes stay empty ("לא הוקלדו") |
| 23 Appraisal | yes, info | 451 s.9 |
| 24 Eligibility | yes | amber "not checked"; amber "eligible but no eligibility track" |
| 25 New home | yes, info | delivery vs grace in months; points to the mkeys tool on the page |
| 26 Mode 2 diff | yes | every change listed: red when it costs more or adds a demand (amount up, rate up, new fee, new track, missing track, term, method, grace, anchor, frequency, guarantors, insurance), amber when lower; amber when the documents come after the hold (451 s.4ג(ו)) |
| 27 Payment instructions | yes, info | confirm by phone to a saved number |
| 28 Credit report | yes, info | Kol Zchut 27.8.2025 + creditdata.org.il |

Not built from the spec: the negotiation letter (moffers has it), a WhatsApp-only share (the shared bar has copy, WhatsApp, case link
and print), FX tracks (0.1% of new loans, delta.md C2). A check that lacks its data goes to "לא ניתן לבדוק" with the reason.

## Worked example (the button "מילוי דוגמה", built at run time from boi-mortgage.json)

Approval dated 5 days before today (on 6.11.2026: 1.11.2026), "בנק אחר", 1,200,000 ₪ on 1,600,000 ₪, single home, second hand,
no guarantors. Proposed basket = the all-banks mix and rates of 9.2026 (effective turned nominal): fixed not linked 368,000 at
4.62%, prime 318,000 at 4.07% (prime minus 0.68), variable not linked every 5 years 420,000 at 4.34%, variable CPI 41,000 at 3.23%
(anchor 1.64 + 1.59), fixed CPI 53,000 at 3.22%; 300 months. Rows 8 to 10 computed by the tool: 6,511 / 6,764 in month 300 /
1,982,050. Row 7 = 5.09%, the all-banks IRR the Bank of Israel published. Uniform baskets at the same track rates: basket 1 6,752 /
2,025,596; basket 2 6,320, 7,514 in month 300, 2,052,809; basket 3 6,557 / 1,945,697. Row 7 of the uniform baskets and row 11 stay
empty: no official figure exists (our own IRR on the system mix is 4.46% against the published 5.09%, because the banks use the
451 forecasts, so it is not printed as if it were the bank's). Context: income 24,000, other loans 1,200, equity 450,000, exit in 7
years, eligibility not checked.

Result: 0 red, 2 to check (19: no margin on the variable not linked track; 24: eligibility not checked), 22 info, 2 not checkable
(11, 14). The summary (7 sentences): 75.0% financing at the 75% limit; 19 days left, until 25.11.2026; first payment 6,511 ₪ = 32.1%
with the other loans, highest 6,764 ₪ in month 300 = 33.2%; IRR 5.09% = the all-banks 9.2026 figure; exit in 7 years: about
5,153 ₪ capitalization fee on about 990,102 ₪; 7.8% CPI-linked, forecast 2.0% (21.10.2026); the counts. Stress: +1% on the
variable tracks 7,220 ₪; the 2022 path peaks at 7,442 ₪ in month 15. 10 questions to ask the bank.

## Tests

- `node build-mcheck/test_mcheck.js`: **91/91 passed** (each check 1 to 28 with its red / amber / info / not-checkable cases; the
  example against the 5,428 calibration and `NLMQ.payPer1`; fee = `NLMR.exitAt`; the summary 5 to 8 sentences; no recommendation
  word, no long dash in any output, copied text or the source; no "0 ₪" for an untyped value; a broken hash cleaned; an
  out-of-range rate not used).
- `python build-mcheck/verify.py`: **99/99 passed** at 390x844 and 1280x900 and once with the live theme CSS: no console errors, no
  horizontal scroll, every control at least 44 px (buttons, selects, input boxes, summaries, share links, the advisor link; inline
  links inside sentences are text, not controls), every input and select labelled, empty state, example, each flag group, the
  questions, all rows, a red case (expired, LTV, totals, reservation fee), mode 2 (rate up, new insurance, after the hold), print
  (form hidden), copy and the case link reopening the same result. Screens in `build-mcheck/screens/` (01 to 12).

## Design

Palette from the house system, not a default: ink #12202A, ink-2 #3E4C58, mute #5E6A75, line #D3DCE2, sea #2F6F86, ground
#F6F8F9; red = the survey red #C42550 (border and the warning underline on red titles); amber = the system's yellow token #F2D15A,
used only as a 4 px marker beside ink text, never as text or a mustard fill; info = sea. Faces: IBM Plex Sans Hebrew for sentences,
IBM Plex Mono for every number (wrapped in `bdi.m` inside sentences). Why not the default look: a regulator's form (the 451 rows,
numbered as on the paper) with survey marks, no cards stamped on every block, no cream, no gradient. CSS is scoped to `#nlmc` with
`!important` on what the theme restyles (legend, list bullets, headings, buttons).

## Open questions / unverified

1. The chip in the /mortgage-calculator/ switcher ("בדיקה לפני חתימה", presign.md section 1) is page content: Ben's call, not built.
2. Existing loan payments are added to the mortgage payment for the 40% / 50% test (the afford.js convention); 329's exact
   definition of disposable income was not re-read here.
3. "Variable" for the two-thirds rule includes every-5-years tracks (the uniform basket 2 sits exactly at 2/3, consistent); not re-read in 329.
4. The 451 forecasts the banks must use are not in our data, so rows 8 to 10 are recomputed on the BoI Research forecast and the
   IRR is never recomputed; the text says so.
5. Stress and replay treat a variable track that changes more often than every 5 years like prime from month 1 (conservative).
6. gov.il lists 9 mortgage banks (incl. Igud and Mishkan); the select offers the 7 banks with data in קו המשווה + "בנק אחר".
7. Kol Zchut's 360 ₪ file fee is shown only as attributed and unsourced.
8. The owner pages linked (/mortgage-calculator/mortgage-pre-approval/, /mortgage-home-insurance/, /mortgage-refinance/,
   /mortgage-advisor/, and ltv-ratio, repayment-capacity, interest-rates, /cpi-calculator/, /new-projects/construction-input-index/
   from the registry's related lists) were not fetched live in this session.
9. On a phone with full rows the result sits below five track cards; a "to the result" jump link may help (not built).
10. Not tried in a real WordPress page, on a real phone, or in Safari.
