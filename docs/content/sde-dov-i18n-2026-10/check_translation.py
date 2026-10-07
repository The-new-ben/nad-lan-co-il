# -*- coding: utf-8 -*-
"""HAD-439 Stage A: the gate for one ChatGPT language version of the Sde Dov hub (/sde-dov/) or of the Sde Dov prices page
(/sde-dov/prices/), before it may be published. Generalized from docs/content/north-tel-aviv-2026-10/check_translation.py:
the pages are a registry (PAGES), so another page pair is one more entry plus its claims.

    python check_translation.py ARTICLE.html --page sde-dov-hub|sde-dov-prices --lang en|fr|ru|ar|he [--meta META.txt]
                                [--peer OTHER.html] [--offline] [--no-link-get] [--write REPORT.md]
    python check_translation.py --selftest [--live] [--offline]
    python check_translation.py --dump-source PAGE        (prints the Hebrew translation source the packets give the writer)

ARTICLE.html is the article body ChatGPT returned (all parts joined, the ```html fences removed). META.txt (optional) holds
the lines "title: ..." and "description: ..." (the SEO title and description ChatGPT returned).

Hard gates (exit code 1 when any fails):
 1. NUMBERS: every number in the visible text, the SEO title and the description is matched to a claim of the page in
    claims.json (the page's claims plus the G conventions). Locale formats are accepted: 9,450,000 / 9 450 000 / 9.450.000
    (thousands), 9,45 (fr/ru decimal), Arabic-Indic digits, ٬ and ٫, 07.10.2026 for 7.10.2026, and the exact million form of
    a round amount (9,450,000 = 9.45 million). A dotted date (4.2026, 12.3.2020) must be a full date of a claim; a plain
    integer may also be a part of one (12 March 2020).
 2. H1: exactly one <h1>.
 3. BANNED words (per language; tech or demo talk, Atlas, source names, "free advice", "coming soon") and em/en dashes.
 4. LINKS: no external link (only nad-lan.co.il, relative links, #anchors and mailto:info@nad-lan.co.il); every internal
    link must be in links.json for this page and language, and (unless --no-link-get/--offline) answer GET 200 now.
 5. SHORTCODES: none ([nadlan_area_map] and [nadlan_price_guide] are inserted by the site, never by the writer).
    MARKER: exactly one component marker of this page (<!-- NLAM --> on the hub, <!-- NLPG --> on the prices page), no
    marker of the other page, placed where the Hebrew page has its component: right after the first paragraph of the first
    H2 section, before the second H2.
 6. DUPLICATES: the H1, the SEO title and every H2 are compared, by their first 4 words (case and punctuation ignored), with
    the title, H1 and H2s of the other live pages in the same language (COMPARATORS: the language's guides, new projects,
    brokers, developer deals, buy-from-abroad and Kikar HaMedina pages, /en/north-tel-aviv/ and /en/north-tel-aviv/rova-4/,
    and the language versions of the Sde Dov project pages; for he the Hebrew equivalents and the other page of this pair).
    Fetched live; --offline uses live-headings.json. The language's plain FAQ heading is exempt.
 7. META lengths: SEO title <= 60 characters, description <= 155 (a warning for he: the Hebrew Yoast fields are not part of
    this task and are reported, not edited).
Warnings (reported, not fatal): soft style words, "!", Hebrew letters left in a non-Hebrew article, word count outside the
packet's budget, H2 count different from the Hebrew source.
"""
import argparse, datetime, html as H, io, json, os, re, sys, time, urllib.error, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://nad-lan.co.il"
UA = {"User-Agent": "nad-lan.co.il translation gate (HAD-439; public pages, 1 req/0.4 s)"}
LANGS = ("he", "en", "fr", "ru", "ar")

