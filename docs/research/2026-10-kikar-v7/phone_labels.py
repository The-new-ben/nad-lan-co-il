# -*- coding: utf-8 -*-
"""V7: on phones the page hides a table's <thead> and shows each row as a card (inc/project-stage.php, ProjectDossier v67), so a
comparison cell such as "0%" or "8%" loses its column. For the tables where that changes the meaning (both tables of nlws-costs and
the deals table, the first table of nlws-prices), every value cell after the first gets its column's name as <small>, which the
page already styles as a small grey line under the value (the old source line's style). Presentation only: no word of the text
changes, the label is the table's own header text.

    python docs/research/2026-10-kikar-v7/phone_labels.py he   (idempotent: a labelled table is left as is)
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def label_table(t):
    head = re.search(r"<thead>(.*?)</thead>", t, re.S)
    if not head or "<small>" in t:
        return t
    cols = re.findall(r"<th>(.*?)</th>", head.group(1), re.S)

    def row(m):
        cells = re.findall(r"<(t[dh])>(.*?)</\1>", m.group(1), re.S)
        out = []
        for k, (tag, val) in enumerate(cells):
            if k > 0 and tag == "td" and k < len(cols):
                val = val + "<small>" + re.sub(r"<[^>]+>", "", cols[k]) + "</small>"
            out.append("<%s>%s</%s>" % (tag, val, tag))
        return "<tr>" + "".join(out) + "</tr>"

    body = re.search(r"<tbody>(.*?)</tbody>", t, re.S)
    nb = re.sub(r"<tr>(.*?)</tr>", row, body.group(1), flags=re.S)
    return t[:body.start(1)] + nb + t[body.end(1):]


def main():
    lang = sys.argv[1]
    p = os.path.join(HERE, "article-%s.html" % lang)
    h = io.open(p, encoding="utf-8").read()
    n = 0

    def section(sid, which):
        nonlocal h, n
        m = re.search(r'(<section[^>]*id="%s"[^>]*>)(.*?)(</section>)' % sid, h, re.S)
        sec = m.group(2)
        tables = list(re.finditer(r"<table>.*?</table>", sec, re.S))
        for k, tm in reversed(list(enumerate(tables))):
            if which is None or k in which:
                new = label_table(tm.group(0))
                if new != tm.group(0):
                    n += 1
                sec = sec[:tm.start()] + new + sec[tm.end():]
        h = h[:m.start(2)] + sec + h[m.end(2):]

    section("nlws-costs", None)
    section("nlws-prices", {0})
    io.open(p, "w", encoding="utf-8", newline="\n").write(h)
    print(lang, "tables labelled:", n)


if __name__ == "__main__":
    main()
