# -*- coding: utf-8 -*-
"""HAD-795 stage 3: tap count of the ten landlord jobs (TEN-JOBS.md) in rentals app v2, LOCAL lab copy only.

Serve first, from the worktree root:   python -m http.server 47914 --bind 127.0.0.1
Run:    python count_v2.py [base_url]
Every press is recorded by the Runner (button, link, tab, field focus, file picker press and choice,
confirm dialogs). Typed characters and scrolling are not counted. Each job runs in a fresh browser
context (fresh sample portfolio), Hebrew, phone 390x844 (mobile + touch) and desktop 1440x900.
Outputs next to this file: taps-v2.csv and shots/J<n>-<phone|desk>.png
"""
import sys, csv, json, pathlib, tempfile, datetime, base64
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
URL = BASE + "?lang=he#/today"
HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)
TMP = pathlib.Path(tempfile.mkdtemp(prefix="taps_v2_"))
PNG = TMP / "photo.png"
PNG.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="))
PDF = TMP / "invoice.pdf"
PDF.write_bytes(b"%PDF-1.1\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF")
L = ".nlrm-layer.is-in "          # anything inside the open sheet / card
NAV = ".nlrm-nav "                # the main navigation (side bar on desktop, top bar on phone)
JS_STATE = "(() => { const d = NLRM.store.d; return JSON.stringify({ ledger: d.ledger.length, events: d.events.length, docs: d.docs.length, tickets: d.tickets.length }); })()"


class Runner:
    def __init__(self, pg, dev):
        self.pg, self.dev, self.taps, self.notes = pg, dev, [], []

    def state(self):
        return json.loads(self.pg.evaluate(JS_STATE))

    def label(self, loc):
        t = loc.evaluate("""e => {
            const clean = s => (s || '').replace(/\\s+/g, ' ').trim();
            if (e.tagName === 'INPUT' || e.tagName === 'TEXTAREA' || e.tagName === 'SELECT') {
                const lb = e.closest('label'); const sp = lb && lb.querySelector('span');
                return 'שדה: ' + clean(sp ? sp.innerText : (e.getAttribute('placeholder') || e.name));
            }
            return clean(e.innerText) || clean(e.getAttribute('aria-label')) || e.tagName;
        }""")
        return t[:60]

    def tap(self, sel, wait=550):
        loc = self.pg.locator(sel).first
        loc.wait_for(state="visible", timeout=8000)
        lab = self.label(loc)
        loc.scroll_into_view_if_needed()          # scrolling is free
        loc.click()
        self.taps.append(lab)
        self.pg.wait_for_timeout(wait)
        return lab

    def pick_file(self, sel, path):
        """pressing the file field = 1 press; choosing in the system file picker = 1 press"""
        loc = self.pg.locator(sel).first
        loc.wait_for(state="visible", timeout=8000)
        lab = self.label(loc)
        with self.pg.expect_file_chooser() as fc:
            loc.click()
        self.taps.append(lab + " (פתיחת בורר הקבצים)")
        fc.value.set_files(str(path))
        self.taps.append("בחירת הקובץ בבורר הקבצים")
        self.pg.wait_for_timeout(300)

    def type_into(self, sel, text):
        """a tap to focus, then typed characters (not counted)"""
        lab = self.tap(sel, wait=150)
        self.pg.locator(sel).first.fill(text)
        return lab


def ctx_for(b, dev):
    if dev == "phone":
        return b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL")
    return b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL")


# ---------- the ten jobs: each returns (ok, check_text, note) after performing its presses on r ----------
def j1(r):
    pg = r.pg
    late = pg.locator("[data-act=pay][data-lease]")           # the Today list: one 'mark paid' per unpaid lease
    n = late.count()
    txt = pg.inner_text(".nlrm-app")
    ok = n >= 2 and "רון מזרחי" in txt and "Daniel Brooks" in txt and "באיחור" in txt
    pg.locator("[data-act=pay][data-lease]").first.scroll_into_view_if_needed()   # scroll is free
    pg.wait_for_timeout(300)
    return ok, "Today lists %d unpaid leases in red (Ron Mizrahi 11,982; Daniel Brooks 4,300)" % n, \
        "0 presses: the home screen already lists them; scroll only on phone. Money > ledger tab (1 press) shows the same per charge."


