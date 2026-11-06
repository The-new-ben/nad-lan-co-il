# -*- coding: utf-8 -*-
"""MortgageWorld N, page 121 (HAD-675, Ben 6.11.2026: the whole mortgage universe in this one page; the bare word משכנתא / משכנתה
is the head keyword; manual SERP; Kol Zchut and the state sites pulled in; tools for registration and fees, the capitalization fee,
hardship and existing-property loans; a map so everything is reachable from everywhere, never floating).
Content only, additive; runs AFTER release 1.72.597 registers the new tools (only chips of registered tools are added: --tools=...).
  1. lead: one definition sentence with both spellings, and the date;
  2. the CTA row: a third link "כל נושאי המשכנתא" to the map;
  3. the switcher: the new chips and panes, and the count in the heading;
  4. the map section after the switcher, then "מה זה משכנתא, ומשכנתא או משכנתה";
  5. the amount ladder (32 amounts) inside "כמה ההחזר על משכנתא של מיליון";
  6. the official-fact chapters from facts_n.py (registration, fees, cancellation, capitalization fee, hardship, rights,
     existing property, banks, 2026 rules), each in its place on the borrower's path;
  7. a back-link to the map at the end of every chapter; the phone fold skips the map;
  8. FAQ additions; a DefinedTerm JSON-LD for משכנתא / משכנתה.
Nothing removed; every original line kept (edited lines in their edited form). python write_page_n.py --dry --tools=mhivun,... first."""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
import map_n, chapters_n  # noqa: E402
try:
    import facts_n  # noqa: E402  (written from the official-facts research; required for a live run)
except ImportError:
    facts_n = None
PID = 121
TOOLS = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--tools=")]
TOOLS = [t for t in (TOOLS[0] if TOOLS else []) if t]
CHIP = {"mhivun": ("tool-hivun", "עמלת היוון", 'עמלת ההיוון על כל ההלוואות במשכנתא שלכם, לפי צו הבנקאות והממוצעים של בנק ישראל: היום, בפירעון חלקי ובכל חודש בשנתיים הקרובות, עם כל שלב בחישוב.'),
        "mrishum": ("tool-rishum", "רישום משכנתה ואגרות", 'איפה רושמים את המשכנתה שלכם, אילו מסמכים צריך, כמה אגרות משלמים לפי טבלת 2026 ומי פטור, וגם ביטול המשכנתא אחרי הסילוק.'),
        "mkashe": ("tool-kashe", "כשקשה לשלם", 'כמה תעלה דחייה או הקפאה של תשלומי המשכנתא, מה קורה כשלא משלמים, ומה מגן עליכם בכל שלב לפי החוק.'),
        "mneches": ("tool-neches", "דירה קיימת", 'כמה בנק רשאי להלוות על הדירה שכבר יש לכם לפי כללי בנק ישראל, בכמה זה יעלה בחודש, ומה מגביל יותר: השווי או ההכנסה.')}
HEB_N = {9: "תשעה", 10: "עשרה", 11: "אחד עשר", 12: "שנים עשר", 13: "שלושה עשר"}

E = []  # (anchor, replacement) or ("SECTION_END:id" / "SECTION_CLOSE:id", html)
# 1. lead
E.append(('וגם הפוך: לפי ההחזר החודשי שמתאים לכם. משכנתא של <bdi>1,000,000 ₪</bdi>',
          'וגם הפוך: לפי ההחזר החודשי שמתאים לכם. משכנתא, ובכתיב הרשמי משכנתה, היא הלוואה לקניית דירה שהדירה משועבדת בה לבנק ונרשמת בטאבו עד הסילוק. משכנתא של <bdi>1,000,000 ₪</bdi>'))
# 2. CTA row
E.append(('<a class="nlu1-btn" href="#bank-offer-check">בדיקת הצעה מהבנק</a></div>',
          '<a class="nlu1-btn" href="#bank-offer-check">בדיקת הצעה מהבנק</a><a class="nlu1-btn" href="#mortgage-map">כל נושאי המשכנתא</a></div>'))
# 3. switcher
n_now = 9 + len(TOOLS)
if TOOLS:
    E.append(('<h2 id="nlmx-sw-h">ומה עוד בודקים: תשעה כלים למשכנתא</h2>', '<h2 id="nlmx-sw-h">ומה עוד בודקים: %s כלים למשכנתא</h2>' % HEB_N[n_now]))
    E.append(('aria-controls="tool-zakaut">מחשבון זכאות</button></div>',
              'aria-controls="tool-zakaut">מחשבון זכאות</button>' + "".join(
                  '<button type="button" data-sw="%s" aria-controls="%s">%s</button>' % (CHIP[t][0], CHIP[t][0], CHIP[t][1]) for t in TOOLS) + '</div>'))
    E.append(('[nadlan_tool id="mzakaut"]\n</div>\n</section>',
              '[nadlan_tool id="mzakaut"]\n</div>\n' + "".join(
                  '<div class="nlmx-pane" id="%s"><p>%s</p>\n[nadlan_tool id="%s"]\n</div>\n' % (CHIP[t][0], CHIP[t][2], t) for t in TOOLS) + '</section>'))
# 4. the map + the definition chapter, right after the switcher
nt, ns = map_n.counts()
E.append(("SECTION_END:tools", map_n.html(n_now + 3, ns) + chapters_n.WHAT))
# 5. the amount ladder
E.append(("SECTION_CLOSE:payment-per-million", chapters_n.ladder()))
# 6. the official-fact chapters
if facts_n:
    for where, html in facts_n.PLACES:
        E.append((where, html))
