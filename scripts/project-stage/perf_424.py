# -*- coding: utf-8 -*-
"""Release 1.72.424 (HAD-421 step 5, the Kikar loop turn 34, design v104.47): start the world's downloads early, quietly.
Measured 5.10 (phone, slow 4G): world.js is imported only after load + idle and finishes at 7.9 s; three.js and world.json
then download from 8.0 to 11.6 s; the scene is usable at 15.5 s. The network is partly idle before that. The world page's head
now hints all three at LOW priority (modulepreload three.js and world.js, preload world.json as fetch), so they fill idle
bandwidth without competing with the first paint; mount() still runs on intent and finds them in the cache.
This reverses the v104 "three.js waits for intent" head rule on purpose (the inherited never-check is narrowed to the eager
form). Applied to the LIVE inc/project-stage.php text (what 1.72.423 wrote): nadlan_ps_world_head, exactly once."""

RELS = ["inc/project-stage.php"]
FILES = {}
ANCHOR = ("\t\techo '<link rel=\"preload\" as=\"image\" type=\"image/webp\" href=\"' . esc_url( $m['wide'] ) . '\" media=\"(min-width:701px)\" "
          "fetchpriority=\"high\">' . \"\\n\";\n")
ADD = """		// v104.47 (HAD-421): the world's three biggest files start at once, at low priority, so the network is never idle while
		// the page paints; mount() still runs on intent and finds them in the cache (the same URLs as the stage's data-cfg)
		$v    = '?ver=' . nadlan_ps_ver();
		$base = 'assets/project-stage/' . $ps['dir'] . '/';
		$pw   = (array) $ps['world'];
		echo '<link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js" crossorigin fetchpriority="low">' . "\\n";
		echo '<link rel="modulepreload" href="' . esc_url( plugins_url( 'assets/project-stage/world/world.js', dirname( __FILE__ ) ) . $v ) . '" fetchpriority="low">' . "\\n";
		echo '<link rel="preload" as="fetch" href="' . esc_url( plugins_url( $base . (string) ( $pw['data'] ?? 'world.json' ), dirname( __FILE__ ) ) . $v ) . '" crossorigin fetchpriority="low">' . "\\n";
"""


def apply(rel, txt):
    if "v104.47 (HAD-421)" in txt:
        raise SystemExit("perf_424: already applied")
    if txt.count(ANCHOR) != 1:
        raise SystemExit("perf_424: the world head anchor is there " + str(txt.count(ANCHOR)) + " times")
    return txt.replace(ANCHOR, ANCHOR + ADD)
