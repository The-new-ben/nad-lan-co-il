# -*- coding: utf-8 -*-
"""Release 1.72.413 = urban's HAD-393 focus-only fix (commit f8947090, Maya ACCEPT 6/6, focus393-verdict.md, 09:29 UTC):
the smart form takes no focus on its first render, so the page no longer scrolls itself down to the form on load
(/urban-renewal/, /buying-apartment/, /sell-by-auction/). Four hunks, frozen in docs/qa/had-393-release/hunks.json
from git diff dc9c572d -> f8947090 (rebuilds urban's expected 4f469baab6 -> 40d6011041 exactly). Applied to the LIVE text by the
runner, each anchor once."""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
H = json.load(io.open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "qa", "had-393-release", "hunks.json"), encoding="utf-8"))
PAIRS = [tuple(p) for p in H["pairs"]]


def apply(txt):
    if "acted=false" in txt:
        raise SystemExit("sf_413: the HAD-393 focus fix is already there")
    for o, n in PAIRS:
        if txt.count(o) != 1:
            raise SystemExit("sf_413: an anchor is there " + str(txt.count(o)) + " times: " + o.strip()[:70])
        txt = txt.replace(o, n)
    return txt
