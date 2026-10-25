# -*- coding: utf-8 -*-
"""U3: full rewrite of /israel-mortgage-non-residents/ (post 4962, an English article on a root URL) to the dna.md 8.3 order.

Decision (Ben, via the coordinator, 26.10.2026): the page stays at its URL and stays English (no second English page, no redirect, no
noindex); lang="en" dir="ltr" comes from a separate code release (a page meta override). This script writes the CONTENT only:
  - the 17 sections of dna.md 8.3 plus the related links; tables T1 to T10 (and the benchmarks, the 10% shekel test and the glossary);
    infographics 1 to 3 and the 2026 rate chart (infographics.py); the 25 questions of 8.8 under the H2 the site's FAQPage builder reads
    (inc/instruments.php nadlan_nli_faq: "Frequently asked questions..." then h3 + p);
  - the calculator mount [nadlan_tool id="nrm"] kept, under H2 "Israeli mortgage calculator for foreign buyers" (section 2);
  - the in-content JSON-LD: Person kept as it is live, Article updated, Dataset added for the rate tables, the old 5-question FAQPage
    removed (the site prints the FAQPage from the visible questions; two FAQPage blocks would compete);
  - post title (the H1) and Yoast title + meta description per 8.2.
Additive law: every section, fact and feature of the live page survives (SURVIVAL below is asserted against the new content); the one
dead link (/transfer-money-to-israel-property/, 404 on 26.10.2026) is not carried over, its paragraph is.
Every number is computed here and asserted against dna.md (section 6 facts, 8.4 tables, 8.8 answers).

  python docs/research/2026-10-26-upgrades/u3-en-mortgage/write_u3_page.py --dry   GET only, gates, preview/u3-page-content.html
  python docs/research/2026-10-26-upgrades/u3-en-mortgage/write_u3_page.py         backup, POST, read-back, live check"""
import hashlib, io, json, os, re, sys, time, urllib.parse, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
import infographics as ig
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID, TYPE, SITE, WA = 4962, "posts", "https://nad-lan.co.il", "972525101555"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
_t = time.localtime(); UPDATED = "%d %s %d" % (_t.tm_mday, MONTHS[_t.tm_mon - 1], _t.tm_year); UPDATED_ISO = time.strftime("%Y-%m-%d")

# ------------------------------------------------------------------ facts (dna.md section 6, verified 25.10.2026)
FX = {"USD": 3.112, "EUR": 3.4844, "GBP": 4.1624}                      # Bank of Israel representative rates, 23 Oct 2026
FX30 = {"USD": (3.017, 3.112), "EUR": (3.4291, 3.4919), "GBP": (4.0068, 4.1624)}  # 30 days from 23 Sep 2026
SYM = {"USD": "$", "EUR": "€", "GBP": "£"}
FXL = "Bank of Israel rate of 23 Oct 2026"
RATE = 4.62                                                            # fixed not linked, average new loans, August 2026
T4A = [("Fixed, not linked (kalatz)", [4.77, 4.73, 4.63, 4.62], ""),
       ("Fixed, CPI-linked, plus inflation", [3.31, 3.27, 3.22, 3.29], ""),
       ("Variable, CPI-linked, plus inflation", [(1.94, 1.49), (1.84, 1.44), (1.68, 1.49), (1.64, 1.55)], "benchmark + margin"),
       ("All CPI-linked tracks", [3.35, 3.28, 3.20, 3.26], ""),
       ("Foreign currency linked", [5.05, 4.46, 4.98, 4.86], "")]
TERM_NL = [("All terms, average", 4.55), ("Up to 1 year (includes prime)", 4.35), ("1 to 5 years", 4.51), ("5 to 10 years", 4.59),
           ("10 to 15 years", 4.61), ("15 to 20 years", 4.74), ("20 to 25 years", 4.79), ("Over 25 years", 4.89)]
TERM_CPI = {"All terms, average": "3.49%", "Up to 1 year (includes prime)": "in up to 5 years", "1 to 5 years": '3.50%<br><span class="s">up to 5 years</span>',
            "5 to 10 years": "3.49%", "10 to 15 years": "3.24%", "15 to 20 years": "3.46%", "20 to 25 years": "3.37%", "Over 25 years": "3.53%"}
BOI, PRIME, CPI12, NEXT = 3.25, 4.75, 1.6, "23 November 2026"
FOREIGN_TOP = 6055070
RES = [(1978745, 0.0), (2347040, 0.035), (6055070, 0.05), (20183565, 0.08), (10 ** 12, 0.10)]   # instruction 1/2026, frozen to 15.1.2028
OLEH = [(1978745, 0.0), (6055070, 0.005), (20183565, 0.08), (10 ** 12, 0.10)]                  # reg. 12A (no relief above 20,183,565)
FEES = 4000000 * 0.005 * 1.18 + 650 + 360   # lawyer 0.5% + 18% VAT; appraiser 650 and file fee 360: typical, unverified (dna 6, nrm.json)


def pmt(p, annual, years):
    r = annual / 1200.0; n = years * 12
    return p * r / (1 - (1 + r) ** -n)


def brackets(price, b):
    tax, lo = 0.0, 0
    for hi, r in b:
        tax += max(0, min(price, hi) - lo) * r; lo = hi
    return tax


def foreign_tax(price): return 0.08 * min(price, FOREIGN_TOP) + 0.10 * max(0, price - FOREIGN_TOP)
def ils(v): return "₪{:,.0f}".format(round(v))
def cur(v, c="USD"): return "{}{:,.0f}".format(SYM[c], round(v / FX[c]))
def num(v): return "{:,.0f}".format(round(v))


# T3: the income test
T3 = []
for P in (1000000, 2000000, 3000000):
    m = pmt(P, RATE, 25); T3.append((P, m, m * 2, m * 3))
assert [round(x[1]) for x in T3] == [5627, 11253, 16880], [round(x[1]) for x in T3]
assert round(T3[1][2]) == 22507 and round(T3[1][3]) == 33760 and cur(T3[1][2]) == "$7,232" and cur(T3[1][3]) == "$10,848"
# T5: cash to close on 4,000,000
PRICE = 4000000
ST = [("Not an Israeli citizen", 0.50, foreign_tax(PRICE), "8% foreign resident"),
      ("Israeli citizen living abroad, first home", 0.75, foreign_tax(PRICE), "8% foreign resident"),
      ("New oleh living in Israel", 0.75, brackets(PRICE, OLEH), "oleh relief, reg. 12A"),
      ("Israeli citizen living in Israel, single home", 0.75, brackets(PRICE, RES), "single home brackets")]
T5 = []
for name, ltv, tax, track in ST:
    loan = PRICE * ltv; close = PRICE - loan + tax + FEES; m = pmt(loan, RATE, 25)
    T5.append(dict(name=name, ltv=ltv, loan=loan, cash=PRICE - loan, tax=tax, track=track, close=close, m=m))
assert round(FEES) == 24610
assert [round(x["close"]) for x in T5] == [2344610, 1344610, 1034716, 1120148]
assert [round(x["tax"]) for x in T5] == [320000, 320000, 10106, 95538]
assert [cur(T5[0]["close"], c) for c in ("USD", "EUR", "GBP")] == ["$753,409", "€672,888", "£563,283"]
assert cur(T5[1]["close"]) == "$432,073" and cur(T5[2]["close"]) == "$332,492" and cur(T5[3]["close"]) == "$359,945"
assert cur(T5[0]["m"]) == "$3,616" and round(T5[1]["m"]) == 16880 and cur(T5[1]["m"]) == "$5,424"
# the 10% shekel test on 11,253
M2 = T3[1][1]
SWING = {c: (M2 / FX[c], M2 / (FX[c] * 1.1), M2 / (FX[c] * 0.9)) for c in FX}
assert [round(v) for v in SWING["USD"]] == [3616, 3287, 4018]
# FAQ numbers
H300 = 300000 * FX["USD"]
assert (round(H300), round(H300 / 2), round(foreign_tax(H300)), round(H300 * 0.25), round(brackets(H300, RES))) == (933600, 466800, 74688, 233400, 0)
L500 = 500000 * FX["USD"]; P500 = pmt(L500, RATE, 30)
assert round(L500) == 1556000 and round(P500) == 7995 and round(P500 / FX["USD"]) == 2569
assert (foreign_tax(3000000), foreign_tax(4000000)) == (240000, 320000)
assert 0.5 * 0.75 + 0.5 * 0.5 == 0.625
assert [round(a + b, 2) for a, b in T4A[2][1]] == [3.43, 3.28, 3.17, 3.19]
GAP = T5[0]["close"] - T5[2]["close"]; assert 1300000 < GAP < 1310000
LINKED_COST = (1 + 0.0329) * (1 + 0.02) - 1; assert 0.053 < LINKED_COST < 0.054   # 3.29% + the 2.0% forecast, our arithmetic

# ------------------------------------------------------------------ HTML helpers
LINK = {  # internal: every one is checked for 200 below
    "buy_en": "/en/buy-property-in-israel/", "ptax": "/israel-purchase-tax-foreign-residents/", "projects_en": "/en/projects/",
    "new_en": "/en/new-projects/", "buy_foreign": "/buy-property-israel-foreign-buyers/", "investor": "/buying-real-estate-israel-foreign-investor/",
    "calc_he": "/mortgage-calculator/", "lawyer": "/real-estate-lawyer/", "author": "/author/ben-betesh/"}
EXT = {  # official and bank pages (read 25.10.2026; gov.il answers 403 to scripts, read by eye)
    "d329": "https://www.boi.org.il/media/ez4npagt/329.pdf", "d329qa": "https://boi.org.il/roles/supervisionregulation/nbt/nbt329/",
    "d451": "https://www.boi.org.il/media/ptchkgxk/451-1-1.pdf",
    "reform": "https://www.boi.org.il/en/information-and-service-to-the-public/banking-customer-service-information/financial-education/the-reform-to-increase-information-transparency-and-competition-in-mortgages/",
    "press": "https://www.boi.org.il/en/communication-and-publications/press-releases/21-10-26ben/",
    "dates": "https://www.boi.org.il/roles/monetary-policy/interest-rate-dates/",
    "avg": "https://www.boi.org.il/he/economic-roles/financial-markets/interestrates/mortgage",
    "mashfix": "https://www.boi.org.il/boi_files/Pikuah/mashfix.xls", "pribmash": "https://www.boi.org.il/boi_files/Pikuah/pribmash.xls",
    "fx": "https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/",
    "compare": "https://www.boi.org.il/en/information-and-service-to-the-public/interest-rates-and-early-repayment-fees/interest-rate-comparisons-housing-loans/",
    "account": "https://boi.org.il/en/questions-and-answers/consumer-information/current-account-general-information/",
    "oleh": "https://boi.org.il/media/xjvffmz5/201802_en.pdf",
    "landtax": "https://he.wikisource.org/wiki/" + urllib.parse.quote("חוק_מיסוי_מקרקעין_(שבח_ורכישה)"),
    "aml": "https://he.wikisource.org/wiki/" + urllib.parse.quote("צו_איסור_הלבנת_הון_(חובות_זיהוי,_דיווח_וניהול_רישומים_של_תאגידים_בנקאיים_למניעת_הלבנת_הון_ומימון_טרור)"),
    "early": "https://he.wikisource.org/wiki/" + urllib.parse.quote("צו_הבנקאות_(פירעון_מוקדם_של_הלוואה_לדיור)"),
    "service": "https://he.wikisource.org/wiki/" + urllib.parse.quote("חוק_הבנקאות_(שירות_ללקוח)"),
    "consumer": "https://he.wikisource.org/wiki/" + urllib.parse.quote("חוק_הגנת_הצרכן"),
    "taxnotice": "https://www.gov.il/he/pages/pa121026-2",
    "inst1": "https://www.gov.il/BlobFolder/policy/inst-01-2026/he/realestate_inst-01-2026.pdf",
    "taxguide": "https://www.gov.il/BlobFolder/generalpage/guide-for-seller-right-in-land/he/Guides_knowrightinland_2026.pdf",
    "notary": "https://www.gov.il/en/service/notary_authorization", "cbs": "https://www.cbs.gov.il/en/Pages/default.aspx",
    "mz_imc": "https://www.mizrahi-tefahot.co.il/en/mortgages/", "mz_qa": "https://www.mizrahi-tefahot.co.il/en/about-mizrahi-tefahot/qa-mortgages-in-israel/",
    "discount": "https://www.discountbank.co.il/en/private-banking/international-private-banking/mortgage-private-banking/",
    "boj": "https://www.bankjerusalem.co.il/en/forex/non-resident-account"}


