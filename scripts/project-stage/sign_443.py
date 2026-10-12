# -*- coding: utf-8 -*-
"""Release 1.72.443 (HAD-495): DealSign, the signing room of a developer cooperation, as a NEW module file inc/deal-sign.php
(the broker's office, the developer's signing page, client registration and the developer's review). No change to
inc/project-stage.php: RELS is empty, the runner ships the new file through FILES/NEWFILES and adds 'deal-sign' to the module
list in nadlan-config.php."""
RELS = []
FILES = {}


def apply(rel, txt):
    raise SystemExit("sign_443: no hunk on " + rel)
