# -*- coding: utf-8 -*-
"""HAD-801 polish loop cycle 4: the /sde-dov/ walk entry plays a real 7 s silent walk recorded from the live tour (AST-12109/12110,
files under <site root>/tour/sde-dov/media/wordpress/clips/). The video is created only when the entry comes into view, never on the
home page, never with reduced motion or Save-Data; the still and its drift stay underneath and the illustration caption stays on top.
One hunk on inc/sdedov-teaser.php (live text bfe3c8025a, released in 1.72.744).
  python make_deploy_clip.py <prev release number>   (writes deploy<prev+1>.py through kl_release.build_release)"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = int(sys.argv[1]); NEW = PREV + 1
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REL = "inc/sdedov-teaser.php"
LIVE = open(os.path.join(REPO, "plugins", "nadlan-config", *REL.split("/")), encoding="utf-8").read()
MD5 = hashlib.md5(LIVE.encode("utf-8")).hexdigest()
assert MD5.startswith("bfe3c8025a"), ("the repo copy is not the 1.72.744 live text", MD5)
JS = ("(function(){var f=document.querySelector('.nlqw-host .nlq-cover');if(!f||!('IntersectionObserver' in window))return;"
      "try{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;}catch(e){}"
      "var c=navigator.connection;if(c&&(c.saveData||/2g/.test(c.effectiveType||'')))return;"
      "var st=document.createElement('style');st.textContent='.nlq .nlq-cover .nlqw-clip{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .7s;z-index:1}.nlq .nlq-cover .nlqw-clip.on{opacity:1}.nlq .nlq-cover figcaption{z-index:2}';document.head.appendChild(st);"
      "var io=new IntersectionObserver(function(es){if(!es[0].isIntersecting)return;io.disconnect();"
      "var v=document.createElement('video');v.muted=true;v.defaultMuted=true;v.loop=true;v.playsInline=true;"
      "v.setAttribute('muted','');v.setAttribute('playsinline','');v.setAttribute('aria-hidden','true');v.className='nlqw-clip';v.preload='auto';"
      "v.src=(window.innerWidth<641?'__PHONE__':'__DESK__');"
      "v.addEventListener('playing',function(){v.classList.add('on')});"
      "f.insertBefore(v,f.querySelector('figcaption'));var p=v.play();if(p&&p.catch)p.catch(function(){});},{rootMargin:'150px'});io.observe(f);})();")
H = []
H.append(("\treturn substr( $content, 0, $j ) . '<div class=\"nlqw-host\" id=\"walk\">' . nadlan_walk_render( array() ) . '</div>' . substr( $content, $j );",
          "\treturn substr( $content, 0, $j ) . '<div class=\"nlqw-host\" id=\"walk\">' . nadlan_walk_render( array() ) . '</div>' . nadlan_sdedov_walk_clip() . substr( $content, $j );"))
H.append(("add_filter( 'the_content', 'nadlan_sdedov_walk_entry', 22 );",
          "add_filter( 'the_content', 'nadlan_sdedov_walk_entry', 22 );\n\n"
          "/* HAD-801 loop cycle 4: the entry starts walking by itself. A 7 s silent loop recorded from the live tour (AST-12109/12110) is\n"
          " * created only when the entry comes into view; reduced motion and Save-Data keep the still. Only on /sde-dov/ (called from the\n"
          " * entry filter), never on the home page. */\n"
          "function nadlan_sdedov_walk_clip() {\n"
          "\t$base = trailingslashit( nadlan_sdedov_tour_url() ) . 'media/wordpress/clips/sde-dov-2036-entry-walk-';\n"
          "\treturn '<script id=\"nlqw-clip-js\">' . str_replace( array( '__PHONE__', '__DESK__' ), array( esc_url( $base . 'phone.mp4' ), esc_url( $base . 'desktop.mp4' ) ), "
          + "'" + JS.replace("\\", "\\\\").replace("'", "\\'") + "'" + " ) . '</script>';\n"
          "}"))
for a, b in H:
    assert LIVE.count(a) == 1, ("anchor x%d" % LIVE.count(a), a[:70])
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
ROWS = ("    ('/sde-dov/?tclip=1', ['data-nlq', 'id=\"walk\"', 'nlqw-clip', 'media/wordpress/clips/sde-dov-2036-entry-walk-phone.mp4', 'הדמיה להמחשה, על פי התכנית', 'class=\"nlam'], %s, []),\n"
        "    ('/?tclip=1', ['nlhp-svcard--tour'], ['Fatal error', 'sde-dov-2036-entry-walk-'], []),\n"
        "    ('/tour/sde-dov/media/wordpress/clips/sde-dov-2036-entry-walk-phone.mp4', [], [], []),\n") % BAD
kl_release.build_release(PREV, NEW, [], [], {REL: H}, {REL: MD5}, ROWS,
                         "the /sde-dov/ walk entry plays a 7 s silent walk from the live tour when it comes into view",
                         "HAD-801 loop cycle 4: entry walk clip")
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy%d.py" % NEW)
_t = open(_d, encoding="utf-8").read()
_a = '            s, html = page(path + sep + "nlv=" + tag)\n'
if _t.count(_a) == 1 and "time.sleep(0.7)" not in _t:
    _t = _t.replace(_a, '            time.sleep(0.7)\n' + _a + '            for _k in range(3):\n                if s != 429:\n                    break\n'
                    '                print(f"[page] 429 on {path[:70]}: waiting {30 * (_k + 1)} s")\n                time.sleep(30 * (_k + 1))\n'
                    '                s, html = page(path + sep + "nlv=" + tag + "q%d" % _k)\n')
    open(_d, "w", encoding="utf-8", newline=chr(10)).write(_t)
    print("runner: 0.7 s pause per check, 429 retried")