def a(key, text): return '<a href="%s">%s</a>' % (LINK[key], text)
def x(key, text): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (EXT[key], text)
def h2(i, s): return '<h2 id="%s">%s</h2>\n' % (i, s)
def h3(s, i=""): return '<h3%s>%s</h3>\n' % (' id="%s"' % i if i else "", s)
def p(s, cls=""): return '<p%s>%s</p>\n' % (' class="%s"' % cls if cls else "", s)
def ul(items): return "<ul>\n" + "".join("<li>%s</li>\n" % i for i in items) + "</ul>\n"


NUMCELL = re.compile(r"^(?:≈ ?)?[₪$€£]?\d[\d,.]*%?$")


def cell(c, tag="td"):
    span = ""
    if isinstance(c, tuple): c, n = c; span = ' colspan="%d"' % n
    cls = ' class="n"' if tag == "td" and NUMCELL.match(re.sub(r"<[^>]+>", "", c.split("<br>")[0]).strip()) else ""
    return "<%s%s%s>%s</%s>" % (tag, span, cls, c, tag)


def table(title, src, head, rows, wide=False):
    hh = "".join('<th scope="col">%s</th>' % c for c in head)
    bb = "".join("<tr>" + '<th scope="row">%s</th>' % r[0] + "".join(cell(c) for c in r[1:]) + "</tr>" for r in rows)
    return ('<figure class="wp-block-table"><table%s><caption><strong>%s</strong> %s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table></figure>\n'
            % (' class="nlu3-wide"' if wide else "", title, src, hh, bb))


def fig(svg, cap): return '<figure class="nlu3-fig">%s<figcaption>%s</figcaption></figure>\n' % (svg, cap)


STYLE = ("<style>.nlu3{color:#2B3440}.nlu3 figure.wp-block-table{margin:22px 0;overflow-x:auto;-webkit-overflow-scrolling:touch}"
         ".nlu3 figure.wp-block-table table{display:table;width:100%;border-collapse:collapse;font-size:15px;line-height:1.45;margin:0}"
         ".nlu3 figure.wp-block-table table.nlu3-wide{min-width:640px}"
         ".nlu3 caption{caption-side:top;text-align:left;font-size:13.5px;line-height:1.45;color:#4A5563;padding:0 0 8px;max-width:calc(100vw - 48px)}"
         ".nlu3 table.nlu3-wide tbody th{min-width:118px}"
         ".nlu3 td .s{display:inline-block;white-space:normal;font-family:'Public Sans','IBM Plex Sans',system-ui,sans-serif;font-size:13px;color:#4A5563;margin-top:2px}"
         ".nlu3 caption strong{display:block;color:#1E2B47;font-size:16px;margin-bottom:2px}"
         ".nlu3 th,.nlu3 td{padding:9px 10px;border-bottom:1px solid #C9D2DC;text-align:left;vertical-align:top}"
         ".nlu3 thead th{background:#1E2B47;color:#fff;font-weight:600;font-size:14px}"
         ".nlu3 tbody th{background:#F6F8FA;font-weight:600;color:#1E2B47}"
         ".nlu3 td.n{font-family:'IBM Plex Mono',ui-monospace,Consolas,monospace;font-size:14px;white-space:nowrap}"
         ".nlu3 .nlu3-fig{margin:26px 0}.nlu3 .nlu3-fig figcaption{font-size:14px;color:#4A5563;margin-top:6px}"
         ".nlu3 .nlu3-by{font-size:14px;color:#4A5563}"
         ".nlu3 .nlu3-strip{border:1px solid #1E2B47;background:#F6F8FA;margin:18px 0}"
         ".nlu3 .nlu3-strip .h{background:#1E2B47;color:#fff;font-size:13px;letter-spacing:.02em;padding:7px 12px;margin:0}"
         ".nlu3 .nlu3-strip .g{display:grid;grid-template-columns:repeat(3,1fr)}@media (max-width:560px){.nlu3 .nlu3-strip .g{grid-template-columns:repeat(2,1fr)}}"
         ".nlu3 .nlu3-strip .i{padding:10px 12px;border-top:1px solid #C9D2DC;border-right:1px solid #C9D2DC;margin:0}"
         ".nlu3 .nlu3-strip .l,.nlu3 .nlu3-strip .d{display:block;font-size:13px;color:#4A5563;line-height:1.35}"
         ".nlu3 .nlu3-strip .v{display:block;font-family:'IBM Plex Mono',ui-monospace,Consolas,monospace;font-size:22px;font-weight:600;color:#1E2B47;line-height:1.3}"
         ".nlu3 .nlu3-strip .fx{padding:9px 12px;border-top:1px solid #C9D2DC;font-size:14px;margin:0}"
         ".nlu3 .nlu3-strip .fx b{font-family:'IBM Plex Mono',ui-monospace,Consolas,monospace;color:#1E2B47;white-space:nowrap}"
         ".nlu3 .nlu3-cta{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 26px}"
         ".nlu3 .nlu3-cta a{display:inline-block;padding:12px 16px;font-weight:600;text-decoration:none;border:2px solid #1E2B47;line-height:1.3}"
         ".nlu3 .nlu3-cta a.p{background:#1E2B47;color:#fff}.nlu3 .nlu3-cta a.s{background:#fff;color:#1E2B47}"
         ".nlu3 .nlu3-toc{border-left:3px solid #0F7C7A;padding:4px 0 4px 14px;margin:24px 0}.nlu3 .nlu3-toc ul{margin:6px 0 0;padding-left:18px}"
         ".nlu3 .nlu3-he{font-family:inherit;white-space:nowrap}</style>")

# ------------------------------------------------------------------ copy
H1 = "Israel Mortgage for Foreigners and Non-Residents: What You Can Borrow"
SEO_TITLE = "Israel Mortgage for Foreigners 2026: Rates, LTV, Calculator"
META = "How much an Israeli bank lends foreigners, Israelis abroad and new olim: Bank of Israel caps, August 2026 average rates, cash to close in $, € or £."
assert len(SEO_TITLE) <= 60 and 140 <= len(META) <= 156, (len(SEO_TITLE), len(META))
WATXT = urllib.parse.quote("Hello, I read the guide to Israeli mortgages for foreigners and would like a lawyer to check my numbers.")

TOP = (p("An Israel mortgage for foreigners is capped at 50% of the home's value: Bank of Israel Directive 329 treats any buyer without Israeli "
         "citizenship as buying an investment home. Israeli citizens living abroad and registered new olim can borrow up to 75% for a first "
         "Israeli home. Average fixed rate: 4.62% (August 2026).")
       + p("In Hebrew the loan is a <em>mashkanta</em>. Two limits apply and the lower one wins: the cap for your status, and a monthly payment of "
           "no more than 50%% of your disposable income. A ₪2,000,000 loan over 25 years at the August 2026 average fixed rate costs %s a month "
           "(≈ %s). On a ₪4,000,000 home, a buyer without Israeli citizenship needs about %s in cash to close, including the 8%% purchase tax a "
           "foreign resident pays (≈ %s; dollar figures approx., %s)." % (ils(M2), cur(M2), ils(T5[0]["close"]), cur(T5[0]["close"]), FXL))
       + p('By %s, Israeli real estate lawyer, Israel Bar licence 29020 · first published 2 July 2026, updated %s · rates checked 25 October 2026; '
           'next Bank of Israel decision %s' % (a("author", "Adv. Ben Betesh"), UPDATED, NEXT), "nlu3-by")
       + '<div class="nlu3-strip"><p class="h">Bank of Israel figures, checked 25 October 2026</p><div class="g">'
       + "".join('<p class="i"><span class="l">%s</span><span class="v">%s</span><span class="d">%s</span></p>' % i for i in (
           ("Bank of Israel rate", "3.25%", "in force since 3 Sep 2026"), ("Prime", "4.75%", "Bank of Israel rate + 1.5"),
           ("Fixed, not linked", "4.62%", "average new loans, Aug 2026"), ("Foreign currency loans", "4.86%", "average new loans, Aug 2026"),
           ("Most a non-citizen can borrow", "50%", "of the value, Directive 329"), ("Next rate decision", "23 Nov", "2026")))
       + '</div><p class="fx">%s: <b>$1 = ₪3.112</b> · <b>€1 = ₪3.4844</b> · <b>£1 = ₪4.1624</b></p></div>\n' % FXL
       + '<p class="nlu3-cta"><a class="p" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">Check my numbers with a lawyer on WhatsApp</a>'
         '<a class="s" href="#calculator">Open the calculator</a></p>\n' % (WA, WATXT))

SEC = []  # (id, h2 text, html) in the 8.3 order
SEC.append(("calculator", "Your borrowing limit by passport and paycheck",
            p("Choose your status (not an Israeli citizen, an Israeli citizen with or without a home in Israel, a new oleh, or a couple of mixed "
              "status), then the price of the home or the cash you have, your currency and your net monthly income. The calculator returns the most "
              "you can borrow and which limit binds you, the Bank of Israel cap for your status or your income, the monthly payment in shekels and "
              "in your currency, the purchase tax on the right track for your residency, the cash you need to close, and your payment if the shekel "
              "moves 10% either way, all at the Bank of Israel rate of the day. The sections below work the same arithmetic by hand for each buyer "
              "status, so you can check any figure before you speak to a bank.")
            + '[nadlan_tool id="nrm"]\n'))

T1 = table("Loan cap by buyer status",
           "Bank of Israel Directive 329 (version 13, June 2026), sections 1, 2 and 4A, and the Bank of Israel questions and answers on the "
           "directive (question 2.4 and the answer on joint buyers), read 25 Oct 2026. The 62.5% is our arithmetic.",
           ["Buyer status", "Loan cap", "What decides it (source)"], [
               [st, cap, '%s<br><span class="s">%s</span>' % (why, srcl)] for st, cap, why, srcl in (
                   ("Not an Israeli citizen, any home", "50%", "Single and replacement homes are defined only for Israeli citizens, so any home a foreign resident buys is an investment home", "Directive 329 s.1, s.2; Q&amp;A 2.4"),
                   ("Israeli citizen (including a registered oleh), only home in Israel", "75%", "The home is your household's only home in Israel and the Area", "Directive 329 s.1, s.2; Land Taxation Law s.9"),
                   ("Israeli citizen replacing a home you will sell", "70%", "You own a home in Israel and will sell it", "Directive 329 s.1, s.2"),
                   ("Israeli citizen who already owns a home in Israel", "50%", "A home that is neither single nor replacement is an investment home", "Directive 329 s.1, s.2"),
                   ("Two buyers of different status, separate buyers for tax", "Weighted by share (50/50: 62.5%)", "The Bank of Israel follows the Tax Authority's view of who is a separate buyer", "Q&amp;A on joint buyers"),
                   ("Reduced-price homes (Mechir Lamishtaken, Mechir Matara)", "Own money of at least ₪100,000", "₪60,000 where the new Mechir Lamishtaken grant applies", "Directive 329 s.4A"))])
