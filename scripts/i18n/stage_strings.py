# -*- coding: utf-8 -*-
"""HAD-361: every Hebrew string the project stage can show, for the language pages' dictionary (i18n/lang-pages.json).
Sources: the stage's scripts (bridge.js, tour.js, slice.js, the four stage.js), the projects' data (facilities.json,
quarter.json, city.json) and the stage's page parts (inc/project-stage.php). A template literal with ${...} becomes a
pattern (each ${} a capture). Writes docs/i18n/stage-strings.json: {"exact": [...], "patterns": [...], "where": {...}}.
  python scripts/i18n/stage_strings.py"""
import io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PS = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage")
HE = re.compile(r"[֐-׿]")
exact, patterns, where = {}, {}, {}


def add(s, src):
    s = re.sub(r"\s+", " ", s).strip()
    if not s or not HE.search(s):
        return
    if "${" in s:
        parts = re.split(r"\$\{[^}]*\}", s)
        rx = "^" + "(.+?)".join(re.escape(p) for p in parts) + "$"
        patterns.setdefault(rx, s)
        where.setdefault(rx, src)
        return
    exact.setdefault(s, src)


def from_js(path, tag):
    s = io.open(path, encoding="utf-8").read()
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)          # block comments
    s = re.sub(r"(?m)^\s*//.*$", " ", s)                   # whole-line comments
    s = re.sub(r"(?<=[;,{}()\s])//[^\n'\"`]*$", " ", s, flags=re.M)  # trailing comments without quotes in them
    for m in re.finditer(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\]|\\.)*)`", s):
        t = m.group(1) or m.group(2) or m.group(3) or ""
        add(t.replace("\\'", "'").replace('\\"', '"'), tag)


def walk_json(o, tag, key=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "src", "url", "source") and isinstance(v, str) and len(v) > 120:
                add(v, tag + ":" + k)  # long notes still go in: they are shown in the cards
            else:
                walk_json(v, tag, k)
    elif isinstance(o, list):
        for v in o:
            walk_json(v, tag, key)
    elif isinstance(o, str):
        add(o, tag + ":" + key)


for f in ("bridge.js", "tour.js", "slice.js"):
    from_js(os.path.join(PS, f), f)
for d in ("rainbow", "duo", "dimri", "ashira"):
    from_js(os.path.join(PS, d, "stage.js"), d + "/stage.js")
    for j in ("facilities.json", "quarter.json"):
        p = os.path.join(PS, d, j)
        if os.path.exists(p):
            walk_json(json.load(io.open(p, encoding="utf-8")), d + "/" + j)
    cj = os.path.join(PS, d, "city.json")
    if os.path.exists(cj):
        c = json.load(io.open(cj, encoding="utf-8"))
        for k, v in c.items():
            if isinstance(v, str):
                add(v, d + "/city.json:" + k)
# the page parts: single-quoted PHP strings inside nadlan_ps_parts / nadlan_ps_deals / the configs
php = io.open(os.path.join(REPO, "plugins", "nadlan-config", "inc", "project-stage.php"), encoding="utf-8").read()
php = re.sub(r"(?m)^\s*//.*$", " ", php)
php = re.sub(r"/\*.*?\*/", " ", php, flags=re.S)
for m in re.finditer(r"'((?:[^'\\]|\\.)*)'", php):
    t = m.group(1).replace("\\'", "'")
    if "<" in t:  # markup fragments: the text between tags
        for x in re.findall(r">([^<]+)<", "<x>" + t + "</x>"):
            add(x, "project-stage.php")
    else:
        add(t, "project-stage.php")
out = os.path.join(REPO, "docs", "i18n")
os.makedirs(out, exist_ok=True)
doc = {"note": "HAD-361: the stage's Hebrew strings (scripts/i18n/stage_strings.py). exact = whole strings as shown; patterns = regex with (.+?) captures, from template literals.",
       "exact": sorted(exact), "patterns": [{"re": k, "he": v} for k, v in sorted(patterns.items())], "where": {**exact, **where}}
io.open(os.path.join(out, "stage-strings.json"), "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
print(len(exact), "exact,", len(patterns), "patterns ->", os.path.join(out, "stage-strings.json"))
