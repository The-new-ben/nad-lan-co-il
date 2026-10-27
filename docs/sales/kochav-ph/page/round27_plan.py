# -*- coding: utf-8 -*-
"""Kochav listing, round 27.10.2026, part two: the architect's plan on the page (Ben: "ויזואליזציה... גבוה בדף, אבל שלא יפעיל על
התמונות ולא יפעיל על הוידאו"; Meital: no measurable areas). Built on the CURRENT live text (live-27-<id>.html, read by
live_io.py --fetch after round27.py went live), Hebrew and English.
- A plan section right under the film, before the long photo gallery (the opening carousel already shows the photos first): the luxury 2D plan traced from the PDF
  (plan/svg, zero digits), a toggle to the rendering of the plan (plan/web/img/dollhouse.jpg, uploaded to the media library), a
  tap on a room highlights it and shows Meital's own photo of it when one exists (the site's copies of her photos), pinch and
  double tap to zoom, no wheel capture (the page scrolls through it). Caption: "הדמיה על פי תוכנית האדריכל", no dimensions.
- The room the plan leaves unnamed behind the main bedroom is called what it is ("a room in the main suite"), not a closet.
- One line of quick links in the opening: the film, the plan, the location (the research: a plan one tap from the first screen
  is the gap; 3 of 13 top pages, 0 Israeli).
  python round27_plan.py <render-url>  -> after-27-7634.html, after-27-7812.html; then live_io.py --apply after-27-7634.html after-27-7812.html
  (round27.py also writes after-27-*.html: do not run it again after this; its base is the text before round 27)"""
import io, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); PLAN = os.path.join(os.path.dirname(H), "plan")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
RENDER = sys.argv[1] if len(sys.argv) > 1 else json.load(open(os.path.join(H, "media.json")))["kochav-mini-penthouse-plan-render.jpg"]["url"]
U = "https://nad-lan.co.il/wp-content/uploads/2026/09/"
PHOTOS = {"living": "L07_DX9wx4ziADM_02", "dining": "L07_DZp43r5DIou_04", "kitchen": "L07_DZp43r5DIou_01",
          "terrace": "L07_DX9wx4ziADM_03", "bath": "L07_DX9wx4ziADM_05"}  # matched to plan/web/img/real-*.jpg by pixels (27.10)
ORDER = ["living", "dining", "kitchen", "terrace", "entry", "corridor", "wc", "room_a", "bed1", "bed2", "bed3", "closet",
         "ensuite", "bath", "laundry", "balcony", "service", "ledge"]
L = {
 "he": dict(pid=7634, sfx="L07-he", svg="plan-lux.svg", closet=("חדר ארונות", "חדר בסוויטת ההורים"), chip={"bed1": "חדר שינה א׳", "bed3": "חדר שינה ב׳", "closet": "חדר בסוויטה"},
    eyebrow="תוכנית הדירה", h2="חמישה חדרים, מרחב פתוח אחד ומרפסת גג",
    lead="סלון, פינת אוכל ומטבח עם אי ארוך במרחב אחד שנפתח אל מרפסת הגג ואל הפרגולות, ואגף שינה נפרד עם סוויטת הורים. בחרו חדר וראו אותו מסומן בתוכנית, ובחדרים שצולמו גם את הצילום מהדירה.",
    seg="תצוגת התוכנית", b2d="תוכנית", b3d="הדמיה", stage="תוכנית הדירה. בחרו חדר מהרשימה או בתוכנית. פלוס ומינוס להגדלה.",
    svg_label="מיני פנטהאוז בכוכב הצפון, הדמיה על פי תוכנית האדריכל", alt3d="הדמיית הדירה מלמעלה, חתך בגובה המותניים, על פי תוכנית האדריכל",
    badge="הדמיה על פי תוכנית האדריכל", hint="בחרו חדר בתוכנית או ברשימה · שתי אצבעות או הקשה כפולה להגדלה",
    zoom=("הגדלה", "הקטנה", "חזרה לתצוגה המלאה", "הגדלה"), chips="חדרי הדירה",
    photo_cap="צילום מהדירה", no_photo="החדר מסומן בתוכנית. הצילומים מהדירה בגלריה למעלה.",
    foot="הדמיה על פי תוכנית האדריכל, להמחשה בלבד וללא מידות. הריהוט כפי ששורטט בתוכנית, והמיטות להמחשה.",
    wa_lab="שאלה על התוכנית? כתבו למיטל",
    jump=[("film", "הסרטון"), ("plan", "תוכנית הדירה"), ("location", "המיקום")], jump_lab="מעבר מהיר"),
 "en": dict(pid=7812, sfx="L07-en", svg="plan-lux-en.svg", closet=("Walk-in closet", "Main suite room"), chip={"bed1": "Bedroom A", "bed3": "Bedroom B"},
    eyebrow="Floor plan", h2="Five rooms, one open space and a roof terrace",
    lead="Living, dining and a kitchen with a long island in one open space that opens onto the roof terrace and its pergolas, and a separate sleeping wing with a main suite. Pick a room to see it marked on the plan, and for the rooms that were photographed, its photo from the home.",
    seg="Plan view", b2d="Plan", b3d="Rendering", stage="The floor plan. Pick a room from the list or on the plan. Plus and minus to zoom.",
    svg_label="Mini penthouse in Kochav HaTzafon, rendered from the architect's plan", alt3d="The home seen from above, cut at waist height, rendered from the architect's plan",
    badge="Rendered from the architect's plan", hint="Pick a room on the plan or in the list · two fingers or a double tap to zoom",
    zoom=("Zoom in", "Zoom out", "Back to the full view", "Zoom"), chips="Rooms of the home",
    photo_cap="Photo from the home", no_photo="The room is marked on the plan. The photos from the home are in the gallery above.",
    foot="Rendered from the architect's plan, for illustration only, without dimensions. Furniture as drawn on the plan; the beds are illustrative.",
    wa_lab="A question about the plan? Message Meital",
    jump=[("film", "The film"), ("plan", "Floor plan"), ("location", "Location")], jump_lab="Quick links"),
}


