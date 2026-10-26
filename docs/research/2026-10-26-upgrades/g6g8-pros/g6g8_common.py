# -*- coding: utf-8 -*-
"""Shared helpers of write_g6_page.py, write_g7_page.py and write_g8_page.py (the professionals cluster: /home-inspection/ page 90,
/real-estate-appraiser/ page 86, /real-estate-lawyer/ page 11). Nothing here writes to the site.
get_live(): --dry reads the PUBLIC REST (content.rendered, no login) so every anchor is checked against what is live today;
a real run reads the raw content through the owner's authorized runner (scripts/skin-a/deployskin.py req), as in G2/G3."""
import io, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
SITE = "https://nad-lan.co.il"; WA = "972525101555"; UPDATED = "26.10.2026"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}
BD = json.load(io.open(os.path.join(DATA, "bedek.json"), encoding="utf-8"))
SH = json.load(io.open(os.path.join(DATA, "shamai.json"), encoding="utf-8"))
OD = json.load(io.open(os.path.join(DATA, "orechdin.json"), encoding="utf-8"))
PT = json.load(io.open(os.path.join(DATA, "ptax.json"), encoding="utf-8"))


def num(n): return "{:,}".format(int(round(n)))
def ils(n): return num(n) + " ₪"
def dmy(iso): y, m, d = iso[:10].split("-"); return "%d.%d.%s" % (int(d), int(m), y)
def pct(x, d=1): return ("%." + str(d) + "f%%") % (100 * x)


def wa_link(text): return "https://wa.me/%s?text=%s" % (WA, urllib.parse.quote(text))


class Tables:
    def __init__(self, prefix): self.p = prefix; self.n = 0

    def __call__(self, caption, head, rows, minw=520, num_cols=False, note=""):
        """The title sits above the scrolling box (a <caption> inside it scrolls away on phones); the table points to it."""
        self.n += 1; tid = "%st%d" % (self.p, self.n)
        h = "".join('<th scope="col">%s</th>' % c for c in head)
        b = "".join('<tr><th scope="row">%s</th>%s</tr>' % (r[0], "".join("<td>%s</td>" % c for c in r[1:])) for r in rows)
        return ('<p class="%s-cap" id="%s">%s</p>\n<div class="%s-t"><table aria-labelledby="%s"%s style="min-width:%dpx"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>\n'
                % (self.p, tid, caption, self.p, tid, ' class="%s-num"' % self.p if num_cols else "", minw, h, b)
                + ('<p class="%s-note">%s</p>\n' % (self.p, note) if note else ""))


