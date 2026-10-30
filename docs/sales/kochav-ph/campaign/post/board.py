# -*- coding: utf-8 -*-
"""The proof board and kit for the Kochav organic post (29.10.2026): the post in four languages (videos, images, the words with copy
buttons), the proof against the award-winning and top real-estate posts (research file, Gemini jury scores, Codex language review),
the tools and how to post. Writes board/index.html and the list of files to publish with it.
  python board.py   -> board/index.html, board/files.json"""
import html, io, json, os
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(H, "out"); B = os.path.join(H, "board"); os.makedirs(B, exist_ok=True)
LANGS = [("he", "עברית"), ("en", "English"), ("fr", "Français"), ("ru", "Русский")]
E = html.escape
crit = {l: json.load(io.open(os.path.join(O, l, "critic.json"), encoding="utf-8")) for l, _ in LANGS}
before = json.load(io.open(os.path.join(H, "critic-before.json"), encoding="utf-8"))
txt = {l: {n: io.open(os.path.join(O, l, n + ".txt"), encoding="utf-8").read().strip() for n in ("post", "comment", "short", "group")} for l, _ in LANGS}
files = {}
for l, _ in LANGS:
    for f in ["cover-4x5.jpg"] + ["card-%d.jpg" % i for i in range(1, 7)] + ["reel-9x16-full.mp4"]:
        files["m/%s/%s" % (l, f)] = os.path.join(O, l, f)

# the checklist as Gemini judged it, per language (the criterion names come from the research file, section 6)
rows = []
n = len(crit["he"]["scores"])
for i in range(n):
    name = crit["he"]["scores"][i]["criterion"]
    cells = "".join('<td class="%s" title="%s">%s</td>' % ("ok" if crit[l]["scores"][i]["pass"] else "no", E(crit[l]["scores"][i]["evidence"][:400]),
                                                         "עומד" if crit[l]["scores"][i]["pass"] else "חסר") if i < len(crit[l]["scores"]) else "<td></td>" for l, _ in LANGS)
    rows.append("<tr><th scope=\"row\" dir=\"ltr\">%s</th>%s</tr>" % (E(name), cells))
score = lambda d: d.get("overall_10")
passed = lambda d: "%d/%d" % (sum(1 for s in d["scores"] if s["pass"]), len(d["scores"]))

tabs = "".join('<button type="button" role="tab" id="t-%s" aria-controls="p-%s" aria-selected="%s" data-l="%s">%s</button>' % (l, l, "true" if l == "he" else "false", l, n) for l, n in LANGS)
panels = []
for l, name in LANGS:
    d = "rtl" if l == "he" else "ltr"
    cards = "".join('<figure><img src="m/%s/card-%d.jpg" alt="" loading="lazy" width="1440" height="1440"><figcaption>%d/6</figcaption></figure>' % (l, i, i) for i in range(1, 7))
    blocks = "".join(
        '<div class="copy"><div class="copy-h"><b>%s</b><button type="button" class="cp" data-for="x-%s-%s">העתקה</button></div>'
        '<pre id="x-%s-%s" dir="%s" lang="%s">%s</pre></div>' % (lab, l, k, l, k, d, l, E(txt[l][k]))
        for k, lab in (("post", "הפוסט"), ("comment", "תגובה ראשונה, עם הקישור"), ("group", "שני נוסחים לקבוצות (בתיקייה של גרוק בוט יש חמישה)")))
    panels.append(
        '<section role="tabpanel" id="p-%s" aria-labelledby="t-%s" %s>' % (l, l, "" if l == "he" else "hidden") +
        '<div class="media"><div class="reel"><video src="m/%s/reel-9x16-full.mp4" controls playsinline preload="metadata"></video>'
        '<p class="cap">רילס במסך מלא, 23.4 שניות: ההליכה של מיטל בדירה, מהמבואה עד המרפסת. יש גם גרסת חלון ריבועי וגרסת פיד 4:5.</p></div>' % l +
        '<div class="cov"><img src="m/%s/cover-4x5.jpg" alt="תמונת הפוסט" width="1440" height="1800"><p class="cap">תמונת הפוסט 4:5, 1440 על 1800</p></div></div>' % l +
        '<div class="cards">%s</div>' % cards + '<div class="copies">%s</div></section>' % blocks)