def svg_for(c):
    s = io.open(os.path.join(PLAN, "svg", c["svg"]), encoding="utf-8").read()
    s = re.sub(r'<g id="title".*?</g>', "", s, flags=re.S)
    s = re.sub(r'<g id="legend".*?</g>\s*(?=</svg>)', "", s, flags=re.S)
    s = re.sub(r"<style>.*?</style>", "", s, flags=re.S)  # its rules are generic (.serif, .room); the section CSS carries them, scoped
    s = re.sub(r'<svg ([^>]*?)viewBox="[^"]*" width="\d+" height="\d+"', r'<svg \1viewBox="170 10 3860 3900" preserveAspectRatio="xMidYMid meet" class="np-svg" focusable="false"', s, count=1)
    s = re.sub(r'aria-label="[^"]*"', 'aria-label="%s"' % c["svg_label"], s, count=1)
    s = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % c["svg_label"], s, count=1)
    s = re.sub(r'\bid="(?!room-)', 'id="np-', s)  # pattern and filter ids: unique on the page
    s = re.sub(r"url\(#", "url(#np-", s)
    n = s.count(c["closet"][0]); assert n >= 2, ("closet label", n)
    s = s.replace(c["closet"][0], c["closet"][1])
    s = re.sub(r">\s+<", "><", s.replace("\r\n", "\n"))
    assert not re.search(r">[^<]*\d[^<]*<", re.sub(r"<(title|desc)>.*?</\1>", "", s)), "a digit in the plan's visible text"
    return s


