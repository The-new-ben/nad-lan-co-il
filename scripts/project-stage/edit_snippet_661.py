# -*- coding: utf-8 -*-
"""HAD-460 / the CEO's approval (7.10.2026): the area-prices card on every project page (snippet 661 x-catalog-plus, function
behind <aside class="nlcp-projctx">) asked "כמה עולה דירה ב{עיר}?" in an H2, which competes with the city price pages
(/tel-aviv-apartment-prices/ owns "כמה עולה דירה בתל אביב"). Now:
- the H2 says "המחירים סביב הפרויקט ב{עיר}" (not the city question);
- the card's source line links to the city's price page with the anchor "מחירי דירות ב{עיר}" when the city has one.
Safety: the live code is read, both anchors must appear exactly once, php -l locally, backup with md5, write, then live checks on
project pages with the card (200, new H2 in, old H2 out, no fatal); any failure writes the old code back.
python edit_snippet_661.py [--dry | --rollback <backup.json>]"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-460", "snippet-661")
SID = 661
ARGS = sys.argv[1:]
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "sn661"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]

OLD_H2 = "<h2>כמה עולה דירה ב' . esc_html( $city ) . '?</h2>"
NEW_H2 = "<h2>המחירים סביב הפרויקט ב' . esc_html( $city ) . '</h2>"
OLD_LINK = "'\">עוד פרויקטים חדשים ב' . esc_html( $city ) . '</a> · <a href=\"' . esc_url( home_url( '/projects/' ) ) . '\">"
NEW_LINK = ("'\">עוד פרויקטים חדשים ב' . esc_html( $city ) . '</a>' . ( function_exists( 'nadlan_cp_price_page' ) && nadlan_cp_price_page( $city ) ? "
            "' · <a href=\"' . esc_url( nadlan_cp_price_page( $city ) ) . '\">מחירי דירות ב' . esc_html( $city ) . '</a>' : '' ) . ' · <a href=\"' . esc_url( home_url( '/projects/' ) ) . '\">")
HELPER = r"""
if ( ! function_exists( 'nadlan_cp_price_page' ) ) {
	/** HAD-460 (7.10.2026): the city's price page on nad-lan, when one exists (the card links to it instead of asking its question). */
	function nadlan_cp_price_page( $city ) {
		$k = str_replace( array( '-', ' ', '"', "'" ), '', (string) $city );
		$map = array( 'תלאביביפו' => 'tel-aviv', 'ירושלים' => 'jerusalem', 'חיפה' => 'haifa', 'ראשוןלציון' => 'rishon-lezion', 'פתחתקווה' => 'petah-tikva',
			'אשדוד' => 'ashdod', 'נתניה' => 'netanya', 'בארשבע' => 'beer-sheva', 'חולון' => 'holon', 'בניברק' => 'bnei-brak', 'רמתגן' => 'ramat-gan',
			'בתים' => 'bat-yam', 'רחובות' => 'rehovot', 'אשקלון' => 'ashkelon', 'הרצליה' => 'herzliya', 'כפרסבא' => 'kfar-saba', 'הודהשרון' => 'hod-hasharon',
			'מודיעיןמכביםרעות' => 'modiin', 'מודיעין' => 'modiin', 'רעננה' => 'raanana', 'גבעתיים' => 'givatayim', 'קריתאונו' => 'kiryat-ono',
			'רמתהשרון' => 'ramat-hasharon', 'אילת' => 'eilat' );
		return isset( $map[ $k ] ) ? home_url( '/' . $map[ $k ] . '-apartment-prices/' ) : '';
	}
}
"""
PAGES = ["/projects/h-infinity-somail-tel-aviv/", "/projects/the-park-bnei-brak/", "/projects/rainbow-tel-aviv/", "/projects/aurelia/"]


def page(path):
    u = "https://nad-lan.co.il" + path + ("&" if "?" in path else "?") + "nl661=%d" % time.time()
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-sn661"}), timeout=90)
    return r.status, r.read().decode("utf-8", "replace")


def lint(code):
    with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as t:
        t.write("<?php\n" + code); tmp = t.name
    try:
        out = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
    finally:
        os.unlink(tmp)
    if out.returncode != 0:
        raise SystemExit("FATAL lint: " + out.stdout + out.stderr)


s, sn = snip("GET", f"/{SID}", None)
if s != 200:
    raise SystemExit(f"FATAL read snippet {SID}: {s}")
code = sn["code"]
if "--rollback" in ARGS:
    bk = json.load(io.open(ARGS[ARGS.index("--rollback") + 1], encoding="utf-8"))
    s, r = snip("PUT", f"/{SID}", {"name": sn["name"], "code": bk["code"], "scope": sn["scope"], "active": True})
    print("[rollback]", s); raise SystemExit(0)
if "nadlan_cp_price_page" in code:
    raise SystemExit("already applied")
if code.count(OLD_H2) != 1 or code.count(OLD_LINK) != 1:
    raise SystemExit(f"FATAL anchors: h2 x{code.count(OLD_H2)}, link x{code.count(OLD_LINK)}")
new = HELPER.strip() + "\n" + code.replace(OLD_H2, NEW_H2).replace(OLD_LINK, NEW_LINK)
lint(new)
print("[lint] ok; old md5", hashlib.md5(code.encode()).hexdigest()[:10], "new", hashlib.md5(new.encode()).hexdigest()[:10])
before = {p: page(p) for p in PAGES}
for p, (st, h) in before.items():
    print("[before]", st, p, "old h2" if "כמה עולה דירה ב" in h else "-")
if "--dry" in ARGS:
    raise SystemExit(0)
os.makedirs(BK, exist_ok=True)
bkp = os.path.join(BK, f"snippet-661-{time.strftime('%Y%m%dT%H%M%S')}.json")
io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": SID, "name": sn["name"], "code": code, "md5": hashlib.md5(code.encode()).hexdigest()}, ensure_ascii=False))
s, r = snip("PUT", f"/{SID}", {"name": sn["name"], "code": new, "scope": sn["scope"], "active": True})
s2, back = snip("GET", f"/{SID}", None)
ok_write = s == 200 and back.get("code") == new and back.get("active")
print("[write]", s, "read-back identical and active:", ok_write, "| backup", os.path.relpath(bkp, REPO))
bad = [] if ok_write else ["write"]
time.sleep(3)
for p in PAGES:
    st, h = page(p)
    had = "כמה עולה דירה ב" in before[p][1]
    good = st == 200 and "Fatal error" not in h and "critical error" not in h and (not had or ("המחירים סביב הפרויקט ב" in h and "<h2>כמה עולה דירה ב" not in h))
    print("[after]", "OK " if good else "BAD", st, p)
    if not good:
        bad.append(p)
st, h = page("/")
if st != 200:
    bad.append("/")
if bad:
    s, r = snip("PUT", f"/{SID}", {"name": sn["name"], "code": code, "scope": sn["scope"], "active": True})
    raise SystemExit(f"ROLLED BACK ({s}): {bad}")
print("[done] snippet 661 updated")
