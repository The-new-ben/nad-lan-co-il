# -*- coding: utf-8 -*-
"""Compose the live Echo City page from the approved redesign file (T3)."""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
SRC = r"C:\Users\777\Downloads\echo-city-redesign.html"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "echo-city-live.html")
html = open(SRC, encoding="utf-8").read()

STRICKER = "https://nad-lan.co.il/wp-content/uploads/2026/08/stricker-13-brandeis-14-plate-capsules.jpg"
BNEI = "https://nad-lan.co.il/wp-content/uploads/2026/08/bnei-dan-54-56-plate-capsules.jpg"
OG = "__OG_URL__"  # substituted by the deployer after the og PNG upload

# 1. swap the 4 embedded data URIs (order: flag stricker, flag bnei, grid bnei, grid stricker)
order = [STRICKER, BNEI, BNEI, STRICKER]
idx = {"i": 0}
def sub_uri(m):
    u = order[idx["i"]]
    idx["i"] += 1
    return u
html, n = re.subn(r'data:image/(?:jpeg|png|webp);base64,[A-Za-z0-9+/=]+', sub_uri, html)
assert n == 4, f"expected 4 data uris, got {n}"

# 2. strip the source's own <title>+font line; keep from <style> onward
style_at = html.index("<style>")
body_inner = html[style_at:]

# 3. form: add name field, make it a real lead form
body_inner = body_inner.replace(
    '<form class="form" aria-label="ספרו לנו מה אתם מחפשים">',
    '<form class="form" id="nl-echo-lead" aria-label="ספרו לנו מה אתם מחפשים">')
body_inner = body_inner.replace(
    '<div class="row">\n          <div><label for="f-city">עיר</label>',
    '<div class="row">\n          <div><label for="f-name">שם מלא</label><input id="f-name" type="text" autocomplete="name" placeholder="השם שלכם"></div>\n          <div><label for="f-city">עיר</label>', 1)
body_inner = body_inner.replace(
    '<div><label for="f-rooms">חדרים</label><select id="f-rooms"><option>3</option><option>4</option><option>5 ומעלה</option><option>פנטהאוז</option></select></div>\n        </div>',
    '</div>\n        <div class="row">\n          <div><label for="f-rooms">חדרים</label><select id="f-rooms"><option>3</option><option>4</option><option>5 ומעלה</option><option>פנטהאוז</option></select></div>')
body_inner = body_inner.replace(
    '<button class="btn btn-money" type="button">מצאו לי דירה באקו סיטי</button>',
    '<button class="btn btn-money" type="submit">מצאו לי דירה באקו סיטי</button>')
body_inner = body_inner.replace(
    '<p class="demo-note">שש שאלות קצרות, ונכוון אתכם לדירות שמתאימות באמת · טופס להדגמה בגרסת התצוגה הזו</p>',
    '<p class="demo-note" id="nl-echo-note">נחזור אליכם בשעות שבחרתם · בלי דואר זבל ובלי התחייבות</p>')

# 4. honesty: the full flight experience opens gradually
body_inner = body_inner.replace(
    '<p class="honest">ההדמיות והמודלים להמחשה בלבד · הנתונים מהפרסומים הרשמיים של אקו סיטי ומקורות ציבוריים</p>',
    '<p class="honest">חוויית הטיסה המלאה נפתחת בהדרגה לכל הבניינים · ההדמיות והמודלים להמחשה בלבד · הנתונים מהפרסומים הרשמיים של אקו סיטי ומקורות ציבוריים</p>')

# 5. lead JS
lead_js = """
<script>
(function(){"use strict";
var form=document.getElementById("nl-echo-lead");if(!form){return;}
var note=document.getElementById("nl-echo-note");
form.addEventListener("submit",function(e){
  e.preventDefault();
  var name=(document.getElementById("f-name")||{}).value||"";
  var phone=(document.getElementById("f-phone")||{}).value||"";
  var city=(document.getElementById("f-city")||{}).value||"";
  var rooms=(document.getElementById("f-rooms")||{}).value||"";
  var when=(document.getElementById("f-when")||{}).value||"";
  var digits=phone.replace(/\\D+/g,"");
  if(digits.length<9){note.textContent="כתבו מספר טלפון תקין ונחזור אליכם";note.style.color="#E4CE92";return;}
  if(!name.trim()){note.textContent="איך קוראים לכם? שדה השם ריק";note.style.color="#E4CE92";return;}
  var btn=form.querySelector("button[type=submit]");btn.disabled=true;btn.textContent="שולחים...";
  fetch("https://nad-lan.co.il/wp-json/nadlan/v1/lead",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
    source:"echo-city-page",goal:"echo-city",name:name.trim(),phone:phone,
    message:"אקו סיטי · עיר: "+city+" · חדרים: "+rooms+" · מועד שיחה: "+when
  })}).then(function(r){return r.ok?r.json().catch(function(){return{};}):Promise.reject(r.status);}).then(function(){
    form.innerHTML="<h3 style=\\"margin:0 0 8px\\">הבקשה התקבלה</h3><p style=\\"color:#B8B1A2;margin:0\\">נחזור אליכם ב"+when+" למספר "+phone+" עם דירות שמתאימות למה שביקשתם.</p>";
  }).catch(function(){
    btn.disabled=false;btn.textContent="מצאו לי דירה באקו סיטי";
    note.textContent="משהו השתבש בשליחה. נסו שוב או חייגו אלינו מהוואטסאפ באתר.";note.style.color="#E4CE92";
  });
});})();
</script>
"""

HEAD = """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>אקו סיטי תל אביב | 22 בניינים בשיווק, דירות וסיור תלת ממד | נדלן</title>
<meta name="description" content="כל 22 הבניינים של אקו סיטי בתל אביב ובגבעתיים במקום אחד: סטטוס בנייה ושיווק לכל כתובת, בחירת דירה על המודל, הנוף מהחלון וכלים לקנייה חכמה.">
<link rel="canonical" href="https://nad-lan.co.il/echo-city/">
<link rel="icon" type="image/svg+xml" href="https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/branding/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="נדלן">
<meta property="og:title" content="אקו סיטי תל אביב | 22 בניינים בשיווק, דירות וסיור תלת ממד">
<meta property="og:description" content="כל הבניינים של אקו סיטי בתל אביב ובגבעתיים: סטטוס, דירות, בחירת קומה על המודל והנוף מהחלון.">
<meta property="og:url" content="https://nad-lan.co.il/echo-city/">
<meta property="og:image" content="__OG_URL__">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":"https://nad-lan.co.il/echo-city/","url":"https://nad-lan.co.il/echo-city/","name":"אקו סיטי תל אביב | 22 בניינים בשיווק, דירות וסיור תלת ממד","inLanguage":"he-IL","description":"כל 22 הבניינים של אקו סיטי בתל אביב ובגבעתיים: סטטוס בנייה, דירות בשיווק וכלי בחירה."},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"בית","item":"https://nad-lan.co.il/"},{"@type":"ListItem","position":2,"name":"פרויקטים","item":"https://nad-lan.co.il/projects/"},{"@type":"ListItem","position":3,"name":"אקו סיטי"}]}]}</script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;500;700&family=Heebo:wght@400;500;600;700&display=swap">
</head>
<body>
"""

final = HEAD + body_inner + lead_js + "\n</body>\n</html>\n"
assert "—" not in final and "–" not in final, "dash law violated"
assert final.count("<h1") == 1
open(OUT, "w", encoding="utf-8").write(final)
print("written:", OUT, len(final), "chars | h1:", final.count("<h1"), "| img srcs:", final.count("plate-capsules.jpg"))
