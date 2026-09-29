# -*- coding: utf-8 -*-
"""Local preview of design system v101 (ApartmentExperience-1, HAD-346) for independent review: no deploy, no push, no lead.

How it works: a real Chrome opens the LIVE page (so the site's origin, fonts, uploads and its public map key all work) and
  1. every file under /wp-content/plugins/nadlan-config/assets/ that exists in this checkout is served from the checkout
     (bridge.js, the four stage.js/stage.css, arealife.js, areamap.js, places.json ...): the branch's JavaScript and CSS, as is;
  2. the page's HTML gets the same changes the branch's PHP prints (listed in PHP_PATCHES below, each checked to apply; a
     patch that no longer matches the live page stops the preview instead of silently showing the old page):
     the site pill + ConsultSheet rendered from inc/conversion-cta.php + inc/cta-sheet.php (WordPress stubbed), the phone stage
     height and the map-first order (inc/project-stage.php), the film's silent state and play/error handling, the estimated
     price labels (inc/project-experience.php, inc/catalog-plus-map.php), the urban map's first view (inc/urban-map.php);
  3. nothing leaves: wa.me / api.whatsapp.com are blocked and every non-GET request to nad-lan.co.il is aborted (no lead, no
     form, no analytics write).
This is the live HTML plus the branch's changes, not a WordPress install: a PHP change outside PHP_PATCHES is not shown.

  python scripts/project-stage/preview_v101.py /projects/rainbow-tel-aviv/ [--w 390 --h 844] [--headed] [--shot out.png] [--probe p.py]
  (a receipt with the SHA-256 of every local file served is printed at the end)"""
import argparse, hashlib, io, json, os, re, subprocess, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PN = os.path.join(REPO, "plugins", "nadlan-config")
ORIGIN = "https://nad-lan.co.il"
served = {}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def php_block(mode, lang, wa):
    """the pill + ConsultSheet exactly as the branch's PHP prints them (WordPress stubbed in preview_v101_cta.php), with the
    site's own WhatsApp number as the live page prints it (WhatsApp itself is blocked in the preview)"""
    out = subprocess.run(["php", os.path.join(REPO, "scripts", "project-stage", "preview_v101_cta.php"), mode, lang], capture_output=True, text=True, encoding="utf-8",
                         env={**os.environ, "NL_SITE_WA": wa})
    if out.returncode != 0 or '<div id="nlcta"' not in out.stdout:
        sys.exit("the pill harness failed: " + out.stderr[:300])
    return out.stdout


def read(rel):
    return io.open(os.path.join(PN, rel), encoding="utf-8").read()


def new_film_js_css():
    ps = read("inc/project-stage.php")
    js = "".join(re.findall(r"\t\t\. '(var bx=d\.querySelector[^\n]*?|var er=document[^\n]*?|function tryPlay\(\)[^\n]*?|pb\.addEventListener[^\n]*?|er\.querySelector\(\"button\"\)[^\n]*?)'\n", ps))
    css = "".join(re.findall(r"\t\t\. '(\.nlfilm\.is-silent [^\n]*?|\.nlfilm-play[^\n]*?|\.nlfilm-err[^\n]*?)'\n", ps))
    return js, css