CASES = [
 ("SERHANT · Signature Content Suite", "Shorty Awards, זוכה, נדל״ן", "המתווכים מול המצלמה בבית האמיתי, סרט קצר וחיתוכים אנכיים מאותו יום צילום", "31.5 מיליון צפיות, 130 מיליון דולר מכירות", "https://shortyawards.com/15th/serhant-signature-content-suite"),
 ("Knight Frank · רילס של סוכנים", "Social Media Campaign of the Year 2024", "רילס עם הסוכנים עצמם בבתים, קריאה אחת לפעולה: הודעה", "39% מעורבות, 0.15 ליש״ט לליד", "https://passion.digital/case-studies/knight-frank-residential-paid-social-case-study/"),
 ("SERHANT · Through The Lens Of", "Shorty Awards, זוכה, נדל״ן", "סיפור לפני מפרט, תזמון לרגע תרבותי", "65.65 מיליון דולר שווקו", "https://shortyawards.com/16th/ThroughTheLensOf"),
 ("REMAX · Get Golden Home", "Shorty Awards, זוכה, נדל״ן", "רכישה אמיתית ואדם אמיתי, מתווך מקומי מול המצלמה", "618 מיליון חשיפות", "https://shortyawards.com/18th/get-golden-home"),
 ("Toll Brothers · Obsession", "NAHB The Nationals 2020, קמפיין החברתי הטוב ביותר", "תשוקה לחדרים מסוימים, לא למפרט", "29 אלף מעורבויות", "https://www.probuilder.com/nationals-2020"),
 ("Concierge Auctions · סרטי נכסים", "10 פרסי Telly 2026", "צילום קולנועי של הנכס האמיתי לכל גודל מסך", "לא פורסם", "https://www.conciergeauctions.com/blog/concierge-auctions-earns-10-telly-awards-honoring-excellence-in-videography-and-real-estate-marketing"),
]
cases = "".join('<li><a href="%s" target="_blank" rel="noopener" dir="ltr">%s</a><span class="aw">%s</span><p>%s</p><span class="res">%s</span></li>' % (u, E(n), E(a), E(w), E(r)) for n, a, w, r, u in CASES)

TOOLS = [("Claude Design", "כרטיס KochavSocialPost במערכת העיצוב: הצבעים, הגופנים, חוקי האזור הבטוח והפריימים"),
         ("צילומי מיטל", "כל תמונה וכל קטע וידאו צולמו בדירה או ממנה. התוכנית מסומנת הדמיה. אין סצנות מצוירות ואין דירה מומצאת"),
         ("Edge ו-HTML", "כל טקסט על התמונות נבנה כטיפוגרפיה אמיתית בעברית, צרפתית ורוסית, וכל כותרת מתכווצת לשורה אחת"),
         ("ffmpeg", "הרילס והפיד: תנועת מצלמה איטית על התמונות, הסרטון של מיטל בחלון מרובע, מעברים, מוזיקת רקע ועוצמה מנורמלת. DaVinci Resolve מותקן ולא נדרש"),
         ("סוכן מחקר", "12 מקרים זוכים, 13 מפרסמים מובילים, הנחיות Meta, נתוני חשיפה אורגנית וכללי האתיקה למתווכים, עם מקור ותאריך לכל טענה"),
         ("Codex (GPT)", "עריכת שפה לאנגלית, צרפתית ורוסית: ציונים 8, 8 ו-7 מתוך 10, והתיקונים הוכנסו"),
         ("Gemini 4 Argon", "שופט עצמאי מול רשימת הבדיקה של הזוכים: ציון לפני התיקונים ואחריהם, בכל שפה"),
         ("Nano Banana ו-gpt-image", "לא שימשו לתמונות הבית, בכוונה. מיטל כבר תפסה תמונה מומצאת אחת, ופוסט של נכס אמיתי מראה רק את הנכס")]
tools = "".join("<li><b>%s</b><span>%s</span></li>" % (E(a), E(b)) for a, b in TOOLS)
sc = "".join('<div class="sc"><b dir="ltr">%s</b><span class="was">%s</span><span class="now">%s</span><span class="pp">%s</span></div>'
             % (n, score(before[l]), score(crit[l]), passed(crit[l])) for l, n in LANGS)
