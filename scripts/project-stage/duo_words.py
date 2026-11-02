# -*- coding: utf-8 -*-
"""HAD-654, finding from R10a (2.11.2026): the DUO article (post 4893) shows visitors the internal word "דוסייה" 54 times
("אין בדוסייה...", "הדוסייה לא אימתה"). language-dna: no internal or technical talk on a sales page. The noun becomes "המקורות"
(with the verbs agreeing); no fact and no number changes: the script stops unless the page's digits are the same before and after,
and unless no "דוסיי" is left. Backup docs/qa/compound-wave/duo-words-backup.json; --undo; --dry."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "duow", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "duo-words-backup.json")
PID = 4893
PAIRS = [  # specific phrases first (grammar), then the plain prepositional forms
    ("על בסיס דוסייה מקורות:", "על בסיס המקורות:"),
    ("הדוסייה מאמתת", "המקורות מאמתים"),
    ("בדוסייה שנאספה לפרויקט נמצאו מקורות רבים", "לפרויקט נאספו מקורות רבים"),
    ("לא פורסם בדוסייה", "לא פורסם"),
    ("לא פורסמה בדוסייה", "לא פורסמה"),
    ("הדוסייה אינה כוללת", "המקורות אינם כוללים"),
    ("שהדוסייה לא אימתה", "שהמקורות לא אימתו"),
    ("הדוסייה מציינת", "המקורות מציינים"),
    ("הדוסייה מצאה מרפאת", "במקורות נמצאה מרפאת"),
    ("הדוסייה מצאה קודי דירות", "במקורות נמצאו קודי דירות"),
    ("אך לא מצאה מקור שממפה", "אך לא נמצא מקור שממפה"),
    ("הדוסייה לא מצאה גובה רשמי", "לא נמצא גובה רשמי"),
    ("הדוסייה אינה מספקת", "המקורות אינם מספקים"),
    ("הדוסייה מציגה את הפרויקט", "המקורות מציגים את הפרויקט"),
    ("כאשר הדוסייה סיווגה את התאריך כ-", "כאשר תאריך הפרסום הוא "),
    ("מהדוסייה", "מהמקורות"),
    ("מאחר שהדוסייה מציגה", "מאחר שהמקורות מציגים"),
    ("הדוסייה אינה מציגה", "המקורות אינם מציגים"),
    ("על נתוני הדוסייה שנאספה לפרויקט", "על המקורות שנאספו לפרויקט"),
    ("המקורות ששימשו לדוסייה", "המקורות ששימשו למאמר"),
    ("תחום החינוך בדוסייה חלקי בלבד", "המידע על חינוך במקורות חלקי בלבד"),
    ("בדוסייה", "במקורות"),
]
digits = lambda s: sorted(re.findall(r"\d+", re.sub(r"<[^>]+>", " ", s)))

if "--undo" in ARGV:
    for pid, c in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": c})[0])
    raise SystemExit(0)
cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{PID}?context=edit&_fields=slug,content"), "read duo")
c0 = cur["content"]["raw"]
if "דוסיי" not in c0:
    print("[done]", PID, cur["slug"]); raise SystemExit(0)
c = c0
for a, b in PAIRS:
    c = c.replace(a, b)
left = len(re.findall("דוסיי", c))
if left or digits(c) != digits(c0):
    print("[STOP]", PID, "left:", left, "digits same:", digits(c) == digits(c0)); raise SystemExit(1)
print(f"[plan] {PID} {cur['slug']}: {len(re.findall('דוסיי', c0))} uses of the word replaced, digits unchanged")
if "--dry" in ARGV:
    for a, b in PAIRS[:6]: print("   e.g.", a, "->", b)
    raise SystemExit(0)
if not os.path.exists(BK):
    json.dump({str(PID): c0}, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{PID}", {"content": c})
print(f"[words] {PID} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == c else 'CHECK ' + str(st)}")
