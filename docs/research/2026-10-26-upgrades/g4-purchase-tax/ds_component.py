# -*- coding: utf-8 -*-
"""G4: the Claude Design component PurchaseTax2 (not published): one self-contained preview.html with the real engine, ptax v3 and
its data inline (data: URL), three states of the tool (the example, two buyers, an oleh with an aliyah date), the CTA row and the
three page infographics taken from preview/g4-page-content.html (run write_g4_page.py --local first), plus README.md.
  python docs/research/2026-10-26-upgrades/g4-purchase-tax/ds_component.py"""
import io, json, os, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
A = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
OUT = os.path.join(os.environ.get("G4_DS", r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components"), "PurchaseTax2")
os.makedirs(OUT, exist_ok=True)
rd = lambda p: io.open(p, encoding="utf-8").read()
core_css, core_js, tool = rd(os.path.join(A, "core.css")), rd(os.path.join(A, "core.js")), rd(os.path.join(A, "tools", "ptax.js"))
data = "ptax.json"  # the engine splits data-nli-data on commas, so the data rides in a fetch shim below, not in a data: URL
SHIM = ("<script>(function(){var J=" + json.dumps(json.load(io.open(os.path.join(A, "data", "ptax.json"), encoding="utf-8")), ensure_ascii=False)
        + ",f=window.fetch;window.fetch=function(u,o){return /ptax\.json$/.test(String(u))?Promise.resolve(new Response(JSON.stringify(J),{headers:{'Content-Type':'application/json'}})):f.apply(this,arguments)};})();</script>")
content = rd(os.path.join(H, "preview", "g4-page-content.html"))
nlag_css = re.search(r'<style id="nlag-css">.*?</style>', content, re.S).group(0)
g4_css = re.search(r'<style id="nlg4-css">.*?</style>', content, re.S).group(0)
cta = re.search(r'<p class="nlg4-cta">.*?</p>', content, re.S).group(0).replace('href="#', 'href="#h0" data-x="')
figs = re.findall(r'<figure class="nlag-chart nlg4-fig".*?</figure>', content, re.S)
assert len(figs) == 3


def tool_div(i, cfg=None):
    return '<section class="nli" dir="rtl" lang="he"><div class="nli-host" data-nli="ptax" id="h%d" data-nli-data="%s"%s></div></section>' % (
        i, data, (" data-nli-set='%s'" % cfg) if cfg else "")


N = lambda s: '<p class="n">%s</p>' % s
html = ('<!-- @dsCard group="Tools" height=2600 subtitle="מחשבון מס רכישה v3: כל המסלולים, מתי מדווחים ומשלמים, מה עולה כל שבוע איחור, שני קונים, חלון העולה ותקנה 12 מול 12א, וקישור שפותח את אותם מספרים" -->\n'
        '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>PurchaseTax2</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
        '<style>' + core_css + '</style>' + nlag_css + g4_css +
        '<style>body{margin:0;background:#F6F8F9;color:#12202A;font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif;overflow-x:hidden}.w{max-width:1040px;margin:0 auto;padding:20px 16px}'
        '.n{font:500 12px/16px "IBM Plex Mono",monospace;color:#5E6A75;margin:26px 0 8px;border-top:1px solid #D3DCE2;padding-top:8px}</style></head><body><div class="w">'
        + N("1 · שורת הפעולות מתחת לפסקת התשובה, ואז הכלי: דירה יחידה ב־3,000,000 ₪, ציר הזמנים של העסקה, הקנס לשבוע איחור, המרחק למדרגה הבאה") + cta + tool_div(0)
        + N("2 · שני קונים שאינם תא משפחתי אחד: חצי דירה יחידה, חצי דירה נוספת") + tool_div(1, '{"preset":"partners"}')
        + N("3 · עולה שעלה ב־1.5.2023: החלון של 8 שנים, ותקנה 12 מול 12א זו לצד זו; תשלום באיחור של 6 שבועות") + tool_div(2, '{"preset":"oleh","aliyah":"2023-05-01","late":6}')
        + N("4 · שלושת האיורים של העמוד (SVG, רוחב טלפון קודם, עד 640 פיקסלים)") + '<div class="nlag">' + "".join(figs) + '</div>'
        + N("פלטה: מכשירי NadLan. דיו #12202A, ים #2F6F86, עמוק #1F4B5C, קו #D3DCE2, אדום מדידה #C42550 רק לאיחור ולשיעור של דירה נוספת. Karantina לכותרת הכלי, IBM Plex Sans Hebrew לטקסט, IBM Plex Mono לכל מספר. בלי שמנת, זהב או גרדיאנט; הצהוב והסגול של המנוע לא בשימוש כאן.")
        + '</div>' + SHIM + '<script>' + core_js + '</script><script>' + tool + '</script></body></html>')
io.open(os.path.join(OUT, "preview.html"), "w", encoding="utf-8", newline="").write(html)
README = """# PurchaseTax2

ptax v3 for /purchase-tax-calculator/ (G4 of the upgrade loop, 26.10.2026: win "מס רכישה" 6,600 a month, no impressions today, and
"מחשבון מס רכישה" 4,400, position 55). Standard engine (tools/ptax.js on core.js), every v2 answer unchanged on 2,961 cases
(test/test_ptax_v3.js in docs/research/2026-10-26-upgrades/g4-purchase-tax/). New: the deal date for every track and the timeline it
starts (declaration in 30 days, payment in 60 days or later under s.51, sell-by for upgraders, resident-by for a foreign buyer) with
a countdown; 0.2% of the tax per week of late payment and a what-if for weeks late; two buyers who are not one family, each by his
own status; the oleh window (a year before aliyah to 7 years after) and regulation 12 against 12A side by side; the distance to the
next bracket and the tax on another 100,000 shekels; a link that reopens the same numbers (#ptax=...). Sources: the Tax Authority's
2026 buyer guide pp. 11, 51, 58-59, instructions 1/2026 and 2/2026, the notice of 12.10.2026.

Plus the page parts: the CTA row under the answer (sea primary, outline secondary, 44 px), and three phone-first SVG figures:
I1 the rate on each shekel for three tracks (a staircase), I2 one apartment of 3,000,000 shekels and ten buyers (bars, red for
8% from the first shekel), I3 from signing to the Land Registry (a vertical rule with every deadline).

Design: NadLan Instruments. Ink #12202A, sea #2F6F86, deep #1F4B5C, line #D3DCE2, survey red #C42550 only for late payment and the
additional-home rate. Karantina for the tool title, IBM Plex Sans Hebrew for text, IBM Plex Mono for every figure. The cost bar uses
sea and red (v2 used the engine's yellow). Why it is not the default AI look: no cream, gold, brass or purple, no soft-shadow card on
every block; the look of a tax assessment form and a survey sheet, thin rules, tabular numbers, one red for money that is due.
The old guide's cream and gold notes on the same page are restyled to the palette by scoped CSS in the page writer.

Not published; nothing on the live site changed.
"""
io.open(os.path.join(OUT, "README.md"), "w", encoding="utf-8", newline="\n").write(README)
print("wrote", OUT, "| preview", len(html) // 1024, "KB")