SEC.append(("ltv-what-non-residents-can-actually-borrow", "How much an Israeli bank can lend you, by status",
            p("Israeli banks do lend to buyers who live abroad. What surprises most of them is how the loan is built: the cap depends on your "
              "citizenship, not on where you live; part of the loan may be linked to the consumer price index; at least a third has to sit on a "
              "fixed rate; you need an Israeli bank account before the money is paid out; and life insurance assigned to the bank is a condition.")
            + p("Bank of Israel %s sets three caps on the loan as a share of the home's value: 75%% for a single home, 70%% for a replacement home and "
                "50%% for an investment home. The first two are defined only for an individual Israeli citizen. A single home is the buyer's only "
                "home in Israel and the Area, and the household counts as one buyer: you, your spouse unless you live permanently apart, and your "
                "children under 18 unless they are married." % x("d329", "Directive 329"))
            + p("The Bank of Israel's own %s closes the question for foreigners: because single and replacement homes are defined only for an "
                "Israeli citizen, a home bought by a foreign resident \"is necessarily an investment home\". That is why a buyer without Israeli "
                "citizenship gets 50%%, even for a first and only home here." % x("d329qa", "questions and answers on the directive"))
            + p("\"Israeli citizen\" in the directive is a legal term borrowed from section 16A of the %s. It covers anyone registered, or required "
                "to be registered, in the Population Registry; an individual who is an Israeli resident; and a person entitled to make aliyah under "
                "the Law of Return who lives in the Area. The Bank of Israel applies these words as written and declines to interpret them, so on a "
                "borderline case the bank's answer is the one that counts. Ask for it in writing." % x("landtax", "Land Taxation Law"))
            + T1
            + fig(ig.rulebooks_svg(RES[0][0], FOREIGN_TOP, "10 Feb 2027"),
                  "Citizenship by residency: the loan cap and the purchase tax track for each. A non-citizen living in Israel is covered by the "
                  "directive's definition as an Israeli resident; the bank's practice is not published, so ask in writing.")
            + p("The value the bank lends against is the lower of the contract price and its own appraisal. If the appraiser values the home below "
                "the price you agreed, the loan shrinks and the gap comes out of your cash, even though the seller still expects the full price. "
                "Check the financing before you sign, not after the payment schedule is binding. For a buyer abroad the gap is sharper, because the "
                "extra money has to pass source of funds checks when it arrives from abroad.")
            + p("Banks say the same in their own words. Mizrahi-Tefahot's %s say olim get up to 75%% instead of the 50%% they would get as foreign "
                "citizens, if they are Israeli citizens or entitled to Israeli citizenship. The directive's own test is the definition above, so "
                "treat \"entitled\" as a question for the bank, not a promise. For olim and diaspora buyers, status planning is part of mortgage "
                "planning, not only a tax question." % x("mz_qa", "English questions and answers"))))

T2 = table("Your status under both rulebooks",
           "Directive 329 s.1, s.2 and its questions and answers; Land Taxation Law s.9 and s.16A; Tax Authority notice of 12 Oct 2026 (foreign "
           "resident rate to 10 Feb 2027) and instruction 1/2026 (single home and oleh brackets, frozen to 15 Jan 2028); read 25 Oct 2026.",
           ["Your situation", "Loan cap (Directive 329)", "Purchase tax track", "Ask the bank in writing"], [
               ["Not an Israeli citizen, living abroad", "50%, any home", "Foreign resident: 8% up to ₪6,055,070 and 10% above, for purchases until 10 Feb 2027", "The cap, the currency of the loan, and whether it offers a foreign currency loan"],
               ["Israeli citizen living abroad, no home in Israel", "75%", "Foreign resident: 8% and 10%, because for tax you are not an Israeli resident", "That your registration in the Population Registry is accepted as citizenship"],
               ["Israeli citizen living abroad who owns a home in Israel", "50%, or 70% if you will sell the home you own", "Additional home: 8% and 10%", "The conditions of the replacement home cap"],
               ["New oleh living in Israel, first home", "75%", "Oleh relief, regulation 12A: 0% up to ₪1,978,745, 0.5% up to ₪6,055,070, 8% up to ₪20,183,565; from 1 year before to 7 years after aliyah", "That your oleh certificate and registration are in the file before the approval in principle"],
               ["Israeli citizen living in Israel, single home", "75%", "Single home: 0% up to ₪1,978,745, 3.5% up to ₪2,347,040, 5% up to ₪6,055,070, 8% up to ₪20,183,565, 10% above", "The appraisal and the payment test"],
               ["Couple: one Israeli citizen, one not", "Weighted by share if you are separate buyers for tax (50/50: 62.5%)", "Spouses count as one buyer for the single home test; how a couple with one foreign spouse is taxed is a question for your lawyer", "How the bank will treat your household, before you sign"]], wide=True)
SEC.append(("two-rulebooks", "Two rulebooks: citizenship sets your loan, residency sets your tax",
            p("Two Israeli authorities look at you through different windows. The Bank of Israel sizes your loan by citizenship. The Tax Authority "
              "sizes your purchase tax by residency. The two tests do not have to agree, and for Israelis who live abroad they usually do not.")
            + p("Take an Israeli citizen who lives in London and buys a first home in Tel Aviv for ₪4,000,000. For the bank he is an Israeli citizen "
                "buying a single home, so he can borrow 75%%, %s. For the Tax Authority he is not an Israeli resident, so he pays the foreign "
                "resident rate, 8%% up to ₪6,055,070 and 10%% above, from the first shekel: %s on this home. A buyer without citizenship pays the "
                "same %s but can borrow only %s. A new oleh who lives in Israel can borrow %s and, under the oleh relief, pays %s."
                % (ils(T5[1]["loan"]), ils(T5[1]["tax"]), ils(T5[0]["tax"]), ils(T5[0]["loan"]), ils(T5[2]["loan"]), ils(T5[2]["tax"])))
            + p("The foreign resident rate of 8%% and 10%% is a temporary order, %s to purchases until 10 February 2027 inclusive. According to the "
                "%s, a foreign resident who becomes an Israeli resident within two years of buying can be treated as a resident for the single home "
                "test and claim the difference back. Tax filing has its own clock: the declaration goes in within 30 days of the deal, and the tax "
                "falls due 60 days from it. The purchase tax itself is covered in our guide to %s."
                % (x("taxnotice", "extended"), x("taxguide", "Tax Authority's 2026 guide for buyers and sellers"), a("ptax", "purchase tax for foreign residents")))
            + T2
            + p("Do not confuse the loan cap with the tax. The bank may treat you as an investor while the Tax Authority treats you as a single home "
                "buyer, or the other way round. Both land on the same budget, so work out the loan, your own money and the purchase tax together "
                "before you commit to a price.")))

T3T = table("Net monthly income a loan needs, 25 years, fixed not linked at 4.62% (August 2026 average)",
            "Our arithmetic on Directive 329 s.5 (payment at most 50%% of disposable income) and Discount Bank's English page (about one third "
            "at most banks). $, € and £ approx., %s." % FXL,
            ["Loan and monthly payment", "Test", "Net income needed", "≈ $", "≈ €", "≈ £"],
            [r for P, m, cap, third in T3 for r in (
                ["%s: %s a month" % (ils(P), ils(m)), "50% legal cap", ils(cap), cur(cap), cur(cap, "EUR"), cur(cap, "GBP")],
                ["%s: %s a month" % (ils(P), ils(m)), "One third", ils(third), cur(third), cur(third, "EUR"), cur(third, "GBP")])], wide=True)
SEC.append(("income-test", "The income test: 50% by law, about one third in practice, in your currency",
            p("The second limit is your income. Directive 329 caps the monthly payment at 50% of disposable income, which is net income minus fixed "
              "commitments that will run for more than 18 months, such as other loans. Above 40%, the directive makes the bank set more capital "
              "aside for the loan, so many banks stop well below the legal cap. Discount Bank's English page says most banks offer up to about one "
              "third. In August 2026 the average new mortgage in Israel took 29.23% of the borrowers' income.")
            + p("The payment is in shekels, so the income behind it is counted in shekels too. If you earn in dollars, euros or pounds, what you "
                "need changes with the exchange rate. The table shows the net household income each loan needs at the legal cap and at one third, "
                "in shekels and converted at the %s." % FXL)
            + T3T
            + p("Two notes. Other debts lower the result: every shekel of fixed monthly commitments that will run for more than 18 months comes off "
                "your income before the test. And the test is not the whole decision: banks also look at your assets, how stable your income is "
                "and your age at the end of the loan, each under its own credit policy.")))

T4AT = table("Average rates on new housing loans, May to August 2026, by track",
             "Bank of Israel, new housing loans of the whole banking system, read 25 Oct 2026 (August is the latest month published). Variable "
             "CPI-linked = the Bank of Israel benchmark plus the average margin.",
             ["Track", "May 2026", "June 2026", "July 2026", "August 2026"],
             [[name] + [("%.2f%%" % (v[0] + v[1]) + ('<br><span class="s">%.2f + %.2f</span>' % v if i == 3 else "")) if isinstance(v, tuple) else "%.2f%%" % v
                        for i, v in enumerate(vals)] for name, vals, note in T4A]
             + [["Prime", ("4.75% since 3 Sep 2026: the Bank of Israel rate plus 1.5. Each bank adds or subtracts its own spread; no official average spread is published.", 4)]],
             wide=True)
T4BT = table("Average mortgage rates by term, reporting month September 2026, in force from 19 Oct 2026",
             "Bank of Israel, average rates on shekel mortgages, not linked and CPI-linked, read 25 Oct 2026. Effective annual averages; your offer "
             "depends on your file.", ["Term", "Not linked (fixed and variable)", "CPI-linked"],
             [[lab, "%.2f%%" % r, TERM_CPI[lab]] for lab, r in TERM_NL])
BENCH = table("The rate benchmarks, checked 25 Oct 2026",
              "Bank of Israel (rate decisions; October 2026 forecast, press release of 21 Oct 2026); Central Bureau of Statistics (consumer price index).",
              ["Benchmark", "Value", "What it means"], [
                  ["Bank of Israel rate", "3.25% since 3 Sep 2026", "The central anchor; prime moves with it"],
                  ["Prime", "4.75%", "The Bank of Israel rate plus 1.5; the base of every prime track"],
                  ["Inflation, 12 months to September 2026", "1.6%", "The backdrop for CPI-linked tracks"],
                  ["Bank of Israel forecast, October 2026", "Rate 3.0% on average in Q3 2027; inflation 2.0% over the next four quarters", "A forecast, not a promise"],
                  ["Next rate decision", NEXT, "When prime can next move"]])
SEC.append(("rates-in-2026-and-the-linkage-trap", "Mortgage rates in Israel today, by track and by term",
            p("Israeli mortgage rates are read through three numbers: the Bank of Israel rate, the prime rate built on it, and the rate each track "
              "of your loan carries. The Bank of Israel rate is 3.25%%, in force since 3 September 2026 after the third cut since May, and it was "
              "left unchanged in October. Prime is the Bank of Israel rate plus 1.5, so 4.75%%. Inflation over the 12 months to September 2026 was "
              "1.6%% (%s). The next rate decision is on %s; in its %s the Bank of Israel expects its rate to average 3.0%% in the third quarter of "
              "2027 and inflation of 2.0%% over the next four quarters."
              % (x("cbs", "Central Bureau of Statistics"), NEXT, x("press", "October 2026 forecast")))
            + fig(ig.rates_svg([(8, 4.00), (148, 3.75), (190, 3.50), (246, 3.25)], [(135, 4.77, "May"), (166, 4.73, "Jun"), (196, 4.63, "Jul"), (227, 4.62, "Aug")],
                               "In force from 8 Jan, 28 May, 9 Jul and 3 Sep 2026; shown to 25 Oct 2026."),
                  "The Bank of Israel rate in 2026 (4.00%, 3.75%, 3.50%, 3.25%), prime 1.5 points above it, and the average fixed not linked rate "
                  "on new mortgages, May to August 2026 (4.77%, 4.73%, 4.63%, 4.62%).")
            + p("The Bank of Israel also publishes the %s every month. The latest month available on 25 October 2026 is August 2026. These are "
                "averages across all borrowers in Israel, not an offer for your file, but they are the best yardstick for any offer you get."
                % x("avg", "average rate on new housing loans"))
            + T4AT
            + p("Read the CPI-linked rates with care. A CPI-linked track adds inflation to the balance, so its lower rate does not compare with a not "
                "linked rate. On the Bank of Israel's 2.0%% inflation forecast, a 3.29%% linked rate costs about %.1f%% a year in shekels, more "
                "than the 4.62%% fixed not linked average (our arithmetic, August 2026 rates)." % (LINKED_COST * 100))
            + p("This is the linkage trap. On a CPI-linked track the inflation adjustment is added to the principal, so the balance can rise even "
                "while every payment is made on time. A buyer who looks only at the first monthly payment understates the cost, and the risk is "
                "larger for someone who thinks in dollars, euros, pounds, Canadian or Australian dollars but repays a shekel loan.")
            + p("A second Bank of Israel table gives average rates by the length of the loan (%s and %s). Banks use it, among other things, to work "
                "out early repayment fees. The figures are effective annual averages for the reporting month of September 2026, in force from 19 "
                "October 2026." % (x("mashfix", "not linked"), x("pribmash", "CPI-linked")))
            + T4BT + BENCH
            + p("Use these figures to test an offer, not to replace one. Ask each bank for a written breakdown by track: which part can change with "
                "prime, which part resets later, which part is linked to the index, whether the balance can rise, and what early repayment would "
                "cost. The lowest opening payment is not necessarily the lowest risk loan.")))

