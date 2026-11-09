# -*- coding: utf-8 -*-
"""Round R (HAD-675, 9.11.2026): patch plugins/nadlan-config/inc/mortgage-market.php for 1.72.615.
  1. the million block (mm_million.php.txt): functions before "/** The section itself. */";
  2. the block printed after the by-bank note, its CSS after the section CSS (Hebrew section only);
  3. REST GET /nadlan/v1/mortgage-million: the CSV of every month and bank;
  4. JSON-LD on the Hebrew page: the market Dataset gains the CSV distribution; a second Dataset for the million series (#million);
     a WebApplication node for the page's calculators with featureList = the tools printed on the page.
Idempotent guard: refuses to run twice. python patch_mm.py [--dry]"""
import io, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
F = os.path.join(REPO, "plugins", "nadlan-config", "inc", "mortgage-market.php")
src0 = io.open(F, encoding="utf-8", newline="").read(); CRLF = chr(13) + chr(10) in src0
src = src0.replace(chr(13) + chr(10), chr(10))
assert "nadlan_mm_million_rows" not in src, "already patched"
add = io.open(os.path.join(H, "mm_million.php.txt"), encoding="utf-8", newline="").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


one("\t/** The section itself. */", add + "\n\t/** The section itself. */", "functions")
one("ההצעה שלכם נבדקת בכלי ההשוואה בראש הדף.</p>';\n",
    "ההצעה שלכם נבדקת בכלי ההשוואה בראש הדף.</p>';\n\t\t$h .= nadlan_mm_million_html( $d, $names );  // 1.72.615 (HAD-675): the month-by-month million series, cite box, CSV\n",
    "call (Hebrew render)")
one("\t\t$h .= nadlan_mm_css();\n\t\treturn $h . '</section>';",
    "\t\t$h .= nadlan_mm_css() . nadlan_mm_million_css();\n\t\treturn $h . '</section>';", "css (Hebrew render)")

REST = '''
/* 1.72.615 (HAD-675): the million series as CSV, every month and bank, for readers, journalists and the Dataset distribution. */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/mortgage-million', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function () {
			$csv = nadlan_mm_million_csv();
			if ( ! headers_sent() ) {
				header( 'Content-Type: text/csv; charset=utf-8' );
				header( 'Content-Disposition: inline; filename="nadlan-mortgage-1m-by-month.csv"' );
				header( 'Cache-Control: public, max-age=3600' );
			}
			echo $csv;  // phpcs:ignore WordPress.Security.EscapeOutput -- CSV body, every cell quoted or numeric
			exit;
		},
	) );
} );
'''
one("\n/* A Dataset JSON-LD for the tables, on a page that holds the shortcode. */", REST + "\n/* A Dataset JSON-LD for the tables, on a page that holds the shortcode. */", "rest")

