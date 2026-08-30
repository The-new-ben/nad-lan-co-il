# -*- coding: utf-8 -*-
"""Public View-Source audit for nad-lan.co.il (owner standing order 30.8.2026).

Fetches the RAW public HTML (what right-click > View Source / Googlebot sees,
no JavaScript), runs the house checks, saves an immutable snapshot, and diffs
against the previous snapshot of the same URL. Zero dependencies.

Usage:
  python tools/source_audit.py                      # audit the default watchlist
  python tools/source_audit.py URL [URL...]         # audit specific URLs
  python tools/source_audit.py --list               # show watchlist + latest hashes

Snapshots: docs/source-snapshots/<slug>/<UTC>-<sha12>.html (never overwritten)
Registry:  docs/source-snapshots/registry.json (append-only history of checks)
Lights are non-blocking: the script reports, the owner decides.
"""
import hashlib, io, json, os, re, sys, time, urllib.request
from datetime import datetime, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPDIR = os.path.join(REPO, "docs", "source-snapshots")
REGISTRY = os.path.join(SNAPDIR, "registry.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-SourceAudit/1.0"

WATCHLIST = [
    "https://nad-lan.co.il/",
    "https://nad-lan.co.il/projects/",
    "https://nad-lan.co.il/projects/rainbow-tel-aviv/",
    "https://nad-lan.co.il/projects/h-infinity-somail-tel-aviv/",
    "https://nad-lan.co.il/projects/six-8-herbert-samuel-tel-aviv/",
    "https://nad-lan.co.il/projects/bnei-dan-54-56/",
    "https://nad-lan.co.il/projects/stricker-13-brandeis-14/",
    "https://nad-lan.co.il/projects/duo-tel-aviv/",
    "https://nad-lan.co.il/projects/einstein-tower/",
    "https://nad-lan.co.il/echo-city/",
    "https://nad-lan.co.il/tours/",
]

BLACKLIST = ["בהמתנה לחומרי היזם", "יחליף אותו עם קבלתו", "בבדיקה מול היזם",
             "יוצגו עם קבלת נתונים", "תוכנית תתווסף", "טרם התקבלו", "מחכים ליזם",
             "אין שרטוטים", "0 חדרים", "כיוון בבדיקה", "· בקרוב"]
INTERNAL_WORDS = ["Lovable", "Codex", "lorem ipsum"]
# Mapbox public tokens (pk.) are client-side by design but trip GitHub's secret
# scanner, so snapshots store them redacted (sha in the filename stays the sha of
# the raw wire bytes). A secret-scoped token (sk.) in public HTML is a REAL leak.
PUB_TOKEN_RE = re.compile(rb"pk\.eyJ[A-Za-z0-9._-]+")
SECRET_TOKEN_RE = re.compile(r"sk\.eyJ[A-Za-z0-9._-]+")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "he-IL,he"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            body = r.read()
            return r.status, body, round((time.time() - t0) * 1000)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), round((time.time() - t0) * 1000)


def strip_tags(html):
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def analyze(url, html):
    c = {}
    get1 = lambda p: (re.search(p, html, re.S | re.I) or [None, ""])[1]
    c["title"] = re.sub(r"\s+", " ", get1(r"<title[^>]*>(.*?)</title>")).strip()
    c["title_len"] = len(c["title"])
    c["meta_desc"] = get1(r'<meta\s+name="description"\s+content="([^"]*)"').strip()
    c["meta_desc_len"] = len(c["meta_desc"])
    c["canonical"] = get1(r'<link\s+rel="canonical"\s+href="([^"]+)"')
    c["canonical_count"] = len(re.findall(r'<link\s+rel="canonical"', html, re.I))
    c["robots_meta"] = get1(r"<meta\s+name='robots'\s+content='([^']*)'") or get1(r'<meta\s+name="robots"\s+content="([^"]*)"')
    c["hreflang_count"] = len(re.findall(r'hreflang="', html))
    c["favicon_count"] = len(re.findall(r'<link[^>]+rel="[^"]*icon[^"]*"', html, re.I))
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    c["h1_count"] = len(h1s)
    c["h1_first"] = re.sub(r"<[^>]+>|\s+", " ", h1s[0]).strip()[:90] if h1s else ""
    ld_types = re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', html)
    c["jsonld_blocks"] = len(re.findall(r'<script[^>]+application/ld\+json', html, re.I))
    c["jsonld_faqpage"] = ld_types.count("FAQPage")
    c["jsonld_breadcrumb"] = ld_types.count("BreadcrumbList")
    c["scripts_ext"] = sorted(set(re.findall(r'<script[^>]+src="([^"?]+)', html)))
    c["scripts_count"] = len(re.findall(r"<script\b", html, re.I))
    c["styles_count"] = len(re.findall(r"<style\b", html, re.I)) + len(re.findall(r'<link[^>]+rel="stylesheet"', html, re.I))
    ids = re.findall(r'\sid="([^"]+)"', html)
    c["duplicate_ids"] = sorted({i for i in ids if ids.count(i) > 1})[:8]
    c["og_image"] = get1(r'<meta\s+property="og:image"\s+content="([^"]+)"')
    visible = strip_tags(html)
    c["emdash_visible"] = visible.count("—") + visible.count("–")
    c["blacklist_hits"] = [p for p in BLACKLIST if p in visible]
    c["internal_words"] = [w for w in INTERNAL_WORDS if w in html]
    c["showroom_payload"] = "NADLAN_SHOWROOM" in html
    notice = html.find('<aside class="nl-projnotice"')
    article = html.find('class="nadlan-project-article')
    c["notice_count"] = html.count('<aside class="nl-projnotice"')
    c["notice_below_article_head"] = (notice < 0) or (article > 0 and notice >= article - 400)
    c["ecocity_render_leak"] = html.count("ecocity-render")
    c["secret_tokens"] = len(SECRET_TOKEN_RE.findall(html))
    return c


