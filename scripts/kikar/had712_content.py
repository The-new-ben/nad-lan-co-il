# -*- coding: utf-8 -*-
"""HAD-712, the content round (Ben 11.11.2026: "research how people search the project, put those words in, make price lists, numbers";
then "Yes, start"). The Hebrew Kikar article (/projects/hamedina/, post 8113) gains what the search research of 11.11.2026 found missing
(docs/research/2026-11-11-kikar-search/summary.md): height per tower, "how many floors", the address, the developer / purchase-group
question, the architect as a question, the building-fee and rent estimates, the project manager's short name, and a table of the numbers
that different publications give differently. Every number was read at its source on 11.11.2026 (docs/qa/had-712/sources.md).
Small anchored replacements on the LIVE post text; the live md5 is pinned; each anchor must appear exactly once. The article names no
outlet (the owner's rule of 1.10.2026). Backup before, read-back after (restored if it differs); dry by default.
  python scripts/kikar/had712_content.py [--go]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
PID, SLUG, PIN = 8113, "hamedina", "4e7690742a45ce011d234053f219bcc7"  # modified 2026-11-11T03:49:45

EST = "בהערכה של איש נדל״ן שפורסמה באוקטובר 2026"

TOWERS = ("<h3>כמה קומות ומה הגובה של כל מגדל?</h3>"
          "<p>שני מגדלים בני 40 קומות ומגדל אחד בן 37 קומות. הטבלה מרכזת את מה שפורסם על כל מגדל; מספר הדירות בכל מגדל לא פורסם.</p>"
          "<table><thead><tr><th>מגדל</th><th>מיקום במגרש</th><th>קומות</th><th>גובה שפורסם</th></tr></thead><tbody>"
          # every cell says what it is: on a phone the theme stacks the cells and hides the header row
          "<tr><td>מגדל A</td><td>בדרום מערב המגרש</td><td>40 קומות</td><td>כ-160 מטר</td></tr>"
          "<tr><td>מגדל B</td><td>בדרום מזרח המגרש</td><td>37 קומות</td><td>כ-157 מטר</td></tr>"
          "<tr><td>מגדל C</td><td>בצפון מזרח המגרש</td><td>40 קומות</td><td>כ-160 מטר</td></tr>"
          "</tbody></table>")

DIFF = ("<p><strong>מספרים שמופיעים אחרת בפרסומים שונים.</strong> חלק מנתוני הפרויקט מתפרסמים בכמה גרסאות. הטבלה מציגה את הגרסאות שנמצאו ב-11.2026 ואת הנתון שמוצג בעמוד הזה.</p>"
        "<table><thead><tr><th>הנתון</th><th>מה מופיע בפרסומים</th><th>מה מוצג בעמוד הזה</th></tr></thead><tbody>"
        "<tr><td>קומות</td><td>בפרסומים: שלושה מגדלים בני 40 קומות, וגם שניים בני 40 קומות ואחד בן 37</td><td>בעמוד הזה: 40, 37 ו-40 קומות, לפי הפירוט של חברת הבנייה</td></tr>"
        "<tr><td>גובה</td><td>בפרסומים: עד כ-160 מטר לכל המגדלים, וגם 160 מטר לשניים ו-157 מטר לשלישי</td><td>בעמוד הזה: עד כ-160 מטר; מגדל B, בן 37 הקומות, כ-157 מטר</td></tr>"
        "<tr><td>מספר הדירות</td><td>בפרסומים: כ-450, וגם 453</td><td>בעמוד הזה: 453 דירות</td></tr>"
        "<tr><td>בעלי הקרקע</td><td>בפרסומים: כ-150, וגם כ-250</td><td>בעמוד הזה: כ-250 בעלי זכויות</td></tr>"
        "<tr><td>שטח</td><td>בפרסומים: כ-27 דונם, כ-50 דונם וגם כ-78 דונם</td><td>בעמוד הזה: כ-78 דונם הוא שטח התוכנית כולה, והפארק הציבורי לבדו כ-40 דונם; בפרסומים שבהם מופיעים כ-27 וכ-50 דונם לא מפורט מה נמדד</td></tr>"
        "<tr><td>סיום הבנייה</td><td>בפרסומים: 2026, וגם אפריל 2027</td><td>בעמוד הזה: השלמת הקמת המגדלים פורסמה ב-10.2026, ומסירת הדירות צפויה בין הרבעון הראשון של 2027 למאי 2027</td></tr>"
        "</tbody></table>")

FAQ_NEW = ("<h3>כמה קומות יש במגדלי כיכר המדינה?</h3>"
           "<p>במגדלים A ו-C יש 40 קומות, ובמגדל B יש 37 קומות. מתחת למגדלים שלושה מפלסי חניון תת קרקעיים. כל קומה מסתובבת ב-1.25 מעלות ביחס לקומה שמתחתיה, ולכן דירות באותו צד של המגדל פונות לכיוון מעט שונה בכל קומה. בבחירת קומה, בקשו את תוכנית הקומה המסוימת ובדקו לאן פונים הסלון והמרפסת.</p>"
           "<h3>מה הכתובת של מגדלי כיכר המדינה?</h3>"
           "<p>המגדלים עומדים בתוך כיכר המדינה בתל אביב, בצפון החדש, וכתובותיהם בהיתר הבנייה הן רחוב ה׳ באייר 25, 45 ו-65. רחוב ה׳ באייר מקיף את הכיכר, רחוב ויצמן מגיע אליה מדרום ורחוב ז׳בוטינסקי ממזרח. בפנייה על דירה, בקשו את כתובת המגדל ואת מספר הדירה, כי כתובת כללית של כיכר המדינה מתאימה גם לבנייני הטבעת שמסביב.</p>"
           "<h3>מי היזם של מגדלי כיכר המדינה, והאם זו קבוצת רכישה?</h3>"
           "<p>את הפרויקט מקימים בעלי הקרקע עצמם: כ-250 בעלי זכויות, יורשיהם של רוכשי המגרשים ב-1942, שהתאגדו ב-1997 ופועלים במסגרת חברת בעלי הקרקע. הם קיבלו דירות כנגד הקרקע, וסדר בחירת הדירות נקבע בהגרלה. בחיפושים הפרויקט מכונה לעיתים קבוצת רכישה; בפועל זו התאגדות של בעלי הקרקע, ולא קבוצה שקנתה את הקרקע יחד. אין יזם שמוכר דירות חדשות לציבור: מי שקונה היום קונה דירה, או זכות לדירה, מאחד מבעלי הזכויות.</p>"
           "<h3>מי האדריכל של מגדלי כיכר המדינה?</h3>"
           "<p>את המגדלים תכנן משרד יסקי מור סיון אדריכלים, שנבחר בתחרות בשנת 2000. התכנון מבוסס על מעטפת מסתובבת: כל קומה מוסטת ב-1.25 מעלות ביחס לקומה שמתחתיה. תכנון הנוף הוא של ת.מ.א, ואת ניהול הפרויקט מרכזת וקסמן גוברין גבע (WXG). את תוכנית הדירה המסוימת ואת המפרט שלה מקבלים מהמוכר, ולא מתיאור כללי של התכנון.</p>"
           "<h3>כמה ועד בית משלמים במגדלי כיכר המדינה?</h3>"
           "<p>תעריף רשמי של דמי הניהול לא פורסם. " + EST + ", דמי התחזוקה צפויים להגיע לכ-4,000 עד 5,000 ₪ לדירה בחודש, בהתאם לשטח הדירה. ההערכה מתייחסת לבניין עם מתקני דיירים, ובהם בריכת שחייה, ספא וחדר כושר. זו הערכה מוקדמת, לפני האכלוס. לפני החלטה, בקשו את החיוב החודשי של הדירה המסוימת ואת פירוט השירותים שהוא כולל.</p>")

SWAPS = [
    # 1. the facts table: height per tower
    ("<tr><th>גובה</th><td>עד כ-160 מטר, במבנים בעלי מעטפת מסובבת.</td></tr>",
     "<tr><th>גובה</th><td>עד כ-160 מטר, במבנים בעלי מעטפת מסובבת. לפי הנתונים שפורסמו, מגדלים A ו-C מגיעים לכ-160 מטר ומגדל B לכ-157 מטר.</td></tr>"),
    # 2. the project manager's short name, as people search it
    ("<td>וקסמן גוברין גבע מנהלת את הפרויקט ומלווה אותו משנת 2001.",
     "<td>וקסמן גוברין גבע (WXG) מנהלת את הפרויקט ומלווה אותו משנת 2001."),
    # 3. after the facts table: the numbers that publications give differently
    ("</tbody></table></section><section class=\"nlws\" id=\"nlws-choose\">",
     "</tbody></table>" + DIFF + "</section><section class=\"nlws\" id=\"nlws-choose\">"),
    # 4. the three towers side by side
    ("במקום לייחס צפיפות למגדל על סמך גובהו.</p><h3>מה הסיבוב עושה למרפסות ולמבט החוצה?</h3>",
     "במקום לייחס צפיפות למגדל על סמך גובהו.</p>" + TOWERS + "<h3>מה הסיבוב עושה למרפסות ולמבט החוצה?</h3>"),
    # 5. the building fee
    ("<p>שם חברת הניהול ודמי הניהול החודשיים לא פורסמו. לצורך תקציב המגורים,",
     "<p>שם חברת הניהול ותעריף רשמי של דמי הניהול לא פורסמו. " + EST + ", דמי התחזוקה (ועד הבית) במגדלים צפויים להגיע לכ-4,000 עד 5,000 ₪ לדירה בחודש, בהתאם לשטח הדירה. זו הערכה מוקדמת, לפני האכלוס. לצורך תקציב המגורים,"),
    # 6. rent
    ("מחירי שכירות במגדלי כיכר המדינה לא פורסמו. בחיפוש שכירות,",
     "שכירות שנסגרה בפועל במגדלי כיכר המדינה עוד לא פורסמה, כי המגדלים טרם אוכלסו. " + EST + ", דירה במגדלים תושכר בכ-25 אלף ₪ בחודש; זו הערכה מוקדמת, ולא עסקת שכירות. בחיפוש שכירות,"),
    # 7. the height answer
    ("<p>גובה המגדלים מגיע עד כ-160 מטר. מגדלים A ו-C בני 40 קומות, ומגדל B בן 37 קומות.",
     "<p>גובה המגדלים מגיע עד כ-160 מטר. לפי הנתונים שפורסמו, מגדלים A ו-C, בני 40 קומות, מגיעים לכ-160 מטר, ומגדל B, בן 37 קומות, לכ-157 מטר."),
    # 8. five questions people search, after "who built"
    ("<h3>מהי כיכר המדינה בתל אביב?</h3>",
     FAQ_NEW + "<h3>מהי כיכר המדינה בתל אביב?</h3>"),
    # 9. the rent answer
    ("<p>השכרה במגדלים מתחילה לאחר האכלוס, ומחירי שכירות לדירות במגדלים לא פורסמו.",
     "<p>השכרה במגדלים מתחילה לאחר האכלוס, ושכירות שנסגרה בפועל עוד לא פורסמה. " + EST + ", דירה במגדלים תושכר בכ-25 אלף ₪ בחודש."),
]


def apply(raw):
    for old, new in SWAPS:
        c = raw.count(old)
        if c != 1:
            raise SystemExit("anchor x%d: %s" % (c, old[:90]))
        raw = raw.replace(old, new)
    return raw


s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
raw = g["content"]["raw"]
now = hashlib.md5(raw.encode("utf-8")).hexdigest()
if now != PIN:
    raise SystemExit("the live post changed since it was read (%s, modified %s): read it again before replacing anything" % (now[:10], g["modified"]))
new = apply(raw)
assert new.count("<table>") == raw.count("<table>") + 2 and new.count("</table>") == new.count("<table>")
assert new.count("<h3>") == raw.count("<h3>") + 6 and new.count("<h2>") == raw.count("<h2>")
print("[plan] post %d: %d replacements; %d -> %d chars" % (PID, len(SWAPS), len(raw), len(new)))
if not GO:
    io.open(os.path.join(HERE, "_had712_preview.html"), "w", encoding="utf-8", newline="").write(new)
    sys.exit(0)
bk = os.path.join(REPO, "docs", "qa", "had-712"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
assert s1 in (200, 201), (s1, str(r1)[:300])
s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
ok = r["content"]["raw"] == new
res = {"post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(), "read_back_equal": ok, "modified": r.get("modified"), "replacements": len(SWAPS)}
json.dump({"stamp": stamp, "result": res}, open(os.path.join(bk, "result-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
if not ok:  # put the old text back and stop
    sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
    raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
print("[done] post %d written and read back; backup and result in docs/qa/had-712/ (%s)" % (PID, stamp))
