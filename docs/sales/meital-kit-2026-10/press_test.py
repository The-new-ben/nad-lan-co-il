# -*- coding: utf-8 -*-
"""HAD-495: real presses on the live DealSign pages, under an internal TEST office (never Meital's).
phone: the broker opens an agreement, signs, gets the developer link; desktop: the developer fills, signs both documents and
lands on the signed copy; phone: the broker registers a client; desktop: the developer confirms the registration.
python press_test.py <test office url>   -> shots/press-*.png and a summary"""
import sys
import time
from playwright.sync_api import sync_playwright

OFFICE = sys.argv[1] if __name__ == "__main__" else ""
OUT = "shots/press-"


def sign(pg):
    c = pg.locator("canvas[data-sig]").first
    c.scroll_into_view_if_needed()
    b = c.bounding_box()
    x0, y0 = b["x"] + b["width"] * 0.2, b["y"] + b["height"] * 0.6
    pg.mouse.move(x0, y0); pg.mouse.down()
    for i in range(1, 30):
        pg.mouse.move(x0 + i * b["width"] * 0.02, y0 - (i % 7) * 6 + (i % 3) * 4, steps=2)
    pg.mouse.up()


if __name__ != "__main__":
    pass
else:
  with sync_playwright() as p:
      br = p.chromium.launch(channel="chrome")
      ph = br.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL")
      dk = br.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL")
      a = ph.new_page(); a.goto(OFFICE, wait_until="networkidle"); a.screenshot(path=OUT + "1-office.png", full_page=False)
      f = a.locator("form[data-form=deal]")
      f.locator("select[name=project]").select_option("ashira")
      f.locator("input[name=dev]").fill("חברת בדיקה פנימית בע״מ")
      f.locator("input[name=rate]").fill("1.5")
      f.locator("input[name=regto]").fill("050-0000000")
      f.locator("input[name=bid]").fill("123456782")
      f.locator("input[name=agree]").check()
      sign(a)
      f.locator("button.btn").click()
      a.wait_for_selector("form[data-form=deal] .msg.ok a", timeout=30000)
      dev_url = f.locator(".msg.ok a").first.get_attribute("href")
      a.screenshot(path=OUT + "2-deal-created.png", full_page=True)
      print("deal created ->", dev_url[:60] + "...")
      d = dk.new_page(); d.goto(dev_url, wait_until="networkidle"); d.screenshot(path=OUT + "3-dev-sign.png", full_page=True)
      g = d.locator("form[data-form=sign]")
      g.locator("input[name=devnum]").fill("512345678"); g.locator("input[name=devaddr]").fill("כתובת בדיקה 1, תל אביב")
      g.locator("input[name=name]").fill("ישראל בדיקה"); g.locator("input[name=role]").fill("מנהל שיווק (בדיקה)")
      g.locator("input[name=email]").fill("test@example.com"); g.locator("input[name=phone]").fill("050-0000000")
      g.locator("input[name=plan][value='3']").check(); g.locator("input[name=agree_a]").check(); g.locator("input[name=agree_b]").check()
      sign(d)
      g.locator("button.btn").click()
      d.wait_for_url("**nlsg_sign=**", timeout=30000); d.wait_for_selector("text=ההסכם נחתם", timeout=30000)
      d.screenshot(path=OUT + "4-signed-copy.png", full_page=True)
      print("signed copy shown:", d.locator("h1").inner_text())
      a.reload(wait_until="networkidle"); a.locator("[data-tab=regs]").click()
      r = a.locator("form[data-form=reg]")
      r.locator("input[name=client]").fill("לקוח בדיקה"); r.locator("input[name=tail]").fill("1234"); r.locator("input[name=want]").fill("קומה גבוהה, לכיוון הים")
      r.locator("input[name=consent]").check(); r.locator("button.btn").click()
      a.wait_for_selector("form[data-form=reg] .msg.ok a", timeout=30000)
      rev_url = r.locator(".msg.ok a").first.get_attribute("href")
      a.screenshot(path=OUT + "5-registered.png", full_page=True)
      print("registered ->", rev_url[:60] + "...", "|", r.locator(".msg.ok div").first.inner_text())
      v = dk.new_page(); v.goto(rev_url, wait_until="networkidle"); v.screenshot(path=OUT + "6-review.png", full_page=True)
      w = v.locator("form[data-form=rev]")
      w.locator("input[name=name]").fill("ישראל בדיקה"); w.locator("input[name=act][value=confirm]").check(); w.locator("button.btn").click()
      v.wait_for_selector("text=החברה אישרה את הרישום", timeout=30000)
      v.screenshot(path=OUT + "7-confirmed.png", full_page=True)
      a.reload(wait_until="networkidle"); a.locator("[data-tab=regs]").click(); time.sleep(1)
      a.screenshot(path=OUT + "8-office-after.png", full_page=True)
      print("office after:", a.locator("#regs .st").first.inner_text(), "|", a.locator("#deals .st").first.inner_text())
      br.close()
