# -*- coding: utf-8 -*-
"""Q3 stage 2 on /glossary/מחירון-דקל-לבנייה-ותשתיות/ (term id from the live link), after release 1.72.522 (dkpick + dkquote).
On the live content written by write_q3.py: the list chooser under the numbers table and the quote check in the "Dekel against a
contractor's quote" section; the two infographics (the decision tree, the anatomy of an item; infographics.py); new real tables:
the item fields and what to check, comparing a quote step by step, the dedicated lists, the mistakes table; a step-by-step section;
two questions (18). Every fact is from dna.md section 6 (dekel.co.il, 25.10.2026); no Dekel price anywhere.
Exact replacements, backup, read-back, live check.   python docs/research/2026-10-26-upgrades/q3-dekel-list/write_q3_stage2.py [--dry]"""
import io, os, re, sys, time, urllib.parse, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
import infographics as ig
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q3b"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
SLUG = "מחירון-דקל-לבנייה-ותשתיות"


def table(caption, head, rows):
    h = "".join("<th scope=\"col\">%s</th>" % c for c in head)
    b = "".join("<tr><th scope=\"row\">%s</th>%s</tr>" % (r[0], "".join("<td>%s</td>" % c for c in r[1:])) for r in rows)
    return "<figure class=\"wp-block-table\"><table><caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table></figure>\n" % (caption, h, b)


def fig(svg, cap):
    return "<figure class=\"nlq3-fig\" style=\"margin:20px 0\">%s<figcaption style=\"font-size:14px;color:#3E4C58;margin-top:6px\">%s</figcaption></figure>\n" % (svg, cap)


QA_NEW = [
    ("איך בודקים הצעת מחיר של קבלן מול מחירון דקל?", "משווים כל סעיף בהצעה לסעיף עם אותו קוד, אותה יחידת מידה ואותה כמות במחירון דקל, במהדורה של החודש שבו ניתנה ההצעה. בודקים מה כלול: לפי דקל מחיר סעיף כולל עבודה, חומרים ורווח קבלן, הריסה כוללת פינוי עד 15 ק\"מ בלי אגרת הטמנה, וברזל הזיון נמדד בנפרד. המחשבון בעמוד מסכם את ההפרש ומוציא את השאלות לקבלן."),
    ("מה ההבדל בין מחירון דקל להצעת מחיר?", "מחירון דקל הוא מחיר ייחוס שמתעדכן בכל 1 לחודש. הצעת מחיר היא מה שהקבלן מציע לעבודה מסוימת, ורק ההסכם איתו מחייב. במכרזי מסגרת הקבלן מציע אחוז הנחה קבוע מהמחירון."),
]
R = []
# 1. the chooser under the numbers table (before "all Dekel lists")
R.append(("<h2>כל מחירוני דקל: איזה מחירון מתאים לאיזו עבודה</h2>",
          "<p>בחרו את סוג העבודה ואת ההיקף, ותראו איזה מחירון של דקל מתאים לה, והאם ההיקף בתוך הטווח שהמחירים שלו מכוונים אליו.</p>\n[nadlan_tool id=\"dkpick\"]\n"
          "<h2>כל מחירוני דקל: איזה מחירון מתאים לאיזו עבודה</h2>"))
# 2. the tree after the lists table: anchor the next section heading
R.append(("<h2>איך קוראים סעיף במחירון דקל</h2>\n",
          fig(ig.tree_svg(), "מהעבודה אל המחירון. למחירון לבנייה ותשתיות ולמחירון לשיפוצים ואחזקה יש טווח היקף שהמחירים מכוונים אליו.")
          + "<h2>איך קוראים סעיף במחירון דקל</h2>\n" + fig(ig.anatomy_svg(), "שורה בכתב כמויות שמפנה לדקל. מחיר היחידה מגיע מהמנוי, מהמהדורה של החודש.")))
