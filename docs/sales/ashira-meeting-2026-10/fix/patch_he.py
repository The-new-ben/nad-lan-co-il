# -*- coding: utf-8 -*-
"""HAD-543: narrow repair of the Hebrew Ashira article (post 4744). Removes internal working notes and the description of a
facade with coloured cells that the page does not have; replaces that one paragraph with what the page really does.
Nothing else changes (title, URL, headings, sources, facts). python patch_he.py -> after-he-4744.html + diff-he.txt"""
import difflib, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, "before-he-4744.html"), encoding="utf-8").read()
EDITS = [
    # (unique start of the paragraph text, replacement paragraph text or None to delete the whole <p>)
    ("השלב השני הוא בחירת הדירה על החזית הקבועה.",
     "השלב השני הוא בחירת הקומה והכיוון על דגם התלת ממד. לחיצה על קומה פותחת כרטיס עם הבניין, הקומה והכיוון, ומשם עוברים לנוף מהקומה, למפת הסביבה ולבקשת תוכניות ומחירים."),
    ("בשלב הראשון נכון ליצור עמודים נפרדים באנגלית", None),
    ("הטכנולוגיה בדף יכולה לקבל בהמשך סרטון יוטיוב", None),
]
for start, new in EDITS:
    ps = [m for m in re.finditer(r"<p[^>]*>.*?</p>", t, re.S) if start in m.group(0)]
    assert len(ps) == 1, (start, len(ps))
    m = ps[0]
    if new is None:
        # drop the paragraph and the block comments that wrap it, if any
        a, b = m.start(), m.end()
        pre = t.rfind("<!-- wp:paragraph", 0, a)
        post = t.find("<!-- /wp:paragraph -->", b)
        if pre != -1 and t[pre:a].count("<p") == 0 and post != -1 and t[b:post].strip() == "":
            a, b = pre, post + len("<!-- /wp:paragraph -->")
        t = t[:a] + t[b:]
    else:
        open_tag = re.match(r"<p[^>]*>", m.group(0)).group(0)
        t = t[:m.start()] + open_tag + new + "</p>" + t[m.end():]
# the anchor sentence inside the Reading paragraph: drop only the internal sentence
s = " בדפים עתידיים לכל פרויקט צריך להחליף את נקודות העוגן לפי המקום"
i = t.find(s); assert i != -1 and t.count(s) == 1
j = t.find(".", i + 10)
# the sentence ends after the list "...לתושבים המקומיים."
j = t.find("לתושבים המקומיים.", i) + len("לתושבים המקומיים.")
t = t[:i] + t[j:]
open(os.path.join(HERE, "after-he-4744.html"), "w", encoding="utf-8").write(t)
b = open(os.path.join(HERE, "before-he-4744.html"), encoding="utf-8").read()
d = list(difflib.unified_diff(b.splitlines(), t.splitlines(), "before", "after", lineterm="", n=0))
open(os.path.join(HERE, "diff-he.txt"), "w", encoding="utf-8").write("\n".join(d))
print("chars", len(b), "->", len(t), "| diff lines", len(d))
for x in ("תא ירוק", "נקודות העוגן", "יוטיוב", "בשלב הראשון נכון"):
    print(x, x in t)
