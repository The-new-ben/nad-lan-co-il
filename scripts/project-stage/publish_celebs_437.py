# -*- coding: utf-8 -*-
"""HAD-437 (Ben 5.10.2026: a full article on where Israeli celebrities live, sources cited, linked smartly to our projects):
publish docs/content/celebs-2026-10/article-he.md as a new Hebrew page /celebs-homes/ in the EditorialArticle style (design system
component EditorialArticle v1, RTL). The URL words celebs / homes own no URL (url_word_audit, 5.10). The facts are the 49 verified
rows (research-facts.md); main removed Yossi Cohen (security), the Ribo tax clause, the Zahavi seller detail.
App password in-process, never printed.   python publish_celebs_437.py [--dry]"""
import html, io, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(REPO, "docs", "content", "celebs-2026-10", "article-he.md")
QA = os.path.join(REPO, "docs", "qa", "had-437")
SLUG = "celebs-homes"
TITLE = "איפה גרים הסלבס בישראל"
SEO_TITLE = "איפה גרים הסלבס בישראל? הדירות והבתים שקנו ידוענים"
SEO_DESC = "עומר אדם בכיכר המדינה, נועה קירל ויהודה לוי בשדה דב, רותם סלע בסומייל: איפה גרים הסלבס בישראל ומה קנו, לפי פרסומים ועם מקורות."
ALLOWED_OWN = ("https://nad-lan.co.il/projects/hamedina/", "https://nad-lan.co.il/projects/rainbow-tel-aviv/",
               "https://nad-lan.co.il/projects/ashira-sde-dov/", "https://nad-lan.co.il/projects/utopia-sde-dov/",
               "https://nad-lan.co.il/projects/h-infinity-somail-tel-aviv/", "https://nad-lan.co.il/compound/sde-dov/")
FORBIDDEN = ("יוסי כהן", "מחלוקת מס", "אפריקה ישראל", "בלעדי", "קומה ", "קומת ", "רוטשילד")
STYLE = """<style>
.nlint{--gold:#9C7A3C;--ink:#1B1A17;--cream:#FAF7F1;font-family:Heebo,system-ui,sans-serif;color:var(--ink);max-width:860px;margin:0 auto;line-height:1.7;direction:rtl}
.nlint h1,.nlint h2,.nlint h3{font-family:"Frank Ruhl Libre",Georgia,serif;line-height:1.25;text-wrap:balance}
.nlint h1{font-size:clamp(1.9rem,1.4rem+2vw,2.7rem);margin:8px 0 14px}
.nlint h2{font-size:clamp(1.35rem,1.1rem+1vw,1.8rem);margin:38px 0 12px;border-bottom:2px solid #E2DCD0;padding-bottom:8px}
.nlint h3{font-size:1.2rem;margin:26px 0 8px}
.nlint .lede{font-size:1.12rem;color:#51483A}
.nlint .src{font-size:.95em;color:#5B5346}
.nlint-tw{overflow-x:auto;margin:14px 0;-webkit-overflow-scrolling:touch}.nlint-tw table{margin:0;min-width:620px}
.nlint table{width:100%;border-collapse:collapse;font-size:14.5px}
.nlint th,.nlint td{border:1px solid #E2DCD0;padding:9px 12px;text-align:start;vertical-align:top}
.nlint th{background:#F3EEE3;color:var(--ink)}
.nlint ul li{margin:7px 0}
.nlint .faq h3{font-size:1.05rem;margin:20px 0 6px;font-family:Heebo,sans-serif;font-weight:700}
.nlint .note{font-size:13.5px;color:#6D665C;background:#F7F1E3;border:1px solid #D6C189;border-radius:10px;padding:12px 16px;margin:16px 0}
</style>
"""
ARGS = sys.argv[1:]


