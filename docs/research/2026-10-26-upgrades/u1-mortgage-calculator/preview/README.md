# Mortgage 2.0 (tool id `mortgage`): local build, 25 to 26.10.2026

Local only. Nothing was deployed, `inc/instruments.php` and `core.js` / `core.css` were not edited, no Linear or Notion item was created.
Spec: `../dna.md` sections 6, 8.4, 8.5, 8.5.1 and 8.6.

## Files (all new)

| File | What it is |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/mortgage.js` | The tool. A custom surface on the engine (`custom(root, data)`, like condo.js and soilmap.js) because the engine's `rows` field only takes number inputs and the spec needs a track select, method, grace type, a moat table, charts and compare. It reuses the engine's identity classes (`nli__panel`, `nli__strip`, `nli__pre`, `nli__seg`, `nli__in`, `nli__answer`, `nli__lines`, `nli__share`...) and injects its own scoped CSS (`.nlm`, `#nlm-css`). Pure math in `window.NLMG`. |
| `plugins/nadlan-config/assets/instruments/data/boi-mortgage.json` | The only data file (key `boim`), 16.8 KB, every value with its date and source URL. |
| `tools/instruments/build_boi_mortgage_data.py` | Builds the JSON from Bank of Israel SDMX (BIR_MRTG_99, MNT_RIB_BOI_D), the BoI files `mashfix.xls` and `pribmash.xls` (https://www.boi.org.il/boi_files/Pikuah/), and CBS series 120010. Any source that fails keeps the last verified value from dna.md section 6 with `"from": "from research 25.10.2026"`. Run with a Python that has xlrd: `python -m venv v && v\Scripts\pip install xlrd==2.0.1 && v\Scripts\python tools/instruments/build_boi_mortgage_data.py` (without xlrd the two xls blocks fall back to the research values). |
| `tools/instruments/test_mortgage_math.py` | Cross-check: an independent Python port vs the real `mortgage.js` run in node. `python tools/instruments/test_mortgage_math.py` |
| `docs/research/.../preview/index.html` | This preview: the engine's own mount markup (the HTML `[nadlan_tool id="mortgage"]` prints), fonts, `core.css`, `core.js`, `mortgage.js`, deferred as on the site. Open over http: `http://localhost:8131/docs/research/2026-10-26-upgrades/u1-mortgage-calculator/preview/` (the projects-hub-preview server). On `file://` the browser blocks the JSON fetch, so use the server. |

## The registry entry to add to `inc/instruments.php` (same shape as `'prime'`)

```php
'mortgage' => array(
	'name' => 'מחשבון משכנתא לפי מסלולים', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · משכנתא',
	'desc' => 'מחשבון משכנתא לפי מסלולים: החזר ראשון, ההחזר הגבוה הצפוי, ריבית, הצמדה ולוח סילוקין, לפי סכום, לפי החזר חודשי או לפי מחיר והון עצמי; שלושת הסלים האחידים של בנק ישראל, בדיקת התמהיל מול הוראה 329, פירעון מוקדם עם הערכת העמלה, והשוואת ההצעה מהבנק לריבית הממוצעת שבנק ישראל פרסם לאותו מסלול ולאותה תקופה.',
	'data' => array( 'boi-mortgage.json' ),
	'related' => array( '/mortgage-calculator/mortgage-repayment-capacity/' => 'כמה משכנתא אפשר לקחת', '/mortgage-calculator/mortgage-interest-rates/' => 'ריבית משכנתא היום', '/mortgage-calculator/mortgage-ltv-ratio/' => 'אחוז מימון', '/mortgage-calculator/reverse-mortgage/' => 'מחשבון משכנתא הפוכה', '/mortgage-refinance/' => 'מחזור משכנתא', '/mortgage-calculator/mortgage-for-any-purpose/' => 'משכנתא לכל מטרה', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת' ),
),
```

Mount: `[nadlan_tool id="mortgage"]`. A page can open on a ready case: `[nadlan_tool id="mortgage" preset="b2"]` (keys `b1`, `b2`, `b3`, `three`, `first2m`; the shortcode already passes `preset`). The offer check carries `id="bank-offer-check"`, so the page CTA "בדיקת הצעה מהבנק" can link to `#bank-offer-check`; for "לחישוב ההחזר" put an anchor right before the shortcode.

Optional, for readers without scripts and for search engines (a branch in `nadlan_nli_summary()`, same pattern as `'prime'`):

```php
if ( 'mortgage' === $id ) {
	$path = dirname( __DIR__ ) . '/assets/instruments/data/boi-mortgage.json';
	$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
	if ( ! is_array( $d ) || empty( $d['rates'] ) ) { return ''; }
	$m = $d['market']['month']; $mm = (int) substr( $m, 5 ) . '.' . substr( $m, 0, 4 );
	return '<p>ריבית ממוצעת במשכנתאות חדשות לפי בנק ישראל (' . esc_html( $mm ) . '): קבועה לא צמודה ' . esc_html( number_format( $d['rates']['fixed_nl']['rate'], 2 ) ) . '%, קבועה צמודה '
		. esc_html( number_format( $d['rates']['fixed_cpi']['rate'], 2 ) ) . '%, משתנה צמודה ' . esc_html( number_format( $d['rates']['var_cpi']['rate'], 2 ) ) . '%. ריבית בנק ישראל '
		. esc_html( number_format( $d['policy']['rate'], 2 ) ) . '%, פריים ' . esc_html( number_format( $d['policy']['prime'], 2 ) ) . '%. ' . esc_html( number_format( $d['market']['loans'] ) ) . ' משכנתאות חדשות בחודש, בממוצע '
		. esc_html( number_format( $d['market']['avg_loan'] ) ) . ' ₪ למשכנתא.</p>';
}
```

## The data (boi-mortgage.json, built 25.10.2026, all sources reached live)

- Track averages, new housing loans, 8.2026 (SDMX): fixed not linked 4.62% (Jun 4.73, Jul 4.63), fixed CPI 3.29%, variable CPI 1.64% + 1.55% = 3.19%.
- Average rate by term, in force from 19.10.2026 (reporting month 9.2026), effective then nominal: not linked up to 1 year 4.35% = 4.27%, 1 to 5 4.51% = 4.42% ... over 25 4.89% = 4.78%; CPI-linked up to 5 3.50% = 3.45% ... over 25 3.53% = 3.47%; history since 2013 / 2011 included for the page chart V4.
- Market, 8.2026: 10,272 loans, 10.90 billion ₪, average 1,061,044 ₪, PTI average 29.23%, not-linked term 23.81 years; track, LTV and PTI shares exactly as dna.md section 6 (54.3 / 35.8 / 6.6 / 3.2 / 0.1; LTV 8.44 / 14.81 / 27.95 / 48.77; PTI 2.62 / 12.52 / 31.82 / 52.64 / 0.39); September first release 8.67 billion ₪.
- Policy rate 3.25% since 3.9.2026 (as of 25.10.2026), prime 4.75%. CPI 12 months to 9.2026: 1.64%; average monthly change of the last 12 indices 0.1368% (the Order's CPI fee).
- Carried from research (not machine readable): the October 2026 forecast (3.0% Q3 2027, inflation 2.0%, markets 3.1% / 1.8%), the next decision 23.11.2026, directive 329 and 451 rules, the Banking Order fees.

## How it was verified

1. Math, `test_mortgage_math.py`: 15 schedule cases + the payment-to-loan solver, Python port vs JS in node, every output equal to the shekel (first, highest and its month, total paid, interest, linkage, balance after 5 and 10 years, month 13, last payment, the balloon or bullet end payment, the new end month after a prepayment, the capitalization fee at unchanged and at 1 point lower averages). Cases: Spitzer, equal principal, balloon, bullet, partial and full grace, CPI-linked at 2%, prime +1.5% from month 13, the BoI forecast path, variable every 5 with +2% at the resets, the opening mix, the old +2% check, prepay shorten and reduce, equal principal linked with prepay. Hand values all hold: 1,000,000 ₪ 25y 4.62% Spitzer 5,627 ₪ and interest 687,997 ₪; equal principal 7,183 to 3,346 ₪, interest 579,425 ₪; T6 4.5% 5,558 ₪ and 5% 5,846 ₪; T5 baskets 20y 6,391 / 6,079 / 6,297, 25y 5,627 / 5,299 / 5,528, 30y 5,138 / 4,796 / 5,035. Result: ALL MATCH.
2. Browser (the app's built-in pane on the preview server; screenshots failed while the app window was minimized, so most checks read the DOM after pressing each control by script): every mode, every preset, every CPI and prime option, every buyer type, add / remove a track, track change (zakaut hint), all four methods, partial and full grace, 31 and 40 years, variable share 75%, prepay in a fixed, prime and variable track at months 60 and 61, shorten and reduce, offer inputs and "fill from the mix", compare (save + three baskets, remove), yearly and monthly schedule, share link reopened in a fresh load with identical numbers (payment mode 7,000 ₪ gives loan 1,221,800 ₪, highest 8,686 ₪, gap 55,997 ₪, the same after reload). No console errors.
3. Screenshots with headless Chrome (Playwright, scratch script outside the repo) at 375 px and 1440 px, the whole tool and each section after pressing controls; no horizontal overflow at 375 px (scrollWidth = 375).
4. Opening numbers: 1,200,000 ₪ in three tracks (600,000 קל״צ 4.62%, 400,000 prime 4.27%, 200,000 variable-5 CPI 3.19%, 25 years, CPI 2%): first payment 6,517 ₪, highest 7,136 ₪ in month 300, total paid 2,040,429 ₪, interest 772,977 ₪, linkage 67,452 ₪, 1.70 ₪ per shekel, PTI 29.6% on 22,000 ₪, LTV 60%, all rule checks pass.
5. Parity with the two old widgets (additive law): with the old rates (prime 4.75%, CPI 0) the 3-track mix gives 6,625 ₪ and the +2% check 8,051 ₪ (+1,427 ₪), exactly the old nlc-mortgage; 1,000,000 ₪ 4.62% 25y with income 22,000 ₪ gives 5,627 ₪, total 1,687,997 ₪, interest 687,997 ₪, ratio 25.6% with the old "מתון" text, stress +1% 6,213 ₪, exactly the old nmc. All old fields exist (amount, rate, years per track; loan, rate, years, net income, stress, fixed expenses) and the three status texts are word for word.
6. Language law scan of every visible string: no em or en dash, none of ממשק, מערכת, פלטפורמה, סימולציה, אינטראקטיבי, PMT, בקרוב, מנגנון, בבדיקה, מודל, Nadlan, נדלן חכם. Zero amounts read as words ("ללא הצמדה", "ללא פער", "נפרעה").

## What was not done, or done differently, and why

- **No edits to core.js / core.css** (the brief's constraint): the chart helper, the payment-to-loan solver and the schedule live in mortgage.js; its CSS is injected by the tool, scoped to `.nlm`.
- **Prime-track average** is not published as its own series. The rate opens at the BoI "up to 1 year" not-linked bucket (which includes loans whose rate changes at unknown dates, i.e. prime), 4.35% effective = 4.27% nominal, the same basis as T5; the hint shows "פריים פחות 0.48%".
- **Variable every 5, not linked** has no housing series in BIR_MRTG_99; it opens at the 1-to-5-year not-linked bucket, 4.51% = 4.42% nominal.
- **Eligibility loan**: amounts and rate for 2026 are unverified, so it opens at the fixed CPI-linked average with a line telling the visitor to type the rate from the certificate; the offer check shows "הריבית נקבעת בזכאות"; prepayment shows no fee (directed loan, Order s.2).
- **Scenarios**: the BoI and market rate paths move the prime track only (linear to the middle of Q3 2027, then flat); +2% and a custom shock move prime from their month and a variable-every-5 track at its next reset. There is no official forecast of the 5-year anchor.
- **The old "+2%" check** adds 2 points to every track, fixed included, exactly like the old widget; it is labelled "בכל המסלולים".
- **PTI** follows directive 329 (payment ÷ (net income − existing loans − fixed expenses)); the old widget used (payment + expenses) ÷ income. The three old status texts stay at 30% and 40%; the 50% cap and the 40% capital-weight line are added.
- **Prepayment fee**: the average rate on the future prepayment day is unknown, so the estimate takes today's average for the remaining period (or the period to the rate change) and also shows the fee if averages fall by 1 point. Under unchanged averages the Order's lower-of-two-formulas rule gives no capitalization fee, which the tool says plainly. The proportional method of the Order's annex (c) is used for partial prepayments; the complementary-loan reductions (10/20/30/40%) are not modelled; the notice fee and the CPI fee are shown as conditional lines.
- **Forecast, next decision date, directive and Order texts** are carried from the research, not fetched (the BoI site sits behind a bot wall for scripts; the SDMX and xls endpoints do not). Update `fixed_blocks()` after 23.11.2026. The directive and Order source links point to boi.org.il (the deep PDF URLs were not verified).
- **Grace length** has no verified limit; the tool accepts up to one month less than the track's term.
- **Not checked on the live theme**: the sticky dark result bar sits at `top:0`; if the site header is sticky, it may need an offset. The site-wide WhatsApp bar was not part of the preview.
- **Excel export** (one competitor has it) was not built; the spec asks for copy, WhatsApp, print and the reopen link, which exist.
