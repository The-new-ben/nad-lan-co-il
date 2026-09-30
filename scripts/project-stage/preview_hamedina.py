# -*- coding: utf-8 -*-
"""Local preview of /projects/hamedina/ and /projects/hamedina-en/ (Kikar Hamedina P7a), as close to the real page as possible
WITHOUT WordPress: no deploy, no push, no lead, nothing written anywhere but the local shots folder.

How the page is made (the preview_v101.py idea):
  1. the live Dimri Yama page (he, or its -en sibling) is fetched read-only: the theme's header, footer, styles and the site's
     WhatsApp bar come from it;
  2. its post content is replaced by what WordPress would hand the stage's compose for the new post: the breadcrumbs, the
     machine H1 (the post title), the answer paragraph as .nl-lead (nadlan_lead_extract), the rest of post-he.html / post-en.html
     with the non-affiliation notice before the article wrapper (nadlan_project_notice_render), and the area map section
     (the live page's own, re-centred on the plot, its place registry = hamedina/places.json, its POI lists emptied: the live
     server computes them per page, and Dimri's belong to another area);
  3. the RELEASE copy of inc/project-stage.php (65af09be + the hunks of hamedina_ps_patch.py: exactly what deploy369 writes)
     composes it through ps_render_harness.php (WordPress stubbed), and its head / footer pieces replace Dimri's stage pieces;
  4. Playwright (Chrome) serves every /wp-content/plugins/nadlan-config/ file from this checkout (the world module, the Hamedina
     data and posters), blocks WhatsApp, analytics and every non-GET request, and takes the shots.

  python scripts/project-stage/preview_hamedina.py            (both languages, 390x844 and 1440x900)
Shots: docs/research/2026-09-30-kikar-hamedina/p7-shots/ ; the receipt (content-first probe, WhatsApp line, errors): p7-shots/receipt.json

P8 (1.72.370): the French, Russian and Arabic pages on the release copy deploy370 writes (hamedina_ps_patch370.py), each on the
live Dimri Yama sibling in the same language (-fr, -ru, -ar: the site's header, footer and WhatsApp bar in that language):
  python scripts/project-stage/preview_hamedina.py --p8        (fr, ru, ar -> p8-shots/)
"""
import hashlib, io, json, os, re, subprocess, sys, tempfile, time, urllib.request, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import hamedina_ps_patch as PATCH  # noqa: E402
import hamedina_page_data as DATA  # noqa: E402
import hamedina_ps_patch370 as PATCH370  # noqa: E402

P8 = "--p8" in sys.argv[1:]
VER = "1.72.370" if P8 else "1.72.369"
LANGS = ("fr", "ru", "ar") if P8 else ("he", "en")

