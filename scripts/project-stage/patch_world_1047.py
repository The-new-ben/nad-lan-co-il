# -*- coding: utf-8 -*-
"""v104.7 (1.10.2026, loop turn 15, HAD-375): the long world card, organized (Codex's QA: 1,065-1,402 px on a phone).
Progressive disclosure: the tower's own facts and its two actions first; the seven facts about all three towers (each with its source)
in a fold "על שלושת המגדלים", closed in the phone's dock and open on wide screens; the ring-building card's ring facts the same way.
Nothing is deleted: one tap opens them.
  python patch_world_1047.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
s = open(JS, encoding="utf-8").read()
if "v104.7" in s:
    raise SystemExit("already patched")


def sub(old, new, name):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{name}] anchor found {n} times")
    s = s.replace(old, new)


WORDS = {"    towersAll: 'מגדלי כיכר המדינה',": ("על שלושת המגדלים", "על טבעת הבניינים"),
         "    towersAll: 'Kikar Hamedina Towers',": ("About the three towers", "About the ring of buildings"),
         "    towersAll: 'Tours Kikar Hamedina',": ("À propos des trois tours", "À propos de l’anneau d’immeubles"),
         "    towersAll: 'Башни Кикар ха-Медина',": ("О трёх башнях", "О кольце зданий"),
         "    towersAll: 'أبراج كيكار همدينا',": ("عن الأبراج الثلاثة", "عن حلقة المباني")}
for tail, (a, b) in WORDS.items():
    sub(tail, tail + f" aboutAll: '{a}', aboutRing: '{b}',", "words " + a)

sub("""  const factList = (lines) => `<ul class="nlw-facts">${(lines || []).map((l) => `<li>${esc(tx(l))}${srcHtml(l.src)}</li>`).join('')}</ul>`;
""", """  const factList = (lines) => `<ul class="nlw-facts">${(lines || []).map((l) => `<li>${esc(tx(l))}${srcHtml(l.src)}</li>`).join('')}</ul>`;
  // v104.7 (loop turn 15, Codex's QA: the card ran 1,065-1,402 px on a phone): the facts that are not about the thing tapped sit in a
  // fold, closed in the phone's dock and open on wide screens. Nothing is deleted; one tap opens them.
  const factFold = (label, lines) => `<details class="nlw-notes nlw-more"${docked ? '' : ' open'}><summary>${esc(label)}</summary>${factList(lines)}</details>`;
""", "factFold")
sub("""      `<div class="nlw-sec">${factList(W.facts.towers)}</div>` + notesHtml();""",
    """      factFold(T.aboutAll, W.facts.towers) + notesHtml();""", "tower card")
sub("""    if (b.flags & 4) html += `<div class="nlw-sec">${factList(W.facts.ring)}</div>`;""",
    """    if (b.flags & 4) html += factFold(T.aboutRing, W.facts.ring);""", "ring card")
open(JS, "w", encoding="utf-8", newline="\n").write(s)
print("world.js patched (v104.7)")
