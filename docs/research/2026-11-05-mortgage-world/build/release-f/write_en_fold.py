# -*- coding: utf-8 -*-
"""MortgageWorld F, English page 8780 (HAD-675): the phone folding of the Hebrew page, in English, nothing removed, no code release.
On phones (below 900 px) a chapter taller than 560 px shows its heading and first paragraph and opens with "Read the full section";
the FAQ becomes a compact list whose answers open on a tap. Not folded: the market block, the four rules, the FAQ section itself,
and the sources. Desktop is untouched. The block goes right before <section id="faq">.
  python write_en_fold.py --dry | python write_en_fold.py"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 8780
ANCHOR = '<section id="faq">'
FOLD = ('<style id="nlmx-fold-css">@media (max-width:899px){.nlmx-more{display:flex;align-items:center;justify-content:center;width:100%;min-height:44px;margin:6px 0 14px;'
        'border:1px solid #D3DCE2!important;border-radius:999px!important;background:#fff!important;color:#2F6F86!important;font:600 15px/1.2 "IBM Plex Sans",system-ui,sans-serif!important;cursor:pointer}'
        '.nlmx-folded>*:not(h2):not(.nlmx-keep):not(.nlmx-more){display:none!important}'
        '#faq h3.nlmx-q{cursor:pointer;position:relative;padding-inline-start:26px!important;min-height:44px;display:flex;align-items:center;'
        'font-size:18px!important;line-height:1.45!important;margin:0!important;padding-block:10px!important;border-bottom:1px solid #D3DCE2}'
        '#faq h3.nlmx-q::before{content:"+";position:absolute;inset-inline-start:0;font:600 20px/1 "IBM Plex Mono",monospace;color:#2F6F86}'
        '#faq h3.nlmx-q[aria-expanded="true"]::before{content:"−"}#faq .nlmx-a{margin:10px 0 14px!important}#faq .nlmx-a[hidden]{display:none!important}}'
        '.entry-content .nli button,.entry-content .nli select,.entry-content .nlmm a{min-height:44px}</style>\n'
        '<script id="nlmx-fold-js">(function(){if(!window.matchMedia||!window.matchMedia("(max-width: 899px)").matches)return;'
        'function go(){var skip={"mortgage-market":1,"rules-facts":1,"faq":1,"sources":1};'
        '[].forEach.call(document.querySelectorAll(".nlen section"),function(s){if(skip[s.id]||s.closest(".nli,#faq,#mortgage-market"))return;'
        'var h=s.querySelector(":scope>h2");if(!h||s.offsetHeight<560)return;var p=h.nextElementSibling;if(!(p&&p.tagName==="P"))p=null;'
        'if(s.offsetHeight-h.offsetHeight-(p?p.offsetHeight:0)<200)return;if(p)p.classList.add("nlmx-keep");s.classList.add("nlmx-folded");'
        'var b=document.createElement("button");b.type="button";b.className="nlmx-more";b.setAttribute("aria-expanded","false");b.textContent="Read the full section";'
        'b.addEventListener("click",function(){s.classList.remove("nlmx-folded");b.remove();});(p||h).after(b);});'
        'var f=document.getElementById("faq");if(f){[].forEach.call(f.querySelectorAll("h3"),function(q){var a=[],n=q.nextElementSibling;while(n&&n.tagName==="P"){a.push(n);n=n.nextElementSibling;}'
        'if(!a.length)return;q.classList.add("nlmx-q");q.setAttribute("role","button");q.setAttribute("tabindex","0");q.setAttribute("aria-expanded","false");a.forEach(function(x){x.classList.add("nlmx-a");x.hidden=true;});'
        'function t(){var o=q.getAttribute("aria-expanded")!=="true";q.setAttribute("aria-expanded",String(o));a.forEach(function(x){x.hidden=!o;});}'
        'q.addEventListener("click",t);q.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();t();}});});}}'
        'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",go);else go();})();</script>\n')

if DRY and "--local" in sys.argv:
    io.open(os.path.join(H, "fold-en.html"), "w", encoding="utf-8", newline="").write(FOLD); print("[local] fold-en.html written"); sys.exit(0)
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_fen"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert 'id="nlmx-fold-js"' not in raw, "already written"
assert raw.count(ANCHOR) == 1, raw.count(ANCHOR)
new = raw.replace(ANCHOR, FOLD + ANCHOR)
for line in raw.split("\n"):
    if line.strip():
        assert line in new, ("an original line is missing", line[:90])
assert not re.search(r"[–—]", re.sub(r"<[^>]+>", " ", FOLD).replace('content:"−"', ""))
print("[page %d] fold block %d bytes; content %d -> %d bytes" % (PID, len(FOLD), len(raw), len(new)))
io.open(os.path.join(H, "fold-en.html"), "w", encoding="utf-8", newline="").write(FOLD)
if DRY:
    print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"fold": 'id="nlmx-fold-js"' in page and "Read the full section" in page, "15 questions": page.count('"@type":"Question"') == 15,
      "one h1": page[page.find("<body"):].count("<h1") == 1, "crumbs": 'aria-label="Breadcrumb"' in page, "market": 'id="mortgage-market"' in page}
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
