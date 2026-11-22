# -*- coding: utf-8 -*-
"""make deploy741.py from deploy740.py: 1.72.741 = HAD-791 owner live alerts (Ben 22.11.2026 through the coordinator: an instant
mail on every meaningful touch on the site, without loading the site or touching SEO). Design board:
https://claude.ai/artifact/7fdnJgxn8scFBeM63vyD9e
  NEW  inc/owner-live.php 1.0.0 (required by visit-trail.php; no module-list change): alerts from the trail batches, the forum
       (nlf_post_created) and sign-up / basket routes (rest_post_dispatch); mail after the response; 10 minutes per visitor + kind,
       40 an hour; the signed live screen GET /wp-json/nadlan/v1/owner-live; admin Lead Inbox > "התראות חיות".
  SWAP inc/visit-trail.php 1.1.1: do_action('nadlan_vt_stored') after a stored batch; /developers/ and /marketing/ keep one 'open'
       in lite mode; the require line.
  SWAP assets/visit-trail/trail.js 1.1.1: one 'open' on those two pages (cfg.watch). No new request on any other page.
Tests: test_trail_12.js 117/117, test_visit_trail_12.php 140/140."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 740
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
A = "/wp-content/plugins/nadlan-config/assets/visit-trail/"
ROWS = ("    ('%strail.js?t741a=1', ['NadLan visit trail 1.1.1', \"if (!lite || cfg.watch) push('open', {});\"], ['Fatal error'], []),\n"
        "    ('/wp-json/nadlan/v1/healthcheck?t741a=1', ['\"owner_live\":{\"version\":\"1.0.0\"', '\"visit_trail\":{\"version\":\"1.1.1\"'], ['Fatal error'], []),\n"
        "    ('/developers/?t741a=1', ['assets/visit-trail/trail.js', '\"watch\":1'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t741a=1', ['assets/visit-trail/trail.js', '\"mode\":\"full\"'], %r + ['\"watch\":1'], []),\n") % (A, E, E)
kl_release.build_release(PREV, 741, ["inc/visit-trail.php", "assets/visit-trail/trail.js", "inc/owner-live.php"], ["inc/owner-live.php"], {}, {}, ROWS,
                         "owner live alerts: a mail on every meaningful touch (projects, plans, basket, forum, sign-up, developers page) and a private live screen",
                         "HAD-791 owner live alerts")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy741.py")
src = open(P, encoding="utf-8").read()
n1 = src.count("NadLan visit trail 1.1.0'")
n2 = src.count('"visit_trail":{"version":"1.1.0"')
src = src.replace("NadLan visit trail 1.1.0'", "NadLan visit trail 1.1.1'").replace('"visit_trail":{"version":"1.1.0"', '"visit_trail":{"version":"1.1.1"')
# the runner's verify_vt() names the module's 1.1.0 (second run rolled back on it): move its two version checks to 1.1.1
for a in ('vt.get("version") == "1.1.0"', 'p.get("version") == "1.1.0" and p.get("db") == 1'):
    assert src.count(a) == 1, (a, src.count(a))
    src = src.replace(a, a.replace('"1.1.0"', '"1.1.1"'))
open(P, "w", encoding="utf-8", newline="\n").write(src)
print("deploy741.py: %d trail header row(s) and %d health row(s) moved to 1.1.1" % (n1, n2))
