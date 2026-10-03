# -*- coding: utf-8 -*-
"""The hunk of release 1.72.409 (HAD-403, design v104.32): the project pages' finance box stops printing a monthly amount.
Measured 3.10.2026: the line computed ppsqm x a FIXED 90 m2 for every project (SIX 8 publishes 232-339 m2), and the projects'
`project_3d_units` are illustrative examples ("דוגמה — קומה 11", "זמינות להדגמה בלבד", "להמחשה"), never published inventory,
so no published size exists to compute from. The box keeps the mortgage-calculator link (already translated on the language
pages) and is shown exactly where it was before (projects with an average price per m2, never on world pages).
Applied to the LIVE text by deploy409.py (the anchor exactly once) and by --apply to the repo copy."""
import io, os, sys

OLD_HEAD = "\t\t\tif ( $ppsqm && ! $nlpjx_world ) :\n\t\t\t\t$est = $ppsqm * 90 * 0.75 * ( 0.05 / 12 ) / ( 1 - pow( 1 + 0.05 / 12, -360 ) );\n"
OLD_TAIL = "\t\t\t\t<a href=\"<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>\">לחישוב אישי במחשבון המשכנתא ←</a></div>\n\t\t\t<?php endif; ?>\n"
NEW = ("\t\t\tif ( $ppsqm && ! $nlpjx_world ) : // HAD-403 (v104.32, 3.10.2026): no monthly amount. The units are illustrative examples,\n"
       "\t\t\t\t// not published inventory, so there is no published size to compute from (the old line used a fixed 90 m2 everywhere).\n"
       "\t\t\t?>\n"
       "\t\t\t<div class=\"nlpjx-fin-est\">\n"
       "\t\t\t\t<a href=\"<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>\">לחישוב אישי במחשבון המשכנתא ←</a></div>\n"
       "\t\t\t<?php endif; ?>\n")


def apply(txt):
    a = txt.find(OLD_HEAD)
    if a < 0 or txt.count(OLD_HEAD) != 1:
        raise SystemExit("px_409: the head anchor is there " + str(txt.count(OLD_HEAD)) + " times")
    b = txt.find(OLD_TAIL, a)
    if b < 0 or txt.count(OLD_TAIL) != 1:
        raise SystemExit("px_409: the tail anchor is there " + str(txt.count(OLD_TAIL)) + " times")
    block = txt[a:b + len(OLD_TAIL)]
    if block.count("\n") > 12 or "סדר גודל של החזר חודשי לדירת ~90 מ״ר" not in block:
        raise SystemExit("px_409: the block between the anchors is not the finance estimate")
    return txt[:a] + NEW + txt[b + len(OLD_TAIL):]


if __name__ == "__main__" and "--apply" in sys.argv:
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "inc", "project-experience.php")
    t = io.open(p, encoding="utf-8", newline="").read()
    crlf = "\r\n" in t
    t = apply(t.replace("\r\n", "\n"))
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
    print("applied to the repo copy")
