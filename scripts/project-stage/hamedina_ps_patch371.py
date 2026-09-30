# -*- coding: utf-8 -*-
"""Kikar Hamedina P9a (1.72.371, HAD-375): the page top's fixes, as anchored hunks on inc/project-stage.php.

The LIVE file is what 1.72.370 wrote: 1.72.369's text + hamedina_ps_patch370.py's hunks (md5 ae0966a4..., deploy-result-370.json).
The release copy of 1.72.371 is that text + these hunks; the branch file (which also carries the unreleased Batch 1/2) gets the same
hunks, so the two never drift. Every anchor sits inside Kikar Hamedina's own text (its config, and the world page's own style block,
printed only on a world page), so the four stage projects (Rainbow, DUO, Dimri, Ashira) are not touched: ps_identity_proof371.py
renders them byte for byte, before and after.

  1. deg-facts : the Hebrew quick fact "1.25° בכל קומה" reads "1.25 מעלות בכל קומה" (the degree sign beside a Hebrew word read
                 "°1.25" on screen; a bidi isolate does not change that in Hebrew, measured; the Arabic page has said "درجة" since P8)
  2. deg-src   : the same in the Hebrew source line under the world
  3. lane      : PhoneFirstScreen (design system v104.1): on phones a landing lane between the page top's buttons and the world, so the
                 WhatsApp bar, which clears the world's tabs, parks between them and never on the third button
  4. cyrillic  : the Russian page's Cyrillic in the house type: Assistant, Noto Serif Hebrew, Heebo and Frank Ruhl Libre each gain the
                 Cyrillic of their own design family (Source Sans 3, Noto Serif, Roboto; Google Fonts, SIL OFL), only on the Russian
                 world page, only the Cyrillic range (unicode-range), font-display swap

  python scripts/project-stage/hamedina_ps_patch371.py --branch     apply the hunks to the working file (once)
  python scripts/project-stage/hamedina_ps_patch371.py              show which hunks the working file and the release carry
"""
import hashlib, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hamedina_ps_patch370 as P8  # noqa: E402  the 370 hunks (the live base of this release)

REPO = P8.REPO
REL = P8.REL
LIVE_370_MD5 = "ae0966a44f5a671cd91ae4bc9b8ef61d"  # deploy-result-370.json: what 1.72.370 wrote

# ------------------------------------------------------------------------------------------------ 1-2. degrees in Hebrew, as a word
DEG_FACTS_OLD = "array( 'הסיבוב', '1.25° בכל קומה', 'כ-50° לאורך מגדל של 40 קומות, לפי ויקיפדיה' ),"
DEG_FACTS_NEW = "array( 'הסיבוב', '1.25 מעלות בכל קומה', 'כ-50 מעלות לאורך מגדל של 40 קומות, לפי ויקיפדיה' ),"
DEG_SRC_OLD = "והסיבוב שפורסם, 1.25° בכל קומה. מיקום האגם"
DEG_SRC_NEW = "והסיבוב שפורסם, 1.25 מעלות בכל קומה. מיקום האגם"

# ------------------------------------------------------------------------------------------------ 3. the phone's first screen
LANE_OLD = """		. '@media(max-width:600px){:root body .nlps-page--world .nlps-stage--world{height:72svh;min-height:460px}}'"""
LANE_NEW = """		. '@media(max-width:600px){:root body .nlps-page--world .nlps-stage--world{height:72svh;min-height:460px}}'
		// PhoneFirstScreen (design system v104.1, P9a): on phones a landing lane (50px + the grid's gap) between the page top's
		// buttons and the world. The WhatsApp bar (50px, 10px clear on each side of it) parks there while the world's tab bar passes
		// its resting place, instead of rising onto the third button ("סיור וירטואלי בכיכר"); conversion-cta.php counts the page
		// top's buttons as controls and takes the free place nearest the bar's resting place
		. '@media(max-width:600px){:root body .nlps-page--world>.nlps-stagebox{margin-top:50px!important}}'"""

