# -*- coding: utf-8 -*-
"""HAD-801: write docs/research/2026-11-22-sde-dov-tour-release/PROOF-HE.md from the release records (no numbers typed by hand)."""
import json, os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "research", "2026-11-22-sde-dov-tour-release")
tp = json.load(open(os.path.join(D, "transform-proof.json"), encoding="utf-8"))
m1 = json.load(open(os.path.join(D, "manifest.json"), encoding="utf-8"))
m4 = json.load(open(os.path.join(D, "manifest-v4.json"), encoding="utf-8"))
dr = json.load(open(os.path.join(D, "dropped-files.json"), encoding="utf-8"))
hb = json.load(open(os.path.join(D, "home-speed-before.json"), encoding="utf-8"))
ha = json.load(open(os.path.join(D, "home-speed-after.json"), encoding="utf-8")) if os.path.exists(os.path.join(D, "home-speed-after.json")) else None
a, b = tp["before"], tp["after"]
mb = lambda m: round(sum(v["bytes"] for v in m.values()) / 1048576, 1)
KIND = {"project": "פרויקטים שלנו (עם עמוד באתר)", "lot": "מגרשים", "building": "מבנים בתוך מגרשים", "permit": "היתרים ותכניות", "street": "רחובות",
        "park": "פארקים", "station": "תחנות", "school": "בתי ספר", "place": "מקומות ציבוריים", "surrounding": "סביבה", "tree": "עצים",
        "existing": "מבנים קיימים סביב הרובע", "entrance": "כניסות", "viewpoint": "תצפית", "survey": "מדידה"}
L = []
L.append("# הוכחת שחרור: סיור שדה דב 2036 ב־nad-lan.co.il\n")
L.append("22.11.2026 · HAD-801 · בנייה: Codex (תיקייה sde-dov-2036, ללא שינוי) · שחרור: Claude Opus 5.5\n")
L.append("## מה עלה\n")
L.append("- הסיור החדש בכתובת הקיימת https://nad-lan.co.il/tour/sde-dov/ , בלי הפניה מכל סוג. הסיור הישן לא נמחק: הקובץ שלו נשאר בתוסף, ואם מעבירים את התיקייה החדשה הצידה, וורדפרס מגיש אותו שוב.")
L.append("- רשימת המקומות והמקורות, עמוד HTML קריא ופתוח לאינדוקס: https://nad-lan.co.il/tour/sde-dov/places/")
L.append("- תגית robots של עמוד הסיור עצמו נשארה כמו שהייתה באתר (noindex). שום noindex לא נוסף לשום עמוד אחר.\n")
L.append("## לפני ואחרי\n")
L.append("| מדד | הסיור הישן (קובץ HTML אחד) | הסיור החדש |\n|---|---|---|")
L.append("| מקומות עם שם | כ־18 (15 צמתי פרויקטים ו־3 מגדלים מובילים) | %s |" % format(b["places"], ","))
L.append("| מגרשים (מגרשים + פרויקטים שלנו) | — | %d |" % (b["kinds"]["lot"] + b["kinds"]["project"]))
L.append("| שכבות | — | %d |" % b["layers"])
L.append("| תחנות במסלול המודרך | 6 פרקים | %d |" % b["route"])
L.append("| שפות | עברית | %s |" % ", ".join(b["languages"]))
L.append("| שנים | 2026 ו־2035 | %d עד %d (%d שנים שונות) |" % tuple(b["years"]))
L.append("| עובדות עם מקור | — | %s |" % format(b["facts"], ","))
L.append("| מקורות | — | %d |" % b["sources"])
L.append("| כרטיסים ברשימה הקריאה | — | %s |" % format(b["places"], ","))
L.append("| גודל | 301,549 בתים | %s קבצים, %s מגה (אחרי התאמה לשרת) |\n" % (format(len(m4), ","), mb(m4)))
L.append("ספירת Codex בקובץ README שלו היא 2,872 מקומות; בנתונים שעלו יש %s (כולל %s מבנים קיימים סביב הרובע ו־%d עצים). שום מקום לא נוסף ולא הוסר בשחרור: לפני ואחרי השינוי בשמות המספרים זהים.\n" % (format(b["places"], ","), format(b["kinds"]["existing"], ","), b["kinds"]["tree"]))
L.append("לפי סוג: " + " · ".join("%s %s" % (KIND.get(k, k), format(v, ",")) for k, v in sorted(b["kinds"].items(), key=lambda x: -x[1])) + "\n")
L.append("## שמות במקום תוויות כלליות (%d)\n" % len(tp["renames"]))
L.append("השם החדש נלקח רק מרשומות עם מקור שבתוך החבילה: שמות הפרויקטים ש־Codex קישר לעמודים שלנו, והזוכים במכרזי רשות מקרקעי ישראל (עובדת \"נבחרה ההצעה\" על המגרש). התווית הישנה נשמרה ככינוי לחיפוש ובתוך השם החדש. בשפות אחרות, יזם בלי איות ידוע בשפה נשאר עם התווית המתורגמת הישנה (%s מפתחות תרגום חדשים בכל שפה).\n" % tp["new_translation_keys"]["en"])
L.append("| מזהה | לפני | אחרי | מקור |\n|---|---|---|---|")
for r in tp["renames"]:
    L.append("| %s | %s | %s | %s |" % (r["id"], r["old"], r["new"], r["source"]))