CSS = ('<style>\n'
       '.nlx .np{--np-ink:var(--nlx-ink,#14212B);--np-deep:var(--nlx-deep,#1F4B5C);--np-sea:var(--nlx-sea,#2F6F86);--np-line:var(--nlx-line,#E3E1DA);--np-mute:var(--nlx-mute,#5F7785);--np-surf:#F4F7F8}\n'
       '.nlx .np-bar{display:flex;justify-content:flex-start;margin:0 0 12px}\n'
       '.nlx .np-seg{display:inline-flex;border:1px solid var(--np-line);border-radius:999px;padding:3px;background:#fff}\n'
       'html body .nlx .np-seg button{min-height:44px;min-width:104px;padding:0 18px;border:0;border-radius:999px;background:transparent;color:var(--np-ink);font:700 16px/1 var(--nlx-sans);cursor:pointer;box-shadow:none}\n'
       'html body .nlx .np-seg button[aria-pressed="true"]{background:var(--np-ink);color:#fff}\n'
       '.nlx .np{container-type:inline-size}\n'
       '.nlx .np-body{display:grid;grid-template-columns:minmax(0,1fr);gap:14px}.nlx .np-body>*{min-width:0}\n'
       '.nlx .np-stage{position:relative;overflow:hidden;border:1px solid var(--np-line);border-radius:16px;background:#fff;aspect-ratio:1/1;max-height:min(680px,82vh);touch-action:pan-y;user-select:none;-webkit-user-select:none;outline:none}\n'
       '/* the page column is about 715px on a desktop: the plan takes the full width, the room card sits under it with the photo beside the name */\n'
       '@container (min-width:600px){.nlx .np-panel{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:18px;align-items:start}'
       '.nlx .np-panel>h3{grid-column:1}.nlx .np-panel>*:not(h3){grid-column:2;grid-row:1/span 2;margin-top:0}}\n'
       '.nlx .np-stage.is3d{aspect-ratio:3/2;background:#E6EBEE}.nlx .np-stage:focus-visible{box-shadow:0 0 0 3px var(--np-sea)}\n'
       '.nlx .np-canvas{position:absolute;inset:0;transform-origin:0 0;will-change:transform}\n'
       '.nlx .np .np-svg{width:100%;height:100%;display:block;max-width:none}\n'
       '.nlx .np-3d{position:absolute;inset:0;display:none}\n'
       'html body .nlx .np .np-3d img{width:100%;height:100%;max-width:none;object-fit:contain;display:block;pointer-events:none;-webkit-user-drag:none;border-radius:0;box-shadow:none;margin:0}\n'
       '.nlx .is3d .np-3d{display:block}.nlx .is3d .np-svg{display:none}\n'
       '.nlx .np-svg .serif{font-family:var(--nlx-serif)}.nlx .np-svg .sans{font-family:var(--nlx-sans)}\n'
       '.nlx .np-svg .lbl{paint-order:stroke;stroke:#fff;stroke-width:14px;stroke-linejoin:round;fill:#14212B}\n'
       '.nlx .np-svg .room{cursor:pointer;outline:none}\n'
       '.nlx .np-svg .room .hl{fill:#2F6F86;fill-opacity:0;stroke:#1F4B5C;stroke-opacity:0;stroke-width:10;transition:fill-opacity .2s,stroke-opacity .2s}\n'
       '.nlx .np-svg .room:hover .hl{fill-opacity:.07}.nlx .np-svg .room:focus-visible .hl{stroke-opacity:.6}\n'
       '.nlx .np-svg .room.active .hl{fill-opacity:.16;stroke-opacity:.9}.nlx .np-svg .room.active .lbl{fill:#1F4B5C}\n'
       '.nlx .np-tag{position:absolute;transform:translate(-50%,-120%);padding:6px 12px;border-radius:999px;background:var(--np-ink);color:#fff;font:700 15px/1.2 var(--nlx-sans);white-space:nowrap;pointer-events:none;box-shadow:0 6px 18px rgba(20,33,43,.25);display:none}\n'
       '.nlx .np-tag::after{content:"";position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);border:6px solid transparent;border-bottom:0;border-top-color:var(--np-ink)}\n'
       '.nlx .np-tag.on{display:block}\n'
       '/* the caption sits in the empty top-left corner of the drawing (and of the rendering), in both languages: physical sides on purpose */\n'
       'html body .nlx .np p.np-badge{position:absolute;top:10px;left:10px;margin:0;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.94);border:1px solid var(--np-line);color:var(--np-deep);font:700 13px/1.2 var(--nlx-sans);pointer-events:none;max-width:none}\n'
       '.nlx .np-tools{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:8px}\n'
       '.nlx .np-zoom{display:flex;gap:6px;flex:0 0 auto}\n'
       'html body .nlx .np-zoom button{width:44px;height:44px;border-radius:12px;border:1px solid var(--np-line);background:#fff;color:var(--np-ink);font:700 22px/1 var(--nlx-sans);cursor:pointer;box-shadow:0 2px 10px rgba(20,33,43,.10);padding:0}\n'
       'html body .nlx .np button:focus-visible{outline:3px solid var(--np-sea);outline-offset:2px}\n'
       'html body .nlx .np p.np-hint{margin:0 2px;font:500 14px/1.35 var(--nlx-sans);color:var(--np-mute);max-width:none}\n'
       '.nlx .np-chips{display:flex;gap:8px;overflow-x:auto;padding:10px 2px 6px;scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch;scrollbar-width:thin}\n'
       'html body .nlx .np-chips button{flex:0 0 auto;scroll-snap-align:start;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid var(--np-line);background:#fff;color:var(--np-ink);font:700 15px/1 var(--nlx-sans);cursor:pointer;box-shadow:none}\n'
       'html body .nlx .np-chips button[aria-pressed="true"]{background:var(--np-deep);border-color:var(--np-deep);color:#fff}\n'
       '@media (min-width:900px){.nlx .np-chips{flex-wrap:wrap;overflow:visible}}\n'
       '.nlx .np-panel{border:1px solid var(--np-line);border-radius:16px;padding:16px;background:var(--np-surf);min-height:120px}\n'
       'html body .nlx .np .np-panel h3{margin:0 0 6px!important;font-family:var(--nlx-serif)!important;font-weight:600!important;font-size:24px!important;line-height:1.25!important;color:var(--np-ink)!important}\n'
       'html body .nlx .np .np-panel p{margin:0;color:var(--np-mute);font:500 15px/1.5 var(--nlx-sans);max-width:none}\n'
       '.nlx .np-panel figure{margin:12px 0 0}\n'
       'html body .nlx .np .np-panel img{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;border-radius:12px;display:block;background:#DFE5E8;margin:0;box-shadow:none}\n'
       'html body .nlx .np .np-panel figcaption{margin-top:6px;font:500 13px/1.3 var(--nlx-sans);color:var(--np-mute);text-align:start}\n'
       '.nlx .np-end{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 16px;margin-top:12px}\n'
       'html body .nlx .np p.np-foot{margin:0;font:400 12.5px/1.55 var(--nlx-sans);color:var(--np-mute);max-width:62ch}\n'
       'html body .nlx .np a.np-wa{display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:10px 16px;border-radius:12px;border:1.5px solid var(--np-deep);background:#fff;color:var(--np-deep)!important;font:700 15px/1.2 var(--nlx-sans);text-decoration:none!important}\n'
       '.nlx .np a.np-wa svg{width:19px;height:19px;flex:0 0 auto}\n'
       '/* phones: the drawing is about 0.09 of its size, so the main room names grow to about 8 to 12px and the names of the small rooms\n'
       '   show only for the room that is picked (the chips name every room); checked on the live page at 390px, 27.10 */\n'
       '@container (max-width:520px){html body .nlx .np-svg text[data-for]{font-size:84px}html body .nlx .np-svg text[data-for=living]{font-size:130px}'
       'html body .nlx .np-svg text[data-for=kitchen],html body .nlx .np-svg text[data-for=terrace]{font-size:118px}html body .nlx .np-svg text[data-for=dining]{font-size:96px}'
       'html body .nlx .np-svg[lang=en] text[data-for=living]{font-size:112px}html body .nlx .np-svg[lang=en] text[data-for=terrace]{font-size:86px}'
       'html body .nlx .np-svg text:is([data-for=corridor],[data-for=wc],[data-for=closet],[data-for=ensuite],[data-for=bath],[data-for=laundry],[data-for=ledge],[data-for=balcony],[data-for=service]){visibility:hidden}'
       'html body .nlx .np-svg text[data-for].on{visibility:visible}'
       'html body .nlx .np p.np-badge{font-size:11.5px;padding:4px 9px}}\n'
       '@media (prefers-reduced-motion:reduce){.nlx .np-svg .room .hl{transition:none}}\n'
       '</style>\n')