def j2(r):
    pg = r.pg
    before = r.state()
    r.tap("[data-act=pay][data-lease='204']")                  # סימון ששולם (Daniel Brooks, 4,300 = this month's rent)
    pre = pg.eval_on_selector_all(L + "[name]", "e => Object.fromEntries(e.map(x => [x.name, x.value]))")
    r.tap(L + "[type=submit]")                                 # שמירה (amount and date already filled)
    row = pg.evaluate("NLRM.store.d.ledger.filter(x => x.kind === 'payment' && x.lease_id === 204).slice(-1)[0]")
    gone = pg.locator("[data-act=pay][data-lease='204']").count() == 0
    ok = bool(row) and row["status"] == "paid" and row["amount"] == 430000 and row["paid_date"] == pre["paid_date"] and gone and r.state()["ledger"] == before["ledger"] + 1
    return ok, "payment row paid 4,300 ILS dated %s; the late row of lease 204 left Today=%s" % (row and row["paid_date"], gone), \
        "Form is prefilled (tenant, amount 4,300, today, method). 1 press if the tenant reported it first (confirm-pay)."


def j3(r):
    pg = r.pg
    before = r.state()
    r.tap("[data-act=wa-remind][data-lease='203']")            # תזכורת בוואטסאפ
    txt = pg.input_value(L + "textarea")
    href = pg.get_attribute(L + "[data-send]", "href")
    ready = txt.startswith("שלום רון") and "11,982" in txt and href.startswith("https://wa.me/972500000103?text=")
    r.tap(L + "[data-send]")                                   # שליחה בוואטסאפ (logs the message; demo mode does not open wa.me)
    ev = pg.evaluate("NLRM.store.d.events[0]")
    ok = ready and ev["type"] == "msg_out" and ev["channel"] == "whatsapp" and r.state()["events"] == before["events"] + 1
    return ok, "text filled (%d chars), wa.me link ready, journal msg_out logged" % len(txt), \
        "Ready-to-send text is already there after press 1; press 2 is the send link."


def j4(r):
    pg = r.pg
    before = r.state()
    r.tap(NAV + "[data-go=repairs]")                           # תקלות
    r.tap("[data-act=new-ticket]")                             # תקלה חדשה
    r.type_into(L + "[name=title]", "נזילה מהכיור במטבח")      # focus + typing
    r.tap(L + "[type=submit]")                                 # שמירה -> the repair card opens by itself
    pg.wait_for_selector(L + "[data-act=upload][data-scope=ticket]", timeout=6000)
    r.tap(L + "[data-act=upload][data-scope=ticket]")          # הוספת תמונה
    r.pick_file(L + "input[type=file]", PNG)
    r.tap(L + "[type=submit]")                                 # שמירה
    after = r.state()
    t = pg.evaluate("NLRM.store.d.tickets.slice(-1)[0]")
    d = pg.evaluate("NLRM.store.d.docs[0]")
    ok = after["tickets"] == before["tickets"] + 1 and after["docs"] == before["docs"] + 1 and d["scope"] == "ticket" and d["scope_id"] == t["id"] and d["name"] == "photo.png"
    return ok, "new repair #%s '%s' with attached photo %s" % (t["id"], t["title"], d["name"]), \
        "Apartment = the form's default (first). Choosing another apartment costs 2 more (open list, choose). Photo kind stays 'other'."


