# -*- coding: utf-8 -*-
"""Generates scripts/project-stage/deploy375.py (release 1.72.375, Kikar Hamedina P9c, design system v104.2) from the runner of the
release right before it (deploy374.py, the main session's v104.4): the same safety chain (health, a token-gated one-run REST
bridge, drift checks against the LAST deploy-result that wrote each file, 374 first, then 373, 372 ... else 65af09be, never the
branch HEAD, .bak375 backups, MD5-verified writes, page checks, the served files byte for byte, automatic rollback, the resilient
record, the bridge always down), with no post written, plus:

  the example apartment in the world (v104.2):
    - inc/project-stage.php: the release copy = the text the last release wrote (1.72.371's, md5 ab944286; 372, 373 and 374 do
      not write it) + hamedina_ps_patch375.py's hunks (the 'examples' config and the world's page config, the mount's option and
      the analytics line, AccessibleCorner, the Arabic phone lane); ps_identity_proof375.py: the eight stage pages byte for byte;
    - assets/project-stage/tour.js and tour.css: the live text (1.72.361's) + an additive language option (o.lang, o.dir,
      o.errorText; the fleet's viewer unchanged without them): checked here by taking the hunk out again and landing on the md5
      the last release recorded;
    - NEW: assets/project-stage/world/example.js and example.css (the album, loaded on the press), and
      assets/project-stage/hamedina/tour/ (examples.json + 31 pictures, cut by scripts/interior/cut_kikar_tour.py);
    - NOT written: world/world.js and world.css. The main session's releases (373, 374) wrote them with the example hooks already
      in (inert until this release puts 'examples' in the page config); before any write the runner reads the served world.js
      for those hooks, and the checks read it again after.

Every file is pinned by MD5 here; if any changes, the runner stops until this generator is run again. The runner refuses unless
the live version is WANT_LIVE (1.72.374 by default), its record says "released and verified", and every drift check holds. The
agent that prepares it never runs it (not even --dry: a dry run opens the bridge on the live site).

  python scripts/project-stage/gen_deploy375.py                 (after 1.72.374 is live: needs deploy-result-374.json, released)
  python scripts/project-stage/gen_deploy375.py --template      (before that: pinned against the record as it stands; re-run after)
  python scripts/project-stage/gen_deploy375.py --want-live 1.72.374 --ps-base FILE   (another base text for inc/project-stage.php)
"""
import ast, glob, hashlib, io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
sys.path.insert(0, HERE)
import hamedina_ps_patch375 as PC  # noqa: E402

ARGS = sys.argv[1:]
TEMPLATE = "--template" in ARGS
WANT_LIVE = ARGS[ARGS.index("--want-live") + 1] if "--want-live" in ARGS else "1.72.374"
SN = WANT_LIVE.split(".")[-1]
V = f"1.72.{int(SN) + 1}"
VN = V.split(".")[-1]
if V != "1.72.375":
    raise SystemExit(f"FATAL generator: this generator writes 1.72.375 (after {WANT_LIVE} it would be {V}); make a new one")
SRC_PATH = os.path.join(HERE, f"deploy{SN}.py")  # the runner of the release right before: its checks carry every page's markers
if not os.path.exists(SRC_PATH):
    raise SystemExit(f"FATAL: no {os.path.basename(SRC_PATH)}: generate the {WANT_LIVE} runner first")
SRC = io.open(SRC_PATH, encoding="utf-8").read()
if f"BAK = \".bak{SN}\"" not in SRC:
    raise SystemExit(f"FATAL: {os.path.basename(SRC_PATH)} is not the {WANT_LIVE} runner (no .bak{SN})")
