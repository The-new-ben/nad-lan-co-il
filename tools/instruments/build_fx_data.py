# -*- coding: utf-8 -*-
"""HAD-575 / Kikar tools #5: the Bank of Israel representative exchange rates (official SDMX series RER_USD_ILS, RER_EUR_ILS,
RER_GBP_ILS, daily) -> plugins/nadlan-config/assets/instruments/data/boi-fx.json (the latest rate of each, its date, and the
last 30 days for a range).   python tools/instruments/build_fx_data.py"""
import csv, io, json, os, time, urllib.request
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "instruments", "data", "boi-fx.json")
since = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 40 * 86400))
fx = {}
for cur in ("USD", "EUR", "GBP"):
    u = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_%s_ILS?c%%5BTIME_PERIOD%%5D=ge:%s&format=csv" % (cur, since)
    raw = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-instruments"}), timeout=120).read().decode("utf-8")
    rows = list(csv.reader(io.StringIO(raw))); head = rows[0]; ti, vi = head.index("TIME_PERIOD"), head.index("OBS_VALUE")
    s = sorted((r[ti], float(r[vi])) for r in rows[1:] if r[vi])
    last30 = [v for d, v in s][-30:]
    fx[cur] = {"rate": s[-1][1], "date": s[-1][0], "min30": min(last30), "max30": max(last30)}
data = {"key": "fx", "source": "Bank of Israel representative exchange rates (series RER_<currency>_ILS)", "url": "https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/",
        "fetched": time.strftime("%Y-%m-%d"), "fx": fx}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(json.dumps(fx))
