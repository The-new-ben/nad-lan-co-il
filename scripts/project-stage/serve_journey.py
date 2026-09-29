# -*- coding: utf-8 -*-
"""A FROZEN LOOPBACK preview of the branch, for a real UI journey clicked by a person or an agent (HAD-346 Batch 2, Codex's
integrated acceptance). No side effects on the site: the site is only read, only on allowlisted public paths, without query
strings, and every copy it read is frozen with its SHA-256.

  python scripts/project-stage/serve_journey.py --rev <commit> [--port 47915] [--state DIR] [--lead-e2e]
      extracts <commit>'s plugins/nadlan-config + scripts/project-stage into DIR/src-<commit>/ (git archive) and serves THAT
      tree (never the working tree); open http://127.0.0.1:47915/projects/rainbow-tel-aviv/
  (without --rev it serves the working tree: for development only, and the manifest says so)

Boundary, enforced here (not only by scripts in the page):
  GET, forwarded to the site (read-only), ONLY: /projects/<slug>/ pages and /wp-content/(themes|uploads|plugins)/,
    /wp-includes/(js|css|fonts)/ files, /favicon.ico. Never a query string upstream. The first copy of each is kept on disk
    (DIR/upstream/, SHA-256 in the manifest) and reused: the pages do not change under the tester.
  Upstream redirects are not followed blindly: only to an allowlisted path on the same host, answered as a local redirect.
  Refused (403): /wp-json/* (except the local ones below), /wp-admin, admin-ajax.php, wp-login.php, wp-cron.php, xmlrpc.php,
    any ?action= / ?wc-ajax= / ?rest_route= / ?add-to-cart= , every other path, every POST/PUT/DELETE/PATCH.
  Local, from the frozen tree: /wp-content/plugins/nadlan-config/* (the branch's files first), /tour/designer/ (the branch's
    assets/tours/designer-tour.html), POST /wp-json/nadlan/v1/lead and /rfp (the branch's REAL callbacks in memory via
    rfp_local_endpoint.php; email recorded, never sent), GET /wp-json/nadlan/v1/rfp/<token> (the branch's renderer).
  Every HTML answer carries a Content-Security-Policy: connections, forms and frames only to this origin (plus the map's
    tiles and the code CDNs the pages load); analytics, payment, WhatsApp and telemetry hosts cannot be reached.
  /__manifest.json (revision, served files + SHA-256, upstream copies + SHA-256, the policy), /__state.json, /__reset.
"""
import argparse, hashlib, http.server, io, json, os, re, socketserver, subprocess, sys, tarfile, threading, time
import urllib.request, urllib.error, urllib.parse, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ORIGIN = "https://nad-lan.co.il"
A = None
TREE = None          # the root served (frozen extract, or the working tree)
PN = None
PV = None
SERVED, UPSTREAM = {}, {}
LOCK = threading.Lock()
TYPES = {"js": "text/javascript", "mjs": "text/javascript", "css": "text/css", "json": "application/json", "svg": "image/svg+xml", "png": "image/png", "jpg": "image/jpeg",
         "jpeg": "image/jpeg", "webp": "image/webp", "gif": "image/gif", "ico": "image/x-icon", "glb": "model/gltf-binary", "mp4": "video/mp4", "mp3": "audio/mpeg",
         "woff2": "font/woff2", "woff": "font/woff", "ttf": "font/ttf", "html": "text/html; charset=utf-8", "geojson": "application/json", "txt": "text/plain"}
PAGE = re.compile(r"^/projects/[a-z0-9-]+/?$")
ASSET = re.compile(r"^/(wp-content/(themes|uploads|plugins)/|wp-includes/(js|css|fonts)/|favicon\.ico$)")
REFUSE = re.compile(r"^/(wp-json|wp-admin|wp-login\.php|wp-cron\.php|xmlrpc\.php)|admin-ajax\.php", re.I)
BAD_QUERY = re.compile(r"(^|&)(action|wc-ajax|rest_route|add-to-cart|preview|p|page_id)=", re.I)
CSP = ("default-src 'self'; "
       "script-src 'self' 'unsafe-inline' 'unsafe-eval' blob: https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://unpkg.com https://ajax.googleapis.com https://api.mapbox.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://api.mapbox.com https://unpkg.com; "
       "font-src 'self' data: https://fonts.gstatic.com; "
       "img-src 'self' data: blob: https://api.mapbox.com https://*.tiles.mapbox.com; "
       "connect-src 'self' blob: data: https://api.mapbox.com https://*.tiles.mapbox.com https://cdn.jsdelivr.net https://unpkg.com https://www.gstatic.com; "
       "worker-src 'self' blob:; child-src 'self' blob:; frame-src 'none'; media-src 'self' blob: data:; object-src 'none'; "
       "form-action 'self'; base-uri 'self'")
