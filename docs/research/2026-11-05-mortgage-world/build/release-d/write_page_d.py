# -*- coding: utf-8 -*-
"""MortgageWorld D, page 121 (HAD-675): the page-level LOSE rows of proof/proof.md, no code release.
  1. A shorter lead: the first paragraph keeps the definition and the number of the month; its last two sentences move, unchanged,
     into a new paragraph right after the quick calculator (nothing removed). The first field on a phone moves up.
  2. The 10 inputs of the classic three-track calculator get aria-label (label text + track number): they had a <label> that was
     not tied to the input.
  3. The old guide photo, hotlinked from Wikimedia Commons (166 KB, no credit), is hosted on the site and credited as its licence
     requires: Chenspec, CC BY-SA 4.0 (checked on the Commons API 5.11.2026).
  4. On phones (<900px) a small script folds the long guide sections behind one button each (the heading and the first paragraph
     stay visible) and turns the FAQ answers into tap-to-open; every word stays in the HTML (search engines, AI answers, FAQPage),
     nothing is removed. Tap targets inside the tools get a 44px minimum.
  python write_page_d.py --dry | python write_page_d.py"""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
LEAD_A = 'בחודש הראשון. הקלידו סכום, בחרו תמהיל או אחד משלושת הסלים האחידים של בנק ישראל, וראו את ההחזר הראשון, את ההחזר הגבוה הצפוי, את לוח הסילוקין, והאם הריבית שהבנק הציע לכם גבוהה מהממוצע שבנק ישראל פרסם החודש. כל הנתונים ממקורות רשמיים, עם תאריך.</p>'
LEAD_B = 'בחודש הראשון.</p>'
MOVED = '<p class="nlu1-sub">הקלידו סכום, בחרו תמהיל או אחד משלושת הסלים האחידים של בנק ישראל, וראו את ההחזר הראשון, את ההחזר הגבוה הצפוי, את לוח הסילוקין, והאם הריבית שהבנק הציע לכם גבוהה מהממוצע שבנק ישראל פרסם החודש. כל הנתונים ממקורות רשמיים, עם תאריך.</p>\n'
QUICK = '[nadlan_tool id="mquick"]\n'
WM = "https://commons.wikimedia.org/wiki/Special:FilePath/Diamond%20Exchange%20complex%20in%20Ramat%20Gan%2C%20Israel%202024%2055.jpg?width=960"
THUMB = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Diamond_Exchange_complex_in_Ramat_Gan%2C_Israel_2024_55.jpg/960px-Diamond_Exchange_complex_in_Ramat_Gan%2C_Israel_2024_55.jpg"
CAP_OLD = "לפני הצעה על דירה, בודקים החזר חודשי, ריבית, תקופה ויחס החזר מהכנסה.</figcaption>"
CAP_NEW = ('לפני הצעה על דירה, בודקים החזר חודשי, ריבית, תקופה ויחס החזר מהכנסה. <span class="nlmx-credit">צילום: Chenspec, '
           '<a href="https://commons.wikimedia.org/wiki/File:Diamond_Exchange_complex_in_Ramat_Gan,_Israel_2024_55.jpg" rel="nofollow noopener" target="_blank">ויקישיתוף</a>, '
           '<a href="https://creativecommons.org/licenses/by-sa/4.0/" rel="nofollow noopener license" target="_blank">CC BY-SA 4.0</a></span></figcaption>')
