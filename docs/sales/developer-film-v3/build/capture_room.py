# -*- coding: utf-8 -*-
"""The shared viewing room (TogetherRoom, inc/together.php + assets/together/together.js) of the live Rainbow page, staged
for the film with demo participants and demo notes. NOTHING reaches the site's room API: every /wp-json/nadlan/v1/room*
request of this browser is answered here (route.fulfill) and the LiveKit library is not loaded; the page itself is a normal
GET of /projects/rainbow-tel-aviv/?room=<an id that does not exist>, which only prints the room's container. No room, note
or participant is created on the site. Analytics are blocked in this browser.

  python capture_room.py <out_dir> <WxH> [--lk]   stills + a CDP screencast of the room (the plan, the notes, the participants);
                                                  --lk: as live (LiveKit on), the video dock with a stand-in library
                                                  (fake_livekit.mjs, connects to nothing, no cameras: tiles show initials)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\developer-film-v2\build")
from live_common import launch
from capture_tools import Cast
from playwright.sync_api import sync_playwright

ROOM = "filmdemo2345"   # [a-z2-7]{12}, never created on the site
URL = f"https://nad-lan.co.il/projects/rainbow-tel-aviv/?room={ROOM}"
NOW = time.time()
PEOPLE = [
    {"pid": "rep23456", "name": "נועה", "role": "rep", "on": True},
    {"pid": "me234567", "name": "Pierre", "role": "buyer", "on": True},
    {"pid": "cl234567", "name": "Claire", "role": "partner", "on": True},
    {"pid": "lu234567", "name": "Lucas", "role": "friend", "on": True},
    {"pid": "so234567", "name": "Sophie", "role": "designer", "on": True},
]
NOTES = [
    {"id": "n1", "n": 1, "pid": "me234567", "author": "Pierre", "role": "buyer", "t": NOW - 420, "where": "הסלון",
     "text": "Ici, un bureau face à la mer", "change": False, "anchor": {"mode": "plan", "sx": 0.30, "sy": 0.34, "floor": 23}},
    {"id": "n2", "n": 2, "pid": "cl234567", "author": "Claire", "role": "partner", "t": NOW - 300, "where": "המטבח",
     "text": "Un îlot à la place du comptoir ?", "change": True, "anchor": {"mode": "plan", "sx": 0.62, "sy": 0.55, "floor": 23}},
    {"id": "n3", "n": 3, "pid": "so234567", "author": "Sophie", "role": "designer", "t": NOW - 180, "where": "חדר השינה",
     "text": "Parquet chêne clair", "change": False, "anchor": {"mode": "plan", "sx": 0.78, "sy": 0.24, "floor": 23}},
]
STATE = {"m": "plan", "f": 23}
LK = "--lk" in sys.argv   # the room as it runs live (LiveKit on): the video dock, a stand-in library, no cameras


def handler(route):
    u = route.request.url
    path = u.split("/wp-json/nadlan/v1/")[1].split("?")[0]
    if path == "room/token":
        body = {"ok": True, "room": ROOM, "pid": "me234567", "key": "k" * 22, "name": "Pierre", "role": "buyer",
                "leader": "rep23456", "participants": PEOPLE, "rev": 3, "state": STATE, "t": 1,
                **({"mode": "livekit", "url": "wss://film.invalid", "token": "film"} if LK else {"mode": "fallback"})}
    elif path == "room/state":
        body = {"ok": True, "participants": PEOPLE, "leader": "rep23456", "state": STATE, "t": 2, "rev": 3}
    elif path == "room/notes":
        body = {"ok": True, "notes": NOTES, "rev": 3}
    elif path == "room/available":
        body = {"ok": True, "now": True}
    else:
        body = {"ok": False, "error": "film"}
    route.fulfill(status=200, content_type="application/json", body=json.dumps(body, ensure_ascii=False))


if __name__ == "__main__":
    out, size = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    w, h = [int(x) for x in size.split("x")]; tag = f"{w}x{h}"
    with sync_playwright() as p:
        b, ctx = launch(p, w, h)
        ctx.route("**/wp-json/nadlan/v1/room**", handler)
        fake = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_livekit.mjs"), encoding="utf-8").read()
        ctx.route("**/livekit-client**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=fake) if LK else r.abort())
        ctx.add_init_script("window.__filmPeople = " + json.dumps(PEOPLE, ensure_ascii=False) + ";")
        pg = ctx.new_page(); pg.on("pageerror", lambda e: print("[pageerror]", str(e)[:200]))
        r = pg.goto(URL, wait_until="domcontentloaded", timeout=120000)
        log = {"url": URL, "status": r.status, "taken": time.strftime("%Y-%m-%d %H:%M:%S"), "mocked": "all /wp-json/nadlan/v1/room* answered locally"}
        pg.wait_for_timeout(9000)
        pg.screenshot(path=os.path.join(out, f"room_join_{tag}.png"))
        pg.fill("#nltg-name", "Pierre"); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(out, f"room_join_named_{tag}.png"))
        cast = Cast(pg, os.path.join(out, f"room_cast_{tag}"), w, h); cast.start()
        pg.wait_for_timeout(600)
        pg.click(".nltg-card button.go"); pg.wait_for_timeout(5000)
        pg.screenshot(path=os.path.join(out, f"room_in_{tag}.png"))
        log["buttons"] = pg.evaluate("""() => [...document.querySelectorAll('#nltg-root button, .nltg-top button')].filter(b => b.offsetParent)
            .map(b => [b.innerText.trim().slice(0, 30), b.getAttribute('aria-label'), b.className.toString().slice(0, 40)])""")
        for ids in (["rep23456"], ["rep23456"], ["me234567"], ["cl234567"], ["rep23456"]):
            pg.evaluate("ids => window.__filmSpeak && window.__filmSpeak(ids)", ids); pg.wait_for_timeout(900)
        cast.stop()
        pg.screenshot(path=os.path.join(out, f"room_plan_{tag}.png"))
        json.dump(log, open(os.path.join(out, f"room_{tag}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps(log, ensure_ascii=False)[:2000])
        b.close()