STRIP = re.compile(r'<script[^>]+src="[^"]*(googletagmanager\.com|google-analytics\.com|connect\.facebook\.net|clarity\.ms|hotjar\.com|js\.stripe\.com)[^"]*"[^>]*>\s*</script>', re.I)
GUARD = """<script>/* serve_journey.py: WhatsApp is stopped here and its text shown (the policy also blocks the host). */
(function(){
  var show=function(u){try{var q=new URL(u,location.href);var t=q.searchParams.get('text')||'';var d=document.getElementById('nlj-wa');
    if(!d){d=document.createElement('div');d.id='nlj-wa';d.setAttribute('role','dialog');d.style.cssText='position:fixed;inset:auto 12px 12px 12px;z-index:2147483647;max-height:60vh;overflow:auto;background:#fff;color:#14212B;border:2px solid #0F7A5C;border-radius:14px;padding:14px;font:14px/1.5 Heebo,Arial,sans-serif;white-space:pre-wrap;box-shadow:0 10px 40px rgba(0,0,0,.3)';document.body.appendChild(d);}
    d.innerHTML='';var h=document.createElement('b');h.textContent='תצוגה מקומית: וואטסאפ לא נפתח. זה הטקסט שהיה נשלח ('+q.hostname+'):';var p=document.createElement('div');p.textContent=t;var x=document.createElement('button');x.textContent='סגירה';x.style.cssText='margin-top:8px;min-height:44px;padding:0 16px';x.onclick=function(){d.remove();};d.append(h,p,x);}catch(e){}};
  var wa=/^https?:\\/\\/(wa\\.me|api\\.whatsapp\\.com|web\\.whatsapp\\.com)\\//i;
  document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(a&&wa.test(a.href)){e.preventDefault();e.stopImmediatePropagation();show(a.href);}},true);
  var wo=window.open;window.open=function(u){if(u&&wa.test(String(u))){show(String(u));return null;}return wo.apply(window,arguments);};
})();</script>"""


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def upstream(path):
    """a read-only GET of an allowlisted path, no query; the first copy is frozen on disk and reused"""
    key = hashlib.sha1(path.encode()).hexdigest()
    body_f = os.path.join(A.upstream_dir, key + ".body"); meta_f = os.path.join(A.upstream_dir, key + ".json")
    with LOCK:
        if os.path.exists(body_f) and os.path.exists(meta_f):
            meta = json.load(open(meta_f, encoding="utf-8")); data = open(body_f, "rb").read()
            UPSTREAM[path] = meta["sha256"]
            return data, meta["ctype"], meta["status"], meta.get("location")
    req = urllib.request.Request(ORIGIN + path, headers={"User-Agent": "Mozilla/5.0 (serve_journey.py local preview; read-only)", "Accept-Encoding": "identity"})
    loc = None
    try:
        with OPENER.open(req, timeout=60) as r:
            data, ctype, status = r.read(), r.headers.get("Content-Type", "application/octet-stream"), r.status
    except urllib.error.HTTPError as e:
        data, ctype, status, loc = e.read(), e.headers.get("Content-Type", "text/plain"), e.code, e.headers.get("Location")
    with LOCK:
        open(body_f, "wb").write(data)
        json.dump({"path": path, "ctype": ctype, "status": status, "location": loc, "sha256": sha_bytes(data), "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, open(meta_f, "w", encoding="utf-8"))
        UPSTREAM[path] = sha_bytes(data)
    return data, ctype, status, loc


def localize(html):
    for a, b in (("https://nad-lan.co.il/", "/"), ("https:\\/\\/nad-lan.co.il\\/", "\\/"), ("//nad-lan.co.il/", "/")):
        html = html.replace(a, b)
    html = STRIP.sub("", html)
    return html.replace("<head>", "<head>" + GUARD, 1) if "<head>" in html else GUARD + html


def endpoint(op, body):
    env = {**os.environ, "NL_REST_BASE": "http://127.0.0.1:%d/wp-json/" % A.port, "NL_SITE_BASE": "http://127.0.0.1:%d" % A.port}
    r = subprocess.run(["php", os.path.join(TREE, "scripts", "project-stage", "rfp_local_endpoint.php"), op, A.state_file], input=body, capture_output=True, text=True, encoding="utf-8", env=env)
    return r.stdout


def seed():
    json.dump({"seq": 900, "inserts": [], "writes": [], "options": {"nadlan_feature_lead_e2e": "1" if A.lead_e2e else "0"}, "content": {}, "names": {}, "hooks": [], "leads": [],
               "transients": {}, "mail": [], "fail_insert_times": 0, "projects": {"rainbow-tel-aviv": 101, "duo-tel-aviv": 102, "dimri-yama-sde-dov": 103, "ashira-sde-dov": 104},
               "types": {"101": "nadlan_project", "102": "nadlan_project", "103": "nadlan_project", "104": "nadlan_project"}, "meta": {}}, open(A.state_file, "w", encoding="utf-8"))


class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def send(self, status, data, ctype, extra=None):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(data))); self.send_header("Cache-Control", "no-store")
        if ctype.startswith("text/html"):
            self.send_header("Content-Security-Policy", CSP)
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers(); self.wfile.write(data)

    def refuse(self, why):
        return self.send(403, json.dumps({"refused": why, "by": "serve_journey.py"}), "application/json")

    def log_message(self, fmt, *args):
        if A.verbose:
            sys.stderr.write("%s %s\n" % (self.command, self.path))

    def do_GET(self):
        u = urllib.parse.urlsplit(self.path)
        bare, query = u.path, u.query
        if BAD_QUERY.search(query):
            return self.refuse("an action query is never served or forwarded")
        if bare == "/":
            return self.send(302, "", "text/plain", {"Location": "/projects/rainbow-tel-aviv/"})
        if bare == "/__manifest.json":
            return self.send(200, json.dumps(manifest(), ensure_ascii=False, indent=1), "application/json")
        if bare == "/__state.json":
            return self.send(200, endpoint("state", "{}"), "application/json")
        if bare == "/__reset":
            seed(); return self.send(200, '{"ok":true}', "application/json")
        m = re.match(r"^/wp-json/nadlan/v1/rfp/([A-Za-z0-9]{16,32})$", bare)
        if m:
            return self.send(200, endpoint("render", json.dumps({"token": m.group(1)})), "text/html; charset=utf-8")
        if bare.startswith("/tour/designer"):
            f = os.path.join(PN, "assets", "tours", "designer-tour.html"); raw = open(f, "rb").read()
            SERVED["assets/tours/designer-tour.html"] = sha_bytes(raw)
            return self.send(200, localize(raw.decode("utf-8")), "text/html; charset=utf-8")
        if bare.startswith("/wp-content/plugins/nadlan-config/"):
            rel = urllib.parse.unquote(bare.split("/wp-content/plugins/nadlan-config/", 1)[1])
            lp = os.path.normpath(os.path.join(PN, *rel.split("/")))
            if lp.startswith(os.path.normpath(PN)) and os.path.isfile(lp):
                raw = open(lp, "rb").read(); SERVED[rel] = sha_bytes(raw)
                return self.send(200, raw, TYPES.get(rel.rsplit(".", 1)[-1].lower(), "application/octet-stream"))
        if REFUSE.search(bare) or BAD_QUERY.search(query):
            return self.refuse("a site API, admin or action URL is never forwarded")
        if not (PAGE.match(bare) or ASSET.match(bare)):
            return self.refuse("not an allowlisted public page or file path")
        data, ctype, status, loc = upstream(bare)  # the path only: a query string never goes upstream
        if 300 <= status < 400:
            t = urllib.parse.urlsplit(urllib.parse.urljoin(ORIGIN + bare, loc or ""))
            if t.netloc == "nad-lan.co.il" and (PAGE.match(t.path) or ASSET.match(t.path)):
                return self.send(302, "", "text/plain", {"Location": t.path + (("?" + query) if query and PAGE.match(t.path) else "")})
            return self.refuse("an upstream redirect outside the allowlist")
        if "text/html" in ctype:
            lang = "he"
            for l in ("en", "fr", "ru", "ar"):
                if re.search(r"-%s/?$" % l, bare.rstrip("/") + "/"):
                    lang = l
            applied = []
            html = PV.transform_html(data.decode("utf-8", "replace"), bare + (("?" + query) if query else ""), lang, applied, strict=False)
            return self.send(status, localize(html), "text/html; charset=utf-8", {"X-NL-Journey": urllib.parse.quote("; ".join(applied))[:1800]})
        if "text/css" in ctype:
            return self.send(status, data.decode("utf-8", "replace").replace("https://nad-lan.co.il/", "/"), ctype)
        return self.send(status, data, ctype)

    def do_POST(self):
        bare = urllib.parse.urlsplit(self.path).path
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n).decode("utf-8") if n else "{}"
        m = re.match(r"^/wp-json/nadlan/v1/(lead|rfp)$", bare)
        if m:
            out = json.loads(endpoint(m.group(1), body))
            return self.send(out["status"], json.dumps(out["body"], ensure_ascii=False), "application/json")
        return self.refuse("only the local lead and request endpoints accept a POST")

    def do_PUT(self): return self.refuse("method")
    do_DELETE = do_PATCH = do_PUT


