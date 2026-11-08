# -*- coding: utf-8 -*-
"""HAD-684 (Ben 8.11.2026, "תדליק מנוע עדכונים אוטומטי... תבצע את זה"): the privacy policy (page 396) says what the price-update
sign-up and the automatic alerts do, before the engine is switched on (the switch screen asks for exactly this sentence). Two exact
edits on the raw content, a backup, a read-back; --undo restores the backup. Nothing else on the page changes."""
import json, os, sys, time
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H); os.chdir(os.path.dirname(os.path.dirname(H)))
UNDO = "--undo" in sys.argv[1:]
src = open(os.path.join(H, "deploy612.py"), encoding="utf-8").read()
sys.argv = ["deploy612.py", "--finish"]
ns = {"__name__": "cms612", "__file__": os.path.join(H, "deploy612.py")}
exec(compile(src[:src.index("def page(path):")], "deploy612", "exec"), ns)
req, must = ns["req"], ns["must"]
QA = os.path.join(os.path.dirname(os.path.dirname(H)), "docs", "qa", "project-stage-2026-09-24")
BK = os.path.join(QA, "cms-612-privacy-396-backup.json")
PID = 396
EDITS = [
    ("<p>מלבד האמור לעיל, מידע נמסר לספקי שירות חיוניים בלבד, כגון ספק הסליקה, שירותי אחסון ושירותי מדידה, לצורך הפעלת האתר.</p>",
     "<p>מלבד האמור לעיל, מידע נמסר לספקי שירות חיוניים בלבד, כגון ספק הסליקה, שירותי אחסון, שירות שליחת מיילים ושירותי מדידה, לצורך הפעלת האתר.</p>"),
    ("<p>לא יישלח אליכם דיוור פרסומי ללא הסכמתכם המפורשת, וניתן לבטל את ההסכמה בכל עת בפנייה אלינו.</p>",
     "<p>לא יישלח אליכם דיוור פרסומי ללא הסכמתכם המפורשת, וניתן לבטל את ההסכמה בכל עת בפנייה אלינו.</p>\n"
     "<p>עדכוני מחירים והתראות: מי שנרשם באתר לעדכוני מחירים או להתראות מקבל קודם מייל אישור, ועדכונים אוטומטיים נשלחים רק אחרי שאישר. "
     "בכל מייל יש קישור להסרה בלחיצה אחת. הטלפון והמייל שנמסרו בהרשמה נשמרים אצלנו לצורך העדכונים ופנייה בעקבותיהם, "
     "ואינם מועברים ליזם, למתווך או לכל גורם אחר בלי הסכמה נפרדת.</p>"),
]


def get():
    return must(*req("GET", f"/wp-json/wp/v2/pages/{PID}?context=edit&_fields=id,slug,content,modified"), "read 396")


cur = get()
raw = cur["content"]["raw"]
if UNDO:
    bk = json.load(open(BK, encoding="utf-8"))
    must(*req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": bk["content"]}), "undo 396")
    print("[undo] restored", len(bk["content"]), "chars")
    raise SystemExit(0)
if EDITS[1][1].split("\n")[1] in raw:
    print("[skip] the sentence is already there"); raise SystemExit(0)
new = raw
for a, b in EDITS:
    n = new.count(a)
    assert n == 1, ("anchor x%d" % n, a[:60])
    new = new.replace(a, b)
if not os.path.exists(BK):
    json.dump({"page": PID, "modified": cur["modified"], "content": raw, "at": time.strftime("%Y-%m-%d %H:%M")}, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[backup]", BK)
must(*req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": new}), "write 396")
back = get()["content"]["raw"]
assert back == new, "read-back differs"
s, b = req("GET", "/%d7%9e%d7%93%d7%99%d7%a0%d7%99%d7%95%d7%aa-%d7%a4%d7%a8%d7%98%d7%99%d7%95%d7%aa/?nlv=" + str(int(time.time())), raw=True, auth=False, timeout=90)
html = b.decode("utf-8", "replace")
print("[public]", s, "| new sentence:", "עדכוני מחירים והתראות:" in html, "| mail service:", "שירות שליחת מיילים" in html)
print("PRIVACY UPDATED")
