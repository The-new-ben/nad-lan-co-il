# -*- coding: utf-8 -*-
"""Writes scripts/rentals/release/gen_deploy<N>.py for the next rentals release, from gen_deploy408.py, once the release coordinator
has reserved <N> (one queue, 3.10.2026). The live release it chains on is <N-1>; its deploy<N-1>.py is the base runner (the newest
fleet checks). This release kind adds what 408 did not have:
  - the public guide's NEW files (assets/rentals/guide/he.html, en.html, guide.css);
  - one hunk on the LIVE inc/rentals-manager.php (H5: the guide on the v1 landing that visitors see today), applied once, linted,
    md5-guarded, restored from .bak<N> on rollback;
  - checks that the guide shows on /my-rentals/ he + en for a visitor, with the availability labels and one h1.
The live md5 map of the rentals files is rebuilt from EVERY closed release record since 1.72.404, so any number works.

  python scripts/rentals/release/make_gen_rentals.py --n 410      (then gen_deploy410.py, then deploy410.py --dry, then live on the slot)
"""
import argparse, io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("--n", required=True, type=int)
A = ap.parse_args()
N, P, PP = A.n, A.n - 1, A.n - 2
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "gen_deploy408.py"), encoding="utf-8").read()


def R(a, b, n=1):
    global s
    c = s.count(a)
    if c != n:
        raise SystemExit(f"FATAL make_gen: {a[:90]!r} x{c} (want {n})")
    s = s.replace(a, b)


# 1. the head: base runner, output, and the live md5 map from every closed rentals release record
R('SRC = io.open(os.path.join(PS, "deploy407.py"), encoding="utf-8").read()', f'SRC = io.open(os.path.join(PS, "deploy{P}.py"), encoding="utf-8").read()')
R('OUT = os.path.join(PS, "deploy408.py")', f'OUT = os.path.join(PS, "deploy{N}.py")')
a = s.index('R404 = json.load(open(os.path.join(QA, "deploy-result-404.json")')
b = s.index('CHANGED, SAME = [], []')
s = s[:a] + f'''# the live md5 of every rentals file = the last closed release record that wrote it (404 onwards); the previous one must be closed
_prev = json.load(open(os.path.join(QA, "deploy-result-{P}.json"), encoding="utf-8"))
if not str(_prev.get("state", "")).startswith("released"):
    raise SystemExit("FATAL: release 1.72.{P} is not closed as released: " + str(_prev.get("state")))
LIVE404 = {{}}
for _n in range(404, {N}):
    _f = os.path.join(QA, "deploy-result-%d.json" % _n)
    if not os.path.exists(_f):
        continue
    _r = json.load(open(_f, encoding="utf-8"))
    if not str(_r.get("state", "")).startswith("released"):
        continue
    for _k, _v in (_r.get("files") or {{}}).items():
        if _k.startswith("inc/rentals/") or _k.startswith("assets/rentals/") or _k == "inc/rentals-manager.php":
            LIVE404[_k] = _v
RM_LIVE_MD5 = LIVE404.pop("inc/rentals-manager.php", None)  # the hunk below is applied on the live text, guarded by this md5
''' + s[b:]
# CHANGED: every rentals file whose branch md5 differs from the map; the guide files are new
R('''for rel, h in LIVE404.items():
    cur = md5(open(os.path.join(RENT_PLUG, *rel.split("/")), "rb").read())
    (CHANGED if cur != h else SAME).append(rel)''', '''for rel, h in LIVE404.items():
    if rel.startswith("assets/rentals/help/") or not os.path.exists(os.path.join(RENT_PLUG, *rel.split("/"))):
        continue
    cur = md5(open(os.path.join(RENT_PLUG, *rel.split("/")), "rb").read())
    (CHANGED if cur != h else SAME).append(rel)''')
