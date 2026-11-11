# -*- coding: utf-8 -*-
"""HAD-712 (Ben 11.11.2026, evening: "what you found in the suggestions goes into the page itself, exactly those keys, those signals").
The manual search of the same evening (docs/research/2026-11-11-kikar-search/manual-2026-11-11/) gave Google's own suggestions for
"כיכר המדינה", "מגדלי כיכר המדינה", "פרויקט כיכר המדינה" and "כיכר המדינה מגדלים". Measured on the live Hebrew article: these were
absent as written: "כיכר המדינה מגדלים", "קבלן", "פרויקט מגורים", "שדרוג" (the municipality's "פרויקט שדרוג כיכר המדינה"), and the
opening had no way to reach the searched topics on a page of 62 phone screens. Six anchored replacements on the LIVE post 8113; no new
number; each sentence stays true and natural. Not added, on purpose: "שמלות ערב" (no source read for the shops), "לוינשטיין" (another
developer's project), "מדלן" (a brand name). md5 pinned; backup before; read-back after; dry by default.
  python scripts/kikar/had712_signals.py [--go]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712s"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
PID, SLUG, PIN = 8113, "hamedina", "b124ffb8ed6a78a6afc98469b4b86e1d"  # modified 2026-11-11T19:40:46 (the plans section)

TOC = (" בעמוד: <a href=\"#nlws-prices\">מחירים ועסקאות</a>, <a href=\"#nlws-homes\">תוכניות דירות</a>, "
       "<a href=\"#nlws-sale\">דירות למכירה ולהשכרה</a>, <a href=\"#nlws-when\">מועד האכלוס</a>, "
       "<a href=\"#nlws-facts\">היזם, הקבלן והכתובת</a>, <a href=\"#nlws-choose\">הגובה ומספר הקומות</a>, "
       "<a href=\"#nlws-square\">החנויות ובתי הקפה</a> ו<a href=\"#nlws-transport\">המפה</a>.")
SWAPS = [
    # 1. the opening: the searched topics, each a link to its section (the suggestions of all four searches)
    ("ולשגרת החיים שאתם מבקשים בעיר.</p>", "ולשגרת החיים שאתם מבקשים בעיר." + TOC + "</p>"),
    # 2. "פרויקט מגורים כיכר המדינה"
    ("<p>פרויקט כיכר המדינה מחבר מגורים במגדלים עם פארק ציבורי בתוך הכיכר.",
     "<p>פרויקט כיכר המדינה הוא פרויקט מגורים: שלושה מגדלים עם פארק ציבורי בתוך הכיכר."),
    # 3. "כיכר המדינה מגדלים", "כיכר המדינה מגדלים קומות"
    ("<p>שני מגדלים בני 40 קומות ומגדל אחד בן 37 קומות. הטבלה מרכזת",
     "<p>בכיכר המדינה מגדלים A ו-C בני 40 קומות ומגדל B בן 37 קומות. הטבלה מרכזת"),
    # 4. "פרויקט כיכר המדינה מחירים"
    ("<p>מחירי הדירות במגדלי כיכר המדינה נבחנים דרך עסקאות שנעשו, לצד הצעות שפורסמו לדירות מסוימות.",
     "<p>המחירים בפרויקט כיכר המדינה נבחנים דרך עסקאות שנעשו במגדלים, לצד הצעות שפורסמו לדירות מסוימות."),
    # 5. "פרויקט כיכר המדינה קבלן", "פרויקט כיכר המדינה אלקטרה"
    ("<p>אלקטרה בנייה ואשטרום בונות במשותף את מגדלי כיכר המדינה, בחוזה ביצוע של כ-1.4 מיליארד ₪.",
     "<p>הקבלן המבצע של פרויקט כיכר המדינה הוא שותפות של אלקטרה בנייה ואשטרום: שתי החברות בונות במשותף את מגדלי כיכר המדינה, בחוזה ביצוע של כ-1.4 מיליארד ₪."),
    # 6. "פרויקט שדרוג כיכר המדינה": the municipality's name for the public works (its page title, seen in the results of 11.11.2026)
    ("זהו פארק ציבורי מתוכנן, לצד שטחי המגורים, ולא גן פרטי של הדיירים.",
     "זהו פארק ציבורי מתוכנן, לצד שטחי המגורים, ולא גן פרטי של הדיירים. עיריית תל אביב-יפו מכנה את הפיתוח הציבורי של הכיכר פרויקט שדרוג כיכר המדינה."),
]
s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
raw = g["content"]["raw"]
now = hashlib.md5(raw.encode("utf-8")).hexdigest()
if now != PIN:
    raise SystemExit("the live post changed since it was read (%s, modified %s): read it again before replacing anything" % (now[:10], g["modified"]))
new = raw
for old, rep in SWAPS:
    c = new.count(old)
    if c != 1:
        raise SystemExit("anchor x%d: %s" % (c, old[:90]))
    new = new.replace(old, rep)
for sid in ("nlws-prices", "nlws-homes", "nlws-sale", "nlws-when", "nlws-facts", "nlws-choose", "nlws-square", "nlws-transport"):
    assert new.count('id="%s"' % sid) == 1, "no section " + sid
assert new.count("<h3>") == raw.count("<h3>") and new.count("<h2>") == raw.count("<h2>")
print("[plan] post %d: %d replacements; %d -> %d chars" % (PID, len(SWAPS), len(raw), len(new)))
if not GO:
    sys.exit(0)
bk = os.path.join(REPO, "docs", "qa", "had-712"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
assert s1 in (200, 201), (s1, str(r1)[:300])
s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
ok = r["content"]["raw"] == new
json.dump({"stamp": stamp, "result": {"post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(), "read_back_equal": ok, "modified": r.get("modified"), "replacements": len(SWAPS)}},
          open(os.path.join(bk, "result-signals-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
if not ok:
    sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
    raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
print("[done] post %d written and read back (%s)" % (PID, stamp))
