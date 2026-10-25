# -*- coding: utf-8 -*-
"""Q5 stage 2 on /glossary/תי-466/ (term 5366), after release 1.72.522 (the t466 chooser). On the live content written by write_q5.py:
the chooser under the "466 and my apartment" table; the building section and the editions timeline (infographics.py); new real tables:
the editions timeline, errata and transition periods, what the standard costs by need, the SII reading room. Every fact is from
dna.md section 6 (SII pages, 25.10.2026); sums are labelled as calculations. Exact replacements, backup, read-back, live check.
  python docs/research/2026-10-26-upgrades/q5-ti-466/write_q5_stage2.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
import infographics as ig
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q5b"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 5366


def table(caption, head, rows):
    h = "".join("<th scope=\"col\">%s</th>" % c for c in head)
    b = "".join("<tr><th scope=\"row\">%s</th>%s</tr>" % (r[0], "".join("<td>%s</td>" % c for c in r[1:])) for r in rows)
    return "<figure class=\"wp-block-table\"><table><caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table></figure>\n" % (caption, h, b)


def fig(svg, cap):
    return "<figure class=\"nlq5-fig\" style=\"margin:20px 0\">%s<figcaption style=\"font-size:14px;color:#3E4C58;margin-top:6px\">%s</figcaption></figure>\n" % (svg, cap)


R = []
# 1. the chooser right after the "466 and my apartment" section (before part 1's section)
R.append(("<h2>ת\"י 466 חלק 1: המהדורה של 2022</h2>",
          "<p>אותה טבלה כבדיקה: בוחרים את המצב, ובדירה חדשה גם את סוג התקרות, ומקבלים את החלקים, המהדורה שבתוקף, המחיר במכון התקנים ומה לשאול. החתך מראה איזה אלמנט בבניין שייך לכל חלק.</p>\n"
          "[nadlan_tool id=\"t466\"]\n<h2>ת\"י 466 חלק 1: המהדורה של 2022</h2>"))
# 2. the building section after the parts 3-5 section heading's list (anchor: the scope section that follows it)
R.append(("<h2>על מה ת\"י 466 חל ועל מה לא</h2>",
          fig(ig.building_svg(), "כל אלמנט בבניין מגורים לפי החלק שחל עליו. חלק 1 חל על כל המבנה.") + "<h2>על מה ת\"י 466 חל ועל מה לא</h2>"))
# 3. errata and transitions + the timeline, after the status section (before 466 vs 118)
R.append(("<h2>ההבדל בין ת\"י 466 לת\"י 118</h2>",
          "<h2>תיקוני טעות, גיליונות תיקון ותקופות מעבר</h2>\n<p>כל חלק עודכן בזמן אחר, ולכן לכל חלק יש היסטוריה משלו. גיליון תיקון משנה סעיפים במהדורה קיימת, תיקון טעות מתקן טעות שנפלה בה, ובתקופת מעבר היו שתי מהדורות בתוקף יחד.</p>\n"
          + table("תיקונים ותקופות מעבר בחלקי ת\"י 466 (מכון התקנים, 25.10.2026)", ["חלק", "גיליונות תיקון", "תיקון טעות", "תקופת מעבר"], [
              ["1", "1", "ספטמבר 2025, ילקוט הפרסומים 13873, 15.10.2025", "מהדורת 2003 בוטלה ביום פרסום המהדורה החדשה, 15.8.2022"],
              ["2", "2", "מרץ 2017, ילקוט הפרסומים 7527, 15.6.2017", "בתוקף 3 חודשים אחרי הפרסום ברשומות, ובשנתיים הבאות גם מהדורת 1979 עם תיקוניה"],
              ["3", "1", "", "שנתיים מהפרסום שבהן גם מהדורת יולי 1987 בתוקף"],
              ["4", "3", "", ""], ["5", "4", "", ""]])
          + fig(ig.timeline_svg(), "המהדורות מ-1977 ועד תיקון הטעות של 2025. מלא: בתוקף היום.")
          + table("ציר המהדורות של ת\"י 466", ["שנה", "חלק", "מה קרה", "בתוקף היום"], [
              ["1977", "4", "מפרט 17, שקדם לחלק 4", "לא"], ["1979", "2", "מהדורת חלק 2 הקודמת", "לא"], ["1987", "3", "מהדורת חלק 3 הקודמת (יולי)", "לא"],
              ["1987", "5", "חלק 5: תקרות מטבלות חלולות טרומות דרוכות (1.12.1987)", "כן"], ["1991", "4", "חלק 4: אלמנטים ומערכות מבטון טרום (1.4.1991)", "כן"],
              ["2003", "1", "מהדורת חלק 1 הקודמת", "לא"], ["2015", "2", "חלק 2: רכיבים (31.12.2015)", "כן"], ["2017", "3", "חלק 3: בטון דרוך (31.3.2017)", "כן"],
              ["2022", "1", "חלק 1: עקרונות כלליים (15.8.2022)", "כן"], ["2025", "1", "תיקון טעות לחלק 1 (ספטמבר 2025)", "כן"]])
          + "<h2>ההבדל בין ת\"י 466 לת\"י 118</h2>"))
# 4. cost by need + the reading room, at the end of the "where to read" section (before the background section)
R.append(("<h2>רקע על ת\"י 466</h2>",
          table("כמה עולה ת\"י 466 לפי מה שצריך (מחירי מכון התקנים, 25.10.2026; הסכומים חישוב)", ["מה צריך", "החלקים", "כולל מע\"מ", "לפני מע\"מ"], [
              ["בניין מגורים יצוק", "1 ו-2", "972.50 ₪", "824.20 ₪"], ["בניין עם תקרות לוח\"דים", "1, 2 ו-5", "1,240.20 ₪", "1,051.10 ₪"],
              ["בניין עם אלמנטים טרומיים", "1, 2 ו-4", "1,336.30 ₪", "1,132.50 ₪"], ["כל חמשת החלקים", "1 עד 5", "2,027.60 ₪", "1,718.40 ₪"]])
          + table("מרכז המידע של מכון התקנים: קריאה בלי תשלום", ["פרט", "מה"], [
              ["כתובת", "רחוב חיים לבנון 42, תל אביב"], ["שעות", "ימים א עד ה, 8:00 עד 15:00"], ["תיאום", "03-6465191/2, library@sii.org.il"],
              ["מה אפשר", "לקרוא תקנים ישראליים בתיאום מראש, בלי תשלום"]])
          + "<p>עותק סרוק של חלק 1 ממהדורת 2003, שמסתובב ברשת, אינו המהדורה שבתוקף: היא הוחלפה ב-15.8.2022, ומאז פורסם לה גם תיקון טעות.</p>\n<h2>רקע על ת\"י 466</h2>"))

s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content,link" % PID)
raw = r["content"]["raw"]; new = raw
for o, n in R:
    c = new.count(o)
    assert c == 1, (c, o[:70])
    new = new.replace(o, n)
vis = re.sub(r"<[^>]+>", " ", re.sub(r"<svg\b.*?</svg>", " ", new, flags=re.S))
assert not re.search(r"[–—]", vis), "long dash"
assert not re.search(r"ממשק|פלטפורמה|סימולצי|בקרוב|טעון אימות", vis), "language DNA"
words = len(re.findall(r"[\w֐-׿\"']+", vis))
print("[term %d] %d replacements | %d words | %d tables in content (+1 in the tool summary) | %d svg | h2 %d, h3 %d" % (
    PID, len(R), words, new.count("<table"), new.count("<svg"), new.count("<h2"), new.count("<h3")))
if DRY:
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "term-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/nadlan_term/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "tool mounted": 'data-nli="t466"' in bd, "tool summary": "איזה חלק של ת״י 466 חל על כל אלמנט" in bd,
      "2 figures": bd.count("nlq5-fig") == 2, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "t466.js enqueued": "tools/t466.js" in page}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
