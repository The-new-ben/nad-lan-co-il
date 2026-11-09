# -*- coding: utf-8 -*-
"""HAD-686: checks for a version of page 9 (/buying-apartment/) before it is written. Read-only.
  python scripts/seo/check_buying_v3.py <page.html> [--live <live.html>] [--json out.json]
Checks: one H1; no long dash in visible text; no banned words; every live link (href + anchor) kept; no H2/H3 starts with a term
protected for another page; tables carry data-l on every td; every official-figure note has a source line; tags balanced;
6-word runs shared with competitor pages (copy check). Prints counts and exits 1 on a hard failure."""
import argparse, glob, html, io, json, os, re, sys
from html.parser import HTMLParser
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRIV = os.path.join(os.path.dirname(REPO), "_private-research", "2026-11-08-buying-guide-re", "html")
OWN = "/buying-apartment/"
BANNED = [r"אטלס", r"\bAtlas\b", r"אפס טפסים", r"\bדמו\b", r"להמחשת המנגנון"]
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "col"}

def visible(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"\[nadlan_[^\]]*\]", " ", t)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))

def hwords(t):
    return re.findall(r"[א-ת][א-ת\"'״׳\-]*|[A-Za-z]{2,}|\d[\d,\.]*", t)

class Bal(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st = []; s.err = []
    def handle_starttag(s, tag, a):
        if tag not in VOID: s.st.append((tag, s.getpos()))
    def handle_endtag(s, tag):
        if tag in VOID: return
        if s.st and s.st[-1][0] == tag: s.st.pop(); return
        # allow implicit close of p/li
        for i in range(len(s.st) - 1, -1, -1):
            if s.st[i][0] == tag:
                skipped = [x for x in s.st[i + 1:] if x[0] not in ("p", "li", "dd", "dt")]
                if skipped: s.err.append("unclosed %s before </%s> at %s" % (skipped[-1][0], tag, s.getpos()))
                del s.st[i:]; return
        s.err.append("stray </%s> at %s" % (tag, s.getpos()))

def links(t):
    out = set()
    for u, a in re.findall(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t, re.S):
        u = u.replace("https://nad-lan.co.il", "")
        out.add((u, " ".join(html.unescape(re.sub(r"<[^>]+>", "", a)).split())))
    return out

def norm_words(t):
    t = re.sub(r"[֑-ׇ]", "", t).replace("״", '"').replace("׳", "'")
    return [w.strip("\"'") for w in re.findall(r"[א-ת][א-ת\"']*", t)]

def grams(words, n=6):
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("page"); ap.add_argument("--live", default=""); ap.add_argument("--json", default="")
    ap.add_argument("--only-new", action="store_true", help="copy check only on text that is not on the live page")
    a = ap.parse_args()
    t = io.open(a.page, encoding="utf-8").read(); vis = visible(t)
    hard = []; rep = {}
    rep["words_he"] = len([w for w in hwords(vis) if re.match(r"[א-ת]", w)])
    rep["words_all"] = len(hwords(vis))
    rep["h1"] = len(re.findall(r"<h1[\s>]", t)); rep["h2"] = len(re.findall(r"<h2[\s>]", t)); rep["h3"] = len(re.findall(r"<h3[\s>]", t))
    rep["chapters"] = len(re.findall(r'class="nlbg-ch"', t)); rep["tools"] = sorted(set(re.findall(r'\[nadlan_tool id="(\w+)"', t)))
    rep["tables"] = len(re.findall(r"<table", t)); rep["fig_notes"] = len(re.findall(r"nlbg-note--fig", t))
    rep["src_lines"] = len(re.findall(r'class="nlbg-src"', t))
    rep["official_links"] = len(set(re.findall(r'href="(https?://[^"]*(?:gov\.il|kolzchut\.org\.il|boi\.org\.il|cbs\.gov\.il|knesset\.gov\.il|wikisource\.org|iec\.co\.il|israelbar\.org\.il)[^"]*)"', t)))
    if rep["h1"] > 1: hard.append("more than one h1")
    dashes = re.findall(r".{0,20}[–—].{0,20}", vis)
    if dashes: hard.append("long dashes: %d" % len(dashes)); rep["dash_samples"] = dashes[:5]
    ban = [(b, len(re.findall(b, vis))) for b in BANNED if re.search(b, vis)]
    if ban: hard.append("banned words: %s" % ban)
    # td data-l
    tds = re.findall(r"<td(?![^>]*data-l=)[^>]*>", t)
    nl_tables = re.findall(r'<table class="nlbg-tbl.*?</table>', t, re.S)
    bad_td = sum(len(re.findall(r"<td(?![^>]*data-l=)", x)) for x in nl_tables)
    if bad_td: hard.append("nlbg tables: %d td without data-l" % bad_td)
    # fig notes need a source line
    figs = re.findall(r'<div class="nlbg-note nlbg-note--fig">(.*?)</div>', t, re.S)
    nosrc = [f for f in figs if "nlbg-src" not in f]
    if nosrc: hard.append("figure notes without a source: %d" % len(nosrc))
    # balance
    b = Bal(); b.feed(t); b.close()
    if b.err: hard.append("tag errors: %d (%s)" % (len(b.err), b.err[:3]))
    # keyword guard on headings
    terms = json.load(io.open(os.path.join(REPO, "docs", "seo", "protected-keywords.json"), encoding="utf-8"))["terms"]
    heads = [" ".join(html.unescape(re.sub(r"<[^>]+>", "", h)).split()) for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", t, re.S)]
    clash = []
    for h in heads:
        hn = re.sub(r"[\"״׳']", "", h)
        for term in terms:
            k = term.get("term") or term.get("kw") or ""; owner = term.get("owner") or term.get("page") or ""
            if not k or owner == OWN: continue
            kn = re.sub(r"[\"״׳']", "", k)
            if hn.startswith(kn + " ") or hn == kn or hn.startswith(kn + ":"):
                clash.append((h, k, owner))
    rep["kw_clashes"] = clash
    if clash: hard.append("headings that lead with another page's protected term: %d" % len(clash))
    # child pages linked from page 9 own these heads (anchors in page-9-internal-links.txt); a heading here must not lead with them
    CHILD = ["איך כדאי לקנות דירה", "בדיקות לפני קניית דירה", "מסמכי הבית המשותף", "זיכרון דברים", "היתר בנייה", "טופס 4",
             "בדיקת דירה להשקעה", "דירה חדשה מול יד שנייה", "ערבות בנקאית", "חוק המכר", "פיצוי על איחור במסירה", "חוזה מכר דירה",
             "חוזה קניית דירה", "ייפוי כוח", "הפרת חוזה", "משא ומתן מול קבלן", "מה לבדוק לפני קניית דירה", "צ'ק ליסט"]
    rep["child_head_leads"] = [h for h in heads if any(h.startswith(c) for c in CHILD)]
    if rep["child_head_leads"]: hard.append("headings that lead with a child page's head: %d" % len(rep["child_head_leads"]))
    # links kept
    if a.live:
        lv = io.open(a.live, encoding="utf-8").read()
        miss = sorted(links(lv) - links(t))
        rep["live_links"] = len(links(lv)); rep["links_missing"] = miss
        if miss: hard.append("live links missing: %d" % len(miss))
        if a.only_new:
            lw = set(grams(norm_words(visible(lv))))
    # copy check against competitors
    comp = {}
    for f in glob.glob(os.path.join(PRIV, "*.json")):
        if f.endswith(".d4s.json") or f.endswith("42115af023.json"): continue
        try: r = json.load(io.open(f, encoding="utf-8"))
        except Exception: continue
        if "nad-lan.co.il" in r.get("url", "") or r.get("words_main", 0) < 250: continue
        comp[r["url"]] = grams(norm_words(" ".join(x["text"] for x in r["blocks"])))
    mine = grams(norm_words(vis))
    if a.live and a.only_new: mine -= lw
    hits = {}
    for u, g in comp.items():
        x = mine & g
        if x: hits[u] = sorted(x)
    rep["copy_6gram_hits"] = {u: v[:8] for u, v in hits.items()}; rep["copy_6gram_total"] = sum(len(v) for v in hits.values())
    rep["hard_failures"] = hard
    if a.json: io.open(a.json, "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1))
    short = {k: v for k, v in rep.items() if k not in ("copy_6gram_hits", "links_missing", "dash_samples")}
    print(json.dumps(short, ensure_ascii=False))
    if hits: print("copy hits by page:", {u.split("/")[2]: len(v) for u, v in hits.items()})
    sys.exit(1 if hard else 0)

if __name__ == "__main__":
    main()
