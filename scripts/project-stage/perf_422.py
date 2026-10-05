# -*- coding: utf-8 -*-
"""Release 1.72.422 (HAD-421 step 2a, the Kikar loop turn 32, design v104.45): the world poster downloads once on phones.
The page's own <picture> picks poster-800.webp up to 700 px (media query). The world module builds a second poster <img> from
srcset "800w, 1600w" with sizes "(max-width:700px) 100vw", so a 390 px phone at DPR 3 asks for 1170 px and fetched
poster-1600.webp too (280 KB, measured 5.10). The phone hint becomes 228px (800 / 3.5), so every phone up to DPR 3.5 picks the
same 800 file the page already holds (a cache hit), exactly what the page shows today. Desktop keeps 70vw (1600, as the
<picture> picks above 700 px). The rendered size is CSS, not sizes: nothing on screen changes.
Applied to the LIVE inc/project-stage.php text (what 1.72.421 wrote), the one occurrence."""

RELS = ["inc/project-stage.php"]
FILES = {}
OLD = "'sizes' => '(max-width:700px) 100vw, 70vw'"
NEW = "'sizes' => '(max-width:700px) 228px, 70vw' /* v104.45 (HAD-421): phones pick the 800 file the page's picture already loaded */"


def apply(rel, txt):
    if "228px, 70vw" in txt:
        raise SystemExit("perf_422: already applied")
    if txt.count(OLD) != 1:
        raise SystemExit("perf_422: the poster sizes hint is there " + str(txt.count(OLD)) + " times")
    return txt.replace(OLD, NEW)
