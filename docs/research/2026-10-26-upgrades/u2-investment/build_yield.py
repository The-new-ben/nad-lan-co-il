import json,os,sys,csv
D=sys.argv[1]; OUT=sys.argv[2]
log=json.load(open(os.path.join(D,"fetch-log.json"),encoding="utf-8"))
names={}
for l in log: names[l["code"]]=l["name"]
lm={ (l["code"],l["kind"]):l.get("last_modified") for l in log}
def series(d,rooms):
    for r in d["trends"]["rooms"]:
        if str(r["numRooms"])==str(rooms):
            return {(g["year"],g["month"]):g.get("settlementPrice") for g in r["graphData"]}, {(g["year"],g["month"]):g.get("countryPrice") for g in r["graphData"]}
    return {},{}
Q=(2026,3)  # quarter 1-3.2026
rows=[]; bad=[]
for code,name in names.items():
    try:
        R=json.load(open(os.path.join(D,f"rent_{code}.json"),encoding="utf-8-sig")); B=json.load(open(os.path.join(D,f"buy_{code}.json"),encoding="utf-8-sig"))
    except Exception as e:
        bad.append((code,name,str(e))); continue
    row={"city":name,"code":code,"name_in_file":R.get("settlementName"),"gov_yield":R["trends"]["indexes"].get("yield"),"gov_price_change":B["trends"]["indexes"].get("priceIncreases"),"gov_luxury":R["trends"]["indexes"].get("luxury"),"rent_latest_all":R.get("settlementPrice"),"rent_country_all":R.get("countryPrice"),"version":R.get("version"),"rent_lm":lm[(code,"rent")],"buy_lm":lm[(code,"buy")]}
    for rooms in ("3","4","5","all"):
        rs,rc=series(R,rooms); bs,bc=series(B,rooms)
        # same quarter Q, else latest common
        q=None
        if rs.get(Q) and bs.get(Q): q=Q
        else:
            common=[k for k in sorted(set(rs)&set(bs),reverse=True) if rs.get(k) and bs.get(k)]
            q=common[0] if common else None
        rq=rs.get(q) if q else None; bq=bs.get(q) if q else None
        rl=None
        for k in sorted(rs,reverse=True):
            if rs[k]: rl=(k,rs[k]); break
        row[f"r{rooms}_q"]=f"{q[1]-2}-{q[1]}.{q[0]}" if q else ""
        row[f"r{rooms}_rent"]=rq; row[f"r{rooms}_price"]=bq
        row[f"r{rooms}_gross"]=round(rq*12/bq*100,2) if rq and bq else None
        row[f"r{rooms}_rent_latest"]=rl[1] if rl else None; row[f"r{rooms}_rent_latest_q"]=f"{rl[0][1]-2}-{rl[0][1]}.{rl[0][0]}" if rl else ""
        # rent yoy latest vs year earlier
        if rl:
            ya=(rl[0][0]-1,rl[0][1]); row[f"r{rooms}_rent_yoy"]=round((rl[1]/rs[ya]-1)*100,1) if rs.get(ya) else None
        # buy yoy at q
        if q:
            ya=(q[0]-1,q[1]); row[f"r{rooms}_price_yoy"]=round((bq/bs[ya]-1)*100,1) if bs.get(ya) else None
    rows.append(row)
# Israel row
R=json.load(open(os.path.join(D,"rent_5000.json"),encoding="utf-8-sig")); B=json.load(open(os.path.join(D,"buy_5000.json"),encoding="utf-8-sig"))
isr={"city":"ישראל (ארצי)","code":"","name_in_file":"countryPrice"}
for rooms in ("3","4","5","all"):
    _,rc=series(R,rooms); _,bc=series(B,rooms)
    for q in [(2026,6),(2026,3)]:
        if rc.get(q) and bc.get(q):
            isr[f"r{rooms}_q"]=f"{q[1]-2}-{q[1]}.{q[0]}"; isr[f"r{rooms}_rent"]=rc[q]; isr[f"r{rooms}_price"]=bc[q]; isr[f"r{rooms}_gross"]=round(rc[q]*12/bc[q]*100,2); break
rows.insert(0,isr)
keys=[]
for r in rows:
    for k in r:
        if k not in keys: keys.append(k)
with open(OUT,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); [w.writerow(r) for r in rows]
json.dump(rows,open(OUT.replace(".csv",".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=0)
print("rows",len(rows),"bad",bad)
