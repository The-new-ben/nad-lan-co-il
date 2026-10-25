# U2 · "מפת התשואה והתזרים" (tool id `invest`): local build, 25.10.2026

Local only. Nothing was deployed, `inc/instruments.php` was not edited, no Linear or Notion item was created.
Spec: `../dna.md` sections 6, 8.4, 8.5, 8.5.1, 8.6.

## Files (all new)
| File | What it is |
|---|---|
| `tools/instruments/build_invest_data.py` | Builds `invest.json`. Default: from the research's raw files (`_private-research/2026-10-26-upgrades/raw/u2/data/nadlan-gov`, 148 files read 25.10.2026; BoI SDMX extract in `raw/u1/boi`; CBS series in `raw/u2/data`). `--fetch DIR` re-downloads everything (runs the research's `fetch_nadlan_gov.py`, retries timeouts, BoI SDMX `BIR_MRTG_99`, CBS API), `--out PATH` writes beside the published file. On every build it re-runs the research's `build_yield.py` and asserts the gross yields are identical. |
| `plugins/nadlan-config/assets/instruments/data/invest.json` | 32.6 KB. 72 cities + Israel; per city and 3 / 4 / 5 rooms: median rent and median deal price of the same quarter, quarter, `n8` (in how many of the last 8 quarters both medians were published), price and rent change on the year; CBS table 4.9 average rent with sampling error (16 cities + Israel, 3 and 4 rooms, January to March 2026); the government site's own yield figure; rules (LTV caps, BoI August 2026 rates 4.62 / 3.29 / 3.19, prime 4.75, purchase tax tracks with the 10.2.2027 end date, VAT, lawyer, rental-tax tracks 5,654 / 11,308 / 10% by 30.1 / marginal 31% or 10% at 60+); every source with URL and dates. |
| `plugins/nadlan-config/assets/instruments/tools/invest.js` | The tool. Engine `mount()` for the form, readout, breakdown bar, ledger lines, scenarios, full table, formula, sources and share bar; under the readout its own blocks: the budget list, the three rental-tax tracks, the ranked board (break-even share of every city against the loan cap and the national line) and the yield vs price scatter. Pure logic in `window.NLIV`. Tool CSS is injected once (`#nliv-css`), scoped under `.nli`. |
| `tools/instruments/test_invest_math.py` | Cross-check: Python from `invest.json` = dna.md section 6 / T2 = every row of the research tables = the JS in node. |
| `docs/research/2026-10-26-upgrades/u2-investment/preview/index.html` | Preview: the shortcode's exact markup, Hebrew fonts, `core.css`, `core.js`, `tools/invest.js`; a second instance opens on a city page case (Haifa, 3 rooms). URL: http://localhost:8131/docs/research/2026-10-26-upgrades/u2-investment/preview/index.html |

## Registry entry for `inc/instruments.php` (same shape as `'pval'`)
```php
'invest' => array(
	'name' => 'מפת התשואה והתזרים', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · נדל״ן להשקעה',
	'desc' => 'דירה להשקעה בכל עיר לפי החציונים הרשמיים של אתר הנדל״ן הממשלתי, לפי מספר החדרים: תשואה ברוטו, משכנתא של 50% בריבית הממוצעת של בנק ישראל, תזרים חודשי לפני ואחרי ההוצאות שלכם, הון עצמי עם מס רכישה של דירה נוספת, שלושת מסלולי המס על שכר הדירה, כמה מהמחיר שכר הדירה לבדו מחזיק, ובדיקה לפי הון עצמי: אילו ערים עובדות.',
	'data' => array( 'invest.json' ),
	'related' => array( '/investment-property-mortgage/' => 'משכנתא לדירה להשקעה', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/investment/real-estate-yield/' => 'איך מחשבים תשואה', '/apartment-prices/' => 'מחירי הדירות לפי עיר' ),
),
```
Mount: `[nadlan_tool id="invest"]` (opens on the national 4-room median). City pages: `[nadlan_tool id="invest" city="חיפה" rooms="4"]` (the city name exactly as in `invest.json`, e.g. `תל אביב-יפו`, `פתח תקווה`). Ready cases: `preset="nat4" | "m1" | "e200" | "e400" | "tlv3"`. A copied result carries a link (`#invest?…`) that reopens the same numbers.

