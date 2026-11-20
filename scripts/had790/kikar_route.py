# -*- coding: utf-8 -*-
"""HAD-790 precheck helper: load the live Kikar page with the new server part put in (the showroom's place after the buttons and
the page class, from place-he.html / place-en.html that php renders from inc/project-stage.php) and the local showroom.js.
Set KF_LOCAL to the folder that holds the two place files; without it nothing is routed (the live site as it is)."""
import os, re
LOCAL = os.environ.get("KF_LOCAL", "")  # precheck: a folder with place-he.html / place-en.html (the new PHP's output, rendered by php)
PLUG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "plugins", "nadlan-config")


def precheck_routes(ctx, lang):
    """the live page with the new server part put in (the place after the buttons, the page class) and the local showroom.js"""
    place = open(os.path.join(LOCAL, "place-%s.html" % lang), encoding="utf-8").read()
    def page(route):
        r = route.fetch(); h = r.text()
        a = h.find('<div class="nlds nlps-ctawrap"'); assert a > 0, "no buttons block"
        depth, e = 0, -1  # the block's own end (it holds the project row with its own divs), like nadlan_ps_close
        for m in re.finditer(r"<(/?)div[\s>]", h[a:]):
            depth += -1 if m.group(1) else 1
            if depth == 0: e = a + m.start() + len("</div>"); break
        assert e > a, "no end of the buttons block"
        h = h[:e] + place + h[e:]
        h = h.replace('<div class="nlps-page nlps-page--world"', '<div class="nlps-page nlps-page--world nlps-page--sr"', 1)
        route.fulfill(response=r, body=h, headers={**r.headers, "content-type": "text/html; charset=UTF-8"})
    ctx.route("**/projects/hamedina*/?kf=*", page)
    ctx.route("**/project-stage/world/showroom.js*", lambda route: route.fulfill(path=os.path.join(PLUG, "assets", "project-stage", "world", "showroom.js"), content_type="text/javascript"))


