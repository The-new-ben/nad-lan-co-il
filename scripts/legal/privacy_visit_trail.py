# -*- coding: utf-8 -*-
"""The privacy policy paragraph for the visit trail (HAD-678, release 1.72.602), inserted ADDITIVELY into the live WordPress page /privacy/.

The block is docs/legal/privacy-visit-trail.html (a heading "מה נרשם בעמודי הפרויקטים" with the anchor #visit-trail, two Hebrew paragraphs, one
English paragraph in a Custom HTML block so the editor keeps lang="en" dir="ltr"). It goes right before the heading "כמה זמן הפרטים נשמרים"
(or, when that heading is not found exactly once, before "הזכויות שלכם"; neither: the script stops). Nothing on the page is removed or
reworded; the one other change is the date in the first line ("עודכן לאחרונה: 24.9.2026." -> today), which the policy itself promises
("כשהמדיניות משתנה, התאריך בראש העמוד מתעדכן"); --keep-date leaves the date alone.

The REST helper is `req` of scripts/skin-a/deployskin.py, taken from its source with ast (DATA_BLOB, dpapi_unprotect, req, must, BASE,
SECRETS_PATH, UA): importing that file would run the skin release itself. The app password is decrypted inside this process only and
never printed.

  python scripts/legal/privacy_visit_trail.py                 DRY (default): reads the live page (context=edit), prints the plan and a diff
                                                              summary, writes nothing
  python scripts/legal/privacy_visit_trail.py --go            writes: a backup of the live text first (docs/legal/backups/), then the page;
                                                              checks the saved text (md5) and the public page; puts the backup back if a
                                                              check fails; on success mirrors the live text into docs/legal/privacy.html
  python scripts/legal/privacy_visit_trail.py --from-file docs/legal/privacy.html --out <file>
                                                              OFFLINE: the same insertion on a local file (no network, no secrets)
Release order: after 1.72.602 is live and verified (the policy describes what the site does)."""
import ast, base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, sys, time, urllib.request, urllib.error, urllib.parse  # noqa: F401 (the helper's imports)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BLOCK_FILE = os.path.join(REPO, "docs", "legal", "privacy-visit-trail.html")
MIRROR = os.path.join(REPO, "docs", "legal", "privacy.html")
BACKUPS = os.path.join(REPO, "docs", "legal", "backups")
ARGS = sys.argv[1:]
GO = "--go" in ARGS
KEEP_DATE = "--keep-date" in ARGS
MARK = 'id="visit-trail"'
ANCHORS = ['<!-- wp:heading -->\n<h2 class="wp-block-heading">כמה זמן הפרטים נשמרים</h2>\n<!-- /wp:heading -->',
           '<!-- wp:heading -->\n<h2 class="wp-block-heading">הזכויות שלכם</h2>\n<!-- /wp:heading -->']
DATE_RE = re.compile(r"עודכן לאחרונה: \d{1,2}\.\d{1,2}\.\d{4}\.")
md5 = lambda s: hashlib.md5(s.encode("utf-8")).hexdigest()


def arg(name):
    return ARGS[ARGS.index(name) + 1] if name in ARGS and ARGS.index(name) + 1 < len(ARGS) else None


def block():
    b = io.open(BLOCK_FILE, encoding="utf-8").read().replace("\r\n", "\n").strip("\n")
    assert b.count(MARK) == 1 and "info@nad-lan.co.il" in b and "12 חודשים" in b and "30 יום" in b and "Global Privacy Control" in b and "Do Not Track" in b, "the block file is not the approved text"
    assert 'lang="en" dir="ltr"' in b and "12 months" in b and "30 days" in b, "the English paragraph is missing"
    assert not re.search("[–—]", b), "a long dash in the block"
    return b


def today():
    t = time.localtime()
    return f"{t.tm_mday}.{t.tm_mon}.{t.tm_year}"


def insert(raw):
    """(new text, report) or (None, why). Additive: the block before the anchor heading, the date line updated (unless --keep-date)."""
    nl = "\r\n" if "\r\n" in raw else "\n"
    t = raw.replace("\r\n", "\n")
    if MARK in t:
        return None, "already there: the page holds id=\"visit-trail\" (nothing to do)"
    a = next((x for x in ANCHORS if t.count(x) == 1), None)
    if a is None:
        return None, "no anchor: neither heading 'כמה זמן הפרטים נשמרים' nor 'הזכויות שלכם' is found exactly once; read the live page first"
    b = block()
    new = t.replace(a, b + "\n\n" + a, 1)
    rep = {"anchor": a.split(">")[2].split("<")[0], "added_chars": len(new) - len(t)}
    if not KEEP_DATE:
        m = DATE_RE.findall(new)
        if len(m) == 1:
            new = new.replace(m[0], f"עודכן לאחרונה: {today()}.", 1)
            rep["date"] = m[0] + " -> " + f"עודכן לאחרונה: {today()}."
        else:
            rep["date"] = f"not changed (the date line is found {len(m)} times)"
    # additive proof: every line of the old text is still there, in order
    old_lines = [x for x in t.split("\n") if x.strip()]
    new_lines = [x for x in new.split("\n") if x.strip()]
    it = iter(new_lines)
    kept = all(any(o == x or (DATE_RE.search(o) and DATE_RE.search(x)) for x in it) for o in old_lines)
    assert kept, "the insertion would remove or reorder a line; stopped"
    rep["lines"] = f"{len(old_lines)} -> {len(new_lines)} (every old line kept, in order)"
    return new.replace("\n", nl), rep


