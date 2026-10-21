# NOAA solar calculator equations (Meeus-based), sunrise/sunset with -0.833 deg (refraction + semi-diameter)
import math,datetime,csv,sys
LAT,LON=32.1125,34.7841
def jd(d): return d.toordinal()+1721424.5
def calc(date):
    out={}
    for event,sign in (('sunrise',-1),('sunset',1)):
        t_utc=12.0
        for _ in range(4):
            JD=jd(date)+t_utc/24; T=(JD-2451545)/36525
            L0=(280.46646+T*(36000.76983+0.0003032*T))%360
            M=357.52911+T*(35999.05029-0.0001537*T); e=0.016708634-T*(0.000042037+0.0000001267*T)
            C=math.sin(math.radians(M))*(1.914602-T*(0.004817+0.000014*T))+math.sin(math.radians(2*M))*(0.019993-0.000101*T)+math.sin(math.radians(3*M))*0.000289
            tl=L0+C; om=125.04-1934.136*T; lam=tl-0.00569-0.00478*math.sin(math.radians(om))
            eps0=23+(26+((21.448-T*(46.815+T*(0.00059-T*0.001813))))/60)/60; eps=eps0+0.00256*math.cos(math.radians(om))
            dec=math.degrees(math.asin(math.sin(math.radians(eps))*math.sin(math.radians(lam))))
            y=math.tan(math.radians(eps/2))**2
            eot=4*math.degrees(y*math.sin(2*math.radians(L0))-2*e*math.sin(math.radians(M))+4*e*y*math.sin(math.radians(M))*math.cos(2*math.radians(L0))-0.5*y*y*math.sin(4*math.radians(L0))-1.25*e*e*math.sin(2*math.radians(M)))
            cosH=(math.cos(math.radians(90.833))/(math.cos(math.radians(LAT))*math.cos(math.radians(dec)))-math.tan(math.radians(LAT))*math.tan(math.radians(dec)))
            H=math.degrees(math.acos(cosH))
            t_new=(720-4*(LON+sign*(-H))*(-1 if False else 1)) if False else None
            # solar noon minutes UTC
            noon=720-4*LON-eot
            t_min=noon+sign*4*H
            t_utc=t_min/60
        az=math.degrees(math.acos(math.sin(math.radians(dec))/math.cos(math.radians(LAT))))
        if sign>0: az=360-az
        out[event]=(t_utc,az)
        out['noon_utc']=noon/60; out['dec']=dec
    return out
def israel_offset(d):
    y=d.year
    last_sun_mar=max(datetime.date(y,3,day) for day in range(25,32) if datetime.date(y,3,day).weekday()==6)
    start=last_sun_mar-datetime.timedelta(days=2)
    end=max(datetime.date(y,10,day) for day in range(25,32) if datetime.date(y,10,day).weekday()==6)
    return 3 if start<=d<end else 2
def fmt(h): 
    m=int(round(h*60)); return f"{(m//60)%24:02d}:{m%60:02d}"
rows=[]
dates=[datetime.date(2026,m,21) for m in range(1,13)]+[datetime.date(2026,3,20),datetime.date(2026,6,21),datetime.date(2026,9,23),datetime.date(2026,12,21)]
for d in sorted(set(dates)):
    c=calc(d); off=israel_offset(d)
    sr,saz=c['sunrise']; ss,sazs=c['sunset']; noon=c['noon_utc']
    alt=90-LAT+c['dec']
    rows.append([d.isoformat(),'IDT (UTC+3)' if off==3 else 'IST (UTC+2)',fmt(sr+off),round(saz),fmt(ss+off),round(sazs),fmt(noon+off),round(alt,1),fmt(ss-sr)])
w=csv.writer(open(sys.argv[1],'w',newline='',encoding='utf-8'))
w.writerow(['date','israel_clock','sunrise_local','sunrise_azimuth_deg','sunset_local','sunset_azimuth_deg','solar_noon_local','noon_sun_altitude_deg','day_length_hh_mm'])
w.writerows(rows)
for r in rows: print(r)