OUT = os.path.join(HERE, f"deploy{VN}.py")
A = "/wp-content/plugins/nadlan-config/assets/project-stage/"
TOUR_DIR = "assets/project-stage/hamedina/tour"
CHANGED = ["inc/project-stage.php", "assets/project-stage/tour.js", "assets/project-stage/tour.css"]
NEW_CODE = ["assets/project-stage/world/example.js", "assets/project-stage/world/example.css"]
NEW_TOUR = sorted(TOUR_DIR + "/" + os.path.basename(f) for f in glob.glob(os.path.join(PLUG, *TOUR_DIR.split("/"), "*")) if f.endswith((".jpg", ".webp", ".json")))
NEWFILES = NEW_CODE + NEW_TOUR
FILES = CHANGED + NEWFILES
WORLD_HOOKS = ["function openExampleApt(", "examples: null,", "exampleHtml()", "exampleTod(k);", "bindExample();"]  # shipped inert in 373
# tour.js / tour.css: the additive hunk (LF here; the files are CRLF like the live ones)
TOUR_HUNKS = {
    "assets/project-stage/tour.js": [("""  root.dir = 'rtl';
  root.lang = 'he';
""", """  // P9c (design system v104.2): a language page's viewer speaks its language (o.lang, o.dir, o.errorText); without them it is
  // the fleet's Hebrew viewer, exactly as before
  root.dir = o.dir === 'ltr' ? 'ltr' : 'rtl';
  root.lang = o.lang || 'he';
  if (o.errorText) root.dataset.err = o.errorText;
""")],
    "assets/project-stage/tour.css": [("""@media (prefers-reduced-motion: reduce) { .nlat-viewer__hint { transition: none; } }
""", """.nlat-viewer[data-err].is-error .nlat-viewer__stage::after { content: attr(data-err); } /* P9c: a language page's own words */
@media (prefers-reduced-motion: reduce) { .nlat-viewer__hint { transition: none; } }
""")],
}


def md5(b):
    return hashlib.md5(b).hexdigest()


def must_replace(text, old, new, n=1, label=""):
    c = text.count(old)
    if c != n:
        raise SystemExit(f"FATAL generator: {label or old[:70]!r} x{c} (want {n})")
    return text.replace(old, new)


def last_written(rel, top):
    """(release number, md5) of the last deploy-result at or below `top` whose "files" name `rel` (a rolled-back one has none)"""
    for n in range(top, 329, -1):
        p = os.path.join(QA, f"deploy-result-{n}.json")
        if os.path.exists(p):
            m = (json.load(open(p, encoding="utf-8")).get("files") or {}).get(rel)
            if m:
                return n, m
    return None, None


# ------------------------------------------------------------------------------------------------ the chain before this release
TOP = int(SN)
rtop = os.path.join(QA, f"deploy-result-{TOP}.json")
if os.path.exists(rtop):
    d = json.load(open(rtop, encoding="utf-8"))
    if d.get("released") != WANT_LIVE or "released and verified" not in str(d.get("state")):
        raise SystemExit(f"FATAL: deploy-result-{TOP}.json is '{d.get('state')}' for {d.get('released')}: {WANT_LIVE} is not released and verified")
    print(f"[chain] {WANT_LIVE}: released and verified; it wrote {sorted((d.get('files') or {}).keys())}")
elif not TEMPLATE:
    raise SystemExit(f"FATAL: no deploy-result-{TOP}.json: {WANT_LIVE} is not live yet. Run this after it, or pass --template to pin against the record as it stands")
else:
    print(f"[chain] TEMPLATE: no deploy-result-{TOP}.json yet; pinned against the records up to 1.72.{TOP - 1}. RE-RUN this generator once {WANT_LIVE} is live.")
for rel in FILES:  # nothing this release writes may have been written after 371 by someone else's release
    n, m = last_written(rel, TOP)
    if n is not None and n >= 372:
        raise SystemExit(f"FATAL: 1.72.{n} wrote {rel} ({m[:10]}); merge its text into this release's copy first")
wn, wm = last_written("assets/project-stage/world/world.js", TOP)
print(f"[chain] world.js last written by 1.72.{wn} ({wm[:10] if wm else '-'}); this release does not write it")

