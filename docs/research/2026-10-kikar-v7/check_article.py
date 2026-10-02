# -*- coding: utf-8 -*-
"""V7: the gates for one ChatGPT article, before it may replace a Kikar Hamedina post.

    python docs/research/2026-10-kikar-v7/check_article.py he [--write]

1. The HTML contract (the lead first, the 14 sections in order with their ids, allowed tags only, the FAQ as h3 + one p, the
   WhatsApp link text and count, internal links only from links.json and each once, the closing marker).
2. The language gate: the banned words of the brief, the project's blacklist (language-dna), no long or en dash, no "developer".
3. The fact check (C1): every number in the visible text is matched to the claims that allow it (claims.py). A number that no
   claim allows is UNMATCHED and must be read by a person. With --write, fact-check-<lang>.md is written.
4. The net word count (wordcount.js, Intl.Segmenter): at least 5,000 without the lead.
Exit code 1 when a hard gate fails (contract, banned word, dash, words < 5,000). UNMATCHED numbers are reported, not fatal: the
reviewer decides each one and records the decision in the fact-check file.
"""
import html as H, io, json, os, re, subprocess, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from claims import CLAIMS  # noqa: E402

ORDER = ["nlws-facts", "nlws-choose", "nlws-homes", "nlws-life", "nlws-prices", "nlws-costs", "nlws-buy", "nlws-sale", "nlws-when",
         "nlws-timeline", "nlws-park", "nlws-square", "nlws-transport", "nlws-faq"]
ALLOWED_TAGS = {"p", "h2", "h3", "section", "table", "thead", "tbody", "tr", "th", "td", "ul", "ol", "li", "b", "a", "small", "div"}
FAQ_H2 = {"he": "שאלות נפוצות", "en": "Frequently asked questions", "fr": "Questions fréquentes", "ru": "Частые вопросы",
          "ar": "أسئلة شائعة"}
WA = {"he": "לקבלת פרטים נוספים בוואטסאפ", "en": "More details on WhatsApp", "fr": "Plus de détails sur WhatsApp",
      "ru": "Подробнее в WhatsApp", "ar": "لمزيد من التفاصيل عبر واتساب"}
# hard bans (whole-word where it matters); the brief's longer list is reviewed by reading
BANNED = {
    "he": [r"יזם", r"יזמ", r"ממשק", r"\bדמו\b", r"הדגמה", r"מנגנון", r"נקודות חמות", r"אינטראקטיב", r"רספונסיב", r"מובייל",
           r"סימולציה", r"טכנולוגי", r"אטלס", r"תלת ממד", r"בקרוב", r"בבדיקה", r"ייעוץ חינם", r"הפלטפורמה", r"המערכת",
           r"חשוב להבין", r"חשוב לזכור", r"ראוי לציין", r"ללא ספק", r"לסיכום", r"מהווה", r"יש לציין", r"דגל אדום", r"מלכודת",
           r"היזהרו", r"ויקיפדיה", r"גלובס", r"כלכליסט", r"דה מרקר", r"מאקו", r"מדלן", r"יד2", r"ביזפורטל", r"סותבי"],
    "en": [r"\bdeveloper", r"\binterface\b", r"\bdemo\b", r"\bhotspot", r"\boverlay\b", r"\bengine\b", r"\bsimulation",
           r"\btechnology\b", r"\bplatform\b", r"\b3D\b", r"coming soon", r"free advice", r"\bdelve", r"\bnestled\b", r"\bboasts?\b",
           r"testament to", r"red flag", r"\bbeware\b", r"Wikipedia", r"Globes", r"Calcalist", r"TheMarker", r"Mako", r"Madlan",
           r"Yad2", r"Bizportal", r"Sotheby"],
    "fr": [r"promoteur", r"\binterface\b", r"\bdémo\b", r"\bmoteur\b", r"simulation", r"technologie", r"plateforme", r"\b3D\b",
           r"bientôt", r"conseil gratuit", r"force est de constater", r"véritable écrin", r"\bniché", r"Wikipédia", r"Wikipedia",
           r"Globes", r"Calcalist", r"TheMarker", r"Mako", r"Madlan", r"Yad2", r"Sotheby"],
    "ru": [r"застройщик", r"девелопер", r"интерфейс", r"\bдемо\b", r"движок", r"симуляц", r"технолог", r"платформ", r"\b3D\b",
           r"\bскоро\b", r"бесплатн\w* консультац", r"стоит отметить", r"важно понимать", r"в заключение", r"уникальный шанс",
           r"Википеди", r"Wikipedia", r"Globes", r"Глобс", r"Calcalist", r"Mako", r"Madlan", r"Мадлан", r"Yad2", r"Sotheby"],
    "ar": [r"مطو[ّ]?ر", r"تجريبي", r"محر[ّ]?ك", r"محاكاة", r"تكنولوج", r"المنصة", r"ثلاثي الأبعاد", r"\b3D\b", r"قريباً",
           r"استشارة مجانية", r"تجدر الإشارة", r"في الختام", r"لا شك", r"ويكيبيديا", r"Wikipedia", r"Globes", r"غلوبس",
           r"Calcalist", r"Mako", r"Madlan", r"Yad2", r"Sotheby"],
}
# conversions the briefs themselves give (units lines), allowed without a claim
EXTRA_OK = {"en": {"1615", "10", "1000", "4"}, "fr": {"1000", "4"}, "ru": {"1000", "4"}, "he": {"1000"}, "ar": {"1000"}}
AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def norm_num(tok, lang):
    """a number token as written -> canonical string(s) (no thousands separators, decimal point)"""
    t = tok.translate(AR_DIGITS).replace(" ", " ").replace(" ", " ").replace("٬", ",").replace("٫", ".")
    if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", t) or re.fullmatch(r"\d{1,2}\.\d{4}", t):  # a date
        parts = [str(int(x)) for x in t.split(".")]
        return [".".join(parts)] + parts
    if lang in ("fr", "ru"):
        t = t.replace(" ", "")
        if re.fullmatch(r"\d+,\d+", t):
            t = t.replace(",", ".")
        t = t.replace(",", "")
    else:
        t = t.replace(" ", "")
        if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", t):
            t = t.replace(",", "")
        elif re.fullmatch(r"\d+,\d+", t):  # a comma decimal in he/en/ar would be a mistake: keep both readings
            return [t.replace(",", "."), t.replace(",", "")]
    try:
        f = float(t)
        s = ("%f" % f).rstrip("0").rstrip(".")
        return [s]
    except ValueError:
        return [t]


