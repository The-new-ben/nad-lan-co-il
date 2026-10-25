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
}


def build(name):
    c = COMP[name]; D = os.path.join(DS, name); os.makedirs(D, exist_ok=True)
    css, core = rd(I, "core.css"), rd(I, "core.js")
    js = "".join("<script>" + rd(I, "tools", f) + "</script>" for f in c["files"])
    data = json.loads(rd(I, "data", c["data"][0]))
    body = []
    mounts = []
    for i, (tid, preset, note) in enumerate(c["cases"]):
        body.append('<p class="n">%d · %s</p><section class="nli" dir="rtl" lang="he"><div class="nli-host" id="h%d"%s></div></section>' % (i + 1, note, i, (" data-nli-set='{\"preset\":\"%s\"}'" % preset) if preset else ""))
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
            + '<script>var D={};D["' + c["key"] + '"]=DATA;' + "".join('NadLanInstruments.mount(document.getElementById("h%d"),SP["%s"],D);' % (i, tid) for i, tid in mounts) + '</script></body></html>')
    io.open(os.path.join(D, "preview.html"), "w", encoding="utf-8").write(html)
    io.open(os.path.join(D, "README.md"), "w", encoding="utf-8").write(c["readme"])
    out = os.path.join(H, "q5-ti-466" if name == "Concrete466" else "q3-dekel-list", "preview"); os.makedirs(out, exist_ok=True)
    io.open(os.path.join(out, name + "-preview.html"), "w", encoding="utf-8").write(html)
    print(name, len(html.encode()), "bytes")


for n in sys.argv[1:] or COMP:
    build(n)
