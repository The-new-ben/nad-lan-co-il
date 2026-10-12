# -*- coding: utf-8 -*-
"""HAD-495 / 1.72.444 presses: Meital's office opens on the materials tab (phone), a PDF opens, the film answers a byte range;
in the internal TEST office a brokerage-only agreement is signed (one document, no advertising plan)."""
import json
import os
import urllib.request

from playwright.sync_api import sync_playwright

from press_test import sign  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MEITAL = json.load(open(os.path.join(HERE, "private", "office-6b3536.json"), encoding="utf-8"))["office_url"]
TEST = json.load(open(os.path.join(HERE, "private", "office-d6bd3d.json"), encoding="utf-8"))["office_url"]
links = json.load(open(os.path.join(HERE, "private", "kit-links.json"), encoding="utf-8"))
r = urllib.request.urlopen(urllib.request.Request(links["film-ashira.mp4"]["url"], headers={"Range": "bytes=0-1023", "User-Agent": "Mozilla/5.0"}), timeout=60)
print("film range:", r.status, r.headers.get("Content-Range"), r.headers.get("Content-Type"), len(r.read()))
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome")
    ph = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL")
    a = ph.new_page(); a.goto(MEITAL, wait_until="networkidle")
    print("meital tabs:", a.locator(".tabs a").all_inner_texts(), "| items:", a.locator("#kit .kit").count(), "| groups:", a.locator("#kit h2").all_inner_texts())
    a.screenshot(path="shots/press2-1-meital-kit.png", full_page=True)
    with a.expect_popup() as pop:
        a.locator("#kit .kit").first.locator("a", has_text="פתיחה").click()
    pdf = pop.value
    pdf.wait_for_load_state()
    print("guide opens:", pdf.url[:60] + "...")
    a.locator("[data-tab=deals]").click()
    print("kind options:", a.locator("form[data-form=deal] input[name=kind]").count(), "| checked:", a.locator("form[data-form=deal] input[name=kind]:checked").get_attribute("value"))
    a.screenshot(path="shots/press2-2-meital-deals.png", full_page=False)
    t = ph.new_page(); t.goto(TEST, wait_until="networkidle"); t.locator("[data-tab=deals]").click()
    f = t.locator("form[data-form=deal]")
    f.locator("select[name=project]").select_option("rainbow")
    f.locator("input[name=dev]").fill("חברת בדיקה פנימית ב׳ בע״מ"); f.locator("input[name=rate]").fill("2")
    f.locator("input[name=regto]").fill("050-0000000"); f.locator("input[name=bid]").fill("123456782"); f.locator("input[name=agree]").check()
    sign(t); f.locator("button.btn").click()
    t.wait_for_selector("form[data-form=deal] .msg.ok a", timeout=30000)
    dev = f.locator(".msg.ok a").first.get_attribute("href")
    dk = br.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL")
    d = dk.new_page(); d.goto(dev, wait_until="networkidle")
    print("broker-only sign page: docs", d.locator(".card.doc").count(), "| plan field", d.locator("input[name=plan]").count(), "| agree_b", d.locator("input[name=agree_b]").count())
    g = d.locator("form[data-form=sign]")
    g.locator("input[name=devnum]").fill("512345678"); g.locator("input[name=devaddr]").fill("כתובת בדיקה 2, תל אביב")
    g.locator("input[name=name]").fill("ישראל בדיקה"); g.locator("input[name=role]").fill("מנהל מכירות (בדיקה)")
    g.locator("input[name=email]").fill("test@example.com"); g.locator("input[name=agree_a]").check()
    sign(d); g.locator("button.btn").click()
    d.wait_for_selector("text=ההסכם נחתם", timeout=30000)
    print("signed copy: docs", d.locator(".card.doc").count(), "| preamble has no advertising:", "בהזמנה נפרדת" not in d.locator(".card.doc").first.inner_text())
    d.screenshot(path="shots/press2-3-broker-only-signed.png", full_page=True)
    br.close()
