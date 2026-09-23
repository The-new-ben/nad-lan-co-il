# -*- coding: utf-8 -*-
"""Live checks of the test broker's eight pages: status, one H1, hreflang cluster, language links, banned words, JSON-LD."""
import html as H, io, json, re, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
urls = {
    "listing he": "https://nad-lan.co.il/properties/florentin-4-rooms-for-sale/",
    "listing en": "https://nad-lan.co.il/en/brokers/system-check/florentin-4-rooms-for-sale/",
    "listing ru": "https://nad-lan.co.il/ru/brokers/system-check/florentin-4-rooms-for-sale/",
    "listing fr": "https://nad-lan.co.il/fr/brokers/system-check/florentin-4-rooms-for-sale/",
    "site he": "https://nad-lan.co.il/brokers/system-check/",
    "site en": "https://nad-lan.co.il/en/brokers/system-check/",
    "site ru": "https://nad-lan.co.il/ru/brokers/system-check/",
    "site fr": "https://nad-lan.co.il/fr/brokers/system-check/",
}
ban = {"he": ["הזדמנות", "חלום", "מושלם", "מדהים", "—", "!"], "en": ["dream", "stunning", "breathtaking", "—", "!"],
       "ru": ["уникальн", "мечт", "идеальн", "потрясающ", "—", "!"], "fr": ["unique", "rêve", "parfait", "magnifique", "—", "!"]}
for k, u in urls.items():
    lang = k.split()[-1]
    try:
        r = urllib.request.urlopen(urllib.request.Request(u + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0 Chrome/128"}), timeout=90)
        t, st = r.read().decode("utf-8", "replace"), r.status
    except urllib.error.HTTPError as e:
        print(k, e.code)
        continue
    head, body = t.split("<body", 1)
    hl = re.findall(r'<link rel="alternate" hreflang="([a-zA-Z-]+)" href="([^"]+)"', head)
    main = body
    txt = H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", main, flags=re.S)))
    art = re.search(r'<article class="(nlx|nlb)".*?</article>', body, re.S)
    atxt = H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", art.group(0) if art else "", flags=re.S)))
    bad = {w: atxt.count(w) for w in ban[lang] if atxt.count(w)}
    html_lang = re.search(r"<html[^>]*\blang=\"([^\"]+)\"", t)
    title = re.search(r"<title>(.*?)</title>", t, re.S)
    langlinks = re.findall(r'class="(?:nlx-lang[^"]*|is-lang)" href="[^"]+" hreflang="([a-z]{2})"', body)
    print(f"{k:11s} {st} h1={len(re.findall(r'<h1[ >]', body))} html_lang={html_lang.group(1) if html_lang else '?'} hreflang={sorted(set(x for x, _ in hl))} "
          f"links={langlinks} jsonld={body.count('application/ld+json')} banned={bad or 'none'} licence={atxt.count('0000001')}")
    print(f"            title: {H.unescape(title.group(1)).strip() if title else ''}")
    if k.startswith("listing"):
        m = re.search(r'class="nlx-title">(.*?)</h[12]>', body, re.S)
        d = re.search(r'class="nlx-dek">(.*?)</p>', body, re.S)
        print("            H:", H.unescape(re.sub(r"<[^>]+>", "", m.group(1))) if m else "", "|", H.unescape(re.sub(r"<[^>]+>", "", d.group(1))) if d else "")
