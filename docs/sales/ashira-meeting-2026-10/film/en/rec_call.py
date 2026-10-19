# -*- coding: utf-8 -*-
"""HAD-543: the English explainer film of the shared viewing room (a LIVE LiveKit video call on the Ashira page), filmed from
both sides in two separate Chrome browsers, the room's own interface in English, a drawn cursor, narration per scene.
The representative is identified to the REST API with the site's application password, injected by this harness into the
room's own requests (nothing typed). Camera feeds are demo clips from generated portraits (said in the end card).
python rec_call.py -> call-en.mp4 (1920x1080)"""
import json, os, shutil, subprocess, sys, time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "audio")
FEEDS = r"C:\Users\777\nad-lan\_private-research\livekit\proof-film"
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "rc"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, AUTH = ns["req"], ns["AUTH"]
N = json.load(open(os.path.join(H, "narration.json"), encoding="utf-8"))["films"]["call"]
D = json.load(open(os.path.join(A, "durations.json"), encoding="utf-8"))
s, r, _ = req("POST", "/wp-json/nadlan/v1/room", {"post": 4744})
if s not in (200, 201) or not r.get("ok"):
    sys.exit("room: %s %s" % (s, r))
JOIN, PAGE = r["join_url"], r["join_url"].split("?")[0]
VW, VH = 1280, 800
CUR = r"""(()=>{if(window.__nlc)return;window.__nlc=1;const s=document.createElement('style');s.textContent=`
#nlcur{position:fixed;left:0;top:0;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;border:3px solid #fff;background:rgba(31,95,168,.35);box-shadow:0 0 0 2px rgba(15,34,51,.6);z-index:2147483647;pointer-events:none}
.nlrip{position:fixed;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;border:3px solid #1F5FA8;z-index:2147483646;pointer-events:none;animation:nlr .6s ease-out forwards}
@keyframes nlr{to{transform:scale(3.2);opacity:0}}
#nlend{position:fixed;inset:0;z-index:2147483647;background:#0F2233;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-family:'Segoe UI',Arial;direction:ltr}
#nlend b{font-size:44px}#nlend span{font-size:22px;color:#D9E7F7}`;document.head.appendChild(s);
const c=document.createElement('div');c.id='nlcur';document.body.appendChild(c);
addEventListener('mousemove',e=>{c.style.left=e.clientX+'px';c.style.top=e.clientY+'px'},true);
addEventListener('mousedown',e=>{const r=document.createElement('div');r.className='nlrip';r.style.left=e.clientX+'px';r.style.top=e.clientY+'px';document.body.appendChild(r);setTimeout(()=>r.remove(),700)},true);})()"""
ARGS = ["--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream", "--autoplay-policy=no-user-gesture-required", "--hide-scrollbars"]
LOG = []


def browser(p, feed, x):
    b = p.chromium.launch(channel="chrome", headless=False, args=ARGS + ["--use-file-for-fake-video-capture=" + os.path.join(FEEDS, feed), "--window-position=%d,0" % x])
    raw = os.path.join(H, "raw-call-" + feed[:-4]); shutil.rmtree(raw, ignore_errors=True)
    ctx = b.new_context(viewport={"width": VW, "height": VH}, locale="en-US", permissions=["camera", "microphone"], record_video_dir=raw, record_video_size={"width": VW, "height": VH})
    ctx.add_init_script("try{sessionStorage.setItem('nltg:lang','en')}catch(e){}")
    return b, ctx


def rep_routes(pg):
    def doc(route):
        resp = route.fetch()
        route.fulfill(response=resp, body=resp.text().replace('&quot;canRep&quot;:false', '&quot;canRep&quot;:true').replace('&quot;user&quot;:&quot;&quot;', '&quot;user&quot;:&quot;Dana, NadLan&quot;'))
    def api(route):
        hd = {k: v for k, v in route.request.headers.items() if k.lower() != "x-wp-nonce"}
        hd["Authorization"] = AUTH
        route.continue_(headers=hd)
    pg.route(lambda u: "room=" in u and "/wp-json/" not in u, doc)
    pg.route("**/wp-json/nadlan/v1/room**", api)


def glide_click(pg, loc, after=900):
    loc.scroll_into_view_if_needed(timeout=10000); bb = loc.bounding_box()
    pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2, steps=24); pg.wait_for_timeout(200)
    pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.up(); pg.wait_for_timeout(after)


def hover(pg, loc, after=1200):
    loc.scroll_into_view_if_needed(timeout=10000); bb = loc.bounding_box()
    pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2, steps=30); pg.wait_for_timeout(after)