def patches(path, lang, is_project):
    P = []  # (label, old, new, required)
    P.append(("stage height 60svh on phones", "@media(max-width:600px){.nlps-stage{height:70svh;min-height:360px}", "@media(max-width:600px){.nlps-stage{height:60svh;min-height:340px}", False))
    P.append(("map first in one column", ".nlps-below>#nlpjx-map{margin:0!important;min-width:0;max-width:none!important}",
              ".nlps-below>#nlpjx-map{margin:0!important;min-width:0;max-width:none!important}@media(max-width:1099px){:root body .nlps-page>.nlps-below>#nlpjx-map{order:-1}}", False))
    js, css = new_film_js_css()
    P += [("film: silent class", '<dialog id="nlfilm" class="nlfilm"', '<dialog id="nlfilm" class="nlfilm is-silent"', False),
          ("film: bar says ללא קול", " שניות · עודכן ", " שניות · ללא קול · עודכן ", False),
          ("film: play/error js", 'var v=d.querySelector("video");', 'var v=d.querySelector("video");' + js, False),
          ("film: tryPlay", "d.showModal();var p=v.play();if(p&&p.catch)p.catch(function(){});}", "d.showModal();tryPlay();}", False),
          ("film: css", ".nlfilm-bar{font-size:13px}}", ".nlfilm-bar{font-size:13px}}" + css, False),
          ("film: hero button", " שניות</small></span></a>", " שניות · ללא קול</small></span></a>", False)]
    PR = {"he": ["מחיר מוערך", "למ״ר", "לא מחייב"], "en": ["Estimated price", "per m²", "not binding"], "fr": ["Prix estimé", "le m²", "non contractuel"],
          "ru": ["Оценка цены", "за м²", "не обязывает"], "ar": ["سعر تقديري", "للمتر²", "غير ملزم"]}[lang]
    P += [("price chip label", 'el.textContent="₪"+Math.round(c.ppsqm/1000)+"K";',
           'var PR=window.NLPJX_PRICE||{est:"מחיר מוערך",sqm:"למ״ר",nb:"לא מחייב"};el.innerHTML="<small style=\\"display:block;font:600 10px/1.25 Heebo,sans-serif;color:#E6D4AE;opacity:.85\\">"+PR.est+"</small>₪"+Math.round(c.ppsqm/1000)+"K "+PR.sqm;', False),
          ("price strings", ";window.NLPJX_PLANS=", ";window.NLPJX_PRICE=" + json.dumps({"est": PR[0], "sqm": PR[1], "nb": PR[2]}, ensure_ascii=False) + ";window.NLPJX_PLANS=", False),
          ("price layer name", "₪ מחירים בסביבה", "₪ מחירים מוערכים בסביבה", False)]
    P += [("catalog chips", "el.textContent=x.name+' '+Math.round(x.psqm/1000)+'K';", "el.textContent=x.name+' ₪'+Math.round(x.psqm/1000)+'K';", False),
          ("catalog caption", "<small>מחיר למ״ר על כל פרויקט · לחיצה פותחת</small>", "<small>בערים: ממוצע עסקאות למ״ר · בפרויקטים: מחיר מוערך</small>", False),
          ("catalog pins", "el.innerHTML=p.own?('<b>'+Math.round(p.psqm/1000)+'K</b> ₪/מ״ר'):'';", "el.innerHTML=p.own?('<small class=nlcp-pin__est>מחיר מוערך</small><b>'+Math.round(p.psqm/1000)+'K</b> ₪/מ״ר'):'';", False),
          ("catalog city labels", "' ₪'],'text-size':11,'text-offset':[0,0],", "' ₪ למ״ר'],'text-size':11,'text-offset':[0,1.9],'text-anchor':'top',", False),
          ("catalog hood labels", "' ₪'],['get','name']]", "' ₪ למ״ר'],['get','name']]", False),
          ("catalog card", "'מחיר למ״ר בפרויקט, לפי היזם: <b>'", "'מחיר מוערך למ״ר בפרויקט, לפי היזם: <b>'", False),
          ("catalog city card", "'מחיר למ״ר ב'+c.name+': <b>'", "'ממוצע עסקאות למ״ר ב'+c.name+': <b>'", False),
          ("catalog pin css", ".nlcp-pin.is-featured{background:var(--sa-sea,#2F6F86)}", ".nlcp-pin__est{display:block;font:600 10px/1.2 Assistant,Heebo,sans-serif;opacity:.85}.nlcp-pin.is-featured{background:var(--sa-sea,#2F6F86)}", False)]
    return P


