# -*- coding: utf-8 -*-
"""Q4 /glossary/דקל-תוכנה/ (term 5392), after the rewrite: (1) the price lists the software works with, chapters and items per list
(dekel.co.il, the same facts as the Q3 page, from data/dekel.json) as a table and a bar chart; (2) two public tenders that price by Dekel,
read in the tender PDFs on 26.10.2026 (Ministry of Energy 42/2025 on gov.il: "המכרז מבוסס על מחירון דקל", viewing rights from Dekel,
possibly paid; Sheba Medical Center annual tender on mr.gov.il: payment by the latest Dekel building and infrastructure edition less
the bid discount), as official sources. Exact insertions, backup, read-back, live check.   python .../write_q4_more.py [--dry]"""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q4m"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 5392
D = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "dekel.json"), encoding="utf-8"))
GOV = "https://www.gov.il/BlobFolder/rfp/tender-42-2025/he/tender-42-2025.pdf"
MR = "https://mr.gov.il/ilgstorefront/he/p/attachment/005056BFAF4C1FE0A09457C65CD2B2EE/%D7%97%D7%95%D7%91%D7%A8%D7%AA%20%D7%94%D7%9E%D7%9B%D7%A8%D7%96"
FONT = "font-family:'IBM Plex Sans Hebrew','IBM Plex Sans',system-ui,sans-serif"; MONO = "font-family:'IBM Plex Mono',ui-monospace,monospace"
INK, INK2, BLUE, GRID = "#12202A", "#3E4C58", "#1F4FA3", "#B9C3CB"


def t(x, y, s, anchor="start", size=13, weight=400, fill=INK, mono=False):
    return '<text x="%s" y="%s" text-anchor="%s" style="%s;font-size:%spx;font-weight:%s" fill="%s">%s</text>' % (x, y, anchor, MONO if mono else FONT, size, weight, fill, s)


L = D["lists"]
ROWS = [(k, L[k]) for k in ("build", "reno", "frame", "renox", "house")]
NUM = {"build": 44000, "reno": 40000, "frame": 48000, "renox": 48000, "house": 2200}  # the item counts dekel.co.il states ("כ-" / "מעל")
for k, x in ROWS: assert str(NUM[k])[:2] in x["items"].replace(",", ""), (k, x["items"])
g = ['<svg viewBox="0 0 420 252" direction="rtl" role="img" aria-label="מספר הסעיפים במחירוני דקל: בנייה ותשתיות כ-44,000, שיפוצים ואחזקה מעל 40,000, הסכמי מסגרת כ-48,000, שיפוצים מורחב כ-48,000, בנייה פרטית כ-2,200" style="display:block;width:100%;height:auto;max-width:640px;background:#fff">',
     t(408, 22, "כמה סעיפים יש בכל מחירון של דקל", size=15, weight=600), t(408, 42, "לפי אתר דקל, 25.10.2026", size=12, fill=INK2)]
for i, (k, x) in enumerate(ROWS):
    y = 62 + i * 36; w = 190 * NUM[k] / 48000.0
    g.append(t(408, y + 15, x["name"].replace("מחירון דקל ", "").replace("מחירון ", ""), size=13, weight=600))
    g.append('<rect x="%.1f" y="%d" width="%.1f" height="20" fill="%s"/>' % (220 - w, y, w, BLUE))
    g.append(t(214 - w, y + 15, x["items"], size=12.5, fill=BLUE, weight=600))
g.append('</svg>')
CHART = '<figure class="nlq4-fig" style="margin:20px 0">%s<figcaption style="font-size:14px;color:#3E4C58;margin-top:6px">%s</figcaption></figure>\n' % ("".join(g), "התוכנה עובדת עם המחירונים. המספרים כפי שדקל מציינת אותם.")
TBL = ("<figure class=\"wp-block-table\"><table><caption>המחירונים שתוכנת דקל עובדת איתם (לפי אתר דקל, 25.10.2026)</caption><thead><tr><th scope=\"col\">המחירון</th><th scope=\"col\">פרקים</th><th scope=\"col\">סעיפים</th><th scope=\"col\">היקף שהמחירים מכוונים אליו</th></tr></thead><tbody>"
       + "".join("<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td>%s</td></tr>" % (x["name"], x.get("ch", "") or "", x["items"], ("%s עד %s ₪" % ("{:,}".format(x["min"]), "{:,}".format(x["max"]))) if x.get("min") else "") for k, x in ROWS)
       + "</tbody></table></figure>\n")
A1 = "<h2>חלופות לתוכנת דקל</h2>"
INS1 = TBL + CHART
A2 = "מכאן שהתוכנה נפוצה אצל מי שמכין מסמכי מכרז ובודק חשבונות.</p>\n"
INS2 = ("<p>שתי דוגמאות ממסמכי מכרז שפורסמו: מכרז 42/2025 של משרד האנרגיה כותב שהמכרז מבוסס על מחירון דקל, ושהמציעים יכולים לפנות לדקל לקבלת הרשאות צפייה, שייתכן שהן בתשלום. "
        "מכרז המחירון השנתי של המרכז הרפואי שיבא משלם לפי מחירון דקל לבנייה ותשתיות במהדורה האחרונה, פחות אחוז ההנחה שהוצע.</p>\n"
        "<p><small>לבדיקה במקור: <a href=\"%s\" rel=\"noopener\">מכרז 42/2025 של משרד האנרגיה</a> · <a href=\"%s\" rel=\"noopener\">מכרז המחירון של המרכז הרפואי שיבא</a></small></p>\n" % (GOV, MR))
s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content,link" % PID)
raw = r["content"]["raw"]
assert raw.count(A1) == 1 and raw.count(A2) == 1 and "מכרז 42/2025" not in raw
new = raw.replace(A1, INS1 + A1).replace(A2, A2 + INS2)
vis = re.sub(r"<[^>]+>", " ", re.sub(r"<svg\b.*?</svg>", " ", new, flags=re.S))
assert not re.search(r"[–—]", vis)
print("[term %d] tables %d -> %d, svg %d -> %d" % (PID, raw.count("<table"), new.count("<table"), raw.count("<svg"), new.count("<svg")))
if DRY:
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "term-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/nadlan_term/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/nadlan_term/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"read-back": back.strip() == new.strip(), "gov link": GOV in page, "chart": "כמה סעיפים יש בכל מחירון של דקל" in page, "one FAQPage": page.count('"@type":"FAQPage"') == 1}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
