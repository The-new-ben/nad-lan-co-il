# -*- coding: utf-8 -*-
"""Page 4484 (retargeted 25.10.2026): its 11 questions become a FAQPage node inside the page's own JSON-LD graph (the page had no
FAQPage before; one FAQPage, built from the visible h3 + p of its "שאלות נפוצות" section). Guard: the live raw content is the one
retarget_tlv.py wrote (page-4484-after.html).
  python docs/research/2026-10-25-projects-hub/retarget_faq.py [--dry]"""
import hashlib, html as HT, io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "rtf"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
s, b, _ = req("GET", "/wp-json/wp/v2/pages/4484?context=edit&_fields=content,link")
raw = b["content"]["raw"]
after = io.open(os.path.join(REPO, "docs", "qa", "projects-hub", "page-4484-after.html"), encoding="utf-8").read()
assert raw == after, "page 4484 is not the retargeted version"
assert "FAQPage" not in raw
sec = raw[raw.find('<h2 dir="rtl">שאלות נפוצות</h2>'):]
qa = re.findall(r'<h3 dir="rtl">(.*?)</h3>\s*<p dir="rtl">(.*?)</p>', sec, re.S)
faq = [{"@type": "Question", "name": HT.unescape(re.sub("<[^>]+>", "", q)).strip(), "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", HT.unescape(re.sub("<[^>]+>", "", a))).strip()}} for q, a in qa]
print("questions:", len(faq))
m = re.search(r'(<script type="application/ld\+json">)(\{"@context":"https://schema.org","@graph":\[.*?\]\})(</script>)', raw, re.S)
g = json.loads(m.group(2)); g["@graph"].append({"@type": "FAQPage", "url": "https://nad-lan.co.il/new-projects/new-projects-tel-aviv/", "mainEntity": faq})
new = raw.replace(m.group(0), m.group(1) + json.dumps(g, ensure_ascii=False, separators=(",", ":")) + m.group(3), 1)
if DRY:
    print("[dry]", len(new) - len(raw), "chars"); sys.exit(0)
s3, b3, _ = req("POST", "/wp-json/wp/v2/pages/4484", {"content": new})
s4, back, _ = req("GET", "/wp-json/wp/v2/pages/4484?context=edit&_fields=content")
print("[write]", s3, "| read-back same:", back["content"]["raw"] == new)
io.open(os.path.join(REPO, "docs", "qa", "projects-hub", "page-4484-after.html"), "w", encoding="utf-8").write(new)
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(b["link"] + "?rf=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("[live] FAQPage blocks:", page.count('"@type":"FAQPage"'))