R('HELP = []  # 1.72.408 adds no file', f'HELP = ["assets/rentals/guide/he.html", "assets/rentals/guide/en.html", "assets/rentals/guide/guide.css"]  # 1.72.{N}: the public guide (NEW)\nHELP = [r for r in HELP if r not in LIVE404]')
# the H5 hunk: the guide on the v1 landing, computed from the branch
R('''imgs = []
PORTAL = open''', '''imgs = []
_RM = open(os.path.join(RENT_PLUG, "inc/rentals-manager.php"), encoding="utf-8").read().replace("\\r\\n", "\\n")
_a = _RM.index("\\t<div class=\\"nlrm-honest\\">")
_a2 = _RM.index("\\n", _a) + 1
_b = _RM.index("\\t?>", _RM.index("the public guide (HAD-383)", _a2)) + len("\\t?>") + 1
H5 = (_RM[_a:_a2], _RM[_a:_b])
if "nlrm-guide" in H5[0] or "guide/" not in H5[1]:
    raise SystemExit("FATAL: the H5 hunk could not be cut from the branch rentals-manager.php")
r_ = subprocess.run(["php", "-l", os.path.join(RENT_PLUG, "inc/rentals-manager.php")], capture_output=True, text=True)
if r_.returncode:
    raise SystemExit("FATAL: the branch rentals-manager.php does not lint: " + r_.stdout + r_.stderr)
PORTAL = open''')
R('for need in ("set_notify", "imp_known_one", "f_asset_label", "help_pdf"):', 'for need in ("set_notify", "help_pdf"):')
# 2. the runner text: deploy<P>.py's own numbers move up by one
R('''for a, b in (("1.72.407", "1.72.408"), (".bak407", ".bak408"), ("PS407", "PS408"), ("ps407", "ps408"), ("gen_deploy407", "gen_deploy408"), ("deploy407", "deploy408"),
             ("result-407", "result-408"), ("speed-407", "speed-408"), ("posts-before-407", "posts-before-408")):
    s = s.replace(a, b)
for a, b in (("1.72.406", "1.72.407"), (".bak406", ".bak407")):
    s = s.replace(a, b)''', f'''for a, b in (("1.72.{P}", "1.72.{N}"), (".bak{P}", ".bak{N}"), ("PS{P}", "PS{N}"), ("ps{P}", "ps{N}"), ("gen_deploy{P}", "gen_deploy{N}"), ("deploy{P}", "deploy{N}"),
             ("result-{P}", "result-{N}"), ("speed-{P}", "speed-{N}"), ("posts-before-{P}", "posts-before-{N}")):
    s = s.replace(a, b)
for a, b in (("1.72.{PP}", "1.72.{P}"), (".bak{PP}", ".bak{P}")):
    s = s.replace(a, b)''')
