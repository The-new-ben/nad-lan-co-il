# -*- coding: utf-8 -*-
"""THE MAKER OF 1.72.732 as it ran (kept under this name because another session wrote its own make_deploy732.py over it at 13:20 on
21.11.2026, while this release was in flight; see docs/coordination/claude-codex.md). deploy732.py was built from THIS text.

1.72.732 = HAD-787, Claude Design board 25 (Ben 21.11.2026, through the coordinator session: "a gentle link, exactly in the right
place" from /property-value-estimator/ to the forum, where people ask what their home is worth).
  SWAP assets/instruments/tools/pval.js: one quiet row inside the result, right after the note that ends "הערכה ראשונית, לא חוות דעת
       שמאית": heading, one line, the link "שאלו בפורום על הדירה שלכם" and a tick that carries city, neighbourhood, rooms, size and the
       estimate (sessionStorage, never the address). Hebrew pages, median results only, and only after the visitor changed a value.
       Events: est_forum_row, est_forum_press {carry}.
  SWAP assets/proforum/home.js, home.css: /forum/#ask-home opens the form "כמה הדירה שלכם שווה" for every visitor, filled with what
       was carried, with a chip whose X takes it out; a guest's filled form waits for him through the one-step entry. Events:
       est_forum_arrive {filled}, est_forum_remove. Nothing is published before "להציג לפורום".
The three live files were byte-equal to the repo's HEAD before the change. Checked BEFORE the release on the live pages with the three
files routed in (scripts/project-stage/est_forum_live_check.py, LOCAL=1): 28 of 28 on phone width and desktop.
Link text checked with tools/seo/kw_guard.py: OK, no protected term."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 731
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
A = "/wp-content/plugins/nadlan-config/assets/"
ROWS = ("    ('%sinstruments/tools/pval.js?t732e=1', ['nlfh_from_est', 'est_forum_press', 'nlpvf-a', 'NI.register'], ['Fatal error'], []),\n"
        "    ('%sproforum/home.js?t732e=1', ['#ask-home', 'nlfh_from_est', 'est_forum_arrive', 'home/vote'], ['Fatal error'], []),\n"
        "    ('%sproforum/home.css?t732e=1', ['.nlfh-from-x', '.nlfh-chipbtn'], ['Fatal error'], []),\n"
        "    ('/property-value-estimator/?t732e=1', ['data-nli=\"pval\"', 'instruments/tools/pval.js?ver=1.72.732', '<h1'], %r, []),\n"
        "    ('/forum/?t732e=1', ['nlf-dir', 'id=\"nlfh-compose\"', 'proforum/home.js'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t732e=1', ['\"status\":\"ok\"'], %r, []),\n") % (A, A, A, E, E, E)
if __name__ == "__main__" and "--build" in sys.argv:  # never by accident: the release already ran
    kl_release.build_release(PREV, 732, ["assets/instruments/tools/pval.js", "assets/proforum/home.js", "assets/proforum/home.css"], [], {}, {}, ROWS,
                             "value estimator: one quiet row after the result, to the forum's form about your own apartment, filled on the visitor's tick",
                             "HAD-787 board 25: from the value estimator to the forum")