if arg("--from-file"):
    src = io.open(arg("--from-file"), encoding="utf-8").read()
    new, rep = insert(src)
    print("[offline]", json.dumps(rep, ensure_ascii=False) if new else rep)
    if new and arg("--out"):
        io.open(arg("--out"), "w", encoding="utf-8", newline="").write(new)
        print("[offline] written", arg("--out"), md5(new)[:10])
    sys.exit(0 if new else 1)

# ---------------------------------------------------------------- the REST helper of deployskin.py, without running that file
DS = os.path.join(REPO, "scripts", "skin-a", "deployskin.py")
_tree = ast.parse(io.open(DS, encoding="utf-8").read())
_keep = [n for n in _tree.body if (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in ("DATA_BLOB", "dpapi_unprotect", "req", "must"))
         or (isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id in ("BASE", "SECRETS_PATH", "UA") for x in n.targets))]
H = {"__name__": "deployskin_helpers", "base64": base64, "ctypes": ctypes, "json": json, "urllib": urllib}
exec(compile(ast.Module(body=_keep, type_ignores=[]), DS, "exec"), H)
for _k in ("DATA_BLOB", "dpapi_unprotect", "req", "must", "BASE", "SECRETS_PATH", "UA"):
    assert _k in H, "deployskin.py no longer defines " + _k
with open(H["SECRETS_PATH"], encoding="utf-8-sig") as _f:
    _sec = json.load(_f)
H["AUTH"] = "Basic " + base64.b64encode(f"{_sec['username']}:{H['dpapi_unprotect'](_sec['password_dpapi'])}".encode()).decode()
del _sec
req, must = H["req"], H["must"]


def live_page():
    s, p, _ = req("GET", "/wp-json/wp/v2/pages?slug=privacy&status=publish&context=edit&_fields=id,status,modified,link,content")
    rows = must(s, p, "read the privacy page")
    if not isinstance(rows, list) or len(rows) != 1:
        raise SystemExit(f"FATAL: {len(rows) if isinstance(rows, list) else rows} published pages with the slug privacy (want one)")
    r = rows[0]
    return r["id"], r["content"]["raw"], r["modified"], r["link"]


def public_ok(link, want_block):
    s, b, _ = req("GET", urllib.parse.urlparse(link).path + f"?nlv=pv{int(time.time())}", raw=True, auth=False, timeout=90)
    html = b.decode("utf-8", "replace") if isinstance(b, (bytes, bytearray)) else ""
    need = ["עוגיות ומדידה", "הזכויות שלכם", "info@nad-lan.co.il"] + (["מה נרשם בעמודי הפרויקטים", MARK, "Global Privacy Control", "12 months"] if want_block else [])
    miss = [x for x in need if x not in html]
    print(f"[public] {s} {link}: {'OK' if s == 200 and not miss else 'BAD missing ' + json.dumps(miss, ensure_ascii=False)}")
    return s == 200 and not miss



s, h, _ = req("GET", "/wp-json/nadlan/v1/health", auth=False)
print("[health]", s, h.get("version") if isinstance(h, dict) else h, h.get("status") if isinstance(h, dict) else "")
pid, raw, modified, link = live_page()
print(f"[live] page {pid} {link}, modified {modified}, {len(raw)} chars, md5 {md5(raw)[:10]}")
new, rep = insert(raw)
if new is None:
    print("[plan]", rep)
    sys.exit(0)
print("[plan]", json.dumps(rep, ensure_ascii=False))
print("[plan] the block:", len(block()), "chars from", os.path.relpath(BLOCK_FILE, REPO))
if not GO:
    print("[dry] nothing written (add --go to write; a backup of the live text is made first)")
    sys.exit(0)

os.makedirs(BACKUPS, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
bak = os.path.join(BACKUPS, f"privacy-page-{pid}.{stamp}.before-visit-trail.html")
io.open(bak, "w", encoding="utf-8", newline="").write(raw)
print("[backup]", os.path.relpath(bak, REPO), md5(raw)[:10])
s, p, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=id,content,modified", body={"content": new})
must(s, p, "write the privacy page")
saved = (p.get("content") or {}).get("raw", "") if isinstance(p, dict) else ""
good = md5(saved.replace("\r\n", "\n")) == md5(new.replace("\r\n", "\n"))
print(f"[write] page {pid}: http {s}, saved text {'= the planned text' if good else 'DIFFERS from the planned text'} ({md5(saved)[:10]})")
if good:
    time.sleep(3)
    good = public_ok(link, True)
if not good:
    s2, p2, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=id,content", body={"content": raw})
    back = isinstance(p2, dict) and md5(((p2.get("content") or {}).get("raw", "")).replace("\r\n", "\n")) == md5(raw.replace("\r\n", "\n"))
    print(f"[rollback] the live text put back: http {s2}, {'identical to the backup' if back else 'NOT identical: restore ' + os.path.relpath(bak, REPO) + ' by hand'}")
    raise SystemExit("FAILED: the privacy page is as it was" if back else "FAILED and the rollback did not verify")
io.open(MIRROR, "w", encoding="utf-8", newline="").write(saved)
print("[mirror]", os.path.relpath(MIRROR, REPO), "= the live text now")
print("PRIVACY POLICY UPDATED: the visit trail paragraph (he + en) is live at", link + "#visit-trail")