def claim_numbers():
    idx = {}
    for c in CLAIMS:
        for n in c["numbers"]:
            forms = set()
            for lang in ("he", "fr"):
                forms.update(norm_num(n, lang))
            for f in forms:
                idx.setdefault(f, set()).add(c["claim_id"])
    return idx


def visible_text(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S)
    return H.unescape(re.sub(r"<[^>]+>", " ", h))


def contract(h, lang, links):
    errs, warns = [], []
    body = h.strip()
    if not body.startswith("<p>"):
        errs.append("the article does not open with the lead <p>")
    lead = re.match(r"<p>(.*?)</p>", body, re.S)
    if lead and len(visible_text(lead.group(1))) < 100:
        errs.append("the lead is shorter than 100 characters")
    ids = re.findall(r'<section class="nlws(?: nlws-faq)?" id="([^"]+)">', body)
    if ids != ORDER:
        errs.append("sections/ids/order differ: %s" % ids)
    if len(re.findall(r"<section\b", body)) != len(ORDER):
        errs.append("section count %d" % len(re.findall(r"<section\b", body)))
    tags = set(t.lower() for t in re.findall(r"</?([a-zA-Z0-9]+)", body))
    bad = tags - ALLOWED_TAGS
    if bad:
        errs.append("tags not allowed: %s" % sorted(bad))
    if re.search(r"\sstyle=", body):
        errs.append("inline style")
    divs = re.findall(r"<div[^>]*>", body)
    if divs != ['<div class="nadlan-project-article">'] or not body.endswith('<div class="nadlan-project-article"></div>'):
        errs.append("the closing marker div is missing or other divs exist: %s" % divs)
    if "—" in body or "–" in body:
        errs.append("long or en dash present (%d)" % (body.count("—") + body.count("–")))
    wa = re.findall(r'<a class="nlws-wa" href="#nlws-wa">(.*?)</a>', body)
    if len(wa) != 2 or any(w != WA[lang] for w in wa):
        errs.append("WhatsApp links: %s" % wa)
    hrefs = [x for x in re.findall(r'href="([^"]+)"', body) if not x.startswith("#")]
    off = [x for x in hrefs if x not in links]
    if off:
        errs.append("links not in the list: %s" % off)
    dup = sorted(set(x for x in hrefs if hrefs.count(x) > 1))
    if dup:
        warns.append("links used twice: %s" % dup)
    if not 8 <= len(hrefs) <= 16:
        warns.append("internal links: %d (asked 10-14)" % len(hrefs))
    faq = body[body.find('id="nlws-faq"'):]
    if "<h2>%s</h2>" % FAQ_H2[lang] not in faq:
        errs.append("the FAQ h2 is not exactly %r" % FAQ_H2[lang])
    pairs = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", faq, re.S)
    h3s = re.findall(r"<h3>", faq)
    if len(pairs) != len(h3s) or len(pairs) < 10:
        errs.append("FAQ pairs %d of %d h3" % (len(pairs), len(h3s)))
    tl = body[body.find('id="nlws-timeline"'):body.find('id="nlws-park"')]
    if 'class="nlws-time"' not in tl or 'class="is-now"' not in tl:
        errs.append("timeline list or its is-now item missing")
    if "<h1" in body:
        errs.append("an h1 inside the article")
    return errs, warns


