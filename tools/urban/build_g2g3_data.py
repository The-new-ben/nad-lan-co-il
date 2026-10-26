# -*- coding: utf-8 -*-
"""G2 + G3 of the upgrade loop (Ben 26.10.2026): the data behind two tools, from official sources only.

  pinui.json  (key "pinui", tool tools/pinui.js on /urban-renewal/pinui-binui/): the rules of the Pinui Binui law as it reads today
              (majorities, the clocks of section 1ד, the elderly, refusal grounds, the authority's appraiser), the tax and betterment
              rules of the authority's 2025 report (annex A), the comparison rules of the strengthening law (TAMA 38), the 2025 report
              series (approval to first permit, plans approved per year, tax-track declarations per year) and the assumptions of the
              government feasibility model (model_dinami).
  urcity.json (key "urcity", tool tools/urcity.js on /urban-renewal/): per city, what the 2025 report says about building renewal
              (the city plan that replaces TAMA 38 and its status, years from permit request to permit, apartments sold in renewal
              projects, tax-track declarations), the permits split (demolition vs strengthening) 2013-2025, the tracks comparison
              (annex A) and the district of each locality (renewal-stats.json). The complexes themselves come from renewal-track.json
              (the authority's map, the data.gov.il file and our snapshots), which both tools load next to their own file.

Every number below is transcribed from the source named next to it, with the page. Totals printed in the report are checked against
the sum of the transcribed rows, so a typo stops the build. Report city names are folded to the names the authority's map uses.

Sources (read 26.10.2026):
  R25  דוח הרשות הממשלתית להתחדשות עירונית לשנת 2025 (gov.il, published 26.5.2026, updated 16.6.2026), PDF 144 pages.
  LAW  חוק פינוי ובינוי (עידוד מיזמי פינוי ובינוי), התשס"ו-2006, as amended to תשפ"ג (the open law book on Wikisource; the binding
       text is the one in Reshumot). LTAMA: חוק המקרקעין (חיזוק בתים משותפים מפני רעידות אדמה), התשס"ח-2008, same.
  FAQ  gov.il/he/departments/faq/renewal_faq (the authority's questions and answers). SHM: gov.il service bakasha-leminuy-shamay-renewal.
  S21  gov.il/he/departments/policies/standard_21. MDL: gov.il/he/pages/model_dinami.

  python tools/urban/build_g2g3_data.py            (writes both files; exits 1 on a failed check)"""
import io, json, os, re, sys

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
STATS = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "data", "renewal-stats.json"), encoding="utf-8"))
TRACK = json.load(io.open(os.path.join(DATA, "renewal-track.json"), encoding="utf-8"))
READ = "2026-10-26"
bad = []


def check(name, got, want):
    if got != want:
        bad.append((name, got, want))
    print(("OK   " if got == want else "BAD  ") + name + ": " + str(got) + ("" if got == want else "  (want %s)" % want))


def norm(s):
    s = re.sub(r"[֑-ׇ]", "", str(s or ""))
    s = re.sub(r"[-‐-―,.;:!?\"'׳״()]", " ", s)
    return re.sub(r"\s+", " ", s).strip().replace("יי", "י").replace("וו", "ו")


MAPC = sorted(set(r["c"] for r in TRACK["recs"]))
NC = {norm(c): c for c in MAPC}
ALIAS = {"יהוד מונוסון": "יהוד", "זיכרון יעקב": "זכרון יעקב", "יקנעם": "יקנעם עילית"}


def nodash(s): return re.sub(r"\s*[–—-]\s*", " ", s).strip()


def city(name):
    """A report city name -> the authority map's spelling (or the report's own, when the map has no complex there)."""
    n = norm(name)
    n = norm(ALIAS.get(n, n))
    return NC.get(n, re.sub(r"\s*[–—-]\s*", " ", name).strip())


