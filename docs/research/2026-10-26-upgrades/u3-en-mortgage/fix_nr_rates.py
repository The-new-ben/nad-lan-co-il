# -*- coding: utf-8 -*-
"""/israel-mortgage-non-residents/ (post 4962, an English article): the rates still described the May 2026 decision (policy rate 3.75%,
prime 5.25%, inflation 1.9%, next decision July 6, May/June averages) and the LTV table said "Israeli resident" where Bank of Israel
Directive 329 says citizen. Current figures from the U3/U1 research (verified 25.10.2026): policy rate 3.25% since 3.9.2026, prime 4.75%,
CPI 1.6% for the 12 months to September 2026, next decision 23.11.2026, August 2026 averages: fixed non-linked 4.62%, fixed CPI-linked
3.29%, variable CPI-linked 3.19%. Exact replacements (each must match), backup, read-back, live check. The language question of this page
(English content at the Hebrew root) is Ben's decision and is not touched here.
  python docs/research/2026-10-26-upgrades/u3-en-mortgage/fix_nr_rates.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "nr"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 4962
NEWFAQ = ("The Bank of Israel policy rate is 3.25% (in force since September 3, 2026; next decision November 23, 2026), and the prime rate is 4.75%. "
          "The Bank of Israel average-rate series showed 4.62% for new fixed non-linked mortgages and 3.29% for fixed CPI-linked mortgages in August 2026 data.")
R = [
    ("The Bank of Israel policy rate was 3.75% after the May 25, 2026 cut, and the prime rate was 5.25%. The Bank of Israel average-rate series showed 3.57% for new CPI-linked mortgages (May 2026 data) and about 4.79% for non-linked mortgages in June 2026.", NEWFAQ),
    ("The Bank of Israel policy rate was 3.75% after the May 25, 2026 cut, and the prime rate was 5.25%. The Bank of Israel average mortgage rate series showed 3.57% for new CPI-linked mortgages in May 2026 data published June 11, 2026, and about 4.79% for non-linked mortgages in June 2026.", NEWFAQ),
    ("<td>Prime stood at 5.25% after the May 25, 2026 Bank of Israel decision</td>", "<td>Prime is 4.75% (the Bank of Israel rate of 3.25% plus 1.5%), October 2026</td>"),
    ("The Bank of Israel Monetary Committee cut the policy rate by 0.25% to 3.75% on May 25, 2026. The prime rate, defined as the policy rate plus 1.5%, now stands at 5.25%. Inflation over the previous 12 months was 1.9%, and the next rate decision is scheduled for July 6, 2026, according to the Bank of Israel press release dated May 25, 2026.",
     "The Bank of Israel policy rate is 3.25%, in force since September 3, 2026, and it was left unchanged in October. The prime rate, defined as the policy rate plus 1.5%, stands at 4.75%. Inflation over the 12 months to September 2026 was 1.6% (Central Bureau of Statistics), and the next rate decision is scheduled for November 23, 2026."),
    ("In May 2026 data published June 11, 2026, the weighted average rate on new CPI-linked mortgages was 3.57%, according to the Bank of Israel average-rate series. The average non-linked mortgage rate stood at about 4.79% in June 2026 according to trackers of the same Bank of Israel series.",
     "In August 2026 data, the latest published, the average rate on new fixed non-linked mortgages was 4.62%, on fixed CPI-linked mortgages 3.29%, and on variable CPI-linked mortgages 3.19%, according to the Bank of Israel average-rate series."),
    ("<td>3.75%</td>\n<td>Central policy anchor after the Monetary Committee cut</td>\n<td>Bank of Israel press release, May 25, 2026</td>",
     "<td>3.25%</td>\n<td>Central policy anchor, in force since September 3, 2026</td>\n<td>Bank of Israel, checked October 25, 2026</td>"),
    ("<td>5.25%</td>\n<td>Policy rate plus 1.5%</td>\n<td>Bank of Israel press release, May 25, 2026</td>",
     "<td>4.75%</td>\n<td>Policy rate plus 1.5%</td>\n<td>Bank of Israel, checked October 25, 2026</td>"),
    ("<td>1.9%</td>\n<td>Inflation backdrop relevant to CPI-linked tracks</td>\n<td>Bank of Israel press release, May 25, 2026</td>",
     "<td>1.6%</td>\n<td>Inflation backdrop relevant to CPI-linked tracks</td>\n<td>Central Bureau of Statistics, 12 months to September 2026</td>"),
    ("<td>Weighted average rate on new CPI-linked mortgages</td>\n<td>3.57%</td>\n<td>Average-rate series anchor, not a borrower-specific quote</td>\n<td>Bank of Israel average mortgage rate series, May 2026 data published June 11, 2026</td>",
     "<td>Average rate on new fixed CPI-linked mortgages</td>\n<td>3.29%</td>\n<td>Average-rate series anchor, not a borrower-specific quote</td>\n<td>Bank of Israel average mortgage rate series, August 2026</td>"),
    ("<td>Average non-linked mortgage rate</td>\n<td>About 4.79%</td>\n<td>Average-rate series anchor, not a borrower-specific quote</td>\n<td>Bank of Israel average mortgage rate series, June 2026</td>",
     "<td>Average rate on new fixed non-linked mortgages</td>\n<td>4.62%</td>\n<td>Average-rate series anchor, not a borrower-specific quote</td>\n<td>Bank of Israel average mortgage rate series, August 2026</td>"),
    ("<td>July 6, 2026</td>\n<td>Scheduled policy update date</td>\n<td>Bank of Israel press release, May 25, 2026</td>",
     "<td>November 23, 2026</td>\n<td>Scheduled policy update date</td>\n<td>Bank of Israel, checked October 25, 2026</td>"),
    ("the LTV cap is 75% for an Israeli resident's first and only home", "the LTV cap is 75% for an Israeli citizen's first and only home"),
    ("<td>Israeli resident, first and only home</td>", "<td>Israeli citizen, first and only home</td>"),
    ("<td>Israeli resident, replacement home</td>", "<td>Israeli citizen, replacement home</td>"),
    ("not the same as for an Israeli resident buying a first home", "not the same as for an Israeli citizen buying a first home"),
    ("Last reviewed: July 2, 2026", "Last reviewed: July 2, 2026 · rates updated October 25, 2026"),
    ("<td>Weighted average rate on new CPI-linked mortgages was 3.57% in May 2026 data, published June 11, 2026 by the Bank of Israel average-rate series</td>",
     "<td>Average rate on new fixed CPI-linked mortgages was 3.29% in August 2026 data, per the Bank of Israel average-rate series</td>"),
    ("<td>Average non-linked mortgage rate stood at about 4.79% in June 2026, per the Bank of Israel average-rate series</td>",
     "<td>Average rate on new fixed non-linked mortgages was 4.62% in August 2026 data, per the Bank of Israel average-rate series</td>"),
]
DESC_OLD = "prime at 5.25%, average rates 3.57-4.79%"
DESC_NEW = "prime at 4.75%, average rates 3.29-4.62% (August 2026)"
for typ in ("posts", "pages"):
    s, p, _ = req("GET", "/wp-json/wp/v2/%s/%d?context=edit&_fields=content,meta,link" % (typ, PID))
    if s == 200:
        break
raw = p["content"]["raw"]; new = raw.replace("\r\n", "\n"); crlf = "\r\n" in raw
for a, b in R:
    assert new.count(a) >= 1, a[:80]
    new = new.replace(a, b)
if crlf:
    new = new.replace("\n", "\r\n")
md = p["meta"].get("_yoast_wpseo_metadesc") or ""
assert md.count(DESC_OLD) == 1, "metadesc"
left = [x for x in ("5.25%", "3.75%", "3.57%", "4.79%", "July 6") if x in new]
print("[post %d] %d replacements | stale left: %s" % (PID, len(R), left))
if DRY:
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "post-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/%s/%d" % (typ, PID), {"content": new, "meta": {"_yoast_wpseo_metadesc": md.replace(DESC_OLD, DESC_NEW)}})
back = req("GET", "/wp-json/wp/v2/%s/%d?context=edit&_fields=content,meta" % (typ, PID))[1]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(p["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"read-back": back["content"]["raw"] == new, "no 5.25 / 3.75 / July 6": not re.search(r"5\.25%|3\.75%|July 6, 2026", page), "4.75 and 23.11": "4.75%" in page and "November 23, 2026" in page,
      "citizen in the LTV table": "Israeli citizen, first and only home" in page, "meta": DESC_NEW in page}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