# ------------------------------------------------------------------ the page registry
PAGES = {
    "sde-dov-hub": {
        "page_id": 4730, "he_path": "/sde-dov/", "rest": os.path.join("source", "hub-4730-rest.json"),
        "edits": "align-edits.json", "marker": "<!-- NLAM -->", "component_start": '<style id="nlam-css">',
        "target": "/{lang}/sde-dov/",
        # parts of the Hebrew page that are NOT translated (site chrome, disclaimers, an external source list)
        "drop": [r"<figure\b.*?</figure>", r"<p[^>]*><em>נבדק ועודכן:.*?</em></p>",
                 r"<p[^>]*><em>אין לראות במאמר זה ייעוץ משפטי.*?</em></p>", r"<p[^>]*><em>גבול הדיוק:.*?</em></p>",
                 r"<h3[^>]*>מקורות תכנון רשמיים</h3>\s*<ul[^>]*>.*?</ul>", r"<div class=\"nltlv-cluster-link-v1\".*?</div>"],
    },
    "sde-dov-prices": {
        "page_id": 4758, "he_path": "/sde-dov/prices/", "rest": os.path.join("source", "prices-4758-rest.json"),
        "edits": None, "marker": "<!-- NLPG -->", "component_start": '<style id="nlpg-css">',
        "target": "/{lang}/sde-dov/prices/",
        "drop": [r"<p>Sde Dov Tel Aviv real estate prices /.*?</p>", r"<p>מקורות לעיון:.*?</p>",
                 r"<p[^>]*><em>המידע מבוסס על מקורות פומביים.*?</em></p>", r"<div class='nadlan-guide'>.*?</section></div>"],
    },
}
MARKERS = {p["marker"] for p in PAGES.values()}
FAQ_H2 = {"he": "שאלות נפוצות", "en": "Frequently asked questions", "fr": "Questions fréquentes", "ru": "Частые вопросы",
          "ar": "أسئلة شائعة"}
# generic structural headings that may repeat across pages (normalised, exact match only)
GENERIC = {"he": {"שאלות נפוצות", "פתיחה", "סיכום קצר"}, "en": {"frequently asked questions"}, "fr": {"questions fréquentes"},
           "ru": {"частые вопросы"}, "ar": {"أسئلة شائعة"}}
SDD_PROJECTS = ["rainbow-tel-aviv", "ashira-sde-dov", "dimri-yama-sde-dov", "zohi-sde-dov", "gindi-vogue-sde-dov",
                "utopia-sde-dov", "shikun-binui-sde-dov"]   # the Sde Dov project pages that have -en/-fr/-ru/-ar versions


def _comparators(l):
    base = ["/%s/new-projects/" % l, "/%s/guides/" % l, "/%s/brokers/" % l, "/%s/developer-deals/" % l,
            "/%s/buy-property-in-israel/" % l, "/projects/hamedina-%s/" % l,
            "/%s/north-tel-aviv/" % l, "/%s/north-tel-aviv/rova-4/" % l]
    return base + ["/projects/%s-%s/" % (s, l) for s in SDD_PROJECTS]


COMPARATORS = {
    "he": ["/new-projects/", "/guides/", "/brokers/", "/developer-deals/", "/projects/hamedina/", "/north-tel-aviv/",
           "/north-tel-aviv/rova-4/"] + ["/projects/%s/" % s for s in SDD_PROJECTS],
    "en": _comparators("en"), "fr": _comparators("fr"), "ru": _comparators("ru"), "ar": _comparators("ar"),
}
PAIR = {k: v["he_path"] for k, v in PAGES.items()}