# ------------------------------------------------------------------------------------------------ gates before anything
for script in ("kikar_copy_gate.py", "ps_identity_proof375.py"):
    r = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True, encoding="utf-8")
    last = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:] or ["(no output)"]
    print(f"[gate] {script}: {last[0]}")
    if r.returncode:
        raise SystemExit(f"FATAL: {script} failed:\n{r.stdout[-1500:]}{r.stderr[-800:]}")

# ------------------------------------------------------------------------------------------------ inc/project-stage.php: base + hunks
psn, ps_base_md5 = last_written("inc/project-stage.php", TOP)
cands = {"hamedina_ps_patch375.live371()": PC.live371()}
if "--ps-base" in ARGS:
    f = ARGS[ARGS.index("--ps-base") + 1]
    cands["--ps-base " + f] = io.open(f, encoding="utf-8", newline="").read()
base = next(((k, v) for k, v in cands.items() if md5(v.encode("utf-8")) == ps_base_md5), None)
if not base:
    raise SystemExit(f"FATAL: no local text of inc/project-stage.php has the md5 1.72.{psn} recorded ({ps_base_md5}); pass --ps-base <file with that text>")
print(f"[base] inc/project-stage.php: 1.72.{psn} wrote {ps_base_md5[:10]} = {base[0]}")
release_ps = PC.release_text(base[1]).encode("utf-8")
branch_ps = io.open(os.path.join(PLUG, "inc", "project-stage.php"), encoding="utf-8", newline="").read()
if not all(PC.carries(branch_ps).values()):
    raise SystemExit("FATAL: the branch's inc/project-stage.php does not carry every P9c hunk (run hamedina_ps_patch375.py --branch)")
NEW = {"inc/project-stage.php": release_ps}

# ------------------------------------------------------------------------------------------------ tour.js / tour.css: live + the hunk only
for rel, hunks in TOUR_HUNKS.items():
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    if b"\r\n" not in b:
        raise SystemExit(f"FATAL: {rel} lost its CRLF line ends (the live file has them)")
    back = b.decode("utf-8")
    for old, new in hunks:
        o2, n2 = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
        if back.count(n2) != 1:
            raise SystemExit(f"FATAL: {rel} does not carry the P9c hunk once")
        back = back.replace(n2, o2)
    n, m = last_written(rel, TOP)
    if md5(back.encode("utf-8")) != m:
        raise SystemExit(f"FATAL: {rel} without the P9c hunk is {md5(back.encode('utf-8'))[:10]}, not what 1.72.{n} wrote ({m and m[:10]}): the branch carries other, unreleased changes")
    print(f"[base] {rel}: 1.72.{n} wrote {m[:10]}; the release = that + the P9c hunk")
    NEW[rel] = b
for rel in NEWFILES:
    NEW[rel] = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
PIN = {rel: md5(NEW[rel]) for rel in FILES}
PS_BASE = {"release": psn, "md5": ps_base_md5}

# lint and syntax
tmp = os.path.join(os.environ.get("TEMP", "."), f"ps{VN}-lint.php")
open(tmp, "wb").write(release_ps)
r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
os.unlink(tmp)
if r.returncode:
    raise SystemExit("FATAL: inc/project-stage.php (release) does not lint: " + r.stdout + r.stderr)
for rel in ("assets/project-stage/world/example.js", "assets/project-stage/tour.js"):
    tmp = os.path.join(os.environ.get("TEMP", "."), f"ps{VN}-" + os.path.basename(rel).replace(".js", ".mjs"))
    open(tmp, "wb").write(NEW[rel])
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode:
        raise SystemExit(f"FATAL: node --check {rel}: {r.stderr[:400]}")
man = json.loads(NEW[TOUR_DIR + "/examples.json"].decode("utf-8"))
need_files = set()
for ex in man["examples"]:
    for s in ex["stills"]:
        need_files |= {s["base"] + x for x in ("-2k.webp", "-card.jpg", "-card.webp", "-thumb.webp")}
    for w in ex["twist"]:
        need_files |= {w["base"] + x for x in ("-card.jpg", "-card.webp", "-thumb.webp")}
    need_files |= {ex["pano"]["base"] + x for x in (".jpg", ".webp", "-2k.jpg", "-2k.webp", "-card.jpg", "-thumb.webp")}
