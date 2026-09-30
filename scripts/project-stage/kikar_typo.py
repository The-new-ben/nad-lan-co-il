# -*- coding: utf-8 -*-
"""Typography of the Kikar Hamedina language posts (P8): each language's own number and punctuation spacing, written into
docs/research/2026-09-30-kikar-hamedina/post-<lang>.html in place (text between tags only; tags, attributes and links untouched).
Idempotent: a second run changes nothing.

  fr: thousands with a narrow no-break space (75 900), a no-break space before : ; ? ! » and after «, and before ₪
  ru: thousands with a no-break space (75 900), a no-break space before ₪
  ar: thousands with a comma (75,900), a no-break space before ₪
In the drafts, "_" between digits marks a thousands separator (9_079 -> 9 079 / 9,079).

  python scripts/project-stage/kikar_typo.py fr ru ar
"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "research", "2026-09-30-kikar-hamedina")
NB, NNB = " ", " "


def fix_text(s, lang):
    thou = {"fr": NNB, "ru": NB, "ar": ","}[lang]
    s = re.sub(r"(?<=\d)_(?=\d{3}(?!\d))", thou, s)
    s = re.sub(r"(\d) ₪", "\\1" + NB + "₪", s)
    if lang == "fr":
        s = re.sub(r" ([:;?!»])", NB + r"\1", s)
        s = re.sub(r"« ", "«" + NB, s)
    return s


def run(lang):
    p = os.path.join(RES, f"post-{lang}.html")
    t = io.open(p, encoding="utf-8").read()
    out = re.sub(r">([^<]+)<", lambda m: ">" + fix_text(m.group(1), lang) + "<", t)
    left = re.findall(r"\d_\d", out)
    if left:
        raise SystemExit(f"{lang}: a thousands mark left: {left[:5]}")
    if out != t:
        io.open(p, "w", encoding="utf-8", newline="\n").write(out)
    print(f"{lang}: {'changed' if out != t else 'unchanged'}")


if __name__ == "__main__":
    for l in sys.argv[1:] or ["fr", "ru", "ar"]:
        if os.path.exists(os.path.join(RES, f"post-{l}.html")):
            run(l)
