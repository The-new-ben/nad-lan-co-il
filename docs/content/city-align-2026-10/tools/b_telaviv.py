# -*- coding: utf-8 -*-
"""Tel Aviv (page 135): the only figures in the body are a per-m2 'opening range' table with no source and no date."""
from mk import Page

P = Page("tel-aviv-apartment-prices")

old1 = "לכן כל טווח צריך להיבדק מול עסקאות דומות ועדכניות."
new1 = ("לכן כל טווח צריך להיבדק מול עסקאות דומות ועדכניות. בטבלה שלהלן מופיעה לכל סוג אזור דוגמה של חציון מחיר העסקה, "
        "לפי נתוני רשות המסים לרבעון הראשון של 2026.")
e1 = P.edit(old1, new1, ["data_quarter"], "WORDING", "Introduces the official neighbourhood medians that replace the per-m2 ranges (edits 2-7).")

e2 = P.edit("<th>טווח פתיחה לבדיקה</th>", "<th>חציון מחיר העסקה, ינואר-מרץ 2026</th>", ["data_quarter"], "UNSOURCED",
            "Column header of the per-m2 ranges, which have no source and no date.")
rows = [
    ("<td>כ-45,000 עד 65,000 ש\"ח למ\"ר</td>",
     "<td>ביד אליהו: 3,160,100 ש\"ח לדירת 3 חדרים ו-3,774,500 ש\"ח לדירת 4 חדרים</td>",
     ["neighbourhoods[יד אליהו].rooms.3", "neighbourhoods[יד אליהו].rooms.4"]),
    ("<td>כ-60,000 עד 90,000 ש\"ח למ\"ר</td>",
     "<td>בלב העיר: 4,738,800 ש\"ח לדירת 3 חדרים ו-6,467,500 ש\"ח לדירת 4 חדרים</td>",
     ["neighbourhoods[לב העיר].rooms.3", "neighbourhoods[לב העיר].rooms.4"]),
    ("<td>כ-65,000 עד 105,000 ש\"ח למ\"ר</td>",
     "<td>בצפון הישן, בחלקו הצפוני: 4,879,800 ש\"ח לדירת 3 חדרים ו-6,542,100 ש\"ח לדירת 4 חדרים. בצפון החדש, בחלקו הצפוני: 4,434,900 ש\"ח לדירת 3 חדרים ו-6,042,800 ש\"ח לדירת 4 חדרים</td>",
     ["neighbourhoods[הצפון הישן-החלק הצפ].rooms.3", "neighbourhoods[הצפון הישן-החלק הצפ].rooms.4",
      "neighbourhoods[הצפון החדש החלק הצפ].rooms.3", "neighbourhoods[הצפון החדש החלק הצפ].rooms.4"]),
    ("<td>כ-80,000 עד 140,000 ש\"ח למ\"ר ומעלה</td>",
     "<td>המחירון שבעמוד אינו מציג חציון נפרד לאזור זה; בודקים עסקאות באותו רחוב ובאותו סוג בניין</td>", ["data_quarter"]),
    ("<td>כ-100,000 עד 200,000 ש\"ח למ\"ר ומעלה</td>",
     "<td>המחירון שבעמוד אינו מציג חציון נפרד לסוג נכס זה; בודקים עסקאות באותו פרויקט ובקומות דומות</td>", ["data_quarter"]),
]
en = []
for old, new, keys in rows:
    en.append(P.edit(old, new, keys, "UNSOURCED",
                     "Per-m2 'opening range' with no named source and no date (the intro cites 'market pages, listings, deals and professional "
                     "publications'); replaced by official neighbourhood medians for 1-3.2026 where the official file has one, else by a check "
                     "instruction without a number."))

old8 = "דירה אחת יכולה להיות מתחת לטווח בגלל צורך בשיפוץ, בניין בעייתי או זכויות מורכבות. דירה אחרת יכולה להיות מעל הטווח בגלל"
new8 = "דירה אחת יכולה להיות מתחת לחציון בגלל צורך בשיפוץ, בניין בעייתי או זכויות מורכבות. דירה אחרת יכולה להיות מעל החציון בגלל"
e8 = P.edit(old8, new8, ["data_quarter"], "WORDING", "Follows the table change: 'range' becomes 'median'.")

C = P.claim
labels = ["דרום ומזרח מתחדשים | כ-45,000 עד 65,000 ש\"ח למ\"ר", "מרכז העיר ולב העיר | כ-60,000 עד 90,000 ש\"ח למ\"ר",
          "הצפון הישן והחדש | כ-65,000 עד 105,000 ש\"ח למ\"ר", "נווה צדק וקו חוף | כ-80,000 עד 140,000 ש\"ח למ\"ר ומעלה",
          "מגדלי יוקרה ופנטהאוזים | כ-100,000 עד 200,000 ש\"ח למ\"ר ומעלה"]
where = ["tr@43482", "tr@43623", "tr@43761", "tr@43897", "tr@44039"]
for w, q, n in zip(where, labels, en):
    C(w, q, "per_m2", "UNSOURCED", f"edit {n}", figures=2, note="no named source, no date; the official data has no per-m2 figure")

P.write(notes=("The Tel Aviv body has no other price, rent or percent figure; it is a method guide. The only figures are the per-m2 table. "
               "Official neighbourhood names are truncated in the file ('הצפון הישן-החלק הצפ', 'הצפון החדש החלק הצפ'); the text uses the "
               "natural names. Rows 4-5 (Neve Tzedek and seafront, luxury towers) have no official neighbourhood median in the city file, so "
               "they get a check instruction without a number. The H2 'טווחי מחיר למ\"ר בתל אביב' carries no number and is kept."))
