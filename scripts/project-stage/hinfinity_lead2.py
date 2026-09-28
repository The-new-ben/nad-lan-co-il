# -*- coding: utf-8 -*-
"""H Infinity's answer paragraph by the project-page checklist (C2): names he+en, developer, exact place, status, unit mix,
a real price with its source and date, what the page lets you do."""
import io, os, re, sys, hashlib, time

REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = io.open(os.path.join(REPO, "scripts", "project-stage", "rainbow_content4.py"), encoding="utf-8").read()
exec(compile(src[src.index("import base64, ctypes"):src.index("FIXES = [")].replace("PID = 4464", "PID = 6548")
             .replace('QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")', 'QA = os.path.join(REPO, "docs", "qa", "hinfinity-content-2026-09-28")'), "head", "exec"))
OLD_START = "<p>במתחם סומייל, החלל הפתוח הגדול האחרון של מרכז תל אביב, בונה קבוצת חג'ג' את H Infinity:"
NEW = ("<p>אייץ' אינפיניטי (H Infinity) של קבוצת חג'ג' נבנה ברחוב אבן גבירול 128, בחלק הצפוני של מתחם סומייל במרכז תל אביב: "
       "מגדל מגורים בן 53 קומות ולצדו בניין בוטיק מעל קומת מסחר, כ-278 דירות של 2 עד 6 חדרים, בתכנון פרופ' משה צור "
       "(לפי הדוח השנתי של החברה לשנת 2025 ודף השיווק). באתר הקבוצה המחירים מתחילים ב-65,000 ₪ למ\"ר (כפי שפורסם בספטמבר 2026). "
       "הפרויקט בבנייה, והחברה מעריכה שעבודות ההקמה יסתיימו ברבעון הרביעי של 2026. "
       "בעמוד: העובדות עם המקור של כל נתון, מחירי העסקאות בסביבה, המפה ושיחת וידאו עם נציג.</p>")
d = read()
raw = d["content"]["raw"]
i = raw.find(OLD_START)
j = raw.find("</p>", i) + 4
assert i == 0 and raw.count(OLD_START) == 1, i
old = raw[i:j]
new = NEW + raw[j:]
print("[old]", re.sub(r"<[^>]+>", "", old)[:120], "...")
print("[new words]", len(re.sub(r"<[^>]+>", "", NEW).split()))
if "--apply" not in sys.argv:
    raise SystemExit(0)
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(QA, "post-6548.raw.%s.before-lead2.html" % stamp), "w", encoding="utf-8").write(raw)
if hashlib.md5(read()["content"]["raw"].encode("utf-8")).hexdigest() != md5:
    raise SystemExit("FATAL: changed while reading")
s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
ok = read()["content"]["raw"] == new
print("[write]", s, "| verified", ok)