JUMP_CSS = ('<style>.nlx .nlx-h27-jump{display:flex;flex-wrap:wrap;gap:8px;margin:2px 0 0}'
            'html body .nlx .nlx-h27-jump a{display:inline-flex;align-items:center;min-height:40px;padding:8px 14px;border-radius:999px;border:1px solid var(--nlx-line);'
            'background:var(--nlx-surf);color:var(--nlx-deep)!important;font:700 14px/1.2 var(--nlx-sans);text-decoration:none!important}'
            'html body .nlx .nlx-h27-jump a:hover{border-color:var(--nlx-deep)}</style>')

JS = r"""<script>(function(){var root=document.getElementById("plan-__SFX__");if(!root||root.__np)return;root.__np=1;
var ROOMS=__ROOMS__,T=__T__,byId={};ROOMS.forEach(function(r){byId[r.id]=r});
var stage=root.querySelector(".np-stage"),canvas=root.querySelector(".np-canvas"),tag=root.querySelector(".np-tag"),panel=root.querySelector(".np-panel"),chips=root.querySelector(".np-chips"),svg=canvas.querySelector("svg"),mode="2d",current=null,AR=1.5;
ROOMS.forEach(function(r){var b=document.createElement("button");b.type="button";b.textContent=r.chip;b.setAttribute("aria-pressed","false");b.dataset.room=r.id;b.addEventListener("click",function(){select(r.id,true)});chips.appendChild(b)});
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function select(id,fromList){var r=byId[id];if(!r)return;current=id;
svg.querySelectorAll(".room").forEach(function(g){g.classList.toggle("active",g.dataset.room===id)});svg.querySelectorAll("text[data-for]").forEach(function(x){x.classList.toggle("on",x.getAttribute("data-for")===id)});
chips.querySelectorAll("button").forEach(function(c){c.setAttribute("aria-pressed",c.dataset.room===id?"true":"false")});
var h="<h3>"+esc(r.name)+"</h3>";if(r.photo)h+='<figure><img src="'+r.photo+'" alt="'+esc(r.name)+'" width="768" height="768" loading="lazy" decoding="async"><figcaption>'+T.cap+"</figcaption></figure>";else h+="<p>"+T.none+"</p>";
panel.innerHTML=h;placeTag();if(fromList){var c=chips.querySelector('[data-room="'+id+'"]');if(c){var cr=c.getBoundingClientRect(),pr=chips.getBoundingClientRect();if(cr.left<pr.left||cr.right>pr.right)chips.scrollBy({left:(cr.left+cr.right-pr.left-pr.right)/2,behavior:"auto"})}}}
function box(){var W=canvas.clientWidth,H=canvas.clientHeight,iw=W,ih=W/AR;if(ih>H){ih=H;iw=H*AR}return[W,H,iw,ih,(W-iw)/2,(H-ih)/2]}
function placeTag(){var r=current&&byId[current];if(mode!=="3d"||!r||!r.hs){tag.classList.remove("on");return}var b=box();tag.textContent=r.name;tag.classList.add("on");
var w=tag.offsetWidth,h=tag.offsetHeight,x=b[4]+r.hs[0]*b[2],y=b[5]+r.hs[1]*b[3];tag.style.left=Math.max(w/2+6,Math.min(b[0]-w/2-6,x))+"px";tag.style.top=Math.max(h*1.2+6,y)+"px"}
root.querySelectorAll(".np-seg button").forEach(function(b){b.addEventListener("click",function(){mode=b.dataset.mode;root.querySelectorAll(".np-seg button").forEach(function(x){x.setAttribute("aria-pressed",x===b?"true":"false")});stage.classList.toggle("is3d",mode==="3d");reset();placeTag()})});
var s=1,tx=0,ty=0,MAX=4;
function clamp(){var w=stage.clientWidth,h=stage.clientHeight;tx=Math.min(0,Math.max(w-w*s,tx));ty=Math.min(0,Math.max(h-h*s,ty))}
function apply(){clamp();canvas.style.transform="translate("+tx+"px,"+ty+"px) scale("+s+")"}
function zoomAt(px,py,ns){ns=Math.max(1,Math.min(MAX,ns));tx=px-(px-tx)*(ns/s);ty=py-(py-ty)*(ns/s);s=ns;apply()}
function reset(){s=1;tx=0;ty=0;apply()}
function center(){return[stage.clientWidth/2,stage.clientHeight/2]}
root.querySelectorAll(".np-zoom button").forEach(function(b){b.addEventListener("click",function(){var c=center();if(b.dataset.z==="in")zoomAt(c[0],c[1],s*1.5);else if(b.dataset.z==="out")zoomAt(c[0],c[1],s/1.5);else reset()})});
stage.addEventListener("wheel",function(e){if(!e.ctrlKey)return;e.preventDefault();var r=stage.getBoundingClientRect();zoomAt(e.clientX-r.left,e.clientY-r.top,s*Math.exp(-e.deltaY*.01))},{passive:false});
stage.addEventListener("keydown",function(e){var c=center();if(e.key==="+"||e.key==="="){zoomAt(c[0],c[1],s*1.5);e.preventDefault()}else if(e.key==="-"){zoomAt(c[0],c[1],s/1.5);e.preventDefault()}else if(e.key==="0"||e.key==="Escape"){reset()}else if(s>1&&/^Arrow/.test(e.key)){var d=40;if(e.key==="ArrowLeft")tx+=d;if(e.key==="ArrowRight")tx-=d;if(e.key==="ArrowUp")ty+=d;if(e.key==="ArrowDown")ty-=d;apply();e.preventDefault()}});
svg.querySelectorAll(".room").forEach(function(g){g.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();select(g.dataset.room)}})});
svg.addEventListener("click",function(e){if(e.detail!==0)return;var g=e.target.closest&&e.target.closest(".room");if(g)select(g.dataset.room)});/* screen readers: their activation is a click with no pointer */
/* gestures (Codex review 27.10, page/codex-review-plan-27.txt): touch-action stays pan-y at every zoom, so one finger moving up or down
   always scrolls the page (Ben: a page never sticks); one finger sideways pans a zoomed plan, two fingers zoom and move it */
var P=new Map(),pinch=null,down=null,lastTap=null;
function startPinch(){var ids=Array.from(P.keys()).slice(0,2),a=ids.map(function(k){return P.get(k)}),r=stage.getBoundingClientRect();
pinch={ids:ids,d:Math.max(1,Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y)),s:s,tx:tx,ty:ty,mx:(a[0].x+a[1].x)/2-r.left,my:(a[0].y+a[1].y)/2-r.top};down=null;lastTap=null}
stage.addEventListener("pointerdown",function(e){if(e.pointerType==="mouse"&&e.button!==0)return;P.set(e.pointerId,{x:e.clientX,y:e.clientY});
if(e.pointerType==="mouse"){try{stage.setPointerCapture(e.pointerId)}catch(_){}}
if(P.size===2)startPinch();else if(P.size>2){pinch=null;down=null;lastTap=null}else{down={x:e.clientX,y:e.clientY,t:Date.now(),moved:false,lx:e.clientX,ly:e.clientY}}});
stage.addEventListener("pointermove",function(e){if(!P.has(e.pointerId))return;if(e.pointerType==="mouse"&&e.buttons===0){P.delete(e.pointerId);down=null;return}
P.set(e.pointerId,{x:e.clientX,y:e.clientY});
if(pinch){if(P.size!==2||pinch.ids.indexOf(e.pointerId)<0)return;var a=pinch.ids.map(function(k){return P.get(k)});if(!a[0]||!a[1])return;
var r=stage.getBoundingClientRect(),d=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y),ns=Math.max(1,Math.min(MAX,pinch.s*d/pinch.d)),mx=(a[0].x+a[1].x)/2-r.left,my=(a[0].y+a[1].y)/2-r.top;
s=ns;tx=mx-(pinch.mx-pinch.tx)*(ns/pinch.s);ty=my-(pinch.my-pinch.ty)*(ns/pinch.s);apply();return}
if(down){var dx=e.clientX-down.lx,dy=e.clientY-down.ly;if(Math.hypot(e.clientX-down.x,e.clientY-down.y)>8){down.moved=true;lastTap=null}if(s>1.001&&down.moved){tx+=dx;ty+=dy;apply()}down.lx=e.clientX;down.ly=e.clientY}});
function end(e){if(!P.has(e.pointerId))return;var wasTap=e.type==="pointerup"&&down&&!down.moved&&(Date.now()-down.t)<400&&P.size===1;P.delete(e.pointerId);
if(pinch&&pinch.ids.indexOf(e.pointerId)>=0){pinch=null;if(P.size===1){var q=P.values().next().value;down={x:q.x,y:q.y,t:0,moved:true,lx:q.x,ly:q.y}}return}/* the finger left after a pinch pans, it never taps */
if(e.type!=="pointerup"){down=null;lastTap=null;return}
if(!wasTap){if(!P.size)down=null;return}
var r=stage.getBoundingClientRect(),px=e.clientX-r.left,py=e.clientY-r.top,now=Date.now();
if(lastTap&&now-lastTap.t<320&&Math.hypot(px-lastTap.x,py-lastTap.y)<30){if(s>1.001)reset();else zoomAt(px,py,2.4);lastTap=null}else{lastTap={t:now,x:px,y:py};tapSelect(e.clientX,e.clientY,px,py)}down=null}
stage.addEventListener("pointerup",end);stage.addEventListener("pointercancel",end);stage.addEventListener("lostpointercapture",end);
function tapSelect(cx,cy,px,py){if(mode==="2d"){/* a tap on a room's name picks that room: in the open space the kitchen's name sits on the line to the living room */
var hit=null;svg.querySelectorAll("text[data-for]").forEach(function(x){if(hit||getComputedStyle(x).visibility==="hidden")return;var q=x.getBoundingClientRect();if(cx>=q.left-6&&cx<=q.right+6&&cy>=q.top-6&&cy<=q.bottom+6)hit=x.getAttribute("data-for")});
if(hit){select(hit);return}var el=document.elementFromPoint(cx,cy),g=el&&el.closest&&el.closest(".room");if(g)select(g.dataset.room);return}
var b=box(),ux=(px-tx)/s,uy=(py-ty)/s,best=null,bd=1e9;ROOMS.forEach(function(r){if(!r.hs)return;var d=Math.hypot(b[4]+r.hs[0]*b[2]-ux,b[5]+r.hs[1]*b[3]-uy);if(d<bd){bd=d;best=r}});if(best&&bd<Math.max(60,b[2]*.09))select(best.id)}
window.addEventListener("resize",function(){apply();placeTag()});apply();select("living");
})();</script>"""


