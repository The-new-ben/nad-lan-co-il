# -*- coding: utf-8 -*-
"""Turns a project article (the small Markdown subset the ChatGPT briefs produce: ##/### headings, paragraphs,
pipe tables, numbered lists with **bold** labels and [text](url) links) into safe HTML for the project page.
Only links to cy-prus.co.il are kept as links; any other link becomes plain text."""
import re
from html import escape

LINK = re.compile(r'\[([^\]]+)\]\((https?://[^)\s]+)\)')


def inline(text):
    out, pos = [], 0
    for m in LINK.finditer(text):
        out.append(escape(text[pos:m.start()]))
        label, url = m.group(1), m.group(2)
        if url.startswith('https://cy-prus.co.il/'):
            out.append(f'<a href="{escape(url)}">{escape(label)}</a>')
        else:
            out.append(escape(label))
        pos = m.end()
    out.append(escape(text[pos:]))
    html = ''.join(out)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)


def to_html(md):
    md = re.sub(r'<!--.*?-->', '', md, flags=re.S)
    blocks, para, rows, items = [], [], [], []

    def flush():
        nonlocal para, rows, items
        if para:
            blocks.append('<p>' + inline(' '.join(para)) + '</p>')
            para = []
        if rows:
            cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows if not re.match(r'^\|\s*-', r)]
            head, body = cells[0], cells[1:]
            wide = ' cyx-table--wide' if len(head) > 3 else ''
            blocks.append(f'<div class="cyx-table{wide}"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>'
                          + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body) + '</tbody></table></div>')
            rows = []
        if items:
            blocks.append('<ol>' + ''.join(f'<li>{inline(i)}</li>' for i in items) + '</ol>')
            items = []

    for line in md.splitlines():
        s = line.strip()
        if not s:
            flush()
            continue
        if s.startswith('|'):
            if para or items:
                flush()
            rows.append(s)
            continue
        if rows:
            flush()
        m = re.match(r'^(#{2,4})\s+(.*)$', s)
        if m:
            flush()
            level = len(m.group(1))
            blocks.append(f'<h{level}>{inline(m.group(2))}</h{level}>')
            continue
        m = re.match(r'^\d+\.\s+(.*)$', s)
        if m:
            if para:
                flush()
            items.append(m.group(1))
            continue
        if items:
            flush()
        para.append(s)
    flush()
    return '\n'.join(blocks)
