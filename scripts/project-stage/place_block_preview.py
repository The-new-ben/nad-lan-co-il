# -*- coding: utf-8 -*-
"""HAD-787 board 24, a look BEFORE the release: the place block's HTML (as inc/pro-forum-place.php prints it) is put at the end of
the article of the LIVE page inside a local browser only, with the live forum.css and the repo's place.css. Nothing is written
to the site.   python scripts/project-stage/place_block_preview.py <out dir>"""
import os, sys, time
from playwright.sync_api import sync_playwright

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSS = open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "proforum", "place.css"), encoding="utf-8").read()
BASE = "https://nad-lan.co.il"
PLACES = [("sde-dov", "שדה דב", "/sde-dov/"), ("hamedina", "כיכר המדינה", "/projects/hamedina/")]


def block(key, label, rows):
    h = '<section class="nlf nlf-win nlfpl" dir="rtl" aria-labelledby="nlfpl-%s-h" data-pro="0" data-pro-name="" data-cat="general" data-nlfpl="%s"><div class="nlfpl-box">' % (key, key)
    h += '<div class="nlfpl-top"><span class="nlfpl-kick">מהפורום של נדל"ן</span>' + ('<span class="nlfpl-live"><i aria-hidden="true"></i>2 דיונים פעילים השבוע</span>' if rows else '') + '</div>'
    h += '<h2 class="nlfpl-h" id="nlfpl-%s-h">שאלות של קונים על %s</h2>' % (key, label)
    h += '<form class="nlfpl-ask" data-nlf-ask novalidate><label class="nlfpl-sr" for="nlfpl-%s-q">מה תרצו לשאול על %s?</label><div class="nlfpl-askrow"><input id="nlfpl-%s-q" type="text" name="q" maxlength="140" autocomplete="off" placeholder="מה תרצו לשאול על %s?"><button type="submit">לשאול</button></div></form>' % (key, label, key, label)
    if rows:
        h += '<div class="nlfpl-list">'
        for n, tint, title, meta in (("2", "background:#E6F0F4;color:#1F4B5C", "שורת דוגמה לבדיקת המראה בלבד, לא תוכן אמיתי", "2 תשובות · לפני שעה"), ("0", "background:#EEF2F4;color:#3A4650", "שורת דוגמה שנייה, ארוכה יותר, כדי לראות שבירת שורות בטלפון", "מחכה לתשובה ראשונה")):
            h += '<a class="nlfpl-row" href="#"><span class="nlfpl-num" style="%s" aria-hidden="true">%s</span><span class="nlfpl-rt"><span class="nlfpl-rtitle">%s</span><span class="nlfpl-rmeta">%s</span></span></a>' % (tint, n, title, meta)
        h += '</div><a class="nlfpl-all" href="#">לכל השאלות על %s</a>' % label
    else:
        h += '<p class="nlfpl-none">עוד אין שאלות. שאלו ראשונים.</p>'
    return h + '</div></section>'


with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    for key, label, path in PLACES:
        for name, mobile in (("phone", True), ("desktop", False)):
            c = br.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1280, "height": 900}, locale="he-IL", is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
            g = c.new_page(); g.goto(BASE + path, wait_until="networkidle", timeout=120000); g.wait_for_timeout(1500)
            g.add_style_tag(url="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Rubik:wght@500;700;800&display=swap")
            g.add_style_tag(url=BASE + "/wp-content/plugins/nadlan-config/assets/proforum/forum.css")
            g.add_style_tag(content=CSS)
            for rows in (False, True):
                info = g.evaluate("""(html) => { document.querySelectorAll('.nlfpl').forEach(e => e.remove());
                    const all = [...document.querySelectorAll('.entry-content')]; const host = all[all.length - 1]; host.insertAdjacentHTML('beforeend', html);
                    const b = host.querySelector('.nlfpl-box'), r = b.getBoundingClientRect(), hr = host.getBoundingClientRect(), h2 = b.querySelector('h2'), btn = b.querySelector('button'), inp = b.querySelector('input');
                    const cs = (e) => getComputedStyle(e);
                    return { hosts: all.length, w: Math.round(r.width), hostW: Math.round(hr.width), h: Math.round(r.height), top: Math.round(r.top + scrollY), page: document.documentElement.scrollHeight, pageW: document.documentElement.scrollWidth, vw: innerWidth,
                             h2: cs(h2).fontFamily.split(',')[0] + ' ' + cs(h2).fontSize + ' ' + cs(h2).color, btn: cs(btn).backgroundColor + ' ' + cs(btn).color + ' h' + Math.round(btn.getBoundingClientRect().height), inp: 'h' + Math.round(inp.getBoundingClientRect().height) + ' ' + cs(inp).fontSize, after: (b.nextElementSibling || {}).className || '(last)' }; }""", block(key, label, rows))
                print(key, name, "rows" if rows else "empty", info)
                g.evaluate("() => { const r = document.querySelector('.nlfpl').getBoundingClientRect(); window.scrollBy(0, r.top - 140); }"); g.wait_for_timeout(2500)
                g.screenshot(path=os.path.join(OUT, "pv-%s-%s-%s.png" % (key, name, "rows" if rows else "empty")))
            c.close()
    br.close()
