# -*- coding: utf-8 -*-
"""Shared helpers of write_g2_page.py and write_g3_page.py (G2 /urban-renewal/pinui-binui/, G3 /urban-renewal/).
Nothing here writes to the site. get_live(): --dry reads the PUBLIC REST (content.rendered, no login) so the anchors are checked
against what is live; a real run reads the raw content through the owner's authorized runner (scripts/skin-a/deployskin.py req)."""
import io, json, math, os, re, sys, time, urllib.error, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
SITE = "https://nad-lan.co.il"; WA = "972525101555"; UPDATED = "26.10.2026"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}
P = json.load(io.open(os.path.join(DATA, "pinui.json"), encoding="utf-8"))
U = json.load(io.open(os.path.join(DATA, "urcity.json"), encoding="utf-8"))
T = json.load(io.open(os.path.join(DATA, "renewal-track.json"), encoding="utf-8"))
STATS = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "data", "renewal-stats.json"), encoding="utf-8"))
K = P["key2025"]
LM = max(i for i, s in enumerate(T["snaps"]) if s["k"] == "map")
MAPD = T["snaps"][LM]["d"]
ON = [r for r in T["recs"] if r["s"][LM] != -1]
NCX = len(ON); NCITY = len(set(r["c"] for r in ON))
PAIR = [r for r in ON if r.get("e") and r.get("p")]
MULT = sum(r["p"] for r in PAIR) / sum(r["e"] for r in PAIR)
STAGE_N = [sum(1 for r in ON if max(0, r["s"][LM]) == k) for k in range(6)]
TRACK_N = [sum(1 for r in ON if r.get("t", 0) == k) for k in range(4)]
assert NCX == STATS["map"]["total"] and NCITY == STATS["map"]["localities"], (NCX, NCITY)


def num(n): return "{:,}".format(int(round(n)))
def dmy(iso): y, m, d = iso.split("-"); return "%d.%d.%s" % (int(d), int(m), y)
HMON = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
def ym(ymv): y, m = ymv.split("-"); return "%s %s" % (HMON[int(m) - 1], y)
def add_months(ymv, k): y, m = int(ymv[:4]), int(ymv[5:7]) - 1 + k; return "%d-%02d" % (y + m // 12, m % 12 + 1)
def at_least(n, a, b): return math.ceil(n * a / b - 1e-9)
def more_than(n, a, b): return math.floor(n * a / b + 1e-9) + 1


class Tables:
    def __init__(self, prefix): self.p = prefix; self.n = 0

    def __call__(self, caption, head, rows, minw=520, num_cols=False):
        """The title sits above the scrolling box (a <caption> inside it scrolls away on phones); the table points to it."""
        self.n += 1; tid = "%st%d" % (self.p, self.n)
        h = "".join('<th scope="col">%s</th>' % c for c in head)
        b = "".join('<tr><th scope="row">%s</th>%s</tr>' % (r[0], "".join("<td>%s</td>" % c for c in r[1:])) for r in rows)
        return ('<p class="%s-cap" id="%s">%s</p>\n<div class="%s-t"><table aria-labelledby="%s"%s style="min-width:%dpx"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>\n'
                % (self.p, tid, caption, self.p, tid, ' class="%s-num"' % self.p if num_cols else "", minw, h, b))


def css(p):
    return ('<style id="%(p)s-css">.%(p)s-t{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 10px;border:1px solid #D3DCE2}'
            '.%(p)s-t table{border-collapse:collapse;width:100%%;font-variant-numeric:tabular-nums;margin:0}'
            '.%(p)s-t th,.%(p)s-t td{padding:8px 10px;font-size:15px;line-height:1.5;vertical-align:top;border-bottom:1px solid #D3DCE2;text-align:right}'
            '.%(p)s-t thead th{background:#12202A;color:#fff;font-weight:600;font-size:14px}'
            '.%(p)s-t tbody th{font-weight:600;color:#12202A;background:#F6F8F9;position:sticky;right:0;z-index:1}'
            '.%(p)s-num td{white-space:nowrap;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:14px}'
            '.%(p)s-cap{font-weight:700;color:#12202A;font-size:15px;line-height:1.5;margin:22px 0 8px}'
            '.%(p)s-fig{margin:22px 0}.%(p)s-fig figcaption{font-size:14px;color:#3E4C58;margin-top:6px;line-height:1.6}'
            '.%(p)s-note{font-size:15px;line-height:1.7;color:#3E4C58}'
            '.%(p)s-cta{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 18px}.%(p)s-cta a{display:inline-block;padding:12px 18px;border-radius:6px;font-weight:600;text-decoration:none;'
            'border:1.5px solid #1F4B5C;color:#1F4B5C;background:#fff}.%(p)s-cta a.%(p)s-go{background:#1F4B5C;color:#fff}'
            '.%(p)s-tool{scroll-margin-top:96px;margin:18px 0 26px}'
            '.%(p)s-en{direction:ltr;text-align:left;border-top:3px solid #12202A;padding-top:6px}'
            '@media(max-width:600px){.%(p)s-t th,.%(p)s-t td{font-size:14px;padding:7px 8px}.%(p)s-cta a{flex:1 1 100%%;text-align:center}'
            '.%(p)s-fig svg{margin-left:calc(50%% - 50vw + 6px);margin-right:calc(50%% - 50vw + 6px);width:calc(100vw - 12px)!important;max-width:none!important}}</style>\n') % {"p": p}


def fig(p, svg, cap): return '<figure class="%s-fig">%s<figcaption>%s</figcaption></figure>\n' % (p, svg, cap)


def faq(items): return "".join("<h3>%s</h3>\n<p>%s</p>\n" % (q, a) for q, a in items)


def visible(html):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"\[nadlan_[a-z_]+[^\]]*\]", " ", h)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)) + " " + " ".join(re.findall(r'aria-label="([^"]*)"', html))


