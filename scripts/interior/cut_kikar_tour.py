# -*- coding: utf-8 -*-
"""Kikar Hamedina P9c: the example apartment's pictures for the web, cut from the P9b Cycles finals (design system v104.2).

The sources are the prototype's final renders (scripts/interior/_renders/kikar/final-*.png, 8-bit RGBA from Blender; not committed),
or, when they are gone, the committed JPGs in docs/research/2026-09-30-kikar-hamedina/interiors-proto/. The output is the fleet's
naming and sizes, in plugins/nadlan-config/assets/project-stage/hamedina/tour/:

  <room>-<tower><floor><side>-<time>[-2k|-card|-thumb].<jpg|webp>
    room  living, bedroom, balcony, living360 (the 360 panorama), twist (the same window on another floor)
    side  w = the side of the plate that faces west on floor 30 (it turns with the tower), nw = the corner beside it
    time  day (21.9, 14:30), sunset (17:36), evening (19:06)
  the 360: 4096 x 2048 (no suffix) and 2048 x 1024 (-2k), JPG like the fleet's tours + WebP (what the page's viewer loads);
           -card is the fleet's straight view through the window (cut_tour.py's projection), 1200 x 675, and -thumb its 480 px
  a still: -2k 2048 x 1152 (WebP), -card 1200 x 675 (JPG + WebP), -thumb 480 x 270 (WebP)
  twist:   -card 1200 x 675 (JPG + WebP), -thumb 480 x 270 (WebP) (rendered at 1280 x 720, so no -2k)

Nothing on the page loads any of these until the visitor presses "היכנסו לדירה לדוגמה".

  python scripts/interior/cut_kikar_tour.py        (writes the files and prints the byte budget)
"""
import io, json, math, os, subprocess, sys
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RENDERS = os.path.join(HERE, "_renders", "kikar")
PROTO = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina", "interiors-proto")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina", "tour")

# the prototype's name -> the release name (tower C, floor 30; the twist frames on floors 20 / 30 / 38, the same window)
STILLS = [("living-sunset", "living-c30w-sunset"), ("living-day", "living-c30w-day"), ("living-evening", "living-c30w-evening"),
          ("bedroom-day", "bedroom-c30nw-day"), ("balcony-sunset", "balcony-c30w-sunset")]
TWIST = [("twist-floor20", "twist-c20w-day"), ("twist-floor30", "twist-c30w-day"), ("twist-floor38", "twist-c38w-day")]
PANO = ("living360-sunset", "living360-c30w-sunset")
Q_JPG, Q_WEBP, Q_WEBP_PANO = 84, 80, 78


def source(name, w):
    png = os.path.join(RENDERS, "final-%s.png" % name)
    if os.path.exists(png):
        return Image.open(png).convert("RGB"), "final-%s.png" % name
    jpg = os.path.join(PROTO, name + ".jpg")
    return Image.open(jpg).convert("RGB"), os.path.relpath(jpg, REPO)


def fit(im, w):
    return im if im.width == w else im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)


def jpg(im, path, q=Q_JPG):
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)


def webp(im, path, q=Q_WEBP):
    im.save(path, "WEBP", quality=q, method=6)


def main():
    os.makedirs(OUT, exist_ok=True)
    made, srcs = [], {}
    for pname, rname in STILLS:
        im, s = source(pname, 2048)
        srcs[rname] = s
        webp(fit(im, 2048), os.path.join(OUT, rname + "-2k.webp"))
        card = fit(im, 1200)
        jpg(card, os.path.join(OUT, rname + "-card.jpg"))
        webp(card, os.path.join(OUT, rname + "-card.webp"))
        webp(fit(im, 480), os.path.join(OUT, rname + "-thumb.webp"), 78)
        made += [rname + x for x in ("-2k.webp", "-card.jpg", "-card.webp", "-thumb.webp")]
    for pname, rname in TWIST:
        im, s = source(pname, 1280)
        srcs[rname] = s
        card = fit(im, 1200)
        jpg(card, os.path.join(OUT, rname + "-card.jpg"))
        webp(card, os.path.join(OUT, rname + "-card.webp"))
        webp(fit(im, 480), os.path.join(OUT, rname + "-thumb.webp"), 78)
        made += [rname + x for x in ("-card.jpg", "-card.webp", "-thumb.webp")]
    # the 360: the fleet's JPGs through cut_tour.py (the same projection for the card), then the WebPs
    pname, rname = PANO
    png = os.path.join(RENDERS, "final-%s.png" % pname)
    if os.path.exists(png):
        r = subprocess.run([sys.executable, os.path.join(HERE, "cut_tour.py"), png, OUT, rname], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("cut_tour: " + r.stderr[-400:])
        srcs[rname] = "final-%s.png" % pname
    else:  # the committed cut (identical projection)
        for suf in ("", "-2k", "-card"):
            Image.open(os.path.join(PROTO, pname + suf + ".jpg")).save(os.path.join(OUT, rname + suf + ".jpg"), "JPEG", quality=82, optimize=True, progressive=True)
        srcs[rname] = os.path.relpath(os.path.join(PROTO, pname + ".jpg"), REPO)
    pano = Image.open(png).convert("RGB") if os.path.exists(png) else Image.open(os.path.join(PROTO, pname + ".jpg")).convert("RGB")
    webp(pano, os.path.join(OUT, rname + ".webp"), Q_WEBP_PANO)
    webp(pano.resize((pano.width // 2, pano.height // 2), Image.LANCZOS), os.path.join(OUT, rname + "-2k.webp"), Q_WEBP_PANO)
    card = Image.open(os.path.join(OUT, rname + "-card.jpg")).convert("RGB")
    webp(fit(card, 480), os.path.join(OUT, rname + "-thumb.webp"), 78)
    made += [rname + x for x in (".jpg", "-2k.jpg", "-card.jpg", ".webp", "-2k.webp", "-thumb.webp")]

    sizes = {f: os.path.getsize(os.path.join(OUT, f)) for f in sorted(made)}
    kb = lambda n: round(n / 1024, 1)
    # the byte budget per visitor action (what the album and the viewer really request, see world/example.js)
    first = ["living-c30w-sunset-card.webp"] + [r + "-thumb.webp" for _, r in STILLS] + [PANO[1] + "-thumb.webp"] + [r + "-thumb.webp" for _, r in TWIST]
    budget = {
        "album_open_phone": sum(sizes[f] for f in first),
        "album_open_desktop_hero_2k": sum(sizes[f] for f in first) - sizes["living-c30w-sunset-card.webp"] + sizes["living-c30w-sunset-2k.webp"],
        "viewer_360_first": sizes[PANO[1] + "-2k.webp"],
        "viewer_360_sharp": sizes[PANO[1] + "-2k.webp"] + sizes[PANO[1] + ".webp"],
        "every_file_on_disk": sum(sizes.values()),
    }
    print(json.dumps({"files": {f: kb(n) for f, n in sizes.items()}, "budget_kb": {k: kb(v) for k, v in budget.items()}, "sources": srcs}, ensure_ascii=False, indent=1))
    io.open(os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina", "p9c-assets.json"), "w", encoding="utf-8").write(
        json.dumps({"files_bytes": sizes, "budget_bytes": budget, "sources": srcs}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
