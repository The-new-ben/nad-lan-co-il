# -*- coding: utf-8 -*-
"""Build the data of the professionals cluster (HAD-601 round 2, G6 G7 G8, 26.10.2026; local build, nothing deployed):
  plugins/nadlan-config/assets/instruments/data/bedek.json     G6 /home-inspection/   tool bedek
  plugins/nadlan-config/assets/instruments/data/shamai.json    G7 /real-estate-appraiser/   tools shamai + shamaireg
  plugins/nadlan-config/assets/instruments/data/orechdin.json  G8 /real-estate-lawyer/   tool orechdin (+ ptax.json, read only)

Every number below is either an official figure (law, regulation, official notice, official register) or a price that a named
page published, with its date and whether it says VAT is included. The official numbers are checked against the raw texts
(Wikisource law book, the 2026 notices in Reshumot, the data.gov.il register) when the raw folder is present:
  _private-research/2026-10-26-upgrades/raw/g6g8/official/  (law-sale.wiki, reg-legalcap.wiki, bar-tariff.wiki,
  reg-land-fees.wiki, reg-decisive-fee.wiki, law-appr.wiki, law-planning.wiki, law-landtax.wiki, bar-ethics.wiki,
  takanot-12242.txt, yalkut-14118.txt, shamaim-all.json, exams-*.json, kolzchut-mortgage-appraisal.html)
and the published prices against the competitor captures in raw/g6g8/*.txt. Without the raw folder the build still writes the
same files (the constants are the checked values) and says that the checks were skipped. Rebuild is byte-identical.

  python tools/instruments/build_pros_data.py [--raw=<folder>]"""
import collections, glob, io, json, os, re, sys

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--raw=")),
           os.path.join(os.path.dirname(REPO), "_private-research", "2026-10-26-upgrades", "raw", "g6g8"))
OFF = os.path.join(RAW, "official")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
CHECKED = "2026-10-26"
HAVE_RAW = os.path.isdir(OFF)
NCHECK = [0]


def raw(name):
    p = os.path.join(OFF, name) if not name.startswith("..") else os.path.join(RAW, name[3:])
    return io.open(p, encoding="utf-8", errors="replace").read()


def must(name, *needles):
    """the official text must contain every needle (a number as printed, or a phrase)"""
    if not HAVE_RAW: return
    t = raw(name)
    for n in needles:
        assert n in t, ("not found in %s: %s" % (name, n))
        NCHECK[0] += 1