def stage_dict(lang):
    """the browser dictionary for a language page, built from the branch's i18n/lang-pages.json + i18n/stage-dict.json exactly
    as inc/project-stage.php prints it (the #nadlan-stage-i18n JSON)"""
    out = {"lang": lang, "exact": {}, "names": {}, "patterns": []}
    for f in ("lang-pages.json", "stage-dict.json"):
        try:
            d = json.load(io.open(os.path.join(PN, "i18n", f), encoding="utf-8"))
        except Exception:
            continue
        for he, tr in (d.get("exact") or {}).items():
            if lang in tr: out["exact"][he] = str(tr[lang])
        for he, tr in (d.get("names") or {}).items():
            if lang in tr: out["names"][he] = str(tr[lang])
        for pt in d.get("patterns") or []:
            if pt.get("re") and lang in pt: out["patterns"].append({"re": str(pt["re"]), "tr": str(pt[lang])})
    return json.dumps(out, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003C").replace(">", "\\u003E")


def urban_block(token):
    """the urban map's style + script from the branch (inc/urban-map.php, WordPress stubbed in preview_v101_urban.php), with
    the page's own public map key"""
    out = subprocess.run(["php", os.path.join(REPO, "scripts", "project-stage", "preview_v101_urban.php")], capture_output=True, text=True, encoding="utf-8",
                         env={**os.environ, "NL_PK": token})
    h = out.stdout
    if "declutter" not in h:
        sys.exit("the urban map harness failed: " + out.stderr[:300])
    a = h.index("<style>"); b = h.index("</script>", a) + len("</script>")
    return h[a:b]


def transform_html(body, path, lang, applied, strict=True):
    """the branch's PHP output applied to a live page (shared by this preview and serve_journey.py)"""
    is_project = "/projects/" in path and path.split("?")[0].strip("/") != "projects"
    # the pill + sheet: printed only where the live page prints the site pill (broker and owner pages keep theirs)
    s = body.find('<div id="nlcta"')
    if s > 0:
        e = body.find("</script>", s) + len("</script>")
        review = "לא מטעם היזם" in body[s:e] or "הסקירה" in body[s:e] or "review" in body[s:e].lower()
        m = re.search(r"wa\.me/(\d{8,15})", body[s:e])
        body = body[:s] + php_block("review" if (is_project and review) else "plain", lang, m.group(1) if m else "") + body[e:]
        applied.append("site pill + ConsultSheet (PHP)")
    # the urban renewal map's first view (inc/urban-map.php)
    us = body.find("<style>" + chr(10) + "#nlurm-map{")
    if us > 0:
        ue = body.find("</script>", us) + len("</script>")
        tk = re.search(r'accessToken="(pk\.[A-Za-z0-9._-]+)"', body[us:ue])
        body = body[:us] + urban_block(tk.group(1) if tk else "") + body[ue:]
        body = body.replace('<p class="nlurm-note">', '<p class="nlurm-sum" id="nlurm-sum" hidden></p><div class="nlurm-top" id="nlurm-top" hidden></div><p class="nlurm-note">', 1)
        applied.append("urban map first view (PHP)")
    # a language page's stage dictionary (inc/project-stage.php prints it from i18n/*.json)
    ds = body.find('<script type="application/json" id="nadlan-stage-i18n">')
    if ds > 0:
        de = body.find("</script>", ds)
        lm = re.search(r'"lang":"([a-z]{2})"', body[ds:de])
        if lm:
            body = body[:ds] + '<script type="application/json" id="nadlan-stage-i18n">' + stage_dict(lm.group(1)) + body[de:]
            applied.append("stage dictionary " + lm.group(1) + " (PHP)")
    for label, old, new, req in patches(path, lang, is_project):
        if old in body:
            body = body.replace(old, new, 1); applied.append(label)
        elif req:
            sys.exit("patch no longer matches the live page: " + label)
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path"); ap.add_argument("--w", type=int, default=1440); ap.add_argument("--h", type=int, default=900)
    ap.add_argument("--headed", action="store_true"); ap.add_argument("--shot", default="")
    ap.add_argument("--init", default="", help="a JavaScript file added as an init script before the page's own scripts (diagnostics)")
    ap.add_argument("--probe", default="", help="a Python file with run(pg, W, H, mob) -> dict, run after the page loads (its result joins the receipt)")
    a = ap.parse_args()
    lang = "he"
    for l in ("en", "fr", "ru", "ar"):
        if re.search(r"-%s/?$" % l, a.path.rstrip("/") + "/") or a.path.startswith("/" + l + "/"): lang = l
    mob = a.w < 600
    applied = []

    def page_route(route):
        r = route.fetch()
        body = transform_html(r.text(), a.path, lang, applied)
        route.fulfill(response=r, body=body, headers={**r.headers, "content-type": "text/html; charset=UTF-8"})

    def asset_route(route):
        u = route.request.url.split("?")[0]
        rel = u.split("/wp-content/plugins/nadlan-config/", 1)[1]
        lp = os.path.join(PN, *rel.split("/"))
        if os.path.isfile(lp):
            ct = {"js": "text/javascript", "css": "text/css", "json": "application/json", "svg": "image/svg+xml"}.get(rel.rsplit(".", 1)[-1], None)
            served[rel] = sha(lp)
            return route.fulfill(path=lp, content_type=ct) if ct else route.fulfill(path=lp)
        return route.continue_()

    def guard(route):
        req = route.request
        if re.match(r"https://(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)/", req.url) or (req.method != "GET" and req.url.startswith(ORIGIN)):
            return route.abort()
        return route.fallback()

    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=not a.headed, args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
        ctx = b.new_context(viewport={"width": a.w, "height": a.h}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1)
        ctx.route("**/*", guard)
        ctx.route(re.compile(r"https://nad-lan\.co\.il/wp-content/plugins/nadlan-config/.*"), asset_route)
        url = ORIGIN + a.path + ("&" if "?" in a.path else "?") + "pv101=%d" % time.time()
        ctx.route(re.compile(re.escape(ORIGIN + a.path.split("?")[0]) + r"\?.*pv101=.*"), page_route)
        if a.init:
            ctx.add_init_script(path=a.init)
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append((str(e)[:200] + " | " + " / ".join(l.strip() for l in (getattr(e, "stack", "") or "").splitlines()[1:4]))[:500]))
        pg.goto(url, wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(4000)
        probe = None
        if a.probe:
            ns = {"__file__": os.path.abspath(a.probe), "__name__": "probe"}
            exec(compile(io.open(a.probe, encoding="utf-8").read(), a.probe, "exec"), ns)
            probe = ns["run"](pg, a.w, a.h, mob)
        if a.shot:
            pg.screenshot(path=a.shot, full_page=True)
        if a.headed:
            print("the preview is open; close the browser window to finish")
            try:
                pg.wait_for_event("close", timeout=0)
            except Exception:
                pass
        receipt = {"path": a.path, "viewport": [a.w, a.h], "lang": lang, "php_changes_applied": applied, "local_files_served": served, "page_errors": errs[:5], "probe": probe,
                   "branch": subprocess.run(["git", "-C", REPO, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip(),
                   "head": subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()}
        print(json.dumps(receipt, ensure_ascii=False, indent=1))
        b.close()


if __name__ == "__main__":
    main()