have = {os.path.basename(f) for f in NEW_TOUR}
if not need_files <= have:
    raise SystemExit(f"FATAL: examples.json names files that are not there: {sorted(need_files - have)}")
TOUR_BYTES = sum(len(NEW[r]) for r in NEW_TOUR)
print(f"[assets] {len(NEW_TOUR)} tour files ({TOUR_BYTES // 1024} KB on disk), every file examples.json names is there")

t = SRC
# ------------------------------------------------------------------------------------------------ header and names
doc_end = t.index('"""', 3) + 3
t = f'''"""Release {V} (P9c of the Kikar Hamedina loop, HAD-375, design system v104.2): the example apartment inside the world
("היכנסו לדירה לדוגמה": the album and the 360 in the fleet's viewer, pictures loaded only on the press), the Arabic phone's first
screen (a lane above the buttons) and the accessibility button's corner on the world pages. GENERATED by gen_deploy{VN}.py from
deploy{SN}.py; do not edit by hand: change the sources and run the generator again (every file is pinned by MD5).

Writes: inc/project-stage.php (what 1.72.371 wrote + hamedina_ps_patch375.py's hunks; every other page byte for byte the same, see
ps_identity_proof375.py), assets/project-stage/tour.js and tour.css (the live text + an additive language option),
NEW assets/project-stage/world/example.js and example.css, NEW assets/project-stage/hamedina/tour/ (examples.json + the pictures),
nadlan-config.php (the version, on the live text). No post, no meta. world.js / world.css are NOT written (the main session's
releases wrote them with the example hooks). Rolls back on any failed check: the changed files from .bak{VN}, the new files
removed. The record deploy-result-{VN}.json is written as soon as the files are written.

  python scripts/project-stage/deploy{VN}.py [--dry | --rollback]
"""''' + t[doc_end:]
t = must_replace(t, f'BAK = ".bak{SN}"', f'BAK = ".bak{VN}"')
t = must_replace(t, f"NadLan-PS{SN}/1.0", f"NadLan-PS{VN}/1.0")
t = must_replace(t, f"NS = 'nadlan-ps{SN}-'", f"NS = 'nadlan-ps{VN}-'")
t = must_replace(t, 'f"x-tmp-ps' + SN + '-ops-{int(time.time())}"', 'f"x-tmp-ps' + VN + '-ops-{int(time.time())}"')
t, _nk = re.subn(r"\t\t\t\$kh_write = array\([^;]*\);[^\n]*", lambda m: f"\t\t\t$kh_write = array(); // {V} writes files only (no post)", t)
if _nk != 1:
    raise SystemExit(f"FATAL generator: the bridge's post list x{_nk}")

