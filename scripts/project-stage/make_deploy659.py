# -*- coding: utf-8 -*-
"""make deploy659.py from deploy658.py: 1.72.659 = HAD-706 fix: the designer's call token comes from the shared LiveKit
project's edge function when the site has no local key (as the live inc/together.php does). No new file."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import call_release  # noqa: E402

call_release.build(658, 659, "20261111T214557Z", NEWLIST=[])
