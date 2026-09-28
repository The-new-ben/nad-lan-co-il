# -*- coding: utf-8 -*-
"""DUO's page text with the developer's latest report (28.9.2026; Linear HAD-365). The research of 28.9
(docs/research/2026-09-28-duo/duo-deals.md) found the article on Q1 2026 figures and one price without its VAT basis:
  - Africa Israel Residences' Q2 2026 report (https://res.afi-g.com/about/Documents/2026/Q2-2026.pdf): section 1.3, 372
    signed contracts of the 510 marketable units at 30.6.2026 (138 left); section 7.13.2, 71K ₪/m² before VAT in the
    contracts of 1-6.2026; section 3.5, 12 units sold in 1-6.2026, 10,985K ₪ average per unit including VAT;
  - Calcalist's 76.5K ₪/m² for Q1 2026 matches the company's Q1 figure, 64.8K before VAT, with 18% VAT added (calculated);
  - the CEO told Globes on 19.4.2026 that Form 4 in Q2 2027 is realistic.
Nothing is removed: each figure is added next to the older one, with its date and basis. Same mechanism as
dimri_first_line.py: raw content over REST (the app password decrypted in-process, never printed), each fix must match
exactly once, guarded by the md5 of the content read just before; the old raw content is saved first.
  python scripts/project-stage/duo_sales_update.py            # show
  python scripts/project-stage/duo_sales_update.py --apply    # write"""
import io, os, sys, hashlib, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = io.open(os.path.join(REPO, "scripts", "project-stage", "rainbow_content4.py"), encoding="utf-8").read()
exec(compile(src[src.index("import base64, ctypes"):src.index("FIXES = [")].replace("PID = 4464", "PID = 4893")
             .replace('QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")', 'QA = os.path.join(REPO, "docs", "qa", "duo-content-2026-09-28")'), "head", "exec"))
Q2 = "לפי דוח החברה לרבעון השני של 2026"
FIXES = [
    # the facts card's price
    ("<span class=\"value\">אין מחירון יזם פומבי. מקורות ברשת מציגים 65 א׳ ₪ למ״ר; כלכליסט דיווח על 76.5 אלף שקל למ״ר ברבעון הראשון של 2026; דוח החברה מציג 69.9 אלף שקל למ״ר לפני מע״מ בחוזים שנחתמו בשנת 2025</span>",
     "<span class=\"value\">אין מחירון יזם פומבי. " + Q2 + ": כ-71 אלף שקל למ״ר לפני מע״מ בחוזים שנחתמו בינואר עד יוני 2026. מקורות ברשת מציגים 65 א׳ ₪ למ״ר; כלכליסט דיווח על 76.5 אלף שקל למ״ר ברבעון הראשון של 2026, מספר שכולל מע״מ; דוח החברה מציג 69.9 אלף שקל למ״ר לפני מע״מ בחוזים שנחתמו בשנת 2025</span>"),
    # the sales paragraph: the latest figure after the 2025 report
    ("זהו מקור חזק אך הוא מבוסס על תאריך ועל בסיס זכויות מוגדר.",
     "זהו מקור חזק אך הוא מבוסס על תאריך ועל בסיס זכויות מוגדר. הנתון המעודכן ביותר: " + Q2 + ", עד 30.6.2026 נחתמו 372 חוזים מתוך 510 הדירות לשיווק, ונותרו 138. במחצית הראשונה של 2026 נמכרו 12 דירות, במחיר ממוצע של כ-11 מיליון שקל לדירה כולל מע״מ."),
    # the price paragraph: Calcalist's figure and its VAT basis
    ("במחיר ממוצע לדירה 10.5 מיליון שקל ובמחיר ממוצע למ״ר 76.5 אלף שקל.",
     "במחיר ממוצע לדירה 10.5 מיליון שקל ובמחיר ממוצע למ״ר 76.5 אלף שקל. המספר הזה תואם את 64.8 אלף שקל למ״ר לפני מע״מ בדוח החברה לאותו רבעון, בתוספת מע״מ של 18%. " + Q2 + ", בחוזים שנחתמו בינואר עד יוני 2026 המחיר הממוצע היה כ-71 אלף שקל למ״ר לפני מע״מ."),
    # the completion row
    ("<td>2027 לפי דוח אפריקה ישראל מגורים ולפי Ynet/CTech; דף אלקטרה מציין דצמבר 2026</td>",
     "<td>2027 לפי דוח אפריקה ישראל מגורים ולפי Ynet/CTech; מנכ״ל החברה אמר לגלובס (19.4.2026) שטופס 4 ברבעון השני של 2027 ריאלי; דף אלקטרה מציין דצמבר 2026</td>"),
    # the questions: sales now
    ("כלכליסט דיווח ב-2026 על 144 דירות שטרם נמכרו מתוך 510 ועל 9 מכירות ברבעון הראשון של 2026.",
     "כלכליסט דיווח ב-2026 על 144 דירות שטרם נמכרו מתוך 510 ועל 9 מכירות ברבעון הראשון של 2026. " + Q2 + ", עד 30.6.2026 נמכרו 372 מתוך 510 ונותרו 138."),
]
d = read()
raw = d["content"]["raw"]
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
new, bad = raw, []
for a, b in FIXES:
    n = new.count(a)
    print("[fix] x%d  %s..." % (n, a[:60]))
    if n != 1:
        bad.append(a[:60])
        continue
    new = new.replace(a, b)
if bad:
    raise SystemExit("FATAL: anchors not found exactly once: %r" % bad)
print("[plan] %d fixes, %d -> %d chars, md5 %s" % (len(FIXES), len(raw), len(new), md5[:10]))
if not APPLY:
    raise SystemExit(0)
os.makedirs(QA, exist_ok=True)
io.open(os.path.join(QA, "duo-4893-before-%s.html" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8").write(raw)
again = hashlib.md5(read()["content"]["raw"].encode("utf-8")).hexdigest()
if again != md5:
    raise SystemExit("FATAL: the content changed while this ran; read it again")
s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
print("[write]", s)
after = read()["content"]["raw"]
print("[verify] written:", hashlib.md5(after.encode("utf-8")).hexdigest() == hashlib.md5(new.encode("utf-8")).hexdigest())
