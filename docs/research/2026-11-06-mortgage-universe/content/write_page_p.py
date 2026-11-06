# -*- coding: utf-8 -*-
"""MortgageWorld P (loop round, HAD-675, 6.11.2026 evening): additive content on page 121.
  1. a chapter "מסלולי משכנתא" after what-is-mortgage: every track with its abbreviation, how the rate moves, linkage, the share of
     new mortgages and the average rate (BoI קו המשווה, September 2026, by_bank system row of boi-mortgage.json), and whether a
     capitalization fee applies (Banking Order s.4); track facts from Kol Zchut "מסלולי הלוואה למשכנתא" (2.3.2025);
  2. registration chapter: the ILA commitment per procedure 90.02B (published 8.7.2025): issued with no fee (s.1.10), when ILA
     issues it, its conditions, and its discharge after payoff or porting;
  3. map link (stage 2 now 9); 4. FAQ +5 (40 years, self-build, porting, the ILA commitment, מ״צ and מל״צ).
Nothing removed. python write_page_p.py --dry, then without --dry."""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, H)
from chapters_n import table, L  # noqa: E402
BACK = '<p class="nlmap-back"><a href="#mortgage-map">↑ לכל נושאי המשכנתא</a></p>\n'
KZT = "https://www.kolzchut.org.il/he/%D7%9E%D7%A1%D7%9C%D7%95%D7%9C%D7%99_%D7%94%D7%9C%D7%95%D7%95%D7%90%D7%94_%D7%9C%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90_(%D7%AA%D7%9E%D7%94%D7%99%D7%9C_%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90)"
ILAP = "https://www.gov.il/BlobFolder/policy/9002b-procedure/he/Procedures_90.02b.pdf"
EQ = "https://www.boi.org.il/information/bank-paymnts/financial-education/campaigns/boi-equator/mortgage/"

d = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "boi-mortgage.json"), encoding="utf-8"))
sysr = [r for r in d["by_bank"]["latest"]["table"] if r["bank"] == "system"][0]; month = d["by_bank"]["latest"]["month"]
assert month == "2026-09", month
P = lambda k: "%.1f%%" % sysr[k]["share"]; R = lambda k: "%.2f%%" % sysr[k]["rate"]
ROWS = [
    ["קבועה לא צמודה <small>קל״צ</small>", "קבועה לכל התקופה", "לא צמודה", P("fixed_nl"), R("fixed_nl"), "כן, כשהממוצע ביום הפירעון נמוך מהריבית שלכם"],
    ["פריים", "ריבית בנק ישראל ועוד 1.5%, ומשתנה איתה", "לא צמודה", P("prime"), R("prime"), "לא"],
    ["משתנה לא צמודה <small>מל״צ</small>", "משתנה במועדים שנקבעים בהסכם, למשל כל 5 שנים", "לא צמודה", P("var_nl_other"), R("var_nl_other"), "כן, עד יום שינוי הריבית; ביום השינוי לא"],
    ["משתנה צמודה למדד <small>מ״צ</small>", "משתנה כל שנה, שנתיים, שנתיים וחצי או חמש", "צמודה למדד", P("var_cpi"), R("var_cpi"), "כן, עד יום שינוי הריבית; ביום השינוי לא"],
    ["קבועה צמודה למדד <small>ק״צ</small>", "קבועה לכל התקופה", "צמודה למדד", P("fixed_cpi"), R("fixed_cpi"), "כן, כשהממוצע ביום הפירעון נמוך מהריבית שלכם"],
    ["צמודה למטבע חוץ <small>מט״ח</small>", "משתנה כל 1 עד 12 חודשים", "צמודה לשער החליפין", "לא מפורסם בנפרד", "לא מפורסם בנפרד", "לא, אם הריבית משתנה לפחות פעם בשנה"],
]
TRACKS = ('<section id="mortgage-tracks">\n<h2>מסלולי משכנתא: קל״צ, פריים, מל״צ, מ״צ וק״צ</h2>\n'
  '<p class="nlx-ans">משכנתא בישראל בנויה מכמה מסלולים, וכל מסלול נקבע לפי שתי שאלות: האם הריבית קבועה או משתנה, והאם הקרן צמודה למדד. '
  'בספטמבר 2026 הקבועה הלא צמודה, הקל״צ, הייתה %s מהמשכנתאות החדשות בריבית ממוצעת של %s, והפריים %s בריבית של %s (בנק ישראל, קו המשווה). '
  'לפחות שליש מהמשכנתא חייב להיות בריבית קבועה (הוראה 329).</p>\n' % (P("fixed_nl"), R("fixed_nl"), P("prime"), R("prime"))
  + table("המסלולים, החלק שלהם והריבית הממוצעת, ספטמבר 2026",
          "חלק מהמשכנתאות החדשות וריבית אפקטיבית ממוצעת בכל הבנקים, בנק ישראל, קו המשווה. עמלת היוון לפי צו הבנקאות (פירעון מוקדם), סעיף 4. התקופות והתדירות לפי כל־זכות, 2.3.2025.",
          ["מסלול", "הריבית", "הצמדה", "חלק מהמשכנתאות", "ריבית ממוצעת", "עמלת היוון בפירעון מוקדם"], ROWS, numcols=[3, 4])
  + '<ul>\n<li><b>ודאות מול מחיר:</b> בקבועה יודעים מראש את הריבית, ובדרך כלל משלמים עליה יותר; במשתנה ובפריים ההחזר זז עם הריבית במשק.</li>\n'
  '<li><b>הצמדה:</b> במסלול צמוד הקרן וההחזר עולים עם מדד המחירים לצרכן; בלא צמוד הקרן לא זזה.</li>\n'
  '<li><b>יציאה:</b> בפריים ובמשתנה ביום שינוי הריבית אפשר לפרוע בלי עמלת היוון, ובמסלולים הקבועים העמלה תלויה בריבית הממוצעת ביום הפירעון.</li>\n'
  '<li><b>מטבע חוץ:</b> ההלוואה ניתנת בשקלים וצמודה לשער החליפין, ולכן ההחזר זז גם עם שער המטבע.</li>\n</ul>\n'
  '<p>התמהיל שלכם על המסלולים האלה: <a href="#mortgage-tool">המחשבון המלא לפי מסלולים</a>. ההסבר המלא על כל מסלול: ' + L(KZT, "מסלולי הלוואה למשכנתא (כל־זכות)") +
  ' · ' + L(EQ, "קו המשווה של בנק ישראל") + '.</p>\n' + BACK + '</section>\n')

ILA = ('<p><b>התחייבות לרישום משכנתא ברשות מקרקעי ישראל:</b> כשהדירה מנוהלת ברשות ולא בחברה משכנת או קבלנית, ולא רשומה בטאבו, הרשות '
  'מנפיקה "כתב התחייבות לרישום משכנתא": היא לא תרשום את הזכויות בטאבו בלי המשכנתא לטובת הבנק, ולא תאשר העברת זכויות בלי הסכמתו. '
  'הכתב ניתן ללא תשלום אגרה (נוהל 90.02B, סעיף 1.10), בתנאי שיש הסכם חכירה בתוקף, אין עיקול, משכון או הערה מגבילה, ואין חוב לרשות. '
  'מגישים באזור האישי "רמ״י שלי", וכל בעלי הזכויות חותמים. אחרי פירעון ההלוואה, או גרירתה לנכס אחר, מסלקים את ההתחייבות עם מסמך '
  'סילוק חתום מהבנק. כשהדירה מנוהלת בחברה משכנת, ההתחייבות מתבקשת מהחברה. ' + L(ILAP, "נוהל 90.02B, פורסם 8.7.2025") + '.</p>\n')

