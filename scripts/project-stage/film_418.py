# -*- coding: utf-8 -*-
"""Release 1.72.418 (design v104.41, the Kikar loop turn 26): captions on the narrated v2 film. Israeli Standard 5568 = WCAG 2.0
AA; 1.2.2 captions (prerecorded) is level A, and the film speaks. One <track kind="captions"> per video in the narration's language
(Hebrew on he, English on en/fr/ru/ar), off by default (the player's CC button); the house cue style.
The caption files are the media library's 8172 (he) and 8173 (en), byte-checked (docs/qa/film-v2r1/media-vtt.json). The uploads
folder serves .vtt as application/octet-stream, which a browser may refuse for a track, so the page points at a small public REST
route that serves the same file as text/vtt. Applied to the LIVE inc/project-stage.php text: the 1.72.417 function, exactly once."""
import io, json, os
import film_417

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
V = json.load(io.open(os.path.join(REPO, "docs", "qa", "film-v2r1", "media-vtt.json"), encoding="utf-8"))
IDS = {}
for lang in ("he", "en"):
    e = V[f"kikar-hamedina-film-v2-{lang}.vtt"]
    if e.get("byte_check") != "OK":
        raise SystemExit("film_418: the " + lang + " caption file was not byte-checked OK")
    IDS[lang] = int(e["id"])
RELS = ["inc/project-stage.php"]
FILES = {}
OLD = film_417.FUNC

NEW = OLD
for a, b in (
    ("\t\t$f = $s[ 'he' === $k ? 'he' : 'en' ];\n",
     "\t\t$cl = 'he' === $k ? 'he' : 'en';\n"
     "\t\t$f = $s[ $cl ];\n"
     "\t\t// v104.41: captions in the narration's language, off by default (the player's CC button)\n"
     "\t\t$cc = '<track kind=\"captions\" srclang=\"' . $cl . '\" label=\"' . ( 'he' === $cl ? 'עברית' : 'English' ) . '\" src=\"' . esc_url( rest_url( 'nadlan/v1/film-cc/' . $cl ) ) . '\">';\n"),
    ("use ( $f ) {", "use ( $f, $cc ) {"),
    ("'\" type=\"video/mp4\"></video>';", "'\" type=\"video/mp4\">' . $cc . '</video>';"),
    (".nlws-film__v1h{margin:8px 0;font-size:18px}</style>",
     ".nlws-film__v1h{margin:8px 0;font-size:18px}.nlws-film__v2 video::cue{font-family:Heebo,Arial,sans-serif;color:#FAF7F1;background:rgba(27,26,23,.82)}</style>"),
):
    if NEW.count(a) != 1:
        raise SystemExit("film_418: the 1.72.417 function has " + str(NEW.count(a)) + " of: " + a.strip()[:70])
    NEW = NEW.replace(a, b)

CC_FUNC = """
if ( ! function_exists( 'nadlan_ps_film_cc_route' ) ) {
	/** v104.41 (3.10.2026 night): the narrated film's captions as text/vtt. The uploads folder serves .vtt as
	 *  application/octet-stream, which a browser may refuse for a <track>; this route serves the same media file
	 *  (he @HE@, en @EN@) with the caption type. Public and read-only, like the file itself. */
	function nadlan_ps_film_cc_route() {
		register_rest_route( 'nadlan/v1', '/film-cc/(?P<lang>he|en)', array(
			'methods'             => 'GET',
			'permission_callback' => '__return_true',
			'callback'            => function ( $r ) {
				$id = array( 'he' => @HE@, 'en' => @EN@ )[ (string) $r['lang'] ] ?? 0;
				$p  = $id ? get_attached_file( $id ) : '';
				$t  = ( $p && is_readable( $p ) ) ? (string) file_get_contents( $p ) : '';
				if ( 0 !== strpos( $t, 'WEBVTT' ) ) {
					return new WP_Error( 'nadlan_film_cc', 'not found', array( 'status' => 404 ) );
				}
				header( 'Content-Type: text/vtt; charset=utf-8' );
				header( 'Cache-Control: public, max-age=86400' );
				echo $t; // a caption file from the media library, served as it is
				exit;
			},
		) );
	}
	add_action( 'rest_api_init', 'nadlan_ps_film_cc_route' );
}
""".replace("@HE@", str(IDS["he"])).replace("@EN@", str(IDS["en"]))


def apply(rel, txt):
    if "nadlan_ps_film_cc_route" in txt:
        raise SystemExit("film_418: already applied")
    if txt.count(OLD) != 1:
        raise SystemExit("film_418: the 1.72.417 function is there " + str(txt.count(OLD)) + " times")
    return txt.replace(OLD, NEW + CC_FUNC)
