# -*- coding: utf-8 -*-
"""Writes deploy415.py from the released and verified deploy414.py: release 1.72.415 = urban's HAD-396 (urban-renewal honesty),
Maya's round-4 ACCEPT, package 0663be07 (ur_396.py), main's code-owner PASS. In ONE release, as the package says:
  - 16 plugin files (the live text must equal the package's live base; then the pinned patched bytes), .bak415;
  - snippet 661 (x-catalog-plus) code, linted on the server with "<?php", fresh before-hash;
  - page 73 content.raw and 3 Yoast metas (73 metadesc, 5471 title + metadesc), each with its fresh before-hash.
Three new bridge ops (lint_code, pcontent, pmeta); every write is undone by rollback() in reverse order. The data patch is NOT run."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ur_396  # noqa: E402  (verifies the pinned package on import)
s = io.open(os.path.join(HERE, "deploy414.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


BRIDGE_OPS = r"""			if ( isset( $b['lint_code'] ) ) { // 1.72.415: a Code Snippets code body, linted as PHP with the opening tag it is stored without
				try { token_get_all( "<?php\n" . (string) $b['lint_code'], TOKEN_PARSE ); $out['lint_code'] = 'ok'; }
				catch ( ParseError $e ) { return new WP_Error( 'lint', $e->getMessage() . ' line ' . $e->getLine(), array( 'status' => 400 ) ); }
			}
			if ( ! empty( $b['pcontent'] ) && is_array( $b['pcontent'] ) ) { // 1.72.415: a page's raw content, guarded by its md5
				$c = $b['pcontent']; $pid = (int) $c['id']; $cur = (string) get_post_field( 'post_content', $pid, 'raw' );
				if ( ! empty( $c['get'] ) ) { $out['pcontent'] = array( 'md5' => md5( $cur ), 'bytes' => strlen( $cur ) ); }
				else {
					if ( empty( $c['force'] ) && md5( $cur ) !== (string) $c['expect'] ) { return new WP_Error( 'drift', 'content changed: ' . md5( $cur ), array( 'status' => 409 ) ); }
					$new = base64_decode( (string) $c['b64'], true );
					if ( false === $new || md5( $new ) !== (string) $c['md5'] ) { return new WP_Error( 'md5', 'content mismatch', array( 'status' => 400 ) ); }
					kses_remove_filters();
					$r = wp_update_post( wp_slash( array( 'ID' => $pid, 'post_content' => $new ) ), true );
					if ( is_wp_error( $r ) ) { return $r; }
					clean_post_cache( $pid );
					$now = (string) get_post_field( 'post_content', $pid, 'raw' );
					do_action( 'litespeed_purge_post', $pid );
					$out['pcontent'] = array( 'md5' => md5( $now ), 'bytes' => strlen( $now ) );
				}
			}
			if ( ! empty( $b['pmeta'] ) && is_array( $b['pmeta'] ) ) { // 1.72.415: one Yoast meta, guarded by its md5
				$m = $b['pmeta']; $pid = (int) $m['id']; $key = (string) $m['key'];
				if ( 0 !== strpos( $key, '_yoast_wpseo_' ) ) { return new WP_Error( 'key', 'only Yoast metas', array( 'status' => 400 ) ); }
				$cur = (string) get_post_meta( $pid, $key, true );
				if ( ! empty( $m['get'] ) ) { $out['pmeta'] = array( 'md5' => md5( $cur ) ); }
				else {
					if ( empty( $m['force'] ) && md5( $cur ) !== (string) $m['expect'] ) { return new WP_Error( 'drift', 'meta changed: ' . md5( $cur ), array( 'status' => 409 ) ); }
					$val = base64_decode( (string) $m['b64'], true );
					if ( false === $val || md5( $val ) !== (string) $m['md5'] ) { return new WP_Error( 'md5', 'meta mismatch', array( 'status' => 400 ) ); }
					update_post_meta( $pid, $key, wp_slash( $val ) );
					$now = (string) get_post_meta( $pid, $key, true );
					do_action( 'litespeed_purge_post', $pid );
					$out['pmeta'] = array( 'md5' => md5( $now ) );
				}
			}
			if ( ! empty( $b['purge'] ) ) {"""
rep("\t\t\tif ( ! empty( $b['purge'] ) ) {", BRIDGE_OPS)

# ---- the files: the 16 of the package, through the live-text loop
rep('PHP_RELS = ["inc/project-stage.php"]  # 1.72.414: the facilities clip hunk on the live text (v104.36), restored from .bak414 on rollback',
    "PHP_RELS = " + repr(ur_396.RELS) + "  # 1.72.415: HAD-396, the package's 16 files on the live text, restored from .bak415 on rollback\n"
    "import ur_396 as UR  # noqa: E402\n"
    "UNDO = []  # 1.72.415: the snippet / page / meta writes, undone by rollback() in reverse order\n"
    "LIVE_SNIPPET = {}")
rep("    import film_414 as PX  # noqa: E402 (1.72.414: the facilities clip under the film)\n", "    import ur_396 as PX  # noqa: E402 (1.72.415: HAD-396, package 0663be07)\n")
rep('    for _rel in ("inc/project-stage.php",):\n', '    for _rel in PX.RELS:\n')
rep("        _txt = PX.apply(_txt)\n", "        _txt = PX.apply(_rel, _txt)\n")
rep('        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.414 facilities clip)")\n',
    '        if _rel.endswith(".php"):\n            php_lint(PHPNEW[_rel], _rel + " (the HAD-396 package bytes)")\n'
    '        if md5(PHPNEW[_rel]) != md5(PX.FILES[_rel][1]):\n            raise SystemExit("FATAL: " + _rel + " is not the package bytes after the line endings")\n')
rep('_rel.replace("inc/", "") + f".{stamp}.live"', '_rel.replace("/", "__") + f".{stamp}.live"')

# ---- fresh before-hashes of the snippet, the page and the metas (also on --dry), before nadlan-config.php is read
rep('    cur_main = live_get("nadlan-config.php")\n', '''    _s, _sn = snip("GET", "/661"); must(_s, _sn, "snippet 661 read")
    LIVE_SNIPPET["code"] = _sn.get("code") or ""
    if md5(LIVE_SNIPPET["code"].encode("utf-8")) != PX.SNIPPET["live_md5"]:
        raise SystemExit("FATAL: snippet 661 is " + md5(LIVE_SNIPPET["code"].encode("utf-8"))[:10] + ", the package's base is " + PX.SNIPPET["live_md5"][:10])
    if not _sn.get("active"):
        raise SystemExit("FATAL: snippet 661 is not active before the release")
    ops({"lint_code": PX.SNIPPET["code"]}, "snippet 661 lint on the server")
    _pc = ops({"pcontent": {"id": 73, "get": 1}}, "page 73 read")["pcontent"]
    if _pc["md5"] != PX.PAGE["before_md5"]:
        raise SystemExit("FATAL: page 73 content is " + _pc["md5"][:10] + ", the package's before is " + PX.PAGE["before_md5"][:10])
    for _m in PX.METAS:
        _g = ops({"pmeta": {"id": _m["id"], "key": _m["key"], "get": 1}}, "meta read")["pmeta"]
        if _g["md5"] != _m["before_md5"]:
            raise SystemExit(f"FATAL: meta {_m['id']} {_m['key']} is {_g['md5'][:10]}, the package's before is {_m['before_md5'][:10]}")
    print("[drift] snippet 661 (lint ok on the server), page 73 and the 3 metas: the package's before-hashes, fresh")
    cur_main = live_get("nadlan-config.php")
''')

# ---- the writes: after the files and the bump, inside the same try (a refusal rolls everything back)
rep('        put("nadlan-config.php", new_main, expect=md5(live_main))\n', '''        put("nadlan-config.php", new_main, expect=md5(live_main))
        # 1.72.415: snippet 661, page 73, the 3 metas; each guarded by its fresh before-hash, each undone by rollback()
        UNDO.append(("snippet", None))
        _s, _u = snip("PUT", "/661", {"name": "x-catalog-plus", "code": PX.SNIPPET["code"], "scope": "global", "active": False}); must(_s, _u, "snippet 661 update")
        _s, _a = snip("PUT", "/661/activate", {}); must(_s, _a, "snippet 661 activate")
        _s, _sn = snip("GET", "/661"); must(_s, _sn, "snippet 661 read back")
        if md5((_sn.get("code") or "").encode("utf-8")) != PX.SNIPPET["md5"] or not _sn.get("active"):
            raise SystemExit("FATAL: snippet 661 after the update is not the package code or not active")
        print("[snippet] 661 x-catalog-plus: " + PX.SNIPPET["md5"][:10] + ", active")
        UNDO.append(("page", None))
        _r = ops({"pcontent": {"id": 73, "expect": PX.PAGE["before_md5"], "b64": base64.b64encode(PX.PAGE["after"]).decode(), "md5": PX.PAGE["after_md5"]}}, "page 73 write")["pcontent"]
        if _r["md5"] != PX.PAGE["after_md5"]:
            raise SystemExit("FATAL: page 73 after the write is " + _r["md5"][:10])
        print("[page] 73 content: " + PX.PAGE["after_md5"][:10])
        for _m in PX.METAS:
            UNDO.append(("meta", _m))
            _r = ops({"pmeta": {"id": _m["id"], "key": _m["key"], "expect": _m["before_md5"], "b64": base64.b64encode(_m["after"]).decode(), "md5": _m["after_md5"]}}, "meta write")["pmeta"]
            if _r["md5"] != _m["after_md5"]:
                raise SystemExit(f"FATAL: meta {_m['id']} {_m['key']} after the write is {_r['md5'][:10]}")
            print(f"[meta] {_m['id']} {_m['key']}: {_m['after_md5'][:10]}")
''')

# ---- rollback: undo the snippet / page / metas first, in reverse order
rep('def rollback(created_any, posts_state=None):\n    print("[rollback] restoring .bak414 files")\n', '''def rollback(created_any, posts_state=None):
    for _kind, _m in reversed(UNDO):  # 1.72.415: the writes that are not files
        try:
            if _kind == "snippet" and LIVE_SNIPPET.get("code"):
                _s1, _ = snip("PUT", "/661", {"name": "x-catalog-plus", "code": LIVE_SNIPPET["code"], "scope": "global", "active": False})
                _s2, _ = snip("PUT", "/661/activate", {})
                print("[rollback] snippet 661 restored", _s1, _s2)
            elif _kind == "page":
                print("[rollback] page 73", ops({"pcontent": {"id": 73, "force": 1, "b64": base64.b64encode(UR.PAGE["before"]).decode(), "md5": UR.PAGE["before_md5"]}}, "page 73 restore").get("pcontent"))
            elif _kind == "meta":
                print("[rollback] meta", _m["id"], _m["key"], ops({"pmeta": {"id": _m["id"], "key": _m["key"], "force": 1, "b64": base64.b64encode(_m["before"]).decode(), "md5": _m["before_md5"]}}, "meta restore").get("pmeta"))
        except BaseException as _e:  # keep undoing the rest; the record shows what could not be undone
            print("[rollback] COULD NOT UNDO", _kind, _e)
    print("[rollback] restoring .bak414 files")
''')
rep('print("RELEASE 1.72.414 LIVE: the Kikar film, option B: the 19.7 s facilities clip under the film, labelled before play, in the page\'s language")',
    'print("RELEASE 1.72.415 LIVE: HAD-396 urban-renewal honesty (16 files + snippet 661 + page 73 + 3 metas), Maya round-4 ACCEPT; the data patch not run")')
rep("""    ("/projects/rainbow-tel-aviv/", ['class="nlps-page"'], ['nlws-facilities']),
]
""", """    ("/projects/rainbow-tel-aviv/", ['class="nlps-page"'], ['nlws-facilities']),
]
# 1.72.415 (HAD-396, urban's package 0663be07): the statute's special majority, the honest registry words, no seeded figures
CHECKS += [
    ("/urban-renewal/", ['כך מגדיר את זה חוק פינוי ובינוי', 'המאגר כולל מתחמים מוכרזים וגם מתחמים שטרם הוכרזו', 'data-num="2" data-den="3"', 'var E=function(s)', '7 שאלות קצרות, ותקבלו כיוון ראשוני', 'acted=false'], ['66% לקידום מתחם פינוי בינוי', '67% לתביעת דייר סרבן', 'data-adv=', 'שש שאלות קצרות', 'class="nlur-src"']),
    ("/urban-renewal/map/", ['מפת התחדשות עירונית בישראל: מתחמי פינוי בינוי לפי עיר', 'מתחמי התחדשות עירונית בישראל לפי עיר'], ['מתחמי התחדשות עירונית מוכרזים בישראל - לפי עיר']),
    ("/sell-by-auction/", ['9 שאלות קצרות, בלי טפסים אפורים', 'הטופס הקצר למטה: 9 שאלות', 'acted=false'], ['שמונה שאלות קצרות', 'שמונה שאלות. אנחנו']),
    ("/buying-apartment/", ['8 שאלות, ונכוון אתכם', 'acted=false'], ['שש שאלות, ונכוון']),
    ("/projects/", ['ובמתחמי התחדשות שנת תוקף התוכנית'], []),
    ("/professionals/demo-avnei-madad-shamai/", ['<h1'], ['class="nlpp-stats"']),
]
""")
for x, y in (("1.72.414", "1.72.415"), (".bak414", ".bak415"), ("PS414", "PS415"), ("ps414", "ps415"), ("deploy414", "deploy415"),
             ("result-414", "result-415"), ("speed-414", "speed-415"), ("posts-before-414", "posts-before-415"), ("make_deploy414", "make_deploy415")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-413.json")', '_prev = os.path.join(QA, "deploy-result-414.json")'),
             ('"FATAL: release 1.72.413 is still in flight', '"FATAL: release 1.72.414 is still in flight'),
             ('WANT_LIVE = "1.72.413"  # the checks name ?ver=1.72.415: this runner is for the release right after 1.72.413',
              'WANT_LIVE = "1.72.414"  # the checks name ?ver=1.72.415: this runner is for the release right after 1.72.414'),
             ("        for n in range(413, 329, -1):", "        for n in range(414, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy415.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy415.py")
