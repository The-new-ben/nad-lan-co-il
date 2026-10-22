# -*- coding: utf-8 -*-
"""/prices-greece/: the Greece price list (Ben 22.10.2026: "the most comprehensive there is ... prove it"; HAD-592). Built from
prices.json (263 places with a price; sources, periods, retrieval dates: prices.md), paid-dkg.json (medians of the prices
actually recorded in the official Property Transfer Values Registry, January to May 2026, as analysed by DKG Development,
published 29.6.2026, updated 29.7.2026; the text is in the private research folder), and the competitor DNA (dna.md).
Writes pages/prices-greece.html + .json.   python docs/research/2026-10-22-greece-prices/build_page.py"""
import io, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
sys.path.insert(0, os.path.join(REPO, "tools", "guides"))
import nlag as K  # noqa: E402
D = json.load(io.open(os.path.join(H, "prices.json"), encoding="utf-8"))
PAID = json.load(io.open(os.path.join(H, "paid-dkg.json"), encoding="utf-8"))
FX = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "boi-fx.json"), encoding="utf-8"))
fx = FX["fx"]["EUR"]["rate"]; n = K.num
P = {p["id"]: p for p in D["places"] if p.get("sale_eur_m2")}
ALL = [p for p in P.values() if not p["id"].startswith("grp-") and not (p["type"] == "region" and not p["id"].startswith("ru-"))]
pct = lambda x, d=1: ("%." + str(d) + "f") % (100 * x) + "%"
sgn = lambda x: ("+" if x >= 0 else "") + pct(x)
ILS = lambda e: "₪" + n(e * fx)
NAT = D["national"]["indomio"]
OUT = os.path.join(H, "pages"); os.makedirs(OUT, exist_ok=True)

# ---------------- asking vs paid (the registry medians; regional units and Athens municipalities)
MAP = {"East Attica": None, "Athens": "ath-centre", "Halkidiki": "ru-halkidiki", "Piraeus": "piraeus", "Thessaloniki": "ru-thessaloniki", "Dodecanese": "ru-dodecanese",
       "Kavala": "ru-kavala", "Ioannina": "ru-ioannina", "Achaia": "ru-achaia", "Corinthia": "ru-corinthia", "Argolis": "ru-argolida", "Xanthi": "ru-xanthi",
       "Magnesia": "ru-magnesia", "Pieria": "ru-pieria", "Evia": "ru-evia", "Serres": "ru-serres", "Drama": "ru-drama", "Laconia": "ru-lakonia", "Imathia": "ru-imathia",
       "Kozani": "ru-kozani", "Pella": "ru-pella", "Glyfada": "glyfada", "Chalandri": "chalandri", "Kifisia": "kifisia", "Agios Dimitrios": "agios-dimitrios",
       "Argyroupoli": "argyroupoli", "Neo Psychiko": "neo-psychiko", "Alimos": "alimos", "Palaio Faliro": "palaio-faliro", "Marousi": "marousi", "Ilioupoli": "ilioupoli",
       "Elliniko": "elliniko", "Dafni": "dafni", "Nea Erythraia": "nea-erythraia", "Melissia": "melissia", "Filothei": "filothei"}
gap_rows, gap_bars = [], []
for name, cnt, val in PAID:
    pid = MAP.get(name.strip().split(". ")[-1].strip())
    if not pid or pid not in P: continue
    a = P[pid]["sale_eur_m2"]; b = float(val.replace(",", "")); c = int(cnt)
    gap = a / b - 1
    gap_rows.append(["%s%s" % (P[pid]["name_he"], " (מדגם קטן)" if c < 30 else ""), "<bdi>€%s</bdi>" % n(a), "<bdi>€%s</bdi>" % n(b), "<bdi>%s</bdi>" % (("+" if gap >= 0 else "") + pct(gap, 0)), "<bdi>%d</bdi>" % c])
    if c >= 50 and pid in ("ath-centre", "piraeus", "ru-thessaloniki", "ru-halkidiki", "ru-dodecanese", "ru-kavala", "ru-achaia"):
        gap_bars.append((P[pid]["name_he"].split(" (")[0], round(100 * gap), "+" + pct(gap, 0)))

