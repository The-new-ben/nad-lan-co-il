# -*- coding: utf-8 -*-
"""Release 1.72.444 (HAD-495): (1) DealSign v2 on the live inc/deal-sign.php (FILES: the brokerage agreement alone by default,
the materials tab, the download route); (2) the hunk here: Meital's square leaves the Rainbow rail until Israel Canada agrees
(Ben, 13.10.2026: she approaches them first as a regular broker). Nothing else in inc/project-stage.php moves."""
RELS = ["inc/project-stage.php"]
FILES = {}
OLD = "\t\t\t\t'rail'           => array( 7833 ),\n"
NEW = "\t\t\t\t'rail'           => array(), // HAD-495 (13.10.2026): Meital's square waits until Israel Canada agrees\n"


def apply(rel, txt):
    if NEW in txt:
        raise SystemExit("rail_444: already applied")
    if txt.count(OLD) != 1:
        raise SystemExit("rail_444: the Rainbow rail line is not there once")
    return txt.replace(OLD, NEW)