def j5(r):
    pg = r.pg
    before = r.state()
    r.tap("[data-act=open][data-open='ticket:501']")           # פתיחה (urgent boiler repair on Today)
    r.tap(L + "[data-act=ticket-vendor]")                      # בחירת בעל מקצוע
    r.tap(L + "[type=submit]")                                 # שמירה (first vendor preselected)
    pg.wait_for_selector(L + "[data-act=vendor-link]", timeout=6000)
    r.tap(L + "[data-act=vendor-link]")                        # שליחה לבעל המקצוע
    txt = pg.input_value(L + "textarea")
    r.tap(L + "[data-send]")                                   # שליחה בוואטסאפ
    t = pg.evaluate("NLRM.store.d.tickets.find(x => x.id === 501)")
    ev = pg.evaluate("NLRM.store.d.events[0]")
    ok = t["vendor_id"] == 109 and ev["scope"] == "ticket" and ev["scope_id"] == 501 and ev["type"] == "msg_out" and "הדוד" in ev["body"] and r.state()["events"] == before["events"] + 1
    return ok, "repair 501 assigned to vendor 109 (Yossi Plumbing); message with the repair details logged (%d chars)" % len(txt), \
        "Vendor list default is the first vendor (a plumber, not the boiler trade); picking another = +2. Dispatch link is a second step after assigning."


def j6(r):
    pg = r.pg
    before = r.state()
    r.tap("[data-act=open][data-open='ticket:501']")           # פתיחה
    r.tap(L + "[data-act=tstatus][data-status=done]")          # טופלה
    pg.wait_for_selector(L + "[data-act=upload][data-scope=ticket]", timeout=6000)
    r.tap(L + "[data-act=upload][data-scope=ticket]")          # הוספת תמונה (the only attach button of the repair)
    r.pick_file(L + "input[type=file]", PDF)
    r.tap(L + "[type=submit]")                                 # שמירה
    t = pg.evaluate("NLRM.store.d.tickets.find(x => x.id === 501)")
    d = pg.evaluate("NLRM.store.d.docs[0]")
    ok = t["status"] == "done" and d["scope"] == "ticket" and d["scope_id"] == 501 and d["name"] == "invoice.pdf" and r.state()["docs"] == before["docs"] + 1
    return ok, "repair 501 status done, file %s attached to it (kind=%s)" % (d["name"], d["kind"]), \
        "The attach button is labelled 'add photo' and the file is saved as kind 'other'; marking it kind 'invoice' = +2 presses. Cost field optional (+1 focus)."


def j7(r):
    pg = r.pg
    before = r.state()
    r.tap(".nlrm-app [data-act=new]")                          # הוספה
    r.tap(L + "[data-sheet-act=upload]")                       # העלאת מסמך
    r.pick_file(L + "input[type=file]", PDF)
    r.tap(L + "[type=submit]")                                 # שמירה
    d = pg.evaluate("NLRM.store.d.docs[0]")
    ok = r.state()["docs"] == before["docs"] + 1 and d["name"] == "invoice.pdf" and d["scope"] == "lease"
    return ok, "document %s stored on lease %s (apartment 7, default target)" % (d["name"], d["scope_id"]), \
        "Target = first lease by default; another apartment = +2; kind 'contract' = +2. Docs screen route is longer on phone (More > Docs)."


def j8(r):
    pg = r.pg
    r.tap(NAV + "[data-go=money]")                             # כספים
    r.tap("[data-mtab=cpi]")                                   # הצמדה למדד
    r.tap("[data-act=cpi-lease][data-lease='203']")            # בדיקת הצמדה עכשיו
    pg.wait_for_selector(L + ".nlrm-kpi", timeout=6000)
    txt = pg.inner_text(L + ".nlrm-kpis")
    ok = "6,056" in txt and "5,900" in txt
    return ok, "PARTIAL: new linked rent computed and shown (5,900 -> 6,056) but nothing is saved (sheet has no save button)", \
        "No 'apply' action exists; the linkage rule feeds future charges by itself (rm-core.js N.mx.amount, next step 1.9.2027), so 'saved for next month' cannot be done or confirmed by the user."


