# -*- coding: utf-8 -*-
"""make deploy695.py from deploy694.py: 1.72.695 = HAD-768 the AI layer of /forms/ (Ben 17.11.2026: "GEO and AIO on top of SEO,
numbers, prices, schemas, deep, and prove it"): the key numbers table (16 statutory deadlines, thresholds and majorities, each with
its section and an official link), CollectionPage about/citation/speakable, HowTo of the 11 stages, Dataset with a JSON download,
GET /wp-json/nadlan/v1/forms, the llms.txt section (once the page exists), and the stage links to our own tools.
  SWAP inc/forms-hub.php, assets/forms/forms.css, assets/forms/forms.json. Proof: docs/research/2026-11-17-gov-forms/GEO-DEPTH.md."""
import os, subprocess, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-694.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["inc/forms-hub.php", "assets/forms/forms.css", "assets/forms/forms.json"]
for rel in F:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, "inc", "forms-hub.php")], capture_output=True, text=True)
assert o.returncode == 0, o.stdout + o.stderr
for t in ("tools/seo/test_h768_forms.php", "tools/seo/test_h743_deals.php", "tools/seo/test_h740_default.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/wp-json/nadlan/v1/forms?t695=1', ['\"stages\"', '\"facts\"', '108,500', 'wp-content\\/uploads'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/forms/forms.css?t695=1', ['.nlfm-facts', '.nlfm-part'], [], []),\n")
kl_release.build_release(694, 695, F, [], {}, {}, ROWS,
                         "the AI layer of the forms hub: numbers table, deep schema, JSON data, llms.txt (HAD-768)",
                         "HAD-768: forms hub AI layer (GEO/AIO)")
