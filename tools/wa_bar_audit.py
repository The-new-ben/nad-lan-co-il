# -*- coding: utf-8 -*-
"""The WhatsApp bar on EVERY content page (owner order, 29.9.2026): reads the RAW public HTML of every URL in the live
sitemaps (read-only GETs, a few at a time) and reports, per URL and per content type:
  - bar:     the site's WhatsApp bar is printed (<div id="nlcta">)
  - mini:    its script still shrinks it to a circle on phones (the old 'is-mini' rule)
  - text:    what the bar says (its bold line)
  - brokers: the page is a broker page, where the old rule stepped the site bar aside
  python tools/wa_bar_audit.py [--out DIR] [--workers 6] [--limit N]
Writes wa-audit.csv and prints a summary. The raw HTML is what every visitor and every bot receives, before any script."""
import argparse, collections, concurrent.futures as cf, csv, io, os, re, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (nadlan wa_bar_audit.py; read-only)", "Accept-Encoding": "identity"}


def urls_from_sitemaps():
    idx = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il/sitemap_index.xml?x=%d" % time.time(), headers=UA), timeout=60).read().decode("utf-8")
    out = []
    for sm in re.findall(r"<loc>([^<]+)</loc>", idx):
        kind = re.sub(r"\d*\.xml$", "", sm.rsplit("/", 1)[1]).replace("-sitemap", "")
        body = urllib.request.urlopen(urllib.request.Request(sm + "?x=%d" % time.time(), headers=UA), timeout=60).read().decode("utf-8")
        out += [(kind, u) for u in re.findall(r"<loc>([^<]+)</loc>", body)]
    return out


def check(item):
    kind, url = item
    try:
        r = urllib.request.urlopen(urllib.request.Request(url + ("&" if "?" in url else "?") + "wa=%d" % time.time(), headers=UA), timeout=45)
        html = r.read().decode("utf-8", "replace"); status = r.status
    except urllib.error.HTTPError as e:
        return {"kind": kind, "url": url, "status": e.code, "bar": "", "mini": "", "text": "", "brokers": ""}
    except Exception as e:
        return {"kind": kind, "url": url, "status": "ERR " + str(e)[:40], "bar": "", "mini": "", "text": "", "brokers": ""}
    s = html.find('<div id="nlcta"')
    block = html[s:html.find("</script>", s) + 9] if s > 0 else ""
    text = re.search(r'class="nlcta-txt"[^>]*>\s*<b>([^<]*)</b>', block)
    return {"kind": kind, "url": url, "status": status, "bar": "yes" if s > 0 else "NO",
            "mini": "yes" if "is-mini" in block else "", "text": (text.group(1).strip() if text else ""),
            "brokers": "yes" if re.search(r'class="[^"]*\bnlb\b|nlb-mbar|nlx-mbar', html) else ""}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="."); ap.add_argument("--workers", type=int, default=6); ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    items = urls_from_sitemaps()
    if a.limit:
        items = items[: a.limit]
    rows = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for i, r in enumerate(ex.map(check, items)):
            rows.append(r)
            if (i + 1) % 250 == 0:
                print("  %d/%d" % (i + 1, len(items)), flush=True)
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "wa-audit.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["kind", "url", "status", "bar", "mini", "text", "brokers"]); w.writeheader(); w.writerows(rows)
    by = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        c = by[r["kind"]]; c["pages"] += 1
        if r["status"] == 200:
            c["ok200"] += 1; c["bar"] += r["bar"] == "yes"; c["no_bar"] += r["bar"] == "NO"; c["mini"] += r["mini"] == "yes"
        else:
            c["not200"] += 1
    print("\n%-22s %6s %6s %6s %7s %6s %7s" % ("type", "pages", "200", "bar", "NO bar", "circle", "not200"))
    tot = collections.Counter()
    for k, c in sorted(by.items(), key=lambda kv: -kv[1]["pages"]):
        print("%-22s %6d %6d %6d %7d %6d %7d" % (k, c["pages"], c["ok200"], c["bar"], c["no_bar"], c["mini"], c["not200"]))
        tot.update(c)
    print("%-22s %6d %6d %6d %7d %6d %7d" % ("ALL", tot["pages"], tot["ok200"], tot["bar"], tot["no_bar"], tot["mini"], tot["not200"]))
    texts = collections.Counter(r["text"] for r in rows if r["bar"] == "yes")
    print("\nbar texts:", dict(texts.most_common(6)))
    print("pages WITHOUT the bar (first 15):")
    for r in [r for r in rows if r["bar"] == "NO"][:15]:
        print("  ", r["kind"], r["url"], "(broker page)" if r["brokers"] else "")


if __name__ == "__main__":
    main()
