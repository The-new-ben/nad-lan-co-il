# -*- coding: utf-8 -*-
"""Release 1.72.446 (HAD-527 live fault): inc/instruments.php built the asset URLs under inc/ (plugins_url relative to
inc/instruments.php), so core.js, core.css, the tool scripts and the data answered 404 on the two tool pages. One line:
the URLs are built from the plugin root. FILES = the changed inc/instruments.php; no hunk."""
RELS = []
FILES = {}


def apply(rel, txt):
    raise SystemExit("fix_446: no hunk on " + rel)
