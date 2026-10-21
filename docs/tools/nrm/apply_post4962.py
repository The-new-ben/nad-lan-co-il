# -*- coding: utf-8 -*-
"""HAD-575 / Kikar tools #5: the English tool "nrm" on post 4962 /israel-mortgage-non-residents/, right after the byline: a short
answer with numbers, then the calculator (content-first: H1, answer, tool, then the article as it is). Guard on the live content
(md5 of the saved copy); backup before, read-back after.   python docs/tools/nrm/apply_post4962.py [--dry]"""
import hashlib, io, os, sys, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "nrm4962"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
H = os.path.dirname(os.path.abspath(__file__))
s, b, _ = req("GET", "/wp-json/wp/v2/posts/4962?context=edit&_fields=content,modified")
raw = b["content"]["raw"]
want_p = os.path.join(H, "post4962-before.html")
if not os.path.exists(want_p):
    io.open(want_p, "w", encoding="utf-8", newline="").write(raw); print("saved post4962-before.html")
want = io.open(want_p, encoding="utf-8", newline="").read()
if hashlib.md5(raw.encode()).hexdigest() != hashlib.md5(want.encode()).hexdigest():
    raise SystemExit("FATAL: post 4962 changed since it was saved (%s)" % b["modified"])
assert "[nadlan_tool" not in raw
i = raw.index("<p"); j = raw.index("</p>", i) + len("</p>")
assert "Ben Betesh" in raw[i:j], "the byline is not the first paragraph"
NEW = ('\n<p><strong>Short answer:</strong> an Israeli bank can lend a non-resident up to 50% of the property value. At the August 2026 '
       'average rate for fixed, non-linked mortgages (4.62%), a ₪2,000,000 loan over 25 years costs about ₪11,253 a month, about $3,641 at the '
       'Bank of Israel rate of 21 October 2026. On a ₪4,000,000 home the cash to close is about ₪2.34 million (about $758,500), including the 8% '
       'purchase tax a foreign resident pays. Put in your own numbers below.</p>\n[nadlan_tool id="nrm"]\n')
out = raw[:j] + NEW + raw[j:]
print("[plan] post 4962: %d -> %d chars, inserted after the byline at %d" % (len(raw), len(out), j))
if "--dry" in sys.argv:
    raise SystemExit(0)
bk = os.path.join(REPO, "docs", "qa", "had-527", "page-backup"); os.makedirs(bk, exist_ok=True)
ts = time.strftime("%Y%m%d-%H%M%S")
io.open(os.path.join(bk, "post4962-%s.html" % ts), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/posts/4962", {"content": out})
s, b3, _ = req("GET", "/wp-json/wp/v2/posts/4962?context=edit&_fields=content")
print("written:", b3["content"]["raw"] == out, "| backup: post4962-%s.html" % ts)