PN = os.path.join(REPO, "plugins", "nadlan-config")
RES = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina")
OUT = os.path.join(RES, "p8-shots" if P8 else "p7-shots")
ORIGIN = "https://nad-lan.co.il"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-P7a-preview/1.0"
LAT, LNG = "32.086758", "34.789776"
TITLE = {l: DATA.POSTS[l]["title"] for l in DATA.POSTS}
SEO = {l: {"title": DATA.POSTS[l]["seo_title"], "desc": DATA.POSTS[l]["seo_desc"], "faq_json": DATA.faq_json(l)} for l in DATA.POSTS}
ICON = {}
GOOGLEBOT_PHONE = ("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/126.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90) as r:
        return r.read().decode("utf-8")


def close_div(html, start):
    depth = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", html[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start + m.end()
    raise SystemExit("unclosed div")


def normalized(content):
    """the post_content as deploy369 stores it: one line, no whitespace between tags"""
    return re.sub(r">\s*\n\s*<", "><", content.strip())


def notice(lang):
    if lang in ("fr", "ru", "ar"):  # the fleet's own words (inc/legal-notice.php), naming the page's developer_name
        src = io.open(os.path.join(PN, "inc", "legal-notice.php"), encoding="utf-8").read()
        m = re.search(r"'" + lang + r"' => array\( \"([^\"]+)\", \"([^\"]+)\"", src)
        dn = DATA.POSTS[lang]["meta"]["developer_name"]
        return ('<aside class="nl-projnotice" dir="' + ("rtl" if lang == "ar" else "ltr") + '" role="note"><b>' + m.group(1) + '</b><span>'
                + m.group(2).replace("%s", dn) + '</span></aside>')
    if lang == "en":
        return ('<aside class="nl-projnotice" dir="ltr" role="note"><b>Independent site</b><span>This page is not the official website of '
                'the Kikar Hamedina landowners’ company and is not operated on its behalf. NadLan is an independent information platform with no '
                'commercial connection to the developer. Details were gathered from public sources and should be verified with the developer.</span></aside>')
    return ('<aside class="nl-projnotice" dir="rtl" role="note"><b>אתר עצמאי</b><span>עמוד זה אינו האתר הרשמי של חברת בעלי הקרקע בכיכר המדינה '
            'ואינו מופעל מטעמה. נדל״ן היא פלטפורמת מידע עצמאית, ללא קשר מסחרי עם היזם. הפרטים נאספו ממקורות גלויים ויש לאמת אותם מול היזם.</span></aside>')


def build_pre(lang, rel_copy):
    live = get(ORIGIN + "/projects/dimri-yama-sde-dov" + ("" if lang == "he" else "-" + lang) + "/?p7a=%d" % time.time())
    html = live
    ICON[lang] = re.search(r'<svg class="nlds-ico" viewBox=.*?</svg>', live, re.S).group(0)
    # the head: title, description, hreflang, the stage's head pieces become the world page's
    html = re.sub(r"<title>.*?</title>", "<title>" + SEO[lang]["title"].replace("&", "&amp;") + "</title>", html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="' + SEO[lang]["desc"] + '"', html, count=1)
    fam = ("he", "en", "fr", "ru", "ar") if P8 else ("he", "en")
    alt = "".join('<link rel="alternate" hreflang="%s" href="https://nad-lan.co.il/projects/hamedina%s/" />\n' % (l, "" if l == "he" else "-" + l) for l in fam)
    html = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]+" />\n?)+',
                  alt + '<link rel="alternate" hreflang="x-default" href="https://nad-lan.co.il/projects/hamedina/" />\n', html, count=1)
    # the post content, as WordPress would hand it to the compose
    a = html.find('<div class="entry-content wp-block-post-content')
    a_in = html.find(">", a) + 1
    e = close_div(html, a)
    inner = html[a_in:e - len("</div>")]
    nav = re.search(r'<style>\.nlptop\{.*?</style><nav class="nlptop".*?</nav>', inner, re.S).group(0)
    nav = re.sub(r"<b>[^<]*</b></div><div class=\"nlptop-l\"", "<b>" + TITLE[lang] + "</b></div><div class=\"nlptop-l\"", nav, count=1)
    lab = {"he": "עב", "en": "EN", "fr": "FR", "ru": "RU", "ar": "AR"}
    sw = "".join(("<b>%s</b>" % lab[l]) if l == lang else ('<a href="https://nad-lan.co.il/projects/hamedina%s/" hreflang="%s">%s</a>' % ("" if l == "he" else "-" + l, l, lab[l])) for l in fam)
    nav = re.sub(r'<div class="nlptop-l".*?</div>', '<div class="nlptop-l" aria-label="Languages">' + sw + '</div>', nav, count=1, flags=re.S)
    mi = html.find('id="nlpjx-map"')
    ms = html.rfind("<section", 0, mi)
    me = html.find("</section>", ms) + len("</section>")
    mapsec = html[ms:me]
    mapsec = re.sub(r'data-lat="[^"]*"', 'data-lat="' + LAT + '"', mapsec)
    mapsec = re.sub(r'data-lng="[^"]*"', 'data-lng="' + LNG + '"', mapsec)
    mapsec = re.sub(r'data-title="[^"]*"', 'data-title="' + TITLE[lang] + '"', mapsec)
    mapsec = re.sub(r'data-places="[^"]*"', 'data-places="https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/hamedina/places.json?ver=' + VER + '"', mapsec)
    mapsec = re.sub(r"<script>window\.NLPJX_POIS=.*?</script>", '<script>window.NLPJX_POIS={"schools":[],"kindergartens":[],"parks":[],"transit":[],"shops":[],"health":[],"food":[]};window.NLPJX_PLANS=[];</script>', mapsec, count=1, flags=re.S)
    body = DATA.content(lang)
    lead = re.match(r"<p>.*?</p>", body).group(0)
    rest = body[len(lead):]
    # as the live theme prints it (read on the live /projects/hamedina-en/, 30.9): the notice, then the whole post content in the
    # theme's article wrapper (div.nadlan-project-article.nadlan-guide), the post's own empty wrapper at its end
    new_inner = (nav + '<h1 id="nl-project-page-title" class="screen-reader-text">' + TITLE[lang] + '</h1>'
                 + '<div class="nl-lead">' + lead + '</div>' + notice(lang) + '<div class="nadlan-project-article nadlan-guide">' + rest + '</div>' + mapsec)
    html = html[:a_in] + new_inner + html[e - len("</div>"):]
    return html


