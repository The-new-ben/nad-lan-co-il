# -*- coding: utf-8 -*-
"""Fact coverage (the second half of the depth proof, Ben 22.10.2026: "prove we are above any other page in the level of
information"). Word counts reward length; this counts KNOWLEDGE: for a list of the facts a buyer needs (each with the
regular expressions that find it, in Hebrew or English), it reads every page's visible text as served and marks which page
states the fact. A fact counts only when the pattern matches the visible text (tools' plain summaries included, scripts and
styles excluded). The facts file is per cluster: [{"label": "...", "re": ["...", "..."]}].

  python tools/fact_coverage.py --facts docs/research/2026-10-22-greece/coverage-facts.json --urls <ours> <competitor> ... [--out x.md]
The first URL is ours. Prints a matrix (✓ / ·) and the totals."""
import argparse, html, io, json, re, sys, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36", "Accept-Language": "he-IL,he;q=0.9"}


def text(u):
    h = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode("utf-8", "replace")
    b = h[h.find("<body"):] if "<body" in h else h
    b = re.sub(r"<(script|style|noscript|template)\b[^>]*>.*?</\1>", " ", b, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", b)))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--facts", required=True); ap.add_argument("--urls", nargs="+", required=True); ap.add_argument("--out")
    a = ap.parse_args()
    facts = json.load(io.open(a.facts, encoding="utf-8"))
    texts = []
    for u in a.urls:
        try: texts.append(text(u))
        except Exception as e: texts.append(""); print("could not read", u, e)
        time.sleep(1)
    short = lambda u: re.sub(r"^https?://(www\.)?", "", u)[:38]
    out = "| fact | " + " | ".join(("**ours** " if i == 0 else "") + short(u) for i, u in enumerate(a.urls)) + " |\n|---|" + "---|" * len(a.urls) + "\n"
    tot = [0] * len(a.urls)
    for f in facts:
        row = []
        for i, t in enumerate(texts):
            hit = any(re.search(p, t, re.I) for p in f["re"])
            tot[i] += hit; row.append("✓" if hit else "·")
        out += "| %s | %s |\n" % (f["label"], " | ".join(row))
    out += "| **total of %d** | %s |\n" % (len(facts), " | ".join("**%d**" % x for x in tot))
    out += "\nRead %s from the pages as served (visible text, scripts excluded)." % time.strftime("%Y-%m-%d %H:%M")
    print(out)
    if a.out: io.open(a.out, "w", encoding="utf-8").write(out + "\n")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    main()