def css(p, guide=False):
    """Instruments identity: ink #12202A, sea #2F6F86, deep #1F4B5C, line #D3DCE2, survey red #C42550 only for a warning.
    The site skin forces its link colour inside page content, so every CTA colour carries !important (fix_r2_cta.py lesson).
    guide=True: the page body sits inside the old .nadlan-guide wrapper, whose p/li/table/section rules would restyle the tool."""
    s = ('<style id="%(p)s-css">.%(p)s-t{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 10px;border:1px solid #D3DCE2;background:#fff}'
         '.%(p)s-t table{border-collapse:collapse;width:100%%;font-variant-numeric:tabular-nums;margin:0;box-shadow:none;border-radius:0;overflow:visible;background:#fff;border:0}'
         '.%(p)s-t th,.%(p)s-t td{padding:8px 10px;font-size:15px;line-height:1.5;vertical-align:top;border-bottom:1px solid #D3DCE2;text-align:right;color:#12202A}'
         '.%(p)s-t thead th{background:#12202A;color:#fff;font-weight:600;font-size:14px}'
         '.%(p)s-t tbody th{font-weight:600;color:#12202A;background:#F6F8F9;position:sticky;right:0;z-index:1}'
         '.%(p)s-num td{white-space:nowrap;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:14px}'
         '.%(p)s-cap{font-weight:700;color:#12202A;font-size:15px;line-height:1.5;margin:22px 0 8px}'
         '.%(p)s-fig{margin:22px 0}.%(p)s-fig figcaption{font-size:14px;color:#3E4C58;margin-top:6px;line-height:1.6}'
         '.%(p)s-note{font-size:15px;line-height:1.7;color:#3E4C58}'
         '.%(p)s-lead{font-size:19px;line-height:1.75;color:#12202A;border-inline-start:4px solid #1F4B5C;padding-inline-start:14px;margin:12px 0 6px}'
         '.%(p)s-cta{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 8px}'
         '.%(p)s-cta a{display:inline-block;padding:12px 18px;border-radius:6px;font-weight:600;font-size:16px;line-height:1.3;text-decoration:none!important;border:1.5px solid #1F4B5C;color:#1F4B5C!important;background:#fff}'
         '.%(p)s-cta a:visited{color:#1F4B5C!important}.%(p)s-cta a.%(p)s-go,.%(p)s-cta a.%(p)s-go:visited,.%(p)s-cta a.%(p)s-go:hover{background:#1F4B5C;color:#fff!important}'
         # 26.10.2026 live: on the guide template the skin's "body.nl-skin-a .nadlan-guide a" (0,2,2, !important) beat the two rules above
         'html body .%(p)s-cta a[href]{color:#1F4B5C!important}html body .%(p)s-cta a.%(p)s-go{color:#fff!important}'
         '.%(p)s-legal{font-size:13px;line-height:1.6;color:#5E6A75;margin:4px 0 14px}'
         '.%(p)s-tool{scroll-margin-top:96px;margin:18px 0 26px}'
         '.%(p)s-box{border:1px solid #D3DCE2;border-inline-start:4px solid #2F6F86;background:#F6F8F9;padding:12px 16px;margin:16px 0;font-size:16px;line-height:1.7;color:#12202A}'
         '.%(p)s-box.is-red{border-inline-start-color:#C42550}'
         '.%(p)s-en{direction:ltr;text-align:left;border-top:3px solid #12202A;padding-top:6px}.%(p)s-en .%(p)s-t th,.%(p)s-en .%(p)s-t td{text-align:left}'
         '.%(p)s-en .%(p)s-t tbody th{right:auto;left:0}'
         '@media(max-width:600px){.%(p)s-t th,.%(p)s-t td{font-size:14px;padding:7px 8px}.%(p)s-cta a{flex:1 1 100%%;text-align:center}.%(p)s-lead{font-size:18px}'
         '.%(p)s-fig svg{margin-left:calc(50%% - 50vw + 6px);margin-right:calc(50%% - 50vw + 6px);width:calc(100vw - 12px)!important;max-width:none!important}}') % {"p": p}
    if guide:
        s += ('.nadlan-guide .nli p,.nadlan-guide .nli li,.nadlan-guide .nli dt,.nadlan-guide .nli dd{margin:0}'
              '.nadlan-guide .nli .nli__lede{font-size:16px;line-height:26px;margin:0 0 16px}.nadlan-guide .nli .nli__note{font-size:14px;line-height:22px}'
              '.nadlan-guide .nli .nli__formula,.nadlan-guide .nli .nli__src,.nadlan-guide .nli .nli__eg{font-size:13px;line-height:20px;margin-top:12px}'
              '.nadlan-guide .nli .nli__kicker{font-size:13px;line-height:18px;margin:0 0 4px}'
              '.nadlan-guide .nli table{box-shadow:none;border-radius:0;overflow:visible;background:none;border:0;margin:8px 0 0}'
              '.nadlan-guide .nli th{background:none;color:#5E6A75}'
              '.nadlan-guide .%(p)s-t th,.nadlan-guide .%(p)s-t td{font-size:15px;padding:8px 10px}.nadlan-guide .%(p)s-t thead th{background:#12202A;color:#fff}'
              '.nadlan-guide .%(p)s-t tbody th{background:#F6F8F9;color:#12202A}.nadlan-guide p.%(p)s-cap,.nadlan-guide p.%(p)s-note{font-size:15px}'
              '.nadlan-guide p.%(p)s-legal{font-size:13px;margin:4px 0 14px}.nadlan-guide p.%(p)s-lead{font-size:19px}'
              '@media(max-width:760px){.nadlan-guide .%(p)s-t th,.nadlan-guide .%(p)s-t td{font-size:14px;padding:7px 8px}}') % {"p": p}
    return s + "</style>\n"


def reform_css(p):
    """Style-only reform of the old .nadlan-guide palette (gold eyebrow, cream notice): applied only with --style (Ben's word)."""
    return ('<style id="%(p)s-reform">.nadlan-guide .eyebrow{background:#fff!important;border:1px solid #D3DCE2!important;color:#1F4B5C!important}'
            '.nadlan-guide .notice,.nadlan-guide .note{background:#F6F8F9!important;border:1px solid #D3DCE2!important;border-inline-start:4px solid #2F6F86!important;color:#12202A!important}</style>\n') % {"p": p}


def fig(p, svg, cap): return '<figure class="%s-fig">%s<figcaption>%s</figcaption></figure>\n' % (p, svg, cap)


