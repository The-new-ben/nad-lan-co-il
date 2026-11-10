# -*- coding: utf-8 -*-
"""HAD-694 (Ben 10.11.2026 late night, relayed by the main session): the catalog cards on /projects/ printed an exact price line
("מחיר למ"ר בתל אביב יפו: 52,856 ₪ · ברחוב אבן גבירול: 72,179 ₪ | 2,432 עסקאות, 10.2023 עד 10.2025 · רשות המסים"). Ben: write a
RANGE instead (his decision of 2.11, HAD-658): rounded, "לפי פרסומים גלויים", no exact figure, no deal count, no dates, no source
name on the cards. Snippet 661 (catalog-plus) changes in three places, cards only (the page's price tables are untouched):
  1. new functions nadlan_cp_card_range_text() / nadlan_cp_card_range_line();
  2. the card enrichment prints nadlan_cp_card_range_line() instead of nadlan_cp_context_line();
  3. the card's "עוד פרטים" fold shows the same range instead of the exact per-metre figures, deal counts and medians.
Wording: the project's own published range (price_min / price_max, or the developer's "החל מ" price on the market row linked to
the page) -> "טווח מחירים: מ־X עד Y ₪" / "החל מ־X ₪" (rounded to 10,000); otherwise the area per metre from the card's two
numbers (city, street) rounded to 1,000 -> "טווח מחירים באזור: כ־53,000 עד 72,000 ₪ למ״ר, לפי פרסומים גלויים"; one number ->
"כ־53,000 ₪ למ״ר, לפי פרסומים גלויים"; none -> nothing.
Safety: live code read, every anchor once, php -l, backup with md5, write, read back, then /projects/, /projects/page/2/ and the
projects-plus route are checked card by card; any failure writes the old code back.
python scripts/project-stage/snippet661_ranges_694.py [--dry | --rollback <backup.json>]"""
import hashlib, io, json, os, re, subprocess, sys, tempfile, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-694", "snippet-661")
SID = 661
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "sn661rg"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
snip = ns["snip"]
T = "\t"
FUNCS = (
    "if ( ! function_exists( 'nadlan_cp_card_range_text' ) ) {\n"
    "\t/** HAD-694 (Ben 10.11.2026): a card shows a rounded price RANGE, never an exact figure, a deal count, dates or a source name. */\n"
    "\tfunction nadlan_cp_card_range_text( $id, $ctx ) {\n"
    "\t\t$r10 = function ( $n ) { return number_format( (float) ( round( (float) $n / 10000 ) * 10000 ), 0, '.', ',' ); };\n"
    "\t\t$lo = (int) get_post_meta( $id, 'price_min', true ); $hi = (int) get_post_meta( $id, 'price_max', true );\n"
    "\t\tif ( $lo < 300000 || $lo > 100000000 ) { $lo = 0; } if ( $hi < 300000 || $hi > 100000000 || ( $lo && $hi < $lo ) ) { $hi = 0; }\n"
    "\t\tif ( ! $lo && function_exists( 'nadlan_dir_market_row' ) ) { $mr = nadlan_dir_market_row( (string) get_post_field( 'post_name', $id ) ); $pf = $mr ? (int) ( $mr['price_from'] ?? 0 ) : 0; if ( $pf >= 300000 ) { $lo = $pf; } }\n"
    "\t\tif ( $lo && $hi && $r10( $hi ) !== $r10( $lo ) ) { return 'טווח מחירים: מ־' . $r10( $lo ) . ' עד ' . $r10( $hi ) . ' ₪'; }\n"
    "\t\tif ( $lo ) { return 'טווח מחירים: החל מ־' . $r10( $lo ) . ' ₪'; }\n"
    "\t\t$v = array();\n"
    "\t\tif ( ! empty( $ctx['row']['psqm_all'] ) ) { $v[] = (int) round( (float) $ctx['row']['psqm_all'] / 1000 ) * 1000; }\n"
    "\t\tif ( ! empty( $ctx['street']['psqm'] ) ) { $v[] = (int) round( (float) $ctx['street']['psqm'] / 1000 ) * 1000; }\n"
    "\t\t$v = array_values( array_unique( array_filter( $v ) ) ); sort( $v );\n"
    "\t\tif ( ! $v ) { return ''; }\n"
    "\t\tif ( 1 === count( $v ) ) { return 'טווח מחירים באזור: כ־' . number_format( $v[0] ) . ' ₪ למ״ר, לפי פרסומים גלויים'; }\n"
    "\t\treturn 'טווח מחירים באזור: כ־' . number_format( $v[0] ) . ' עד ' . number_format( end( $v ) ) . ' ₪ למ״ר, לפי פרסומים גלויים';\n"
    "\t}\n"
    "\tfunction nadlan_cp_card_range_line( $id, $ctx ) {\n"
    "\t\t$t = nadlan_cp_card_range_text( $id, $ctx );\n"
    "\t\treturn '' === $t ? '' : '<p class=\"nlcp-ctx nlcp-range\"><span class=\"nlcp-ctx__k\" aria-hidden=\"true\">₪</span><span>' . esc_html( $t ) . '</span></p>';\n"
    "\t}\n"
    "}\n"
)
A1 = "if ( ! function_exists( 'nadlan_cp_more_html' ) ) {"
A2 = "$inner .= nadlan_cp_context_line( $ctx );"
N2 = "$inner .= function_exists( 'nadlan_cp_card_range_line' ) ? nadlan_cp_card_range_line( $id, $ctx ) : ''; // HAD-694: a range, not exact figures"
A3_START = "\t\t$row = $ctx['row'];\n\t\tif ( $row && ! empty( $row['psqm_all'] ) ) {\n\t\t\t$rows[] = array( 'מחיר למ\"ר בעיר'"
A3_END = "\t\t$h  = '<details class=\"nlcp-more\">"
N3 = ("\t\t$row = $ctx['row'];\n"
      "\t\t$rg = function_exists( 'nadlan_cp_card_range_text' ) ? nadlan_cp_card_range_text( $id, $ctx ) : '';\n"
      "\t\tif ( '' !== $rg ) { $rg2 = explode( ': ', $rg, 2 ); $rows[] = array( $rg2[0], $rg2[1] ?? '' ); } // HAD-694: the range only\n")
