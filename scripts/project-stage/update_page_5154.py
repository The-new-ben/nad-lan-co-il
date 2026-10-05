# -*- coding: utf-8 -*-
"""HAD-429 (Ben 5.10.2026: "everything is approved, upload and then send links"): page 5154 (/en/buy-property-in-israel/) gets
the 6,008-net-word family-home article from Ben's package (docs/research/2026-10-05-story-package/articles/
page-5154-family-home-en-informative-v2.md, sha256 ec08f4c7...). The package's rule: replace the body with the whole approved
source, never append it to the old body; the URL, the parent, the canonical and the language fields stay as they are.
- The page keeps its own design (the .nlint style block: Frank Ruhl Libre headings, Heebo text, gold, the tables); three
  additions only: h3, the contents list, and tables that scroll sideways on a phone.
- The Yoast title and description follow the new body (the old ones promised "3D Apartments" and "2026 Taxes", 73 and 175 chars).
- Checked before: the Bank of Israel page says "This page was last updated on: 27/09/2026" (as the article says); the two gov.il
  pages open in a real browser; the four nad-lan links answer 200.
The app password is used in-process only, never printed.
  python scripts/project-stage/update_page_5154.py [--dry | --rollback]"""
import glob, hashlib, html, io, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
QA = os.path.join(REPO, "docs", "qa", "page-5154")
ART = os.path.join(REPO, "docs", "research", "2026-10-05-story-package", "articles", "page-5154-family-home-en-informative-v2.md")
ART_SHA = "ec08f4c79d25dd58170c3083b7ed7699278a5d523d1c0f62749ee05e4f9f9cc8"
NEW_TITLE = "Buying Property in Israel from Abroad: A Family Home Guide"
NEW_SEO_TITLE = "Buying Property in Israel from Abroad: A Family Home Guide"
NEW_DESC = "Buying a family home in Israel from abroad: set its purpose, test the location and the evidence, plan the full budget, appoint independent help."
EXTRA_CSS = (".nlint h3{font-family:\"Frank Ruhl Libre\",Georgia,serif;font-size:1.2rem;line-height:1.3;margin:26px 0 8px}\n"
             ".nlint .faq h3{font-size:1.05rem;margin:20px 0 6px;font-family:Heebo,sans-serif;font-weight:700}\n"
             ".nlint .nlint-toc{background:#FAF7F1;border:1px solid #E2DCD0;border-radius:12px;padding:12px 18px 12px 34px;margin:8px 0 18px}\n"
             ".nlint-tw{overflow-x:auto;margin:14px 0;-webkit-overflow-scrolling:touch}.nlint-tw table{margin:0;min-width:560px}\n")
ARGS = sys.argv[1:]


def helpers():
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
    ns = {"__name__": "upload_helpers"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
    return ns["req"]


def slug(t):
    t = re.sub(r"[^a-z0-9 \-]", "", t.lower())
    return re.sub(r" ", "-", t.strip())


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)

    def link(m):
        txt, url = m.group(1), m.group(2)
        ext = not url.startswith(("https://nad-lan.co.il", "#", "/"))
        return '<a href="%s"%s>%s</a>' % (html.escape(url, quote=True), ' target="_blank" rel="noopener"' if ext else "", txt)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)


def to_html(md):
    lines = md.replace("\r\n", "\n").split("\n")
    out, i, first_p, in_faq, toc_next = [], 0, True, False, False
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("# "):
            out.append("<h1>%s</h1>" % inline(ln[2:].strip()))
            i += 1
            continue
        if ln.startswith("## "):
            t = ln[3:].strip()
            if in_faq:
                out.append("</div>")
                in_faq = False
            out.append('<h2 id="%s">%s</h2>' % (slug(t), inline(t)))
            if t == "Buyer FAQs":
                out.append('<div class="faq">')
                in_faq = True
            toc_next = t == "Contents"
            i += 1
            continue
        if ln.startswith("### "):
            t = ln[4:].strip()
            out.append('<h3 id="%s">%s</h3>' % (slug(t), inline(t)))
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            out.append('<div class="nlint-tw"><table><thead><tr>' + "".join("<th>%s</th>" % inline(c) for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>" for r in body) + "</tbody></table></div>")
            continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:].strip())
                i += 1
            cls = ' class="nlint-toc"' if toc_next else ""
            toc_next = False
            out.append("<ul%s>" % cls + "".join("<li>%s</li>" % inline(x) for x in items) + "</ul>")
            continue
        para = [ln.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "- ")):
            para.append(lines[i].strip())
            i += 1
        text = " ".join(para)
        cls = ""
        if first_p:
            cls, first_p = ' class="lede"', False
        elif text.startswith("This article provides general information"):
            cls = ' class="note"'
        out.append("<p%s>%s</p>" % (cls, inline(text)))
    if in_faq:
        out.append("</div>")
    return "\n".join(out)