BANNED = {
    "he": [r"אטלס", r"ממשק", r"(?<![א-ת])דמו(?![א-ת])", r"הדגמה", r"נקודות חמות", r"אינטראקטיב",
           r"רספונסיב", r"מובייל", r"סימולציה", r"טכנולוגי", r"תלת ממד", r"בקרוב", r"(?:כיוון|מחיר|נתון|מועד|מידע)\s+בבדיקה",
           r"ייעוץ חינם", r"הפלטפורמה",
           r"(?<![א-ת])המערכת(?![א-ת])", r"ויקיפדיה", r"גלובס", r"כלכליסט", r"דה ?מרקר", r"מאקו", r"מדלן",
           r"יד ?2", r"ביזפורטל", r"סותבי", r"מעריב", r"וויינט|ynet", r"מרכז הנדל[״\"]ן", r"Atlas"],
    "en": [r"\batlas\b", r"\binterface\b", r"\bdemo\b", r"\bhotspots?\b", r"\boverlay\b", r"\bengine\b", r"\bsimulation",
           r"\btechnology\b", r"\bplatform\b", r"\b3D\b", r"coming soon", r"free advice", r"free consultation", r"Wikipedia",
           r"Globes", r"Calcalist", r"TheMarker", r"\bMako\b", r"Madlan", r"Yad ?2", r"Bizportal", r"Sotheby", r"Maariv",
           r"\bYnet\b", r"nadlancenter", r"Merkaz HaNadlan", r"ice\.co\.il", r"Psagot"],
    "fr": [r"\batlas\b", r"\binterface\b", r"\bdémo\b", r"\bmoteur\b", r"simulation", r"technologie", r"plateforme", r"\b3D\b",
           r"bientôt", r"conseil gratuit", r"consultation gratuite", r"Wikip[ée]dia", r"Globes", r"Calcalist", r"TheMarker",
           r"\bMako\b", r"Madlan", r"Yad ?2", r"Bizportal", r"Sotheby", r"Maariv", r"\bYnet\b", r"nadlancenter", r"Psagot"],
    "ru": [r"атлас", r"интерфейс", r"\bдемо\b", r"движок", r"симуляц", r"технолог", r"платформ", r"\b3D\b", r"\bскоро\b",
           r"бесплатн\w* консультац", r"Википеди", r"Wikipedia", r"Globes", r"Глобс", r"Calcalist", r"Калькалист", r"\bMako\b",
           r"Madlan", r"Мадлан", r"Yad ?2", r"Яд ?2", r"Bizportal", r"Sotheby", r"Маарив", r"Maariv", r"\bYnet\b", r"Psagot"],
    "ar": [r"أطلس", r"تجريبي", r"محر[ّ]?ك", r"محاكاة", r"تكنولوج", r"المنصة", r"ثلاثي الأبعاد", r"\b3D\b", r"قريباً",
           r"استشارة مجانية", r"ويكيبيديا", r"Wikipedia", r"Globes", r"غلوبس", r"Calcalist", r"كالكاليست", r"\bMako\b", r"Madlan",
           r"Yad ?2", r"Bizportal", r"Sotheby", r"معاريف", r"Maariv", r"\bYnet\b", r"Psagot"],
}
SOFT = {
    "he": [r"(?<![א-ת])בבדיקה", r"מנגנון", r"(?<![א-ת])שכבה", r"יחסית", r"כמעט", r"מהווה", r"ללא ספק", r"חשוב להבין", r"חשוב לזכור",
           r"ראוי לציין", r"לסיכום", r"יש לציין", r"דגל אדום", r"מלכודת", r"היזהרו"],
    "en": [r"\bdelve", r"\bnestled\b", r"\bboasts?\b", r"testament to", r"red flag", r"\bbeware\b", r"it is important to note",
           r"in conclusion", r"needless to say", r"\blayer\b"],
    "fr": [r"force est de constater", r"véritable écrin", r"\bniché", r"en conclusion", r"il est important de noter"],
    "ru": [r"стоит отметить", r"важно понимать", r"в заключение", r"уникальный шанс"],
    "ar": [r"تجدر الإشارة", r"في الختام", r"لا شك"],
}
AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
SPACES = "    "


def num_re(lang):
    """number tokens; a plain space joins thousands only in fr/ru (elsewhere only no-break / narrow / thin spaces do)"""
    sp = "    " if lang in ("fr", "ru") else "   "
    return re.compile(
        r"(?<![0-9A-Za-z.,])("
        r"\d{1,2}[./]\d{1,2}[./]\d{4}"                                   # 12.3.2020, 12/03/2020
        r"|\d{1,2}\.\d{4}(?![0-9])"                                     # 4.2026
        r"|\d{1,3}(?:(?:,\d{3})+|(?:\.\d{3}){2,}|(?:[" + sp + r"]\d{3})+)(?:[.,]\d+)?(?![0-9])"  # 9,450,000 / 9 450 000
        r"|\d+(?:[.,]\d+)?"                                              # 9.45 / 9,45 / 2026
        r")(?![0-9])")


# ------------------------------------------------------------------ text helpers
def visible_text(h):
    h = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    return H.unescape(re.sub(r"<[^>]+>", " ", h))


