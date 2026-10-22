# -*- coding: utf-8 -*-
"""make deploy498.py from deploy497.py: 1.72.498 (HAD-592, Ben 22.10.2026, the page loop: "one click with your fingers to get
everything", "title, breadcrumbs and h1 are never the same", "make sure they index on all the search engines and the AI bots").
  - assets/instruments/core.js + core.css: presets (a row of ready cases; one tap fills every field), euro formatting.
  - inc/instruments.php: the shortcode passes preset/region/kind/price; /llms.txt (a reading list for AI assistants) and the
    IndexNow key file.
  - inc/breadcrumbs.php: [nadlan_crumbs], an opt-in trail for regular pages (visible + BreadcrumbList with the #breadcrumb @id
    that Yoast's WebPage already points to). No page carries it yet.
  - inc/page-h1.php: a page that opens with its trail keeps the trail above the H1; the profession archives get a Hebrew heading
    and title instead of "Profession: קבלן" (site gap audit 21.10, item 2).
No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/instruments/core.js", "assets/instruments/core.css", "inc/instruments.php", "inc/breadcrumbs.php", "inc/page-h1.php"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy497.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set([])"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.498: no hunk; the files come back from .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.497", "1.72.498"), ("ps497", "ps498"), ("bak497", "bak498"), ("make_deploy497", "make_deploy498"),
             ("deploy-result-497", "deploy-result-498"), ("speed-497", "speed-498"), ("posts-before-497", "posts-before-498"),
             ("ashira_497", "ashira_498"), ("deploy-result-496", "deploy-result-497"), ("1.72.496", "1.72.497")]:
    src = src.replace(a, b)
src = re.sub(r"\?t497([a-z]?)=1", r"?t498\1=1", src)
src = re.sub(r"&t497([a-z]?)=1", r"&t498\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(497, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_498 as PX  # noqa: E402 \([^)]*\)", "import ashira_498 as PX  # noqa: E402 (1.72.498: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t498d=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/core.js?t498p=1', ['applyPreset', 'nli__pre', \"eur: function\"], []),\n"
                       "    ('/wp-content/plugins/nadlan-config/assets/instruments/core.css?t498q=1', ['.nli__pre{', 'nli__prelab'], []),\n"
                       "    ('/llms.txt?t498l=1', ['# nad-lan.co.il', '## Calculators', '/purchase-tax-calculator/'], ['<html']),\n"
                       "    ('/f25cb29869da9a9709dedcde8a7efc7a.txt?t498x=1', ['f25cb29869da9a9709dedcde8a7efc7a'], ['<html']),\n"
                       "    ('/profession/%D7%A7%D7%91%D7%9C%D7%9F/?t498r=1', ['קבלני בנייה וביצוע בפרויקטים באתר'], ['Profession: ', 'ארכיון קבלן']),\n"
                       "    ('/profession/%D7%99%D7%96%D7%9D/?t498s=1', ['יזמי נדל״ן בישראל: החברות והפרויקטים'], ['Profession: ']),\n"
                       "    ('/beit-hakerem/?t498h=1', ['data-nli-set', 'FAQPage', 'nlds-pagehead__title'], ['nlbc--page']),\n"
                       "    ('/tel-aviv-plans/yad-eliyahu/?t498y=1', ['data-nli=\"pval\"', '65210057', 'FAQPage'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.498 LIVE: [^"]*"\)', 'print("RELEASE 1.72.498 LIVE: presets, euros, page breadcrumbs, llms.txt + IndexNow, Hebrew profession headings")', src)
open(os.path.join(H, "deploy498.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_498.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.498 (HAD-592): presets, euros, page breadcrumbs, llms.txt + IndexNow, Hebrew profession headings. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy498.py + ashira_498.py written")
