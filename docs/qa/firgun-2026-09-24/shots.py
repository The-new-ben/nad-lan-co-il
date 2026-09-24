# -*- coding: utf-8 -*-
import sys, time, json
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
ST = json.load(open(r"C:/Users/777/nad-lan/nad-lan-co-il/docs/qa/firgun-2026-09-24/selftest-251.json", encoding="utf-8"))
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for W, H, tag in ((1440, 900, "desktop"), (390, 844, "mobile")):
        pg = b.new_page(viewport={"width": W, "height": H}, is_mobile=W < 700, has_touch=W < 700)
        # 1. the live explainer
        pg.goto("https://nad-lan.co.il/firgun/?v=%d" % time.time(), wait_until="networkidle", timeout=90000)
        pg.screenshot(path=f"fg/{tag}-1-intro.png")
        # 2. the live join form: choose a profession, try to send empty, see the messages
        pg.goto("https://nad-lan.co.il/firgun/?join=1&v=%d" % time.time(), wait_until="networkidle", timeout=90000)
        pg.select_option("#nlfg-jp", "shamai")
        g = pg.evaluate("() => { const r = document.querySelector('[data-fg-gender-row]'); return [r.hidden, [...document.querySelectorAll('#nlfg-jg option')].map(o => o.textContent)]; }")
        pg.click('[data-fg="join"] button[type="submit"]')
        pg.wait_for_timeout(300)
        m1 = pg.evaluate("() => document.querySelector('[data-fg=\"join\"] [data-fg-msg]').textContent")
        pg.fill("#nlfg-jn", "בדיקה"); pg.fill("#nlfg-jc", "תל אביב"); pg.fill("#nlfg-jt", "123")
        pg.click('[data-fg="join"] button[type="submit"]'); pg.wait_for_timeout(300)
        m2 = pg.evaluate("() => document.querySelector('[data-fg=\"join\"] [data-fg-msg]').textContent")
        pg.fill("#nlfg-jt", "050-1234567"); pg.click('[data-fg="join"] button[type="submit"]'); pg.wait_for_timeout(300)
        m3 = pg.evaluate("() => document.querySelector('[data-fg=\"join\"] [data-fg-msg]').textContent")
        pg.evaluate("() => document.querySelector('#nlfg-join').scrollIntoView({block: 'start'})")
        pg.wait_for_timeout(400)
        pg.screenshot(path=f"fg/{tag}-2-join.png", full_page=False)
        print(tag, "gender row hidden:", g[0], "forms:", g[1], "| messages:", m1, "/", m2, "/", m3)
        # 3. the give form from the self-test, with the real script: search the live directory, pick, choose qualities
        pg.goto("https://nad-lan.co.il/firgun/?v=%d" % time.time(), wait_until="networkidle", timeout=90000)
        js = pg.evaluate("() => document.getElementById('nadlan-firgun-js').textContent")
        pg.evaluate("(h) => { const old = document.getElementById('nlfg'); const d = document.createElement('div'); d.innerHTML = h; old.replaceWith(d.firstElementChild); }", ST["page_give"])
        pg.evaluate(js)
        pg.fill("#nlfg-q", "כה")
        pg.wait_for_timeout(1800)
        n = pg.evaluate("() => document.querySelectorAll('[data-fg-list] .nlds-pick__item').length")
        pg.evaluate("() => document.querySelector('[data-fg=\"give\"]').scrollIntoView({block: 'start'})")
        pg.wait_for_timeout(300)
        pg.screenshot(path=f"fg/{tag}-3-give-search.png")
        if n:
            pg.click("[data-fg-list] .nlds-pick__item")
        for q in ("pro", "trust", "avail", "clear"):
            pg.click(f'[data-fg="give"] [data-q="{q}"]')
        pressed = pg.evaluate("() => [...document.querySelectorAll('[data-fg=\"give\"] [aria-pressed=\"true\"]')].map(c => c.textContent)")
        pg.fill("#nlfg-line", "עבדנו יחד על עסקה אחת, והכול היה מסודר.")
        pg.click('[data-fg="give"] button[type="submit"]'); pg.wait_for_timeout(1500)
        m4 = pg.evaluate("() => document.querySelector('[data-fg=\"give\"] [data-fg-msg]').textContent")
        pg.screenshot(path=f"fg/{tag}-4-give-filled.png")
        print(tag, "search results:", n, "| pressed (max 3):", pressed, "| send with the masked token:", m4)
        # 4. the strips from the self-test on Meital's page
        pg.goto("https://nad-lan.co.il/professionals/meital-katzir/?v=%d" % time.time(), wait_until="networkidle", timeout=90000)
        pg.evaluate("(h) => { const v = document.querySelector('.nlpp-video'); const d = document.createElement('div'); d.innerHTML = h; v.after(d.firstElementChild); }", ST["strip_from"])
        pg.evaluate("(h) => { const v = document.querySelector('.nlpp-network'); const d = document.createElement('div'); d.innerHTML = h; v.before(d.firstElementChild); }", ST["strip_to"])
        pg.evaluate("() => document.querySelector('.nlpp-network').scrollIntoView({block: 'start'})")
        pg.wait_for_timeout(600)
        pg.screenshot(path=f"fg/{tag}-5-strips.png")
        pg.close()
    b.close()
