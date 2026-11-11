# -*- coding: utf-8 -*-
"""make deploy650.py from deploy649.py: 1.72.650 = HAD-712, the French Kikar page (/projects/hamedina-fr/, post 8116): the calculator
financing block (one hunk on the LIVE inc/project-stage.php, the 649 text) and the FAQPage meta with the five new questions. The article
itself was edited before this release by scripts/kikar/had712_lang.py fr. All the logic is in kl_release.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

kl_release.build(649, 650, "fr", "da003ba5")
