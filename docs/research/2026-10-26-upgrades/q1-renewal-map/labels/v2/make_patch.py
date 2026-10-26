"""Assemble urban-map-v2.patch.php.txt (26.10.2026) from src/style.css.txt and src/script.js.txt plus the small PHP hunks below.
Each OLD text is cut from the live text (scripts/project-stage/live-520/urban-map.php) so it matches byte for byte.

    python make_patch.py
"""
import hashlib
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..', '..'))
LIVE = os.path.join(REPO, 'scripts', 'project-stage', 'live-520', 'urban-map.php')
OUT = os.path.join(HERE, 'urban-map-v2.patch.php.txt')
src = open(LIVE, encoding='utf-8').read()


def cut(start, end_incl):
    i = src.find(start)
    j = src.find(end_incl, i) + len(end_incl)
    assert i > -1 and j > i, start
    return src[i:j]


hunks = []

# V1: one more centroid, so the three cities on the authority map that our import never had (עפולה, דימונה, ערד) get a point
old = "\t\t\t'תל מונד'      => array( 34.9170, 32.2500 ),\n"
assert src.count(old) == 1
hunks.append(('V1 · a centroid for ערד (the only city on the authority map without one)', old,
              old + "\t\t\t'ערד'          => array( 35.2126, 31.2589 ), // v2 labels (26.10.2026): on the authority map from its 20.10.2026 check, not in our import\n"))

# V2: what the map script needs from PHP, printed once into the script (no new request)
old = "/* city aggregates - one computation feeding BOTH"
assert src.count(old) == 1
boot_fn = r"""/* v2 labels (proposal 26.10.2026): the centroids and the official apartment price medians the site already shows
   (assets/instruments/data/value.json: Tax Authority closed deals by room count, from the public summary files of nadlan.gov.il),
   printed once into the map script so the tags can say a price range without a new request. Unknown = omitted: a city without a
   median gets no price. */
if ( ! function_exists( 'nadlan_ur_map_v2_boot' ) ) {
	function nadlan_ur_map_v2_boot() {
		static $out = null;
		if ( null !== $out ) { return $out; }
		$px   = array();
		$src  = array();
		$path = dirname( __DIR__ ) . '/assets/instruments/data/value.json';
		$v    = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
		if ( is_array( $v ) && ! empty( $v['cities'] ) && is_array( $v['cities'] ) ) {
			foreach ( $v['cities'] as $name => $c ) {
				$row = array();
				foreach ( array( 'r3', 'r4', 'r5' ) as $k ) {
					if ( ! empty( $c[ $k ] ) ) {
						$row[ $k ] = array( (int) $c[ $k ], (string) ( $c[ 'q' . substr( $k, 1 ) ] ?? ( $c['q'] ?? '' ) ) );
					}
				}
				if ( $row ) {
					$row['page'] = (string) ( $c['page'] ?? '' );
					$px[ (string) $name ] = $row;
				}
			}
			$src = array( 'source' => (string) ( $v['source'] ?? '' ), 'url' => (string) ( $v['url'] ?? '' ), 'file' => (string) ( $v['file'] ?? '' ) );
		}
		$cent = array();
		foreach ( nadlan_ur_city_centroids() as $k => $ll ) { $cent[ (string) $k ] = array( (float) $ll[0], (float) $ll[1] ); }
		$out = wp_json_encode( array(
			'px'     => (object) $px,
			'pxsrc'  => (object) $src,
			'cent'   => (object) $cent,
			'pulled' => function_exists( 'nadlan_ur_source_pulled' ) ? (string) nadlan_ur_source_pulled() : '13.7.2026',
		), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP );
		if ( ! is_string( $out ) || '' === $out ) { $out = '{}'; }
		return $out;
	}
}

"""
hunks.append(('V2 · the data the tags need, printed once (PHP function)', old, boot_fn + old))

# V3: the shortcode computes it
old = "\t$rest = esc_url( rest_url( 'nadlan/v1/renewal-map-data' ) );\n"
assert src.count(old) == 1
hunks.append(('V3 · the shortcode reads it (PHP)', old, old + "\t$v2   = nadlan_ur_map_v2_boot(); // v2 labels: centroids + price medians as JSON, printed into the map script\n"))

# V4: the note under the map says what the tags now show
old = cut('\t<p class="nlurm-note">', '</p>\n')
new = ('\t<p class="nlurm-note">התוויות במפה מראות לכל עיר את מתחמי ההתחדשות ושלביהם לפי מפת הרשות הממשלתית להתחדשות עירונית, ואת מחירי הדירות '
       'לפי עסקאות שדווחו לרשות המסים. בפרטי כל עיר כתובים המקור והתאריך של כל מספר. עמודי המתחמים באתר נבנו מהקובץ הרשמי (data.gov.il) כפי שנמשך ב-'
       "<?php echo esc_html( function_exists( 'nadlan_ur_source_pulled' ) ? nadlan_ur_source_pulled() : '13.7.2026' ); ?>"
       '. הקישו על עיר לפרטים ולרשימת המתחמים בה.</p>\n')
hunks.append(('V4 · the note under the map (markup)', old, new))

# V5, V6: the style and the script of the map block
old = cut('<style>\n#nlurm-map{', '</style>\n')
new = open(os.path.join(HERE, 'src', 'style.css.txt'), encoding='utf-8').read()
if not new.endswith('\n'):
    new += '\n'
hunks.append(('V5 · the map block style (CSS)', old, new))
old = cut('<script>\n(function(){\n\tvar host=document.getElementById("nlurm-map")', '</script>\n')
new = open(os.path.join(HERE, 'src', 'script.js.txt'), encoding='utf-8').read()
if not new.endswith('\n'):
    new += '\n'
hunks.append(('V6 · the map block script (JS)', old, new))

md5 = hashlib.md5(open(LIVE, 'rb').read()).hexdigest()
head = """urban-map.php · renewal map v2: tags that carry the facts, chips that re-label the map, a city panel · proposal of 26.10.2026 · NOT APPLIED
=====================================================================================================================================

Target: the LIVE text of inc/urban-map.php = scripts/project-stage/live-520/urban-map.php (md5 %s; the live page of
1.72.529 serves the same map block and note, checked by build.py). NOT the repo copy inc/urban-map.php, which carries an
unreleased batch. Each hunk: the OLD text must appear exactly once and is replaced by the NEW text; apply in order. build.py
applies them to a scratch copy (v2/out/), runs php -l, runs the new PHP function under php-cli, checks the live page against the
target, and the proof (proof2.py) runs exactly the patched block inside the live page.

What changes: the map block (style + script), the note under the map, one PHP function that prints the centroids and the
official price medians (value.json, already on the server) into the script, and one centroid (ערד). Not touched: routes, REST
answers, the SEO block, the data block, the schemas, the page text above and below, URLs, robots, indexing.

New requests on the page: the Mapbox RTL text plugin (Hebrew base-map labels). The tracker file is the one the page already loads
for "יומן המתחמים" (same URL). The renewal-lookup endpoint is no longer called by the map while the tracker file is on the page
(the list comes from the tracker file, every complex instead of the first 8); it stays the fallback, with an honest message at its
hourly limit (HAD-605).

""" % md5
body = ''.join('=== %s ===\n--- OLD\n%s\n--- NEW\n%s\n=== END\n\n' % (n, o.rstrip('\n'), w.rstrip('\n')) for n, o, w in hunks)
open(OUT, 'w', encoding='utf-8', newline='\n').write(head + body)
print('written', OUT, len(hunks), 'hunks', len((head + body).encode('utf-8')), 'bytes')
