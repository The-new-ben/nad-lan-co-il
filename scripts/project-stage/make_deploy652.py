# -*- coding: utf-8 -*-
"""make deploy652.py from deploy651.py: 1.72.652 = HAD-712, the Arabic Kikar page (/projects/hamedina-ar/, post 8118): the calculator
financing block (one hunk on the LIVE inc/project-stage.php, the 651 text) and the FAQPage meta with the five new questions. The article
itself was edited before this release by scripts/kikar/had712_lang.py ar. All the logic is in kl_release.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

kl_release.build(651, 652, "ar", "3fd26aa9")