SRC = {
    "R25": {"label": "דוח הרשות הממשלתית להתחדשות עירונית לשנת 2025", "url": "https://www.gov.il/he/pages/urban_renewal_report_2025", "date": "2026-06-16"},
    "LAW": {"label": "חוק פינוי ובינוי (עידוד מיזמי פינוי ובינוי), התשס\"ו-2006", "url": "https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%A4%D7%99%D7%A0%D7%95%D7%99_%D7%95%D7%91%D7%99%D7%A0%D7%95%D7%99_(%D7%A2%D7%99%D7%93%D7%95%D7%93_%D7%9E%D7%99%D7%96%D7%9E%D7%99_%D7%A4%D7%99%D7%A0%D7%95%D7%99_%D7%95%D7%91%D7%99%D7%A0%D7%95%D7%99)", "date": READ},
    "LTAMA": {"label": "חוק המקרקעין (חיזוק בתים משותפים מפני רעידות אדמה), התשס\"ח-2008", "url": "https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%A7%D7%A8%D7%A7%D7%A2%D7%99%D7%9F_(%D7%97%D7%99%D7%96%D7%95%D7%A7_%D7%91%D7%AA%D7%99%D7%9D_%D7%9E%D7%A9%D7%95%D7%AA%D7%A4%D7%99%D7%9D_%D7%9E%D7%A4%D7%A0%D7%99_%D7%A8%D7%A2%D7%99%D7%93%D7%95%D7%AA_%D7%90%D7%93%D7%9E%D7%94)", "date": READ},
    "FAQ": {"label": "שאלות ותשובות של הרשות הממשלתית להתחדשות עירונית", "url": "https://www.gov.il/he/departments/faq/renewal_faq", "date": READ},
    "SHM": {"label": "בקשה למינוי שמאי פינוי ובינוי, gov.il", "url": "https://www.gov.il/he/service/bakasha-leminuy-shamay-renewal", "date": READ},
    "S21": {"label": "תקן 21, gov.il", "url": "https://www.gov.il/he/departments/policies/standard_21", "date": READ},
    "MDL": {"label": "המחשבון לחישוב כדאיות כלכלית של מתחמי פינוי ובינוי, gov.il", "url": "https://www.gov.il/he/pages/model_dinami", "date": READ},
    "MAP": {"label": "מפת הרשות הממשלתית להתחדשות עירונית, gov.il", "url": "https://www.gov.il/he/departments/topics/mapa-renewal", "date": TRACK["agg"]["to"]},
    "FILE": {"label": "קובץ מתחמי ההתחדשות העירונית, data.gov.il", "url": "https://data.gov.il/dataset/urban_renewal", "date": STATS["file"]["last_modified"]},
}

# ------------------------------------------------------------------ R25 series
# p.87: average years from plan approval to the first building permit in pinui binui, by permit year (complexes)
APPROVAL_TO_PERMIT = [[2015, 5.6, 4], [2016, 6.0, 7], [2017, 4.2, 9], [2018, 3.1, 10], [2019, 2.7, 10], [2020, 3.1, 5], [2021, 4.9, 23], [2022, 4.1, 33], [2023, 3.9, 28], [2024, 4.0, 43], [2025, 4.0, 28]]
# p.25: pinui binui plans approved per year and the proposed units in them (all planning institutions)
PLANS = [[2010, 8, 1909], [2011, 7, 2022], [2012, 10, 2662], [2013, 7, 2994], [2014, 9, 3052], [2015, 12, 6214], [2016, 17, 8219], [2017, 24, 7725], [2018, 30, 12785],
         [2019, 34, 27977], [2020, 38, 26941], [2021, 42, 18482], [2022, 58, 39903], [2023, 111, 40928], [2024, 156, 57386], [2025, 186, 75925]]
