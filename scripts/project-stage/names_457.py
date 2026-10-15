# -*- coding: utf-8 -*-
"""Release 1.72.457 (HAD-534, Ben 15.10.2026): no project or company names on the soil page. The public data file drops the
developer, note, press and page fields (the named research stays in docs/research/2026-10-15-sde-dov-soil/); each plot gets
its phase (a project in marketing, an RMI tender, a municipal permit request) and a one-tap "ask us for details" button
(WhatsApp). Calmer, precise wording ("בדיקות הקרקע"). Files: tools/soilmap.js, tools/soilask.js, core.css,
inc/instruments.php, data/sde-dov-soil.json. No hunk."""
RELS = []
FILES = {}


def apply(rel, txt):
    raise SystemExit("names_457: no hunk on " + rel)
