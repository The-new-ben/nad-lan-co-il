# -*- coding: utf-8 -*-
"""Claude Design components for G2 + G3 (design system artifact, NOT published here): PinuiBinuiPage and UrbanRenewalHub.
Each preview.html is self-contained: the real engine (core.css + core.js), the real tool file, the real data files, a few cases,
then the page's top block (H1, answer, CTAs, the numbers table) and the page infographics, exactly as the writers emit them.
  python ds_g2g3.py      writes <scratchpad>/ds/project/components/{PinuiBinuiPage,UrbanRenewalHub}/{preview.html,README.md}
                         and a copy of each preview in ./preview/ds-*.html"""
import html as H_, io, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
I = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
DS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components"
rd = lambda *p: io.open(os.path.join(*p), encoding="utf-8").read()
import infographics as ig  # noqa: E402

PALETTE = ("פלטה: גיליון תכנון של הוועדה. דיו #12202A, ים #2F6F86 למה שבתהליך, ים עמוק #1F4B5C למה שאושר או מתקיים, קו #D3DCE2 לרשת, אדום מדידה #C42550 רק למה שחסר "
           "(חתימה, תנאי). IBM Plex Sans Hebrew לטקסט ו-IBM Plex Mono למספרים. למה זה לא המראה של AI: אין שמנת, אין זהב או טרקוטה, אין גרדיאנט ואין כרטיס כהה עם צבע חומצי; "
           "הצבעים והצורות לקוחים מתשריט ומטבלת זכויות, וכל צבע אומר מצב.")
COMP = {
    "PinuiBinuiPage": {
        "tool": "pinui", "data": ["pinui.json", "renewal-track.json"], "content": "g2-page-content.html",
        "subtitle": "פינוי בינוי: הרוב לפי החוק בניין אחר בניין, תקרת הפטור ממס לדירה שלכם, השעון של סעיף 1ד, והעמוד שסביב המחשבון",
        "cases": [(None, "1 · ברירת המחדל: שלושה בניינים, 48 דירות. שני שלישים במקבץ, וחסרה חתימה בבניין השני (הקו האדום)"),
                  ("ok", "2 · אותם בניינים, הרוב מתקיים בכל בניין"),
                  ("mine", "3 · מה מגיע לי: דירה של 68 מ\"ר, בעלת דירה בת 76. התקרה לפטור ממס וחלופות מגיל 75"),
                  ("clock", "4 · השעון של החוק: העסקה הראשונה ב-6.2024, המועד הבא ומה עבר"),
                  ("approved", "5 · מתחם אמיתי מתכנית מאושרת: השנים מאז האישור מול הממוצע של הרשות, כממוצע ולא כתחזית")],
        "figs": [("איור עמוד I1", ig.g2_majority), ("איור עמוד I2", ig.g2_clock), ("איור עמוד I3", ig.g2_permit_years), ("איור עמוד I4", ig.g2_plans)],
        "readme": """# PinuiBinuiPage

G2 of the upgrade loop (Ben 26.10.2026): /urban-renewal/pinui-binui/, the owner page of "פינוי בינוי" (12,100 searches a month) and
"חוק פינוי בינוי" (880). Local build, nothing deployed. Research and spec: docs/research/2026-10-26-upgrades/g2g3-urban-renewal/dna.md.

**The tool (pinui, tools/pinui.js).** Three views on one set of answers: the special majority of section 1 of the Pinui Binui law,
building by building (two thirds of the cluster, three fifths of every building, 3 in a building of 4 or 5), what is missing, the
more-than-two-fifths line for the authority's free appraiser and the 40% line of section 1ג; what I get (the tax-free ceiling of the
new apartment for my own size, the multiplier of my complex or city, the options for 70+ and 75+); the clock of section 1ד from the
first signed deal, and the years since the plan was approved against the authority's 4.0-year average. Data: pinui.json (the law as
it reads to תשפ"ג, the 2025 report, gov.il) + renewal-track.json (the tracker).

**The page.** H1, the answer paragraph with the head term first, three CTAs, the tool, the numbers table, then the law sections (13
tables, 4 infographics), 29 FAQ and an English section. Honesty: no promised area, price or date; every computed number labelled.

**Look.** """ + "A planning sheet, not a card: ink, sea for what is in process, deep sea for what holds, survey red only for a gap. Plex Sans Hebrew and Plex Mono.\n",
    },
    "UrbanRenewalHub": {
        "tool": "urcity", "data": ["urcity.json", "renewal-track.json"], "content": "g3-page-content.html",
        "subtitle": "התחדשות עירונית: העיר שלכם אצל הרשות, המסלול לבניין שלכם, השוואת ערים, ושלושת המסלולים זה לצד זה",
        "cases": [(None, "1 · ברירת המחדל: ירושלים. 215 מתחמים לפי שלב, המסלולים, המכפיל, ומה הדוח אומר על תמ\"א 38 בעיר"),
                  ("pt", "2 · פתח תקוה: התכנית שמחליפה את תמ\"א 38 אושרה ב-2025"),
                  ("tlv", "3 · תל אביב יפו: בלי הארכה לתמ\"א 38"),
                  ("bld", "4 · המסלול לבניין שלי: 16 דירות משנות ה-70 ברמת גן, מה פתוח וכמה חתימות"),
                  ("rank", "5 · השוואת ערים: 15 הערים המובילות וכל הטבלה")],
        "figs": [("איור עמוד I1", ig.g3_tracks), ("איור עמוד I2", ig.g3_taxdecl), ("איור עמוד I3", ig.g3_permit_split)],
        "readme": """# UrbanRenewalHub

G3 of the upgrade loop (Ben 26.10.2026): /urban-renewal/, the owner page of "התחדשות עירונית" (8,100 searches a month), the umbrella
of the cluster. Local build, nothing deployed. Research and spec: docs/research/2026-10-26-upgrades/g2g3-urban-renewal/dna.md.

**The tool (urcity, tools/urcity.js).** The city: its complexes on the authority's map by stage and track, units today and after
building and the multiplier, what moved since the data.gov.il file, and what the 2025 report says about building renewal there
(the plan that replaces TAMA 38 and its status, the extension, years from request to permit, apartments sold, tax-track declarations).
The building: which of the three tracks stays open for its size, permit year and complex, and the majority each needs by law. The
ranking of every city. Data: urcity.json (the 2025 report, annex A, the laws) + renewal-track.json (the tracker).

**The page.** H1, answer, CTAs, the tool, the numbers table, the three tracks side by side, the tax and authorities tracks, TAMA 38
in every city, urban renewal by city, the authority; 9 tables, 3 new infographics, 25 FAQ, an English section. The old start band, link
lines and Tel Aviv box move from cream, brown and terracotta to the Instruments palette (style only, text kept).

**Look.** """ + "A planning sheet: ink, sea, deep sea, survey red only for a gap; Plex Sans Hebrew and Plex Mono.\n",
    },
}


