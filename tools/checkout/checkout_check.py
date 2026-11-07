# Live checkout check (HAD-678, 7.11.2026): adds product 489 to the cart, fills a TEST identity (checkout-test@nad-lan.co.il), places the order and
# waits for the Morning/Grow card form on /checkout/order-pay/. Never types card data. Afterwards run cancel_test_order.py <order id>.
# Usage: python tools/checkout/checkout_check.py <out dir>   (pass = a frame from creditguard/meshulam with "מספר כרטיס" fields, no "גישה נדחתה")
# Live checkout test up to the Morning payment page. Never types card data. Test identity only.
import sys, time, re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": 1280, "height": 900}, locale="he-IL")
    pg.goto("https://nad-lan.co.il/?add-to-cart=489", wait_until="domcontentloaded", timeout=90000)
    pg.goto("https://nad-lan.co.il/checkout/", wait_until="networkidle", timeout=90000)
    def fill(sel, val):
        el = pg.locator(sel).first
        el.wait_for(timeout=20000); el.fill(val)
    fill("#email", "checkout-test@nad-lan.co.il")
    try:
        pg.select_option("#billing-country", "IL")
    except Exception as e:
        print("country select:", str(e)[:120])
    fill("#billing-first_name", "בדיקת")
    fill("#billing-last_name", "מערכת")
    fill("#billing-address_1", "בדיקה 1")
    fill("#billing-city", "תל אביב")
    try: fill("#billing-postcode", "6100000")
    except Exception: pass
    pg.get_by_label(re.compile("כרטיסי אשראי")).first.check()
    time.sleep(1)
    pg.screenshot(path=OUT + "/co-1-filled.png", full_page=False)
    pg.get_by_role("button", name=re.compile("לבצע הזמנה")).click()
    for i in range(30):
        time.sleep(1)
        txt = pg.inner_text("body")[:4000]
        if "גישה נדחתה" in txt or "order-pay" in pg.url or "greeninvoice" in pg.url or "morning" in pg.url or "order-received" in pg.url:
            break
    time.sleep(18)
    print("URL:", re.sub(r"key=[^&]+", "key=…", pg.url))
    frames = [re.sub(r"\?.*", "", f.url) for f in pg.frames if f.url and f.url != "about:blank"]
    print("frames:", frames[:6])
    body = pg.inner_text("body")
    for kw in ("גישה נדחתה", "נא להתחבר מחדש", "שגיאה", "error", "Error", "מספר כרטיס", "card"):
        if kw in body: print("text has:", kw)
    print("notices:", [t.strip()[:160] for t in pg.locator(".wc-block-components-notice-banner, .woocommerce-error, .woocommerce-message, .woocommerce-info").all_inner_texts()][:5])
    for f in pg.frames:
        try:
            t = f.inner_text("body")[:300].replace(chr(10), " | ")
            if t.strip(): print("frame text:", re.sub(r"[?].*", "", f.url)[:80], "->", t[:200])
        except Exception: pass
    pg.screenshot(path=OUT + "/co-2-after.png", full_page=False)
    b.close()
