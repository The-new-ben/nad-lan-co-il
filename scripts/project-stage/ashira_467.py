# -*- coding: utf-8 -*-
"""Release 1.72.467 (HAD-543, phones first): the how-to film of 1.72.466 sits in the side rail, which drops to the bottom of
the page under 1280px (about 6,300px down on a phone). The same card now also shows right under the stage there, and the rail
copy hides at those widths; desktop keeps the card under the broker slot exactly as Ben asked. Hunks on the LIVE text."""
import ashira_466 as P
RELS = ["inc/project-stage.php"]
OLD_RAIL = P.RAIL
NEW_RAIL = (
    "\t\t// ShowroomHowTo (1.72.466, Ben 19.10.2026): the film of the showroom's controls, under the broker slot on the side;\n"
    "\t\t// 1.72.467: the same card under the stage below 1280px, where the rail drops to the bottom of the page\n"
    "\t\t$nlps_howto = '';\n"
    "\t\tif ( ! empty( $ps['howto']['src'] ) && is_readable( dirname( __DIR__ ) . '/assets/project-stage/' . $ps['dir'] . '/' . $ps['howto']['src'] ) ) {\n"
    "\t\t\t$hu = plugins_url( 'assets/project-stage/' . $ps['dir'] . '/', dirname( __FILE__ ) );\n"
    "\t\t\t$hv = '?ver=' . nadlan_ps_ver();\n"
    "\t\t\t$nlps_howto = '<figure class=\"nlps-howto\"><figcaption class=\"nlps-howto__k\">' . esc_html( (string) $ps['howto']['title'] ) . '</figcaption>'\n"
    "\t\t\t\t. '<video class=\"nlps-howto__v\" controls playsinline preload=\"none\" width=\"1280\" height=\"720\" poster=\"' . esc_url( $hu . $ps['howto']['poster'] . $hv ) . '\" data-nlps-ev=\"howto\"><source src=\"' . esc_url( $hu . $ps['howto']['src'] . $hv ) . '\" type=\"video/mp4\"></video>'\n"
    "\t\t\t\t. '<p class=\"nlps-howto__s\">' . esc_html( (string) $ps['howto']['sub'] ) . '</p></figure>';\n"
    "\t\t\t$rail .= '<div class=\"nlds nlps-howtowrap\">' . $nlps_howto . '</div>';\n"
    "\t\t}\n")
A_STAGE = ". $legend . $src . '</div></div>';\n"
NEW_STAGE = ". $legend . $src . '</div>' . ( '' !== $nlps_howto ? '<div class=\"nlds nlps-howtom\">' . $nlps_howto . '</div>' : '' ) . '</div>';\n"
OLD_CSS = P.CSS
NEW_CSS = ("\t\t. ':root body .nlps-howto{margin:0;background:#fff;border:1px solid #C9D5DC;border-radius:10px;padding:10px 10px 12px}'\n"
           "\t\t. ':root body .nlps-howto__k{margin:0 0 8px;font-weight:700;font-size:15px;line-height:1.3;color:#0F2233}'\n"
           "\t\t. ':root body .nlps-howto__v{display:block;width:100%;height:auto;aspect-ratio:16/9;border-radius:6px;background:#0F2233}'\n"
           "\t\t. ':root body .nlps-howto__s{margin:8px 0 0;font-size:13px;line-height:1.45;color:#46596A}'\n"
           "\t\t. ':root body .nlps-howtom{display:none}'\n"
           "\t\t. '@media(max-width:1279px){:root body .nlps-page>.nlps-rail>.nlps-howtowrap{display:none!important}:root body .nlps-howtom{display:block;margin-top:12px;max-width:640px}}'\n")


def apply(rel, txt):
    if rel != "inc/project-stage.php":
        return txt
    for a in (OLD_RAIL, A_STAGE, OLD_CSS):
        if txt.count(a) != 1:
            raise SystemExit(f"ashira_467: anchor x{txt.count(a)} in the live {rel}: {a.strip()[:60]}")
    return txt.replace(OLD_RAIL, NEW_RAIL, 1).replace(A_STAGE, NEW_STAGE, 1).replace(OLD_CSS, NEW_CSS, 1)