# ---------------- tables from the price data
regions = [p for p in D["places"] if p["type"] == "region" and not p["id"].startswith(("ru-", "grp-")) and p.get("sale_eur_m2")]
reg_rows = [[p["name_he"], "<bdi>€%s</bdi>" % n(p["sale_eur_m2"]), ("<bdi>%s</bdi>" % sgn(p["sale_yoy"])) if p.get("sale_yoy") is not None else "", ("<bdi>€%.1f</bdi>" % p["rent_eur_m2"]) if p.get("rent_eur_m2") else "", ("<bdi>%s</bdi>" % pct(p["gross_yield"])) if p.get("gross_yield") else ""]
            for p in sorted(regions, key=lambda x: -x["sale_eur_m2"])]
isl = sorted([p for p in ALL if p["type"] == "island"], key=lambda x: -x["sale_eur_m2"])
SEA = {"South Aegean": "דרום הים האגאי (קיקלאדים ודודקנס)", "Ionian Islands": "האיים היוניים", "North Aegean": "צפון הים האגאי", "Attica": "איי המפרץ הסרוני",
       "Thessaly": "ספוראדס", "Central Greece": "ספוראדס ואוויה", "East Macedonia & Thrace": "צפון הים האגאי", "Crete": "כרתים"}
gvs = lambda g: "€800,000" if g == 800000 else "€400,000" if g == 400000 else "לפי המקום" if g == "mixed" else "לבדיקה"
isl_rows = [[p["name_he"], SEA.get(p["region"], p["region"]), "<bdi>€%s</bdi>" % n(p["sale_eur_m2"]), ("<bdi>%s</bdi>" % sgn(p["sale_yoy"])) if p.get("sale_yoy") is not None else "", gvs(p["gv_tier"]), "היתר מראש" if p.get("border_permit") else ""] for p in isl]
LADDER = K.bars("סולם האיים: 15 היקרים, אירו למ״ר", [(p["name_he"], p["sale_eur_m2"], "€" + n(p["sale_eur_m2"])) for p in isl[:15]], note="מחיר מבוקש, Indomio, ספטמבר 2026, ובאיים שאין להם, Spitogatos.")
top = sorted(ALL, key=lambda x: -x["sale_eur_m2"])
risers = sorted([p for p in ALL if p.get("sale_yoy") is not None], key=lambda x: -x["sale_yoy"])
row3 = lambda p: [p["name_he"], "<bdi>€%s</bdi>" % n(p["sale_eur_m2"]), ("<bdi>%s</bdi>" % sgn(p["sale_yoy"])) if p.get("sale_yoy") is not None else ""]
BOG = D["spi_history"]["bank_of_greece_annual_avg_2007eq100"]
yrs = sorted(BOG["whole_country_all"].keys())
CH = K.chart("מדד מחירי הדירות של בנק יוון, ממוצע שנתי (2007 = 100)", yrs, [BOG["greater_athens_all"][y] for y in yrs], [BOG["whole_country_all"][y] for y in yrs], "אתונה רבתי", "כל יוון", every=1)
TR = D["transactions"]["elstat_notarial_property_sales"]["values"]
tr_rows = [[y, "<bdi>%s</bdi>" % n(v)] for y, v in sorted(TR.items())]
NVO = D["price_by_type"]["new_vs_old_spitogatos_2025"]["sale"]
AREA_HE = {"Athens Centre": "מרכז אתונה", "Athens East": "הפרברים המזרחיים", "Athens North": "הפרברים הצפוניים", "Athens South": "הפרברים הדרומיים", "Athens West": "הפרברים המערביים",
           "Piraeus": "פיראוס", "Piraeus suburbs": "פרברי פיראוס", "Thessaloniki municipality": "עיריית סלוניקי", "Thessaloniki suburbs": "פרברי סלוניקי"}
