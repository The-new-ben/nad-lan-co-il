# -*- coding: utf-8 -*-
"""HAD-801 (Ben via the coordinator, 23.11.2026): (1) the street-kit rider stood upright through the bike frame; (2) add a generic
food-delivery courier (square insulated box on the back, no logo or text, plain colours).
In Codex's street kit (part-5KYHLEMD.js) people and bikes are built from simple shapes. This adds two figures built the same way,
in the bike's own coordinates (front = -z; handlebar y .99 z -.37; saddle y .78 z .26; cranks at y .36 z .13):
  cyclistBlue  - seated on the saddle, torso leaning to the bars, hands on the bars, knees bent to the pedals (one foot down, one up;
                 thigh .42, shin .40, knees solved by two-bone geometry)
  courierRider - the same seated pose in a plain red jacket, with a black square insulated box (with a grey band) on the rear rack
The street bundle then uses them: every moving bike pair alternates courier / cyclist, scale 1, no upward lift.
Three files change and so get new names (static .js is cached for a year): part-5KYHLEMD-r3.js, part-SBNMZNQM-r3.js (imports it),
walk-DGQMIG45-r3.js (imports both); all registered in transfer/; the ten street pages point to walk-DGQMIG45-r3.js. Old files stay.
  python fix_cyclists.py <package dir (site2)> <manifest out>"""
import gzip, hashlib, json, os, re, subprocess, sys
P, MAN = sys.argv[1], sys.argv[2]
assert "site2" in P
def sha(b): return hashlib.sha256(b).hexdigest()
def brotli(b):
    return subprocess.run(["node", "-e", "const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d));process.stdin.on('end',()=>process.stdout.write(z.brotliCompressSync(Buffer.concat(c),{params:{[z.constants.BROTLI_PARAM_QUALITY]:11}})))"],
                          input=b, capture_output=True, check=True).stdout
def rd(n): return open(os.path.join(P, "packed", n), encoding="utf-8").read()
KIT, KIT3 = "part-5KYHLEMD.js", "part-5KYHLEMD-r3.js"
SB, SB3 = "part-SBNMZNQM.js", "part-SBNMZNQM-r3.js"
WALK, WALK3 = "walk-DGQMIG45-r1.js", "walk-DGQMIG45-r3.js"

def rider_parts(shirt):
    return ("s(f,o,0,1.53,-.05,.114,.154,.113),s(f,d,0,1.622,-.04,.111,.08,.11),"
            "g(i,%s,[0,.9,.22],[0,1.38,0],.15),s(f,\"dark\",0,.88,.24,.168,.115,.12),"
            "g(i,t.dark,[-.092,.88,.24],[-.1,.586,-.06],.073),g(i,t.dark,[-.1,.586,-.06],[-.1,.22,.1],.06),s(f,\"black\",-.1,.2,.05,.079,.058,.14),"
            "g(i,t.dark,[.092,.88,.24],[.1,.744,-.157],.073),g(i,t.dark,[.1,.744,-.157],[.1,.5,.16],.06),s(f,\"black\",.1,.48,.11,.079,.058,.14),"
            "g(i,%s,[-.19,1.32,.03],[-.22,1.15,-.17],.079),g(i,%s,[.19,1.32,.03],[.22,1.15,-.17],.079),"
            "g(i,o,[-.22,1.15,-.17],[-.17,1,-.36],.044),g(i,o,[.22,1.15,-.17],[.17,1,-.36],.044)") % (shirt, shirt, shirt)
CYC = "cyclistBlue:p([" + rider_parts("t.blue") + "]),"
COU = ("courierRider:p([" + rider_parts("t.red") + ","
       "s(r,\"black\",0,.87,.6,.44,.4,.42),s(r,\"steel\",0,.87,.6,.448,.035,.428),s(r,\"steel\",0,.66,.6,.06,.02,.4)]),")
kit = rd(KIT)
A = "personRed:b(t.red,o),"
assert kit.count(A) == 1 and kit.count('"human"),c={') == 1
kit3 = kit.replace(A, A + CYC + COU)
sb3 = rd(SB)
assert sb3.count("./" + KIT) == 1
sb3 = sb3.replace("./" + KIT, "./" + KIT3)
w = rd(WALK)
R1 = 'kind:"personBlue",id:v,x:be.x,z:be.z,s:.8,a:-be.yaw,walk:ye,home:ze,speed:2.75*le,rider:!0'
R2 = 'me.y=H.ground(Wn.x,Wn.z)+.19+(me.rider?.17:0)'
for a in (R1, R2, "./" + KIT, "./" + SB):
    assert w.count(a) == 1, (a, w.count(a))
w3 = (w.replace(R1, 'kind:he%2?"cyclistBlue":"courierRider",id:v,x:be.x,z:be.z,s:1,a:-be.yaw,walk:ye,home:ze,speed:2.75*le,rider:!0')
       .replace(R2, 'me.y=H.ground(Wn.x,Wn.z)+.19').replace("./" + KIT, "./" + KIT3).replace("./" + SB, "./" + SB3))
res_p = os.path.join(P, "transfer", "resources.json"); res = json.load(open(res_p, encoding="utf-8"))
for name, txt in ((KIT3, kit3), (SB3, sb3), (WALK3, w3)):
    open(os.path.join(P, "packed", name), "w", encoding="utf-8", newline="").write(txt)
    reg = re.sub(r'"\./((?:part|walk)-[A-Z0-9]+(?:-r\d)?\.js)"', r'"./?f=\1"', txt).encode("utf-8")
    h = sha(reg); gz = gzip.compress(reg, compresslevel=9, mtime=0); br = brotli(reg)
    for ext, data in (("raw", reg), ("gz", gz), ("br", br)):
        open(os.path.join(P, "transfer", "%s.%s" % (h, ext)), "wb").write(data)
    res["packed"][name] = {"sha256": h, "bytes": len(reg), "br": len(br), "gzip": len(gz)}
open(res_p, "w", encoding="utf-8", newline="\n").write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
PG = os.path.join(P, "pages"); n = 0
for f in sorted(os.listdir(PG)):
    if not f.endswith(".html") or f.endswith(("-directory.html", "-places.html")):
        continue
    p = os.path.join(PG, f); b = open(p, encoding="utf-8").read()
    if "./packed/" + WALK in b:
        b = b.replace("./packed/" + WALK, "./packed/" + WALK3)
        open(p, "w", encoding="utf-8", newline="").write(b)
        open(p + ".gz", "wb").write(gzip.compress(b.encode("utf-8"), compresslevel=6, mtime=0)); n += 1
dg = {f: hashlib.sha256(open(os.path.join(PG, f), "rb").read()).hexdigest() for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
man = {}
for root, _, files in os.walk(P):
    for f in files:
        q = os.path.join(root, f); man[os.path.relpath(q, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(q), "md5": hashlib.md5(open(q, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print("pages ->", WALK3, n, "| files", len(man))
