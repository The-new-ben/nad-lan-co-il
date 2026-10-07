"""Geocode the Rova 4 urban-renewal addresses with OpenStreetMap Nominatim.

Design prototype helper (7.10.2026). Stdlib only. One request per second, descriptive User-Agent,
results cached in raw/nominatim.json (re-runs reuse the cache; delete an entry to re-query it).
Source rows: docs/content/rova-4-2026-10/facts.md (R41-R51) and
docs/research/2026-10-07-kikar-prices/press-facts.md section 5 (U1-U12) and D1 (Henkin 3).
"""
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "raw", "nominatim.json")
UA = "nad-lan.co.il-area-map-prototype/1.0 (design preview for nad-lan.co.il; one-off, 1 req/s)"
CITY = "תל אביב-יפו"

# key -> list of query strings tried in order (first hit with a house number wins)
QUERIES = {
    "zlotisti-4": ["זלוציסטי 4, תל אביב-יפו"],
    "remez-27": ["דוד רמז 27, תל אביב-יפו", "רמז 27, תל אביב-יפו"],
    "jabotinsky-152": ["ז'בוטינסקי 152, תל אביב-יפו", "זבוטינסקי 152, תל אביב-יפו"],
    "beeri-36": ["בארי 36, תל אביב-יפו"],
    "beeri-56": ["בארי 56, תל אביב-יפו"],
    "jabotinsky-135": ["ז'בוטינסקי 135, תל אביב-יפו", "זבוטינסקי 135, תל אביב-יפו"],
    "jabotinsky-137": ["ז'בוטינסקי 137, תל אביב-יפו", "זבוטינסקי 137, תל אביב-יפו"],
    "jabotinsky-133": ["ז'בוטינסקי 133, תל אביב-יפו", "זבוטינסקי 133, תל אביב-יפו"],
    "remez-44": ["דוד רמז 44, תל אביב-יפו", "רמז 44, תל אביב-יפו"],
    "remez-42": ["דוד רמז 42, תל אביב-יפו", "רמז 42, תל אביב-יפו"],
    "remez-22": ["דוד רמז 22, תל אביב-יפו", "רמז 22, תל אביב-יפו"],
    "remez-25": ["דוד רמז 25, תל אביב-יפו", "רמז 25, תל אביב-יפו"],
    "lissin-27": ["ליסין 27, תל אביב-יפו"],
    "sharet-30": ["משה שרת 30, תל אביב-יפו", "שרת 30, תל אביב-יפו"],
    "zichron-yaakov-16": ["זכרון יעקב 16, תל אביב-יפו", "זיכרון יעקב 16, תל אביב-יפו"],
    "henkin-3": ["חנקין 3, תל אביב-יפו"],
}


def nominatim(q):
    params = {
        "format": "json", "q": q, "countrycodes": "il", "addressdetails": "1",
        "limit": "3", "accept-language": "he",
    }
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "he"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8")), url


def main():
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE, encoding="utf-8"))
    for key, qs in QUERIES.items():
        if key in cache and cache[key].get("results"):
            continue
        attempts = []
        chosen = None
        for q in qs:
            res, url = nominatim(q)
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            attempts.append({"q": q, "url": url, "retrieved": now, "results": res})
            time.sleep(1.1)
            hit = [x for x in res if x.get("address", {}).get("house_number")]
            if hit:
                chosen = len(attempts) - 1
                break
        cache[key] = {"attempts": attempts, "chosen_attempt": chosen,
                      "results": attempts[chosen]["results"] if chosen is not None else []}
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(key, "hit" if chosen is not None else "NO HOUSE-NUMBER HIT")
    for key, v in cache.items():
        r = v["results"]
        top = r[0] if r else None
        print(key, top and (top["lat"], top["lon"], top.get("addresstype"), top["display_name"][:110]))


if __name__ == "__main__":
    main()