nvo_rows = [[AREA_HE.get(k, k), "<bdi>€%s</bdi>" % n(v["old"]), "<bdi>€%s</bdi>" % n(v["new"]), "<bdi>+%s</bdi>" % pct(v["new"] / v["old"] - 1, 0)] for k, v in NVO.items()]
LUX = [r for r in D["luxury"]["rows"] if r.get("low")]
LUXHE = {"Mykonos": "מיקונוס", "Santorini": "סנטוריני", "Paros": "פארוס", "Athens Riviera": "הריביירה של אתונה", "Ellinikon": "אליניקון", "Porto Heli": "פורטו חלי"}
lux_rows = [[LUXHE.get(r["place"], r["place"]), "<bdi>€%s עד €%s</bdi>" % (n(r["low"]), n(r["high"])) if r.get("high") else "<bdi>€%s</bdi>" % n(r["low"]),
             "חציון היוקרה ומודעת השיא (GEOAXIS)" if "GEOAXIS" in r["what"] else "טווח של בית תיווך (Engel & Völkers)" if "Engel" in r["what"] else "פרויקט או מתווך"] for r in LUX]
cnt800 = sum(1 for p in ALL if p["gv_tier"] == 800000); cnt400 = sum(1 for p in ALL if p["gv_tier"] == 400000)
cheap, dear = top[-1], top[0]

ANSWER = ('<p class="nlag-answer"><strong>כמה עולה דירה ביוון:</strong> המחיר המבוקש הממוצע הוא <bdi>€%s</bdi> למ״ר (Indomio, ספטמבר 2026), %s משנה קודם. במחירים שנרשמו בעסקאות '
          'בפועל המספר נמוך בהרבה: חציון של <bdi>€1,479</bdi> למ״ר לדירה, לפי רישום העסקאות הרשמי של ינואר עד מאי 2026. דירה של 80 מ״ר עולה, לפי המחיר המבוקש, מכ־<bdi>€%s</bdi> ב%s '
          'ועד כ־<bdi>€%s</bdi> ב%s. במפה שלמטה %d מקומות ביוון, כל אחד עם המחיר שלו, השכירות, התשואה וסף הגולדן ויזה.</p>'
          % (n(NAT["sale_eur_m2"]), sgn(NAT["sale_yoy"]), n(round(cheap["sale_eur_m2"] * 80, -3)), cheap["name_he"], n(round(dear["sale_eur_m2"] * 80, -3)), dear["name_he"], len(ALL)))
CLUSTER = [("/global/greece/", "נדל״ן ביוון", "אזורים, פרויקטים להמחשה ומדריכים"), ("/athens-apartments/", "מחירי אתונה לפי אזור", "שכונות, תשואה והקפאת Airbnb"),
           ("/acquisition-greece/", "מחשבון עלות הקנייה", "השלבים, המסמכים וכל העלויות"), ("/taxation-greece-israel/", "מיסוי דירה ביוון", "מה משלמים ביוון ומה בישראל"),
           ("/short-term-rentals-abroad/short-term-rentals-greece/", "השכרה לטווח קצר ביוון", "AMA, אגרת אקלים והקפאות")]
