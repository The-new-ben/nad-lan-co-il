# -*- coding: utf-8 -*-
"""Checks for the Rova 4 component translations (7.10.2026, HAD-460): PriceGuide rova-4.<lang>.json and AreaMap
rova-4.<lang>.json against their Hebrew files. Prints a JSON report.
 1. non-text fields identical (every key, number, date, src, id, position); same structure
 2. numbers per string: every number in each Hebrew string appears in its translation and vice versa (values compared after
    normalising each language's separators; "7 October 2026" / "7 octobre 2026" read as 7.10.2026)
 3. numbers per file: the multiset of all numbers in the Hebrew file = that of the language file (text leaves + effective ui)
 4. placeholders, scan (dashes, "!", source names, banned words, leftover Hebrew), render test"""
import collections
import html as _h
import io
import json
import os
import re
import sys

REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
PG = os.path.join(REPO, "scripts", "project-stage", "price_guide")
AM = os.path.join(REPO, "scripts", "project-stage", "area_map")
sys.path.insert(0, PG)
sys.path.insert(0, AM)
import render as R  # noqa: E402
import render_map as M  # noqa: E402

L = ("en", "fr", "ru", "ar")
SEP = {"he": (",", "."), "en": (",", "."), "ar": (",", "."), "fr": ("\u202f", ","), "ru": ("\u00a0", ",")}
MONTH = re.compile(r"\b(\d{1,2}) (October|octobre) (\d{4})\b")
NUM = re.compile(r"\d[\d,.\u00a0\u202f]*\d|\d")


def nums(s, lang):
    s = MONTH.sub(lambda m: "%s.10.%s" % (m.group(1), m.group(3)), s)
    g, dec = SEP[lang]
    out = []
    for tok in NUM.findall(s):
        tok = tok.rstrip(",.")
        t = tok.replace(g, "")
        if lang in ("fr", "ru"):
            t = t.replace("\u00a0", "").replace("\u202f", "")
            t = t.replace(",", ".")
        else:
            t = t.replace(",", "")
        parts = t.split(".")
        out.append(".".join(p.lstrip("0") or "0" for p in parts))
    return out


def leaves(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, path + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, path + (i,))
    else:
        yield path, x


def norm_path(p):
    if len(p) == 3 and p[0] == "places":  # a place row is a list: keep the column index
        return ("places", "#", p[2])
    return tuple("#" if isinstance(k, int) else k for k in p)


# text paths (with # for any list index); everything else must be identical
PG_TEXT = {("title",), ("calc_title",), ("answer",), ("src_line",), ("tiles", "#", "big"), ("tiles", "#", "small"),
           ("groups", "#", "name"), ("groups", "#", "rows", "#", "what"), ("groups", "#", "rows", "#", "sub"),
           ("groups", "#", "rows", "#", "m2"), ("groups", "#", "rows", "#", "price"), ("calc", "modes", "#", "label"),
           ("calc", "modes", "#", "why"), ("calc", "gap"), ("see", "#", "text"), ("see", "#", "href"),
           ("kinds", "deal"), ("kinds", "ask"), ("kinds", "est"), ("kinds", "mkt"), ("kinds", "med")}
AM_TEXT = {("kicker",), ("title",), ("lead",), ("caption",), ("projects", "#", "name"), ("projects", "#", "fact"),
           ("projects", "#", "dev"), ("projects", "#", "url"), ("renewal", "#", "address"), ("renewal", "#", "before"),
           ("renewal", "#", "after"), ("renewal", "#", "dev"), ("renewal", "#", "stage"), ("renewal", "#", "note"),
           ("places", "#", 1), ("places", "#", 2), ("places", "#", 3)}

SOURCES = ["Globes", "Bizportal", "Calcalist", "ynet", "Madlan", "Yad2", "nadlan.gov.il", "Mako", "TheMarker", "Sotheby",
           "גלובס", "ביזפורטל", "כלכליסט", "מדלן", "יד2", "דה מרקר"]
BANNED = {"en": ["interface", "platform", "simulation", "demo", "engine", "broker", "best ", "unique", "perfect", "atlas"],
          "fr": ["interface", "plateforme", "simulation", "démo", "moteur", "courtier", "meilleur", "unique", "parfait", "atlas"],
          "ru": ["интерфейс", "платформ", "симуляц", "демо", "движок", "брокер", "маклер", "лучш", "уникальн", "идеальн", "атлас"],
          "ar": ["واجهة", "منصة", "محاكاة", "تجريبي", "محرك", "سمسار", "الأفضل", "فريد", "مثالي", "أطلس"]}