def strip_tags(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def canon(s):
    """'9,450,000' / '17.0' / '4.5' (claim style) -> canonical number string"""
    s = s.replace(",", "")
    try:
        f = float(s)
    except ValueError:
        return s
    return ("%f" % f).rstrip("0").rstrip(".")


def is_date(s):
    return bool(re.fullmatch(r"\d{1,2}[./]\d{1,2}[./]\d{4}|\d{1,2}\.\d{4}", s))


def date_canon(s):
    return ".".join(str(int(x)) for x in re.split(r"[./]", s))


def token_forms(tok, lang):
    """a number token as written in the article -> (kind, canonical) ; kind 'date', 'num' or 'either'"""
    t = tok.translate(AR_DIGITS).replace("٬", ",").replace("٫", ".")
    if is_date(t) and not re.fullmatch(r"\d{1,3}\.\d{3}", t):
        return "date", date_canon(t)
    for sp in SPACES:
        t = t.replace(sp, "")
    if re.fullmatch(r"\d{1,3}(\.\d{3}){2,}", t):            # 9.450.000
        t = t.replace(".", "")
    if lang in ("fr", "ru"):
        if re.fullmatch(r"\d+,\d+", t) and not re.fullmatch(r"\d{1,3}(,\d{3})+", t):
            t = t.replace(",", ".")
        elif re.fullmatch(r"\d+,\d+", t):                  # 3,665 in fr is ambiguous: keep both readings
            return "either", (canon(t.replace(",", ".")), canon(t))
        t = t.replace(",", "")
    else:
        if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", t):
            t = t.replace(",", "")
        elif re.fullmatch(r"\d+,\d+", t):
            return "either", (canon(t.replace(",", ".")), canon(t))
    return "num", canon(t)


# ------------------------------------------------------------------ claims
def load_claims(page):
    cl = json.load(io.open(os.path.join(HERE, "claims.json"), encoding="utf-8"))
    return [c for c in cl if c["page"] in (page, "both")]


def claim_index(claims):
    nums, dates = {}, {}
    for c in claims:
        for n in c["numbers"]:
            n = str(n)
            if re.fullmatch(r"\d+-\d+", n):                   # '1-3' (quarter months)
                for p in n.split("-"):
                    nums.setdefault(canon(p), set()).add(c["claim_id"])
                continue
            if is_date(n):
                d = date_canon(n)
                dates.setdefault(d, set()).add(c["claim_id"])
                for p in d.split("."):
                    nums.setdefault(canon(p), set()).add(c["claim_id"])
                continue
            k = canon(n)
            nums.setdefault(k, set()).add(c["claim_id"])
            try:
                v = float(n.replace(",", ""))
            except ValueError:
                continue
            if v >= 1_000_000 and v % 10_000 == 0:            # exact million form of a round amount
                nums.setdefault(canon("%.4f" % (v / 1e6)), set()).add(c["claim_id"])
            if v >= 1_000_000_000 and v % 10_000_000 == 0:
                nums.setdefault(canon("%.4f" % (v / 1e9)), set()).add(c["claim_id"])
    return nums, dates


def fact_check(text, lang, idx):
    nums, dates = idx
    rows = []
    t = text.translate(AR_DIGITS).replace("٬", ",").replace("٫", ".")
    for m in num_re(lang).finditer(t):
        tok = m.group(1)
        kind, val = token_forms(tok, lang)
        ids = set()
        if kind == "date":
            ids = dates.get(val, set())
        elif kind == "either":
            for v in val:
                ids |= nums.get(v, set())
        else:
            ids = nums.get(val, set())
        ctx = re.sub(r"\s+", " ", t[max(0, m.start() - 55):m.end() + 40]).strip()
        rows.append({"num": tok, "kind": kind, "claims": sorted(ids), "ok": bool(ids), "ctx": ctx})
    return rows


# ------------------------------------------------------------------ headings and links
def norm_heading(s):
    s = strip_tags(s).lower()
    s = re.sub(r"[֑-ׇ]", "", s)                    # Hebrew points
    s = re.sub(r"[^\w\s֐-׿؀-ۿ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def key4(s):
    return " ".join(norm_heading(s).split()[:4])


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)

    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    op = urllib.request.build_opener(NoRedir)
    try:
        r = op.open(req, timeout=timeout)
        return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def page_headings(html_text):
    title = [strip_tags(x) for x in re.findall(r"<title>(.*?)</title>", html_text, re.S)][:1]
    h1 = [strip_tags(x) for x in re.findall(r"<h1\b[^>]*>(.*?)</h1>", html_text, re.S)]
    h2 = [strip_tags(x) for x in re.findall(r"<h2\b[^>]*>(.*?)</h2>", html_text, re.S)]
    return {"title": title, "h1": h1, "h2": h2}


def live_headings(lang, page, offline=False):
    """comparators' title/H1/H2 in this language; live, or the saved snapshot"""
    snap_path = os.path.join(HERE, "live-headings.json")
    snap = json.load(io.open(snap_path, encoding="utf-8")) if os.path.exists(snap_path) else {"pages": {}}
    urls = list(COMPARATORS[lang])
    if lang == "he":
        urls += [u for p, u in PAIR.items() if p != page]
    out, src = {}, "live"
    for u in urls:
        got = None
        if not offline:
            try:
                st, body = fetch(SITE + u)
                got = {"status": st, **(page_headings(body) if st == 200 else {"title": [], "h1": [], "h2": []})}
                time.sleep(0.4)
            except Exception:  # network down: fall back
                got = None
        if got is None:
            got = snap["pages"].get(u)
            src = "snapshot %s" % snap.get("retrieved_utc", "?")
        if got:
            out[u] = got
    return out, src


def heading_dupes(own, lang, comps):
    """own: list of (kind, text). Returns list of (kind, text, url, other)."""
    hits = []
    generic = GENERIC.get(lang, set())
    for kind, text in own:
        if not text or norm_heading(text) in generic:
            continue
        k = key4(text)
        for u, d in comps.items():
            if d.get("status", 200) != 200:
                continue
            for okind in ("title", "h1", "h2"):
                for o in d.get(okind, []):
                    if lang != "he" and re.search(r"[א-ת]", o):
                        continue  # untranslated Hebrew site chrome on a language page
                    if norm_heading(o) in generic:
                        continue
                    if key4(o) == k:
                        hits.append((kind, text, u, "%s: %s" % (okind, o)))
    return hits


def check_links(h, lang, page, get=True):
    errs, warns, checked = [], [], []
    allowed = json.load(io.open(os.path.join(HERE, "links.json"), encoding="utf-8"))["pages"][page][lang]
    allowed_urls = {x["url"] for x in allowed}
    for href in re.findall(r"<a\b[^>]*\bhref\s*=\s*[\"']([^\"']+)[\"']", h, re.I):
        if href.startswith("#"):
            continue
        if href.lower() == "mailto:info@nad-lan.co.il":
            continue
        if href.startswith("/"):
            full = SITE + href
        elif re.match(r"https?://(www\.)?nad-lan\.co\.il(/|$)", href):
            full = re.sub(r"^https?://(www\.)?", "https://", href)
        else:
            errs.append("external or non-http link: %s" % href)
            continue
        if not full.endswith("/") and "?" not in full and "#" not in full:
            warns.append("link without a trailing slash: %s" % href)
        if full.split("#")[0] not in allowed_urls:
            errs.append("internal link not in links.json for %s/%s: %s" % (page, lang, href))
        checked.append(full.split("#")[0])
    if get:
        for u in sorted(set(checked)):
            try:
                st, _ = fetch(u)
            except Exception as e:
                st = str(e)
            if st != 200:
                errs.append("internal link does not answer 200 now (%s): %s" % (st, u))
            time.sleep(0.4)
    return errs, warns, checked


def check_marker(h, page):
    """the page's component marker: exactly once, after the first paragraph of the first H2 section, before the 2nd H2"""
    errs = []
    mk = PAGES[page]["marker"]
    n = h.count(mk)
    if n != 1:
        errs.append("marker %s appears %d times (must be exactly 1)" % (mk, n))
    for other in MARKERS - {mk}:
        if other in h:
            errs.append("marker %s belongs to another page" % other)
    if n == 1:
        i = h.find(mk)
        h2 = [m.start() for m in re.finditer(r"<h2\b", h, re.I)]
        if len(h2) < 2 or not h2[0] < i < h2[1]:
            errs.append("marker %s is not inside the first H2 section (the Hebrew page has its component there)" % mk)
        elif not re.search(r"</p>\s*$", h[:i]):
            errs.append("marker %s does not follow a paragraph" % mk)
        else:
            first_p = h.find("</p>", h2[0])
            if h.find("</p>", first_p + 1, i) != -1:
                errs.append("marker %s is not right after the FIRST paragraph of the first H2 section" % mk)
    return errs


def word_count(text, lang):
    if lang in ("he", "ar", "fr", "ru", "en"):
        return len(re.findall(r"[\w֐-׿؀-ۿ]+(?:['’][\w]+)?", text))
    return len(text.split())


# ------------------------------------------------------------------ the gate
def run(h, page, lang, meta=None, peer=None, offline=False, link_get=True, quiet=False):
    errs, warns = [], []
    body = h.strip()
    vis = visible_text(body)
    claims = load_claims(page)
    idx = claim_index(claims)
    # 1. numbers
    meta = meta or {}
    rows = fact_check(vis, lang, idx)
    for k in ("title", "description"):
        if meta.get(k):
            for r in fact_check(meta[k], lang, idx):
                r["ctx"] = "[SEO %s] %s" % (k, r["ctx"])
                rows.append(r)
    unmatched = [r for r in rows if not r["ok"]]
    if unmatched:
        errs.append("%d number(s) match no claim" % len(unmatched))
    # 2. H1
    h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", body, re.S | re.I)
    if len(h1s) != 1:
        errs.append("H1 count is %d (must be exactly 1)" % len(h1s))
    # 3. banned words and dashes
    bans = []
    for pat in BANNED[lang]:
        for m in re.finditer(pat, vis + " " + meta.get("title", "") + " " + meta.get("description", ""), flags=re.I):
            bans.append((pat, re.sub(r"\s+", " ", vis[max(0, m.start() - 40):m.end() + 40])))
    if bans:
        errs.append("%d banned-word hit(s)" % len(bans))
    dash_text = vis + meta.get("title", "") + meta.get("description", "")
    dashes = dash_text.count("—") + dash_text.count("–")
    if dashes:
        errs.append("%d em/en dash(es)" % dashes)
    soft = []
    for pat in SOFT.get(lang, []):
        for m in re.finditer(pat, vis, flags=re.I):
            soft.append((pat, re.sub(r"\s+", " ", vis[max(0, m.start() - 30):m.end() + 30])))
    if "!" in vis:
        warns.append("%d exclamation mark(s)" % vis.count("!"))
    # 4. links
    lerrs, lwarns, links = check_links(body, lang, page, get=link_get and not offline)
    errs += lerrs
    warns += lwarns
    # 5. shortcodes and the component marker
    sc = re.findall(r"\[/?[a-z_]+(?:\s[^\]]*)?\]", vis)
    sc = [s for s in sc if re.match(r"\[/?(nadlan|nl|vc_|et_|elementor|caption|gallery|embed)", s)]
    if sc:
        errs.append("shortcode(s): %s" % sc)
    errs += check_marker(body, page)
    # 6. duplicates
    own = [("h1", strip_tags(x)) for x in h1s] + [("h2", strip_tags(x)) for x in re.findall(r"<h2\b[^>]*>(.*?)</h2>", body, re.S)]
    if meta.get("title"):
        own.append(("seo-title", meta["title"]))
    comps, comp_src = live_headings(lang, page, offline=offline)
    if peer:
        comps["(peer file)"] = {"status": 200, **page_headings(peer)}
    dupes = heading_dupes(own, lang, comps)
    if dupes:
        errs.append("%d heading(s) duplicate another live page (first 4 words)" % len(dupes))
    # 7. meta lengths (the Hebrew Yoast fields are reported only: not part of this task)
    meta_msgs = []
    if meta.get("title") and len(meta["title"]) > 60:
        meta_msgs.append("SEO title is %d characters (max 60)" % len(meta["title"]))
    if meta.get("description") and len(meta["description"]) > 155:
        meta_msgs.append("SEO description is %d characters (max 155)" % len(meta["description"]))
    if lang == "he":
        warns += ["Hebrew source meta (not edited here): " + m for m in meta_msgs]
    else:
        errs += meta_msgs
    # warnings
    if lang != "he":
        heb = re.findall(r"[א-ת]+(?:[\s״׳\"'][א-ת]+)*", vis)
        if heb:
            warns.append("Hebrew left in the text (%d runs; names in parentheses are fine): %s" % (len(heb), heb[:6]))
    wc = word_count(vis, lang)
    packet_path = os.path.join(HERE, "packets", "%s-%s.json" % (page, lang))
    n_h2 = len([x for x in own if x[0] == "h2"])
    if lang != "he" and os.path.exists(packet_path):
        pk = json.load(io.open(packet_path, encoding="utf-8"))
        lo, hi = pk["words_total_range"]
        if not lo <= wc <= hi:
            warns.append("net words %d outside the packet's range %d-%d" % (wc, lo, hi))
        if n_h2 != pk["h2_count"]:
            warns.append("H2 count %d, the Hebrew source has %d" % (n_h2, pk["h2_count"]))
    res = {"page": page, "lang": lang, "words": wc, "h2": n_h2, "numbers": len(rows), "unmatched": unmatched, "errors": errs,
           "warnings": warns, "banned": bans, "soft": soft, "dupes": dupes, "links": links, "comparators": list(comps),
           "comparator_source": comp_src, "rows": rows}
    if not quiet:
        report(res)
    return res


def report(r):
    print("== %s/%s | net words %d | H2 %d | numbers %d, unmatched %d | errors %d | warnings %d | comparators %d (%s)"
          % (r["page"], r["lang"], r["words"], r["h2"], r["numbers"], len(r["unmatched"]), len(r["errors"]),
             len(r["warnings"]), len(r["comparators"]), r["comparator_source"]))
    for e in r["errors"]:
        print("  FAIL:", e)
    for u in r["unmatched"]:
        print("    UNMATCHED %s: ...%s..." % (u["num"], u["ctx"]))
    for p, c in r["banned"]:
        print("    BANNED %s: ...%s..." % (p, c))
    for k, t, u, o in r["dupes"]:
        print("    DUPLICATE %s %r ~ %s %s" % (k, t, u, o))
    for w in r["warnings"]:
        print("  warn:", w)
    if r["soft"]:
        print("  warn: %d soft style word(s): %s" % (len(r["soft"]), sorted(set(p for p, _ in r["soft"]))))
    print("  RESULT:", "PASS" if not r["errors"] else "FAIL")


def write_md(r, path):
    by = {c["claim_id"]: c for c in json.load(io.open(os.path.join(HERE, "claims.json"), encoding="utf-8"))}
    md = ["# Translation check, %s / %s (%s UTC)\n" % (r["page"], r["lang"], datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")),
          "- Result: **%s**. Errors: %d. Warnings: %d." % ("PASS" if not r["errors"] else "FAIL", len(r["errors"]), len(r["warnings"])),
          "- Net words: %d. H2: %d. Numbers: %d, unmatched: %d." % (r["words"], r["h2"], r["numbers"], len(r["unmatched"])),
          "- Heading comparators (%s): %s\n" % (r["comparator_source"], ", ".join(r["comparators"]))]
    md += ["## Errors\n"] + ["- %s" % e for e in r["errors"]] + ["", "## Warnings\n"] + ["- %s" % w for w in r["warnings"]]
    md += ["", "## Every number\n", "| # | number | claims | context |", "|---|---|---|---|"]
    for k, x in enumerate(r["rows"], 1):
        md.append("| %d | %s | %s | %s |" % (k, x["num"], ", ".join(x["claims"]) or "**UNMATCHED**", x["ctx"].replace("|", "/")))
    used = sorted(set(i for x in r["rows"] for i in x["claims"]))
    md += ["", "## Claims used\n", "| claim | statement | source |", "|---|---|---|"]
    md += ["| %s | %s | %s |" % (i, by[i]["claim"].replace("|", "/"), by[i]["source"].replace("|", "/")) for i in used if i in by]
    io.open(path, "w", encoding="utf-8").write("\n".join(md) + "\n")


def read_meta(path):
    meta = {}
    if path:
        for line in io.open(path, encoding="utf-8-sig"):
            m = re.match(r"\s*(title|description|url)\s*:\s*(.+?)\s*$", line, re.I)
            if m:
                meta[m.group(1).lower()] = m.group(2)
    return meta


# ------------------------------------------------------------------ the Hebrew translation sources
def apply_edits(content, edits_file, quiet=False):
    """align-edits.json applied in memory, in order; each old must match exactly once at its turn"""
    edits = json.load(io.open(os.path.join(HERE, edits_file), encoding="utf-8"))["edits"]
    applied, missed = 0, []
    for e in edits:
        n = content.count(e["old"])
        if n != e.get("expect_matches", 1):
            missed.append((e["n"], n))
            continue
        content = content.replace(e["old"], e["new"])
        applied += 1
    if not quiet:
        print("  %s: %d of %d align edits applied in memory%s" % (edits_file, applied, len(edits),
                                                                    (" (missed: %s)" % missed) if missed else ""))
    return content


def hebrew_source(page, live=False, quiet=False):
    """the Hebrew page exactly as the writer receives it: align edits applied (hub), the site component replaced by its
    marker, the untranslated parts dropped. Returns (html, meta)."""
    cfg = PAGES[page]
    if live:
        st, js = fetch(SITE + "/wp-json/wp/v2/pages/%d?_fields=content,title,yoast_head_json" % cfg["page_id"])
        rest = json.loads(js)
    else:
        rest = json.load(io.open(os.path.join(HERE, cfg["rest"]), encoding="utf-8"))
    c = rest["content"]["rendered"].replace("\r\n", "\n")
    if cfg["edits"]:
        c = apply_edits(c, cfg["edits"], quiet=quiet)
    a = c.find(cfg["component_start"])
    b = c.find("</script>", a)
    if a >= 0 and b > a:
        c = c[:a] + "\n" + cfg["marker"] + "\n" + c[b + len("</script>"):]
    elif not quiet:
        print("  WARNING: no component found on", page)
    for pat in cfg["drop"]:
        c = re.sub(pat, "", c, flags=re.S)
    c = re.sub(r"<!--(?! NL(?:AM|PG) -->).*?-->", "", c, flags=re.S)   # comments other than the marker
    c = re.sub(r"<(script|style|svg)\b.*?</\1>", "", c, flags=re.S)
    if "<h1" not in c:   # the H1 is normally in the content of these pages; fall back to the title
        c = "<h1>%s</h1>\n%s" % (H.unescape(rest["title"]["rendered"]), c)
    meta = {"title": H.unescape((rest.get("yoast_head_json") or {}).get("title", "")),
            "description": H.unescape((rest.get("yoast_head_json") or {}).get("description", ""))}
    return c, meta


def selftest(live=False, offline=False):
    ok = True
    for page in PAGES:
        h, meta = hebrew_source(page, live)
        # the Hebrew pages link to Hebrew pages only; links.json "he" lists them
        res = run(h, page, "he", meta=meta, offline=offline, link_get=not offline)
        ok = ok and not res["errors"]
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("article", nargs="?")
    ap.add_argument("--page", choices=sorted(PAGES))
    ap.add_argument("--lang", choices=LANGS)
    ap.add_argument("--meta")
    ap.add_argument("--peer")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--no-link-get", action="store_true")
    ap.add_argument("--write")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--dump-source", choices=sorted(PAGES))
    a = ap.parse_args()
    if a.dump_source:
        print(hebrew_source(a.dump_source, a.live, quiet=True)[0])
        return
    if a.selftest:
        sys.exit(0 if selftest(a.live, a.offline) else 1)
    if not (a.article and a.page and a.lang):
        ap.error("ARTICLE, --page and --lang are required (or --selftest)")
    h = io.open(a.article, encoding="utf-8-sig").read()
    h = re.sub(r"^\s*```html\s*|\s*```\s*$", "", h)
    peer = io.open(a.peer, encoding="utf-8-sig").read() if a.peer else None
    res = run(h, a.page, a.lang, meta=read_meta(a.meta), peer=peer, offline=a.offline, link_get=not a.no_link_get)
    if a.write:
        write_md(res, a.write)
        print("  wrote", a.write)
    sys.exit(1 if res["errors"] else 0)


if __name__ == "__main__":
    main()
