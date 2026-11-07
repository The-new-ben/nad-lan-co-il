# Builds the Claude Design cards for ExpertAdvisor (DS v107) from the PRODUCTION files: advisor.css, advisor.js, the section markup
# rendered by inc/expert-advisor.php, and real answers captured from the model (replay-*.json). Nothing is drawn by hand.
import io, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); PLUG = os.path.join(H, "..", "..", "..", "..", "plugins", "nadlan-config")
css = io.open(os.path.join(PLUG, "assets", "expert-advisor", "advisor.css"), encoding="utf-8").read()
js = io.open(os.path.join(PLUG, "assets", "expert-advisor", "advisor.js"), encoding="utf-8").read()
OUT = os.path.join(H, "..", "design", "project", "components", "ExpertAdvisor")
FONTS_HE = "https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"
FONTS_EN = "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@600&family=IBM+Plex+Mono:wght@400;500&display=swap"
PAGE_CSS = """body{margin:0;background:#fff;font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#3E4C58}
.site{border-bottom:1px solid #D3DCE2;padding:12px 20px;font:600 15px/1 "IBM Plex Sans Hebrew",sans-serif;color:#12202A;display:flex;justify-content:space-between}
.site small{font:400 12px/1 "IBM Plex Mono",monospace;color:#5E6A75}
.wrapx{max-width:1120px;margin:0 auto;padding:20px 16px 40px}
h1{font:600 30px/1.2 "IBM Plex Sans Hebrew",sans-serif;color:#12202A;margin:6px 0 12px}
.hero p{font-size:16.5px;line-height:1.7;margin:0 0 12px;max-width:72ch}
.cta{display:inline-block;background:#1F4B5C;color:#fff;padding:12px 18px;border-radius:6px;font-weight:600;margin:4px 0 6px}
.next h2{font:600 22px/1.3 "IBM Plex Sans Hebrew",sans-serif;color:#1F4B5C;margin:8px 0 8px}.next p{margin:0;line-height:1.7}
.note{font:400 12px/1.4 "IBM Plex Mono",monospace;color:#5E6A75;margin:0 0 10px}"""

def doc(card, lang, section, replay, page, opener, open_hand, width_note):
    en = lang == "en"
    q = [x["q"] for x in replay]
    rs = [dict(x["r"], ok=True) for x in replay]
    mock = """<script>
window.NL_ADV_CFG=%s;
(function(){var R=%s,Q=%s,i=0;var of=window.fetch;
window.fetch=function(u,o){if(String(u).indexOf('/advisor')>-1){var r=R[Math.min(i++,R.length-1)];return new Promise(function(res){setTimeout(function(){res({json:function(){return Promise.resolve(r)}})},350)})}
if(String(u).indexOf('/lead')>-1){return Promise.resolve({status:200,json:function(){return Promise.resolve({ok:true,lead_id:1})}})}return of.apply(this,arguments)};
window.addEventListener('load',function(){var k=0;function go(){if(k>=Q.length){%s return}window.NL_ADV.send(Q[k++]);setTimeout(go,900)}setTimeout(go,200)})})();
</script>""" % (json.dumps({"endpoint": "/wp-json/nadlan/v1/advisor", "lead": "/wp-json/nadlan/v1/lead", "page": page["id"], "tok": "x" * 24, "lang": lang, "kind": page["kind"], "title": page["title"], "v": "0.1.0"}, ensure_ascii=False),
                     json.dumps(rs, ensure_ascii=False), json.dumps(q, ensure_ascii=False),
                     "var b=document.getElementById('nladv-open');if(b&&!b.hidden)b.click();" if open_hand else "")
    return """%s
<!doctype html>
<html lang="%s" dir="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ExpertAdvisor 107</title>
<link rel="stylesheet" href="%s">
<style>%s</style>
<style>%s</style>
</head>
<body>
<div class="site"><span>%s</span><small>%s</small></div>
<div class="wrapx"><h1>%s</h1>
<div class="entry-content"><div class="nadlan-guide"><section class="hero wrap"><div><p>%s</p><span class="cta">%s</span></div></section>
<div class="next"><h2>%s</h2><p>%s</p></div></div></div></div>
%s
%s
<script>%s</script>
</body>
</html>
""" % (card, lang, "ltr" if en else "rtl", FONTS_EN if en else FONTS_HE, PAGE_CSS, css,
       "NadLan · nad-lan.co.il" if en else "נדל״ן · nad-lan.co.il", width_note,
       page["title"], opener, page["cta"], page["next"], page["next_p"], section.replace(" hidden>", ">", 1), mock, js)

he = json.load(io.open(os.path.join(H, "replay-he.json"), encoding="utf-8"))
en = json.load(io.open(os.path.join(H, "replay-en.json"), encoding="utf-8"))
s9 = io.open(os.path.join(H, "section-9.html"), encoding="utf-8").read().strip()
s5154 = io.open(os.path.join(H, "section-5154.html"), encoding="utf-8").read().strip()
P9 = {"id": 9, "kind": "guide", "title": "קניית דירה בישראל: מדריך בדיקות לפני חתימה", "cta": "בדיקת עלות כוללת",
      "next": "לפני שמתחילים לראות דירות", "next_p": "המדריך ממשיך כאן, מתחת ליועץ, בלי שינוי."}
OP9 = "קניית דירה בישראל היא אחת ההחלטות הכלכליות הגדולות ביותר למשפחה, לזוג צעיר או למשקיע. המחיר שמופיע במודעה הוא רק נקודת פתיחה."
P5 = {"id": 5154, "kind": "guide", "title": "Buying a Family Home in Israel from Abroad", "cta": "Check the total cost",
      "next": "Before you look at homes", "next_p": "The guide continues here, under the advisor, unchanged."}
OP5 = "Buying a home in Israel from abroad starts with three numbers: the purchase tax for foreign residents, the bank's 50% financing cap and the cash you need on top."
cards = [
    ("preview.html", '<!-- @dsCard group="Cards" height=1900 width=1180 subtitle="יועץ הנדל״ן בתוך המדריך, מחשב (גרסה 107, אב טיפוס מאחורי ?advisor=on)" -->', "he", s9, he, P9, OP9, True, "1180px · desktop"),
    ("preview-phone.html", '<!-- @dsCard group="Cards" height=3400 width=400 subtitle="יועץ הנדל״ן בטלפון, 390px (גרסה 107)" -->', "he", s9, he, P9, OP9, True, "390px · phone"),
    ("preview-en.html", '<!-- @dsCard group="Cards" height=1500 width=1180 subtitle="The NadLan advisor on the English guide (version 107)" -->', "en", s5154, en, P5, OP5, False, "1180px · desktop"),
]
for name, card, lang, sec, rep, page, op, oh, wn in cards:
    io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n").write(doc(card, lang, sec, rep, page, op, oh, wn))
    io.open(os.path.join(H, "local-" + name), "w", encoding="utf-8", newline="\n").write(doc("", lang, sec, rep, page, op, oh, wn))
    print(name, os.path.getsize(os.path.join(OUT, name)))