FOLD = ('<style id="nlmx-fold-css">@media (max-width:899px){.nlmx-more{display:flex;align-items:center;justify-content:center;width:100%;min-height:44px;margin:6px 0 14px;'
        'border:1px solid #D3DCE2!important;border-radius:999px!important;background:#fff!important;color:#2F6F86!important;font:600 15px/1.2 "IBM Plex Sans Hebrew",system-ui,sans-serif!important;cursor:pointer}'
        '.nlmx-folded>*:not(h2):not(.nlmx-keep):not(.nlmx-more){display:none!important}'
        '#faq h3.nlmx-q{cursor:pointer;position:relative;padding-inline-start:26px!important;min-height:44px;display:flex;align-items:center}'
        '#faq h3.nlmx-q::before{content:"+";position:absolute;inset-inline-start:0;font:600 20px/1 "IBM Plex Mono",monospace;color:#2F6F86}'
        '#faq h3.nlmx-q[aria-expanded="true"]::before{content:"−"}#faq .nlmx-a[hidden]{display:none!important}}'
        '.entry-content .nli button,.entry-content .nli select,.entry-content .nlmm a{min-height:44px}.nlmx-credit{display:block;font-size:12px;color:#5E6A75}</style>\n'
        '<script id="nlmx-fold-js">(function(){if(!window.matchMedia||!window.matchMedia("(max-width: 899px)").matches)return;'
        'function go(){var skip={"tools":1,"mortgage-market":1,"mortgage-rules-facts":1,"faq":1};'
        '[].forEach.call(document.querySelectorAll(".nadlan-guide section"),function(s){if(skip[s.id]||s.closest(".nlmx-sw,.nli,#faq,#mortgage-market"))return;var h=s.querySelector(":scope>h2");'
        'if(!h||s.offsetHeight<1100)return;var p=h.nextElementSibling;if(p&&p.tagName==="P")p.classList.add("nlmx-keep");s.classList.add("nlmx-folded");'
        'var b=document.createElement("button");b.type="button";b.className="nlmx-more";b.setAttribute("aria-expanded","false");b.textContent="להמשך הפרק";'
        'b.addEventListener("click",function(){s.classList.remove("nlmx-folded");b.remove();});(p&&p.classList.contains("nlmx-keep")?p:h).after(b);});'
        'var f=document.getElementById("faq");if(f){[].forEach.call(f.querySelectorAll("h3"),function(q){var a=[],n=q.nextElementSibling;while(n&&n.tagName==="P"){a.push(n);n=n.nextElementSibling;}'
        'if(!a.length)return;q.classList.add("nlmx-q");q.setAttribute("role","button");q.setAttribute("tabindex","0");q.setAttribute("aria-expanded","false");a.forEach(function(x){x.classList.add("nlmx-a");x.hidden=true;});'
        'function t(){var o=q.getAttribute("aria-expanded")!=="true";q.setAttribute("aria-expanded",String(o));a.forEach(function(x){x.hidden=!o;});}'
        'q.addEventListener("click",t);q.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();t();}});});}}'
        'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",go);else go();})();</script>\n')

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_d"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, AUTH, BASE, UA = ns["req"], ns["AUTH"], ns["BASE"], ns["UA"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert 'id="nlmx-fold-js"' not in raw, "already written"
new = raw
EDITS = [(LEAD_A, LEAD_B), (QUICK, QUICK + MOVED), (CAP_OLD, CAP_NEW)]
for o, n_ in EDITS:
    assert new.count(o) == 1, ("anchor", o[:50], new.count(o)); new = new.replace(o, n_)
# 2. the classic inputs: <label>X</label><input ... data-t="N" -> aria-label
cls = new.index('id="nlc-mortgage"'); cle = new.index("</script>", cls)
seg = new[cls:cle]
cnt = [0]
def lab(m):
    cnt[0] += 1
    t = m.group(2); k = re.search(r'data-t="(\d)"', m.group(3)); tr = " · מסלול %d" % (int(k.group(1)) + 1) if k else ""
    return m.group(1) + '<input aria-label="' + t.replace('"', "") + tr + '"' + m.group(3)
seg2 = re.sub(r'(<label>([^<]+)</label>\s*)<input(?![^>]*aria-label)([^>]*>)', lab, seg)
new = new[:cls] + seg2 + new[cle:]
# 3. the photo (uploaded below; the dry run checks the anchor only)
assert new.count(WM) == 1, new.count(WM)
# 4. the phone folding, before the FAQ section
FAQ_A = '<section id="faq">'
assert new.count(FAQ_A) == 1
new = new.replace(FAQ_A, FOLD + FAQ_A)
# checks: every original line kept (the edited ones in their edited form; the classic inputs differ only by aria-label)
NOARIA = re.sub(r'<input aria-label="[^"]*"', '<input', new)
for line in raw.split("\n"):
    if not line.strip():
        continue
    ln = line
    for o, n_ in EDITS:
        ln = ln.replace(o, n_)
    assert ln in new or ln in NOARIA, ("an original line is missing", line[:90])
print("[page %d] edits %d | classic inputs labelled %d | fold script %d bytes" % (PID, len(EDITS), cnt[0], len(FOLD)))
assert cnt[0] >= 9, cnt[0]
v = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", MOVED + CAP_NEW))
assert not re.search(r"[–—]", v)
if DRY:
    io.open(os.path.join(H, "preview-content-d.html"), "w", encoding="utf-8", newline="").write(new); print("[dry] ok"); sys.exit(0)
# upload the photo
img = urllib.request.urlopen(urllib.request.Request(THUMB, headers={"User-Agent": "nad-lan-media/1.0"}), timeout=60).read()
assert img[:3] == b"\xff\xd8\xff" and len(img) > 50000, len(img)
rq = urllib.request.Request(BASE + "/wp-json/wp/v2/media", data=img, method="POST", headers={"Authorization": AUTH, "User-Agent": UA, "Content-Type": "image/jpeg",
                            "Content-Disposition": 'attachment; filename="diamond-exchange-ramat-gan-chenspec-cc-by-sa.jpg"'})
m = json.load(urllib.request.urlopen(rq, timeout=180))
req("POST", "/wp-json/wp/v2/media/%d" % m["id"], {"alt_text": "בנייני משרדים ומגורים בישראל לפני חישוב החזר משכנתא", "caption": "צילום: Chenspec, ויקישיתוף, CC BY-SA 4.0"})
new = new.replace(WM, m["source_url"])
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"photo self-hosted": "commons.wikimedia.org/wiki/Special:FilePath" not in page and m["source_url"] in page, "credit": "Chenspec" in page, "fold script": 'id="nlmx-fold-js"' in page,
      "38 questions": page.count('"@type":"Question"') == 38, "one h1": page[page.find("<body"):].count("<h1") == 1, "moved paragraph": 'class="nlu1-sub"' in page}
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
print("[media]", m["id"], m["source_url"])
