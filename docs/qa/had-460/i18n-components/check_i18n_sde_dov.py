# -*- coding: utf-8 -*-
"""Checks for the Sde Dov component translations (7.10.2026, HAD-460): PriceGuide sde-dov-prices.<lang>.json and AreaMap
sde-dov.<lang>.json against their Hebrew files. Same checks as check_i18n.py (the Rova 4 run), whose helpers it reuses;
two differences:
 - month names are read as numbers in every language ("April 2026", "avril 2026", "в апреле 2026", "نيسان 2026" and the
   Hebrew "במרץ 2026" -> 4.2026 / 3.2026), not only October, so a month written as a word must still carry the same date;
 - the PriceGuide scan allows the word "developer": the Hebrew file itself says "דוחות היזמים" / "לפי היזם" (the counts of
   both are printed).
Extra: Hebrew letters anywhere in the rendered HTML (data-cfg included) and in any non-metadata string of the file.
Prints a JSON report."""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_i18n as C  # noqa: E402

R, M, PG, AM = C.R, C.M, C.PG, C.AM
L = ("en", "fr", "ru", "ar")
WA = "972525101555"

MONTHS = {
    "he": ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
    "ru": ["январ[а-яё]*", "феврал[а-яё]*", "март[а-яё]*", "апрел[а-яё]*", "ма[йея][а-яё]*", "июн[а-яё]*", "июл[а-яё]*",
           "август[а-яё]*", "сентябр[а-яё]*", "октябр[а-яё]*", "ноябр[а-яё]*", "декабр[а-яё]*"],
    "ar": ["كانون الثاني", "شباط", "آذار", "نيسان", "أيار", "حزيران", "تموز", "آب", "أيلول", "تشرين الأول", "تشرين الثاني", "كانون الأول"],
}
MRE = {lang: [(re.compile(r"(?:(\d{1,2})\s+)?" + ("" if lang in ("he", "ar") else r"(?<![^\W\d_])") + "(?:" + m + r")\s+(\d{4})"), i + 1)
              for i, m in enumerate(ms)] for lang, ms in MONTHS.items()}
NUM = C.NUM
SEP = C.SEP


def months(s, lang):
    for rx, n in MRE[lang]:
        s = rx.sub(lambda m: ("%s.%d.%s" % (m.group(1), n, m.group(2))) if m.group(1) else ("%d.%s" % (n, m.group(2))), s)
    return s


def nums(s, lang):
    s = months(s, lang)
    out = []
    for tok in NUM.findall(s):
        tok = tok.rstrip(",.")
        g, dec = SEP[lang]
        t = tok.replace(g, "")
        if lang in ("fr", "ru"):
            t = t.replace(" ", "").replace(" ", "").replace(",", ".")
        else:
            t = t.replace(",", "")
        out.append(".".join(p.lstrip("0") or "0" for p in t.split(".")))
    return out


C.nums = nums  # compare() reads the module global

HEB = re.compile(r"[֐-׿]")
META = {"sources", "src", "note", "tax_src", "gap_src", "research", "page", "updated"}


def hebrew_in_file(d):
    hits = []

    def walk(x, path, meta):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, path + (k,), meta or k in META)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, path + (i,), meta)
        elif isinstance(x, str) and not meta and HEB.search(x):
            hits.append((path, x[:80]))
    walk(d, (), False)
    return hits


DEVWORD = {"he": r"יזמ|יזם", "en": r"developer", "fr": r"promoteur", "ru": r"застройщик", "ar": r"المطوّر|المطور|للمطوّرين|مطوّر"}


