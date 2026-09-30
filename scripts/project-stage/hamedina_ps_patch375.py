# -*- coding: utf-8 -*-
"""Kikar Hamedina P9c (1.72.375, HAD-375, design system v104.2): the example apartment in the world, the Arabic phone's first
screen and the accessibility button's corner on the world pages, as anchored hunks on inc/project-stage.php.

The LIVE file is what 1.72.371 wrote (md5 ab944286..., deploy-result-371.json; 1.72.372 did not write it): 1.72.370's text + the
P9a hunks (hamedina_ps_patch371.release_text(), md5-checked). The release copy of 1.72.375 is that text + these hunks; the branch
file (which also carries the unreleased Batch 1/2) gets the same hunks, so the two never drift. Every anchor sits inside Kikar
Hamedina's own text (its config, the world page's parts, script and style), printed only on a world page, so the four stage
projects (Rainbow, DUO, Dimri, Ashira) are not touched: ps_identity_proof375.py renders them byte for byte, before and after.

  1. doc       : the world page's comment no longer says "no example apartment"
  2. cfg-doc   : the same in the 'hamedina' config's comment
  3. examples  : the 'hamedina' world config names the example apartment that has pictures (tower C, floors 27-33, the side that
                 faces 265.61° on floor 30; hamedina/tour/examples.json holds the files and the times)
  4. cfg       : the world's page config passes { url, list } to the world module, only when tour/examples.json is on the server
  5. mount     : mountWorld() gets the examples; the example's opening goes to analytics (stage_example)
  6. a11y      : AccessibleCorner (v104.2): on a world page the accessibility button keeps its corner and takes the nearest free
                 place above it when it would sit on a control (the page top's buttons, the world's tabs, sheet and card), never
                 onto the answer paragraph (then it stays in its corner); the site-wide button itself is not changed
  7. lane-ar   : ArabicFirstScreen (v104.2): on Arabic phones the answer paragraph is long, so the page top's buttons start 50px
                 lower; the WhatsApp bar, blocked by the buttons at its resting place, parks in that lane, clear of the buttons AND
                 of the paragraph (it rose onto the paragraph's last lines at 1.72.371)

  python scripts/project-stage/hamedina_ps_patch375.py --branch     apply the hunks to the working file (once)
  python scripts/project-stage/hamedina_ps_patch375.py              show which hunks the working file and the release carry
"""
import hashlib, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hamedina_ps_patch371 as P9  # noqa: E402  the 371 hunks (the live base of this release)

REPO = P9.REPO
REL = P9.REL
LIVE_371_MD5 = "ab9442860d0b6b22420ced51afbf02f0"  # deploy-result-371.json: what 1.72.371 wrote (1.72.372 did not write this file)
AR_LANE = "@media(max-width:600px){:root body .nlps-page--world .nlps-ctawrap[lang=\"ar\"]{margin-top:50px!important}}"

DOC_OLD = """from the floor and sets window.__nlpsPick for the WhatsApp source line. No interiors ship yet, so there is no 360, no
   example apartment and no steps row. */"""
DOC_NEW = """from the floor and sets window.__nlpsPick for the WhatsApp source line. The example apartment (P9c, design system v104.2)
   opens from the world's floor view (world/example.js and the fleet's 360 viewer, loaded on the press); there is no steps row. */"""

CFGDOC_OLD = """No interiors ship yet: no 'units', no"""
CFGDOC_NEW = """P9c: one example apartment ('examples'): no 'units', no"""