def render(lang, rel_copy, pre_html):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(pre_html)
        pre = t.name
    slug = "hamedina" + ("" if lang == "he" else "-" + lang)
    r = subprocess.run(["php", os.path.join(HERE, "ps_render_harness.php"), rel_copy, slug, pre], capture_output=True,
                       env={**os.environ, "NL_SITE_WA": "972525101555", "NL_VER": VER, "NL_LAT": LAT, "NL_LNG": LNG})
    os.unlink(pre)
    if r.returncode:
        raise SystemExit("harness: " + r.stderr.decode("utf-8", "replace")[:500])
    d = json.loads(r.stdout.decode("utf-8"))
    html = d["composed"]
    if 'nlps-stage--world' not in html:
        raise SystemExit("the compose did not run (no world stage in the page)")
    # head: Dimri's stage block (import map .. the stage's modulepreload) and its layout style -> the release copy's
    hs = html.find('<script type="importmap" id="nadlan-ps-importmap">')
    he_ = html.find("\n", html.find('rel="modulepreload" href="https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/dimri/stage.js'))
    html = html[:hs] + d["wp_head"]["1#0"].strip() + html[he_:]
    css_s = html.find('<style id="nadlan-ps-css">')
    css_e = html.find("</style>", css_s) + len("</style>")
    ps_css = [v for k, v in d["wp_head"].items() if 'id="nadlan-ps-css"' in v][0].strip()
    html = html[:css_s] + ps_css + d["wp_head"]["1000#0"].strip() + html[css_e:]
    # footer: no bridge.js, no stage dictionary; the world's module script instead
    html = re.sub(r'<script type="module" id="nadlan-ps-bridge"[^>]*></script>', d["wp_footer"]["60#0"].strip(), html, count=1)
    html = re.sub(r'<script type="application/json" id="nadlan-stage-i18n">.*?</script>', "", html, count=1, flags=re.S)
    html = re.sub(r'<script id="nadlan-stage-i18n-js">.*?</script>', "", html, count=1, flags=re.S)
    # a language page: the server's language pass (inc/lang-pages.php) turns the stage blocks' dir="rtl" lang="he" into the
    # page's direction and language (Arabic stays right to left)
    if lang != "he":
        s0 = html.find('<div class="nlps-page')
        e0 = html.find('<section class="nlws"', s0)
        html = html[:s0] + html[s0:e0].replace('dir="rtl" lang="he"', 'dir="%s" lang="%s"' % ("rtl" if lang == "ar" else "ltr", lang)) + html[e0:]
    # the WhatsApp icon as the site prints it (the harness stubs nlds_icon), and the branch's source line (inc/wa-source.php)
    html = html.replace('<svg class="nlds-ico" data-i="whatsapp"></svg>', ICON[lang])
    ws = io.open(os.path.join(PN, "inc", "wa-source.php"), encoding="utf-8").read()
    ws = ws[ws.index('<script id="nadlan-wa-source">'): ws.index("</script>", ws.index('<script id="nadlan-wa-source">')) + 9]
    html = re.sub(r'<script id="nadlan-wa-source">.*?</script>', lambda m: ws, html, count=1, flags=re.S)
    # P8: the branch's WhatsApp pill (inc/conversion-cta.php: its style and its script, the release's P7.1 and ru fixes)
    cc = io.open(os.path.join(PN, "inc", "conversion-cta.php"), encoding="utf-8").read()
    cs = cc.index("<style>\n#nlcta{position:fixed")
    c_style = cc[cs: cc.index("</style>", cs) + 8]
    ks = cc.index("<script>\n(function(){\n\twindow.dataLayer")
    c_script = cc[ks: cc.index("</script>", ks) + 9]
    m1 = re.search(r"<style>\s*#nlcta\{position:fixed", html)
    if m1:
        hs = m1.start()
        he_ = html.index("</style>", hs) + 8
        html = html[:hs] + c_style + html[he_:]
        m2 = re.compile(r"<script>\s*\(function\(\)\{\s*window\.dataLayer").search(html, hs)
        if m2:
            ke2 = html.index("</script>", m2.start()) + 9
            html = html[:m2.start()] + c_script + html[ke2:]
    # the FAQ schema of the English page (_nl_faq_schema, printed by inc/schema-meta.php) replaces Dimri's
    html = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>', "", html, count=1, flags=re.S)
    if lang != "he":
        html = html.replace("</head>", '<script type="application/ld+json">' + SEO[lang]["faq_json"] + "</script>\n</head>", 1)
    return html