# ------------------------------------------------------------------------------------------------ the checks
cs, ce = t.index("CHECKS = ["), t.index("H1_EXACTLY_ONE = [")
checks = t[cs:ce]
old_kh, kept = {}, []
for line in checks.split("\n"):
    if line.startswith(("    ('/projects/hamedina", "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/",
                        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/hamedina/")):
        tup = ast.literal_eval(line.strip().rstrip(","))
        old_kh[tup[0]] = tup
        continue
    kept.append(line)
if len(old_kh) != 10:
    raise SystemExit(f"FATAL generator: expected the 10 Kikar lines of {SN}'s CHECKS, found {len(old_kh)}: {list(old_kh)}")
n_ver = "\n".join(kept).count(WANT_LIVE)
checks = "\n".join(kept).replace(WANT_LIVE, V)
up = lambda xs: [x.replace(WANT_LIVE, V) for x in xs]
KH_EX = [f"hamedina\\/tour\\/examples.json?ver={V}", "&quot;id&quot;:&quot;c30w&quot;", "examples: c.examples || null", "AccessibleCorner",
         "ga('stage_example'", PC.AR_LANE]
new_checks = []
for slug in ("hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar"):
    p0 = f"/projects/{slug}/"
    tup = old_kh[p0]
    new_checks.append((p0, up(tup[1]) + KH_EX, list(tup[2]), list(tup[3]) if len(tup) > 3 else []))
for key in (f"{A}world/world.js?ver={WANT_LIVE}", f"{A}world/world.css?ver={WANT_LIVE}", f"{A}hamedina/world.json?ver={WANT_LIVE}",
            f"{A}hamedina/places.json?ver={WANT_LIVE}", f"{A}hamedina/world-i18n.json?ver={WANT_LIVE}"):
    tup = old_kh[key]
    need = up(tup[1]) + (WORLD_HOOKS if "world/world.js" in key else [".nlw-btn--ex", ".nlw-exlink"] if "world/world.css" in key else [])
    new_checks.append((key.replace(WANT_LIVE, V), need, list(tup[2]), list(tup[3]) if len(tup) > 3 else []))
new_checks += [
    (f"{A}world/example.js?ver={V}", ["export function openExample(", "התוכנית להמחשה, חלוקת הדירות לא פורסמה", "../tour.js", "window.__nlExample"], [], []),
    (f"{A}world/example.css?ver={V}", [".nlex__go360", "html.nlex-open"], [], []),
    (f"{A}hamedina/tour/examples.json?ver={V}", ['"id": "c30w"', '"living360-c30w-sunset"'], [], []),
    (f"{A}tour.js?ver={V}", ["root.dataset.err = o.errorText", "root.lang = o.lang || 'he';", "BuildingWalk v96"], [], []),
    (f"{A}tour.css?ver={V}", ["content: attr(data-err)", ".nlat-door {"], [], []),
]
body = "".join("    (%r, %r, %r, %r),\n" % c for c in new_checks)
checks = checks.rstrip()
if not checks.endswith("]"):
    raise SystemExit("FATAL generator: CHECKS does not end with ]")
checks = checks[:-1] + body + "]\n"
t = t[:cs] + checks + "\n" + t[ce:]
t = must_replace(t, f'print("[rollback] restoring .bak{SN} files")', f'print("[rollback] restoring .bak{VN} files")')

# ------------------------------------------------------------------------------------------------ main
ms = t.index("# ---------------------------------------------------------------- main")
MAIN = r'''# ---------------------------------------------------------------- main (__V__: Kikar Hamedina P9c, design system v104.2)
import signal  # noqa: E402
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage"))
import hamedina_ps_patch375 as PC  # noqa: E402  the release copy of inc/project-stage.php = the base below + the P9c hunks

WANT_LIVE = "__WANT__"  # the checks name ?ver=__V__: this runner is for the release right after __WANT__
TEMPLATE_PINNED = __TEMPLATE__  # True: generated before __WANT__ was live; the drift checks below still decide at run time
PIN = __PIN__
PS_BASE = __PS_BASE__  # the release that last wrote inc/project-stage.php and its md5: the base of the release copy
WORLD_HOOKS = __WORLD_HOOKS__  # what the live world.js must carry (the main session's releases ship them inert)
NEWFILES = set(__NEWFILES__)
FILES = __FILES__
RESULT = os.path.join(QA, "deploy-result-__VN__.json")
TOP = int(WANT_LIVE.split(".")[-1])


def last_written(rel):
    for n in range(TOP, 329, -1):  # the last release that wrote the file (a rolled-back record has no "files"); else 65af09be
        p = os.path.join(QA, f"deploy-result-{n}.json")
        if os.path.exists(p):
            m = (json.load(open(p, encoding="utf-8")).get("files") or {}).get(rel)
            if m:
                return n, m
    return None, None


NEW = {}
_n, _m = last_written("inc/project-stage.php")
if [_n, _m] != [PS_BASE["release"], PS_BASE["md5"]]:
    raise SystemExit(f"FATAL: inc/project-stage.php was last written by 1.72.{_n} ({_m}), not the base this runner was generated on {PS_BASE}; run gen_deploy__VN__.py again")
if PS_BASE["md5"] != PC.LIVE_371_MD5:
    raise SystemExit("FATAL: the base of inc/project-stage.php is not 1.72.371's text; run gen_deploy__VN__.py again (with --ps-base)")
NEW["inc/project-stage.php"] = PC.release_text(PC.live371()).encode("utf-8")
for rel in FILES[1:]:
    NEW[rel] = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
for rel in FILES:
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy__VN__.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
if not all(PC.carries(open(os.path.join(PLUG, "inc", "project-stage.php"), encoding="utf-8").read()).values()):
    raise SystemExit("FATAL: the branch's inc/project-stage.php lacks the P9c hunks the release writes")
php_lint(NEW["inc/project-stage.php"], "inc/project-stage.php")
HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES if rel not in NEWFILES}
os.makedirs(os.path.join(QA, "live-backup"), exist_ok=True)


def _stop(signum, frame):  # a stop from outside (the shell's timeout, a console break): the finally still runs
    raise KeyboardInterrupt(f"signal {signum}")


for _sg in ("SIGTERM", "SIGBREAK"):
    if hasattr(signal, _sg):
        try:
            signal.signal(getattr(signal, _sg), _stop)
        except Exception:
            pass


def sweep(when):
    """every temporary release bridge (x-tmp-*-ops-*) still on the site is switched off and deleted (bridge_sweep.py's rule)"""
    s, lst = snip("GET", "")
    rows = [x for x in (lst if s == 200 and isinstance(lst, list) else []) if re.match(r"x-tmp-[a-z0-9]+-ops-", str(x.get("name", ""))) and x.get("active")]
    if BR is not None:
        rows = [x for x in rows if x.get("id") != BR or when == "end"]
    for x in rows:
        a = snip("PUT", f"/{x['id']}/deactivate", {})[0]
        d = snip("DELETE", f"/{x['id']}", None)[0]
        print(f"[sweep {when}] active bridge {x['id']} {x['name']}: deactivate {a}, delete {d}")
    if not rows:
        print(f"[sweep {when}] no active temporary bridge left (http {s})")


REC = {}


def record(state, **extra):
    """deploy-result-__VN__.json, written at once and then updated: a run stopped from outside never loses what it wrote.
    A rolled-back run keeps its record with an empty "files" (the next runner's drift check then looks further back)."""
    REC.update({"released": REC.get("released"), "from": REC.get("from"), "state": state, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    REC.update(extra)
    tmp = RESULT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(REC, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, RESULT)
    print(f"[record] {os.path.basename(RESULT)}: {state}")


def served_exact(tag):
    """each written asset as the site serves it to a page (?ver=__V__), byte for byte the pinned file (the PHP is checked by its pages)"""
    ok = True
    for rel in FILES:
        if rel.endswith(".php"):
            continue
        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=__V__&nlv=" + tag
        try:
            s, b = req("GET", path, raw=True, auth=False, timeout=90)
        except Exception as e:
            s, b = str(e)[:60], b""
        good = s == 200 and md5(b) == PIN[rel]
        if not good or not rel.startswith("assets/project-stage/hamedina/tour/"):
            print(f"[served] {'OK ' if good else 'BAD'} {s} {rel}: {md5(b)[:10] if b else '-'} (want {PIN[rel][:10]})")
        ok = ok and good
    print(f"[served] {'all' if ok else 'NOT all'} {len([r for r in FILES if not r.endswith('.php')])} assets byte for byte")
    return ok


def run_checks(tag):
    bad = verify_pages("ps__VN__" + tag + str(int(time.time())))
    if not bad and not served_exact("ps__VN__s" + tag + str(int(time.time()))):
        bad = ["served-files"]
    if not bad and not verify_order("ps__VN__o" + tag + str(int(time.time()))):
        bad = ["order"]
    if not bad and not verify_home_order("ps__VN__h" + tag + str(int(time.time()))):
        bad = ["home-order"]
    if not bad and not verify_kh("ps__VN__k" + tag + str(int(time.time()))):
        bad = ["kikar-hamedina"]
    return bad


created = False
try:
    sweep("start")
    bridge_up()
    before = {}
    if "--rollback" in ARGS:
        rollback(True)
        wait_version(LIVE_VER)
        if os.path.exists(RESULT):
            REC.update(json.load(open(RESULT, encoding="utf-8")))
            REC["rolled_back_files"] = REC.get("files") or REC.get("rolled_back_files") or {}
            record("rolled back (--rollback)", files={})
        raise SystemExit(0)
    if LIVE_VER != WANT_LIVE:
        raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> __V__ (its checks name the version); regenerate it")
    _r = os.path.join(QA, f"deploy-result-{TOP}.json")
    if not os.path.exists(_r) or "released and verified" not in str(json.load(open(_r, encoding="utf-8")).get("state")):
        raise SystemExit(f"FATAL: deploy-result-{TOP}.json is missing or not 'released and verified'; this release chains after it")

    LIVE = {}
    for rel in FILES:
        cur = live_get(rel)
        if rel in NEWFILES:
            if not cur.get("missing"):
                raise SystemExit(f"FATAL: {rel} already exists on the server; this release creates it: diff it first")
            LIVE[rel] = None
            continue
        if cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + rel)
        LIVE[rel] = base64.b64decode(cur["b64"])
        n, prev = last_written(rel)
        print(f"[drift] live {rel} {md5(LIVE[rel])[:10]}; last written by 1.72.{n}: {prev[:10] if prev else '-'}")
        if prev:
            if md5(LIVE[rel]) != prev:
                raise SystemExit(f"FATAL: live {rel} is not what the last release wrote; diff it before replacing it")
        elif HEAD[rel] is None or LIVE[rel].replace(CRLF, LF) != HEAD[rel].replace(CRLF, LF):
            raise SystemExit(f"FATAL: live {rel} differs from 65af09be; diff it before replacing it")
    # the world module this release plugs into: the live world.js, as the site serves it, must carry the example hooks
    _s, _wj = req("GET", "/wp-content/plugins/nadlan-config/assets/project-stage/world/world.js?ver=" + WANT_LIVE + "&nlv=pre__VN__" + str(int(time.time())), raw=True, auth=False, timeout=90)
    _miss = [h for h in WORLD_HOOKS if h.encode("utf-8") not in (_wj or b"")]
    print(f"[world] the served world.js ({WANT_LIVE}): http {_s}, example hooks {'all there' if not _miss else 'MISSING ' + str(_miss)}")
    if _s != 200 or _miss:
        raise SystemExit("FATAL: the live world.js lacks the example hooks this release needs; the world module must ship them first")
    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])
    stamp = time.strftime("%Y%m%dT%H%M%S")
    if not DRY:
        for rel in FILES:
            if LIVE[rel] is not None:
                open(os.path.join(QA, "live-backup", rel.split("/")[-1] + f".{stamp}.live"), "wb").write(LIVE[rel])
        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)

    # the version bump, on the live text
    text = live_main.decode("utf-8")
    m = re.search(r"\* Version: (\d+)\.(\d+)\.(\d+)", text)
    old = ".".join(m.groups())
    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
    if new != "__V__":
        raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not __V__")
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    if text.count("'project-stage', 'together'") != 1:
        raise SystemExit("FATAL: the live module list lost 'project-stage', 'together'")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; writing {len(FILES)} files ({len(NEWFILES)} new): {', '.join(f for f in FILES if not f.startswith('assets/project-stage/hamedina/tour/'))} + hamedina/tour/ ({len([f for f in FILES if f.startswith('assets/project-stage/hamedina/tour/')])} files)")
    print("[plan] no post, no meta; world.js / world.css are not written (the live ones carry the example hooks)")
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    REC.update({"released": new, "from": old, "live_before": dict({rel: (md5(LIVE[rel]) if LIVE[rel] is not None else "missing") for rel in FILES}, **{"nadlan-config.php": md5(live_main)})})
    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})
    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect=("missing" if LIVE[rel] is None else md5(LIVE[rel])))
        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("written, checks pending", files=FILES_MD5)
    except BaseException as e:  # a write refused half way (drift, lint, md5, a stop from outside): put everything back
        print("[FAIL] during writes:", e)
        rollback(created)
        if REC.get("released"):
            record("rolled back during the writes: " + str(e)[:200], files={}, rolled_back_files=FILES_MD5)
        raise
    print("[purge]", ops({"purge": 1}, "purge"))

    healthy = wait_version(new)
    bad = run_checks("a") if healthy else ["health"]
    after = speed("after") if healthy else {}
    if bad:
        print("[checks] first round:", bad, "- purge and look again")
        ops({"purge": 1}, "purge again")
        time.sleep(12)
        healthy = wait_version(new, 45)
        bad = run_checks("b") if healthy else ["health"]
    if bad:
        print("[FAIL] pages:", bad)
        rollback(created)
        wait_version(old, 60)
        record("rolled back after the checks: " + ", ".join(bad), files={}, rolled_back_files=FILES_MD5)
        raise SystemExit("ROLLED BACK")
    record("released and verified", files=FILES_MD5,
           checks="verify_pages (+ the example hooks in the served world.js) + served_exact (every asset at ?ver=__V__, byte for byte) + verify_order + verify_home_order + verify_kh: OK")
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-__VN__.json"), "w", encoding="utf-8"), indent=2)
    print("RELEASE __V__ LIVE: https://nad-lan.co.il/projects/hamedina/ (+ -en, -fr, -ru, -ar): the floor view's example apartment")
    print("NEXT (read-only, a real browser): python scripts/project-stage/kh_first_screen_check.py ; live eyes: tower C, floor 30, west -> the button -> the album -> the 360")


finally:
    try:
        bridge_down()
    except BaseException as e:
        print("[bridge] down failed:", e)
    try:
        sweep("end")
    except BaseException as e:
        print("[sweep end] failed:", e)
'''
MAIN = (MAIN.replace("__PIN__", json.dumps(PIN, indent=4)).replace("__FILES__", json.dumps(FILES)).replace("__NEWFILES__", json.dumps(NEWFILES))
        .replace("__PS_BASE__", json.dumps(PS_BASE)).replace("__WORLD_HOOKS__", json.dumps(WORLD_HOOKS)).replace("__WANT__", WANT_LIVE)
        .replace("__TEMPLATE__", "True" if TEMPLATE and not os.path.exists(rtop) else "False").replace("__VN__", VN).replace("__V__", V))
t = t[:ms] + MAIN
io.open(OUT, "w", encoding="utf-8", newline="\n").write(t)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit(f"FATAL: deploy{VN}.py does not compile: " + r.stderr)
bs = t.index("BRIDGE = r'''") + len("BRIDGE = r'''")
bridge_php = "<?php\n" + t[bs:t.index("'''", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", f".bak{VN}").replace("__NS__", f"nadlan-ps{VN}-xxxxxxxx")
tmp = os.path.join(os.environ.get("TEMP", "."), f"bridge{VN}-lint.php")
open(tmp, "w", encoding="utf-8").write(bridge_php)
r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
os.unlink(tmp)
if r.returncode:
    raise SystemExit("FATAL: the bridge PHP does not lint: " + r.stdout + r.stderr)
print("wrote", OUT, "|", len(t), "chars | pinned", len(PIN), f"files ({len(NEWFILES)} new) | WANT_LIVE {WANT_LIVE}{' (TEMPLATE: re-run after it is live)' if TEMPLATE and not os.path.exists(rtop) else ''}",
      f"| from {os.path.basename(SRC_PATH)} | CHECKS moved to {V} ({n_ver} names) + {len(new_checks)} Kikar / asset lines | bridge lint ok | py_compile ok")
for k in CHANGED + NEW_CODE:
    print(f"   {PIN[k]}  {k}")
print(f"   + {len(NEW_TOUR)} files in {TOUR_DIR}/ ({TOUR_BYTES // 1024} KB)")