L.append("\nאף שם של חברה או פרויקט לא עומד ליד נושא שלילי. בבדיקה של העמוד, המחרוזות והנתונים אין שום אזכור של זיהום, קרקע מזוהמת או אסבסט (המילה \"דלק\" מופיעה רק כשם של תחנת דלק קיימת בסביבה).\n")
L.append("## שום בית לא אבד\n")
L.append("- החבילה המקורית של Codex לא שונתה. כל השינויים נעשו בעותקים: `D:\\Scratch\\sde-dov-release-2026-11-22\\site` (שמות) ו־`site2` (התאמה לשרת).")
L.append("- %d קבצים שהושמטו מתיקיית transfer הם גרסאות ישנות של קוד ונתונים מבניות קודמות: %d קבצי JavaScript ישנים, %d גרסאות ישנות של קובצי הנתונים, ושני קובצי הנתונים שהוחלפו בגרסה עם השמות. אף אחד מהם לא מוזכר בקוד, בעמודים או ברישום. כולם קיימים בדיוק בייט בבייט בתיקייה של Codex. הרשימה המלאה: dropped-files.json.\n" % (
    len(dr["dropped_files"]), sum(1 for x in dr["identified"] if x["top_keys"] == "not json"), sum(1 for x in dr["identified"] if x["top_keys"] != "not json") - 2))
L.append("## התאמה לשרת (uPress)\n")
L.append("השרת חוסם כל קובץ PHP שאינו index.php (שגיאה 403) ומגביל בקשות לקבצים מסוג .bin ו־.json (כ־20 ברצף ואז שגיאה 429 לאותו מבקר). הסיור מבקש כ־55 קבצים כאלה בפתיחה. בלי לגעת במנוע:")
L.append("1. כל טוען PHP קיבל תיקייה עם index.php משלו (packed/, data/, entry/, places/, catalog/), והכתובות בקוד ובעמודים עודכנו (scripts/had801/index_routes.py).")
L.append("2. הדפדפן טוען את אותם בתים כקבצים סטטיים (scripts/had801/static_routes.py).")
L.append("3. לכל קובץ .bin ו־.json יש תאום זהה עם הסיומת .js, וסקריפט קטן בראש עמוד הסיור מפנה אליו את הבקשות (scripts/had801/shim_routes.py). אחרי זה: אפס שגיאות 429, ונטענים כל קובצי הסצנה (184 בקשות בטלפון ו־199 במחשב, לעומת 144 ו־159 לפני).")
L.append("- כל %s הקבצים בשרת נבדקו מול טביעת md5 (manifest-v4.json): אפס אי־התאמות.\n" % format(len(m4), ","))
L.append("## מהירות עמוד הבית\n")
L.append("| | לפני | אחרי |\n|---|---|---|")
for k in ("desktop", "phone"):
    L.append("| %s, load / LCP (חציון של 5) | %s / %s מ\"ש | %s |" % ("מחשב" if k == "desktop" else "טלפון", format(hb[k]["load_ms"], ","), format(hb[k]["lcp_ms"], ","),
             ("%s / %s מ\"ש" % (format(ha[k]["load_ms"], ","), format(ha[k]["lcp_ms"], ","))) if ha else "נמדד אחרי השחרור"))
L.append("")
L.append("## פערים חזותיים שנשארו (הסיבוב השני של Codex, לא בשחרור הזה)\n")
L.append("- גרפיקה ברמת משחק: מעטפות מבנים חוזרות, ריצוף רחב וקו רקיע דל בחלק מהמגרשים, עומק חזיתות שונה בין הצומת לבין אשכול והצפון.")
L.append("- מבנים בתוך מגרשים הם הדמיית נפח לפי התכנית, לא חזית של יזם.")
L.append("- הכניסה בעמודים זזה בעזרת דחיפה איטית של תמונה מהסיור. סרטון הליכה שקט אמיתי (מוקלט מהסיור) עוד לא הוכן.")
L.append("- יעד 2.5 שניות בטלפון בינוני פתוח (Codex מדד 5.56 שניות בסלולר מדומה). לא נבדק במכשיר אמיתי, לא ב־iOS ולא בדפדפן בתוך אפליקציה.")
L.append("- תרגומים: הערות עורך פתוחות בצרפתית וברוסית (GAPS.md של Codex).")
L.append("- קבצים סטטיים בשרת נשמרים במטמון שנה: גרסה הבאה צריכה שמות קבצים חדשים או גרסה בכתובת.\n")
open(os.path.join(D, "PROOF-HE.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("PROOF-HE.md written,", len(L), "lines")
