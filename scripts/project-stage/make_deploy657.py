# -*- coding: utf-8 -*-
"""make deploy657.py from deploy656.py: 1.72.657 = HAD-706, a real LiveKit video call inside the apartment designer (start with
one press, join by a link, everyone moves things, invite by link or WhatsApp). All the logic is in call_release.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import call_release  # noqa: E402

call_release.build(656, 657, "20261111T212646Z")
