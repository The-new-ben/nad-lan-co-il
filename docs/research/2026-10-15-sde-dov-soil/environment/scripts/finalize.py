import json,csv,glob,math,sys,os
ENV,SP=sys.argv[1],sys.argv[2]
SECT=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
# combined sector totals
rows=[]
for src,f in (('IMS Tel Aviv Coast 2410, 2016-2025, 24h (3-hourly)','raw/windrose_ims_summary.json'),('NOAA ISD Sde Dov 401762 (METAR), 2009-2018, ~05-22 local only','raw/windrose_sde_dov_metar_summary.json')):
    s=json.load(open(os.path.join(ENV,f),encoding='utf-8'))
    for S in ['year','winter','spring','summer','autumn']:
        for i,(n,p) in enumerate(s[S]['all_sectors_pct']):
            rows.append([src,S,n,i*22.5,p])
        rows.append([src,S,'CALM','',s[S]['calm_pct']])
        if 'variable_pct' in s[S]: rows.append([src,S,'VARIABLE','',s[S]['variable_pct']])
with open(os.path.join(ENV,'windrose_sectors.csv'),'w',newline='',encoding='utf-8') as fo:
    w=csv.writer(fo); w.writerow(['source','season','sector','direction_from_deg','percent']); w.writerows(rows)
# raw extracts
recs=[]
for f in sorted(glob.glob(SP+'/dl_ims/h2410_*.json')): recs+=json.load(open(f,encoding='utf-8'))['result']['records']
with open(os.path.join(ENV,'raw','ims_2410_tel_aviv_coast_2005_2026.csv'),'w',newline='',encoding='utf-8') as fo:
    w=csv.writer(fo); w.writerow(['stn_num','time_obs','wind_dir_deg','wind_spd_ms','tmp_air_dry_c','hmd_rlt_pct'])
    for r in recs: w.writerow([r['stn_num'],r['time_obs'],r['wind_dir'],r['wind_spd'],r['tmp_air_dry'],r['hmd_rlt']])
with open(os.path.join(ENV,'raw','noaa_isd_401762_sde_dov_wind_2009_2018.csv'),'w',newline='',encoding='utf-8') as fo:
    w=csv.writer(fo); w.writerow(['date_utc','report_type','WND(dir,dir_qc,type,speed_ms_x10,speed_qc)','TMP(C_x10,qc)'])
    for f in sorted(glob.glob(SP+'/env/isd/*.csv')):
        for r in csv.DictReader(open(f,encoding='utf-8')): w.writerow([r['DATE'],r['REPORT_TYPE'].strip(),r['WND'],r['TMP']])
# coastline points
d=json.load(open(SP+'/dl_osm/coast.json',encoding='utf-8'))
with open(os.path.join(ENV,'raw','osm_coastline_points.csv'),'w',newline='',encoding='utf-8') as fo:
    w=csv.writer(fo); w.writerow(['way_id','lat','lon'])
    for e in d['elements']:
        for g in e['geometry']: w.writerow([e['id'],g['lat'],g['lon']])
# air stations
ref=(179778,668867)
iec={"תל אביב יפו- שיכון ל'":(180493,668562),'תל אביב יפו- הצפון החדש':(179731,665876),'תל אביב יפו- שכונת המשתלה':(184444,670930),'תל אביב יפו- לב תל אביב':(179119,663292)}
vals={"תל אביב יפו- שיכון ל'":'PM10 annual 39.0 ug/m3 (data availability 78%), 5 daily exceedances (2023, IEC report p.21)',
 'תל אביב יפו- הצפון החדש':'NO2 annual 19.7 ug/m3 (94%), 0 hourly exceedances; PM2.5 annual 17.8 ug/m3 (98%), 8 daily exceedances; O3 annual 66.2 ug/m3, max 8-h 125.9, 0 exceedances of 140 (2023, IEC report p.19-21)',
 'תל אביב יפו- שכונת המשתלה':'NO2 annual 18.0 ug/m3 (92%); O3 max 8-h 129.7, 0 exceedances (2023, IEC report p.19-20)',
 'תל אביב יפו- לב תל אביב':'NO2 annual 24.6 ug/m3 (89%); PM2.5 annual 18.0 ug/m3 (99%), 7 daily exceedances (2023, IEC report p.19, 21)'}
st=json.load(open(SP+'/dl_air/stations_ds.json',encoding='utf-8'))['result']['records']
out=[]
for x in st:
    try: X=float(x['X']); Y=float(x['Y'])
    except: continue
    name=x['שם התחנה החדש'].strip()
    if name in iec: X,Y=iec[name]; csrc='IEC 2023 report table 1'
    else: csrc='data.gov.il air-stations'
    dist=math.hypot(X-ref[0],Y-ref[1])/1000
    if dist>6.5: continue
    brg=(math.degrees(math.atan2(X-ref[0],Y-ref[1]))+360)%360
    out.append([round(dist,1),round(brg),name,x['שם התחנה הישן'].strip(),x['הגוף המנטר'].replace(' iso','').strip(),x['Station type'],x['שנת הקמה'],(x['כתובת'] or '').strip(),int(X),int(Y),csrc,(x['מזהמי אוויר'] or '').strip(),(x['פרמטרים מטאורולוגיים'] or '').strip(),vals.get(name,'not found (Ministry annual summaries not reachable, see facts.json)' if 'המשרד להגנת הסביבה' in x['הגוף המנטר'] else '')])
out.sort()
with open(os.path.join(ENV,'air_stations.csv'),'w',newline='',encoding='utf-8-sig') as fo:
    w=csv.writer(fo); w.writerow(['distance_km_from_mid_district','bearing_deg_from_mid_district','station_name','old_name','operator','station_type','year_established','address','itm_x','itm_y','coord_source','pollutants_measured','met_params','annual_values_found'])
    w.writerows(out)
for r in out: print(r[:7], r[13][:60])
