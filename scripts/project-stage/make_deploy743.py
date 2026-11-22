# -*- coding: utf-8 -*-
"""make deploy743.py from deploy742.py: 1.72.743 = the DUO Tel Aviv fact audit (coordinator order 22.11.2026: the DUO page must be
beyond reproach before Ben writes to Africa Israel Residences). Audit: docs/research/2026-11-22-duo-audit/AUDIT-HE.md.
The five DUO posts were already corrected through scripts/duo/ (backups and read-backs in docs/research/2026-11-22-duo-audit/backup/).
This release fixes the DUO data in inc/project-stage.php (hunks computed from the LIVE text, docs/qa/live-read/20261122T154515Z):
  - the fact strip: 2 towers of 50 floors (the developer, Yashar Architects and Electra publish 50; the 54-floor line goes);
  - the "372 of 510 sold" summary line goes (nothing about the company's sales);
  - the three floor-tied 2021 deals go: the company reported them as pre-sales to related parties, which is corporate detail and,
    without that label, would read as market prices (the price block's matching row goes too);
  - in the price block: the sales clause and the sold-count item go, the two asking prices from resale listings go (unsupported),
    and the unsourced "2 rooms, per the developer" row goes.
Three INHERITED check rows required the removed deals header, the related-party line, "372 מתוך 510" and data-nlps-floor="17";
those tokens are trimmed from them (the rows keep their other checks)."""
import os, sys, json, re, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV, NEW = 742, 743
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIVE = open(os.path.join(REPO, "docs", "qa", "live-read", "20261122T154515Z", "inc", "project-stage.php"), encoding="utf-8").read()
LIVE_MD5 = hashlib.md5(LIVE.encode("utf-8")).hexdigest()
assert LIVE_MD5.startswith("49f38e94b6"), LIVE_MD5

H = []
H.append(("array( 'בניינים', '2 מגדלים של 54 קומות', '50 קומות מגורים בכל מגדל' ),",
          "array( 'בניינים', '2 מגדלים של 50 קומות', 'לפי אתר הפרויקט, ישר אדריכלים ואלקטרה' ),"))
H.append(("\t\t\t\t\tarray( '372 מתוך 510', 'דירות נמכרו עד 6.2026, לפי דוח היזם' ),\n", ""))
# the three related-party pre-sale rows of 'deals' (DUO): from the first row to the line before the array's close
i = LIVE.find("'duo-tel-aviv' => array(")
a = LIVE.find("\t\t\t\t\tarray( 'floor' => '17', 'n' => 17, 'bld' => 'הבניין השני בפרויקט'", i)
b = LIVE.find("\t\t\t\t\tarray( 'floor' => '12', 'n' => 12, 'bld' => 'הבניין השני בפרויקט'", a)
b = LIVE.find("\n", b) + 1
assert i > 0 and a > i and b > a and LIVE[a:b].count("'floor' =>") == 3, (i, a, b)
H.append((LIVE[a:b], ""))
# the price block (PriceGuide, duo-tel-aviv|he)
pg = LIVE.find("case 'duo-tel-aviv|he'")
blk = LIVE[pg:pg + 17500]
H.append((', ועד <span class="nlds-num">6.2026</span> נמכרו <span class="nlds-num">372</span> מתוך <span class="nlds-num">510</span> הדירות.', '.'))
H.append(('<li><b><span class="nlds-num">372</span> מתוך <span class="nlds-num">510</span></b><span>דירות נמכרו בפרויקט, לפי דוחות היזם</span><i><span class="nlds-num">6.2026</span></i></li>', ''))
for pat in (r'<tr>(?:(?!</tr>).)*?nlpg__k--ask(?:(?!</tr>).)*?</tr>', r'<tr>(?:(?!</tr>).)*?<span>לפי היזם</span>(?:(?!</tr>).)*?</tr>',
            r'<tr>(?:(?!</tr>).)*?שלוש עסקאות במכירה המוקדמת(?:(?!</tr>).)*?</tr>'):
    for m in re.finditer(pat, blk, re.S):
        H.append((m.group(0), ""))
for old, new in H:
    assert LIVE.count(old) == 1, ("anchor x%d" % LIVE.count(old), old[:90])
print("hunks:", len(H))

A = "/wp-content/plugins/nadlan-config/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
ROWS = ("    ('/projects/duo-tel-aviv/?t743d=1', ['id=\"nlps\"', 'mountDuoStage', '2 מגדלים של 50 קומות', 'id=\"nlpg\"'], ['2 מגדלים של 54 קומות', 'דירות נמכרו בפרויקט, לפי דוחות היזם', 'מכירה מוקדמת לבעלי עניין', '<span>לפי היזם</span>', 'Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/projects/duo-tel-aviv-en/?t743d=1', ['Africa Israel Residences is welcome to send us official materials', 'Each of the two towers rises 50 floors'], ['510-apartment', 'Fatal error'], []),\n"
        "    ('/projects/duo-tel-aviv-fr/?t743d=1', ['nous mettrons la page à jour'], ['Fatal error'], []),\n"
        "    ('/projects/rainbow-tel-aviv/?t743d=1', ['id=\"nlps\"', 'mountRainbowStage', 'id=\"nlpg\"'], %s, []),\n") % (BAD,)
kl_release.build_release(PREV, NEW, [], [], {"inc/project-stage.php": H}, {"inc/project-stage.php": LIVE_MD5}, ROWS,
                         "the DUO page: facts as the developer, architects and contractor publish them, no sales or related-party detail, sources and an invitation to the developer",
                         "DUO fact audit: project-stage DUO data")

# the inherited rows that asserted what this release removes on purpose (tokens trimmed, the rows keep their other checks)
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy%d.py" % NEW)
_t = open(_d, encoding="utf-8").read()
n0 = 0
for tok in ("'דירות שנמכרו במגדלי דואו תל אביב, לפי קומה', ", "'לפי דיווח החברה: מכירה מוקדמת לבעלי עניין', ", "'372 מתוך 510', ", "'data-nlps-floor=\"17\"', "):
    c = _t.count(tok)
    n0 += c
    _t = _t.replace(tok, "")
_t = _t.replace(", 'דירות שנמכרו במגדלי דואו תל אביב, לפי קומה']", "]")
open(_d, "w", encoding="utf-8", newline=chr(10)).write(_t)
print("trimmed inherited DUO tokens:", n0, "| left:", _t.count("דירות שנמכרו במגדלי דואו"), _t.count("372 מתוך 510"))

# 1.72.743 second run: the inherited rows on /tour/sde-dov/ assert the OLD tour; HAD-801 swapped that folder live at 16:57 UTC
# today without a plugin release (claude-codex.md), so those rows check another session's retired files. They are dropped here,
# not rewritten (the new tour is HAD-801's to check).
_t = open(_d, encoding="utf-8").read()
_lines = _t.split("\n")
_keep = [l for l in _lines if not (l.strip().startswith("('/tour/sde-dov/") or l.strip().startswith('("/tour/sde-dov/'))]
print("dropped inherited /tour/sde-dov/ rows:", len(_lines) - len(_keep))
open(_d, "w", encoding="utf-8", newline=chr(10)).write("\n".join(_keep))
