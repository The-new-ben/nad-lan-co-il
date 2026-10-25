# -*- coding: utf-8 -*-
"""The design-system component GypsumWall (DS artifact L9Nqz7Viv7K3MYeZrBc9s8): a live preview that runs the real engine
(assets/instruments/core.css + core.js) and the real tool (tools/gwall.js) on the real data (gwall.json), three cases, plus the two
page infographics from infographics.py.   python docs/research/2026-10-26-upgrades/q6-red-gypsum/ds_component.py"""
import io, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
import infographics as ig
D = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components\GypsumWall"
os.makedirs(D, exist_ok=True)
I = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
rd = lambda *p: io.open(os.path.join(I, *p), encoding="utf-8").read()
css, core, js, data = rd("core.css"), rd("core.js"), rd("tools", "gwall.js"), rd("data", "gwall.json")
html = ('<!-- @dsCard group="Tools" height=2600 subtitle="מחשבון קיר גבס ורוד: סוג הלוח, כמה להזמין, משקל, עלות אצל ספקים, המחיצה שנבדקה, ושני איורי עמוד (חתך מחיצת אש ומפת צבעים)" -->\n'
        '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>GypsumWall</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
        '<style>' + css + '\nbody{margin:0;background:#F4F6FA;color:#12202A;font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif}.w{max-width:1040px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-left,0px))}'
        '.n{font:500 12px/16px "IBM Plex Mono",monospace;color:#5E6A75;margin:26px 0 8px;border-top:1px solid #D3DCE2;padding-top:8px}.fig{background:#fff;border:1px solid #D3DCE2;padding:12px;max-width:664px}</style></head><body><div class="w">'
        '<p class="n">1 · ברירת המחדל: חדר מדרגות, 120 דקות. הלוח, כמה להזמין (הגדול מבין שטח ופחת לבין תוכנית חיתוך), משקל לפי טבלת הספק, עלות, שרטוט החזית והחתך, והמחיצה שנבדקה</p>'
        '<section class="nli" dir="rtl" lang="he"><div class="nli-host" id="g1"></div></section>'
        '<p class="n">2 · קיר של 100 מטר: השרטוט מציג קטע של 4.80 מ\' ומסמן זאת; אין מחיר בדוק ללוח 3.00, ולכן אין שורת עלות</p>'
        '<section class="nli" dir="rtl" lang="he"><div class="nli-host" id="g2" data-nli-set=\'{"preset":"long"}\'></div></section>'
        '<p class="n">3 · חדר רטוב עם דרישת אש: הלוח המשולב, בלי משקל ומחיר שלא בדקנו, ובלי מחיצה שנבדקה בהרכב הזה</p>'
        '<section class="nli" dir="rtl" lang="he"><div class="nli-host" id="g3" data-nli-set=\'{"preset":"wet60"}\'></div></section>'
        '<p class="n">4 · איור עמוד: חתך המחיצה שנבדקה (120 דקות, נתוני ספק). גיליון תוכנית בטיחות אש: נייר לבן, קו שחור, לוח אש בקווקוו אדום, צמר בגל אפור</p>'
        '<div class="fig">' + ig.partition_svg() + '</div>'
        '<p class="n">5 · איור עמוד: מפת הצבעים, 3 על 3, ומה מהם לוח אש</p>'
        '<div class="fig">' + ig.colours_svg() + '</div>'
        '<p class="n">פלטה: לבן, דיו #12202A, אדום הבטיחות #C42550 רק ללוח אש ולדרישה, אפור #8A97A2 לצמר. IBM Plex Sans Hebrew למילים, IBM Plex Mono למספרים ולתקנים. לא שמנת, לא זהב, לא כרטיסים רכים.</p>'
        '</div><script>' + core + '</script><script>var DATA=' + data + ';var SP={};NadLanInstruments.register=function(id,s){SP[id]=s};</script><script>' + js + '</script>'
        '<script>["g1","g2","g3"].forEach(function(id){NadLanInstruments.mount(document.getElementById(id),SP.gwall,{gwall:DATA})});</script></body></html>')
io.open(os.path.join(D, "preview.html"), "w", encoding="utf-8").write(html)
readme = """# GypsumWall

The wall calculator of the red (pink) gypsum board term, /glossary/לוח-גבס-אדום/ (HAD-601, Q6 stage 2, release 1.72.521).

**Job.** A buyer, a renovator or a site manager asks three things at once: which board, how many, how much. Nobody in the Israeli
results answers them together, and nobody says the one thing that matters for fire: the minutes belong to the tested wall, never to
the board. The tool answers all of it from a wall: place, the consultant's fire requirement, length, height, sides, layers, board size,
thickness, waste, price per board.

**Output.** The board for the place (white, green, pink FR, combined FM, special fire board, or "not outside"); boards to order = the
larger of area with the reader's waste and a cut plan (columns of 1.20 m, top pieces, the narrow last column and its corner cut from
whole boards); the weight from the supplier table (27 kg per 2.60 board of 12.5 mm); the cost and the four supplier prices of
25.10.2026 side by side; the tested partition when a supplier published one for that build (2 + 2 pink boards on 70 mm studs with
5 cm wool: 120 minutes, Rotenberg 11.5.2025), or a plain "no tested partition found for this build"; the documents to ask for
(931 test report of the whole partition, 755 classification, 1490 part 1 mark, the tested build detail).

**Drawing.** The face of the wall with every board, joint and cut piece (staggered joints when the wall is taller than the board, a
4.80 m segment for a long wall), and the cut through the layers. A fire-safety plan sheet: white paper, black line work, red hatch
only for fire-rated board, the grey wave for wool, the requirement in a red box. Plex Sans Hebrew for words, Plex Mono for numbers.
Engine hook added for it: `r.figure` (a tool's own drawing, built from escaped parts), one line in core.js.

**Honesty rules.** No minutes for a board. No weight or price that was not read on a manufacturer or supplier site that day; a
missing one is left out, never estimated as a fact. VAT is stated only where the supplier states it.

**Page infographics** (same sheet language): the tested partition cut with the three standards, and the nine-colour board map that
marks which boards are fire boards (orange, yellow and blue are not).
"""
io.open(os.path.join(D, "README.md"), "w", encoding="utf-8").write(readme)
print("preview", len(html.encode()), "bytes")