EX_OLD = """					'pond'   => true, // the pond is sourced (Mako 24.9.2026: 1 m deep); its outline is drawn and labelled "הדמיה להמחשה בלבד\""""
EX_NEW = """					'pond'   => true, // the pond is sourced (Mako 24.9.2026: 1 m deep); its outline is drawn and labelled "הדמיה להמחשה בלבד"
					// P9c (design system v104.2): the example apartment that has pictures (Blender Cycles from the world's data,
					// docs/research/2026-09-30-kikar-hamedina/interiors-plan.md): tower C, floor 30, the side that faces 265.61° there;
					// it turns with the tower, so floors 27-33 show the same apartment (the album says the pictures are from floor 30).
					// Its files and times are in assets/project-stage/hamedina/tour/examples.json, read only on the button's press.
					'examples' => array(
						array( 'id' => 'c30w', 'tower' => 'C', 'floor' => 30, 'band' => array( 27, 33 ), 'bearing' => 265.61 ),
					),"""

CFG_OLD = """			'pond'   => ! array_key_exists( 'pond', $pw ) || ! empty( $pw['pond'] ),"""
CFG_NEW = """			'pond'   => ! array_key_exists( 'pond', $pw ) || ! empty( $pw['pond'] ),
			// P9c (v104.2): which tower, floors and side have an example apartment; its manifest loads only on the press
			'examples' => ! empty( $pw['examples'] ) && is_readable( dirname( __DIR__ ) . '/' . $base . 'tour/examples.json' )
				? array( 'url' => plugins_url( $base . 'tour/examples.json', dirname( __FILE__ ) ) . $v, 'list' => array_values( (array) $pw['examples'] ) ) : null,"""

MOUNT_OLD = """      intent: 'visible', mode: c.mode, season: c.season, hour: c.hour, pond: c.pond !== false });"""
MOUNT_NEW = """      intent: 'visible', mode: c.mode, season: c.season, hour: c.hour, pond: c.pond !== false, examples: c.examples || null });"""

A11Y_OLD = """  addEventListener('nl:facing', (e) => { const d = e.detail || {}; if (d.source === 'user') ga('stage_facing', { tower: d.tower, floor: d.floor, facing: d.facing }); });
}"""
A11Y_NEW = """  addEventListener('nl:facing', (e) => { const d = e.detail || {}; if (d.source === 'user') ga('stage_facing', { tower: d.tower, floor: d.floor, facing: d.facing }); });
  addEventListener('nl:example', (e) => { const d = e.detail || {}; if (d.open) ga('stage_example', { tower: d.tower, floor: d.floor, facing: d.facing, example: d.id }); });
  /* AccessibleCorner (design system v104.2, P9c): the accessibility button (inc/accessibility.php) keeps its bottom corner (the
     owner, 25.9.2026). On this page the world's tab bar and sheet, and the page top's buttons, pass under that corner as the
     visitor scrolls (the first tab "מבט על" on the Hebrew phone's first screen); there the button takes the nearest free place
     above its corner, in its own column, and comes back when the corner is free. It never moves onto the answer paragraph: with no
     free place clear of it, it stays in its corner. It measures from its corner (its own lift is taken out), so it never
     flickers; while its panel is open it does not move. */
  (() => {
    const box = document.getElementById('nla11y'), btn = document.getElementById('nla11y-btn');
    if (!box || !btn) return;
    const CTRL = '.nlps-hero__cta a,#nlps .nlw-top button,#nlps .nlw-panel button,#nlps .nlw-panel input,#nlps .nlw-panel a,#nlps .nlw-card button,#nlps .nlw-card a,#nlps .nlw-compass button,#nlps .nlw-enter';
    let lift = 0, raf = 0;
    const fit = () => {
      raf = 0;
      const pan = document.getElementById('nla11y-panel');
      if (pan && !pan.hidden) return;
      if (document.querySelector('#nlps .nlw--full')) return; // the world fills the screen above the page: nothing to clear
      const r = btn.getBoundingClientRect();
      if (!r.width) return;
      const h = r.height, t0 = r.top + lift, l = r.left - 6, rr = r.right + 6, vh = innerHeight;
      const col = (q) => q.height && q.right > l && q.left < rr && q.bottom > 0 && q.top < vh;
      const hard = [...document.querySelectorAll(CTRL)].map((e) => e.getBoundingClientRect()).filter(col).map((q) => [q.top - 8, q.bottom + 8]);
      const soft = [...document.querySelectorAll('.nl-lead')].map((e) => e.getBoundingClientRect()).filter(col).map((q) => [q.top - 4, q.bottom + 4]);
      const hit = (t, L) => L.some(([a, b]) => t < b && t + h > a);
      let best = 0;
      if (hit(t0, hard)) {
        best = 0;
        for (let d = 4; d <= vh * 0.5; d += 4) { const t = t0 - d; if (t < 76) break; if (!hit(t, hard)) { best = hit(t, soft) ? 0 : d; break; } }
      }
      if (best !== lift) { lift = best; box.style.transform = lift ? 'translateY(' + (-lift) + 'px)' : ''; }
    };
    const ask = () => { if (!raf) raf = requestAnimationFrame(fit); };
    box.style.transition = matchMedia('(prefers-reduced-motion: reduce)').matches ? '' : 'transform .18s ease';
    addEventListener('scroll', ask, { passive: true });
    addEventListener('resize', ask);
    for (const ev of ['nl:floor', 'nl:facing', 'nl:example', 'load']) addEventListener(ev, ask);
    document.addEventListener('click', () => setTimeout(ask, 80), true);
    setTimeout(ask, 1200); setTimeout(ask, 3000);
    ask();
  })();
}"""