# p.70: complexes declared in the tax track per year and the proposed units
TAXDECL = [[2015, 7, 1186], [2016, 9, 4472], [2017, 20, 7196], [2018, 8, 2875], [2019, 16, 7478], [2020, 29, 12751], [2021, 19, 7087], [2022, 15, 4029], [2023, 38, 17265], [2024, 80, 31806], [2025, 77, 28771]]
# p.26: approved pinui binui units by district, cumulative to the end of 2025 (plans, proposed units)
DISTRICT_APPROVED = [["תל אביב", 246, 96081], ["המרכז", 174, 112068], ["ירושלים", 211, 54349], ["חיפה", 97, 44553], ["הצפון", 12, 4939], ["הדרום", 50, 29789], ["יהודה ושומרון", 1, 600]]
# p.68: preliminary decisions in the tax track, cumulative (complexes, existing units, proposed units); total row printed
TAXPRE = [["תל אביב", 239, 23976, 79732], ["המרכז", 134, 16856, 64000], ["חיפה", 70, 8430, 45463], ["ירושלים", 135, 10778, 44956], ["הדרום", 36, 5939, 30514], ["הצפון", 11, 1101, 9307], ["יהודה ושומרון", 2, 214, 1290]]
check("R25 p.68 tax-track preliminary decisions: 627 / 67,294 / 275,262", [sum(r[i] for r in TAXPRE) for i in (1, 2, 3)], [627, 67294, 275262])
# p.71: tax-track declarations, cumulative by district (complexes, existing, proposed); total printed 337 / 33,488 / 133,321
TAXDIST = [["תל אביב", 146, 14782, 50026], ["המרכז", 73, 7506, 29809], ["ירושלים", 86, 6829, 28749], ["הדרום", 13, 2026, 11031], ["חיפה", 17, 2078, 11901], ["הצפון", 1, 120, 778]]
# The report's own tables do not add up (checked in the PDF images, 26.10.2026): the p.71 rows sum to 336 / 33,341 / 132,294 under a
# printed total of 337 / 33,488 / 133,321, and the p.72 locality chart sums to 337 complexes and 133,044 units. The rows are kept as
# printed; the page quotes the locality rows and the printed total only with this note, never a total of our own.
TAXDIST_TOTAL_PRINTED = [337, 33488, 133321]
check("R25 p.71 rows as transcribed (report total differs, see note)", [sum(r[i] for r in TAXDIST) for i in (1, 2, 3)], [336, 33341, 132294])
# p.72: tax-track declared complexes and proposed units by locality, cumulative to the end of 2025
TAXCITY = [["ירושלים", 84, 27032], ["תל אביב–יפו", 35, 10710], ["בת ים", 23, 10506], ["נתניה", 21, 7679], ["רמת גן", 36, 7070], ["קריית אונו", 16, 6237], ["אשדוד", 7, 5649],
           ["חדרה", 7, 5186], ["הרצלייה", 10, 4597], ["פתח תקווה", 14, 4471], ["קריית גת", 3, 4187], ["רמלה", 3, 3921], ["גבעתיים", 6, 3719], ["אור יהודה", 5, 3118],
           ["ראשון לציון", 4, 2613], ["חולון", 10, 2541], ["חיפה", 4, 2442], ["יהוד–מונוסון", 5, 2197], ["יבנה", 7, 1984], ["באר יעקב", 1, 1880], ["אור עקיבא", 1, 1750],
           ["בית שמש", 2, 1717], ["קריית ים", 1, 1450], ["לוד", 3, 1360], ["רחובות", 2, 1164], ["רמת השרון", 2, 879], ["נוף הגליל", 1, 778], ["טירת כרמל", 2, 773],
           ["אשקלון", 1, 758], ["מעלה אדומים", 1, 750], ["גבעת שמואל", 3, 715], ["רעננה", 5, 665], ["הוד השרון", 3, 540], ["אזור", 1, 390], ["נס ציונה", 1, 387],
           ["פרדס חנה–כרכור", 2, 300], ["בני ברק", 2, 259], ["באר שבע", 1, 242], ["כפר סבא", 1, 233], ["קריית מלאכי", 1, 195]]
check("R25 p.72 by locality adds up to p.71: complexes", sum(r[1] for r in TAXCITY), 337)
check("R25 p.72 by locality as transcribed: proposed units (p.71 prints 133,321)", sum(r[2] for r in TAXCITY), 133044)
# p.92-93: city-wide plans that replace TAMA 38 (buildings in the plan, existing units, proposed units, status); total row printed
REPLACE = [["רמלה", 348, 3959, 4368, "אושרה לתוקף 2024"], ["יבנה", 20, 438, 1088, "אושרה לתוקף 2024"], ["רעננה", 295, 3650, 12163, "אושרה לתוקף 2024"],
           ["כפר סבא", 418, 6634, 13534, "אושרה לתוקף 2025"], ["פתח תקווה", 1304, 16028, 28400, "אושרה לתוקף 2025"], ["באר שבע", 800, 17408, 34508, "אושרה לתוקף 2025"],
           ["לוד", 255, 1671, 4776, "אושרה לתוקף 2025"], ["אשדוד", 2242, 22565, 29980, "בהליכי אישור לתוקף"], ["נהרייה", 6000, 19939, 29500, "מילוי תנאים לתוקף"],
           ["חדרה", 1038, 7897, 19800, "דיון בהתנגדויות"], ["רמת גן", 900, 6695, 21000, "דיון בהתנגדויות"], ["ראשון לציון", 683, 8536, 25167, "מילוי תנאים להפקדה"],
           ["חיפה", 13000, 72171, 103512, "מילוי תנאים להפקדה"], ["בת ים", 2691, 85000, 130000, "הוגש לתנאי סף"], ["בני ברק", 2927, 24140, 34820, "הוגש לתנאי סף"],
           ["אשקלון", 620, 12715, 56215, "הוגש לוועדה המקומית"], ["בית שמש", 202, 3436, 5326, "הכנת מסמכים"], ["רחובות", 2476, 17260, 55000, "התחלת תכנון"],
           ["טירת כרמל", 200, 1714, 4500, "התחלת תכנון"], ["רמת השרון", 75, 962, 2598, "התחלת תכנון"], ["קריית שמונה", 159, 2117, 5937, "התחלת תכנון"]]
