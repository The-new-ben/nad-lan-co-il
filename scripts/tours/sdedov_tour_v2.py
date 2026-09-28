# -*- coding: utf-8 -*-
"""The Sde Dov tour, corrected (1.72.311, design system SdeDovTour v57).

Reads experience/sde-dov/index.html (the byte-identical source of the live tour), fixes the facts and the promises, and
writes the result to experience/sde-dov/index.html and to plugins/nadlan-config/assets/tours/sde-dov-tour.html (the copy
inc/tour-routes.php now serves first, so the tour ships through the release runner like everything else).

- Rainbow: "כ־38 קומות · 480 דירות · בשיווק" -> 39 floors, 459 apartments (the developer's number; 480 was the 2023 design
  plan), under construction, as Rainbow's own page says. Dimri Yama (39 floors, 458) and Ashira (35/16/8/8, 406) already
  match their pages.
- The tour has no apartment picking: "לעמוד הפרויקט ולבחירת דירה", "בחרו דירה בבניין הזה", "בחרו דירה מתוך הבניין",
  "חופש בחירה מלא — בניין, קומה, כיוון ונוף", "לבחירת דירה", "מהדגלים אפשר להמשיך לבחירת דירה אמיתית" and the English
  twins say what is there: the project pages.
- Narration clips 3 and 5 (both languages) come from assets/tours/narr-sdedov-*-v2.mp3 (scripts/tours/narr_sdedov_v2.py);
  their captions say the same words.

    python scripts/tours/sdedov_tour_v2.py
"""
import io, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC = os.path.join(ROOT, "experience", "sde-dov", "index.html")
OUT = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "tours", "sde-dov-tour.html")
s = io.open(SRC, encoding="utf-8", newline="").read()
if "NARR_FIX" in s:
    raise SystemExit("already corrected")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, n, a[:90])
    s = s.replace(a, b)
    print("ok x%d  %s" % (n, a[:70]))


# the markup
rep('aria-label="לפרק: סיום ובחירת דירה"', 'aria-label="לפרק: סיום והפרויקטים"')
rep('>לעמוד הפרויקט ולבחירת דירה ←</a>', '>לעמוד הפרויקט ←</a>', 4)
rep('<li><b>כ־38</b> קומות</li>', '<li><b>39</b> קומות</li>')
rep('<li><b>480</b> דירות</li>', '<li><b>459</b> דירות</li>')
i = s.index('<div class="en">RAINBOW TEL AVIV</div>')
j = s.index('<li>סטטוס: <b>בשיווק</b></li>', i)
assert j - i < 400, j - i
s = s[:j] + '<li>סטטוס: <b>בבנייה</b></li>' + s[j + len('<li>סטטוס: <b>בשיווק</b></li>'):]
print("ok x1  the Rainbow card's status")
rep('<h2>בחרו דירה מתוך הבניין</h2>', '<h2>שלושה פרויקטים ברובע</h2>')
rep('<p>שלושה פרויקטים, חופש בחירה מלא — בניין, קומה, כיוון ונוף.</p>', '<p>לכל פרויקט עמוד משלו, עם העובדות והמקורות.</p>')
rep('<span>מגדל הדגל · כ־38 קומות · 480 דירות</span>', '<span>מגדל הדגל · 39 קומות · 459 דירות</span>')
rep('<em>לבחירת דירה ←</em>', '<em>לעמוד הפרויקט ←</em>', 3)
rep('<button id="mmEnd">לבחירת דירה</button>', '<button id="mmEnd">לשלושת הפרויקטים</button>')
rep('<li id="gw5">מהדגלים אפשר להמשיך לבחירת דירה אמיתית</li>', '<li id="gw5">מהדגלים עוברים לעמודי הפרויקטים</li>')
rep('~480 units,', '459 units per the developer (480 in the 2023 design plan),')

