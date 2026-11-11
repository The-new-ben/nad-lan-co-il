# -*- coding: utf-8 -*-
"""make deploy655.py from deploy654.py: 1.72.655 = HAD-701, the second release of Ben's 11.11.2026 evening orders: the floor and
the paint on a photo of the visitor's own room ([nadlan_room_photo]), camera measuring in Chrome on Android behind its trial
switch (?scan=on), and the planmaker's second round (counting tiles, calibration by the contract area). All the logic is in
photo_release.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import photo_release  # noqa: E402

photo_release.build(654, 655, "20261111T191224Z")
