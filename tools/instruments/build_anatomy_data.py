# -*- coding: utf-8 -*-
"""HAD-681 (Ben 7.11.2026): anatomy.json, the sources of the tool "מה יש בתוך המחיר של דירה חדשה" (panatomy).

    python tools/instruments/build_anatomy_data.py   -> plugins/nadlan-config/assets/instruments/data/anatomy.json

STRICT HONESTY (owner order): a component carries a number or a range ONLY with a named, dated public source recorded here with
its URL, its date, the date we read it and the sentence it says (verbatim, "q"). A component with no such source is a named
slice with an explanation and NO number. Rules that are law (VAT, betterment levy, purchase tax on land) are rules, not shares.
The research trail (read 7.11.2026): Bank of Israel, Research Department, box "התפתחות מחירי קרקע למגורים בשנים 1998-2012"
(5.6.2013, the .doc on boi.org.il, text read from the file); the inter-ministry team's interim report on the Third Schedule
(July 2026, gov.il PDF); Reichman University, Phoenix Institute, "תמונת מצב בענף הנדל"ן היזמי" (April 2026, PDF); VAT, purchase
tax and fees from the site's own checked files (cost.json, ptax.json); the construction-input index from cbs-200010.json; the
Bank of Israel prime rate from boi-mortgage.json. Searched and NOT found as a dated public number: developer margin across the
market, construction cost per m2, planning and permit costs, development levies per unit nationally, financing cost as a share.
"""
import io
import json
import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")


def load(name):
    return json.load(io.open(os.path.join(DATA, name), encoding="utf-8"))


