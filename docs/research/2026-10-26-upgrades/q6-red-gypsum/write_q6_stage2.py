# -*- coding: utf-8 -*-
"""Q6 stage 2 on /glossary/לוח-גבס-אדום/ (term 5256), after release 1.72.521 (the gwall calculator). On the live content written by
write_q6.py: the calculator under the numbers table; the two infographics (colour map, tested partition cut, infographics.py); a
price chart; new real tables: what each standard does, the documents to ask for, the Fire and Rescue directives, price per m² white
against pink, the choice table, the mistakes table; the worked example in the calculator's own method; two questions (18).
Every fact is from dna.md section 6. Exact replacements (each must match once), backup, read-back, live check.
  python docs/research/2026-10-26-upgrades/q6-red-gypsum/write_q6_stage2.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
import infographics as ig
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q6b"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 5256


def table(caption, head, rows):
    h = "".join("<th scope=\"col\">%s</th>" % c for c in head)
    b = "".join("<tr><th scope=\"row\">%s</th>%s</tr>" % (r[0], "".join("<td>%s</td>" % c for c in r[1:])) for r in rows)
    return "<figure class=\"wp-block-table\"><table><caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table></figure>\n" % (caption, h, b)


def fig(svg, cap):
    return "<figure class=\"nlq6-fig\" style=\"margin:20px 0\">%s<figcaption style=\"font-size:14px;color:#3E4C58;margin-top:6px\">%s</figcaption></figure>\n" % (svg, cap)


def price_svg():
    """The four supplier prices of a 2.60 m pink board on 25.10.2026, as shown on their sites (only Rotenberg states VAT)."""
    rows = [("נוימן", 81.42, "כפי שמופיע, משלוח חינם"), ("רוטנברג", 80.8, "כולל מע\"מ"), ("טגטק", 70, "כפי שמופיע"), ("ועקנין", 58, "כפי שמופיע")]
    W, x1, x0 = 420, 300, 24  # bars grow from the right edge of the bar area (x1) to the left
    g = ['<svg viewBox="0 0 %d 250" direction="rtl" role="img" aria-label="מחיר לוח גבס ורוד 2.60 מטר אצל ארבעה ספקים ב-25.10.2026: נוימן 81.42, רוטנברג 80.8, טגטק 70, ועקנין 58 שקלים" style="display:block;width:100%%;height:auto;max-width:640px;background:#fff">' % W]
    g.append(ig.t(W - 12, 24, "מחיר לוח ורוד 12.5 מ\"מ, 2.60 × 1.20, ב-25.10.2026", size=15, weight=600))
    g.append(ig.t(W - 12, 44, "כפי שמופיע באתרי הספקים. רק רוטנברג מציין שהמחיר כולל מע\"מ", size=12.5, fill=ig.INK2))
    for i, (s, v, note) in enumerate(rows):
        y = 64 + i * 44; w = (x1 - x0) * v / 90.0
        g.append('<rect x="%.1f" y="%d" width="%.1f" height="22" fill="url(#q6fr)" stroke="%s"/>' % (x1 - w, y, w, ig.INK))
        g.append(ig.t(W - 12, y + 16, s, size=14, weight=600))
        g.append(ig.t(x1 - w - 6, y + 16, ("%s ₪" % ("%g" % v)), size=14, weight=600, mono=True))
        g.append(ig.t(W - 12, y + 34, note, size=11.5, fill=ig.INK2))
    g.insert(1, ig.DEFS)
    g.append('</svg>')
    return "".join(g)


QA_NEW = [
    ("כמה לוחות גבס צריך לקיר?", "מחלקים את שטח הקיר, כפול מספר הצדדים והשכבות, בשטח הלוח (3.12 מ\"ר בלוח של 2.60 על 1.20), ומוסיפים פחת. בודקים גם תוכנית חיתוך, כי קיר שגבוה מהלוח או שאורכו לא מתחלק ב-1.20 צריך חלקים נוספים, ומזמינים את המספר הגדול מבין השניים. קיר של 4 על 2.6 מטר, שני צדדים ושתי שכבות בכל צד, צריך 15 לוחות עם 10% פחת. המחשבון בעמוד עושה את שני החישובים."),
    ("כמה שוקל קיר גבס ורוד?", "לפי טבלת הספק לוח ורוד של 12.5 מ\"מ במידה 2.60 על 1.20 שוקל 27 ק\"ג. 15 הלוחות של קיר בגודל 4 על 2.6 מטר, בשני צדדים ובשתי שכבות, שוקלים כ-405 ק\"ג, בלי השלד והבידוד."),
]

R = []  # (old, new): each old must appear exactly once in the live content
# 1. the calculator, right under the numbers table
R.append(("<h2>צבעי לוחות הגבס: מה כל צבע אומר</h2>",
          "<p>כמה לוחות להזמין לקיר שלכם, כמה הם שוקלים וכמה הם עולים אצל הספקים, ואיזו מחיצה שנבדקה מתאימה להרכב: מקלידים את מידות הקיר ואת דרישת האש שקבע היועץ.</p>\n"
          "[nadlan_tool id=\"gwall\"]\n"
          "<h2>צבעי לוחות הגבס: מה כל צבע אומר</h2>"))
# 2. the colour map before the colours table
R.append(("<p>הצבע מסמן את התכונה העיקרית של הלוח. אדום וורוד הם אותו לוח, ולוח כתום, צהוב או כחול אינו תחליף ללוח אש.</p>\n",
          "<p>הצבע מסמן את התכונה העיקרית של הלוח. אדום וורוד הם אותו לוח, ולוח כתום, צהוב או כחול אינו תחליף ללוח אש.</p>\n"
          + fig(ig.colours_svg(), "תשעה צבעים, ורק שלושה מהם לוחות אש. הפירוט המלא בטבלה.")))
# 3. the partition cut + the standards table after the fire section
STD = table("מה בודק כל תקן (לפי אתר מכון התקנים)", ["תקן", "שם", "מהדורה", "מה הוא קובע"], [
    ["ת\"י 931 חלק 1.1", "עמידות אש של אלמנטי בניין, שיטות בדיקה: דרישות כלליות", "31.7.2014", "איך בודקים אלמנט בניין באש סטנדרטית, ולכמה זמן הוא עומד בקריטריונים"],
    ["ת\"י 931 חלק 1.8", "דרישות לאלמנטים לא נושאים מפרידים אנכיים", "31.12.2012", "מחיצות שאינן נושאות, כשצד אחד מחומם. לא לקיר מסך ולא לקיר עם דלת או זיגוג"],
    ["ת\"י 755", "סיווג בשרפה של מוצרי בנייה ושל אלמנטי בניין", "30.11.2023", "סיווג התגובה של מוצר הבנייה באש"],
    ["ת\"י 1490 חלק 1", "מחיצות וחיפויי גבס: לוחות", "1.12.1993, עם 2 גיליונות תיקון", "לוחות גבס עד עובי 25 מ\"מ למחיצות ולחיפויים פנימיים של קירות ותקרות"],
    ["ת\"י 1142", "מעקים ומסעדים", "30.5.2019", "מעקים ומסעדים. אינו תקן אש"]])
R.append(("<h2>מחיצות אש שנבדקו: דוגמאות מספקים</h2>",
          "<h2>מה בודק כל תקן</h2>\n<p>שלושה תקנים נוגעים ללוח ולקיר, וכל אחד עונה על שאלה אחרת: האם הלוח עצמו תקני, איך הוא מגיב באש, וכמה זמן הקיר כולו מחזיק.</p>\n" + STD
          + fig(ig.partition_svg(), "חתך של מחיצה שספק פרסם עם הבדיקה שלה: 2 לוחות ורודים מכל צד, ניצבי פלדה של 70 מ\"מ וצמר של 5 ס\"מ, 120 דקות. דוגמה, לא אישור לקיר שלכם.")
          + "<h2>מחיצות אש שנבדקו: דוגמאות מספקים</h2>"))
# 4. the directives as a table under their paragraph
DIR = table("הוראות נציב כבאות והצלה והנחיה עירונית על קירות עמידי אש", ["הוראה", "תחום", "עדכון", "מה כתוב על קירות"], [
    ["הוראת נציב 505", "בתי חולים ומוסדות בריאות", "דצמבר 2020", "אלמנט עמיד אש הוא חלק בניין בעל עמידות אש לפי ת\"י 931, למשך 90 דקות או זמן אחר שנקבע בהוראות"],
    ["הוראת נציב 523", "מוסדות חינוך", "אוגוסט 2022", "קירות ותקרות שמפרידים בין חלקי הבניין עומדים בת\"י 931 ובעמידות האש שבחקיקה (סעיף 7.1.6)"],
    ["הנחיות התכנון של עיריית תל אביב-יפו", "תכנון בתל אביב-יפו", "", "מחיצות אש לפי תקנות התכנון והבנייה, הוראות הנציב ות\"י 931; עמידות האש של קיר לא פחות מ-60 דקות"]])
R.append(("מספר הדקות לקיר מסוים מגיע מיועץ הבטיחות ומההיתר, לא מהלוח.</p>\n",
          "מספר הדקות לקיר מסוים מגיע מיועץ הבטיחות ומההיתר, לא מהלוח.</p>\n" + DIR
          + "<h2>המסמכים שמבקשים מהקבלן</h2>\n<p>ארבעה מסמכים מראים שהקיר שנבנה הוא הקיר שנבדק. בלי תעודת הבדיקה של המחיצה כולה, מספר הדקות הוא הבטחה בלבד.</p>\n"
          + table("המסמכים לקיר גבס עמיד אש", ["מסמך", "לפי", "מה הוא מוכיח", "ממי מבקשים"], [
              ["תעודת בדיקה של המחיצה", "ת\"י 931 חלק 1.8", "כמה דקות עמד הקיר כולו, בהרכב מסוים", "הקבלן, מהיצרן או מהספק של המערכת"],
              ["סיווג תגובה באש", "ת\"י 755", "איך הלוח מגיב באש", "הקבלן, מהיצרן"],
              ["תו תקן ללוח", "ת\"י 1490 חלק 1", "שהלוח עומד בתקן לוחות הגבס", "סימון על הלוח ותעודה מהיצרן"],
              ["פרט ביצוע", "המערכת שנבדקה", "שהקיר נבנה כמו בבדיקה: שלד, בידוד, מספר שכבות וברגים", "היועץ והקבלן"]])))
# 5. the weights: a calculated line already there; the price section gets the chart and a per-m² table
R.append(("<p>אצל רוטנברג הלוח הוורוד יקר בכ-32% מהלבן באותה מידה (68.5 מול 52 ₪ לפני מע\"מ).</p>\n",
          "<p>אצל רוטנברג הלוח הוורוד יקר בכ-32% מהלבן באותה מידה (68.5 מול 52 ₪ לפני מע\"מ).</p>\n"
          + fig(price_svg(), "ארבעת הספקים שציינו את אורך הלוח, 2.60 מטר. ההפרש בין הזול ליקר: 23.42 ₪ ללוח.")
          + "<h3>מחיר למ\"ר: לוח לבן מול לוח ורוד</h3>\n"
          + table("מחיר למ\"ר לפני מע\"מ אצל רוטנברג, 25.10.2026", ["לוח", "מידה", "מחיר ללוח לפני מע\"מ", "מחיר למ\"ר לפני מע\"מ"], [
              ["ורוד 12.5 מ\"מ", "2.60 × 1.20 (3.12 מ\"ר)", "68.5 ₪", "21.95 ₪"], ["ורוד 12.5 מ\"מ", "2.00 × 1.20 (2.4 מ\"ר)", "53.1 ₪", "22.1 ₪"],
              ["לבן 12.5 מ\"מ", "2.60 × 1.20 (3.12 מ\"ר)", "52 ₪", "16.6 ₪"]])
          + "<p>הלוח הארוך זול מעט יותר למ\"ר, וגם חוסך תפרים כשהקיר גבוה.</p>\n"))
# 6. the choice list becomes a table
R.append(("<h2>גבס אדום, ורוד, משולב או מיוחד לאש: איך בוחרים</h2>\n<ul>\n<li><strong>מחיצה או תקרה בחדר יבש עם דרישת אש:</strong> לוח ורוד (FR).</li>\n<li><strong>חדר רטוב עם דרישת אש:</strong> לוח משולב ירוק ורוד (FM).</li>\n<li><strong>פירים, תעלות, עמודים וקירות פלדה:</strong> לוחות מיוחדים לאש בעובי 22 עד 25 מ\"מ.</li>\n<li><strong>קיר חוץ:</strong> לא לוח ורוד. יש לוחות חיצוניים, ואחד מהם מסווג A1 לפי ת\"י 755.</li>\n</ul>\n",
          "<h2>גבס אדום, ורוד, משולב או מיוחד לאש: איך בוחרים</h2>\n<p>הבחירה מתחילה במקום של הקיר ובדרישת האש שקבע היועץ. זה גם הסדר של המחשבון למעלה.</p>\n"
          + table("איזה לוח לאיזה קיר", ["המקום", "הלוח", "למה", "עובי נפוץ"], [
              ["חדר יבש בלי דרישת אש", "לבן רגיל (RE)", "זול יותר: אצל רוטנברג הוורוד יקר ממנו בכ-32%", "12.5 מ\"מ"],
              ["חדר יבש עם דרישת אש", "ורוד מעכב בעירה (FR)", "ליבה עם סיבי זכוכית וורמיקוליט", "12.5 או 16 מ\"מ"],
              ["חדר רטוב עם דרישת אש", "משולב ירוק ורוד (FM)", "מעכב בעירה ועמיד במים ובלחות", "לפי היצרן"],
              ["פירים, תעלות, עמודים וקירות פלדה", "לוח מיוחד לאש (פייר דיפנדר, דיפנדר+)", "מערכות מיוחדות שנבדקו", "22 עד 25 מ\"מ"],
              ["קיר חוץ", "לוח חוץ, לא ורוד", "הלוח הוורוד לשימוש פנימי בלבד; לחוץ עם דרישת אש יש לוח שמסווג A1 לפי ת\"י 755", "לפי היצרן"]])))
# 7. the worked example in the calculator's method
R.append(("<p>קיר באורך 100 מטר ובגובה 3 מטרים, צד אחד בשכבה אחת: שטח 300 מ\"ר. לוח של 1.20 על 3.00 מטר מכסה 3.6 מ\"ר, ולכן צריך 300 ÷ 3.6 = 83.3, כלומר 84 לוחות. הפחת נקבע לפי הקיר, למשל 10%: 84 × 1.1 = 92.4, כלומר 93 לוחות. בקיר עם שני צדדים ושתי שכבות בכל צד מכפילים פי 4. המשקל לפי 9.2 ק\"ג למ\"ר: 300 מ\"ר בשכבה אחת שוקלים כ-2,760 ק\"ג.</p>\n",
          "<p>קיר באורך 100 מטר ובגובה 3 מטרים, צד אחד בשכבה אחת: שטח 300 מ\"ר. לוח של 1.20 על 3.00 מטר מכסה 3.6 מ\"ר. לפי שטח, עם פחת של 10% שנקבע לפי הקיר: 300 × 1.1 ÷ 3.6 = 91.7, כלומר 92 לוחות. לפי תוכנית חיתוך: 83 עמודות מלאות של 1.20 מטר ועמודה צרה של 0.40 מטר, שנחתכת מלוח אחד, כלומר 84 לוחות. מזמינים את הגדול מבין השניים, 92. המשקל לפי טבלת הספק, 31 ק\"ג ללוח: כ-2,852 ק\"ג. לפי 9.2 ק\"ג למ\"ר, 300 המ\"ר שעל הקיר שוקלים כ-2,760 ק\"ג.</p>\n"))
# 8. the mistakes list becomes a table
R.append(("<h2>טעויות נפוצות</h2>\n<ul>\n<li>לייחס מספר דקות ללוח עצמו, במקום לקיר שנבדק.</li>\n<li>להשתמש בלוח כתום, צהוב או כחול כלוח אש.</li>\n<li>להתקין לוח ורוד בחוץ.</li>\n<li>לבנות מערכת שנבדקה עם שלד, ברגים או בידוד אחרים.</li>\n<li>לצטט תקן לא נכון: הבדיקה של קיר היא לפי ת\"י 931, לא לפי ת\"י 1142.</li>\n</ul>\n",
          "<h2>טעויות נפוצות</h2>\n" + table("טעויות נפוצות בקיר גבס עמיד אש", ["הטעות", "למה זו טעות", "מה עושים"], [
              ["לייחס מספר דקות ללוח עצמו", "הדקות שייכות לקיר שנבדק, עם השלד והבידוד שלו", "מבקשים את תעודת הבדיקה של המחיצה לפי ת\"י 931"],
              ["להשתמש בלוח כתום, צהוב או כחול כלוח אש", "הם לוחות חוץ ורטיבות, לא לוחות אש", "בוחרים לוח ורוד, משולב או מיוחד לאש"],
              ["להתקין לוח ורוד בחוץ", "הלוח לשימוש פנימי בלבד", "לחוץ בוחרים לוח חוץ, ולחוץ עם דרישת אש לוח שמסווג A1 לפי ת\"י 755"],
              ["לבנות מערכת שנבדקה עם רכיבים אחרים", "שינוי בשלד, בברגים או בבידוד יכול לבטל את מספר הדקות", "בונים לפי פרט הביצוע של המערכת שנבדקה"],
              ["לצטט ת\"י 1142", "זה תקן של מעקים ומסעדים", "הבדיקה של קיר היא לפי ת\"י 931"],
              ["לחשב לוחות לפי שטח בלבד", "קיר גבוה מהלוח או שאורכו לא מתחלק ב-1.20 צריך חלקים נוספים", "בודקים גם תוכנית חיתוך ומזמינים את המספר הגדול"]])))
# 9. two questions at the end of the FAQ (before the sources line)
R.append(("<p><small>לבדיקה במקור:", "".join("<h3>%s</h3>\n<p>%s</p>\n" % qa for qa in QA_NEW) + "<p><small>לבדיקה במקור:"))
R.append(("<p><small>עודכן 25.10.2026. מחירים ונתוני מוצר לפי אתרי היצרנים והספקים באותו יום.</small></p>", "<p><small>עודכן 25.10.2026. מחירים ונתוני מוצר לפי אתרי היצרנים והספקים באותו יום, והמחשבון לפי אותם נתונים.</small></p>"))

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
    io.open(os.path.join(H, "preview", "q6-stage2-content.html"), "w", encoding="utf-8").write(new)
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "term-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/nadlan_term/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "tool mounted": 'data-nli="gwall"' in bd, "tool summary table": "כמה לוחות גבס ורודים של 12.5" in bd,
      "svg x3 in text": bd.count("nlq6-fig") == 3, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "18 questions": page.count('"@type":"Question"') == 18,
      "SoftwareApplication": '"@type":"SoftwareApplication"' in page, "gwall.js enqueued": "tools/gwall.js" in page}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
