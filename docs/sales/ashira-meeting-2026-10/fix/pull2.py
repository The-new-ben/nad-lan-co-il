import os
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "p2"}; exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
for lang, pid in (("en", 4927), ("fr", 4926), ("ru", 4924), ("ar", 4925)):
    s, d, _ = req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit")
    open(os.path.join(HERE, f"live-{lang}-{pid}.raw"), "wb").write(d["content"]["raw"].encode("utf-8"))
    print(lang, pid, s, d.get("modified"))
