# -*- coding: utf-8 -*-
"""HAD-670 R13g: builds docs/tools/hazards/page-en.html for /en/environmental-hazards/ from the English ChatGPT Pro article
(docs/research/2026-11-03-hazards/hazards.en.article.html), in the same order as the Hebrew page (build_page.py): the answer paragraph,
three buttons, the aerial figure, the numbers, the five tools (English on an /en/ page, release 1.72.579), the professionals with the
sponsor slot, the honesty statement, then the rest of the article with the two pictures after their headings."""
import io
import os
import re

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
U = "https://nad-lan.co.il/wp-content/uploads/2026/11/"
art = io.open(os.path.join(REPO, "docs", "research", "2026-11-03-hazards", "hazards.en.article.html"), encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"<p>.*?</p>", art, re.S)
first, rest = m.group(0), art[m.end():].strip()


def sc(i):
    return '<!-- wp:shortcode -->\n[nadlan_tool id="%s"]\n<!-- /wp:shortcode -->' % i


def after_h2(html, word, block):
    mm = re.search(r"<h2[^>]*>[^<]*" + word + r"[^<]*</h2>", html, re.I)
    return html[:mm.end()] + "\n" + block + "\n" + html[mm.end():] if mm else html


LAB = [("High-voltage line", "Power line", 10.5, 29.0, "#0b8fb3"), ("Substation", "Substation", 21.0, 66.0, "#0a5f78"),
       ("Fuel station", "Fuel", 87.0, 56.0, "#e0701b"), ("Industrial zone", "Industry", 80.0, 15.0, "#c0392b")]
lab = "".join('<span class="hzf-l" style="--x:%s%%;--y:%s%%;--c:%s"><b class="l">%s</b><b class="s">%s</b></span>' % (x, y, c, t, s) for t, s, x, y, c in LAB)
fig = ('<figure class="hzf"><img src="%senvironmental-hazards-neighbourhood-aerial.webp" alt="An aerial view of an Israeli residential neighbourhood: a high-voltage line on pylons, '
       'a fenced substation, a fuel station on a street corner and an industrial zone behind" width="1376" height="768" fetchpriority="high">%s<figcaption>What environmental hazards look like next to a '
       'residential neighbourhood: a power line, a substation, a fuel station and an industrial zone. Illustration.</figcaption></figure>') % (U, lab)
cta = ('<div class="hzp-cta"><a class="is-main" href="#hz-map">Check what is near an address</a><a href="#hz-compare">Compare two addresses</a>'
       '<a href="#hz-plan">A radiation test: who measures and what it costs</a></div>')
nums = ('<div class="hzn"><div><strong>8,531</strong><span>active cellular antenna sites in the register</span><small>Ministry of Environmental Protection, 3.11.2026</small></div>'
        '<div><strong>2.95%</strong><span>median measured radiation, of the health threshold</span><small>the highest: 29.96%</small></div>'
        '<div><strong>801</strong><span>plants that report emissions</span><small>Israeli PRTR, since 2012</small></div>'
        '<div><strong>1,255</strong><span>fuel stations</span><small>Ministry of Energy</small></div></div>')
PROS = [("A licensed radiation surveyor", "Measures radio-frequency radiation from antennas and the magnetic field from power lines, a substation or a transformer room inside the home, and gives a report. Check that the surveyor holds a valid licence from the Ministry of Environmental Protection.", "About NIS 500 to 650 per flat, from a published commercial price list"),
        ("An acoustic consultant", "Measures noise from a road, a railway or aircraft, by day and by night, and suggests fixes: windows, sealing and insulation.", "Price not published"),
        ("An environmental consultant", "Reads emission reports, monitoring-station data, the soil database and the plans for the area, and explains what they mean for living there.", "Price not published"),
        ("A home inspector", "Checks the flat itself: damp, electrics, plumbing and building defects.", "About NIS 1,700 to 1,800 on average, from a published commercial price list"),
        ("A planning and building lawyer", "Checks permit requests and plans at the local planning committee and files an objection in time, for example to an antenna about to be built.", "Price not published")]
pros = ('<h2 id="hz-pros">Professionals who help you check the surroundings</h2><div class="hzpros">'
        + "".join('<div class="hzpro"><p class="t">%s</p><p>%s</p><p class="m">%s</p></div>' % p for p in PROS)
        + '<div class="hzpro hzslot"><p class="t">A place for a licensed professional</p><p>Radiation surveyors, acoustic and environmental consultants and home inspectors: one card by the tools, marked "Ad", for a year.</p>'
        '<p><a href="/advertise/">Advertise on this page</a></p></div></div>')
honest = ('<div class="hzhonest" id="hz-honest"><h2>Our honesty statement: what this page shows and what it does not</h2><ul>'
          '<li><strong>Every figure is published.</strong> Every map layer comes from an open government register (the Ministry of Environmental Protection, the Ministry of Energy) or from OpenStreetMap, with its source and the date we read it.</li>'
          '<li><strong>Distance, not exposure.</strong> The map measures distance. It does not calculate radiation, magnetic fields, noise or pollution inside a flat. Only a licensed surveyor measures that.</li>'
          '<li><strong>There is no official "safe distance".</strong> No official source we found sets a safe distance from a cellular antenna or a power line. If someone quotes such a number, ask where it comes from.</li>'
          '<li><strong>No mark does not mean no hazard.</strong> Transformer rooms, fuel and gas pipelines, airport noise contours and live air-pollution values are not published as open data, so they are not on the map.</li>'
          '<li><strong>No names.</strong> We do not show the names of mobile operators, plants or site owners next to a hazard.</li>'
          '<li><strong>"Suspected" stays suspected.</strong> Most sites in the national soil database are marked as suspected contamination that was not confirmed, and they are marked that way here.</li></ul></div>')
img_ant = ('<figure class="hzf"><img src="%scellular-antenna-rooftop-israel.webp" alt="A cellular antenna with three panels on the roof of an Israeli apartment building, beside solar water heaters" width="1376" height="768" loading="lazy">'
           '<figcaption>A cellular antenna on a residential roof. Illustration.</figcaption></figure>') % U
img_sv = ('<figure class="hzf"><img src="%sradiation-survey-apartment.webp" alt="A radiation surveyor measuring in a flat with a meter by the window and a probe on a tripod in the living room" width="1376" height="768" loading="lazy">'
          '<figcaption>A radiation survey in a flat: the surveyor measures by windows and balconies and in the rooms where people spend time. Illustration.</figcaption></figure>') % U
rest = after_h2(rest, "Cellular antennas", img_ant)
rest = after_h2(rest, "Who can help", img_sv)
out = [first, cta, fig, nums,
       '<div id="hz-map">\n' + sc("hzmap") + "\n</div>", '<div id="hz-ant">\n' + sc("hzant") + "\n</div>",
       '<div id="hz-compare">\n' + sc("hzcompare") + "\n</div>", '<div id="hz-city">\n' + sc("hzcity") + "\n</div>",
       '<div id="hz-plan">\n' + sc("hzplan") + "\n</div>", pros, honest, rest]
io.open(os.path.join(H, "page-en.html"), "w", encoding="utf-8", newline="\n").write("\n\n".join(out) + "\n")
print("page-en.html", sum(len(x) for x in out), "chars")