FAQ = [
    ("כמה עולה דירה ביוון ב־2026?", "המחיר המבוקש הממוצע הוא €%s למ״ר (ספטמבר 2026). במחירים שנרשמו בעסקאות החציון הוא €1,479 למ״ר, ודירה טיפוסית של 68 מ״ר נמכרה בכ־€95,000 (ינואר עד מאי 2026)." % n(NAT["sale_eur_m2"])),
    ("כמה עולה מטר מרובע ביוון?", "בממוצע €%s במודעות. בין המקומות: מ־€%s ב%s ועד €%s ב%s." % (n(NAT["sale_eur_m2"]), n(cheap["sale_eur_m2"]), cheap["name_he"], n(dear["sale_eur_m2"]), dear["name_he"])),
    ("כמה עולה דירה באתונה?", "במרכז אתונה המחיר המבוקש €%s למ״ר, ובעסקאות שנרשמו בעיריית אתונה החציון €1,838. הפירוט לפי אזור נמצא במחירי אתונה לפי אזור." % n(P["ath-centre"]["sale_eur_m2"])),
    ("כמה עולה דירה בסלוניקי?", "במחוז סלוניקי המחיר המבוקש €%s למ״ר, ובעסקאות שנרשמו החציון €1,509." % n(P["ru-thessaloniki"]["sale_eur_m2"])),
    ("כמה עולה בית בכרתים?", "לפי המחוזות: חאניה €%s, הרקליון €%s, רתימנו €%s ולסיתי €%s למ״ר (מחיר מבוקש)." % tuple(n(P[k]["sale_eur_m2"]) for k in ("ru-chania", "ru-heraklion", "ru-rethymno", "ru-lasithi"))),
    ("איפה הכי זול לקנות דירה ביוון?", "בצפון המערבי של היבשה: פלורינה, קסטוריה וגרבנה, מתחת ל־€750 למ״ר במודעות. בין האיים הזולים ביותר: %s." % ", ".join(p["name_he"] for p in isl[-3:])),
    ("איפה הכי יקר ביוון?", "ווליאגמני והריביירה של אתונה, מיקונוס, אנטיפארוס והידרה, מעל €7,000 למ״ר במודעות. ביוקרה עצמה, במיקונוס ובסנטוריני, נכסים נמכרים ב־€14,000 עד €30,000 למ״ר."),
    ("האם מחירי הדירות ביוון עולים?", "כן, אבל לאט יותר: במדד של בנק יוון +5.5% בשנה עד רבעון 2 של 2026, אחרי +9.1% ב־2024. המחירים כבר מעל השיא של 2008."),
    ("מה ההבדל בין מחיר מבוקש למחיר בעסקה?", "המחיר במודעות גבוה בדרך כלל ממה שנרשם בעסקאות. ברוב המחוזות הפער בטבלה כאן הוא עשרות אחוזים, וחלק ממנו כי דירות שנמכרות שונות מדירות שמפורסמות."),
    ("כמה מטרים אפשר לקנות ביוון ב־€150,000?", "אחרי עלויות קנייה של כ־8%%, כ־%s מ״ר במרכז אתונה, כ־%s מ״ר בסלוניקי ויותר מ־150 מ״ר בעיירות בצפון. במחשבון רואים את כל המקומות." % (n(150000 / 1.0826 / P["ath-centre"]["sale_eur_m2"]), n(150000 / 1.0826 / P["thess-municipality"]["sale_eur_m2"]))),
    ("כמה עולה שכירות ביוון?", "בממוצע €%.2f למ״ר לחודש (ספטמבר 2026), כלומר כ־€%s לדירת 70 מ״ר." % (NAT["rent_eur_m2"], n(NAT["rent_eur_m2"] * 70))),
    ("איזה סכום צריך לגולדן ויזה?", "€800,000 באטיקה, ביחידת סלוניקי, במיקונוס, בסנטוריני ובכל אי מעל 3,100 תושבים, ו־€400,000 בשאר יוון, בנכס אחד של 120 מ״ר. €250,000 מספיקים רק להסבה של מבנה מסחרי למגורים או לשיקום מבנה לשימור. בכל שורה במפה מופיע הסף של המקום."),
]
DATASET = {"@context": "https://schema.org", "@type": "Dataset", "name": "מחירון נדל״ן ביוון 2026: מחיר מבוקש למ״ר ב־%d מקומות" % len(ALL),
           "description": "מחיר מבוקש באירו למ״ר, שינוי שנתי, שכירות ותשואה ברוטו לפי אזור, עיר, אי ושכונה ביוון, עם מחירי העסקאות שנרשמו בפועל לפי מחוז.",
           "temporalCoverage": "2025-09/2026-09", "spatialCoverage": {"@type": "Place", "name": "Greece"}, "variableMeasured": ["EUR per square metre (asking)", "gross rental yield", "year-on-year change"],
           "creator": {"@type": "Organization", "name": "nad-lan.co.il", "url": "https://nad-lan.co.il/"}, "isBasedOn": ["https://www.indomio.gr/en/agora-akiniton/", "https://www.spitogatos.gr/", "https://www.xe.gr/", "https://www.bankofgreece.gr/"],
           "url": "https://nad-lan.co.il/prices-greece/", "dateModified": "2026-10-22", "inLanguage": "he"}
