# -*- coding: utf-8 -*-
"""make deploy644.py from deploy643.py: 1.72.644 = HAD-712, Ben 11.11.2026 after seeing ?kikar=show: "Yes, open it".
  SWAP assets/project-stage/world/journey.js: the showroom stage (1.72.643) is the Hebrew Kikar page for every visitor;
       ?kikar=journey keeps the earlier path (tower list, floor slider, view list) for comparison.
  No PHP change; nadlan-config.php on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
PREV, NEWV = 643, 644
md5 = lambda b: hashlib.md5(b).hexdigest()
W = "assets/project-stage/world/"
FILES = [W + "journey.js"]
NEWFILES = set()
_jp = os.path.join(PLUG, *(W + "journey.js").split("/"))
assert b"\r\n" not in open(_jp, "rb").read(), "CRLF"
o = subprocess.run(["node", "--check", _jp], capture_output=True, text=True)
assert o.returncode == 0, o.stderr[-300:]
jy = open(_jp, encoding="utf-8").read()
assert jy.count("get('kikar') !== 'journey'") == 1 and "get('kikar') === 'show'" not in jy and "m.mountShowroom(stage)" in jy
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first" % PREV
assert W + "journey.js" in (rp.get("files") or {}) and W + "showroom.js" in rp["files"], "1.72.643 did not write the showroom"
# the only difference from the 1.72.643 file is the gate line and its comment
_g = subprocess.run(["git", "-C", REPO, "show", "947b1b21:plugins/nadlan-config/" + W + "journey.js"], capture_output=True)
assert _g.returncode == 0 and md5(_g.stdout) == rp["files"][W + "journey.js"], "no copy of the 1.72.643 journey.js to compare with"
_a, _b = _g.stdout.decode("utf-8").split("\n"), jy.split("\n")
_d = [(x, y) for x, y in zip(_a, _b) if x != y]
assert len(_a) == len(_b) and len(_d) == 2 and all("SHOWROOM" in x for x, _ in _d), "journey.js changed more than the gate"
print("[%d] released | journey.js: the gate line and its comment only" % PREV)

src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
_m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
assert _m and _m.group(1) == "kikar_643", "no PX import"
AP = open(os.path.join(H, "kikar_641.py"), encoding="utf-8").read()
assert "\nRELS = []" in AP and "raise SystemExit('kikar_641: no hunk on ' + rel)" in AP, "kikar_641.py is not the no-hunk module"
AP = AP.replace("kikar_641", "kikar_644").replace("Release 1.72.641 (HAD-710, the Kikar living room in 360 from every apartment)", "Release 1.72.644 (HAD-712, Kikar's showroom stage open to every visitor)").replace("make_deploy641.py", "make_deploy644.py")
open(os.path.join(H, "kikar_644.py"), "w", encoding="utf-8", newline="\n").write(AP)

P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
assert src.count('WANT_LIVE = "1.72.%s"' % PP) == 1, "deploy643.py is not built on 1.72.642"
src = src.replace('WANT_LIVE = "1.72.%s"' % PP, 'WANT_LIVE = "@@WANT@@"')
for a, b in [("1.72." + P, "1.72." + N), ("ps" + P, "ps" + N), ("bak" + P, "bak" + N), ("make_deploy" + P, "make_deploy" + N),
             ("deploy-result-" + P, "deploy-result-" + N), ("speed-" + P, "speed-" + N), ("posts-before-" + P, "posts-before-" + N),
             ("deploy-result-" + PP, "deploy-result-" + P)]:
    src = src.replace(a, b)
src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.%s"' % P)
BS = chr(92)
src = re.sub(r"\?t" + P + r"([a-z]*)=1", "?t" + N + BS + "1=1", src)
src = re.sub(r"&t" + P + r"([a-z]*)=1", "&t" + N + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(%s, 329, -1)" % P, src); assert n == 1, n
src, n = re.subn(r"^    import kikar_643 as PX  # noqa: E402 \(.*$", "    import kikar_644 as PX  # noqa: E402 (1.72.644: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.644 LIVE: [^"]*"\)', 'print("RELEASE 1.72.644 LIVE: Kikar showroom stage open to every visitor of /projects/hamedina/")', src); assert n == 1, n
# the row that pinned the gate: journey.js now opens the showroom unless ?kikar=journey
_old = [l for l in src.split("\n") if "journey.js?t644a=1'" in l]
assert len(_old) == 1 and "get('kikar') === 'show'" in _old[0], _old
src = src.replace(_old[0], _old[0].replace("get('kikar') === 'show'", "get('kikar') !== 'journey'"), 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.644: one swap (from .bak644)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.644: no hunked PHP; nadlan-config.php is restored from .bak644 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "kikar_643 as PX" not in src and ("t" + P + "a=1") not in src
assert src.count('WANT_LIVE = "1.72.643"') == 1 and src.count('BAK = ".bak644"') == 1 and src.count("range(643, 329, -1)") == 1
assert src.count('if new != "1.72.644":') == 1
open(os.path.join(H, "deploy644.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy644.py + kikar_644.py written | 1 swap (journey.js) | the gate row rewritten")
