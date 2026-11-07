# -*- coding: utf-8 -*-
"""Talking advisor, LIVE experiment (Ben 7.11.2026 night: "כרגע תעשה רק באנגלית... אני רוצה לראות את זה לייב... תנועות שפתיים ממש מינימליות").
One English page only: /en/buy-property-in-israel/ (page 5154). Additive block at the end of the page content: scoped CSS + markup + script.
Nothing is printed for search engines except the block markup (no headings); the face, mouth patches and voice are media-library files.
She pops up 1.2 s after load, speaks on the visitor's first tap anywhere (browsers block sound before a tap), lips barely move, closes with
one tap and stays closed for that visitor. "Chat with our team" opens the site's WhatsApp. Backup before, read-back after.
python deploy_live.py [--go] | --remove"""
import io, json, os, re, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", ".."))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "ag"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
PAGE = 5154; GO = "--go" in sys.argv; START, END = "<!-- nlagent:start -->", "<!-- nlagent:end -->"
WA = "https://wa.me/972525101555?text=Hi%2C%20I%E2%80%99d%20like%20more%20details."
FILES = {"face": ("demo/face.webp", "image/webp", "nlagent-face-v1.webp"), "B": ("demo/m-B.webp", "image/webp", "nlagent-mouth-b-v1.webp"),
         "C": ("demo/m-C.webp", "image/webp", "nlagent-mouth-c-v1.webp"), "BLINK": ("demo/m-BLINK.webp", "image/webp", "nlagent-blink-v1.webp"),
         "voice": ("demo/greet-en.mp3", "audio/mpeg", "nlagent-greet-en-v1.mp3")}

def media(path, mime, name):
    slug = os.path.splitext(name)[0]
    s, r, _ = req("GET", "/wp-json/wp/v2/media?slug=%s&_fields=id,source_url" % slug); assert s == 200, (s, r)
    hit = [x for x in r if x["source_url"].rsplit("/", 1)[-1] == name]
    if hit: return hit[0]["source_url"]
    if not GO: return "(would upload %s)" % name
    rq = urllib.request.Request(ns["BASE"] + "/wp-json/wp/v2/media", data=open(os.path.join(H, path), "rb").read(), method="POST")
    rq.add_header("Authorization", ns["AUTH"]); rq.add_header("User-Agent", ns["UA"]); rq.add_header("Content-Type", mime)
    rq.add_header("Content-Disposition", 'attachment; filename="%s"' % name)
    with urllib.request.urlopen(rq, timeout=300) as resp: up = json.loads(resp.read().decode())
    req("POST", "/wp-json/wp/v2/media/%d" % up["id"], {"title": "NadLan talking advisor (computer-made character)", "alt_text": ""})
    return up["source_url"]

s, pg, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PAGE); assert s == 200, s
raw = pg["content"]["raw"]
if "--remove" in sys.argv:
    a, b = raw.find(START), raw.find(END); assert a >= 0 and b > a
    s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PAGE, {"content": raw[:a].rstrip() + raw[b + len(END):]}); print("removed", s2); sys.exit(0)
U = {k: media(*v) for k, v in FILES.items()}
meta = json.load(open(os.path.join(H, "demo", "meta.json")))
cues = json.load(open(os.path.join(H, "greet-en.cues.json"), encoding="utf-8"))["mouthCues"]
cues = [[c["start"], c["end"], c["value"]] for c in cues if c["value"] not in ("A", "X")]
text = json.load(open(os.path.join(H, "lines.json"), encoding="utf-8"))["en"].replace("Nad-Lan", "NadLan")
P = {k: meta["patches"][k] for k in ("B", "C", "BLINK")}
cfg = {"u": U, "p": P, "s": meta["size"], "c": cues, "t": text, "wa": WA}
CSS = (".nlag{position:fixed;inset-inline:12px;bottom:calc(144px + env(safe-area-inset-bottom,0px));z-index:99990;max-width:360px;margin-inline:auto;background:#0F2233;color:#fff;"
       "border:1px solid #24435C;border-radius:16px;box-shadow:0 18px 50px rgba(8,20,32,.45);padding:12px;font:15px/1.5 'IBM Plex Sans',system-ui,sans-serif;"
       "transform:translateY(140%);opacity:0;transition:transform .55s cubic-bezier(.2,1.3,.4,1),opacity .35s;direction:ltr;text-align:left}"
       ".nlag.on{transform:none;opacity:1}@media(min-width:900px){.nlag{inset-inline:auto 24px;bottom:128px;width:330px}}"
       ".nlag-top{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px}.nlag-who{font-weight:700;font-size:16px}"
       ".nlag-who small{display:block;font-weight:400;font-size:12px;color:#A9BCCB}.nlag-x{width:32px;height:32px;border-radius:50%;border:1px solid #24435C;"
       "background:transparent;color:#fff;font-size:18px;cursor:pointer;line-height:1}.nlag-face{position:relative;width:100%;aspect-ratio:1/1;max-height:29vh;margin-inline:auto;"
       "border-radius:12px;overflow:hidden;background:#1a2f40}.nlag-f{position:absolute;inset:0;animation:nlagb 4.2s ease-in-out infinite;transform-origin:50% 60%}"
       ".nlag-f img{position:absolute;display:block;pointer-events:none;margin:0;max-width:none}.nlag-f img.p{visibility:hidden}"
       "@keyframes nlagb{0%,100%{transform:scale(1)}50%{transform:scale(1.012)}}.nlag-tap{position:absolute;left:0;right:0;bottom:10px;margin:auto;width:max-content;"
       "background:#fff;color:#12202A;font-weight:700;border:0;border-radius:22px;padding:8px 15px;font-size:14px;cursor:pointer}"
       ".nlag-cap{margin:10px 2px 9px;font-size:15.5px;min-height:3em}.nlag-cap b{font-weight:600;color:#fff}.nlag-cap span{color:#A9BCCB}"
       ".nlag-row{display:flex;gap:8px}.nlag-row a,.nlag-row button{flex:1;height:42px;border-radius:10px;font:600 14.5px 'IBM Plex Sans',sans-serif;"
       "display:flex;align-items:center;justify-content:center;text-decoration:none;cursor:pointer}.nlag-go{background:#2F6F86;color:#fff!important;border:0}"
       ".nlag-re{background:transparent;color:#fff;border:1px solid #24435C}.nlag-note{margin-top:7px;font-size:11.5px;color:#A9BCCB;text-align:center}")
