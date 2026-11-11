# -*- coding: utf-8 -*-
"""make deploy653.py from deploy652.py: 1.72.653 = HAD-701 / HAD-708 / HAD-707 (Ben 11.11.2026 evening): "my plan" (a visitor
loads his own apartment plan: upload, scale, trace, or room by room from measurements) and the new designer on the page every
project opens for "עיצוב הדירה" (/tour/designer/). All the logic is in myplan_release.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import myplan_release  # noqa: E402

myplan_release.build(652, 653, "20261111T180008Z")
