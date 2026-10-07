# -*- coding: utf-8 -*-
"""HAD-460 Stage A: the gate for one ChatGPT language version of the North Tel Aviv hub or of Rova 4, before it may be
published. Modelled on docs/research/2026-10-kikar-v7/check_article.py.

    python check_translation.py ARTICLE.html --page hub|rova-4 --lang en|fr|ru|ar|he [--meta META.txt] [--peer OTHER.html]
                                [--offline] [--no-link-get] [--write REPORT.md]
    python check_translation.py --selftest [--live] [--offline]

ARTICLE.html is the article body ChatGPT returned (all parts joined, the ```html fences removed). META.txt (optional) holds
the lines "title: ..." and "description: ..." (the SEO title and description ChatGPT returned).

Hard gates (exit code 1 when any fails):
 1. NUMBERS: every number in the visible text, the SEO title and the description is matched to a claim of the page in
    claims.json (the page's claims plus the G conventions). Locale formats are accepted: 6,835,800 / 6 835 800 / 6.835.800
    (thousands), 30,7 (fr/ru decimal), Arabic-Indic digits, ٬ and ٫, 23.05.2018 for 23.5.2018, and the exact million form
    of a round amount (17,600,000 = 17.6 million). A dotted date (3.2026, 23.5.2018) must be a full date of a claim; a plain
    integer may also be a part of one (23 May 2018).
 2. H1: exactly one <h1>.
 3. BANNED words (per language; tech or demo talk, Atlas, source names, "free advice", "coming soon") and em/en dashes.
 4. LINKS: no external link (only nad-lan.co.il, relative links, #anchors and mailto:info@nad-lan.co.il); every internal
    link must be in links.json for this page and language, and (unless --no-link-get/--offline) answer GET 200 now.
 5. SHORTCODES: none ([nadlan_price_guide] and [nadlan_area_map] are inserted by the site, never by the writer).
 6. DUPLICATES: the H1, the SEO title and every H2 are compared, by their first 4 words (case and punctuation ignored), with
    the title, H1 and H2s of the other live pages in the same language (/en/new-projects/, /en/guides/, /en/brokers/,
    /en/developer-deals/, /en/buy-property-in-israel/, the language's Kikar HaMedina page, and their fr/ru/ar siblings that
    exist; for he the Hebrew equivalents and the other page of this pair). Fetched live; --offline uses live-headings.json.
    The language's plain FAQ heading ("Frequently asked questions", ...) is exempt.
 7. META lengths: SEO title <= 60 characters, description <= 155.
Warnings (reported, not fatal): soft style words, "!", Hebrew letters left in a non-Hebrew article, word count outside the
packet's budget, H2 count different from the Hebrew source.
"""
import argparse, datetime, html as H, io, json, os, re, sys, time, urllib.error, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://nad-lan.co.il"
UA = {"User-Agent": "nad-lan.co.il translation gate (HAD-460; public pages, 1 req/0.4 s)"}
LANGS = ("he", "en", "fr", "ru", "ar")
FAQ_H2 = {"he": "שאלות נפוצות", "en": "Frequently asked questions", "fr": "Questions fréquentes", "ru": "Частые вопросы",
          "ar": "أسئلة شائعة"}
# generic structural headings that may repeat across pages (normalised, exact match only)
GENERIC = {"he": {"שאלות נפוצות", "פתיחה"}, "en": {"frequently asked questions"}, "fr": {"questions fréquentes"},
           "ru": {"частые вопросы"}, "ar": {"أسئلة شائعة"}}