def probe_js():
    return """(() => { const R = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
  return r.height ? Math.round(r.top + scrollY) : null; };
  const X = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.right]; };
  const a = X('.nl-lead'), b = X('#nlps');
  const stacked = !!(a && b && Math.min(a[1], b[1]) - Math.max(a[0], b[0]) > 40);
  return { h1: R('h1'), h1n: document.querySelectorAll('h1').length, lead: R('.nl-lead'), cta: R('.nlps-hero__cta'), stage: R('#nlps'), map: R('#nlpjx-map'),
           facts: R('#nlws-facts'), faq: R('#nlws-faq'), stacked, vh: innerHeight }; })()"""


def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    rel_copy = os.path.join(tempfile.mkdtemp(prefix="kh-rel-"), "project-stage.php")
    if P8:  # what deploy370 writes: what 1.72.369 wrote (md5-checked) + the P8 hunks
        io.open(rel_copy, "w", encoding="utf-8", newline="").write(PATCH370.release_text())
    else:
        base = subprocess.run(["git", "-C", REPO, "show", PATCH.BASE_COMMIT + ":" + PATCH.REL], capture_output=True).stdout.decode("utf-8")
        io.open(rel_copy, "w", encoding="utf-8", newline="").write(PATCH.apply(base, PATCH.BASE_COMMIT))
    pages = {lang: render(lang, rel_copy, build_pre(lang, rel_copy)) for lang in LANGS}
    for lang, h in pages.items():
        io.open(os.path.join(OUT, "_page-%s.html" % lang), "w", encoding="utf-8").write(h)
    served, receipt = {}, {"when": time.strftime("%Y-%m-%d %H:%M"), "release_copy_md5": hashlib.md5(open(rel_copy, "rb").read()).hexdigest(), "pages": {}}

    def asset(route):
        u = route.request.url.split("?")[0]
        rel = u.split("/wp-content/plugins/nadlan-config/", 1)[1]
        lp = os.path.join(PN, *rel.split("/"))
        if os.path.isfile(lp):
            served[rel] = hashlib.sha256(open(lp, "rb").read()).hexdigest()[:16]
            ct = {"js": "text/javascript", "css": "text/css", "json": "application/json", "webp": "image/webp", "jpg": "image/jpeg"}.get(rel.rsplit(".", 1)[-1])
            return route.fulfill(path=lp, content_type=ct) if ct else route.fulfill(path=lp)
        return route.continue_()

    def guard(route):
        rq = route.request
        if re.match(r"https://(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)/", rq.url) or (rq.method != "GET" and rq.url.startswith(ORIGIN)) \
                or re.search(r"google-analytics\.com|googletagmanager\.com|doubleclick\.net|facebook\.(com|net)|clarity\.ms|hotjar", rq.url):
            return route.abort()
        return route.fallback()

    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"])
        for lang in LANGS:
            path = "/projects/hamedina" + ("" if lang == "he" else "-" + lang) + "/"
            for size, w, h, mob, ua in (("390", 390, 844, True, None), ("1440", 1440, 900, False, None), ("412g", 412, 915, True, GOOGLEBOT_PHONE)):
                ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if size == "390" else 1,
                                    **({"user_agent": ua} if ua else {}), locale={"he": "he-IL", "en": "en-US", "fr": "fr-FR", "ru": "ru-RU", "ar": "ar"}[lang])
                ctx.route("**/*", guard)
                ctx.route(re.compile(r"https://nad-lan\.co\.il/wp-content/plugins/nadlan-config/.*"), asset)
                html = pages[lang]
                def serve_page(body):
                    def f(route):
                        route.fulfill(status=200, body=body, content_type="text/html; charset=utf-8")
                    return f
                ctx.route(re.compile(re.escape(ORIGIN + path) + r"\?pv=.*"), serve_page(html))
                pg = ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)[:240]))
                pg.on("console", lambda m: errs.append("console " + m.type + ": " + m.text[:200]) if m.type == "error" else None)
                pg.goto(ORIGIN + path + "?pv=%d" % time.time(), wait_until="load", timeout=120000)
                pg.wait_for_timeout(1500)
                pr = pg.evaluate(probe_js())
                key = f"{lang}-{size}"
                rec = {"probe": pr}
                vh = pr["vh"]
                if size in ("412g", "390"):
                    rec["C3"] = pr["lead"] is not None and pr["lead"] <= 1.2 * vh and (pr["stage"] is None or pr["lead"] < pr["stage"])
                    rec["C4"] = pr["stage"] is not None and pr["stage"] <= 1.5 * vh
                    if size == "412g":
                        receipt["pages"][key] = rec
                        ctx.close()
                        continue
                if size == "1440":
                    rec["C3"] = pr["lead"] is not None and pr["lead"] <= vh
                    rec["C4"] = pr["stage"] is not None and pr["stage"] <= vh
                pre = "%s-%s" % (lang, size)
                pg.screenshot(path=os.path.join(OUT, pre + "-01-first-screen.png"))
                # the world: scroll to it, wait until it is ready
                pg.evaluate("document.getElementById('nlps').scrollIntoView({block:'center'})")
                try:
                    pg.wait_for_function("window.__nlpsWorld && document.querySelector('.nlw-poster.is-gone')", timeout=90000)
                    rec["world_ready"] = True
                except Exception as e:
                    rec["world_ready"] = "no: " + str(e)[:120]
                pg.wait_for_timeout(1200)
                pg.locator("#nlps").screenshot(path=os.path.join(OUT, pre + "-02-world-aerial.png"))
                # the hero's "virtual tour" button: the walk
                pg.evaluate("window.scrollTo(0,0)")
                pg.click('[data-nlps-ev="hero-world"]')
                pg.wait_for_timeout(2600)
                pg.locator("#nlps").screenshot(path=os.path.join(OUT, pre + "-03-world-walk.png"))
                # a tower, a floor, a facing (as a visitor would, source 'user'): the view from the window and the card's WhatsApp
                pg.evaluate("(async()=>{const w=window.__nlpsWorld; w.setMode('tower','user'); w.pickTower('C','user'); w.setFloor(30,'user'); w.setFacing(270,'user'); w.setView('window');})()")
                pg.wait_for_timeout(2600)
                pg.locator("#nlps").screenshot(path=os.path.join(OUT, pre + "-04-world-window-C30-west.png"))
                pg.evaluate("window.__nlpsWorld.setView('out')")
                pg.evaluate("window.__nlpsWorld.show('tower','C')")
                pg.wait_for_timeout(1500)
                pg.locator("#nlps").screenshot(path=os.path.join(OUT, pre + "-05-world-card-tower-C.png"))
                rec["pick"] = pg.evaluate("window.__nlpsPick || null")
                wa = pg.evaluate("""() => { const a = document.querySelector('#nlps .nlw-btn--wa'); if (!a) return null;
                    const bg = getComputedStyle(a).backgroundColor;
                    a.addEventListener('click', (e) => e.preventDefault(), { once: true });
                    a.click(); const u = new URL(a.getAttribute('href')); return { bg, text: u.searchParams.get('text') }; }""")
                rec["card_whatsapp"] = wa
                pg.evaluate("window.__nlpsWorld.closeCard()")
                # what is nearby (the place registry, walking minutes): the cafés
                pg.evaluate("(async()=>{const w=window.__nlpsWorld; w.setView('out'); w.setMode('places','user'); w.setCategory('food');})()")
                pg.wait_for_timeout(2600)
                pg.evaluate("document.getElementById('nlps').scrollIntoView({block:'end'})")
                pg.wait_for_timeout(600)
                pg.locator("#nlps").screenshot(path=os.path.join(OUT, pre + "-05b-world-nearby-food.png"))
                # the sections
                for sid, nm in (("nlws-facts", "06-facts"), ("nlps-deals", "07-deals-table"), ("nlws-prices", "08-prices"), ("nlws-when", "09-when"), ("nlws-timeline", "10-timeline"), ("nlws-faq", "11-faq"), ("nlpjx-map", "12-area-map")):
                    if pg.locator("#" + sid).count():
                        # instant, under the sticky header (the theme scrolls smoothly: a shot mid-scroll paints half a page)
                        pg.evaluate(f"(()=>{{const e=document.getElementById('{sid}');window.scrollTo({{top:e.getBoundingClientRect().top+scrollY-90,behavior:'instant'}});}})()")
                        pg.wait_for_timeout(1400)
                        pg.screenshot(path=os.path.join(OUT, f"{pre}-{nm}.png"))
                pg.evaluate("window.scrollTo(0,0)")
                pg.wait_for_timeout(400)
                pg.screenshot(path=os.path.join(OUT, pre + "-00-full.png"), full_page=True)
                rec["errors"] = errs[:12]
                receipt["pages"][key] = rec
                print(key, json.dumps({k: v for k, v in rec.items() if k != "probe"}, ensure_ascii=False)[:600])
                print("   probe", pr)
                ctx.close()
        b.close()
    # the shots as WebP (quality 88), like the P5 world shots: the repository keeps them small
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".png"):
            im = Image.open(os.path.join(OUT, f)).convert("RGB")
            if im.height > 16000:  # WebP's limit is 16,383 px: a phone's full page is scaled to fit
                im = im.resize((round(im.width * 16000 / im.height), 16000), Image.LANCZOS)
            im.save(os.path.join(OUT, f[:-4] + ".webp"), "WEBP", quality=88, method=6)
            os.remove(os.path.join(OUT, f))
    keep = os.environ.get("NL_KEEP_PAGES")  # a folder OUTSIDE the repository (the scratchpad) to check the runner's needs against
    for f in ["_page-%s.html" % l for l in LANGS]:  # the rendered pages carry the site's public map token: not kept in the repository
        if os.path.exists(os.path.join(OUT, f)):
            if keep:
                os.makedirs(keep, exist_ok=True)
                os.replace(os.path.join(OUT, f), os.path.join(keep, f))
            else:
                os.remove(os.path.join(OUT, f))
    receipt["local_files_served"] = served
    io.open(os.path.join(OUT, "receipt.json"), "w", encoding="utf-8").write(json.dumps(receipt, ensure_ascii=False, indent=1))
    print("shots in", OUT)


if __name__ == "__main__":
    main()
