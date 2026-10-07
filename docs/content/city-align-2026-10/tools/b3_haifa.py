# -*- coding: utf-8 -*-
"""Tier 3, Haifa (page 4579). Tier 2 already put the CBS figures in; what is left is two illustrative rents (2,700 and 5,000) in the same example."""
from b3lib import *


def build(P):
    old = P.sub('אם דירה דומה מושכרת רק ב-2,700 ש"ח, המחיר המבוקש צריך לקבל הסבר נוסף. אם היא מושכרת ב-5,000 ש"ח, יש לבדוק')
    new = 'אם דירה דומה מושכרת בסכום נמוך משמעותית מהממוצע, המחיר המבוקש צריך לקבל הסבר נוסף. אם היא מושכרת בסכום גבוה משמעותית ממנו, יש לבדוק'
    P.edit(old, new, "B", 'removed the two illustrative rents 2,700 and 5,000 from the example (the CBS averages 3,405 and 3,119 stay in the same paragraph); the two cases are stated in words',
           "Left over after tier 2: two invented comparison rents (2,700 'much lower', 5,000 'much higher') that sit around the CBS figure in the same example. They are not official and have no counterpart; the numbers go and the logic (a rent far below or far above the average needs an explanation) stays.")