def net_words(h):
    t = re.sub(r"<ul class=\"nlint-toc\">.*?</ul>", " ", h, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", html.unescape(t)))


def main():
    req = helpers()
    if "--rollback" in ARGS:
        b = sorted(glob.glob(os.path.join(QA, "backup-*.json")))[0]
        old = json.load(io.open(b, encoding="utf-8"))
        s, r, _ = req("POST", "/wp-json/wp/v2/pages/5154", {"content": old["content"]["raw"], "title": old["title"]["raw"],
                      "meta": {"_yoast_wpseo_title": old["meta"]["_yoast_wpseo_title"], "_yoast_wpseo_metadesc": old["meta"]["_yoast_wpseo_metadesc"]}})
        print("[rollback] from", os.path.basename(b), "http", s)
        return
    md = io.open(ART, encoding="utf-8").read()
    if hashlib.sha256(md.encode("utf-8")).hexdigest() != ART_SHA:
        raise SystemExit("FATAL: the article is not the package's (sha256 differs)")
    base = json.load(io.open(sorted(glob.glob(os.path.join(QA, "backup-*.json")))[0], encoding="utf-8"))
    raw_old = base["content"]["raw"]
    style = raw_old[:raw_old.index("</style>")]
    body = to_html(md)
    new = style + EXTRA_CSS + "</style>\n<div class=\"nlint\">\n" + body + "\n</div>\n"
    words = net_words(body)
    print("[build] h1:", new.count("<h1"), "| h2:", new.count("<h2"), "| h3:", new.count("<h3"), "| tables:", new.count("<table"),
          "| net words (contents list excluded):", words, "| bytes:", len(new.encode("utf-8")))
    if new.count("<h1") != 1 or words < 5800:
        raise SystemExit("FATAL: build check failed")
    for a in re.findall(r'href="#([^"]+)"', new):
        if 'id="%s"' % a not in new:
            raise SystemExit("FATAL: contents anchor without a heading: " + a)
    io.open(os.path.join(QA, "new-content.html"), "w", encoding="utf-8").write(new)
    s, cur, _ = req("GET", "/wp-json/wp/v2/pages/5154?context=edit&_fields=modified,content,title,meta,link,parent,slug")
    if cur.get("modified") != base["modified"] or cur["content"]["raw"] != raw_old:
        raise SystemExit("FATAL: page 5154 changed since the backup (%s vs %s); re-read before writing" % (cur.get("modified"), base["modified"]))
    if "--dry" in ARGS:
        print("[dry] no writes; new content saved to docs/qa/page-5154/new-content.html")
        return
    s, r, _ = req("POST", "/wp-json/wp/v2/pages/5154", {"content": new, "title": NEW_TITLE,
                  "meta": {"_yoast_wpseo_title": NEW_SEO_TITLE, "_yoast_wpseo_metadesc": NEW_DESC}})
    print("[write] http", s)
    s, after, _ = req("GET", "/wp-json/wp/v2/pages/5154?context=edit&_fields=modified,content,title,meta,link,parent,slug")
    ok = (after["content"]["raw"] == new and after["title"]["raw"] == NEW_TITLE and after["meta"].get("_yoast_wpseo_title") == NEW_SEO_TITLE
          and after["meta"].get("_yoast_wpseo_metadesc") == NEW_DESC and after["link"] == base["link"] and after["parent"] == base["parent"] and after["slug"] == base["slug"])
    rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "ok": ok, "content_sha256": hashlib.sha256(new.encode("utf-8")).hexdigest(),
           "article_sha256": ART_SHA, "net_words": words, "old_title": base["title"]["raw"], "new_title": NEW_TITLE,
           "old_seo_title": base["meta"]["_yoast_wpseo_title"], "new_seo_title": NEW_SEO_TITLE, "new_desc": NEW_DESC,
           "link": after["link"], "modified": after["modified"]}
    io.open(os.path.join(QA, "update-record.json"), "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
    print("[verify] stored content, title, Yoast fields, link, parent, slug:", "OK" if ok else "MISMATCH")
    if not ok:
        raise SystemExit("FATAL: read-back mismatch; run --rollback")


main()