gaps = "".join("<li>%s</li>" % E(x) for x in (
    "הוחלט ב-30.10: מפרסמים כמו שזה, בלי מיטל מול המצלמה. הבדיקה היחידה שנשארת פתוחה בגלל זה היא אדם מול המצלמה; אם יגיע קליפ שלה, הוא נכנס לפתיחת הרילס בלי לשנות שום דבר אחר",
    "הסכמת הבעלים על הפרסום (מיטל מחזיקה בלעדיות). כשהדירה נמכרת, מורידים את הפוסט",
    "גרוק בוט מפרסם לעמוד NadLan ולקבוצות. כל החומר, החוקים, העובדות וחמישה נוסחים לקבוצות בכל שפה נמצאים בתיקייה שלו: C:\\Users\\777\\Documents\\grok-bot\\nadlan-campaign. בקבוצות: נוסח שונה בכל קבוצה, עד 5 קבוצות ביום. אין לנו ערוץ ב-X"))

PAGE = """<title>פוסט כוכב הצפון</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@600&family=Assistant:wght@400;600;700;800&family=Noto+Sans:wght@400;600&display=swap">
<style>
/* a listing sheet: the media first, the words to paste beside it, the proof under it; plan-sheet ink, sea blue for marking */
:root{--bg:#F4F7F8;--paper:#FFFFFF;--ink:#14212B;--ink2:#3E4C58;--mute:#5E6A75;--line:#D3DCE2;--sea:#2F6F86;--ok:#1E7A55;--okbg:#E3F2EA;--no:#9A3B1E;--nobg:#F6E7E1;
 --serif:"Noto Serif Hebrew",Georgia,serif;--sans:Assistant,"Noto Sans","Segoe UI",Arial,sans-serif;--mono:ui-monospace,Consolas,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0E171E;--paper:#15222C;--ink:#EAF1F4;--ink2:#C2CED5;--mute:#93A3AE;--line:#2A3A46;--sea:#7FB9CE;--ok:#7FD1AE;--okbg:#173327;--no:#F0A58C;--nobg:#3A221B;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0E171E;--paper:#15222C;--ink:#EAF1F4;--ink2:#C2CED5;--mute:#93A3AE;--line:#2A3A46;--sea:#7FB9CE;--ok:#7FD1AE;--okbg:#173327;--no:#F0A58C;--nobg:#3A221B;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink2);font:400 16px/1.65 var(--sans)}
.w{max-width:1180px;margin:0 auto;padding-block:28px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1{font:600 clamp(26px,4vw,38px)/1.2 var(--serif);color:var(--ink);margin:0 0 8px;text-wrap:balance}
h2{font:600 clamp(20px,2.6vw,26px)/1.3 var(--serif);color:var(--ink);margin:0;text-wrap:balance}
.lede{max-width:70ch;margin:0;color:var(--ink2)}
.k{font:700 13px/1.3 var(--sans);letter-spacing:.06em;color:var(--sea);margin:0 0 6px}
.sec{display:grid;gap:16px;margin-top:40px;padding-top:18px;border-top:2px solid var(--ink)}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.tabs button{font:700 15px/1 var(--sans);padding:11px 16px;border-radius:999px;border:1.5px solid var(--line);background:var(--paper);color:var(--ink);cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.tabs button:focus-visible,.cp:focus-visible{outline:3px solid var(--sea);outline-offset:2px}
[role=tabpanel]{display:grid;gap:18px;margin-top:16px}
.media{display:grid;grid-template-columns:minmax(0,300px) minmax(0,360px);gap:18px;align-items:start}
.reel video{width:100%;aspect-ratio:9/16;background:#0E171E;border-radius:14px;display:block;max-width:100%}
.cov img{width:100%;height:auto;border-radius:10px;display:block}
.cap{font:600 13px/1.4 var(--sans);color:var(--mute);margin:6px 0 0}
.cards{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}
.cards figure{margin:0}.cards img{width:100%;height:auto;border-radius:8px;display:block}
.cards figcaption{font:600 12px var(--sans);color:var(--mute);text-align:center;margin-top:3px}
.copies{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.copy{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:12px 14px;min-width:0}
.copy-h{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:8px}
.copy-h b{font:700 14.5px var(--sans);color:var(--ink)}
.cp{font:700 13.5px var(--sans);padding:8px 14px;border-radius:8px;border:0;background:var(--sea);color:var(--paper);cursor:pointer}
pre{margin:0;white-space:pre-wrap;word-break:break-word;font:400 15px/1.6 var(--sans);color:var(--ink);max-height:360px;overflow:auto}
.scores{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.sc{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px;display:grid;gap:2px}
.sc b{font:700 14px var(--sans);color:var(--ink)}.sc .was{font:600 14px var(--sans);color:var(--mute);text-decoration:line-through}
.sc .now{font:800 34px/1.1 var(--sans);color:var(--ink);font-variant-numeric:tabular-nums}.sc .pp{font:600 13px var(--sans);color:var(--mute)}
.sc .was::before{content:"לפני התיקונים "}.sc .pp::before{content:"בדיקות שעברו "}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--paper)}
table{border-collapse:collapse;width:100%;min-width:640px;font:500 13.5px/1.45 var(--sans)}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:start;vertical-align:top}
thead th{background:var(--ink);color:var(--bg);font-weight:700}
tbody th{font-weight:600;color:var(--ink);text-align:left}
td.ok{color:var(--ok);background:var(--okbg);font-weight:800;text-align:center}td.no{color:var(--no);background:var(--nobg);font-weight:800;text-align:center}
.cases{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.cases li{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:14px;display:grid;gap:6px;align-content:start}
.cases a{font:700 15px var(--sans);color:var(--ink)}.cases .aw{font:700 12.5px var(--sans);color:var(--sea)}
.cases p{margin:0;font-size:14.5px}.cases .res{font:700 13.5px var(--sans);color:var(--ink)}
.us{background:var(--paper);border-inline-start:4px solid var(--sea);padding:12px 16px;border-radius:6px;max-width:80ch}
.tools{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.tools li{display:grid;grid-template-columns:minmax(120px,170px) minmax(0,1fr);gap:12px;padding:10px 0;border-bottom:1px solid var(--line)}
.tools b{color:var(--ink)}
ul.gaps{margin:0;padding-inline-start:20px;display:grid;gap:8px;max-width:80ch}
@media (max-width:900px){.media{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.cards{grid-template-columns:repeat(3,minmax(0,1fr))}.cases{grid-template-columns:minmax(0,1fr)}.scores{grid-template-columns:repeat(2,minmax(0,1fr))}.tools{grid-template-columns:minmax(0,1fr)}}
@media (max-width:640px){.media,.copies{grid-template-columns:minmax(0,1fr)}.tools li{grid-template-columns:minmax(0,1fr)}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style>
<div class="w" dir="rtl" lang="he">
<p class="k">כוכב הצפון · פוסט אורגני · 29.10.2026</p>
<h1>מיני פנטהאוז בכוכב הצפון: הפוסט, בארבע שפות</h1>
<p class="lede">רילס, תמונת פוסט ושישה כרטיסים מהצילומים של מיטל, והטקסט להדבקה. הכול מהדף החי: 76 מ״ר מרפסות, חדר כושר וחדר דיירים, מתווכת ורישיון. הקישור לדף בשפה המתאימה נמצא בתגובה הראשונה.</p>
<div class="tabs" role="tablist" aria-label="שפה">__TABS__</div>
__PANELS__
__OLD__
<section class="sec"><p class="k">ההוכחה</p><h2>ציון של שופט עצמאי מול רשימת הבדיקה של הזוכים</h2>
<p class="lede">Gemini 4 Argon קיבל את התמונות, פריימים מהרילס והטקסטים, ובדק כל שפה מול 18 בדיקות שנגזרו מהעבודות שזכו בפרסים ומהנחיות Meta. הציון בכל כרטיס הוא אחרי התיקונים; הציון המחוק הוא לפניהם.</p>
<div class="scores">__SCORES__</div>
<div class="tbl"><table><thead><tr><th>הבדיקה (מקובץ המחקר)</th><th>עברית</th><th>English</th><th>Français</th><th>Русский</th></tr></thead><tbody>__ROWS__</tbody></table></div></section>
<section class="sec"><p class="k">מה עושים הזוכים</p><h2>שש עבודות שזכו בפרסים, ומה לקחנו מהן</h2>
<ul class="cases">__CASES__</ul>
<p class="us">מה לקחנו מהן לפוסט: צילום אמיתי של הנכס, סרטון אנכי לצד התמונות, משפט על החיים בבית לפני רשימת הנתונים, קריאה אחת לפעולה (וואטסאפ למיטל), טקסט על המסך לצפייה בלי קול, המתווכת בשמה ועם הרישיון, והקישור בתגובה ולא בגוף הפוסט (98.9% מהצפיות בפייסבוק הן בפוסטים בלי קישור, לפי Meta).</p></section>
<section class="sec"><p class="k">הכלים</p><h2>מה כל כלי עשה</h2><ul class="tools">__TOOLS__</ul></section>
<section class="sec"><p class="k">סופי · 30.10.2026</p><h2>לפני שהבוט מפרסם</h2><ul class="gaps">__GAPS__</ul></section>
</div>
<script>
(function(){var tabs=[].slice.call(document.querySelectorAll('[role=tab]'));
function show(l){tabs.forEach(function(t){var on=t.dataset.l===l;t.setAttribute('aria-selected',on?'true':'false');document.getElementById('p-'+t.dataset.l).hidden=!on;if(!on){var v=document.querySelector('#p-'+t.dataset.l+' video');if(v)v.pause()}})}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.l)})});
var h=(location.hash||'').slice(1);if(['he','en','fr','ru'].indexOf(h)>=0)show(h);
document.querySelectorAll('.cp').forEach(function(b){b.addEventListener('click',function(){var el=document.getElementById(b.dataset.for),t=el.textContent;
function sel(){var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r)}
var done=function(){b.textContent='הועתק';setTimeout(function(){b.textContent='העתקה'},1600)};
try{navigator.clipboard.writeText(t).then(done,function(){sel();b.textContent='סומן, העתיקו'})}catch(e){sel();b.textContent='סומן, העתיקו'}})});})();
</script>"""
OLD = [("הפוסט בעברית בעמוד NadLan (פורסם הבוקר)", "פוסט קישור: בפייסבוק 98.9% מהצפיות הן בפוסטים בלי קישור, ופוסט קישור מקבל את המעורבות הנמוכה ביותר (0.05% מול 0.18% לרילס ולאלבום). חסרים המילה מתווכת ומספר הרישיון, שהתקנות מחייבות. מזמין לסיור תלת ממד, אחרי שמיטל ביקשה להציג רק צילומים אמיתיים."),
       ("הפוסט באנגלית (פורסם הבוקר)", "הסרט המלא של שתי דקות, שנפתח בפריימים שחורים, כך ששלוש השניות הראשונות לא עוצרות גלילה. המשפט opened straight onto the city's biggest park לא מדויק לפני שהגשר נפתח ב-2027. אין רישיון."),
       ("העמוד עצמו", "לעמוד NadLan יש 0 עוקבים, ולכן פוסט אורגני בו כמעט לא נראה. החשיפה תגיע משיתוף בעמוד ובפרופיל של מיטל, מקבוצות (ידנית) ומשיתופים.")]
old = '<section class="sec"><p class="k">מה כבר עלה</p><h2>הפוסטים שעלו היום, ולמה החדש ברמה אחרת</h2><ul class="cases">%s</ul></section>' % "".join(
    '<li><b style="color:var(--ink)">%s</b><p>%s</p></li>' % (E(a), E(b)) for a, b in OLD)
out = (PAGE.replace("__TABS__", tabs).replace("__PANELS__", "\n".join(panels)).replace("__SCORES__", sc).replace("__ROWS__", "".join(rows))
       .replace("__CASES__", cases).replace("__TOOLS__", tools).replace("__GAPS__", gaps).replace("__OLD__", old))
io.open(os.path.join(B, "index.html"), "w", encoding="utf-8").write(out)
json.dump(files, io.open(os.path.join(B, "files.json"), "w", encoding="utf-8"), indent=1)
print("board", len(out) // 1024, "KB,", len(files), "files,", sum(os.path.getsize(p) for p in files.values()) // (1024 * 1024), "MB")
