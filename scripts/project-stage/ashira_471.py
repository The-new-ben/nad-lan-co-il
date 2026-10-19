# -*- coding: utf-8 -*-
"""Release 1.72.471 (HAD-543, Ben 19.10.2026: "yes put the walk and vids in the page"): the free walk around Ashira
(assets/walk/ashira/, its own three.js page that reads the stage's city, places and the tour's 360 files) gets a card at the
top of the how-to card (same place: under the broker slot on desktop, under the stage on phones); a tap opens it full screen
over the page, with a close button. The films stay below it. Hunks on the LIVE inc/project-stage.php, each anchor once."""
RELS = ["inc/project-stage.php"]
A_CFG = "\t\t\t\t\t'films' => array(\n"
CFG = "\t\t\t\t\t'walk'  => array( 'src' => 'walk/ashira/index.html', 'thumb' => 'walk/ashira/thumb.jpg' ), // 1.72.471\n" + A_CFG
A_RAIL = "\t\t\t$rail .= '<div class=\"nlds nlps-howtowrap\">' . $nlps_howto . '</div>';\n"
JS = ('(function(){if(window.__nlpsWalk)return;window.__nlpsWalk=1;document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[data-nlps-walk]");if(!a)return;e.preventDefault();'
      'var o=document.createElement("div");o.className="nlps-walkov";o.setAttribute("role","dialog");o.setAttribute("aria-label","הליכה חופשית במתחם");'
      'var f=document.createElement("iframe");f.src=a.href;f.title="הליכה חופשית במתחם";f.allow="fullscreen";'
      'var x=document.createElement("button");x.type="button";x.className="nlps-walkov__x";x.setAttribute("aria-label","סגירה");x.textContent="×";'
      'var k=function(ev){if(ev.key==="Escape")c()};var c=function(){o.remove();document.documentElement.style.overflow="";document.removeEventListener("keydown",k);a.focus()};'
      'x.onclick=c;document.addEventListener("keydown",k);o.appendChild(f);o.appendChild(x);document.body.appendChild(o);document.documentElement.style.overflow="hidden";'
      'f.addEventListener("load",function(){try{f.focus()}catch(err){}});try{if(window.gtag)gtag("event","walk_open",{project:"ashira"})}catch(err){}})})();')
RAIL = (
    "\t\t// WalkAshira (1.72.471, Ben 19.10.2026): the free walk around the compound, a card over the films; it opens full screen\n"
    "\t\tif ( '' !== $nlps_howto && ! empty( $ps['howto']['walk']['src'] ) && is_readable( dirname( __DIR__ ) . '/assets/' . $ps['howto']['walk']['src'] ) ) {\n"
    "\t\t\t$wu = plugins_url( 'assets/', dirname( __FILE__ ) );\n"
    "\t\t\t$nlps_howto = '<a class=\"nlps-walk\" data-nlps-walk data-nlps-ev=\"walk\" href=\"' . esc_url( $wu . $ps['howto']['walk']['src'] . $hv ) . '\">'\n"
    "\t\t\t\t. '<img src=\"' . esc_url( $wu . $ps['howto']['walk']['thumb'] . $hv ) . '\" alt=\"הליכה חופשית במתחם אשירה ובסביבה (הדמיה)\" width=\"1280\" height=\"720\" loading=\"lazy\" decoding=\"async\">'\n"
    "\t\t\t\t. '<span class=\"nlps-walk__b\"><b>הליכה חופשית במתחם ובסביבה</b><small>הולכים בין הבניינים, נכנסים ללובי, למתקנים ולדירה, ורואים כמה דקות הליכה לכל מקום.</small><i>להתחיל ללכת</i></span></a>'\n"
    "\t\t\t\t. '<script>" + JS + "</script>' . $nlps_howto;\n"
    "\t\t}\n" + A_RAIL)
A_CSS = "\t\t. ':root body .nlps-howto__tab[aria-selected=\"true\"]{background:#0F2233;border-color:#0F2233;color:#fff}'\n"
CSS = (A_CSS +
       "\t\t. ':root body .nlps-walk{display:block;margin:0 0 10px;border-radius:10px;overflow:hidden;background:#0F2233;border:1px solid #0F2233;text-decoration:none!important;color:#fff!important}'\n"
       "\t\t. ':root body .nlps-walk img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}'\n"
       "\t\t. ':root body .nlps-walk__b{display:grid;gap:4px;padding:10px 12px 12px}'\n"
       "\t\t. ':root body .nlps-walk__b b{font-size:16px;line-height:1.3;color:#fff}'\n"
       "\t\t. ':root body .nlps-walk__b small{font-size:13px;line-height:1.45;color:#D9E7F7}'\n"
       "\t\t. ':root body .nlps-walk__b i{font-style:normal;justify-self:start;margin-top:4px;background:#fff;color:#0F2233;font-weight:700;font-size:14px;padding:8px 16px;border-radius:999px}'\n"
       "\t\t. ':root body .nlps-walkov{position:fixed;inset:0;z-index:2147483000;background:#0F2233}'\n"
       "\t\t. ':root body .nlps-walkov iframe{display:block;width:100%;height:100%;border:0}'\n"
       "\t\t. ':root body .nlps-walkov__x{position:absolute;left:50%;transform:translateX(-50%);top:max(10px,env(safe-area-inset-top));width:48px;height:48px;border-radius:50%;border:2px solid #fff;background:#0F2233;color:#fff;font-size:28px;line-height:1;cursor:pointer}'\n")


def apply(rel, txt):
    if rel != "inc/project-stage.php":
        return txt
    for a in (A_CFG, A_RAIL, A_CSS):
        if txt.count(a) != 1:
            raise SystemExit(f"ashira_471: anchor x{txt.count(a)} in the live {rel}: {a.strip()[:60]}")
    return txt.replace(A_CFG, CFG, 1).replace(A_RAIL, RAIL, 1).replace(A_CSS, CSS, 1)