FAQ = [
    ("אפשר לקחת משכנתא ל־40 שנה?",
     'לא בבנק בישראל. לפי הוראה 329 של בנק ישראל, תקופת הלוואה לדיור היא עד 30 שנה. מי שרוצה החזר נמוך יותר מאריך עד 30 שנה, ומשלם על כך יותר ריבית לאורך כל התקופה.'),
    ("מה זה משכנתא לבנייה עצמית?",
     'הלוואה לבניית בית על קרקע שלכם. הכסף ניתן בשלבים לפי קצב התקדמות הבנייה, ובהלוואת זכאות מתחילים לממש תוך 36 חודשים מהיתר הבנייה. '
     'לפי הפיקוח על הבנקים, הלוואה לבנייה של דירת מגורים היא הלוואה לדיור ולא הלוואה לכל מטרה.'),
    ("מה זה גרירת משכנתא?",
     'העברה של המשכנתא הקיימת, באותם תנאים, מהדירה שנמכרת לדירה החדשה, במקום לפרוע אותה ולקחת חדשה. כך אפשר לחסוך עמלת פירעון מוקדם. '
     'הבנק בודק את הדירה החדשה כבטוחה. פירוט: <a href="/mortgage-calculator/mortgage-porting/">גרירת משכנתא</a>.'),
    ("מה זה התחייבות לרישום משכנתא?",
     'כשהדירה עדיין לא רשומה בטאבו, הגוף שמנהל את הזכויות, רשות מקרקעי ישראל או החברה המשכנת, מתחייב לבנק לרשום את המשכנתא כשהדירה תירשם, '
     'ולא להעביר זכויות בלי הסכמתו. ברשות מקרקעי ישראל הכתב ניתן ללא תשלום אגרה (נוהל 90.02B).'),
    ("מה ההבדל בין מ״צ למל״צ?",
     'שניהם מסלולים בריבית משתנה. מ״צ, משתנה צמודה, מתעדכנת כל שנה, שנתיים, שנתיים וחצי או חמש שנים והקרן צמודה למדד. מל״צ, משתנה לא צמודה, '
     'לא צמודה למדד. בשניהם ביום שינוי הריבית אפשר לפרוע בלי עמלת היוון.'),
]

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_p"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]; assert 'id="mortgage-tracks"' not in raw, "already written"


def sec_bounds(txt, sid):
    m0 = re.search(r'<section\b[^>]*\bid="%s"' % re.escape(sid), txt); i = m0.start(); depth = 0
    for m in re.finditer(r'<section\b|</section>', txt[i:]):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return i, i + m.start(), i + m.end()


def one(txt, a, b):
    assert txt.count(a) == 1, ("anchor", a[:70], txt.count(a)); return txt.replace(a, b)


new = raw
i, c, e = sec_bounds(new, "what-is-mortgage"); new = new[:e] + "\n" + TRACKS + new[e:].lstrip("\n")
i, c, e = sec_bounds(new, "mortgage-registration"); k = new.rfind('<p class="nlmap-back">', i, c); new = new[:k] + ILA + new[k:]
new = one(new, '<li><a href="#uniform-baskets">שלושת הסלים האחידים</a></li>',
          '<li><a href="#uniform-baskets">שלושת הסלים האחידים</a></li><li><a href="#mortgage-tracks">מסלולי משכנתא: קל״צ, פריים, מ״צ</a></li>')
new = one(new, '<span>2 · בבנק</span><small>8</small>', '<span>2 · בבנק</span><small>9</small>')
i, c, e = sec_bounds(new, "faq"); new = new[:c] + "".join("<h3>%s</h3>\n<p>%s</p>\n" % qa for qa in FAQ) + new[c:]
vis = re.sub(r"<[^>]+>", " ", TRACKS + ILA + "".join(q + a for q, a in FAQ))
assert not re.search(r"[–—]", vis), "long dash"
for bad in ("סימולציה", "ממשק", "דמו", "המערכת", "הפלטפורמה", "עולם המשכנתא"):
    assert not re.search(r"(?<![֐-׿])%s(?![֐-׿])" % bad, vis), bad
for line in raw.split("\n"):
    if line.strip() and line not in new:
        assert ('<span>2 · בבנק</span><small>8</small>' in line or 'שלושת הסלים האחידים</a></li>' in line), ("missing", line[:80])
print("[page 121] round P; content %d -> %d bytes; FAQ +%d; shares fixed_nl %s prime %s" % (len(raw), len(new), len(FAQ), P("fixed_nl"), P("prime")))
if DRY:
    io.open(os.path.join(H, "preview-content-p.html"), "w", encoding="utf-8", newline="").write(new); print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live:", 'id="mortgage-tracks"' in page, page.count('"@type":"Question"'), "questions", "90.02B" in page)
