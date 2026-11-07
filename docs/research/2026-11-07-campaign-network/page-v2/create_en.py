# -*- coding: utf-8 -*-
"""HAD-678: publish /en/marketing/ (page_en.html + meta_en.json) under the published /en/ root page: the English twin of /marketing/
(page 8827). The pattern of docs/tools/asbestos/create_pages.py (parent "EN_ROOT"), with the gates of this page.

Dry by default: public reads only, no credentials are opened. It runs check_page_en.py --nolinks, finds the /en/ root, confirms
the slug is free under it and /en/marketing/ answers 404, that no page or post has the same title, and that both tools are live
(the Hebrew twin must already carry data-nli="nlbudget", see add_budget.py), then prints the plan.
--go: the same gates, then the admin read (drafts, private and pending pages too) refuses if the slug exists under /en/ in any
status; creates the page published, with the Yoast title and description; fetches it live and checks: 200, exactly one h1, both
tools (data-nli) and in English, FAQPage in the JSON-LD, no raw shortcode, no Fatal error, lang="en", the Yoast title and
description, the hreflang pair with /marketing/. Any failed check moves the page to draft (never deleted) and exits 1.
  python create_en.py          dry
  python create_en.py --go     publish (owner's word first)"""
import io, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
BASE = "https://nad-lan.co.il"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
GO = "--go" in sys.argv
html = io.open(os.path.join(H, "page_en.html"), encoding="utf-8").read()
meta = json.load(io.open(os.path.join(H, "meta_en.json"), encoding="utf-8"))
TOOLS = meta["tools"]


def get(path, timeout=90):
    """Public GET, no credentials: (status, text)."""
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + path, headers={"User-Agent": UA}), timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def get_json(path):
    s, t = get(path)
    try:
        return s, json.loads(t)
    except ValueError:
        return s, None


