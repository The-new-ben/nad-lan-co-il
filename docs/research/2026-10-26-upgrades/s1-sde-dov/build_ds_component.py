# -*- coding: utf-8 -*-
"""S1: the Claude Design component "SdeDovHub" (not published here; the coordinator publishes the design system):
<scratchpad>/ds/project/components/SdeDovHub/preview.html, one self-contained file (core.css, core.js, tool/sdplan.js and
data/sdplan.json inlined, the data as a data: URL), showing the new hub copy in its page order with the live tool.
  python docs/research/2026-10-26-upgrades/s1-sde-dov/build_ds_component.py"""
import base64, io, json, os, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
DS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components\SdeDovHub"
os.makedirs(DS, exist_ok=True)
A = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
css = io.open(os.path.join(A, "core.css"), encoding="utf-8").read()
core = io.open(os.path.join(A, "core.js"), encoding="utf-8").read()
tool = io.open(os.path.join(H, "tool", "sdplan.js"), encoding="utf-8").read()
data = io.open(os.path.join(H, "data", "sdplan.json"), "rb").read()
S = json.load(io.open(os.path.join(H, "data", "s1-sections.json"), encoding="utf-8"))
durl = "about:blank"  # replaced at load time by a blob: URL of the inlined data (the engine splits data-nli-data on commas, so no data: URL)
TOOLHTML = ('<section class="nli" dir="rtl" lang="he" aria-label="כל מגרש ברובע שדה דב"><div class="nli-host" data-nli="sdplan" data-nli-data="%s"><div class="nli__panel"><p class="nli__kicker">מגרש אחר מגרש · רובע שדה דב</p>'
            '<h2 class="nli__title">כל מגרש ברובע שדה דב: מי זכה בו, בכמה, ובאיזה שלב הוא היום</h2></div></div></section>' % durl)
order = ["after_h1", "before_history", "before_projects", "before_transport", "before_affordable", "before_legal", "before_summary"]
NOTE = {"after_h1": "מתחת ל־H1: פסקת התשובה ושורת הפעולות (לפני תמונת הרובע)", "before_history": "אחרי מפת האזור (nlam), לפני ההיסטוריה: הכלי, I1, T8, T1, T2, I2, T3, I3",
        "before_projects": "אחרי שלושת המתחמים: I4 (מפת המגרשים הסטטית) ותכנית 3700 (T6)", "before_transport": "אחרי המחירים: החציונים שסביב הרובע (T5)",
        "before_affordable": "בפרק התחבורה: הקו הירוק (T4)", "before_legal": "לפני הבדיקות המשפטיות: מה לבדוק לפי השלב (T7)", "before_summary": "סוף השאלות הנפוצות: 16 שאלות חדשות"}
body = '<h1 style="font:800 30px/1.25 Heebo,sans-serif;margin:24px 0 8px">רובע שדה דב: פרויקטים ודירות למכירה</h1>'
for k in order:
    body += '<p class="dsnote">◂ %s</p>' % NOTE[k] + S[k].replace('[nadlan_tool id="sdplan"]', TOOLHTML)
html = ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>SdeDovHub</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;800&family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
        '<style>' + css + '</style><style>html,body{margin:0;background:#fff;color:#12202A;font:16px/1.7 Heebo,Arial,sans-serif}main{padding:0 16px 40px}main>*{max-width:760px;margin-left:auto;margin-right:auto}'
        'h2{font:700 24px/1.3 Heebo,sans-serif;margin:30px auto 10px}h3{font:700 19px/1.35 Heebo,sans-serif;margin:22px auto 8px}.dsnote{font:500 13px/1.5 "IBM Plex Mono",monospace;color:#C42550;border-top:1px dashed #D3DCE2;padding-top:10px;margin-top:28px}</style>'
        '</head><body><main>' + body + '</main><script>window.__SDP=' + data.decode('utf-8') + ';(function(){var u=URL.createObjectURL(new Blob([JSON.stringify(window.__SDP)],{type:"application/json"}));[].forEach.call(document.querySelectorAll("[data-nli=sdplan]"),function(h){h.setAttribute("data-nli-data",u);});})();</script><script>' + core + '</script><script>' + tool + '</script></body></html>')
io.open(os.path.join(DS, "preview.html"), "w", encoding="utf-8", newline="").write(html)
print("preview.html", len(html), "bytes ->", DS)
