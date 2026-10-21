# -*- coding: utf-8 -*-
"""HAD-575 (Ben 21.10.2026: "link the tools from the related pages, without clashing"): one plain sentence with one link to a tool,
right after a named paragraph of an existing page or post, from docs/research/2026-10-21-kikar-tools/linking-plan.json, one wave at a
time (the owner's no-mass-change rule). Skips a page that already links the tool. Backup before, read-back after, the live page then
checked for the link and one H1.   python scripts/project-stage/place_tool_links.py <wave 1|2|3> [--dry]"""
import io, json, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "toollinks"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
PLAN = json.load(io.open(os.path.join(REPO, "docs", "research", "2026-10-21-kikar-tools", "linking-plan.json"), encoding="utf-8"))
BK = os.path.join(REPO, "docs", "qa", "had-575", "page-backup"); os.makedirs(BK, exist_ok=True)
wave = sys.argv[1]; DRY = "--dry" in sys.argv
FORCE = {int(x) for a in sys.argv if a.startswith("--force=") for x in a[8:].split(",")}  # ids whose only link is a list at the bottom: add the in-body one anyway
ids = set(PLAN["pace"]["wave_" + wave])
rows = [x for x in PLAN["links"] if x["from_id"] in ids]
by = {}
for x in rows: by.setdefault((x["type"], x["from_id"]), []).append(x)
plain = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()
report = []
for (typ, pid), xs in by.items():
    ep = {"page": "pages", "post": "posts"}.get(typ)
    if not ep:
        report.append((pid, "SKIP type " + typ)); continue
    s, b, _ = req("GET", "/wp-json/wp/v2/%s/%d?context=edit&_fields=content,link,modified" % (ep, pid))
    raw = b["content"]["raw"]; new = raw; done = []
    for x in xs:
        path = x["tool_url"].replace("https://nad-lan.co.il", "")
        if pid not in FORCE and ('href="%s"' % x["tool_url"] in new or 'href="%s"' % path in new):
            done.append(x["tool"] + ": already linked"); continue
        m = re.search(r'starts "([^"]{12,})', x["after_heading_or_text"])
        if not m:
            done.append(x["tool"] + ": NO ANCHOR TEXT"); continue
        start = m.group(1)[:40]
        hit = None
        for pm in re.finditer(r"<p\b[^>]*>(.*?)</p>", new, re.S):
            if plain(pm.group(1)).startswith(plain(start)[:30]):
                hit = pm; break
        if not hit:
            done.append(x["tool"] + ": PARAGRAPH NOT FOUND (%s)" % start[:30]); continue
        sent, at = x["anchor_sentence"], x.get("anchor_text") or ""
        link = '<a href="%s">%s</a>' % (path if path.startswith("/") else x["tool_url"], at)
        sent_html = sent.replace(at, link, 1) if at and at in sent else sent + " " + link
        new = new[:hit.end()] + "\n<p>" + sent_html + "</p>" + new[hit.end():]
        done.append(x["tool"] + ": after «%s…»" % plain(hit.group(1))[:40])
    report.append((pid, "; ".join(done)))
    if new == raw or DRY:
        continue
    io.open(os.path.join(BK, "%s-%d-%s.html" % (typ, pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    req("POST", "/wp-json/wp/v2/%s/%d" % (ep, pid), {"content": new})
    back = req("GET", "/wp-json/wp/v2/%s/%d?context=edit&_fields=content" % (ep, pid))[1]["content"]["raw"]
    time.sleep(1)
    html = urllib.request.urlopen(urllib.request.Request(b["link"] + ("&" if "?" in b["link"] else "?") + "nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    body = html[html.find("<body"):]
    ok = back == new and body.count("<h1") == 1 and all((x["tool_url"].replace("https://nad-lan.co.il", "") in body) for x in xs) and all(x["anchor_sentence"][:20] in body for x in xs if x["anchor_sentence"][:20] in new)
    report[-1] = (pid, report[-1][1] + (" | LIVE OK" if ok else " | LIVE CHECK FAILED"))
for pid, r in report:
    print(pid, r)