DEV = {"en": "developer", "fr": "promoteur", "ru": "застройщик", "ar": "مطو"}


def visible(h):
    h = re.sub(r'data-cfg="[^"]*"', "", h)
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S)
    return _h.unescape(re.sub(r"<[^>]+>", " ", h))


def compare(he, tr, text_paths, lang, he_ui_nums, tr_ui_nums):
    res = {"missing_keys": [], "extra_keys": [], "changed": [], "num_mismatch": [], "strings": 0}
    hl, tl = dict(leaves(he)), dict(leaves(tr))
    for p in hl:
        if p and p[0] in ("ui",):
            continue
        if p not in tl and p[0] != "facts":
            res["missing_keys"].append(p)
    for p in tl:
        if p and p[0] in ("ui", "updated_shown"):
            continue
        if p not in hl and not (p[0] == "facts"):
            res["extra_keys"].append(p)
    for p, v in hl.items():
        if p and p[0] == "ui":
            continue
        if p[0] == "facts":
            continue
        np_ = norm_path(p)
        if np_ in text_paths:
            if isinstance(v, str) and p in tl and isinstance(tl[p], str):
                res["strings"] += 1
                if np_[-1] == "href" or np_[-1] == "url":
                    continue
                a, b = sorted(nums(v, "he")), sorted(nums(tl[p], lang))
                if a != b:
                    res["num_mismatch"].append({"path": p, "he": v, "tr": tl[p], "he_nums": a, "tr_nums": b})
            elif v != tl.get(p):
                res["changed"].append(p)
        else:
            if tl.get(p, object()) != v:
                res["changed"].append(p)
    # facts: compare values in order
    if "facts" in he:
        for (hk, hv), (tk, tv) in zip(he["facts"].items(), tr.get("facts", {}).items()):
            res["strings"] += 2
            for a, b in ((hk, tk), (hv, tv)):
                if sorted(nums(a, "he")) != sorted(nums(b, lang)):
                    res["num_mismatch"].append({"path": ("facts",), "he": a, "tr": b})
    # whole file
    fa = collections.Counter(n for p, v in hl.items() if isinstance(v, str) and norm_path(p) in text_paths
                             and norm_path(p)[-1] not in ("href", "url") for n in nums(v, "he"))
    fb = collections.Counter(n for p, v in tl.items() if isinstance(v, str) and norm_path(p) in text_paths
                             and norm_path(p)[-1] not in ("href", "url") for n in nums(v, lang))
    for k, v in he.get("facts", {}).items():
        fa.update(nums(k + " " + v, "he"))
    for k, v in tr.get("facts", {}).items():
        fb.update(nums(k + " " + v, lang))
    fa.update(he_ui_nums)
    fb.update(tr_ui_nums)
    res["file_numbers"] = {"he_count": sum(fa.values()), "tr_count": sum(fb.values()),
                           "only_he": dict(fa - fb), "only_tr": dict(fb - fa)}
    return res


def scan(h, lang, allow_dev=False):
    v = visible(h)
    out = {}
    out["em_en_dash"] = [c for c in ("\u2014", "\u2013") if c in v]
    out["exclamation"] = v.count("!")
    out["sources"] = [s for s in SOURCES if s.lower() in v.lower()]
    low = v.lower()
    out["banned"] = [w for w in BANNED[lang] if re.search(r"(?<!\w)" + re.escape(w.strip()) + r"(?!\w)" if lang in ("en", "fr") else re.escape(w), low)]
    if not allow_dev and DEV[lang] in low:
        out["banned"].append(DEV[lang])
    if lang == "ar":
        out["broker_word"] = len(re.findall(r"(?<![\u0621-\u064a])(?:ال)?وسيط(?!ة)", v))
    out["hebrew_left"] = re.findall(r"[\u0590-\u05ff][\u0590-\u05ff\s\"'״׳-]*", v)[:5]
    return out


def ph(s):
    return sorted(re.findall(r"\{\w+\}", s))


