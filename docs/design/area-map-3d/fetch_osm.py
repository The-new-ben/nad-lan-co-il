"""One polite Overpass query for the Rova 4 bounding box: daily-life places + the four boundary lines.

Design prototype helper (7.10.2026). Stdlib only. Saves the raw answer to raw/overpass.json with the
retrieval time. Re-running overwrites it (run it rarely; the data is OpenStreetMap, ODbL).
"""
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "raw", "overpass.json")
UA = "nad-lan.co.il-area-map-prototype/1.0 (design preview for nad-lan.co.il; one query)"
ENDPOINTS = ["https://overpass-api.de/api/interpreter", "https://z.overpass-api.de/api/interpreter"]
BBOX = "32.070,34.775,32.104,34.806"  # south, west, north, east (a margin around Rova 4)

QUERY = f"""[out:json][timeout:120][bbox:{BBOX}];
(
  nwr["amenity"~"^(school|kindergarten|cafe|pharmacy)$"];
  nwr["shop"="supermarket"];
  nwr["leisure"="park"];
  nwr["railway"~"^(station|halt|stop|tram_stop)$"];
  nwr["public_transport"="station"];
)->.pois;
.pois out center tags;
(
  way["highway"]["name"="אבן גבירול"];
  way["highway"]["name"~"שאול המלך"];
  way["highway"="motorway"];
  way["waterway"="river"];
  relation["boundary"]["name"~"רובע"];
)->.edges;
.edges out tags geom;
"""


def main():
    data = urllib.parse.urlencode({"data": QUERY}).encode("utf-8")
    payload = None
    for attempt in range(6):  # the public server was busy on 7.10.2026; wait and retry politely
        endpoint = ENDPOINTS[attempt % len(ENDPOINTS)]
        try:
            req = urllib.request.Request(endpoint, data=data, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                payload = json.loads(r.read().decode("utf-8"))
            ENDPOINT = endpoint
            break
        except Exception as exc:  # 504 / 429 / dispatcher timeout page
            print("attempt", attempt + 1, endpoint, "failed:", exc)
            time.sleep(30)
    if payload is None:
        raise SystemExit("Overpass unavailable")
    payload["_retrieved"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload["_endpoint"] = ENDPOINT
    payload["_query"] = QUERY
    json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print("elements", len(payload["elements"]), "retrieved", payload["_retrieved"])


if __name__ == "__main__":
    main()