# the strings, Hebrew
rep("btnProject: 'לעמוד הפרויקט ולבחירת דירה ←'", "btnProject: 'לעמוד הפרויקט ←'")
rep("pickHere: 'בחרו דירה בבניין הזה ←'", "pickHere: 'לעמוד הפרויקט ←'")
rep("liStSale: 'סטטוס: <b>בשיווק</b>',", "liStSale: 'סטטוס: <b>בשיווק</b>', liStBuild: 'סטטוס: <b>בבנייה</b>',")
rep("liRain1: '<b>כ־38</b> קומות', liRain2: '<b>480</b> דירות'", "liRain1: '<b>39</b> קומות', liRain2: '<b>459</b> דירות'")
rep("finH2: 'בחרו דירה מתוך הבניין'", "finH2: 'שלושה פרויקטים ברובע'")
rep("finP: 'שלושה פרויקטים, חופש בחירה מלא — בניין, קומה, כיוון ונוף.'", "finP: 'לכל פרויקט עמוד משלו, עם העובדות והמקורות.'")
rep("finSpan2: 'מגדל הדגל · כ־38 קומות · 480 דירות'", "finSpan2: 'מגדל הדגל · 39 קומות · 459 דירות'")
rep("finEm: 'לבחירת דירה ←'", "finEm: 'לעמוד הפרויקט ←'")
rep("mmEnd: 'לבחירת דירה'", "mmEnd: 'לשלושת הפרויקטים'")
rep("gw5: 'מהדגלים אפשר להמשיך לבחירת דירה אמיתית'", "gw5: 'מהדגלים עוברים לעמודי הפרויקטים'")
# the strings, English
rep("btnProject: 'Project page & pick a home →'", "btnProject: 'To the project page →'")
rep("pickHere: 'Pick a home in this building →'", "pickHere: 'To the project page →'")
rep("liStSale: 'Status: <b>in sales</b>',", "liStSale: 'Status: <b>in sales</b>', liStBuild: 'Status: <b>under construction</b>',")
rep("liRain1: '<b>~38</b> floors', liRain2: '<b>480</b> homes'", "liRain1: '<b>39</b> floors', liRain2: '<b>459</b> homes'")
rep("finH2: 'Pick your home from the building itself'", "finH2: 'Three projects in the quarter'")
rep("finP: 'Three projects, full freedom — building, floor, direction and view.'", "finP: 'Each project has its own page, with the facts and the sources.'")
rep("finSpan2: 'Flagship tower · ~38 floors · 480 homes'", "finSpan2: 'Flagship tower · 39 floors · 459 homes'")
rep("finEm: 'Pick a home →'", "finEm: 'Project page →'")
rep("mmEnd: 'Pick a home'", "mmEnd: 'The three projects'")
rep("gw5: 'From the flagships you can continue to a real apartment picker'", "gw5: 'From the flags you go on to the project pages'")
rep("['#card-rainbow li:nth-child(3)', 'liStSale']", "['#card-rainbow li:nth-child(3)', 'liStBuild']")
# the narration: captions say what the new clips say
rep("במגרש הצמוד לפארק ולכיכר השער.'", "במגרש הצמוד לפארק ולכיכר השער.'")  # anchor check only
rep("מגדל דגל ושישה בנייני חצר, כ־480 דירות,", "מגדל דגל ושישה בנייני חצר, 459 דירות לפי היזם,")
rep("לחצו על כל בניין, בחרו דירה, וצאו לסיור חופשי ברחובות.", "לחצו על כל בניין כדי להכיר אותו, וצאו לסיור חופשי ברחובות.")
rep("about four hundred eighty homes, right by the park", "four hundred fifty-nine homes by the developer’s count, right by the park")
rep("Tap any building, pick an apartment, and take a free walk through the streets.", "Tap any building to meet it, and take a free walk through the streets.")
rep("const NARR_BASE = 'https://nad-lan.co.il/wp-content/uploads/2026/08/';",
    "const NARR_BASE = 'https://nad-lan.co.il/wp-content/uploads/2026/08/';\n"
    "/* 1.72.311: clips 3 (Rainbow: 459 apartments, not about 480) and 5 (no apartment picking) re-voiced, same voices and rates */\n"
    "const NARR_FIX = { 'he-3': 1, 'he-5': 1, 'en-3': 1, 'en-5': 1 };\n"
    "const NARR_FIX_BASE = 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/tours/';")
rep("new Audio(NARR_BASE + 'narr-sdedov-' + L + '-' + i + '.mp3')",
    "new Audio(NARR_FIX[L + '-' + i] ? NARR_FIX_BASE + 'narr-sdedov-' + L + '-' + i + '-v2.mp3' : NARR_BASE + 'narr-sdedov-' + L + '-' + i + '.mp3')")
left = [w for w in ("ולבחירת דירה", "בחרו דירה", "חופש בחירה", "כ־480", "כ־38", "pick a home", "Pick a home", "apartment picker", "pick an apartment") if w in s]
print("left:", left)
io.open(SRC, "w", encoding="utf-8", newline="").write(s)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="").write(s)
print("written", len(s.encode("utf-8")))
