# -*- coding: utf-8 -*-
"""HAD-543: the deck for the meeting with Avisror (19.10.2026), Ben + Meital Katsir.
python build_meeting.py [--pdf]  ->  meeting-deck.html (one self-contained file, arrows to move, works offline except fonts)
                                     meeting-deck.pdf  (16:9, one slide per page, the backup if the internet fails)
Design: NOT the old cream/gold kit (owner law 13.10.2026). Palette from the aeronautical chart of the old Sde Dov airfield
(cool chart paper, approach blue, VFR magenta, runway black); faces IBM Plex Sans Hebrew + IBM Plex Mono (instrument readouts,
an engineer's document: Meital is a civil and safety engineer). Facts only from the repo ledgers; no traffic numbers (owner rule)."""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "meital-kit-2026-10", "img")


def img(name):
    return "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(IMG, name), "rb").read()).decode()


CSS = """
:root{--chart:#EEF3F2;--chart2:#DDE7E5;--grid:#C5D4D1;--ink:#0E1B24;--ink2:#3B4C57;--mute:#6B7C86;
--blue:#0B5C8E;--blue2:#7FB3D5;--mag:#B3126F;--mag2:#F3D3E4;--night:#0E1B24;--night2:#16293A}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#0E1B24}
body{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",Arial,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.deck{position:relative;width:1600px;height:900px;margin:0 auto;overflow:hidden}
.slide{position:absolute;inset:0;padding:84px 96px;background:var(--chart);display:none;direction:rtl;
background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
background-size:80px 80px;background-position:-1px -1px}
.slide.on{display:block}
.slide.dark{background-color:var(--night);color:var(--chart);background-image:linear-gradient(#1D3346 1px,transparent 1px),linear-gradient(90deg,#1D3346 1px,transparent 1px)}
.kick{font-family:"IBM Plex Mono",monospace;font-size:19px;letter-spacing:.14em;color:var(--mag);text-transform:uppercase;margin-bottom:22px;direction:ltr;text-align:right}
.dark .kick{color:#F06BB0}
h1{font-size:76px;line-height:1.08;font-weight:700;letter-spacing:-.02em;max-width:1150px}
h2{font-size:54px;line-height:1.12;font-weight:700;letter-spacing:-.015em;max-width:1250px;margin-bottom:34px}
p.lead{font-size:28px;line-height:1.5;color:var(--ink2);max-width:1100px}
.dark p.lead{color:#B9CBD4}
.num{font-family:"IBM Plex Mono",monospace;font-weight:600}
.foot{position:absolute;bottom:34px;right:96px;left:96px;display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;font-size:15px;color:var(--mute);direction:rtl}
.dark .foot{color:#6E8797}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:20px}
.cols.c2{grid-template-columns:1fr 1fr}.cols.c4{grid-template-columns:repeat(4,1fr)}
.box{background:#fff;border:2px solid var(--ink);padding:30px 30px 34px;position:relative}
.dark .box{background:var(--night2);border-color:#3C5A70}
.box h3{font-size:30px;line-height:1.2;margin-bottom:14px}
.box p{font-size:22px;line-height:1.5;color:var(--ink2)}
.dark .box p{color:#B9CBD4}
.box .tag{position:absolute;top:-15px;right:24px;background:var(--mag);color:#fff;font-family:"IBM Plex Mono",monospace;font-size:15px;padding:3px 10px;letter-spacing:.08em}
.route{display:flex;gap:0;margin-top:40px;align-items:stretch}
.route .st{flex:1;border-top:6px solid var(--blue);padding:22px 14px 0 18px;position:relative}
.route .st:nth-child(odd){border-top-color:var(--ink)}
.route .st b{display:block;font-family:"IBM Plex Mono",monospace;color:var(--mag);font-size:20px;margin-bottom:10px}
.route .st span{font-size:24px;line-height:1.35;font-weight:600}
.route .st small{display:block;font-size:18px;color:var(--ink2);margin-top:8px;line-height:1.4}
.shot{border:2px solid var(--ink);box-shadow:14px 14px 0 var(--blue);display:block;width:100%;height:100%;object-fit:cover}
.split{display:grid;grid-template-columns:1.05fr 1fr;gap:64px;align-items:center;height:620px}
.list{list-style:none;margin-top:10px}
.list li{font-size:26px;line-height:1.45;padding:12px 44px 12px 0;position:relative;border-bottom:1px solid var(--grid)}
.dark .list li{border-color:#2A4356}
.list li:before{content:"";position:absolute;right:4px;top:24px;width:20px;height:20px;border:3px solid var(--mag);transform:rotate(45deg)}
.big{font-size:40px;line-height:1.3;font-weight:700;max-width:1200px;border-right:10px solid var(--mag);padding-right:30px;margin-top:40px}
.price{font-family:"IBM Plex Mono",monospace;font-size:48px;font-weight:600;color:var(--blue);direction:ltr;text-align:right;margin:8px 0 6px}
.price small{font-size:18px;color:var(--mute);font-family:"IBM Plex Sans Hebrew",sans-serif}
.cover h1 em{font-style:normal;color:#F06BB0}
.who{position:absolute;bottom:90px;right:96px;display:flex;gap:70px;font-size:22px;color:#B9CBD4}
.who b{display:block;font-size:30px;color:var(--chart);margin-bottom:4px}
.runway{position:absolute;left:96px;top:84px;width:420px;height:700px;border:2px solid #3C5A70;overflow:hidden}
.runway img{width:100%;height:100%;object-fit:cover;opacity:.92}
.nav{position:fixed;bottom:14px;left:14px;font-family:"IBM Plex Mono",monospace;font-size:13px;color:#6E8797;direction:ltr}
@media print{.slide{display:block;position:relative;page-break-after:always;break-after:page}.deck{height:auto}.nav{display:none}html,body{background:none}}
"""


