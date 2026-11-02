# -*- coding: utf-8 -*-
"""HAD-654 R10a (Ben 2.11.2026, the moat: "wrapped in the right key phrases, synonyms and intent"): H INFINITY had no FAQ. Its
Search Console queries (8-10.2026) ask where it is and its address, who the developer is (חגג אבן גבירול, אינפיניטי חגג), the
Somail compound and prices (מתחם סומייל מחירים, h infinity מחירים). Six questions in those words go in before the sources section;
every answer repeats a figure the page already gives with its source (facts table, מרכז הנדל״ן 11.10.2026; prices: the group's
site 9.2026, the marketing page, the developer's reports). The FAQPage schema follows from the visible section (inc/instruments.php).
Backup docs/qa/compound-wave/faq-r10a-backup.json; --undo restores it; --dry prints the plan."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "faq", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "faq-r10a-backup.json")

QA = {6548: [
    ("איפה נמצא H INFINITY ומה הכתובת?",
     "H INFINITY נמצא בפינת הרחובות אבן גבירול וז'בוטינסקי בתל אביב, במתחם סומייל, לפי מרכז הנדל״ן (11.10.2026)."),
    ("מי היזם של מגדל אינפיניטי בתל אביב?",
     "היזם הוא קבוצת חג'ג', והקבלן המבצע הוא אלקטרה. את המגדל תכנן האדריכל משה צור."),
    ("כמה קומות ודירות יש ב-H INFINITY?",
     "מגדל מגורים בן 52 קומות עם 278 יחידות דיור, ולצדו בניין בוטיק מעל קומת מסחר. המתקנים: בריכת שחייה, מתחמי ספא וכושר ובר דיירים."),
    ("כמה דירות נשארו למכירה?",
     "לפי הפרסום, עד 8.2026 נמכרו 221 מתוך 278 הדירות (210 חוזים ו-11 בקשות רכישה), ונותרו 57 דירות."),
    ("מתי האכלוס של H INFINITY?",
     "הפרויקט בשלב ביצוע מתקדם, והחברה מעריכה שהאכלוס יהיה ברבעון הראשון של 2027 (10.2026). זו הערכה של החברה, לא התחייבות."),
    ("מה המחירים במגדל אינפיניטי במתחם סומייל?",
     "באתר הקבוצה המחירים מתחילים ב-65,000 ₪ למ\"ר (9.2026), ובדף השיווק מחיר הפתיחה לדירה בפרויקט (2 עד 6 חדרים) הוא 5.82 מיליון ₪. "
     "ממוצע החוזים של 2025 בפרויקט היה כ-7.6 מיליון ₪ לדירה, לפי דוחות היזם. מחירי העסקאות סביב הפרויקט מופיעים בעמוד, ברשימת המחירים."),
]}
ANCHOR = "<h2>מקורות</h2>"


def block(pairs):
    return "<h2>שאלות נפוצות</h2>\n" + "\n".join(f"<h3>{q}</h3>\n<p>{a}</p>" for q, a in pairs) + "\n"


if "--undo" in ARGV:
    for pid, c in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": c})[0])
    raise SystemExit(0)
for t in [x for pairs in QA.values() for p in pairs for x in p]:
    assert "—" not in t and "–" not in t, t
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
for pid, pairs in QA.items():
    cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=slug,content"), f"read {pid}")
    c = cur["content"]["raw"]
    if "<h2>שאלות נפוצות</h2>" in c:
        print("[done]", pid, cur["slug"]); continue
    if c.count(ANCHOR) != 1:
        print("[STOP]", pid, cur["slug"], "anchor found", c.count(ANCHOR)); continue
    body = c.replace(ANCHOR, block(pairs) + ANCHOR)
    print(f"[plan] {pid} {cur['slug']}: {len(pairs)} questions before the sources section")
    if "--dry" in ARGV:
        continue
    if str(pid) not in bk:
        bk[str(pid)] = c; json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": body})
    print(f"[faq] {pid} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == body else 'CHECK ' + str(st)}")