check("R25 p.92 replacement plans: buildings / existing / proposed", [sum(r[i] for r in REPLACE) for i in (1, 2, 3)], [36653, 334935, 622192])
NO_EXTENSION = ["בני ברק", "בת ים"]  # p.92: in the listed cities TAMA 38 was extended until the replacement plan is approved, except these two
SELF = [["ירושלים", "בבדיקה תכנונית מוקדמת", True], ["תל אביב–יפו", "בהכנת מסמכי תכנית", False], ["גבעתיים", "אושרה לתוקף 2025 (14,000 יח\"ד קיימות, 22,840 מוצעות)", True]]  # p.93; True = TAMA 38 extended
IN_FORCE_BEFORE = ["הרצלייה", "הוד השרון", "חולון", "יקנעם", "קריית גת", "קריית מוצקין", "רמת השרון"]  # p.93: had a city-wide plan in force on the eve of the expiry
# p.109-110: building renewal, years from the permit request to the permit, by locality (permits in 2025, years)
REQ2PERMIT = [["רמת גן", 39, 6.2], ["רחובות", 8, 6.1], ["ראשון לציון", 26, 6.1], ["הרצלייה", 16, 6.0], ["קריית ים", 1, 6.0], ["אשדוד", 22, 5.8], ["חיפה", 39, 5.7], ["בת ים", 21, 5.5],
              ["קריית ביאליק", 8, 5.4], ["כפר סבא", 6, 5.2], ["גבעתיים", 9, 5.0], ["קריית אונו", 1, 5.0], ["הוד השרון", 5, 5.0], ["רמת השרון", 5, 4.6], ["בני ברק", 6, 4.5],
              ["חדרה", 3, 4.4], ["נתניה", 6, 4.3], ["יבנה", 4, 4.1], ["תל אביב–יפו", 180, 4.1], ["נהרייה", 11, 4.0], ["עכו", 8, 3.6], ["פתח תקווה", 44, 3.6], ["רעננה", 17, 3.4],
              ["ירושלים", 50, 3.4], ["זיכרון יעקב", 3, 2.8], ["נס ציונה", 3, 2.8], ["רמלה", 1, 2.8], ["גני תקווה", 2, 2.3], ["חולון", 10, 2.2], ["קריית אתא", 8, 2.0], ["קריית מוצקין", 6, 1.7]]
# p.41: apartments reported sold in renewal projects in 2025, by locality
SOLD = [["תל אביב–יפו", 1292], ["פתח תקווה", 817], ["ירושלים", 769], ["נתניה", 573], ["רמת גן", 486], ["בת ים", 458], ["אשדוד", 440], ["חיפה", 418], ["גבעתיים", 347], ["חדרה", 276],
        ["ראשון לציון", 234], ["רעננה", 222], ["חולון", 217], ["קריית אונו", 216], ["רמת השרון", 213], ["יהוד–מונוסון", 213], ["בית שמש", 160], ["אור יהודה", 149], ["לוד", 140],
        ["הרצלייה", 133], ["קריית גת", 121], ["בני ברק", 109], ["קריית ים", 104]]
