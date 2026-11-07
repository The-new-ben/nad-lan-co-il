# HAD-678: after 1.72.600, put the nlbudget block back on /marketing/ (page 8827): the live content must equal the publish copy; the new content is page_he.html (a superset).
import io, os, re, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "ab"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
full = io.open(os.path.join(H, "page_he.html"), encoding="utf-8").read()
i = full.index('<div id="budget-tool"'); k = full.index('[nadlan_tool id="nlbudget"]') + len('[nadlan_tool id="nlbudget"]')
pub = full[:i] + full[k:]; a = pub.index("<p>המחשבון נשען"); b = pub.index("</p>", a) + 4; pub = pub[:a] + pub[b:]
pub = pub.replace('href="#budget-tool">חשבו את תקציב השיווק של הפרויקט', 'href="#line-items">פירוק התקציב רכיב אחר רכיב')
s, r, _ = req("GET", "/wp-json/wp/v2/pages/8827?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]
assert "nlbudget" not in raw, "already there"
assert raw.strip() == pub.strip(), "live content changed since publish: stop and merge by hand"
for line in raw.split("\n"):
    assert not line.strip() or line in full or 'href="#line-items">פירוק התקציב' in line, ("missing", line[:80])
print("[plan] restore the budget block: %d -> %d chars" % (len(raw), len(full)))
if "--go" not in sys.argv: sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-8827-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/8827", {"content": full}); assert s2 in (200, 201), s2
time.sleep(5)
live = urllib.request.urlopen(urllib.request.Request(r["link"] + "?z=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print({"nlbudget": 'data-nli="nlbudget"' in live, "nlcamp": 'data-nli="nlcamp"' in live, "raw shortcode": "[nadlan_tool" in live, "h1": len(re.findall(r"<h1[\s>]", live)), "fatal": "Fatal error" in live})
