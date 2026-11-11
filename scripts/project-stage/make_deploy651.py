# -*- coding: utf-8 -*-
"""make deploy651.py from deploy650.py: 1.72.651 = HAD-712, the Russian Kikar page (/projects/hamedina-ru/, post 8117): the calculator
financing block (one hunk on the LIVE inc/project-stage.php, the 650 text) and the FAQPage meta with the five new questions. The article
itself was edited before this release by scripts/kikar/had712_lang.py ru. All the logic is in kl_release.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

kl_release.build(650, 651, "ru", "e0bb3816")
