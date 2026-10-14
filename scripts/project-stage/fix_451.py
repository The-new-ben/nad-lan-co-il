# -*- coding: utf-8 -*-
"""Release 1.72.451 (HAD-533 follow-up): the forced-table rule in core.css (1.72.447) also set white-space:nowrap on every
cell, which beat the 1.72.450 wrap; now text cells wrap and only figure cells (td.n) stay on one line. No hunk."""
RELS = []
FILES = {}


def apply(rel, txt):
    raise SystemExit("fix_451: no hunk on " + rel)