def main():
    rep = {"price_guide": {}, "area_map": {}}
    he = json.load(io.open(os.path.join(PG, "rova-4.json"), encoding="utf-8"))
    uhe = R.ui(he)
    he_ui = [n for k, v in uhe.items() if isinstance(v, str) and k not in ("lang", "dir", "loc", "grp", "dec") for n in nums(v, "he")]
    for lang in L:
        tr = json.load(io.open(os.path.join(PG, "rova-4.%s.json" % lang), encoding="utf-8"))
        u = R.ui(tr)
        tr_ui = [n for k, v in u.items() if isinstance(v, str) and k not in ("lang", "dir", "loc", "grp", "dec") for n in nums(v, lang)]
        r = compare(he, tr, PG_TEXT, lang, he_ui + nums(he["updated_he"], "he"), tr_ui + nums(tr["updated_shown"], lang))
        # placeholders and ui completeness
        miss_ui = [k for k in R.UI_HE if k not in (tr.get("ui") or {})]
        miss_js = [k for k in R.UI_HE["js"] if k not in (tr["ui"].get("js") or {})]
        bad_ph = [k for k in ("u_m2", "u_floor", "u_mil", "u_ils", "u_pm2", "approx") if u[k].count("{n}") != 1]
        bad_js = [k for k in R.UI_HE["js"] if ph(R.ui(he)["js"][k]) != ph(u["js"][k])]
        ui_nums = {k: (nums(R.UI_HE[k], "he") if isinstance(R.UI_HE[k], str) else None,
                       nums(u[k], lang) if isinstance(u[k], str) else None)
                   for k in R.UI_HE if isinstance(R.UI_HE[k], str) and k not in ("lang", "dir", "loc", "grp", "dec")}
        ui_bad = {k: v for k, v in ui_nums.items() if sorted(v[0]) != sorted(v[1])}
        js_bad = {k: (nums(R.ui(he)["js"][k], "he"), nums(u["js"][k], lang)) for k in R.UI_HE["js"]
                  if sorted(nums(R.ui(he)["js"][k], "he")) != sorted(nums(u["js"][k], lang))}
        h = R.html(tr, "972525101555")
        r.update({"lang": u["lang"], "dir": u["dir"], "loc": u["loc"], "grp": "U+%04X" % ord(u["grp"]), "dec": u["dec"],
                  "ui_missing": miss_ui, "js_missing": miss_js, "unit_patterns_bad": bad_ph, "js_placeholders_bad": bad_js,
                  "ui_number_mismatch": ui_bad, "js_number_mismatch": js_bad, "render_bytes": len(h),
                  "default": R.default_result(tr, u), "scan": scan(h, lang), "links": u["links"], "see": tr["see"],
                  "updated_shown": tr["updated_shown"]})
        rep["price_guide"][lang] = r
    rep["price_guide"]["he_default"] = R.default_result(he, R.ui(he))
    # area map
    he = M.load("rova-4")
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
    for lang in L:
        p = os.path.join(AM, "rova-4.%s.json" % lang)
        if not os.path.exists(p):
            continue
        tr = M.load("rova-4." + lang)
        u = M.ui(tr)
        r = compare(he, tr, AM_TEXT, lang, uinums(uh, "he"), uinums(u, lang))
        h = M.html(tr)
        miss = [k for k in M.UI if k != "js" and k not in tr["ui"]]
        miss_js = [k for k in M.UI["js"] if k not in tr["ui"]["js"]]
        miss_cats = [k for k in M.UI["js"]["cats"] if k not in tr["ui"]["js"].get("cats", {})]
        miss_loc = [k for k in M.UI["js"]["loc"] if k not in tr["ui"]["js"].get("loc", {})]
        types = sorted({pl[1] for pl in tr["places"]})
        no_plural = [t for t in types if t not in tr["ui"].get("plural", {})]
        lrt = tr["ui"]["js"].get("lrt", "")
        lrt_hits = [pl[2] for pl in tr["places"] if pl[0] == "transit" and lrt and lrt in pl[1]]
        fx_ok = all(k in lrt_hits for k in tr.get("facts", {}))
        r.update({"lang": u["lang"], "dir": u["dir"], "ui_missing": miss, "js_missing": miss_js, "cats_missing": miss_cats,
                  "loc_missing": miss_loc, "types_without_plural": no_plural, "light_rail_stops": lrt_hits,
                  "facts_shown_on_a_light_rail_card": fx_ok, "render_bytes": len(h),
                  "hebrew_in_visible": scan(h, lang, allow_dev=True)})
        rep["area_map"][lang] = r
    print(json.dumps(rep, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