LANE_OLD = """		. '@media(max-width:600px){:root body .nlps-page--world>.nlps-stagebox{margin-top:50px!important}}'"""
LANE_NEW = """		. '@media(max-width:600px){:root body .nlps-page--world>.nlps-stagebox{margin-top:50px!important}}'
		// ArabicFirstScreen (design system v104.2, P9c): the Arabic answer paragraph is about three lines longer, so on a phone its
		// buttons sat where the WhatsApp bar rests and the bar rose onto the paragraph's last lines. A 50px lane above the buttons:
		// the bar, blocked by them, parks between the paragraph and the buttons, clear of both
		. '""" + AR_LANE + """'"""

HUNKS = [
    ("doc", DOC_OLD, DOC_NEW),
    ("cfg-doc", CFGDOC_OLD, CFGDOC_NEW),
    ("examples", EX_OLD, EX_NEW),
    ("cfg", CFG_OLD, CFG_NEW),
    ("mount", MOUNT_OLD, MOUNT_NEW),
    ("a11y", A11Y_OLD, A11Y_NEW),
    ("lane-ar", LANE_OLD, LANE_NEW),
]


def apply(text, label=""):
    for name, old, new in HUNKS:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"FATAL P9c hunk {name}: anchor x{n} in {label}")
        text = text.replace(old, new)
    return text


def carries(text):
    return {name: (new in text) for name, old, new in HUNKS}


def live371():
    """the text 1.72.371 wrote (370's text + the P9a hunks), checked against its recorded md5"""
    t = P9.release_text()
    m = hashlib.md5(t.encode("utf-8")).hexdigest()
    if m != LIVE_371_MD5:
        raise SystemExit(f"FATAL: 370 + the P9a hunks is {m}, not what 1.72.371 wrote ({LIVE_371_MD5})")
    return t


def release_text(base=None):
    """the release copy: the given live base text (default: what 1.72.371 wrote) + the P9c hunks"""
    return apply(base if base is not None else live371(), "the release base")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    path = os.path.join(REPO, *REL.split("/"))
    cur = io.open(path, encoding="utf-8", newline="").read()
    if "--branch" in sys.argv:
        if all(carries(cur).values()):
            print("the working file already carries every P9c hunk")
        else:
            io.open(path, "w", encoding="utf-8", newline="").write(apply(cur, "the working file"))
            print("applied", [h[0] for h in HUNKS], "to", REL)
    else:
        print("working file:", carries(cur))
        r = release_text()
        print("release copy (371 + P9c):", hashlib.md5(r.encode("utf-8")).hexdigest(), carries(r))
