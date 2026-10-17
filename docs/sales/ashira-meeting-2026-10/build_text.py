# -*- coding: utf-8 -*-
"""HAD-543: the meeting playbook and the business ground as A4 documents (Hebrew), same identity as the deck.
python build_text.py  ->  playbook.html/.pdf (scripts.md) and business.html/.pdf (business.md)"""
import html
import os
import re

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = """:root{--chart:#EEF3F2;--grid:#C5D4D1;--ink:#0E1B24;--ink2:#3B4C57;--blue:#0B5C8E;--mag:#B3126F}
*{box-sizing:border-box}body{font-family:"IBM Plex Sans Hebrew",Arial,sans-serif;color:var(--ink);direction:rtl;margin:0;background:#fff;
font-size:15.5px;line-height:1.65;-webkit-print-color-adjust:exact;print-color-adjust:exact}
main{max-width:820px;margin:0 auto;padding:40px 24px}
h1{font-size:34px;line-height:1.15;margin:0 0 6px;border-bottom:6px solid var(--ink);padding-bottom:14px}
h2{font-size:24px;margin:34px 0 10px;color:var(--ink);border-right:8px solid var(--mag);padding-right:12px;break-after:avoid}
h3{font-size:18px;margin:22px 0 6px;color:var(--blue);break-after:avoid}
p{margin:8px 0}ul,ol{margin:6px 0;padding-right:22px}li{margin:4px 0}
strong{font-weight:700}blockquote{margin:14px 0;padding:12px 16px;background:var(--chart);border-right:4px solid var(--blue);font-size:17px}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px;break-inside:avoid}th,td{border:1px solid var(--grid);padding:6px 8px;text-align:right;vertical-align:top}
th{background:var(--ink);color:#fff}pre{background:var(--chart);padding:12px 14px;white-space:pre-wrap;font-family:"IBM Plex Sans Hebrew",sans-serif;border:1px solid var(--grid)}
hr{border:0;border-top:1px solid var(--grid);margin:26px 0}.meta{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink2)}"""


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def md(src):
    out, lines, i = [], src.split("\n"), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(html.escape(lines[j])); j += 1
            out.append("<pre>" + "\n".join(buf) + "</pre>"); i = j + 1; continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            h = "<tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>"
            b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f"<table>{h}{b}</table>"); continue
        m = re.match(r"^(#{1,3}) (.*)", l)
        if m:
            n = len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); i += 1; continue
        if re.match(r"^\s*([-*]|\d+\.) ", l):
            tag = "ol" if re.match(r"^\s*\d+\.", l) else "ul"
            items = []
            while i < len(lines) and (re.match(r"^\s*([-*]|\d+\.) ", lines[i]) or (lines[i].startswith("   ") and lines[i].strip())):
                if re.match(r"^\s*([-*]|\d+\.) ", lines[i]):
                    items.append(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[i]))
                else:
                    items[-1] += "<br>" + lines[i].strip()
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x).replace('&lt;br&gt;', '<br>')}</li>" for x in items) + f"</{tag}>"); continue
        if l.startswith("> "):
            out.append(f"<blockquote>{inline(l[2:])}</blockquote>"); i += 1; continue
        if l.strip() == "---":
            out.append("<hr>"); i += 1; continue
        if l.strip():
            out.append(f"<p>{inline(l)}</p>")
        i += 1
    return "\n".join(out)


def page(title, body):
    return ("<!doctype html><html lang='he' dir='rtl'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)}</title><link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans+Hebrew:wght@400;700&display=swap' rel='stylesheet'>"
            f"<style>{CSS}</style></head><body><main>{body}<p class='meta'>nad-lan.co.il · מיטל קציר, מתווכת מורשית 3131540 · אוקטובר 2026</p></main></body></html>")


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page()
    for src, name, title in (("scripts.md", "playbook", "ספר המכירה · פגישת אשירה"), ("business.md", "business", "הקרקע העסקית · פגישת אשירה")):
        out = os.path.join(HERE, name + ".html")
        open(out, "w", encoding="utf-8").write(page(title, md(open(os.path.join(HERE, src), encoding="utf-8").read())))
        pg.goto("file:///" + out.replace("\\", "/")); pg.wait_for_timeout(1500)
        pdf = os.path.join(HERE, name + ".pdf")
        pg.pdf(path=pdf, format="A4", print_background=True, margin={"top": "14mm", "bottom": "14mm", "left": "12mm", "right": "12mm"})
        print(name, os.path.getsize(pdf))
    pg.set_viewport_size({"width": 900, "height": 1200}); pg.goto("file:///" + os.path.join(HERE, "playbook.html").replace("\\", "/")); pg.wait_for_timeout(1200)
    pg.screenshot(path=os.path.join(HERE, "playbook-shot.png"))
    b.close()