def section(c, wa):
    plan = json.load(open(os.path.join(PLAN, "trace", "plan.json"), encoding="utf-8"))
    hs = json.load(open(os.path.join(PLAN, "renders", "dollhouse-hotspots.json"), encoding="utf-8"))
    assert hs["size"] == [2400, 1600]
    key = "he" if c["sfx"].endswith("he") else "en"
    names = {r["id"]: r[key] for r in plan["rooms"]}; names["closet"] = c["closet"][1]
    rooms = [{"id": i, "name": names[i], "chip": c["chip"].get(i, names[i]),
              "photo": (U + PHOTOS[i] + "-768x768.jpg") if i in PHOTOS else None, "hs": hs["rooms"].get(i)} for i in ORDER]
    js = (JS.replace("__SFX__", c["sfx"]).replace("__ROOMS__", json.dumps(rooms, ensure_ascii=False))
          .replace("__T__", json.dumps({"cap": c["photo_cap"], "none": c["no_photo"]}, ensure_ascii=False)))
    z = c["zoom"]
    wa_svg = re.search(r'<svg viewBox="0 0 24 24".*?</svg>', io.open(os.path.join(H, "round27.py"), encoding="utf-8").read(), re.S).group(0)
    return ('<section class="nlx-sec" id="plan-%s">\n' % c["sfx"] + CSS +
            '<div class="nlx-sec-head"><p class="nlx-eyebrow">%s</p><h2 class="nlx-h2">%s</h2><p class="nlx-lead">%s</p></div>\n' % (c["eyebrow"], c["h2"], c["lead"]) +
            '<div class="np">\n<div class="np-bar"><div class="np-seg" role="group" aria-label="%s"><button type="button" data-mode="2d" aria-pressed="true">%s</button>'
            '<button type="button" data-mode="3d" aria-pressed="false">%s</button></div></div>\n' % (c["seg"], c["b2d"], c["b3d"]) +
            '<div class="np-body"><div>\n<div class="np-stage" tabindex="0" role="application" aria-roledescription="%s" aria-label="%s"><div class="np-canvas">'
            % (c["eyebrow"], c["stage"]) + svg_for(c) +
            '<div class="np-3d"><img src="%s" alt="%s" width="1536" height="1024" loading="lazy" decoding="async"></div><div class="np-tag" aria-hidden="true"></div></div>'
            '<p class="np-badge">%s</p></div>\n' % (RENDER, c["alt3d"], c["badge"]) +
            '<div class="np-tools"><p class="np-hint">%s</p><div class="np-zoom" role="group" aria-label="%s"><button type="button" data-z="in" aria-label="%s">+</button>'
            '<button type="button" data-z="out" aria-label="%s">&minus;</button><button type="button" data-z="reset" aria-label="%s">&#10530;</button></div></div>\n'
            % (c["hint"], z[3], z[0], z[1], z[2]) +
            '<div class="np-chips" role="group" aria-label="%s"></div>\n</div>\n<div class="np-panel" aria-live="polite"></div>\n</div>\n' % c["chips"] +
            '<div class="np-end"><p class="np-foot">%s</p><a class="np-wa" href="%s" rel="noopener" target="_blank">%s<span>%s</span></a></div>\n</div>\n'
            % (c["foot"], wa, wa_svg, c["wa_lab"]) + js + "\n</section>\n")


