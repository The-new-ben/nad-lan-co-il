# -*- coding: utf-8 -*-
"""U1 quick fixes in the mortgage cluster (Ben 25.10.2026: "start with the small fixes"), from dna.md sections 7 and 9:
  1. 17 internal links that answer 404 (/reverse-mortgage/, /mortgage-ltv-ratio/, /mortgage-interest-rates/,
     /mortgage-repayment-capacity/) now point at the real pages under /mortgage-calculator/ (an href edit, not a redirect);
  2. the calculators on /mortgage-calculator/ open with the official averages instead of 5.2 / 6.0 / 5.5 / 4.8: fixed unlinked 4.62%
     and variable CPI-linked 3.19% (Bank of Israel, new housing loans, August 2026), prime 4.75% (October 2026), with the date in the note;
     "סימולציית" and "PMT" and "נדלן חכם" leave the visible text (language DNA);
  3. the interest-rates page description said "ריבית בנק ישראל סביב 4% והפריים סביב 5.5%": now 3.25% and 4.75% (October 2026).
Backup of each live content first, exact replacements (each must match), read-back, live check.
  python docs/research/2026-10-26-upgrades/u1-mortgage-calculator/fix_cluster_quick.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "u1q"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
BAD = ["reverse-mortgage", "mortgage-ltv-ratio", "mortgage-interest-rates", "mortgage-repayment-capacity"]
NOTE_OLD = "החישוב מבוסס על נוסחת PMT סטנדרטית (לוח שפיצר). ערכי ריבית הם להמחשה, בנקים מציעים ריביות שונות לפי דירוג אשראי ויחס מימון. זה אינו ייעוץ פיננסי. נדלן חכם."
NOTE_NEW = ("החישוב לפי לוח שפיצר. הריביות שמופיעות מראש הן הממוצע במשכנתאות חדשות לפי בנק ישראל באוגוסט 2026: קל&quot;צ 4.62%, "
            "משתנה צמודה כל 5 שנים 3.19%, והפריים באוקטובר 2026: 4.75%. הבנק יציע ריבית לפי דירוג האשראי ושיעור המימון שלכם. זה אינו ייעוץ פיננסי.")
EXTRA = {
    121: [
        ('data-k="rate" data-t="0" value="5.2"', 'data-k="rate" data-t="0" value="4.62"'),
        ('data-k="rate" data-t="1" value="6.0"', 'data-k="rate" data-t="1" value="4.75"'),
        ('data-k="rate" data-t="2" value="5.5"', 'data-k="rate" data-t="2" value="3.19"'),
        ('<input id="nmc-rate" type="number" value="4.8"', '<input id="nmc-rate" type="number" value="4.62"'),
        ("סימולציית עליית ריבית (+2%)", "בדיקת עליית ריבית (+2%)"),
        (NOTE_OLD, NOTE_NEW),
    ],
}
META = {514: ("ריבית בנק ישראל סביב 4% והפריים סביב 5.5%", "ריבית בנק ישראל 3.25% והפריים 4.75% (אוקטובר 2026)")}
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for pid in (121, 519, 514, 513, 512):
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,meta,link" % pid)
    raw = r["content"]["raw"]; new = raw; n = 0
    for b in BAD:
        new, k = re.subn(r'href="(?:https://nad-lan\.co\.il)?/%s/"' % re.escape(b), 'href="/mortgage-calculator/%s/"' % b, new); n += k
    for a, b2 in EXTRA.get(pid, []):
        assert new.count(a) == 1, (pid, new.count(a), a[:60])
        new = new.replace(a, b2)
    body = {"content": new}
    if pid in META:
        md = r["meta"].get("_yoast_wpseo_metadesc") or ""
        assert md.count(META[pid][0]) == 1, (pid, "metadesc")
        body["meta"] = {"_yoast_wpseo_metadesc": md.replace(*META[pid])}
    print("[page %d] %s | links fixed %d | extra %d | meta %s" % (pid, r["link"].replace("https://nad-lan.co.il", ""), n, len(EXTRA.get(pid, [])), pid in META))
    if DRY:
        continue
    io.open(os.path.join(bk, "page-%d-%s.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    req("POST", "/wp-json/wp/v2/pages/%d" % pid, body)
    back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
    time.sleep(2)
    page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    bd = page[page.find("<body"):]
    dead = [b for b in BAD if re.search(r'href="(?:https://nad-lan\.co\.il)?/%s/"' % b, bd)]
    ok = {"read-back": back == new, "no dead link left": not dead, "one h1": bd.count("<h1") == 1}
    if pid == 121:
        ok["rates 4.62 / 4.75 / 3.19 in the calculator"] = all(('value="%s"' % v) in bd for v in ("4.62", "4.75", "3.19"))
        ok["no PMT / סימולציית / נדלן חכם"] = not re.search(r"PMT|סימולציית|נדלן חכם", re.sub(r"<script\b.*?</script>", "", bd, flags=re.S))
    for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