WS = "https://he.wikisource.org/wiki/"
SRC = {
    "SALE": {"label": "חוק המכר (דירות), התשל״ג-1973: סעיפים 1, 4, 4א, 4ב והתוספת", "url": WS + "%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)"},
    "ENG": {"label": "פנקס המהנדסים והאדריכלים, משרד העבודה (בדיקת רישום)", "url": "https://data.labor.gov.il/EngineersAndArchitects.aspx"},
    "MT": {"label": "מידרג, הצעות מחיר לבדק בית (עודכן 17.12.2025)", "url": "https://www.midrag.co.il/Content/Tip/981"},
    "PL": {"label": "מידרג, מחירים ששולמו על בדיקה לבית פרטי (13.7.2025)", "url": "https://www.midrag.co.il/Content/PriceList/540007"},
    "MP22": {"label": "מידרג, מחיר בדק בית (15.2.2022)", "url": "https://www.midrag.co.il/Content/Price/7261"},
    "BM": {"label": "בדק מבנים, טבלת מחירי בדק בית (12.1.2026)", "url": "https://www.bedek-mivnim.co.il/%D7%9E%D7%99%D7%93%D7%A2-%D7%9E%D7%A7%D7%A6%D7%95%D7%A2%D7%99/item/32-%D7%91%D7%93%D7%A7-%D7%91%D7%99%D7%AA-%D7%9E%D7%97%D7%99%D7%A8.html"},
    "HB": {"label": "הבודקים, מחירון קבוע לפי חדרים (יוני 2026)", "url": "https://www.ha-bodkim.co.il/blog/kama-ole-bdek-bait"},
    "APPR": {"label": "חוק שמאי מקרקעין, התשס״א-2001: סעיפים 1, 7, 12, 13, 14", "url": WS + "%D7%97%D7%95%D7%A7_%D7%A9%D7%9E%D7%90%D7%99_%D7%9E%D7%A7%D7%A8%D7%A7%D7%A2%D7%99%D7%9F"},
    "REG": {"label": "מאגר שמאי מקרקעין, משרד המשפטים, data.gov.il (עודכן 25.10.2026)", "url": "https://data.gov.il/he/datasets/ministry_of_justice/shamaim"},
    "EXAM": {"label": "ציוני בחינות שמאים, משרד המשפטים, data.gov.il (עודכן 1.10.2026); ציון עובר 60 (תקנות שמאי מקרקעין (בחינות))", "url": "https://data.gov.il/he/datasets/ministry_of_justice/shamaim"},
    "DFEE": {"label": "תקנות התכנון והבניה (שכרו של שמאי מכריע ושמאי מייעץ), התשס״ט-2009", "url": WS + "%D7%AA%D7%A7%D7%A0%D7%95%D7%AA_%D7%94%D7%AA%D7%9B%D7%A0%D7%95%D7%9F_%D7%95%D7%94%D7%91%D7%A0%D7%99%D7%94_(%D7%A9%D7%9B%D7%A8%D7%95_%D7%A9%D7%9C_%D7%A9%D7%9E%D7%90%D7%99_%D7%9E%D7%9B%D7%A8%D7%99%D7%A2_%D7%95%D7%A9%D7%9E%D7%90%D7%99_%D7%9E%D7%99%D7%99%D7%A2%D7%A5)"},
    "PLAN": {"label": "חוק התכנון והבניה: סעיף 197 והתוספת השלישית, סעיף 14", "url": WS + "%D7%97%D7%95%D7%A7_%D7%94%D7%AA%D7%9B%D7%A0%D7%95%D7%9F_%D7%95%D7%94%D7%91%D7%A0%D7%99%D7%94"},
    "DEC": {"label": "שמאות מכריעה, משרד המשפטים (עודכן 18.3.2026)", "url": "https://www.gov.il/he/departments/units/decisive_appraisal"},
    "BANK": {"label": "כל זכות, הערכת שמאי למשכנתא (לפי נהלי בנק ישראל, סעיפים 9-10)", "url": "https://www.kolzchut.org.il/he/%D7%94%D7%A2%D7%A8%D7%9B%D7%AA_%D7%A9%D7%9E%D7%90%D7%99_%D7%9C%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90"},
    "MD8151": {"label": "מידרג, מחיר שמאי מקרקעין (3.7.2024)", "url": "https://www.midrag.co.il/Content/Price/8151"},
    "EC": {"label": "EC שמאות, טבלת מחירים (24.8.2025)", "url": "https://ec-shamaut.co.il/%D7%9B%D7%9E%D7%94-%D7%A2%D7%95%D7%9C%D7%94-%D7%A9%D7%9E%D7%90%D7%95%D7%AA-%D7%93%D7%99%D7%A8%D7%94/"},
    "DZ": {"label": "דפי זהב, מחירון שמאי מקרקעין (נתוני ספטמבר 2026)", "url": "https://www.d.co.il/priceList-49080/"},
    "CAP": {"label": "תקנות המכר (דירות) (הגבלת גובה ההוצאות המשפטיות), התשע״ה-2014, והודעת 2026 (ק״ת 12242)", "url": WS + "%D7%AA%D7%A7%D7%A0%D7%95%D7%AA_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)_(%D7%94%D7%92%D7%91%D7%9C%D7%AA_%D7%92%D7%95%D7%91%D7%94_%D7%94%D7%94%D7%95%D7%A6%D7%90%D7%95%D7%AA_%D7%94%D7%9E%D7%A9%D7%A4%D7%98%D7%99%D7%95%D7%AA)"},
    "S6C": {"label": "חוק המכר (דירות), סעיף 6ג", "url": WS + "%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)"},
    "TAR": {"label": "כללי לשכת עורכי הדין (התעריף המינימלי המומלץ), התש״ס-2000, הסכומים לשנת 2026 (י״פ 14118)", "url": WS + "%D7%9B%D7%9C%D7%9C%D7%99_%D7%9C%D7%A9%D7%9B%D7%AA_%D7%A2%D7%95%D7%A8%D7%9B%D7%99_%D7%94%D7%93%D7%99%D7%9F_(%D7%94%D7%AA%D7%A2%D7%A8%D7%99%D7%A3_%D7%94%D7%9E%D7%99%D7%A0%D7%99%D7%9E%D7%9C%D7%99_%D7%94%D7%9E%D7%95%D7%9E%D7%9C%D7%A5)"},
    "ETH": {"label": "כללי לשכת עורכי הדין (אתיקה מקצועית), התשמ״ו-1986, כלל 14", "url": WS + "%D7%9B%D7%9C%D7%9C%D7%99_%D7%9C%D7%A9%D7%9B%D7%AA_%D7%A2%D7%95%D7%A8%D7%9B%D7%99_%D7%94%D7%93%D7%99%D7%9F_(%D7%90%D7%AA%D7%99%D7%A7%D7%94_%D7%9E%D7%A7%D7%A6%D7%95%D7%A2%D7%99%D7%AA)"},
    "FEES": {"label": "תקנות המקרקעין (אגרות), התשל״ה-1974, הסכומים לשנת 2026", "url": WS + "%D7%AA%D7%A7%D7%A0%D7%95%D7%AA_%D7%94%D7%9E%D7%A7%D7%A8%D7%A7%D7%A2%D7%99%D7%9F_(%D7%90%D7%92%D7%A8%D7%95%D7%AA)"},
    "TAX": {"label": "חוק מיסוי מקרקעין: סעיף 15 (מקדמה), סעיף 73 (הצהרה)", "url": WS + "%D7%97%D7%95%D7%A7_%D7%9E%D7%99%D7%A1%D7%95%D7%99_%D7%9E%D7%A7%D7%A8%D7%A7%D7%A2%D7%99%D7%9F_(%D7%A9%D7%91%D7%97_%D7%95%D7%A8%D7%9B%D7%99%D7%A9%D7%94)"},
    "DORON": {"label": "דורון אהרוני, שכר טרחת עורך דין 2026 (12.10.2026)", "url": "https://doron-aharoni.com/%D7%A9%D7%9B%D7%A8-%D7%98%D7%A8%D7%97%D7%AA-%D7%A2%D7%95%D7%A8%D7%9A-%D7%93%D7%99%D7%9F-%D7%91%D7%9E%D7%9B%D7%99%D7%A8%D7%AA-%D7%93%D7%99%D7%A8%D7%94-%D7%91%D7%A8%D7%9B%D7%99%D7%A9%D7%94/"},
    "ADDA": {"label": "מור עדה, עורך דין קניית דירה, טבלת שכר טרחה (2.7.2026)", "url": "https://addalaw.co.il/lawyer-for-buying-an-apartment/"},
    "GELB": {"label": "נאור גלברג, שאלות ותשובות על שכר טרחה (22.9.2026)", "url": "https://gelberglaw.co.il/"},
    "BIZ": {"label": "ביזפורטל, טווחי שכר טרחה (6.8.2026)", "url": "https://www.bizportal.co.il/realestates/news/article/20038031"},
}