def rep1(t, a, b, label):
    n = t.count(a); assert n >= 1, (label, n, a[:60])
    return t.replace(a, b)


# the film v3 files in the media library (upload_media.py records them in media.json); the swap runs once all three are there
_M = json.load(open(os.path.join(H, "media.json"))) if os.path.exists(os.path.join(H, "media.json")) else {}
FILM = None
if all(k in _M for k in ("kochav-film-en-v3.mp4", "kochav-film-en-v3-he.mp4", "kochav-film-v3.jpg")):
    _p = lambda k: _M[k]["url"].rsplit("/", 1)[1]
    FILM = {"he": {"mp4": _p("kochav-film-en-v3-he.mp4"), "jpg": _p("kochav-film-v3.jpg")},
            "en": {"mp4": _p("kochav-film-en-v3.mp4"), "jpg": _p("kochav-film-v3.jpg")}}
    assert all(_M[k]["url"].startswith("https://nad-lan.co.il/wp-content/uploads/2026/10/") for k in ("kochav-film-en-v3.mp4", "kochav-film-en-v3-he.mp4", "kochav-film-v3.jpg"))
L["he"].update(
    film_lead=("בוקר בשכונה, קפה במרכז המסחרי, הגשר החדש לפארק הירקון, הבית עצמו, ערב עם חברים במרפסת, והמספרים של האזור. באנגלית, עם כתוביות.",
               "בוקר בשכונה, קפה במרכז המסחרי, הגשר החדש לפארק הירקון, מגרשי הטניס והכדורגל ליד הבית, הבית החדש עצמו, ערב במרפסת, והמספרים של האזור. קריינות באנגלית, עם כתוביות בעברית."),
    film_note=("הבית צולם בדירה עצמה. הגשר, השכונה מלמעלה ותמונות האווירה הן הדמיות, ומסומנות בסרט.",
               "הבית והשכונה מלמעלה צולמו על ידי מיטל. הגשר המתוכנן ותמונות האווירה הן הדמיות, ומסומנות בסרט."))
