# -*- coding: utf-8 -*-
"""HAD-698 (10.11.2026): the catalog ItemList (snippet 661, nadlan_cp_schema) gets typed items. One statement changes: each
ListItem is built by nadlan_dir_itemlist_item() (inc/directory.php, from 1.72.639) when it exists, else exactly as before.
Safety: read the live code, the anchor must appear once, php -l locally, backup with md5, write, read back, then /projects/ and
/projects/page/2/ must answer 200 with valid JSON-LD; any failure writes the old code back.
python scripts/project-stage/snippet661_itemlist_698.py [--dry | --rollback <backup.json>]"""
import hashlib, io, json, os, re, subprocess, sys, tempfile, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-698", "snippet-661")
SID = 661
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "sn661il"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
snip = ns["snip"]
OLD = ("$i++; $it = array( '@type' => 'ListItem', 'position' => $i, 'url' => get_permalink( $p ), 'name' => get_the_title( $p ) );\n"
       "\t\t\t\t$img = get_the_post_thumbnail_url( $p, 'large' ); if ( $img ) { $it['image'] = $img; }\n"
       "\t\t\t\t$items[] = $it;")
NEW = ("$i++; if ( function_exists( 'nadlan_dir_itemlist_item' ) ) { $items[] = nadlan_dir_itemlist_item( $p->ID, $i ); continue; } // HAD-698: typed items\n"
       "\t\t\t\t$it = array( '@type' => 'ListItem', 'position' => $i, 'url' => get_permalink( $p ), 'name' => get_the_title( $p ) );\n"
       "\t\t\t\t$img = get_the_post_thumbnail_url( $p, 'large' ); if ( $img ) { $it['image'] = $img; }\n"
       "\t\t\t\t$items[] = $it;")
PHP = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
PHP = next((os.path.join(PHP, d, "php.exe") for d in sorted(os.listdir(PHP)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(PHP) else "php"


def page(p):
    u = "https://nad-lan.co.il" + p + ("&" if "?" in p else "?") + "nl698=" + str(int(time.time()))
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (site owner audit)"}), timeout=90) as f:
            return f.status, f.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


def ld_ok(h):
    for m in re.finditer(r'<script type="application/ld\+json" class="nlcp-schema">(.*?)</script>', h, re.S):
        d = json.loads(m.group(1))
        il = [g for g in d.get("@graph", []) if g.get("@type") == "ItemList"]
        return bool(il) and len(il[0].get("itemListElement", [])) > 0, il[0]["itemListElement"][0] if il else None
    return False, None


s, sn = snip("GET", "/%d" % SID, None)
if s != 200:
    raise SystemExit("FATAL read snippet: %s" % s)
code = sn["code"]
if "--rollback" in sys.argv:
    bk = json.load(io.open(sys.argv[sys.argv.index("--rollback") + 1], encoding="utf-8"))
    s, r = snip("PUT", "/%d" % SID, {"name": sn["name"], "code": bk["code"], "scope": sn["scope"], "active": True}); print("[rollback]", s); raise SystemExit(0)
if "nadlan_dir_itemlist_item" in code:
    raise SystemExit("already applied")
if code.count(OLD) != 1:
    i = code.find("$i++; $it = array( '@type' => 'ListItem'")
    raise SystemExit("FATAL anchor x%d; live text near it: %r" % (code.count(OLD), code[i:i + 300]))
new = code.replace(OLD, NEW)
with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as t:
    t.write("<?php\n" + new); tmp = t.name
o = subprocess.run([PHP, "-l", tmp], capture_output=True, text=True); os.unlink(tmp)
if o.returncode != 0:
    raise SystemExit("FATAL lint: " + o.stdout + o.stderr)
print("[lint] ok | old md5", hashlib.md5(code.encode()).hexdigest()[:10], "new", hashlib.md5(new.encode()).hexdigest()[:10])
if "--dry" in sys.argv:
    raise SystemExit(0)
os.makedirs(BK, exist_ok=True)
bkp = os.path.join(BK, "snippet-661-%s.json" % time.strftime("%Y%m%dT%H%M%S"))
io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": SID, "name": sn["name"], "code": code, "md5": hashlib.md5(code.encode()).hexdigest()}, ensure_ascii=False))
s, r = snip("PUT", "/%d" % SID, {"name": sn["name"], "code": new, "scope": sn["scope"], "active": True})
s2, back = snip("GET", "/%d" % SID, None)
ok = s == 200 and back.get("code") == new and back.get("active")
print("[write]", s, "| read-back identical and active:", ok, "| backup", os.path.relpath(bkp, REPO))
time.sleep(3)
bad = [] if ok else ["write"]
for p in ("/projects/", "/projects/page/2/"):
    st, h = page(p)
    good, first = ld_ok(h) if st == 200 else (False, None)
    good = good and "Fatal error" not in h
    print("[after]", "OK " if good else "BAD", st, p, json.dumps(first, ensure_ascii=False)[:300] if first else "")
    if not good:
        bad.append(p)
if bad:
    s, r = snip("PUT", "/%d" % SID, {"name": sn["name"], "code": code, "scope": sn["scope"], "active": True})
    raise SystemExit("ROLLED BACK (%s): %s" % (s, bad))
print("DONE")