def manifest():
    return {"revision": A.rev or "WORKING TREE (not frozen)", "tree": TREE, "lead_e2e": A.lead_e2e, "state": A.state_file,
            "served_branch_files": dict(sorted(SERVED.items())), "upstream_copies": dict(sorted(UPSTREAM.items())), "csp": CSP,
            "allow": {"page": PAGE.pattern, "asset": ASSET.pattern}, "refuse": [REFUSE.pattern, BAD_QUERY.pattern]}


def extract(rev, into):
    repo = os.path.dirname(os.path.dirname(HERE))
    full = subprocess.run(["git", "-C", repo, "rev-parse", rev], capture_output=True, text=True, check=True).stdout.strip()
    dest = os.path.join(into, "src-" + full[:12])
    if not os.path.isdir(dest):
        tar = subprocess.run(["git", "-C", repo, "archive", "--format=tar", full, "plugins/nadlan-config", "scripts/project-stage", "scripts/i18n"], capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            t.extractall(dest)
    return full, dest


class TS(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def main():
    global A, TREE, PN, PV
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default=""); ap.add_argument("--port", type=int, default=47915); ap.add_argument("--state", default=os.path.join(HERE, "_journey"))
    ap.add_argument("--lead-e2e", action="store_true"); ap.add_argument("--verbose", action="store_true")
    A = ap.parse_args()
    os.makedirs(A.state, exist_ok=True)
    if A.rev:
        A.rev, TREE = extract(A.rev, A.state)
    else:
        TREE = os.path.dirname(os.path.dirname(HERE))
    PN = os.path.join(TREE, "plugins", "nadlan-config")
    spec = importlib.util.spec_from_file_location("preview_v101", os.path.join(TREE, "scripts", "project-stage", "preview_v101.py"))
    PV = importlib.util.module_from_spec(spec); spec.loader.exec_module(PV)
    A.upstream_dir = os.path.join(A.state, "upstream"); os.makedirs(A.upstream_dir, exist_ok=True)
    A.state_file = os.path.join(A.state, "journey-state.json")
    seed()
    srv = TS(("127.0.0.1", A.port), H)
    print("serve_journey.py: revision %s, tree %s\n  http://127.0.0.1:%d/projects/rainbow-tel-aviv/   (manifest /__manifest.json, state /__state.json, reset /__reset)" % (A.rev or "WORKING TREE", TREE, A.port), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
