# -*- coding: utf-8 -*-
"""make deploy649.py from deploy648.py: 1.72.649 = HAD-712, the English Kikar page (/projects/hamedina-en/, post 8114): the calculator
financing block (one hunk on the LIVE inc/project-stage.php, the 648 text) and the FAQPage meta with the five new questions. The article
itself was edited before this release by scripts/kikar/had712_lang.py en. All the logic is in kl_release.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

kl_release.build(648, 649, "en", "d26a538f")
