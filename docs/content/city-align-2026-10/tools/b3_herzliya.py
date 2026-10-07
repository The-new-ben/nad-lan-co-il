# -*- coding: utf-8 -*-
"""Tier 3, Herzliya (page 154). Tier 2 already put the CBS figures in; what is left is one illustrative rent (8,000)."""
from b3lib import *


def build(P):
    old = P.sub('לכן שכירות של כ-8,000 ש"ח אינה אומרת אוטומטית שמחיר')
    new = 'לכן שכירות של דירה אחת אינה אומרת אוטומטית שמחיר'
    P.edit(old, new, "B", 'removed the illustrative rent 8,000 (it matches neither the CBS city average 6,775 nor any CBS size group); the sentence says it in words',
           "Left over after tier 2: 'a rent of about 8,000 does not automatically mean that a price of about 3.8 million is right'. 8,000 is a listing-site level, not the CBS 6,775 (all flats) or any size group, and the flat's size is not stated, so there is no CBS counterpart; the number goes and the point stays.")