# 7. phone fold skips the map; back-links
E.append(('var skip={"tools":1,"mortgage-market":1,"mortgage-rules-facts":1,"faq":1};',
          'var skip={"tools":1,"mortgage-market":1,"mortgage-rules-facts":1,"faq":1,"mortgage-map":1};'))
for sid in ("mortgage-numbers-today", "offer-vs-average", "before-signing", "mortgages-this-month", "average-mortgage-rates",
            "payment-per-million", "uniform-baskets", "bank-of-israel-rules", "eligibility-loan", "mortgage-rules-facts",
            "spitzer-equal-balloon-grace", "cpi-prime-forecast", "early-repayment-refinance", "calculator-method"):
    E.append(("SECTION_CLOSE:" + sid, map_n.BACK))
# 8. FAQ
FAQ = chapters_n.FAQ_BASE + (facts_n.FAQ if facts_n else [])
E.append(("SECTION_CLOSE:faq", chapters_n.faq_html(FAQ)))
TERM = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": "https://nad-lan.co.il/mortgage-calculator/#mashkanta",
        "name": "משכנתא", "alternateName": ["משכנתה", "משכנתאות", "משכנתות"], "inLanguage": "he",
        "description": "הלוואה גדולה לטווח ארוך, בדרך כלל לקניית דירה, שהדירה משועבדת בה לבנק ונרשמת בטאבו עד שההלוואה נפרעת. בחוק: \"משכנתה היא מישכון של מקרקעין\" (חוק המקרקעין, התשכ\"ט-1969, סעיף 4).",
        "url": "https://nad-lan.co.il/mortgage-calculator/#what-is-mortgage"}
TERM_LD = '<script type="application/ld+json" id="nlx-term">' + json.dumps(TERM, ensure_ascii=False) + '</script>\n'

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns_ = {"__name__": "mw_n"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns_)
req = ns_["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert 'id="mortgage-map"' not in raw, "already written"
new = raw


def sec_bounds(txt, sid):
    m0 = re.search(r'<section\b[^>]*\bid="%s"' % re.escape(sid), txt)
    if not m0:
        raise SystemExit("no section " + sid)
    i = m0.start(); depth = 0
    for m in re.finditer(r'<section\b|</section>', txt[i:]):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return i, i + m.start(), i + m.end()
    raise SystemExit("unclosed " + sid)


for a, b in E:
    if a.startswith(("SECTION_END:", "SECTION_CLOSE:")):
        kind, sid = a.split(":", 1)
        assert len(re.findall(r'<section\b[^>]*\bid="%s"' % re.escape(sid), new)) == 1, sid
        i, c, e = sec_bounds(new, sid)
        new = (new[:e] + "\n" + b + new[e:].lstrip("\n")) if kind == "SECTION_END" else (new[:c] + b + new[c:])
    else:
        assert new.count(a) == 1, ("anchor", a[:60], new.count(a)); new = new.replace(a, b)
k = new.index('<p class="nlx-byline"')
new = new[:k] + TERM_LD + new[k:]
REPL = [(a, b) for a, b in E if not a.startswith("SECTION_")]
for line in raw.split("\n"):
    if not line.strip():
        continue
    ln = line
    for a, b in REPL:
        ln = ln.replace(a, b)
    assert ln in new, ("an original line is missing", line[:90])
vis = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", " ", "".join(b for a, b in E))
assert not re.search(r"[–—]", vis), "long dash"
for bad in ("סימולציה", "ממשק", "דמו", "הדגמה", "המערכת", "הפלטפורמה", "אטלס", "עולם המשכנתא"):
    assert not re.search(r"(?<![֐-׿])%s(?![֐-׿])" % bad, vis), bad
ids = re.findall(r'\bid="([^"]+)"', new)
dup = sorted({x for x in ids if ids.count(x) > 1}); assert not dup, ("duplicate ids", dup)
for href in re.findall(r'<a href="(#[^"]+)"', "".join(b for a, b in E)):
    tid = href[1:]
    if tid.startswith("tool-") and tid not in ids and not any(CHIP[t][0] == tid for t in TOOLS):
        print("   note: map link to a chip that is not on the page yet:", href)
    elif not tid.startswith("tool-") and tid not in ids and tid not in ("quick", "mortgage-market"):
        if facts_n:
            raise SystemExit("broken in-page link " + href)
        print("   note: chapter not written yet (facts_n missing):", href)
for href in sorted(set(re.findall(r'<a href="(/[^"#]*)"', "".join(b for a, b in E)))):
    st = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il" + href, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).status
    assert st == 200, ("guide link", href, st)
n_faq = len(re.findall(r"<h3>", new[new.index('<section id="faq"'):]))
print("[page %d] %d edits; content %d -> %d bytes; tools %s; FAQ h3 now %d" % (PID, len(E) + 1, len(raw), len(new), TOOLS, n_faq))
if DRY:
    io.open(os.path.join(H, "preview-content-n.html"), "w", encoding="utf-8", newline="").write(new); print("[dry] ok"); sys.exit(0)
assert facts_n, "facts_n.py is required for the live run"
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"map": 'id="mortgage-map"' in page and page.count('class="nlmap__d"') == 8, "definition": 'id="what-is-mortgage"' in page,
      "tools": all(('data-nli="%s"' % t) in page for t in TOOLS), "term": 'id="nlx-term"' in page,
      "byline last": page.find('class="nlx-byline"') > page.find('id="faq"'), "one h1": page[page.find("<body"):].count("<h1") == 1}
for k_, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k_)
