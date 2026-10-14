# -*- coding: utf-8 -*-
"""HAD-527: the Bank of Israel policy rate (official SDMX series MNT_RIB_BOI_D, daily) reduced to its decisions (every change
and its date) since 2015, plus prime = rate + 1.5 (the Israeli banks' prime convention).
python build_boi_data.py -> plugins/nadlan-config/assets/instruments/data/boi-rate.json"""
import csv
import io
import json
import os
import time
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "instruments", "data", "boi-rate.json")
U = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/BR/1.0/MNT_RIB_BOI_D?c%5BTIME_PERIOD%5D=ge:2015-01-01&format=csv"
raw = urllib.request.urlopen(urllib.request.Request(U, headers={"User-Agent": "Mozilla/5.0 NadLan-instruments"}), timeout=120).read().decode("utf-8")
rows = list(csv.reader(io.StringIO(raw)))
head = rows[0]; ti, vi = head.index("TIME_PERIOD"), head.index("OBS_VALUE")
series = sorted((r[ti], float(r[vi])) for r in rows[1:] if r[vi])
changes, last = [], None
for d, v in series:
    if v != last:
        changes.append({"from": d, "rate": v, "prime": round(v + 1.5, 2)})
        last = v
data = {"key": "boi", "source": "בנק ישראל, ריבית בנק ישראל (סדרה MNT_RIB_BOI_D)", "fetched": time.strftime("%Y-%m-%d"), "asof": series[-1][0],
        "rate": series[-1][1], "prime": round(series[-1][1] + 1.5, 2), "changes": changes}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("as of", data["asof"], "rate", data["rate"], "prime", data["prime"], "| decisions since 2015:", len(changes), "| last 4:", changes[-4:])