T6 = table("The tracks, what moves them and what leaving early costs",
           "Directive 329 s.7 and s.12.3; Banking Order (early repayment of a housing loan) 2002; average rates from the Bank of Israel, August "
           "2026. Every early repayment can also carry an operational fee of up to ₪60, and 0.1% if you give less than 10 days' notice.",
           ["Track", "What moves your payment", "Average rate", "Counts toward the two-thirds variable cap", "Early repayment fee"], [
               ["Fixed, not linked (kalatz)", "Nothing: rate and balance are fixed", "4.62% (Aug 2026)", "No", "A capitalization fee is possible when market rates have fallen below yours; it is cut by 20% after 3 years and 30% after 5"],
               ["Fixed, CPI-linked", "The index: the balance grows with inflation", "3.29% plus inflation (Aug 2026)", "No", "Possible, as on the fixed not linked track"],
               ["Prime", "The Bank of Israel rate, at every decision", "4.75% plus or minus the bank's spread (Oct 2026)", "Yes", "No capitalization fee"],
               ["Variable every 5 years, not linked", "The new rate at each reset", "Quoted by the bank", "Yes", "Ask how the fee works on and between reset dates"],
               ["Variable every 5 years, CPI-linked", "The index, and the new rate at each reset", "3.19% plus inflation (Aug 2026)", "Yes", "Ask how the fee works on and between reset dates"],
               ["Foreign currency", "The exchange rate and the foreign benchmark", "4.86% (Aug 2026)", "Not for a foreign resident, if the bank's quarterly book stays within the cap", "Ask the bank"]], wide=True)
SEC.append(("the-israeli-mortgage-tracks-explained", "Tracks and the one-third fixed rule",
            p("An Israeli mortgage is usually built from several tracks rather than one loan at one rate. The mix matters more than the headline "
              "rate, because each track reacts to something different: prime, the consumer price index, a reset date, or an exchange rate. A fixed "
              "not linked track gives the most clarity; a fixed CPI-linked track can start lower but its balance follows inflation; a prime track "
              "moves with every rate decision; a track that resets every 5 years looks calm at the start and can change later; a foreign currency "
              "track can match foreign income but adds exchange and benchmark risk.")
            + p("Directive 329 limits the variable part to 66.66%% of the loan, so at least one third must sit on a fixed rate. The rule leaves room "
                "for many mixes, which is why %s makes every approval in principle show three uniform baskets the Bank of Israel defined: all fixed "
                "not linked; thirds of fixed not linked, prime and variable CPI-linked every 5 years; and half fixed not linked, half prime. Each "
                "basket comes with its expected total interest, total repayment and highest expected monthly payment, so you can compare banks on "
                "the same terms (the Bank of Israel explains this %s)." % (x("d451", "Directive 451"), x("reform", "in English")))
            + T6
            + p("The right mix depends on the currency you earn in, how much payment risk you can carry, how long you plan to hold the home, whether "
                "you may repay early and whether aliyah is on the horizon. This guide gives no ready-made mix, because no single mix suits every "
                "foreign buyer. What it can tell you is how each track behaves, and that is what to ask the bank to show you in writing.")))

SW = table("A ₪%s monthly payment in your currency" % num(M2),
           "Our arithmetic at the %s and at the same rates moved 10%%; the 30-day range is from 23 Sep to 23 Oct 2026." % FXL,
           ["Currency", "Today", "Shekel 10% weaker", "Shekel 10% stronger", "30-day range of the rate"],
           [[{"USD": "US dollar", "EUR": "Euro", "GBP": "Pound sterling"}[c], "≈ " + cur(M2, c), "≈ {}{:,.0f}".format(SYM[c], SWING[c][1]),
             "≈ {}{:,.0f}".format(SYM[c], SWING[c][2]), "₪%s to ₪%s" % (FX30[c][0], FX30[c][1])] for c in ("USD", "EUR", "GBP")], wide=True)
SEC.append(("foreign-currency", "Borrowing in dollars, euros or pounds",
            p("Israeli banks can lend in foreign currency or linked to it, but few borrowers take it. In August 2026 foreign currency loans were "
              "0.1% of new housing lending by volume, all of them on a variable rate; no fixed foreign currency loans were made that month. Their "
              "average rate was 4.86%: the foreign benchmark at 2.93% plus an average margin of 1.92.")
            + p("For a non-citizen one rule makes them more flexible. Directive 329 section 12.3 lets a bank leave foreign currency housing loans to "
                "a foreign resident out of the two-thirds variable cap, provided all its variable housing loans approved in principle in that "
                "quarter stay within 66.66%. In plain words, the bank may allow a fully variable foreign currency loan if its overall book allows "
                "it. A bank that rarely gives housing loans need not meet even that test for a foreign resident client.")
            + p("A foreign currency loan suits you only if you earn in the same currency and expect to keep doing so. The apartment, the purchase "
                "tax and most costs stay in shekels, so the loan also moves the shekel value of your debt. Bank of Jerusalem is known for foreign "
                "residents' business, but none of the banks' English pages we read on 25 October 2026 listed current foreign currency loan terms. "
                "Ask in writing which currencies are offered, at what margin and for how long.")
            + h3("The 10% shekel test")
            + p("If you borrow in shekels and earn abroad, run the payment through a 10%% move in the exchange rate. A ₪2,000,000 loan over 25 years "
                "at the August 2026 average of 4.62%% costs %s a month, ≈ %s at the %s. If the shekel weakens 10%% ($1 = ₪3.4232), the same payment costs you ≈ $%s; if it "
                "strengthens 10%% ($1 = ₪2.8008), ≈ $%s. Over the 30 days to 23 October 2026 the dollar alone moved from ₪3.017 to ₪3.112."
                % (ils(M2), cur(M2), FXL, num(SWING["USD"][1]), num(SWING["USD"][2])))
            + SW
            + p("Should you borrow at home instead? Compare the total cost in the currency you earn. A loan at home in your own currency carries no "
                "exchange swing on the payment, but it is secured and priced under your home country's rules; a shekel loan moves with the "
                "exchange rate, as the table shows.")))

T5T = table("Cash to close on a ₪4,000,000 home, 25 years at 4.62% fixed not linked (August 2026)",
            "Our arithmetic: caps from Directive 329; purchase tax from the Tax Authority notice of 12 Oct 2026 and instruction 1/2026; lawyer "
            "0.5%% plus 18%% VAT, appraiser ₪650 and bank file fee ₪360 are typical figures, check your own bank's tariff; $, € and £ approx., %s." % FXL,
            [""] + [s["name"] for s in T5], [
                ["Loan cap"] + ["%d%%" % (s["ltv"] * 100) for s in T5],
                ["Loan"] + [ils(s["loan"]) for s in T5],
                ["Your cash toward the price"] + [ils(s["cash"]) for s in T5],
                ["Purchase tax"] + ['%s<br><span class="s">%s</span>' % (ils(s["tax"]), s["track"]) for s in T5],
                ["Lawyer and bank fees, typical"] + [ils(FEES) for s in T5],
                ["Cash to close"] + ["<strong>%s</strong>" % ils(s["close"]) for s in T5],
                ["≈ $"] + [cur(s["close"]) for s in T5],
                ["≈ €"] + [cur(s["close"], "EUR") for s in T5],
                ["≈ £"] + [cur(s["close"], "GBP") for s in T5],
                ["Monthly payment"] + ["%s<br>≈ %s" % (ils(s["m"]), cur(s["m"])) for s in T5],
                ["Net income needed at one third"] + [ils(s["m"] * 3) for s in T5]], wide=True)
SEC.append(("cash-to-close", "Cash to close on a ₪4,000,000 home, by status",
            p("Put the two rulebooks together and the cash you need on the same home changes by about ₪1.3 million. The table works a ₪4,000,000 "
              "home with a 25-year loan on the fixed not linked track at the August 2026 average of 4.62%, at the highest cap for each status.")
            + T5T
            + fig(ig.cash_svg([("Not an Israeli citizen" if i == 0 else ("Israeli citizen abroad, first home" if i == 1 else ("New oleh living in Israel" if i == 2 else "Israeli citizen in Israel, single home")),
                                s["loan"], s["cash"], s["tax"], FEES, s["close"], s["close"] / FX["USD"]) for i, s in enumerate(T5)], FXL),
                  "The same ₪4,000,000 home, four buyers: the loan, the buyer's own cash toward the price, the purchase tax and typical fees. "
                  "Dollar figures approx., %s." % FXL)
            + p("Three things move these numbers most. The appraisal: if the bank values the home at ₪3,800,000, a non-citizen's loan falls to "
                "₪1,900,000 and the cash needed rises by ₪100,000. The price bracket: above ₪6,055,070 the foreign resident rate rises to 10% on "
                "the part above it. And the date: the 8% and 10% rate applies to purchases until 10 February 2027.")
            + p("The price is in shekels. Under the %s a dealer may publish the price of a home only in Israeli currency, so read the dollar, euro "
                "and pound figures as conversions at one day's rate: they will move." % x("consumer", "Consumer Protection Law (section 17D)"))))

T7 = table("Documents, who asks for them and why",
           "Money Laundering Prohibition Order for banks (2001), s.2A, s.3, s.4 and s.6; Bank of Israel Directive 451 (circular 2694 of 31 Jan "
           "2022); Mizrahi-Tefahot and Discount Bank English pages; read 25 Oct 2026.",
           ["Document", "Who asks", "Why", "Rule"], [
               ["Passport, plus a second document with a photo and ID number", "The bank, when you open the account", "Identifying a foreign resident", "Order s.3(a)(2)"],
               ["Source of funds, occupation, purpose and planned activity; your connection to Israel; whether you are a foreign public figure", "The bank", "Know your customer", "Order s.2A"],
               ["Signed declaration on whether anyone else benefits from the account", "The bank, at opening", "Beneficiary declaration", "Order s.4(a)"],
               ["Proof of income: payslips, tax returns or an accountant's letter, translated as the bank asks", "The mortgage department", "The income test", "Each bank's policy; the full list comes with the approval in principle (Directive 451)"],
               ["Bank and asset statements", "The mortgage department", "Your own money and your reserves", "Each bank's policy"],
               ["Contract and property papers", "The appraiser and the bank", "The value the loan rests on", "Directive 451; Discount Bank page"],
               ["Life and property insurance assigned to the bank", "The bank", "A condition of the loan", "Mizrahi-Tefahot and Discount Bank pages"],
               ["Notarized signatures or a power of attorney", "The bank and your lawyer", "Signing from abroad", "Each bank's acceptance rules"]], wide=True)
T8 = table("The Israeli bank account",
           "Banking (Customer Service) Law 1981 s.2(a), as the Bank of Israel explains it (page updated 15 Nov 2022); Money Laundering Prohibition "
           "Order for banks s.6(a); Bank of Jerusalem's non-resident account page; Bank of Israel letter 793-17-BC of 22 Mar 2018; read 25 Oct 2026.",
           ["Question", "What the rule says", "Source"], [
               ["Can a bank refuse me?", "A bank may not unreasonably refuse to open a current account in shekels that stays in credit. A suspicion of money laundering is a reasonable ground.", x("account", "Banking (Customer Service) Law s.2(a)")],
               ["Do I have to fly in?", "Face-to-face identification is needed before the first action. Abroad it can be done by an Israeli-licensed lawyer, an Israeli diplomatic or consular representative, an authority under the Apostille Convention, or other means the Supervisor of Banks approves. Each bank chooses which it accepts.", x("aml", "Order s.6(a)")],
               ["What does one bank ask for a non-resident account?", "Bank of Jerusalem: Israel is not your or your family's permanent home; you have no business in or tied to Israel; the account is opened only at its Private Banking, Tel Aviv, Ashdod or Netanya branches, not by proxy; the non-resident declaration is renewed every three years.", x("boj", "Bank of Jerusalem")],
               ["I just made aliyah. Is my oleh certificate enough?", "The Bank of Israel told banks that an oleh certificate counts as an ID card for up to 30 days from its issue when you open an account.", x("oleh", "Bank of Israel letter, 22 Mar 2018")]])