# p.34: share of building-renewal permits by track, 2013-2025 (demolition and rebuild %, strengthening %)
PERMIT_SPLIT = [[2013, 28, 72], [2014, 39, 61], [2015, 48, 52], [2016, 42, 58], [2017, 41, 59], [2018, 48, 52], [2019, 51, 49], [2020, 54, 46], [2021, 55, 45], [2022, 55, 45], [2023, 58, 42], [2024, 60, 40], [2025, 65, 35]]
for y, a, b in PERMIT_SPLIT: assert a + b == 100, y   # p.102 prints 52 for strengthening in 2016; p.34 prints 58 (42 + 58 = 100), p.34 kept
# p.102: share of building-renewal permit REQUESTS by track (demolition %, strengthening %)
REQUEST_SPLIT = [[2013, 44, 56], [2014, 50, 50], [2015, 47, 53], [2016, 47, 53], [2017, 49, 51], [2018, 50, 50], [2019, 49, 51], [2020, 58, 42], [2021, 69, 31], [2022, 71, 29], [2023, 72, 28], [2024, 76, 24], [2025, 71, 29]]
for y, a, b in REQUEST_SPLIT: assert a + b == 100, y
# p.96: building renewal 2025 (buildings, units) by track
BUILDING_2025 = {"requests": {"strengthen": [126, 2040], "rebuild": [304, 8638], "total": [430, 10678]},
                 "permits": {"strengthen": [197, 5489], "rebuild": [371, 10347], "total": [568, 15836]},
                 "added": {"strengthen": 2443, "rebuild": 5718, "total": 8161},
                 "occupied": {"strengthen": [96, 2946], "rebuild": [164, 4473], "total": [260, 7419]},
                 "requests2024_units": 25617, "permits2024_units": 15574, "added2024": 7859}
for k in ("requests", "permits", "occupied"):
    check("R25 p.96 %s adds up" % k, [BUILDING_2025[k]["strengthen"][i] + BUILDING_2025[k]["rebuild"][i] for i in (0, 1)], BUILDING_2025[k]["total"])
check("R25 p.96 added units add up", BUILDING_2025["added"]["strengthen"] + BUILDING_2025["added"]["rebuild"], BUILDING_2025["added"]["total"])
# p.22 + the report page: the year in one line
KEY_2025 = {"pb_plans": 186, "pb_units": 75925, "pb_added": 55074, "pb_share": 34, "ur_share_approved": 35, "starts_share": 28, "sold_share": "כל דירה חמישית",
            "permits_units": 28902, "permits_pb_complexes": 38, "permits_pb_units": 13066, "permits_bld_projects": 568, "permits_bld_units": 15836,
            "started_complexes": 86, "started_units": 65461, "started_added": 48701, "bld_plans": 5, "bld_plans_added": 14084, "replace_plans": 21, "replace_added": 286500,
            "minhalot": 51, "tax_new": 77, "tax_new_units": 28771, "budget_m": 366, "ombud_filed": 135, "ombud_closed": 73, "ombud_decided": 185}
check("R25 p.22 permits = pinui binui + building renewal", KEY_2025["permits_pb_units"] + KEY_2025["permits_bld_units"], KEY_2025["permits_units"])
check("R25 p.25 2025 row = p.22", (PLANS[-1][1], PLANS[-1][2]), (KEY_2025["pb_plans"], KEY_2025["pb_units"]))
check("R25 p.70 2025 row = p.68", (TAXDECL[-1][1], TAXDECL[-1][2]), (KEY_2025["tax_new"], KEY_2025["tax_new_units"]))
check("R25 p.87 2025 = the urtrack average", (APPROVAL_TO_PERMIT[-1][1], APPROVAL_TO_PERMIT[-1][2]), (TRACK["avg"]["years"], TRACK["avg"]["n"]))

