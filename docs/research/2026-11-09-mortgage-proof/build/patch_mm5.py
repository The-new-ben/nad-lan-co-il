# -*- coding: utf-8 -*-
"""Round R part 5: the digits and the shekel line of the lead ("1,000,000 ₪") use Assistant's LATIN file, a separate download that
also arrived late (the last 0.07 of CLS in the probe). Preload three files: Noto Serif Hebrew (hebrew), Assistant (hebrew), Assistant (latin)."""
import io, os
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
F = os.path.join(REPO, "plugins", "nadlan-config", "inc", "mortgage-market.php")
b = io.open(F, encoding="utf-8", newline="").read()
s = b.replace(chr(13) + chr(10), chr(10))
i = s.index("\tfunction nadlan_mm_font_preload() {"); j = s.index("\n\t}\n", i) + len("\n\t}\n")
NEW = r'''	function nadlan_mm_font_preload() {
		$urls = get_transient( 'nadlan_mm_font_preload_v3' );
		if ( is_array( $urls ) && 3 === count( $urls ) ) { return $urls; }
		$urls = array(  // read from Google with a phone browser on 9.11.2026
			'https://fonts.gstatic.com/s/notoserifhebrew/v30/k3k5o9MMPvpLmixYH7euCwmkS9DohjX1-kRyiqyBqIxnoLbD-VBM2jVkL3Lr.woff2',
			'https://fonts.gstatic.com/s/assistant/v24/2sDcZGJYnIjSi6H75xkzamW5Kb8VZBHR.woff2',
			'https://fonts.gstatic.com/s/assistant/v24/2sDcZGJYnIjSi6H75xkzaGW5Kb8VZA.woff2',
		);
		$ttl = DAY_IN_SECONDS;
		$res = wp_remote_get( 'https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&family=Assistant:wght@300;400;600;700&display=swap',
			array( 'timeout' => 3, 'user-agent' => 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36' ) );  // phones and Mac get these files; Windows gets hinted ones
		if ( ! is_wp_error( $res ) && 200 === (int) wp_remote_retrieve_response_code( $res ) ) {
			$css = (string) wp_remote_retrieve_body( $res ); $found = array();
			foreach ( array( array( 'hebrew', 'Noto Serif Hebrew' ), array( 'hebrew', 'Assistant' ), array( 'latin', 'Assistant' ) ) as $sf ) {
				if ( preg_match( "#/\\* " . $sf[0] . " \\*/\\s*@font-face\\s*\\{[^}]*font-family:\\s*'" . preg_quote( $sf[1], '#' ) . "'[^}]*src:\\s*url\\((https://fonts\\.gstatic\\.com/[^)]+\\.woff2)\\)#", $css, $m ) ) { $found[] = $m[1]; }
			}
			if ( 3 === count( $found ) ) { $urls = $found; $ttl = WEEK_IN_SECONDS; }
		}
		set_transient( 'nadlan_mm_font_preload_v3', $urls, $ttl );
		return $urls;
	}
'''
s = s[:i] + NEW + s[j:]
assert s.count("nadlan_mm_font_preload_v3") == 2 and "nadlan_mm_font_preload_v2" not in s
io.open(F, "w", encoding="utf-8", newline="").write(s.replace(chr(10), chr(13) + chr(10)))
print("ok")
