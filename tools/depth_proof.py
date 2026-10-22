# -*- coding: utf-8 -*-
"""Depth proof (Ben 22.10.2026: "give me an honesty statement and prove that we are above any other page in the level of
information"; HAD-592). Reads our page and each competitor page as Google gets them (raw HTML, no scripts run) and counts the same
things on each, so the comparison is mechanical, not a claim:

  words        visible words in the main text (nav, header, footer, scripts, styles removed)
  figures      numbers in the text (amounts, percents, years, rates), each counted once per occurrence
  tables       <table> elements with at least 2 rows; table cells
  tools        interactive calculators: our [nadlan_tool] mounts, or forms with 2+ number/select inputs
  faq          questions answered (FAQPage entries, else h3/strong lines ending with "?")
  headings     h2 + h3
  visuals      <svg> charts + <img> in the main text
  sources      outbound links to official domains (gov, .gov.*, europa.eu, bankofgreece, aade, etc.)
  schema       JSON-LD types on the page
  updated      dateModified / article:modified_time

  python tools/depth_proof.py --ours https://nad-lan.co.il/x/ --them https://a.co.il/... https://b.co.il/... [--out proof.md]
Writes a Markdown table (ours first) and prints it. A metric where a competitor beats us is printed with "<" so the honesty
statement can name it."""
import argparse, html, json, re, sys, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
      "Accept-Language": "he-IL,he;q=0.9,en;q=0.6"}
OFFICIAL = re.compile(r"https?://[^\"' ]*(gov\.il|\.gov\.|gov\.gr|aade\.gr|bankofgreece|europa\.eu|ktimatologio|enterprisegreece|migration\.gov|boi\.org\.il|cbs\.gov\.il|nadlan\.gov\.il|data\.gov\.il|oecd\.org|imf\.org|statistics\.gr)", re.I)


def fetch(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60)
    return r.read().decode("utf-8", "replace")


def main_text(h):
    b = h[h.find("<body"):] if "<body" in h else h
    b = re.sub(r"<(script|style|noscript|template)\b[^>]*>.*?</\1>", " ", b, flags=re.S | re.I)
    for tag in ("header", "footer", "nav", "aside"):
        b = re.sub(r"<%s\b[^>]*>.*?</%s>" % (tag, tag), " ", b, flags=re.S | re.I)
    m = re.search(r"<(main|article)\b[^>]*>(.*)</\1>", b, re.S | re.I)
    return m.group(2) if m else b


def metrics(u):
    h = fetch(u)
    mt = main_text(h)
    txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", mt))).strip()
    words = len(re.findall(r"[\w֐-׿Ͱ-Ͽ']+", txt))
    figs = len(re.findall(r"(?<![\w.])(?:€|₪|\$)?\d[\d,.]*\s?(?:%|€|₪|אחוז|יורו|מ\"ר|מ״ר|m2|מיליון|אלף|K\b)?", txt))
    tables = [t for t in re.findall(r"<table\b.*?</table>", mt, re.S | re.I) if t.lower().count("<tr") >= 2]
    cells = sum(len(re.findall(r"<t[dh]\b", t, re.I)) for t in tables)
    tools = len(re.findall(r'data-nli="', h))
    if not tools:
        for f in re.findall(r"<form\b.*?</form>", mt, re.S | re.I):
            if len(re.findall(r'<input[^>]+type="(?:number|range|text)"|<select\b', f, re.I)) >= 2 and not re.search(r'type="(?:email|password)"', f, re.I):
                tools += 1
    faq = 0
    for blk in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
        faq += blk.count('"Question"')
    if not faq:
        faq = len([q for q in re.findall(r"<(?:h3|h4|strong|summary)\b[^>]*>(.*?)</(?:h3|h4|strong|summary)>", mt, re.S | re.I) if re.sub(r"<[^>]+>", "", q).strip().endswith("?")])
    heads = len(re.findall(r"<h2\b", mt, re.I)) + len(re.findall(r"<h3\b", mt, re.I))
    visuals = len(re.findall(r"<svg\b", mt, re.I)) + len(re.findall(r"<img\b", mt, re.I))
    srcs = len(set(m.group(0) for m in OFFICIAL.finditer(mt)))
    types = sorted(set(re.findall(r'"@type"\s*:\s*"([A-Za-z]+)"', " ".join(re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I)))))
    upd = (re.search(r'"dateModified"\s*:\s*"([^"]+)"', h) or re.search(r'article:modified_time"\s+content="([^"]+)"', h) or [None, ""])[1][:10]
    title = html.unescape((re.search(r"<title[^>]*>(.*?)</title>", h, re.S) or [None, ""])[1].strip())
    return {"url": u, "title": title, "words": words, "figures": figs, "tables": len(tables), "cells": cells, "tools": tools, "faq": faq,
            "headings": heads, "visuals": visuals, "sources": srcs, "schema": ",".join(t for t in types if t not in ("ListItem", "Organization", "ImageObject", "WebSite", "SearchAction", "EntryPoint", "PropertyValueSpecification", "ReadAction", "Answer", "Question", "Offer")), "updated": upd}


KEYS = ["words", "figures", "tables", "cells", "tools", "faq", "headings", "visuals", "sources"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ours", required=True)
    ap.add_argument("--them", nargs="+", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    rows = []
    for u in [a.ours] + a.them:
        try:
            rows.append(metrics(u))
        except Exception as e:
            rows.append({"url": u, "title": "(could not read: %s)" % str(e)[:60]})
        time.sleep(1)
    ours = rows[0]
    out = "| page | " + " | ".join(KEYS) + " | schema | updated |\n|---|" + "---|" * (len(KEYS) + 2) + "\n"
    lost = []
    for i, r in enumerate(rows):
        cells = []
        for k in KEYS:
            v = r.get(k, "")
            if i and isinstance(v, int) and isinstance(ours.get(k), int) and v > ours[k]:
                cells.append("**%s** <" % v); lost.append((k, r["url"], v, ours[k]))
            else:
                cells.append(str(v))
        out += "| %s%s | %s | %s | %s |\n" % ("**ours** " if i == 0 else "", r["url"], " | ".join(cells), r.get("schema", ""), r.get("updated", ""))
    out += "\nRead %s. Counts from raw HTML as served (no scripts run)." % time.strftime("%Y-%m-%d %H:%M")
    if lost:
        out += "\n\nWhere a competitor is ahead (for the honesty statement):\n" + "\n".join("- %s: %s has %s, we have %s" % x for x in lost)
    else:
        out += "\n\nNo competitor is ahead of us on any counted metric."
    print(out)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out + "\n\n```json\n" + json.dumps(rows, ensure_ascii=False, indent=1) + "\n```\n")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    main()
