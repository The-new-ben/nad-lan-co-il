# -*- coding: utf-8 -*-
"""make deploy654.py from deploy653.py (the designer's 1.72.653): 1.72.654 = HAD-712, the Russian Kikar page: the FAQ meta follows the
reworded article (no dashes in the Russian additions; scripts/kikar/had712_ru_dashes.py). No file, no hunk. Logic in kl_release.py (build_meta_only)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

kl_release.build(653, 654, "ru", "4f58afe2", meta_only=True)
