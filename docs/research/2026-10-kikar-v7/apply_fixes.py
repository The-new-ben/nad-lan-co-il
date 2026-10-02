# -*- coding: utf-8 -*-
"""V7: apply the reviewer's fact-check corrections (fixes.json) to article-<lang>.html, each exactly once, and list them in
fact-check-<lang>.md. Only factual corrections go here (a wrong or missing date, a number outside the claims); the wording stays
ChatGPT's (project law 8).

    python docs/research/2026-10-kikar-v7/apply_fixes.py he
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    lang = sys.argv[1]
    path = os.path.join(HERE, "article-%s.html" % lang)
    h = io.open(path, encoding="utf-8").read()
    fixes = [f for f in json.load(io.open(os.path.join(HERE, "fixes.json"), encoding="utf-8")) if f["lang"] == lang]
    done = []
    for f in fixes:
        n = h.count(f["old"])
        if n != 1:
            raise SystemExit("fix not applied (found %d times): %r" % (n, f["old"][:80]))
        h = h.replace(f["old"], f["new"])
        done.append(f)
    io.open(path, "w", encoding="utf-8", newline="\n").write(h)
    fc = os.path.join(HERE, "fact-check-%s.md" % lang)
    if os.path.exists(fc):
        t = io.open(fc, encoding="utf-8").read()
        lines = ["", "### Corrections applied to ChatGPT's text (apply_fixes.py)", ""]
        for f in done:
            lines.append("- **%s**: \"%s\" -> \"%s\". %s" % (f["claim"], f["old"], f["new"], f["why"]))
        if not done:
            lines.append("- none")
        t = t.replace("(filled after reading)\n", "(filled after reading)\n" + "\n".join(lines) + "\n", 1)
        io.open(fc, "w", encoding="utf-8").write(t)
    print(lang, "fixes applied:", len(done))


if __name__ == "__main__":
    main()