def banned(h, lang):
    t = visible_text(h)
    hits = []
    for pat in BANNED[lang]:
        for m in re.finditer(pat, t, flags=re.I):
            hits.append((pat, t[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")))
    return hits


def fact_check(h, lang):
    idx = claim_numbers()
    t = visible_text(h)
    rows = []
    for m in re.finditer(r"(?<![\w.])(\d{1,3}(?:[   ,.]\d{3})+(?:[.,]\d+)?|\d{1,2}\.\d{1,2}\.\d{4}|\d{1,2}\.\d{4}|\d+(?:[.,]\d+)?)(?![\w])",
                         t.translate(AR_DIGITS)):
        tok = m.group(1).strip()
        forms = norm_num(tok, lang)
        ids = set()
        for f in forms:
            ids |= idx.get(f, set())
        ok = bool(ids) or any(f in EXTRA_OK.get(lang, set()) for f in forms)
        ctx = t[max(0, m.start() - 60):m.end() + 50].replace("\n", " ")
        ctx = re.sub(r"\s+", " ", ctx).strip()
        rows.append({"num": tok, "norm": forms[0], "claims": sorted(ids), "ok": ok, "ctx": ctx})
    return rows


def words(path, lang):
    out = subprocess.run(["node", os.path.join(HERE, "wordcount.js"), path, lang], capture_output=True, text=True, encoding="utf-8")
    return json.loads(out.stdout)


def main():
    lang = sys.argv[1]
    write = "--write" in sys.argv
    path = os.path.join(HERE, "article-%s.html" % lang)
    h = io.open(path, encoding="utf-8").read().strip()
    links = json.load(io.open(os.path.join(HERE, "links.json"), encoding="utf-8"))[lang]
    errs, warns = contract(h, lang, links)
    bans = banned(h, lang)
    rows = fact_check(h, lang)
    wc = words(path, lang)
    unmatched = [r for r in rows if not r["ok"]]
    print("== %s | words %d (without the lead %d) | numbers %d, unmatched %d | contract errors %d | banned %d"
          % (lang, wc["words_all"], wc["words_without_lead"], len(rows), len(unmatched), len(errs), len(bans)))
    for e in errs:
        print("  CONTRACT:", e)
    for w in warns:
        print("  warn:", w)
    for p, c in bans:
        print("  BANNED %s: …%s…" % (p, c))
    for r in unmatched:
        print("  UNMATCHED %s: …%s…" % (r["num"], r["ctx"]))
    print("  sections:", wc["sections"])
    if write:
        by = {c["claim_id"]: c for c in CLAIMS}
        used = sorted(set(i for r in rows for i in r["claims"]))
        md = ["# Fact check, %s (V7, Kikar Hamedina)\n" % lang,
              "- Article: `article-%s.html`. Claims: `claims.py` (sources there; the article names none)." % lang,
              "- Net words (Intl.Segmenter, isWordLike): **%d** in all, **%d** without the lead paragraph." % (wc["words_all"], wc["words_without_lead"]),
              "- Numbers in the visible text: %d. Matched to a claim: %d. Unmatched: %d (each one decided below)." % (len(rows), len(rows) - len(unmatched), len(unmatched)),
              "- Contract errors: %d. Banned-word hits: %d.\n" % (len(errs), len(bans)),
              "## Every number, with the claims that allow it\n", "| # | Number | Claims | In context |", "|---|---|---|---|"]
        for k, r in enumerate(rows, 1):
            md.append("| %d | %s | %s | %s |" % (k, r["num"], ", ".join(r["claims"]) or ("unit conversion" if r["ok"] else "**UNMATCHED**"),
                                                r["ctx"].replace("|", "/")))
        md += ["\n## The claims used, with their sources\n", "| Claim | Statement | Source | Date |", "|---|---|---|---|"]
        for i in used:
            c = by[i]
            md.append("| %s | %s | %s | %s |" % (i, c["claim"].replace("|", "/"), c["source"].replace("|", "/"), c["date"]))
        md.append("\n## Reviewer's decisions on unmatched numbers and on claims read in the text\n\n(filled after reading)\n")
        io.open(os.path.join(HERE, "fact-check-%s.md" % lang), "w", encoding="utf-8").write("\n".join(md) + "\n")
        print("  wrote fact-check-%s.md" % lang)
    hard = errs or bans or wc["words_without_lead"] < 5000
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
