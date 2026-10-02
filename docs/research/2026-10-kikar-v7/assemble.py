# -*- coding: utf-8 -*-
"""V7: join the three ChatGPT parts of one language into article-<lang>.html.

    python docs/research/2026-10-kikar-v7/assemble.py he

Reads raw/<lang>-p1.html, -p2.html, -p3.html (each is the content of one ```html block, copied from the ChatGPT conversation with
its own copy button, saved from the clipboard byte for byte). Strips a stray ``` fence if the copy carried one, puts one block
element per line, and writes article-<lang>.html. The words are ChatGPT's; nothing is rewritten here."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def clean(t):
    t = t.replace("\r\n", "\n").strip()
    t = re.sub(r"^```[a-z]*\n", "", t)
    t = re.sub(r"\n```$", "", t)
    # ChatGPT's citation markers to the attached brief (not article text): removed, the sentence kept
    t = re.sub(r"\s*<small>\s*:chatgpt-content-reference\{[^}]*\}\s*</small>", "", t)
    t = re.sub(r"\s*:chatgpt-content-reference\{[^}]*\}", "", t)
    t = re.sub(r"\s*【[^】]*】", "", t)
    return t.strip()


def main():
    lang = sys.argv[1]
    parts = []
    for k in (1, 2, 3):
        p = os.path.join(HERE, "raw", "%s-p%d.html" % (lang, k))
        parts.append(clean(io.open(p, encoding="utf-8-sig").read()))
    h = "\n".join(parts)
    # one block element per line (the post file's habit); inline content untouched
    h = re.sub(r">\s*\n\s*<", ">\n<", h)
    h = re.sub(r"(</(?:p|h2|h3|li|tr|table|ul|ol|section|thead|tbody)>)(?=<)", r"\1\n", h)
    h = re.sub(r"\n{2,}", "\n", h).strip() + "\n"
    out = os.path.join(HERE, "article-%s.html" % lang)
    io.open(out, "w", encoding="utf-8", newline="\n").write(h)
    print("wrote", out, len(h), "chars")


if __name__ == "__main__":
    main()
