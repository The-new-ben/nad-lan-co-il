# -*- coding: utf-8 -*-
"""make deploy660.py from deploy659.py: 1.72.660 = HAD-706, the call's designed interface (docs/design-lab/apartment-designer/
call-design/): assets only, no PHP hunk, no new file. The swap list is proven against the live read named below."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_release  # noqa: E402

design_release.build(659, 660, "20261111T230122Z")
