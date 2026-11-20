# -*- coding: utf-8 -*-
"""Rentals, release 1.72.728 (HAD-795): the PUBLIC demo of version 1 on https://nad-lan.co.il/my-rentals/, as a visitor.
For every sample home with a tenant, he and en, wide and phone width:
  - the demo answer of the server holds no phone at all;
  - inside the rentals block there is no link to wa.me, tel: or mailto:, and the phone box is empty;
  - the tenant's name wears the example mark;
  - the reminder press shows the wording with a copy button and opens nothing.
Modes:
  (default)  the live site as it is (run AFTER the release);
  --pre      BEFORE the release: the live page, with rental-manager.js served from the working copy and the phone blanked in the
             demo answer the way the PHP change does it. Proves the script change, not the server change.
Headless Edge with a real GPU for the 3D model, NOT a real phone.
Usage: python scripts/rentals/lab_sample_people_v1.py [--pre]"""
import sys, json, pathlib, re, random
from playwright.sync_api import sync_playwright

PRE = "--pre" in sys.argv
ROOT = pathlib.Path(__file__).resolve().parents[2]
JS = ROOT / "plugins/nadlan-config/assets/rentals/rental-manager.js"
OUT = ROOT / "docs/rentals/build/slice1/shots-728"
OUT.mkdir(parents=True, exist_ok=True)
SITE = "https://nad-lan.co.il"
MARK = {"he": "(דוגמה)", "en": "(example)"}
results = {"mode": "pre-release (script from the working copy, phone blanked in the answer)" if PRE else "live", "checks": [], "errors": []}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:260]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:190] if info != "" else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist"])
    for lang in ("he", "en"):
        for w, h in ((1280, 900), (390, 844)):
            tag = "%s %dx%d" % (lang, w, h)
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=w < 900, locale="he-IL")
            popups = []
            ctx.on("page", lambda pg2: popups.append(pg2.url))
            pg = ctx.new_page(); errs = []; answers = []
            if PRE:
                pg.route(re.compile(r"/assets/rentals/rental-manager\.js"), lambda r: r.fulfill(status=200, content_type="application/javascript; charset=utf-8", body=JS.read_text(encoding="utf-8")))

                def demo(route):
                    resp = route.fetch()
                    d = resp.json()
                    for pr in d.get("props", []):
                        for u in pr.get("units", []):
                            u["tenant_phone"] = ""
                    route.fulfill(response=resp, body=json.dumps(d, ensure_ascii=False), headers={**resp.headers, "content-type": "application/json; charset=UTF-8"})
                pg.route(re.compile(r"/wp-json/nadlan/v1/rental-demo"), demo)

            def on_resp(r):
                if "/nadlan/v1/rental-demo" in r.url and "seed" not in r.url:
                    try:
                        answers.append(r.text())
                    except Exception as e:  # noqa: BLE001
                        answers.append("ERR " + str(e))
            pg.on("response", on_resp)
            pg.goto("%s/my-rentals/?%st728v=%d" % (SITE, "lang=en&" if lang == "en" else "", random.randint(1000, 99999)), wait_until="domcontentloaded", timeout=60000)
            try:
                pg.wait_for_selector("#nlrm-mount #nlrm-props button", timeout=30000)
            except Exception as e:  # noqa: BLE001
                check("%s: the public demo loads" % tag, False, str(e)[:120]); ctx.close(); continue
            pg.evaluate("document.querySelector('#nlrm-mount').scrollIntoView()")
            try:
                pg.wait_for_selector("#nlrm-mount model-viewer button.nlrm-hot", state="attached", timeout=40000)
            except Exception as e:  # noqa: BLE001
                check("%s: the 3D building of the demo is built" % tag, False, str(e)[:120]); ctx.close(); continue
            popups.clear()
            ans = " ".join(answers)
            nums = re.findall(r'"tenant_phone":"([^"]+)"', ans)
            check("%s: the demo answer holds no tenant phone and no phone-shaped number" % tag, len(answers) >= 1 and not nums and not re.search(r"9725\d{8}|05\d{8}", ans), (len(answers), nums[:3]))
            nprops = pg.evaluate("() => document.querySelectorAll('#nlrm-props button').length")
            seen = []; bad = []
            for pi in range(nprops):
                pg.evaluate("i => document.querySelectorAll('#nlrm-props button')[i].click()", pi)
                pg.wait_for_timeout(900)
                try:
                    pg.wait_for_selector("#nlrm-mount model-viewer button.nlrm-hot", state="attached", timeout=20000)
                except Exception:  # noqa: BLE001
                    bad.append(("no 3D", pi)); continue
                nh = pg.evaluate("() => document.querySelectorAll('#nlrm-mount model-viewer button.nlrm-hot:not(.is-ghost)').length")
                for hi in range(nh):
                    pg.evaluate("i => document.querySelectorAll('#nlrm-mount model-viewer button.nlrm-hot:not(.is-ghost)')[i].click()", hi)
                    pg.wait_for_timeout(350)
                    s = pg.evaluate("""() => { const box = document.querySelector('#nlrm-unit'), m = document.querySelector('#nlrm-mount');
                      const links = [...m.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => /wa\\.me|whatsapp\\.com|^tel:|^mailto:|^sms:/i.test(h));
                      const ph = document.getElementById('nlu-phone'), nm = document.getElementById('nlu-name') || box.querySelector('input[type=text]');
                      const txt = m.innerText, shaped = txt.match(/(?:\\+?972|0)5\\d[\\s-]?\\d{3}[\\s-]?\\d{4}/g) || [];
                      const names = [...box.querySelectorAll('input')].map(i => i.value).filter(v => v && /[\\u0590-\\u05ffA-Za-z]/.test(v));
                      return { links, phone: ph ? ph.value : null, shaped, names, demoBtn: !!document.getElementById('nlu-wademo'), title: (box.querySelector('h4') || {}).textContent || '' }; }""")
                    tenant = [n for n in s["names"] if MARK[lang] in n or "(דוגמה)" in n]
                    rec = {"prop": pi, "home": s["title"][:30], "tenant": (tenant or [""])[0]}
                    if s["links"] or s["phone"] or s["shaped"]:
                        bad.append(("link or number", rec, s["links"][:2], s["phone"], s["shaped"][:2])); continue
                    if s["demoBtn"]:
                        if not tenant:
                            bad.append(("name without the mark", rec, s["names"][:3])); continue
                        pg.evaluate("document.getElementById('nlu-wademo').scrollIntoView({ block: 'center' })")
                        pg.wait_for_timeout(200)
                        url0 = pg.url
                        pg.click("#nlu-wademo", timeout=5000)
                        pg.wait_for_timeout(250)
                        r = pg.evaluate("""() => { const m = document.getElementById('nlu-wamsg'), t = document.getElementById('nlu-watxt'), c = document.getElementById('nlu-wacopy'), r = m.getBoundingClientRect();
                          return { shown: !m.hidden && r.height > 20, txt: t.textContent, copy: !!c && c.getBoundingClientRect().height >= 24, exp: document.getElementById('nlu-wademo').getAttribute('aria-expanded'),
                            links: [...document.querySelectorAll('#nlrm-mount a[href]')].map(a => a.getAttribute('href')).filter(h => /wa\\.me|^tel:|^mailto:/.test(h)) }; }""")
                        if not (r["shown"] and len(r["txt"]) > 10 and r["copy"] and r["exp"] == "true" and not r["links"]) or pg.url != url0:
                            bad.append(("reminder", rec, r)); continue
                        if not seen:
                            pg.evaluate("document.getElementById('nlu-wamsg').scrollIntoView({ block: 'center' })")
                            pg.wait_for_timeout(200)
                            pg.screenshot(path=str(OUT / ("v1-%s-%s-%d.png" % ("pre" if PRE else "live", lang, w))))
                        rec["wording"] = r["txt"][:60]
                    seen.append(rec)
            withTen = [x for x in seen if x.get("wording")]
            check("%s: %d sample homes opened, %d with a tenant; no chat, call or mail link and no number anywhere in the rentals block" % (tag, len(seen), len(withTen)), len(seen) >= 3 and len(withTen) >= 3 and not bad, bad[:2] or [x["tenant"] for x in withTen])
            check("%s: each tenant's reminder shows its wording with a copy button and opens nothing" % tag, len(withTen) >= 3 and not bad and not popups, (bad[:1], popups[:2]) if (bad or popups) else withTen[0]["wording"])
            results["errors"] += errs; ctx.close()
    b.close()

ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
(ROOT / ("docs/rentals/build/slice1/lab-728-v1-%s-results.json" % ("pre" if PRE else "live"))).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nRESULT %d/%d checks passed (%s)" % (ok, n, results["mode"]))
sys.exit(0 if ok == n else 1)
