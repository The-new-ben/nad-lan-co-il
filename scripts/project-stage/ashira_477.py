# -*- coding: utf-8 -*-
"""Release 1.72.477 (HAD-534 item d; Ben 21.10.2026 "don't drop tasks"): no hunk. The Instruments engine speaks English on
/en/ pages (core.js, core.css, inc/instruments.php: LTR, en-US numbers, IBM Plex Sans for Latin, English summaries, related
links and JSON-LD) for the tools that carry an English block (soilmap, pfas, soilask). Hebrew output unchanged, except one
fix: the Hebrew soil letter printed "ב־," with no date on five plots. Patch prepared and pressed in docs/tools/soil-en/."""
RELS = []


def apply(rel, txt):
    return txt