SEC.append(("documents-checklist", "Documents, the Israeli bank account and identification from abroad",
            p("A mortgage from abroad is a paperwork project. The bank has to identify you, test your income, trace the money you bring, value the "
              "home and meet its own compliance duties. A clean file moves; a weak one gets delayed, sent back for translations or approved for less.")
            + p("Two sets of rules sit behind the requests. The %s says no account is opened without identification and a know-your-customer "
                "process: where the money comes from, what you do, why you need the account and how you plan to use it. For a foreign resident it "
                "adds two questions: your connection to Israel, and whether you are a foreign public figure. Directive 451 then makes the bank give "
                "you the list of documents it needs for the loan together with the approval in principle, so you get one list, in writing."
                % x("aml", "money laundering order for banks"))
            + T7
            + h3("A checklist to start the file")
            + ul(["Passport and identity documents for every borrower, plus a second photo ID.", "Israeli identity or citizenship documents, if you have them or may be entitled to them.",
                  "Proof of your address outside Israel.", "Tax returns from the country where you live.", "Payslips, an employer letter or an accountant's letter showing current income.",
                  "Bank and asset statements showing your own money and reserves.", "Documents showing where the money for your own part comes from.",
                  "The draft or signed purchase contract, depending on the stage.", "Property documents the bank, your lawyer or the appraiser ask for.",
                  "Translations, where the bank requires them.", "Life insurance assigned to the bank.", "Property insurance the bank requires.",
                  "A power of attorney, if you will sign through a lawyer or a representative."])
            + p("Income earned abroad needs more paper than an Israeli salary. A salaried buyer may need an employer letter and income history; a "
                "self-employed buyer, accountant letters and tax filings; a company owner, the company's accounts. Mizrahi-Tefahot says it counts "
                "income from Israel or abroad, including investment income. The exact package depends on the bank, the country and your profile, "
                "so confirm it before you sign a binding contract.")
            + p("The money you bring for your own part is checked separately from the loan. The bank may ask where it came from, when it was "
                "earned, how it moved between accounts and whether it is yours. Plan the transfer route early, so the money is not stuck in review "
                "when a payment date arrives.")
            + h3("The Israeli bank account", "israeli-bank-account")
            + p("In practice you need an Israeli account before the loan is paid out, because the payments run through it. Open it early: the "
                "opening triggers its own know-your-customer review, and a contract with a tight payment date becomes stressful if the account, "
                "the identity checks or the incoming transfer are still under review.")
            + T8))

T9 = table("The steps and the clock behind each",
           "Bank of Israel Directive 451 (circular 2694 of 31 Jan 2022), s.4 and its rules on appraisal and outside insurance; Tax Authority 2026 "
           "guide for buyers and sellers; Money Laundering Prohibition Order for banks; read 25 Oct 2026.",
           ["Step", "What happens", "Clock", "Rule"], [
               ["Account and identification", "Passport and a second ID, know-your-customer questions, face-to-face identification", "Before the first action in the account", "Order s.3, s.6"],
               ["Approval in principle", "A written answer; three uniform baskets with total interest, total repayment and the highest payment; the list of documents", "5 business days; 7 in cases the bank's credit policy defines in advance, with a reasoned notice", "Directive 451 s.4"],
               ["Appraisal", "An appraiser on the bank's list values the home; the loan rests on the lower of price and value", "A report can be used for 90 days", "Directive 451"],
               ["Contract", "Sign after the approval; payment dates matched to the dates the bank can release money", "Your contract's dates", "Good practice"],
               ["Insurance", "Life and property policies assigned to the bank; you may bring your own", "The bank tells you within 14 days if your policy falls short", "Directive 451"],
               ["Purchase tax", "Declaration and payment", "Declaration within 30 days; payment due 60 days from the deal", "Tax Authority"],
               ["Security and release", "The bank registers its security, often with a warning note first, and pays the money out", "After the loan documents are signed", "Each bank's practice"]], wide=True)
SEC.append(("timeline", "From approval in principle to the money: the timeline",
            p("The order of the steps protects you. Get the approval in principle before you sign, match the contract's payment dates to the dates "
              "the bank can release money, and leave room for the appraisal and the insurance. A contract that assumes fast funding puts you under "
              "pressure if any step slips.")
            + T9
            + fig(ig.timeline_svg([
                ("Before", "first action", "Account and identification", ["Passport + a second photo ID. Abroad: an", "Israeli lawyer, consul or apostille authority"], True),
                ("5 days", "business", "Approval in principle", ["Written answer, 7 days in predefined cases;", "three baskets and the document list"], True),
                ("90 days", "report life", "Appraisal", ["A listed appraiser's report; the loan rests", "on the lower of price and value"], False),
                ("Sign", "the contract", "Contract", ["After the approval; payment dates matched", "to the bank's release dates"], False),
                ("14 days", "bank answer", "Insurance", ["Life and property cover assigned to the", "bank; your own policy is allowed"], True),
                ("30 / 60", "days", "Purchase tax", ["Declaration within 30 days; payment", "due 60 days from the deal"], False),
                ("Release", "of funds", "Security and release", ["The bank registers its security", "and pays the seller"], False)]),
                  "The rule-set clocks from account opening to the release of the loan, and the three points where the bank asks for documents.")
            + p("There is no official figure for how long the whole process takes, so treat any promise in days or weeks as an estimate. The two "
                "clocks set by rule are the bank's answer on the approval in principle and its answer on an outside insurance policy.")
            + h3("Buying a new apartment from a developer")
            + p("A new home bought from a developer adds timing to the loan. You pay in stages, and the bank releases the loan according to its own "
                "rules and the project's. It will want to see the project, the developer's documents, the payment schedule and the security you get "
                "for your payments. Compare %s, or browse the %s, once your loan ceiling and the route for your own money are clear."
                % (a("new_en", "new projects in Israel"), a("projects_en", "English catalog of new building projects")))
            + p("Before you sign anything, ask the bank or a mortgage broker for a written pre-check: the most it will lend, the expected track mix, "
                "how the appraisal could change the loan, the document list and how you will sign from abroad.")))

SEC.append(("signing-from-abroad", "Signing from abroad and insurance",
            p("Much of the process can be done without flying to Israel, but each bank decides which signatures it accepts. The usual routes are a "
              "power of attorney to an Israeli lawyer, signatures before an Israeli consul, or a local notary with an apostille. Some banks still "
              "want an in-person or consular signature. Confirm the route with the bank before you sign the purchase contract or book anything.")
            + p("Israeli missions abroad %s in person, before a consular representative; they do not prepare legal documents for you. The service is "
                "also open to a foreign citizen who needs a notarized signature on a document to be submitted in Israel, so bring the document "
                "ready to sign." % x("notary", "notarize signatures"))
            + p("Find out early whether the bank will want you in person at any stage, whether it needs original documents, and whether opening the "
                "account requires a branch visit. At Bank of Jerusalem, for example, a non-resident account is opened at a branch and not by proxy.")
            + h3("Life and property insurance")
            + p("Banks require life insurance and property insurance assigned to them as a condition of the loan. You do not have to buy them from "
                "the bank: Directive 451 lets you bring an outside policy, and the bank must confirm it received it and tell you and the insurer "
                "within 14 days if the policy does not meet its requirements. For older buyers or buyers with a medical history, start the "
                "insurance early, because a delayed or limited approval can hold up the loan.")))

SEC.append(("olim", "Olim and returning Israelis",
            p("Aliyah changes the loan before it changes anything else. Once you are registered in the Population Registry you count as an Israeli "
              "citizen under Directive 329, and a first home can be financed up to 75% instead of 50%. Returning Israelis who stayed in the "
              "Registry are Israeli citizens for the bank wherever they have lived.")
            + p("Timing matters. Some brokers' and news pages say buyers who plan aliyah within two years can already get 75%. The directive's text "
                "does not say so, so if your plan depends on it, get the bank's answer in writing before you sign. The same applies to a buyer who "
                "is entitled to make aliyah but has not yet done so.")
            + p("On the tax side, an oleh buying a single home from one year before aliyah to seven years after it can use the oleh relief of "
                "regulation 12A: 0%% up to ₪1,978,745, 0.5%% up to ₪6,055,070 and 8%% up to ₪20,183,565, with no relief above that. On a "
                "₪4,000,000 home that is %s. A buyer who becomes an Israeli resident within two years after buying as a foreign resident can be "
                "treated as a resident for the single home test and claim a refund." % ils(T5[2]["tax"]))
            + p("Olim may also be eligible for a state-assisted mortgage with an eligibility certificate, the <em>teudat zakaut</em>. We do not "
                "print its amount or rate here: the figures quoted on bank and broker pages differ, and we found no official 2026 figure on 25 "
                "October 2026. Ask the bank for the current terms in writing.")
            + p("The oleh certificate also opens a bank account: the Bank of Israel told banks it counts as an ID card for up to 30 days from its "
                "issue. Status improves the cap, but it does not replace the credit decision; the bank still looks at your income, the home, your "
                "ability to repay, the insurance and the documents.")))

SEC.append(("above-50", "Above 50%: what exists and what it costs",
            p("No Israeli bank can lend a buyer without Israeli citizenship more than 50% of the value of a home, because Directive 329 binds every "
              "bank. Any route above 50% is therefore outside the bank.")
            + p("Brokers advertise extra loans from non-bank lenders on top of the bank mortgage. Those lenders are not banks, the directive does not "
                "apply to them, and their terms appear in no official comparison. If you consider one, ask for the full cost in writing: the rate, "
                "every fee, the term, the security they take, and what happens to the bank mortgage if a payment is missed.")
            + p("Israelis who sell one home to buy another sometimes use a bridge loan between the two deals. For an Israeli citizen, a home bought "
                "to replace one he will sell is financed up to 70%. A non-citizen stays at 50% whatever he sells.")
            + p("The plain way above 50% is more of your own money, a less expensive home, or a change of status that the bank accepts in writing.")))

T10 = table("What the banks' own English pages say",
            "Read 25 Oct 2026. Bank pages are undated; offers differ from bank to bank and from the averages above.",
            ["Bank", "Page", "What it says"], [
                ["Mizrahi-Tefahot", x("mz_imc", "International Mortgage Center"), "Shekel mortgages for international clients, loans up to 30 years, up to 50% of the property value, fixed or variable"],
                ["Mizrahi-Tefahot", x("mz_qa", "Questions and answers on mortgages"), "Olim up to 75% instead of 50% as foreign citizens, if they are Israeli citizens or entitled to citizenship; income from Israel or abroad counts, including investment income; the bank checks where your money comes from; life insurance is a condition"],
                ["Discount Bank", x("discount", "International private banking, mortgage"), "Value is the lower of contract price and appraisal; payment up to 50% of income by law and up to about one third at most banks; after the approval in principle: appraisal, life and property insurance, mortgage deeds, notarized documents; named English-speaking advisers"],
                ["Bank of Jerusalem", x("boj", "Non-resident account"), "The conditions for a non-resident account, opened at four named branches and not by proxy, with a declaration renewed every three years; its English mortgage page showed no foreign currency loan terms"],
                ["Bank Leumi", "None found", "No English mortgage page found on 25 Oct 2026"],
                ["Bank Hapoalim", "None found", "No English mortgage page found on 25 Oct 2026"],
                ["Bank of Israel", x("compare", "Interest rate comparisons, housing loans"), "Rates by bank and by track; the latest period in the English version was October 2025 when we checked"]], wide=True)
SEC.append(("which-banks-work-with-foreign-buyers", "What Israeli banks say on their own English pages",
            p("The large Israeli mortgage lenders active with foreign buyers include Mizrahi-Tefahot, Bank Leumi, Bank Hapoalim, Israel Discount Bank "
              "and Bank of Jerusalem. The lender's name matters, but so does the desk that "
              "handles your file: not every branch or banker is used to foreign income.")
            + p("Leumi, Hapoalim and Discount are major banks with broad mortgage activity. For you the question is not whether a bank has a mortgage "
                "department, but whether it will understand foreign income, accept translated documents, open the account, handle the "
                "know-your-customer questions and keep to the contract's timetable. Some bank pages give 40% or one third as their own payment "
                "limit; that is their policy, and the directive's ceiling stays 50%.")
            + T10
            + h3("Going direct or through a mortgage broker", "using-a-mortgage-broker-vs-going-direct")
            + p("You can go to the banks yourself, and many foreign buyers use a broker who works with non-residents. A good broker does more than "
                "shop for a rate: he packages foreign income in a form an Israeli bank can underwrite, knows which bank is likely to understand your "
                "file, explains the track mixes and keeps the documents moving.")
            + p("Going direct works when your income is a simple salary, your documents are strong, your Israeli status is clear and you have time to "
                "speak with several banks; it also shows you how each bank communicates. A broker earns his fee when you are self-employed, earn in "
                "several currencies, own a company, hold complex assets, want a foreign currency loan or will sign through a power of attorney. "
                "Neither route guarantees approval.")
            + p("A broker does not replace your lawyer. The broker handles the loan; the lawyer handles the rights in the property, the contract, the "
                "purchase tax filing, the warning note, the registration and the legal risk. The two should talk before you sign if the payment "
                "schedule depends on the loan.")
            + p("Whichever way you go, ask for written answers: the most the bank will lend, how the appraisal affects it, the documents, the steps to "
                "open the account, the insurance, how you will sign, the track mix, the index exposure and when the money will be released. A vague "
                "answer on financing becomes a cash problem very quickly.")))