def main():
    cost = load("cost.json")
    ptax = load("ptax.json")
    boim = load("boi-mortgage.json")
    nlb = load("nlbudget.json")["figures"]["sp_sm"]
    pol = boim["policy"]
    S = {
        "boi13": {
            "he": "בנק ישראל, חטיבת המחקר: התפתחות מחירי קרקע למגורים בשנים 1998 עד 2012 (סקירת ההתפתחויות הכלכליות)",
            "url": "https://boi.org.il/media/znmgkuou/%D7%A7%D7%98%D7%A2-%D7%9E%D7%AA%D7%95%D7%9A-%D7%A1%D7%A7%D7%99%D7%A8%D7%AA-%D7%94%D7%94%D7%AA%D7%A4%D7%AA%D7%97%D7%95%D7%99%D7%95%D7%AA-%D7%94%D7%9B%D7%9C%D7%9B%D7%9C%D7%99%D7%95%D7%AA-%D7%90%D7%9E%D7%99%D7%93%D7%95%D7%AA-%D7%A9%D7%9C-%D7%9E%D7%97%D7%99%D7%A8%D7%99-%D7%A7%D7%A8%D7%A7%D7%A2-562013.doc",
            "date": "2013-06-05", "read": "2026-11-07", "kind": "official",
            "q": [
                "בישראל היווה מחיר הקרקע, בממוצע כלל ארצי לשנים 2009-2010, בערך שליש ממחיר הדירה לצרכן; במרכז הארץ חלקה של הקרקע גבוה בהרבה מאשר בפריפריה. עלויות הבנייה היוו גם כן כשליש מהמחיר והיתר נזקף לרווח יזמי ולמסים",
                "בשנת 2011 הגיעו מחירי הקרקעות (לא כולל מע\"מ) לשיאם: במרכז המחירים הגיעו לסדר גודל של 450 אלף ש\"ח ליחידת דיור לבנייה רוויה ובפריפריה הם התקרבו ל-100 אלף ש\"ח; מדובר על כשליש ועל כעשירית, בהתאמה, ממחירה של דירה טיפוסית בת 3.5-4 חדרים",
                "הוא לוג מחיר הקרקע ליחידת דיור (כולל הוצאות הפיתוח וללא מע\"מ)",
            ],
        },
        "hashbacha": {
            "he": "הצוות הבין־משרדי לבחינת התוספת השלישית לחוק התכנון והבנייה: היטל השבחה, דו״ח ביניים",
            "url": "https://www.gov.il/BlobFolder/reports/betterment-tax/he/Planning-and-Building-Law.pdf",
            "date": "2026-07", "read": "2026-11-07", "kind": "official",
            "q": ["ככלל, שיעור ההיטל עומד על מחצית (50%) ההשבחה. ההשבחה נקבעת בשומה הנערכת על ידי שמאי מקרקעין"],
        },
        "runi26": {
            "he": "אוניברסיטת רייכמן, מכון הפניקס לחקר שוק ההון: תמונת מצב בענף הנדל״ן היזמי, נייר מדיניות",
            "url": "https://www.runi.ac.il/media/qv2exvtr/%D7%AA%D7%9E%D7%95%D7%A0%D7%AA-%D7%9E%D7%A6%D7%91-%D7%91%D7%A2%D7%A0%D7%A3-%D7%94%D7%A0%D7%93%D7%9C%D7%9F-%D7%94%D7%99%D7%96%D7%9E%D7%99_13042026.pdf",
            "date": "2026-04", "read": "2026-11-07", "kind": "research",
            "q": ["הטבות אלו היוו ב-2025 כ-40% מהעסקאות בשוק החופשי, ונאמדו בממוצע בכ-13% ממחיר הדירה"],
        },
        "vat": {"he": cost["sources"][0]["label"], "url": cost["sources"][0]["url"], "date": "2025-01-01", "read": cost["checked"], "kind": "official", "q": []},
        "ptax": {"he": ptax["source"], "url": ptax["url"], "date": ptax["effective"], "read": ptax["checked"], "kind": "official", "q": []},
        "fees": {"he": cost["sources"][1]["label"], "url": cost["sources"][1]["url"], "date": "2026-08-06", "read": cost["checked"], "kind": "press", "q": []},
        "ltv": {"he": cost["sources"][2]["label"], "url": cost["sources"][2]["url"], "date": "2026-06-30", "read": cost["checked"], "kind": "official", "q": []},
        "prime": {"he": pol["src"]["label"], "url": pol["src"]["url"], "date": pol["from"], "read": pol["asof"], "kind": "official", "q": []},
        "input": {"he": "הלשכה המרכזית לסטטיסטיקה, מדד מחירי תשומה בבנייה למגורים (סדרה 200010)", "url": "https://www.cbs.gov.il/", "date": "monthly", "read": "cbs-200010.json", "kind": "official", "q": []},
        "mkt": {"he": nlb["src_he"] + " (חברת שיווק נדל״ן, עמוד השירות שלה)", "url": nlb["url"], "date": nlb["date"], "read": nlb["retrieved"], "kind": "claim",
                "q": [nlb["ev"][0]["value"]]},
    }
    # developer side: the parts of the price of a new apartment. share: a number ONLY with a source key; sub: the named sub-parts.
    dev = [
        {"id": "land", "he": "הקרקע", "k": "housing",
         "share": {"nat": {"v": 1 / 3, "say": "כשליש", "src": "boi13", "when": "ממוצע ארצי 2009 עד 2010"},
                   "center": {"v": 1 / 3, "say": "כשליש", "src": "boi13", "when": "מרכז הארץ, שיא 2011"},
                   "periph": {"v": 0.1, "say": "כעשירית", "src": "boi13", "when": "פריפריה, שיא 2011"}},
         "txt": "המחיר שהיזם שילם על המגרש במכרז של רשות מקרקעי ישראל או בעסקה פרטית, מחולק בין הדירות. במחקר של בנק ישראל מחיר הקרקע ליחידת דיור כולל את הוצאות הפיתוח, בלי מע״מ. במרכז הארץ חלקה של הקרקע גבוה בהרבה מאשר בפריפריה.",
         "sub": [
             {"he": "מחיר המגרש", "txt": "התמורה במכרז או בעסקה, לפי מספר הדירות שמותר לבנות במגרש."},
             {"he": "הוצאות פיתוח והיטלי פיתוח", "txt": "כבישים, מים, ביוב וניקוז. במכרזי רשות מקרקעי ישראל הן משולמות עם הקרקע, ובבנק ישראל הן חלק ממחיר הקרקע ליחידה. אין מספר ארצי אחד לדירה."},
             {"he": "היטל השבחה", "rule": "50% מעליית השווי", "src": "hashbacha", "txt": "כשתוכנית מעלה את שווי הקרקע, הוועדה המקומית גובה מחצית מההשבחה, לפי שומת שמאי. זה שיעור מתוך ההשבחה, לא חלק קבוע ממחיר הדירה."},
             {"he": "מס רכישה על הקרקע", "rule": f"{round(100 * ptax['land'])}% ממחיר הקרקע", "src": "ptax", "txt": "היזם משלם מס רכישה על קרקע לפי שיעור קבוע, והוא נכנס לעלות הקרקע."},
         ]},
        {"id": "build", "he": "הבנייה", "k": "sea",
         "share": {"nat": {"v": 1 / 3, "say": "כשליש", "src": "boi13", "when": "ממוצע ארצי 2009 עד 2010"}},
         "txt": "עלויות הבנייה עצמן: חומרים, עבודה וציוד. המחיר שלהן זז עם מדד תשומות הבנייה של הלמ״ס, ובדירה מקבלן חלק מהתשלומים צמוד אליו לפי חוק המכר.",
         "trend": "input",
         "sub": [
             {"he": "שלד", "txt": "יסודות, עמודים, תקרות וקירות נושאים: בטון, ברזל וטפסנות."},
             {"he": "גמר", "txt": "ריצוף, חיפוי, טיח וצבע, נגרות, דלתות וחלונות, מטבח וכלים סניטריים."},
             {"he": "מערכות", "txt": "חשמל, אינסטלציה, מיזוג, גז, כיבוי אש ותקשורת."},
             {"he": "ממ״ד", "txt": "חדר מוגן בכל דירה: קירות ותקרה מבטון מזוין, דלת וחלון הדף."},
             {"he": "חניון תת־קרקעי", "txt": "חפירה, דיפון ומרתפי חניה מתחת לבניין."},
             {"he": "מעליות", "txt": "מעליות ופירים, לפי גובה הבניין ומספר הדירות בקומה."},
         ]},
        {"id": "rest", "he": "רווח היזם ומסים", "k": "civic",
         "share": {"nat": {"v": 1 / 3, "say": "היתר, כשליש", "src": "boi13", "when": "ממוצע ארצי 2009 עד 2010"}},
         "txt": "לפי בנק ישראל, מה שנשאר אחרי הקרקע והבנייה נזקף לרווח היזמי ולמסים. בתוכו המע״מ, שמחושב היום במדויק, ושאר הרכיבים, שאין להם חלוקה רשמית.",
         "sub": [
             {"he": "מע״מ", "rule": "18% על המחיר לפני מע״מ", "src": "vat", "vat": True, "txt": "דירה חדשה מקבלן נמכרת עם מע״מ. 18% על המחיר לפני מע״מ הם 15.3% מהמחיר הסופי. בדירה יד שנייה מאדם פרטי אין מע״מ."},
             {"he": "רווח היזם", "txt": "הרווח שהיזם מכניס למחיר על ההון ועל הסיכון שלו. לא מצאנו מקור ציבורי עדכני עם שיעור ממוצע לכל השוק, ולכן אין כאן מספר."},
             {"he": "מימון", "src": "runi26", "facts": ["prime", "runi"], "txt": "ליווי בנקאי, ערבויות חוק המכר לקונים והריבית על הקרקע עד שהבנייה מתחילה. במבצעי מימון כמו 10/90 ו־20/80 הקונה משלם מעט בחתימה ואת היתרה במסירה, והיזם נושא בעלות המימון בינתיים."},
             {"he": "תכנון והיתרים", "txt": "אדריכלים, מהנדסים ויועצים, אגרות בנייה והיתר. אין מספר ציבורי אחד לדירה."},
             {"he": "שיווק ומכירה", "src": "mkt", "claim": {"lo": nlb["lo"], "hi": nlb["hi"]}, "txt": "משרד מכירות, צוות מכירה, פרסום והדמיות."},
         ]},
    ]
    out = {
        "key": "anatomy", "built": time.strftime("%Y-%m-%d"),
        "note": "HAD-681. A number only with a source (src) recorded here; rules are rules (rule), not shares. Built by tools/instruments/build_anatomy_data.py.",
        "src": S, "dev": dev,
        "facts": {"prime": {"v": pol["prime"], "from": pol["from"], "src": "prime"},
                  "runi": {"deals": 0.40, "disc": 0.13, "year": 2025, "src": "runi26"}},
        "buyer": {"vat": cost["vat"], "lawyer": cost["lawyer"], "broker": cost["broker"], "appraiser": cost["appraiser"],
                  "inspection": cost["inspection"], "mortgage_fee": cost["mortgage_fee"], "ltv": cost["ltv"]},
        "none": ["רווח היזם כשיעור ממוצע לכל השוק", "עלות בנייה למ״ר", "תכנון והיתרים לדירה", "היטלי פיתוח לדירה בממוצע ארצי", "עלות המימון כחלק מהמחיר"],
    }
    path = os.path.join(DATA, "anatomy.json")
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("wrote", path, os.path.getsize(path), "bytes;", len(dev), "groups;", sum(len(g["sub"]) for g in dev), "sub-parts")


if __name__ == "__main__":
    main()
