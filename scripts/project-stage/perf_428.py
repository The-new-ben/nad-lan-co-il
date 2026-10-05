# -*- coding: utf-8 -*-
"""Release 1.72.428 (HAD-421 step 9, A/B, the Kikar loop turn 38, design v104.51): an address switch to mount the world early.
The world's boot module (nadlan_ps_world_script, <script type="module" id="nadlan-ps-world">) waits for window 'load' and then
an idle moment. Measured 5.10 on slow 4G: FCP 2.8 s, DOMContentLoaded 5.1 s, load 8.4 s; the world starts loading at 8.5 s and
is usable at 12.4 s. With ?nlwboot=early in the address, mount() runs as soon as the module runs (modules run before
DOMContentLoaded), through requestIdleCallback with a 600 ms ceiling. Without the switch NOTHING changes: the old line stays as
the else branch. The default flips only after the A/B (tools/stage_speed.py on both addresses) shows a gain.
Applied to the LIVE inc/project-stage.php text (what 1.72.427 wrote): the boot line, exactly once."""

RELS = ["inc/project-stage.php"]
FILES = {}
OLD = "  if (document.readyState === 'complete') later(); else addEventListener('load', later, { once: true });\n"
NEW = ("  // v104.51 (HAD-421, A/B): ?nlwboot=early mounts once the document is parsed (this module runs before DOMContentLoaded)\n"
       "  // instead of after window load; without the switch the default below is unchanged until the A/B is measured\n"
       "  if (/[?&]nlwboot=early(&|$)/.test(location.search)) { if ('requestIdleCallback' in window) requestIdleCallback(mount, { timeout: 600 }); else setTimeout(mount, 0); }\n"
       "  else if (document.readyState === 'complete') later(); else addEventListener('load', later, { once: true });\n")


def apply(rel, txt):
    if "nlwboot=early" in txt:
        raise SystemExit("perf_428: already applied")
    if txt.count(OLD) != 1:
        raise SystemExit("perf_428: the boot line is there " + str(txt.count(OLD)) + " times")
    return txt.replace(OLD, NEW)