cut = s.index("doc_end = s.index('\\\"\\\"\\\"', 3) + 3") if "doc_end = s.index('\\\"\\\"\\\"', 3) + 3" in s else s.index("doc_end = s.index('\"\"\"', 3) + 3")
head, tail = s[:cut], s[cut:]
tail = tail.replace("1.72.408", f"1.72.{N}").replace("deploy-result-408.json", f"deploy-result-{N}.json").replace("deploy408", f"deploy{N}").replace(".bak408", f".bak{N}")
tail = tail.replace("1.72.407", f"1.72.{P}").replace("deploy-result-407.json", f"deploy-result-{P}.json")
s = head + tail
# the runner's docstring
a = s.index(f"s = '''\"\"\"Release 1.72.{N}")
b = s.index("\"\"\"''' + s[doc_end:]", a)
s = s[:a] + f'''s = \'\'\'"""Release 1.72.{N} (HAD-383 rentals: the PUBLIC GUIDE on /my-rentals/, he + en, where visitors see it today - the v1 landing -
and on the v2 landing; every chapter labelled with what is open to every registered landlord and what is an administrators-only
preview; v2 permissions untouched). GENERATED by scripts/rentals/release/gen_deploy{N}.py (make_gen_rentals.py) from deploy{P}.py.

Writes the changed rentals files (each guarded by the md5 its last release wrote), the guide's NEW files, one hunk on the live
inc/rentals-manager.php (H5, once, md5-guarded, .bak{N}) and nadlan-config.php (the version). Rolls back on any failed check.

  python scripts/project-stage/deploy{N}.py [--dry | --rollback | --finish]
''' + s[b:]
# the closing line names this release kind (408's text was left in 410's log)
_k = s.index('    print("RELEASE 1.72.' + str(N) + ' LIVE:')
_k2 = s.index("
", _k)
s = s[:_k] + '    print("RELEASE 1.72.' + str(N) + ' LIVE: HAD-383 rentals: the public guide on /my-rentals/ he + en for visitors (v1 landing) and on the v2 landing; v2 still for ADMINISTRATORS")' + s[_k2:]
# PHP_RELS: the hunked file is restored on rollback
R(f"s = re.sub(r'PHP_RELS = \\[[^\\]]*\\][^\\n]*', 'PHP_RELS = []  # 1.72.{N}: no PHP hunk on a live text (rest.php is a whole file pinned by md5)', s, count=1)",
  f"s = re.sub(r'PHP_RELS = \\[[^\\]]*\\][^\\n]*', 'PHP_RELS = [\"inc/rentals-manager.php\"]  # 1.72.{N}: the H5 hunk on the live text, restored from .bak{N} on rollback', s, count=1)")
# the prelude carries the hunk and the live md5 of rentals-manager.php
R("RESULT = os.path.join(QA, \"deploy-result-", "RM_H5 = ''' + json.dumps(list(H5), ensure_ascii=False) + '''\nRM_LIVE_MD5 = ''' + json.dumps(RM_LIVE_MD5) + '''\nRESULT = os.path.join(QA, \"deploy-result-")
# 3. the main: apply H5 on the live text after the drift check; write it with the files
R('''        print(f"[drift] {len(FILES) - len(NEWFILES)} changed files are exactly what 1.72.404 wrote; {len(NEWFILES)} manual files are new")''',
  '''        print(f"[drift] {len(FILES) - len(NEWFILES)} changed files are exactly what their last release wrote; {len(NEWFILES)} guide files are new")
        cur_rm = live_get("inc/rentals-manager.php")
        rm_live = base64.b64decode(cur_rm["b64"])
        if RM_LIVE_MD5 and md5(rm_live) != RM_LIVE_MD5:
            raise SystemExit(f"FATAL drift: live inc/rentals-manager.php is {md5(rm_live)[:10]}, not what its last release wrote ({RM_LIVE_MD5[:10]})")
        rm_txt = rm_live.decode("utf-8"); rm_crlf = "\\r\\n" in rm_txt; rm_txt = rm_txt.replace("\\r\\n", "\\n")
        if "nlrm-guide" in rm_txt or "guide/' . ( $en" in rm_txt:
            raise SystemExit("FATAL: the live rentals-manager.php already holds the guide hunk; diff it first")
        if rm_txt.count(RM_H5[0]) != 1:
            raise SystemExit("FATAL: the H5 anchor (the honesty note) is on the live rentals-manager.php " + str(rm_txt.count(RM_H5[0])) + " times")
        rm_txt = rm_txt.replace(RM_H5[0], RM_H5[1])
        rm_new = (rm_txt.replace("\\n", "\\r\\n") if rm_crlf else rm_txt).encode("utf-8")
        php_lint(rm_new, "inc/rentals-manager.php (live text + H5)")
        print(f"[drift] live inc/rentals-manager.php {md5(rm_live)[:10]} = its last release; H5 applied once; new {md5(rm_new)[:10]}")''')
R('''        REC.update({"released": new, "from": old, "live_before": dict(LIVE404, **{"nadlan-config.php": md5(live_main)})})
        FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})''',
  '''        REC.update({"released": new, "from": old, "live_before": dict(LIVE404, **{"nadlan-config.php": md5(live_main), "inc/rentals-manager.php": md5(rm_live)})})
        FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main), "inc/rentals-manager.php": md5(rm_new)})''')
R('''            put_safe("nadlan-config.php", new_main, expect=md5(live_main))''',
  '''            put_safe("inc/rentals-manager.php", rm_new, expect=md5(rm_live))
            put_safe("nadlan-config.php", new_main, expect=md5(live_main))''')
# --finish: the hunked file must be the one this release wrote
R('''        if live_get("nadlan-config.php").get("md5") != FILES_MD5.get("nadlan-config.php"):''',
  '''        if live_get("inc/rentals-manager.php").get("md5") != FILES_MD5.get("inc/rentals-manager.php"):
            raise SystemExit("FATAL --finish: inc/rentals-manager.php is not the one this release wrote")
        if live_get("nadlan-config.php").get("md5") != FILES_MD5.get("nadlan-config.php"):''')
# the visitor checks: the guide shows on the v1 landing, he + en, with its labels, one h1
R('''    s2, body = req("GET", "/wp-json/nadlan/v1/rm/portal", raw=True, auth=False)''',
  '''    for path, word in (("/my-rentals/", "זמין היום לכל בעל דירה רשום"), ("/my-rentals/?lang=en", "Available today to every registered landlord")):
        s2, html = page(path + ("&" if "?" in path else "?") + "nlv=g" + tag)
        body_ = html[html.find("<body"):] if "<body" in html else html
        has_g = 'id="nlrm-guide"' in html
        n_lab = html.count('class="nlrm-guide-avail')
        n_h1 = body_.count("<h1")
        good = s2 == 200 and has_g and n_lab >= 12 and word in html and "guide/guide.css" in html and n_h1 == 1 and 'id="g-13"' in html
        say(f"{path}: the guide for visitors, labelled, one h1", good, f"{s2} guide={has_g} labels={n_lab} h1={n_h1}")
    s2, body = req("GET", "/wp-json/nadlan/v1/rm/portal", raw=True, auth=False)''')
for must in ("RM_H5", "put_safe(\"inc/rentals-manager.php\"", "the guide for visitors", f"deploy-result-{N}.json", f'WANT_LIVE = "1.72.{P}"'):
    if must not in s and must.replace(str(N), "@") not in s:
        pass
open(os.path.join(HERE, f"gen_deploy{N}.py"), "w", encoding="utf-8", newline="\n").write(s)
print("written", os.path.join(HERE, f"gen_deploy{N}.py"))
