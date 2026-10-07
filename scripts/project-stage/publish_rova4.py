# -*- coding: utf-8 -*-
"""HAD-460 spoke (Ben 7.10.2026: content about Kikar HaMedina and all its area, no cannibalization): publish
docs/content/rova-4-2026-10/article-he.md as a new Hebrew page /north-tel-aviv/rova-4/ (child of /north-tel-aviv/, page 4866),
in the EditorialArticle style (.nlint, RTL), with the price guide [nadlan_price_guide key="rova-4"] right after the opening
paragraphs (needs plugin 1.72.433+: the shortcode door). URL words: north, tel, aviv, rova, 4 (rova owned by no URL, 7.10).
Owns "רובע 4 תל אביב" (320/mo), "רובע 4" (90); the towers' prices stay on /projects/hamedina/, "הצפון הישן" on /old-north/.
App password in-process, never printed.   python publish_rova4.py [--dry]"""
import html
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(REPO, "docs", "content", "rova-4-2026-10", "article-he.md")
QA = os.path.join(REPO, "docs", "qa", "had-460", "rova-4")
SLUG, PARENT = "rova-4", 4866
SHORT = '[nadlan_price_guide key="rova-4"]'
OWN_OK = re.compile(r"^https://nad-lan\.co\.il/[a-z0-9/\-]*$")
FORBIDDEN = ("אטלס", "—", "–", "!", "הזדמנות", "מושלם", "מדהים", "חלום", "אנחנו מתווכים", "גלובס", "ביזפורטל", "כלכליסט", "דה מרקר",
             "ynet", "מדלן", "יד2", "nadlan.gov.il")
STYLE = """<style>
.nlint{--gold:#9C7A3C;--ink:#14212b;font-family:Assistant,Heebo,system-ui,sans-serif;color:var(--ink);max-width:860px;margin:0 auto;line-height:1.7;direction:rtl}
.nlint h1,.nlint h2,.nlint h3{font-family:"Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif;line-height:1.25;text-wrap:balance}
.nlint h2{font-size:clamp(1.35rem,1.1rem + 1vw,1.8rem);margin:38px 0 12px;border-bottom:1px solid #e3e1da;padding-bottom:8px}
.nlint h3{font-size:1.2rem;margin:26px 0 8px}
.nlint .lede{font-size:1.12rem;color:#3b4753}
.nlint-tw{overflow-x:auto;margin:14px 0;-webkit-overflow-scrolling:touch}.nlint-tw table{margin:0;min-width:560px}
.nlint table{width:100%;border-collapse:collapse;font-size:14.5px}
.nlint th,.nlint td{border:1px solid #e3e1da;padding:9px 12px;text-align:start;vertical-align:top}
.nlint th{background:#eee9dd;color:var(--ink)}
.nlint ul li{margin:7px 0}
.nlint .faq h3{font-size:1.05rem;margin:20px 0 6px;font-family:Assistant,Heebo,sans-serif;font-weight:700}
.nlint .nlpg{margin-block:22px 8px !important}
</style>
"""
ARGS = sys.argv[1:]


def helpers():
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
    ns = {"__name__": "rova4"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
    return ns["req"]


def slug(t):
    t = re.sub(r"[^\w \-]", "", t.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", "-", t.strip())


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", t)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: '<a href="%s">%s</a>' % (html.escape(m.group(2), quote=True), m.group(1)), t)


def to_html(md):
    lines = md.replace("\r\n", "\n").split("\n")
    out, i, first_p, in_faq, short_done = [], 0, True, False, False
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith("## "):
            if not short_done:  # the price guide after the opening paragraphs, before the first section
                out.append("\n" + SHORT + "\n"); short_done = True
            t = ln[3:].strip()
            if in_faq:
                out.append("</div>"); in_faq = False
            out.append('<h2 id="%s">%s</h2>' % (slug(t), inline(t)))
            if t == "שאלות נפוצות":
                out.append('<div class="faq">'); in_faq = True
            i += 1; continue
        if ln.startswith("### "):
            t = ln[4:].strip(); out.append('<h3 id="%s%s">%s</h3>' % ("faq-" if in_faq else "", slug(t), inline(t))); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, body = rows[0], rows[2:]
            out.append('<div class="nlint-tw"><table><thead><tr>' + "".join("<th>%s</th>" % inline(c) for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>" for r in body) + "</tbody></table></div>")
            continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:].strip()); i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % inline(x) for x in items) + "</ul>"); continue
        para = [ln.strip()]; i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "- ")):
            para.append(lines[i].strip()); i += 1
        out.append("<p%s>%s</p>" % (' class="lede"' if first_p else "", inline(" ".join(para))))
        first_p = False
    if in_faq:
        out.append("</div>")
    return "\n".join(out)