def helpers():
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
    ns = {"__name__": "h437"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
    return ns["req"]


def slug(t):
    t = re.sub(r"[^\w \-]", "", t.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", "-", t.strip())


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", t)

    def link(m):
        txt, url = m.group(1), m.group(2)
        own = url.startswith("https://nad-lan.co.il")
        return '<a href="%s"%s>%s</a>' % (html.escape(url, quote=True), "" if own else ' target="_blank" rel="noopener"', txt)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)


def to_html(md):
    lines = md.replace("\r\n", "\n").split("\n")
    out, i, first_p, in_faq = [], 0, True, False
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith("# "):
            out.append("<h1>%s</h1>" % inline(ln[2:].strip())); i += 1; continue
        if ln.startswith("## "):
            t = ln[3:].strip()
            if in_faq:
                out.append("</div>"); in_faq = False
            out.append('<h2 id="%s">%s</h2>' % (slug(t), inline(t)))
            if t == "שאלות נפוצות":
                out.append('<div class="faq">'); in_faq = True
            i += 1; continue
        if ln.startswith("### "):
            t = ln[4:].strip(); out.append('<h3 id="%s%s">%s</h3>' % ('faq-' if in_faq else '', slug(t), inline(t))); i += 1; continue
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
        text = " ".join(para)
        if text.startswith("*") and text.endswith("*") and text.count("*") == 2:
            out.append('<p class="note">%s</p>' % inline(text.strip("*"))); continue
        cls = ' class="lede"' if first_p else ""
        first_p = False
        out.append("<p%s>%s</p>" % (cls, inline(text)))
    if in_faq:
        out.append("</div>")
    return "\n".join(out)


def main():
    md = io.open(ART, encoding="utf-8").read()
    body_md = md[md.index("\n---\n") + 5:]
    for w in FORBIDDEN:
        if w in body_md:
            raise SystemExit("FATAL: forbidden text in the article: " + w)
    body = to_html(body_md)
    new = STYLE + '<div class="nlint">\n' + body + "\n</div>\n"
    own = sorted(set(re.findall(r'href="(https://nad-lan\.co\.il[^"]*)"', new)))
    bad = [u for u in own if u not in ALLOWED_OWN]
    words = len(re.findall(r"\S+", html.unescape(re.sub(r"<[^>]+>", " ", body))))
    print("[build] h1:", new.count("<h1"), "| h2:", new.count("<h2"), "| tables:", new.count("<table"), "| own links:", own, "| words:", words)
    if new.count("<h1") != 1 or bad or words < 2500:
        raise SystemExit("FATAL: build check failed; bad links: %s" % bad)
    os.makedirs(QA, exist_ok=True)
    io.open(os.path.join(QA, "celebs-homes.html"), "w", encoding="utf-8").write(new)
    req = helpers()
    s, ex, _ = req("GET", "/wp-json/wp/v2/pages?slug=%s&status=publish,draft,private,pending,future&_fields=id,status,link" % SLUG)
    if isinstance(ex, list) and ex:
        raise SystemExit("FATAL: a page with this slug already exists: %s" % ex)
    if "--dry" in ARGS:
        print("[dry] no writes; html saved to docs/qa/had-437/celebs-homes.html"); return
    s, r, _ = req("POST", "/wp-json/wp/v2/pages", {"title": TITLE, "slug": SLUG, "status": "publish", "content": new,
                  "meta": {"_yoast_wpseo_title": SEO_TITLE, "_yoast_wpseo_metadesc": SEO_DESC}})
    if s not in (200, 201):
        raise SystemExit("FATAL create: http %s %s" % (s, str(r)[:300]))
    pid = r["id"]
    s, b, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,link,status,content,meta,slug" % pid)
    ok = b["content"]["raw"] == new and b["slug"] == SLUG and b["status"] == "publish" and b["meta"].get("_yoast_wpseo_title") == SEO_TITLE
    rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "id": pid, "link": b["link"], "ok": ok, "words": words}
    io.open(os.path.join(QA, "publish-record.json"), "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
    print("[publish] page", pid, b["link"], "| read-back identical:", ok)


main()
