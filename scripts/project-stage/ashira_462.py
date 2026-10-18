# -*- coding: utf-8 -*-
"""Release 1.72.462 (HAD-543, Ben 18.10.2026 "fix before the meeting"): the "nearby projects to compare" table on a project's
language pages listed the project itself (the Hebrew twin, about 11 m away: "ASHIRA Sde Dov ~75,000 11 m"). Siblings with a
-en/-fr/-ru/-ar slug were skipped, the base page was not. Now any project closer than 60 m (the same building) is skipped, and
the cache key moves to v3 so every page drops the stale list at once. One hunk on the LIVE text of inc/project-experience.php."""
RELS = ["inc/project-experience.php"]
OLD_KEY = "\t\t$key = 'nlpjx_comps_v2_' . $id;"
NEW_KEY = "\t\t$key = 'nlpjx_comps_v3_' . $id; // 1.72.462: v3 drops the lists that held the page's own twin"
OLD_DIST = "\t\t\t$dist = (int) round( 111320 * sqrt( pow( $plat - $lat, 2 ) + pow( ( $plng - $lng ) * cos( deg2rad( $lat ) ), 2 ) ) );\n"
NEW_DIST = OLD_DIST + "\t\t\tif ( $dist < 60 ) { continue; } // 1.72.462: the same building (the page's own language twin) is never a comp\n"


def apply(rel, txt):
    if rel != "inc/project-experience.php":
        raise SystemExit("ashira_462: no hunk on " + rel)
    for old, new in ((OLD_KEY, NEW_KEY), (OLD_DIST, NEW_DIST)):
        n = txt.count(old)
        if n != 1:
            raise SystemExit(f"ashira_462: anchor x{n} in the live {rel}: {old.strip()[:70]!r}")
        txt = txt.replace(old, new)
    return txt