# ------------------------------------------------------------------------------------------------ 4. Cyrillic in the house type
CYR_OLD = """		. ':root body .nlws p{font-size:15.5px!important}}'
		. '</style>' . "\\n";
}, 1000 );"""
CYR_NEW = """		. ':root body .nlws p{font-size:15.5px!important}}'
		. '</style>' . "\\n";
	// P9a (1.72.371): the Russian page's Cyrillic in the house type. The site's faces have no Cyrillic, so Russian fell back to the
	// system's (Segoe UI, Georgia, Arial). Each family gains the Cyrillic of its own design family: Assistant's Latin is Source Sans,
	// Noto Serif Hebrew's is Noto Serif, Heebo's is Roboto; Frank Ruhl Libre takes Noto Serif too (Google Fonts, SIL Open Font
	// License). The same weights the site declares (a weight the site does not declare would take the Latin with it); only the
	// Cyrillic range is fetched, and only when Cyrillic is on screen (unicode-range); only on this page; font-display swap.
	if ( 'ru' === (string) ( $ps['lang'] ?? '' ) ) {
		$cyr = 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116';
		$gs  = 'https://fonts.gstatic.com/s/';
		$fam = array(
			'Assistant'         => array( $gs . 'sourcesans3/v19/nwpStKy2OAdR1K-IwhWudF-R3wsaZfrc.woff2', array( 300, 400, 600, 700 ) ),
			'Noto Serif Hebrew' => array( $gs . 'notoserif/v33/ga6daw1J5X9T9RW6j9bNVls-hfgvz8JcMofYTYf-D33Esw.woff2', array( 500, 600, 700 ) ),
			'Heebo'             => array( $gs . 'roboto/v51/KFO7CnqEu92Fr1ME7kSn66aGLdTylUAMa3iUBGEe.woff2', array( 300, 400, 500, 700 ) ),
			'Frank Ruhl Libre'  => array( $gs . 'notoserif/v33/ga6daw1J5X9T9RW6j9bNVls-hfgvz8JcMofYTYf-D33Esw.woff2', array( 400, 500, 700, 900 ) ),
		);
		$css = '';
		foreach ( $fam as $name => $f ) {
			foreach ( $f[1] as $wt ) {
				$css .= "@font-face{font-family:'" . $name . "';font-style:normal;font-weight:" . (int) $wt . ';font-display:swap;src:url(' . $f[0] . ") format('woff2');unicode-range:" . $cyr . '}';
			}
		}
		echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\\n" . '<style id="nadlan-ps-world-cyr">' . $css . '</style>' . "\\n";
	}
}, 1000 );"""

HUNKS = [
    ("deg-facts", DEG_FACTS_OLD, DEG_FACTS_NEW),
    ("deg-src", DEG_SRC_OLD, DEG_SRC_NEW),
    ("lane", LANE_OLD, LANE_NEW),
    ("cyrillic", CYR_OLD, CYR_NEW),
]


def apply(text, label=""):
    for name, old, new in HUNKS:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"FATAL P9a hunk {name}: anchor x{n} in {label}")
        text = text.replace(old, new)
    return text


def carries(text):
    return {name: (new in text) for name, old, new in HUNKS}


def live370():
    """the text 1.72.370 wrote (369's text + the P8 hunks), checked against its recorded md5"""
    t = P8.release_text()
    m = hashlib.md5(t.encode("utf-8")).hexdigest()
    if m != LIVE_370_MD5:
        raise SystemExit(f"FATAL: 369 + the P8 hunks is {m}, not what 1.72.370 wrote ({LIVE_370_MD5})")
    return t


def release_text():
    return apply(live370(), "the 370 release copy")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    path = os.path.join(REPO, *REL.split("/"))
    cur = io.open(path, encoding="utf-8", newline="").read()
    if "--branch" in sys.argv:
        if all(carries(cur).values()):
            print("the working file already carries every P9a hunk")
        else:
            io.open(path, "w", encoding="utf-8", newline="").write(apply(cur, "the working file"))
            print("applied", [h[0] for h in HUNKS], "to", REL)
    else:
        print("working file:", carries(cur))
        r = release_text()
        print("release copy (370 + P9a):", hashlib.md5(r.encode("utf-8")).hexdigest(), carries(r))