with sync_playwright() as p:
    rb, rctx = browser(p, "rep.y4m", 0); rep = rctx.new_page(); rep_routes(rep); tr0 = time.time()
    bb_, bctx = browser(p, "buyer.y4m", 1290); buy = bctx.new_page(); tb0 = time.time()
    # set-up, before the film's clock: the representative enters the room; the buyer is on the project page
    rep.goto(JOIN, wait_until="load", timeout=120000); rep.wait_for_selector("#nltg-name", timeout=60000)
    rep.fill("#nltg-name", "Dana, NadLan"); rep.click('.nltg-roles [data-role="rep"]'); rep.click(".nltg-card .go"); rep.wait_for_timeout(6000)
    for b_ in (rep, ):
        try:
            b_.locator(".nltg-scrim button:visible, .nltg-modal button:visible", has_text="Close").first.click(timeout=3000)
        except Exception:
            pass
    buy.goto(PAGE + "?nlv=callfilm", wait_until="load", timeout=120000); buy.wait_for_timeout(3000)
    for pg in (rep, buy):
        pg.evaluate(CUR)
    F0 = time.time()

    def sc(i, fn):
        sid, text = N[i]; st = time.time() - F0; t1 = time.time()
        for pg in (rep, buy):
            pg.evaluate(CUR)
        try:
            fn(); ok = "ok"
        except Exception as e:
            ok = "skip: " + str(e)[:90]
        left = D[f"call-{i:02d}-{sid}"] + 0.7 - (time.time() - t1)
        if left > 0:
            rep.wait_for_timeout(int(left * 1000))
        LOG.append({"i": i, "id": sid, "start": round(st, 2), "text": text, "status": ok}); print(i, sid, round(st, 1), ok)

    def s0():
        hover(buy, buy.locator("a:visible, button:visible", has_text="שיחת וידאו עם נציג").first, 1500)
    def s1():
        glide_click(rep, rep.locator("button:visible", has_text="Invite someone").first, 2500)
        hover(buy, buy.locator("a:visible, button:visible", has_text="שיחת וידאו עם נציג").first, 800)
    def s2():
        try:
            rep.locator("button:visible", has_text="Close").first.click(timeout=3000)
        except Exception:
            pass
        buy.goto(JOIN, wait_until="load", timeout=120000); buy.wait_for_selector("#nltg-name", timeout=60000); buy.evaluate(CUR)
        glide_click(buy, buy.locator("#nltg-name"), 300); buy.keyboard.type("Levi family", delay=90)
        glide_click(buy, buy.locator('.nltg-roles [data-role="buyer"]'), 600)
    def s3():
        glide_click(buy, buy.locator(".nltg-card .go"), 4500); buy.evaluate(CUR)
    def s4():
        glide_click(rep, rep.locator("button:visible", has_text="Follow me").first, 2200)
        glide_click(rep, rep.locator('.nltg-modes [data-mode="view"]:visible, .nltg-modesel [data-mode="view"]').first, 3200)
        glide_click(rep, rep.locator('.nltg-modes [data-mode="inside"]:visible, .nltg-modesel [data-mode="inside"]').first, 2500)
    def s5():
        glide_click(buy, buy.locator("button:visible", has_text="Invite someone").first, 3000)
        try:
            buy.locator("button:visible", has_text="Close").first.click(timeout=3000)
        except Exception:
            pass
    def s6():
        glide_click(rep, rep.locator('.nltg-modes [data-mode="building"]:visible, .nltg-modesel [data-mode="building"]').first, 1500)
        hover(buy, buy.locator("button:visible, a:visible", has_text="file").first, 1500)
    def s7():
        for pg in (rep, buy):
            pg.evaluate("()=>{const e=document.createElement('div');e.id='nlend';e.innerHTML='<b>The shared viewing room · NadLan</b><span>The call is not recorded · demo camera images · AI voice</span>';document.body.appendChild(e)}")

    for i, fn in enumerate((s0, s1, s2, s3, s4, s5, s6, s7)):
        sc(i, fn)
    LOG.append({"videos": [rep.evaluate("document.querySelectorAll('.nltg-tile video').length"), buy.evaluate("document.querySelectorAll('.nltg-tile video').length")]})
    rv, bv = rep.video.path(), buy.video.path(); rctx.close(); bctx.close(); rb.close(); bb_.close()

json.dump({"log": LOG, "rv": rv, "bv": bv, "offr": F0 - tr0, "offb": F0 - tb0}, open(os.path.join(H, "call-log.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
subprocess.run([sys.executable, os.path.join(H, "compose_call.py")], check=True)