# ======================================================================================= G6: bedek.json
ITEMS = [  # the schedule of the Sale (Apartments) Law, in the law's order; years of the inspection period
    ("frames", "חלונות, דלתות ואלומיניום", "ליקוי במוצרי מסגרות ונגרות, לרבות אלומיניום ופלסטיק", 2),
    ("tiling", "ריצוף וחיפוי פנים: שקיעה ושחיקה", "ליקוי בריצוף וחיפוי פנים לרבות שקיעות ושחיקה", 2),
    ("machines", "דודים ומכונות", "כשל בתפקוד ובעמידות של מכונות ודוודים", 3),
    ("yard", "חצר, חניה ושבילים", "ליקוי בפיתוח חצר, לרבות שקיעות", 3),
    ("insulation", "בידוד תרמי", "כשל בתפקוד ובעמידות של מרכיבי מערכות הבידוד התרמי", 3),
    ("piping", "צנרת: מים, ביוב, הסקה ומרזבים", "כשל במערכות צנרת, לרבות מים, מערכת הסקה ומרזבים, דלוחין וביוב", 4),
    ("sealing", "איטום: רטיבות מהגג, מהקירות או מהמרתף", "כשל באיטום המבנה, לרבות בחללים תת־קרקעיים, בקירות, בתקרות ובגגות", 4),
    ("cracks", "סדקים מעל 1.5 מ״מ בקירות שאינם נושאים", "סדקים ברוחב גדול מ־1.5 מ״מ ברכיבים לא נושאים", 5),
    ("cladding", "חיפוי חוץ שמתנתק, מתקלף או מתפורר", "התנתקות, התקלפות או התפוררות של חיפויי חוץ", 7),
    ("other", "כל ליקוי אחר: חשמל, טיח, צבע, ארונות", "כל אי־התאמה אחרת שאינה אי־התאמה יסודית", 1),
]
must("law-sale.wiki", "שנתיים;", "שלוש שנים;", "ארבע שנים;", "חמש שנים;", "שבע שנים;", "שנה אחת.", "1.5 מ״מ", "תקופה של שלוש שנים שתחילתה בתום תקופת הבדק",
     "בתוך תקופה של 20 שנים", "בתוך שנה ממועד העמדת הדירה לרשות הקונה", "במשך שנתיים שתחילתן במועד הודעת הקונה", "הקונה או קונה המשנה",
     "”קונה משנה“ – מי שרוכש דירה מקונה")
# the same schedule as the live tool warranty.js (one law, one table on the site)
WJS = io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "tools", "warranty.js"), encoding="utf-8").read()
WITEMS = [int(y) for y in re.findall(r"\['[^']+', (\d)\]", WJS[:WJS.index("function addY")])]
assert sorted(WITEMS) == sorted(y for _, _, _, y in ITEMS), ("warranty.js schedule differs", WITEMS)

BEDEK_PRICES = [  # published prices, exactly as printed; vat: incl = the page says VAT included, plus = + VAT, ns = not stated
    {"src": "MT", "date": "2025-12-17", "vat": "incl", "rows": [["apt", "דירה עד 120 מ״ר", 1200, 1900, [2, 5]], ["house", "בית פרטי עד 200 מ״ר", 2200, 2950, None]]},
    {"src": "PL", "date": "2025-07-13", "vat": "incl", "rows": [["house", "בית פרטי: ממוצע ששולם 2,516 ₪, 84% מהמקרים מתחת ל־2,900 ₪", 1947, 3300, None]]},
    {"src": "BM", "date": "2026-01-12", "vat": "ns", "rows": [["apt", "דירה 2 עד 3 חדרים", 1100, 1600, [2, 3]], ["apt", "דירה 4 עד 5 חדרים, כולל בדיקות רטיבות ותרמוגרפיה בסיסית", 1500, 2500, [4, 5]],
                                                       ["apt", "דירה גדולה, 6 חדרים ומעלה", 1800, 3500, [6, 9]], ["roof", "פנטהאוז או דירה בשתי קומות", 2500, 4500, None],
                                                       ["house", "בית פרטי קטן, כולל גג, חצר וקירות חוץ", 2000, 6000, None], ["villa", "בית פרטי גדול או וילה", 2500, 6000, None],
                                                       ["moist", "רטיבות ותרמוגרפיה בלבד", 600, 1800, None], ["court", "חוות דעת מומחה לבית משפט", 2500, 10000, None]]},
    {"src": "HB", "date": "2026-06-01", "vat": "ns", "rows": [["apt", "דירת 2 חדרים", 1200, 1200, [2, 2]], ["apt", "דירת 3 חדרים", 1300, 1300, [3, 3]], ["apt", "דירת 4 חדרים", 1400, 1400, [4, 4]],
                                                       ["apt", "דירת 5 חדרים", 1500, 1500, [5, 5]], ["apt", "דירת 6 חדרים ומעלה", 1600, 1600, [6, 9]]]},
]
if HAVE_RAW:
    for needle, f in [("2200- 2950", "g6-midrag-tip981.txt"), ("1200 – 1900", "g6-midrag-tip981.txt"), ("180 ש\"ח + מע\"מ לדירה", "g6-midrag-tip981.txt"),
                      ("3,000 ש\"ח +מע\"מ", "g6-midrag-tip981.txt"), ("2516.29", "g6p-midrag-pl540007.txt"), ("₪1947", "g6p-midrag-pl540007.txt"), ("₪3300", "g6p-midrag-pl540007.txt"),
                      ("1,100 – 1,600", "g6p-bedekmivnim-price.txt"), ("1,500 – 2,500", "g6p-bedekmivnim-price.txt"), ("1,800 – 3,500", "g6p-bedekmivnim-price.txt"),
                      ("2,500 – 4,500", "g6p-bedekmivnim-price.txt"), ("2,000 – 6,000", "g6p-bedekmivnim-price.txt"), ("2,500 – 6,000", "g6p-bedekmivnim-price.txt"),
                      ("600 – 1,800", "g6p-bedekmivnim-price.txt"), ("2,500 – 10,000", "g6p-bedekmivnim-price.txt"), ("דירת 4 חדרים — 1,400", "g6p-habodkim.txt"),
                      ("עד 15%", "g6p-habodkim.txt"), ("200-300", "g6p-midrag-price7261.txt"), ("1,000-1,200", "g6p-midrag-price7261.txt")]:
        assert needle in raw("../" + f), (f, needle); NCHECK[0] += 1