# ------------------------------------------------------------------ the law (LAW, LTAMA), the authority (FAQ, SHM, S21, MDL), the tax annex (R25 pp.114-116)
PINUI = {
    "key": "pinui", "built": READ,
    "law": {
        "name": "חוק פינוי ובינוי (עידוד מיזמי פינוי ובינוי), התשס\"ו-2006", "amended": "תשפ\"ג",
        "building_min_apts": 4,                     # s.1 "בית משותף": at least four apartments
        "complex_share": [2, 3],                    # s.1 רוב מיוחס: two thirds of all apartments in the cluster
        "building_share": [3, 5],                   # ... and three fifths in every building of the cluster
        "small_building": {"apts": [4, 5], "min_yes": 3, "min_owners": 3},   # 4 or 5 apartments: at least 3 apartments, more than two owners
        "common_property": "more than half",        # ... and more than half of the common property in every building
        "appraiser_share": [2, 5],                  # s.1 + s.2א: MORE than two fifths of the apartments and of the common property in every building
        "appraiser_days": 15,                       # s.2א(ב): the director names the appraiser within 15 days
        "convention_cancel_below": 0.40,            # s.1ג: signed before the convention / the offer document -> a majority may cancel while under 40% signed
        "offer_doc_days": 14,                       # s.1א(ב): the offer document at least two weeks before the first deal
        "clock": {"half_months": 24, "three_fifths_months": 48, "plan_months": 54, "big_complex_units": 120, "big_complex_extra_months": 12, "public_max": 0.40},  # s.1ד
        "owner_cap": {"min_apts": 6, "cap": 0.30, "extra": 1 / 3},  # s.4
        "elderly_age": 70, "elderly_years": 2, "elderly_out_age": 75,  # s.1 קשיש; s.2(ב)(6), (7)
        "refusal_grounds": ["העסקה לא כדאית כלכלית (אם שמאי פינוי ובינוי קבע שהיא כדאית, זו חזקה עד שיוכח אחרת)",
                            "לא הוצעו מגורים חלופיים לתקופת הבנייה, ולאדם עם מוגבלות: מגורים עם ההתאמות",
                            "לא הוצעו בטוחות הולמות",
                            "נסיבות אישיות מיוחדות שבגללן העסקה בתנאים שסוכמו אינה סבירה",
                            "אדם עם מוגבלות בדירה ודירת הקבע החלופית בלי ההתאמות, או בלי תמורה בשווי ההתאמות",
                            "קשיש (70 במועד העסקה הראשונה, גר בדירה שנתיים) שלא הוצעה לו אף חלופה מהחוק",
                            "בן 75 ומעלה, חולה הנוטה למות או זכאי לגמלת סיעוד ברמה 5 או 6, שלא הוצעה לו חלופה מחוץ לפרויקט"],
        "elderly_options": ["מעבר לבית הורים, לרבות תשלומי איזון, בשווי דומה לשווי המהוון של דירת התמורה",
                            "רכישת דירה חלופית בשווי דומה, ככל הניתן בסמוך לדירה הנוכחית אם ביקש",
                            "סכום כסף בשווי המהוון של דירת התמורה, לרכישת דירה עד מועד הפינוי",
                            "שתי דירות בשווי מצטבר דומה לשווי דירת התמורה",
                            "דירה קטנה יותר בפרויקט עם תשלומי איזון, בשווי דומה"],
        "elderly_out": 3,                           # the first three are the out-of-project options (s.2(ב)(6)(א)), required for 75+ (s.2(ב)(7))
        "abusive": ["חתימה בשפה שבעל הדירה לא מבין, בלי הסבר של עיקרי העסקה בשפה שהוא מבין",
                    "ניצול מוגבלות רפואית, נפשית או שכלית שהיזם ידע או היה צריך לדעת עליה",
                    "מצג שהחותם מטעם היזם הוא נציג של רשות ציבורית",
                    "מידע מטעה, כולל על מספר החותמים או על התנאים שהוסכמו עם אחרים"],
        "deal_must": ["העקרונות לקביעת התמורה של כל בעל דירה", "המועדים המרביים לאישור תכנית מפורטת, להיתר בנייה ולמסירת הדירה החדשה",
                      "הגורם שיבצע את הבנייה, או התנאים לבחירתו וניסיונו", "התחייבות היזם להעמיד ערבויות לטובת בעל הדירה"],
        "disclosure": "מי שפועל מטעם יזם, מקבל ממנו תמורה או ששכרו תלוי בעסקה חייב לומר זאת בפנייה הראשונה ובהסכם, ולדווח על כל שינוי לא זניח בתמורה של בעל דירה אחר; הפרה מאפשרת לחזור מההסכמה גם אחרי חתימה (סעיף 6)",
        "src": "LAW",
    },
    "tama_law": {  # LTAMA ss.4, 5, 5א, 5ב(ב1), 5ג: the comparison rows of the building tracks
        "expand_share": 0.60, "new_apts": [2, 3], "rebuild": [2, 3], "rebuild_min_apts": 4, "elderly_age": 75,
        "clock": {"half_months": 18, "majority_months": 36, "permit_request_months": 42}, "src": "LTAMA",
    },
    "complex_def": {"min_existing": 24, "min_new": 70, "or_double": True, "src": "R25 p.114"},
    "tax": {  # R25 annex A pp.115-116 (pinui binui complexes)
        "shevach": "פטור ממס שבח לפי פרק חמישי 4 לחוק מיסוי מקרקעין", "purchase": "פטור ממס רכישה לבעלי הדירות הקיימות", "vat": "מע\"מ בשיעור אפס על שירותי הבנייה (סעיף 31א לחוק מע\"מ)",
        "units_limit": "אין הגבלה על מספר הדירות של אותו אדם", "downsize": "בעסקת שנמוך (דירה קטנה יותר ותשלום): פטור לדירה אחת במתחם",
        "cap_sqm": 120, "cap_value_pct": 150, "cap_grow_pct": 50, "cap_grow_max_sqm": 200, "rent_note": "בתוספת דמי שכירות לתקופת הביניים וההוצאות הכרוכות בה, כפי שקבע המנהל",
        "betterment": "היטל השבחה של 25% מההשבחה במתחם מוכרז; ממאי 2022 רשות מקומית רשאית לקבוע לפי אזורים 25%, 50% או פטור מלא, לתכניות שייקלטו עד מאי 2027",
        "ila": "פטור מדמי היתר לרמ\"י בבנייה רוויה", "src": "R25 pp.115-116"},
    "tama_tax": {"shevach": "פטור לפי פרק חמישי 5, בתוקף עד סוף 2033", "units": "בהריסה ובנייה: 2 דירות בבניין; בחיזוק ועיבוי: ללא הגבלה",
                 "cap_strengthen_sqm": 25, "cap_rebuild_sqm": 25, "cap_rebuild_value": 1777600, "betterment_tama": "פטור מלא לזכויות שבתמ\"א; בהריסה ובנייה 25% על זכויות שמעבר ל-2.5 קומות טיפוסיות מורחבות",
                 "betterment_fast": "25% על הזכויות המרביות שבחוק ו-50% על כל תוספת", "src": "R25 pp.115-116"},
    "authority": {"appraiser_free": True, "appraiser_share_service": 0.40, "pays": "היזמים משלמים על מלוא עלויות הפרויקט: הבנייה, שכר הדירה ואנשי המקצוע של הדיירים", "src": "FAQ, SHM"},
    "s21": {"updated": "2022-06-13", "old_sqm": 25, "old_profit": 20, "src": "S21"},
    "model": {"evac_months": 36, "mamad_sqm": 12, "land_sqm": 90, "tenant_costs_pct": 5, "fund_years": 10, "fund_amount": 350, "fund_share_pct": 65, "dev_ptax_pct": 5, "profit_pct": 20, "src": "MDL"},
    "series": {"approval_to_permit": APPROVAL_TO_PERMIT, "plans": PLANS, "taxdecl": TAXDECL, "district_approved": DISTRICT_APPROVED, "src": "R25 pp.25, 26, 70, 87"},
    "key2025": KEY_2025,
    "sources": SRC,
}