COMPARATORS = {
    "he": ["/new-projects/", "/guides/", "/brokers/", "/developer-deals/", "/projects/hamedina/"],
    "en": ["/en/new-projects/", "/en/guides/", "/en/brokers/", "/en/developer-deals/", "/en/buy-property-in-israel/",
           "/projects/hamedina-en/"],
    "fr": ["/fr/new-projects/", "/fr/guides/", "/fr/brokers/", "/fr/developer-deals/", "/fr/buy-property-in-israel/",
           "/projects/hamedina-fr/"],
    "ru": ["/ru/new-projects/", "/ru/guides/", "/ru/brokers/", "/ru/developer-deals/", "/ru/buy-property-in-israel/",
           "/projects/hamedina-ru/"],
    "ar": ["/ar/new-projects/", "/ar/guides/", "/ar/brokers/", "/ar/developer-deals/", "/ar/buy-property-in-israel/",
           "/projects/hamedina-ar/"],
}
PAIR = {"hub": "/north-tel-aviv/", "rova-4": "/north-tel-aviv/rova-4/"}

BANNED = {
    "he": [r"אטלס", r"ממשק", r"(?<![א-ת])דמו(?![א-ת])", r"הדגמה", r"נקודות חמות", r"אינטראקטיב",
           r"רספונסיב", r"מובייל", r"סימולציה", r"טכנולוגי", r"תלת ממד", r"בקרוב", r"(?:כיוון|מחיר|נתון|מועד|מידע)\s+בבדיקה",
           r"ייעוץ חינם", r"הפלטפורמה",
           r"(?<![א-ת])המערכת(?![א-ת])", r"ויקיפדיה", r"גלובס", r"כלכליסט", r"דה ?מרקר", r"מאקו", r"מדלן",
           r"יד ?2", r"ביזפורטל", r"סותבי", r"מעריב", r"וויינט|ynet", r"מרכז הנדל[״\"]ן", r"Atlas"],
    "en": [r"\batlas\b", r"\binterface\b", r"\bdemo\b", r"\bhotspots?\b", r"\boverlay\b", r"\bengine\b", r"\bsimulation",
           r"\btechnology\b", r"\bplatform\b", r"\b3D\b", r"coming soon", r"free advice", r"free consultation", r"Wikipedia",
           r"Globes", r"Calcalist", r"TheMarker", r"\bMako\b", r"Madlan", r"Yad ?2", r"Bizportal", r"Sotheby", r"Maariv",
           r"\bYnet\b", r"nadlancenter", r"Merkaz HaNadlan", r"ice\.co\.il"],
    "fr": [r"\batlas\b", r"\binterface\b", r"\bdémo\b", r"\bmoteur\b", r"simulation", r"technologie", r"plateforme", r"\b3D\b",
           r"bientôt", r"conseil gratuit", r"consultation gratuite", r"Wikip[ée]dia", r"Globes", r"Calcalist", r"TheMarker",
           r"\bMako\b", r"Madlan", r"Yad ?2", r"Bizportal", r"Sotheby", r"Maariv", r"\bYnet\b", r"nadlancenter"],
    "ru": [r"атлас", r"интерфейс", r"\bдемо\b", r"движок", r"симуляц", r"технолог", r"платформ", r"\b3D\b", r"\bскоро\b",
           r"бесплатн\w* консультац", r"Википеди", r"Wikipedia", r"Globes", r"Глобс", r"Calcalist", r"Калькалист", r"\bMako\b",
           r"Madlan", r"Мадлан", r"Yad ?2", r"Яд ?2", r"Bizportal", r"Sotheby", r"Маарив", r"Maariv", r"\bYnet\b"],
    "ar": [r"أطلس", r"تجريبي", r"محر[ّ]?ك", r"محاكاة", r"تكنولوج", r"المنصة", r"ثلاثي الأبعاد", r"\b3D\b", r"قريباً",
           r"استشارة مجانية", r"ويكيبيديا", r"Wikipedia", r"Globes", r"غلوبس", r"Calcalist", r"كالكاليست", r"\bMako\b", r"Madlan",
           r"Yad ?2", r"Bizportal", r"Sotheby", r"معاريف", r"Maariv", r"\bYnet\b"],
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
SPACES = "\u00a0\u202f\u2009 "


def num_re(lang):
    """number tokens; a plain space joins thousands only in fr/ru (elsewhere only no-break / narrow / thin spaces do)"""
    sp = "\u00a0\u202f\u2009 " if lang in ("fr", "ru") else "\u00a0\u202f\u2009"
    return re.compile(
        r"(?<![0-9A-Za-z.,])("
        r"\d{1,2}[./]\d{1,2}[./]\d{4}"                                   # 23.5.2018, 23/05/2018
        r"|\d{1,2}\.\d{4}(?![0-9])"                                     # 3.2026
        r"|\d{1,3}(?:(?:,\d{3})+|(?:\.\d{3}){2,}|(?:[" + sp + r"]\d{3})+)(?:[.,]\d+)?(?![0-9])"  # 6,835,800 / 6 835 800
        r"|\d+(?:[.,]\d+)?"                                              # 4.5 / 30,7 / 2026
        r")(?![0-9])")


# ------------------------------------------------------------------ text helpers
def visible_text(h):
    h = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    return H.unescape(re.sub(r"<[^>]+>", " ", h))


def strip_tags(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def canon(s):
    """'6,835,800' / '17.0' / '4.5' (claim style) -> canonical number string"""
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
    """a number token as written in the article -> (kind, canonical) ; kind 'date' or 'num'"""
    t = tok.translate(AR_DIGITS).replace("٬", ",").replace("٫", ".")
    if is_date(t) and not re.fullmatch(r"\d{1,3}\.\d{3}", t):
        return "date", date_canon(t)
    for sp in SPACES:
        t = t.replace(sp, "")
    if re.fullmatch(r"\d{1,3}(\.\d{3}){2,}", t):            # 6.835.800
        t = t.replace(".", "")
    if lang in ("fr", "ru"):
        if re.fullmatch(r"\d+,\d+", t) and not re.fullmatch(r"\d{1,3}(,\d{3})+", t):
            t = t.replace(",", ".")
        elif re.fullmatch(r"\d+,\d+", t):                  # 6,835 in fr is ambiguous: keep both readings
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
            except Exception as e:  # network down: fall back
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
    dashes = vis.count("—") + vis.count("–") + meta.get("title", "").count("—") + meta.get("title", "").count("–")
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
    # 5. shortcodes
    sc = re.findall(r"\[/?[a-z_]+(?:\s[^\]]*)?\]", vis)
    sc = [s for s in sc if re.match(r"\[/?(nadlan|nl|vc_|et_|elementor|caption|gallery|embed)", s)]
    if sc:
        errs.append("shortcode(s): %s" % sc)
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
    # 7. meta lengths
    if meta.get("title") and len(meta["title"]) > 60:
        errs.append("SEO title is %d characters (max 60)" % len(meta["title"]))
    if meta.get("description") and len(meta["description"]) > 155:
        errs.append("SEO description is %d characters (max 155)" % len(meta["description"]))
    # warnings
    if lang != "he":
        heb = re.findall(r"[א-ת]+(?:[\s״׳\"'][א-ת]+)*", vis)
        if heb:
            warns.append("Hebrew left in the text (%d runs; names in parentheses are fine): %s" % (len(heb), heb[:6]))
    wc = word_count(vis, lang)
    packet_path = os.path.join(HERE, "packets", "%s-%s.json" % (page, lang))
    if lang != "he" and os.path.exists(packet_path):
        pk = json.load(io.open(packet_path, encoding="utf-8"))
        lo, hi = pk["words_total_range"]
        if not lo <= wc <= hi:
            warns.append("net words %d outside the packet's range %d-%d" % (wc, lo, hi))
        n_h2 = len([x for x in own if x[0] == "h2"])
        if n_h2 != pk["h2_count"]:
            warns.append("H2 count %d, the Hebrew source has %d" % (n_h2, pk["h2_count"]))
    res = {"page": page, "lang": lang, "words": wc, "numbers": len(rows), "unmatched": unmatched, "errors": errs,
           "warnings": warns, "banned": bans, "soft": soft, "dupes": dupes, "links": links, "comparators": list(comps),
           "comparator_source": comp_src, "rows": rows}
    if not quiet:
        report(res)
    return res


def report(r):
    print("== %s/%s | net words %d | numbers %d, unmatched %d | errors %d | warnings %d | comparators %d (%s)"
          % (r["page"], r["lang"], r["words"], r["numbers"], len(r["unmatched"]), len(r["errors"]), len(r["warnings"]),
             len(r["comparators"]), r["comparator_source"]))
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
          "- Net words: %d. Numbers: %d, unmatched: %d." % (r["words"], r["numbers"], len(r["unmatched"])),
          "- Heading comparators (%s): %s\n" % (r["comparator_source"], ", ".join(r["comparators"]))]
    md += ["## Errors\n"] + ["- %s" % e for e in r["errors"]] + ["", "## Every number\n", "| # | number | claims | context |", "|---|---|---|---|"]
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


# ------------------------------------------------------------------ self-test on the Hebrew sources
def hebrew_sources(live=False):
    """(hub article html after align-edits.json applied in memory, its meta) and (Rova 4 article html, meta)"""
    if live:
        st, js = fetch(SITE + "/wp-json/wp/v2/pages/4866?_fields=content,title,yoast_head_json")
        hub = json.loads(js)
        st, js = fetch(SITE + "/wp-json/wp/v2/pages/8218?_fields=content,title,yoast_head_json")
        rova = json.loads(js)
    else:
        hub = json.load(io.open(os.path.join(HERE, "source", "hub-4866-rest.json"), encoding="utf-8"))
        rova = json.load(io.open(os.path.join(HERE, "source", "rova-4-8218-rest.json"), encoding="utf-8"))
    c = hub["content"]["rendered"]
    edits = json.load(io.open(os.path.join(HERE, "align-edits.json"), encoding="utf-8"))["edits"]
    applied = 0
    for e in edits:
        n = c.count(e["old"])
        if n != e.get("expect_matches", 1):
            print("  SELFTEST: edit %d matches %d times in the hub (expected %d)" % (e["n"], n, e.get("expect_matches", 1)))
            continue
        c = c.replace(e["old"], e["new"])
        applied += 1
    print("  hub: %d of %d align edits applied in memory" % (applied, len(edits)))
    hub_h1 = H.unescape(hub["title"]["rendered"])
    hub_html = "<h1>%s</h1>\n%s" % (hub_h1, re.sub(r"<(script|style|svg)\b.*?</\1>", "", c, flags=re.S))
    hub_meta = {"title": (hub.get("yoast_head_json") or {}).get("title", ""),
                "description": (hub.get("yoast_head_json") or {}).get("description", "")}
    r = rova["content"]["rendered"]
    a, b = r.find("<p><style"), r.find('<h2 id="איפה-נמצא')
    if a > 0 and b > a:   # the PriceGuide and AreaMap components sit in one <p> between the lead and the first H2
        r = r[:a] + r[b:]
    r = re.sub(r"<(script|style|svg)\b.*?</\1>", "", r, flags=re.S)
    rova_meta = {"title": (rova.get("yoast_head_json") or {}).get("title", ""),
                 "description": (rova.get("yoast_head_json") or {}).get("description", "")}
    return (hub_html, hub_meta), (r, rova_meta)


def selftest(live=False, offline=False):
    (hub_html, hub_meta), (rova_html, rova_meta) = hebrew_sources(live)
    ok = True
    for page, h, meta in (("hub", hub_html, hub_meta), ("rova-4", rova_html, rova_meta)):
        # the Hebrew pages link to Hebrew pages only; links.json "he" lists them
        res = run(h, page, "he", meta=meta, offline=offline, link_get=not offline)
        ok = ok and not res["errors"]
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("article", nargs="?")
    ap.add_argument("--page", choices=("hub", "rova-4"))
    ap.add_argument("--lang", choices=LANGS)
    ap.add_argument("--meta")
    ap.add_argument("--peer")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--no-link-get", action="store_true")
    ap.add_argument("--write")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--live", action="store_true")
    a = ap.parse_args()
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
