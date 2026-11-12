# -*- coding: utf-8 -*-
"""make deploy662.py from deploy661.py: 1.72.662 = HAD-706: on a phone the designer's video call (and its entry sheet) takes the
whole screen in any page, because inside /design-studio/ the designer is a block in the text and the site's floating bar sat on
the call's buttons (measured on the live page). Assets only: assets/designer/studio.js + the designer page for this version."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_release  # noqa: E402

design_release.build(661, 662, "20261112T003249Z", want=["assets/tours/designer-tour.html", "assets/designer/studio.js"],
                     line="on a phone the designer's video call takes the whole screen in any page (the site's floating bar no longer sits on its buttons)")