GLO = [("Mashkanta", "משכנתא", "A mortgage: a loan secured on the home"),
       ("Ishur ekroni", "אישור עקרוני", "Approval in principle: the bank's first written answer, with the three baskets and the document list"),
       ("Maslul", "מסלול", "A track: one part of the loan with its own type of rate"),
       ("Kalatz", "קל״צ", "Fixed rate, not linked to the index"), ("Katz", "ק״צ", "Fixed rate, linked to the consumer price index"),
       ("Prime", "פריים", "The Bank of Israel rate plus 1.5; 4.75% since 3 Sep 2026"),
       ("Madad", "מדד", "The consumer price index; linked tracks add it to the balance"), ("Shamai", "שמאי", "The appraiser who values the home for the bank"),
       ("Teudat zakaut", "תעודת זכאות", "The eligibility certificate for a state-assisted mortgage"),
       ("Teudat oleh", "תעודת עולה", "The oleh certificate; it counts as ID for 30 days when you open an account"),
       ("Toshav chutz", "תושב חוץ", "Foreign resident: for the bank, anyone who is not an Israeli citizen; for the Tax Authority, anyone who is not an Israeli resident"),
       ("Ezrach yisraeli", "אזרח ישראלי", "Israeli citizen as the directive defines it: registered in the Population Registry, an Israeli resident, or entitled to aliyah and living in the Area"),
       ("Mas rechisha", "מס רכישה", "Purchase tax"), ("Yipui koach", "ייפוי כוח", "Power of attorney"),
       ("He'arat azhara", "הערת אזהרה", "A warning note registered for the buyer in the land registry")]
SEC.append(("hebrew-terms", "Hebrew terms you will hear",
            p("Israeli bankers switch to English for clients abroad, but the documents and many of the words stay Hebrew. These are the ones you will "
              "meet first.")
            + table("Hebrew mortgage terms in plain English", "As used by Israeli banks and in Directive 329.", ["Term", "Hebrew", "What it means"],
                    [[t1, '<span class="nlu3-he" lang="he" dir="rtl">%s</span>' % t2, t3] for t1, t2, t3 in GLO])))

FAQ = [
    ("Can a foreigner get a mortgage in Israel?",
     "Yes. Israeli banks lend to buyers without Israeli citizenship, mostly in shekels, up to 50% of the home's value. Bank of Israel Directive 329 "
     "treats any home a non-citizen buys as an investment home, so the 50% cap applies even to your first and only home in Israel. The value is the "
     "lower of the price and the bank's appraisal, and your payment must also pass the income test."),
    ("How much will an Israeli bank lend me?",
     "Two limits apply and the lower one wins. The first is the cap by status under Directive 329: 50% for a non-citizen, 75% for an Israeli "
     "citizen's only home, 70% for a replacement home. The second is the income cap: the monthly payment may not pass 50% of your disposable "
     "income, and most banks prefer about one third. Banks count the value as the lower of price and appraisal."),
    ("What is the minimum down payment?",
     "For a non-citizen, half the price plus purchase tax and fees. A home priced at ₪933,600 (≈ $300,000, approx., %s) needs ₪466,800 down from "
     "a non-citizen, plus ₪74,688 purchase tax at 8%%. An Israeli citizen buying an only home needs 25%%, ₪233,400, plus the purchase tax of his "
     "residency track: 8%% if he lives abroad, nothing at this price if he lives in Israel." % FXL),
    ("I am an Israeli citizen living abroad. Can I borrow 75%?",
     "Yes, for your only home in Israel. The directive's \"Israeli citizen\" includes anyone registered, or required to be registered, in the "
     "Population Registry, wherever you live today. Your purchase tax is a different matter: for the Tax Authority you are not an Israeli "
     "resident, so you pay the foreign resident rate of 8% up to ₪6,055,070 and 10% above, for purchases until 10 Feb 2027."),
    ("I am making aliyah. When does 75% start?",
     "When you count as an Israeli citizen under the directive, which in practice means once you are registered. Mizrahi-Tefahot's English page, "
     "for example, offers olim 75% instead of 50%. Some brokers' and news pages say buyers planning aliyah within two years can get 75% already; "
     "the directive's text does not say so. If your budget depends on it, get the bank's answer in writing before you sign."),
    ("My spouse is Israeli and I am not. What can we borrow?",
     "The Bank of Israel follows the Tax Authority here. If you are separate buyers for tax, the cap is the average weighted by your shares: half "
     "each of 75% and 50% gives 62.5%. But spouses normally count as one buyer for the single home test, so how your household is treated is a "
     "question for the bank, in writing, before you sign."),
    ("What are mortgage rates in Israel now?",
     "The latest Bank of Israel averages on new loans are for August 2026: fixed not linked 4.62%, fixed CPI-linked 3.29% plus inflation, variable "
     "CPI-linked 3.19% plus inflation, and foreign currency loans 4.86%. Prime is 4.75%, the Bank of Israel rate of 3.25% (since 3 Sep 2026) plus "
     "1.5. The next rate decision is on 23 Nov 2026. Your own quote depends on the bank, the track mix, the loan share, your income and the term."),
    ("Do foreigners pay higher rates than Israelis?",
     "The Bank of Israel does not publish rates by citizenship, so there is no official figure either way. What changes for a foreign buyer is the "
     "size of the loan, the paperwork and the time it takes. Compare the written offers you receive against the official monthly averages, track "
     "by track."),
    ("Which bank in Israel is best for foreigners?",
     "There is no official ranking. Mizrahi-Tefahot runs an International Mortgage Center (shekel loans, up to 50%, up to 30 years); Discount Bank "
     "and Bank of Jerusalem have English pages for clients abroad, and Leumi and Hapoalim also lend to foreign buyers. The right bank depends on "
     "your status, your income country, your currency and the banker's experience with files like yours. The Bank of Israel publishes rate "
     "comparisons by bank."),
    ("Can I borrow in dollars, euros or pounds?",
     "Yes, Israeli banks can lend in foreign currency or linked to it. The average rate on those loans was 4.86% in August 2026, and they were 0.1% "
     "of new housing lending. For a non-citizen they can sit outside the two-thirds variable cap, if the bank's quarterly book allows it. They suit "
     "you only if you earn in that currency."),
    ("Should I borrow at home instead?",
     "Compare the total cost in the currency you earn. A shekel loan moves with the exchange rate: a ₪2,000,000 loan over 25 years at the "
     "August 2026 average of 4.62%% costs "
     "%s a month, ≈ %s at the %s, and ≈ $%s or ≈ $%s if the shekel weakens or strengthens 10%%. A loan at home avoids that swing but follows your "
     "home country's rules." % (ils(M2), cur(M2), FXL, num(SWING["USD"][1]), num(SWING["USD"][2]))),
    ("How much do I need to earn?",
     "The payment may not pass 50%% of your disposable income, and most banks prefer about one third. A ₪2,000,000 loan over 25 years at the "
     "August 2026 average of 4.62%% costs %s a month, so you need %s net a month at the legal cap (≈ %s) and %s at one third (≈ %s), approx., %s."
     % (ils(M2), ils(T3[1][2]), cur(T3[1][2]), ils(T3[1][3]), cur(T3[1][3]), FXL)),
    ("How do banks count income earned abroad?",
     "Each bank sets its own policy. The directive counts net income minus fixed commitments that run for more than 18 months. Expect translated "
     "payslips or tax returns, an accountant's letter if you are self-employed, and source of funds checks on the money you bring. Mizrahi-Tefahot, "
     "for example, says it counts income from Israel or abroad, including investment income."),
    ("What documents do I need?",
     "A passport and a second photo ID, proof of income, bank statements, evidence of where your own money comes from, the contract and property "
     "papers, life and property insurance, and signatures or a power of attorney. Under Directive 451 the bank must give you its list of documents "
     "together with the approval in principle, so ask for it then."),
    ("Do I need an Israeli bank account, and can I open one as a non-resident?",
     "In practice yes: the loan is paid out and repaid through it. A bank may not unreasonably refuse a shekel current account that stays in credit. "
     "You can be identified face to face abroad by an Israeli lawyer or an Israeli consul, but each bank decides its own process; Bank of Jerusalem, "
     "for example, opens non-resident accounts only at a branch and not by proxy."),
    ("How long does approval take?",
     "The bank must answer a request for approval in principle in writing within 5 business days, or 7 in cases its credit policy defines in "
     "advance. The appraisal, the insurance and the security come after that, and there is no official figure for the whole process, so treat any "
     "promise in weeks as an estimate."),
    ("Can I do it all without flying to Israel?",
     "Often, yes: with a power of attorney to an Israeli lawyer, and with signatures before an Israeli consul or a notary with an apostille. Some "
     "banks still want an in-person or consular signature, or a branch visit to open the account. Each bank decides which signatures it accepts, "
     "so confirm before you sign the purchase contract or book anything."),
    ("Is life insurance required, and can I use my own policy?",
     "Yes. Banks require life and property insurance assigned to them as a condition of the loan. You may bring an outside policy instead of the "
     "bank's: under Directive 451 the bank must tell you and the insurer within 14 days if the policy does not meet its requirements. Older buyers "
     "should start the insurance early."),
    ("What is the longest mortgage term?",
     "30 years under Bank of Israel Directive 329, for any buyer. Within that limit, age limits and the term a bank will actually offer you are each "
     "bank's own policy. For comparison, the average new not linked loan in Israel in August 2026 ran for 23.8 years."),
    ("Does part of the loan have to be fixed?",
     "Yes. The variable part may not pass 66.66% of the loan, so at least one third sits on a fixed rate, linked or not. Prime and tracks that reset "
     "every 5 years count as variable. The exception is a foreign currency loan to a non-citizen, which a bank may leave outside the cap if its "
     "quarterly book stays within it."),
    ("What if the appraisal comes in below the price?",
     "The bank lends on the lower figure and you cover the gap in cash. On a ₪4,000,000 home valued at ₪3,800,000, a non-citizen's loan falls from "
     "₪2,000,000 to ₪1,900,000. A report by an appraiser on the bank's list can be used for 90 days, so time the appraisal close to the contract."),
    ("How much purchase tax does a foreign buyer pay?",
     "8% up to ₪6,055,070 and 10% on the part above, from the first shekel, for purchases until 10 Feb 2027 inclusive. On ₪3,000,000 that is "
     "₪240,000; on ₪4,000,000, ₪320,000. The test is residency, not citizenship: an Israeli citizen living abroad pays the same rate."),
    ("Can I repay early, and what does it cost?",
     "Prime and other tracks whose rate changes at least once a year carry no capitalization fee. Fixed tracks can, when market rates have fallen "
     "below your rate; the fee drops by 20% after 3 years and 30% after 5. There is also an operational fee of up to ₪60, and 0.1% if you give "
     "less than 10 days' notice."),
    ("Can I borrow more than 50% as a foreigner?",
     "Not from an Israeli bank while you are not an Israeli citizen: Directive 329 binds every bank. Brokers offer extra loans from non-bank lenders "
     "on top of the mortgage; those lenders work outside the directive. Ask for the full cost in writing, including the rate, every fee and the "
     "security they take."),
    ("What is the monthly payment on a $500,000 loan over 30 years?",
     "$500,000 is %s at the %s. At the August 2026 average fixed not linked rate of 4.62%%, a 30-year loan of that size costs %s a month, about "
     "$%s. As a non-citizen you would need a home worth at least %s to borrow that much." % (ils(L500), FXL, ils(P500), num(P500 / FX["USD"]), ils(L500 * 2))),
]
FAQ_H2 = "Frequently asked questions about Israeli mortgages for foreigners"
SEC.append(("faq-israeli-mortgages-for-foreigners", FAQ_H2, "".join(h3(q) + p(ans) for q, ans in FAQ)))

