#!/usr/bin/env python3
"""Create DRAFT nadlan_property posts (Hebrew) + the broker page draft from the Cowork package.
Drafts only. No publish path. CSS is inlined inside the Custom HTML block (no live code change).
Credentials: DPAPI-protected app password, decrypted in-process only, never printed."""
import base64, ctypes, ctypes.wintypes as wt, json, os, sys, urllib.request, urllib.error, urllib.parse, time

SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
PKG = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\aa08c3e7-cd8f-4254-9186-99468d8a8a08\scratchpad\meital\nadlan-meital-listings"
WP = "https://nad-lan.co.il"
APPLY = "--apply" in sys.argv
ONLY = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")]
ONLY = set(ONLY[0].split(",")) if ONLY else set()

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi_unprotect(b64):
    raw = base64.b64decode(b64)
    blob_in = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        raise RuntimeError("DPAPI decrypt failed")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)

with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi_unprotect(sec['password_dpapi'])}".encode()).decode()

def req(method, path, body=None, params=None):
    url = WP + "/wp-json" + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={"Authorization": AUTH, "Content-Type": "application/json; charset=utf-8", "User-Agent": "nadlan-runner"})
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "null")
        except Exception:
            return e.code, None

def rd(p):
    return open(os.path.join(PKG, p), encoding="utf-8").read()

# ---- preflight ----
st, me = req("GET", "/wp/v2/users/me", params={"context": "edit"})
caps = (me or {}).get("capabilities", {}) if st == 200 else {}
st2, opt = req("OPTIONS", "/wp/v2/nadlan_property")
meta_keys = set(((((opt or {}).get("schema") or {}).get("properties") or {}).get("meta") or {}).get("properties", {}).keys())
print(json.dumps({"user_ok": st == 200, "user_id": (me or {}).get("id"), "unfiltered_html": bool(caps.get("unfiltered_html")), "meta_keys": len(meta_keys)}, ensure_ascii=False))
if not caps.get("unfiltered_html"):
    sys.exit("STOP: user lacks unfiltered_html")

st, terms = req("GET", "/wp/v2/nadlan_city", params={"per_page": 100})
term_by_name = {t["name"]: t["id"] for t in (terms or []) if isinstance(t, dict)}

MAP_PATH = os.path.join(PKG, "data", "import-map.json")
imap = json.load(open(MAP_PATH, encoding="utf-8")) if os.path.exists(MAP_PATH) else {}
css_listing = rd("assets/nlx-prestige.css")
css_broker = rd("broker/nlb-broker.css")
idx = json.load(open(os.path.join(PKG, "data", "listings.json"), encoding="utf-8"))["listings"]
results = []

def inline_css(content, css):
    marker = "<!-- wp:html -->"
    assert content.startswith(marker), "content not wrapped"
    return marker + "\n<style>\n" + css + "\n</style>\n" + content[len(marker):]

for it in idx:
    if ONLY and it["id"] not in ONLY:
        continue
    p = json.load(open(os.path.join(PKG, "listings", it["id"], "wp-he.json"), encoding="utf-8"))
    assert p["status"] == "draft"
    content = inline_css(rd(f"listings/{it['id']}/{p['content_file']}"), css_listing)
    meta = {k: v for k, v in p["meta"].items() if v is not None and k in meta_keys}
    dropped = sorted(k for k, v in p["meta"].items() if v is not None and k not in meta_keys)
    ids = [term_by_name[n] for n in p["terms"]["nadlan_city"] if n in term_by_name]
    missing_terms = [n for n in p["terms"]["nadlan_city"] if n not in term_by_name]
    body = {"status": "draft", "title": p["title"], "slug": p["slug"], "content": content, "excerpt": p["excerpt"], "meta": meta}
    if ids:
        body["nadlan_city"] = ids
    key = f"{it['id']}-he"
    row = {"key": key, "title": p["title"], "slug": p["slug"], "chars": len(content), "dropped_meta": dropped, "missing_terms": missing_terms}
    if APPLY:
        path = f"/wp/v2/nadlan_property/{imap[key]}" if key in imap else "/wp/v2/nadlan_property"
        st, res = req("POST", path, body)
        if st not in (200, 201):
            row["error"] = f"HTTP {st}: {json.dumps(res, ensure_ascii=False)[:300]}"
            results.append(row); print(json.dumps(row, ensure_ascii=False)); break
        imap[key] = res["id"]
        json.dump(imap, open(MAP_PATH, "w", encoding="utf-8"), indent=1)
        st, chk = req("GET", f"/wp/v2/nadlan_property/{res['id']}", params={"context": "edit"})
        raw = ((chk or {}).get("content") or {}).get("raw", "")
        row.update({"id": res["id"], "status": res.get("status"), "link": res.get("link"),
                    "preview": f"{WP}/?post_type=nadlan_property&p={res['id']}&preview=true",
                    "saved_chars": len(raw),
                    "markers_missing": [m for m in ('type="radio"', "<svg", "<details", "application/ld+json", "<style") if m not in raw]})
        time.sleep(0.5)
    results.append(row)
    print(json.dumps(row, ensure_ascii=False))

# ---- broker page (Hebrew) ----
if not ONLY or "broker" in ONLY:
    bp = json.load(open(os.path.join(PKG, "broker", "wp-page-he.json"), encoding="utf-8"))
    assert bp["status"] == "draft"
    content = inline_css(rd("broker/" + bp["content_file"]), css_broker)
    st, parents = req("GET", "/wp/v2/pages", params={"slug": bp["parent_slug"], "context": "edit", "status": "publish,draft,private"})
    parent = parents[0]["id"] if st == 200 and parents else None
    body = {"status": "draft", "title": bp["title"], "slug": bp["slug"], "content": content, "excerpt": bp["excerpt"]}
    if parent:
        body["parent"] = parent
    key = "broker-he"
    row = {"key": key, "title": bp["title"], "slug": bp["slug"], "parent_found": bool(parent), "chars": len(content)}
    if APPLY:
        path = f"/wp/v2/pages/{imap[key]}" if key in imap else "/wp/v2/pages"
        st, res = req("POST", path, body)
        if st not in (200, 201):
            row["error"] = f"HTTP {st}: {json.dumps(res, ensure_ascii=False)[:300]}"
        else:
            imap[key] = res["id"]
            json.dump(imap, open(MAP_PATH, "w", encoding="utf-8"), indent=1)
            st, chk = req("GET", f"/wp/v2/pages/{res['id']}", params={"context": "edit"})
            raw = ((chk or {}).get("content") or {}).get("raw", "")
            row.update({"id": res["id"], "status": res.get("status"), "link": res.get("link"),
                        "preview": f"{WP}/?page_id={res['id']}&preview=true", "saved_chars": len(raw),
                        "markers_missing": [m for m in ('type="radio"', "<svg", "nlb-lcard", "<style") if m not in raw]})
    results.append(row)
    print(json.dumps(row, ensure_ascii=False))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meital_drafts_result.json")
json.dump({"apply": APPLY, "results": results}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done; drafts only; apply=%s; rows=%d" % (APPLY, len(results)))