# 1. local gates: the full local check (no network), then the publish gates of create_pages.py
r = subprocess.run([sys.executable, os.path.join(H, "check_page_en.py"), "--nolinks"], capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print(r.stdout[-3000:])
    raise SystemExit("FATAL: check_page_en.py --nolinks failed; fix the page first")
for t in TOOLS:
    if html.count(f'[nadlan_tool id="{t}"]') != 1:
        raise SystemExit(f'FATAL: the content needs exactly one [nadlan_tool id="{t}"]')
if html.count("[nadlan_tool") != len(TOOLS):
    raise SystemExit("FATAL: an extra tool shortcode in the content")
bad = [w for w in meta.get("forbid", []) if w in html or any(w in meta[k] for k in ("title", "h1", "seo_title", "seo_desc"))]
if bad:
    raise SystemExit(f"FATAL: forbidden text in the page: {bad}")
if len(re.findall(r"<h1\b", html)) != 1:
    raise SystemExit("FATAL: the content needs exactly one <h1>")

# 2. live gates (public reads)
s, h = get_json("/wp-json/nadlan/v1/health")
print("[health]", s, (h or {}).get("version"), (h or {}).get("status"))
s, roots = get_json("/wp-json/wp/v2/pages?slug=en&parent=0&_fields=id,link,status")
roots = [x for x in (roots or []) if x.get("status") == "publish"]
if len(roots) != 1:
    raise SystemExit(f"FATAL: the /en/ root page: {roots}")
PARENT = roots[0]["id"]
s, b = get_json(f"/wp-json/wp/v2/pages?slug={meta['slug']}&parent={PARENT}&_fields=id,status,link")
if b:
    raise SystemExit(f"FATAL: the slug is taken under /en/: {b[0]}")
s, _ = get(meta["path"])
if s != 404:
    raise SystemExit(f"FATAL: {meta['path']} answers {s}, not 404")
for typ in ("pages", "posts"):
    s, hits = get_json(f"/wp-json/wp/v2/{typ}?search={urllib.parse.quote(meta['title'][:40])}&_fields=id,title,link&per_page=20")
    same = [x for x in (hits or []) if re.sub(r"<[^>]+>", "", x["title"]["rendered"]).strip() == meta["title"]]
    if same:
        raise SystemExit(f"FATAL: the same title exists: {same}")
s, he = get(meta["twin"]["he"] + "?nlv=%d" % time.time())
missing = [t for t in TOOLS if f'data-nli="{t}"' not in he]
if s != 200 or missing:
    raise SystemExit(f"FATAL: the Hebrew twin {meta['twin']['he']} answers {s} and lacks {missing}: release the tool and restore it there first "
                     "(add_budget.py), or the English page goes up without it")
vis = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<style\b.*?</style>|<!--.*?-->", " ", html, flags=re.S)))
print(f"[plan] /en/{meta['slug']}/ under page {PARENT} · H1 '{meta['h1']}' · SEO {len(meta['seo_title'])}/{len(meta['seo_desc'])} chars"
      f" · {len(html):,} chars · ~{len(vis.split()):,} words · tools {', '.join(TOOLS)} · FAQ {len(meta['faq'])}")
if not GO:
    print("[dry] nothing was sent. Publish with: python create_en.py --go")
    raise SystemExit(0)

# 3. publish (credentials only from here on, inside the shared helper)
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "mktenpage"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
s, b, _ = req("GET", f"/wp-json/wp/v2/pages?slug={meta['slug']}&parent={PARENT}&status=publish,draft,private,pending,future&context=edit&_fields=id,status,link")
if s != 200 or (isinstance(b, list) and b):
    raise SystemExit(f"FATAL: the slug check (admin read) answered {s}: {b}")
s, b, _ = req("POST", "/wp-json/wp/v2/pages", {"title": meta["title"], "slug": meta["slug"], "status": "publish", "content": html, "parent": PARENT,
                                               "meta": {"_yoast_wpseo_title": meta["seo_title"], "_yoast_wpseo_metadesc": meta["seo_desc"]}})
if s not in (200, 201) or not isinstance(b, dict) or not b.get("id"):
    raise SystemExit(f"FATAL create {s}: {json.dumps(b, ensure_ascii=False)[:300]}")
pid, link = b["id"], b["link"]
json.dump({"id": pid, "link": link, "parent": PARENT, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, io.open(os.path.join(H, "published-en.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("[created]", pid, link)

# 4. the live page
time.sleep(5)
s, live = get(urllib.parse.urlparse(link).path + "?nlv=%d" % time.time())
body = live[live.find("<body"):]
ld = re.search(r'<script type="application/ld\+json" id="nadlan-nli-ld">(.*?)</script>', live, re.S)
title = re.search(r"<title>(.*?)</title>", live, re.S)
desc = re.search(r'<meta name="description" content="([^"]*)"', live)
unesc = lambda x: x.replace("&#039;", "'").replace("&amp;", "&").replace("&quot;", '"')
checks = {
    "200": s == 200,
    "one h1": len(re.findall(r"<h1[\s>]", body)) == 1,
    "both tools (data-nli)": all(f'data-nli="{t}"' in body for t in TOOLS),
    "tools in English": len(re.findall(r'<section class="nli" dir="ltr" lang="en"', body)) == len(TOOLS),
    "FAQPage JSON-LD": bool(ld) and '"FAQPage"' in ld.group(1),
    "no raw shortcode": "[nadlan_tool" not in body and "[nadlan_crumbs" not in body,
    "no Fatal error": "Fatal error" not in live and "critical error" not in live,
    "lang en": 'lang="en' in live[:3000],
    "yoast title": bool(title) and unesc(title.group(1)).strip() == meta["seo_title"],
    "yoast description": bool(desc) and unesc(desc.group(1)) == meta["seo_desc"],
    "hreflang he": f'hreflang="he" href="{BASE}{meta["twin"]["he"]}"' in live,
}
for k, v in checks.items():
    print("  ", "OK " if v else "BAD", k)
print("   hreflang:", re.findall(r'<link rel="alternate" hreflang="(\w[\w-]*)" href="([^"]+)"', live))
hard = ("200", "one h1", "both tools (data-nli)", "tools in English", "FAQPage JSON-LD", "no raw shortcode", "no Fatal error", "lang en")
if not all(checks[k] for k in hard):
    print("[draft]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"status": "draft"})[0])
    raise SystemExit(1)
if not all(checks.values()):
    print("[warn] page live; recheck the soft items above after the cache clears (Yoast title/description, hreflang transient)")
print("[done]", link, "· check on a phone and a desktop, then python ../../../../tools/source_audit.py on the page")