SRC = [x("d329", "Bank of Israel, Proper Conduct of Banking Business Directive 329 on housing loans, version 13 (June 2026)"),
       x("d329qa", "Bank of Israel, Directive 329 page with its questions and answers (question 2.4; joint buyers)"),
       x("d451", "Bank of Israel, Directive 451 on housing loan procedures (circular 2694 of 31 Jan 2022)"),
       x("reform", "Bank of Israel, the mortgage reform explained in English (the uniform baskets)"),
       x("press", "Bank of Israel, interest rate decision and staff forecast, 21 Oct 2026"),
       x("dates", "Bank of Israel, interest rate decision dates (next: 23 Nov 2026)"),
       x("avg", "Bank of Israel, average rates on new housing loans (August 2026, read 25 Oct 2026)"),
       x("mashfix", "Bank of Israel, average mortgage rates by term, not linked") + " and " + x("pribmash", "CPI-linked") + " (reporting month September 2026)",
       x("fx", "Bank of Israel, representative exchange rates (23 Oct 2026)"),
       x("compare", "Bank of Israel, interest rate comparisons, housing loans"),
       x("account", "Bank of Israel, current account questions and answers (Banking (Customer Service) Law s.2(a))"),
       x("oleh", "Bank of Israel, letter on opening an account for a new immigrant (22 Mar 2018)"),
       x("landtax", "Land Taxation Law (Betterment and Purchase), sections 9 and 16A (Hebrew)"),
       x("aml", "Money Laundering Prohibition Order for banking corporations, 2001 (Hebrew)"),
       x("early", "Banking Order (early repayment of a housing loan), 2002 (Hebrew)"),
       x("service", "Banking (Customer Service) Law, 1981 (Hebrew)"),
       x("consumer", "Consumer Protection Law, section 17D (Hebrew)"),
       x("taxnotice", "Tax Authority, purchase tax temporary order extended to 10 Feb 2027 (notice of 12 Oct 2026, Hebrew)"),
       x("inst1", "Tax Authority, instruction 1/2026 on purchase tax brackets (Hebrew)"),
       x("taxguide", "Tax Authority, 2026 guide for buyers and sellers of real estate rights (Hebrew)"),
       x("notary", "Ministry of Foreign Affairs, notarization at Israeli missions"),
       x("cbs", "Central Bureau of Statistics, consumer price index"),
       "Bank pages: " + x("mz_imc", "Mizrahi-Tefahot International Mortgage Center") + ", " + x("mz_qa", "Mizrahi-Tefahot questions and answers") + ", "
       + x("discount", "Discount Bank international private banking") + ", " + x("boj", "Bank of Jerusalem non-resident account") + " (all read 25 Oct 2026)"]
SEC.append(("sources", "Sources and how we checked",
            p("Every rate on this page carries its month and every rule its section. Rates are the Bank of Israel's monthly figures; exchange rates "
              "are the Bank of Israel representative rates of 23 October 2026; the date next to each figure is the date we read it.")
            + ul(SRC)
            + h3("How we compared")
            + p("We read the pages Google ranked on 25 October 2026 for searches such as \"Israel mortgage for foreigners\", \"Israel mortgage for "
                "non residents\", \"mortgage in Israel\" and \"mortgage for olim Israel\", in Israel, the United States and the United Kingdom, as "
                "Google receives them, and counted their words, figures, tables, questions and official sources. Some rivals stay ahead in ways a "
                "page cannot change: the banks and Nefesh B'Nefesh carry the authority of who they are, we did not measure links from other sites, "
                "one broker runs a wide network of linked guides, and all the rival pages together hold more words than this one. Bank offers "
                "differ from the averages shown here; the averages are a yardstick, not a quote.")))

SEC.append(("related", "Related guides",
            ul(["%s: the buying process step by step, from the offer to registration" % a("buy_en", "How to buy a home in Israel from abroad"),
                "%s: the 8%% and 10%% rate and how to file" % a("ptax", "Purchase tax for foreign residents"),
                a("buy_foreign", "The complete guide to buying property in Israel as a foreign buyer"),
                a("investor", "Buying real estate in Israel as a foreign investor"),
                "%s, with the same calculator" % a("projects_en", "New building projects in Israel, in English"),
                a("new_en", "New projects in Israel"),
                "%s, with the Bank of Israel uniform baskets" % a("calc_he", "Mortgage calculator in Hebrew")])))

TOC = ('<nav class="nlu3-toc" aria-label="On this page"><p><strong>On this page</strong></p><ul>'
       + "".join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t, _ in SEC[1:-1]) + "</ul></nav>\n")
DISCLAIMER = ('<hr/><p><em>This guide is general information, not legal or financial advice. Every transaction needs its own review of the '
              'facts. For an initial consultation on a purchase in Israel, %s.</em></p>' % a("lawyer", "contact the office"))
BODY = (TOP + h2(SEC[0][0], SEC[0][1]) + SEC[0][2] + TOC + "".join(h2(i, t) + html for i, t, html in SEC[1:]) + DISCLAIMER)

# ------------------------------------------------------------------ gates on the new copy (before any network call)


def visible(html, keep_svg=False):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    if not keep_svg: h = re.sub(r"<svg\b.*?</svg>", " ", h, flags=re.S)
    h = re.sub(r"\[nadlan_tool[^\]]*\]", " ", h)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).replace("&amp;", "&").strip()


VIS, VIS_ALL = visible(BODY), visible(BODY, keep_svg=True)
assert not re.search(r"[–—]", VIS_ALL), re.findall(r".{20}[–—].{20}", VIS_ALL)[:3]
BANNED = r"\b(?:algorithms?|API|data series|datasets?|SDMX|platforms?|interfaces?|simulat\w*|interactive|coming soon|beta|demo|prototype|widgets?|models?|modell?ing|Nadlan|Atlas|pipeline|backend|database|series)\b"
hits = re.findall(r".{0,25}%s.{0,25}" % BANNED, VIS_ALL, flags=re.I)
assert not hits, ("banned word", hits[:5])
assert not re.search(r"\bAI\b", VIS_ALL), "AI"
for s in re.split(r"(?<=[.;:])\s", VIS_ALL):
    assert not ("75%" in s and re.search(r"Israeli resident", s) and "citizen" not in s), ("75% with 'Israeli resident'", s)
assert not re.search(r"5\.25%|5\.0%|4\.5% prime|prime (?:is |of |at )?(?:5|4\.5)", VIS_ALL), "stale prime"
assert not re.search(r"(?:40|33)% of (?:your |net |disposable )?income", VIS_ALL), "payment cap must be 50%"
for b in re.findall(r"<(?:p|li)\b[^>]*>.*?</(?:p|li)>|<figure class=\"wp-block-table\">.*?</figure>", re.sub(r"<svg\b.*?</svg>", "", BODY, flags=re.S), flags=re.S):
    if re.search(r"[$€£]\s?\d", re.sub(r"<[^>]+>", "", b)) and "<svg" not in b:
        assert FXL in b or "Bank of Israel rate of 23 Oct 2026" in b, ("conversion without the rate label", visible(b)[:120])
for b in re.findall(r"<(?:p|li)\b[^>]*>.*?</(?:p|li)>", BODY, flags=re.S):   # every average rate in running text carries its month (tables: in the header)
    v = visible(b)
    for r in ("4.62%", "3.29%", "3.19%", "4.86%"):
        if r in v: assert re.search(r"Aug(?:ust)? 2026|August|Aug", v), ("rate without its month", r, v[:120])
for sv in re.findall(r"<svg\b.*?</svg>", BODY, flags=re.S):
    assert 'viewBox="0 0 420 ' in sv and min(float(z) for z in re.findall(r"font-size:([\d.]+)px", sv)) >= 12, "svg box or font"
    assert "<style" not in sv and "class=" not in sv, "svg inline styles only"
assert "<h1" not in BODY, "the H1 is the post title"
assert BODY.count('[nadlan_tool id="nrm"]') == 1
calc_at = BODY.index('[nadlan_tool id="nrm"]'); assert BODY.index('id="calculator"') < calc_at < BODY.index('id="ltv-what-non-residents-can-actually-borrow"')
# the FAQPage builder (inc/instruments.php nadlan_nli_faq), run here the same way
fm = re.search(r"<h2[^>]*>\s*(?:שאלות נפוצות|Frequently asked questions)[^<]{0,60}</h2>(.*?)(?=<h2|$)", BODY, flags=re.S)
QA = re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", fm.group(1), flags=re.S)
QS = [re.sub(r"<[^>]+>", "", q).strip() for q, _ in QA]
assert len(QS) == 25 and len(set(QS)) == 25, len(QS)
wc = [len(visible(ans).split()) for _, ans in QA]
assert min(wc) >= 40 and max(wc) <= 90, list(zip(QS, wc))
H2S = re.findall(r"<h2[^>]*>(.*?)</h2>", BODY); H3S = re.findall(r"<h3[^>]*>(.*?)</h3>", BODY)
assert H2S == [t for _, t, _ in SEC] and len(H2S) == 18, H2S
WORDS = len([w for w in VIS.split() if re.search(r"[A-Za-z0-9]", w)])
TABLES = BODY.count("<table"); CELLS = len(re.findall(r"<t[dh][ >]", BODY)); SVGS = BODY.count("<svg")
FIGS = len(re.findall(r"\d[\d,.]*", VIS))
OFFICIAL = sorted(set(re.findall(r'href="(https://(?:www\.)?(?:boi\.org\.il|gov\.il|www\.gov\.il|he\.wikisource\.org|www\.cbs\.gov\.il)[^"]*)"', BODY)))