HTML = ('<div class="nlag" id="nlag" role="dialog" aria-label="NadLan advisor"><div class="nlag-top"><div class="nlag-who">NadLan advisor'
        '<small>A computer-made character</small></div><button class="nlag-x" id="nlagx" aria-label="Close">×</button></div>'
        '<div class="nlag-face"><div class="nlag-f" id="nlagf"></div><button class="nlag-tap" id="nlagt">Tap to hear her</button></div>'
        '<div class="nlag-cap" id="nlagc"></div><div class="nlag-row"><a class="nlag-go" id="nlagw" target="_blank" rel="noopener">Chat with our team</a>'
        '<button class="nlag-re" id="nlagr">Hear again</button></div><div class="nlag-note">A computer-made character, not a person.</div></div>')
JS = r"""(function(){var C=window.__NLAG;if(!C)return;try{if(localStorage.getItem('nlag-closed')==='1')return}catch(e){}
var box=document.getElementById('nlag'),f=document.getElementById('nlagf'),cap=document.getElementById('nlagc'),tap=document.getElementById('nlagt');
document.body.appendChild(box);document.getElementById('nlagw').href=C.wa;
var b=new Image();b.src=C.u.face;b.alt='';b.style.cssText='inset:0;width:100%;height:100%';f.appendChild(b);var P={};
['B','C','BLINK'].forEach(function(k){var m=C.p[k],i=new Image();i.src=C.u[k];i.className='p';i.alt='';
i.style.left=(m.x/C.s*100)+'%';i.style.top=(m.y/C.s*100)+'%';i.style.width=(m.w/C.s*100)+'%';i.style.height=(m.h/C.s*100)+'%';f.appendChild(i);P[k]=i});
var MAP={B:'B',C:'B',D:'C',E:'B',F:'B',G:'B',H:'B'},OPA={B:.55,C:.5},cur=null,words=C.t.split(' '),au=new Audio(C.u.voice);au.preload='auto';
function shape(k){if(k===cur)return;if(cur)P[cur].style.visibility='hidden';if(k){P[k].style.opacity=OPA[k];P[k].style.visibility='visible'}cur=k}
function capt(t){var d=au.duration||12,n=Math.min(words.length,Math.ceil(words.length*Math.min(1,t/(d*.97))));cap.innerHTML='<b>'+words.slice(0,n).join(' ')+'</b> <span>'+words.slice(n).join(' ')+'</span>'}
function blink(){P.BLINK.style.visibility='visible';setTimeout(function(){P.BLINK.style.visibility='hidden'},140);setTimeout(blink,2600+Math.random()*2400)}
function tick(){var t=au.currentTime,k=null;for(var i=0;i<C.c.length;i++){if(t>=C.c[i][0]&&t<C.c[i][1]){k=MAP[C.c[i][2]]||null;break}}
shape(au.paused?null:k);capt(t);if(!au.ended&&!au.paused)requestAnimationFrame(tick);else{shape(null);if(au.ended)capt(99)}}
function speak(){au.currentTime=0;var p=au.play();if(p&&p.then){p.then(function(){tap.style.display='none';tick()}).catch(function(){tap.style.display='block'})}}
function first(){document.removeEventListener('pointerdown',first,true);document.removeEventListener('keydown',first,true);if(box.classList.contains('on')&&au.paused&&au.currentTime===0)speak()}
tap.onclick=function(e){e.stopPropagation();speak()};document.getElementById('nlagr').onclick=speak;
document.getElementById('nlagx').onclick=function(){au.pause();box.classList.remove('on');try{localStorage.setItem('nlag-closed','1')}catch(e){}};
capt(0);setTimeout(blink,1800);document.addEventListener('pointerdown',first,true);document.addEventListener('keydown',first,true);
setTimeout(function(){box.classList.add('on');setTimeout(speak,650)},1200)})();"""
BLOCK = (START + "<style>" + CSS + "</style>" + HTML + "<script>window.__NLAG=" + json.dumps(cfg, ensure_ascii=False) + ";" + JS + "</script>" + END)
if START in raw:
    a, b = raw.find(START), raw.find(END) + len(END); new = raw[:a] + BLOCK + raw[b:]; mode = "swap"
else:
    new = raw.rstrip() + "\n" + BLOCK; mode = "append"
print("[plan] page %d %s: %d -> %d chars; media: %s" % (PAGE, mode, len(raw), len(new), json.dumps(U)))
if not GO: sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s-pre-agent.html" % (PAGE, time.strftime("%Y%m%dT%H%M%S"))), "w", encoding="utf-8").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PAGE, {"content": new}); assert s2 in (200, 201), s2
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PAGE); assert r["content"]["raw"] == new, "read-back"
time.sleep(5)
live = urllib.request.urlopen(urllib.request.Request(pg["link"] + "?f=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print({"block": live.count('id="nlag"'), "script": "window.__NLAG" in live, "h1": len(re.findall(r"<h1[\s>]", live)), "fatal": "Fatal error" in live})
