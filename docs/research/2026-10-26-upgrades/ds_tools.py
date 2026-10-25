# -*- coding: utf-8 -*-
"""Design-system components for the upgrade-loop tools (DS artifact L9Nqz7Viv7K3MYeZrBc9s8): a live preview that runs the real engine
(core.css + core.js) and the real tool files on the real data, a few cases each, plus the page infographics, and a README.
  python docs/research/2026-10-26-upgrades/ds_tools.py Concrete466 | DekelTools"""
import io, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
I = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
DS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components"
rd = lambda *p: io.open(os.path.join(*p), encoding="utf-8").read()
sys.path.insert(0, os.path.join(H, "q5-ti-466"))


def q5_figs():
    import infographics as ig5
    return [("איור עמוד: ת\"י 466 בבניין, כל חלק בדיו שרטוט משלו (כחול, ירוק, אדום, סגול, גרפיט)", ig5.building_svg()), ("איור עמוד: ציר המהדורות, מלא בתוקף וחלול הוחלף", ig5.timeline_svg())]


COMP = {
    "Concrete466": {
        "files": ["t466.js"], "data": ["t466.json"], "key": "t466",
        "subtitle": "ת\"י 466 לפי המצב שלכם: החלקים שחלים, המהדורה והמחיר, מי אחראי ומה לשאול, וחתך בניין שמדליק את האלמנטים",
        "cases": [("t466", None, "ברירת המחדל: דירה חדשה מקבלן, תקרות יצוקות. חלקים 1 ו-2, המסגרת המקווקוות של חלק 1 סביב כל המבנה"),
                  ("t466", "newh", "דירה חדשה עם תקרות לוח\"דים: חלק 5 נדלק בגרפיט"), ("t466", "crack", "סדק או ברזל חשוף: חלק 1 ות\"י 26 חלק 6")],
        "figs": q5_figs,
        "palette": "פלטה: גיליון שרטוט קונסטרוקציה. נייר לבן, קו שחור, בטון בקווקוו נקודות ומשולשים, חמש דיו שרטוט לחמשת החלקים. IBM Plex Sans Hebrew ו-IBM Plex Mono. לא שמנת, לא זהב, לא כרטיס כהה.",
        "readme": "# Concrete466\n\nThe chooser of /glossary/תי-466/ (HAD-601, Q5 stage 2, release 1.72.522). A situation (buying new and the slab type, opening a concrete wall, building a house, a crack or exposed rebar, prestressed, precast or hollow-core slabs) gives the parts of the concrete code that apply, each with its edition in force and SII price, who is responsible, the questions to ask, the related standards and the free reading room at SII. The drawing: a section through a residential building, each element in the drafting ink of its part, lit when it applies; part 1 as a dashed frame around the whole structure.\n\n**Honesty.** Scope lines from the SII pages only, no clause text, no thresholds, no legal entitlements. Prices as SII shows them on 25.10.2026, incl. VAT.\n\n**Look.** A structural drawing sheet: white paper, black line work, the dots-and-triangles concrete hatch, five drafting inks (blue #1F4FA3, green #2E7D4F, red #C42550, violet #6B4FA0, graphite #5E6A75). Plex Sans Hebrew and Plex Mono.\n",
    },
    "DekelTools": {
        "files": ["dekel.js"], "data": ["dekel.json"], "key": "dekel",
        "subtitle": "מחירון דקל: איזה מחירון לאיזו עבודה (עץ בחירה), ובדיקת הצעת מחיר מול מחירי דקל עם השאלות לקבלן",
        "cases": [("dkpick", None, "ברירת המחדל: פרויקט חדש של 2.5 מיליון ₪, המחירון לבנייה ותשתיות, בתוך הטווח"), ("dkpick", "reno", "שיפוץ של 90 אלף ₪: מתחת לטווח של המחירון לשיפוצים, אזהרה באדום"),
                  ("dkquote", None, "בדיקת הצעה בלי מחירים: השאלות לפי הכללים של דקל מופיעות כבר עכשיו. אין במחשבון אף מחיר של דקל")],
        "figs": None,
        "palette": "פלטה: כתב כמויות מודפס ומסומן. נייר לבן, רשת גרפיט, כותרות בדיו כחולה #1F4FA3, אדום הבודק רק לחריגה. IBM Plex Sans Hebrew ו-IBM Plex Mono לקודים ולמספרים.",
        "readme": "# DekelTools\n\nTwo tools of /glossary/מחירון-דקל-לבנייה-ותשתיות/ (HAD-601, Q3 stage 2, release 1.72.522), one file tools/dekel.js.\n\n**dkpick.** The kind of work and its size give the Dekel list that fits (building and infrastructure, renovation and maintenance, framework agreements, private house, tenant changes, apartment renovation, the per-m² calculator), its chapters and items, and a red warning when the size is outside the band the list is calibrated for (800 thousand to 6 million; 150 to 500 thousand). A decision tree lights the path.\n\n**dkquote.** A contractor's quote line by line (quantity, the reader's own Dekel unit price, the quote's unit price): totals, the gap in ₪ and %, and the questions to the contractor from Dekel's own rules (disposal up to 15 km but not the landfill fee, steel priced apart, remote areas and night work in \"תוספות והפחתות\", the monthly edition).\n\n**Honesty.** No Dekel price is stored or shown; Dekel sells them. Every rule is from Dekel's FAQ and list pages, 25.10.2026.\n",
    },
    "Mortgage2": {
        "files": ["mortgage.js"], "data": ["boi-mortgage.json"], "key": "boim", "custom": True,
        "subtitle": "מחשבון משכנתא 2.0: מסלולים, שיטות, גרייס, תרחישי ריבית, בדיקת התמהיל מול הוראה 329, פירעון מוקדם, וההצעה מהבנק מול הממוצע של בנק ישראל",
        "cases": [("mortgage", None, "ברירת המחדל: 1.2 מיליון ₪ בשלושה מסלולים, ההחזר הראשון, ההחזר הגבוה, בדיקת הכללים, הגרפים ולוח הסילוקין")],
        "figs": None, "out": "u1-mortgage-calculator",
        "palette": "פלטה: מכשירי NadLan (ים #2F6F86, דיו #12202A, אדום מדידה #C42550 לחריגה), Karantina לכותרת, IBM Plex Sans Hebrew ו-IBM Plex Mono. בלי שמנת, זהב או גרדיאנט.",
        "readme": """# Mortgage2

Mortgage 2.0 for /mortgage-calculator/ (HAD-601, U1). Tracks with method, grace, CPI and prime paths; payment, loan or price modes; the three uniform Bank of Israel baskets; directive 329 checks; prepayment with the fee estimate; the bank offer against the BoI average for the same track and term, placed among last month's 10,272 loans. Data: boi-mortgage.json (BoI SDMX, BoI xls, CBS 120010, 25.10.2026), every value dated. Built locally by an Opus builder, math cross-checked in Python (16 cases), old calculators reproduced exactly (6,625 / 8,051; 5,627 / 25.6%).
""",
    },
    "NrmForeign": {
        "files": ["nrm.js"], "data": ["ptax.json", "nrm.json", "boi-fx.json"], "key": "nrm", "custom": True,
        "out": "u3-en-mortgage", "outname": {"en": "index.html", "he": "he.html"},
        "subtitle": "Israel mortgage calculator for foreigners: the loan cap by citizenship, the purchase tax by residency, the income test in your currency, the 10% shekel swing",
        "langs": {
            "en": [("nrm", None, "1 · Default: a non-citizen, ₪4,000,000 home, 50% loan, $12,000 net a month. The status cap binds, not the income"),
                   ("nrm", "abroad", "2 · Israeli citizen living abroad: 75% loan by citizenship, the 8% purchase tax by residency"),
                   ("nrm", "cash", "3 · What $800,000 buys: the highest price after tax and fees, thirds mix (basket 2), stacked bar")],
            "he": [("nrm", None, "1 · ברירת המחדל: בלי אזרחות ישראלית, דירה ב־4,000,000 ₪, מימון 50%, הכנסה של $12,000 נטו בחודש"),
                   ("nrm", "oleh", "2 · עולה חדש בישראל: מימון 75%, מס רכישה לפי תקנה 12א"),
                   ("nrm", "couple", "3 · זוג, אחד ישראלי: תקרה משוקללת 62.5%")],
        },
        "figs": None,
        "palette": "Palette: passport navy #1E2B47, visa violet #5B3FA0, security-print teal #0F7C7A, cool paper #F6F8FA, slate #2B3440; figures in IBM Plex Mono, copy in IBM Plex Sans (Plex Sans Hebrew in Hebrew). Not cream, not brass, not an acid accent on black: the colours of passports, visa stamps and banknote security print.",
        "readme": "# NrmForeign\n\nThe Israel mortgage calculator for foreigners (nrm v2, U3): your Israeli borrowing limit by passport and paycheck. Status (non-citizen, Israeli citizen with or without a home or selling, new oleh, mixed couple), where you live, borrow or cash mode, income and commitments in your currency, appraisal, track mix from the Bank of Israel uniform baskets or a foreign currency loan for non-citizens. Out: the status cap, the income caps at 50% and one third and which binds, first payment, prime +1, a year of CPI, cash to close with the right purchase tax track, the 10% shekel swing, warnings, dated sources. English and Hebrew. Math: tools/instruments/test_nrm_math.py.\n",
    },
    "InvestMap": {
        "files": ["invest.js"], "data": ["invest.json"], "key": "invest", "custom": True,
        "subtitle": "מפת התשואה והתזרים: 65 ערים, כמה מהמחיר שכר הדירה מחזיק כמשכנתא, תשואה ברוטו, תזרים חודשי, מצב תקציב ודירוג ערים",
        "cases": [("invest", None, "ברירת המחדל: עיר אחת, 4 חדרים, תשואה, תזרים, מסלולי מס על שכר דירה וגרף הערים")],
        "figs": None, "out": "u2-investment",
        "palette": "פלטה: מכשירי NadLan, ירוק #00806A במקום #1F7A5A שנכשל בבדיקת הניגודיות. IBM Plex Sans Hebrew ו-IBM Plex Mono.",
        "readme": """# InvestMap

The yield and cash-flow map for /investment/ (HAD-601, U2). 72 cities and the national median, 3 to 5 rooms: the share of the price that rent alone carries as a mortgage, gross yield, monthly payment and cash flow, own money, purchase tax in months of rent; a budget mode ranking the cities that fit; the three rental-tax tracks; a ranked chart and a yield-against-price chart. Data: invest.json from 148 nadlan.gov.il files (20.8.2026), BoI 4.62% (8.2026), CBS rent index. Built locally by an Opus builder; math test passes.
""",
    },
}