Optional, for readers without scripts, search engines and AI answers: add this branch inside `nadlan_nli_summary()` (before the final `return ''`). Linted with PHP 8.3 and run against `invest.json` with WordPress stubs (scratch harness): it prints the national paragraph and a 65-row table sorted by break-even share.
```php
if ( 'invest' === $id ) {  // U2 /investment/: the yield and cash-flow map as text and a table
	$path = dirname( __DIR__ ) . '/assets/instruments/data/invest.json';
	$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
	if ( ! is_array( $x ) || empty( $x['rows'] ) ) { return ''; }
	$L = $x['rules']; $rate = (float) $L['rates'][0]['rate']; $r = $rate / 1200; $af = ( 1 - pow( 1 + $r, -300 ) ) / $r;
	$qm = array( '03' => 'ינואר עד מרץ', '06' => 'אפריל עד יוני', '09' => 'יולי עד ספטמבר', '12' => 'אוקטובר עד דצמבר' );
	$hm = array( 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר' );
	$ql = function ( $q ) use ( $qm ) { $p = explode( '-', $q ); return ( isset( $qm[ $p[1] ] ) ? $qm[ $p[1] ] : $p[1] ) . ' ' . $p[0]; };
	$list = array(); $g = array(); $pos = 0;
	foreach ( $x['rows'] as $c ) {
		if ( ! empty( $c['nat'] ) || empty( $c['r']['4'] ) || $x['cityQ'] !== $c['r']['4']['q'] ) { continue; }
		$p = $c['r']['4']; $pay = 0.5 * $p['price'] / $af; $g[] = $p['rent'] * 12 / $p['price']; if ( $p['rent'] > $pay ) { $pos++; }
		$list[] = array( $c['n'], $p['rent'], $p['price'], $p['rent'] * 12 / $p['price'], $pay, $p['rent'] * $af / $p['price'] );
	}
	$n = count( $list ); if ( ! $n ) { return ''; }
	usort( $list, function ( $a, $b ) { return $b[5] <=> $a[5]; } );
	sort( $g ); $med = $n % 2 ? $g[ intdiv( $n, 2 ) ] : ( $g[ $n / 2 - 1 ] + $g[ $n / 2 ] ) / 2;
	$nat = $x['rows'][0]['r']['4']; $pm = explode( '-', $L['ratesPeriod'] ); $ex = $L['ptax']['extra'];
	$rows = '';
	foreach ( $list as $c ) { $rows .= '<tr><td>' . esc_html( $c[0] ) . '</td><td>' . number_format( $c[1] ) . '</td><td>' . number_format( $c[2] ) . '</td><td>' . number_format( 100 * $c[3], 2 ) . '%</td><td>' . number_format( round( $c[4] ) ) . '</td><td>' . number_format( 100 * $c[5], 1 ) . '%</td></tr>'; }
	return '<p>תשואה ברוטו על דירת 4 חדרים לפי החציונים הרשמיים של אתר הנדל״ן הממשלתי, ' . esc_html( $ql( $x['cityQ'] ) ) . ' (החישוב שלנו): חציון של ' . number_format( 100 * $med, 1 ) . '% ב־' . $n . ' ערים. בחציון הארצי של '
		. esc_html( $ql( $nat['q'] ) ) . ': מחיר ' . number_format( $nat['price'] ) . ' ₪, שכר דירה ' . number_format( $nat['rent'] ) . ' ₪, תשואה ברוטו ' . number_format( 100 * $nat['rent'] * 12 / $nat['price'], 2 ) . '%. במשכנתא של 50% לדירה נוספת, 25 שנה בריבית '
		. number_format( $rate, 2 ) . '% (הממוצע של בנק ישראל ב' . esc_html( $hm[ (int) $pm[1] - 1 ] . ' ' . $pm[0] ) . '), כל 100,000 ₪ עולים ' . number_format( round( 100000 / $af ) ) . ' ₪ בחודש, ושכר הדירה מכסה את ההחזר ב־' . $pos . ' מתוך ' . $n
		. ' ערים. מס רכישה על דירה נוספת: ' . number_format( 100 * $ex[0][1] ) . '% עד ' . number_format( $ex[0][0] ) . ' ₪ ו־' . number_format( 100 * $ex[1][1] ) . '% מעל, עד ' . esc_html( date_i18n( 'j.n.Y', strtotime( $L['ptax']['until']['extra'] ) ) ) . '.</p>'
		. '<table><caption>כמה מהדירה שכר הדירה קונה: ' . $n . ' ערים, 4 חדרים, ' . esc_html( $ql( $x['cityQ'] ) ) . ', משכנתא 50% ל־25 שנה בריבית ' . number_format( $rate, 2 ) . '% (החישוב שלנו)</caption><thead><tr><th>עיר</th><th>שכר דירה חציוני (₪)</th><th>מחיר חציוני (₪)</th><th>תשואה ברוטו</th><th>החזר חודשי (₪)</th><th>כמה מהדירה שכר הדירה קונה</th></tr></thead><tbody>' . $rows . '</tbody></table>';
}
```

## Data files
- Runtime: only `invest.json` (the rules from `ptax.json`, `cost.json`, `boi-rate.json` are copied in at build time with their sources; `value.json` gives the city price-page links).
- Refresh: `python tools/instruments/build_invest_data.py --fetch <empty dir> --out <tmp>`; compare; then run without `--out`. Government files are quarterly (the files of 20.8.2026 carry city prices to January to March 2026); the next file should bring April to June 2026, and the build then pairs that quarter automatically (newest of the last four quarters with both medians).

