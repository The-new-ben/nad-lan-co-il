# -*- coding: utf-8 -*-
"""
Counted benchmark: https://nad-lan.co.il/mortgage-calculator/ against the Israeli top results and the world's
leading mortgage-calculator pages (HAD-675, 5.11.2026).

Research and measurement only. Nothing is submitted, no form is filled, no consent is clicked.
Politeness: ONE browser load per page per pass (cold context), plus one robots.txt and one llms.txt request
per domain. A page behind a bot check is recorded as blocked and is never "solved".

Usage (Python 3.11, only `requests` and `playwright` are needed; Chrome must be installed):
    python measure.py measure [--only id1,id2] [--cache DIR]   # loads the pages, writes proof.json
    python measure.py verify-ours [--cache DIR]                # presses our own tools (our site only)
    python measure.py report                                   # verdict table from proof.json -> proof-table.md (cache dir)

Every parameter is defined in PARAMS below (group, id, direction, definition). The same definitions are printed in
proof.md. Manual adjudications (where a keyword hit was checked by eye or by a second look at the page) are in MANUAL,
each with its reason; proof.json keeps the automatic value next to the adjudicated one.
"""
import argparse
import datetime as dt
import html as htmlmod
import json
import os
import re
import sys
import time
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

import requests

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PROOF_JSON = os.path.join(HERE, "proof.json")
DEFAULT_CACHE = os.path.join(os.environ.get("TEMP", "/tmp"), "mortgage-proof-cache")
TODAY = dt.date(2026, 11, 5)
UA_MOBILE = ("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/156.0.0.0 Mobile Safari/537.36")
UA_PLAIN = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/156.0.0.0 Safari/537.36")
VIEWPORT = {"width": 390, "height": 844}

# --------------------------------------------------------------------------------------------------------------------
# Pages. IL = the top 10 for "מחשבון משכנתא" on desktop AND on mobile (DataForSEO, Google IL, Hebrew, 5.11.2026
# 19:47 UTC, serp-2026-11-05.json); that union already contains Mashcantaman, Hapoalim, Mizrahi-Tefahot and Leumi.
# WORLD = the world.md section 1 pages that are mortgage calculators (home pages and hubs without a calculator left out).
# --------------------------------------------------------------------------------------------------------------------
PAGES = [
    ("ours", "OURS", "nad-lan (ours)", "https://nad-lan.co.il/mortgage-calculator/"),
    # Israel, desktop top 10
    ("hapoalim", "IL", "Bank Hapoalim", "https://www.bankhapoalim.co.il/mortgage/mortgage-calculator"),
    ("mashcantaman", "IL", "Mashcantaman", "https://mashcantaman.co.il/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90/"),
    ("mizrahi", "IL", "Mizrahi-Tefahot", "https://www.mizrahi-tefahot.co.il/mortgages/calculator/"),
    ("leumi_calc", "IL", "Leumi calculator app", "https://ufapi.bankleumi.co.il/mortgageCalculator/Calc"),
    ("discount_m", "IL", "Discount mortgages", "https://mortgage.discountbank.co.il/calculator"),
    ("clalbit", "IL", "Clal Insurance", "https://www.clalbit.co.il/calculatormashcanta/"),
    ("leumi_m", "IL", "Leumi Mortgages", "https://mortgage.leumi.co.il/all-about-mortgage/category/calculator/mortgage-calculator"),
    ("supermarker", "IL", "Supermarker", "https://www.supermarker.themarker.com/Calculators/Mortgage/MartgageCalculator.aspx"),
    ("taxo_change", "IL", "Taxo (rate change)", "https://www.taxo.co.il/biz/C_ChangeIntLoan_Taxo.asp"),
    ("fibi", "IL", "FIBI (Bainleumi)", "https://www.fibi.co.il/private/loansandmortgages/mortgages/calculators/"),
    # Israel, mobile top 10
    ("heshevavoda", "IL", "Heshev Avoda", "https://www.heshevavoda.co.il/cal/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%94%D7%9C%D7%95%D7%95%D7%90%D7%94/"),
    ("taxo_mix", "IL", "Taxo (mix)", "https://www.taxo.co.il/biz/C_mixLoan_Taxo.asp"),
    ("harel_cav", "IL", "Harel servicebank", "https://servicebank.cav.co.il/mortgageCalculator/f653648e-ef5c-4f3d-953c-d33527be12d9"),
    ("mydira", "IL", "Mydira", "https://www.mydira.co.il/mortgage_calc.htm"),
    ("familyecon", "IL", "Family-economy", "https://www.family-economy.co.il/mashkanta_cal.asp"),
    ("mercantile", "IL", "Mercantile", "https://www.mercantile.co.il/private/loans/calculator/"),
    ("gemel", "IL", "Gemel.net", "https://www.gemel.net/%D7%9B%D7%9C%D7%99%D7%9D-%D7%95%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%A0%D7%99%D7%9D/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90"),
    ("sbc", "IL", "SBC", "https://sbc-il.co.il/calculators/mortgage-payment/"),
    ("discount_l", "IL", "Discount loans", "https://www.discountbank.co.il/private/loans/loans-calculator/"),
    ("goola", "IL", "Goola group", "https://goola-group.com/branches/concept/calculators/mortgage/"),
    # World
    ("nerdwallet", "WORLD", "NerdWallet (US)", "https://www.nerdwallet.com/mortgages/calculators/mortgage-calculator"),
    ("bankrate", "WORLD", "Bankrate (US)", "https://www.bankrate.com/mortgages/mortgage-calculator/"),
    ("zillow", "WORLD", "Zillow (US)", "https://www.zillow.com/mortgage-calculator/"),
    ("redfin", "WORLD", "Redfin (US)", "https://www.redfin.com/mortgage-calculator"),
    ("rocket", "WORLD", "Rocket Mortgage (US)", "https://www.rocketmortgage.com/calculators/mortgage-calculator"),
    ("calcnet", "WORLD", "Calculator.net (US)", "https://www.calculator.net/mortgage-calculator.html"),
    ("forbes", "WORLD", "Forbes Advisor (US)", "https://www.forbes.com/advisor/mortgages/mortgage-calculator/"),
    ("chase", "WORLD", "Chase (US)", "https://www.chase.com/personal/mortgage/calculators-resources/mortgage-calculator"),
    ("better", "WORLD", "Better (US)", "https://better.com/b/calculators/mortgage-calculator"),
    ("mcorg", "WORLD", "MortgageCalculator.org (US)", "https://www.mortgagecalculator.org/"),
    ("mse", "WORLD", "MoneySavingExpert (UK)", "https://www.moneysavingexpert.com/mortgages/mortgage-rate-calculator/"),
    ("which", "WORLD", "Which? (UK)", "https://www.which.co.uk/money/mortgages-and-property/mortgage-calculators/mortgage-repayment-calculator-aaq242x4qttl"),
    ("moneyfacts", "WORLD", "Moneyfacts (UK)", "https://moneyfactscompare.co.uk/mortgages/mortgage-repayment-calculator/"),
    ("mojo", "WORLD", "Mojo (UK)", "https://mojomortgages.com/mortgage-calculator"),
    ("nationwide", "WORLD", "Nationwide (UK)", "https://www.nationwide.co.uk/mortgages/mortgage-calculators"),
    ("ratehub", "WORLD", "Ratehub (CA)", "https://www.ratehub.ca/mortgage-payment-calculator"),
    ("wowa", "WORLD", "WOWA (CA)", "https://wowa.ca/calculators/mortgage-calculator"),
    ("nesto", "WORLD", "nesto (CA)", "https://www.nesto.ca/calculators/mortgage-payment/"),
    ("finder", "WORLD", "Finder (AU)", "https://www.finder.com.au/home-loans/home-loan-calculators/home-loan-repayment-calculator"),
    ("rea", "WORLD", "realestate.com.au (AU)", "https://www.realestate.com.au/home-loans/mortgage-calculator/"),
    ("interhyp", "WORLD", "Interhyp (DE)", "https://www.interhyp.de/baufinanzierungsrechner/"),
    ("drklein", "WORLD", "Dr. Klein (DE)", "https://www.drklein.de/baufinanzierungsrechner.html"),
    ("hypofriend", "WORLD", "Hypofriend (DE)", "https://hypofriend.de/en/german-mortgage-calculator"),
    ("meilleurtaux", "WORLD", "Meilleurtaux (FR)", "https://www.meilleurtaux.com/credit-immobilier/simulation-de-pret-immobilier/calcul-des-mensualites.html"),
    ("pretto", "WORLD", "Pretto (FR)", "https://www.pretto.fr/calculette-pret-immobilier/"),
    ("hypotheker", "WORLD", "De Hypotheker (NL)", "https://www.hypotheker.nl/zelf-berekenen/wat-worden-mijn-maandlasten/"),
]

# --------------------------------------------------------------------------------------------------------------------
# Regular expressions shared by the counts
# --------------------------------------------------------------------------------------------------------------------
MONEY_OR_PCT = re.compile(
    r"(?:[₪$€£]\s?\d[\d,.  ]*\d?"
    r"|\d[\d,.  ]*\s?(?:%|₪|€|£|ש\"ח|ש״ח|שקלים|שקל|EUR\b|USD\b|CAD\b|AUD\b|GBP\b))")
MONEY = re.compile(
    r"(?:[₪$€£]\s?\d[\d,.  ]*"
    r"|\d[\d,.  ]*\s?(?:₪|€|£|ש\"ח|ש״ח|שקלים|שקל|EUR\b|USD\b|CAD\b|AUD\b|GBP\b))")
PCT = re.compile(r"\d[\d,.]*\s?%")
TERM = re.compile(r"(\d+\s?(?:שנה|שנים|years?|yrs?|Jahre[n]?|ans?|jaar)\b|\b(?:שנה|שנים)\b)", re.I)
WORD = re.compile(r"\w", re.U)

OFFICIAL_SUFFIX = (".gov", ".gov.il", ".gov.uk", ".gc.ca", ".gouv.fr", ".europa.eu", ".bund.de", ".gov.au",
                   ".govt.nz", ".admin.ch")
OFFICIAL_HOSTS = {
    "boi.org.il", "cbs.gov.il", "gov.il", "freddiemac.com", "fanniemae.com", "bankofcanada.ca", "bankofengland.co.uk",
    "fca.org.uk", "bundesbank.de", "bafin.de", "destatis.de", "banque-france.fr", "insee.fr", "dnb.nl", "cbs.nl",
    "afm.nl", "nhg.nl", "rba.gov.au", "abs.gov.au", "apra.gov.au", "moneyhelper.org.uk", "ecb.europa.eu",
    "cmhc-schl.gc.ca", "osfi-bsif.gc.ca", "statcan.gc.ca", "federalreserve.gov", "consumerfinance.gov",
    "nibud.nl", "economie.gouv.fr", "service-public.fr", "legifrance.gouv.fr", "nevo.co.il", "knesset.gov.il",
    "taxes.gov.il", "data.gov.il", "kolzchut.org.il",
}
SOURCE_WORDS = re.compile(
    r"(בנק ישראל|הלמ\"ס|הלמ״ס|למ\"ס|למ״ס|הלשכה המרכזית לסטטיסטיקה|רשות המסים|המפקח על הבנקים|"
    r"Bank of Israel|Freddie Mac|Fannie Mae|Federal Reserve|\bFed\b|Bank of Canada|\bCMHC\b|Bank of England|"
    r"\bBoE\b|\bECB\b|\bEZB\b|Bundesbank|Banque de France|\bINSEE\b|\bDNB\b|Nibud|\bONS\b|Curinos|"
    r"Statistics Canada|Statistisches Bundesamt|Destatis|Moneyfacts|Bank of America|Bankrate|Zillow|"
    r"Mortgage Research Center|Quadrant|\bMBA\b|\bOSFI\b|\bHCSF\b|Banque centrale)", re.I)

HE_MONTHS = {"ינואר": 1, "פברואר": 2, "מרץ": 3, "מרס": 3, "אפריל": 4, "מאי": 5, "יוני": 6, "יולי": 7, "אוגוסט": 8,
             "ספטמבר": 9, "אוקטובר": 10, "נובמבר": 11, "דצמבר": 12}
EN_MONTHS = {m: i + 1 for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                              "september", "october", "november", "december"])}
EN_MONTHS.update({m[:3]: i for m, i in list(EN_MONTHS.items())})
EN_MONTHS["sept"] = 9
DE_MONTHS = {"januar": 1, "februar": 2, "märz": 3, "april": 4, "mai": 5, "juni": 6, "juli": 7, "august": 8,
             "september": 9, "oktober": 10, "november": 11, "dezember": 12}
