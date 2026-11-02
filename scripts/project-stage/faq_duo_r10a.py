# -*- coding: utf-8 -*-
"""HAD-654 R10a for DUO (post 4893). DUO already shows 12 questions and answers, under the heading "שאלות ותשובות"; the FAQPage
emitters know only "שאלות נפוצות" (the stage page's one in inc/project-stage.php reads the rendered page and takes the first 12
pairs), so DUO had no FAQ schema. Widening the emitters would add schema to many pages in one day (house law), so only DUO's
heading changes. One question is added second, for the developer queries ("duo אפריקה ישראל", "דואו", "סמל דרום"), in words
the page's developer section already states with its sources. Backup docs/qa/compound-wave/faq-duo-backup.json; --undo; --dry."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "duo", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "faq-duo-backup.json")
PID = 4893
OLD_H = "<h2>שאלות ותשובות</h2>"
NEW_H = "<h2>שאלות נפוצות</h2>"
NEXT = "<h3>מה הגוש והחלקה של הפרויקט?</h3>"
ADD = ("<h3>מי היזם של מגדלי DUO (דואו) בתל אביב?</h3>\n\n"
       "היזם הוא אפריקה ישראל מגורים, ובדוחות החברה הפרויקט מופיע בשם DUO סמל דרום. האדריכלות מיוחסת לישר אדריכלים, "
       "ואלקטרה בילדינג מופיעה כקבלן בפרויקט באתר שלה.\n\n")
assert "—" not in ADD and "–" not in ADD

if "--undo" in ARGV:
    for pid, c in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": c})[0])
    raise SystemExit(0)
cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{PID}?context=edit&_fields=slug,content"), "read duo")
c = cur["content"]["raw"]
if NEW_H in c and ADD in c:
    print("[done]", PID, cur["slug"]); raise SystemExit(0)
if c.count(OLD_H) != 1 or c.count(NEXT) != 1:
    print("[STOP]", PID, "heading", c.count(OLD_H), "next question", c.count(NEXT)); raise SystemExit(1)
body = c.replace(OLD_H, NEW_H).replace(NEXT, ADD + NEXT)
print(f"[plan] {PID} {cur['slug']}: heading -> שאלות נפוצות, +1 question (developer), second")
if "--dry" in ARGV:
    raise SystemExit(0)
if not os.path.exists(BK):
    json.dump({str(PID): c}, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{PID}", {"content": body})
print(f"[faq] {PID} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == body else 'CHECK ' + str(st)}")
