# -*- coding: utf-8 -*-
"""make deploy680.py from deploy679.py: 1.72.680 = the admin 403 fix (diagnosis 15.11.2026, docs/qa/had-740/admin-403-*.json).
Our three listing post types are registered with capability_type 'listing', map_meta_cap true and the capability map of
nadlan_listing_capabilities(), whose 'read_post' => 'read' made WordPress record the primitive 'read' as a per-post meta cap:
map_meta_cap('read') -> read_post with no post -> do_not_allow, so current_user_can('read') was false for every user and the
Dashboard, Profile and Updates screens returned 403 to the administrator.
  SWAP inc/roles.php (live = repo HEAD, md5 cface7ac4a): the one line 'read_post' => 'read' is removed; WordPress then uses its default
  'read_listing' as the meta cap, which still maps a published post to the primitive 'read' and a private one to read_private_listings.
Searched before (live plugins, live theme, the 19 active snippets, the repo): nothing calls current_user_can('read', <post>),
read_listing or ->cap->read_post."""
import hashlib, os, subprocess, sys, json, glob, re, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-679.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
_live = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "2026111[5-9]T*", "inc", "roles.php")))
_lb = open(_live[-1], "rb").read()
assert hashlib.md5(_lb).hexdigest().startswith("cface7ac4a"), "live roles.php changed: " + _live[-1]
_head = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/inc/roles.php"], capture_output=True, cwd=REPO).stdout
assert _head == _lb, "the repo HEAD roles.php is not the live text"
_new = open(os.path.join(PLUG, "inc", "roles.php"), "rb").read()
assert b"\r\n" not in _new and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", _new)
_ch = [l for l in difflib.unified_diff(_lb.decode("utf-8").split("\n"), _new.decode("utf-8").split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
assert _ch == ["-\t\t\t'read_post'              => 'read',"], _ch
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, "inc", "roles.php")], capture_output=True, text=True)
assert o.returncode == 0, o.stdout + o.stderr
print("[diff] roles.php: one line removed | php -l ok")
ROWS = ("    ('/projects/rainbow-tel-aviv/?t680r=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/properties/?t680r=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/professionals/?t680r=1', ['<h1', 'nldir-results'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-json/wp/v2/nadlan_project?per_page=2&t680r=1', ['\"type\":\"nadlan_project\"', '\"status\":\"publish\"'], ['rest_forbidden'], []),\n"
        "    ('/wp-json/wp/v2/nadlan_professional?per_page=2&t680r=1', ['\"type\":\"nadlan_professional\"'], ['rest_forbidden'], []),\n"
        "    ('/wp-json/wp/v2/nadlan_property?per_page=2&t680r=1', ['\"type\":\"nadlan_property\"'], ['rest_forbidden'], []),\n")
kl_release.build_release(679, 680, ["inc/roles.php"], [], {}, {}, ROWS,
                         "the administrator can open the Dashboard, Profile and Updates again (read is no longer a per-post meta cap)",
                         "admin 403 fix: 'read_post' => 'read' removed from the listing capability map")
