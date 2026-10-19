# -*- coding: utf-8 -*-
"""make deploy470.py from deploy469.py: the two English narrated films (+ posters, new files) and the ashira_470 hunk (the
how-to card becomes a two-tab gallery); the film check now looks for the gallery."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/project-stage/ashira/film-call-en.jpg", "assets/project-stage/ashira/film-call-en.mp4",
         "assets/project-stage/ashira/film-showroom-en.jpg", "assets/project-stage/ashira/film-showroom-en.mp4"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy469.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(FILES) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.470: the ashira_470 hunk, restored from .bak470'
    elif l.startswith("    ('/projects/ashira-sde-dov/?t469=1', ['class=\"nlds nlps-howtowrap\""):
        lines[i] = "    ('/projects/ashira-sde-dov/?t470=1', ['class=\"nlds nlps-howtowrap\"', 'class=\"nlps-howto__v\"', 'assets/project-stage/ashira/film-showroom-en.mp4?ver=1.72.470', 'assets/project-stage/ashira/film-call-en.mp4?ver=1.72.470', 'nlps-howto__tab', 'סרטוני הסבר'], ['howto-he.mp4']),"
src = "\n".join(lines)
for a, b in [("1.72.469", "1.72.470"), ("ps469", "ps470"), ("bak469", "bak470"), ("make_deploy469", "make_deploy470"),
             ("deploy-result-469", "deploy-result-470"), ("speed-469", "speed-470"), ("posts-before-469", "posts-before-470"),
             ("ashira_469", "ashira_470"), ("deploy-result-468", "deploy-result-469"), ("1.72.468", "1.72.469"),
             ("range(468, 329", "range(469, 329"), ("?t469d=1", "?t470d=1"), ("?t469c=1", "?t470c=1"), ("?t469b=1", "?t470b=1")]:
    src = src.replace(a, b)
assert "?t470=1" in src
src = src.replace('print("RELEASE 1.72.470 LIVE: Ashira rooms with and without furniture, every direction, floors 25 and 10")', 'print("RELEASE 1.72.470 LIVE: Ashira film gallery (English, narrated): the showroom and the video call")')
open(os.path.join(H, "deploy470.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy470.py written", PIN)