# 3. a fields table after the four h3 of the item section (anchor: the "what is included" heading)
R.append(("<h2>מה כלול במחיר סעיף ומה לא</h2>",
          table("השדות של סעיף דקל ומה בודקים בכל אחד", ["שדה", "מה הוא", "מה בודקים בהצעה"], [
              ["קוד", "פרק, תת פרק וסעיף, למשל 68.035.0010", "שהקוד זהה ושהוא מאותה מהדורה"],
              ["תיאור", "העבודה ומה כלול בה", "האם ברזל הזיון, הפינוי או חומר מסוים כלולים"],
              ["יחידת מידה", "מ\"ר, מ\"ק, מטר אורך, יחידה או קומפלט", "שהכמות בהצעה באותה יחידה"],
              ["כמות", "מכתב הכמויות או ממדידה", "שהכמות תואמת את התוכניות או את המדידה"],
              ["מחיר יחידה", "לפי המהדורה החודשית", "הפרש מול דקל, ותוספות לפי תוספות והפחתות"]])
          + "<h2>מה כלול במחיר סעיף ומה לא</h2>"))
# 4. the quote check + a step-by-step section in the "Dekel against a quote" section
R.append(("<h2>מחירון דקל מול הצעת מחיר של קבלן</h2>\n<p>המחירון הוא מחיר ייחוס, לא חוזה. משווים סעיף מול סעיף: אותו קוד, אותה יחידת מידה ואותה כמות. במכרזי מסגרת הקבלן מציע אחוז הנחה קבוע מהמחירון, וכל סעיף מחושב לפיו. תוספות לאזור מרוחק, לעבודת לילה או לעבודה קטנה מהיקף המחירון נכנסות לפי טבלת תוספות והפחתות, ולא לפי תחושה.</p>\n",
          "<h2>מחירון דקל מול הצעת מחיר של קבלן</h2>\n<p>המחירון הוא מחיר ייחוס, לא חוזה. משווים סעיף מול סעיף: אותו קוד, אותה יחידת מידה ואותה כמות. במכרזי מסגרת הקבלן מציע אחוז הנחה קבוע מהמחירון, וכל סעיף מחושב לפיו. תוספות לאזור מרוחק, לעבודת לילה או לעבודה קטנה מהיקף המחירון נכנסות לפי טבלת תוספות והפחתות, ולא לפי תחושה.</p>\n"
          "[nadlan_tool id=\"dkquote\"]\n"
          "<h3>שלב 1: אותה מהדורה</h3>\n<p>המחירים מתעדכנים בכל 1 לחודש. מבקשים מהקבלן לציין לפי איזו מהדורה הוא תמחר, ומשווים לאותה מהדורה במנוי.</p>\n"
          "<h3>שלב 2: אותו סעיף ואותה יחידה</h3>\n<p>לכל שורה בהצעה מחפשים את הקוד במחירון. אם אין קוד, משווים לפי התיאור והיחידה, ומסמנים את השורה כשורה שצריך לשאול עליה.</p>\n"
          "<h3>שלב 3: מה כלול</h3>\n<p>בודקים את הכללים של דקל: פינוי עד 15 ק\"מ כלול בהריסה ואגרת ההטמנה לא, ברזל הזיון בנפרד, ותוספות לאזור מרוחק ולעבודת לילה לפי תוספות והפחתות.</p>\n"
          "<h3>שלב 4: ההפרש והשאלות</h3>\n<p>מסכמים את ההפרש בשקלים ובאחוזים, ושולחים לקבלן את השאלות בכתב לפני החתימה.</p>\n"
          + table("השוואת הצעה למחירון דקל: מה משווים", ["מה משווים", "בהצעה", "במחירון דקל"], [
              ["מהדורה", "החודש שבו ניתנה ההצעה", "המהדורה של אותו חודש"], ["סעיף", "התיאור והקוד של הקבלן", "אותו קוד ואותו תיאור"],
              ["יחידה וכמות", "היחידה והכמות בהצעה", "אותה יחידת מידה"], ["מחיר", "מחיר היחידה של הקבלן", "מחיר היחידה במנוי"],
              ["תוספות", "תוספת שהקבלן הוסיף", "רק לפי תוספות והפחתות"]])))
