# -*- coding: utf-8 -*-
"""HAD-712 (Ben 11.11.2026, evening: "people also search for plans; push the word plans into the title"). Before the title promises
plans, the page answers the search: Google suggests "כיכר המדינה מגדלים תוכניות דירות" (manual search of 11.11.2026, screenshots in
docs/research/2026-11-11-kikar-search/manual-2026-11-11/), and the Hebrew article had the word "תוכניות" once. This adds one h3 with
that phrase under the apartments section: what was published (the sizes already in the table above it), that official plans were
not published, and how to get the plan of a specific apartment. No new fact: every number is from the table in the same section.
One anchored insertion on the LIVE post 8113; md5 pinned; backup before; read-back after; dry by default.
  python scripts/kikar/had712_plans.py [--go]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712p"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
PID, SLUG, PIN = 8113, "hamedina", "6445338ea576c0df607981d41232d2fb"  # modified 2026-11-11T18:57:49 (the opening sentence)
OLD = "<td>57 מ״ר של שטחי חוץ</td></tr></tbody></table><figure class=\"nlws-fig\">"
PLANS = ("<h3>תוכניות דירות במגדלי כיכר המדינה</h3>"
         "<p>תוכניות דירה רשמיות לא פורסמו לציבור: הדירות שייכות לבעלי הקרקע, ואת תוכנית הדירה מקבלים מהמוכר שלה. מה שפורסם בעסקאות ובמודעות הוא הגדלים שבטבלה: דירות 4 חדרים בשטח של 132 עד 148 מ״ר, חלקן עם מרפסת של 14 עד כ-15.5 מ״ר, דירת 5 חדרים של 154 מ״ר עם מרפסת של 12 מ״ר, דירה של 168 מ״ר, ופנטהאוז של 258 מ״ר עם 57 מ״ר של שטחי חוץ. המעטפת מסתובבת מקומה לקומה, ולכן גם דירות באותו גודל אינן זהות בתוכנית: כיוון הסלון והמרפסת משתנה לאורך המגדל.</p>"
         "<p>לפני השוואת מחירים, בקשו את תוכנית הדירה המסוימת ואת תוכנית הקומה, ובדקו בהן את כיווני הפתחים, את מיקום הכניסה ביחס למעליות ואת שטח המרפסת. באולם התצוגה שבראש העמוד אפשר לבחור מגדל, קומה וכיוון ולראות לאן הדירה פונה, עוד לפני שמבקשים את התוכנית מהמוכר.</p>"
         "<p><a class=\"nlws-wa\" href=\"#nlws-wa\">לקבלת פרטים נוספים בוואטסאפ</a></p>")
NEW = "<td>57 מ״ר של שטחי חוץ</td></tr></tbody></table>" + PLANS + "<figure class=\"nlws-fig\">"
s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
raw = g["content"]["raw"]
now = hashlib.md5(raw.encode("utf-8")).hexdigest()
if now != PIN:
    raise SystemExit("the live post changed since it was read (%s, modified %s): read it again before replacing anything" % (now[:10], g["modified"]))
assert raw.count(OLD) == 1, raw.count(OLD)
assert raw.count("<a class=\"nlws-wa\" href=\"#nlws-wa\">לקבלת פרטים נוספים בוואטסאפ</a>") >= 1, "the existing WhatsApp link wording is not in the post"
new = raw.replace(OLD, NEW)
assert new.count("<h3>") == raw.count("<h3>") + 1
print("[plan] post %d: the plans section; %d -> %d chars" % (PID, len(raw), len(new)))
if not GO:
    sys.exit(0)
bk = os.path.join(REPO, "docs", "qa", "had-712"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
assert s1 in (200, 201), (s1, str(r1)[:300])
s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
ok = r["content"]["raw"] == new
json.dump({"stamp": stamp, "result": {"post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(), "read_back_equal": ok, "modified": r.get("modified")}},
          open(os.path.join(bk, "result-plans-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
if not ok:
    sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
    raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
print("[done] post %d written and read back (%s)" % (PID, stamp))