def build(name):
    c = COMP[name]; D = os.path.join(DS, name); os.makedirs(D, exist_ok=True)
    css, core, tool = rd(I, "core.css"), rd(I, "core.js"), rd(I, "tools", c["tool"] + ".js")
    dd = {}
    for i, f in enumerate(c["data"]):
        x = json.loads(rd(I, "data", f)); dd[x.get("key") or ("d%d" % i)] = x
    content = rd(H, "preview", c["content"])
    top = content[:content.index('<div id="%s-tool"' % ("pinui" if c["tool"] == "pinui" else "urcity"))]
    tbl = re.search(r'<p class="nl[a-z0-9]+-cap"[^>]*>.*?</div>\n', content[len(top):], flags=re.S).group(0)
    body = ['<p class="n">0 · ראש העמוד כפי שהכותב מדפיס אותו: H1, פסקת התשובה, שלושה כפתורים</p><div class="page">' + top + '</div>']
    for i, (preset, note) in enumerate(c["cases"]):
        st = ' data-nli-set="%s"' % H_.escape(json.dumps({"preset": preset}, ensure_ascii=False), quote=True) if preset else ""
        body.append('<p class="n">%s</p><section class="nli" dir="rtl" lang="he"><div class="nli-host" data-nli="%s" id="h%d"%s></div></section>' % (note, c["tool"], i, st))
    body.append('<p class="n">טבלת המספרים שמתחת למחשבון</p><div class="page">' + tbl + '</div>')
    for lab, f in c["figs"]:
        body.append('<p class="n">%s</p><div class="page"><figure class="fig">%s</figure></div>' % (lab, f()))
    body.append('<p class="n">%s</p>' % PALETTE)
    html = ('<!-- @dsCard group="Tools" height=2600 subtitle="%s" -->\n' % c["subtitle"]
            + '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title><link rel="icon" href="data:,">' % name
            + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=Heebo:wght@700;800&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
            + '<style>' + css + '\nbody{margin:0;background:#F4F6FA;color:#12202A;font:400 16px/1.7 "IBM Plex Sans Hebrew",system-ui,sans-serif}.w{max-width:820px;margin:0 auto;padding:20px 16px}'
            + '.n{font:500 12px/16px "IBM Plex Mono",monospace;color:#5E6A75;margin:26px 0 8px;border-top:1px solid #D3DCE2;padding-top:8px}.page{background:#fff;border:1px solid #D3DCE2;padding:12px 16px}'
            + '.page h1{font:800 28px/1.3 Heebo,sans-serif;margin:6px 0}.fig{margin:0}.fig svg{max-width:640px}</style></head><body><div class="w">'
            + "".join(body) + '</div><script>' + core + '</script><script>var D=' + json.dumps(dd, ensure_ascii=False, separators=(",", ":")) + ';var SP={};NadLanInstruments.register=function(id,s){SP[id]=s};</script><script>' + tool + '</script>'
            + '<script>' + "".join('(function(){var h=document.getElementById("h%d");var s=h.getAttribute("data-nli-set");NadLanInstruments.mount(h,SP["%s"],D);})();' % (i, c["tool"]) for i in range(len(c["cases"]))) + '</script></body></html>')
    io.open(os.path.join(D, "preview.html"), "w", encoding="utf-8").write(html)
    io.open(os.path.join(D, "README.md"), "w", encoding="utf-8").write(c["readme"])
    io.open(os.path.join(H, "preview", "ds-%s.html" % name), "w", encoding="utf-8").write(html)
    print(name, len(html.encode()), "bytes ->", D)


if __name__ == "__main__":
    for n in COMP: build(n)
