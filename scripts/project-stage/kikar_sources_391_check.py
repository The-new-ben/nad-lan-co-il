# -*- coding: utf-8 -*-
"""Verify the source-free Kikar posts: (a) source names in visible text, (b) numbers kept, (c) structure, (d) word counts.
old = git HEAD, pre = the working copy before this edit (scratchpad/kikar/pre), new = the working copy now."""
import io, os, re, sys, subprocess, collections
from html.parser import HTMLParser
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
REL = "docs/research/2026-09-30-kikar-hamedina/post-{}.html"
PRE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pre", "post-{}.html")
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "area", "col", "embed", "param", "track"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.chunks, self.tags, self.stack, self.errors = [], collections.Counter(), [], []
        self.h3, self.in_h3, self.cur, self.in_faq = [], False, "", False
        self.wa, self.in_wa = [], False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags[tag] += 1
        if tag not in VOID:
            self.stack.append(tag)
        if tag == "section":
            self.in_faq = a.get("id") == "nlws-faq"
        if tag == "h3" and self.in_faq:
            self.in_h3, self.cur = True, ""
        if tag == "a" and "nlws-wa" in (a.get("class") or ""):
            self.in_wa, self.cur_wa = True, ""

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unexpected </{tag}>, open: {self.stack[-3:]}")
        else:
            self.stack.pop()
        if tag == "h3" and self.in_h3:
            self.h3.append(self.cur); self.in_h3 = False
        if tag == "a" and self.in_wa:
            self.wa.append(self.cur_wa); self.in_wa = False

    def handle_data(self, d):
        self.chunks.append(d)
        if self.in_h3:
            self.cur += d
        if self.in_wa:
            self.cur_wa += d


def parse(html):
    p = P(); p.feed(html); p.close()
    if p.stack:
        p.errors.append(f"unclosed at end: {p.stack}")
    p.text = " ".join(p.chunks)
    return p


NAMES = ["גלובס", "מאקו", "ביזפורטל", "כלכליסט", "ויקיפדיה", "דה מרקר", "מדלן", "סותבי", "Globes", "Mako", "N12", "Bizportal", "Calcalist",
         "Wikipedia", "TheMarker", "Madlan", "Sotheby", "ynet", r"\bice\b", "Israel Property Hub", "Anglo-Saxon", "Homepic",
         "לפי רישום", "נקרא ב-", "read 30.9", "consulté", "просмотрено", "اطُّلع",
         # extra names/phrases this edit also targeted (localised forms and other credits)
         "Wikipédia", "Википеди", "ويكيبيديا", "Jerusalem Post", "Project TLV", "Alum Eshet", "אלום אשת", "ילקוט", "Yalkut", "Yalkout",
         "Ялкут", "يلكوت", "OpenStreetMap", "Mapbox", "findplace", "וואלה", "Walla", "Yad2", "יד2", "אנגלו",
         "רישום אתר הבנייה", "building-site record", "registre des chantiers", "реестр стройплощадок", "سجل مواقع البناء",
         "open GIS", "геоданн", "données géographiques", "המידע הגאוגרפי", "البيانات الجغرافية",
         "משרד התחבורה", "Ministry of Transport", "ministère des Transports", "Министерство транспорта", "وزارة المواصلات",
         "Official Gazette", "Journal officiel", "Официальный вестник", "الجريدة الرسمية",
         "administration fiscale", "Налоговое управление", "سلطة الضرائب",
         # the word "source(s)" itself
         "מקור", r"\bsources?\b", r"\bsources?\b", "источник", "مصدر", "مصادر"]
NUM = re.compile(r"\d{1,3}(?:[\u00a0\u202f]\d{3})+(?!\d)|\d+(?:[.,/\-]\d+)*")


def ctx(text, tok, w=45):
    i = text.find(tok)
    return text[max(0, i - w):i + len(tok) + w].replace("\n", " ") if i >= 0 else ""


def sections(html):
    return re.findall(r'<section[^>]*\bid="([^"]+)"', html)


def block(html, sid):
    i = html.index(f'id="{sid}"'); i = html.rfind("<section", 0, i)
    return html[i:html.index("</section>", i)]


