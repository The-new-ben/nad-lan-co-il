# -*- coding: utf-8 -*-
"""HAD-654 R10b (intent wrap), Migdalei Hayam Sde Dov (post 4751). Its Search Console queries (8-11.2026) are long questions no
heading answered: "מגדלי הים התיכון דיור מוגן יוקרתי איזה סוגי דירות יש ומה גודל ממוצע" (26), "האם אפשר לצאת ולחזור חופשי
מדיור מוגן" (9), "איזה מסמכים צריך להביא להרשמה למגדלי הים התיכון" (6), "אילו שירותים כלולים בדיור מוגן?" (6), "מה העלות
הכוללת של דיור מוגן יוקרתי" (6). Five questions in those words join the page's FAQ (its FAQPage follows, 1.72.569).
Sources (kept here, not on the page): the facts table (פאנדר 27.3.2025; פרויקט תל אביב; ביזפורטל 9.7.2026) for the project;
כל זכות, "דיור מוגן לבני הגיל השלישי" (21.7.2026) and "תשלום פיקדון לבית דיור מוגן" (28.1.2026) for the law. The question
"does it suit someone who does not want to be alone" has no source and is left out.
Backup docs/qa/compound-wave/faq-mh-backup.json; --undo; --dry."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "mh", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "faq-mh-backup.json")
PID = 4751
ANCHOR = '<h2 dir="rtl">שורת סיום והפניות</h2>'
QA = [
    ("אילו סוגי דירות יהיו במגדלי הים התיכון בשדה דב, ומה גודלן?",
     "הפרויקט נמצא בשלבי תכנון (7.2026), ותמהיל הדירות וגודלן טרם פורסמו. ידוע שמתוכננות בו 300 יחידות דיור מוגן, על מגרש 150 בצפון רובע שדה דב, בשטח של 4,663 מ״ר."),
    ("האם אפשר לצאת ולחזור באופן חופשי מדיור מוגן?",
     "דיירי דיור מוגן הם עצמאיים: הם גרים ביחידת דיור משלהם ומשלמים עבור שירותי האחזקה, הניקיון והשמירה שהם מקבלים. כללים כמו היעדרות ארוכה נקבעים בהסכם ההתקשרות עם הבית, ולכן כדאי לבקש אותו ולקרוא אותו לפני החתימה."),
    ("אילו מסמכים צריך להרשמה למגדלי הים התיכון בשדה דב?",
     "רשימת מסמכים להרשמה לבית בשדה דב טרם פורסמה, כי הפרויקט עדיין בתכנון. לפני חתימה על הסכם התקשרות, בית דיור מוגן מוסר לדייר מסמך גילוי ואת ההסכם עצמו, ובהם תנאי הפיקדון, התשלומים והשירותים. שאלות ותלונות על בית דיור מוגן מופנות לממונה על חוק הדיור המוגן במשרד הרווחה."),
    ("אילו שירותים כלולים בדיור מוגן?",
     "דיירי דיור מוגן משלמים עבור שירותי האחזקה, הניקיון והשמירה שהם מקבלים. השירותים שיינתנו בבית בשדה דב טרם פורסמו, ואת הרשימה המלאה מקבלים במסמך הגילוי ובהסכם."),
    ("מה העלות הכוללת של דיור מוגן יוקרתי, ואיך הפיקדון מוגן?",
     "המחירים לבית בשדה דב טרם פורסמו. בדיור מוגן נדרשים הדיירים במקרים רבים להפקיד פיקדון, ובנוסף משלמים תשלומים שוטפים. לפי החוק, בית שמחזיק יותר מ-7% מהפיקדון או יותר מ-70,000 ₪, הנמוך מביניהם, חייב להבטיח את הכסף: במשכנתא ראשונה, בערבות בנקאית או בהעברת 40% מהפיקדון לנאמן. הפיקדון מוחזר ביום שבו מוחזרת הדירה או ביום סיום ההסכם, המאוחר מביניהם, בהצמדה למדד."),
]
for q, a in QA:
    assert "—" not in q + a and "–" not in q + a, q
ADD = "".join(f'<h3 dir="rtl">{q}</h3>\n<p dir="rtl">{a}</p>\n' for q, a in QA)

if "--undo" in ARGV:
    for pid, c in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": c})[0])
    raise SystemExit(0)
cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{PID}?context=edit&_fields=slug,content"), "read mh")
c = cur["content"]["raw"]
if ADD in c:
    print("[done]", PID, cur["slug"]); raise SystemExit(0)
if c.count(ANCHOR) != 1:
    print("[STOP]", PID, "anchor", c.count(ANCHOR)); raise SystemExit(1)
body = c.replace(ANCHOR, ADD + "\n" + ANCHOR)
print(f"[plan] {PID} {cur['slug']}: +{len(QA)} questions at the end of the FAQ")
if "--dry" in ARGV:
    raise SystemExit(0)
if not os.path.exists(BK):
    json.dump({str(PID): c}, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{PID}", {"content": body})
print(f"[faq] {PID} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == body else 'CHECK ' + str(st)}")
