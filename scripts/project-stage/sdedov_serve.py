"""The repo root over HTTP for the harnesses, plus the COMMITTED bridge.js (git show HEAD:...) at /__head__/bridge.js, so a
stage is tested against what is live and not against a working copy another session may be editing.
python scripts/project-stage/sdedov_serve.py 47962"""
import functools, http.server, subprocess, sys
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
HEAD_BRIDGE = subprocess.run(["git", "-C", REPO, "show", "HEAD:plugins/nadlan-config/assets/project-stage/bridge.js"], capture_output=True, check=True).stdout


class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/__head__/bridge.js":
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript; charset=utf-8")
            self.send_header("Content-Length", str(len(HEAD_BRIDGE)))
            self.end_headers()
            self.wfile.write(HEAD_BRIDGE)
            return
        return super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))


port = int(sys.argv[1]) if len(sys.argv) > 1 else 47962
http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(H, directory=REPO)).serve_forever()
