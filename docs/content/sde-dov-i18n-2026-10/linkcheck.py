# -*- coding: utf-8 -*-
"""HAD-439 Stage A: GET-check every internal link the Sde Dov language versions may use, and their language equivalents.

    python docs/content/sde-dov-i18n-2026-10/linkcheck.py      -> source/linkcheck-20261007.json

Public GETs only, without following redirects (a 301/302 is NOT a valid link target), one request per 0.4 s.
The candidates: every internal link of the two Hebrew pages, its /<lang>/ path, the -<lang> variant of every project page,
and the language pages the packets may offer as optional extras.
"""
import datetime, io, json, os, sys, time, urllib.error, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://nad-lan.co.il"
UA = {"User-Agent": "nad-lan.co.il i18n link check (HAD-439; public pages, 1 req/0.4 s)"}
LANGS = ("en", "fr", "ru", "ar")

HE_PATHS = ["/sde-dov/", "/sde-dov/prices/", "/real-estate-lawyer/", "/sde-dov/eshkol/", "/sde-dov/merkaz/",
            "/sde-dov/tzafon/", "/sde-dov/hotels/", "/sde-dov/parks/", "/sde-dov/marina/", "/sde-dov/transport/",
            "/sde-dov/institutions/", "/sde-dov/employment/", "/purchase-tax-calculator/", "/mortgage-calculator/",
            "/investment-apartment/", "/new-projects/", "/tel-aviv-plans/", "/north-tel-aviv/", "/north-tel-aviv/rova-4/",
            "/ramat-aviv/"]
PROJECTS = ["rainbow-tel-aviv", "first-sde-dov", "ashira-sde-dov", "dimri-yama-sde-dov", "zohi-sde-dov",
            "gindi-vogue-sde-dov", "utopia-sde-dov", "shikun-binui-sde-dov", "migdalei-hayam-sde-dov", "hamedina"]
EXTRAS = ["/{l}/new-projects/", "/{l}/buy-property-in-israel/", "/{l}/brokers/", "/{l}/guides/", "/{l}/developer-deals/",
          "/{l}/property-value-estimator/", "/{l}/"]
EN_ONLY = ["/israel-purchase-tax-foreign-residents/", "/israel-mortgage-non-residents/"]


class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def get(path):
    op = urllib.request.build_opener(NoRedir)
    try:
        r = op.open(urllib.request.Request(SITE + path, headers=UA), timeout=40)
        return r.status, r.headers.get("Location") or ""
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location") or ""
    except Exception as e:  # network error
        return str(e), ""


def candidates():
    out = list(HE_PATHS)
    for p in HE_PATHS:
        out += ["/%s%s" % (l, p) for l in LANGS]
    for s in PROJECTS:
        out.append("/projects/%s/" % s)
        out += ["/projects/%s-%s/" % (s, l) for l in LANGS]
    for e in EXTRAS:
        out += [e.format(l=l) for l in LANGS]
    out += EN_ONLY
    seen, res = set(), []
    for u in out:
        if u not in seen:
            seen.add(u)
            res.append(u)
    return res


def main():
    res = {}
    for u in candidates():
        st, loc = get(u)
        res[u] = {"status": st, "location": loc}
        print(st, u, loc)
        time.sleep(0.4)
    doc = {"checked_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "no_redirect_follow": True,
           "results": res}
    os.makedirs(os.path.join(HERE, "source"), exist_ok=True)
    io.open(os.path.join(HERE, "source", "linkcheck-20261007.json"), "w", encoding="utf-8").write(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print("200:", sum(1 for v in res.values() if v["status"] == 200), "of", len(res))


if __name__ == "__main__":
    main()
