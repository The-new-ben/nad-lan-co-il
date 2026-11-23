# -*- coding: utf-8 -*-
"""HAD-795 23.11.2026: the tutorial film row (inc/rentals/portfolio.php nadlan_rm_film_row + assets/rentals/rm-film.js).
Lab: renders the row with PHP CLI (WordPress stubs) into docs/design-lab/rentals/film-<lang>.html. Live: pass the page URL.
For he and en at 390x844 and 1280x800: the row is visible, no video request before the press, the press opens the player in
place and it plays WITH sound (not muted, time moves), the close button puts the row back, 0 page errors.
Headless Edge, NOT a real phone.  Usage: python scripts/rentals/lab_film.py [https://nad-lan.co.il/my-rentals/]"""
import sys, json, pathlib, subprocess, http.server, threading, functools
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
LIVE = sys.argv[1] if len(sys.argv) > 1 else ""
OUT = ROOT / "docs/rentals/build/film" / ("shots-live" if LIVE else "shots-lab"); OUT.mkdir(parents=True, exist_ok=True)
PHP = r"C:\Users\777\tools\php-8.3\php.exe"
STUB = r"""<?php define('ABSPATH','/'); define('NADLAN_CONFIG_VERSION','lab');
function content_url($p=''){return 'https://nad-lan.co.il/wp-content'.$p;} function plugins_url($p='',$f=''){return '../../../plugins/nadlan-config/'.$p;}
function esc_url($s){return htmlspecialchars($s,ENT_QUOTES);} function esc_attr($s){return htmlspecialchars($s,ENT_QUOTES);} function esc_html($s){return htmlspecialchars($s,ENT_QUOTES);}
require '%s'; $l=$argv[1]; echo '<!doctype html><html lang="'.$l.'" dir="'.($l==='he'?'rtl':'ltr').'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><style>body{margin:0;background:#f6f8f9;font-family:Heebo,sans-serif}header{text-align:center;padding:30px 16px}body:not(.x) button{background:#c2563a!important;color:#fff!important;border-radius:4px!important;padding:14px 30px!important;font:700 15px Heebo!important;text-transform:uppercase!important}</style></head><body><header><h1>H1</h1><p class="nlrm-one">answer line</p>'; nadlan_rm_film_row($l); echo '</header><div style="height:900px;background:#0d2129"></div></body></html>';"""
results = {"checks": []}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:300]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:220] if info != "" else ""))


srv = None
if not LIVE:
    stub = ROOT / "docs/design-lab/rentals/_film_stub.php"
    stub.write_text(STUB % str(ROOT / "plugins/nadlan-config/inc/rentals/portfolio.php").replace("\\", "/"), encoding="utf-8")
    for l in ("he", "en"):
        html = subprocess.run([PHP, str(stub), l], capture_output=True).stdout
        (ROOT / ("docs/design-lab/rentals/film-%s.html" % l)).write_bytes(html)
    stub.unlink()
    H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    H.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47923), H); threading.Thread(target=srv.serve_forever, daemon=True).start()

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--autoplay-policy=user-gesture-required"])
    for lang in ("he", "en"):
        for w, h in ((390, 844), (1280, 800)):
            tag = "%s %dx%d" % (lang, w, h)
            ctx = b.new_context(viewport={"width": w, "height": h}, has_touch=w < 900, locale="he-IL")
            pg = ctx.new_page(); errs = []; vids = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
            pg.on("console", lambda m: errs.append("console: " + m.text[:160]) if m.type == "error" else None)
            pg.on("request", lambda r: vids.append(r.url) if ".mp4" in r.url else None)
            url = (LIVE + ("?lang=en" if lang == "en" else "")) if LIVE else "http://127.0.0.1:47923/docs/design-lab/rentals/film-%s.html" % lang
            pg.goto(url, wait_until="load", timeout=90000); pg.wait_for_timeout(2500)
            s = pg.evaluate("""() => { const b = document.querySelector('#nlrm-film .nlrm-film-go'), r = b && b.getBoundingClientRect(), h1 = document.querySelector('h1'), st = document.querySelector('#nlpf');
              const t = r && document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
              return { has: !!b, top: r ? Math.round(r.top + scrollY) : null, hgt: r ? Math.round(r.height) : null, wid: r ? Math.round(r.width) : null, free: !!t && (t === b || b.contains(t)),
                h1: h1 ? Math.round(h1.getBoundingClientRect().top + scrollY) : null, stage: st ? Math.round(st.getBoundingClientRect().top + scrollY) : null, bg: b ? getComputedStyle(b).backgroundColor : '', label: b ? b.getAttribute('aria-label') : '',
                text: b ? b.innerText.replace(/\\s+/g, ' ') : '', vid: document.querySelectorAll('#nlrm-film video').length, ox: document.scrollingElement.scrollWidth - innerWidth }; }""")
            check("%s the film row is there under the H1 and above the stage, white, free to press, at least 44 px tall, no sideways scroll" % tag,
                  s["has"] and s["free"] and s["hgt"] >= 44 and s["bg"] == "rgb(255, 255, 255)" and s["ox"] <= 0 and (s["h1"] is None or s["top"] > s["h1"]) and (s["stage"] is None or s["top"] < s["stage"]), s)
            check("%s nothing of the film is requested before the press (no video element, no mp4 request)" % tag, s["vid"] == 0 and not vids, vids[:2])
            pg.locator("#nlrm-film .nlrm-film-go").scroll_into_view_if_needed()
            pg.screenshot(path=str(OUT / ("film-%s-%d-row.png" % (lang, w))))
            pg.click("#nlrm-film .nlrm-film-go"); pg.wait_for_timeout(6000)
            v = pg.evaluate("""() => { const v = document.querySelector('#nlrm-film video'), f = document.querySelector('#nlrm-film figure'), r = f && f.getBoundingClientRect();
              return v ? { t: v.currentTime, paused: v.paused, muted: v.muted, vol: v.volume, ctl: v.controls, src: v.currentSrc, w: Math.round(r.width), h: Math.round(r.height), err: v.error ? v.error.code : 0, rowHidden: getComputedStyle(document.querySelector('#nlrm-film .nlrm-film-go')).display === 'none' } : null; }""")
            check("%s pressed: the player opens in place and plays WITH sound (time moves, not muted, controls on)" % tag,
                  v and v["t"] > 1 and not v["paused"] and not v["muted"] and v["vol"] > 0 and v["ctl"] and not v["err"] and v["rowHidden"] and (("-en-" in v["src"]) == (lang == "en")), v)
            pg.screenshot(path=str(OUT / ("film-%s-%d-playing.png" % (lang, w))))
            pg.click("#nlrm-film .nlrm-film-x"); pg.wait_for_timeout(500)
            c = pg.evaluate("() => ({ vid: document.querySelectorAll('#nlrm-film video').length, row: getComputedStyle(document.querySelector('#nlrm-film .nlrm-film-go')).display !== 'none' })")
            check("%s close puts the row back and removes the player" % tag, c["vid"] == 0 and c["row"], c)
            check("%s no page errors and no console errors" % tag, not errs, errs[:3])
            ctx.close()
    b.close()
if srv:
    srv.shutdown()
ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
(ROOT / ("docs/rentals/build/film/%s-film-results.json" % ("live" if LIVE else "lab"))).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nRESULT %d/%d checks passed" % (ok, n))
sys.exit(0 if ok == n else 1)
