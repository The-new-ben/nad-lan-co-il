# -*- coding: utf-8 -*-
"""Local look at the project designer page (HAD-708) before a release: serves the repo's plugin files at the live paths.
  /tour/designer/               -> plugins/nadlan-config/assets/tours/designer-tour.html (any query string)
  /wp-content/plugins/...       -> plugins/...
  /projects/<slug>/             -> a tiny page with a link to the designer (so the referrer carries the project)
  /design-studio/               -> docs/tools/design-studio/hub/preview.html when it exists
python serve_local.py [port, default 47962]   (binds 127.0.0.1 only)"""
import http.server, os, sys, urllib.parse
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 47962
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".json": "application/json; charset=utf-8", ".glb": "model/gltf-binary", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml", ".pdf": "application/pdf"}


class Hd(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="text/html; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        f = None
        if path.rstrip("/") == "/tour/designer":
            f = os.path.join(REPO, "plugins", "nadlan-config", "assets", "tours", "designer-tour.html")
        elif path.startswith("/wp-content/plugins/"):
            f = os.path.normpath(os.path.join(REPO, "plugins", path[len("/wp-content/plugins/"):]))
        elif path.startswith("/projects/"):
            slug = path.strip("/").split("/")[-1]
            return self.send(200, '<!doctype html><meta charset="utf-8"><title>%s</title><body dir="rtl"><p>דף פרויקט לבדיקה: %s</p><p><a id="plain" href="/tour/designer/">עיצוב הדירה</a></p><p><a id="unit" href="/tour/designer/?project=%s&unit=S1-25-w&pn=%s&ul=%s">עיצוב הדירה שנבחרה</a></p>' % (slug, slug, slug, urllib.parse.quote("פרויקט לבדיקה"), urllib.parse.quote("קומה 25 · מערב · 5 חדרים")))
        elif path.rstrip("/") == "/design-studio":
            f = os.path.join(H, "hub", "preview.html")
        else:
            f = os.path.normpath(os.path.join(REPO, path.lstrip("/")))
        if not f or not f.startswith(REPO) or not os.path.isfile(f):
            return self.send(404, "not found: " + path)
        with open(f, "rb") as fh:
            self.send(200, fh.read(), TYPES.get(os.path.splitext(f)[1].lower(), "application/octet-stream"))


http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Hd).serve_forever()
