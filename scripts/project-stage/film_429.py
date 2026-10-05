# -*- coding: utf-8 -*-
"""Release 1.72.429 (ProjectFilm v80; HAD-419 DUO, HAD-400 Rainbow, HAD-420 Dimri Yama; Ben 5.10.2026: "everything is approved,
upload and then send links"). The three project films go live on their pages:
- Hebrew film on the Hebrew page, the English film on -en/-fr/-ru/-ar (before v80 the film was Hebrew-only and unset there);
- Rainbow's v79 film (49 s, media 8106-8109) is replaced by the v1 film; DUO and Dimri get their first film;
- the hero button, the dialog's direction, close label and bar, and the VideoObject follow the page's language
  (nadlan_ps_film_t); fr/ru/ar say the film is in English; the bar names the project in its English form there.
The URLs are the exact uploaded ones (docs/qa/film-v1-projects/media.json, every file byte-checked).
The film audit (5.10): no draft label in any frame; badge "הדמיה להמחשה" on every frame; the map-data credit on the end card;
no developer name and no price.
Applied to the LIVE inc/project-stage.php text (what 1.72.428 wrote); every anchor exactly once."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(io.open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "qa", "film-v1-projects", "media.json"), encoding="utf-8"))
for n, v in M.items():
    if v.get("byte_check") != "OK":
        raise SystemExit("film_429: " + n + " was not byte-checked OK")
U = {n: v["url"].replace("'", "") for n, v in M.items()}
RELS = ["inc/project-stage.php"]
FILES = {}

FILMS = {
    "duo-tel-aviv": dict(secs=54, name_en="DUO Tel Aviv",
        he="סרטון של 54 שניות על DUO תל אביב במתחם סומייל: המיקום, שני המגדלים, הדירות, המסחר, שלב הבנייה לפי דוח החברה והנוף המשוער מהקומות. הדמיה להמחשה.",
        en="A 54-second film on DUO Tel Aviv in the Somail compound: the location, the two towers, the apartments, the retail, the construction stage per the company report and the estimated view from the floors. Illustrative visualisation."),
    "rainbow-tel-aviv": dict(secs=54, name_en="Rainbow Tel Aviv",
        he="סרטון של 54 שניות על Rainbow תל אביב ברובע שדה דב: המיקום, המגדל ובנייני הבוטיק, הדירות, מועדון הדיירים, שלב הבנייה והנוף המשוער מהקומות. הדמיה להמחשה.",
        en="A 54-second film on Rainbow Tel Aviv in the Sde Dov quarter: the location, the tower and the boutique buildings, the apartments, the residents' club, the construction stage and the estimated view from the floors. Illustrative visualisation."),
    "dimri-yama-sde-dov": dict(secs=47, name_en="Dimri Yama Sde Dov",
        he="סרטון של 47 שניות על דמרי ימה שדה דב במתחם אשכול: המיקום, המגדל, הדירות וחדרי המלון לפי היזם, שלב השיווק והנוף המשוער מהקומות. הדמיה להמחשה.",
        en="A 47-second film on Dimri Yama Sde Dov in the Eshkol compound: the location, the tower, the apartments and hotel rooms per the developer, the marketing stage and the estimated view from the floors. Illustrative visualisation."),
}


def film_php(slug):
    f = FILMS[slug]
    def one(lang, desc, extra=""):
        u = lambda fmt, x: U[f"{slug}-film-v1-{lang}-{fmt}{x}"]
        return ("array(\n"
                f"\t\t\t\t\t'wide' => '{u('16x9', '.mp4')}', 'tall' => '{u('9x16', '.mp4')}',\n"
                f"\t\t\t\t\t'poster_wide' => '{u('16x9', '-poster.jpg')}', 'poster_tall' => '{u('9x16', '-poster.jpg')}',\n"
                f"\t\t\t\t\t'secs' => {f['secs']}, 'date' => '2026-10-05', 'date_he' => '5.10.2026', 'lang' => '{lang}',{extra}\n"
                "\t\t\t\t\t'desc' => '" + desc.replace("\\", "\\\\").replace("'", "\\'") + "',\n"
                "\t\t\t\t),\n")
    return ("\t\t\t\t// ProjectFilm v80 (5.10.2026, Ben: \"everything is approved\"): the film loop's v1 film, Hebrew here and English on the\n"
            "\t\t\t\t// language pages (film_en); 720p web copies, byte-checked (docs/qa/film-v1-projects/media.json)\n"
            "\t\t\t\t'film'           => " + one("he", f["he"]) +
            "\t\t\t\t'film_en'        => " + one("en", f["en"], f" 'name' => '{f['name_en']}',"))


EDITS = []
# A. Rainbow: the v79 film block is replaced
_RB_START = "\t\t\t\t// ProjectFilm v79 (28.9.2026): the project's film, 49 s, from scripts/project-video (every line's source in\n"
_RB_END = "\t\t\t\t// the floor card's line where no sold apartment is known: what the developer said about that height (Bizportal\n"
# B. DUO and Dimri: the film arrays open their project entry
EDITS += [("\t\t\t'duo-tel-aviv' => array(\n", "\t\t\t'duo-tel-aviv' => array(\n" + film_php("duo-tel-aviv")),
          ("\t\t\t'dimri-yama-sde-dov' => array(\n", "\t\t\t'dimri-yama-sde-dov' => array(\n" + film_php("dimri-yama-sde-dov"))]
# C. the language pages keep the English film
EDITS += [("\t\t\tunset( $memo['film'], $memo['deals'], $memo['deals_sum'], $memo['basket_hint'] );\n",
           "\t\t\t$fe = $memo['film_en'] ?? null; // ProjectFilm v80: a project with an English film shows it on its language pages\n"
           "\t\t\tunset( $memo['film'], $memo['deals'], $memo['deals_sum'], $memo['basket_hint'] );\n"
           "\t\t\tif ( ! empty( $fe['wide'] ) ) { $memo['film'] = $fe; }\n")]
# D. the hero button in the page's language
EDITS += [("<span>סרטון הפרויקט <small>· ' . (int) $ps['film']['secs'] . ' שניות</small></span></a>'",
           "<span>' . esc_html( nadlan_ps_film_t( $ps )['btn'] ) . ' <small>· ' . (int) $ps['film']['secs'] . ' ' . esc_html( nadlan_ps_film_t( $ps )['secs'] ) . '</small></span></a>'")]
# E. the VideoObject follows the film shown
EDITS += [("\t\t'name' => $ps['name'] . ': סרטון הפרויקט', 'description' => (string) $f['desc'],\n",
           "\t\t'name' => (string) ( 'he' === nadlan_ps_film_t( $ps )['lang'] ? $ps['name'] : ( $f['name'] ?? $ps['name'] ) ) . ': ' . nadlan_ps_film_t( $ps )['btn'], 'description' => (string) $f['desc'],\n"),
          ("'contentUrl' => $f['wide'], 'inLanguage' => 'he',", "'contentUrl' => $f['wide'], 'inLanguage' => (string) ( $f['lang'] ?? 'he' ),")]
# F. the dialog in the page's language
_DLG_OLD = ("\techo '<dialog id=\"nlfilm\" class=\"nlfilm\" dir=\"rtl\" lang=\"he\" aria-label=\"' . esc_attr( 'סרטון הפרויקט: ' . $ps['name'] ) . '\"'\n")
_DLG_NEW = ("\t$ft = nadlan_ps_film_t( $ps ); // ProjectFilm v80: the player in the page's language\n"
            "\t$fn = 'he' === $ft['lang'] ? $ps['name'] : (string) ( $f['name'] ?? $ps['name'] );\n"
            "\techo '<dialog id=\"nlfilm\" class=\"nlfilm\" dir=\"' . esc_attr( $ft['dir'] ) . '\" lang=\"' . esc_attr( $ft['lang'] ) . '\" aria-label=\"' . esc_attr( $ft['btn'] . ': ' . $fn ) . '\"'\n")
EDITS += [(_DLG_OLD, _DLG_NEW),
          ("'<button type=\"button\" class=\"nlfilm-x\" aria-label=\"סגירה\">&#10005;</button>",
           "'<button type=\"button\" class=\"nlfilm-x\" aria-label=\"' . esc_attr( $ft['close'] ) . '\">&#10005;</button>"),
          ("'<div class=\"nlfilm-bar\"><span><b>' . esc_html( $ps['name'] ) . '</b> · סרטון הפרויקט · ' . (int) $f['secs'] . ' שניות · עודכן ' . esc_html( $f['date_he'] ) . '</span><span>הדמיה להמחשה. כל נתון עם המקור שלו.</span></div>'",
           "'<div class=\"nlfilm-bar\"><span><b>' . esc_html( $fn ) . '</b> · ' . esc_html( $ft['btn'] ) . ' · ' . (int) $f['secs'] . ' ' . esc_html( $ft['secs'] ) . ' · ' . esc_html( $ft['upd'] ) . ' ' . esc_html( $f['date_he'] ) . '</span><span>' . esc_html( $ft['note'] ) . '</span></div>'")]
# G. the strings, before the ProjectFilm hooks
_HOOKS = "/* ProjectFilm v79 (design system, 28.9.2026): the project's film in a dialog, and a VideoObject for search. The button is in\n"
_HELPER = """if ( ! function_exists( 'nadlan_ps_film_t' ) ) {
	/** ProjectFilm v80 (5.10.2026): the film's button and player strings in the page's language (he, en, fr, ru, ar); the language
	 *  pages show the English film, and fr/ru/ar say so. */
	function nadlan_ps_film_t( $ps ) {
		$l = (string) ( $ps['lang'] ?? 'he' );
		$T = array(
			'he' => array( 'btn' => 'סרטון הפרויקט', 'secs' => 'שניות', 'upd' => 'עודכן', 'note' => 'הדמיה להמחשה. כל נתון עם המקור שלו.', 'close' => 'סגירה', 'dir' => 'rtl' ),
			'en' => array( 'btn' => 'Project film', 'secs' => 'seconds', 'upd' => 'updated', 'note' => 'Illustrative visualisation. Every figure has its source.', 'close' => 'Close', 'dir' => 'ltr' ),
			'fr' => array( 'btn' => 'Film du projet', 'secs' => 'secondes', 'upd' => 'mis à jour le', 'note' => 'Visualisation illustrative. Film en anglais.', 'close' => 'Fermer', 'dir' => 'ltr' ),
			'ru' => array( 'btn' => 'Фильм о проекте', 'secs' => 'сек.', 'upd' => 'обновлено', 'note' => 'Иллюстративная визуализация. Фильм на английском языке.', 'close' => 'Закрыть', 'dir' => 'ltr' ),
			'ar' => array( 'btn' => 'فيلم المشروع', 'secs' => 'ثانية', 'upd' => 'آخر تحديث', 'note' => 'تصور توضيحي. الفيلم باللغة الإنجليزية.', 'close' => 'إغلاق', 'dir' => 'rtl' ),
		);
		if ( ! isset( $T[ $l ] ) ) { $l = 'he'; }
		return $T[ $l ] + array( 'lang' => $l );
	}
}

"""
EDITS += [(_HOOKS, _HELPER + _HOOKS)]


def apply(rel, txt):
    if "nadlan_ps_film_t" in txt:
        raise SystemExit("film_429: already applied")
    a, b = txt.find(_RB_START), txt.find(_RB_END)
    if txt.count(_RB_START) != 1 or txt.count(_RB_END) != 1 or not (0 < a < b) or b - a > 2500:
        raise SystemExit("film_429: the Rainbow v79 film block was not found once")
    txt = txt[:a] + film_php("rainbow-tel-aviv") + txt[b:]
    for old, new in EDITS:
        if txt.count(old) != 1:
            raise SystemExit("film_429: anchor x%d: %r" % (txt.count(old), old[:90]))
        txt = txt.replace(old, new)
    return txt
