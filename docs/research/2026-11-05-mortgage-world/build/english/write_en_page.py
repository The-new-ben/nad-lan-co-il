# -*- coding: utf-8 -*-
"""HAD-675: the English twin of /mortgage-calculator/ at /en/mortgage-calculator/ (hreflang pair with page 121).

The recipe is the one of /en/asbestos/ (8761) and /en/environmental-hazards/ (8769), docs/tools/asbestos/create_pages.py:
a WordPress PAGE under the published /en/ root page (slug "en", parent 0; id 5011 on 5.11.2026), slug "mortgage-calculator",
Yoast title and description in the post meta (_yoast_wpseo_title, _yoast_wpseo_metadesc). No language meta is needed:
inc/page-lang.php reads the language from the top ancestor's slug (en), prints <html lang="en" dir="ltr">, and pairs the page with
/mortgage-calculator/ by path (the family key is the path minus the /en/ prefix): hreflang he, en and x-default (he) on BOTH pages
once both are PUBLISHED. The page title is the H1 (the theme's pagehead); the content has no <h1>.

Needs, live, BEFORE --publish (the release, see README.md): build/english/mquick.js, build/english/mortgage-market.php, and two
hunks in inc/instruments.php (an 'en' block on the mquick registry entry, and the 'mquick' line in nadlan_nli_summary_en()).
Without them the page would show the quick calculator in Hebrew; --publish checks this and refuses.

  python write_en_page.py --build     local only: computes every number from boi-mortgage.json, writes page-en.html + seo.json
  python write_en_page.py --dry       GET only: local gates, then the site checks (en root, slug free, Hebrew twin, live components)
  python write_en_page.py             creates the page as a DRAFT (POST), saves published-en.json; no publish
  python write_en_page.py --publish   (after Ben's review, after the release) publishes the draft, then reads the live page and
                                      moves it back to draft if any check fails
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from decimal import Decimal, ROUND_HALF_UP

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
MODE = "build" if "--build" in sys.argv else "dry" if "--dry" in sys.argv else "publish" if "--publish" in sys.argv else "create"
PAGE = os.path.join(H, "page-en.html")
SEOF = os.path.join(H, "seo.json")
PUB = os.path.join(H, "published-en.json")
BASE = "https://nad-lan.co.il"
UPDATED = "5 November 2026"

# ------------------------------------------------------------------------------------------------ numbers (from the data file)
D = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "boi-mortgage.json"), encoding="utf-8"))
BB = D["by_bank"]; I = len(BB["months"]) - 1; YM = BB["months"][I]
TR = ["fixed_nl", "prime", "var_nl_other", "var_cpi", "fixed_cpi"]
ENM = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def month(ym):
    y, m = ym.split("-"); return ENM[int(m) - 1] + " " + y


def day(iso):
    y, m, d = iso.split("-"); return "%d %s %s" % (int(d), ENM[int(m) - 1], y)


def r0(x):
    return int(Decimal(repr(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def ils(x):
    return "₪{:,}".format(r0(x))


def pct(x, d=2):  # PHP number_format rounding (half up on the decimal text), so page and server blocks agree
    return str(Decimal(repr(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)) + "%"


def eff(e):
    return (1 + e / 100) ** (1 / 12) - 1


def pmt(P, r, n):
    return P * r / (1 - (1 + r) ** -n) if r else P / n


def pay(bank, loan=1e6, years=25, i=I):
    mix = BB["mix"][bank]; rate = BB["rate"][bank]; tot = sum(mix[t][i] for t in TR)
    return sum(pmt(loan * mix[t][i] / tot, eff(rate[t][i]), years * 12) for t in TR)


MON = month(YM)
P15, P20, P25, P30 = pay("system", years=15), pay("system", years=20), pay("system"), pay("system", years=30)
if YM == "2026-09":
    assert r0(P25) == 5428, r0(P25)  # the number the Hebrew page and the data headline state
RT = {t: BB["rate"]["system"][t][I] for t in TR + ["irr"]}
MX = {t: BB["mix"]["system"][t][I] for t in TR}
VAR = MX["prime"] + MX["var_nl_other"] + MX["var_cpi"]
names = {b["k"]: b["en"] for b in BB["banks"]}
big5 = ["hapoalim", "leumi", "discount", "mizrahi", "fibi"]
LO = min(big5, key=lambda b: BB["rate"][b]["irr"][I]); HI = max(big5, key=lambda b: BB["rate"][b]["irr"][I])
PRIME_HI = max(big5, key=lambda b: BB["mix"][b]["prime"][I])
POL = D["policy"]; CPI = D["cpi"]; FC = D["forecast"]; MK = D["market"]; RU = D["rules"]; FE = D["fees"]; TERM = D["term"]["nl"]
LTV_ABOVE75 = sum(b["share"] for b in MK["ltv"] if b["from"] >= 75)
LTV_60_75 = [b["share"] for b in MK["ltv"] if b["from"] == 60][0]
PTI_30_40 = [b["share"] for b in MK["pti"] if b["from"] == 30][0]
PTI_40_50 = [b["share"] for b in MK["pti"] if b["from"] == 40][0]
FX = [t["share"] for t in MK["tracks"] if t["k"] == "fx"][0]
assert RU["ltv"]["single"] == 0.75 and RU["ltv"]["replace"] == 0.7 and RU["ltv"]["invest"] == 0.5 and RU["pti_max"] == 0.5 and RU["pti_risk"] == 0.4
assert RU["term_max"] == 30 and abs(RU["variable_max"] - 0.6666) < 1e-9 and POL["rate"] == 3.25 and POL["prime"] == 4.75

# the three uniform baskets (directive 451) at this month's all-banks average rate of each track; the CPI third at var_cpi
B1 = pmt(1e6, eff(RT["fixed_nl"]), 300)
B2 = sum(pmt(1e6 / 3, eff(RT[t]), 300) for t in ("fixed_nl", "prime", "var_cpi"))
B3 = sum(pmt(5e5, eff(RT[t]), 300) for t in ("fixed_nl", "prime"))
assert B1 > B3 > B2, (B1, B2, B3)  # the text below says so


def schedule():
    """Yearly Spitzer schedule of 1,000,000 over 25 years, each track amortized on its own at its average effective rate."""
    tot = sum(MX.values()); rows = []
    bal = {t: 1e6 * MX[t] / tot for t in TR}; r = {t: eff(RT[t]) for t in TR}; m = {t: pmt(bal[t], r[t], 300) for t in TR}
    for y in range(1, 26):
        pi = pr = 0.0
        for _ in range(12):
            for t in TR:
                it = bal[t] * r[t]; p = m[t] - it; bal[t] -= p; pi += it; pr += p
        rows.append((y, pi + pr, pi, pr, max(0.0, sum(bal.values()))))
    return rows


SCH = schedule()
assert abs(SCH[-1][4]) < 1
INT_TOTAL = sum(x[2] for x in SCH)

# ------------------------------------------------------------------------------------------------ the page
FOREIGN = '<a href="/israel-mortgage-non-residents/">Israel mortgage for foreigners</a>'
HE_TERM = lambda s: '<span lang="he" dir="rtl">' + s + '</span>'

CSS = ('<style id="nlen-css">.nlen{font-family:"IBM Plex Sans",system-ui,sans-serif;color:#12202A}.nlen p,.nlen li{font-size:17px;line-height:1.7;color:#24323D}'
       '.nlen .nlen-lead{font-size:19px;line-height:1.65;color:#12202A;max-width:70ch;margin:6px 0 12px}.nlen .nlen-sub{max-width:70ch;margin:0 0 14px}'
       '.nlen-cta{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 12px}body .nlen-cta a.nlen-btn.nlen-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 18px;border-radius:999px;border:1.5px solid #2F6F86;background:#fff!important;color:#2F6F86!important;text-decoration:none!important;font-weight:600;font-size:16px;line-height:1.2}'
       'body .nlen-cta a.nlen-btn.nlen-btn.is-main{background:#2F6F86!important;color:#fff!important}a.nlen-btn:focus-visible{outline:3px solid #12202A;outline-offset:2px}'
       '.nlen .nlen-aside{font-size:15px;color:#3E4C58;border-left:3px solid #2F6F86;padding:4px 0 4px 12px;margin:0 0 16px}.nlen .nlen-aside a,.nlen .nlen-meta a,.nlen p a{color:#2F6F86}'
       '.nlen-anchor,.nlen section{scroll-margin-top:84px}.nlen h2{margin:36px 0 10px;line-height:1.25}.nlen h3{margin:24px 0 6px;font-size:20px;line-height:1.35}'
       '.nlen .nlen-t{margin:14px 0 8px;overflow-x:auto;-webkit-overflow-scrolling:touch}'
       '.nlen .nlen-t table{display:table!important;width:100%!important;border-collapse:separate;border-spacing:0;background:#fff;border:0;border-top:2px solid #12202A;border-bottom:1px solid #12202A;border-radius:0;margin:0}'
       '.nlen .nlen-t thead{display:table-header-group!important}.nlen .nlen-t tbody{display:table-row-group!important}'
       '.nlen .nlen-t tr{display:table-row!important;border:0!important;border-radius:0!important;margin:0!important;padding:0!important;background:#fff!important;box-shadow:none!important}'
       '.nlen .nlen-t caption{caption-side:top;text-align:left;padding:0 0 8px;font-size:15px;font-weight:600;color:#12202A;line-height:1.45}'
       '.nlen .nlen-t th,.nlen .nlen-t td{display:table-cell!important;width:auto!important;padding:9px 10px!important;border:0!important;border-bottom:1px solid #D3DCE2!important;font-size:15px!important;line-height:1.5!important;text-align:left!important;vertical-align:top;color:#12202A!important;background:#fff!important;font-weight:400!important;letter-spacing:0!important}'
       '.nlen .nlen-t thead th{color:#3E4C58!important;font-weight:600!important;font-size:13px!important;border-bottom:1px solid #12202A!important;vertical-align:bottom}'
       '.nlen .nlen-t tbody th{font-weight:600!important;min-width:96px}.nlen .nlen-t td.n{font-family:"IBM Plex Mono",ui-monospace,monospace!important;font-size:14.5px!important;white-space:nowrap}'
       '.nlen .nlen-meta{font-size:14px;line-height:1.7;color:#3E4C58;border-top:1px solid #D3DCE2;padding-top:10px;margin-top:10px}'
       '.nlen dl.nlen-gl{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:0;border-top:2px solid #12202A;margin:12px 0}.nlen dl.nlen-gl dt,.nlen dl.nlen-gl dd{margin:0;padding:8px 10px;border-bottom:1px solid #D3DCE2;font-size:15px;line-height:1.5}'
       '.nlen dl.nlen-gl dt{font-weight:600}.nlen dl.nlen-gl dt span{font-weight:400;color:#3E4C58;margin-left:6px}'
       '.nlen ul.nlen-list{padding-left:20px;margin:8px 0 12px}.nlen ul.nlen-list li{margin:0 0 6px}'
       '@media(max-width:640px){.nlen .nlen-lead{font-size:18px}.nlen .nlen-t th,.nlen .nlen-t td{padding:8px 8px!important;font-size:14px!important}.nlen .nlen-t td.n{font-size:13px!important;padding:8px 6px!important}.nlen dl.nlen-gl{grid-template-columns:1fr}.nlen dl.nlen-gl dt{border-bottom:0;padding-bottom:0}}</style>\n')

LEAD = ('<p class="nlen-lead">This Israel mortgage calculator works out the monthly payment on a shekel mortgage at the Bank of Israel\'s latest average rates and track mix. '
        'In ' + MON + ', a <bdi>₪1,000,000</bdi> mortgage over 25 years at the all-banks average mix cost <bdi>' + ils(P25) + '</bdi> in the first month, or <bdi>' + ils(P30) + '</bdi> over 30 years. '
        'Change the amount, term or bank below.</p>\n')
SUB = ('<p class="nlen-sub">Israeli mortgages (' + HE_TERM("משכנתא") + ', mashkanta) are split into tracks with different rates and linkage, so the payment depends on the mix as much as on any one rate. '
       'Amounts are in Israeli new shekels (NIS, ₪). Every figure on this page comes from the Bank of Israel, the Central Bureau of Statistics or the Israel Tax Authority, with its month.</p>\n')
CTA = ('<div class="nlen-cta"><a class="nlen-btn is-main" href="#quick">Calculate your payment</a><a class="nlen-btn" href="#mortgage-market">Rates by bank</a>'
       '<a class="nlen-btn" href="#amortization-schedule">Amortization schedule</a></div>\n')
ASIDE = '<p class="nlen-aside">Not an Israeli citizen, or buying from abroad? The limits are different: read ' + FOREIGN + '.</p>\n'
QUICK = '<div id="quick" class="nlen-anchor"></div>\n<!-- wp:shortcode -->\n[nadlan_tool id="mquick"]\n<!-- /wp:shortcode -->\n'
MARKET = '<!-- wp:shortcode -->\n[nadlan_mortgage_market lang="en"]\n<!-- /wp:shortcode -->\n'


def table(caption, head, rows, num_cols):
    h = '<div class="nlen-t"><table><caption>' + caption + '</caption><thead><tr>' + "".join('<th scope="col">' + c + '</th>' for c in head) + '</tr></thead><tbody>'
    for r in rows:
        h += '<tr><th scope="row">' + r[0] + '</th>' + "".join('<td' + (' class="n"' if k + 1 in num_cols else '') + '>' + c + '</td>' for k, c in enumerate(r[1:])) + '</tr>'
    return h + '</tbody></table></div>\n'


TRACKS = table(
    "Average effective annual rate and share of new mortgage credit by track, all banks, " + MON,
    ["Track", "Hebrew name", "How the rate behaves", "Average rate", "Share of new loans"],
    [["Prime", HE_TERM("פריים"), "Variable; follows the Bank of Israel rate. Prime is that rate plus 1.5 points: " + pct(POL["prime"]) + " since " + day(POL["from"]), "<bdi>" + pct(RT["prime"]) + "</bdi>", "<bdi>" + pct(MX["prime"], 1) + "</bdi>"],
     ["Fixed, not linked", HE_TERM("קל״צ") + " (kalatz)", "Fixed for the whole term, no link to the CPI", "<bdi>" + pct(RT["fixed_nl"]) + "</bdi>", "<bdi>" + pct(MX["fixed_nl"], 1) + "</bdi>"],
     ["Fixed, CPI-linked", HE_TERM("ק״צ") + " (katz)", "Fixed rate; the balance moves with the consumer price index", "<bdi>" + pct(RT["fixed_cpi"]) + "</bdi>", "<bdi>" + pct(MX["fixed_cpi"], 1) + "</bdi>"],
     ["Variable, not linked (other than prime)", HE_TERM("משתנה לא צמודה"), "Changes at set dates, for example every 5 years", "<bdi>" + pct(RT["var_nl_other"]) + "</bdi>", "<bdi>" + pct(MX["var_nl_other"], 1) + "</bdi>"],
     ["Variable, CPI-linked", HE_TERM("משתנה צמודה"), "Changes at set dates; the balance moves with the CPI", "<bdi>" + pct(RT["var_cpi"]) + "</bdi>", "<bdi>" + pct(MX["var_cpi"], 1) + "</bdi>"]],
    (3, 4))

HOW = ('<section id="how-israeli-mortgages-work">\n<h2>How Israeli mortgages work</h2>\n'
       '<p>An Israeli mortgage is rarely one loan at one rate. The bank splits it into tracks (' + HE_TERM("מסלולים") + ', maslulim), each with its own rate, its own link or no link to the consumer price index (CPI), and often its own term. '
       'You pay all the tracks together every month, so the payment depends on the mix as much as on any one rate. Nearly all of it is in shekels: in ' + month(MK["month"]) + ' loans in foreign currency were <bdi>' + pct(FX, 1) + '</bdi> of new mortgage money (Bank of Israel).</p>\n'
       '<h3>The tracks and their average rates in ' + MON + '</h3>\n' + TRACKS
       + '<p class="nlen-meta">Source: Bank of Israel, Banking Supervision, interest rate comparison for housing loans (TamInt010, ' + MON + ', file of ' + day(BB["src"]["file_date"]) + '): effective annual rates and each track\'s share of the month\'s credit. '
       'Together the variable tracks were <bdi>' + pct(VAR, 1) + '</bdi> of new mortgages, close to the two-thirds limit on variable rates.</p>\n'
       '<p>The rates are effective annual rates, the way the Bank of Israel publishes them. A CPI-linked track starts at a lower rate, but its balance and payment rise with the index: the CPI rose <bdi>' + pct(CPI["y12"]) + '</bdi> in the 12 months to ' + month(CPI["latest"]) + ' (Central Bureau of Statistics), '
       'and the Bank of Israel\'s ' + month(FC["published"][:7]) + ' forecast puts inflation at <bdi>' + pct(FC["inflation_4q"], 1) + '</bdi> over the next four quarters. The calculator keeps the index unchanged, so on linked tracks it shows the first payment, not the later ones.</p>\n'
       '<h3>The Bank of Israel rate and prime</h3>\n'
       '<p>The Bank of Israel rate has been <bdi>' + pct(POL["rate"]) + '</bdi> since ' + day(POL["from"]) + '. In 2026 it was set at ' + ", ".join(pct(r) + " on " + day(d)[:-5] for d, r in POL["path2026"][:-1]) + ' and ' + pct(POL["path2026"][-1][1]) + ' on ' + day(POL["path2026"][-1][0])[:-5] + '. '
       'Prime is that rate plus 1.5 points, <bdi>' + pct(POL["prime"]) + '</bdi>, and a prime track follows every change: a cut lowers the payment, a rise lifts it. '
       'The next rate decision is on ' + day(FC["next_decision"]) + ', and the Bank of Israel\'s ' + month(FC["published"][:7]) + ' forecast has the rate at <bdi>' + pct(FC["rate_q3_2027"], 1) + '</bdi> on average in the third quarter of 2027.</p>\n'
       '<p>The average rate in the prime track was <bdi>' + pct(RT["prime"]) + '</bdi> in ' + MON + ', below prime itself: the track is priced as prime plus or minus a margin, and on average the margin was a discount.</p>\n</section>\n')

BASKETS = ('<section id="uniform-baskets">\n<h2>The three uniform baskets in every approval in principle</h2>\n'
           '<p>Since 31 August 2022 every approval in principle (' + HE_TERM("אישור עקרוני") + ', ishur ekroni) from an Israeli bank must price the same three uniform baskets, so offers from different banks can be compared on equal terms (Bank of Israel Directive 451, circular 2694). '
           'Each basket is offered for 10, 15, 20, 25 and 30 years on a Spitzer schedule, and the approval must show the predicted total interest, the total predicted repayment and the highest predicted monthly payment.</p>\n'
           + table("First payment on ₪1,000,000 over 25 years, at the all-banks average rate of each track, " + MON,
                   ["Basket", "Mix", "First payment"],
                   [["Basket 1", "All fixed, not linked", "<bdi>" + ils(B1) + "</bdi>"],
                    ["Basket 2", "One third fixed not linked, one third prime, one third variable every 5 years, CPI-linked", "<bdi>" + ils(B2) + "</bdi>"],
                    ["Basket 3", "Half fixed not linked, half prime", "<bdi>" + ils(B3) + "</bdi>"]], (2,))
           + '<p class="nlen-meta">Our calculation at the Bank of Israel averages for ' + MON + ' (TamInt010); the CPI-linked third at the average variable CPI-linked rate, with the index unchanged. Your bank\'s rates will differ.</p>\n'
           '<p>The baskets are a yardstick, not advice. At these averages basket 1 has the highest first payment and keeps it for the whole term; basket 2 starts lowest because its linked third starts at a lower rate and then moves with the index; '
           'basket 3 sits between them and moves with prime on half the loan.</p>\n</section>\n')

LIMITS = ('<section id="bank-of-israel-limits">\n<h2>What the Bank of Israel allows: down payment, income, mix and term</h2>\n'
          + table("Bank of Israel Directive 329, limits on housing loans (version of 8 February 2026, updated 30 June 2026)",
                  ["Rule", "Limit", "Section"],
                  [["Loan to value, single home", "Up to 75% of the value, so at least 25% equity", "s.2"],
                   ["Loan to value, replacement home", "Up to 70% when you are selling your current home", "s.2"],
                   ["Loan to value, additional home", "Up to 50%", "s.2"],
                   ["Reduced-price homes (Mechir LaMishtaken, Mechir Matara)", "The buyer pays at least ₪100,000 of their own money (₪60,000 with the new Mechir LaMishtaken grant); the value may rest on an appraisal, capped at ₪2.1 million or the price if higher", "s.4A"],
                   ["Payment to income", "Up to 50% of disposable income; above 40% the bank must hold more capital against the loan", "s.5, s.6"],
                   ["Variable-rate part", "At most 66.66% of the loan, so at least one third fixed", "s.7"],
                   ["Term", "Up to 30 years", "s.8"],
                   ["Any-purpose loan on a home", "50% of the value, up to 70% if the part above 50% is at most ₪200,000", "s.4, s.10A"]], ())
          + '<p>In practice most borrowers stay well inside the limits. In ' + month(MK["month"]) + ' the average payment on new mortgages was <bdi>' + pct(MK["pti_avg"]) + '</bdi> of income; <bdi>' + pct(PTI_30_40, 1) + '</bdi> of new mortgage money went to loans at 30% to 40% of income and only <bdi>' + pct(PTI_40_50, 1) + '</bdi> to loans at 40% to 50%. '
          '<bdi>' + pct(LTV_60_75, 1) + '</bdi> went to loans at 60% to 75% of the value and about <bdi>' + pct(LTV_ABOVE75) + '</bdi> above 75% (Bank of Israel, new housing loans, BIR_MRTG_99). '
          'In ' + month(MK["month"]) + ' the average term of new loans not linked to the CPI was <bdi>' + "{:.1f}".format(MK["term_nl"]) + '</bdi> years.</p>\n</section>\n')

PREPAY = ('<section id="early-repayment">\n<h2>Paying off early: fees and when they apply</h2>\n'
          '<p>Early repayment of an Israeli housing loan is governed by the Banking Order (Early Repayment of a Housing Loan), 2002, as amended in 2014. The main points:</p>\n<ul class="nlen-list">'
          '<li>An operational fee of up to <bdi>₪' + str(FE["operational_max"]) + '</bdi>.</li>'
          '<li><bdi>0.1%</bdi> of the amount if you give less than ' + str(FE["notice_days"]) + ' days\' notice; it is not charged when the bank itself refinances the loan or after the borrower\'s death. Notice can be given up to ' + str(FE["notice_max_days"]) + ' days ahead.</li>'
          '<li>A capitalization fee on fixed-rate tracks, only when the current average rate is below your loan\'s rate; the bank charges the lower of two formulas.</li>'
          '<li>No capitalization fee on tracks whose rate changes at least once a year or at unknown dates, such as prime, and none on a rate-change date.</li>'
          '<li>On CPI-linked tracks repaid between the 1st and the 15th of the month: half the average monthly CPI change of the last 12 indices.</li>'
          '<li>The capitalization fee is cut by 20% after 3 years and by 30% after 5 years (on complementary loans by 10%, 20%, 30% and 40% after 1, 2, 3 and 4 years).</li>'
          '<li>State eligibility loans (directed loans): no fee.</li></ul>\n'
          '<p>The average rates used for the fee are published monthly by the Bank of Israel. For loans not linked to the CPI, the ' + month(TERM["month"][:7]) + ' averages in force from ' + day(TERM["inforce"]) + ' ran from <bdi>' + pct(TERM["buckets"][0]["eff"]) + '</bdi> for terms up to one year to <bdi>' + pct(TERM["buckets"][-1]["eff"]) + '</bdi> for terms over 25 years.</p>\n</section>\n')

OLIM = ('<section id="olim">\n<h2>Olim and returning residents: what to check before you borrow</h2>\n'
        '<p>The rules above apply to every borrower at an Israeli bank. A few of them matter more when the Israeli system is new to you.</p>\n'
        '<h3>Citizenship decides the single-home cap</h3>\n'
        '<p>Directive 329 allows up to 75% of the value for a single home, 70% for a replacement home and 50% for an additional home. A buyer who is not an Israeli citizen cannot count as a single-home buyer, so the cap is 50%. If that is your case, read ' + FOREIGN + '.</p>\n'
        '<h3>How the bank counts your income</h3>\n'
        '<p>The payment test is against disposable income: net income minus fixed commitments that run longer than 18 months, alimony, and rent if you will not live in the home you are buying. '
        'A spouse who lives with you counts in full; half of the income of a first-degree relative who guarantees the loan may count. The payment may be up to 50% of that income, and above 40% the bank must hold more capital against the loan.</p>\n'
        '<h3>The eligibility loan counts years since immigration</h3>\n'
        '<p>The state eligibility loan (' + HE_TERM("משכנתא בזכאות") + ', mashkanta bezakaut) is a CPI-linked, fixed-rate loan whose amount and terms the government sets by points: years of marriage or since immigration, children, siblings and service, plus a place loan in priority areas. '
        'It can be repaid early with no fee and no notice. Ask the bank for the amount that applies to you.</p>\n'
        '<h3>Compare offers in the same format</h3>\n'
        '<p>Every approval in principle carries the three uniform baskets with the total predicted repayment and the highest predicted payment, so offers can be read side by side even when the rest of the paperwork is in Hebrew. '
        'Take each bank\'s rate per track and compare it with that bank\'s ' + MON + ' average in the table by bank above.</p>\n'
        '<h3>Words you will see</h3>\n<dl class="nlen-gl">'
        + "".join('<dt>' + a + ' <span lang="he" dir="rtl">' + b + '</span></dt><dd>' + c + '</dd>' for a, b, c in (
            ("Mashkanta", "משכנתא", "Mortgage"), ("Ishur ekroni", "אישור עקרוני", "Approval in principle, the bank's offer before you sign"),
            ("Maslul", "מסלול", "Track, one part of the mortgage with its own rate"), ("Prime", "פריים", "The variable track that follows the Bank of Israel rate"),
            ("Kalatz", "קל״צ", "Fixed rate, not linked to the CPI"), ("Katz", "ק״צ", "Fixed rate, linked to the CPI"),
            ("Mishtana", "משתנה", "Variable rate, changing at set dates"), ("Madad", "מדד", "The consumer price index (CPI)"),
            ("Hon atzmi", "הון עצמי", "Your own money in the purchase (equity)"), ("Luach silukin", "לוח סילוקין", "Amortization schedule")))
        + '</dl>\n<p class="nlen-meta">Sources: Directive 329 (8 February 2026, updated 30 June 2026); the eligibility loan from a bank disclosure (Mizrahi-Tefahot, read 25 October 2026) and the Banking Order (Early Repayment of a Housing Loan), 2002, s.2.</p>\n</section>\n')


def t_row(r):
    return '<tr><th scope="row">' + str(r[0]) + '</th><td class="n"><bdi>' + ils(r[1]) + '</bdi></td><td class="n"><bdi>' + ils(r[2]) + '</bdi></td><td class="n"><bdi>' + ils(r[3]) + '</bdi></td><td class="n"><bdi>' + ils(r[4]) + '</bdi></td></tr>'


SCHED = ('<section id="amortization-schedule">\n<h2>Amortization schedule: ₪1,000,000 over 25 years</h2>\n'
         '<p>A yearly amortization schedule (' + HE_TERM("לוח סילוקין") + ', luach silukin) for <bdi>₪1,000,000</bdi> over 25 years at the all-banks average mix and rates of ' + MON + ', on a Spitzer schedule: each track repays with its own fixed payment, and the CPI-linked tracks with the index unchanged. '
         'In year 1 you pay <bdi>' + ils(SCH[0][1]) + '</bdi>, of which <bdi>' + ils(SCH[0][2]) + '</bdi> is interest and only <bdi>' + ils(SCH[0][3]) + '</bdi> principal; by the last year almost all of the payment is principal. '
         'Total interest over the term: <bdi>' + ils(INT_TOTAL) + '</bdi>.</p>\n'
         '<div class="nlen-t"><table><caption>Yearly amortization: ₪1,000,000 over 25 years, average mix of ' + MON + '</caption><thead><tr><th scope="col">Year</th><th scope="col">Paid in the year</th><th scope="col">Interest</th><th scope="col">Principal</th><th scope="col">Balance at year end</th></tr></thead><tbody>'
         + "".join(t_row(r) for r in SCH) + '</tbody></table></div>\n'
         '<p class="nlen-meta">Rates and mix: Bank of Israel, interest rate comparison for housing loans (' + MON + '). Our calculation; your payments depend on the rate you get, the CPI and changes in prime.</p>\n</section>\n')

MYTHS = ('<section id="rules-facts">\n<h2>Four mortgage rules that are often stated wrong</h2>\n'
         '<p>Some answers about Israeli mortgages, including summaries shown in search results, repeat rules that have changed or never existed. This is what Directive 329 of the Bank of Israel says today.</p>\n'
         '<h3>Only a third in prime? There is no such cap</h3>\n'
         '<p>No rule today limits prime to a third of the mortgage. The limit is on the whole variable part, prime and the other variable tracks together: at most <bdi>66.66%</bdi> of the loan, so at least a third at a fixed rate (Directive 329, s.7). '
         'In ' + MON + ' prime was <bdi>' + pct(MX["prime"], 1) + '</bdi> of new mortgages across the banks, and <bdi>' + pct(BB["mix"][PRIME_HI]["prime"][I], 1) + '</bdi> at ' + names[PRIME_HI] + ', according to the Bank of Israel.</p>\n'
         '<h3>Payment up to 40% of income? The limit is 50%</h3>\n'
         '<p>The monthly payment may be up to <bdi>50%</bdi> of disposable income. Above <bdi>40%</bdi> the bank must hold more capital against the loan, which is why most loans stay below it: in ' + month(MK["month"]) + ' the average payment on new mortgages was <bdi>' + pct(MK["pti_avg"]) + '</bdi> of income (Directive 329, s.5; Bank of Israel).</p>\n'
         '<h3>A 40-year mortgage? Banks lend for up to 30 years</h3>\n'
         '<p>The longest term for a bank housing loan is <bdi>30</bdi> years (Directive 329, s.8). A longer term lowers the payment and raises the interest: <bdi>₪1,000,000</bdi> over 30 years costs <bdi>' + ils(P30) + '</bdi> in the first month against <bdi>' + ils(P25) + '</bdi> over 25 years, at the ' + MON + ' average mix.</p>\n'
         '<h3>60% for buyers who are not citizens? The cap is 50%</h3>\n'
         '<p>A buyer who is not an Israeli citizen cannot count as a single-home buyer, so the maximum is <bdi>50%</bdi>, as for an additional home. A single home: up to <bdi>75%</bdi>; a replacement home: up to <bdi>70%</bdi> (Directive 329, s.2 and its definitions).</p>\n'
         '<p class="nlen-meta">Source: Bank of Israel, Proper Conduct of Banking Business Directive 329, limits on housing loans (version of 8 February 2026, updated 30 June 2026); payment to income: Bank of Israel, new housing loans.</p>\n</section>\n')


def qa(q, a):
    return '<h3>' + q + '</h3>\n<p>' + a + '</p>\n'


FAQ = ('<section id="faq">\n<h2>Frequently asked questions</h2>\n'
       + qa("What are mortgage rates in Israel today?",
            "The latest Bank of Israel figures are for " + MON + ". Across all banks the forecast all-in rate (IRR) on new mortgages averaged " + pct(RT["irr"]) + "; by track, fixed not linked averaged " + pct(RT["fixed_nl"]) + ", the prime track " + pct(RT["prime"]) + ", fixed CPI-linked " + pct(RT["fixed_cpi"]) + " and variable CPI-linked " + pct(RT["var_cpi"]) + " (effective annual rates). The Bank of Israel rate is " + pct(POL["rate"]) + " and prime " + pct(POL["prime"]) + ". The table by bank on this page updates every month.")
       + qa("How much is the monthly payment on a 1 million shekel mortgage in Israel?",
            "At the all-banks average mix and rates of " + MON + ", the first payment on ₪1,000,000 is " + ils(P25) + " over 25 years, " + ils(P20) + " over 20 years, " + ils(P15) + " over 15 years and " + ils(P30) + " over 30 years (Spitzer schedule, CPI-linked tracks with the index unchanged).")
       + qa("How much of a down payment do I need to buy a home in Israel?",
            "At least 25% of the value for a single home, since banks may lend up to 75%; 30% for a replacement home and 50% for an additional home. For reduced-price homes such as Mechir LaMishtaken the buyer pays at least ₪100,000 of their own money, or ₪60,000 with the new grant (Directive 329). Purchase tax, the lawyer and other costs are paid from your own money on top.")
       + qa("How much mortgage can I get on my salary in Israel?",
            "The payment can be up to 50% of disposable income, and above 40% the loan costs the bank more capital, so most loans stay below. For example, the " + MON + " average payment on ₪1,000,000 over 25 years, " + ils(P25) + ", needs disposable income of at least " + ils(r0(P25) / 0.5) + " at the 50% limit, or " + ils(r0(P25) / 0.4) + " to stay at 40%. The calculator's monthly payment mode shows the loan a payment carries.")
       + qa("What is the prime rate in Israel?",
            "Prime is the Bank of Israel rate plus 1.5 points: " + pct(POL["prime"]) + " since " + day(POL["from"]) + ", when the Bank of Israel rate was cut to " + pct(POL["rate"]) + ". The next rate decision is on " + day(FC["next_decision"]) + ".")
       + qa("What is the Bank of Israel interest rate now?",
            pct(POL["rate"]) + ", in force since " + day(POL["from"]) + ". In 2026 it was set at " + ", ".join(pct(r) + " on " + day(d)[:-5] for d, r in POL["path2026"][:-1]) + " and " + pct(POL["path2026"][-1][1]) + " on " + day(POL["path2026"][-1][0])[:-5] + ". The Bank of Israel's " + month(FC["published"][:7]) + " forecast has it at " + pct(FC["rate_q3_2027"], 1) + " on average in the third quarter of 2027.")
       + qa("Which Israeli bank has the lowest mortgage rates?",
            "There is no single answer, because each borrower gets a personal rate. By the Bank of Israel's averages for " + MON + ", the lowest forecast all-in rate among the five largest banks was " + pct(BB["rate"][LO]["irr"][I]) + " at " + names[LO] + " and the highest " + pct(BB["rate"][HI]["irr"][I]) + " at " + names[HI] + ". An average is not an offer: get approvals in principle from several banks and compare the three uniform baskets.")
       + qa("What is a mashkanta?",
            "Mashkanta is the Hebrew word for a mortgage, a loan secured on a home. In Israel it is usually split into tracks with different rates and linkage, such as prime, fixed not linked (kalatz) and fixed CPI-linked (katz).")
       + qa("Can my whole mortgage be in prime?",
            "No. Prime counts as a variable rate, and the variable part of the loan, prime and the other variable tracks together, may be at most 66.66% (Directive 329, s.7). There is no separate one-third cap on prime.")
       + qa("What is the longest mortgage term in Israel?",
            "30 years at the banks (Directive 329, s.8). At the " + MON + " average mix, ₪1,000,000 over 30 years costs " + ils(P30) + " in the first month against " + ils(P25) + " over 25 years, but the total interest is higher: " + ils(P30 * 360 - 1e6) + " against " + ils(P25 * 300 - 1e6) + ".")
       + qa("Can olim get a mortgage in Israel?",
            "Yes, from the same banks and under the same Directive 329 limits as any borrower. An Israeli citizen buying a single home can borrow up to 75% of the value; a buyer who is not a citizen is limited to 50%. Years since immigration count toward the points of the state eligibility loan.")
       + qa("How does inflation affect an Israeli mortgage?",
            "Only the CPI-linked tracks move with inflation: their balance and payment rise with the consumer price index. The CPI rose " + pct(CPI["y12"]) + " in the 12 months to " + month(CPI["latest"]) + ", and the Bank of Israel's " + month(FC["published"][:7]) + " forecast is " + pct(FC["inflation_4q"], 1) + " over the next four quarters. Prime and the other tracks that are not linked do not move with the CPI, but prime moves with the Bank of Israel rate.")
       + qa("Is there a penalty for paying off a mortgage early in Israel?",
            "Sometimes. Fixed-rate tracks can carry a capitalization fee when the current average rate is below your loan's rate; prime and tracks whose rate changes at least once a year have none. There is also an operational fee of up to ₪60, and 0.1% if you give less than 10 days' notice. The capitalization fee is cut by 20% after 3 years and by 30% after 5 years (Banking Order, 2002).")
       + qa("What are the three uniform baskets?",
            "Three standard mixes that every approval in principle must price, so banks can be compared: basket 1 is all fixed not linked; basket 2 is a third fixed not linked, a third prime and a third variable every 5 years, CPI-linked; basket 3 is half fixed not linked and half prime (Directive 451, in force since 31 August 2022). At the " + MON + " averages their first payments on ₪1,000,000 over 25 years are " + ils(B1) + ", " + ils(B2) + " and " + ils(B3) + ".")
       + qa("What is a Spitzer amortization schedule?",
            "A Spitzer schedule keeps the payment on each track constant, so early payments are mostly interest and later ones mostly principal. On ₪1,000,000 over 25 years at the " + MON + " average mix, year one costs " + ils(SCH[0][1]) + ", of which " + ils(SCH[0][2]) + " is interest and " + ils(SCH[0][3]) + " principal. The full yearly schedule is on this page.")
       + '</section>\n')

SOURCES = ('<section id="sources">\n<h2>Sources and method</h2>\n'
           '<p>Rates, track mix and the forecast all-in rate by bank: Bank of Israel, Banking Supervision, interest rate comparison for housing loans (TamInt010, ' + MON + ', file of ' + day(BB["src"]["file_date"]) + '). '
           'New mortgages, payment to income and loan-to-value bands: Bank of Israel, new housing loans (BIR_MRTG_99, ' + month(MK["month"]) + '). Bank of Israel rate: series MNT_RIB_BOI_D; forecast: Bank of Israel Research Department, ' + month(FC["published"][:7]) + '. '
           'CPI: Central Bureau of Statistics, series 120010. Average rates for early-repayment fees: Bank of Israel, in force from ' + day(TERM["inforce"]) + '. '
           'Rules: Directive 329 (8 February 2026, updated 30 June 2026), Directive 451 (circular 2694), the Banking Order (Early Repayment of a Housing Loan), 2002. Home prices: Israel Tax Authority medians of closed deals.</p>\n'
           '<p>Method: each track is repaid on its own Spitzer schedule, with the monthly rate converted from the effective annual rate, and the CPI-linked tracks with the index unchanged. The payments are averages, not offers. Updated ' + UPDATED + '.</p>\n'
           '<p class="nlen-meta">This page in Hebrew, with the full track-by-track calculator, four mixes side by side and a check of a bank offer: <a href="/mortgage-calculator/" hreflang="he" lang="he">מחשבון משכנתא</a>.</p>\n</section>\n')

HTML = CSS + '<div class="nlen">\n' + LEAD + SUB + CTA + ASIDE + QUICK + MARKET + HOW + BASKETS + LIMITS + PREPAY + OLIM + SCHED + MYTHS + FAQ + SOURCES + '</div>\n'

SEO = {
    "title": "Israeli Mortgage Calculator: Monthly Payment, Track Mix and Amortization",
    "slug": "mortgage-calculator",
    "parent": "EN_ROOT",
    "parent_seen": 5011,
    "status": "draft",
    "seo_title": "Israel Mortgage Calculator 2026: Payments, Rates, Schedule",
    "seo_desc": "Israeli mortgage calculator in English: monthly payment in NIS at the latest Bank of Israel rates by bank and track, amortization schedule and 2026 rules.",
    "meta": ["_yoast_wpseo_title", "_yoast_wpseo_metadesc"],
    "tools": ["mquick"],
    "shortcodes": ['[nadlan_tool id="mquick"]', '[nadlan_mortgage_market lang="en"]'],
    "not_mounted": {"mortgage": "tools/mortgage.js is Hebrew only (its header: 'Hebrew only (RTL)'; no langOf) and its registry entry has no 'en' block"},
    "hreflang": {"he": BASE + "/mortgage-calculator/", "en": BASE + "/en/mortgage-calculator/", "x-default": BASE + "/mortgage-calculator/",
                 "how": "inc/page-lang.php nadlan_pglang_family(): same path minus the /en/ prefix, both published"},
    "owns": ["israel mortgage calculator", "mortgage calculator israel", "israeli mortgage calculator", "israel mortgage rates", "mashkanta calculator", "amortization schedule israel"],
    "never_targets": "foreigners and non-residents (owner: /israel-mortgage-non-residents/, post 4962); linked with the exact anchor 'Israel mortgage for foreigners'",
    "mquick_en": {"name": "Quick mortgage calculator", "kicker": "Calculator · Mortgage",
                  "desc": "A quick Israeli mortgage calculator: the first monthly payment, the total repaid and the interest by mortgage amount, by home price and equity, or by the monthly payment that suits you, over 15 to 30 years, at the average track mix and rates of all banks or of one bank, from the latest Bank of Israel data."},
    "data": {"month": YM, "pay_1m_25y": r0(P25), "built": D.get("built")},
    "forbid": ["—", "–", "Atlas", "atlas", "platform", "algorithm", "demo", "coming soon", "AI-powered", "Nadlan smart", "best in the world", "guaranteed"],
}


# ------------------------------------------------------------------------------------------------ local gates
def visible(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"\[[a-z_]+[^\]]*\]", " ", h); h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h.replace("&nbsp;", " ")).strip()


def gates(html, seo):
    v = visible(html)
    faq = re.search(r'<h2[^>]*>\s*Frequently asked questions[^<]{0,60}</h2>(.*?)(?=<h2|$)', re.sub(r"<!--.*?-->", "", html, flags=re.S), re.S)
    pairs = re.findall(r'<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)', faq.group(1), re.S) if faq else []
    lead = re.search(r'<p class="nlen-lead">(.*?)</p>', html, re.S).group(1)
    lead_words = len(visible(lead).split())
    ids = set(re.findall(r'\sid="([^"]+)"', html)) | {"mortgage-market"}  # mortgage-market: the server block's own id
    heads = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", html, re.S)
    order = [html.index(x) for x in ('class="nlen-lead"', 'class="nlen-cta"', '[nadlan_tool id="mquick"]', '[nadlan_mortgage_market lang="en"]', '<h2>How Israeli mortgages work', '<h2>Frequently asked questions')]
    g = {
        "no <h1> in the content (the page title is the H1)": "<h1" not in html,
        "exactly one [nadlan_tool id=\"mquick\"]": html.count('[nadlan_tool id="mquick"]') == 1 and html.count("[nadlan_tool") == 1,
        "the full Hebrew tool is not mounted": '[nadlan_tool id="mortgage"]' not in html,
        "exactly one [nadlan_mortgage_market lang=\"en\"]": html.count("[nadlan_mortgage_market") == 1 and html.count('[nadlan_mortgage_market lang="en"]') == 1,
        "order: lead, CTAs, mquick, market, guide, FAQ": order == sorted(order),
        "answer paragraph 40 to 60 words with this month's number": 40 <= lead_words <= 60 and ils(P25) in lead,
        "FAQ: 15 h3 + p pairs under 'Frequently asked questions'": len(pairs) == 15,
        "exact anchor to the foreigners page": html.count(FOREIGN) >= 1,
        "no heading targets foreigners or non-residents": not any(re.search(r"foreign|non-resident", visible(x), re.I) for x in heads),
        "no long dash anywhere": not re.search(r"[–—]", html + seo["seo_title"] + seo["seo_desc"] + seo["title"]),
        "no spaced hyphen in visible text": not re.search(r"(?:^|\s)-{1,3}(?:\s|$)", v),
        "no forbidden word": not [w for w in seo["forbid"] if w in v or w in seo["seo_title"] or w in seo["seo_desc"] or w in seo["title"]],
        "every in-page link has a target": all(a in ids for a in re.findall(r'href="#([^"]+)"', html)),
        "Yoast title <= 60 and head term first": len(seo["seo_title"]) <= 60 and seo["seo_title"].startswith("Israel Mortgage Calculator"),
        "meta description <= 158": len(seo["seo_desc"]) <= 158,
        "H1, title and breadcrumb differ": seo["title"] != seo["seo_title"],
        "no ASCII straight double quote in visible text": '"' not in v,
    }
    return g, v, len(pairs), lead_words


# ------------------------------------------------------------------------------------------------ site (GET helpers; writes only in create/publish)
def site_req():
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
    ns = {"__name__": "mw_en_page"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
    return ns["req"]


def public_get(path, raw=False):
    r = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0 NadLan-EN-twin/1.0"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        b = resp.read(); return resp.status, (b.decode("utf-8", "replace") if raw else json.loads(b.decode() or "null"))


def live_components():
    """The English capability of the live components (no admin needed): mquick.js English strings, and the English summary in a live tool."""
    out = {}
    try:
        s, h = public_get("/wp-json/nadlan/v1/health"); out["version"] = h.get("version")
    except Exception as e:
        out["version"] = "unreadable: %s" % e
    try:
        s, js = public_get("/wp-content/plugins/nadlan-config/assets/instruments/tools/mquick.js?nlv=%d" % time.time(), raw=True)
        out["mquick.js speaks English"] = "Quick mortgage calculator" in js and "nlmq-css-en" in js
    except Exception as e:
        out["mquick.js speaks English"] = False
    return out


if MODE == "build":
    io.open(PAGE, "w", encoding="utf-8", newline="\n").write(HTML)
    io.open(SEOF, "w", encoding="utf-8", newline="\n").write(json.dumps(SEO, ensure_ascii=False, indent=1) + "\n")

html = io.open(PAGE, encoding="utf-8").read()
seo = json.load(io.open(SEOF, encoding="utf-8"))
if MODE == "build" and html != HTML:
    raise SystemExit("FATAL: page-en.html differs from the build")
if MODE != "build" and html != HTML:
    print("[warn] page-en.html differs from a fresh build (a newer data file?); the reviewed page-en.html is what gets sent")
g, v, nfaq, lw = gates(html, seo)
for k, ok in g.items():
    print("  ", "OK " if ok else "BAD", k)
print("[page] %s chars, about %s visible words, FAQ %d, lead %d words, H1 '%s' | SEO title %d: %s | desc %d"
      % ("{:,}".format(len(html)), "{:,}".format(len(v.split())), nfaq, lw, seo["title"], len(seo["seo_title"]), seo["seo_title"], len(seo["seo_desc"])))
print("[numbers] %s: 1M/25y %s, 20y %s, 30y %s, 15y %s | IRR %s | baskets %s / %s / %s | year 1 interest %s, total interest %s"
      % (MON, ils(P25), ils(P20), ils(P30), ils(P15), pct(RT["irr"]), ils(B1), ils(B2), ils(B3), ils(SCH[0][2]), ils(INT_TOTAL)))
if not all(g.values()):
    raise SystemExit("FATAL: a local gate failed")
if MODE == "build":
    print("[build] wrote page-en.html and seo.json (local only)")
    raise SystemExit(0)

# ---------------------------------------------------------------------------------------- GET checks (dry, create, publish)
req = site_req()
s, b, _ = req("GET", "/wp-json/wp/v2/pages?slug=en&parent=0&_fields=id,link,status")
roots = [x for x in (b or []) if x.get("status") == "publish"] if isinstance(b, list) else []
if len(roots) != 1:
    raise SystemExit("FATAL: the /en/ root page: %s %s" % (s, b))
PARENT = roots[0]["id"]
print("[get] /en/ root:", PARENT, roots[0]["link"])
s, he, _ = req("GET", "/wp-json/wp/v2/pages?slug=mortgage-calculator&parent=0&_fields=id,link,status")
he = [x for x in (he or []) if x.get("status") == "publish"] if isinstance(he, list) else []
if len(he) != 1 or he[0]["id"] != 121:
    raise SystemExit("FATAL: the Hebrew twin /mortgage-calculator/ (page 121, root path, published): %s" % he)
print("[get] Hebrew twin:", he[0]["id"], he[0]["link"])
s, taken, _ = req("GET", "/wp-json/wp/v2/pages?slug=%s&parent=%d&status=publish,draft,private,pending,future&context=edit&_fields=id,status,link" % (seo["slug"], PARENT))
mine = json.load(io.open(PUB, encoding="utf-8")) if os.path.exists(PUB) else {}
others = [x for x in (taken or []) if x.get("id") != mine.get("id")] if isinstance(taken, list) else None
print("[get] slug %s under %d: %s" % (seo["slug"], PARENT, "free" if others == [] else others if others is not None else "unknown (HTTP %s)" % s))
if others:
    raise SystemExit("FATAL: the slug is taken under /en/")
for t in ("pages", "posts"):
    s, hits, _ = req("GET", "/wp-json/wp/v2/%s?search=%s&_fields=id,title,link&per_page=20" % (t, urllib.parse.quote(seo["title"][:40])))
    same = [x for x in (hits or []) if re.sub(r"<[^>]+>", "", x["title"]["rendered"]).strip() == seo["title"] and x.get("id") != mine.get("id")]
    if same:
        raise SystemExit("FATAL: the same title exists: %s" % same)
print("[get] no page or post with the same title")
s, fp, _ = req("GET", "/wp-json/wp/v2/posts/4962?_fields=id,link,status")
print("[get] foreigners page (link target):", s, fp.get("link") if isinstance(fp, dict) else fp)
if not (s == 200 and fp.get("link") == BASE + "/israel-mortgage-non-residents/"):
    raise SystemExit("FATAL: /israel-mortgage-non-residents/ is not where the page links")
lc = live_components()
print("[get] live components:", lc)
if MODE == "dry":
    print("[dry] GET only; nothing written to the site. Next: release the components (README), then run without flags for the draft.")
    raise SystemExit(0)

# ------------------------------------------------------------------------------------------------ create the DRAFT
if MODE == "create":
    if mine.get("id"):
        raise SystemExit("FATAL: published-en.json already names page %s; use --publish, or remove the file after checking" % mine["id"])
    if not lc.get("mquick.js speaks English"):
        print("[warn] the live mquick.js has no English yet: the draft will show the quick calculator in Hebrew until the release")
    s, b, _ = req("POST", "/wp-json/wp/v2/pages", {"title": seo["title"], "slug": seo["slug"], "status": "draft", "content": html, "parent": PARENT,
                                                   "meta": {"_yoast_wpseo_title": seo["seo_title"], "_yoast_wpseo_metadesc": seo["seo_desc"]}})
    if s not in (200, 201) or not b.get("id"):
        raise SystemExit("FATAL create %s: %s" % (s, json.dumps(b, ensure_ascii=False)[:300]))
    s2, back, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,status,parent,slug,content,meta" % b["id"])
    ok = {"draft": back.get("status") == "draft", "parent": back.get("parent") == PARENT, "slug": back.get("slug") == seo["slug"],
          "content read-back": back["content"]["raw"].strip() == html.strip(), "yoast title": (back.get("meta") or {}).get("_yoast_wpseo_title") == seo["seo_title"],
          "yoast description": (back.get("meta") or {}).get("_yoast_wpseo_metadesc") == seo["seo_desc"]}
    for k, v_ in ok.items():
        print("  ", "OK " if v_ else "BAD", k)
    json.dump({"id": b["id"], "status": "draft", "parent": PARENT, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, io.open(PUB, "w", encoding="utf-8"))
    print("[draft]", b["id"], "edit: %s/wp-admin/post.php?post=%d&action=edit" % (BASE, b["id"]))
    raise SystemExit(0 if all(ok.values()) else 1)

# ------------------------------------------------------------------------------------------------ publish (after review + release)
if not mine.get("id"):
    raise SystemExit("FATAL: no draft yet (published-en.json); run without flags first")
if not lc.get("mquick.js speaks English"):
    raise SystemExit("FATAL: the live mquick.js has no English: release build/english/ (README) before publishing")
pid = mine["id"]
s, b, _ = req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"status": "publish"})
if s != 200:
    raise SystemExit("FATAL publish %s" % s)
link = b["link"]
print("[published]", pid, link)
time.sleep(5)
live = urllib.request.urlopen(urllib.request.Request(link + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
body = live[live.find("<body"):]
ds = re.search(r'<script type="application/ld\+json" id="nadlan-mm-dataset">(.*?)</script>', live, re.S)
ld = re.search(r'<script type="application/ld\+json" id="nadlan-nli-ld">(.*?)</script>', live, re.S)
hl = dict((a, u) for a, u in re.findall(r'<link rel="alternate" hreflang="([\w-]+)" href="([^"]+)"', live))
checks = {
    "url": link == BASE + "/en/mortgage-calculator/",
    "html lang en ltr": 'lang="en" dir="ltr"' in live[:3000],
    "one h1": body.count("<h1") == 1,
    "hreflang he/en/x-default": hl.get("he") == BASE + "/mortgage-calculator/" and hl.get("en") == link and hl.get("x-default") == BASE + "/mortgage-calculator/",
    "mquick section in English": 'lang="en" aria-label="Quick mortgage calculator"' in body and 'data-nli="mquick"' in body,
    "mquick English summary": "over 25 years, <bdi>₪" in body,
    "mquick.js enqueued": "tools/mquick.js" in live,
    "market block in English": '<section class="nlmm" id="mortgage-market" dir="ltr" lang="en"' in body,
    "Dataset in English": bool(ds) and '"inLanguage":"en"' in ds.group(1),
    "one FAQPage, 15 questions": live.count('"@type":"FAQPage"') == 1 and bool(ld) and ld.group(1).count('"@type":"Question"') == 15,
    "no raw shortcode": "[nadlan_tool" not in body and "[nadlan_mortgage_market" not in body,
    "Yoast title": "<title>" + seo["seo_title"] in live,
    "no Hebrew tool on the page": 'aria-label="מחשבון משכנתא מהיר"' not in body,
}
for k, v_ in checks.items():
    print("  ", "OK " if v_ else "BAD", k)
try:
    hp = urllib.request.urlopen(urllib.request.Request(BASE + "/mortgage-calculator/?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    print("   (info) the Hebrew page now lists hreflang en:", ('hreflang="en" href="' + link + '"') in hp, "(a cached copy can lag until the cache is purged)")
except Exception as e:
    print("   (info) Hebrew page not read:", e)
if not all(checks.values()):
    print("[draft again]", req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"status": "draft"})[0])
    raise SystemExit(1)
json.dump({"id": pid, "status": "publish", "link": link, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, io.open(PUB, "w", encoding="utf-8"))
print("[done]", link)