def faq(items): return "".join("<h3>%s</h3>\n<p>%s</p>\n" % (q, a) for q, a in items)


def visible(html):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"\[nadlan_[a-z_]+[^\]]*\]", " ", h)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)) + " " + " ".join(re.findall(r'aria-label="([^"]*)"', html))


# the language law (skills/language-dna): "המערכת" / "הפלטפורמה" as our product are banned; the law's own "מערכות צנרת" is not
BANNED_NEW = r"ממשק|המערכת|מערכת שלנו|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה(?! תכנונית)|טעון אימות|נדל[״\"]?ן חכם|Nadlan|nadlan(?!\.gov)|מודל|מנגנון|שכבה|שכבות|הדגמה|טכנולוגי|יחסית|כמעט|אטלס|Atlas|פיילוט|פרוטוטייפ|רספונסיבי|מובייל|לחצו|לחיצה|הקליקו"
BANNED_PAGE = r"ממשק|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|טעון אימות|נדל[״\"]?ן חכם|Nadlan"


def gates(new_html, page_html, faq_n_want, h1_in_content=True):
    nv, pv = visible(new_html), visible(page_html)
    assert not re.search(r"[–—]", nv), "long dash in the new copy: " + str(re.findall(r".{20}[–—].{20}", nv)[:3])
    hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_NEW, nv); assert not hits, ("language law, new copy", hits[:5])
    hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_PAGE, pv); assert not hits, ("language law, whole page", hits[:5])
    assert not re.search(r"(?<![\d.,])0 (₪|חדרים|חודשים|ערים|דירות|ימים)|₪0(?![\d.,])", nv), "a zero number on visible text"
    assert new_html.count("<h1") == 0, "the new copy adds an h1"
    for sv in re.findall(r"<svg\b.*?</svg>", new_html, flags=re.S):
        assert min(float(x) for x in re.findall(r"font-size:([\d.]+)px", sv)) >= 12 and 'viewBox="0 0 420 ' in sv and 'aria-label="' in sv, "svg rules"
    fs = re.search(r"<h2[^>]*>\s*(?:שאלות נפוצות|Frequently asked questions)[^<]{0,60}</h2>(.*?)(?=<h2|$)", re.sub(r"<!--.*?-->", "", page_html, flags=re.S), flags=re.S)
    assert fs, "no FAQ section (h2 שאלות נפוצות)"
    qs = [re.sub(r"<[^>]+>", "", q).strip() for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", fs.group(1), flags=re.S)]
    assert len(qs) == faq_n_want and len(set(qs)) == len(qs), ("FAQ count", len(qs), faq_n_want, len(set(qs)))
    assert all(q.endswith("?") for q in qs), ("every FAQ entry is a question", [q for q in qs if not q.endswith("?")][:3])
    return qs


class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


OP = urllib.request.build_opener(NoRedir)


def status(u):
    try: return OP.open(urllib.request.Request(u, headers=UA), timeout=60).status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return type(e).__name__


def check_links(html, skip_external=False):
    hrefs = sorted(set(re.findall(r'href="([^"#][^"]*)"', html)))
    inner = [h for h in hrefs if h.startswith("/") or h.startswith(SITE)]
    bad = []
    for h in inner:
        st = status(h if h.startswith("http") else SITE + urllib.parse.quote(h, safe="/:?=&%"))
        if st != 200: bad.append((h, st))
        time.sleep(0.15)
    offi = [] if skip_external else [(h, status(h)) for h in hrefs if h.startswith("http") and not h.startswith(SITE) and "wa.me" not in h]
    return inner, bad, offi


def get_live(pid, dry):
    """dry: the public REST (rendered content, no login); otherwise the raw content via the owner's authorized runner."""
    if dry:
        r = json.loads(urllib.request.urlopen(urllib.request.Request(SITE + "/wp-json/wp/v2/pages/%d?_fields=content,link,modified,title" % pid, headers=UA), timeout=90).read().decode("utf-8"))
        return None, r["content"]["rendered"], r
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "g6g8page"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
    req = ns["req"]
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,modified,meta,title" % pid)
    return req, r["content"]["raw"], r


def apply(raw, R):
    """R: list of (anchor, replacement). Every anchor must match exactly once in the live content (raw or rendered)."""
    new = raw
    for o, n in R:
        c = new.count(o)
        assert c == 1, ("anchor must match once", c, o[:120])
        new = new.replace(o, n)
    return new


def before_block(html, text):
    """The start of the block that holds `text` (a heading or paragraph text that is the same in raw and rendered content): the
    nearest opening <h2|h3|p|div|section> before it, and the block comment (<!-- wp:... -->) right before that when there is one.
    Returns the exact substring from that start to the end of `text`, so it can be used as a unique anchor in apply()."""
    i = html.find(text); assert i > -1 and html.count(text) == 1, ("block text must be unique", html.count(text), text[:80])
    j = max(html.rfind(t, 0, i) for t in ("<h2", "<h3", "<p", "<div", "<section"))
    k = html.rfind("<!--", 0, j)
    if k > -1 and html[k:j].strip().endswith("-->") and html[html.find("-->", k) + 3:j].strip() == "" and not html[k:j].startswith("<!-- /"):
        j = k
    return html[j:i + len(text)]


def render_shell(path, title, h1, content, tool_ids, extra_head=""):
    """A local render: the H1 and the content in a 760px column with the engine and the tools from the local files, mounted as the
    shortcode does (the host section with kicker and title; the engine replaces it)."""
    A = "../../../../../plugins/nadlan-config/assets/instruments/"
    data = {"bedek": ["bedek.json"], "shamai": ["shamai.json"], "shamaireg": ["shamai.json"], "orechdin": ["orechdin.json", "ptax.json"]}
    files = {"bedek": "bedek", "shamai": "shamai", "shamaireg": "shamai", "orechdin": "orechdin"}
    names = {"bedek": ("מחשבון · בדק בית", "בדק בית: עד מתי הקבלן אחראי, מתי לבדוק וכמה זה עולה"),
             "shamai": ("מחשבון · שמאי מקרקעין", "איזה שמאי אתם צריכים, מי משלם, מה המועד וכמה זה עולה"),
             "shamaireg": ("חיפוש · פנקס שמאי המקרקעין", "האם השמאי רשום בפנקס? חיפוש לפי שם או מספר רישיון"),
             "orechdin": ("מחשבון · עורך דין מקרקעין", "עורך דין מקרקעין: כמה זה עולה, מה מותר לקבלן לגבות ומה המועדים")}
    for tid in tool_ids:
        k, n = names[tid]
        host = ('<section class="nli" dir="rtl" lang="he" aria-label="%s"><div class="nli-host" data-nli="%s" data-nli-data="%s"><div class="nli__panel"><p class="nli__kicker">%s</p><h2 class="nli__title">%s</h2></div></div></section>'
                % (n, tid, ",".join(A + "data/" + f + "?ver=local" for f in data[tid]), k, n))
        content = content.replace('[nadlan_tool id="%s"]' % tid, host)
    scripts = sorted(set(files[t] for t in tool_ids))
    shell = ('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,">'
             '<title>%s · תצוגה מקומית</title>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800;900&family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
             '<link rel="stylesheet" href="%score.css?ver=local"><style>html,body{margin:0;background:#fff;color:#12202A;font:400 17px/1.75 "IBM Plex Sans Hebrew",Heebo,sans-serif;overflow-x:hidden}'
             '.entry-content{padding:0 16px}.entry-content>*:not(.nadlan-guide):not(main){max-width:760px;margin-left:auto;margin-right:auto}h1.pagehead{font:800 30px/1.25 Heebo,sans-serif;margin:24px auto 8px;max-width:760px;padding:0 16px}'
             '.entry-content h2{font:700 24px/1.35 Heebo,sans-serif;margin:34px auto 10px}.entry-content h3{font:700 19px/1.4 Heebo,sans-serif;margin:22px auto 6px}a{color:#1F4B5C}%s</style></head>'
             '<body><main>%s<div class="entry-content">%s</div></main><script src="%score.js?ver=local" defer></script>%s</body></html>'
             % (title, A, extra_head, ('<h1 class="pagehead">%s</h1>' % h1) if h1 else "", content, A, "".join('<script src="%stools/%s.js?ver=local" defer></script>' % (A, f) for f in scripts)))
    io.open(path, "w", encoding="utf-8", newline="").write(shell)


def counts(new):
    words = len(re.findall(r"[\w֐-׿\"'״]+", visible(re.sub(r"<svg\b.*?</svg>", " ", new, flags=re.S))))
    cells = len(re.findall(r"<t[dh][ >]", re.sub(r"<svg\b.*?</svg>", "", new, flags=re.S)))
    figs = len(re.findall(r"\d[\d,.]*", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg)\b.*?</\1>", " ", new, flags=re.S))))
    return {"words": words, "tables": new.count("<table"), "cells": cells, "figures": figs, "svg": new.count("<svg"), "h2": new.count("<h2"), "h3": new.count("<h3")}
