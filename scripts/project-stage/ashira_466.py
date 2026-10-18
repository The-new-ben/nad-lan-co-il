# -*- coding: utf-8 -*-
"""Release 1.72.466 (HAD-543, Ben 19.10.2026: "embed the video high on the page, under the broker's spot on the side"):
Ashira's how-to film of the showroom (recorded on the live page, real clicks) goes into the side rail right under the broker
slot. (1) Ashira's config gets a 'howto' block; (2) the classic rail adds the film card when the file is on the site;
(3) the page's inline sheet styles the card (the full rail width on narrow screens). Hunks on the LIVE text, each anchor once."""
RELS = ["inc/project-stage.php"]
A_CFG = "\t\t\t\t'poster_alt'     => 'הדמיה של פרויקט אשירה"
CFG = ("\t\t\t\t// ShowroomHowTo (1.72.466): the showroom's how-to film under the broker slot (docs/sales/ashira-meeting-2026-10/film)\n"
       "\t\t\t\t'howto'          => array( 'src' => 'howto-he.mp4', 'poster' => 'howto-he.jpg', 'title' => 'איך משתמשים באולם התצוגה', 'sub' => 'סרטון קצר: קומה וכיוון, נוף ומפה, כניסה לדירה, המתקנים ושיחת וידאו עם נציג.' ),\n")
A_RAIL = "\t\tif ( 'he' === ( $ps['lang'] ?? 'he' ) ) { $rail .= nadlan_ps_slot(); }\n"
RAIL = (
    "\t\t// ShowroomHowTo (1.72.466, Ben 19.10.2026): the film of the showroom's controls, under the broker slot on the side\n"
    "\t\tif ( ! empty( $ps['howto']['src'] ) && is_readable( dirname( __DIR__ ) . '/assets/project-stage/' . $ps['dir'] . '/' . $ps['howto']['src'] ) ) {\n"
    "\t\t\t$hu = plugins_url( 'assets/project-stage/' . $ps['dir'] . '/', dirname( __FILE__ ) );\n"
    "\t\t\t$hv = '?ver=' . nadlan_ps_ver();\n"
    "\t\t\t$rail .= '<div class=\"nlds nlps-howtowrap\"><figure class=\"nlps-howto\"><figcaption class=\"nlps-howto__k\">' . esc_html( (string) $ps['howto']['title'] ) . '</figcaption>'\n"
    "\t\t\t\t. '<video class=\"nlps-howto__v\" controls playsinline preload=\"none\" width=\"1280\" height=\"720\" poster=\"' . esc_url( $hu . $ps['howto']['poster'] . $hv ) . '\" data-nlps-ev=\"howto\"><source src=\"' . esc_url( $hu . $ps['howto']['src'] . $hv ) . '\" type=\"video/mp4\"></video>'\n"
    "\t\t\t\t. '<p class=\"nlps-howto__s\">' . esc_html( (string) $ps['howto']['sub'] ) . '</p></figure></div>';\n"
    "\t\t}\n")
A_CSS = "\t\t. ':root body .nlps-rail .nlds .nlbslot{min-height:0!important}'\n"
CSS = ("\t\t. ':root body .nlps-rail .nlps-howto{margin:0;background:#fff;border:1px solid #C9D5DC;border-radius:10px;padding:10px 10px 12px}'\n"
       "\t\t. ':root body .nlps-rail .nlps-howto__k{margin:0 0 8px;font-weight:700;font-size:15px;line-height:1.3;color:#0F2233}'\n"
       "\t\t. ':root body .nlps-rail .nlps-howto__v{display:block;width:100%;height:auto;aspect-ratio:16/9;border-radius:6px;background:#0F2233}'\n"
       "\t\t. ':root body .nlps-rail .nlps-howto__s{margin:8px 0 0;font-size:13px;line-height:1.45;color:#46596A}'\n"
       "\t\t. '@media(max-width:1279px){:root body .nlps-page>.nlps-rail>.nlps-howtowrap{grid-column:1/-1;max-width:640px}}'\n")


def apply(rel, txt):
    if rel != "inc/project-stage.php":
        return txt
    for a in (A_CFG, A_RAIL, A_CSS):
        if txt.count(a) != 1:
            raise SystemExit(f"ashira_466: anchor x{txt.count(a)} in the live {rel}: {a.strip()[:60]}")
    if "ShowroomHowTo" in txt:
        raise SystemExit("ashira_466: the live file already has ShowroomHowTo")
    txt = txt.replace(A_CFG, CFG + A_CFG, 1)
    txt = txt.replace(A_RAIL, A_RAIL + RAIL, 1)
    return txt.replace(A_CSS, A_CSS + CSS, 1)
