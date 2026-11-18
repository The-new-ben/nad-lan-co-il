# -*- coding: utf-8 -*-
"""make deploy698.py from deploy697.py: 1.72.698 = HAD-783 (owner 18.11.2026): a forum member opens an OWN professional card
for free, and the video call is obvious and one tap away. Follows Claude Design board 18
(docs/design-lab/pro-forum/boards/board-18-member-opens-own-card-video.png).
  NEW  inc/pro-forum-card.php, assets/proforum/card.js, assets/proforum/card.css: the invitation to a member who marked
       "בעל מקצוע" and has no card, the form (name, trade with its form, city, what I do, phone optional, how to reach me, a
       checked video checkbox), the card it creates (nadlan_professional, source forum_member; live at once for a member with
       an approved post and clean text, else pending with signed approve / reject links to the owner; lawyers always pending),
       and the card page's top for such a card ("חבר בפורום מאז...", never a register tick; a large video button).
  SWAP inc/pro-forum.php (one require line), inc/pro-forum-render.php (five HOOK filters), inc/pro-forum-call.php and
       assets/proforum/call.js (a member may call any member who switched video on, from his card or from a discussion he wrote
       in; a room can carry a card; 3 calls a day to the same person; the pill next to every answer whose author allowed video).
  A new file goes in BOTH lists (the 676 lesson). Built by an Opus agent from a brief, reviewed by the release session.
  133 + 123 + 85 + 91 local tests pass."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-697.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
PRO = "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
A = "/wp-content/plugins/nadlan-config/assets/proforum/"
ROWS = ("    ('/forum/6/?t698f=1', ['nlf-thread', 'assets/proforum/card.js', 'assets/proforum/card.css', 'assets/proforum/social.js'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/forum/?t698f=1', ['nlf-dir', 'nlf-card', 'assets/proforum/card.js'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('%s?t698f=1', ['nlf nlf-win nlf-emb', 'nlf-emb-ask', 'nlpp-req'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'nlfm-member-card'], []),\n"
        "    ('/wp-json/nadlan/v1/forum/ping?t698f=1', ['\"loaded\":true', '\"public\":true'], [], []),\n"
        "    ('%scard.js?t698f=1', ['card/save'], ['Fatal error'], []),\n"
        "    ('%scard.css?t698f=1', ['nlfm'], ['Fatal error'], []),\n"
        "    ('%scall.js?t698f=1', ['data-nlf-callcard', 'createBoard'], ['Fatal error'], []),\n") % (PRO, A, A, A)
NEW = ["inc/pro-forum-card.php", "assets/proforum/card.js", "assets/proforum/card.css"]
kl_release.build_release(697, 698, ["inc/pro-forum.php", "inc/pro-forum-render.php", "inc/pro-forum-call.php", "assets/proforum/call.js"] + NEW,
                         NEW, {}, {}, ROWS,
                         "a forum member opens an own professional card for free; the video call is one tap from a card or an answer",
                         "HAD-783 forum round: own card for members, visible video call (design board 18)")

# 18.11.2026, after the first run rolled back: five INHERITED rows still asserted Meital Katsir's listings, licence and
# placement. The owner retired her on 18.11 (her 45 pages were set to draft after 1.72.697 was released), so those rows
# describe a state that no longer exists and fail every release from now on. Only the stale tokens go; the rest of each
# row stays. Rows whose whole subject was her listing are dropped.
import ast
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy698.py")
src = open(D, encoding="utf-8").read()
head, rest = src.split("CHECKS = [\n", 1)
body, tail = rest.split("\n]\n", 1)
STALE_MUST = {"/properties/": {"רישיון 3131540", 'class="nlpl-pager"'}, "/brokers/": {'class="nlds-licence__vf"', 'class="nlds-bfeat"'}}
STALE_NEVER = {"/properties/": {"מודעה לדוגמה"}}
DROP = {"/properties/?city=%D7%A0%D7%95%D7%A4%D7%99%20%D7%99%D7%9D", "/property-value/?pl307=1", "/properties/page/2/"}
keep, changed, dropped = [], 0, 0
for ln in body.split("\n"):
    st = ln.strip()
    if st.startswith("(") and st.endswith("),"):
        try:
            row = list(ast.literal_eval(st[:-1]))
        except Exception:
            keep.append(ln); continue
        path = row[0]
        if path in DROP and ("מיטל קציר" in st or "נופי ים, תל אביב-יפו" in st or "nlpl-card--demo" in st):
            dropped += 1; continue
        if path in STALE_MUST and any(t in row[1] for t in STALE_MUST[path]):
            row[1] = [t for t in row[1] if t not in STALE_MUST[path]]
            if len(row) > 2 and path in STALE_NEVER: row[2] = [t for t in row[2] if t not in STALE_NEVER[path]]
            keep.append("    " + repr(tuple(row)) + ","); changed += 1; continue
    keep.append(ln)
assert (changed, dropped) == (2, 3), (changed, dropped)
open(D, "w", encoding="utf-8", newline="\n").write(head + "CHECKS = [\n" + "\n".join(keep) + "\n]\n" + tail)
print("rows about the retired broker: %d trimmed, %d dropped; deploy698.py rewritten" % (changed, dropped))
