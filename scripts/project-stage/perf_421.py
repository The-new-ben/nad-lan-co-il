# -*- coding: utf-8 -*-
"""Release 1.72.421 (HAD-421 step 3, the Kikar loop turn 31, design v104.44): lazy film posters. Every <video> in the Kikar film
section (the narrated v2 film, V1 and the facilities clip, wide and upright) carried poster="...", so a phone fetched all six
posters at page load, including the wide ones that phones never show (display:none), far below the first screen. The poster
URL moves to data-nlposter, and one small script sets the real poster when a video comes within 800 px of the screen.
A hidden video never intersects, so its poster is never fetched. Without IntersectionObserver every poster is set at once.
Nothing else changes: the same posters, the same players, no autoplay, preload none.
Applied to the LIVE inc/project-stage.php text (what 1.72.420 wrote): the three poster attributes, and the script once."""

RELS = ["inc/project-stage.php"]
FILES = {}
POSTER = "controls playsinline preload=\"none\" poster=\"' . esc_url("
LAZY = "controls playsinline preload=\"none\" data-nlposter=\"' . esc_url("
STYLE_END = ".nlws-film figcaption{margin-top:8px;font-size:13px;color:#6B6558}</style>';\n"
SCRIPT = ("<script id=\"nlws-film-lazy\">(function(){var vs=document.querySelectorAll(\"video[data-nlposter]\");if(!vs.length)return;"
          "var set=function(v){if(!v.getAttribute(\"poster\")){v.setAttribute(\"poster\",v.getAttribute(\"data-nlposter\"));}};"
          "if(!(\"IntersectionObserver\" in window)){for(var i=0;i<vs.length;i++){set(vs[i]);}return;}"
          "var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){set(e.target);io.unobserve(e.target);}});},{rootMargin:\"800px 0px\"});"
          "for(var j=0;j<vs.length;j++){io.observe(vs[j]);}})();</script>")
if "'" in SCRIPT:
    raise SystemExit("perf_421: the script must hold no single quote (it sits in a single-quoted PHP string)")


def apply(rel, txt):
    if "nlws-film-lazy" in txt:
        raise SystemExit("perf_421: already applied")
    if txt.count(POSTER) != 3:
        raise SystemExit("perf_421: expected 3 poster attributes, found " + str(txt.count(POSTER)))
    if txt.count(STYLE_END) != 1:
        raise SystemExit("perf_421: the film style end is there " + str(txt.count(STYLE_END)) + " times")
    txt = txt.replace(POSTER, LAZY)
    # v104.44: the lazy-poster script, once, right after the film section's style
    return txt.replace(STYLE_END, STYLE_END[:-2] + "\n\t\t\t. '" + SCRIPT + "'; // v104.44 lazy posters (HAD-421)\n")