FR_MONTHS = {"janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7, "août": 8,
             "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12}
NL_MONTHS = {"januari": 1, "februari": 2, "maart": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7, "augustus": 8,
             "september": 9, "oktober": 10, "november": 11, "december": 12}
ALL_MONTHS = {}
for d_ in (HE_MONTHS, EN_MONTHS, DE_MONTHS, FR_MONTHS, NL_MONTHS):
    ALL_MONTHS.update(d_)
MONTH_ALT = "|".join(sorted((re.escape(k) for k in ALL_MONTHS), key=len, reverse=True))
DATE_PATTERNS = [
    ("dmy", re.compile(r"\b(\d{1,2})[./](\d{1,2})[./](20\d{2})\b")),
    ("ymd", re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")),
    ("mdy_name", re.compile(r"\b(" + MONTH_ALT + r")\.?\s+(\d{1,2}),?\s+(20\d{2})\b", re.I)),
    ("dmy_name", re.compile(r"\b(\d{1,2})\.?\s+(?:ב)?(" + MONTH_ALT + r")\s+(20\d{2})\b", re.I)),
    ("my_name", re.compile(r"(?:\b|ב)(" + MONTH_ALT + r")\s+(20\d{2})\b", re.I)),
]


def extract_dates(text):
    """All calendar dates in a text (day precision; month-only dates count as day 1). Future dates are dropped."""
    found = []
    for kind, rx in DATE_PATTERNS:
        for m in rx.finditer(text):
            try:
                if kind == "dmy":
                    d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
                    if mo > 12 and d <= 12:  # US order
                        d, mo = mo, d
                    found.append(dt.date(y, mo, d))
                elif kind == "ymd":
                    found.append(dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
                elif kind == "mdy_name":
                    found.append(dt.date(int(m.group(3)), ALL_MONTHS[m.group(1).lower()], int(m.group(2))))
                elif kind == "dmy_name":
                    found.append(dt.date(int(m.group(3)), ALL_MONTHS[m.group(2).lower()], int(m.group(1))))
                elif kind == "my_name":
                    found.append(dt.date(int(m.group(2)), ALL_MONTHS[m.group(1).lower()], 1))
            except (ValueError, KeyError):
                pass
    return [d for d in found if dt.date(2015, 1, 1) <= d <= TODAY]


# --------------------------------------------------------------------------------------------------------------------
# Raw HTML (as served, no JavaScript): a small stdlib parser
# --------------------------------------------------------------------------------------------------------------------
BLOCK_TAGS = {"p", "div", "li", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "br", "section", "article",
              "header", "footer", "nav", "ul", "ol", "table", "dd", "dt", "details", "summary", "figcaption",
              "blockquote", "main", "aside", "form", "label", "option", "caption"}
SKIP_TAGS = {"script", "style", "noscript", "svg", "template", "head", "title", "iframe", "object"}


class RawParser(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.skip = 0
        self.parts = []
        self.counts = {"table": 0, "td": 0, "th": 0, "img": 0, "h": 0, "details": 0}
        self.headings = []
        self.cur_heading = None
        self.links = []
        self.jsonld = []
        self.in_jsonld = False
        self.jsonld_buf = []
        self.meta = {}
        self.lang = ""
        self.canonical = ""
        self.itemtypes = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "") or ""
        if tag == "script" and (a.get("type") or "").lower().strip() == "application/ld+json":
            self.in_jsonld = True
            self.jsonld_buf = []
        if tag in SKIP_TAGS:
            self.skip += 1
            return
        if tag == "meta":
            k = (a.get("property") or a.get("name") or a.get("itemprop") or "").lower()
            if k:
                self.meta[k] = a.get("content", "") or ""
        if tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href", "") or ""
        if a.get("itemtype"):
            for t in re.findall(r"schema\.org/(\w+)", a.get("itemtype")):
                self.itemtypes.add(t)
        if self.skip:
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")
        if tag in self.counts:
            self.counts[tag] += 1
        if re.fullmatch(r"h[1-6]", tag):
            self.counts["h"] += 1
            self.cur_heading = []
        if tag == "a" and a.get("href"):
            self.links.append(urljoin(self.base, a.get("href")))

    def handle_endtag(self, tag):
        if tag == "script" and self.in_jsonld:
            self.in_jsonld = False
            self.jsonld.append("".join(self.jsonld_buf))
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if re.fullmatch(r"h[1-6]", tag) and self.cur_heading is not None:
            self.headings.append(re.sub(r"\s+", " ", "".join(self.cur_heading)).strip())
            self.cur_heading = None
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld_buf.append(data)
            return
        if self.skip:
            return
        self.parts.append(data)
        if self.cur_heading is not None:
            self.cur_heading.append(data)

    def text(self):
        t = "".join(self.parts)
        t = re.sub(r"[ \t\r\f\v ]+", " ", t)
        t = re.sub(r"\n\s*\n+", "\n", t)
        return t.strip()


def walk_ld(node, types, faq_q, dates, persons, depth=0):
    if depth > 40:
        return
    if isinstance(node, list):
        for x in node:
            walk_ld(x, types, faq_q, dates, persons, depth + 1)
        return
    if not isinstance(node, dict):
        return
    t = node.get("@type")
    tl = t if isinstance(t, list) else ([t] if t else [])
    for x in tl:
        if isinstance(x, str):
            types.add(x)
    if "FAQPage" in tl:
        me = node.get("mainEntity")
        me = me if isinstance(me, list) else ([me] if me else [])
        faq_q.append(sum(1 for q in me if isinstance(q, dict)))
    for k in ("dateModified", "datePublished"):
        v = node.get(k)
        if isinstance(v, str) and k == "dateModified":
            dates.append(v)
    for k in ("author", "reviewedBy", "editor"):
        v = node.get(k)
        vv = v if isinstance(v, list) else ([v] if v else [])
        for p in vv:
            if isinstance(p, dict) and (p.get("name") or p.get("@id")):
                persons.append({"role": k, "type": p.get("@type"), "name": p.get("name") or p.get("@id")})
            elif isinstance(p, str):
                persons.append({"role": k, "type": None, "name": p})
    for v in node.values():
        if isinstance(v, (dict, list)):
            walk_ld(v, types, faq_q, dates, persons, depth + 1)


def parse_date_any(s):
    m = re.match(r"(20\d{2})-(\d{2})-(\d{2})", s or "")
    if m:
        try:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None


def host_of(u):
    h = (urlparse(u).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def is_official(h):
    if not h:
        return False
    if h in OFFICIAL_HOSTS or any(h.endswith("." + x) for x in OFFICIAL_HOSTS):
        return True
    return h.endswith(OFFICIAL_SUFFIX) or h in {s.lstrip(".") for s in OFFICIAL_SUFFIX}


def sentences(text):
    out = []
    for line in text.split("\n"):
        for s in re.split(r"(?<=[.!?:;])\s+(?=\S)", line):
            s = s.strip()
            if len(s) > 8:
                out.append(s)
    return out


def analyse_raw(html, url):
    p = RawParser(url)
    try:
        p.feed(html)
        p.close()
    except Exception as e:  # malformed pages
        pass
    text = p.text()
    words = sum(1 for tok in text.split() if WORD.search(tok))
    figures = len(MONEY_OR_PCT.findall(text))
    types, faq_q, dates, persons = set(), [], [], []
    bad_ld = 0
    for raw in p.jsonld:
        s = raw.strip()
        s = re.sub(r"^\s*<!\[CDATA\[|\]\]>\s*$", "", s)
        try:
            obj = json.loads(s)
        except Exception:
            try:
                obj = json.loads(re.sub(r",\s*([}\]])", r"\1", s))
            except Exception:
                bad_ld += 1
                continue
        walk_ld(obj, types, faq_q, dates, persons)
    types_all = set(types) | set(p.itemtypes)
    own = host_of(url)
    off = sorted({host_of(l) for l in p.links if is_official(host_of(l)) and host_of(l) != own})
    sents = sentences(text)
    worked = [s for s in sents if len(MONEY.findall(s)) >= 2 and (PCT.search(s) or TERM.search(s))]
    dated_src = [s for s in sents if MONEY_OR_PCT.search(s) and SOURCE_WORDS.search(s) and extract_dates(s)]
    qheads = [h for h in p.headings if h.strip().endswith("?") or h.strip().startswith(("מה ", "איך ", "כמה ", "האם ", "למה ", "מתי ", "how ", "what ", "why ", "can ", "should ", "is ", "do ", "does "))]
    dm = [parse_date_any(x) for x in dates]
    for k in ("article:modified_time", "og:updated_time", "last-modified", "dc.date.modified", "datemodified"):
        if p.meta.get(k):
            dm.append(parse_date_any(p.meta.get(k)))
    dm = [d for d in dm if d and d <= TODAY + dt.timedelta(days=1)]
    return {
        "html_lang": p.lang,
        "canonical": p.canonical,
        "words_raw": words,
        "figures_raw": figures,
        "tables_raw": p.counts["table"],
        "cells_raw": p.counts["td"] + p.counts["th"],
        "headings_raw": p.counts["h"],
        "headings_sample": p.headings[:80],
        "question_headings": len(qheads),
        "img_raw": p.counts["img"],
        "jsonld_blocks": len(p.jsonld),
        "jsonld_unparsed": bad_ld,
        "jsonld_types": sorted(types_all),
        "faq_schema_q": max(faq_q) if faq_q else 0,
        "date_modified": max(dm).isoformat() if dm else None,
        "persons": persons[:10],
        "official_sources": off,
        "worked_examples": len(worked),
        "worked_examples_sample": worked[:6],
        "dated_sourced": len(set(dated_src)),
        "dated_sourced_sample": list(dict.fromkeys(dated_src))[:8],
        "raw_text_len": len(text),
        "meta_author": p.meta.get("author", ""),
    }


# --------------------------------------------------------------------------------------------------------------------
# robots.txt (longest-match, as Google and the AI crawlers document it) and llms.txt
# --------------------------------------------------------------------------------------------------------------------
AI_BOTS = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]


def robots_verdict(robots_txt, token, path):
    groups, cur, last_was_ua = [], None, False
    for line in robots_txt.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if not last_was_ua or cur is None:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(v.lower())
            last_was_ua = True
        elif k in ("allow", "disallow") and cur is not None:
            cur["rules"].append((k, v))
            last_was_ua = False
        else:
            last_was_ua = False
    tok = token.lower()
    specific = [g for g in groups if any(a != "*" and a in tok for a in g["agents"])]
    use = specific or [g for g in groups if "*" in g["agents"]]
    rules = [r for g in use for r in g["rules"]]
    best, best_len = ("allow", ""), -1
    for k, v in rules:
        if k == "disallow" and v == "":
            continue
        rx = "^" + re.escape(v).replace(r"\*", ".*")
        if rx.endswith(r"\$"):
            rx = rx[:-2] + "$"
        if re.match(rx, path):
            if len(v) > best_len or (len(v) == best_len and k == "allow"):
                best, best_len = (k, v), len(v)
    return {"verdict": best[0], "rule": best[1], "named": bool(specific)}


def fetch_domain_files(url, cache):
    pr = urlparse(url)
    root = f"{pr.scheme}://{pr.netloc}"
    out = {"root": root}
    s = requests.Session()
    s.headers["User-Agent"] = UA_PLAIN
    try:
        r = s.get(root + "/robots.txt", timeout=20, allow_redirects=True)
        txt = r.text if (r.status_code == 200 and "<html" not in r.text[:500].lower()) else ""
        out["robots_status"] = r.status_code
        out["robots"] = {b: robots_verdict(txt, b, pr.path or "/") for b in AI_BOTS}
        out["robots_named"] = [b for b in AI_BOTS if out["robots"][b]["named"]]
    except Exception as e:
        out["robots_status"] = f"error {type(e).__name__}"
        out["robots"] = {}
    try:
        r = s.get(root + "/llms.txt", timeout=20, allow_redirects=True)
        ct = r.headers.get("content-type", "")
        body = r.text or ""
        ok = r.status_code == 200 and "html" not in ct.lower() and not body.lstrip().startswith("<") and len(body) > 50
        out["llms_status"] = r.status_code
        out["llms_txt"] = bool(ok)
        out["llms_chars"] = len(body) if ok else 0
    except Exception as e:
        out["llms_status"] = f"error {type(e).__name__}"
        out["llms_txt"] = False
    return out


# --------------------------------------------------------------------------------------------------------------------
# In-browser extraction (JavaScript)
# --------------------------------------------------------------------------------------------------------------------
INIT_JS = r"""
window.__lcp = null; window.__cls = 0;
try { new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.startTime; })
      .observe({type:'largest-contentful-paint', buffered:true}); } catch(e) {}
try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; })
      .observe({type:'layout-shift', buffered:true}); } catch(e) {}
"""

COMMON_JS = r"""
const T = s => (s||'').replace(/\s+/g,' ').trim();
const EXC = 'header, nav, footer, [role=search], [role=banner], [role=navigation], [role=contentinfo], [id*=cookie i], [class*=cookie i], [id*=consent i], [class*=consent i], [id*=onetrust i], [class*=onetrust i], [id*=didomi i], [class*=didomi i], [id*=usercentrics i], [class*=gdpr i], [id*=CybotCookiebot]';
const LEAD = /(phone|טלפון|נייד|שם מלא|^\s*שם|e-?mail|מייל|דוא"ל|\bname\b|\bnom\b|vorname|nachname|naam|telefoon|search|חיפוש|suche|recherche|zoeken)/i;
const looseVis = el => { if (!el || !el.getBoundingClientRect) return false; const r = el.getBoundingClientRect();
  if (r.width < 1 || r.height < 1) return false; const cs = getComputedStyle(el);
  return cs.visibility !== 'hidden' && cs.display !== 'none'; };
const isVis = el => looseVis(el) && parseFloat(getComputedStyle(el).opacity || '1') > 0.02;
const labelOf = el => {
  let t = '';
  try { if (el.id) document.querySelectorAll('label[for="'+CSS.escape(el.id)+'"]').forEach(l => t += ' ' + l.textContent); } catch(e) {}
  const wl = el.closest('label'); if (wl) t += ' ' + wl.textContent;
  t += ' ' + (el.getAttribute('aria-label')||'') + ' ' + (el.getAttribute('title')||'');
  const lb = el.getAttribute('aria-labelledby'); if (lb) lb.split(/\s+/).forEach(id => { const e = document.getElementById(id); if (e) t += ' ' + e.textContent; });
  return T(t);
};
const hasLabel = el => {
  if (el.getAttribute('aria-label') && T(el.getAttribute('aria-label'))) return true;
  if (el.getAttribute('aria-labelledby')) return true;
  if (el.getAttribute('title') && T(el.getAttribute('title'))) return true;
  if (el.closest('label') && T(el.closest('label').textContent)) return true;
  try { if (el.id && document.querySelector('label[for="'+CSS.escape(el.id)+'"]')) return true; } catch(e) {}
  return false;
};
const ctxOf = el => { let p = el.parentElement, t = '';
  for (let i = 0; i < 4 && p; i++, p = p.parentElement) { t = T(p.innerText || p.textContent); if (t.length > 3) break; }
  return t.slice(0, 160); };
const docY = el => el.getBoundingClientRect().top + window.scrollY;
"""

FRAME_JS = "() => {" + COMMON_JS + r"""
  const out = {inputs: [], buttons: [], options: [], tabs: [], summaries: [], legends: [], links: [], headings: [],
               tables: [], url: location.href};
  for (const el of document.querySelectorAll('input, select, textarea, [role=slider], [role=spinbutton], [role=combobox]')) {
    const type = (el.tagName === 'INPUT' ? (el.getAttribute('type') || 'text') : (el.getAttribute('role') || el.tagName)).toLowerCase();
    if (['hidden','submit','button','image','reset','file'].includes(type)) continue;
    const lab = labelOf(el) + ' ' + (el.getAttribute('placeholder') || '');
    out.inputs.push({type, label: T(lab).slice(0, 160), ctx: ctxOf(el), name: T((el.name || '') + ' ' + (el.id || '')).slice(0, 80),
                     vis: looseVis(el), labelled: hasLabel(el), exc: !!el.closest(EXC)});
    if (el.tagName === 'SELECT') for (const o of el.options) out.options.push(T(o.textContent).slice(0, 80));
  }
  for (const el of document.querySelectorAll('button, [role=button], input[type=submit], input[type=button]')) {
    const t = T(el.innerText || el.textContent || el.value || '') || T(el.getAttribute('aria-label') || el.getAttribute('title') || '');
    if (t) out.buttons.push(t.slice(0, 120));
  }
  for (const el of document.querySelectorAll('[role=tab], [role=radio], [role=switch], [role=option], [role=menuitemradio], [role=checkbox]')) {
    const t = T(el.innerText || el.textContent || el.getAttribute('aria-label') || ''); if (t) out.tabs.push(t.slice(0, 120));
  }
  for (const el of document.querySelectorAll('input[type=radio], input[type=checkbox]')) {
    const t = labelOf(el) || ctxOf(el); if (t) out.tabs.push(t.slice(0, 120));
  }
  for (const el of document.querySelectorAll('summary')) out.summaries.push(T(el.innerText || el.textContent).slice(0, 160));
  for (const el of document.querySelectorAll('legend, fieldset > label, [class*=tab i] > *')) {
    const t = T(el.innerText || el.textContent); if (t && t.length < 120) out.legends.push(t);
  }
  const seen = new Set();
  for (const a of document.querySelectorAll('a[href]')) {
    const t = T(a.innerText || a.textContent || a.getAttribute('aria-label') || ''); const k = t + '|' + a.getAttribute('href');
    if (t && !seen.has(k) && out.links.length < 2500) { seen.add(k); out.links.push({t: t.slice(0, 140), h: (a.href || '').slice(0, 200)}); }
  }
  for (const h of document.querySelectorAll('h1,h2,h3,h4,h5,h6')) out.headings.push({l: h.tagName, t: T(h.innerText || h.textContent).slice(0, 200), vis: looseVis(h)});
  for (const tb of document.querySelectorAll('table')) {
    const rows = tb.querySelectorAll('tr').length; const head = T(Array.from(tb.querySelectorAll('th')).map(x => x.textContent).join(' | ')).slice(0, 400);
    out.tables.push({rows, cells: tb.querySelectorAll('td,th').length, head, text: T(tb.textContent).slice(0, 3000), vis: looseVis(tb)});
  }
  // visible text and all text (text nodes, scripts and styles excluded)
  out.visible_text = document.body ? (document.body.innerText || '') : '';
  let all = []; if (document.body) { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {acceptNode: n => {
      const p = n.parentElement; if (!p) return NodeFilter.FILTER_REJECT;
      if (p.closest('script,style,noscript,template')) return NodeFilter.FILTER_REJECT; return NodeFilter.FILTER_ACCEPT; }});
    let n, c = 0; while ((n = w.nextNode()) && c < 200000) { const v = n.nodeValue; if (v && v.trim()) { all.push(v.trim()); c++; } } }
  out.all_text = all.join(' \n');
  return out;
}"""

FIRST_JS = "() => {" + COMMON_JS + r"""
  // value-entry fields only (selects and comboboxes are left out: on several pages they are "on this page" menus or
  // rate-table filters, not the calculator); off-screen and negative positions are ignored
  const okTypes = ['text','number','tel','range','slider','spinbutton','decimal',''];
  let fi = null; const all = [];
  for (const el of document.querySelectorAll('input, [role=slider], [role=spinbutton]')) {
    const type = (el.tagName === 'INPUT' ? (el.getAttribute('type') || 'text') : (el.getAttribute('role') || '')).toLowerCase();
    if (!okTypes.includes(type)) continue;
    let tgt = el; if (!looseVis(el)) continue;
    if (el.closest(EXC)) continue;
    const rr = el.getBoundingClientRect(); if (rr.right <= 0 || rr.left >= window.innerWidth) continue;
    const lab = labelOf(el) + ' ' + (el.getAttribute('placeholder') || '') + ' ' + (el.name || '') + ' ' + (el.id || '');
    if (LEAD.test(lab)) continue;
    const y = docY(tgt); if (y < 0) continue;
    all.push({y: Math.round(y), label: T(lab).slice(0, 60), type});
    if (fi === null || y < fi.y) fi = {y: Math.round(y), label: T(lab).slice(0, 80), type};
  }
  all.sort((a, b) => a.y - b.y);
  const MONEY = /(?:[₪$€£]\s?\d)|(?:\d[\d.,   ]*\s?(?:₪|€|£|ש"ח|ש״ח|שקל))/;
  let fm = null;
  if (document.body) {
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {acceptNode: n => {
      const p = n.parentElement; if (!p || p.closest('script,style,noscript,template')) return NodeFilter.FILTER_REJECT;
      return MONEY.test(n.nodeValue || '') ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP; }});
    let n, c = 0;
    while ((n = w.nextNode()) && c < 5000) { c++;
      const p = n.parentElement; if (!isVis(p) || p.closest(EXC)) continue;
      const m = (n.nodeValue || '').match(MONEY); if (!m) continue;
      const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, Math.min(n.nodeValue.length, m.index + m[0].length));
      const rc = r.getBoundingClientRect(); if (rc.width < 1 || rc.height < 1) continue;
      const y = rc.top + window.scrollY;
      if (fm === null || y < fm.y) fm = {y: Math.round(y), text: T(n.nodeValue).slice(0, 80)};
    }
  }
  return {first_input: fi, first_money: fm, inputs_top: all.slice(0, 8)};
}"""

PHONE_JS = "() => {" + COMMON_JS + r"""
  const vw = window.innerWidth, vh = window.innerHeight, de = document.documentElement, b = document.body || de;
  let h = Math.max(de.scrollHeight, b.scrollHeight), scroller = null;
  for (const el of document.querySelectorAll('div, main, section')) {
    if (el.clientHeight < vh * 0.5) continue; const cs = getComputedStyle(el);
    if (!/(auto|scroll)/.test(cs.overflowY)) continue; if (el.scrollHeight > h) { h = el.scrollHeight; scroller = el.tagName + '.' + (el.className || '').toString().slice(0, 40); }
  }
  const overflow = Math.max(de.scrollWidth, b.scrollWidth) > vw + 1;
  // tap targets
  const cand = new Set();
  document.querySelectorAll('button, select, textarea, summary, [role=button], [role=tab], [role=switch], [role=radio], [role=checkbox], [role=link], input:not([type=hidden])').forEach(e => cand.add(e));
  document.querySelectorAll('a[href]').forEach(a => { const d = getComputedStyle(a).display; if (d !== 'inline') cand.add(a); });
  let n = 0, n44 = 0, n24 = 0;
  for (let el of cand) {
    if (el.tagName === 'INPUT' && /^(checkbox|radio)$/i.test(el.type) && el.closest('label')) el = el.closest('label');
    if (!isVis(el)) continue; const r = el.getBoundingClientRect(); n++;
    if (r.height >= 44) n44++; if (r.height >= 24 && r.width >= 24) n24++;
  }
  // overlays on load: sample 6 x 12 tap points over the first screen; a point is covered when the element a tap would
  // hit sits inside a position:fixed layer or a dialog (a top bar shorter than 25% of the screen is the page header and
  // is ignored). A layer covering >= 20% of the points is an interruption. Invisible or click-through layers are not hit.
  const fixedAnc = el => { let e = el; while (e && e !== document.body && e !== document.documentElement) {
      const cs = getComputedStyle(e); if (cs.position === 'fixed' || e.getAttribute('aria-modal') === 'true' || e.getAttribute('role') === 'dialog' || e.tagName === 'DIALOG') return e;
      e = e.parentElement; } return null; };
  const agg = new Map(); let covered = 0, total = 0;
  for (let i = 0; i < 6; i++) for (let j = 0; j < 12; j++) {
    total++; const el = document.elementFromPoint((i + 0.5) * vw / 6, (j + 0.5) * vh / 12); if (!el) continue;
    const a = fixedAnc(el); if (!a) continue; const r = a.getBoundingClientRect();
    const dialog = a.getAttribute('role') === 'dialog' || a.getAttribute('aria-modal') === 'true' || a.tagName === 'DIALOG';
    if (!dialog && r.top <= 2 && r.height < vh * 0.25) continue;
    covered++; agg.set(a, (agg.get(a) || 0) + 1);
  }
  const ov = [];
  for (const [a, n] of agg) {
    const t = T(a.innerText || a.textContent || '').slice(0, 300); const sig = t + ' ' + (a.id || '') + ' ' + (a.className || '').toString() + ' ' + (a.src || '');
    let kind = 'other';
    if (/cookie|consent|privacy|עוגיות|cookies|datenschutz|confidentialit|toestemming|we value your privacy|gdpr|onetrust/i.test(sig)) kind = 'cookie';
    else if (/captcha|px-captcha|challenge/i.test(sig)) kind = 'bot-check';
    else if (/\bapp\b|אפליקציה|download our|open in app|continue in/i.test(t)) kind = 'app';
    ov.push({kind, cover: Math.round(n / total * 100) / 100, tag: a.tagName, id: (a.id || '').slice(0, 40), cls: (a.className || '').toString().slice(0, 60), text: t.slice(0, 120)});
  }
  ov.sort((x, y) => y.cover - x.cover);
  // accessibility basics
  const imgs = Array.from(document.images); const imgAlt = imgs.filter(i => i.hasAttribute('alt')).length;
  const ctrls = Array.from(document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]):not([type=image]):not([type=reset]), select, textarea')).filter(looseVis);
  const ctrlLab = ctrls.filter(hasLabel).length;
  // visuals and charts (rendered >= 100 x 100, outside icons)
  let visuals = 0, charts = 0;
  for (const el of document.querySelectorAll('img, video, canvas, svg, iframe')) {
    if (el.tagName === 'svg' && el.parentElement && el.parentElement.closest('svg')) continue;
    if (!isVis(el)) continue; const r = el.getBoundingClientRect();
    if (el.tagName === 'IFRAME' && !/youtube|vimeo|player/i.test(el.src || '')) continue;
    if (r.width >= 100 && r.height >= 100) visuals++;
    if ((el.tagName === 'CANVAS' || el.tagName === 'svg') && r.width >= 150 && r.height >= 100 && !el.closest('a,button')) {
      if (el.tagName === 'CANVAS' || el.querySelectorAll('path,rect,circle,line,polyline').length >= 6) charts++;
    }
  }
  return {page_height: Math.round(h), scroller, h_overflow: overflow, scroll_width: Math.max(de.scrollWidth, b.scrollWidth),
          tap_n: n, tap_44: n44, tap_24: n24, overlays: ov, overlay_cover_total: Math.round(covered / total * 100) / 100,
          img_n: imgs.length, img_alt: imgAlt, ctrl_n: ctrls.length, ctrl_labelled: ctrlLab, html_lang: de.lang || '',
          visuals, charts, title: document.title};
}"""

PERF_JS = r"""() => {
  const n = performance.getEntriesByType('navigation')[0] || {};
  return {ttfb: n.responseStart || null, dcl: n.domContentLoadedEventEnd || null, load: n.loadEventEnd || null,
          lcp: window.__lcp, cls: Math.round((window.__cls || 0) * 1000) / 1000,
          nav_transfer: n.transferSize || null, nav_decoded: n.decodedBodySize || null};
}"""

BLOCK_RX = re.compile(r"(captcha|are you a human|confirm you are human|verify you are human|access denied|just a moment|"
                      r"attention required|pardon our interruption|request unsuccessful|incapsula|px-captcha|"
                      r"checking your browser|bot detection|unusual traffic|radware)", re.I)


def measure_page(pw_browser, pid, region, name, url, cache):
    rec = {"id": pid, "region": region, "name": name, "url": url, "measured_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"}
    ctx = pw_browser.new_context(viewport=VIEWPORT, device_scale_factor=3, is_mobile=True, has_touch=True,
                                 user_agent=UA_MOBILE, locale="he-IL" if region != "WORLD" else "en-US",
                                 timezone_id="Asia/Jerusalem")
    ctx.add_init_script(INIT_JS)
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    net = {"req": set(), "bytes": 0, "fail": 0}
    cdp.send("Network.enable")
    cdp.on("Network.requestWillBeSent", lambda e: net["req"].add(e["requestId"]))
    cdp.on("Network.loadingFinished", lambda e: net.__setitem__("bytes", net["bytes"] + (e.get("encodedDataLength") or 0)))
    cdp.on("Network.loadingFailed", lambda e: net.__setitem__("fail", net["fail"] + 1))
    t0 = time.time()
    resp, err = None, None
    try:
        resp = page.goto(url, wait_until="load", timeout=60000)
    except Exception as e:
        err = f"{type(e).__name__}: {str(e)[:160]}"
    rec["goto_error"] = err
    page.wait_for_timeout(3000)
    rec["final_url"] = page.url
    rec["status"] = resp.status if resp else None
    raw = ""
    if resp:
        try:
            raw = resp.text()
        except Exception as e:
            raw = ""
            rec["raw_error"] = str(e)[:120]
    rec["html_bytes"] = len(raw.encode("utf-8"))
    perf = {}
    try:
        perf = page.evaluate(PERF_JS)
    except Exception as e:
        rec["perf_error"] = str(e)[:120]
    rec["speed"] = {"ttfb_ms": perf.get("ttfb"), "dcl_ms": perf.get("dcl"), "load_ms": perf.get("load"),
                    "lcp_ms": perf.get("lcp"), "cls": perf.get("cls"), "transfer_bytes": net["bytes"],
                    "requests": len(net["req"]), "failed_requests": net["fail"],
                    "html_transfer_bytes": perf.get("nav_transfer"), "wall_s": round(time.time() - t0, 1)}
    # first screen: overlays + first input / money (scrollY = 0)
    try:
        page.screenshot(path=os.path.join(cache, f"{pid}-first.jpg"), type="jpeg", quality=45)
    except Exception:
        pass
    try:
        phone0 = page.evaluate(PHONE_JS)
    except Exception as e:
        phone0 = {"error": str(e)[:160]}
    first = {"first_input": None, "first_money": None}
    try:
        first = page.evaluate(FIRST_JS)
    except Exception as e:
        rec["first_error"] = str(e)[:160]
    # look inside child frames (calculators embedded in an iframe)
    sy = 0
    for fr in page.frames[1:12]:
        try:
            fe = fr.frame_element()
            bb = fe.bounding_box()
            if not bb or bb["width"] < 200 or bb["height"] < 150:
                continue
            f1 = fr.evaluate(FIRST_JS)
            for k in ("first_input", "first_money"):
                if f1.get(k):
                    y = round(bb["y"] + f1[k]["y"])
                    if first.get(k) is None or y < first[k]["y"]:
                        first[k] = dict(f1[k], y=y, frame=fr.url[:120])
        except Exception:
            continue
    rec["first_screen"] = first
    blocked_txt = ""
    try:
        blocked_txt = page.evaluate("() => (document.title + ' ' + (document.body ? document.body.innerText.slice(0, 1500) : ''))")
    except Exception:
        pass
    rec["blocked"] = bool((rec["status"] and rec["status"] >= 400) or (BLOCK_RX.search(blocked_txt) and len(blocked_txt) < 1600))
    # scroll through once (lazy blocks), back to the top
    try:
        page.evaluate("""async () => { const vh = innerHeight; let y = 0; for (let i = 0; i < 140; i++) {
            y += vh; window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120));
            if (y > document.documentElement.scrollHeight) break; } window.scrollTo(0, 0); }""")
        page.wait_for_timeout(1200)
    except Exception:
        pass
    try:
        phone1 = page.evaluate(PHONE_JS)
    except Exception as e:
        phone1 = {"error": str(e)[:160]}
    rec["phone"] = {
        "first_input_y": (first.get("first_input") or {}).get("y"),
        "first_input_label": (first.get("first_input") or {}).get("label"),
        "first_money_y": (first.get("first_money") or {}).get("y"),
        "first_money_text": (first.get("first_money") or {}).get("text"),
        "page_height_initial": phone0.get("page_height"),
        "page_height": max(phone0.get("page_height") or 0, phone1.get("page_height") or 0) or None,
        "h_overflow": phone1.get("h_overflow"), "scroll_width": phone1.get("scroll_width"),
        "tap_n": phone1.get("tap_n"), "tap_44": phone1.get("tap_44"), "tap_24": phone1.get("tap_24"),
        "overlays_on_load": phone0.get("overlays"), "overlay_cover_total": phone0.get("overlay_cover_total"),
        "inputs_top": first.get("inputs_top"), "scroller": phone1.get("scroller"),
    }
    rec["a11y"] = {"img_n": phone1.get("img_n"), "img_alt": phone1.get("img_alt"), "ctrl_n": phone1.get("ctrl_n"),
                   "ctrl_labelled": phone1.get("ctrl_labelled"), "html_lang": phone1.get("html_lang")}
    rec["visuals_rendered"] = phone1.get("visuals")
    rec["charts_rendered"] = phone1.get("charts")
    rec["title"] = phone1.get("title")
    # controls and text, main frame + calculator frames
    frames_out = []
    for i, fr in enumerate(page.frames[:12]):
        try:
            if i > 0:
                bb = fr.frame_element().bounding_box()
                if not bb or bb["width"] < 200 or bb["height"] < 150:
                    continue
            frames_out.append(fr.evaluate(FRAME_JS))
        except Exception:
            continue
    merged = {k: [] for k in ("inputs", "buttons", "options", "tabs", "summaries", "legends", "links", "headings", "tables")}
    vt, at = [], []
    for fo in frames_out:
        for k in merged:
            merged[k].extend(fo.get(k, []))
        vt.append(fo.get("visible_text", ""))
        at.append(fo.get("all_text", ""))
    merged["frames"] = [fo.get("url") for fo in frames_out]
    visible_text = "\n".join(vt)
    all_text = "\n".join(at)
    rec["rendered"] = {"words": sum(1 for t in visible_text.split() if WORD.search(t)),
                       "figures": len(MONEY_OR_PCT.findall(visible_text)),
                       "tables": len(merged["tables"]), "cells": sum(t["cells"] for t in merged["tables"]),
                       "inputs": len([x for x in merged["inputs"] if x["vis"] and not x["exc"]]),
                       "frames": merged["frames"]}
    with open(os.path.join(cache, f"{pid}-raw.html"), "w", encoding="utf-8") as f:
        f.write(raw)
    with open(os.path.join(cache, f"{pid}-visible.txt"), "w", encoding="utf-8") as f:
        f.write(visible_text)
    with open(os.path.join(cache, f"{pid}-all.txt"), "w", encoding="utf-8") as f:
        f.write(all_text)
    with open(os.path.join(cache, f"{pid}-controls.json"), "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=0)
    rec["raw"] = analyse_raw(raw, page.url) if raw else None
    ctx.close()
    return rec


# --------------------------------------------------------------------------------------------------------------------
# Feature detection (keywords in he / en / de / fr / nl). Scopes: ctrl = input labels, buttons, tabs, options,
# summaries, legends; link = link texts; head = headings; vis = visible text. "Y" needs a ctrl-level hit
# (or the scope named in the spec); a hit only in prose is reported as "text" and does not count as a tool.
# --------------------------------------------------------------------------------------------------------------------
IL_BANKS = ["הפועלים", "לאומי", "דיסקונט", "מזרחי", "הבינלאומי", "ירושלים", "מרכנתיל", "יהב", "One Zero", "וואן זירו"]
WORLD_LENDERS = ["Chase", "Wells Fargo", "Bank of America", "Rocket", "U.S. Bank", "Citi", "RBC", "TD", "Scotiabank", "BMO",
                 "CIBC", "National Bank", "Barclays", "HSBC", "Nationwide", "Santander", "Lloyds", "NatWest", "Halifax",
                 "Deutsche Bank", "Commerzbank", "Sparkasse", "ING", "ABN AMRO", "Rabobank", "BNP", "Société Générale",
                 "Crédit Agricole", "LCL", "Commonwealth Bank", "Westpac", "ANZ", "NAB", "DKB", "Postbank", "Allianz"]
CITIES = ["תל אביב", "ירושלים", "חיפה", "ראשון לציון", "פתח תקווה", "אשדוד", "נתניה", "באר שבע", "חולון", "בני ברק",
          "רמת גן", "רחובות", "אשקלון", "בת ים", "הרצליה", "כפר סבא", "חדרה", "מודיעין", "רעננה", "לוד", "רמלה",
          "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "London", "Manchester", "Birmingham",
          "Berlin", "München", "Hamburg", "Frankfurt", "Köln", "Paris", "Lyon", "Marseille", "Amsterdam", "Rotterdam",
          "Utrecht", "Sydney", "Melbourne", "Brisbane", "Perth", "California", "Texas", "Florida", "New York",
          "Ontario", "Quebec", "British Columbia", "Alberta", "Los Angeles", "Chicago", "Houston"]

R = lambda s: re.compile(s, re.I)
FEATURES = [
    # id, label, spec
    ("payment_from_loan", "Solves the monthly payment from a loan amount or price",
     {"lab_all": [R(r"(loan amount|mortgage amount|amount|home price|purchase price|price|value|סכום|מחיר|שווי|montant|prix|darlehen|kredit|kaufpreis|hypotheek|koopsom|bedrag|lening)"),
                  R(r"(rate|ריבית|taux|zins|rente|interest)")]}),
    ("loan_from_payment", "Solves the loan or price from a monthly payment",
     {"lab": R(r"(monthly payment|desired payment|payment you can afford|monthly budget|החזר (חודשי )?(רצוי|מבוקש|מקסימלי|מתוכנן)|יכולת החזר|ההחזר החודשי (שתוכלו לשלם|שמתאים לכם)|mensualit|monatliche rate|monatsrate|wunschrate|maandlast|max(imum)? (monthly )?payment)"),
      "ctrl": R(r"(by (monthly )?payment|לפי החזר|לפי יכולת החזר|from (a |the )?payment|calculate (loan|mortgage) amount|capacité d.emprunt|combien (puis-je|pouvez-vous|je peux) emprunter)")}),
    ("price_plus_equity", "Starts from price and down payment (equity)",
     {"lab_all": [R(r"(home price|purchase price|house price|property (price|value)|home value|מחיר|שווי (ה)?(דירה|נכס)|prix|kaufpreis|immobilienpreis|koopsom|woningwaarde|aankoopprijs|price|value)"),
                  R(r"(down ?payment|deposit|equity|הון עצמי|apport|eigenkapital|eigen (geld|middelen|inbreng)|downpayment)")]}),
    ("affordability_income", "Affordability from income (and debts)",
     {"lab": R(r"(income|salary|earnings|הכנסה|הכנסות|משכורת|\bשכר\b|revenus?|salaire|einkommen|gehalt|inkomen)")}),
    ("multi_track", "Several loan tracks or parts in one calculation",
     {"ctrl_all": [R(r"(קל\"צ|קל״צ|קבועה לא צמודה|לא צמודה)"), R(r"פריים")],
      "ctrl": R(r"(loan parts|leningdelen|hypotheekdelen|darlehensteile|split (loan|mortgage)|add (a )?(loan )?part|prêts? multiples)")}),
    ("compare_scenarios", "Compares two or more mixes or scenarios side by side",
     {"ctrl": R(r"(compare (two|2|scenarios|mortgages)|השוואת (תמהילים|מסלולים|תרחישים)|השוו|תמהיל (1|2|3|4|א|ב)|scenario [0-9a-d]|vergleich|comparer|vergelijk)")}),
    ("schedule", "Amortization or repayment schedule",
     {"ctrl": R(r"(amorti[sz]ation|לוח סילוקין|לוח (ה)?תשלומים|לוח שפיצר|repayment schedule|payment schedule|tableau d.amortissement|tilgungsplan|aflossingsschema|aflosschema|schedule|restschuld)"),
      "table_head": R(r"(balance|יתרה|יתרת|restschuld|solde|restschuld|capital restant|remaining)")}),
    ("stress_test", "Rate change, payment shock or stress test",
     {"ctrl": R(r"(stress|shock|rate (rise|increase|change)|if rates (rise|go up)|עליית (ה)?ריבית|אם הריבית|תרחיש|רגישות|מבחן העמידות|לחץ \(פריים|משבר \(פריים|שינוי ריבית|zinsänderung|zinsanstieg|zinserhöhung|hausse des taux|renteschok|rentestijging|what if)")}),
    ("historical_stress", "Replays a historical rate path (e.g. 2022)",
     {"ctrl": R(r"(אם 2022|2022 חוזרת|if 2022|historical (rates|scenario|stress|path)|replay|תרחיש היסטורי|historische[sn]? (szenario|scenario|stresstest))")}),
    ("forecast_scenario", "Uses a published central-bank or market forecast path",
     {"ctrl": R(r"(תחזית|forecast|prognose|prévision|outlook)")}),
    ("prepayment_fee", "Early-repayment (exit) fee calculation",
     {"ctrl": R(r"(עמלת פירעון|עמלת היוון|עמלת יציאה|הערכת העמלה|כמה תעלה היציאה|עלות היציאה|exit cost|early repayment charge|\bERCs?\b|prepayment (penalty|fee|charge)|exit fee|indemnit[ée]s? de remboursement|vorfälligkeitsentschädigung|boeterente)")}),
    ("extra_payments", "Extra payment or overpayment simulation",
     {"ctrl": R(r"(extra (monthly |yearly |annual |one-time )?payments?|overpay|additional payment|lump sum|פירעון מוקדם|פירעון חלקי|סילוק חלקי|סכום לסילוק|sondertilgung|remboursement anticip|extra aflossen|accelerated)")}),
    ("refinance", "Refinance, renewal or switch tool (link = link to a sibling page only)",
     {"ctrl": R(r"(מחזור|refinanc|renewal|remortgage|anschlussfinanzierung|umschuldung|forward-?darlehen|renégoci|rachat de cr[ée]dit|oversluiten|ditch your fix|switch(ing)? (mortgage|lender|deal))"),
      "link_partial": R(r"(מחזור משכנתא|refinanc|renewal|remortgage|anschlussfinanzierung|renégoci|oversluiten)")}),
    ("afford_to_homes", "From the result to real homes for sale",
     {"ctrl": R(r"(homes for sale|houses for sale|see (matching )?homes|browse homes|דירות (למכירה|שמתאימות|בתקציב)|נכסים (שמתאימים|בתקציב)|פרויקטים בתקציב|properties (for sale|in your budget)|biens? à vendre|immobilien (suchen|finden)|huizen te koop|woningaanbod)"),
      "link_partial": R(r"(homes for sale|houses for sale|explore houses|דירות למכירה|properties for sale)")}),
    ("offer_comparison", "Enters several bank offers and compares them",
     {"ctrl": R(r"(השוואת הצעות|שלוש הצעות|הצעה (1|2|3|ראשונה|שנייה|שלישית)|הצעת (ה)?בנק|compare (offers|quotes|lenders)|offer (1|2|a|b)|angebote vergleichen|comparer (les )?offres|offertes vergelijken)")}),
    ("per_bank_benchmark", "Your rate vs a named bank's own published average",
     {"bank_select": 3,
      "ctrl": R(r"(ממוצע (של )?(ה)?בנק|bank.s own average|vs\.? (the )?(bank|lender).{0,20}average)")}),
    ("offer_vs_market_money", "Your offered rate vs the market average, gap in money",
     {"lab": R(r"(הריבית (שהבנק הציע|בהצעה)|rate you (were|have been) offered|offered rate|your (offer|quote)d? rate|taux (proposé|de votre offre)|angebotener zins|aangeboden rente)")}),
    ("readiness_docs", "Approval-in-principle readiness or a document checklist",
     {"ctrl": R(r"(רשימת מסמכים|מסמכים (נדרשים|לאישור|שצריך)|מוכנים לאישור|מוכנות|readiness|what documents|document(s)? (checklist|list)|checklist|unterlagen|pièces justificatives|benodigde documenten)")}),
    ("rate_decision_impact", "Central-bank rate decision turned into your payment",
     {"ctrl": R(r"(החלטת (ה)?ריבית|ריבית בנק ישראל|rate decision|view impact|leitzins|taux directeur|(bank of canada|bank of england|ecb|ezb|bce|fed).{0,30}(decision|rate))")}),
    ("regulatory_checks", "Checks against lending rules (LTV, PTI or DTI, term, variable share)",
     {"ctrl": R(r"(הוראה 329|מגבל|שיעור (ה)?מימון|\bLTV\b|יחס (ה)?החזר|חלק מההכנסה להחזר|\bPTI\b|debt.to.income|\bDTI\b|taux d.endettement|\bHCSF\b|loan.to.value|beleihung|tragbarkeit|toetsinkomen|\bNHG\b)"),
      "vis": R(r"(חורג מ|עומד בכלל|עומד בכללי|exceeds the (limit|maximum)|within the limit|above the limit|dépasse le|überschreitet)")}),
    ("total_cost", "Total interest or total repayment shown",
     {"vis": R(r"(total interest|total (of )?payments|total cost|סה\"כ (ריבית|החזר|תשלומים|תשלום)|סה״כ (ריבית|החזר|תשלומים|תשלום)|סך (ה)?(ריבית|תשלומים|החזר)|coût total|total des intérêts|gesamtkosten|zinskosten|gesamtbetrag|totale (rente|kosten)|total paid|total repaid|interest paid)")}),
    ("costs_in_payment", "Taxes, insurance or HOA inside the monthly figure",
     {"lab": R(r"(property tax|homeowner.?s insurance|insurance|\bHOA\b|\bPMI\b|ביטוח|ארנונה|ועד בית|assurance|versicherung|verzekering|condo fee|strata|taxes)")}),
    ("local_defaults", "Local defaults by ZIP, province or city",
     {"lab": R(r"(\bzip\b|postal|postcode|province|\bstate\b|location|\bcity\b|county|עיר|יישוב|département|bundesland|\bort\b|plaats|gemeente|where are you buying)")}),
    ("charts", "Chart drawn on the page (canvas or SVG >= 150 x 100 with >= 6 shapes)", {"charts": 1}),
    ("share_link", "Share or copy-link of the result",
     {"btn": R(r"(^share|share (this|your|the) |שתף|שתפו|שיתוף|קישור (שפותח|למקרה|לתוצאה|לחישוב)|copy (this )?(link|url|estimate)|העתק(ת|ו)? (את )?(ה)?קישור|teilen|partager|^delen|link kopieren|copy link|get link)")}),
    ("print_export", "Print, PDF, Excel or CSV of the result",
     {"btn": R(r"(print|הדפס|הדפסה|\bPDF\b|excel|\bCSV\b|הורד|הורדה|drucken|imprimer|afdrukken|t[ée]l[ée]charger|herunterladen|export|ייצוא)")}),
    ("tool_switcher", "Several calculators behind one switcher on the page (>= 3 entries)",
     {"switch": R(r"(calculator|מחשבון|rechner|calculette|simulat|berekenen|כמה |בדיקת|תקציב|הצעות|budget|offers?|overpay|ditch|borrow)")}),
    ("payment_frequency", "Payment frequency options (weekly, bi-weekly)",
     {"ctrl": R(r"(bi-?weekly|\bweekly\b|fortnightly|accelerated|semi-?monthly|payment frequency|fréquence|zahlungsrhythmus|דו.?שבועי)")}),
    ("cpi_indexation", "CPI-linked (indexed) loan handling",
     {"ctrl": R(r"(מדד|צמוד|\bCPI\b|inflation|index-linked|indexed|indexierung|index[ée])")}),
    ("rent_vs_buy", "Rent vs buy on the page (link = link only)",
     {"ctrl": R(r"(rent (vs\.?|or) buy|buy (vs\.?|or) rent|לקנות או לשכור|לשכור או לקנות|שכירות מול|mieten (oder|vs\.?) kaufen|kaufen (oder|vs\.?) mieten|louer ou acheter|acheter ou louer|huren of kopen|kopen of huren)"),
      "link_partial": R(r"(rent (vs\.?|or) buy|buy (vs\.?|or) rent|לקנות או לשכור|שכירות|mieten oder kaufen|kauf-?miet|louer ou acheter|huren of kopen|reverse rent)")}),
    ("lead_cta", "Pre-approval, advisor or broker call to action",
     {"ctrl_or_link": R(r"(pre-?approv|pre-?qualif|get (my|a|your) rate|get a quote|apply now|talk to|speak (with|to)|advis|broker|ייעוץ|יועץ|וואטסאפ|whatsapp|צרו קשר|צור קשר|לתיאום|beratung|berater|angebot anfordern|conseiller|courtier|adviseur|afspraak|request offer|decision in principle|אישור עקרוני|financing certificate|attestation)")}),
    # data group
    ("market_rate_near_input", "Market or average rate shown with the rate input",
     {"ctrl": R(r"(ממוצע|average|national avg|market rate|taux march|marktzins|today.s (best )?rate|current rate|ריבית (ממוצעת|עדכנית)|בנק ישראל|bank of israel)")}),
    ("by_bank_rates", "Rates by named bank or lender (>= 3 lenders with a rate)", {"lenders_table": 3}),
    ("borrower_distribution", "Distribution of new loans by LTV or PTI band",
     {"vis_all": [R(r"(שיעור (ה)?מימון|\bLTV\b|loan.to.value|יחס (ה)?החזר|\bPTI\b|\bDTI\b)"), R(r"(התפלגות|distribution|מתוך ההלוואות|of new (loans|mortgages)|מההלוואות החדשות|מהמשכנתאות החדשות|מהכסף ניתן|share of (new )?(loans|mortgages))")]}),
    ("city_payments", "Payments or prices by city or region (>= 5 places in one table)", {"cities_table": 5}),
]


def _ctrl_text(c):
    parts = []
    for x in c.get("inputs", []):
        parts.append(x.get("label", ""))
        parts.append(x.get("ctx", ""))
    parts += c.get("buttons", []) + c.get("options", []) + c.get("tabs", []) + c.get("summaries", []) + c.get("legends", [])
    return " | ".join(p for p in parts if p)


def _snip(rx, text, w=50):
    m = rx.search(text)
    if not m:
        return None
    a, b = max(0, m.start() - w), min(len(text), m.end() + w)
    return re.sub(r"\s+", " ", text[a:b])


def detect_features(c, visible, rec):
    ctrl = _ctrl_text(c)
    labs = " | ".join((x.get("label", "") + " " + x.get("ctx", "") + " " + x.get("name", "")) for x in c.get("inputs", [])
                      if not x.get("exc"))
    btns = " | ".join(c.get("buttons", []) + c.get("tabs", []))
    links = " | ".join(l["t"] for l in c.get("links", []))
    heads = " | ".join(h["t"] for h in c.get("headings", []))
    tables = c.get("tables", [])
    out = {}
    for fid, flabel, spec in FEATURES:
        val, ev = "-", None
        if "lab_all" in spec:
            if all(rx.search(labs) for rx in spec["lab_all"]):
                val, ev = "Y", " / ".join(_snip(rx, labs, 25) or "" for rx in spec["lab_all"])
        if "lab" in spec and val != "Y":
            s = _snip(spec["lab"], labs)
            if s:
                val, ev = "Y", s
        if "ctrl_all" in spec and val != "Y":
            if all(rx.search(ctrl) for rx in spec["ctrl_all"]):
                val, ev = "Y", " / ".join(_snip(rx, ctrl, 25) or "" for rx in spec["ctrl_all"])
        if "ctrl" in spec and val != "Y":
            s = _snip(spec["ctrl"], ctrl)
            if s:
                val, ev = "Y", s
        if "btn" in spec and val != "Y":
            s = _snip(spec["btn"], btns)
            if s:
                val, ev = "Y", s
        if "ctrl_or_link" in spec and val != "Y":
            s = _snip(spec["ctrl_or_link"], ctrl + " | " + links)
            if s:
                val, ev = "Y", s
        if "table_head" in spec and val != "Y":
            for t in tables:
                if t["rows"] >= 6 and spec["table_head"].search(t["head"] or t["text"][:300]):
                    val, ev = "Y", "table: " + (t["head"] or t["text"][:120])[:160]
                    break
        if "vis" in spec and val != "Y":
            s = _snip(spec["vis"], visible)
            if s:
                val, ev = ("Y" if fid in ("total_cost", "regulatory_checks") else "text"), s
        if "vis_all" in spec and val != "Y":
            if all(rx.search(visible) for rx in spec["vis_all"]):
                val, ev = "Y", " / ".join(_snip(rx, visible, 25) or "" for rx in spec["vis_all"])
        if "link_partial" in spec and val != "Y":
            s = _snip(spec["link_partial"], links)
            if s:
                val, ev = "link", s
        if "charts" in spec:
            n = rec.get("charts_rendered") or 0
            val, ev = ("Y", f"{n} chart-like canvas/svg") if n else ("-", None)
        if "bank_select" in spec and val != "Y":
            opts = " | ".join(c.get("options", []) + c.get("tabs", []) + c.get("buttons", []))
            n_il = sum(1 for b in IL_BANKS if b in opts)
            n_w = sum(1 for b in WORLD_LENDERS if re.search(r"\b" + re.escape(b) + r"\b", opts))
            if max(n_il, n_w) >= spec["bank_select"]:
                val, ev = "Y", f"lender options in controls: IL {n_il}, world {n_w}"
        if "lenders_table" in spec:
            best = 0
            for t in tables:
                if "%" not in t["text"]:
                    continue
                n = sum(1 for b in IL_BANKS if b in t["text"]) + sum(1 for b in WORLD_LENDERS if re.search(r"\b" + re.escape(b) + r"\b", t["text"]))
                best = max(best, n)
            val, ev = ("Y", f"{best} lenders in one rate table") if best >= spec["lenders_table"] else ("-", f"max {best}")
        if "cities_table" in spec:
            best = 0
            for t in tables:
                n = sum(1 for cty in CITIES if cty in t["text"])
                best = max(best, n)
            val, ev = ("Y", f"{best} places in one table") if best >= spec["cities_table"] else ("-", f"max {best}")
        if "switch" in spec:
            entries = [x for x in (c.get("tabs", []) + c.get("options", []) + c.get("buttons", [])) if spec["switch"].search(x) and len(x) < 60
                       and not x.strip().endswith("?") and not re.match(r"(?i)(how|what|why|does|is|can|calculators?$|show (more|previous))", x.strip())]
            entries = list(dict.fromkeys(entries))
            val, ev = ("Y", " | ".join(entries[:8])) if len(entries) >= 3 else ("-", " | ".join(entries[:8]) or None)
        if val == "-" and fid not in ("charts", "by_bank_rates", "city_payments", "tool_switcher"):
            # prose-only evidence, reported but never counted as a tool
            for rxname in ("ctrl", "lab"):
                rx = spec.get(rxname)
                if rx is not None:
                    s = _snip(rx, heads + " | " + visible)
                    if s:
                        val, ev = "text", s
                        break
        out[fid] = {"auto": val, "evidence": ev}
    return out


def methodology(heads_text):
    rx = R(r"(method|methodolog|how we calculate|how (is|are|do|does|to).{0,30}calculat|formula|נוסח|איך מחשבים|כיצד מחשבים|"
           r"איך (ה)?מחשבון (עובד|מחשב)|מתודולוגיה|מקורות|sources|quellen|so berechne|berechnung|comment (est )?calcul|méthod|"
           r"berekening|hoe bereken|about the data|על הנתונים|how this calculator works)")
    return _snip(rx, heads_text, 30)


BYLINE = R(r"(written by|reviewed by|edited by|fact[- ]checked|audited|nachgeprüft|geprüft von|relu par|rédigé par|écrit par|"
           r"geschreven door|auteur ?:|autor ?:|נכתב (על ידי|ע\"י)|נבדק (על ידי|ע\"י)|עריכה ?:|כתיבה ?:)")


# --------------------------------------------------------------------------------------------------------------------
# Parameters: group, id, label, direction, definition. direction: bool (Y > link > text/-), hi (more is better),
# lo (less is better). tol = (absolute, relative) tolerance for a TIE.
# --------------------------------------------------------------------------------------------------------------------
PARAMS = []
DATA_FEATURES = {"market_rate_near_input", "by_bank_rates", "borrower_distribution", "city_payments"}
for fid, flabel, _ in [f for f in FEATURES if f[0] not in DATA_FEATURES]:
    PARAMS.append(("1 Tool", fid, flabel, "bool", (0, 0), "keyword hit in the tool's own controls (labels, buttons, tabs, options) after one phone load, adjudicated where noted"))
PARAMS += [
    ("2 Data", "market_rate_near_input", "Market or average rate shown with the rate input", "bool", (0, 0), "control-level hit, adjudicated"),
    ("2 Data", "by_bank_rates", "Rates by named bank (>= 3 lenders with rates)", "bool", (0, 0), "a rendered table with >= 3 named lenders and a % sign"),
    ("2 Data", "borrower_distribution", "Distribution of new loans by LTV or PTI band", "bool", (0, 0), "visible text names LTV and a distribution; adjudicated"),
    ("2 Data", "city_payments", "Payments or prices by city or region", "bool", (0, 0), "a rendered table naming >= 5 places"),
    ("2 Data", "dated_sourced", "Dated, sourced figure statements (proxy for official dated series)", "hi", (0, 0), "raw-HTML sentences with a figure + a named official source + a date"),
    ("2 Data", "update_recency_days", "Days since the newest date shown on the page", "lo", (1, 0), "newest calendar date (<= today) in the visible text"),
    ("2 Data", "market_data_age_days", "Age of the newest market rate figure (days, manual)", "lo", (2, 0), "read on the page: the as-of date of the newest rate figure"),
    ("3 Content", "words_raw", "Visible words in raw HTML", "hi", (0, 0.02), "body text without script/style/svg/noscript, tokens with a letter or digit"),
    ("3 Content", "words_rendered", "Visible words after JavaScript", "hi", (0, 0.02), "document.body.innerText, all frames"),
    ("3 Content", "figures_raw", "Money and % figures in raw HTML", "hi", (0, 0.02), "numbers next to ₪ $ € £ ש\"ח or %"),
    ("3 Content", "tables_raw", "Tables in raw HTML", "hi", (0, 0), "<table> count"),
    ("3 Content", "cells_raw", "Table cells in raw HTML", "hi", (0, 0.02), "<td> + <th>"),
    ("3 Content", "faq_schema_q", "FAQ questions in FAQPage schema", "hi", (0, 0), "Question items in the largest FAQPage"),
    ("3 Content", "question_headings", "Question headings in raw HTML", "hi", (0, 0), "h1-h6 ending with ? or starting with a question word"),
    ("3 Content", "headings_raw", "Headings in raw HTML", "hi", (0, 0), "h1-h6 count"),
    ("3 Content", "official_sources", "Official sources linked (distinct domains)", "hi", (0, 0), "links to government, central-bank or statistics domains"),
    ("3 Content", "worked_examples", "Worked examples in plain HTML", "hi", (0, 0), "sentences with >= 2 money figures and a % or a term"),
    ("3 Content", "visuals_rendered", "Images, video, charts rendered >= 100 x 100 px", "hi", (0, 0), "img/video/canvas/svg/player iframes at phone width"),
    ("4 AI and search", "jsonld_types", "Distinct schema.org types (JSON-LD + microdata)", "hi", (0, 0), "@type values"),
    ("4 AI and search", "breadcrumb", "BreadcrumbList schema", "bool", (0, 0), "type present"),
    ("4 AI and search", "dataset", "Dataset schema", "bool", (0, 0), "type present"),
    ("4 AI and search", "faqpage", "FAQPage schema", "bool", (0, 0), "type present"),
    ("4 AI and search", "webapp", "WebApplication or SoftwareApplication schema", "bool", (0, 0), "type present"),
    ("4 AI and search", "date_modified_days", "Days since schema/meta dateModified", "lo", (1, 0), "JSON-LD dateModified or article:modified_time"),
    ("4 AI and search", "author_reviewer", "Named author or reviewer", "bool", (0, 0), "Person in author/reviewedBy, or a visible byline"),
    ("4 AI and search", "methodology", "Method or sources section", "bool", (0, 0), "a heading about method, formula or sources"),
    ("4 AI and search", "llms_txt", "llms.txt at the domain", "bool", (0, 0), "200, not HTML, > 50 chars"),
    ("4 AI and search", "robots_ai_allowed", "AI crawlers allowed for the page (of 4)", "hi", (0, 0), "GPTBot, ClaudeBot, PerplexityBot, Google-Extended, longest-match rule"),
    ("4 AI and search", "raw_figure_share", "Share of the page's figures already in raw HTML", "hi", (0.02, 0), "raw figures / rendered figures, capped at 1"),
    ("5 Phone 390x844", "first_input_y", "First calculator input (y px)", "lo", (0, 0.05), "topmost visible number/text/select/range input outside header, nav, cookie and lead forms"),
    ("5 Phone 390x844", "first_money_y", "First money figure (y px)", "lo", (0, 0.05), "topmost visible text with a currency"),
    ("5 Phone 390x844", "page_height", "Page height (px)", "lo", (0, 0.05), "max scrollHeight after one scroll-through"),
    ("5 Phone 390x844", "h_overflow", "Horizontal overflow (0 = none)", "lo", (0, 0), "scrollWidth > 391"),
    ("5 Phone 390x844", "tap44_share", "Share of tappable controls >= 44 px tall", "hi", (0.02, 0), "buttons, inputs, selects, tabs, block links"),
    ("5 Phone 390x844", "interruptions", "Overlays on load covering >= 20% of the first screen", "lo", (0, 0), "fixed/sticky/dialog boxes, 3 s after load"),
    ("6 Speed (cold, one load)", "html_bytes", "HTML bytes (decoded document)", "lo", (0, 0.05), "document response body"),
    ("6 Speed (cold, one load)", "transfer_bytes", "Total transfer bytes to load + 3 s", "lo", (0, 0.05), "CDP encodedDataLength sum"),
    ("6 Speed (cold, one load)", "requests", "Requests to load + 3 s", "lo", (0, 0.05), "CDP requestWillBeSent"),
    ("6 Speed (cold, one load)", "ttfb_ms", "Time to first byte (ms)", "lo", (0, 0.10), "Navigation Timing responseStart"),
    ("6 Speed (cold, one load)", "dcl_ms", "DOMContentLoaded (ms)", "lo", (0, 0.10), "Navigation Timing"),
    ("6 Speed (cold, one load)", "load_ms", "Load event (ms)", "lo", (0, 0.10), "Navigation Timing"),
    ("6 Speed (cold, one load)", "lcp_ms", "Largest Contentful Paint (ms)", "lo", (0, 0.10), "PerformanceObserver, before any scroll"),
    ("6 Speed (cold, one load)", "cls", "Cumulative Layout Shift", "lo", (0.01, 0), "PerformanceObserver layout-shift"),
    ("7 Accessibility", "img_alt_share", "Images with an alt attribute", "hi", (0.01, 0), "share of <img> with alt"),
    ("7 Accessibility", "input_label_share", "Form controls with a label", "hi", (0.01, 0), "label[for], wrapping label, aria-label(ledby), title"),
    ("7 Accessibility", "html_lang", "html lang set", "bool", (0, 0), "<html lang>"),
]

# --------------------------------------------------------------------------------------------------------------------
# Manual adjudications: (page id, param id) -> (value, reason). Filled after reading the evidence snippets and, where
# needed, the page itself. See proof.md for the list.
# --------------------------------------------------------------------------------------------------------------------
MANUAL = {
    # ours
    # 5.11 (pass 1): ("-", "the keyword hit is the documents checklist item 'ביטוח חיים וביטוח מבנה'; no insurance, arnona or fees enter the monthly figure").
    # 6.11, after 1.72.592 (mquick v5): the auto hit is now the quick calculator's own fields, checked by pressing them live: 250 + 600 typed
    # give "העלות החודשית של הדירה" 6,278 = 5,428 + 250 + 600 (round-g/verify-live.json). Kept as an explicit ruling so the evidence is on record.
    ("ours", "costs_in_payment"): ("Y", "mquick v5 fields 'ביטוח חיים ומבנה' and 'ארנונה וועד בית' enter 'העלות החודשית של הדירה' (pressed live 6.11.2026: 5,428 + 250 + 600 = 6,278)"),
    ("ours", "afford_to_homes"): ("Y", "the automatic hit was the site menu; the real evidence is the budget tool 'כמה דירה זה קונה' with 'הראו לי את הדירות האלה' and rooms x cities buttons that link to listings (verify-ours)"),
    ("ours", "market_data_age_days"): (36, "default rates are the Bank of Israel averages for September 2026 (published 20.10.2026); age counted from 30.9.2026"),
    # Israel
    ("supermarker", "loan_from_payment"): ("Y", "quick mode input 'ההחזר החודשי שתוכלו לשלם' solves the loan"),
    ("supermarker", "stress_test"): ("Y", "'מבחן העמידות': ready scenarios 'לחץ (פריים +2, מדד 3.5%)', 'משבר (פריים +3, מדד 5%)' and a prime-change slider"),
    ("supermarker", "regulatory_checks"): ("Y", "the mix shows 'עומד בכלל' for one third fixed, two thirds variable and 30 years, and LTV from the optional price"),
    ("supermarker", "local_defaults"): ("-", "the town fields belong to the advisor lead form, not to the calculator"),
    ("supermarker", "market_data_age_days"): (36, "'הריביות הממוצעות של בנק ישראל, ספטמבר 2026'"),
    ("supermarker", "historical_stress"): ("-", "its 'משבר' scenario is a fixed shock (prime +3), not a replay of a historical path"),
    ("supermarker", "offer_comparison"): ("-", "one offer (rate per track) against the market average, not several offers side by side"),
    ("mashcantaman", "local_defaults"): ("-", "'בחירת יישוב' belongs to the advisor lead form"),
    ("mashcantaman", "extra_payments"): ("Y", "'סילוק חלקי/מלא', 'סכום לסילוק', 'מועד הסילוק' inside each track"),
    ("mashcantaman", "stress_test"): ("Y", "'שינוי ריבית: בשדה זה ניתן לדמות עליית ריבית עתידית במסלולים משתנים'"),
    ("clalbit", "costs_in_payment"): ("-", "the hits are the site search suggestions ('ביטוח רכב'), not calculator fields"),
    ("leumi_m", "refinance"): ("-", "the hit is a search suggestion ('מחזור משכנתא'), not a tool"),
    ("mydira", "loan_from_payment"): ("Y", "'גובה הלוואה לפי החזר חודשי' with input 'החזר חודשי מבוקש'"),
    # world
    ("hypotheker", "historical_stress"): ("-", "only a link 'Historische rentestanden' (a rates history page), no replay"),
    ("hypotheker", "regulatory_checks"): ("text", "'Is NHG mogelijk voor mij?' is a link to another calculator"),
    ("pretto", "regulatory_checks"): ("text", "the hit is an FAQ heading on the 35% debt ratio"),
    ("pretto", "prepayment_fee"): ("link", "'Calculez le coût d'un remboursement anticipé' links to a separate calculator"),
    ("ratehub", "regulatory_checks"): ("Y", "the page states the calculator shows 'the minimum down payment required based on Canadian mortgage rules' (world.md render saw the rule in the tool)"),
    ("redfin", "regulatory_checks"): ("text", "the hit is prose ('... when the mortgage exceeds the limit for Fannie Mae and Freddie Mac'), not a check of the user's numbers"),
    ("rocket", "tool_switcher"):("-", "hits are FAQ accordions and the 'Calculators' menu"),
    ("hypofriend", "tool_switcher"): ("-", "hits are FAQ accordions"),
    ("hypofriend", "forecast_scenario"): ("text", "'Expected interest rate' is their rate estimate for the profile, not a forecast path in the tool"),
    ("finder", "by_bank_rates"): ("Y", "the rate-rise result lists named lenders with rates (P&N Bank, BCU Bank, Greater Bank, Bendigo Bank, NRMA Home Loans)"),
    ("chase", "afford_to_homes"): ("link", "'Explore houses for sale' under the calculator, not tied to the result"),
    ("mse", "prepayment_fee"): ("link", "'Ditch your fix' (asks the early repayment charge) is one choice away in its calculator select, on a sibling URL"),
    ("nationwide", "prepayment_fee"): ("link", "'Calculate Early Repayment Charges (ERCs)' links to a separate calculator"),
    ("drklein", "prepayment_fee"): ("link", "'Vorfälligkeitsentschädigungsrechner' links to a separate calculator"),
    ("wowa", "first_input_y"): (930, "the two unlabeled inputs at y 121 are the filters of the 'Best 5-Year Fixed / Insured' rate widget (first-screen screenshot); the calculator's fields start at 930"),
    ("nerdwallet", "market_data_age_days"):(0, "'today's best rate on NerdWallet (6.67%) vs. the 7.01% national average'"),
    ("nesto", "market_data_age_days"): (0, "'Today's Best Mortgage Rates as of November 5, 2026'"),
    ("meilleurtaux", "market_data_age_days"): (0, "'taux moyens constatés le 05-11-2026'"),
}
# Pages whose single load returned an error or wall page (seen in the first-screen screenshot) although the status was 200.
MANUAL_BLOCKED = {
    "discount_m": "the load returned Discount's '404, page not found' screen with a reference number (a firewall page, status 200); "
                  "the calculator was never served to the script",
}


def flat_values(rec, dom):
    """All parameter values for one page record (automatic), as a dict param -> value."""
    v = {}
    raw = rec.get("raw") or {}
    feats = rec.get("features") or {}
    for fid, _, _ in FEATURES:
        v[fid] = (feats.get(fid) or {}).get("auto", "?")
    days = lambda d: (TODAY - dt.date.fromisoformat(d)).days if d else None
    vis_dates = extract_dates(rec.get("_visible_text", "") or "")
    v["dated_sourced"] = raw.get("dated_sourced")
    v["update_recency_days"] = (TODAY - max(vis_dates)).days if vis_dates else None
    v["market_data_age_days"] = None
    v["words_raw"] = raw.get("words_raw")
    v["words_rendered"] = (rec.get("rendered") or {}).get("words")
    v["figures_raw"] = raw.get("figures_raw")
    v["tables_raw"] = raw.get("tables_raw")
    v["cells_raw"] = raw.get("cells_raw")
    v["faq_schema_q"] = raw.get("faq_schema_q")
    v["question_headings"] = raw.get("question_headings")
    v["headings_raw"] = raw.get("headings_raw")
    v["official_sources"] = len(raw.get("official_sources") or []) if raw else None
    v["worked_examples"] = raw.get("worked_examples")
    v["visuals_rendered"] = rec.get("visuals_rendered")
    types = set(raw.get("jsonld_types") or [])
    v["jsonld_types"] = len(types) if raw else None
    v["breadcrumb"] = "Y" if "BreadcrumbList" in types else "-"
    v["dataset"] = "Y" if "Dataset" in types else "-"
    v["faqpage"] = "Y" if "FAQPage" in types else "-"
    v["webapp"] = "Y" if types & {"WebApplication", "SoftwareApplication", "FinancialCalculator"} else "-"
    v["date_modified_days"] = days(raw.get("date_modified"))
    def _is_person(p):
        t = p.get("type")
        return t == "Person" or (isinstance(t, list) and "Person" in t)
    plist = raw.get("persons") or []
    persons = [p for p in plist if _is_person(p) and p.get("name") and not str(p.get("name")).startswith("http")]
    if not persons and "Person" in types and any(p.get("role") in ("author", "reviewedBy") for p in plist):
        persons = [p for p in plist if p.get("role") in ("author", "reviewedBy")]
    byl = _snip(BYLINE, rec.get("_visible_text", "") or "", 30)
    v["author_reviewer"] = "Y" if (persons or byl) else "-"
    rec["_author_evidence"] = {"persons": persons[:4], "byline": byl}
    heads = " | ".join((raw.get("headings_sample") or [])) + " | " + " | ".join(h["t"] for h in (rec.get("_controls") or {}).get("headings", []))
    m = methodology(heads)
    v["methodology"] = "Y" if m else "-"
    rec["_method_evidence"] = m
    d = dom.get(urlparse(rec["url"]).netloc, {})
    v["llms_txt"] = "Y" if d.get("llms_txt") else "-"
    rb = d.get("robots") or {}
    v["robots_ai_allowed"] = sum(1 for b in AI_BOTS if (rb.get(b) or {}).get("verdict") == "allow") if rb else None
    rf = (rec.get("rendered") or {}).get("figures") or 0
    v["raw_figure_share"] = round(min(1.0, (raw.get("figures_raw") or 0) / rf), 2) if rf else (1.0 if raw.get("figures_raw") else 0.0)
    ph = rec.get("phone") or {}
    v["first_input_y"] = ph.get("first_input_y")
    v["first_money_y"] = ph.get("first_money_y")
    v["page_height"] = ph.get("page_height")
    # a page without a phone viewport lays out at ~980 px and is shrunk: that counts as overflow too
    v["h_overflow"] = (1 if (ph.get("h_overflow") or (ph.get("scroll_width") or 0) > VIEWPORT["width"] + 1) else 0) \
        if ph.get("scroll_width") is not None else None
    v["tap44_share"] = round(ph["tap_44"] / ph["tap_n"], 2) if ph.get("tap_n") else None
    v["interruptions"] = len([o for o in (ph.get("overlays_on_load") or []) if (o.get("cover") or 0) >= 0.2])
    sp = rec.get("speed") or {}
    v["html_bytes"] = rec.get("html_bytes") or None
    for k in ("transfer_bytes", "requests", "ttfb_ms", "dcl_ms", "load_ms", "lcp_ms", "cls"):
        val = sp.get(k)
        v[k] = round(val) if isinstance(val, float) and k != "cls" else val
    a = rec.get("a11y") or {}
    v["img_alt_share"] = round(a["img_alt"] / a["img_n"], 2) if a.get("img_n") else None
    v["input_label_share"] = round(a["ctrl_labelled"] / a["ctrl_n"], 2) if a.get("ctrl_n") else None
    v["html_lang"] = "Y" if (a.get("html_lang") or raw.get("html_lang")) else "-"
    return v


def cmd_measure(args):
    from playwright.sync_api import sync_playwright
    cache = args.cache
    os.makedirs(cache, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    existing = {}
    if os.path.exists(PROOF_JSON) and only:
        with open(PROOF_JSON, encoding="utf-8") as f:
            existing = {r["id"]: r for r in json.load(f).get("pages", [])}
    records = dict(existing)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        for pid, region, name, url in PAGES:
            if only and pid not in only:
                continue
            print(f"[{dt.datetime.utcnow():%H:%M:%S}] {pid} {url}", flush=True)
            try:
                rec = measure_page(browser, pid, region, name, url, cache)
            except Exception as e:
                rec = {"id": pid, "region": region, "name": name, "url": url, "error": f"{type(e).__name__}: {str(e)[:200]}"}
            records[pid] = rec
            print(f"    status={rec.get('status')} blocked={rec.get('blocked')} h={((rec.get('phone') or {}).get('page_height'))} "
                  f"req={((rec.get('speed') or {}).get('requests'))} err={rec.get('goto_error') or rec.get('error')}", flush=True)
        browser.close()
    # robots.txt / llms.txt once per domain
    domains = {}
    for pid, region, name, url in PAGES:
        net = urlparse(url).netloc
        if net in domains or (only and pid not in only and net not in {urlparse(r['url']).netloc for r in records.values()}):
            continue
        domains[net] = fetch_domain_files(url, cache)
    prev_dom = {}
    if os.path.exists(PROOF_JSON):
        with open(PROOF_JSON, encoding="utf-8") as f:
            prev_dom = json.load(f).get("domains", {})
    prev_dom.update(domains)
    finalize(records, prev_dom, cache)


def finalize(records, domains, cache):
    order = [p[0] for p in PAGES]
    pages = []
    for pid in order:
        rec = records.get(pid)
        if not rec:
            continue
        try:
            with open(os.path.join(cache, f"{pid}-controls.json"), encoding="utf-8") as f:
                ctrl = json.load(f)
            with open(os.path.join(cache, f"{pid}-visible.txt"), encoding="utf-8") as f:
                vis = f.read()
        except FileNotFoundError:
            ctrl, vis = {}, ""
        rec["_controls"], rec["_visible_text"] = ctrl, vis
        if pid in MANUAL_BLOCKED:
            rec["blocked"] = True
            rec["blocked_reason"] = MANUAL_BLOCKED[pid]
        botl = [o for o in ((rec.get("phone") or {}).get("overlays_on_load") or []) if o.get("kind") == "bot-check" and (o.get("cover") or 0) >= 0.5]
        if botl:
            rec["blocked"] = True
            rec["blocked_reason"] = "a bot-check layer (" + (botl[0].get("id") or botl[0].get("tag")) + ") covered the page on load; not attempted"
        if ctrl:
            rec["features"] = detect_features(ctrl, vis, rec)
        vals = flat_values(rec, domains)
        adj = {}
        for (mpid, mparam), (mval, why) in MANUAL.items():
            if mpid == pid:
                adj[mparam] = {"value": mval, "auto": vals.get(mparam), "reason": why}
                vals[mparam] = mval
        rec["values"] = vals
        rec["adjudicated"] = adj
        # proof.json lives in a public repo: keep only short evidence samples of other sites' text
        if pid != "ours" and rec.get("raw"):
            rw = rec["raw"]
            rw["headings_sample"] = [h[:80] for h in (rw.get("headings_sample") or [])[:12]]
            for k in ("worked_examples_sample", "dated_sourced_sample"):
                rw[k] = [s[:160] for s in (rw.get(k) or [])[:2]]
        rec.pop("_controls", None)
        rec.pop("_visible_text", None)
        pages.append(rec)
    out = {"about": "Counted benchmark for https://nad-lan.co.il/mortgage-calculator/ (HAD-675). One cold phone load "
                    "(390x844, is_mobile, has_touch, Chrome 156 headless, no throttling, from Israel) per page; raw HTML "
                    "= the document response of that load. Definitions: proof.md / measure.py PARAMS.",
           "generated_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
           "params": [{"group": g, "id": i, "label": l, "direction": d, "tolerance": t, "definition": df} for g, i, l, d, t, df in PARAMS],
           "domains": domains, "pages": pages}
    with open(PROOF_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print("wrote", PROOF_JSON)


def cmd_refeature(args):
    """Re-run detection and adjudication on the cached loads (no network)."""
    with open(PROOF_JSON, encoding="utf-8") as f:
        data = json.load(f)
    records = {r["id"]: r for r in data["pages"]}
    if args.pass1:  # keep the first pass's timings next to the pass of record (variance check)
        with open(args.pass1, encoding="utf-8") as f:
            p1 = {r["id"]: r for r in json.load(f)["pages"]}
        for pid, rec in records.items():
            if pid in p1 and p1[pid].get("speed"):
                rec["speed_pass1"] = {k: p1[pid]["speed"].get(k) for k in ("ttfb_ms", "dcl_ms", "load_ms", "lcp_ms", "transfer_bytes", "requests")}
    finalize(records, data["domains"], args.cache)


# --------------------------------------------------------------------------------------------------------------------
# Verdicts
# --------------------------------------------------------------------------------------------------------------------
BOOL_SCORE = {"Y": 1.0, "link": 0.5, "text": 0.0, "-": 0.0}


def score(direction, v):
    if v is None or v == "?":
        return None
    if direction == "bool":
        return BOOL_SCORE.get(v, 0.0)
    return float(v)


def best_of(direction, cands):
    """cands: list of (name, value). Returns (best_value, [names])."""
    sc = [(n, v, score(direction, v)) for n, v in cands]
    sc = [x for x in sc if x[2] is not None]
    if not sc:
        return None, []
    pick = max if direction in ("bool", "hi") else min
    b = pick(x[2] for x in sc)
    names = [n for n, v, s in sc if s == b]
    bv = next(v for n, v, s in sc if s == b)
    return bv, names


def verdict(direction, tol, ours, best):
    so, sb = score(direction, ours), score(direction, best)
    if so is None:
        return "n/a"
    if sb is None:
        return "LEAD"
    if direction == "bool":
        return "LEAD" if so > sb else ("TIE" if so == sb else "LOSE")
    ab, rel = tol
    margin = max(ab, rel * abs(sb))
    if abs(so - sb) <= margin:
        return "TIE"
    better = so > sb if direction == "hi" else so < sb
    return "LEAD" if better else "LOSE"


def fmt(v):
    if v is None:
        return "n/a"
    if isinstance(v, float) and v <= 1.0 and v >= 0:
        return f"{v:.2f}"
    if isinstance(v, (int, float)):
        return f"{v:,.0f}" if abs(v) >= 1000 else (f"{v:g}" if isinstance(v, float) else str(v))
    return str(v)


NOTES = {
    "multi_track": "an Israeli mortgage concept; foreign loans have no tracks",
    "compare_scenarios": "ours: 4 mixes + the 3 BoI baskets side by side",
    "stress_test": "Supermarker: 'stress' and 'crisis' presets",
    "historical_stress": "Supermarker's 'crisis' is a fixed shock, not the real 2022 path",
    "forecast_scenario": "Supermarker also uses the BoI research forecast",
    "prepayment_fee": "world: one click away on a sibling URL (MSE, Nationwide, Dr. Klein, Pretto)",
    "refinance": "ours: the refinance break-even in the exit tool (1.72.591) + the link to the refinance page",
    "afford_to_homes": "budget tool links to /properties/; Chase: a generic link",
    "offer_comparison": "Supermarker checks one offer against the market",
    "per_bank_benchmark": "from the BoI per-bank averages",
    "offer_vs_market_money": "Supermarker has it too (all-bank average)",
    "regulatory_checks": "Supermarker checks 3 rules + LTV; ours 4 rules",
    "costs_in_payment": "ours: optional insurance and arnona/building-fee fields add to the payment (1.72.592); no defaults, since Israel has no official insurance price table",
    "local_defaults": "",
    "tool_switcher": "Supermarker has 2 modes",
    "payment_frequency": "Israeli mortgages are paid monthly",
    "cpi_indexation": "an Israeli concept",
    "by_bank_rates": "Finder: commercial offers; ours: official averages",
    "dated_sourced": "a proxy count",
    "market_data_age_days": "BoI publishes monthly, about 3 weeks after the month ends",
    "figures_raw": "Calculator.net prints a 360-row schedule in HTML",
    "cells_raw": "same reason",
    "first_input_y": "ours opens with H1, answer paragraph and CTAs (content-first order)",
    "first_money_y": "ours: the figure in the answer paragraph",
    "page_height": "world leaders with a full article: NerdWallet 13,548, nesto 23,390",
    "tap44_share": "0.66 in pass 1 (the page changed between passes)",
    "html_bytes": "ours: 105 KB inline CSS, 71 KB inline JS, 34 KB JSON-LD",
    "transfer_bytes": "Stripe 287 KB, tawk.to 241 KB, fonts 207 KB, a 166 KB hotlinked photo",
    "ttfb_ms": "pass 1: 967 ms; no page-cache header seen",
    "load_ms": "pass 1: 2,479 ms",
    "input_label_share": "9 of 55: the classic calculator's 3 x 3 grid",
}


def cmd_report(args):
    with open(PROOF_JSON, encoding="utf-8") as f:
        data = json.load(f)
    pages = data["pages"]
    ours = next(p for p in pages if p["id"] == "ours")
    usable = lambda p: not p.get("blocked") and not p.get("error") and p.get("values")
    il = [p for p in pages if p["region"] == "IL" and usable(p)]
    wo = [p for p in pages if p["region"] == "WORLD" and usable(p)]
    rows, tally = [], {"IL": {"LEAD": 0, "TIE": 0, "LOSE": 0, "n/a": 0}, "WORLD": {"LEAD": 0, "TIE": 0, "LOSE": 0, "n/a": 0}}
    # pages without a phone layout (laid out at ~980 px and shrunk) cannot hold the best phone position or size
    phone_layout = lambda p: ((p.get("phone") or {}).get("scroll_width") or 0) <= 440
    phone_pos = {"first_input_y", "first_money_y", "page_height", "tap44_share"}
    for g, pid, label, direction, tol, definition in PARAMS:
        ov = ours["values"].get(pid)
        il_p = [p for p in il if phone_layout(p)] if pid in phone_pos else il
        wo_p = [p for p in wo if phone_layout(p)] if pid in phone_pos else wo
        bil, nil = best_of(direction, [(p["name"], p["values"].get(pid)) for p in il_p])
        bwo, nwo = best_of(direction, [(p["name"], p["values"].get(pid)) for p in wo_p])
        vil, vwo = verdict(direction, tol, ov, bil), verdict(direction, tol, ov, bwo)
        tally["IL"][vil] += 1
        tally["WORLD"][vwo] += 1
        rows.append({"group": g, "id": pid, "label": label, "ours": ov, "best_il": bil, "best_il_pages": nil,
                     "best_world": bwo, "best_world_pages": nwo, "v_il": vil, "v_world": vwo, "direction": direction})
    lines = ["| # | Group | Parameter | Ours | Best Israel (page) | Best world (page) | vs IL | vs world | Note |",
             "|---|---|---|---|---|---|---|---|---|"]
    n_il, n_wo = len(il), len(wo)
    for i, r in enumerate(rows, 1):
        def cell(best, names, n):
            if best is None:
                return "n/a"
            if r["direction"] == "bool" and BOOL_SCORE.get(best, 0) == 0:
                return f"none of {n}"
            if r["direction"] == "bool":
                return f"{best}: " + ", ".join(names[:3]) + (f" +{len(names) - 3}" if len(names) > 3 else "") + f" ({len(names)} of {n})"
            return f"{fmt(best)} (" + ", ".join(names[:2]) + (f" +{len(names) - 2}" if len(names) > 2 else "") + ")"
        lines.append(f"| {i} | {r['group'][2:]} | {r['label']} | {fmt(r['ours'])} | {cell(r['best_il'], r['best_il_pages'], n_il)} | "
                     f"{cell(r['best_world'], r['best_world_pages'], n_wo)} | {r['v_il']} | {r['v_world']} | {NOTES.get(r['id'], '')} |")
    out = os.path.join(args.cache, "proof-table.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n\n" + json.dumps(tally) + "\n")
    with open(os.path.join(args.cache, "proof-rows.json"), "w", encoding="utf-8") as f:
        json.dump({"rows": rows, "tally": tally, "il_pages": [p["name"] for p in il], "world_pages": [p["name"] for p in wo],
                   "excluded": [{"name": p["name"], "status": p.get("status"), "blocked": p.get("blocked"), "error": p.get("error") or p.get("goto_error")}
                                for p in pages if p["id"] != "ours" and not usable(p)]}, f, ensure_ascii=False, indent=1, default=str)
    # keep the verdicts and the pressed-tools check inside proof.json as well
    data["verdicts"] = {"tally": tally, "rows": rows, "il_pages": [p["name"] for p in il], "world_pages": [p["name"] for p in wo]}
    vpath = os.path.join(args.cache, "verify-ours.json")
    if os.path.exists(vpath):
        with open(vpath, encoding="utf-8") as f:
            data["ours_pressed"] = json.load(f)
    with open(PROOF_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, default=str)
    print(out)
    print(json.dumps(tally))


# --------------------------------------------------------------------------------------------------------------------
# Our own tools, pressed (our site only)
# --------------------------------------------------------------------------------------------------------------------
def cmd_verify_ours(args):
    from playwright.sync_api import sync_playwright
    url = "https://nad-lan.co.il/mortgage-calculator/"
    res = {"url": url, "checked_utc": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z", "tools": []}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(viewport=VIEWPORT, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA_MOBILE, locale="he-IL")
        page = ctx.new_page()
        cdp = ctx.new_cdp_session(page)
        cdp.send("Network.enable")
        reqs = {}
        cdp.on("Network.requestWillBeSent", lambda e: reqs.setdefault(e["requestId"], {"url": e["request"]["url"], "type": e.get("type"), "bytes": 0}))
        cdp.on("Network.loadingFinished", lambda e: reqs.get(e["requestId"], {}).__setitem__("bytes", e.get("encodedDataLength") or 0))
        resp = page.goto(url, wait_until="load", timeout=90000)
        page.wait_for_timeout(4000)
        hdr = resp.headers if resp else {}
        res["document_headers"] = {k: v for k, v in hdr.items() if k.lower() in ("cache-control", "x-cache", "x-cache-status", "cf-cache-status", "age", "x-varnish", "x-proxy-cache", "server", "x-litespeed-cache", "x-upress-cache", "content-encoding", "x-powered-by")}
        by_host, by_type = {}, {}
        for r in reqs.values():
            h = urlparse(r["url"]).netloc or r["url"][:20]
            by_host.setdefault(h, [0, 0]); by_host[h][0] += 1; by_host[h][1] += r["bytes"]
            t = r.get("type") or "?"
            by_type.setdefault(t, [0, 0]); by_type[t][0] += 1; by_type[t][1] += r["bytes"]
        res["requests_by_host"] = sorted(([h, n, b] for h, (n, b) in by_host.items()), key=lambda x: -x[2])
        res["requests_by_type"] = sorted(([t, n, b] for t, (n, b) in by_type.items()), key=lambda x: -x[2])
        res["largest_requests"] = sorted(([r["url"][:140], r.get("type"), r["bytes"]] for r in reqs.values()), key=lambda x: -x[2])[:15]
        HOSTS_JS ="""() => Array.from(document.querySelectorAll('[data-nli]')).map(h => ({tool: h.getAttribute('data-nli'),
              inputs: h.querySelectorAll('input,select,textarea').length, buttons: h.querySelectorAll('button').length,
              tables: h.querySelectorAll('table').length, checkboxes: h.querySelectorAll('input[type=checkbox]').length,
              money: ((h.innerText || '').match(/\\d[\\d,.]*\\s?₪|₪\\s?\\d/g) || []).length,
              text: (h.innerText || '').replace(/\\s+/g, ' ').slice(0, 600), visible: !!(h.offsetWidth || h.offsetHeight)}))"""
        res["hosts_on_load"] = page.evaluate(HOSTS_JS)

        def host_text(tool):
            return page.evaluate("t => { const h = document.querySelector('[data-nli=\"' + t + '\"]'); return h ? (h.innerText || '').replace(/\\s+/g, ' ') : null; }", tool)

        steps = []

        def step(name, fn):
            try:
                r = fn()
                steps.append({"step": name, "ok": bool(r.get("ok")), **r})
            except Exception as e:
                steps.append({"step": name, "ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"})

        q = page.locator('[data-nli="mquick"]')

        def quick_amount():
            before = host_text("mquick")
            inp = q.locator("input:visible").first
            inp.fill("1500000")
            inp.press("Tab")
            page.wait_for_timeout(800)
            after = host_text("mquick")
            return {"ok": before != after and "₪" in (after or ""), "before": (before or "")[:240], "after": (after or "")[:240]}

        def quick_mode(label, values):
            def run():
                q.get_by_role("button", name=label, exact=True).first.click()
                page.wait_for_timeout(500)
                vis = q.locator("input:visible")
                n = vis.count()
                before = host_text("mquick")
                for i, v in enumerate(values[:n]):
                    vis.nth(i).fill(v)
                    vis.nth(i).press("Tab")
                page.wait_for_timeout(800)
                after = host_text("mquick")
                return {"ok": n >= len(values) and before != after, "visible_inputs": n, "after": (after or "")[:300]}
            return run

        def quick_bank():
            before = host_text("mquick")
            q.get_by_role("button", name="לאומי", exact=True).first.click()
            page.wait_for_timeout(800)
            after = host_text("mquick")
            return {"ok": before != after, "after": (after or "")[:240]}

        step("quick: change the amount", quick_amount)
        step("quick: by price and equity", quick_mode("לפי מחיר והון עצמי", ["2400000", "800000"]))
        step("quick: by monthly payment", quick_mode("לפי החזר חודשי", ["7000"]))
        step("quick: one bank (Leumi)", quick_bank)
        page.screenshot(path=os.path.join(args.cache, "verify-quick.jpg"), type="jpeg", quality=55)

        def full_tool():
            info = page.evaluate("""() => { const h = document.querySelector('[data-nli="mortgage"]'); if (!h) return null;
                const t = (h.innerText || h.textContent || '').replace(/\\s+/g, ' ');
                return {tracks: h.querySelectorAll('select').length, baskets: /סל אחיד 1/.test(h.textContent), compare: /שמירת התמהיל הזה להשוואה/.test(h.textContent),
                        prepay: /לחשב פירעון מוקדם/.test(h.textContent), schedule: /לוח הסילוקין|להצגת כל/.test(h.textContent),
                        directive: /(329|שיעור המימון|חורג|עומד)/.test(h.textContent), offer: /הריבית בהצעה/.test(h.textContent),
                        tables: h.querySelectorAll('table').length, excerpt: t.slice(0, 300)}; }""")
            return {"ok": bool(info and info["baskets"] and info["compare"] and info["prepay"] and info["schedule"]), **(info or {})}

        step("Mortgage 2.0 present (tracks, baskets, compare, prepayment, schedule, 329, offer)", full_tool)

        def add_baskets():
            # on phones the full tool sits inside a closed <details> after it draws: open it first, as a user would
            page.evaluate("""() => { const h = document.querySelector('[data-nli="mortgage"]'); const d = h && h.closest('details');
                if (d && !d.open) { d.querySelector('summary').scrollIntoView(); d.querySelector('summary').click(); } }""")
            page.wait_for_timeout(800)
            m = page.locator('[data-nli="mortgage"]')
            btn = m.get_by_role("button", name="הוספת שלושת הסלים האחידים").first
            btn.scroll_into_view_if_needed()
            t0 = page.evaluate("() => document.querySelector('[data-nli=\"mortgage\"]').querySelectorAll('table').length")
            btn.click()
            page.wait_for_timeout(1000)
            t1 = page.evaluate("() => document.querySelector('[data-nli=\"mortgage\"]').querySelectorAll('table').length")
            txt = host_text("mortgage") or ""
            i = txt.find("סל אחיד 1")
            return {"ok": t1 >= t0 and ("סל אחיד 1" in txt), "tables_before": t0, "tables_after": t1, "excerpt": txt[max(0, i - 80): i + 300]}

        step("Mortgage 2.0: add the three BoI baskets to the comparison", add_baskets)

        switch = [("כמה דירה זה קונה", "mbudget"), ("שלוש הצעות, טבלה אחת", "moffers"), ("החלטת הריבית", "mdecision"),
                  ("אם 2022 חוזרת", "mreplay"), ("כמה תעלה היציאה", "mexit"), ("מוכנים לאישור עקרוני?", "mready")]
        for label, tool in switch:
            def run(label=label, tool=tool):
                btn = page.get_by_role("button", name=label, exact=True).first
                btn.scroll_into_view_if_needed()
                btn.click()
                page.wait_for_timeout(1500)
                hs = page.evaluate(HOSTS_JS)
                h = next((x for x in hs if x["tool"] == tool), None)
                try:
                    page.locator(f'[data-nli="{tool}"]').first.screenshot(path=os.path.join(args.cache, f"verify-{tool}.jpg"), type="jpeg", quality=50)
                except Exception:
                    pass
                return {"ok": bool(h and h["visible"] and h["money"] > 0), "tool": tool, "visible": h and h["visible"],
                        "money_figures": h and h["money"], "inputs": h and h["inputs"], "tables": h and h["tables"],
                        "checkboxes": h and h["checkboxes"], "excerpt": h and h["text"][:420]}
            step(f"switcher: {label}", run)

        def budget_homes():
            h = page.locator('[data-nli="mbudget"]')
            links = h.locator("a[href]")
            hrefs = [(links.nth(i).inner_text().strip()[:40], links.nth(i).get_attribute("href")) for i in range(min(links.count(), 30))]
            homes = [h for h in hrefs if "nad-lan.co.il/properties" in (h[1] or "") or (h[1] or "").startswith("/properties")]
            return {"ok": bool(homes), "homes_links": homes[:6], "all_links": len(hrefs)}

        step("budget tool links to real homes on the site (href only, not opened)", budget_homes)

        def ready_docs():
            n = page.evaluate("() => { const h = document.querySelector('[data-nli=\"mready\"]'); return h ? {cb: h.querySelectorAll('input[type=checkbox]').length, src: (h.textContent.match(/נבדק|מקור/g) || []).length} : null; }")
            return {"ok": bool(n and n["cb"] >= 10), **(n or {})}

        step("readiness tool: document checklist", ready_docs)
        res["steps"] = steps
        res["passed"] = sum(1 for s in steps if s["ok"])
        res["total"] = len(steps)
        b.close()
    out = os.path.join(args.cache, "verify-ours.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["measure", "refeature", "report", "verify-ours"])
    ap.add_argument("--only", default="")
    ap.add_argument("--cache", default=DEFAULT_CACHE)
    ap.add_argument("--pass1", default="", help="refeature: an earlier proof.json whose timings are kept as speed_pass1")
    a = ap.parse_args()
    {"measure": cmd_measure, "refeature": cmd_refeature, "report": cmd_report, "verify-ours": cmd_verify_ours}[a.cmd](a)