## How it was verified (25.10.2026)
- **Official sources, fresh**: `--fetch` re-downloaded all 148 data.nadlan.gov.il files (a first run lost one file to a timeout, so the build now retries; the second full run read 148 of 148): byte-identical to the research's files (148 of 148, version 20-08-2026, Last-Modified 20.8.2026); BoI SDMX live: fixed not linked August 2026 = 4.62%, CPI-linked 3.29%, variable CPI-linked 1.64 + 1.55 = 3.19%, investment-home loans 694 / 0.89 bn; CBS API: rent index +3.2% (September 2026), dwelling prices down 1.8%, CPI +1.6%. The rebuilt rows and rules are identical to the published `invest.json`.
- **Research reproduced**: gross yields equal `build_yield.py` on all 181 same-quarter pairs. New finding: the government site's "תשואת שכירות חציונית שנתית" equals all-rooms annual median rent × 12 ÷ all-rooms annual median price in **70 of 70** cities that show it (dna.md had checked Tel Aviv only).
- **`test_invest_math.py`: PASS, 0 mismatches**. 4 rooms: national 2.85% / payment 5,708 / short 883 / 42.3% / equity 1,188,674 / purchase tax 162,304 = 34 months of rent; Tel Aviv 2.29% / 14,713 / short 4,713 / 34.0%; Jerusalem 3.00% / 44.4%; Haifa 3.31% / short 94 / 49.0%; Beer Sheva 3.59% / +215 / 53.2%; Ashkelon 3.76% / +445 / 55.6%; 563 ₪ per 100,000; annuity factor 177.73; 65 cities, median 3.0%, 2.16% Givatayim to 5.36% Nazareth, 54 between 2.3% and 3.6%, rent covers the payment in 13 of 65; 400,000 own money buys up to about 683,000; CBS yields national 3.15%, Tel Aviv 2.03%. Every row of `data/cashflow-by-city.csv` (126) and `data/breakeven-ltv-4rooms.csv` (66) is equal, and the JS (`window.NLIV` in node) equals Python on all six cities, the ranking (65 / 13) and the budget mode (682,700). Each expected figure is also matched as a literal string in dna.md.
- **In the browser** (built-in browser tab on localhost:8131; the pane was hidden, so screenshots and pointer clicks failed there and controls were driven with DOM events on the real handlers; images from Playwright + Chrome at 1440 and 375 px): every ready case, both modes, the quick / full toggle, 3 / 4 / 5 rooms, the CBS source switch (Tel Aviv 30.1%, 2.03%), the three buyer tracks (single home: 75% loan, purchase tax 1,752, equity 520,922), loan above the cap (warning), signing after 10.2.2027 (warning), the four rates (own 5.5% gives 6,229), costs + empty month + 10% track (short 1,835 before tax, 2,277 after; net 1.87%, return on equity −2.3%, rent needed 6,827, all checked by hand), partial exemption (3,000 other rent: 4,342 taxable), the marginal track (method only), an older-quarter city (Kfar Saba 4 rooms, labelled, out of the ranking), a missing room count (Nazareth 5: message), the scenarios (each pressed state), "כל 65 הערים" (65 rows, back to 20), a pick from the board (Ashkelon) and from the scatter (Haifa), the hover tooltip, a budget row opening its city (Dimona 3 rooms 71.2%), copy text and the reopen link (Beer Sheva 3 rooms, own rent 2,800: same numbers after reload), the city-page instance (Haifa 3 rooms 51.7%). No page overflow at 375 or 1440, no console errors, all assets 200.
- **Language and design**: blacklist grep (ממשק, מערכת, פלטפורמה, סימולציה, אינטראקטיבי, בקרוב, מודל, מנגנון, שכבה, em / en dash) = 0 in the tool and the preview; no "₪0" in the output. Palette: engine tokens for the shell; marks verdigris #00806A and signal red #B8322A (dataviz validator: all checks pass, deutan ΔE 9.2; the dna's #1F7A5A failed the chroma floor and was replaced), ink #12304F, cool paper #F6F8FA, IBM Plex Sans Hebrew / Mono. Small samples (n8 ≤ 4 of 8 quarters) are marked ◦, lighter, and named in the note.

## What I could not do / left for the coordinator
- `inc/instruments.php` was not touched (the registry entry and the summary branch above are ready to paste); not deployed; not checked on the live theme (the engine's scoping should hold, as for the other tools).
- CBS table 4.9 is a PDF that cbs.gov.il serves only to browsers; the build reuses the research's parse (`../data/cbs-rent-table-4-9-2026q2.json`) and cites the CBS site, not a deep URL. Kol Zchut also blocks scripts; its URL is cited as the research read it (eyes). The 2026 rental ceiling still rests on Kol Zchut plus the indexation freeze (primary Tax Authority 2026 table: pending, as in dna.md).
- No Claude Design board was made first (design-first law): the tool follows the existing NadLan Instruments design system and the dna 8.5 ledger palette; a design review is still owed.
- Not in this scope: the page sections (T1 to T9, the facts strip, FAQ, schema), the 20 city pages mounting the tool, the neighbourhood level (phase 2), the `/investment-property-cashflow-calculator/` rebuild.
- On phones the readout sits below the form (about 1,400 px down), the same order as every engine tool; the ready cases above the form give a one-tap answer.