def main():
    rep = {"price_guide": {}, "area_map": {}}
    he = json.load(io.open(os.path.join(PG, "sde-dov-prices.json"), encoding="utf-8"))
    uhe = R.ui(he)
    he_ui = [n for k, v in uhe.items() if isinstance(v, str) and k not in ("lang", "dir", "loc", "grp", "dec") for n in nums(v, "he")]
    hh = R.html(he, WA)
    rep["price_guide"]["he"] = {"default": R.default_result(he, uhe), "render_bytes": len(hh),
                                "dev_word_visible": len(re.findall(DEVWORD["he"], C.visible(hh))),
                                "rows": sum(len(g["rows"]) for g in he["groups"]), "sources": len(he["sources"])}
    for lang in L:
        tr = json.load(io.open(os.path.join(PG, "sde-dov-prices.%s.json" % lang), encoding="utf-8"))
        u = R.ui(tr)
        tr_ui = [n for k, v in u.items() if isinstance(v, str) and k not in ("lang", "dir", "loc", "grp", "dec") for n in nums(v, lang)]
        r = C.compare(he, tr, C.PG_TEXT, lang, he_ui + nums(he["updated_he"], "he"), tr_ui + nums(tr["updated_shown"], lang))
        miss_ui = [k for k in R.UI_HE if k not in (tr.get("ui") or {})]
        miss_js = [k for k in R.UI_HE["js"] if k not in (tr["ui"].get("js") or {})]
        bad_ph = [k for k in ("u_m2", "u_floor", "u_mil", "u_ils", "u_pm2", "approx") if u[k].count("{n}") != 1]
        bad_js = [k for k in R.UI_HE["js"] if C.ph(uhe["js"][k]) != C.ph(u["js"][k])]
        js_bad = {k: (nums(uhe["js"][k], "he"), nums(u["js"][k], lang)) for k in R.UI_HE["js"]
                  if sorted(nums(uhe["js"][k], "he")) != sorted(nums(u["js"][k], lang))}
        h = R.html(tr, WA)
        r.update({"lang": u["lang"], "dir": u["dir"], "loc": u["loc"], "grp": "U+%04X" % ord(u["grp"]), "dec": u["dec"],
                  "rows": sum(len(g["rows"]) for g in tr["groups"]), "sources": len(tr["sources"]), "open_groups": tr.get("open_groups"),
                  "ui_missing": miss_ui, "js_missing": miss_js, "unit_patterns_bad": bad_ph, "js_placeholders_bad": bad_js,
                  "js_number_mismatch": js_bad, "render_bytes": len(h), "default": R.default_result(tr, u),
                  "scan": C.scan(h, lang, allow_dev=True), "dev_word_visible": len(re.findall(DEVWORD[lang], C.visible(h), re.I)),
                  "hebrew_in_full_html": HEB.findall(h)[:5], "hebrew_in_file_text": hebrew_in_file(tr),
                  "links": u["links"], "see": tr["see"], "updated_shown": tr["updated_shown"]})
        rep["price_guide"][lang] = r
    # area map
    he = M.load("sde-dov")
    uh = M.ui(he)

    def uinums(u, lang):
        out = []
        for k, v in u.items():
            if k in ("lang", "dir", "colon"):
                continue
            if isinstance(v, str):
                out += nums(v, lang)
        for k, v in u["js"].items():
            if isinstance(v, str):
                out += nums(v, lang)
            elif isinstance(v, dict):
                for x in v.values():
                    out += nums(x, lang)
        for k, lab, _ in u["chips"]:
            out += nums(lab, lang)
        return out
    hm = M.html(he)
    rep["area_map"]["he"] = {"render_bytes": len(hm), "projects": len(he["projects"]), "places": len(he["places"])}
    for lang in L:
        tr = M.load("sde-dov." + lang)
        u = M.ui(tr)
        r = C.compare(he, tr, C.AM_TEXT, lang, uinums(uh, "he"), uinums(u, lang))
        h = M.html(tr)
        miss = [k for k in M.UI if k != "js" and k not in tr["ui"]]
        miss_js = [k for k in M.UI["js"] if k not in tr["ui"]["js"]]
        miss_cats = [k for k in M.UI["js"]["cats"] if k not in tr["ui"]["js"].get("cats", {})]
        miss_loc = [k for k in M.UI["js"]["loc"] if k not in tr["ui"]["js"].get("loc", {})]
        types = sorted({pl[1] for pl in tr["places"]})
        no_plural = [t for t in types if t not in tr["ui"].get("plural", {})]
        same_geo = ([(p["id"], p["lat"], p["lng"], p["hero"]) for p in he["projects"]] ==
                    [(p["id"], p["lat"], p["lng"], p["hero"]) for p in tr["projects"]] and
                    [(p[0], p[4], p[5], p[6]) for p in he["places"]] == [(p[0], p[4], p[5], p[6]) for p in tr["places"]] and
                    he["boundary"] == tr["boundary"] and he["view"] == tr["view"])
        r.update({"lang": u["lang"], "dir": u["dir"], "ui_missing": miss, "js_missing": miss_js, "cats_missing": miss_cats,
                  "loc_missing": miss_loc, "types": types, "types_without_plural": no_plural, "ids_coords_order_identical": same_geo,
                  "project_urls": [p["url"] for p in tr["projects"]], "render_bytes": len(h),
                  "scan": C.scan(h, lang, allow_dev=True), "hebrew_in_full_html": HEB.findall(h)[:5],
                  "hebrew_in_file_text": hebrew_in_file(tr)})
        rep["area_map"][lang] = r
    print(json.dumps(rep, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