BANNED_NEW = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה(?! תכנונית)|טעון אימות|נדל[״\"]?ן חכם|Nadlan|nadlan(?!\.gov)|מודל|מנגנון|שכבה|שכבות|הדגמה|טכנולוגי|יחסית|כמעט|אטלס|Atlas|פיילוט|פרוטוטייפ|רספונסיבי|מובייל|לחצו|לחיצה|הקליקו"
BANNED_PAGE = r"ממשק|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|טעון אימות|נדל[״\"]?ן חכם|Nadlan"


def gates(new_html, page_html, faq_n_want):
    nv, pv = visible(new_html), visible(page_html)
    assert not re.search(r"[–—]", nv), "long dash in the new copy: " + str(re.findall(r".{20}[–—].{20}", nv)[:3])
    hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_NEW, nv); assert not hits, ("language law, new copy", hits[:5])
    hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_PAGE, pv); assert not hits, ("language law, whole page", hits[:5])
    assert not re.search(r"(?<![\d.,])0 (₪|חדרים|חודשים|ערים|מתחמים|דירות)", nv), "a zero number on visible text"
    assert new_html.count("<h1") <= 1, "the new copy adds an h1"
    assert page_html.count("<h1") == 1, ("exactly one h1", page_html.count("<h1"))
    for sv in re.findall(r"<svg\b.*?</svg>", new_html, flags=re.S):
        assert min(float(x) for x in re.findall(r"font-size:([\d.]+)px", sv)) >= 12 and 'viewBox="0 0 420 ' in sv and 'direction="rtl"' in sv and 'aria-label="' in sv
    fs = re.search(r"<h2[^>]*>\s*(?:שאלות נפוצות|Frequently asked questions)[^<]{0,60}</h2>(.*?)(?=<h2|$)", re.sub(r"<!--.*?-->", "", page_html, flags=re.S), flags=re.S).group(1)
    qs = [re.sub(r"<[^>]+>", "", q).strip() for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", fs, flags=re.S)]
    assert len(qs) == faq_n_want and len(set(qs)) == len(qs), ("FAQ count", len(qs), faq_n_want, len(set(qs)))
    return qs


class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


OP = urllib.request.build_opener(NoRedir)


def status(u):
    try: return OP.open(urllib.request.Request(u, headers=UA), timeout=60).status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return type(e).__name__


def check_links(html):
    hrefs = sorted(set(re.findall(r'href="([^"#][^"]*)"', html)))
    inner = [h for h in hrefs if h.startswith("/") or h.startswith(SITE)]
    bad = []
    for h in inner:
        st = status(h if h.startswith("http") else SITE + urllib.parse.quote(h, safe="/:?=&%"))
        if st != 200: bad.append((h, st))
        time.sleep(0.15)
    offi = [(h, status(h)) for h in hrefs if h.startswith("http") and not h.startswith(SITE) and "wa.me" not in h]
    return inner, bad, offi


def get_live(pid, dry):
    """dry: the public REST (rendered content, no login); otherwise the raw content via the owner's authorized runner."""
    if dry:
        r = json.loads(urllib.request.urlopen(urllib.request.Request(SITE + "/wp-json/wp/v2/pages/%d?_fields=content,link,modified" % pid, headers=UA), timeout=90).read().decode("utf-8"))
        return None, r["content"]["rendered"], r
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "g2g3page"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
    req = ns["req"]
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,modified,meta" % pid)
    return req, r["content"]["raw"], r


def apply(raw, R):
    new = raw
    for o, n in R:
        c = new.count(o)
        assert c == 1, ("anchor must match once", c, o[:90])
        new = new.replace(o, n)
    return new


def render_shell(path, title, content, tool_ids, prefix):
    """A local render: the content in a 760px column with the engine and the tools from the local files, mounted as the shortcode does."""
    A = "../../../../../plugins/nadlan-config/assets/instruments/"
    data = {"pinui": ["pinui.json", "renewal-track.json"], "urcity": ["urcity.json", "renewal-track.json"]}
    names = {"pinui": ("מחשבון · פינוי בינוי", "הבניין שלכם בפינוי בינוי: הרוב לפי החוק, מה מגיע לכם וכמה זמן"), "urcity": ("מפה · התחדשות עירונית", "התחדשות עירונית בעיר שלכם: מתחמים, מסלולים ותמ\"א 38")}
    for tid in tool_ids:
        k, n = names[tid]
        host = ('<section class="nli" dir="rtl" lang="he" aria-label="%s"><div class="nli-host" data-nli="%s" data-nli-data="%s"><div class="nli__panel"><p class="nli__kicker">%s</p><h2 class="nli__title">%s</h2></div></div></section>'
                % (n, tid, ",".join(A + "data/" + f + "?ver=local" for f in data[tid]), k, n))
        content = content.replace('[nadlan_tool id="%s"]' % tid, host)
    shell = ('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">'
             '<title>%s · תצוגה מקומית</title>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800&family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
             '<link rel="stylesheet" href="%score.css?ver=local"><style>html,body{margin:0;background:#fff;color:#12202A;font:400 17px/1.75 "IBM Plex Sans Hebrew",Heebo,sans-serif}'
             '.entry-content{padding:0 16px}.entry-content>*{max-width:760px;margin-left:auto;margin-right:auto}h1{font:800 30px/1.25 Heebo,sans-serif;margin:24px auto 8px}'
             'h2{font:700 24px/1.35 Heebo,sans-serif;margin:34px auto 10px}h3{font:700 19px/1.4 Heebo,sans-serif;margin:22px auto 6px}a{color:#1F4B5C}</style></head>'
             '<body><main><div class="entry-content">%s</div></main><script src="%score.js?ver=local" defer></script>%s</body></html>'
             % (title, A, content, A, "".join('<script src="%stools/%s.js?ver=local" defer></script>' % (A, t) for t in tool_ids)))
    io.open(path, "w", encoding="utf-8", newline="").write(shell)


def counts(new):
    words = len(re.findall(r"[\w֐-׿\"'״]+", visible(re.sub(r"<svg\b.*?</svg>", " ", new, flags=re.S))))
    cells = len(re.findall(r"<t[dh][ >]", re.sub(r"<svg\b.*?</svg>", "", new, flags=re.S)))
    figs = len(re.findall(r"\d[\d,.]*", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg)\b.*?</\1>", " ", new, flags=re.S))))
    return {"words": words, "tables": new.count("<table"), "cells": cells, "figures": figs, "svg": new.count("<svg"), "h2": new.count("<h2"), "h3": new.count("<h3")}
