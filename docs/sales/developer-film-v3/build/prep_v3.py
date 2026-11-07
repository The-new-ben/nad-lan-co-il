# -*- coding: utf-8 -*-
"""Gather every picture the film page draws into the shared web folder, and hand it a variant's timeline (local only).

  python prep_v3.py [--variant <name>] [--assets]

- always: the variant's timeline (made by vo_build.py) -> <WORK>/web/timelines/<name>.json (film.html reads ?tl=timelines/<name>.json)
- with --assets, or when <WORK>/web/assets.json is missing: the pictures themselves, shared by every variant
  - from v2 (<WORK>/v2_assets.json and, if it still exists, v2's scratch web folder): Ben's clips (ben/<clip>), the Rainbow stage
    screencasts (cast/stage_h, cast/stage_v), the French page scroll (cast/fr), land.json, the French phone page
  - the v3 screencasts (capture_room.py, capture_v3.py; raw frames in <captures>/<x>/<cast> or <WORK>/casts_raw), resampled to a
    constant 30 fps by their CDP timestamps, with the named moments ("marks") turned into seconds from the start of each cast
  - stills: the Rainbow page elements (capture_rainbow.py), the room, the planner's five steps, our other pages
  - the wall of renders: twelve of OUR OWN renders from the plugin's project-stage tours (Kikar Hamedina cards, Rainbow and DUO
    facility panoramas, centre-cropped); no developer's image, no logo
"""
import json, os, shutil, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import variant as VAR

S, CAP, WEB = VAR.WORK, os.path.join(VAR.ROOT, "captures"), VAR.WEB
V2 = "C:/Users/777/AppData/Local/Temp/claude/231dc6a3026aa599/f8200c1d-6798-4a3e-8a9f-7b12503e42b2/scratchpad/film2/web"   # v2's work folder (may be gone; its parts are already in WEB)
PS = r"C:\Users\777\nad-lan\nad-lan-co-il\plugins\nadlan-config\assets\project-stage"
WALL = ["hamedina/tour/living-c30w-day-card.jpg", "hamedina/tour/balcony-c30w-sunset-card.jpg", "hamedina/tour/fac-pool-c-card.jpg",
        "rainbow/tour/fac-roofpool.jpg", "hamedina/tour/living-c30w-evening-card.jpg", "hamedina/tour/bedroom-c30nw-day-card.jpg",
        "rainbow/tour/fac-lobby.jpg", "hamedina/tour/fac-spa-c-card.jpg", "hamedina/tour/twist-c20w-day-card.jpg",
        "duo/tour/fac-lobby.jpg", "hamedina/tour/fac-gym-c-card.jpg", "rainbow/tour/fac-club.jpg"]


def resample(src_dir, name, fps=30):
    L = json.load(open(os.path.join(src_dir, "frames.json")))
    F = [x for x in L if "f" in x]; t0 = F[0]["t"]; total = F[-1]["t"] - t0
    d = os.path.join(WEB, "cast", name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    j = 0; n = int(total * fps) + 1
    for k in range(n):
        t = t0 + k / fps
        while j + 1 < len(F) and F[j + 1]["t"] <= t:
            j += 1
        shutil.copyfile(os.path.join(src_dir, F[j]["f"]), os.path.join(d, "%04d.jpg" % (k + 1)))
    marks = {}
    for x in L:
        if "mark" in x:
            after = x["after"]; marks[x["mark"]] = round(F[min(after, len(F)) - 1]["t"] - t0, 3) if after else 0
    im = Image.open(os.path.join(d, "0001.jpg"))
    return {"frames": n, "seconds": round(total, 2), "w": im.size[0], "h": im.size[1], "marks": marks}


def wall():
    d = os.path.join(WEB, "wall"); os.makedirs(d, exist_ok=True)
    for i, f in enumerate(WALL):
        im = Image.open(os.path.join(PS, f)).convert("RGB")
        w, h = im.size
        if w == 2 * h:   # an equirectangular panorama: the centre, at about 16:10
            cw = int(w * 0.24); ch = int(cw * 10 / 16); im = im.crop((int(w * 0.38), int(h * 0.5 - ch * 0.55), int(w * 0.38) + cw, int(h * 0.5 - ch * 0.55) + ch))
        else:
            ch = int(w * 10 / 16)
            if ch <= h:
                im = im.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch))
        im = im.resize((960, 600), Image.LANCZOS)
        im.save(os.path.join(d, "w%02d.jpg" % (i + 1)), quality=88)
    return WALL


