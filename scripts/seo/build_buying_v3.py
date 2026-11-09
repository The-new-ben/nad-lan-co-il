# -*- coding: utf-8 -*-
"""HAD-686: assemble page 9 v3 (/buying-apartment/) from the LIVE content and the writers' chapter fragments. Local only.
  python scripts/seo/build_buying_v3.py            -> docs/research/2026-11-08-buying-guide-re/page-9-v3.html
Every live section is kept (some move to their chapter, some H2s become H3 inside a chapter), every live link stays, the H1,
the answer paragraph, the buttons and the first five tools stay where they are. The guide map comes right before chapter 1."""
import html, io, json, os, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = os.path.join(REPO, "docs", "research", "2026-11-08-buying-guide-re")
CH = os.path.join(R, "chapters")
LIVE = io.open(os.path.join(R, "page-9-live-2026-11-09.html"), encoding="utf-8").read()
# Fact fixes on live sentences (LEDGER-DECISIONS 1: the advance is 7.5%, or 15% when the seller bought up to 6.11.2001). Additive only.
FIXES = [
    ("אחרי שעברתם 40% מהמחיר, 7.5% מהמחיר עוברים לרשות המסים, אלא אם",
     "אחרי שעברתם 40% מהמחיר, 7.5% מהמחיר עוברים לרשות המסים (15% כשהמוכר קנה את הדירה עד 6.11.2001), אלא אם"),
    ("אחרי שעברו 40% מהמחיר: 7.5% מהמחיר לרשות המסים</td>",
     "אחרי שעברו 40% מהמחיר: 7.5% מהמחיר לרשות המסים (15% כשהמוכר קנה עד 6.11.2001)</td>"),
    ("מקדמה של 7.5% מהמחיר אחרי שעברו 40% מהמחיר,",
     "מקדמה של 7.5% מהמחיר (15% כשהמוכר קנה את הדירה עד 6.11.2001) אחרי שעברו 40% מהמחיר,"),
    ("<p class=\"nlbp-eyebrow\">מדריך קניית דירה · עודכן 8.11.2026</p>", "<p class=\"nlbp-eyebrow\">מדריך קניית דירה · עודכן 9.11.2026</p>"),
    # deep-link ids on four live FAQ questions (chapter 18 and the new FAQ link to them); attributes only, no text change
    ("<h3>קניית דירה מכונס נכסים: על מה שמים לב?</h3>", '<h3 id="faq-kones">קניית דירה מכונס נכסים: על מה שמים לב?</h3>'),
    ("<h3>קניית דירה עם שותפים או על שם הילד: מה צריך לדעת?</h3>", '<h3 id="faq-partners">קניית דירה עם שותפים או על שם הילד: מה צריך לדעת?</h3>'),
    ("<h3>ההורים עוזרים: מתנה או הלוואה, ומה עם האחים?</h3>", '<h3 id="faq-parents">ההורים עוזרים: מתנה או הלוואה, ומה עם האחים?</h3>'),
    ("<h3>קונים לפני החתונה: על שם מי רושמים?</h3>", '<h3 id="faq-wedding">קונים לפני החתונה: על שם מי רושמים?</h3>'),
]
for _a, _b in FIXES:
    assert LIVE.count(_a) == 1, ("fix anchor not once", _a)
    LIVE = LIVE.replace(_a, _b)
TOOL_H = "3"  # tools inside a chapter render their title as h3 (buying-hub.php supports h="3")
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "col"}

PHASES = [("לפני שקונים", [1, 2, 3, 4]), ("לפני החתימה", [5, 6, 7, 8]), ("החתימה", [9, 10, 11, 12]),
          ("אחרי החתימה עד המפתח", [13, 14, 15, 16]), ("מסלולים נוספים", [17, 18])]
SHORT = {1: "תקציב ומחיר נוח", 2: "מימון ואישור עקרוני", 3: "עיר, שכונה ומחיר", 4: "ביקור ובדיקה פיזית", 5: "נסח וזכויות",
         6: "המוכר ומי שגר בדירה", 7: "בית משותף ותכנון", 8: "המסים בעסקה", 9: "זיכרון דברים ומשא ומתן", 10: "החוזה וההגנות",
         11: "לוח התשלומים", 12: "יום החתימה", 13: "הערת אזהרה", 14: "דיווח, אישורים ומשכנתאות", 15: "המסירה",
         16: "הרישום על שמכם", 17: "קנייה מקבלן", 18: "מקרים מיוחדים"}
TOTAL = 18