def j9(r):
    pg = r.pg
    if r.dev == "phone":
        r.tap(".nlrm-app [data-act=more]")                     # עוד
        r.tap(L + "[data-more=reports]")                       # דוחות
    else:
        r.tap(NAV + "[data-go=reports]")                       # דוחות
    r.tap("[data-act=rep-year]")                               # פתיחה (yearly report card)
    with pg.context.expect_page() as pop:
        r.tap(L + "[type=submit]")                             # פתיחה (year preselected)
    w = pop.value
    w.wait_for_load_state()
    w.wait_for_timeout(500)
    body = w.inner_text("body")
    r.popup = w
    ok = "2026" in body and "ארלוזורוב" in body and "₪" in body
    return ok, "yearly report opens in a new page: per-apartment totals (%d chars), 2026" % len(body), \
        "Year defaults to this year (Jan-Apr: last year). It opens as a printable page; Money > Tax tab is only a tax estimate form, not income per apartment."


def j10(r):
    pg = r.pg
    before = r.state()
    r.tap("[data-act=wa-renew][data-lease='202']")             # הצעת חידוש
    txt = pg.input_value(L + "textarea")
    href = pg.get_attribute(L + "[data-send]", "href")
    r.tap(L + "[data-send]")                                   # שליחה בוואטסאפ
    ev = pg.evaluate("NLRM.store.d.events[0]")
    today = pg.evaluate("NLRM.todayIso()")
    ok = href.startswith("https://wa.me/") and ev["type"] == "msg_out" and ev["scope"] == "lease" and ev["scope_id"] == 202 and ev["at"][:10] == today and r.state()["events"] == before["events"] + 1
    return ok, "renewal offer text (%d chars) logged on lease 202 in the journal dated %s" % (len(txt), ev["at"]), \
        "Recorded as a journal message, not as a lease change. The formal route (unit > lease tab > renew) is 4+ presses."


JOBS = [("J1", j1), ("J2", j2), ("J3", j3), ("J4", j4), ("J5", j5), ("J6", j6), ("J7", j7), ("J8", j8), ("J9", j9), ("J10", j10)]


def main():
    rows, errs = [], []
    today = datetime.date.today().isoformat()
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        for name, fn in JOBS:
            for dev in ("phone", "desk"):
                ctx = ctx_for(b, dev)
                pg = ctx.new_page()
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "404" not in m.text else None)
                pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
                pg.goto(URL, wait_until="networkidle")
                pg.wait_for_selector(".nlrm-kpis", timeout=15000)
                pg.wait_for_timeout(800)
                r = Runner(pg, dev)
                r.popup = None
                try:
                    ok, check, note = fn(r)
                    err = ""
                except Exception as e:  # a job that fails is reported, never hidden
                    ok, check, note, err = False, "SCRIPT ERROR: %s" % str(e).splitlines()[0][:160], "", "x"
                shot = "%s-%s.png" % (name, dev)
                pg.wait_for_timeout(350)
                (r.popup or pg).screenshot(path=str(SHOTS / shot))
                rows.append({"job": name, "device": "phone 390" if dev == "phone" else "desktop 1440", "taps": len(r.taps),
                             "path": " > ".join(r.taps) if r.taps else "(no press: visible on the home screen)",
                             "done_check": check if check.startswith("PARTIAL") else (("PASS: " if ok else "FAIL: ") + check), "screenshot": "shots/" + shot, "note": note,
                             "date": today, "url": URL})
                print(name, dev, len(r.taps), "PASS" if ok else "FAIL", "|", " > ".join(r.taps))
                ctx.close()
        b.close()
    with open(HERE / "taps-v2.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("console errors:", len(errs), errs[:3])
    print("fails:", [(x["job"], x["device"]) for x in rows if not x["done_check"].startswith("PASS")])


if __name__ == "__main__":
    main()
