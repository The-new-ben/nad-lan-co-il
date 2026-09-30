# -*- coding: utf-8 -*-
"""The copy gate for Kikar Hamedina (the language-dna skill's blacklist, .claude/skills/language-dna/SKILL.md, plus the site's
own blacklist in tools/source_audit.py): every visible word the P7 (he, en) and P8 (fr, ru, ar) releases add.

Scanned: the five post contents (docs/research/2026-09-30-kikar-hamedina/post-<lang>.html), the page top the world branch prints
(the 'hamedina' config and the world words in inc/project-stage.php, rendered by ps_render_harness.php in each language), the
world module's own strings (assets/project-stage/world/world.js, I18N, one block per language) and the world data's fr / ru / ar
texts (assets/project-stage/hamedina/world-i18n.json).
Also: no long dash, no spaced hyphen (WordPress turns it into a dash), no ASCII double quote in Hebrew text (gershayim ״), no
straight apostrophe in French text (’), and none of the internal words. Exit 1 on any hit.

  python scripts/project-stage/kikar_copy_gate.py
"""
import io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RES = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina")
PLUG = os.path.join(REPO, "plugins", "nadlan-config")

HE = ["ממשק", "דמו ", "הדגמה", "מודל", "מנגנון", "נקודות חמות", "נקודה חמה", "שכבה", "שכבת", "שכבות", "אריח", "הבניין הוא המפה",
      "מפה חיה", "מפה לחיצה", "אינטראקטיב", "ריחוף", "כל קומה מגיבה", "רספונסיבי", "מובייל", "סקיצה", "סכמטי", "פיילוט",
      "פרוטוטייפ", "המערכת", "הפלטפורמה", "החוויה הדיגיטלית", "טכנולוגי", "סימולציה", "3D", "תלת ממד", "תלת-ממד", "בקרוב",
      "בבדיקה", "אטלס", "Atlas", "אפס טפסים", "כיוון בבדיקה", "0 חדרים"]
EN = ["interface", "demo", "hotspot", "overlay", "engine", " UI", "UX", "tile", "map layer", "prototype", "MVP", "3D",
      "simulation", "platform", "technology", "coming soon", "Codex", "Lovable", "lorem"]
# the other languages: their own tech and waiting words (the language-dna rule, said in that language), and the few English
# words that would show as English (a substring list like "tile" would hit French "utile", so only whole marks here)
FR = ["interface", "démo", "démonstration", "hotspot", "point chaud", "plateforme", "technolog", "simulation", "prototype", "bientôt",
      "interactif", "interactive", "maquette numérique", "en attente", "calque", "moteur 3D", "Atlas"]
RU = ["интерфейс", "демо", "демонстрац", "хотспот", "платформ", "технолог", "симуляц", "прототип", r"\bскоро\b", "интерактив",
      "в ожидании", "движок", "слой", "Атлас"]
AR = ["واجهة المستخدم", "تجريبي", "منصة", "منصّة", "تكنولوج", "تقني", "محاكاة", "نموذج أولي", "قريباً", "قريبا", "تفاعلي", "أطلس"]
EN_ANY = ["3D", "Codex", "Lovable", "lorem", "hotspot", "MVP", "coming soon"]
SITE = ["בהמתנה לחומרי היזם", "יחליף אותו עם קבלתו", "בבדיקה מול היזם", "יוצגו עם קבלת נתונים", "תוכנית תתווסף", "טרם התקבלו",
        "מחכים ליזם", "אין שרטוטים", "· בקרוב"]
LISTS = {"he": HE + EN, "en": EN, "fr": FR + EN_ANY, "ru": RU + EN_ANY, "ar": AR + EN_ANY}


def visible(html):
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"&#8217;", "’", html)


def check(label, text, lang):
    low = text.lower() if lang in ("fr", "ru") else text
    # an entry starting with \b is a whole word ("скоро" alone, not "скоростных")
    hits = [w for w in LISTS[lang] + SITE if (re.search(w, low) if w.startswith("\b") else (w.lower() if lang in ("fr", "ru") else w) in low)]
    hits += ["long dash"] if ("—" in text or "–" in text) else []
    hits += ["spaced hyphen"] if re.search(r"\s-\s", text) else []
    if lang == "he" and re.search(r'[֐-׿]"[֐-׿]', text):
        hits.append('ASCII quote inside a Hebrew word (use ״)')
    if lang == "fr" and re.search(r"[A-Za-zÀ-ÿ]'[A-Za-zÀ-ÿ]", text):
        hits.append("straight apostrophe in French (use ’)")
    print(f"[{'OK ' if not hits else 'BAD'}] {label}: {len(text.split())} words" + (f"  hits: {hits}" if hits else ""))
    return not hits


def js_strings(block):
    return " ".join(a or b for a, b in re.findall(r"'([^'\\]*(?:\\.[^'\\]*)*)'|`([^`]*)`", block))


def main():
    ok = True
    for lang in ("he", "en", "fr", "ru", "ar"):
        f = os.path.join(RES, f"post-{lang}.html")
        ok &= check(f"post-{lang}.html", visible(io.open(f, encoding="utf-8").read()), lang)
    ps = os.path.join(PLUG, "inc", "project-stage.php")
    for slug, lang in (("hamedina", "he"), ("hamedina-en", "en"), ("hamedina-fr", "fr"), ("hamedina-ru", "ru"), ("hamedina-ar", "ar")):
        r = subprocess.run(["php", os.path.join(HERE, "ps_render_harness.php"), ps, slug], capture_output=True)
        d = json.loads(r.stdout.decode("utf-8"))
        c = d["composed"] or ""
        top = c[c.find('<div class="nlps-page'):]
        top = top[: top.find("An answer paragraph")] + top[top.find("</p></div>", top.find("An answer paragraph")) + 10:]  # the harness's own lead
        top = top.split('<aside class="nlcp-projctx">')[0]
        ok &= check("page top " + slug, visible(top.replace("TITLE OF " + slug, "")), lang)
    js = io.open(os.path.join(PLUG, "assets", "project-stage", "world", "world.js"), encoding="utf-8").read()
    i18n = js[js.index("const I18N = {"): js.index("const DEFAULTS = {")]
    starts = [(m.group(1), m.start()) for m in re.finditer(r"\n  (he|en|fr|ru|ar): \{", i18n)]
    for i, (lang, s) in enumerate(starts):
        e = starts[i + 1][1] if i + 1 < len(starts) else len(i18n)
        block = i18n[s:e]
        # the Hebrew keys of the 'opens' maps are lookups, not words the page shows
        block = re.sub(r"'[֐-׿][^']*': ", "", block) if lang != "he" else block
        ok &= check(f"world.js {lang} strings", js_strings(block), lang)
    wi = json.load(io.open(os.path.join(PLUG, "assets", "project-stage", "hamedina", "world-i18n.json"), encoding="utf-8"))
    for lang in ("fr", "ru", "ar"):
        ok &= check(f"world-i18n.json {lang}", " ".join(wi[lang].values()), lang)
    print("RESULT", "OK" if ok else "BLOCKED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
