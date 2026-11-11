# -*- coding: utf-8 -*-
"""HAD-707: publish or update the three design pages from docs/tools/design-studio/<key>/page.html + meta.json.
  hub            /design-studio/                    a root page
  designer-cost  /design-studio/designer-cost/      a child of the hub
  designers      /profession/מעצב-פנים/             a child of the PRIVATE page "profession" (never public itself);
                                                     inc/design-pages.php hands that address to the page
A new page is created published; an existing one is updated after its live content is saved under docs/qa/design-studio/.
After each write the public page is fetched and checked (200, one h1, no raw shortcode, every tool's host, the designer or the
list, the title, the canonical, index). A failed check on a NEW page moves it to draft (never deleted, never redirected).
No redirect, no noindex, no indexing request.   python publish_pages.py <key> [<key> ...] [--dry]"""
import io, json, os, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "designpages"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
DRY = "--dry" in sys.argv
KEYS = [a for a in sys.argv[1:] if not a.startswith("--")]
QA = os.path.join(REPO, "docs", "qa", "design-studio")
os.makedirs(QA, exist_ok=True)
ANY = "publish,draft,private,pending"


def find(slug, parent):
    s, b, _ = req("GET", "/wp-json/wp/v2/pages?slug=%s&parent=%d&status=%s&context=edit&_fields=id,status,link,slug,parent" % (urllib.parse.quote(slug), parent, ANY))
    if s != 200 or not isinstance(b, list):
        raise SystemExit("FATAL lookup %s: %s" % (slug, s))
    return b


def parent_id(path):
    if not path:
        return 0
    hit = find(path, 0)
    if hit:
        return hit[0]["id"]
    if path != "profession":
        raise SystemExit("FATAL: the parent page /%s/ does not exist; publish it first" % path)
    if DRY:
        print("[dry] would create the PRIVATE parent page 'profession'"); return -1
    s, b, _ = req("POST", "/wp-json/wp/v2/pages", {"title": "אנשי מקצוע לפי תחום", "slug": "profession", "status": "private", "content": ""})
    if s not in (200, 201) or not b.get("id"):
        raise SystemExit("FATAL create parent: %s" % s)
    print("[parent] private page 'profession' created:", b["id"])
    return b["id"]


def fetch(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/141 Safari/537.36"})
    with urllib.request.urlopen(r, timeout=90) as f:
        return f.status, f.geturl(), f.read().decode("utf-8", "replace")


def check(key, meta, link):
    time.sleep(3)
    st, final, live = fetch(link + "?nlv=%d" % time.time())
    body = live[live.find("<body"):]
    art = body[body.find('nlds-pg'):]
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', live)
    robots = re.search(r"<meta name=.robots. content=.([^'\"]+)", live)
    want = "https://nad-lan.co.il" + meta["path"]
    cz = urllib.parse.unquote(canon.group(1)) if canon else ""
    c = {
        "200 and no redirect": st == 200 and urllib.parse.unquote(final.split("?")[0]) == want,
        "one h1": body.count("<h1") == 1,
        "no raw shortcode": "[nadlan_" not in body,
        "every tool host": all('data-nli="%s"' % t in body for t in meta["tools"]),
        "tool titles under the sections (no h2 tool title)": '<h2 class="nli__title"' not in art,
        "design.js loaded": (not meta["tools"]) or "/assets/instruments/tools/design.js" in live,
        "the page style": 'id="nlds-pages-css"' in body,
        "title": meta["seo_title"].split(":")[0].split("|")[0].strip() in live[:30000],
        "canonical": cz == want,
        "index": bool(robots) and "noindex" not in robots.group(1),
        "FAQPage": '"@type":"FAQPage"' in live,
        "no PHP error": "Fatal error" not in live and "Warning</b>" not in live,
    }
    if key == "hub":
        c["the designer host"] = 'class="nadlan-designer"' in body and 'type="importmap"' in live and "assets/designer/designer.js" in body
        c["the plan chooser"] = body.count("plans/example-") >= 3
    if key == "designers":
        c["the list"] = body.count('class="nlds-rec"') >= 50 and '"@type":"ItemList"' in body
    for k, v in c.items():
        print("   ", "OK " if v else "BAD", k)
    return all(c.values())


for key in KEYS:
    W = os.path.join(H, key)
    html = io.open(os.path.join(W, "page.html"), encoding="utf-8").read()
    meta = json.load(io.open(os.path.join(W, "meta.json"), encoding="utf-8"))
    pid_parent = parent_id(meta["parent_path"])
    hit = find(meta["slug"], pid_parent) if pid_parent >= 0 else []
    payload = {"title": meta["wp_title"], "content": html, "meta": {"_yoast_wpseo_title": meta["seo_title"], "_yoast_wpseo_metadesc": meta["seo_desc"]}}
    print("[plan] %s -> %s | parent %s | %s | %d KB | title %d / desc %d" % (key, meta["path"], pid_parent, "UPDATE %s" % hit[0]["id"] if hit else "CREATE", len(html.encode("utf-8")) // 1024, len(meta["seo_title"]), len(meta["seo_desc"])))
    if DRY:
        continue
    if hit:
        pid = hit[0]["id"]
        s, cur, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,status,content,title,meta" % pid)
        if s != 200:
            raise SystemExit("FATAL read %d: %s" % (pid, s))
        bk = os.path.join(QA, "%s-%d-%s.before.json" % (key, pid, time.strftime("%Y%m%dT%H%M%S")))
        json.dump(cur, io.open(bk, "w", encoding="utf-8"), ensure_ascii=False)
        s, b, _ = req("POST", "/wp-json/wp/v2/pages/%d" % pid, dict(payload, status="publish"))
        if s != 200:
            raise SystemExit("FATAL update %d: %s" % (pid, s))
        link, new = b["link"], False
        print("[updated]", pid, urllib.parse.unquote(link), "| backup", os.path.relpath(bk, REPO))
    else:
        s, b, _ = req("POST", "/wp-json/wp/v2/pages", dict(payload, slug=meta["slug"], status="publish", parent=pid_parent))
        if s not in (200, 201) or not b.get("id"):
            raise SystemExit("FATAL create %s: %s %s" % (key, s, str(b)[:300]))
        pid, link, new = b["id"], b["link"], True
        print("[created]", pid, urllib.parse.unquote(link))
    json.dump({"id": pid, "link": urllib.parse.unquote(link), "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, io.open(os.path.join(W, "published.json"), "w", encoding="utf-8"), ensure_ascii=False)
    ok = check(key, meta, link)
    if not ok and new:
        print("[draft] a new page failed its checks, moved to draft:", req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"status": "draft"})[0])
        raise SystemExit(1)
    if not ok:
        raise SystemExit("CHECKS FAILED on an updated page (left as written; the backup is saved): " + key)
    print("[done]", urllib.parse.unquote(link))
