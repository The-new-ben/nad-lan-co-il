# -*- coding: utf-8 -*-
"""The Somail tour, corrected (1.72.312, design system SomailTour v58).

Reads experience/somail/index.html (the byte-identical source of the live tour), fixes one fact and the promises, and
writes the result to experience/somail/index.html and to plugins/nadlan-config/assets/tours/somail-tour.html (served
first by inc/tour-routes.php since 1.72.311).

- DUO: "בבנייה מתקדמת · אכלוס צפוי 2026-2027" -> "בבנייה · השלמה מתוכננת 2027, לפי דוחות החברה", as DUO's page says
  (2 towers, 54 floors, 668 apartments already matched).
- The tour has no apartment picking, and DUO has none either (its page: no official typical floor plan): "לעמוד הפרויקט
  ולבחירת דירה", "בחרו דירה בבניין הזה", "בחרו דירה ב־DUO", "בניין, קומה, כיוון ונוף לבחירתכם", "לבחירת דירה" and the
  English twins say what is there: the project page.

    python scripts/tours/somail_tour_v2.py
"""
import io, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC = os.path.join(ROOT, "experience", "somail", "index.html")
OUT = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "tours", "somail-tour.html")
s = io.open(SRC, encoding="utf-8", newline="").read()
if "SOMAIL_FIX_312" in s:
    raise SystemExit("already corrected")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, n, a[:90])
    s = s.replace(a, b)
    print("ok x%d  %s" % (n, a[:70]))


# the markup
rep('aria-label="לפרק: סיום ובחירת דירה"', 'aria-label="לפרק: סיום והפרויקטים"')
rep('>לעמוד הפרויקט ולבחירת דירה ←</a>', '>לעמוד הפרויקט ←</a>', 2)
rep('<li>סטטוס: <b>בבנייה מתקדמת</b> · אכלוס צפוי 2026-2027</li>', '<li>סטטוס: <b>בבנייה</b> · השלמה מתוכננת 2027, לפי דוחות החברה</li>')
rep('<h2>בחרו דירה ב־DUO</h2>', '<h2>DUO תל אביב, בלב המתחם</h2>')
rep('<p>שני מגדלים תאומים על אבן גבירול — בניין, קומה, כיוון ונוף לבחירתכם.</p>', '<p>שני מגדלים תאומים על אבן גבירול. בעמוד הפרויקט: העובדות והמקורות.</p>')
rep('<em>לבחירת דירה ←</em>', '<em>לעמוד הפרויקט ←</em>')
rep('<button id="mmEnd">לבחירת דירה</button>', '<button id="mmEnd">לפרויקטים במתחם</button>')
rep('delivery est. 2026-2027', 'completion planned 2027 per the company (DUO page)')

# the strings, Hebrew
rep("btnProject: 'לעמוד הפרויקט ולבחירת דירה ←'", "btnProject: 'לעמוד הפרויקט ←'")
rep("pickHere: 'בחרו דירה בבניין הזה ←'", "pickHere: 'לעמוד הפרויקט ←'")
rep("liDuo4: 'סטטוס: <b>בבנייה מתקדמת</b> · אכלוס צפוי 2026-2027'", "liDuo4: 'סטטוס: <b>בבנייה</b> · השלמה מתוכננת 2027, לפי דוחות החברה'")
rep("finH2: 'בחרו דירה ב־DUO'", "finH2: 'DUO תל אביב, בלב המתחם'")
rep("finP: 'שני מגדלים תאומים על אבן גבירול — בניין, קומה, כיוון ונוף לבחירתכם.'", "finP: 'שני מגדלים תאומים על אבן גבירול. בעמוד הפרויקט: העובדות והמקורות.'")
rep("finEm1: 'לבחירת דירה ←'", "finEm1: 'לעמוד הפרויקט ←'")
rep("mmEnd: 'לבחירת דירה'", "mmEnd: 'לפרויקטים במתחם'")
# the strings, English
rep("btnProject: 'Project page & pick a home →'", "btnProject: 'To the project page →'")
rep("pickHere: 'Pick a home in this building →'", "pickHere: 'To the project page →'")
rep("liDuo4: 'Status: <b>advanced construction</b> · occupancy est. 2026-2027'", "liDuo4: 'Status: <b>under construction</b> · completion planned 2027, per the company'")
rep("finH2: 'Pick your home at DUO'", "finH2: 'DUO Tel Aviv, at the heart of the compound'")
rep("finP: 'Twin towers on Ibn Gvirol — building, floor, direction and view, your pick.'", "finP: 'Twin towers on Ibn Gvirol. On the project page: the facts and the sources.'")
rep("finEm1: 'Pick a home →'", "finEm1: 'Project page →'")
rep("mmEnd: 'Pick a home'", "mmEnd: 'The compound’s projects'")
s = s.replace("<script type=\"module\">", "<script type=\"module\">\n/* SOMAIL_FIX_312: facts and promises corrected by scripts/tours/somail_tour_v2.py */", 1)
left = [w for w in ("ולבחירת דירה", "בחרו דירה", "לבחירתכם", "לבחירת דירה", "2026-2027", "pick a home", "Pick a home", "your pick", "Pick your home") if w in s]
print("left:", left)
assert not left, left
io.open(SRC, "w", encoding="utf-8", newline="").write(s)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="").write(s)
print("written", len(s.encode("utf-8")))
