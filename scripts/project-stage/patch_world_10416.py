# -*- coding: utf-8 -*-
"""v104.16 (1.10.2026, loop turn 25, HAD-375): on the en/fr/ru/ar pages "what's nearby" counts every place, as the Hebrew page.
Live 1.72.386 left out every place whose name exists only in Hebrew (education 10 of 94, community 5 of 49, health 6 of 35, parks
23 of 77...), while the area map on the same page counted them all, named by their kind. Now one rule for the whole page, the
area map's: the name in the page's language, else the English name, else a name with no Hebrew letters, else the kind in the
page's language (T.kinds, else the category). Nothing is translated or transliterated. The card of a place named by its kind
shows its Hebrew name (right-to-left, so a buyer can match it to the street sign). The places' de-duplication keys on the Hebrew
name, so two different kindergartens are never merged because both read "Kindergarten".
  python patch_world_10416.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js")
s = open(JS, encoding="utf-8").read()
if "v104.16" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


sub("""  const placeName = (p) => (lang === 'he' ? p.name : (p.names && (p.names[lang] || p.names.en)) || p.name);""",
    """  // v104.16 (loop turn 25): the area map's rule, so one page never disagrees with itself: the name in the page's language, else the
  // English name, else a name with no Hebrew letters, else the kind in the page's language (never translated, never left out).
  // A "name in another language" that is itself in Hebrew (bad source data: "צמרת G" as names.en) counts as no name.
  const otherName = (p) => { const n = p.names || {}; const v = n[lang] || n.en; return v && !heOnly(v) ? v : (n.en && !heOnly(n.en) ? n.en : ''); };
  const kindName = (p) => lang !== 'he' && !otherName(p) && heOnly(p.name);
  const placeName = (p) => (lang === 'he' ? p.name : otherName(p) || (kindName(p) ? (T.kinds[p.k] || T.cats[p.g] || p.name) : p.name));""",
    "placeName")
sub("""        const nm = placeName(p);
        if (seen.some((q) => q.nm === nm && Math.hypot(q.x - p.x, q.z - p.z) < 160)) continue;
        seen.push({ nm, x: p.x, z: p.z });""",
    """        const nm = placeName(p);
        // v104.16: the same place twice (a stop on both sides of a street) is told by its own name, not by a kind word
        if (seen.some((q) => q.he === p.name && Math.hypot(q.x - p.x, q.z - p.z) < 160)) continue;
        seen.push({ he: p.name, x: p.x, z: p.z });""",
    "dedupe")
sub("""    let html = eyebrow(`${T.cats[p.g] || ''}${kind && kind !== T.cats[p.g] ? ' · ' + kind : ''}`) + title(placeName(p)) + `<div class="nlw-kv">${kv.join('')}</div>`;
    const lines = [];""",
    """    const byKind = kindName(p); // v104.16: named by its kind here; its own name, in Hebrew, is the first line
    let html = eyebrow(`${T.cats[p.g] || ''}${kind && kind !== T.cats[p.g] && !byKind ? ' · ' + kind : ''}`) + title(placeName(p)) + `<div class="nlw-kv">${kv.join('')}</div>`;
    const lines = [];
    if (byKind && T.heName) lines.push(`${esc(T.heName)}: <bdi lang="he" dir="rtl">${esc(p.name)}</bdi>`);""",
    "card")
for a, b, nm in (("    walkMin: (m) => `${m} min walk`,", "    walkMin: (m) => `${m} min walk`,\n    heName: 'Name in Hebrew', // v104.16", "en"),
                 ("    walkMin: (m) => `${m} min à pied`,", "    walkMin: (m) => `${m} min à pied`,\n    heName: 'Nom en hébreu', // v104.16", "fr"),
                 ("    walkMin: (m) => `${m} мин пешком`,", "    walkMin: (m) => `${m} мин пешком`,\n    heName: 'Название на иврите', // v104.16", "ru"),
                 ("    walkMin: (m) => `${arN(m, 'دقيقة واحدة', 'دقيقتان', 'دقائق', 'دقيقة')} سيراً`,", "    walkMin: (m) => `${arN(m, 'دقيقة واحدة', 'دقيقتان', 'دقائق', 'دقيقة')} سيراً`,\n    heName: 'الاسم بالعبرية', // v104.16", "ar")):
    sub(a, b, "words " + nm)
open(JS, "w", encoding="utf-8", newline="\n").write(s)
print("world.js patched (v104.16)")
