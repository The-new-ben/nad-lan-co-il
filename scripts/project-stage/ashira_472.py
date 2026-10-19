# -*- coding: utf-8 -*-
"""Release 1.72.472 (HAD-543): the walk's full screen gets a thin top bar (title + "סגירה") so the close button never sits on
the walk's own title on phones (seen on 1.72.471). Hunks on the LIVE inc/project-stage.php: the 1.72.471 script and sheet."""
import ashira_471 as P
RELS = ["inc/project-stage.php"]
OLD_JS = 'x.onclick=c;document.addEventListener("keydown",k);o.appendChild(f);o.appendChild(x);'
NEW_JS = ('x.textContent="סגירה \u00d7";var hd=document.createElement("div");hd.className="nlps-walkov__h";var ht=document.createElement("b");ht.textContent="הליכה חופשית · אשירה";hd.appendChild(ht);hd.appendChild(x);'
          'x.onclick=c;document.addEventListener("keydown",k);o.appendChild(hd);o.appendChild(f);')
OLD_CSS = [l for l in P.CSS.split("\n") if "nlps-walkov" in l]
NEW_CSS = [
    "\t\t. ':root body .nlps-walkov{position:fixed;inset:0;z-index:2147483000;background:#0F2233;display:flex;flex-direction:column}'",
    "\t\t. ':root body .nlps-walkov iframe{display:block;width:100%;flex:1 1 auto;min-height:0;border:0}'",
    "\t\t. ':root body .nlps-walkov__h{flex:none;display:flex;align-items:center;justify-content:space-between;gap:10px;direction:rtl;padding:max(6px,env(safe-area-inset-top)) max(12px,env(safe-area-inset-right)) 6px max(12px,env(safe-area-inset-left));background:#0F2233;color:#fff}'",
    "\t\t. ':root body .nlps-walkov__h b{font-size:15px;color:#fff}'",
    "\t\t. ':root body .nlps-walkov__x{min-height:40px;padding:6px 14px;border-radius:999px;border:2px solid #fff;background:#0F2233;color:#fff;font-size:15px;font-weight:700;line-height:1;cursor:pointer}'",
]


def apply(rel, txt):
    if rel != "inc/project-stage.php":
        return txt
    if txt.count(OLD_JS) != 1 or len(OLD_CSS) != 3:
        raise SystemExit("ashira_472: the 1.72.471 script anchor x%d, css lines %d" % (txt.count(OLD_JS), len(OLD_CSS)))
    txt = txt.replace(OLD_JS, NEW_JS, 1)
    a = "\n".join(OLD_CSS) + "\n"
    if txt.count(a) != 1:
        raise SystemExit("ashira_472: the 1.72.471 sheet x%d" % txt.count(a))
    return txt.replace(a, "\n".join(NEW_CSS) + "\n", 1)
