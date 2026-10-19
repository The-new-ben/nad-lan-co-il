# -*- coding: utf-8 -*-
"""Release 1.72.470 (HAD-543, Ben 19.10.2026: "redo the film with a voice, in English... and in the same window switch to a
film on the video call: a gallery of explainer films, without pushing the showroom down"): the how-to card (same place, same
size) becomes a small gallery of two English narrated films, the showroom and the shared video call, switched by two tabs
in the card. Hunks on the LIVE inc/project-stage.php (the 1.72.467 card), each anchor once."""
RELS = ["inc/project-stage.php"]
A_CFG = "\t\t\t\t'howto'          => array( 'src' => 'howto-he.mp4', 'poster' => 'howto-he.jpg', 'title' => 'איך משתמשים באולם התצוגה', 'sub' => 'סרטון קצר: קומה וכיוון, נוף ומפה, כניסה לדירה, המתקנים ושיחת וידאו עם נציג.' ),\n"
CFG = ("\t\t\t\t'howto'          => array( 'src' => 'film-showroom-en.mp4', 'poster' => 'film-showroom-en.jpg', 'title' => 'סרטוני הסבר', 'sub' => 'באנגלית, עם כתוביות. הדמיות להמחשה בלבד.',\n"
       "\t\t\t\t\t'films' => array(\n"
       "\t\t\t\t\t\tarray( 'src' => 'film-showroom-en.mp4', 'poster' => 'film-showroom-en.jpg', 'tab' => 'איך משתמשים באולם התצוגה' ),\n"
       "\t\t\t\t\t\tarray( 'src' => 'film-call-en.mp4', 'poster' => 'film-call-en.jpg', 'tab' => 'שיחת וידאו עם נציג' ),\n"
       "\t\t\t\t\t),\n"
       "\t\t\t\t),\n")
A_FIG = "\t\t\t$nlps_howto = '<figure class=\"nlps-howto\"><figcaption class=\"nlps-howto__k\">' . esc_html( (string) $ps['howto']['title'] ) . '</figcaption>'\n"
FIG = (A_FIG +
       "\t\t\t\t// HowToGallery (1.72.470): the films as tabs; a tap swaps the video in place (no reflow, nothing loads before the tap)\n"
       "\t\t\t\t. ( count( (array) ( $ps['howto']['films'] ?? array() ) ) > 1 ? '<div class=\"nlps-howto__tabs\" role=\"tablist\">' . implode( '', array_map( function ( $f, $i ) use ( $hu, $hv ) {\n"
       "\t\t\t\t\treturn '<button type=\"button\" role=\"tab\" class=\"nlps-howto__tab\" aria-selected=\"' . ( 0 === $i ? 'true' : 'false' ) . '\" data-src=\"' . esc_url( $hu . $f['src'] . $hv ) . '\" data-poster=\"' . esc_url( $hu . $f['poster'] . $hv ) . '\" onclick=\"var g=this.closest(\\'.nlps-howto\\'),v=g.querySelector(\\'video\\');g.querySelectorAll(\\'.nlps-howto__tab\\').forEach(function(b){b.setAttribute(\\'aria-selected\\',b===this?\\'true\\':\\'false\\')},this);v.pause();v.poster=this.dataset.poster;v.querySelector(\\'source\\').src=this.dataset.src;v.load();v.play().catch(function(){});\">' . esc_html( (string) $f['tab'] ) . '</button>';\n"
       "\t\t\t\t}, array_values( (array) $ps['howto']['films'] ), array_keys( array_values( (array) $ps['howto']['films'] ) ) ) ) . '</div>' : '' )\n")
A_CSS = "\t\t. ':root body .nlps-howtom{display:none}'\n"
CSS = (A_CSS +
       "\t\t. ':root body .nlps-howto__tabs{display:flex;gap:6px;margin:0 0 8px;flex-wrap:wrap}'\n"
       "\t\t. ':root body .nlps-howto__tab{flex:1 1 0;min-height:40px;padding:6px 8px;border:1px solid #C9D5DC;border-radius:8px;background:#F5F7F8;color:#0F2233;font:600 13px/1.2 inherit;cursor:pointer}'\n"
       "\t\t. ':root body .nlps-howto__tab[aria-selected=\"true\"]{background:#0F2233;border-color:#0F2233;color:#fff}'\n")


def apply(rel, txt):
    if rel != "inc/project-stage.php":
        return txt
    for a in (A_CFG, A_FIG, A_CSS):
        if txt.count(a) != 1:
            raise SystemExit(f"ashira_470: anchor x{txt.count(a)} in the live {rel}: {a.strip()[:60]}")
    return txt.replace(A_CFG, CFG, 1).replace(A_FIG, FIG, 1).replace(A_CSS, CSS, 1)