# survival of the live page's sections, facts and features (re-worded or merged; asserted against the new copy)
SURVIVAL = [
    ("Byline: Adv. Ben Betesh, Israeli real estate lawyer, bar licence 29020, first published 2 July 2026", "top byline", ["Adv. Ben Betesh", "29020", "2 July 2026"]),
    ("Short answer: 50%, 4.62% August 2026, ₪2,000,000 over 25 years = ₪11,253, cash to close on ₪4,000,000 with the 8% tax", "answer paragraphs (FX moved to 23 Oct 2026)", ["₪11,253", "₪2,344,610", "8% purchase tax"]),
    ("Calculator [nadlan_tool id=\"nrm\"]", "section 2 under its H2", ['[nadlan_tool id="nrm"]']),
    ("Intro: lend to non-residents, about 50%, income abroad, account before the loan, CPI linkage, mixed tracks, life insurance", "section 3, first paragraph", ["consumer price index", "Israeli bank account before the money is paid out", "life insurance assigned to the bank"]),
    ("Table of contents (8 anchors)", "'On this page' after the calculator; old anchor ids kept on the matching H2/H3", ['id="ltv-what-non-residents-can-actually-borrow"', 'id="the-israeli-mortgage-tracks-explained"', 'id="which-banks-work-with-foreign-buyers"', 'id="documents-checklist"', 'id="rates-in-2026-and-the-linkage-trap"', 'id="using-a-mortgage-broker-vs-going-direct"', 'id="faq-israeli-mortgages-for-foreigners"', 'id="sources"']),
    ("H2 LTV: what non-residents can actually borrow (75/70/50, lower of price or appraisal, check before signing, source of funds on the equity)", "section 3 (T1, infographic 1) and section 4", ["75% for a single home, 70% for a replacement home", "lower of the contract price and its own appraisal", "Check the financing before you sign", "source of funds checks"]),
    ("LTV table (4 rows)", "T1, six rows, 'Israeli citizen' wording", ["Not an Israeli citizen, any home", "Israeli citizen replacing a home you will sell"]),
    ("Mizrahi: citizen or entitled to citizenship, 75% instead of 50%", "section 3 last paragraph, T10, FAQ 5", ["entitled to Israeli citizenship", "entitled to citizenship"]),
    ("Do not confuse LTV with purchase tax; link to purchase tax for foreign residents", "section 4", ["Do not confuse the loan cap with the tax", 'href="/israel-purchase-tax-foreign-residents/"']),
    ("Link: complete guide to buying property in Israel as a foreign buyer", "Related guides", ['href="/buy-property-israel-foreign-buyers/"']),
    ("H2 The Israeli mortgage tracks explained (tracks, one-third fixed rule, track table, linkage trap, mix depends on currency, risk, holding period, prepayment, aliyah)", "sections 6 and 7 (T6)", ["at least one third must sit on a fixed rate", "This is the linkage trap", "whether aliyah is on the horizon", "Canadian or Australian dollars"]),
    ("H2 Which banks work with foreign buyers (Mizrahi, Leumi, Hapoalim, Discount, Bank of Jerusalem; the desk matters; the unsourced largest-mortgage-bank claim dropped (not in dna 6); what to ask)", "section 15 (T10)", ["Mizrahi-Tefahot, Bank Leumi, Bank Hapoalim, Israel Discount Bank and Bank of Jerusalem", "accept translated documents"]),
    ("Bank of Jerusalem foreign currency mortgages 'up to 20 years, benchmark plus a fixed spread'", "section 8 and T10: Bank of Jerusalem kept; the 20-year term not repeated (its English page no longer shows it, dna 6 unverified)", ["Bank of Jerusalem is known for foreign residents' business", "showed no foreign currency loan terms"]),
    ("New-construction financing paragraph, link to projects", "section 11, h3 'Buying a new apartment from a developer', links to /en/new-projects/ and /en/projects/", ["Buying a new apartment from a developer", 'href="/en/new-projects/"', 'href="/en/projects/"']),
    ("H2 Documents checklist (13-item list, income abroad, money laundering checks on the equity, insurance for older buyers)", "section 10 (T7, T8, the checklist), section 12", ["A checklist to start the file", "Proof of your address outside Israel", "Income earned abroad needs more paper", "checked separately from the loan", "older buyers"]),
    ("Link /transfer-money-to-israel-property/", "dropped: 404 on the live site (26.10.2026); its paragraph is kept in section 10", ["Plan the transfer route early"]),
    ("H2 Rates in 2026 and the linkage trap (three lenses, policy rate, prime, CPI, averages, rate anchors table, ask for a track-by-track breakdown)", "section 6 (T4a, T4b, benchmarks table, chart)", ["three numbers: the Bank of Israel rate", "The rate benchmarks", "written breakdown by track"]),
    ("Link /mortgage-calculator/", "Related guides", ['href="/mortgage-calculator/"']),
    ("H2 Using a mortgage broker vs going direct (5 paragraphs)", "section 15, h3 with the old anchor", ["Going direct or through a mortgage broker", "A broker does not replace your lawyer", "A vague answer on financing becomes a cash problem"]),
    ("FAQ (5): how much can a non-resident borrow; best bank; rates in 2026; olim terms; signing without coming", "FAQ 1, 9, 7, 5 (and section 13), 17", ["Can a foreigner get a mortgage in Israel?", "Which bank in Israel is best for foreigners?", "What are mortgage rates in Israel now?", "When does 75% start?", "Can I do it all without flying to Israel?"]),
    ("Sources (BoI announcements, average rate figures, Mizrahi QA, Bank of Jerusalem, BoI directives)", "section 18, 23 dated entries", ["interest rate decision and staff forecast", "average rates on new housing loans", "Mizrahi-Tefahot questions and answers", "Bank of Jerusalem non-resident account", "Directive 329 on housing loans"]),
    ("Next step: written pre-check before signing", "section 11", ["written pre-check"]),
    ("Disclaimer and link to the office", "end of the page", ["general information, not legal or financial advice", 'href="/real-estate-lawyer/"']),
    ("Inline JSON-LD: Person (Ben Betesh), Article, FAQPage (5)", "Person kept, Article updated, Dataset added; FAQPage printed by the site from the 25 visible questions", []),
    ("Scoped style (scrollable tables)", "kept and extended (.nlu3)", ["overflow-x:auto"]),
]
for old, new_home, toks in SURVIVAL:
    for tk in toks:
        assert tk in BODY or tk in STYLE, ("lost from the live page", old, tk)

print("[post %d] new copy: %d words | %d tables, %d cells | %d svg | h2 %d, h3 %d | FAQ %d (answers %d to %d words) | figures %d | official links %d"
      % (PID, WORDS, TABLES, CELLS, SVGS, len(H2S), len(H3S), len(QS), min(wc), max(wc), FIGS, len(OFFICIAL)))
print("  gates: no long dash (text and svg), no banned word, conversions labelled with the %s, average rates with their month, svg 420 box, "
      "text >= 12px, inline styles, no h1, one calculator mount under its H2, FAQPage regex finds 25" % FXL)

# ------------------------------------------------------------------ links: internal must answer 200 with no redirect


class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kw): return None


OP = urllib.request.build_opener(NoRedir); UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}


def status(u):
    try: return OP.open(urllib.request.Request(u, headers=UA), timeout=60).status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return type(e).__name__


inner = sorted(set(h for h in re.findall(r'href="(/[^"#]*)"', BODY)))
bad = [(h, st) for h in inner for st in [status(SITE + h)] if st != 200]
assert not bad, ("internal links must answer 200", bad)
ext = sorted(set(EXT.values()))
ext_st = [(u, status(u)) for u in ext]
print("  internal links: %d, all 200 | external: %s" % (len(inner), ", ".join("%s %s" % (urllib.parse.urlsplit(u).netloc, s) for u, s in ext_st if s != 200) or "all 200"))

# ------------------------------------------------------------------ the live post (GET), guard, JSON-LD
sys.stdout.flush()  # deployskin.py re-wraps sys.stdout; flush first or the lines above are lost in a pipe
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "u3page"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/%s/%d?context=edit&_fields=id,type,link,modified,title,content,meta" % (TYPE, PID))
assert s == 200 and r.get("type") == "post", (s, r.get("type"))
raw = r["content"]["raw"]; meta = r.get("meta") or {}
assert "nlu3" not in raw, "already rewritten by this script; nothing to do"
for marker in ('[nadlan_tool id="nrm"]', "nadlan-en-article", "By Adv. Ben Betesh", "FAQ: Israeli mortgages for foreigners", "Prime is 4.75%"):
    assert marker in raw, ("the live page is not the expected baseline", marker)
assert "_yoast_wpseo_title" in meta and "_yoast_wpseo_metadesc" in meta, "Yoast meta not exposed in REST for this post"
old_h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", raw)
print("  live: post %d (%s), modified %s, %d chars, sha1 %s | title %r | %d h2: %s"
      % (PID, r["type"], r.get("modified"), len(raw), hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12], r["title"]["raw"], len(old_h2), " / ".join(old_h2)))
ld_old = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', raw, flags=re.S).group(1))
person = [n for n in ld_old["@graph"] if n.get("@type") == "Person"][0]
article = [n for n in ld_old["@graph"] if n.get("@type") == "Article"][0]
article.update({"headline": H1, "inLanguage": "en", "dateModified": UPDATED_ISO, "description": META})
dataset = {"@type": "Dataset", "name": "Average interest rates on new housing loans in Israel, by track (May to August 2026) and by term (September 2026)",
           "description": "Monthly average interest rates on new housing loans in Israel by track (fixed not linked, fixed CPI-linked, variable CPI-linked, "
                          "foreign currency linked) for May to August 2026, average mortgage rates by term for the reporting month of September 2026, the "
                          "Bank of Israel rate and prime, as published by the Bank of Israel and read on 25 October 2026.",
           "url": r["link"] + "#rates-in-2026-and-the-linkage-trap", "inLanguage": "en", "isAccessibleForFree": True, "temporalCoverage": "2026-05/2026-09",
           "creator": {"@type": "Organization", "name": "Bank of Israel", "url": "https://www.boi.org.il/en/"},
           "isBasedOn": [EXT["avg"], EXT["mashfix"], EXT["pribmash"]]}
LD = '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@graph": [person, article, dataset]}, ensure_ascii=False)
NEW = ('<!-- wp:html -->\n<div dir="ltr" lang="en" class="nadlan-en-article nlu3" style="text-align:left">' + STYLE + LD + "\n" + BODY + "</div>\n<!-- /wp:html -->")
assert '"FAQPage"' not in NEW, "one FAQPage per page: the site prints it from the visible questions"
print("  JSON-LD in content: Person (kept), Article (headline, inLanguage, dateModified %s), Dataset; FAQPage removed (site prints 25)" % UPDATED_ISO)
print("  survival of the live page:")
for old, new_home, toks in SURVIVAL:
    print("    - %s  ->  %s" % (old, new_home))

if DRY:
    pv = os.path.join(H, "preview"); os.makedirs(pv, exist_ok=True)
    mock = ('<section style="border:2px dashed #5B3FA0;padding:14px;margin:12px 0;background:#fff"><p style="margin:0 0 4px;font-size:13px;color:#4A5563">'
            'Calculator · Israeli mortgage (preview placeholder)</p><h2 style="margin:0 0 6px">Israeli mortgage calculator for non-residents</h2>'
            '<p style="margin:0">The live page mounts <code>[nadlan_tool id="nrm"]</code> here.</p></section>')
    shell = ('<!doctype html>\n<html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
             '<title>%s</title><style>body{margin:0;background:#fff;font:17px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif;color:#2B3440}'
             '.wrap{max-width:760px;margin:0 auto;padding:16px}h1{font-size:30px;line-height:1.2;color:#1E2B47}h2{font-size:24px;line-height:1.25;'
             'color:#1E2B47;margin-top:40px}h3{font-size:19px;color:#1E2B47;margin-top:26px}a{color:#0F7C7A}</style></head><body><div class="wrap">'
             '<h1>%s</h1>\n%s\n</div></body></html>\n' % (SEO_TITLE, H1, NEW.replace('[nadlan_tool id="nrm"]', mock)))
    io.open(os.path.join(pv, "u3-page-content.html"), "w", encoding="utf-8").write(shell)
    io.open(os.path.join(pv, "u3-post-content.raw.html"), "w", encoding="utf-8", newline="").write(NEW)
    print("  DRY: nothing written to the site. Preview: preview/u3-page-content.html | exact content: preview/u3-post-content.raw.html")
    print("  would POST: title %r | _yoast_wpseo_title %r (%d chars) | _yoast_wpseo_metadesc (%d chars)" % (H1, SEO_TITLE, len(SEO_TITLE), len(META)))
    sys.exit(0)

# ------------------------------------------------------------------ write, read back, live check
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True); stamp = time.strftime("%Y%m%d-%H%M%S")
io.open(os.path.join(bk, "post-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
io.open(os.path.join(bk, "post-%d-%s.meta.json" % (PID, stamp)), "w", encoding="utf-8").write(json.dumps(
    {"title": r["title"]["raw"], "_yoast_wpseo_title": meta.get("_yoast_wpseo_title"), "_yoast_wpseo_metadesc": meta.get("_yoast_wpseo_metadesc")}, ensure_ascii=False, indent=1))
s, w, _ = req("POST", "/wp-json/wp/v2/%s/%d" % (TYPE, PID), {"content": NEW, "title": H1, "meta": {"_yoast_wpseo_title": SEO_TITLE, "_yoast_wpseo_metadesc": META}})
assert s == 200, (s, str(w)[:300])
back = req("GET", "/wp-json/wp/v2/%s/%d?context=edit&_fields=content,title,meta" % (TYPE, PID))[1]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back content": back["content"]["raw"].strip() == NEW.strip(), "read-back title": back["title"]["raw"] == H1,
      "read-back Yoast": (back.get("meta") or {}).get("_yoast_wpseo_title") == SEO_TITLE and (back.get("meta") or {}).get("_yoast_wpseo_metadesc") == META,
      "one h1, the new title": bd.count("<h1") == 1 and H1 in re.sub(r"\s+", " ", " ".join(re.findall(r"<h1[^>]*>(.*?)</h1>", bd, flags=re.S))),
      "<title> is the SEO title": SEO_TITLE in page[:page.find("</title>")], "meta description": META in page.replace("&amp;", "&"),
      "calculator mounted": 'data-nli="nrm"' in bd, "4 svg in the text": bd.count("nlu3-fig") == 4,
      "one FAQPage": page.count('"@type":"FAQPage"') + page.count('"@type": "FAQPage"') == 1, "25 questions": page.count('"@type":"Question"') == 25,
      "SoftwareApplication": '"@type":"SoftwareApplication"' in page, "Dataset": '"@type": "Dataset"' in page or '"@type":"Dataset"' in page,
      "no stale prime": not re.search(r"5\.25%|July 6, 2026", visible(bd))}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
