# -*- coding: utf-8 -*-
"""The copy gate for Kikar Hamedina (the language-dna skill's blacklist, .claude/skills/language-dna/SKILL.md, plus the site's
own blacklist in tools/source_audit.py): every visible word the P7 release adds.

Scanned: the two post contents (docs/research/2026-09-30-kikar-hamedina/post-he.html, post-en.html), the page top the world
branch prints (the 'hamedina' config and the world words in inc/project-stage.php, rendered by ps_render_harness.php in
Hebrew and English), and the world module's own strings (assets/project-stage/world/world.js, I18N).
Also: no long dash, no ASCII double quote in Hebrew text (gershayim ״ instead), no spaced hyphen (WordPress turns it into a
dash), and none of the internal words. Exit 1 on any hit.

  python scripts/project-stage/kikar_copy_gate.py
"""
import io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RES = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina")

HE = ["ממשק", "דמו ", "הדגמה", "מודל", "מנגנון", "נקודות חמות", "נקודה חמה", "שכבה", "שכבת", "שכבות", "אריח", "הבניין הוא המפה",
      "מפה חיה", "מפה לחיצה", "אינטראקטיב", "ריחוף", "כל קומה מגיבה", "רספונסיבי", "מובייל", "סקיצה", "סכמטי", "פיילוט",
      "פרוטוטייפ", "המערכת", "הפלטפורמה", "החוויה הדיגיטלית", "טכנולוגי", "סימולציה", "3D", "תלת ממד", "תלת-ממד", "בקרוב",
      "בבדיקה", "אטלס", "Atlas", "אפס טפסים", "כיוון בבדיקה", "0 חדרים"]
EN = ["interface", "demo", "hotspot", "overlay", "engine", " UI", "UX", "tile", "map layer", "prototype", "MVP", "3D",
      "simulation", "platform", "technology", "coming soon", "Codex", "Lovable", "lorem"]
SITE = ["בהמתנה לחומרי היזם", "יחליף אותו עם קבלתו", "בבדיקה מול היזם", "יוצגו עם קבלת נתונים", "תוכנית תתווסף", "טרם התקבלו",
        "מחכים ליזם", "אין שרטוטים", "· בקרוב"]


def visible(html):
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"&#8217;", "’", html)


def check(label, text, he=True):
    hits = [w for w in (HE if he else []) + EN + SITE if w in text]
    # "platform" and "engine" are fine inside a URL-free English sentence? No: they are product words; kept strict.
    hits += ["long dash"] if ("—" in text or "–" in text) else []
    hits += ["spaced hyphen"] if re.search(r"\s-\s", text) else []
    if he and re.search(r'[֐-׿]"[֐-׿]', text):
        hits.append('ASCII quote inside a Hebrew word (use ״)')
    print(f"[{'OK ' if not hits else 'BAD'}] {label}: {len(text.split())} words" + (f"  hits: {hits}" if hits else ""))
    return not hits


def main():
    ok = True
    for f, he in (("post-he.html", True), ("post-en.html", False)):
        ok &= check(f, visible(io.open(os.path.join(RES, f), encoding="utf-8").read()), he)
    ps = os.path.join(REPO, "plugins", "nadlan-config", "inc", "project-stage.php")
    for slug, he in (("hamedina", True), ("hamedina-en", False)):
        r = subprocess.run(["php", os.path.join(HERE, "ps_render_harness.php"), ps, slug], capture_output=True)
        d = json.loads(r.stdout.decode("utf-8"))
        c = d["composed"] or ""
        top = c[c.find('<div class="nlps-page'):]
        top = top[: top.find("An answer paragraph")] + top[top.find("</p></div>", top.find("An answer paragraph")) + 10:]  # the harness's own lead
        top = top.split('<aside class="nlcp-projctx">')[0]
        ok &= check("page top " + slug, visible(top.replace("TITLE OF " + slug, "")), he)
    js = io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "world", "world.js"), encoding="utf-8").read()
    i18n = js[js.index("const I18N = {"): js.index("const DEFAULTS = {")]
    he_part, en_part = i18n[: i18n.index("\n  en: {")], i18n[i18n.index("\n  en: {"):]
    strings = lambda s: " ".join(re.findall(r"'([^'\\]*(?:\\.[^'\\]*)*)'|`([^`]*)`", s) and [a or b for a, b in re.findall(r"'([^'\\]*(?:\\.[^'\\]*)*)'|`([^`]*)`", s)])
    ok &= check("world.js he strings", strings(he_part), True)
    ok &= check("world.js en strings", strings(en_part), False)
    print("RESULT", "OK" if ok else "BLOCKED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