body = "\n".join([
    ANSWER,
    K.ledger([("מחיר מבוקש ממוצע", "€%s" % n(NAT["sale_eur_m2"]), "למ״ר · ספטמבר 2026"), ("מחיר בעסקאות, חציון", "€1,479", "למ״ר · ינואר עד מאי 2026"),
              ("שינוי בשנה", sgn(NAT["sale_yoy"]), "מחיר מבוקש · Indomio"), ("שכירות ממוצעת", "€%.2f" % NAT["rent_eur_m2"], "למ״ר לחודש"),
              ("מדד בנק יוון", "+5.5%", "שנה עד רבעון 2 2026"), ("מקומות במחירון", str(len(ALL)), "אזורים, ערים, איים ושכונות")]),
    '[nadlan_tool id="grmap"]',
    '<h2>מחיר מבוקש מול מחיר שנרשם בעסקאות</h2>',
    '<p>כמעט כל מחירון שמתפרסם, גם בעברית, מתבסס על מחירים במודעות. ביוון יש גם מאגר רשמי של הערכים שנרשמו בהעברות, וניתוח של 13,193 העברות מינואר עד מאי 2026 נותן תמונה אחרת: '
    'חציון של <bdi>€1,479</bdi> למ״ר לדירה, ודירה טיפוסית של 68 מ״ר ב־<bdi>€95,000</bdi>. 59% מהדירות נמכרו מעל השווי האובייקטיבי שקובעת המדינה, והחציון היה פי 1.11 ממנו. '
    'הטבלה משווה בין המחיר המבוקש היום לבין החציון שנרשם, מחוז אחרי מחוז. הפער לא כולו הנחה במשא ומתן: דירות שנמכרות בפועל הן לרוב ישנות וקטנות יותר מדירות שמפורסמות.</p>',
    K.bars("כמה המחיר במודעות גבוה מהמחיר שנרשם", gap_bars, unit="", note="מחיר מבוקש: ספטמבר 2026. מחיר בעסקאות: חציון ינואר עד מאי 2026. רק מחוזות עם 50 עסקאות ומעלה."),
    K.table("מחיר מבוקש מול חציון העסקאות, לפי מחוז ועירייה", ["מחוז או עירייה", "מבוקש למ״ר", "נרשם בעסקאות למ״ר", "הפער", "עסקאות"], gap_rows),
    '<h2>המחירים לפי מחוז</h2>',
    '<p>יוון מחולקת ל־13 מחוזות. בחלק מהם אין מספר אחד שמתפרסם, ולכן בטבלה רק המחוזות שיש להם, והשאר נמצאים במפה לפי היחידות האזוריות שלהם. התשואה מחושבת רק כשהשכירות '
    'והמחיר מאותו מקור ומאותו חודש.</p>',
    K.table("המחוזות של יוון, מחיר מבוקש", ["מחוז", "€ למ״ר", "שינוי בשנה", "שכירות למ״ר", "תשואה ברוטו"], reg_rows),
    '<h2>סולם האיים</h2>',
    '<p>%d איים במחירון, מהקיקלאדים ועד האיים היוניים. מיקונוס ואנטיפארוס בראש, והאיים הגדולים כמו כרתים, רודוס וקורפו באמצע. רוב האיים נמצאים בסף של <bdi>€800,000</bdi> '
    'לגולדן ויזה, כי יש בהם יותר מ־3,100 תושבים. באיי הדודקנס, ובהם רודוס וקוס, ובסנטוריני, קונה ישראלי צריך היתר מראש.</p>' % len(isl),
    LADDER,
    K.table("כל האיים, מהיקר לזול", ["אי", "ים", "€ למ״ר", "שינוי בשנה", "גולדן ויזה", "אזור גבול"], isl_rows),
    '<h2>עשר שנים של מחירים</h2>',
    '<p>במדד של בנק יוון המחירים ירדו עד 2017, התחילו לעלות ב־2019, ועברו את השיא של 2008. אתונה עלתה מהר יותר משאר המדינה. במקביל מספר העסקאות כמעט שילש את עצמו: '
    'מ־43,443 העברות ב־2014 ל־145,765 ב־2024, לפי הרשות הסטטיסטית היוונית.</p>', CH,
    K.table("העברות נכסים בנוטריון, כל סוגי הנכסים (ELSTAT)", ["שנה", "העברות"], tr_rows),
    '<h2>דירה חדשה מול דירה ישנה</h2>',
    '<p>דירה חדשה ביוון יקרה בהרבה מדירה ישנה באותו אזור, לפעמים פי 1.8. במדד של בנק יוון דירות חדשות עלו בשנה האחרונה ב־6.2%, וישנות ב־5.0%.</p>',
    K.table("מחיר מבוקש לפי גיל הבניין, 2025 (Spitogatos)", ["אזור", "דירה ישנה", "דירה חדשה", "הפער"], nvo_rows),
    '<h2>מה מקבלים בכל תקציב</h2>',
    '<p>תקציב אחד, כל המקומות: המחשבון מוריד את עלויות הקנייה ומראה כמה מטרים התקציב קונה בכל מקום, מהגדול לקטן. העלויות שהוא מוריד: מס העברה של 3.09%, על המחיר או על השווי האובייקטיבי, הגבוה מהשניים, ועוד נוטריון, רישום בקדסטר, עורך דין ומתווך, יחד כ־8.3% מהמחיר. העלויות המלאות, צעד אחרי צעד, נמצאות ב<a href="/acquisition-greece/">מחשבון עלות הקנייה</a>.</p>',
    '[nadlan_tool id="grbudget" preset="b150"]',
    '<h2>הדירה שלכם בישראל, ביוון</h2>',
    '<p>בוחרים עיר בישראל ומספר חדרים, והמחשבון לוקח את המחיר החציוני הרשמי של העסקאות שם, ממיר ליורו לפי בנק ישראל ומראה כמה מטרים הוא קונה בכל מקום ביוון.</p>',
    '[nadlan_tool id="grisrael" preset="tlv4"]',
    '<h2>הכי יקר, הכי זול, והכי עלה</h2>',
    K.table("10 המקומות היקרים", ["מקום", "€ למ״ר", "שינוי בשנה"], [row3(p) for p in top[:10]]),
    K.table("10 המקומות הזולים", ["מקום", "€ למ״ר", "שינוי בשנה"], [row3(p) for p in top[-10:][::-1]]),
    K.table("10 המקומות שעלו הכי הרבה בשנה", ["מקום", "€ למ״ר", "שינוי בשנה"], [row3(p) for p in risers[:10]]),
    '<p>שינוי שנתי גדול במקום קטן נשען לפעמים על מעט מודעות. בלרוס, למשל, העלייה של 35% מבוססת על מדגם קטן.</p>',
    '<h2>יוקרה: מחירי הקצה</h2>',
    '<p>הממוצעים במחירון מתארים את כל הדירות. בנכסי היוקרה המספרים אחרים לגמרי, והם מגיעים ממקורות אחרים, ולכן הם בטבלה נפרדת ואי אפשר להשוות אותם לממוצע.</p>',
    K.table("נכסי יוקרה, אירו למ״ר", ["מקום", "טווח", "מה המספר"], lux_rows),
    '<h2>גולדן ויזה, אזורי גבול ו־Airbnb, מקום אחרי מקום</h2>',
    '<p>בכל שורה במפה מופיעים שלושה דברים שמשנים את ההחלטה. <b>הגולדן ויזה:</b> ב־%d מקומות הסף <bdi>€800,000</bdi> וב־%d הוא <bdi>€400,000</bdi>, תמיד בנכס אחד של 120 מ״ר לפחות. מסלול שלישי של <bdi>€250,000</bdi> פתוח בכל מקום, אבל רק להסבה של מבנה מסחרי למגורים או לשיקום מלא של מבנה לשימור; '
    'הבדיקה המלאה נמצאת ב<a href="/acquisition-greece/#golden-visa">מדריך הקנייה</a>. <b>אזור גבול:</b> באיי הדודקנס, בסנטוריני, בלסבוס, בכיוס, בסאמוס ובאזורים בצפון היבשה, '
    'ישראלי צריך היתר מראש. <b>Airbnb:</b> במחוזות 1 עד 3 של אתונה ובמרכז סלוניקי אין רישום חדש של השכרה לטווח קצר עד סוף 2026.</p>' % (cnt800, cnt400),
    K.israel("לפני שמתחייבים על נכס", '<p>המחיר הוא רק נקודת הפתיחה. הבעלות, חובות שנשארים על הנכס, חריגות בנייה והיתר אזור גבול נבדקים על ידי עורך דין ביוון, לפני כל מקדמה. '
             'למי שמחפש: <a href="https://jus-tice.co.il/greece-lawyers/">עורך דין ביוון לבדיקת זכויות בנכס</a>.</p>'),
    K.honest("על הנתונים", [
        "המחיר בכל שורה הוא מחיר מבוקש במודעות. %d מהמקומות לפי Indomio, ספטמבר 2026, כדי שכולם יימדדו באותה שיטה ובאותו חודש; היכן שאין, Spitogatos או xe.gr, והתקופה מופיעה ליד המספר." % sum(1 for p in ALL if p.get("sale_provider") == "Indomio.gr"),
        "המחירים שנרשמו בעסקאות: חציונים מתוך מאגר ערכי ההעברה הרשמי, ינואר עד מאי 2026, כפי שנותחו ופורסמו ב־29.6.2026. מחוז עם פחות מ־30 עסקאות מסומן כמדגם קטן.",
        "התשואה ברוטו היא שכירות כפול 12 חלקי המחיר, רק כשהשניים מאותו מקור ומאותו חודש. לפני הוצאות, מסים ותקופות ריקות.",
        "סף הגולדן ויזה באיים קטנים שהאוכלוסייה שלהם קרובה ל־3,100, ובאוויה, מסומן לבדיקה. את הסף של כתובת מסוימת בודק עורך הדין.",
        "יש פערים בין המקורות: באיים Indomio גבוה לפעמים ב־15% עד 30% מ־Spitogatos. בחרנו מקור אחד לכל המחירון כדי שההשוואה בין מקומות תהיה הוגנת.",
        'המקורות הרשמיים של המדד ושל מספר העסקאות: <a href="https://www.bankofgreece.gr/en/statistics/real-estate-market/residential-and-commercial-property-price-indices-and-other-short-term-indices">מדדי מחירי הדירות של בנק יוון</a> ו<a href="https://www.statistics.gr/">הרשות הסטטיסטית של יוון</a>.',
        "העדכון הבא: ינואר 2027, עם מחירי רבעון 4 של 2026."],"השער: €1 = ₪%s, השער היציג של בנק ישראל ב־%s. נבדק 22.10.2026." % (("%.4f" % fx).rstrip("0"), ".".join(str(int(x)) for x in FX["fx"]["EUR"]["date"].split("-")[::-1]))),
    K.faq("שאלות נפוצות על מחירי הנדל״ן ביוון", FAQ),
    K.cluster(CLUSTER),
    '<script type="application/ld+json">' + json.dumps(DATASET, ensure_ascii=False) + '</script>',
])
html = K.wrap(body, '[nadlan_crumbs label="מחירון יוון" hub="/global/|השקעות בחו״ל;/global/greece/|יוון"]')
meta = {"title": "מחירון נדל״ן ביוון 2026: מחיר למ״ר בכל אזור ואי", "seo_t": "כמה עולה דירה ביוון? מחירון 2026 לפי אזור ואי", "crumb": "מחירון יוון",
        "seo_d": "מחירון נדל״ן ביוון: מחיר מבוקש למ״ר ב־%d מקומות (ספטמבר 2026), מחירי עסקאות בפועל, שכירות ותשואה, מפה, מחשבון תקציב והשוואה לדירה שלכם בישראל." % len(ALL)}
io.open(os.path.join(OUT, "prices-greece.html"), "w", encoding="utf-8").write(html)
json.dump(meta, io.open(os.path.join(OUT, "prices-greece.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import re
txt = re.sub(r"<[^>]+>", " ", re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", html, flags=re.S))
print("prices-greece | words", len(re.findall(r"[\w֐-׿]+", txt)), "| bytes", len(html.encode()), "| dashes", len(re.findall(r"[–—]", txt)), "| places", len(ALL), "| gap rows", len(gap_rows), "| islands", len(isl))