# Hebrew Dataset: add the CSV distribution next to the JSON one (the English branch is untouched)
HE_DIST_OLD = "\t\t'distribution' => array( array( '@type' => 'DataDownload', 'encodingFormat' => 'application/json', 'contentUrl' => plugins_url( 'assets/instruments/data/boi-mortgage.json', dirname( __DIR__ ) . '/nadlan-config.php' ) ) ),\n\t);\n\techo \"\\n<script type=\\\"application/ld+json\\\" id=\\\"nadlan-mm-dataset\\\">\" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . \"</script>\\n\";\n}, 31 );"
assert src.count(HE_DIST_OLD) == 1, "hebrew dataset tail x%d" % src.count(HE_DIST_OLD)
HE_DIST_NEW = ("\t\t'distribution' => array( array( '@type' => 'DataDownload', 'encodingFormat' => 'application/json', 'contentUrl' => plugins_url( 'assets/instruments/data/boi-mortgage.json', dirname( __DIR__ ) . '/nadlan-config.php' ) ),\n"
               "\t\t\tarray( '@type' => 'DataDownload', 'encodingFormat' => 'text/csv', 'name' => 'ההחזר הראשון על מיליון ₪ לפי חודש ובנק', 'contentUrl' => rest_url( 'nadlan/v1/mortgage-million' ) ) ),\n"
               "\t);\n"
               "\techo \"\\n<script type=\\\"application/ld+json\\\" id=\\\"nadlan-mm-dataset\\\">\" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . \"</script>\\n\";\n"
               "\t// 1.72.615 (HAD-675): the million series as its own Dataset, and the page's calculators as one WebApplication\n"
               "\t$rows = nadlan_mm_million_rows( $d ); $pg = get_permalink( $p );\n"
               "\tif ( count( $rows ) > 2 ) {\n"
               "\t\t$mil = array(\n"
               "\t\t\t'@context' => 'https://schema.org', '@type' => 'Dataset', '@id' => $pg . '#million',\n"
               "\t\t\t'name' => 'כמה עולה משכנתא של מיליון שקל, חודש אחר חודש',\n"
               "\t\t\t'description' => 'ההחזר החודשי הראשון על משכנתא של 1,000,000 ₪ ל־25 שנה, בלוח שפיצר, בתמהיל ובריביות האפקטיביות הממוצעים של כל הבנקים ושל כל בנק בנפרד, לכל חודש מ' . nadlan_mm_month( $rows[0]['ym'] ) . ' עד ' . nadlan_mm_month( end( $rows )['ym'] ) . '. חישוב של נדל״ן מנתוני בנק ישראל, מתעדכן בכל חודש.',\n"
               "\t\t\t'url' => $pg . '#million', 'inLanguage' => 'he', 'isAccessibleForFree' => true,\n"
               "\t\t\t'temporalCoverage' => $rows[0]['ym'] . '/' . end( $rows )['ym'], 'spatialCoverage' => array( '@type' => 'Place', 'name' => 'Israel' ),\n"
               "\t\t\t'dateModified' => (string) ( $d['built'] ?? '' ),\n"
               "\t\t\t'variableMeasured' => array( 'החזר חודשי ראשון על מיליון ₪ ל־25 שנה, כל הבנקים', 'החזר חודשי ראשון לפי בנק', 'ריבית כוללת חזויה (IRR)' ),\n"
               "\t\t\t'isBasedOn' => 'https://www.boi.org.il/boi_files/Pikuah/TamInt010.xls',\n"
               "\t\t\t'creator' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ),\n"
               "\t\t\t'distribution' => array( array( '@type' => 'DataDownload', 'encodingFormat' => 'text/csv', 'contentUrl' => rest_url( 'nadlan/v1/mortgage-million' ) ) ),\n"
               "\t\t);\n"
               "\t\techo '<script type=\"application/ld+json\" id=\"nadlan-mm-million\">' . wp_json_encode( $mil, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . \"</script>\\n\";\n"
               "\t}\n"
               "\t$feat = array();\n"
               "\tif ( function_exists( 'nadlan_nli_page_ids' ) && function_exists( 'nadlan_nli_tools' ) && function_exists( 'nadlan_nli_t' ) ) {\n"
               "\t\t$tools = nadlan_nli_tools();\n"
               "\t\tforeach ( (array) nadlan_nli_page_ids() as $tid ) { if ( isset( $tools[ $tid ] ) ) { $t = nadlan_nli_t( $tools[ $tid ], 'he' ); if ( ! empty( $t['name'] ) ) { $feat[] = $t['name']; } } }\n"
               "\t}\n"
               "\tif ( count( $feat ) >= 3 ) {\n"
               "\t\t$app = array(\n"
               "\t\t\t'@context' => 'https://schema.org', '@type' => 'WebApplication', '@id' => $pg . '#calculators',\n"
               "\t\t\t'name' => 'מחשבון משכנתא', 'url' => $pg, 'inLanguage' => 'he', 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any',\n"
               "\t\t\t'browserRequirements' => 'Requires JavaScript', 'isAccessibleForFree' => true, 'offers' => array( '@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'ILS' ),\n"
               "\t\t\t'featureList' => array_values( array_unique( $feat ) ), 'dateModified' => (string) ( $d['built'] ?? '' ),\n"
               "\t\t\t'publisher' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ),\n"
               "\t\t);\n"
               "\t\techo '<script type=\"application/ld+json\" id=\"nadlan-mm-webapp\">' . wp_json_encode( $app, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . \"</script>\\n\";\n"
               "\t}\n"
               "}, 31 );")
src = src.replace(HE_DIST_OLD, HE_DIST_NEW)

vis = re.sub(r"<[^>]+>", " ", add)
assert not re.search("[–—]", src), "long dash"
assert "\r\n" not in src
print("mortgage-market.php patched: %d -> %d bytes" % (os.path.getsize(F), len(src.encode("utf-8"))))
if "--dry" not in sys.argv:
    io.open(F, "w", encoding="utf-8", newline="").write(src.replace(chr(10), chr(13) + chr(10)) if CRLF else src)
    print("written")
