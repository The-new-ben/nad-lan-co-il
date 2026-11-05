# -*- coding: utf-8 -*-
"""MortgageWorld F, page 121 (HAD-675): a shorter phone page, nothing removed, no code release.
The phone folding script of round D (nlmx-fold-css + nlmx-fold-js in the page content) becomes v2:
  1. A long chapter folds when it is taller than 560 px (was 1,100) and the folded part is worth a button (at least 200 px):
     the heading and the first paragraph stay visible, the rest opens with "להמשך הפרק". Every word stays in the HTML.
     Not folded, as before: the tools, the market block, the four rules, the FAQ; new: the guide's opening block (the photo and the
     links to the child pages stay in view).
  2. The FAQ questions become a compact list on phones (18 px, one rule between questions); the answers still open on a tap.
Desktop (900 px and up) is untouched: the script returns at once.
  python write_page_f.py --dry   (writes preview-content-f.html and fold-f.html for the local check)
  python write_page_f.py         (writes the page, backup first, then live checks)"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
FOLD_RE = re.compile(r'<style id="nlmx-fold-css">.*?</style>\n<script id="nlmx-fold-js">.*?</script>\n', re.S)
FOLD = ('<style id="nlmx-fold-css">@media (max-width:899px){.nlmx-more{display:flex;align-items:center;justify-content:center;width:100%;min-height:44px;margin:6px 0 14px;'
        'border:1px solid #D3DCE2!important;border-radius:999px!important;background:#fff!important;color:#2F6F86!important;font:600 15px/1.2 "IBM Plex Sans Hebrew",system-ui,sans-serif!important;cursor:pointer}'
        '.nlmx-folded>*:not(h2):not(.nlmx-keep):not(.nlmx-more){display:none!important}'
        '#faq h3.nlmx-q{cursor:pointer;position:relative;padding-inline-start:26px!important;min-height:44px;display:flex;align-items:center;'
        'font-size:18px!important;line-height:1.45!important;margin:0!important;padding-block:10px!important;border-bottom:1px solid #D3DCE2}'
        '#faq h3.nlmx-q::before{content:"+";position:absolute;inset-inline-start:0;font:600 20px/1 "IBM Plex Mono",monospace;color:#2F6F86}'
        '#faq h3.nlmx-q[aria-expanded="true"]::before{content:"−"}#faq .nlmx-a{margin:10px 0 14px!important}#faq .nlmx-a[hidden]{display:none!important}}'
        '.entry-content .nli button,.entry-content .nli select,.entry-content .nlmm a{min-height:44px}.nlmx-credit{display:block;font-size:12px;color:#5E6A75}</style>\n'
        '<script id="nlmx-fold-js">(function(){if(!window.matchMedia||!window.matchMedia("(max-width: 899px)").matches)return;'
        'function go(){var skip={"tools":1,"mortgage-market":1,"mortgage-rules-facts":1,"faq":1};'
        '[].forEach.call(document.querySelectorAll(".nadlan-guide section"),function(s){if(skip[s.id]||s.classList.contains("nadlan-hero-shell")||s.closest(".nlmx-sw,.nli,#faq,#mortgage-market"))return;'
        'var h=s.querySelector(":scope>h2");if(!h||s.offsetHeight<560)return;var p=h.nextElementSibling;if(!(p&&p.tagName==="P"))p=null;'
        'if(s.offsetHeight-h.offsetHeight-(p?p.offsetHeight:0)<200)return;if(p)p.classList.add("nlmx-keep");s.classList.add("nlmx-folded");'
        'var b=document.createElement("button");b.type="button";b.className="nlmx-more";b.setAttribute("aria-expanded","false");b.textContent="להמשך הפרק";'
        'b.addEventListener("click",function(){s.classList.remove("nlmx-folded");b.remove();});(p||h).after(b);});'
        'var f=document.getElementById("faq");if(f){[].forEach.call(f.querySelectorAll("h3"),function(q){var a=[],n=q.nextElementSibling;while(n&&n.tagName==="P"){a.push(n);n=n.nextElementSibling;}'
        'if(!a.length)return;q.classList.add("nlmx-q");q.setAttribute("role","button");q.setAttribute("tabindex","0");q.setAttribute("aria-expanded","false");a.forEach(function(x){x.classList.add("nlmx-a");x.hidden=true;});'
        'function t(){var o=q.getAttribute("aria-expanded")!=="true";q.setAttribute("aria-expanded",String(o));a.forEach(function(x){x.hidden=!o;});}'
        'q.addEventListener("click",t);q.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();t();}});});}}'
        'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",go);else go();})();</script>\n')

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_f"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert "s.offsetHeight<560" not in raw, "already written"
m = list(FOLD_RE.finditer(raw))
assert len(m) == 1, len(m)
old = m[0].group(0)
new = raw.replace(old, FOLD)
# every original line kept, except the two lines of the folding block that this round replaces
for line in raw.split("\n"):
    if line.strip() and line + "\n" not in old:
        assert line in new, ("an original line is missing", line[:90])
assert new.count('id="nlmx-fold-js"') == 1 and new.count('id="nlmx-fold-css"') == 1
assert not re.search(r"[–—]", re.sub(r"<[^>]+>", " ", FOLD).replace('content:"−"', ""))
print("[page %d] folding block %d -> %d bytes; content %d -> %d bytes" % (PID, len(old), len(FOLD), len(raw), len(new)))
if DRY:
    io.open(os.path.join(H, "preview-content-f.html"), "w", encoding="utf-8", newline="").write(new)
    io.open(os.path.join(H, "fold-old.html"), "w", encoding="utf-8", newline="").write(old)
    io.open(os.path.join(H, "fold-f.html"), "w", encoding="utf-8", newline="").write(FOLD)
    print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"fold v2": "s.offsetHeight<560" in page, "one fold script": page.count('id="nlmx-fold-js"') == 1, "38 questions": page.count('"@type":"Question"') == 38,
      "one h1": page[page.find("<body"):].count("<h1") == 1, "HowTo": 'id="nlmx-howto"' in page, "market": 'id="mortgage-market"' in page}
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
