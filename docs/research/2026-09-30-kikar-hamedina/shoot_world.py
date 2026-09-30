# -*- coding: utf-8 -*-
"""Screenshots + fps/bytes report of the shared world module (P5, LOCAL ONLY).

    python docs/research/2026-09-30-kikar-hamedina/shoot_world.py              every shot, desktop 1440x900 and phone 390x844
    python docs/research/2026-09-30-kikar-hamedina/shoot_world.py aerial walk  only these shots
    python docs/research/2026-09-30-kikar-hamedina/shoot_world.py --desktop | --mobile | --nobench

Serves the repo root with python's http.server on 127.0.0.1:8765, opens world-test.html in Chrome (Playwright,
channel "chrome", the local GPU through ANGLE/D3D11), writes world-shots/<shot>-<size>.webp (quality 90) and world-shots/report.json
(load bytes by file, time to ready, draw calls, triangles, fps while orbiting / looking around).
"""
import functools, gzip, http.server, io, json, os, pathlib, socketserver, sys, threading, time

from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = HERE / "world-shots"
OUT.mkdir(exist_ok=True)
PORT = 8765
PAGE = "http://127.0.0.1:%d/docs/research/2026-09-30-kikar-hamedina/world-test.html" % PORT

places = json.load(io.open(REPO / "plugins/nadlan-config/assets/project-stage/hamedina/places.json", encoding="utf-8"))["places"]
pid = lambda name: next(p["id"] for p in sorted(places, key=lambda p: p["dist"]) if p["name"] == name)
ICHILOV_ST = pid("תחנת איכילוב, הקו הסגול")
GYM = pid("הגימנסיה העברית הרצליה")

SHOTS = [
    ("aerial", "mode=aerial&season=9&hour=10"),
    ("aerial-card-tower-B", "mode=aerial&season=9&hour=10&show=tower:B&wa=1"),
    ("aerial-card-ring-building", "mode=aerial&season=9&hour=10&show=block:ring"),
    ("walk-ring", "mode=walk&season=6&hour=17"),
    ("walk-park", "mode=walk&spot=park&season=9&hour=10"),
    ("aerial-card-dog-garden", "mode=aerial&season=9&hour=10&show=feature:dog"),
    ("aerial-card-school", "mode=aerial&season=9&hour=10&show=civic:school"),
    ("tower-C-floor30-out", "mode=tower&tower=C&floor=30&season=9&hour=10"),
    ("tower-C-floor30-window-west", "mode=tower&tower=C&floor=30&facing=270&season=6&hour=9"),
    ("tower-A-floor30-window-north-dec13", "mode=tower&tower=A&floor=30&facing=0&season=12&hour=13"),
    ("tower-B-floor12-out-shade-dec15", "mode=tower&tower=B&floor=12&facing=200&view=out&season=12&hour=15&collapsed=0"),
    ("places-transport", "mode=places&cat=transport"),
    ("places-route-ichilov-station", "mode=places&cat=transport&place=" + ICHILOV_ST),
    ("places-education-route-gymnasium", "mode=places&cat=education&place=" + GYM),
    ("en-aerial", "lang=en&mode=aerial&season=9&hour=10"),
    ("en-tower-A-floor36-window-west", "lang=en&mode=tower&tower=A&floor=36&facing=270&season=9&hour=17"),
]
SIZES = [("desktop", 1440, 900, 1, False), ("mobile", 390, 844, 2, True)]
BENCH = {"aerial", "walk-ring", "tower-C-floor30-window-west", "places-transport"}

args = [a for a in sys.argv[1:] if not a.startswith("--")]
only = set(args)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def serve():
    handler = functools.partial(Quiet, directory=str(REPO))
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def local_sizes():
    out = {}
    for rel in ["plugins/nadlan-config/assets/project-stage/world/world.js", "plugins/nadlan-config/assets/project-stage/world/world.css",
                "plugins/nadlan-config/assets/project-stage/hamedina/world.json", "plugins/nadlan-config/assets/project-stage/hamedina/places.json"]:
        b = (REPO / rel).read_bytes()
        out[rel.split("/")[-2] + "/" + rel.split("/")[-1]] = {"bytes": len(b), "gzip": len(gzip.compress(b, 9))}
    return out