# 5. dedicated lists table in the buyers section
R.append(("<p>להבנת המסמכים סביב המחירון:",
          table("מחירונים ייעודיים באתר דקל (מפת האתר, 25.10.2026)", ["מחירון", "למי"], [
              ["המאגר המאוחד של מנהל הדיור הממשלתי", "עבודות של מנהל הדיור הממשלתי"], ["משרד הביטחון", "עבודות למשרד הביטחון"],
              ["משטרת ישראל", "עבודות למשטרת ישראל"], ["נתיבי איילון", "עבודות לנתיבי איילון"], ["שב\"ס", "עבודות לשירות בתי הסוהר"],
              ["מחירון באנגלית", "פרויקטים בינלאומיים, מעל 40,000 סעיפים"]])
          + "<p>להבנת המסמכים סביב המחירון:"))
# 6. mistakes as a table
R.append(("<h2>טעויות נפוצות</h2>\n<ul>\n<li>לחשוב שהמחירון מתעדכן פעם בשנה: הוא מתעדכן בכל 1 לחודש.</li>\n<li>להשתמש ב-PDF של שנה קודמת.</li>\n<li>לבחור מחירון שלא מתאים להיקף העבודה, למשל בנייה חדשה לשיפוץ קטן.</li>\n<li>לשכוח את אגרת ההטמנה בסעיפי הריסה.</li>\n<li>להניח שברזל הזיון כלול בסעיף הבטון.</li>\n</ul>\n",
          "<h2>טעויות נפוצות</h2>\n" + table("טעויות נפוצות עם מחירון דקל", ["הטעות", "מה נכון", "מה עושים"], [
              ["לחשוב שהמחירון מתעדכן פעם בשנה", "הוא מתעדכן בכל 1 לחודש", "משווים למהדורה של החודש"],
              ["להשתמש ב-PDF של שנה קודמת", "קובץ ישן אינו המהדורה הנוכחית", "משתמשים במנוי או במהדורה שהקבלן ציין"],
              ["לבחור מחירון שלא מתאים להיקף", "כל מחירון מכוון להיקף אחר", "בוחרים לפי סוג העבודה וההיקף, ומתאימים לפי תוספות והפחתות"],
              ["לשכוח את אגרת ההטמנה", "הריסה כוללת פינוי עד 15 ק\"מ, לא את ההטמנה", "שואלים מי משלם את האגרה"],
              ["להניח שהברזל כלול בבטון", "ברזל הזיון נמדד ומתומחר בנפרד", "בודקים בתיאור הסעיף"],
              ["להתייחס למחירון כחוזה", "הוא מחיר ייחוס", "מה שמחייב הוא ההסכם עם הקבלן"]])))
# 7. two questions at the end of the FAQ (after the last answer, before whatever follows the FAQ)
R.append(("<h2>שאלות נפוצות על מחירון דקל</h2>\n", "<h2>שאלות נפוצות על מחירון דקל</h2>\n" + "".join("<h3>%s</h3>\n<p>%s</p>\n" % qa for qa in QA_NEW)))

s, lst, _ = req("GET", "/wp-json/wp/v2/nadlan_term?slug=" + urllib.parse.quote(SLUG) + "&_fields=id")
PID = lst[0]["id"]
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
print("[term %d] %d replacements | %d words | %d tables in content (+2 in the tool summaries) | %d svg | h2 %d, h3 %d" % (
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
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "dkpick": 'data-nli="dkpick"' in bd, "dkquote": 'data-nli="dkquote"' in bd,
      "2 figures": bd.count("nlq3-fig") == 2, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "dekel.js enqueued": "tools/dekel.js" in page}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
