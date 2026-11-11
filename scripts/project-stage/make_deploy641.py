# -*- coding: utf-8 -*-
"""make deploy641.py from deploy640.py (the /projects/ session's runner): 1.72.641 = HAD-710 (HAD-699, Ben 10.11.2026: "complete Kikar
seriously"): the living room in 360 from every apartment.
  NEW  assets/project-stage/hamedina/apt/<T><f>-<s>.webp + -card.webp: 48 day renders (towers A, B, C x floors 10, 20, 30 and the top
       floor x the plate's four sides), each with the real window view at that height (scripts/interior/render_kikar_360s.py, the
       web pictures by scripts/kikar/build_apt360.py).
  SWAP assets/project-stage/hamedina/cockpit.json (an "inside" list: tower, floor, true facing, picture, card; built by
       scripts/kikar/build_cockpit_data.py; nothing else changes but the build date) + world/cockpit.js (the "בפנים · 360°" tile
       shows this apartment's living room and opens it first; the three finishes of the C30 example stay as choices).
  No PHP change; nadlan-config.php on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
PREV, NEWV = 640, 641
md5 = lambda b: hashlib.md5(b).hexdigest()
W = "assets/project-stage/world/"
K = "assets/project-stage/hamedina/"
APT = sorted(os.listdir(os.path.join(PLUG, *(K + "apt").split("/"))))
assert len(APT) == 96 and all(f.endswith(".webp") for f in APT), len(APT)
FILES = [W + "cockpit.js", K + "cockpit.json"] + [K + "apt/" + f for f in APT]
NEWFILES = set(K + "apt/" + f for f in APT)
for r in (W + "cockpit.js", K + "cockpit.json"):
    assert b"\r\n" not in open(os.path.join(PLUG, *r.split("/")), "rb").read(), "CRLF " + r
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
o = subprocess.run(["node", "--check", os.path.join(PLUG, *(W + "cockpit.js").split("/"))], capture_output=True, text=True)
assert o.returncode == 0, o.stderr[-300:]
ck = open(os.path.join(PLUG, *(W + "cockpit.js").split("/")), encoding="utf-8").read()
assert "function insideOf(c)" in ck and "inside: () => scrInside(c)" in ck and "sub.pano = 0;" in ck and "/tour/designer/" not in ck
cj = json.load(open(os.path.join(PLUG, *(K + "cockpit.json").split("/")), encoding="utf-8"))
assert len(cj["inside"]) == 48 and all(K + x["img"] in NEWFILES and K + x["card"] in NEWFILES for x in cj["inside"])
# the data the live cockpit reads must be the 1.72.636 file but for the new list and the build date
_g = subprocess.run(["git", "-C", REPO, "show", "66256053:plugins/nadlan-config/" + K + "cockpit.json"], capture_output=True)
assert _g.returncode == 0
_old = json.loads(_g.stdout.decode("utf-8"))
assert {k for k in set(_old) | set(cj) if _old.get(k) != cj.get(k)} == {"built", "inside"}, "cockpit.json changed more than the inside list"
rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first" % PREV
assert not any(k.startswith((W, K)) or k == "inc/project-stage.php" for k in (rp.get("files") or {})), "1.72.640 wrote a Kikar file"
r639 = json.load(open(os.path.join(QA, "deploy-result-639.json"), encoding="utf-8"))["files"]
r636 = json.load(open(os.path.join(QA, "deploy-result-636.json"), encoding="utf-8"))["files"]
assert W + "cockpit.js" in r639 and K + "cockpit.json" in r636
print("[%d] released and wrote no Kikar file | %d files, %d new (%d KB)" % (PREV, len(FILES), len(NEWFILES),
      sum(os.path.getsize(os.path.join(PLUG, *r.split("/"))) for r in NEWFILES) // 1024))

src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
_m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
assert _m and _m.group(1) == "ashira_640", "no PX import"
AP = open(os.path.join(H, "ashira_640.py"), encoding="utf-8").read()
assert "\nRELS = []" in AP and "raise SystemExit('ashira_640: no hunk on ' + rel)" in AP, "ashira_640.py is not the no-hunk module"
AP = AP.replace("ashira_640", "kikar_641").replace("Release 1.72.640 (HAD-684 lead mail + contact)", "Release 1.72.641 (HAD-710, the Kikar living room in 360 from every apartment)").replace("make_deploy640.py", "make_deploy641.py")
open(os.path.join(H, "kikar_641.py"), "w", encoding="utf-8", newline="\n").write(AP)

P, N = str(PREV), str(NEWV)
assert src.count('WANT_LIVE = "1.72.639"') == 1, "deploy640.py is not built on 1.72.639"
src = src.replace('WANT_LIVE = "1.72.639"', 'WANT_LIVE = "@@WANT@@"')
for a, b in [("1.72." + P, "1.72." + N), ("ps" + P, "ps" + N), ("bak" + P, "bak" + N), ("make_deploy" + P, "make_deploy" + N),
             ("deploy-result-" + P, "deploy-result-" + N), ("speed-" + P, "speed-" + N), ("posts-before-" + P, "posts-before-" + N),
             ("deploy-result-639", "deploy-result-" + P)]:
    src = src.replace(a, b)
src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.%s"' % P)
BS = chr(92)
src = re.sub(r"\?t" + P + r"([a-z]*)=1", "?t" + N + BS + "1=1", src)
src = re.sub(r"&t" + P + r"([a-z]*)=1", "&t" + N + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(%s, 329, -1)" % P, src); assert n == 1, n
src, n = re.subn(r"^    import ashira_640 as PX  # noqa: E402 \(.*$", "    import kikar_641 as PX  # noqa: E402 (1.72.641: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.641 LIVE: [^"]*"\)', 'print("RELEASE 1.72.641 LIVE: the living room in 360 from every Kikar apartment, with its own window view")', src); assert n == 1, n
A = "/wp-content/plugins/nadlan-config/" + K
ROWS = ("    ('" + A + "cockpit.json?t641j=1', ['\"inside\":[{\"tower\":\"A\",\"floor\":10,\"bearing\":17.4,\"img\":\"apt/A10-0.webp\"', '\"card\":\"apt/C38-90-card.webp\"', '\"deals\":['], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/" + W + "cockpit.js?t641c=1', ['function insideOf(c)', \"[['הדירה הזאת', 0]]\", 'sub.pano = 0;'], [], ['/tour/designer/']),\n"
        "    ('" + A + "apt/B20-90.webp?t641a=1', [], []),\n"
        "    ('" + A + "apt/C38-270-card.webp?t641a=1', [], []),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
assert src.count("int(m.group(3)) + 1}") == 1, "the version bump is not +1 in deploy640.py"
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = " + repr(NEWFILES) + "  # 1.72.641: the 48 living rooms in 360 and their cards are new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.641: no hunked PHP; nadlan-config.php is restored from .bak641 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_640 as PX" not in src and ("t" + P + "p=1") not in src and ("t" + P + "b=1") not in src
assert src.count('WANT_LIVE = "1.72.640"') == 1 and src.count('BAK = ".bak641"') == 1 and src.count("range(640, 329, -1)") == 1
assert src.count('if new != "1.72.641":') == 1
open(os.path.join(H, "deploy641.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy641.py + kikar_641.py written | 2 swaps + %d new pictures | 4 new check rows" % len(NEWFILES))
