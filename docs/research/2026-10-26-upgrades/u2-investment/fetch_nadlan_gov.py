import json,os,sys,time,urllib.request,datetime
OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
UA={"User-Agent":"nad-lan.co.il investment research (official public summary files; polite 1 req/s)"}
C={"תל אביב-יפו":5000,"ירושלים":3000,"חיפה":4000,"ראשון לציון":8300,"פתח תקווה":7900,"אשדוד":70,"נתניה":7400,"באר שבע":9000,"בני ברק":6100,"חולון":6600,"רמת גן":8600,"אשקלון":7100,"רחובות":8400,"בת ים":6200,"בית שמש":2610,"כפר סבא":6900,"הרצליה":6400,"חדרה":6500,"מודיעין-מכבים-רעות":1200,"נצרת":7300,"לוד":7000,"רמלה":8500,"רעננה":8700,"ראש העין":2640,"הוד השרון":9700,"גבעתיים":6300,"קריית אתא":6800,"נהריה":9100,"קריית גת":2630,"אילת":2600,"עפולה":7700,"יבנה":2660,"נס ציונה":7200,"עכו":7600,"טבריה":6700,"קריית ביאליק":9500,"קריית מוצקין":8200,"קריית ים":9600,"כרמיאל":1139,"קריית אונו":2620,"רמת השרון":2650,"אור יהודה":2400,"נתיבות":246,"אופקים":31,"שדרות":1031,"דימונה":2200,"טירת כרמל":2100,"נשר":2500,"אור עקיבא":1020,"יהוד-מונוסון":9400,"גבעת שמואל":681,"באר יעקב":2530,"קריית מלאכי":1034,"קריית שמונה":2800,"צפת":8000,"חריש":1247,"אריאל":3570,"אלעד":1309,"מעלה אדומים":3616,"גדרה":2550,"זכרון יעקב":9300,"פרדס חנה-כרכור":7800,"כפר יונה":168,"קדימה-צורן":195,"גני תקווה":229,"שוהם":1304,"מבשרת ציון":1015,"יקנעם עילית":240,"מגדל העמק":874,"בית שאן":9200,"ערד":2560,"ירוחם":831,"אום אל-פחם":2710,"רהט":1161}
log=[]
for name,code in C.items():
    for kind in ("rent","buy"):
        u=f"https://data.nadlan.gov.il/api/pages/settlement/{kind}/{code}.json"
        t=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60); b=r.read()
            open(os.path.join(OUT,f"{kind}_{code}.json"),"wb").write(b)
            log.append({"name":name,"code":code,"kind":kind,"url":u,"status":r.status,"last_modified":r.headers.get("Last-Modified"),"utc":t,"bytes":len(b)})
        except Exception as e:
            log.append({"name":name,"code":code,"kind":kind,"url":u,"status":getattr(e,"code",None),"error":str(e)[:150],"utc":t})
        time.sleep(1)
json.dump(log,open(os.path.join(OUT,"fetch-log.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(sum(1 for l in log if l.get("status")==200),"ok of",len(log))