A4 = "if ( $row && ! empty( $row['psqm_all'] ) ) { $h .= '<p class=\"nlcp-src\">מחירי הסביבה: עסקאות שדווחו לרשות המסים, דירות בבתי קומות, חציון. אינם מחיר הפרויקט.</p>'; }"
N4 = "if ( '' !== $rg && false !== strpos( $rg, 'באזור' ) ) { $h .= '<p class=\"nlcp-src\">טווח המחירים באזור אינו מחיר הפרויקט.</p>'; }"
PHP = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
PHP = next((os.path.join(PHP, d, "php.exe") for d in sorted(os.listdir(PHP)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(PHP) else "php"
BAD_IN_CARD = ("עסקאות", "רשות המסים", "מחיר למ\"ר ב", "חציון")


def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (site owner audit)"}), timeout=120) as f:
            return f.status, f.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


def cards_ok(html):
    cards = re.findall(r'<article class="nlcp-card">.*?</article>', html, re.S)
    bad = [c for c in cards if any(b in c for b in BAD_IN_CARD)]
    rng = sum(1 for c in cards if "טווח מחירים" in c)
    return len(cards), len(bad), rng, (bad[0][:400] if bad else "")


s, sn = snip("GET", "/%d" % SID, None)
if s != 200:
    raise SystemExit("FATAL read snippet: %s" % s)
code = sn["code"]
if "--rollback" in sys.argv:
    bk = json.load(io.open(sys.argv[sys.argv.index("--rollback") + 1], encoding="utf-8"))
    s, r = snip("PUT", "/%d" % SID, {"name": sn["name"], "code": bk["code"], "scope": sn["scope"], "active": True}); print("[rollback]", s); raise SystemExit(0)
if "nadlan_cp_card_range_text" in code:
    raise SystemExit("already applied")
i3, j3 = code.find(A3_START), code.find(A3_END)
for name, ok in (("A1", code.count(A1) == 1), ("A2", code.count(A2) == 1), ("A3", code.count(A3_START) == 1 and j3 > i3 > 0), ("A4", code.count(A4) == 1)):
    if not ok:
        raise SystemExit("FATAL anchor " + name)
new = code[:i3] + N3 + code[j3:]
new = new.replace(A1, FUNCS + A1).replace(A2, N2).replace(A4, N4)
with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as t:
    t.write("<?php\n" + new); tmp = t.name
o = subprocess.run([PHP, "-l", tmp], capture_output=True, text=True); os.unlink(tmp)
if o.returncode != 0:
    raise SystemExit("FATAL lint: " + o.stdout + o.stderr)
assert not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", new.replace("\t", "").replace("\n", "")), "control character"
print("[lint] ok | old md5", hashlib.md5(code.encode()).hexdigest()[:10], "new", hashlib.md5(new.encode()).hexdigest()[:10], "| removed block:", repr(code[i3:j3][:120]))
st, h = get("https://nad-lan.co.il/projects/?nl694=%d" % time.time())
print("[before] /projects/ cards, cards with an exact line, cards with a range:", cards_ok(h)[:3])
if "--dry" in sys.argv:
    io.open(os.path.join(HERE, "_snippet661_ranges_new.php"), "w", encoding="utf-8", newline="\n").write(new)
    raise SystemExit(0)
os.makedirs(BK, exist_ok=True)
bkp = os.path.join(BK, "snippet-661-%s.json" % time.strftime("%Y%m%dT%H%M%S"))
io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": SID, "name": sn["name"], "code": code, "md5": hashlib.md5(code.encode()).hexdigest()}, ensure_ascii=False))
s, r = snip("PUT", "/%d" % SID, {"name": sn["name"], "code": new, "scope": sn["scope"], "active": True})
s2, back = snip("GET", "/%d" % SID, None)
ok = s == 200 and back.get("code") == new and back.get("active")
print("[write]", s, "| read-back identical and active:", ok, "| backup", os.path.relpath(bkp, REPO))
time.sleep(3)
bad = [] if ok else ["write"]
for u in ("https://nad-lan.co.il/projects/?nl694b=%d" % time.time(), "https://nad-lan.co.il/projects/page/2/?nl694b=%d" % time.time(),
          "https://nad-lan.co.il/projects/?city=%D7%97%D7%99%D7%A4%D7%94&nl694b=1"):
    st, h = get(u)
    n, nb, nr, ex = cards_ok(h)
    good = st == 200 and "Fatal error" not in h and n >= 20 and nb == 0 and nr > 0
    print("[after]", "OK " if good else "BAD", st, u.split("?")[0][-30:], "| cards", n, "| exact lines", nb, "| ranges", nr, ex[:200])
    if not good:
        bad.append(u)
st, js = get("https://nad-lan.co.il/wp-json/nadlan/v1/projects-plus?paged=2&per_page=24&nl694=1")
try:
    d = json.loads(js); n, nb, nr, ex = cards_ok(d.get("html", ""))
except Exception as e:
    n, nb, nr, ex = 0, 0, 0, str(e)[:100]
good = st == 200 and n >= 20 and nb == 0 and nr > 0
print("[after]", "OK " if good else "BAD", st, "projects-plus page 2 | cards", n, "| exact lines", nb, "| ranges", nr, ex[:200])
if not good:
    bad.append("projects-plus")
if bad:
    s, r = snip("PUT", "/%d" % SID, {"name": sn["name"], "code": code, "scope": sn["scope"], "active": True})
    raise SystemExit("ROLLED BACK (%s): %s" % (s, bad))
print("DONE")
