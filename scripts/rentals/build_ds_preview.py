# -*- coding: utf-8 -*-
"""Builds the Claude Design previews for the rentals app from the REAL code
(assets/rentals/*), so the design and the code can never drift apart.
Writes <out>/project/components/RentalsManager/preview.html and
<out>/project/components/RentalsManagerPhone/preview.html.
Usage: python scripts/rentals/build_ds_preview.py <out_dir> [lang]"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
A = ROOT / "plugins/nadlan-config/assets/rentals"
OUT = pathlib.Path(sys.argv[1])
read = lambda p: (A / p).read_text(encoding="utf-8")

def page(card_line, width, start_lang, hash_route):
    css = read("rm.css")
    js = "\n".join(read(f) for f in ("rm-core.js", "rm-demo.js", "rm-views.js", "rm-drawers.js", "rm-lease.js", "rm-import.js"))
    he = json.loads(read("i18n/he.json")); en = json.loads(read("i18n/en.json")); lease = json.loads(read("i18n/lease.json")); triage = json.loads(read("i18n/triage.json"))
    has3d = (A / "rm-3d.js").exists()
    three = read("rm-3d.js") if has3d else ""
    for bad in ("</script", "</SCRIPT"):
        assert bad not in js and bad not in three, "a literal </script inside the bundle"
    data = json.dumps({"he": he, "en": en, "lease": lease, "triage": triage}, ensure_ascii=False).replace("</", "<\\/")
    return f"""{card_line}
<!doctype html>
<html lang="{start_lang}" dir="{'rtl' if start_lang == 'he' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RentalsManager</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&amp;family=Assistant:wght@300;400;600;700;800&amp;display=swap">
<script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}}}</script>
<style>{css}
body{{margin:0;background:#f7f6f2}}
.ds-wrap{{max-width:{width}px;margin:0 auto;padding:12px 16px 40px}}
</style>
</head>
<body>
<div class="ds-wrap"><div id="app"></div></div>
<script>{js}</script>
<script>
(function () {{
	var D = {data};
	var N = window.NLRM, lang = "{start_lang}";
	N.LEASE = D.lease;
	N.TRIAGE = D.triage;
	var strings = {{ he: D.he.ui, en: D.en.ui }}, msg = {{ he: D.he.msg, en: D.en.msg }};
	N.setStrings(lang, strings[lang]);
	if (!location.hash) {{ try {{ history.replaceState(null, "", "#/{hash_route}"); }} catch (e) {{}} }}
	N.mount(document.getElementById("app"), {{ lang: lang, strings: strings, msg: msg, adapter: N.DemoAdapter(lang), inPlaceLang: true,
		me: {{ display: lang === "he" ? "דני כהן" : "Dan Cohen", phone: "972500000999", pay: {{ bit: "972500000999" }} }}, urls: {{ pros: "https://nad-lan.co.il/professionals/", wizard: "https://nad-lan.co.il/post-listing/" }} }});
}})();
</script>
{('<script type="module">' + three + '</script>') if has3d else ''}
</body>
</html>
"""

for comp, width, line in (
    ("RentalsManager", 1240, '<!-- @dsCard group="Pages" height=1500 width=1440 subtitle="ניהול השכרות v2 (1.10.2026): האפליקציה עצמה על נתוני דוגמה. עברית ואנגלית, לחיצה על כל דירה, שוכר ותקלה פותחת את כל המידע" -->'),
    ("RentalsManagerPhone", 390, '<!-- @dsCard group="Pages" height=1600 width=420 subtitle="ניהול השכרות v2 בטלפון (390): אותה אפליקציה, ניווט בשורה אחת, כרטיסים על כל המסך, בלי גלילה בתוך גלילה" -->'),
):
    d = OUT / "project/components" / comp
    d.mkdir(parents=True, exist_ok=True)
    (d / "preview.html").write_text(page(line, width, "he", "today"), encoding="utf-8")
    print(comp, (d / "preview.html").stat().st_size, "bytes")
