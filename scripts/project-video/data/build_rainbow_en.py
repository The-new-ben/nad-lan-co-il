# -*- coding: utf-8 -*-
"""The English cut of the Rainbow film: data/rainbow-tel-aviv-en.json from data/rainbow-tel-aviv.json.
Every on-screen line is the Hebrew line translated, nothing added: the same facts, the same sources and dates. The composer
draws it left to right ("dir": "ltr", the mirrored layout). Rerun after the Hebrew file changes; a Hebrew line without an
English one stops the build.
  python data/build_rainbow_en.py"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "rainbow-tel-aviv.json")
OUT = os.path.join(HERE, "rainbow-tel-aviv-en.json")

EN = {
    "נדל״ן": "NadLan",
    "פלטפורמה עצמאית, לא מטעם היזם": "An independent platform, not on behalf of the developer",
    "הדמיה להמחשה": "Illustration",
    "הדמיה להמחשה, נוף משוער": "Illustration, estimated view",
    "Rainbow תל אביב": "Rainbow Tel Aviv",
    "רובע שדה דב, צפון תל אביב": "Sde Dov quarter, north Tel Aviv",
    "יזם: ישראל קנדה": "Developer: Israel Canada",
    "המיקום": "Location",
    "רובע שדה דב": "Sde Dov quarter",
    "צפון תל אביב, כ-700 מ׳ מהים": "North Tel Aviv, about 700 m from the sea",
    "מרחק בקו אווירי, לפי מפות עיריית תל אביב-יפו": "Straight-line distance, by the Tel Aviv-Yafo municipality's maps",
    "הבניינים": "The buildings",
    "מגדל 39 קומות": "A 39-floor tower",
    "ובנייני בוטיק בני 9 קומות סביב חצר פנימית": "and 9-floor boutique buildings around an inner courtyard",
    "לפי תכנית העיצוב שאושרה ב-10.5.2023": "By the design plan approved on 10.5.2023",
    "הדירות": "The apartments",
    "459 דירות": "459 apartments",
    "בבנייה, הקבלן המבצע: אשטרום": "Under construction; main contractor: Ashtrom",
    "אכלוס צפוי ב-2030": "Occupancy expected in 2030",
    "לפי היזם ואתר הפרויקט": "By the developer and the project's website",
    "מחירים ומכירות": "Prices and sales",
    "כ-81,800 ₪ למ״ר": "about ₪81,800 per m²",
    "המחיר הממוצע שדווח בדירות שנמכרו עד 3.2026": "the reported average in apartments sold up to 3.2026",
    "275 מתוך 459": "275 of 459",
    "דירות נמכרו עד 6.2026, לפי דוחות היזם": "apartments sold by 6.2026, per the developer's reports",
    "מקורות: ביזפורטל, 29.5.2026; גלובס, 27.8.2026. מחיר וזמינות מחייבים אישור היזם.":
        "Sources: Bizportal, 29.5.2026; Globes, 27.8.2026. Price and availability need the developer's confirmation.",
    "המתקנים בפרויקט": "The facilities",
    "שתי בריכות על הגגות": "Two rooftop pools",
    "Rainbow Club, מועדון הדיירים": "Rainbow Club, the residents' club",
    "לובי בכל בניין": "A lobby in every building",
    "מסחר בקומת הקרקע": "Retail on the ground floor",
    "חניון תת־קרקעי": "Underground parking",
    "לפי תכנית העיצוב (10.5.2023) ואתר ישראל קנדה. מיקום המתקנים בהדמיה להמחשה.":
        "By the design plan (10.5.2023) and Israel Canada's website. The facilities' places in the illustration are indicative.",
    "הנוף מהקומה": "The view from the floor",
    "קומה 36": "Floor 36",
    "קומה 10": "Floor 10",
    "מהסלון, מבט מערבה": "From the living room, looking west",
    "מהמרפסת, מבט דרומה": "From the balcony, looking south",
    "מהמרפסת, מבט מערבה": "From the balcony, looking west",
    "דירה לדוגמה: החלוקה, הגמרים והנוף משוערים ואינם לפי תוכנית מכר":
        "Example apartment: the layout, finishes and view are estimates, not a sales plan",
    "שיחת וידאו עם נציג": "Video call with a representative",
    "שאלות? וואטסאפ": "Questions? WhatsApp",
}


def heb(s):
    return any("֐" <= c <= "׿" for c in s)


missing = []


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "text" and isinstance(v, str) and heb(v):
                if v in EN:
                    o[k] = EN[v]
                else:
                    missing.append((path, v))
            elif isinstance(v, (dict, list)) and (k not in ("sources", "page") and not k.startswith("page_")):
                walk(v, path + "." + k)   # a scene's "source" is an on-screen line {text}; a line's own "source" is provenance
            elif k not in ("source", "sources", "note", "page", "checked") and not k.startswith("page_"):
                walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + "[%d]" % i)


d = json.load(io.open(SRC, encoding="utf-8"))
walk(d)
if missing:
    for p, v in missing:
        print("NO ENGLISH:", p, v)
    sys.exit(1)
d["slug"] = "rainbow-tel-aviv-en"
d["dir"], d["lang"] = "ltr", "en"
d["note"] = "The English cut, built by data/build_rainbow_en.py from rainbow-tel-aviv.json (translation only). " + str(d.get("note", ""))
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("wrote", OUT)