URCITY = {
    "key": "urcity", "built": READ,
    "replace": [{"c": city(r[0]), "name": nodash(r[0]), "bld": r[1], "e": r[2], "p": r[3], "st": r[4], "ext": r[0] not in NO_EXTENSION} for r in REPLACE]
               + [{"c": city(r[0]), "name": nodash(r[0]), "st": r[1], "ext": r[2], "self": True} for r in SELF],
    "inforce": [city(c) for c in IN_FORCE_BEFORE],
    "req2permit": [{"c": city(r[0]), "n": r[1], "y": r[2]} for r in REQ2PERMIT],
    "sold": [{"c": city(r[0]), "n": r[1]} for r in SOLD],
    "taxcity": [{"c": city(r[0]), "n": r[1], "p": r[2]} for r in TAXCITY],
    "taxpre": TAXPRE, "taxdist": TAXDIST, "taxdist_total_printed": TAXDIST_TOTAL_PRINTED, "taxcity_sum": [337, 133044], "permit_split": PERMIT_SPLIT, "request_split": REQUEST_SPLIT, "building2025": BUILDING_2025, "key2025": KEY_2025,
    "district": {c["city"]: c["district"] for c in STATS["file"]["cities"]},
    "tama": {"expired": "2023-10", "extension": "עד מאי 2026 או עד אישור התכנית העירונית, המוקדם מביניהם", "tlv_no_extension": True, "permit_before": "1980-01-01", "permit_until_with_engineer": "1984-12-31", "src": "R25 pp.90-93, 114"},
    "fast": {"section": "145א1 לחוק התכנון והבנייה (תיקון 139)", "rebuild": 400, "rebuild_merge3": 500, "strengthen": 200, "move_rebuild": 300, "move_strengthen": 100, "order": [450, 500, 550], "permit_at_deposit": True, "src": "R25 p.94"},
    "tracks": [  # R25 annex A p.114 (rows the comparison table and the tool print)
        {"id": "pb", "name": "פינוי בינוי (מתחם)", "do": "הריסת המתחם ובנייה מחדש, או עיבוי בנייה במתחם", "bld": "ללא מגבלת גיל לבניין", "route": "תכנית מפורטת בוועדה מחוזית, בותמ\"ל או בוועדה מקומית עצמאית מיוחדת, ואחריה היתר בוועדה המקומית",
         "declare": "יש", "plan": "יש", "scope": "מתחם עם 24 יחידות קיימות לפחות, בדרך כלל כמה בניינים סמוכים ושטחים ציבוריים", "rights": "זכויות מוקנות לפי התכנית: 70 יחידות לפחות או הכפלה, הגבוה מביניהם"},
        {"id": "tama", "name": "תמ\"א 38 (בניין)", "do": "חיזוק ותוספת לבניין ולדירות, או הריסה ובנייה מחדש", "bld": "היתר לפני 1.1.1980, או עד 31.12.1984 באישור מהנדס שלא נבנה לפי תקן רעידות אדמה", "route": "היתר בנייה מכוח התמ\"א בוועדה המקומית, בלי תכנית",
         "declare": "אין", "plan": "אין", "scope": "בניין שנקבע לגביו בתכנית מפורטת, בגובה 2 קומות לפחות ובשטח כולל של יותר מ-400 מ\"ר", "rights": "זכויות מותנות, עד המרבי שבתמ\"א, לפי שיקול הוועדה המקומית"},
        {"id": "fast", "name": "תכנית לרישוי מהיר (חלופת שקד)", "do": "בעיקר הריסה ובנייה של בניין, או חיזוק", "bld": "כמו בתמ\"א 38", "route": "תכנית מפורטת והיתר, שתיהן בוועדה המקומית; בקשה להיתר כבר בהפקדה",
         "declare": "אין", "plan": "יש", "scope": "בניין בנוי ב-2 קומות לפחות ובו 4 יחידות דיור לפחות", "rights": "זכויות מותנות, עד המרבי שבתיקון 139, לפי החלטת הוועדה המקומית"},
    ],
    "sources": SRC,
}
URCITY["law"] = {"complex_share": PINUI["law"]["complex_share"], "building_share": PINUI["law"]["building_share"], "tama": PINUI["tama_law"], "complex_def": PINUI["complex_def"],
                 "tax": {"pb": PINUI["tax"], "tama": PINUI["tama_tax"]}, "approval_to_permit": APPROVAL_TO_PERMIT[-1]}

# every report city must fold to a map city or be a known report-only city
known_only = {"גני תקווה", "קריית שמונה", "נהרייה"}
for lst, nm in ((REQ2PERMIT, "p.109"), (SOLD, "p.41"), (TAXCITY, "p.72"), (REPLACE, "p.92")):
    miss = [r[0] for r in lst if city(r[0]) not in MAPC and r[0] not in known_only]
    check("R25 %s cities fold to a map city" % nm, miss, [])
for nm, js in (("pinui.json", PINUI), ("urcity.json", URCITY)):
    s = json.dumps(js, ensure_ascii=False, separators=(",", ":"))
    check(nm + " has no long dash", bool(re.search(r"[–—]", s)), False)
if bad:
    print("FAILED:", bad); sys.exit(1)
for nm, js in (("pinui.json", PINUI), ("urcity.json", URCITY)):
    s = json.dumps(js, ensure_ascii=False, separators=(",", ":"))
    io.open(os.path.join(DATA, nm), "w", encoding="utf-8", newline="").write(s)
    print("wrote", nm, len(s.encode()), "bytes")
