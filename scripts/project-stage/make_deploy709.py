# -*- coding: utf-8 -*-
"""1.72.709 = HAD-793 release A (packages 7-8 of the long film). The generator is scripts/had793/make_release_a.py (prev, new):
  python scripts/had793/make_release_a.py 708 709"""
import os, runpy, sys
sys.argv = [sys.argv[0], "708", "709"]
runpy.run_path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "had793", "make_release_a.py"), run_name="__main__")
