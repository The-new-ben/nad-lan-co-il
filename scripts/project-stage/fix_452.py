# -*- coding: utf-8 -*-
"""Release 1.72.452 (HAD-533 follow-up, found by measuring the live phone table): two theme rules with !important stripped
the Instruments cells on phones (nl-premium-ui: padding 8px 0 + width 100%; skin-a: its own font), so dates ran into each
other. core.css now wins with its own !important cell rules; core.js gains table.phoneHide (columns a phone does not need);
warranty.js folds the end date into the status cell and hides the two date columns on phones. No hunk."""
RELS = []
FILES = {}


def apply(rel, txt):
    raise SystemExit("fix_452: no hunk on " + rel)