L["en"].update(
    film_lead=("Morning in the neighbourhood, coffee at the local centre, the new bridge to Yarkon Park, the home itself, an evening with friends on the terrace, and the area's numbers.",
               "Morning in the neighbourhood, coffee at the local centre, the new bridge to Yarkon Park, the tennis courts and football pitches by the home, the new home itself, an evening on the terrace, and the area's numbers."),
    film_note=("The home was filmed in the apartment itself. The bridge, the aerial views and the lifestyle scenes are illustrations, and are marked in the film.",
               "The home and the aerial views are Meital's own footage. The planned bridge and the lifestyle scenes are illustrations, and are marked in the film."))


def build(lang):
    c = L[lang]; sfx = c["sfx"]
    # the live text before the plan (saved from live-27 before the first plan write); live-27 itself is the text with the plan now
    t = io.open(os.path.join(H, "live-27-preplan-%d.html" % c["pid"]), encoding="utf-8").read().replace("\r\n", "\n"); n0 = len(t)
    assert 'id="plan-%s"' % sfx not in t, "the plan is already on the page"
    assert 'id="top-%s"' % sfx in t and "nlx-h27-jump" not in t
    wa = re.search(r'https://wa\.me/972523631582\?text=[^"]+', t).group(0)
    # 1. the plan right under the film, before the long photo gallery (the first write put it after the gallery: y=6530 on a
    #    phone); the opening's carousel shows the photos first, so the plan sits under the photos and the video, never over them
    a = t.find('<section class="nlx-sec" id="photos-%s"' % sfx); assert a > 0
    assert t.find('id="top-%s"' % sfx) < t.find('id="film-%s"' % sfx) < a
    t = t[:a] + section(c, wa) + t[a:]
    # the page's table of contents: the plan first
    m = re.search(r'<nav class="nlx-toc"[^>]*><a class="nlx-home"[^>]*>[^<]*</a>', t); assert m
    t = t.replace(m.group(0), m.group(0) + '<a href="#plan-%s">%s</a>' % (sfx, c["jump"][1][1]), 1)
    # 2. quick links in the opening, under the call buttons (the price and the facts stay where they are)
    ids = [k for k, _ in c["jump"]]
    for k in ids: assert t.count('id="%s-%s"' % (k, sfx)) == 1, k
    nav = (JUMP_CSS + '<nav class="nlx-h27-jump" aria-label="%s">' % c["jump_lab"] +
           "".join('<a href="#%s-%s">%s</a>' % (k, sfx, lab) for k, lab in c["jump"]) + "</nav>\n")
    old = '<p class="nlx-h27-note">'; assert t.count(old) == 1
    t = t.replace(old, nav + old)
    # 3. the film v3 (film/v3/CHANGES.md: no price per m², no invented towers, tennis and football, a new home, Meital's end card);
    #    the Hebrew page gets the cut with Hebrew captions
    if FILM:
        f = FILM[lang]; t = t.replace("kochav-film-en-v2.mp4", f["mp4"]).replace("kochav-film-en.jpg", f["jpg"])
        t = rep1(t, c["film_lead"][0], c["film_lead"][1], "film lead"); t = rep1(t, c["film_note"][0], c["film_note"][1], "film note")
        t = rep1(t, '"uploadDate": "2026-10-20", "duration": "PT2M10S"', '"uploadDate": "2026-10-27", "duration": "PT2M7S"', "film schema")
        assert "kochav-film-en-v2" not in t and t.count(f["mp4"]) == 2, "film"
    seg = re.sub(r"<(script|style)\b.*?</\1>", "", t[t.find('id="plan-%s"' % sfx):t.find('id="photos-%s"' % sfx)], flags=re.S)
    seg = re.sub(r"<[^>]+>", " ", seg)  # the visible words only (the drawing's colour codes are not words)
    for bad in ("תלת־ממד", "תלת ממד", "אינטראקטיב", "ממשק", "לחצו על", "3D", "—", "–"):  # language DNA
        assert bad not in seg, bad
    # the public source carries no working notes (the source audit flagged "internal:Codex" on 27.10): the comments in this
    # script's CSS and JS stay here, and round27's research comment in the opening's CSS goes too
    a = t.find('id="plan-%s"' % sfx); b = t.find("</section>", a)
    t = t[:a] + re.sub(r"/\*.*?\*/", "", t[a:b], flags=re.S) + t[b:]
    t, n = re.subn(r"/\* the research \(27\.10\):.*?\*/\n?", "", t, flags=re.S); assert n == 1, n
    for w in ("Codex", "codex", "Claude", "Ben:", "(Ben", "27.10"):
        assert w not in re.sub(r'<script type="application/ld\+json">.*?</script>', "", t, flags=re.S), ("working note in the source", w)
    io.open(os.path.join(H, "after-27-%d.html" % c["pid"]), "w", encoding="utf-8", newline="\n").write(t)
    print(lang, c["pid"], "written after-27-%d.html: %d -> %d chars" % (c["pid"], n0, len(t)))


build("he"); build("en")
print("OK: the plan section and the quick links, both languages")
