# -*- coding: utf-8 -*-
"""Read live plugin files through a temporary release bridge (the runner's own functions; nothing else is written). Saves to scratchpad/live/."""
import base64, os, sys
H = r"C:\Users\777\nad-lan\nad-lan-co-il\scripts\project-stage"
sys.path.insert(0, H); os.chdir(r"C:\Users\777\nad-lan\nad-lan-co-il")
src = open(os.path.join(H, "deploy520.py"), encoding="utf-8").read()
sys.argv = ["deploy520.py", "--dry"]
ns = {"__name__": "fetchlive", "__file__": os.path.join(H, "deploy520.py")}
exec(compile(src[:src.index("def page(path):")], "deploy520", "exec"), ns)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live"); os.makedirs(OUT, exist_ok=True)
ns["bridge_up"]()
try:
    for rel in sys.argv[1:] or ["inc/urban-map.php", "inc/term-faq-schema.php"]:
        pass
    for rel in ["inc/urban-map.php", "inc/term-faq-schema.php"]:
        g = ns["live_get"](rel)
        if g.get("missing"):
            print(rel, "missing"); continue
        d = base64.b64decode(g["b64"]); p = os.path.join(OUT, rel.replace("/", "__"))
        open(p, "wb").write(d); print(rel, len(d), "bytes, md5", g["md5"][:10], "->", p)
finally:
    ns["bridge_down"]()