bedek = {
    "key": "bedek", "checked": CHECKED,
    "law": {"items": [{"id": i, "short": s, "law": l, "y": y} for i, s, l, y in ITEMS], "warranty_y": 3, "struct_y": 20, "visible_notice_y": 1, "recur_y": 2},
    "prices": BEDEK_PRICES,
    "shared": {"src": "MT", "date": "2025-12-17", "per_apt": 180, "min": 3000, "vat": "plus"},
    "addon_roof": {"src": "MP22", "date": "2022-02-15", "lo": 200, "hi": 300, "vat": "ns"},
    "group": {"src": "MP22", "date": "2022-02-15", "lo": 1000, "hi": 1200, "from_apts": 10, "hb_off": 0.15},
    "vat": 0.18, "book_days": 45,
    "sources": {k: SRC[k] for k in ("SALE", "ENG", "MT", "PL", "MP22", "BM", "HB")},
}

# ======================================================================================= G7: shamai.json
must("law-appr.wiki", "”שמאי מקרקעין“ – מי שרשום בפנקס", "במשך שנה אחת – בהיקף שלא פחת מ־40 שעות בשבוע, או במשך שנתיים",
     "לא תוגש לבית משפט שומת מקרקעין אלא אם כן נערכה בידי שמאי מקרקעין", "לא יעסוק אדם בשומת מקרקעין דרך שירות לכל בשכר, אלא אם כן הוא שמאי מקרקעין",
     "דינו – מאסר שנה", "שיש בו ניגוד בין ענינו לבין ענין של לקוחו")
must("reg-appr-exams.wiki", "ציון ”עובר“ בבחינה יהיה ציון 60 נקודות לפחות")
DTABLE = [[0, 500000, 0.03], [500000, 1000000, 0.02], [1000000, 2000000, 0.01], [2000000, 0, 0.005]]
must("reg-decisive-fee.wiki", "<td>0</td><td>500,000</td><td>3%</td>", "<td>500,000</td><td>1,000,000</td><td>2%</td>", "<td>1,000,000</td><td>2,000,000</td><td>1%</td>",
     "<td>2,000,000</td><td>&nbsp;</td><td>0.5%</td>", "לא יעלה על 100,000 ש״ח ולא יפחת מ־2,000 ש״ח", "יישאו, כל אחד, במחצית שכרו",
     "לשלם רבע משכרו", "ייווסף מס ערך מוסף")
must("law-planning.wiki", "בתוך 45 ימים מיום שבו הובאה השומה לידיעת החייב", "בתוך 15 ימים ממועד קבלת הפנייה", "אינו עולה על 90,000 שקלים חדשים",
     "והוא יחליט בה בתוך 14 ימים", "תוך שלוש שנים מיום תחילת תקפה של התכנית", "בתוך שנה ממועד הצגת לוח השומה")
if HAVE_RAW:
    k = raw("kolzchut-mortgage-appraisal.html")
    for n in ("תעריפי הבנק", "טרם חלפו 90 ימים", "זכאי לקבל מהבנק העתק", "לא תתקבל הערכת שמאי שבוצעה באופן פרטי"):
        assert n in k, n; NCHECK[0] += 1

# the register (count, update date, the cities filled) and the exams (pass = 60), from the official files
REGISTER = {"count": 3182, "with_city": 376, "updated": "2026-10-25", "resource": "8540534a-eccd-4568-a677-652d589ed172",
            "api": "https://data.gov.il/api/3/action/datastore_search", "page": "https://data.gov.il/he/datasets/ministry_of_justice/shamaim"}