def foot(i):
    return f'<div class="foot"><span>nad-lan.co.il · מיטל קציר, מתווכת מורשית 3131540</span><span class="num">{i:02d}</span></div>'


def slides():
    S = []
    S.append(f"""<section class="slide dark cover">
<div class="runway"><img src="{img('rainbow-hero.jpg')}" alt=""></div>
<div class="kick">nad-lan.co.il · 19.10.2026</div>
<h1>חדר ההחלטה<br>של הדירות החדשות<br><em>בתל אביב.</em></h1>
<p class="lead" style="margin-top:34px;max-width:860px">מיפוי תלת ממדי של פרויקטים חדשים, עם כל המידע על הסביבה, בחמש שפות. הקונה בוחר, מתרשם ומחליט, ומגיע אליכם מוכן.</p>
<div class="who"><div><b>בן</b>מייסד nad-lan.co.il</div><div><b>מיטל קציר</b>מתווכת מורשית · מהנדסת אזרחית ומהנדסת בטיחות</div></div>
</section>""")
    S.append(f"""<section class="slide">
<div class="kick">The shift</div>
<h2>בעולם, קונים כבר מחליטים אונליין.</h2>
<div class="cols">
<div class="box"><div class="tag">USA</div><h3>זילו</h3><p>הפכה סיור תלת ממד בדירה לחלק רגיל מהחיפוש. הקונה נכנס לבית לפני שהוא יוצא מהבית.</p></div>
<div class="box"><div class="tag">USA</div><h3>קומפס</h3><p>חיברה טכנולוגיה עם מתווכים אמיתיים. הפלטפורמה מביאה את הקונה, והאדם סוגר את העסקה.</p></div>
<div class="box"><div class="tag">UK</div><h3>רייטמוב</h3><p>יזמים בבריטניה משלמים בממוצע כ־<span class="num">2,135</span> ליש״ט לחודש כדי להציג פרויקטים חדשים (דוח שנתי 2025).</p></div>
</div>
<div class="big">בישראל עוד אין לפרויקט חדש חדר החלטה כזה. אנחנו בונים אותו.</div>
{foot(2)}</section>""")
    S.append(f"""<section class="slide">
<div class="kick">The buyer's route</div>
<h2>מה הקונה עושה אצלנו, צעד אחרי צעד.</h2>
<div class="route">
<div class="st"><b>01</b><span>בוחר בניין</span><small>על דגם תלת ממד של הפרויקט</small></div>
<div class="st"><b>02</b><span>קומה וכיוון</span><small>ים, עיר או פארק</small></div>
<div class="st"><b>03</b><span>הנוף מהקומה</span><small>מה רואים מהחלון</small></div>
<div class="st"><b>04</b><span>דירה לדוגמה</span><small>מסתובב בחדרים, בוחר סגנון</small></div>
<div class="st"><b>05</b><span>המתקנים</span><small>לובי, בריכה, חדר כושר</small></div>
<div class="st"><b>06</b><span>הסביבה</span><small>בתי ספר, ים, תחבורה, קניות, מחירים</small></div>
<div class="st"><b>07</b><span>פונה</span><small>וואטסאפ בלחיצה או שיחת וידאו</small></div>
</div>
<div class="cols c2" style="margin-top:44px;height:330px">
<img class="shot" style="height:330px" src="{img('rainbow-floor.jpg')}" alt=""><img class="shot" style="height:330px" src="{img('rainbow-map.jpg')}" alt="">
</div>
{foot(3)}</section>""")
    S.append(f"""<section class="slide dark">
<div class="kick">What we see</div>
<h2>זו לא סקרנות. זו כוונת קנייה.</h2>
<div class="split" style="height:560px">
<div><ul class="list">
<li>הגולשים בוחרים דירה, מסתכלים על הנוף ועל הסביבה, ורק אז מבקשים פרטים.</li>
<li>מי שפונה כבר יודע איזה בניין, איזו קומה ואיזה כיוון הוא רוצה.</li>
<li>השיחה הראשונה עם איש המכירות מתחילה באמצע ולא מאפס.</li>
</ul>
<p class="lead" style="margin-top:30px">בסרט המצורף: שחזור של מסע אמיתי של קונה, מהכניסה ועד הפנייה. בלי שום פרט אישי.</p></div>
<img class="shot" style="height:520px" src="{img('rainbow-fview.jpg')}" alt="">
</div>
{foot(4)}</section>""")
    S.append(f"""<section class="slide">
<div class="kick">Who comes</div>
<h2>קונים מחו״ל וקונים עם הכנסה גבוהה.</h2>
<div class="cols c2">
<div class="box"><h3>חמש שפות</h3><p>עברית, אנגלית, צרפתית, רוסית וערבית. לעמודי הפרויקטים בשדה דב מגיעים גולשים מארצות הברית, מבריטניה, מצרפת ומרוסיה.</p></div>
<div class="box"><h3>מה שקונה מחו״ל צריך</h3><p>לא רק דירה. הוא צריך להבין איך קונים בישראל: מס רכישה לתושב חוץ, משכנתא למי שאינו תושב, הצמדה למדד, טאבו. אנחנו מסבירים את זה בשפה שלו.</p></div>
<div class="box"><h3>משפחות</h3><p>בית ספר, גן, פארק וים, ובכמה דקות הליכה.</p></div>
<div class="box"><h3>משקיעים ומשפרי דיור</h3><p>שכירות, תשואה, וההבדל בין קומה לקומה ובין כיוון לכיוון.</p></div>
</div>
{foot(5)}</section>""")
    S.append(f"""<section class="slide dark">
<div class="kick">The people</div>
<h2>טכנולוגיה, ואיש מקצוע אמיתי לידה.</h2>
<div class="cols c2" style="margin-top:10px">
<div class="box"><div class="tag">BROKER · ENGINEER</div><h3>מיטל קציר · נדל״ן על הים</h3><p>מתווכת מורשית (רישיון <span class="num">3131540</span>). מהנדסת אזרחית (B.Tech) ומהנדסת בטיחות (B.Sc). פעילה מאוד בלמד החדשה, ברמת אביב, בכוכב הצפון, בנופי ים ובצוקי אביב. אליה מגיעות פניות של קונים עם פוטנציאל גבוה, גם לפרויקטים חדשים. כמהנדסת היא עונה בביטחון על שאלות של בנייה, מפרט ובטיחות, ומלווה את הקונה עד החתימה.</p></div>
<div class="box"><div class="tag">PLATFORM</div><h3>nad-lan.co.il</h3><p>פלטפורמה עצמאית: דגמי תלת ממד, מפת סביבה, חמש שפות, שיחת וידאו עם נציג, וואטסאפ בלחיצה בכל עמוד. משרד דיגיטלי למתווכת: הסכמים בחתימה דיגיטלית, רישום לקוחות עם הגנה ל־12 חודשים, וחומרים מוכנים לשליחה.</p></div>
</div>
<div class="big" style="color:var(--chart)">הפלטפורמה מביאה את הקונה מוכן. מיטל עונה על כל שאלה ומביאה אותו לחתימה.</div>
{foot(6)}</section>""")
    S.append(f"""<section class="slide">
<div class="kick">Speed</div>
<h2>תופסים את הקונה לפני שהוא עובר לפרויקט אחר.</h2>
<div class="route" style="margin-top:60px">
<div class="st"><b>00:00</b><span>הקונה פונה</span><small>מתוך הדירה שבחר</small></div>
<div class="st"><b>00:05</b><span>מענה מיידי</span><small>בשפה שלו, עם הדירה שבחר</small></div>
<div class="st"><b>00:10</b><span>מסתובב בפרויקט</span><small>קומה, נוף, מתקנים, סביבה</small></div>
<div class="st"><b>היום</b><span>שיחת וידאו</span><small>עם נציג, על אותה דירה</small></div>
<div class="st"><b>השבוע</b><span>פגישה אצלכם</span><small>במשרד המכירות</small></div>
</div>
<p class="lead" style="margin-top:70px">קונה שמתעניין היום ושומע תשובה רק מחר, כבר מסתכל על פרויקט אחר. אצלנו הוא מקבל חוויה מלאה של הפרויקט מהדקה הראשונה.</p>
{foot(7)}</section>""")
    S.append(f"""<section class="slide">
<div class="kick">What you get</div>
<h2>מה היזם מקבל.</h2>
<div class="cols">
<div class="box"><h3>חלון ראווה רשמי</h3><p>הנתונים שלכם: מחירון, תוכניות, הדמיות וסרט, מדויקים ומאושרים על ידכם.</p></div>
<div class="box"><h3>פניות מסודרות</h3><p>אם נסכם על כך בפיילוט: פניות מהעמוד יגיעו לצוות המכירות, עם מה שהקונה בדק.</p></div>
<div class="box"><h3>מרכז מפרסם וסטודיו</h3><p>אזור משלכם בפלטפורמה לעדכון פרטים ולהעלאת חומרים. בפיילוט נוסיף סיכום של מה הקונים שאלו.</p></div>
<div class="box"><h3>עולם שדה דב</h3><p>מדריכים וכלים על הרובע (מרחקים, עלויות, שכירות) בעברית ובאנגלית, שמביאים קונים שמחפשים את האזור.</p></div>
<div class="box"><h3>קונים מחו״ל</h3><p>חמש שפות, והקמפיינים בארץ ובחו״ל שאנחנו מתחילים עכשיו.</p></div>
<div class="box"><h3>מתווכת מהשכונה</h3><p>הקונים של מיטל, והליווי שלה עד החתימה, לפי הסכם התיווך שלה.</p></div>
</div>
{foot(8)}</section>""")
    S.append(f"""<section class="slide dark">
<div class="kick">With your materials</div>
<h2>עם החומרים שלכם, החוויה עולה לרמה אחרת.</h2>
<div class="split" style="height:560px">
<div><ul class="list">
<li>הדמיות של הדירות והדירה לדוגמה</li>
<li>תוכניות המתקנים: לובי, בריכה, ספא, חדר כושר</li>
<li>צילומים מהאתר: איך הבנייה עומדת היום</li>
<li>מחירון וזמינות, כפי שתבחרו לפרסם</li>
</ul>
<p class="lead" style="margin-top:28px">הקונה יחווה את המתקנים, את הדירה ואת הנוף לפני שהוא מחליט על פרויקט אחר.</p></div>
<img class="shot" style="height:520px" src="{img('rainbow-door.jpg')}" alt="">
</div>
{foot(9)}</section>""")
    S.append(f"""<section class="slide">
<div class="kick">The vision</div>
<h2>כל הפרויקטים החדשים בתל אביב, ואחר כך ישראל.</h2>
<div class="cols">
<div class="box"><div class="tag">NOW</div><h3>שדה דב וצפון תל אביב</h3><p>פרויקטי הדגל של הרובע כבר בתלת ממד, עם מפת סביבה ומחירים.</p></div>
<div class="box"><div class="tag">NEXT</div><h3>כל תל אביב</h3><p>כל פרויקט חדש בעיר, באותה רמה ובאותו מסע החלטה.</p></div>
<div class="box"><div class="tag">THEN</div><h3>ישראל</h3><p>הערים הגדולות, ומדף אחד לקונה מחו״ל.</p></div>
</div>
<div class="big">צמיחה אורגנית בגוגל כבר עכשיו, וקמפיינים בארץ ובחו״ל שמתחילים בקרוב.</div>
{foot(10)}</section>""")
    S.append(f"""<section class="slide">
<div class="kick">Ashira today</div>
<h2>כך אשירה נראית אצלנו היום.</h2>
<div class="split">
<div><p class="lead">בנינו את העמוד ממקורות ציבוריים ומהתוכניות המאושרות, בחמש שפות. עם הנתונים הרשמיים שלכם הוא יהיה העמוד הכי מדויק ברשת על אשירה, באישור שלכם.</p>
<p class="lead" style="margin-top:26px">קונה שרוצה את אשירה תמיד מגיע לאשירה. שיתוף פעולה רק הופך את הדרך לישירה ולמהירה.</p></div>
<img class="shot" style="height:560px" src="{img('ashira-hero.jpg')}" alt="">
</div>
{foot(11)}</section>""")
    S.append(f"""<section class="slide">
<div class="kick">Options</div>
<h2>שלושה מסלולים. בוחרים מה שמתאים לכם.</h2>
<div class="cols">
<div class="box"><h3>פיילוט</h3><div class="price">3,990 <small>₪ לחודש</small></div><p>שלושה חודשים. חלון ראווה עם הנתונים שלכם.</p></div>
<div class="box"><div class="tag">FOUNDERS</div><h3>חלון ראווה לשנה</h3><div class="price">2,490 <small>₪ לחודש</small></div><p>מחיר מייסדים במקום 3,990. הנתונים שלכם, סרט ומחירון.</p></div>
<div class="box"><h3>שותף שדה דב לשנה</h3><div class="price">6,900 <small>₪ לחודש</small></div><p>כל מה שבחלון הראווה, ועוד: עדיפות בפניות על הרובע, מקום ראשון במדריכים ובכלים של שדה דב, והקמפיינים לקונים מחו״ל.</p></div>
</div>
<div class="big">בכל מסלול שנתי: אחרי 90 יום אפשר לצאת בלי קנס. כל המחירים כוללים מע״מ.</div>
{foot(12)}</section>""")
    S.append(f"""<section class="slide dark">
<div class="kick">Next step</div>
<h2>הצעד הבא.</h2>
<div class="route" style="margin-top:50px">
<div class="st" style="border-color:var(--mag)"><b>01</b><span>בוחרים מסלול</span><small>היום, בחדר</small></div>
<div class="st" style="border-color:var(--blue2)"><b>02</b><span>שולחים לנו חומרים</span><small>מחירון, תוכניות, הדמיות</small></div>
<div class="st" style="border-color:var(--mag)"><b>03</b><span>חתימה דיגיטלית</span><small>מהטלפון, בקישור</small></div>
<div class="st" style="border-color:var(--blue2)"><b>04</b><span>מעדכנים את העמוד</span><small>תוך 14 יום מקבלת החומרים</small></div>
</div>
<div class="who" style="bottom:110px"><div><b>בן</b>nad-lan.co.il</div><div><b>מיטל קציר</b>052-363-1582 · נדל״ן על הים</div></div>
</section>""")
    return S


