# -*- coding: utf-8 -*-
"""RenewalRoomPro explainer: SILENT captioned draft, captured from the LOCAL preview (sample data, never the live site).

  php -S 127.0.0.1:8765 build/preview/server.php        (from the renewal-room folder)
  python film/build/capture.py 16x9 he                   -> film/renewal-room-he-16x9.mp4
  python film/build/capture.py 9x16 he                   -> film/renewal-room-he-9x16.mp4
  python film/build/capture.py 16x9 en                   -> film/renewal-room-en-16x9.mp4

How: Playwright drives the real room (the plugin's own route and REST code over the sample data), a caption bar, a cursor
and a "נתוני דוגמה" tag are injected into THIS browser only. Motion (cursor moves, scrolls, typing) is captured frame by frame
at 30 fps; holds are one frame with a duration. ffmpeg's concat demuxer turns the list into a 30 fps H.264 file.
Every number on screen comes from the sample data the room computes; the caption numbers are read from the page.
"""
import json, os, sys, time, shutil, subprocess, urllib.request, datetime
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
BASE = os.environ.get("RR_BASE", "http://127.0.0.1:8765")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FFMPEG = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
SCRATCH = os.environ.get("RR_FRAMES", r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\frames")
FPS = 30
ASPECT = {"16x9": {"vp": (1280, 720), "dsf": 1.5}, "9x16": {"vp": (432, 768), "dsf": 2.5}}
T = json.load(open(os.path.join(HERE, "captions.json"), encoding="utf-8"))

OVERLAY_CSS = """
.site-strip{display:none!important}
#film-cap{position:fixed;inset-inline:0;bottom:0;z-index:99999;background:rgba(18,32,42,.94);color:#fff;padding:var(--cp);font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;direction:var(--cd);text-align:start;pointer-events:none}
#film-cap b{display:block;font-weight:600;font-size:var(--cs);line-height:1.3}
#film-cap i{display:block;font-style:normal;font-weight:400;font-size:var(--ks);color:#9FD0E0;margin-bottom:4px;letter-spacing:0}
#film-tag{position:fixed;top:var(--tt);inset-inline-start:var(--tt);z-index:99999;background:#E9F1F4;color:#12202A;border:1px solid #9FD0E0;font:600 var(--ts) "IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;padding:4px 8px;border-radius:2px;pointer-events:none}
#film-cur{position:fixed;left:0;top:0;width:var(--cu);height:var(--cu);z-index:100000;pointer-events:none;transform:translate(-3px,-2px)}
#film-cur::after{content:"";position:absolute;left:-14px;top:-14px;width:30px;height:30px;border-radius:50%;border:3px solid #C42550;opacity:0;transition:none}
#film-cur.press::after{opacity:1}
.film-hl{outline:3px solid #C42550!important;outline-offset:3px!important}
"""
CURSOR_SVG = '<svg viewBox="0 0 24 24" width="100%" height="100%"><path d="M3 2 L3 20 L8 15 L11.5 22 L14.5 20.6 L11 13.8 L18 13.8 Z" fill="#12202A" stroke="#fff" stroke-width="1.6"/></svg>'


class Film:
    def __init__(self, page, aspect, lang, out_dir):
        self.p, self.aspect, self.lang, self.dir = page, aspect, lang, out_dir
        self.list = []      # (file, seconds)
        self.n = 0
        self.cx, self.cy = ASPECT[aspect]["vp"][0] * 0.5, ASPECT[aspect]["vp"][1] * 0.45
        self.cap = ("", "")

    def overlay(self):
        big = self.aspect == "16x9"
        vars_ = {"--cp": "10px 24px 14px" if big else "12px 16px 16px", "--cs": "24px" if big else "18px", "--ks": "13px" if big else "12px",
                 "--tt": "14px" if big else "10px", "--ts": "13px" if big else "11px", "--cu": "26px" if big else "20px", "--cd": "rtl" if self.lang == "he" else "ltr"}
        self.p.add_style_tag(content=":root{" + ";".join(f"{k}:{v}" for k, v in vars_.items()) + "}" + OVERLAY_CSS)
        self.p.evaluate("""([svg, tag]) => {
            if (!document.getElementById('film-cap')) { const c = document.createElement('div'); c.id = 'film-cap'; c.innerHTML = '<i></i><b></b>'; document.body.appendChild(c); }
            if (!document.getElementById('film-tag')) { const g = document.createElement('div'); g.id = 'film-tag'; g.textContent = tag; document.body.appendChild(g); }
            if (!document.getElementById('film-cur')) { const u = document.createElement('div'); u.id = 'film-cur'; u.innerHTML = svg; document.body.appendChild(u); }
        }""", [CURSOR_SVG, T["tag"][self.lang]])
        self.set_caption(*self.cap)
        self.place_cursor()

    def set_caption(self, kicker, text):
        self.cap = (kicker, text)
        self.p.evaluate("([k, t]) => { const c = document.getElementById('film-cap'); if (!c) return; c.querySelector('i').textContent = k; c.querySelector('b').textContent = t; c.style.display = t ? 'block' : 'none'; }", [kicker, text])

    def place_cursor(self, show=True):
        self.p.evaluate("([x, y, s]) => { const u = document.getElementById('film-cur'); if (u) { u.style.left = x + 'px'; u.style.top = y + 'px'; u.style.display = s ? 'block' : 'none'; } }", [self.cx, self.cy, show])

    def frame(self, seconds):
        self.n += 1
        f = os.path.join(self.dir, f"{self.n:05d}.jpg")
        self.p.screenshot(path=f, type="jpeg", quality=90)
        self.list.append((f, seconds))

    def hold(self, s):
        self.frame(s)

    def goto(self, url, wait=".rrp"):
        self.p.goto(BASE + url, wait_until="networkidle", timeout=60000)
        self.p.wait_for_selector(wait, timeout=30000)
        self.p.evaluate("document.fonts.ready")
        self.p.wait_for_timeout(500)
        self.overlay()

    def ease(self, t):
        return t * t * (3 - 2 * t)

    def move_to(self, sel, secs=0.8, dx=0.5, dy=0.5):
        box = self.p.locator(sel).first.bounding_box()
        if not box:
            raise SystemExit("not visible: " + sel)
        tx, ty = box["x"] + box["width"] * dx, box["y"] + box["height"] * dy
        x0, y0, n = self.cx, self.cy, max(1, int(secs * FPS))
        for i in range(1, n + 1):
            e = self.ease(i / n)
            self.cx, self.cy = x0 + (tx - x0) * e, y0 + (ty - y0) * e
            self.place_cursor()
            self.frame(1 / FPS)

    def click(self, sel, secs=0.8, wait_after=None, settle=600):
        self.move_to(sel, secs)
        self.p.evaluate("document.getElementById('film-cur').classList.add('press')")
        self.frame(0.12)
        self.p.locator(sel).first.click()
        if wait_after:
            self.p.wait_for_selector(wait_after, timeout=30000)
        self.p.wait_for_timeout(settle)
        if not self.p.query_selector("#film-cap"):
            self.overlay()
        self.p.evaluate("document.getElementById('film-cur') && document.getElementById('film-cur').classList.remove('press')")
        self.place_cursor()

    def scroll_to(self, sel, secs=1.0, top=0.12):
        y0 = self.p.evaluate("window.scrollY")
        y1 = self.p.evaluate("([s, f]) => { const e = document.querySelector(s); return Math.max(0, e.getBoundingClientRect().top + window.scrollY - window.innerHeight * f); }", [sel, top])
        y1 = min(y1, self.p.evaluate("document.documentElement.scrollHeight - window.innerHeight"))
        n = max(1, int(secs * FPS))
        for i in range(1, n + 1):
            self.p.evaluate("y => window.scrollTo(0, y)", y0 + (y1 - y0) * self.ease(i / n))
            self.frame(1 / FPS)

    def type_into(self, sel, text, secs=2.5):
        self.p.locator(sel).first.click()
        n = max(1, int(secs * FPS)); L = len(text)
        for i in range(1, n + 1):
            self.p.evaluate("([s, v]) => { const e = document.querySelector(s); e.value = v; }", [sel, text[: int(L * i / n)]])
            self.frame(1 / FPS)

    def highlight(self, sel, on=True):
        self.p.evaluate("([s, on]) => { const e = document.querySelector(s); if (e) e.classList.toggle('film-hl', on); }", [sel, on])

    def card(self, kind):
        c = T["cards"][kind][self.lang]
        big = self.aspect == "16x9"
        html = f"""<!doctype html><html lang="{self.lang}" dir="{'rtl' if self.lang == 'he' else 'ltr'}"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;600&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@500&display=block">
<style>html,body{{margin:0;height:100%;background:#12202A;color:#fff;font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",sans-serif}}
.w{{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 {'120px' if big else '36px'}}}
.k{{font-size:{'20px' if big else '15px'};color:#9FD0E0;font-weight:400;margin-bottom:{'18px' if big else '12px'}}}
.t{{font-size:{'58px' if big else '38px'};font-weight:600;line-height:1.18;max-width:{'1100px' if big else '100%'}}}
.s{{font-size:{'24px' if big else '18px'};color:#C9D6DE;margin-top:{'22px' if big else '16px'};line-height:1.5}}
.rule{{width:{'120px' if big else '80px'};height:3px;background:#2F6F86;margin:{'26px' if big else '20px'} 0}}
.cta{{display:inline-block;margin-top:{'26px' if big else '20px'};background:#1F4B5C;border:1px solid #9FD0E0;color:#fff;font-weight:600;font-size:{'22px' if big else '17px'};padding:{'14px 22px' if big else '12px 16px'};border-radius:6px}}
.tag{{position:absolute;top:{'28px' if big else '18px'};inset-inline-start:{'28px' if big else '18px'};background:#E9F1F4;color:#12202A;border:1px solid #9FD0E0;font-weight:600;font-size:{'14px' if big else '12px'};padding:4px 8px;border-radius:2px}}
.grid{{position:absolute;inset-inline-end:{'120px' if big else '36px'};bottom:{'90px' if big else '120px'};display:grid;grid-template-columns:repeat(4,{'34px' if big else '26px'});gap:4px;opacity:.9}}
.grid i{{display:block;height:{'28px' if big else '22px'};border:1px solid #9FD0E0}}
.grid i.y{{background:#2F6F86}} .grid i.p{{background:repeating-linear-gradient(135deg,#9FD0E0 0 2px,transparent 2px 5px)}}
</style></head><body><div class="tag">{T['tag'][self.lang]}</div><div class="w"><div class="k">{c['kicker']}</div><div class="t">{c['title']}</div><div class="rule"></div><div class="s">{c['sub']}</div>{('<div><span class="cta">' + c['cta'] + '</span></div>') if c.get('cta') else ''}</div>
<div class="grid">{''.join('<i class="' + ('y' if k in (0,1,2,4,5,6,8,9,12) else 'p' if k in (3,10) else '') + '"></i>' for k in range(16))}</div></body></html>"""
        self.p.set_content(html, wait_until="networkidle")
        self.p.evaluate("document.fonts.ready")
        self.p.wait_for_timeout(400)
        self.frame(c["secs"])


def run(aspect, lang):
    ids = json.loads(urllib.request.urlopen(BASE + "/__reset").read())
    A = ids["a"]
    frames = os.path.join(SCRATCH, f"{lang}-{aspect}")
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames)
    cfg = ASPECT[aspect]
    C = T["shots"]
    q = "" if lang == "he" else f"&lang={lang}"
    t0 = time.time()
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME, headless=True)
        ctx = b.new_context(viewport={"width": cfg["vp"][0], "height": cfg["vp"][1]}, device_scale_factor=cfg["dsf"], locale="he-IL")
        page = ctx.new_page()
        page.clock.set_fixed_time(datetime.datetime(2026, 10, 26, 10, 0, 0))
        f = Film(page, aspect, lang, frames)
        # 1 title
        f.card("open")
        # 2 portfolio
        f.cap = (C["portfolio"]["k"][lang], C["portfolio"]["t"][lang])
        f.goto(f"/room.html?as=staff{q}", ".rrp-kpis")
        f.hold(1.6)
        f.click('[data-pf="attn"]', 0.9)
        f.hold(2.2)
        f.click('[data-pf="all"]', 0.6)
        f.hold(0.8)
        # 3 open complex A
        f.cap = (C["open"]["k"][lang], C["open"]["t"][lang])
        f.set_caption(*f.cap)
        f.click(f'tr[data-open="{A}"] td.nm' if aspect == "16x9" else f'button[data-open="{A}"]', 0.9, wait_after="[data-consent] .rrp-consent__big", settle=900)
        f.hold(3.0)
        # 4 the facade and one apartment
        f.set_caption(C["apt"]["k"][lang], C["apt"]["t"][lang])
        f.scroll_to(".rrp-sheet", 1.0, 0.08)
        f.hold(0.6)
        f.click('[data-apt="b1-f4-3"]', 0.9, wait_after="[data-ed-log] time", settle=700)
        if aspect != "16x9":
            f.scroll_to("[data-drawer]", 0.9, 0.05)
        f.hold(1.2)
        for i in (0, 1):
            f.click(f'[data-own]:nth-child({i + 1}) [data-o="signed"]', 0.5, settle=150)
        page.select_option("[data-ed='status']", "consented")
        f.move_to("[data-ed='status']", 0.5)
        f.hold(0.5)
        f.click('[data-ed-doc="signed_agreement"]', 0.5, settle=150)
        f.click('[data-ed-doc="ownership_nesach"]', 0.4, settle=150)
        if aspect != "16x9":
            f.scroll_to("[data-ed-save]", 0.7, 0.35)
        f.set_caption(C["saved"]["k"][lang], C["saved"]["t"][lang])
        f.click("[data-ed-save]", 0.6, settle=900)
        page.wait_for_function("(() => { const m = document.querySelector('[data-ed-msg]'); return m && m.textContent.length > 3 && m.textContent.indexOf('...') < 0; })()")
        f.hold(1.0)
        if aspect != "16x9":
            f.scroll_to(".rrp-logh", 0.9, 0.3)
        else:
            f.move_to(".rrp-log li", 0.6)
        f.hold(2.4)
        # 5 the law
        f.set_caption(C["law"]["k"][lang], C["law"]["t"][lang])
        f.scroll_to("[data-law]", 1.1, 0.06)
        f.move_to(".rrp-lawlist > li:nth-child(1)", 0.6, 0.15)
        f.hold(1.6)
        f.move_to(".rrp-lawlist > li:nth-child(2) .rrp-lawb li:nth-child(3)", 0.8)
        f.hold(1.8)
        f.move_to(".rrp-lawlist > li:nth-child(3) .rrp-lawb li:nth-child(1)", 0.7)
        f.hold(1.6)
        # 6 what is missing
        f.set_caption(C["missing"]["k"][lang], C["missing"]["t"][lang])
        f.scroll_to(".rrp-tasks", 1.0, 0.06)
        f.move_to(".rrp-tasks li:nth-child(2)", 0.6)
        f.hold(3.0)
        # 7 updates and WhatsApp
        f.set_caption(C["updates"]["k"][lang], C["updates"]["t"][lang])
        page.evaluate("window.scrollTo(0, 0)")
        f.click('[data-tab="updates"]', 0.8, wait_after="[data-up-text]", settle=500)
        f.scroll_to("[data-up-text]", 0.6, 0.15)
        f.type_into("[data-up-text]", T["update_text"][lang], 2.4)
        f.click("[data-up-send]", 0.6, wait_after="[data-up-msg] a", settle=500)
        f.scroll_to("[data-up-msg]", 0.5, 0.3)
        f.move_to("[data-up-msg] a", 0.7)
        f.highlight("[data-up-msg] a", True)
        f.hold(2.6)
        f.highlight("[data-up-msg] a", False)
        # 8 report
        f.set_caption(C["report"]["k"][lang], C["report"]["t"][lang])
        page.evaluate("window.scrollTo(0, 0)")
        f.click('[data-tab="report"]', 0.8, wait_after=".rrp-rep", settle=500)
        f.move_to("[data-print]", 0.6)
        f.hold(1.4)
        f.scroll_to(".rrp-rep table", 1.4, 0.1)
        f.hold(2.0)
        # 9 what a neighbour sees
        f.cap = (C["neighbor"]["k"][lang], C["neighbor"]["t"][lang])
        f.goto(f"/room.html?as=neighbor&space={A}{q}", ".rrp-nb")
        f.place_cursor(False)
        f.hold(1.4)
        f.scroll_to(".rrp-nb .rrp-status", 1.2, 0.3)
        f.hold(3.2)
        # 10 end
        f.card("end")
        b.close()
    # assemble
    lst = os.path.join(frames, "list.txt")
    with open(lst, "w", encoding="utf-8") as fh:
        for fn, s in f.list:
            fh.write(f"file '{fn.replace(os.sep, '/')}'\nduration {s:.4f}\n")
        fh.write(f"file '{f.list[-1][0].replace(os.sep, '/')}'\n")
    out = os.path.join(FILM, f"renewal-room-{lang}-{aspect}.mp4")
    w, h = (1920, 1080) if aspect == "16x9" else (1080, 1920)
    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf", f"scale={w}:{h}:flags=lanczos,fps={FPS},format=yuv420p",
           "-c:v", "libx264", "-profile:v", "high", "-crf", "19", "-preset", "medium", "-movflags", "+faststart", "-an", out]
    subprocess.run(cmd, check=True, capture_output=True)
    total = sum(s for _, s in f.list)
    info = {"file": os.path.basename(out), "seconds": round(total, 2), "frames_captured": f.n, "capture_seconds": round(time.time() - t0)}
    print(json.dumps(info))
    return info


if __name__ == "__main__":
    aspect = sys.argv[1] if len(sys.argv) > 1 else "16x9"
    lang = sys.argv[2] if len(sys.argv) > 2 else "he"
    run(aspect, lang)
