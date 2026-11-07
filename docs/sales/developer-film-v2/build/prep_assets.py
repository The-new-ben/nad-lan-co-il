# -*- coding: utf-8 -*-
"""Prepare every picture the film page draws (local only).

  python prep_assets.py <scratch>/film2

- Ben's film (1.11.2026): the recordings and interior shots, cut out of his cream frames (crop rectangles below, in his
  1280x720 picture), upscaled x2 (lanczos), 30 fps JPEG sequences -> web/ben/<clip>/0001.jpg ...
- The live screencasts (stage 16:9 and 9:16, the French page scroll): resampled to a constant 30 fps by their CDP timestamps
  -> web/cast/<name>/0001.jpg ...
- Stills (stage, English page tile and FAQ, French bars, the planner steps from capture_planner.py) -> web/img/
- World land outline (world-atlas 2.0.2, land-50m, public Natural Earth data) -> web/land.json as lon/lat rings
- Contact sheet of the first frame of every Ben clip -> <scratch>/film2/crops_check.jpg
"""
import json, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

FF = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
BEN = r"C:\Users\777\.claude\uploads\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\479ba69e-VID-20261101-WA0001.mp4"
S = sys.argv[1]
WEB = os.path.join(S, "web"); LIVE = os.path.join(S, "live")

# name: (from s, to s, x0, y0, x1, y1) in Ben's 1280x720 frame
CLIPS = {
    "g_fr":    (9.05, 10.40, 154, 138, 1126, 615),   # Google search typed in French
    "view":    (30.70, 32.40, 154, 138, 1126, 640),  # the view from floor 25 toward the sea, example apartment (no furniture)
    "furn":    (40.50, 42.60, 154, 150, 1126, 640),  # furnished, sunset
    "ph_il":   (58.50, 60.90, 468, 138, 812, 632),   # Hotjar recording, Israel, phone
    "desk_il": (61.30, 63.60, 231, 195, 1126, 618),  # Hotjar recording, Israel, desktop, mouse path
    "brit":    (64.00, 66.10, 87, 254, 593, 515),    # UK desktop panel (building inside as in Ben's film)
    "ph_fr":   (64.00, 66.10, 676, 210, 910, 546),   # France, phone
    "ph_au":   (64.00, 66.10, 968, 190, 1206, 566),  # Australia, phone, mouse path
    "heat_d":  (66.60, 71.20, 114, 191, 712, 588),   # click heatmap, desktop (empty 3D canvas area)
    "heat_m":  (66.60, 71.20, 814, 221, 1159, 578),  # click heatmap, phone
    "contact": (72.10, 73.90, 231, 195, 1126, 618),  # the click on contact
}


def ff(*a):
    subprocess.run([FF, "-y", "-loglevel", "error", *[str(x) for x in a]], check=True)


def ben():
    meta = {}
    for name, (a, b, x0, y0, x1, y1) in CLIPS.items():
        d = os.path.join(WEB, "ben", name)
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
        w, h = x1 - x0, y1 - y0
        ff("-ss", a, "-i", BEN, "-t", round(b - a, 3), "-vf", f"crop={w}:{h}:{x0}:{y0},scale={w*2}:{h*2}:flags=lanczos",
           "-q:v", 3, os.path.join(d, "%04d.jpg"))
        n = len([f for f in os.listdir(d) if f.endswith(".jpg")])
        meta[name] = {"from": a, "to": b, "crop": [x0, y0, x1, y1], "frames": n, "w": w * 2, "h": h * 2}
    return meta


def resample(src_dir, name, fps=30):
    L = json.load(open(os.path.join(src_dir, "frames.json")))
    t0 = L[0]["t"]; total = L[-1]["t"] - t0
    d = os.path.join(WEB, "cast", name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    j = 0; n = int(total * fps) + 1
    for k in range(n):
        t = t0 + k / fps
        while j + 1 < len(L) and L[j + 1]["t"] <= t:
            j += 1
        shutil.copyfile(os.path.join(src_dir, L[j]["f"]), os.path.join(d, "%04d.jpg" % (k + 1)))
    im = Image.open(os.path.join(d, "0001.jpg"))
    return {"frames": n, "seconds": round(total, 2), "w": im.size[0], "h": im.size[1]}


def stills():
    d = os.path.join(WEB, "img"); os.makedirs(d, exist_ok=True)
    for f in ["stage_floor23_1920x1080.png", "stage_floor23_1080x1920.png", "stage_hero_1920x1080.png", "stage_hero_1080x1920.png",
              "en_price_tile.png", "en_faq.png", "fr_topbar_x4.png", "fr_langbar_x4.png", "fr_top_1920.png", "fr_top_390.png", "fr_phone_full.png"]:
        shutil.copyfile(os.path.join(LIVE, f), os.path.join(d, f))
    for k in range(1, 6):   # capture_planner.py: the planner's own five steps, the project field filled as "הפרויקט שלכם"
        shutil.copyfile(os.path.join(S, "planner", f"plan{k}.png"), os.path.join(d, f"plan{k}.png"))
    # the first 2 questions of the FAQ only (keeps the block legible at film size)
    faq = Image.open(os.path.join(d, "en_faq.png"))
    faq.crop((0, 0, faq.size[0], min(faq.size[1], 590))).save(os.path.join(d, "en_faq2.png"))


def land():
    topo = json.load(open(os.path.join(S, "dl", "land-50m.json")))
    sc, tr = topo["transform"]["scale"], topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append([round(x * sc[0] + tr[0], 3), round(y * sc[1] + tr[1], 3)])
        arcs.append(pts)

    def ring(ix):
        out = []
        for i in ix:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(a if not out else a[1:])
        return out
    rings = []
    for g in topo["objects"]["land"]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        for poly in polys:
            for r in poly:
                pts = ring(r)
                # keep the part of the world the film shows (the Americas' east coast to Iran)
                if any(-100 < p[0] < 60 and 15 < p[1] < 72 for p in pts):
                    rings.append(pts)
    json.dump(rings, open(os.path.join(WEB, "land.json"), "w"))
    return len(rings)


def check_sheet(meta):
    font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22)
    tiles = []
    for name in CLIPS:
        im = Image.open(os.path.join(WEB, "ben", name, "0001.jpg")).convert("RGB")
        im.thumbnail((520, 400)); t = Image.new("RGB", (540, 440), "white"); t.paste(im, (10, 34))
        ImageDraw.Draw(t).text((10, 6), f"{name} {meta[name]['frames']}f", fill="black", font=font); tiles.append(t)
    cols = 4; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 540, rows * 440), "#888")
    for i, t in enumerate(tiles):
        sh.paste(t, ((i % cols) * 540, (i // cols) * 440))
    sh.save(os.path.join(S, "crops_check.jpg"), quality=85)


if __name__ == "__main__":
    os.makedirs(WEB, exist_ok=True)
    meta = {"ben": ben()}
    meta["cast"] = {"stage_h": resample(os.path.join(LIVE, "stage_cast_1920x1080"), "stage_h"),
                    "stage_v": resample(os.path.join(LIVE, "stage_cast_1080x1920"), "stage_v"),
                    "fr": resample(os.path.join(LIVE, "fr_cast_1920"), "fr")}
    stills()
    meta["land_rings"] = land()
    json.dump(meta, open(os.path.join(WEB, "assets.json"), "w"), indent=1)
    check_sheet(meta["ben"])
    print(json.dumps(meta, indent=1))
