import csv,glob,collections,sys,math,json
from datetime import datetime,timedelta
src,out=sys.argv[1],sys.argv[2]
SECT=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
BINS=[(0.5,2,'0.5-2'),(2,4,'2-4'),(4,6,'4-6'),(6,8,'6-8'),(8,99,'8+')]
def season(m): return {12:'winter',1:'winter',2:'winter',3:'spring',4:'spring',5:'spring',6:'summer',7:'summer',8:'summer'}.get(m,'autumn')
recs={}
for f in sorted(glob.glob(src+'/*.csv')):
    for r in csv.DictReader(open(f,encoding='utf-8')):
        if r['REPORT_TYPE'].strip()!='FM-15': continue
        w=r['WND'].split(',')
        if len(w)<5: continue
        d,dq,t,s,sq=w
        if sq not in '0145' and t!='C': continue
        sp=int(s)/10 if s!='9999' else None
        dt=datetime.fromisoformat(r['DATE'])
        key=dt.strftime('%Y%m%d%H')
        if key in recs: continue  # one report per UTC hour
        recs[key]=(dt,t,int(d),sp)
cnt=collections.defaultdict(lambda: collections.Counter()); tot=collections.Counter()
calm=collections.Counter(); var=collections.Counter(); spd=collections.defaultdict(list)
diur=collections.defaultdict(list)
for k,(dt,t,d,sp) in recs.items():
    ss=season(dt.month)
    for S in (ss,'year'):
        tot[S]+=1
        if t=='C' or (sp is not None and sp<0.5): calm[S]+=1; continue
        if t=='V' or d==999: var[S]+=1; spd[S].append(sp or 0); continue
        sec=int(((d+11.25)%360)//22.5)
        b=next(lab for lo,hi,lab in BINS if lo<=sp<hi)
        cnt[S][(sec,b)]+=1; spd[S].append(sp)
    # local standard time approx: Israel UTC+2 winter, UTC+3 summer (IDT) - use month rule
    off=3 if 4<=dt.month<=10 else 2
    lh=(dt.hour+off)%24
    diur[(ss,lh)].append((t,d,sp))
with open(out+'/windrose.csv','w',newline='',encoding='utf-8') as fo:
    wr=csv.writer(fo); wr.writerow(['season','sector','direction_from_deg','speed_bin_ms','percent_of_reports','reports'])
    for S in ['year','winter','spring','summer','autumn']:
        for i,n in enumerate(SECT):
            for lo,hi,lab in BINS:
                c=cnt[S][(i,lab)]; wr.writerow([S,n,i*22.5,lab,round(100*c/tot[S],2),c])
        wr.writerow([S,'VARIABLE','',"<4 typical",round(100*var[S]/tot[S],2),var[S]])
        wr.writerow([S,'CALM','',"<0.5",round(100*calm[S]/tot[S],2),calm[S]])
summ={}
for S in ['year','winter','spring','summer','autumn']:
    secs=[(SECT[i],round(100*sum(cnt[S][(i,b)] for _,_,b in BINS)/tot[S],1)) for i in range(16)]
    top=sorted(secs,key=lambda x:-x[1])[:4]
    seaside=sum(p for (n,p) in secs if n in ('SSW','SW','WSW','W','WNW','NW','NNW','N'))
    landside=sum(p for (n,p) in secs if n in ('NE','ENE','E','ESE','SE','SSE'))
    summ[S]={'reports':tot[S],'top_sectors_pct':top,'all_sectors_pct':secs,'calm_pct':round(100*calm[S]/tot[S],1),'variable_pct':round(100*var[S]/tot[S],1),
      'mean_speed_ms':round(sum(spd[S])/len(spd[S]),2),'from_sea_side_SSW_to_N_pct':round(seaside,1),'from_land_side_NE_to_SSE_pct':round(landside,1),
      'share_ge_8ms_pct':round(100*sum(cnt[S][(i,'8+')] for i in range(16))/tot[S],1)}
with open(out+'/diurnal.csv','w',newline='',encoding='utf-8') as fo:
    wr=csv.writer(fo); wr.writerow(['season','local_hour','reports','vector_mean_dir_from_deg','mean_speed_ms','pct_from_sea_side_SSW_to_N','pct_from_land_side_NE_to_SSE'])
    for ss in ['winter','spring','summer','autumn']:
        for h in range(24):
            L=diur.get((ss,h),[])
            if len(L)<200: continue
            u=v=0; sp=[]; sea=land=0
            for t,d,s in L:
                if s is None: continue
                sp.append(s)
                if t in('C','V') or d==999: continue
                u+=-s*math.sin(math.radians(d)); v+=-s*math.cos(math.radians(d))
                sec=SECT[int(((d+11.25)%360)//22.5)]
                if sec in ('SSW','SW','WSW','W','WNW','NW','NNW','N'): sea+=1
                if sec in ('NE','ENE','E','ESE','SE','SSE'): land+=1
            md=(math.degrees(math.atan2(-u,-v))+360)%360
            wr.writerow([ss,h,len(L),round(md),round(sum(sp)/len(sp),2),round(100*sea/len(L),1),round(100*land/len(L),1)])
yrs=sorted({k[:4] for k in recs}); 
summ['_meta']={'station':'NOAA ISD 401762-99999 SDE DOV, IS (ICAO LLSD), 32.117N 34.783E, elev 13 m','years':yrs,'hourly_reports_used':len(recs),
 'report_type':'FM-15 METAR only, first report per UTC hour','coverage_note':'airport METARs cover roughly 05:00-22:00 local time; night hours are almost absent, so the rose describes daytime wind',
 'local_time_rule':'UTC+3 Apr-Oct, UTC+2 Nov-Mar (approximation of Israel daylight time)','sectors':'16 x 22.5 deg, direction the wind blows FROM'}
json.dump(summ,open(out+'/windrose_summary.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps({k:{kk:vv for kk,vv in v.items() if kk!='all_sectors_pct'} for k,v in summ.items()},indent=1))
