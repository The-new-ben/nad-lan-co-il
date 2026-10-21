import json,glob,collections,sys,math,csv
src,out=sys.argv[1],sys.argv[2]
SECT=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
BINS=[(0.5,2,'0.5-2'),(2,4,'2-4'),(4,6,'4-6'),(6,8,'6-8'),(8,99,'8+')]
SEA=('SSW','SW','WSW','W','WNW','NW','NNW','N'); LAND=('NE','ENE','E','ESE','SE','SSE')
def season(m): return {12:'winter',1:'winter',2:'winter',3:'spring',4:'spring',5:'spring',6:'summer',7:'summer',8:'summer'}.get(m,'autumn')
recs=[]
for f in sorted(glob.glob(src+'/h2410_*.json')):
    recs+=json.load(open(f,encoding='utf-8'))['result']['records']
Y0,Y1=2016,2025
rows=[]; dz=collections.Counter(); spd_vals=collections.Counter()
for r in recs:
    y=int(r['time_obs'][:4]); h=int(r['time_obs'][11:13])
    if not (Y0<=y<=Y1) or h%3: continue
    if r['wind_dir'] in ('',None) or r['wind_spd'] in ('',None): continue
    d=float(r['wind_dir']); s=float(r['wind_spd']); m=int(r['time_obs'][5:7])
    rows.append((y,m,h,d,s))
    if s<0.5: dz['calm']+=1
    if d==0: dz['dir0']+=1
print('obs',len(rows),dz)
cnt=collections.defaultdict(collections.Counter); tot=collections.Counter(); calm=collections.Counter(); spd=collections.defaultdict(list)
di=collections.defaultdict(list)
for y,m,h,d,s in rows:
    ss=season(m)
    for S in (ss,'year'):
        tot[S]+=1; spd[S].append(s)
        if s<0.5 or d==0: calm[S]+=1; continue
        sec=int(((d+11.25)%360)//22.5); b=next(l for lo,hi,l in BINS if lo<=s<hi)
        cnt[S][(sec,b)]+=1
    di[(ss,h)].append((d,s))
with open(out+'/windrose_ims_tel_aviv_coast.csv','w',newline='',encoding='utf-8') as fo:
    w=csv.writer(fo); w.writerow(['season','sector','direction_from_deg','speed_bin_ms','percent_of_obs','obs'])
    for S in ['year','winter','spring','summer','autumn']:
        for i,n in enumerate(SECT):
            for lo,hi,l in BINS:
                c=cnt[S][(i,l)]; w.writerow([S,n,i*22.5,l,round(100*c/tot[S],2),c])
        w.writerow([S,'CALM','','<0.5',round(100*calm[S]/tot[S],2),calm[S]])
summ={}
for S in ['year','winter','spring','summer','autumn']:
    secs=[(SECT[i],round(100*sum(cnt[S][(i,b)] for _,_,b in BINS)/tot[S],1)) for i in range(16)]
    summ[S]={'obs':tot[S],'top_sectors_pct':sorted(secs,key=lambda x:-x[1])[:4],'all_sectors_pct':secs,'calm_pct':round(100*calm[S]/tot[S],1),
      'mean_speed_ms':round(sum(spd[S])/len(spd[S]),2),'from_sea_side_SSW_to_N_pct':round(sum(p for n,p in secs if n in SEA),1),
      'from_land_side_NE_to_SSE_pct':round(sum(p for n,p in secs if n in LAND),1),'share_ge_8ms_pct':round(100*sum(cnt[S][(i,'8+')] for i in range(16))/tot[S],1)}
with open(out+'/diurnal_ims_tel_aviv_coast.csv','w',newline='',encoding='utf-8') as fo:
    w=csv.writer(fo); w.writerow(['season','obs_hour_utc','local_hour_israel_summer_time_utc+3','local_hour_winter_utc+2','obs','vector_mean_dir_from_deg','mean_speed_ms','pct_from_sea_side_SSW_to_N','pct_from_land_side_NE_to_SSE'])
    for ss in ['winter','spring','summer','autumn']:
        for h in range(0,24,3):
            L=di[(ss,h)]; u=v=0; sea=land=0
            for d,s in L:
                if s<0.5 or d==0: continue
                u+=-s*math.sin(math.radians(d)); v+=-s*math.cos(math.radians(d))
                n=SECT[int(((d+11.25)%360)//22.5)]; sea+=n in SEA; land+=n in LAND
            md=(math.degrees(math.atan2(-u,-v))+360)%360
            w.writerow([ss,h,(h+3)%24,(h+2)%24,len(L),round(md),round(sum(s for _,s in L)/len(L),2),round(100*sea/len(L),1),round(100*land/len(L),1)])
# strong winds by direction in winter
sw=collections.Counter(SECT[int(((d+11.25)%360)//22.5)] for y,m,h,d,s in rows if season(m)=='winter' and s>=8 and d!=0)
summ['_strong_winter_ge8_by_sector']=sw.most_common(6)
summ['_meta']={'station':'IMS TEL AVIV COAST, stn_num 2410 (env 178), 32.058N 34.7588E, 10 m; automatic; opened 2005-04-01','years':f'{Y0}-{Y1}','obs_used':len(rows),
 'sampling':'3-hourly synoptic observations (00,03,...,21); times treated as UTC (WMO synoptic convention) - not confirmed in IMS documentation (the file explaining the data requires a sign-in)'}
json.dump(summ,open(out+'/windrose_ims_summary.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps({k:({kk:vv for kk,vv in v.items() if kk!='all_sectors_pct'} if isinstance(v,dict) else v) for k,v in summ.items()},ensure_ascii=False))