def main():
    httpd = serve()
    report = {"when": time.strftime("%Y-%m-%d %H:%M"), "files": local_sizes(), "shots": {}, "bench": {}, "load": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True,
                                    args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu-rasterization", "--enable-unsafe-swiftshader"])
        for size, w, h, dsf, mobile in SIZES:
            if "--desktop" in sys.argv and size != "desktop":
                continue
            if "--mobile" in sys.argv and size != "mobile":
                continue
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dsf, is_mobile=mobile, has_touch=mobile,
                                      locale="he-IL")
            page = ctx.new_page()
            logs, resp = [], []
            page.on("console", lambda m: logs.append("%s: %s" % (m.type, m.text)))
            page.on("pageerror", lambda e: logs.append("pageerror: %s" % e))

            def on_resp(r):
                try:
                    body = r.body()
                    try:
                        wire = r.request.sizes().get("responseBodySize")
                    except Exception:
                        wire = None
                    resp.append((r.url, len(body), wire))
                except Exception:
                    pass
            page.on("response", on_resp)
            first = True
            for name, q in SHOTS:
                if only and not any(name.startswith(o) for o in only):
                    continue
                resp.clear()
                t0 = time.time()
                page.goto(PAGE + "?" + q, wait_until="load")
                try:
                    page.wait_for_function("window.__ready === true", timeout=180000)
                except Exception as e:
                    print("NOT READY", name, size, e)
                    print("\n".join(logs[-20:]))
                    continue
                page.wait_for_timeout(700)
                png = OUT / ("_%s-%s.png" % (name, size))
                page.screenshot(path=str(png))
                f = OUT / ("%s-%s.webp" % (name, size))
                from PIL import Image
                Image.open(png).convert("RGB").save(f, "WEBP", quality=90, method=6)
                png.unlink()
                st = page.evaluate("() => window.__world.stats()")
                t_ready = page.evaluate("() => window.__tReady")
                report["shots"]["%s-%s" % (name, size)] = {"stats": st, "ready_ms": round(t_ready), "wall_s": round(time.time() - t0, 1),
                                                          "picks": page.evaluate("() => window.__picks || []")[-3:],
                                                          "events": page.evaluate("() => window.__events || []")[-2:],
                                                          "pick": page.evaluate("() => window.__nlpsPick || null")}
                if first:
                    by, wire = {}, {}
                    for url, n, w_ in resp:
                        key = url.split("?")[0].split("/")[-1] or url
                        if "fonts.gstatic" in url:
                            key = "fonts (woff2)"
                        by[key] = by.get(key, 0) + n
                        wire[key] = wire.get(key, 0) + (w_ if isinstance(w_, int) and w_ > 0 else n)
                    report["load"][size] = {"decoded": by, "decoded_total": sum(by.values()), "wire": wire, "wire_total": sum(wire.values()),
                                            "note": "wire = bytes on the network (the CDN compresses three.js and the fonts; the local test server does not compress, so for our own files see files.*.gzip)"}
                    first = False
                print("%-40s %-8s ready %5dms  calls %3s  tris %8s  %s" % (name, size, t_ready, st["drawCalls"], st["triangles"], f.name))
                if name in BENCH and "--nobench" not in sys.argv:
                    b = page.evaluate("() => window.__world.bench(3000)")
                    report["bench"]["%s-%s" % (name, size)] = b
                    print("   bench", b)
            # destroy() leaves nothing behind
            try:
                report["destroy_" + size] = page.evaluate("() => { window.__world.destroy(); return { root: !!document.querySelector('.nlw'), canvas: !!document.querySelector('canvas') }; }")
            except Exception as e:
                report["destroy_" + size] = str(e)[:200]
            errs = [l for l in logs if l.startswith(("error", "pageerror"))]
            if errs:
                print("console errors:\n  " + "\n  ".join(errs[:12]))
            report["console_errors_" + size] = errs[:20]
            gl = page.evaluate("""() => { const c = document.createElement('canvas').getContext('webgl2');
                const e = c && c.getExtension('WEBGL_debug_renderer_info'); return e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a'; }""")
            report["gpu"] = gl
            ctx.close()
        browser.close()
    httpd.shutdown()
    prev = {}
    rp = OUT / "report.json"
    if rp.exists() and only:
        prev = json.load(io.open(rp, encoding="utf-8"))
        for k in ("shots", "bench", "load"):
            prev.setdefault(k, {}).update(report[k])
        prev.update({k: v for k, v in report.items() if k not in ("shots", "bench", "load")})
        report = prev
    io.open(rp, "w", encoding="utf-8").write(json.dumps(report, ensure_ascii=False, indent=1))
    print("report", rp)


main()
