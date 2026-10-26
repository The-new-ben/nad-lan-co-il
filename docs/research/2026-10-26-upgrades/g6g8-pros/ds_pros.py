# -*- coding: utf-8 -*-
"""Claude Design component for G6 G7 G8 (design system artifact, NOT published here): ProsCluster.
preview.html is self-contained: the real engine (core.css + core.js), the three real tool files, the real data files, the presets of
every tool, the top block of each page (H1, answer, CTAs) exactly as the writers emit it, the three numbers tables and the 9 drawings.
  python ds_pros.py      writes <scratchpad>/ds/project/components/ProsCluster/{preview.html,README.md} and preview/ds-ProsCluster.html"""
import html as H_, io, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
I = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
DS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components"
rd = lambda *p: io.open(os.path.join(*p), encoding="utf-8").read()
import infographics as ig  # noqa: E402

PALETTE = ("פלטה: גיליון בדיקה הנדסי ופנקס רשמי. דיו #12202A לטקסט ולכותרות טבלה, ים #2F6F86 למה שבתהליך או בטווח, ים עמוק #1F4B5C למה שקבוע בחוק או מתקיים, קו #D3DCE2 לרשת, "
           "אדום מדידה #C42550 רק לגבול: מועד בחוק, תקרה, ליקוי אחרי התקופה. IBM Plex Sans Hebrew לטקסט ו-IBM Plex Mono למספרים. למה זה לא המראה של AI: אין שמנת, זהב, טרקוטה או גרדיאנט, "
           "אין כרטיסים עם צל רך; הצורות לקוחות מדוח בדק בית, מטבלת אגרות ומפנקס רשמי, וכל צבע אומר מצב.")
TOOLS = [("bedek", ["bedek.json"], [(None, "G6 · 1 · ברירת המחדל: רטיבות בקיר, דירה שנמסרה ב-15.3.2023 (בתקופת הבדק עד 15.3.2027)"), ("cal", "G6 · 2 · לוח הבדיקות לדירה שנמסרה ב-30.6.2025"),
                                          ("apt4", "G6 · 3 · כמה עולה בדק בית לדירת 4 חדרים: כל המחירים שפורסמו"), ("sub", "G6 · 4 · קונים דירה בת 3 שנים: נזילה בצנרת, קונה משנה")]),
         ("shamai", ["shamai.json"], [(None, "G7 · 1 · ברירת המחדל: דרישת היטל השבחה, המועד האחרון לערור"), ("bank", "G7 · 2 · משכנתא: השמאי של הבנק"), ("dec", "G7 · 3 · שמאי מכריע על השבחה של 800 אלף: השכר לפי התקנות")]),
         ("shamaireg", ["shamai.json"], [(None, "G7 · 4 · חיפוש חי בפנקס שמאי המקרקעין (data.gov.il)")]),
         ("orechdin", ["orechdin.json", "ptax.json"], [(None, "G8 · 1 · ברירת המחדל: יד שנייה ב-2.4 מיליון עם משכנתא"), ("new", "G8 · 2 · דירה מקבלן ב-3.2 מיליון: מה מותר לקבלן לגבות"),
                                                       ("lux", "G8 · 3 · דירה מקבלן ב-5 מיליון: מעל התקרה"), ("steps", "G8 · 4 · צעדי העסקה מיום החתימה")])]
FILES = {"bedek": "bedek", "shamai": "shamai", "shamaireg": "shamai", "orechdin": "orechdin"}
README = """# ProsCluster

G6 G7 G8 of the upgrade loop (Ben 26.10.2026): the professionals cluster of nad-lan.co.il. Local build, nothing deployed.
Research and spec: docs/research/2026-10-26-upgrades/g6g8-pros/dna.md.

| Page | Owner of | Tool | What it does |
|---|---|---|---|
| /home-inspection/ | בדק בית (2,900/mo) | bedek | one defect against the Sale (Apartments) Law: inspection period, warranty, burden of proof, notice, repair rule, sub-buyer; the inspection calendar from the handover; every published price by property type with its date and VAT |
| /real-estate-appraiser/ | שמאי מקרקעין (2,400/mo) | shamai + shamaireg | which appraisal (8 purposes): who orders, who pays, the deadline from the reader's date (45 days, 3 years); published prices; the decisive appraiser's fee by regulation; a live search of the official register (3,182) |
| /real-estate-lawyer/ | עורך דין מקרקעין (1,600/mo) | orechdin | published fees against the Bar's recommended minimum, the legal cap on the developer's lawyer (5,915 or 0.5%, none above 4,642,750), Land Registry fees 2026; the steps and the tax dates from the signing day |

**Look.** An engineering report and an official register, not a card deck: ink, sea for ranges and processes, deep sea for what the law fixes, survey red only for a limit or a deadline. Plex Sans Hebrew and Plex Mono. No cream, gold, terracotta or gradient.

**Honesty.** No invented professional, rating or count; the directory's demo profiles are not linked. Prices are published prices with their date and VAT status, never offers. The lawyer page says it is not legal advice and that the site represents no side.
"""