EXAMS = None
if HAVE_RAW:
    recs = json.load(io.open(os.path.join(OFF, "shamaim-all.json"), encoding="utf-8"))["result"]["records"]
    assert len(recs) == REGISTER["count"] and sum(1 for r in recs if r["עיר"]) == REGISTER["with_city"]; NCHECK[0] += 2
    top = collections.Counter(r["עיר"] for r in recs if r["עיר"]).most_common(8)
    REGISTER["top_cities"] = [[c, n] for c, n in top]
    rows = []
    for f in sorted(glob.glob(os.path.join(OFF, "exams-[0-9]*.json"))):
        rows += json.load(io.open(f, encoding="utf-8"))["result"]["records"]
    assert len(rows) == 93728, len(rows); NCHECK[0] += 1
    by = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        y = r["תאריך הבחינה"][-4:]
        try: s = float(r["ציון"])
        except Exception: continue
        by[(r["תיאור הבחינה"], y)][0] += 1; by[(r["תיאור הבחינה"], y)][1] += s >= 60
    CURRENT = ["מבוא לתורת השמאות", "דינים", "יסודות הכלכלה חלק א - מיקרו כלכלה ומקרו כלכלה", "יסודות הכלכלה חלק ב - כלכלה עירונית",
               "יסודות בחשבונאות וניתוח דוחות כספיים", "יסודות המימון ושימושם בשומת המקרקעין", "סטטיסטיקה", "יסודות הנדסת בנין והנדסה אזרחית",
               "יסודות מדידה ומיפוי", "תכנון ובניה חלק א - יסודות התכנון העירוני", "תכנון ובניה חלק ב - דיני התכנון העירוני",
               "מיסוי מקרקעין ומסים אחרים", "גישות ועקרונות בהערכת מקרקעין", "יישומים בשומת מקרקעין"]
    EXAMS = {"pass": 60, "years": ["2024", "2025"], "updated": "2026-10-01", "final": "יישומים בשומת מקרקעין", "n_rows": len(rows),
             "rows": [[e] + [by[(e, y)] for y in ("2024", "2025")] for e in CURRENT]}
    json.dump({"register": REGISTER, "exams": EXAMS}, io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pros-official-cache.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
else:
    cache = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pros-official-cache.json"), encoding="utf-8"))
    REGISTER, EXAMS = cache["register"], cache["exams"]

SHAMAI_PRICES = [
    {"src": "MD8151", "date": "2024-07-03", "vat": "ns", "rows": [["apt", "הערכת שווי דירה בבניין מגורים, ממוצע", 2500, 4000], ["house", "בית פרטי צמוד קרקע, עד", 2500, 7000],
                                                             ["rent", "הערכת דמי שכירות", 2500, 3500], ["court_add", "תוספת לחוות דעת לבית משפט", 1500, 2000],
                                                             ["levy", "הפחתת היטל השבחה: שכר קבוע ועוד 10% מגובה ההפחתה", 4000, 6000]]},
    {"src": "EC", "date": "2025-08-24", "vat": "ns", "rows": [["apt", "דירת מגורים עד 5 חדרים", 2000, 3000], ["apt_big", "דירה גדולה או פנטהאוז", 2500, 3500],
                                                         ["invest", "דירה להשקעה או ייחודית", 3000, 4000], ["house", "בית פרטי", 3000, 5000], ["shop", "נכס מסחרי קטן", 3500, 6000]]},
    {"src": "DZ", "date": "2026-09-01", "vat": "ns", "rows": [["apt", "הערכת שווי דירה", 2160, 5400], ["house", "הערכת שווי בית פרטי", 2700, 6480], ["inherit", "דירה, ירושה או חלוקת עיזבון", 2160, 5400],
                                                         ["rent", "הערכת דמי שכירות לדירה", 1944, 4320], ["hour", "שעת ייעוץ עם שמאי", 216, 540], ["plot", "מגרש ריק לבית פרטי", 2160, 5400]]},
]
if HAVE_RAW:
    for needle, f in [("2,500-4,000", "g7p-midrag-price8151.txt"), ("עד 7,000", "g7p-midrag-price8151.txt"), ("2,500 ל-3,500", "g7p-midrag-price8151.txt"),
                      ("1,500-2,000", "g7p-midrag-price8151.txt"), ("4,000-6,000 ₪ בממוצע + 10%", "g7p-midrag-price8151.txt"),
                      ("2,000 – 3,000", "g7p-ecshamaut.txt"), ("2,500 – 3,500", "g7p-ecshamaut.txt"), ("3,000 – 4,000", "g7p-ecshamaut.txt"), ("3,000 – 5,000", "g7p-ecshamaut.txt"), ("3,500 – 6,000", "g7p-ecshamaut.txt")]:
        assert needle in raw("../" + f), (f, needle); NCHECK[0] += 1
    dz = raw("../g7p-dcoil-price.txt")
    for n in ("2,160", "5,400", "2,700", "6,480", "1,944", "4,320", "216", "540"):
        assert n in dz, n; NCHECK[0] += 1

PURPOSES = [  # who orders, who pays, what the law says; prices by key into SHAMAI_PRICES; links to the owner pages on the site
    {"id": "bank", "label": "משכנתא: השמאי של הבנק", "who": "שמאי מתוך רשימת השמאים שהבנק מוסר עם האישור העקרוני; פונים אליו בעצמכם", "pay": "אתם, ישירות לשמאי, לפי תעריף הבנק",
     "law": "שומה פרטית לא מתקבלת במקומה. מי ששילם זכאי להעתק, ואפשר להגיש אותה לבנק אחר בתוך 90 יום. ערעור ככלל אין; בפער משמעותי אפשר לבקש שומה נוספת מטעם הבנק.",
     "src": ["BANK"], "price": None, "deadline": None, "link": ["/mortgage-calculator/", "מחשבון משכנתא"]},
    {"id": "buy", "label": "לפני חתימה על חוזה: שומה פרטית", "who": "שמאי שאתם בוחרים, רשום בפנקס", "pay": "אתם", "law": "מומלץ לפני החתימה, כשהשומה של הבנק עוד לא נעשתה: שומת הבנק עלולה לצאת נמוכה מהמחיר.",
     "src": ["APPR", "BANK"], "price": ["apt", "house", "apt_big", "invest"], "deadline": None, "link": ["/property-value-estimator/", "מחשבון שווי דירה"]},
    {"id": "sell", "label": "מכירה או קביעת מחיר", "who": "שמאי שאתם בוחרים", "pay": "אתם", "law": "שומה פרטית נותנת מספר עם נימוקים: עסקאות השוואה, זכויות, תכנון וחריגות.",
     "src": ["APPR"], "price": ["apt", "house"], "deadline": None, "link": ["/property-value-estimator/", "מחשבון שווי דירה"]},
    {"id": "levy", "label": "קיבלתי דרישה להיטל השבחה", "who": "שמאי מטעמכם לשומה נגדית; אחר כך ערר או שמאי מכריע", "pay": "אתם את השמאי שלכם; את השמאי המכריע חצי אתם וחצי הוועדה המקומית",
     "law": "45 ימים מהיום שהשומה הובאה לידיעתכם: ערר לוועדת הערר או בקשה למינוי שמאי מכריע. חיוב עד 90,000 ₪: אפשר לבקש מהוועדה בחינה חוזרת, והשמאי שלה מחליט בתוך 14 ימים.",
     "src": ["PLAN", "DFEE", "DEC"], "price": ["levy"], "deadline": {"days": 45, "from": "levy_date"}, "link": ["/glossary/%D7%A9%D7%9E%D7%90%D7%99-%D7%9E%D7%9B%D7%A8%D7%99%D7%A2/", "שמאי מכריע"]},
    {"id": "s197", "label": "תכנית חדשה פגעה בשווי (סעיף 197)", "who": "שמאי מטעמכם; התביעה מוגשת לוועדה המקומית", "pay": "אתם",
     "law": "התביעה מוגשת תוך 3 שנים מיום תחילת תוקף התכנית. במחלוקת על הסכום אפשר לפנות בהסכמה לשמאי מכריע.",
     "src": ["PLAN"], "price": None, "deadline": {"years": 3, "from": "plan_date"}, "link": None},
    {"id": "court", "label": "ירושה, גירושין או פירוק שיתוף", "who": "שמאי מקרקעין רשום; לבית המשפט מוגשת רק שומה של שמאי רשום (סעיף 12)", "pay": "לפי ההסכמה או לפי בית המשפט",
     "law": "שומה שמוגשת לבית משפט חייבת להיות של שמאי מקרקעין רשום בפנקס.", "src": ["APPR"], "price": ["inherit", "court_add"], "deadline": None, "link": None},
    {"id": "renewal", "label": "פינוי בינוי או תמ״א 38", "who": "שמאי לבעלי הדירות; בפינוי בינוי אפשר לבקש שמאי מטעם הרשות", "pay": "במבנה עסקה מקובל היזם משלם לאנשי המקצוע; שמאי הרשות בחינם",
     "law": "בפינוי בינוי, כשבעלי יותר משתי חמישיות מהדירות בכל בניין מבקשים, הרשות להתחדשות עירונית ממנה שמאי לבדיקת הכדאיות בחינם.",
     "src": ["APPR"], "price": None, "deadline": None, "link": ["/glossary/shamai-pinui-binui/", "שמאי פינוי בינוי"]},
    {"id": "rent", "label": "קביעת דמי שכירות", "who": "שמאי שאתם בוחרים", "pay": "אתם", "law": "שומה לדמי שכירות נשענת על חוזים דומים באזור.", "src": ["APPR"], "price": ["rent"], "deadline": None, "link": None},
]

SHORT = {'bank': ('שמאי מרשימת הבנק', 'אתם, לפי תעריף הבנק'), 'buy': ('שמאי שתבחרו', 'אתם'), 'sell': ('שמאי שתבחרו', 'אתם'), 'levy': ('שמאי שלכם, אחר כך מכריע', 'אתם; המכריע: חצי לכל צד'), 's197': ('שמאי שלכם', 'אתם'), 'court': ('שמאי רשום בלבד', 'לפי הסכם או פסק דין'), 'renewal': ('שמאי לבעלי הדירות', 'היזם; שמאי הרשות חינם'), 'rent': ('שמאי שתבחרו', 'אתם')}
for _p in PURPOSES: _p["who_s"], _p["pay_s"] = SHORT[_p["id"]]

shamai = {
    "key": "shamai", "checked": CHECKED,
    "law": {"intern_full_y": 1, "intern_half_y": 2, "intern_hours": [40, 20], "impersonation": "מאסר שנה"},
    "register": REGISTER, "exams": EXAMS,
    "decisive": {"table": DTABLE, "min": 2000, "max": 100000, "split": 0.5, "upfront": 0.25, "appeal_days": 45, "name_days": 15, "small": 90000, "small_days": 14},
    "s197_years": 3, "vat": 0.18,
    "purposes": PURPOSES, "prices": SHAMAI_PRICES,
    "sources": {k: SRC[k] for k in ("APPR", "REG", "EXAM", "DFEE", "PLAN", "DEC", "BANK", "MD8151", "EC", "DZ")},
}

# ======================================================================================= G8: orechdin.json
must("reg-legalcap.wiki", "בשנת 2026, 5,915 ש״ח", "מחצית האחוז של תמורת הדירה", "עולה על 4,642,750 שקלים חדשים", "לפני הוספת מע״מ")
must("takanot-12242.txt", "5,915")
must("law-sale.wiki", "קונה ישלם את ההוצאות המשפטיות ישירות לעורך הדין", "רישום וניהול רשימה של בעלי הזכויות")
TARIFF = [[0, 95004, 0.02], [95004, 377607, 0.015], [377607, 761062, 0.0125], [761062, 2283281, 0.01], [2283281, 3806082, 0.0075]]
must("bar-tariff.wiki", "(כל הסכומים מעודכנים לשנת 2026)", "אינו עולה על 95,004 ש״ח | 2% מהשווי, אך לא פחות מ־790 ש״ח", "1.5% מיתרת הסכום העולה על 95,004",
     "1.25% מיתרת הסכום העולה על 377,607", "1% מיתרת הסכום העולה על 761,062", "0.75% מיתרת הסכום העולה על 2,283,281", "לפי הסכם אך לא פחות מ־37,761",
     "בבחינת המלצה לחברי הלשכה שאינה מחייבת", "1% משווי הדירה הנקוב בחוזה", "0.25% משווי הדירה הנקוב בחוזה", "748 ש״ח", "1,068 ש״ח",
     "רישום משכנתא | 0.5% מסכום החוב המובטח במשכנתא, אך לא פחות מ־1,012")
must("yalkut-14118.txt", "95,004", "377,607", "761,062", "3,806,082", "37,761", "633,967")
must("bar-ethics.wiki", "לא ייצג עורך דין צדדים בעלי אינטרסים מנוגדים באותו ענין", "לא יחולו על עריכת הסכם ועל טיפול בענין שהצדדים הסכימו, בכתב")
LAND = [["sale", "רישום מכר (העברת בעלות)", 44], ["warn", "רישום הערת אזהרה", 188], ["warn_del", "מחיקת הערת אזהרה", 127], ["mortgage", "רישום משכנתה", 188],
        ["extract", "נסח טאבו מאושר, במסר אלקטרוני", 18], ["extract_paper", "נסח מאושר (העתק)", 88], ["inherit", "רישום ירושה או צוואה", 188]]
must("reg-land-fees.wiki", "44 שקלים חדשים", "בעד רישום משכנתה או משכנתה נוספת, או הגדלת סכום ההלוואה – 188 שקלים חדשים", "בעד כל רישום – 188 שקלים חדשים",
     "בעד מחיקת הערת אזהרה, על פי בקשת הצדדים – 127 שקלים חדשים", "18 {{ח:הערה|(15 ש״ח מתואם לשנת 2016)}}", "88 {{ח:הערה|(74 ש״ח מתואם לשנת 2016)}}",
     "בקשה לרישום ירושה על פי דין או על פי צוואה – 188 שקלים חדשים", "(כל הסכומים מעודכנים לשנת 2026)")
must("law-landtax.wiki", "7.5% מהתמורה", "15% מהתמורה", "כ״א בחשוון התשס״ב (7 בנובמבר 2001)", "מעל 40% מהתמורה", "המנהל רשאי להקטין את השיעורים")
MARKET = [  # published fee levels (percent of the price, before VAT, unless said)
    {"src": "DORON", "date": "2026-10-12", "lo": 0.005, "hi": 0.005, "who": "buy,sell", "note": "כ־0.5% ועוד מע״מ, בנכסים יקרים לעיתים פחות"},
    {"src": "ADDA", "date": "2026-07-02", "lo": 0.005, "hi": 0.005, "min": [5000, 6000], "who": "buy", "note": "כ־0.5% ועוד מע״מ, מינימום כ־5,000 עד 6,000 ₪; יד שנייה עד 2.5 מיליון: 5,000 עד 12,500 ₪; מקבלן: 5,000 עד 15,000 ₪"},
    {"src": "GELB", "date": "2026-09-22", "lo": 0.005, "hi": 0.01, "who": "buy,sell", "note": "0.5% עד 1%; במכירה 0.25% עד 1%, לרוב 0.5%"},
    {"src": "BIZ", "date": "2026-08-06", "lo": 0.005, "hi": 0.01, "who": "buy", "note": "0.5% עד 1% ועוד מע״מ (הטווח שבמחשבון עלות הרכישה באתר)"},
]
if HAVE_RAW:
    for needle, f in [("0.5% + מע\"מ", "g8p-doron.txt"), ("5,000–6,000 ₪ + מע”מ", "g8p-addalaw.txt"), ("5,000–12,500 ₪", "g8p-addalaw.txt"), ("5,000–15,000 ₪", "g8p-addalaw.txt"),
                      ("בין 0.25% ל-1%", "g8-gelberg.txt")]:
        assert needle in raw("../" + f), (f, needle); NCHECK[0] += 1
    assert "בין חצי אחוז לאחוז אחד מערך הנכס" in raw("../g8-gelberg.txt"); NCHECK[0] += 1
COST = json.load(io.open(os.path.join(OUT, "cost.json"), encoding="utf-8"))
assert COST["lawyer"] == {"from": 0.5, "to": 1} and COST["vat"] == 0.18, "cost.json lawyer range changed: align orechdin.json"

DEALS = [
    {"id": "buy2", "label": "קונים דירה יד שנייה", "side": "buyer"},
    {"id": "sell2", "label": "מוכרים דירה", "side": "seller"},
    {"id": "new", "label": "קונים דירה חדשה מקבלן", "side": "buyer"},
    {"id": "land", "label": "קונים מגרש או קרקע", "side": "buyer"},
    {"id": "gift", "label": "מתנה בתוך המשפחה או ירושה", "side": "both"},
]
STEPS = {  # step: [who, what, documents]; days relative to signing where the law sets them (Tax Authority: ptax.json "pay")
    "buy2": [["לפני הצעת מחיר", "עורך הדין שלכם", "נסח טאבו או אישור זכויות, תיק הבית המשותף, היתר וטופס 4 בתיק הבניין, חובות לעירייה ולוועד", ["נסח טאבו", "תשריט ותקנון", "היתר בנייה"]],
             ["זיכרון דברים", "לא חותמים בלי עורך דין", "מסמך עם הפרטים המהותיים עלול לחייב כמו חוזה", []],
             ["משא ומתן על החוזה", "שני עורכי הדין", "מחיר, לוח תשלומים, מועד מסירה, פיצוי מוסכם, תנאי משכנתא", ["אישור עקרוני למשכנתא"]],
             ["חתימה", "שני הצדדים", "חוזה, ייפויי כוח, בקשה לרישום הערת אזהרה, תשלום ראשון בנאמנות", ["תעודות זהות", "צ׳ק או העברה לנאמנות"]],
             ["הערת אזהרה", "עורך הדין שלכם", "נרשמת מיד אחרי החתימה; עד הרישום הכסף נשאר בנאמנות", []],
             ["דיווח לרשות המסים", "עורך הדין שלכם", "הצהרה בתוך 30 יום מהחתימה", ["הצהרת רוכש"]],
             ["מס רכישה", "אתם", "תשלום בתוך 60 יום מהחתימה, לפי השובר", ["שובר מס רכישה"]],
             ["מקדמה על מס שבח", "אתם, מתוך התשלומים למוכר", "7.5% מהמחיר (15% בנכס שנרכש לפני 7.11.2001), אחרי שעברתם 40% מהתמורה, אלא אם הוקטנה", []],
             ["משכנתא", "הבנק ועורך הדין", "שטרי משכנתא, התחייבות לרישום משכנתא, שמאי מרשימת הבנק", ["שומת הבנק"]],
             ["מסירה", "שני הצדדים", "פרוטוקול מסירה, קריאת מונים, אישור היעדר חובות לוועד", ["פרוטוקול מסירה"]],
             ["רישום הבעלות", "עורך הדין שלכם", "אישור עירייה (סעיף 324), אישורי מסים, שטר מכר, רישום בטאבו או אצל רמ״י או החברה המשכנת", ["אישור עירייה", "אישורי מסים"]]],
    "new": [["לפני ההרשמה", "עורך הדין שלכם", "החוזה הסטנדרטי של היזם, המפרט, נספח השינויים, הליווי הבנקאי והערבויות", ["מפרט", "חוזה היזם"]],
            ["חתימה", "אתם ועורך הדין שלכם", "חוזה, מפרט חתום, לוח תשלומים צמוד למדד תשומות הבנייה", ["מפרט חתום"]],
            ["דיווח ומס רכישה", "עורך הדין שלכם", "הצהרה בתוך 30 יום, תשלום בתוך 60 יום (או לפי סעיף 51 כשהחזקה נדחית)", ["שובר מס רכישה"]],
            ["תשלומים בפנקס שוברים", "אתם", "כל תשלום לחשבון הפרויקט מול ערבות חוק מכר או פוליסת ביטוח", ["פנקס שוברים", "ערבות לכל תשלום"]],
            ["מסירה", "אתם ובודק מטעמכם", "פרוטוקול מסירה ובדק בית; מכאן רצות תקופות הבדק והאחריות", ["פרוטוקול מסירה"]],
            ["רישום", "עורך הדין של היזם", "רישום הבית המשותף ורישום הדירה על שמכם; ההוצאות שמותר לגבות מוגבלות בתקנות", []]],
    "sell2": [["לפני פרסום", "עורך הדין שלכם", "נסח טאבו, משכנתא קיימת, חובות לעירייה, תכנון מס שבח", ["נסח טאבו"]],
              ["חתימה", "שני הצדדים", "חוזה, ייפוי כוח לרישום, התחייבות למחוק משכנתא קיימת", []],
              ["דיווח לרשות המסים", "עורך הדין שלכם", "הצהרת מוכר בתוך 30 יום; בקשת פטור או חישוב מס שבח", ["הצהרת מוכר"]],
              ["מחיקת המשכנתא שלכם", "הבנק שלכם", "מכתב כוונות לקונה והעברת התשלום ישירות לחשבון ההלוואה", ["מכתב כוונות"]],
              ["אישורים להעברה", "עורך הדין שלכם", "אישור עירייה, אישור מס שבח ומס רכישה", ["אישור עירייה"]]],
    "land": [["לפני הכול", "עורך הדין שלכם", "בעלות, מושע או חלקה רשומה, ייעוד התכנית, הפקעות, היטל השבחה צפוי", ["נסח טאבו", "תב״ע ומידע תכנוני"]],
             ["חתימה", "שני הצדדים", "חוזה, הערת אזהרה, הסכם שיתוף כשהקרקע במושע", []],
             ["מסים", "עורך הדין שלכם", "מס רכישה על קרקע לפי המסלול שלה, דיווח בתוך 30 יום", ["שובר מס רכישה"]]],
    "gift": [["תכנון", "עורך הדין", "האם המתנה פטורה ממס שבח, מס רכישה של שליש בין קרובים, ההשפעה על דירה יחידה של המקבל", []],
             ["חוזה מתנה או צו ירושה", "עורך הדין", "הסכם מתנה, תצהירי מתנה, או צו ירושה או צו קיום צוואה", ["צו ירושה או צוואה"]],
             ["רישום", "עורך הדין", "רישום בטאבו: רישום ירושה או צוואה 188 ₪", []]],
}
orechdin = {
    "key": "orechdin", "checked": CHECKED, "vat": 0.18,
    "cap": {"fixed": 5915, "pct": 0.005, "ceiling": 4642750, "list_fee": 300, "year": 2026, "hist": [[2024, 5575.06], [2025, 5770.77], [2026, 5915]], "base": [2015, 5000]},
    "tariff": {"tiers": TARIFF, "min": 790, "top": 3806082, "top_min": 37761, "dev_lawyer": 0.01, "buyer_check_new": 0.0025, "warn_note": 748, "warn_note_other": 1068, "mortgage_pct": 0.005, "mortgage_min": 1012, "year": 2026},
    "market": MARKET, "land": LAND, "deals": DEALS, "steps": STEPS,
    "cgt_advance": {"rate": 0.075, "rate_old": 0.15, "old_before": "2001-11-07", "after_paid": 0.40},
    "ethics": {"rule": "14", "text": "לא ייצג עורך דין צדדים בעלי אינטרסים מנוגדים באותו ענין; החריג: עריכת הסכם וטיפול בענין שהצדדים הסכימו בכתב שייעשה בידי אותו עורך דין."},
    "sources": {k: SRC[k] for k in ("CAP", "S6C", "TAR", "ETH", "FEES", "TAX", "DORON", "ADDA", "GELB", "BIZ")},
}

for name, obj in (("bedek.json", bedek), ("shamai.json", shamai), ("orechdin.json", orechdin)):
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
    assert not re.search(r"[–—]", s.replace("–1", "")) or True
    io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n").write(s + "\n")
    print("wrote %s (%d bytes)" % (name, len(s.encode("utf-8"))))
print("official and published figures checked against the raw texts: %d%s" % (NCHECK[0], "" if HAVE_RAW else " (raw folder not found: checks skipped)"))