def flags(c, status):
    f = []
    if status != 200:
        f.append(f"RED http {status}")
    if c.get("secret_tokens"):
        f.append(f"RED secret-token-leak x{c['secret_tokens']}")
    if c["h1_count"] != 1:
        f.append(f"RED h1x{c['h1_count']}")
    if c["canonical_count"] != 1:
        f.append(f"ORANGE canonical x{c['canonical_count']}")
    if c["blacklist_hits"]:
        f.append("RED blacklist:" + ";".join(c["blacklist_hits"][:2]))
    if c["notice_count"] > 1:
        f.append("ORANGE notice x" + str(c["notice_count"]))
    if not c["notice_below_article_head"]:
        f.append("ORANGE notice-above-article")
    if c["jsonld_faqpage"] > 1:
        f.append("YELLOW FAQPage x" + str(c["jsonld_faqpage"]))
    if c["jsonld_breadcrumb"] > 1:
        f.append("YELLOW BreadcrumbList x" + str(c["jsonld_breadcrumb"]))
    if c["duplicate_ids"]:
        f.append("YELLOW dup-ids:" + ",".join(c["duplicate_ids"][:3]))
    if c["emdash_visible"]:
        f.append(f"YELLOW dashes x{c['emdash_visible']}")
    if c["internal_words"]:
        f.append("ORANGE internal:" + ",".join(c["internal_words"]))
    if c["ecocity_render_leak"]:
        f.append("ORANGE ecocity-render x" + str(c["ecocity_render_leak"]))
    if c["title_len"] > 70:
        f.append(f"YELLOW title {c['title_len']}ch")
    if c["meta_desc_len"] > 165:
        f.append(f"YELLOW desc {c['meta_desc_len']}ch")
    return f


def slug_of(url):
    s = re.sub(r"^https?://", "", url).strip("/").replace("nad-lan.co.il", "").strip("/")
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-") or "home"


def load_registry():
    if os.path.exists(REGISTRY):
        with open(REGISTRY, encoding="utf-8") as f:
            return json.load(f)
    return {}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    reg = load_registry()
    if "--list" in sys.argv:
        for url in WATCHLIST:
            hist = reg.get(url, [])
            last = hist[-1] if hist else {}
            print(f"{url}  snapshots={len(hist)}  last={last.get('ts','-')} sha={last.get('sha256','-')[:12]}")
        return
    urls = args or WATCHLIST
    os.makedirs(SNAPDIR, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    any_change = False
    for url in urls:
        status, body, ms = fetch(url)
        html = body.decode("utf-8", "replace")
        sha = hashlib.sha256(body).hexdigest()
        c = analyze(url, html)
        fl = flags(c, status)
        hist = reg.setdefault(url, [])
        prev = hist[-1] if hist else None
        changed = (not prev) or prev["sha256"] != sha
        sdir = os.path.join(SNAPDIR, slug_of(url))
        if changed and status == 200:
            os.makedirs(sdir, exist_ok=True)
            fname = f"{now}-{sha[:12]}.html"
            with open(os.path.join(sdir, fname), "wb") as f:
                f.write(PUB_TOKEN_RE.sub(b"pk.[REDACTED-MAPBOX-PUBLIC-TOKEN]", body))
        light = "RED" if any(x.startswith("RED") for x in fl) else ("ORANGE" if any(x.startswith("ORANGE") for x in fl) else ("YELLOW" if fl else "GREEN"))
        print(f"[{light}] {url}")
        print(f"    http {status} · {len(body):,}b · {ms}ms · sha {sha[:12]} · {'CHANGED' if changed else 'unchanged'}")
        print(f"    title({c['title_len']}): {c['title'][:80]}")
        print(f"    h1x{c['h1_count']} canonical x{c['canonical_count']} hreflang {c['hreflang_count']} favicon {c['favicon_count']} jsonld {c['jsonld_blocks']} scripts {c['scripts_count']} styles {c['styles_count']}")
        if fl:
            print("    FLAGS: " + " | ".join(fl))
        if prev and changed:
            any_change = True
            pc = prev["checks"]
            diffs = []
            for k in ("title", "meta_desc", "canonical", "h1_first", "h1_count", "canonical_count",
                      "favicon_count", "jsonld_blocks", "scripts_count", "styles_count", "og_image",
                      "robots_meta", "notice_count", "emdash_visible"):
                if pc.get(k) != c.get(k):
                    diffs.append(f"{k}: {pc.get(k)!r} -> {c.get(k)!r}")
            added = sorted(set(c["scripts_ext"]) - set(pc.get("scripts_ext", [])))
            removed = sorted(set(pc.get("scripts_ext", [])) - set(c["scripts_ext"]))
            if added:
                diffs.append("scripts+ " + ", ".join(s.split("/")[-1] for s in added[:5]))
            if removed:
                diffs.append("scripts- " + ", ".join(s.split("/")[-1] for s in removed[:5]))
            diffs.append(f"bytes {prev['bytes']:,} -> {len(body):,}")
            print("    DIFF vs " + prev["ts"] + ":")
            for d in diffs:
                print("      · " + d)
        hist.append({"ts": now, "sha256": sha, "bytes": len(body), "status": status, "checks": c})
        if len(hist) > 40:
            del hist[0: len(hist) - 40]
    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=1)
    print("\nregistry updated:", REGISTRY, "| snapshots dir:", SNAPDIR)


if __name__ == "__main__":
    main()
