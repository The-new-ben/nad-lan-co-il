# -*- coding: utf-8 -*-
import io, os, sys, time, json
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = io.open(os.path.join(REPO, "scripts", "project-stage", "rainbow_content4.py"), encoding="utf-8").read()
exec(compile(src[src.index("import base64, ctypes"):src.index("FIXES = [")].replace("PID = 4464", "PID = 6548"), "head", "exec"))
NEW = "H Infinity - מגדל אינפיניטי של קבוצת חג'ג' במתחם סומייל, תל אביב"
s, d = req("GET", "/wp-json/wp/v2/nadlan_project/6548?context=edit&_fields=id,title,slug")
old = d["title"]["raw"]
print("[old]", old, "| slug", d["slug"])
if "--apply" in sys.argv:
    io.open(os.path.join(REPO, "docs", "qa", "hinfinity-content-2026-09-28", "title.%s.before.txt" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8").write(old)
    s, r = req("POST", "/wp-json/wp/v2/nadlan_project/6548", {"title": NEW})
    s, d = req("GET", "/wp-json/wp/v2/nadlan_project/6548?context=edit&_fields=id,title,slug")
    print("[write]", s, "| now", d["title"]["raw"], "| slug", d["slug"])
