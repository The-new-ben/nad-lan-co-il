# -*- coding: utf-8 -*-
"""L7 of docs/loop/LANG-PROJECTS-LOOP.md (Ben 25.10.2026: the language pages strengthen each other): the buyer guide of each
language (/en|ru|fr/new-projects/, its own intent) gets one sentence after its opening paragraph that sends the reader to the
catalog in the same language (/xx/projects/). One sentence per page, written natively; nothing else in the page changes.
Backup of the live content first, read-back, live check. Skips a page that already links to its catalog.
  python docs/research/2026-10-25-projects-hub/link_guides.py [--dry] [en ru fr]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "lg"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
LANGS = [a for a in sys.argv[1:] if a in ("en", "ru", "fr")] or ["en", "ru", "fr"]
SENT = {
    "en": 'Looking for the developments on the market right now? The full list, with the prices developers publish, by city and by Tel Aviv area, is on <a href="/en/projects/">New Projects in Israel</a>.',
    "ru": 'Ищете проекты, которые продаются сейчас? Полный список новостроек с ценами застройщиков, по городам и районам Тель-Авива: <a href="/ru/projects/">Новостройки в Израиле</a>.',
    "fr": 'Vous cherchez les programmes en commercialisation aujourd’hui ? La liste complète, avec les prix publiés par les promoteurs, par ville et par quartier de Tel Aviv : <a href="/fr/projects/">Programmes neufs en Israël</a>.',
}
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for lang in LANGS:
    s, root, _ = req("GET", "/wp-json/wp/v2/pages?slug=%s&parent=0&_fields=id" % lang)
    s, np, _ = req("GET", "/wp-json/wp/v2/pages?slug=new-projects&parent=%d&context=edit&_fields=id,link,content" % root[0]["id"])
    p = np[0]; raw = p["content"]["raw"]; pid = p["id"]
    if re.search(r'href="(?:https://nad-lan\.co\.il)?/%s/projects/"' % lang, raw):
        print("[%s] already links to /%s/projects/, skipped" % (lang, lang)); continue
    i = raw.index("</p>") + 4
    m = re.match(r"\s*<!-- /wp:paragraph -->", raw[i:])
    if m:
        i += m.end(); add = '\n\n<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->' % SENT[lang]
    else:
        add = '\n<p>%s</p>' % SENT[lang]
    new = raw[:i] + add + raw[i:]
    print("[%s] page %d: insert after char %d | before: ...%s" % (lang, pid, i, re.sub(r"<[^>]+>", "", raw[max(0, i - 160):i]).replace("\n", " ")[-120:]))
    if DRY:
        continue
    io.open(os.path.join(bk, "page-%d-%s.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": new})
    back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
    time.sleep(2)
    page = urllib.request.urlopen(urllib.request.Request(p["link"] + "?nll=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    bd = page[page.find("<body"):]
    ok = {"read-back": back == new, "link on the page": ('href="/%s/projects/"' % lang) in bd, "one h1": bd.count("<h1") == 1,
          "no long dash added": not re.search(r"[–—]", SENT[lang])}
    for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
