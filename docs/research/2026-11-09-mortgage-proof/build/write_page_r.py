# -*- coding: utf-8 -*-
"""Round R (HAD-675, Ben 9.11.2026): on-page fixes on page 121 (/mortgage-calculator/). Additive: no sentence is removed.
  1. Topic map: the "מדריך" badge sat inside 12 links to child pages, so the anchor text read "ריבית משכנתא היוםמדריך". The badge
     keeps its look (CSS ::after from data-t) and the anchor text becomes the child page's phrase alone.
  2. The Spitzer formula in the notation the AI answers quote (M, P, r, n), with the worked example already on the page (5,627 ₪).
  3. "מה המחשבון בודק": one sentence that lists what the calculators do, in the shape of Google's AI summary for the query.
  4. FAQ: two questions asked the same thing twice. The 40-year pair is merged (both answers kept under the first question);
     the second "בלי הון עצמי" question is re-targeted to "משכנתא הורים" (a real search, keyword ideas 6.11.2026), its answer kept.
  5. The map and the market section link to the new block #million ("כמה עולה משכנתא של מיליון שקל, חודש אחר חודש").
python write_page_r.py --dry, then without --dry (backup first; --undo restores the newest backup)."""
import glob, io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
DRY = "--dry" in sys.argv; UNDO = "--undo" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_r"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
BK = os.path.join(H, "page-backup"); os.makedirs(BK, exist_ok=True)

if UNDO:
    last = sorted(glob.glob(os.path.join(BK, "page-121-*.html")))[-1]
    old = io.open(last, encoding="utf-8", newline="").read()
    s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": old}); assert s2 in (200, 201), s2
    print("restored", os.path.basename(last)); sys.exit(0)

s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link,modified"); assert s == 200, s
raw = r["content"]["raw"]; new = raw
assert 'data-t="מדריך"' not in raw, "already written"


def one(old, rep, what, count=1):
    global new
    n = new.count(old)
    assert n == count, "%s: x%d (want %d)" % (what, n, count)
    new = new.replace(old, rep)


# 1. badge out of the anchor text, same look
nb = new.count('<i class="g">מדריך</i></a>'); assert nb >= 10, nb
one('<i class="g">מדריך</i></a>', '<i class="g" data-t="מדריך"></i></a>', "badges", nb)
one(".nlmap__d li a i.g{background:none;color:#5E6A75;border:1px solid #D3DCE2}",
    ".nlmap__d li a i.g{background:none;color:#5E6A75;border:1px solid #D3DCE2}.nlmap__d li a i.g:empty::after{content:attr(data-t)}", "badge css")

# 2. the formula in the notation AI answers use
SP = ("<p>ההחזר בשפיצר: סכום ההלוואה כפול הריבית החודשית, חלקי אחד פחות (אחד ועוד הריבית החודשית) בחזקת מינוס מספר החודשים. "
      "הריבית החודשית היא הריבית השנתית חלקי 12.</p>\n")
FORM = ('<p>בסימון המקובל: <bdi dir="ltr" class="nlf">M = P × r × (1 + r)<sup>n</sup> ÷ ((1 + r)<sup>n</sup> − 1)</bdi>, כאשר <bdi dir="ltr">P</bdi> הוא סכום '
        'המשכנתא, <bdi dir="ltr">r</bdi> הריבית החודשית ו־<bdi dir="ltr">n</bdi> מספר התשלומים. בדוגמה של 1,000,000 ₪ ל־25 שנה בריבית 4.62%: '
        '<bdi dir="ltr">r = 4.62% ÷ 12 = 0.385%</bdi>, <bdi dir="ltr">n = 25 × 12 = 300</bdi>, ולכן <bdi dir="ltr">M = 5,627</bdi> ₪ בחודש. '
        'ההחזר הראשון בפועל משתנה כשהמסלול צמוד למדד או בפריים, ולכן המחשבון מחשב כל מסלול לחוד.</p>\n')
one(SP, SP + FORM, "formula")

# 3. what the calculators do, one sentence
ANS = new[new.index('<h2>איך משתמשים במחשבון המשכנתא?</h2>'):]
k = ANS.index("</p>\n") + len("</p>\n"); first = ANS[:k]
assert 'class="nlx-ans"' in first and "5,428" in first, first[:200]
FEAT = ('<p>מה המחשבון בודק: החזר חודשי לפי מסלולים ותמהיל, וגם הפוך, כמה משכנתא אפשר לקחת לפי ההחזר שמתאים לכם; לוח סילוקין בשפיצר, '
        'בקרן שווה, בבוליט, בבלון ועם גרייס, כולל השפעת המדד והפריים; שלושת הסלים האחידים של בנק ישראל על הסכום שלכם; השוואה של הצעות '
        'הבנקים לממוצע של כל בנק; מבחן לחץ אם הריבית של 2022 חוזרת; עמלת פירעון מוקדם ועמלת היוון; אגרת רישום משכנתה; וזכאות של משרד '
        'הבינוי והשיכון. לכל אחד מהם יש כלי בעמוד הזה, ו<a href="#million">כמה עולה משכנתא של מיליון שקל</a> מתעדכן בכל חודש.</p>\n')
one(first, first + FEAT, "features")

