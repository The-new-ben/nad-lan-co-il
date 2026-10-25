# nrm v2: Israel mortgage calculator for foreigners (local build, not released)

"Your Israeli borrowing limit by passport and paycheck" (dna.md 8.6 and 8.7). Built locally on 26.10.2026. Nothing was deployed;
`inc/*.php`, `core.js` and `core.css` are untouched. This file lists what a release needs.

## Files

| File | What changed |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/nrm.js` | v2. Same id `nrm`, the v1 fields keep their ids and meaning, the v1 default case gives the same loan, payment, tax, fees and cash to close. `NLNR.compute` keeps the v1 signature (`tools/instruments/test_tools.js` passes); the new logic is `NLNR.full`. English and Hebrew: the tool follows its own section's `lang`, so the English tool inside the English article on the Hebrew path stays English. |
| `plugins/nadlan-config/assets/instruments/data/nrm.json` | funder.co.il source replaced by the Bank of Israel (BIR_MRTG_99, August 2026, series listed); `ltv_by_status`; rates fixed not linked 4.62, fixed CPI 3.29, prime 4.75 (+ spread; replaces "variable, not linked (approx.) 4.42"), variable CPI 3.19; `fx_track` 4.86; `cpi_forecast` 2.0 (21.10.2026); `rate_by_term` (9/2026); `baskets` (Directive 451); `next_decision` 2026-11-23; `ltv_source` points to the Directive 329 PDF, `ltv_qa` names the Q&A (no public URL found, so no link). Appraiser 650 and the file fee rule are kept but marked unverified, and the tool labels them "typical, check your bank's tariff". `rates[0]` is still the fixed rate, which the `afford` tool reads. |
| `tools/instruments/test_nrm_math.py` | Independent Python port against the real `nrm.js` in node: 28 cases, the dna hand values, the warnings, the cash solver, and v1 (git HEAD) against v2. `python tools/instruments/test_nrm_math.py` exits 1 on any mismatch. |
| `docs/research/2026-10-26-upgrades/ds_tools.py` | New entry `NrmForeign` and `build_langs()` (several data files, one page per language). `python docs/research/2026-10-26-upgrades/ds_tools.py NrmForeign` |
| `preview/index.html`, `preview/he.html` | The real engine + tool + data, inline. English page (`<html lang="en">`) and Hebrew page (`<html lang="he">`), three cases each. |

## What the tool does

Inputs: status (not an Israeli citizen · Israeli citizen, no home in Israel · Israeli citizen who owns a home · Israeli citizen
selling the Israeli home · new oleh living in Israel · couple, one citizen and one not, with the share), where you live (for the
citizen statuses and the couple: this picks the purchase tax track), mode (what can I borrow / what can my cash buy), price or
cash, currency, net monthly income and fixed commitments in that currency, loan share (opens at the status cap), years, mix
(one track · thirds, basket 2 · half fixed half prime, basket 3 · foreign currency loan, offered only to a non-citizen), track,
prime spread and CPI assumption when the mix has them, and behind "Adjust": appraisal (% of price), rate, lawyer fee.

Outputs: the most you can borrow (or the most home your cash buys) and which limit binds, in one sentence; the status cap, the
income caps at 50% and at one third; your loan; first payment in ₪ and your currency; prime +1 point (only the prime part reprices;
for a foreign currency loan, its own rate +1); a year of CPI on the linked part; payment as a share of disposable income; the net
income the payment needs at 50% and one third; purchase tax on the right track with its end date (foreign resident and additional
home 10.2.2027, single home and oleh brackets 15.1.2028); fees; cash to close; total interest; the Bank of Israel rate of the day
with its 30-day low and high; the payment in your currency if the shekel moves 10% either way; warnings (variable above 66.66%
except a foreign currency loan to a non-citizen, term above 30, loan above the status cap, payment above 50% of income, above 40%,
appraisal below price, cash mode clipped to the cap); notes on the two rulebooks for the status; dated sources; the formula; a
drawing (borrow mode: the two-limit bars with a dashed mark at the lower limit; cash mode: the stacked bar of loan, cash toward the
price, purchase tax and fees). Palette dna 8.5: passport navy #1E2B47, visa violet #5B3FA0, security-print teal #0F7C7A, paper
#F6F8FA, slate #2B3440; figures in IBM Plex Mono. Drawing text 14 to 17 px in a 420 box (about 11 to 13 px on a 390 px phone).

Ready cases (also usable from a page: `[nadlan_tool id="nrm" preset="abroad"]`): `foreign`, `abroad`, `oleh`, `couple`, `cash`
(what $800,000 buys, thirds), `fx` (borrow in dollars). Presets keep the reader's own income, commitments and currency.

## Registry change in `plugins/nadlan-config/inc/instruments.php`

**Phase 1, with this release.** Keep `'only' => 'en'`: `/israel-mortgage-non-residents/` is still an English article on a Hebrew
path (dna finding 1; owner decision 8.10). Only the name and description change; data files and related links stay as they are.

```php
'nrm' => array(
	'only' => 'en', 'name' => 'Israel mortgage calculator for foreigners', 'cat' => 'FinanceApplication', 'kicker' => 'Calculator · Israeli mortgage',
	'desc' => 'Your Israeli borrowing limit by passport and paycheck: the Bank of Israel loan cap by citizenship (50% for a non-citizen, 75% for an Israeli citizen or registered oleh buying the only home in Israel, 70% for a replacement home), the payment tested against your income at 50% and at one third in your own currency, the purchase tax by residency (foreign resident, Israeli resident, oleh), the cash to close, and the payment in dollars, euros or pounds with a 10% move in the shekel, at the Bank of Israel rates of the day.',
	'data' => array( 'ptax.json', 'nrm.json', 'boi-fx.json' ),
	'related' => array( '/israel-purchase-tax-foreign-residents/' => 'Purchase tax for foreign residents', '/en/buy-property-in-israel/' => 'Buying a home in Israel from abroad', '/en/north-tel-aviv/' => 'North Tel Aviv', '/projects/hamedina-en/' => 'Kikar HaMedina towers' ),
),
```

**Phase 2, only after the root page is rewritten in Hebrew** (dna 8.1). Drop `'only'`, Hebrew at the top level, English in the
`'en'` block. `nadlan_nli_tool_lang()` then gives Hebrew on the Hebrew page and English on `/en/` pages, and the tool follows.
Until then, removing `'only'` would print the Hebrew tool inside today's English article.

```php
'nrm' => array(
	'name' => 'מחשבון משכנתא לתושבי חוץ, לישראלים בחו״ל ולעולים', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · משכנתא לתושבי חוץ',
	'desc' => 'כמה משכנתא תקבלו בישראל לפי האזרחות וההכנסה: תקרת המימון של בנק ישראל לפי אזרחות (50% למי שאינו אזרח ישראלי, 75% לאזרח או לעולה רשום שקונה את הדירה היחידה בישראל, 70% לדירה חלופית), ההחזר מול ההכנסה במטבע שלכם (50% ושליש), מס רכישה לפי תושבות, הכסף לסגירה וההחזר בדולר, באירו או בלירה כשהשקל זז ב־10%, לפי נתוני בנק ישראל.',
	'data' => array( 'ptax.json', 'nrm.json', 'boi-fx.json' ),
	'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/mortgage-calculator/mortgage-repayment-capacity/' => 'כמה משכנתא אפשר לקחת' ),
	'en' => array(
		'name' => 'Israel mortgage calculator for foreigners', 'kicker' => 'Calculator · Israeli mortgage',
		'desc' => '(the phase 1 English desc)',
		'related' => array( '/israel-purchase-tax-foreign-residents/' => 'Purchase tax for foreign residents', '/en/buy-property-in-israel/' => 'How to buy a home in Israel from abroad', '/en/projects/' => 'New projects in Israel', '/projects/hamedina-en/' => 'Kikar HaMedina towers' ),
	),
),
```

Note: the llms list (around line 649) prints the top-level `name` and `desc`; in phase 2 that becomes the Hebrew text, like the
other tools.

## Optional: the no-script summary

Replace the `'nrm'` branch of `nadlan_nli_summary_en()` (today: 50%, 8% / 10%, 4.62%, the rates). All figures come from the data
files. Linted with PHP 8.3 and run against the real data (scratchpad `nrm/summary_check.php`); output: "Bank of Israel Directive
329 sizes an Israeli mortgage by citizenship: up to 50% ... 75% ... 70% ... 50% ... August 2026: fixed not linked 4.62%, fixed
CPI-linked 3.29%, foreign currency loans 4.86%. Prime 4.75% (Bank of Israel rate 3.25% since 3 Sep 2026, next decision 23 Nov
2026). Purchase tax is set by residency: a foreign resident pays 8% up to ILS 6,055,070 and 10% above, until 10 Feb 2027. Bank of
Israel representative rates on 21 Oct 2026: ..."

```php
if ( 'nrm' === $id ) {
	$dir = dirname( __DIR__ ) . '/assets/instruments/data/';
	$rd  = function ( $f ) use ( $dir ) { $p = $dir . $f; $x = is_readable( $p ) ? json_decode( (string) file_get_contents( $p ), true ) : null; return is_array( $x ) ? $x : array(); };
	$n = $rd( 'nrm.json' ); $x = $rd( 'boi-fx.json' ); $t = $rd( 'ptax.json' );
	if ( empty( $n['ltv_by_status'] ) || empty( $t['tracks']['foreign'] ) ) { return ''; }
	$c = $n['ltv_by_status']; $r = array(); foreach ( (array) $n['rates'] as $k ) { $r[ $k['id'] ] = $k['rate']; }
	$pct = function ( $v ) { return rtrim( rtrim( number_format( (float) $v, 2 ), '0' ), '.' ) . '%'; };
	$day = function ( $iso ) { return gmdate( 'j M Y', strtotime( $iso . ' UTC' ) ); };
	$f   = $t['tracks']['foreign'];
	$fx  = ! empty( $x['fx']['USD'] ) ? ' Bank of Israel representative rates on ' . esc_html( $day( $x['fx']['USD']['date'] ) ) . ': 1 USD = ILS ' . esc_html( $x['fx']['USD']['rate'] ) . ', 1 EUR = ILS ' . esc_html( $x['fx']['EUR']['rate'] ) . ', 1 GBP = ILS ' . esc_html( $x['fx']['GBP']['rate'] ) . '.' : '';
	return '<p>Bank of Israel Directive 329 sizes an Israeli mortgage by citizenship: up to ' . $pct( 100 * $c['foreign'] ) . ' of the value for a buyer who is not an Israeli citizen (any home a non-citizen buys is an investment home), '
		. $pct( 100 * $c['cit_first'] ) . ' for an Israeli citizen or registered oleh buying the only home in Israel, ' . $pct( 100 * $c['cit_sell'] ) . ' for a replacement home and ' . $pct( 100 * $c['cit_own'] ) . ' for a citizen who already owns one. '
		. 'The payment may not pass 50% of disposable income, the variable part 66.66% of the loan, the term 30 years. Average rates on new mortgages, ' . esc_html( gmdate( 'F Y', strtotime( $n['rates_month'] . '-01 UTC' ) ) ) . ': fixed not linked ' . $pct( $r['fixed'] )
		. ', fixed CPI-linked ' . $pct( $r['linked'] ) . ', foreign currency loans ' . $pct( $n['fx_track']['rate'] ) . '. Prime ' . $pct( $n['prime'] ) . ' (Bank of Israel rate ' . $pct( $n['boi_rate'] ) . ' since ' . esc_html( $day( $n['boi_rate_from'] ) ) . ', next decision ' . esc_html( $day( $n['next_decision'] ) ) . '). '
		. 'Purchase tax is set by residency: a foreign resident pays ' . $pct( 100 * $f[0][1] ) . ' up to ILS ' . number_format( $f[0][0] ) . ' and ' . $pct( 100 * $f[1][1] ) . ' above, until ' . esc_html( $day( $t['valid']['foreign'] ) ) . '.' . $fx . '</p>';
}
```

Phase 2 also needs a Hebrew branch in `nadlan_nli_summary( $id, 'he' )`; the same data, Hebrew text, in
`summary_check.php` (`nrm_summary_he`).

## Before a release

1. Refresh `data/boi-fx.json` with `python tools/instruments/build_fx_data.py`: the file in the repo is dated 21.10.2026 (USD
   3.091), so the preview shows that day; the dna numbers ($3,616, $3,287 / $4,018) are at the 23.10.2026 rate (USD 3.112), which
   the math test uses as its fixture.
2. CAD, AUD and ZAR: not in `boi-fx.json` today, so the tool shows USD, EUR and GBP only. The tool already lists any of the six it
   finds in the file. To add them, change the builder's loop to `("USD", "EUR", "GBP", "CAD", "AUD", "ZAR")` (series
   `RER_CAD_ILS`, `RER_AUD_ILS`, `RER_ZAR_ILS`; not changed or run in this build). `projects-hub-lang.php` and the Greece tools read
   only USD, EUR and GBP from that file, so extra keys do not touch them.
3. Ship `tools/nrm.js` + `data/nrm.json` together (v2 reads `ltv_by_status`, `prime`, `baskets`, `fx_track`, `cpi_forecast`; v1
   reads only fields that are still there). The registry change is optional for phase 1 (the old name and desc still describe
   the tool, less fully).
4. Run `python tools/instruments/test_nrm_math.py` and `node tools/instruments/test_tools.js`; after the release, the public-source
   audit on the two pages that mount `nrm` today (`/israel-mortgage-non-residents/` and `/en/projects/`) and the spot-checks.

## Not verified (kept out or labelled)

- Appraiser ₪650 and the file fee rule 0.25% up to ₪360: no bank tariff read. Labelled "typical, check your bank's tariff".
- Mixed couple: the weighted cap is the Bank of Israel's rule for separate buyers; how the Tax Authority (and so the bank) treats a
  married couple with one foreign spouse is unverified, and the tool says to ask the bank in writing. For a couple living in
  Israel, the tool uses the single-home brackets and says they hold only if both count as Israeli residents for tax.
- Israeli citizen selling the home, living in Israel: single-home brackets on condition the old home is sold within the period the
  law allows; the tool says so and does not name the months.
- A non-citizen who is an Israeli resident (329 points to Land Taxation Law s.16A(a)(1a)): bank practice unverified, so the
  non-citizen status is taken as living abroad, 50%, foreign-resident tax.
- Prime spread: no official average; default 0, labelled. Which currencies a bank lends in: each bank's choice (said in the note).
- The intending-oleh 75% claim of brokers is not in the directive and is not used.
- `rate_by_term` is stored for the page tables (T4b) but the tool does not pick a rate by term.