fails = 0
for L in ("he", "en", "fr", "ru", "ar"):
    old_html = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + REL.format(L)], capture_output=True).stdout.decode("utf-8")
    pre_html = io.open(PRE.format(L), encoding="utf-8", newline="").read()
    new_html = io.open(os.path.join(REPO, REL.format(L)), encoding="utf-8", newline="").read()
    o, n = parse(old_html), parse(new_html)
    print(f"\n=================== {L} ===================")
    # (a)
    print("(a) source names in visible text, HEAD -> now:")
    row = []
    for w in dict.fromkeys(NAMES):
        rx = re.compile(w if w.startswith("\\") else re.escape(w), re.I if w.startswith("\\b") else 0)
        a, b = len(rx.findall(o.text)), len(rx.findall(n.text))
        if a or b:
            row.append(f"{w.replace(chr(92) + 'b', '')}: {a}->{b}")
            if b:
                m = rx.search(n.text)
                row[-1] += f"  [LEFT: ...{n.text[max(0, m.start() - 50):m.end() + 50]}...]"
    print("   " + "\n   ".join(row) if row else "   (none in either)")
    tot_o = sum(len(re.findall(w if w.startswith("\\") else re.escape(w), o.text)) for w in dict.fromkeys(NAMES[:28]))
    tot_n = sum(len(re.findall(w if w.startswith("\\") else re.escape(w), n.text)) for w in dict.fromkeys(NAMES[:28]))
    print(f"   TOTAL of the 28 listed names/phrases: {tot_o} -> {tot_n}")
    # (b)
    on, nn = collections.Counter(NUM.findall(o.text)), collections.Counter(NUM.findall(n.text))
    gone = sorted(set(on) - set(nn))
    added = sorted(set(nn) - set(on))
    print(f"(b) distinct numbers: HEAD {len(on)}, now {len(nn)}; disappeared ({len(gone)}):")
    for t in gone:
        print(f"   {t!r} x{on[t]}  e.g. ...{ctx(o.text, t)}...")
    print(f"   numbers new in the text (should be none): {added}")
    dropped = {t: (on[t], nn[t]) for t in on if t in nn and nn[t] < on[t]}
    print(f"   numbers still present but fewer times: {dropped}")
    # (c)
    ok = True
    s_o, s_n = sections(old_html), sections(new_html)
    c1 = s_o == s_n
    c2 = (o.tags["h2"], o.tags["h3"]) == (n.tags["h2"], n.tags["h3"])
    c3 = o.h3 == n.h3
    c4 = new_html.count("\u2014") <= old_html.count("\u2014") and new_html.count("\u2013") <= old_html.count("\u2013")
    tag_diff = {t: (o.tags[t], n.tags[t]) for t in set(o.tags) | set(n.tags) if o.tags[t] != n.tags[t]}
    c5 = all(t in ("small", "a") and n.tags[t] < o.tags[t] for t in tag_diff)
    c6 = not n.errors
    c7 = old_html.count("\n") == new_html.count("\n") and "\r" not in new_html
    c8 = o.wa == n.wa
    first_p = lambda h: h[:h.index("</p>") + 4]
    c9 = first_p(pre_html) == first_p(new_html) and all(block(pre_html, s) == block(new_html, s) for s in ("nlws-prices", "nlws-sale"))
    c10 = (L != "ru") or ("Все цены здесь: опубликованные открытые данные." in new_html)
    c11 = "<small>" not in new_html
    for name, c in [("same section ids in order", c1), ("same h2/h3 counts", c2), ("same FAQ h3 questions", c3),
                    ("no em/en dash added", c4), ("tag counts equal except fewer <small>/<a>", c5), ("tags balanced", c6),
                    ("same line count, LF only", c7), ("WhatsApp link texts unchanged", c8),
                    ("lead + nlws-prices + nlws-sale byte-identical to pre-edit", c9), ("ru uncommitted fix kept", c10), ("no <small> left", c11)]:
        ok &= c
        print(f"(c) {'PASS' if c else 'FAIL'}  {name}")
    print(f"    sections: {s_n}")
    print(f"    h2/h3: {n.tags['h2']}/{n.tags['h3']}; FAQ questions: {len(n.h3)}; tag changes: {tag_diff}; parse errors: {n.errors}")
    print(f"    em dashes {old_html.count(chr(0x2014))}->{new_html.count(chr(0x2014))}, en dashes {old_html.count(chr(0x2013))}->{new_html.count(chr(0x2013))}; lines {old_html.count(chr(10))}->{new_html.count(chr(10))}")
    fails += not ok
    # (d)
    wo, wn = len(o.text.split()), len(n.text.split())
    print(f"(d) visible words: HEAD {wo} -> now {wn} ({wn - wo:+d}, {100 * (wn - wo) / wo:+.1f}%)")
print("\nSTRUCTURE:", "ALL PASS" if not fails else f"{fails} file(s) FAIL")
