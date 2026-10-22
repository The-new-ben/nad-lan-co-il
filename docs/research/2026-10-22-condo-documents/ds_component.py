# -*- coding: utf-8 -*-
"""The design-system component CondoDocFinder (DS artifact L9Nqz7Viv7K3MYeZrBc9s8): a live preview that runs the real tool code
(assets/instruments/tools/condo.js) on the real data (condo.json) with a small stand-in for the instruments engine.
  python docs/research/2026-10-22-condo-documents/ds_component.py"""
import io, json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components\CondoDocFinder"
os.makedirs(D, exist_ok=True)
I = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
js = io.open(os.path.join(I, "tools", "condo.js"), encoding="utf-8").read()
data = io.open(os.path.join(I, "data", "condo.json"), encoding="utf-8").read()
STUB = ("window.NadLanInstruments={fmt:{num:function(x,d){return Number(x).toLocaleString('en-US',{maximumFractionDigits:d||0,minimumFractionDigits:d||0})}},"
        "esc:function(s){return String(s).replace(/[&<>\"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]})},"
        "register:function(id,spec){var r=document.querySelector('[data-nli=\"'+id+'\"]');if(r)spec.custom(r,{condo:DATA});}};")
html = ('<!-- @dsCard group="Tools" height=1500 subtitle="איזה מסמך עונה על השאלה: לחיצה על שאלה מדליקה את החלק בתשריט לדוגמה ופותחת כרטיס, ומחשבון רוב בבית משותף" -->\n'
        '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>CondoDocFinder</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
        '<style>body{margin:0;background:#F4F6FA;color:#12202A}.w{max-width:960px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-left,0px))}'
        '.nli{--nli-sans:"IBM Plex Sans Hebrew",system-ui,sans-serif;--nli-mono:"IBM Plex Mono",monospace;font-family:var(--nli-sans);margin:0 0 24px}'
        '.nli__panel{background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:20px}.nli__kicker{font:500 12px "IBM Plex Mono";color:#5E6A75;margin:0}'
        '.nli__title{font:700 26px/32px "IBM Plex Sans Hebrew";color:#14213D;margin:4px 0 6px}.nli__lede{font:400 15px/23px "IBM Plex Sans Hebrew";color:#3E4C58;margin:0}'
        '.n{font:500 12px/16px "IBM Plex Mono",monospace;color:#5E6A75;margin:22px 0 8px;border-top:1px solid #D3DCE2;padding-top:8px}</style></head><body><div class="w">'
        '<p class="n">1 · שאלה אחת, לחיצה אחת: החלק בתשריט נדלק, והכרטיס אומר באיזה מסמך, מה מחפשים, והדגל האדום בקו מקווקו כמו בתשריט עצמו</p>'
        '<div class="nli-host" data-nli="condo"></div>'
        '<p class="n">2 · מחשבון רוב: פעולה ומספר דירות, ושורת דירות שמראה כמה צריכות להסכים</p>'
        '<div class="nli-host" data-nli="condomaj"></div>'
        '<p class="n">פלטה: נייר שרטוט לבן עם רשת 1:100, דיו כחול כהה של הרשם, צבע לכל דירה כמו בתשריט הרשמי (אף פעם לא שחור), אדום מקווקו רק לחריגה. בלי שמנת, זהב או גרדיאנט.</p>'
        '</div><script>var DATA=' + data + ';' + STUB + '</script><script>' + js + '</script></body></html>')
io.open(os.path.join(D, "preview.html"), "w", encoding="utf-8").write(html)
print("preview", len(html.encode()), "bytes")