def main():
    md = io.open(ART, encoding="utf-8").read()
    fm, body_md = md.split("\n---\n", 1)
    meta = dict(re.findall(r"^(\w+):\s*(.+)$", fm.replace("---\n", "", 1), re.M))
    for w in FORBIDDEN:
        if w in body_md or w in meta.get("seo_title", "") + meta.get("meta_description", "") + meta.get("h1", ""):
            raise SystemExit("FATAL: forbidden text: " + w)
    body = "<h1>%s</h1>\n" % html.escape(meta["h1"], quote=False) + to_html(body_md)  # the page's one H1 lives in the content (as on /celebs-homes/)
    new = STYLE + '<div class="nlint">\n' + body + "\n</div>\n"
    own = sorted(set(re.findall(r'href="([^"]+)"', new)))
    bad = [u for u in own if not OWN_OK.match(u)]
    words = len(re.findall(r"\S+", html.unescape(re.sub(r"<[^>]+>", " ", body))))
    print("[build] h1:", new.count("<h1"), "| h2:", new.count("<h2"), "| tables:", new.count("<table"), "| links:", own, "| words:", words,
          "| shortcode:", new.count(SHORT))
    if new.count("<h1") != 1 or bad or words < 2000 or new.count(SHORT) != 1:
        raise SystemExit("FATAL: build check failed; external or odd links: %s" % bad)
    for u in own:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-link-check"}), timeout=60)
        if r.status != 200:
            raise SystemExit("FATAL: link %s answers %s" % (u, r.status))
    os.makedirs(QA, exist_ok=True)
    io.open(os.path.join(QA, "rova-4.html"), "w", encoding="utf-8").write(new)
    req = helpers()
    s, ex, _ = req("GET", "/wp-json/wp/v2/pages?slug=%s&parent=%d&status=publish,draft,private,pending,future&_fields=id,status,link" % (SLUG, PARENT))
    if isinstance(ex, list) and ex:
        raise SystemExit("FATAL: a page with this slug already exists: %s" % ex)
    s, h, _ = req("GET", "/wp-json/nadlan/v1/health")
    v = tuple(int(x) for x in str(h.get("version", "0.0.0")).split("."))
    if v < (1, 72, 433):
        raise SystemExit("FATAL: the shortcode needs plugin 1.72.433 or later; live is %s" % h.get("version"))
    if "--dry" in ARGS:
        print("[dry] no writes; html saved to docs/qa/had-460/rova-4/rova-4.html"); return
    s, r, _ = req("POST", "/wp-json/wp/v2/pages", {"title": "רובע 4 בתל אביב", "slug": SLUG, "parent": PARENT, "status": "publish", "content": new,
                  "meta": {"_yoast_wpseo_title": meta["seo_title"], "_yoast_wpseo_metadesc": meta["meta_description"]}})
    if s not in (200, 201):
        raise SystemExit("FATAL create: http %s %s" % (s, str(r)[:300]))
    pid = r["id"]
    s, b, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,link,status,content,meta,slug,parent" % pid)
    ok = b["content"]["raw"] == new and b["slug"] == SLUG and b["parent"] == PARENT and b["status"] == "publish" and b["meta"].get("_yoast_wpseo_title") == meta["seo_title"]
    rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "id": pid, "link": b["link"], "ok": ok, "words": words}
    io.open(os.path.join(QA, "publish-record.json"), "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
    print("[publish] page", pid, b["link"], "| read-back identical:", ok)


main()