def build_langs(name):
    """A tool with several data files and an English and a Hebrew block: one page per language, <html lang> and the section's lang
    set to it (the engine and the tool follow them), every data file keyed as the shortcode would load it."""
    c = COMP[name]; D = os.path.join(DS, name); os.makedirs(D, exist_ok=True)
    css, core = rd(I, "core.css"), rd(I, "core.js")
    js = "".join("<script>" + rd(I, "tools", f) + "</script>" for f in c["files"])
    datas = [json.loads(rd(I, "data", f)) for f in c["data"]]
    dd = {}
    for i, x in enumerate(datas):
        dd[x.get("key") or ("d%d" % i)] = x; dd["d%d" % i] = x
    out = os.path.join(H, c["out"], "preview"); os.makedirs(out, exist_ok=True)
    fonts = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@600'
             '&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&family=Karantina:wght@700&display=swap">')
    for lg, cases in c["langs"].items():
        d = "ltr" if lg == "en" else "rtl"
        face = '"IBM Plex Sans",system-ui,sans-serif' if lg == "en" else '"IBM Plex Sans Hebrew",system-ui,sans-serif'
        body = []
        for i, (tid, preset, note) in enumerate(cases):
            body.append('<p class="n">%s</p><section class="nli" dir="%s" lang="%s"><div class="nli-host" data-nli="%s" id="h%d"%s></div></section>' % (note, d, lg, tid, i, (" data-nli-set='{\"preset\":\"%s\"}'" % preset) if preset else ""))
        body.append('<p class="n">%s</p>' % c["palette"])
        html = ('<!-- @dsCard group="Tools" height=2400 subtitle="%s" -->\n' % c["subtitle"]
                + '<!doctype html><html lang="%s" dir="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title>' % (lg, d, name) + fonts
                + '<style>' + css + '\nbody{margin:0;background:#F4F6FA;color:#12202A;font-family:' + face + '}.w{max-width:1040px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-left,0px))}'
                + '.n{font:500 12px/16px "IBM Plex Mono",monospace;color:#5E6A75;margin:26px 0 8px;border-top:1px solid #D3DCE2;padding-top:8px}</style></head><body><div class="w">'
                + "".join(body) + '</div><script>' + core + '</script><script>var D=' + json.dumps(dd, ensure_ascii=False) + ';var SP={};NadLanInstruments.register=function(id,s){SP[id]=s};</script>' + js
                + '<script>' + "".join(('SP["%s"].custom(document.getElementById("h%d"),D);' % (tid, i)) if c.get("custom") else ('NadLanInstruments.mount(document.getElementById("h%d"),SP["%s"],D);' % (i, tid)) for i, (tid, _, _) in enumerate(cases)) + '</script></body></html>')
        io.open(os.path.join(out, c["outname"][lg]), "w", encoding="utf-8").write(html)
        io.open(os.path.join(D, "preview.html" if lg == "en" else "preview-%s.html" % lg), "w", encoding="utf-8").write(html)
        print(name, lg, len(html.encode()), "bytes ->", os.path.join(out, c["outname"][lg]))
    io.open(os.path.join(D, "README.md"), "w", encoding="utf-8").write(c["readme"])