def assets():
    os.makedirs(os.path.join(WEB, "img"), exist_ok=True)
    for sub in ["ben", "cast/stage_h", "cast/stage_v", "cast/fr"]:
        dst = os.path.join(WEB, sub)
        if not os.path.isdir(dst):
            shutil.copytree(os.path.join(V2, sub), dst)
    for f in ("land.json", os.path.join("img", "fr_phone_full.png")):
        if not os.path.exists(os.path.join(WEB, f)):
            shutil.copyfile(os.path.join(V2, f), os.path.join(WEB, f))
    v2 = json.load(open(os.path.join(S, "v2_assets.json")))
    meta = {"ben": v2["ben"], "cast": {k: v2["cast"][k] for k in ["stage_h", "stage_v", "fr"]}}
    casts = {"t360_h": "tour360/t360_cast_1920x1080", "t360_v": "tour360/t360_cast_1080x1920",
             "room_h": "room/room_cast_1920x1080", "room_v": "room/room_cast_1080x1920",
             "walk_h": "walk/walk_cast_1920x1080", "walk_v": "walk/walk_cast_1080x1920",
             "pg_mort": "pages/pg_cast_mortgage-calculator", "pg_tax": "pages/pg_cast_purchase-tax-calculator"}
    for name, rel in casts.items():
        src = os.path.join(CAP, rel)
        if not os.path.isdir(src):   # the raw screencast frames are kept in the scratch folder, not in the repo
            src = os.path.join(S, "casts_raw", rel)
        if os.path.isdir(src):
            meta["cast"][name] = resample(src, name); print(name, meta["cast"][name])
        else:
            print("MISSING", src)
    for sub in ["rainbow", "room", "planner", "pages", "tour360", "walk", "hamedina"]:
        dd = os.path.join(CAP, sub)
        for f in os.listdir(dd) if os.path.isdir(dd) else []:
            if f.endswith(".png"):
                shutil.copyfile(os.path.join(dd, f), os.path.join(WEB, "img", f))
    meta["wall"] = wall()
    # crops of the captured pages: the room's notes list (h and v), the price box of the Rainbow page without its table of
    # neighbouring projects (no other project's name on screen)
    for tag, k in (("1920x1080", "h"), ("1080x1920", "v")):
        Image.open(os.path.join(CAP, "room", f"room_plan_{tag}.png")).crop((28, 545, 377, 800)).save(os.path.join(WEB, "img", f"room_notes_{k}.png"))
    Image.open(os.path.join(CAP, "rainbow", "rb_price.png")).crop((1300, 0, 2800, 440)).save(os.path.join(WEB, "img", "rb_price_top.png"))
    Image.open(os.path.join(CAP, "rainbow", "rb_deals.png")).crop((1640, 40, 2800, 450)).save(os.path.join(WEB, "img", "rb_deals_top.png"))
    # where the room's parts are in the room screencasts (CSS px of the capture), for the film's highlight ring
    meta["roomUI"] = {"tiles": {"room_h": [[28, 104, 348, 152], [264, 262, 113, 77], [146, 262, 113, 77], [28, 262, 113, 77], [264, 345, 113, 77]],
                                "room_v": [[28, 104, 348, 152], [264, 262, 113, 77], [146, 262, 113, 77], [28, 262, 113, 77], [264, 345, 113, 77]]},
                      "plan": {"room_h": [945, 405, 590, 345], "room_v": [583, 866, 452, 262]},
                      "hero": [840, 300, 348, 104]}
    json.dump(meta, open(os.path.join(WEB, "assets.json"), "w"), indent=1)
    print("assets ok", WEB)


if __name__ == "__main__":
    VA = VAR.load(); PA = VAR.Paths(VA)
    if "--assets" in sys.argv or not os.path.exists(os.path.join(WEB, "assets.json")):
        assets()
    os.makedirs(os.path.dirname(PA.tl_web), exist_ok=True)
    shutil.copyfile(os.path.join(PA.audio, "timeline.json"), PA.tl_web)
    print("timeline ->", PA.tl_web)