def top_of(content, tool_id):
    i = content.find('[nadlan_tool id="%s"]' % tool_id)
    j = content.rfind('<div class="nl', 0, i)
    return content[:j]


def build():
    D = os.path.join(DS, "ProsCluster"); os.makedirs(D, exist_ok=True)
    css, core = rd(I, "core.css"), rd(I, "core.js")
    dd = {}
    for f in ("bedek.json", "shamai.json", "orechdin.json", "ptax.json"):
        x = json.loads(rd(I, "data", f)); dd[x.get("key")] = x
    body, n = [], 0
    pages = {"bedek": ("g6-page-content.html", "בדק בית: מה בודקים, כמה זה עולה ועד מתי הקבלן אחראי"), "shamai": ("g7-page-content.html", None), "orechdin": ("g8-page-content.html", None)}
    for tid, files, cases in TOOLS:
        if tid in pages:
            content = rd(H, "preview", pages[tid][0])
            if tid == "bedek":
                t = "<h1>%s</h1>" % pages[tid][1] + re.sub(r"<style\b.*?</style>", "", top_of(content, tid), flags=re.S)
            else:
                m = re.search(r'<h2>([^<]+)</h2>\n(<p class="nl[a-z]+-lead">.*?</p>\n<div class="nl[a-z]+-cta">.*?</div>\n(?:<p class="nl[a-z]+-legal">.*?</p>\n)?)', content, flags=re.S)
                t = "<h1>%s</h1>%s" % (m.group(1), m.group(2))
            css_page = re.search(r'<style id="nl[a-z]+-css">.*?</style>', content, flags=re.S).group(0)
            body.append('<p class="n">%s · ראש העמוד כפי שהכותב מדפיס אותו: H1, פסקת התשובה, הכפתורים</p><div class="page">%s%s</div>' % ({"bedek": "G6", "shamai": "G7", "orechdin": "G8"}[tid], css_page, t))
        for preset, note in cases:
            st = ' data-nli-set="%s"' % H_.escape(json.dumps({"preset": preset}, ensure_ascii=False), quote=True) if preset else ""
            body.append('<p class="n">%s</p><section class="nli" dir="rtl" lang="he"><div class="nli-host" data-nli="%s" id="h%d"%s></div></section>' % (note, tid, n, st)); n += 1
    for k, f in ig.ALL.items():
        body.append('<p class="n">איור %s</p><div class="page"><figure class="fig">%s</figure></div>' % (k, f()))
    body.append('<p class="n">%s</p>' % PALETTE)
    mounts = []
    i = 0
    for tid, files, cases in TOOLS:
        for _ in cases:
            mounts.append('(function(){var h=document.getElementById("h%d");var s=SP["%s"];if(s.custom)s.custom(h,D);else NadLanInstruments.mount(h,s,D);})();' % (i, tid)); i += 1
    tools_js = "".join("<script>" + rd(I, "tools", f + ".js") + "</script>" for f in ("bedek", "shamai", "orechdin"))
    html = ('<!-- @dsCard group="Tools" height=3200 subtitle="אנשי המקצוע: בדק בית, שמאי מקרקעין ועורך דין מקרקעין. שלושה כלים, החיפוש בפנקס השמאים, ראשי העמודים ותשעה איורים" -->\n'
            + '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ProsCluster</title><link rel="icon" href="data:,">'
            + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=Heebo:wght@700;800&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
            + '<style>' + css + '\nbody{margin:0;background:#F4F6FA;color:#12202A;font:400 16px/1.7 "IBM Plex Sans Hebrew",system-ui,sans-serif}.w{max-width:820px;margin:0 auto;padding:20px 16px}'
            + '.n{font:500 12px/16px "IBM Plex Mono",monospace;color:#5E6A75;margin:26px 0 8px;border-top:1px solid #D3DCE2;padding-top:8px}.page{background:#fff;border:1px solid #D3DCE2;padding:12px 16px}'
            + '.page h1{font:800 28px/1.3 Heebo,sans-serif;margin:6px 0}.fig{margin:0}.fig svg{max-width:640px}</style></head><body><div class="w">'
            + "".join(body) + '</div><script>' + core + '</script><script>var D=' + json.dumps(dd, ensure_ascii=False, separators=(",", ":")) + ';var SP={};NadLanInstruments.register=function(id,s){SP[id]=s};</script>'
            + tools_js + '<script>' + "".join(mounts) + '</script></body></html>')
    io.open(os.path.join(D, "preview.html"), "w", encoding="utf-8").write(html)
    io.open(os.path.join(D, "README.md"), "w", encoding="utf-8").write(README)
    io.open(os.path.join(H, "preview", "ds-ProsCluster.html"), "w", encoding="utf-8").write(html)
    print("ProsCluster", len(html.encode()), "bytes ->", D)


if __name__ == "__main__":
    build()