def build():
    S = slides()
    js = """<script>(function(){var s=[].slice.call(document.querySelectorAll('.slide')),i=0,n=document.querySelector('.nav');
function go(k){i=Math.max(0,Math.min(s.length-1,k));s.forEach(function(e,j){e.classList.toggle('on',j===i)});n.textContent=(i+1)+' / '+s.length+'  ·  ← →';fit()}
function fit(){var d=document.querySelector('.deck'),z=Math.min(innerWidth/1600,innerHeight/900);d.style.transform='scale('+z+')';d.style.transformOrigin='top center'}
addEventListener('keydown',function(e){if(e.key==='ArrowLeft'||e.key===' '||e.key==='PageDown')go(i+1);if(e.key==='ArrowRight'||e.key==='PageUp')go(i-1);if(e.key==='f')document.documentElement.requestFullscreen()});
addEventListener('click',function(e){go(e.clientX<innerWidth/2?i+1:i-1)});addEventListener('resize',fit);go(0)})();</script>"""
    html = ("<!doctype html><html lang='he' dir='rtl'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>nad-lan.co.il · חדר ההחלטה · 19.10.2026</title>"
            "<link rel='preconnect' href='https://fonts.googleapis.com'><link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&display=swap' rel='stylesheet'>"
            f"<style>{CSS}</style></head><body><div class='deck'>{''.join(S)}</div><div class='nav'></div>{js}</body></html>")
    out = os.path.join(HERE, "meeting-deck.html")
    open(out, "w", encoding="utf-8").write(html)
    print("html", out, len(html))
    if "--pdf" in sys.argv:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            pg = b.new_page(viewport={"width": 1600, "height": 900})
            pg.goto("file:///" + out.replace("\\", "/"))
            pg.wait_for_timeout(2500)
            pg.emulate_media(media="print")
            pdf = os.path.join(HERE, "meeting-deck.pdf")
            pg.pdf(path=pdf, width="1600px", height="900px", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            for k in (1, 3, 8, 12):
                pg.emulate_media(media="screen")
                pg.evaluate(f"document.querySelectorAll('.slide').forEach(function(e,j){{e.classList.toggle('on',j==={k - 1})}});document.querySelector('.deck').style.transform='none'")
                pg.screenshot(path=os.path.join(HERE, f"deck-shot-{k:02d}.png"))
            b.close()
        print("pdf", pdf, os.path.getsize(pdf))


if __name__ == "__main__":
    build()