def phase_of(n):
    for name, ns in PHASES:
        if n in ns: return name

# ---------- live sections ----------
H2 = [(m.start(), " ".join(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split())) for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", LIVE, re.S)]
def sec(title_start):
    for i, (pos, tt) in enumerate(H2):
        if tt.startswith(title_start):
            end = H2[i + 1][0] if i + 1 < len(H2) else len(LIVE)
            return pos, end
    raise SystemExit("live section not found: " + title_start)
def take(title_start):
    a, b = sec(title_start); return LIVE[a:b]

FIRST = "לפני שמחפשים"
PREFIX = LIVE[:sec(FIRST)[0]]
S = {k: take(k) for k in ["לפני שמחפשים", "עלות כוללת", "קודם המימון", "סיוע ברכישת דירה ראשונה", "בחירת עיר ושכונה",
                          "איך משווים מחיר", "בדיקת זכויות ומסמכים", "בדיקת מצב הדירה", "יד שנייה, מקבלן", "תפקיד עורך הדין",
                          "קניית דירה: המועדים", "ציר זמן מומלץ", "טעויות נפוצות", "קניית דירה: השאלות", "קנייה טובה",
                          "מדריכים קשורים", "פרויקטים מהקטלוג"]}
# the live sections must cover the page from FIRST to the end with nothing left over
_cover = sum(len(v) for v in S.values())
assert _cover == len(LIVE) - len(PREFIX), ("live sections do not cover the page", _cover, len(LIVE) - len(PREFIX))

def demote(block):
    return re.sub(r"<h2([^>]*)>(.*?)</h2>", r"<h3\1>\2</h3>", block, count=1, flags=re.S)
def cut_tool(block, tid):
    sc = '[nadlan_tool id="%s"]' % tid
    assert block.count(sc) == 1, ("tool not once", tid)
    return block.replace(sc, ""), sc
def cut_h3(block, h3_start):
    m = None
    for x in re.finditer(r"<h3[^>]*>(.*?)</h3>", block, re.S):
        if " ".join(html.unescape(re.sub(r"<[^>]+>", "", x.group(1))).split()).startswith(h3_start): m = x; break
    assert m, ("h3 not found", h3_start)
    nxt = re.search(r"<h[23][\s>]", block[m.end():])
    end = m.end() + nxt.start() if nxt else len(block)
    return block[:m.start()] + block[end:], block[m.start():end]

# ---------- fragments ----------
def top_level(s):
    """split an HTML string into its top-level elements (comments and text kept as their own items)"""
    out, i, depth, start = [], 0, 0, 0
    tagre = re.compile(r"<!--.*?-->|<(/?)([a-zA-Z0-9]+)([^>]*)>", re.S)
    for m in tagre.finditer(s):
        if m.group(0).startswith("<!--"):
            if depth == 0:
                if s[start:m.start()].strip(): out.append(s[start:m.start()])
                out.append(m.group(0)); start = m.end()
            continue
        close, tag, rest = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or rest.endswith("/"): continue
        if not close:
            if depth == 0:
                if s[start:m.start()].strip(): out.append(s[start:m.start()])
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append(s[start:m.end()]); start = m.end()
    if s[start:].strip(): out.append(s[start:])
    return [x.strip() for x in out if x.strip()]

def inner(el):
    return re.sub(r"^<[^>]+>", "", re.sub(r"</[a-zA-Z]+>\s*$", "", el.strip()))

LIVE_MARK = "%%LIVE%%"

def conv(el):
    """a writer's comment becomes a tool shortcode, a live-content marker, or nothing"""
    m = re.match(r"<!--\s*TOOL\s+(\w+).*?-->$", el, re.S)
    if m: return '[nadlan_tool id="%s" h="%s"]' % (m.group(1), TOOL_H)
    if re.match(r"<!--\s*(LIVE|MOVE HERE|EXISTING SECTION)", el): return LIVE_MARK
    if el.startswith("<!--"): return None
    return re.sub(r"<!--\s*TOOL\s+(\w+).*?-->", lambda m: '[nadlan_tool id="%s" h="%s"]' % (m.group(1), TOOL_H), el, flags=re.S)

def frag(n):
    """the writer's material for chapter n: head parts (h2, ans, who, todo), the body of the first block, and the later
    nlbg-add blocks (placed into the live text by PLACES)"""
    p = os.path.join(CH, "c%d.html" % n)
    if not os.path.exists(p): return None
    t = io.open(p, encoding="utf-8").read()
    blocks = []
    for el in top_level(t):
        if re.match(r'<(section|div)[^>]*class="(nlbg-ch|nlbg-add)', el): blocks.append(top_level(inner(el)))
        elif not el.startswith("<!--"): blocks.append([el])
    head = {"h2": None, "ans": None, "who": None, "todo": None}; outb = []
    for bl in blocks:
        cur = []
        for el in bl:
            if el.startswith('<p class="nlbg-kick"') or el.startswith('<p class="nlbg-back"'): continue
            if el.startswith("<h2") and head["h2"] is None: head["h2"] = el; continue
            if el.startswith('<p class="nlbg-ans"') and head["ans"] is None: head["ans"] = el; continue
            if el.startswith('<div class="nlbg-who"') and head["who"] is None: head["who"] = el; continue
            if el.startswith('<div class="nlbg-todo"') and head["todo"] is None: head["todo"] = el; continue
            if el.startswith("<h2"): el = demote(el)
            c = conv(el)
            if c: cur.append(c)
        outb.append(cur)
    return head, outb[0] if outb else [], outb[1:]

def place(parts, block_html, part_i, anchor, mode):
    """put block_html into live part part_i: before the anchor, before the <p> that precedes the anchor, before the first
    nlbp-go row after the anchor, or at the end of the part"""
    s = parts[part_i]
    if mode == "end": parts[part_i] = s.rstrip() + "\n" + block_html + "\n"; return
    assert s.count(anchor) == 1, ("anchor not once", anchor, s.count(anchor))
    i = s.index(anchor)
    if mode == "before_prev_p": i = s.rfind("<p", 0, i)
    elif mode == "before_go_after": i = s.index('<p class="nlbp-go"', i)
    parts[part_i] = s[:i] + block_html + "\n" + s[i:]

def chapter(n, live_h2=None, live_parts=(), places=()):
    f = frag(n)
    if f is None and live_h2 is None and os.environ.get("DRAFT"):
        f = ({"h2": "<h2>%s</h2>" % SHORT[n], "ans": None, "who": None, "todo": None}, [], [])  # draft placeholder only
    head, body, extra = f if f else ({"h2": None, "ans": None, "who": None, "todo": None}, [], [])
    parts = [x for x in live_parts]
    # tools that arrive with the live text and also as a writer's marker appear once
    for i, x in enumerate(parts):
        for tid in re.findall(r'\[nadlan_tool id="(\w+)"\]', x):
            if any('[nadlan_tool id="%s" h=' % tid in b for b in body):
                bare = re.fullmatch(r'\s*(?:<span id="[\w-]+" class="nlbp-anchor"></span>\s*)?\[nadlan_tool id="%s"\]\s*' % tid, x)
                unit = x.strip().replace('[nadlan_tool id="%s"]' % tid, '[nadlan_tool id="%s" h="%s"]' % (tid, TOOL_H))
                if bare:  # the writer placed this live tool: the tool and its anchor go to the marker
                    body = [re.sub(r'\[nadlan_tool id="%s" h="%s"\]' % (tid, TOOL_H), lambda _m: unit, b) for b in body]
                    parts[i] = ""
                else:     # the live paragraph carries the tool: keep it there and drop the marker
                    body = [b for b in body if b != '[nadlan_tool id="%s" h="%s"]' % (tid, TOOL_H)]
                    parts[i] = unit
    # later nlbg-add blocks go to their places inside the live text
    for bi, pi, anchor, mode in places:
        assert bi < len(extra), ("chapter %d has no add block %d" % (n, bi))
        place(parts, "\n".join(extra[bi]), pi, anchor, mode)
    for bi in range(len(extra)):
        if bi not in [p[0] for p in places]: body += extra[bi]
    out = ['<section class="nlbg-ch" id="nlbg-c%d" data-ch="c%d">' % (n, n),
           '<p class="nlbg-kick">שלב %d מתוך %d · %s</p>' % (n, TOTAL, phase_of(n))]
    if live_h2 is not None: out.append(live_h2.strip())
    else:
        assert head["h2"], "chapter %d has no h2" % n
        out.append(head["h2"])
    for k in ("ans", "who", "todo"):
        if head[k]: out.append(head[k])
    parts = [x.strip() for x in parts if x.strip()]
    marks = [i for i, b in enumerate(body) if b == LIVE_MARK]
    if marks:
        for j, i in enumerate(marks):
            body[i] = "\n".join(parts[j:j + 1] if j < len(marks) - 1 else parts[j:])
        out += [b for b in body if b]
    else:
        out += parts + body
    out.append('<p class="nlbg-back"><a href="#nlbg-map">חזרה למפת המדריך</a></p>')
    out.append("</section>")
    # every tool inside a chapter titles itself h3 (the chapter owns the h2); id stays first in the shortcode
    return re.sub(r'\[nadlan_tool id="(\w+)"\]', r'[nadlan_tool id="\1" h="%s"]' % TOOL_H, "\n".join(out))

def split_h2(block):
    m = re.match(r"\s*(<h2[^>]*>.*?</h2>)(.*)", block, re.S); assert m, block[:80]
    return m.group(1), m.group(2)

# ---------- the chapters ----------
c1_h2, c1_rest = split_h2(S["לפני שמחפשים"])
c2_h2, c2_rest = split_h2(S["קודם המימון"])
c3_h2, c3_rest = split_h2(S["בחירת עיר ושכונה"])
_VISIT_P = c3_rest[c3_rest.index("<p>לכל דירה שרואים פותחים דף ביקור"):c3_rest.index('[nadlan_tool id="bvisit"]') + len('[nadlan_tool id="bvisit"]')]
c3_rest, sc_bvisit = c3_rest.replace(_VISIT_P, ""), _VISIT_P  # the visit paragraph, its #visit anchor and the tool move to chapter 4
c5_h2, c5_rest = split_h2(S["בדיקת זכויות ומסמכים"])
cond, h3_dev = cut_h3(S["בדיקת מצב הדירה"], "קניית דירה עם חריגות בנייה")
_WHO = '<span id="who-pays" class="nlbp-anchor"></span>\n[nadlan_tool id="bwho"]'
assert S["תפקיד עורך הדין"].count(_WHO) == 1, "who-pays anchor + bwho"
lawyer, sc_bwho = S["תפקיד עורך הדין"].replace(_WHO, ""), _WHO  # the anchor moves with the table (the FAQ links #who-pays)

CHS = [
    chapter(1, c1_h2, [c1_rest, demote(S["עלות כוללת"]), demote(S["סיוע ברכישת דירה ראשונה"])],
            [(0, 0, "<p>המדריך הזה מסדר", "before"), (1, 1, "<p>לפני שמתקדמים להצעה", "before"), (2, 2, "", "end")]),
    chapter(2, c2_h2, [c2_rest], [(0, 0, '<span id="before-sale"', "before_prev_p")]),
    chapter(3, c3_h2, [c3_rest, demote(S["איך משווים מחיר"])],
            [(0, 0, "<p>מבקרים באזור יותר מפעם אחת", "before_go_after"), (1, 1, "<h3>איך משווים מחיר", "before_go_after")]),
    chapter(4, None, [sc_bvisit, demote(cond)]),
    chapter(5, c5_h2, [c5_rest], [(0, 0, "<h3>קניית דירה שלא רשומה", "before"), (1, 0, "<h3>קניית דירה שלא רשומה", "before_go_after")]),
    chapter(6),
    chapter(7, None, [h3_dev]),
    chapter(8, None, [sc_bwho]),
    chapter(9),
    chapter(10, None, [demote(lawyer)]),
    chapter(11),
    chapter(12),
    chapter(13),
    chapter(14, None, [demote(S["קניית דירה: המועדים"])]),
    chapter(15),
    chapter(16),
    chapter(17, None, [demote(S["יד שנייה, מקבלן"])]),
    chapter(18),
]

# ---------- the guide map ----------
MAP = ['<nav class="nlbg-map" id="nlbg-map" aria-label="מפת המדריך">', "<h2>מפת המדריך: %d שלבים מהתקציב ועד הנסח על שמכם</h2>" % TOTAL,
       '<p class="nlbg-map__lede">השלבים לפי הסדר שבו עסקה אמיתית קורית. כל שלב נפתח בתשובה קצרה, ואחריה הפירוט, הכלים והמקורות הרשמיים.</p>',
       '<div class="nlbg-map__phases">']
for name, ns in PHASES:
    MAP.append('<div class="nlbg-map__phase"><h3>%s</h3><ol class="nlbg-map__chips">' % name)
    for n in ns:
        MAP.append('<li><a href="#nlbg-c%d" data-ch="c%d"><b>%d</b>%s</a></li>' % (n, n, n, SHORT[n]))
    MAP.append("</ol></div>")
MAP += ["</div>", "</nav>"]

# ---------- FAQ, glossary, sources ----------
faq = S["קניית דירה: השאלות"]
fa = os.path.join(CH, "faq-add.html")
if os.path.exists(fa):
    add = re.sub(r"<!--.*?-->", "", io.open(fa, encoding="utf-8").read(), flags=re.S).strip()
    faq = faq.rstrip() + "\n" + add + "\n"
gl = os.path.join(CH, "glossary.html")
GLOSS = ""
if os.path.exists(gl):
    g = re.sub(r"<!--.*?-->", "", io.open(gl, encoding="utf-8").read(), flags=re.S).strip()
    if "<h2" not in g: g = '<h2 id="nlbg-gloss-h">מילון המונחים לקונה</h2>\n' + g
    GLOSS = '<section class="nlbg-glossary" id="nlbg-glossary">\n' + g + "\n</section>"
def build_sources(htm):
    """every official source line on the page (link, name, reading date), grouped by the body that publishes it"""
    rows = {}
    for blk in re.findall(r'<p class="nlbg-src">(.*?)</p>', htm, re.S):
        dm = re.search(r"נבדק\s*([\d\.]+)", blk); d = dm.group(1).rstrip(".") if dm else ""
        for u, a in re.findall(r'<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', blk, re.S):
            name = " ".join(html.unescape(re.sub(r"<[^>]+>", "", a)).split())
            if u not in rows: rows[u] = (name, d)
    def body(u):
        if "kolzchut" in u: return "כל זכות"
        if "boi.org.il" in u or "boi.gov.il" in u: return "בנק ישראל"
        if "cbs.gov.il" in u: return "הלשכה המרכזית לסטטיסטיקה"
        if "wikisource" in u or "knesset" in u or "nevo" in u: return "נוסח החוק"
        if "iec.co.il" in u: return "חברת החשמל"
        if "israelbar" in u: return "לשכת עורכי הדין"
        if "land.gov.il" in u or "rmi" in u.lower(): return "רשות מקרקעי ישראל"
        if "gov.il" in u or "masmak" in u: return "gov.il (משרדי הממשלה ורשויות המדינה)"
        return "מקור רשמי אחר"
    order = ["gov.il (משרדי הממשלה ורשויות המדינה)", "רשות מקרקעי ישראל", "בנק ישראל", "הלשכה המרכזית לסטטיסטיקה", "נוסח החוק",
             "כל זכות", "לשכת עורכי הדין", "חברת החשמל", "מקור רשמי אחר"]
    items = sorted(rows.items(), key=lambda kv: (order.index(body(kv[0])), kv[1][0]))
    out = ['<section class="nlbg-sources" id="nlbg-sources">', "<h2>המקורות הרשמיים של המדריך</h2>",
           "<p>כל מספר וכל כלל במדריך נשען על מקור רשמי: אתרי הממשלה, בנק ישראל, הלשכה המרכזית לסטטיסטיקה, נוסח החוק עצמו ואתר כל זכות. "
           "ליד כל מקור מופיע התאריך שבו נקרא. אגרות, מדרגות מס ושיעורי ריבית מתעדכנים, ולכן לפני תשלום בודקים את המספר במקור עצמו. "
           "בטבלה %d מקורות.</p>" % len(items),
           '<div class="nlbg-tw"><table class="nlbg-tbl"><thead><tr><th>הגוף</th><th>המקור</th><th>נקרא</th></tr></thead><tbody>']
    for u, (name, d) in items:
        out.append('<tr><td data-l="הגוף">%s</td><td data-l="המקור"><a href="%s" rel="noopener">%s</a></td><td data-l="נקרא">%s</td></tr>'
                   % (body(u), html.escape(u, quote=True), html.escape(name or u), d))
    out += ["</tbody></table></div>", "</section>"]
    return "\n".join(out), len(items)

_body = "\n".join(CHS) + faq + GLOSS
SOURCES, N_SRC = build_sources(_body)
print("sources chapter:", N_SRC, "official pages")
PAGE = "\n".join([PREFIX.rstrip(), "\n".join(MAP), "\n\n".join(CHS), S["ציר זמן מומלץ"].strip(), S["טעויות נפוצות"].strip(), faq.strip(),
                  GLOSS, SOURCES, S["קנייה טובה"].strip(), S["מדריכים קשורים"].strip(), S["פרויקטים מהקטלוג"].strip()]) + "\n"
PAGE = re.sub(r"\n{3,}", "\n\n", PAGE)
out = os.path.join(R, "page-9-v3.html")
io.open(out, "w", encoding="utf-8", newline="\n").write(PAGE)
missing = [n for n in range(1, TOTAL + 1) if not os.path.exists(os.path.join(CH, "c%d.html" % n))]
print("written", out, len(PAGE), "chars; chapters without a fragment:", missing)