def build(name):
    if COMP[name].get("langs"):
        return build_langs(name)
    c = COMP[name]; D = os.path.join(DS, name); os.makedirs(D, exist_ok=True)
    css, core = rd(I, "core.css"), rd(I, "core.js")
    js = "".join("<script>" + rd(I, "tools", f) + "</script>" for f in c["files"])
    data = json.loads(rd(I, "data", c["data"][0]))
    body = []
    mounts = []
    for i, (tid, preset, note) in enumerate(c["cases"]):
        body.append('<p class="n">%d · %s</p><section class="nli" dir="rtl" lang="he"><div class="nli-host" data-nli="%s" id="h%d"%s></div></section>' % (i + 1, note, tid, i, (" data-nli-set='{\"preset\":\"%s\"}'" % preset) if preset else ""))
        mounts.append((i, tid))
    if c["figs"]:
        for j, (note, svg) in enumerate(c["figs"]()):
            body.append('<p class="n">%d · %s</p><div class="fig">%s</div>' % (len(c["cases"]) + j + 1, note, svg))
    body.append('<p class="n">%s</p>' % c["palette"])
    html = ('<!-- @dsCard group="Tools" height=2400 subtitle="%s" -->\n' % c["subtitle"]
            + '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + name + '</title>'
            + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
            + '<style>' + css + '\nbody{margin:0;background:#F4F6FA;color:#12202A;font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif}.w{max-width:1040px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-left,0px))}'
            + '.n{font:500 12px/16px "IBM Plex Mono",monospace;color:#5E6A75;margin:26px 0 8px;border-top:1px solid #D3DCE2;padding-top:8px}.fig{background:#fff;border:1px solid #D3DCE2;padding:12px;max-width:664px}</style></head><body><div class="w">'
            + "".join(body) + '</div><script>' + core + '</script><script>var DATA=' + json.dumps(data, ensure_ascii=False) + ';var SP={};NadLanInstruments.register=function(id,s){SP[id]=s};</script>' + js
            + '<script>var D={};D["' + c["key"] + '"]=DATA;D.d0=DATA;' + "".join(('SP["%s"].custom(document.getElementById("h%d"),D);' % (tid, i)) if c.get("custom") else ('NadLanInstruments.mount(document.getElementById("h%d"),SP["%s"],D);' % (i, tid)) for i, tid in mounts) + '</script></body></html>')
    io.open(os.path.join(D, "preview.html"), "w", encoding="utf-8").write(html)
    io.open(os.path.join(D, "README.md"), "w", encoding="utf-8").write(c["readme"])
    out = os.path.join(H, c.get("out") or ("q5-ti-466" if name == "Concrete466" else "q3-dekel-list"), "preview"); os.makedirs(out, exist_ok=True)
    io.open(os.path.join(out, name + "-preview.html"), "w", encoding="utf-8").write(html)
    print(name, len(html.encode()), "bytes")


for n in sys.argv[1:] or COMP:
    build(n)