# 4. FAQ: one question per intent
Q40a = "<h3>האם ניתן לקבל משכנתא ל־40 שנה?</h3>"; Q40b = "<h3>אפשר לקחת משכנתא ל־40 שנה?</h3>"
fa = new.index(Q40b); fb = new.index("<h3", fa + 5); dup = new[fa:fb]
ans40b = dup[len(Q40b):].strip()
assert ans40b.startswith("<p>") and ans40b.endswith("</p>"), ans40b[:80]
new = new[:fa] + new[fb:]
A40 = "<p>לא בבנק. לפי הוראה 329 התקופה המרבית של הלוואה לדיור היא 30 שנה. משכנתא של 1,000,000 ₪ ל־30 שנה בתמהיל הממוצע של ספטמבר 2026 עולה 4,931 ₪ בחודש הראשון.</p>"
ADD40 = "מי שרוצה החזר נמוך יותר מאריך עד 30 שנה, ומשלם על כך יותר ריבית לאורך כל התקופה."
assert ADD40 in ans40b and "30 שנה" in ans40b, ans40b
one(Q40a + "\n" + A40, Q40a + "\n" + A40[:-4] + " " + ADD40 + "</p>", "40y merged")
PQ_OLD = ("<h3>אפשר לקחת משכנתא בלי הון עצמי?</h3>\n<p>בבנק לא: המימון המרבי הוא 75% בדירה יחידה, 70% בדירה חליפית ו־50% בדירה להשקעה. "
          "הורים יכולים לעזור בהלוואה על הדירה שלהם, עד 50% משוויה, ובדירה במחיר מופחת משלמים מכספכם לפחות 100,000 ₪.</p>")
PQ_NEW = ("<h3>משכנתא הורים: אפשר להיעזר בדירה של ההורים?</h3>\n<p>כן, בהלוואה על הדירה של ההורים, עד 50% משוויה. על הדירה שקונים, "
          "בבנק אי אפשר בלי הון עצמי: המימון המרבי הוא 75% בדירה יחידה, 70% בדירה חליפית ו־50% בדירה להשקעה, ובדירה במחיר מופחת משלמים "
          "מכספכם לפחות 100,000 ₪.</p>")
one(PQ_OLD, PQ_NEW, "parents q")

# 5. links to #million from the market section's lead and the map
one('<a href="#mortgage-market">', '<a href="#mortgage-market">', "market link (exists)", new.count('<a href="#mortgage-market">'))
if '<a href="#million">' not in new.split(FEAT)[0]:
    pass  # the features sentence carries the first link; the map item is added below when the market item exists
mk = re.search(r'<li><a href="#mortgage-market">[^<]*</a></li>', new)
if mk:
    new = new[:mk.end()] + '<li><a href="#million">כמה עולה משכנתא של מיליון שקל, חודש אחר חודש</a></li>' + new[mk.end():]

# 6. the photo below the first screen: real size (no jump when it arrives) and lazy, so it stops competing with the fonts on phones
IMG_OLD = '<img decoding="async" src="https://nad-lan.co.il/wp-content/uploads/2026/11/diamond-exchange-ramat-gan-chenspec-cc-by-sa.jpg" alt="בנייני משרדים ומגורים בישראל לפני חישוב החזר משכנתא" loading="eager">'
IMG_NEW = '<img decoding="async" src="https://nad-lan.co.il/wp-content/uploads/2026/11/diamond-exchange-ramat-gan-chenspec-cc-by-sa.jpg" alt="בנייני משרדים ומגורים בישראל לפני חישוב החזר משכנתא" width="960" height="540" loading="lazy">'
one(IMG_OLD, IMG_NEW, "photo")

# checks: every old line is still there (the removed duplicate question line is the one exception), no long dash, no banned words
removed = {Q40b.strip(), ans40b.strip(), A40, "<h3>אפשר לקחת משכנתא בלי הון עצמי?</h3>", PQ_OLD.split("\n")[1]}
for line in raw.split("\n"):
    t = line.strip()
    if not t or t in removed:
        continue
    t2 = t.replace(IMG_OLD, IMG_NEW).replace('<i class="g">מדריך</i></a>', '<i class="g" data-t="מדריך"></i></a>').replace(
        ".nlmap__d li a i.g{background:none;color:#5E6A75;border:1px solid #D3DCE2}",
        ".nlmap__d li a i.g{background:none;color:#5E6A75;border:1px solid #D3DCE2}.nlmap__d li a i.g:empty::after{content:attr(data-t)}")
    assert t2 in new or t2 == ans40b, ("missing", t[:90])
vis = re.sub(r"<[^>]+>", " ", FORM + FEAT)
assert not re.search(r"[–—]", vis), "long dash"
for bad in ("סימולציה", "ממשק", "דמו", "המערכת", "הפלטפורמה", "עולם המשכנתא"):
    assert not re.search(r"(?<![֐-׿])%s(?![֐-׿])" % bad, vis), bad
nq = len(re.findall(r"<h3>[^<]*\?</h3>", new.split('id="faq"')[-1])) if 'id="faq"' in new else -1
print("[page 121] round R; content %d -> %d bytes; badges %d; map item #million %s; faq h3 now %d" % (len(raw), len(new), nb, bool(mk), nq))
if DRY:
    io.open(os.path.join(H, "preview-content-r.html"), "w", encoding="utf-8", newline="").write(new); print("[dry] ok"); sys.exit(0)
io.open(os.path.join(BK, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live:", 'data-t="מדריך"' in page, "בסימון המקובל" in page, "מה המחשבון בודק" in page, page.count('"@type":"Question"'), "questions")
