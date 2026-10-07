# -*- coding: utf-8 -*-
"""AreaMap (design system component, 7.10.2026): a 3D map of a neighbourhood with the projects on the site, the urban
renewal around them and daily life (schools, parks, shops, transport), for an area page and later project pages.
One source for the design system preview and for the plugin's server-rendered section:
  html(d, sfx="") -> the section's markup: heading, filters, the map frame (a calm placeholder until the map loads),
                     the caption with the OpenStreetMap credit, and a server-rendered list of every place (for search,
                     screen readers, and as the fallback when the map cannot load). The data rides in data-cfg.
  CSS, JS         -> the component's style (every rule starts with .nlam) and its one classic script.
The script loads nothing heavy up front: MapLibre GL JS 5.24.0 (cdnjs, SRI), the RTL text plugin and the tiles are
requested only when the section comes within 300px of the screen. Several instances can share one page (sfx).
Data: area_map/<key>.json (made by make_data.py from docs/design/area-map-3d/data.json, where every item keeps its
source and retrieval time); a language version is <key>.<lang>.json with a "ui" object (v1.1, see ui()). v1.1 also drops
the filter and the list heading of a layer that has no places. CSS: the LTR mirror is a separate [dir="ltr"] block, so
the Hebrew rules are untouched."""
import html as _h
import io
import json
import os
import re

E = lambda s: _h.escape(str(s), quote=True)

NUMRE = re.compile(r"\d(?:[\d,.:]*\d)?(?:-\d(?:[\d,.]*\d)?)?")

CHIPS = [("projects", "פרויקטים", "pill"), ("renewal", "התחדשות עירונית", "sq"), ("edu", "בתי ספר וגנים", ""),
         ("parks", "פארקים", ""), ("shop", "קניות", ""), ("transit", "תחבורה", "")]
PLURAL = {"בית ספר": "בתי ספר", "גן ילדים": "גני ילדים", "פארק": "פארקים", "סופרמרקט": "סופרמרקטים",
          "בית קפה": "בתי קפה", "בית מרקחת": "בתי מרקחת", "תחנת הרכבת הקלה": "תחנות הרכבת הקלה",
          "תחנת רכבת": "תחנות רכבת", "מסוף אוטובוסים": "מסופי אוטובוסים"}
UI = {
    "chips_label": "מה מוצג", "wait": "המפה נטענת", "reset": "חזרה למבט הכללי", "close": "סגירה",
    "list": "כל הפרויקטים והמקומות שבמפה", "fail": "המפה אינה זמינה כרגע. אלה המקומות שמופיעים בה:",
    "osm": "© OpenStreetMap contributors",
    "js": {
        "proj": "פרויקט", "ren": "התחדשות עירונית", "before": "לפני", "after": "אחרי", "newb": "בבניין החדש",
        "dev": "יזם: ", "stage": "שלב: ", "to_p": "לעמוד הפרויקט", "to_c": "לעמוד המתחם", "edge": "על גבול הרובע",
        "key": "גבולות הרובע, בקירוב",
        "cats": {"projects": "פרויקט", "renewal": "התחדשות עירונית", "edu": "בתי ספר וגנים", "parks": "פארקים",
                 "shop": "קניות", "transit": "תחבורה"},
        "loc": {"CooperativeGesturesHandler.WindowsHelpText": "להגדלה ולהקטנה: Ctrl וגלגלת העכבר",
                "CooperativeGesturesHandler.MacHelpText": "להגדלה ולהקטנה: ⌘ וגלגלת העכבר",
                "CooperativeGesturesHandler.MobileHelpText": "שתי אצבעות להזזת המפה",
                "NavigationControl.ZoomIn": "הגדלה", "NavigationControl.ZoomOut": "הקטנה",
                "NavigationControl.ResetBearing": "חזרה לצפון", "AttributionControl.ToggleAttribution": "קרדיט",
                "Map.Title": "מפה", "Marker.Title": "סימון", "Popup.Close": "סגירה"},
    },
}



def ui(d):
    """v1.1 (7.10.2026, HAD-460): the interface words and the section's language. Hebrew (UI, CHIPS, PLURAL, rtl) unless the
    data file carries "ui": {"lang", "dir", "colon", any UI key, "chips": {cat: label}, "plural": {type: plural},
    "js": {...; "cats" and "loc" merge key by key; "lrt" = the words in a light-rail stop's type}}. Without "ui" the
    section is byte-identical to v1."""
    o = d.get("ui") or {}
    u = {"lang": "he", "dir": "rtl", "colon": ": "}
    u.update({k: v for k, v in UI.items() if k != "js"})
    u.update({k: v for k, v in o.items() if k not in ("js", "chips", "plural")})
    js = dict(UI["js"])
    for k, v in (o.get("js") or {}).items():
        js[k] = dict(js[k], **v) if isinstance(js.get(k), dict) else v
    u["js"] = js
    lab = o.get("chips") or {}
    u["chips"] = [(k, lab.get(k, label), shape) for k, label, shape in CHIPS]
    u["plural"] = dict(PLURAL, **(o.get("plural") or {}))
    return u


ICO_RESET = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/></svg>')
ICO_X = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
         'aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg>')
ICO_MAP = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
           'stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M9 4.5 3.5 6.5v13l5.5-2 6 2 5.5-2v-13l-5.5 2-6-2z"/>'
           '<path d="M9 4.5v13M15 6.5v13"/></svg>')


def rich(t):
    """Escaped text, every number (or range, or date) one left-to-right island inside the Hebrew line."""
    return NUMRE.sub(lambda m: '<span class="nlam__num">' + m.group(0) + '</span>', _h.escape(str(t), quote=False))


def counts(d):
    c = {"projects": len(d["projects"]), "renewal": len(d["renewal"])}
    for k in ("edu", "parks", "shop", "transit"):
        c[k] = sum(1 for p in d["places"] if p[0] == k)
    return c


def bounds(ring, pad=0.035):
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    return [[round(min(xs) - pad, 4), round(min(ys) - pad, 4)], [round(max(xs) + pad, 4), round(max(ys) + pad, 4)]]


def cfg(d, u=None):
    u = u or ui(d)
    pr = [{"n": p["name"], "f": p["fact"], "d": p.get("dev"), "u": p["url"], "y": p["lat"], "x": p["lng"],
           "h": 1 if p.get("hero") else 0} for p in d["projects"]]
    rn = [{"a": r["address"], "b": r.get("before"), "f": r.get("after"), "d": r.get("dev"), "s": r.get("stage"),
           "o": r.get("note"), "u": r.get("url"), "y": r["lat"], "x": r["lng"]} for r in d["renewal"]]
    t = dict(u["js"])
    t["loc"] = dict(t["loc"], **{"Map.Title": d["title"]})
    return {"v": d["view"], "mb": bounds(d["boundary"]), "b": d["boundary"], "pr": pr, "rn": rn, "pl": d["places"],
            "fx": d.get("facts", {}), "t": t}


def _list(d, u=None):
    u = u or ui(d)
    T = lambda s: _h.escape(str(s), quote=False)
    lab = {k: label for k, label, _ in u["chips"]}
    col = u["colon"]
    out = []
    if d["projects"]:  # v1.1: a layer without places prints no heading (Sde Dov has no renewal pins)
        out.append('<h3 class="nlam__lh">' + E(lab["projects"]) + '</h3><ul class="nlam__ul">')
        for p in d["projects"]:
            out.append('<li><a href="' + E(p["url"]) + '"><bdi>' + E(p["name"]) + '</bdi></a>' + T(col) + rich(p["fact"]) + '</li>')
        out.append('</ul>')
    if d["renewal"]:
        out.append('<h3 class="nlam__lh">' + E(lab["renewal"]) + '</h3><ul class="nlam__ul">')
        for r in d["renewal"]:
            parts = []
            if r.get("before"):
                parts.append(T(u["js"]["before"] + col) + rich(r["before"]))
            if r.get("after"):
                parts.append(T(u["js"]["after"] + col) + rich(r["after"]))
            for k in ("dev", "stage"):
                if r.get(k):
                    parts.append(rich(r[k]))
            name = rich(r["address"])
            if r.get("url"):
                name = '<a href="' + E(r["url"]) + '">' + name + '</a>'
            out.append('<li>' + name + (T(col) + ' · '.join(parts) if parts else '') + '</li>')
        out.append('</ul>')
    PL = u["plural"]
    for cat, label, _ in u["chips"][2:]:
        rows = [p for p in d["places"] if p[0] == cat]
        if not rows:
            continue
        out.append('<h3 class="nlam__lh">' + E(label) + '</h3>')
        types = []
        for p in rows:
            if p[1] not in types:
                types.append(p[1])
        for ty in types:
            names = []
            for p in rows:
                if p[1] == ty and p[2] not in names:
                    names.append(p[2])
            many = {n: sum(1 for p in rows if p[1] == ty and p[2] == n) for n in names}
            out.append('<p class="nlam__lp"><b>' + E(PL.get(ty, ty) + u["colon"].rstrip()) + '</b> ' + ', '.join(
                '<bdi>' + E(n) + '</bdi>' + (' <span class="nlam__num">(' + str(many[n]) + ')</span>' if many[n] > 1 else '')
                for n in names) + '</p>')
    return ''.join(out)


def html(d, sfx=''):
    rid = 'nlam' + sfx
    u = ui(d)
    c = counts(d)
    data = json.dumps(cfg(d, u), ensure_ascii=False, separators=(',', ':'))
    out = ['<section class="nlds nlam" id="' + rid + '" data-state="wait" aria-labelledby="' + rid + '-t" dir="' + E(u["dir"]) +
           '" lang="' + E(u["lang"]) + '" '
           'data-cfg="' + E(data) + '">',
           '<header class="nlam__head"><p class="nlam__kicker">' + E(d["kicker"]) + '</p>',
           '<h2 class="nlam__title" id="' + rid + '-t">' + rich(d["title"]) + '</h2>',
           '<p class="nlam__lead">' + rich(d["lead"]) + '</p></header>',
           '<div class="nlam__chips" role="group" aria-label="' + E(u["chips_label"]) + '">']
    for k, label, shape in u["chips"]:
        if not c[k]:  # v1.1: no filter for an empty layer (a visible "0" is not allowed on the site)
            continue
        out.append('<button type="button" class="nlam__chip" data-cat="' + k + '" aria-pressed="true" disabled>'
                   '<span class="nlam__sw' + (' nlam__sw--' + shape if shape else '') + '" style="--c:var(--am-' + k + ')"></span>' +
                   E(label) + ' <span class="nlam__n">' + str(c[k]) + '</span></button>')
    out.append('</div>')
    out.append('<div class="nlam__frame">'
               '<div class="nlam__map" role="region" aria-label="' + E(d["title"]) + '"></div>'
               '<div class="nlam__wait" aria-hidden="true">' + ICO_MAP + '<span>' + E(u["wait"]) + '</span></div>'
               '<button type="button" class="nlam__reset">' + ICO_RESET + E(u["reset"]) + '</button>'
               '<div class="nlam__key" aria-hidden="true"><i></i>' + E(u["js"]["key"]) + '</div>'
               '<div class="nlam__card" role="dialog" aria-modal="false" aria-labelledby="' + rid + '-ch" hidden>'
               '<button type="button" class="nlam__x" aria-label="' + E(u["close"]) + '">' + ICO_X + '</button>'
               '<div class="nlam__cb"></div></div></div>')
    cap = rich(d["caption"]).replace('OpenStreetMap', '<bdi>OpenStreetMap</bdi>', 1)
    out.append('<p class="nlam__cap">' + cap + ' <a class="nlam__osm" href="https://www.openstreetmap.org/copyright" '
               'rel="noopener" target="_blank"><bdi>' + E(u["osm"]) + '</bdi></a></p>')
    out.append('<p class="nlam__failnote">' + E(u["fail"]) + '</p>')
    out.append('<details class="nlam__list"><summary>' + E(u["list"]) + '</summary>' + _list(d, u) + '</details>')
    out.append('</section>')
    return ''.join(out)


CSS = r"""
.nlam{--am-sea:var(--nlds-sa-sea,#2f6f86);--am-seah:var(--nlds-sa-seah,#255c70);--am-ink:var(--nlds-sa-ink,#14212b);--am-ink2:var(--nlds-sa-ink2,#3b4753);--am-line:var(--nlds-sa-line,#e3e1da);--am-paper:var(--nlds-sa-paper,#f7f6f2);--am-sand:var(--nlds-sa-sand,#eee9dd);--am-surf:var(--nlds-sa-surf,#fff);--am-deep:var(--nlds-sa-deep,#1f4b5c);--am-serif:var(--nlds-font-serif,"Noto Serif Hebrew","David Libre",Georgia,serif);--am-sans:var(--nlds-font-sans,Assistant,"Segoe UI",Arial,sans-serif);--am-projects:#1f4b5c;--am-renewal:#3b4753;--am-edu:#4a3aa7;--am-parks:#1baf7a;--am-shop:#eb6834;--am-transit:#2a78d6;display:block !important;container-type:inline-size !important;container-name:nlam !important;margin:clamp(18px,3vw,34px) auto 0 !important;max-width:var(--nlds-container,1240px) !important;padding:0 clamp(16px,3vw,32px) !important;box-sizing:border-box !important;font-family:var(--am-sans) !important;color:var(--am-ink) !important;text-align:start !important}
.nlam *,.nlam *::before,.nlam *::after{box-sizing:border-box !important}
.nlam__head{display:grid !important;gap:8px !important;margin:0 0 14px !important}
.nlam__kicker{margin:0 !important;font:700 14px/1.3 var(--am-sans) !important;letter-spacing:.02em !important;color:var(--am-sea) !important}
.nlam__title{margin:0 !important;padding:0 !important;border:0 !important;background:none !important;font-family:var(--am-serif) !important;font-weight:600 !important;font-size:clamp(23px,1.2rem + 1.1vw,31px) !important;line-height:1.22 !important;letter-spacing:-.005em !important;color:var(--am-ink) !important;text-align:start !important;text-wrap:balance !important}
.nlam__title::before,.nlam__title::after{content:none !important;display:none !important}
.nlam__lead{margin:0 !important;max-width:72ch !important;font-size:clamp(15.5px,1rem + .15vw,17px) !important;line-height:1.7 !important;color:var(--am-ink2) !important}
.nlam__num{direction:ltr !important;unicode-bidi:isolate !important;font:inherit !important;color:inherit !important}
.nlam__chips{display:flex !important;gap:8px !important;margin:0 0 12px !important;padding:2px 0 6px !important;overflow-x:auto !important;scrollbar-width:none !important;-webkit-overflow-scrolling:touch}
.nlam__chips::-webkit-scrollbar{display:none !important}
.nlam__chip{flex:0 0 auto !important;display:inline-flex !important;align-items:center !important;gap:8px !important;width:auto !important;height:auto !important;min-height:40px !important;margin:0 !important;padding:0 14px !important;border:1px solid var(--am-line) !important;border-radius:999px !important;background:var(--am-surf) !important;color:var(--am-ink2) !important;font:600 15px/1 var(--am-sans) !important;text-transform:none !important;letter-spacing:0 !important;box-shadow:none !important;cursor:pointer !important;transition:border-color .2s,background-color .2s,color .2s !important}
.nlam__chip:hover:not(:disabled){border-color:var(--am-sea) !important}
.nlam__chip[aria-pressed="true"]:not(:disabled){background:var(--am-sea) !important;border-color:var(--am-sea) !important;color:#fff !important}
.nlam__chip:disabled{opacity:.72 !important;cursor:default !important}
.nlam__chip:focus-visible,.nlam__reset:focus-visible,.nlam__x:focus-visible,.nlam__pin:focus-visible,.nlam__cta:focus-visible{outline:2px solid var(--am-sea) !important;outline-offset:2px !important}
.nlam__sw{flex:0 0 auto !important;width:12px !important;height:12px !important;border-radius:50% !important;background:var(--c) !important;box-shadow:0 0 0 2px #fff !important}
.nlam__sw--sq{border-radius:3px !important}
.nlam__sw--pill{width:18px !important;border-radius:999px !important}
.nlam__n{font-weight:400 !important;opacity:.8 !important;direction:ltr !important;unicode-bidi:isolate !important;font-variant-numeric:tabular-nums !important}
.nlam__frame{position:relative !important;display:block !important;height:70vh !important;min-height:460px !important;max-height:760px !important;margin:0 !important;padding:0 !important;border:1px solid var(--am-line) !important;border-radius:22px !important;overflow:hidden !important;background:var(--am-sand) !important;isolation:isolate !important}
.nlam__map{position:absolute !important;inset:0 !important}
.nlam__wait{position:absolute !important;inset:0 !important;z-index:1 !important;display:grid !important;place-content:center !important;justify-items:center !important;gap:10px !important;background:var(--am-sand) !important;color:var(--am-ink2) !important;font:600 15.5px/1.4 var(--am-sans) !important}
.nlam__wait svg{width:30px !important;height:30px !important;color:var(--am-deep) !important;opacity:.75 !important}
.nlam[data-state="ready"] .nlam__wait{display:none !important}
.nlam__reset{position:absolute !important;z-index:3 !important;top:14px !important;left:14px !important;display:inline-flex !important;align-items:center !important;gap:8px !important;width:auto !important;height:auto !important;min-height:40px !important;margin:0 !important;padding:0 16px !important;border:1px solid var(--am-line) !important;border-radius:999px !important;background:rgba(255,255,255,.96) !important;color:var(--am-deep) !important;font:600 15px/1 var(--am-sans) !important;text-transform:none !important;box-shadow:0 1px 2px rgba(20,33,43,.04) !important;cursor:pointer !important}
.nlam__reset:hover{background:var(--am-sand) !important;border-color:var(--am-sea) !important}
.nlam__reset svg{width:17px !important;height:17px !important}
.nlam:not([data-state="ready"]) .nlam__reset,.nlam:not([data-state="ready"]) .nlam__key{display:none !important}
.nlam__key{position:absolute !important;z-index:2 !important;right:12px !important;bottom:30px !important;display:inline-flex !important;align-items:center !important;gap:8px !important;padding:6px 11px !important;border:1px solid var(--am-line) !important;border-radius:999px !important;background:rgba(255,255,255,.92) !important;color:var(--am-deep) !important;font:600 13px/1.2 var(--am-sans) !important;pointer-events:none !important}
.nlam__key i{display:block !important;width:22px !important;height:0 !important;border-top:2px dashed var(--am-deep) !important}
.nlam__pin{display:flex !important;flex-direction:column !important;align-items:center !important;width:auto !important;height:auto !important;min-width:0 !important;min-height:0 !important;margin:0 !important;padding:0 !important;border:0 !important;background:none !important;box-shadow:none !important;font-family:var(--am-sans) !important;line-height:1 !important;text-transform:none !important;cursor:pointer !important}
.nlam__pl{display:inline-flex !important;align-items:center !important;padding:7px 12px !important;border-radius:999px !important;background:var(--am-deep) !important;color:#fff !important;font-weight:700 !important;font-size:14px !important;line-height:1 !important;white-space:nowrap !important;box-shadow:0 8px 20px rgba(20,33,43,.18) !important;transition:transform .2s,background-color .2s !important}
.nlam__ps{display:block !important;width:2px !important;height:16px !important;background:var(--am-deep) !important}
.nlam__pf{position:relative !important;display:block !important;width:10px !important;height:10px !important;margin-top:-2px !important;border-radius:50% !important;background:#fff !important;border:3px solid var(--am-deep) !important}
.nlam__pin--hero .nlam__pl{background:var(--am-sea) !important;font-family:var(--am-serif) !important;font-weight:600 !important;font-size:16px !important;padding:9px 15px !important}
.nlam__pin--hero .nlam__ps{background:var(--am-sea) !important;height:22px !important}
.nlam__pin--hero .nlam__pf{border-color:var(--am-sea) !important}
.nlam__pin:hover .nlam__pl,.nlam__pin.is-on .nlam__pl{transform:translateY(-2px) !important;background:var(--am-seah) !important}
.nlam__pin.is-compact .nlam__pl{display:none !important}
.nlam__pin.is-compact .nlam__ps{height:6px !important}
.nlam__pin.is-compact .nlam__pf{width:16px !important;height:16px !important;border-width:4px !important}
.nlam__pin.is-compact .nlam__pf::after{content:"" !important;position:absolute !important;inset:-12px !important;border-radius:50% !important}
.nlam__card{position:absolute !important;z-index:4 !important;top:14px !important;right:14px !important;width:330px !important;max-height:calc(100% - 28px) !important;overflow:auto !important;margin:0 !important;padding:18px 20px !important;background:var(--am-surf) !important;border:1px solid var(--am-line) !important;border-radius:16px !important;box-shadow:0 14px 34px rgba(20,33,43,.1) !important;text-align:start !important}
.nlam__card[hidden]{display:none !important}
.nlam__x{position:absolute !important;top:10px !important;left:10px !important;display:grid !important;place-items:center !important;width:36px !important;height:36px !important;min-height:0 !important;margin:0 !important;padding:0 !important;border:0 !important;border-radius:999px !important;background:transparent !important;color:var(--am-ink2) !important;box-shadow:none !important;cursor:pointer !important}
.nlam__x:hover{background:var(--am-sand) !important}
.nlam__x svg{width:18px !important;height:18px !important}
.nlam__ck{display:flex !important;align-items:center !important;gap:8px !important;margin:0 0 6px !important;color:var(--am-sea) !important;font:700 13.5px/1.3 var(--am-sans) !important}
.nlam__ct{margin:0 0 8px !important;margin-inline-end:34px !important;padding:0 !important;border:0 !important;font-family:var(--am-serif) !important;font-weight:600 !important;font-size:21px !important;line-height:1.3 !important;color:var(--am-ink) !important}
.nlam__ct::before,.nlam__ct::after{content:none !important;display:none !important}
.nlam__card p{margin:0 0 6px !important;font-size:15.5px !important;line-height:1.5 !important;color:var(--am-ink2) !important}
.nlam__card p.nlam__cm{font-size:14px !important}
.nlam__ba{display:grid !important;grid-template-columns:1fr auto 1fr !important;align-items:stretch !important;gap:8px !important;margin:10px 0 !important}
.nlam__ba--one{grid-template-columns:1fr !important}
.nlam__ba>div{background:var(--am-paper) !important;border:1px solid var(--am-line) !important;border-radius:12px !important;padding:9px 11px !important}
.nlam__ba b{display:block !important;margin:0 0 3px !important;font-size:12.5px !important;font-weight:600 !important;color:var(--am-ink2) !important}
.nlam__ba>div>span{display:block !important;font-size:15px !important;line-height:1.35 !important;font-weight:600 !important;color:var(--am-ink) !important}
.nlam__ba i{align-self:center !important;font-style:normal !important;font-weight:700 !important;color:var(--am-sea) !important}
.nlam__cta{display:inline-flex !important;align-items:center !important;min-height:44px !important;margin:10px 0 0 !important;padding:0 20px !important;border-radius:999px !important;background:var(--am-sea) !important;color:#fff !important;font:700 15.5px/1 var(--am-sans) !important;text-decoration:none !important;box-shadow:none !important}
.nlam__cta:hover{background:var(--am-seah) !important;color:#fff !important}
.nlam__cap{margin:12px 0 0 !important;font-size:13.5px !important;line-height:1.55 !important;color:var(--am-ink2) !important}
.nlam__cap a{color:var(--am-ink2) !important;text-decoration:underline !important;text-underline-offset:2px !important}
.nlam__failnote{display:none !important;margin:0 0 6px !important;font-size:15.5px !important;line-height:1.6 !important;color:var(--am-ink2) !important}
.nlam__list{margin:14px 0 0 !important;padding:10px 0 0 !important;border-top:1px solid var(--am-line) !important}
.nlam__list>summary{display:flex !important;align-items:center !important;min-height:44px !important;cursor:pointer !important;color:var(--am-sea) !important;font:700 15px/1.3 var(--am-sans) !important}
.nlam__lh{margin:14px 0 6px !important;padding:0 !important;border:0 !important;font-family:var(--am-serif) !important;font-weight:600 !important;font-size:17px !important;line-height:1.35 !important;color:var(--am-ink) !important}
.nlam__lh::before,.nlam__lh::after{content:none !important;display:none !important}
.nlam__ul{margin:0 !important;padding:0 !important;padding-inline-start:18px !important;list-style:disc !important}
.nlam__ul li{margin:0 0 6px !important;padding:0 !important;font-size:15px !important;line-height:1.55 !important;color:var(--am-ink2) !important}
.nlam__ul li::before{content:none !important}
.nlam__lp{margin:0 0 6px !important;font-size:15px !important;line-height:1.6 !important;color:var(--am-ink2) !important}
.nlam__lp b{color:var(--am-ink) !important;font-weight:600 !important}
.nlam__list a{color:var(--am-sea) !important;text-decoration:underline !important;text-underline-offset:3px !important}
.nlam[data-state="fail"] .nlam__frame,.nlam[data-state="fail"] .nlam__chips{display:none !important}
.nlam[data-state="fail"]{display:flex !important;flex-direction:column !important}
.nlam[data-state="fail"] .nlam__cap{order:3 !important}
.nlam[data-state="fail"] .nlam__failnote{display:block !important}
.nlam[data-state="fail"] .nlam__list{border-top:0 !important;padding-top:0 !important}
.nlam .maplibregl-map{position:absolute !important;inset:0 !important;overflow:hidden !important}
.nlam .maplibregl-canvas{position:absolute !important;left:0 !important;top:0 !important}
.nlam .maplibregl-marker{position:absolute !important;top:0 !important;left:0 !important;will-change:transform}
.nlam .maplibregl-ctrl-group{border-radius:14px !important;border:1px solid var(--am-line) !important;box-shadow:0 1px 2px rgba(20,33,43,.06) !important}
.nlam .maplibregl-ctrl-group button{width:38px !important;height:38px !important;min-height:0 !important;padding:0 !important;margin:0 !important;box-shadow:none !important}
.nlam .maplibregl-ctrl-bottom-left{bottom:6px !important}
.nlam .maplibregl-ctrl-attrib{font-family:var(--am-sans) !important;font-size:11.5px !important;line-height:1.4 !important;background:rgba(255,255,255,.88) !important}
.nlam .maplibregl-ctrl-attrib a{color:var(--am-ink2) !important}
.nlam .maplibregl-cooperative-gesture-screen{font-family:var(--am-sans) !important;font-weight:600 !important;font-size:18px !important;background:rgba(20,33,43,.55) !important}
@container nlam (max-width:640px){
 .nlam__frame{height:60vh !important;height:60svh !important;min-height:380px !important;border-radius:16px !important}
 .nlam__card{top:auto !important;bottom:30px !important;right:10px !important;left:10px !important;width:auto !important;max-height:64% !important;padding:16px !important}
 .nlam__ct{font-size:19px !important}
 .nlam__pl{font-size:13px !important;padding:6px 10px !important}
 .nlam__pin--hero .nlam__pl{font-size:14.5px !important;padding:8px 12px !important}
 .nlam__reset{top:10px !important;left:10px !important;min-height:36px !important;padding:0 12px !important;font-size:13.5px !important;gap:6px !important}
 .nlam__reset svg{width:15px !important;height:15px !important}
 .nlam .maplibregl-ctrl-bottom-left{display:none !important}
}
.nlam[dir="ltr"] .nlam__reset{left:auto !important;right:14px !important}
.nlam[dir="ltr"] .nlam__key{right:auto !important;left:12px !important}
.nlam[dir="ltr"] .nlam__card{right:auto !important;left:14px !important}
.nlam[dir="ltr"] .nlam__x{left:auto !important;right:10px !important}
.nlam[dir="ltr"] .nlam__ba i{transform:scaleX(-1) !important}
@container nlam (max-width:640px){
 .nlam[dir="ltr"] .nlam__reset{right:10px !important}
 .nlam[dir="ltr"] .nlam__card{left:10px !important;right:10px !important}
}
@media (prefers-reduced-motion:reduce){.nlam__pl,.nlam__chip{transition:none !important}}
"""

JS = r"""
(function(){'use strict';var W=window;if(W.nlamInit){W.nlamInit();return}
var CDN='https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/',
 SRI_JS='sha512-rOFgoUgWaVi69JW1dzBu6PWF9xKW9rxYfY5u2SexFABHhWk0qUWkJoWNz4UuZRMvSXsNZG66+tU5B+HlwWF5kA==',
 SRI_CSS='sha512-KIMsMWIdnoG9OwZa+oaIafmbDonqck1UCmq+/zcUi2aaZ97N9QE6TqpTM+n36EO40HGh64hU/375zxtjx7WTyQ==',
 RTL='https://cdn.jsdelivr.net/npm/@mapbox/mapbox-gl-rtl-text@0.3.0/dist/mapbox-gl-rtl-text.js',
 STYLE='https://tiles.openfreemap.org/styles/positron',FONT=['Noto Sans Regular'],lib=null;
var COL={edu:'#4a3aa7',parks:'#1baf7a',shop:'#eb6834',transit:'#2a78d6',renewal:'#3b4753'};
var GLYPH={edu:'M3 9.5l9-4 9 4-9 4-9-4z M7 11.5v3.5c0 1.6 2.3 3 5 3s5-1.4 5-3v-3.5',
 parks:'M12 3.5a4.6 4.6 0 0 0-4.5 4.1A3.8 3.8 0 0 0 8 15.3h8a3.8 3.8 0 0 0 .5-7.7A4.6 4.6 0 0 0 12 3.5z M12 15.3v5.2',
 shop:'M5.5 8.5h13l-1 11.5h-11l-1-11.5z M9 8.5V7a3 3 0 0 1 6 0v1.5',
 transit:'M7.5 4h9a2 2 0 0 1 2 2v8.5a2 2 0 0 1-2 2h-9a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z M5.5 10.5h13 M9 16.5l-2 3.5 M15 16.5l2 3.5',
 renewal:'M5 20.5V9.5l7-4 7 4v11 M9.5 20.5v-5h5v5 M3.5 20.5h17'};
function tag(n,a){var e=document.createElement(n);for(var k in a)e.setAttribute(k,a[k]);return e}
function loadLib(){if(W.maplibregl&&W.maplibregl.Map)return Promise.resolve(W.maplibregl);if(lib)return lib;
 lib=new Promise(function(res,rej){var n=0,over=false;
  function no(){if(!over){over=true;rej(new Error('nlam'))}}
  function ok(){if(over)return;if(++n===2){if(W.maplibregl&&W.maplibregl.Map){over=true;res(W.maplibregl)}else no()}}
  var l=tag('link',{rel:'stylesheet',href:CDN+'maplibre-gl.css',integrity:SRI_CSS,crossorigin:'anonymous'});
  l.onload=ok;l.onerror=ok;document.head.appendChild(l);
  var s=tag('script',{src:CDN+'maplibre-gl.js',integrity:SRI_JS,crossorigin:'anonymous'});
  s.async=true;s.onload=ok;s.onerror=no;document.head.appendChild(s);setTimeout(no,20000)});
 return lib}
function gl(){try{var c=document.createElement('canvas');return !!(c.getContext('webgl2')||c.getContext('webgl'))}catch(e){return false}}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function num(s){return esc(s).replace(/(\d(?:[\d,.:]*\d)?(?:-\d(?:[\d,.]*\d)?)?)/g,'<span class="nlam__num">$1</span>')}
function icon(cat,sq){var S=30,R=2,c=document.createElement('canvas');c.width=c.height=S*R;var g=c.getContext('2d');g.scale(R,R);
 g.fillStyle=COL[cat];g.strokeStyle='#fff';g.lineWidth=2;g.beginPath();
 if(sq){if(g.roundRect)g.roundRect(2,2,S-4,S-4,7);else g.rect(2,2,S-4,S-4)}else g.arc(S/2,S/2,S/2-2,0,Math.PI*2);
 g.fill();g.stroke();g.save();g.translate(S/2-8.4,S/2-8.4);g.scale(.7,.7);g.lineWidth=2.1;g.lineCap='round';g.lineJoin='round';
 g.stroke(new Path2D(GLYPH[cat]));g.restore();return g.getImageData(0,0,S*R,S*R)}
function fc(list,f){return{type:'FeatureCollection',features:list.map(function(p,i){return{type:'Feature',id:i,properties:f(p,i),geometry:{type:'Point',coordinates:[p.x,p.y]}}})}}
function one(root){if(root.__nlam)return;var C;try{C=JSON.parse(root.getAttribute('data-cfg'))}catch(e){return}if(!C||!C.v)return;root.__nlam=1;
 var LTR=root.getAttribute('dir')==='ltr',LN=(root.getAttribute('lang')||'he').slice(0,2),
  NAME=LN==='he'?['coalesce',['get','name:he'],['get','name']]:['coalesce',['get','name:'+LN],['get','name:en'],['get','name']];
 var T=C.t,q=function(s){return root.querySelector(s)},mapEl=q('.nlam__map'),card=q('.nlam__card'),cb=q('.nlam__cb'),
  xb=q('.nlam__x'),reset=q('.nlam__reset'),fr=q('.nlam__frame'),list=q('.nlam__list'),chips=root.querySelectorAll('.nlam__chip'),
  on={projects:1,renewal:1,edu:1,parks:1,shop:1,transit:1},map=null,started=false,pins=[],last=null,HOME=null,
  still=!!(W.matchMedia&&W.matchMedia('(prefers-reduced-motion: reduce)').matches),
  places=C.pl.map(function(a){return{c:a[0],t:a[1],n:a[2],a:a[3],y:a[4],x:a[5],e:a[6]}});
 function st(s){root.setAttribute('data-state',s)}
 function fail(why){if(root.getAttribute('data-state')==='ready')return;try{console.warn('nlam: map unavailable, showing the list ('+(why&&why.message||why||'')+')')}catch(e){}st('fail');if(list)list.open=true;try{if(map)map.remove()}catch(e){}map=null}
 function start(){if(started)return;started=true;if(!gl())return fail('webgl');st('load');loadLib().then(build,fail)}
 if('IntersectionObserver' in W){var io=new IntersectionObserver(function(es){for(var i=0;i<es.length;i++)if(es[i].isIntersecting){io.disconnect();start();break}},{rootMargin:'300px 0px 300px 0px'});io.observe(root)}else start();
 function restyle(){var L=map.getStyle().layers;L.forEach(function(l){var id=l.id;try{
   if(l.type==='background')map.setPaintProperty(id,'background-color','#f3f1ea');
   else if(id==='water')map.setPaintProperty(id,'fill-color','#c9dfe6');
   else if(id==='waterway')map.setPaintProperty(id,'line-color','#b9d4dd');
   else if(id==='park'){map.setPaintProperty(id,'fill-color','#dfe7d6');map.setPaintProperty(id,'fill-opacity',.9)}
   else if(id==='landcover_wood')map.setPaintProperty(id,'fill-color','#d9e3cf');
   else if(id==='landuse_residential')map.setPaintProperty(id,'fill-color','#efede5');
   else if(id==='building'){map.setPaintProperty(id,'fill-color','#e9e5da');map.setLayerZoomRange(id,0,13.4)}
   else if(/^(boundary_|airport|highway-shield|road_shield|label_country|label_state)/.test(id))map.setLayoutProperty(id,'visibility','none');
   else if(/highway_(major|motorway)_(inner|subtle)$/.test(id)||id==='highway_minor')map.setPaintProperty(id,'line-color','#ffffff');
   else if(/casing$/.test(id)&&l.type==='line')map.setPaintProperty(id,'line-color','#dcd8cc');
   if(l.type==='symbol'&&l.layout&&l.layout['text-field']&&!/shield/.test(id)){map.setLayoutProperty(id,'text-field',NAME);
    map.setPaintProperty(id,'text-color','#5a6670');map.setPaintProperty(id,'text-halo-color','rgba(247,246,242,.95)')}}catch(e){}});
  var first=(L.filter(function(l){return l.type==='symbol'})[0]||{}).id;var h=['coalesce',['get','render_height'],0],b=['coalesce',['get','render_min_height'],0];
  map.addLayer({id:'nlam-3d',type:'fill-extrusion',source:'openmaptiles','source-layer':'building',minzoom:13,filter:['!=',['get','hide_3d'],true],
   paint:{'fill-extrusion-color':['interpolate',['linear'],h,0,'#fbfaf7',30,'#f1ede4',90,'#e6e0d3',160,'#dcd5c6'],
    'fill-extrusion-height':['interpolate',['linear'],['zoom'],13,0,13.6,h],'fill-extrusion-base':['interpolate',['linear'],['zoom'],13,0,13.6,b],
    'fill-extrusion-opacity':.94,'fill-extrusion-vertical-gradient':true}},first)}
 function layers(){var ring=C.b;
  ['edu','parks','shop','transit'].forEach(function(k){map.addImage('nlam-'+k,icon(k,0),{pixelRatio:2})});map.addImage('nlam-renewal',icon('renewal',1),{pixelRatio:2});
  map.addSource('nlam-veil',{type:'geojson',data:{type:'Feature',properties:{},geometry:{type:'Polygon',coordinates:[[[34.5,31.9],[35,31.9],[35,32.3],[34.5,32.3],[34.5,31.9]],ring.slice().reverse()]}}});
  map.addLayer({id:'nlam-veil',type:'fill',source:'nlam-veil',paint:{'fill-color':'#f7f6f2','fill-opacity':.42}},'nlam-3d');
  map.addSource('nlam-edge',{type:'geojson',data:{type:'Feature',properties:{},geometry:{type:'LineString',coordinates:ring}}});
  map.addLayer({id:'nlam-edge-glow',type:'line',source:'nlam-edge',paint:{'line-color':'#fff','line-width':6,'line-opacity':.8}});
  map.addLayer({id:'nlam-edge',type:'line',source:'nlam-edge',paint:{'line-color':'#1f4b5c','line-width':1.6,'line-dasharray':[3,2],'line-opacity':.85}});
  map.addLayer({id:'nlam-edge-label',type:'symbol',source:'nlam-edge',layout:{'symbol-placement':'line','text-field':T.key,'text-font':FONT,'text-size':12.5,'symbol-spacing':520,'text-offset':[0,-.9]},
   paint:{'text-color':'#1f4b5c','text-halo-color':'rgba(255,255,255,.95)','text-halo-width':1.6}});
  map.addSource('nlam-proj',{type:'geojson',data:fc(C.pr,function(p){return{h:p.h}})});
  map.addLayer({id:'nlam-halo',type:'circle',source:'nlam-proj',paint:{'circle-pitch-alignment':'map','circle-pitch-scale':'map',
   'circle-radius':['interpolate',['exponential',2],['zoom'],13,['case',['==',['get','h'],1],9,5],18,['case',['==',['get','h'],1],290,160]],
   'circle-color':'#2f6f86','circle-opacity':.13,'circle-stroke-color':'#2f6f86','circle-stroke-width':1.2,'circle-stroke-opacity':.5}},'nlam-3d');
  map.addSource('nlam-sel',{type:'geojson',data:{type:'FeatureCollection',features:[]}});
  map.addLayer({id:'nlam-sel',type:'circle',source:'nlam-sel',paint:{'circle-radius':19,'circle-color':'rgba(47,111,134,.16)','circle-stroke-color':'#2f6f86','circle-stroke-width':2.5}});
  map.addSource('nlam-places',{type:'geojson',data:fc(places,function(p,i){return{i:i,cat:p.c,name:p.n}})});
  map.addLayer({id:'nlam-places',type:'symbol',source:'nlam-places',layout:{'icon-image':['concat','nlam-',['get','cat']],
   'icon-size':['interpolate',['linear'],['zoom'],13,.56,15,.72,17,.95],'icon-allow-overlap':false,'icon-padding':1,
   'symbol-sort-key':['match',['get','cat'],'transit',1,'edu',2,'parks',3,4],'text-field':['step',['zoom'],'',16.3,['get','name']],
   'text-font':FONT,'text-size':12,'text-offset':[0,1.35],'text-anchor':'top','text-optional':true,'text-max-width':9},
   paint:{'text-color':'#3b4753','text-halo-color':'rgba(255,255,255,.95)','text-halo-width':1.5}});
  map.addSource('nlam-ren',{type:'geojson',data:fc(C.rn,function(r,i){return{i:i,a:r.a}})});
  map.addLayer({id:'nlam-ren',type:'symbol',source:'nlam-ren',layout:{'icon-image':'nlam-renewal','icon-allow-overlap':true,'icon-ignore-placement':true,
   'icon-size':['interpolate',['linear'],['zoom'],13,.6,15,.82,17,1.05],'text-field':['step',['zoom'],'',16.6,['get','a']],
   'text-font':FONT,'text-size':12,'text-offset':[0,1.4],'text-anchor':'top','text-optional':true},
   paint:{'text-color':'#14212b','text-halo-color':'rgba(255,255,255,.95)','text-halo-width':1.5}});
  ['nlam-places','nlam-ren'].forEach(function(id){
   map.on('click',id,function(e){var f=e.features&&e.features[0];if(!f)return;if(id==='nlam-ren')openRen(C.rn[f.properties.i]);else openPlace(places[f.properties.i])});
   map.on('mouseenter',id,function(){map.getCanvas().style.cursor='pointer'});map.on('mouseleave',id,function(){map.getCanvas().style.cursor=''})});
  map.on('click',function(e){var t=e.originalEvent&&e.originalEvent.target;if(t&&t.closest&&t.closest('.nlam__pin'))return;
   if(!map.queryRenderedFeatures(e.point,{layers:['nlam-places','nlam-ren']}).length&&!card.hidden)hide()})}
 function build(ml){
  try{if(ml.getRTLTextPluginStatus()==='unavailable')ml.setRTLTextPlugin(RTL,true).catch(function(){})}catch(e){}
  var V=C.v,P=V.phone||{},narrow=fr.clientWidth<640;
  HOME=narrow?{center:P.center||V.center,zoom:P.zoom||14.2,pitch:P.pitch||V.pitch,bearing:V.bearing}:{center:V.center,zoom:V.zoom,pitch:V.pitch,bearing:V.bearing};
  try{map=new ml.Map({container:mapEl,style:STYLE,center:HOME.center,zoom:HOME.zoom,pitch:HOME.pitch,bearing:HOME.bearing,minZoom:12.8,maxZoom:18.5,maxPitch:70,
   maxBounds:C.mb,cooperativeGestures:true,attributionControl:{compact:false},locale:T.loc})}catch(e){return fail(e)}
  root.__nlamMap=map;
  if(!narrow)map.addControl(new ml.NavigationControl({visualizePitch:true}),LTR?'bottom-right':'bottom-left');
  var styled=false,timer=setTimeout(function(){if(!styled)fail('style timeout')},20000);
  map.on('error',function(e){var er=e&&e.error;if(!styled&&er&&(er.status||/fetch|network|ajax|load/i.test(er.message||''))){clearTimeout(timer);fail(er)}});
  map.on('style.load',function(){if(styled||!map)return;styled=true;clearTimeout(timer);
   try{restyle();layers()}catch(e){}
   st('ready');for(var i=0;i<chips.length;i++)chips[i].disabled=false;filters();measure();declutter()});
  C.pr.forEach(function(p){var b=document.createElement('button');b.type='button';b.className='nlam__pin'+(p.h?' nlam__pin--hero':'');b.setAttribute('aria-label',p.n);
   b.innerHTML='<span class="nlam__pl"><bdi>'+esc(p.n)+'</bdi></span><span class="nlam__ps"></span><span class="nlam__pf"></span>';
   b.addEventListener('click',function(ev){ev.stopPropagation();openProj(p,b,ev.detail===0)});
   new ml.Marker({element:b,anchor:'bottom'}).setLngLat([p.x,p.y]).addTo(map);pins.push({el:b,p:p,lb:b.firstChild})});
  map.on('move',queue);map.on('resize',queue);
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){measure();declutter()})}
 function measure(){pins.forEach(function(x){x.el.classList.remove('is-compact');x.w=x.lb.offsetWidth||90;x.hh=x.lb.offsetHeight||28})}
 var queued=false;function queue(){if(!queued){queued=true;requestAnimationFrame(declutter)}}
 function declutter(){queued=false;if(!map)return;var cv=map.getCanvas(),Wd=cv.clientWidth,cr=cv.getBoundingClientRect(),bb=reset.getBoundingClientRect(),placed=[];
  if(bb.width)placed.push({l:bb.left-cr.left-4,r:bb.right-cr.left+4,t:bb.top-cr.top-4,b:bb.bottom-cr.top+4});
  pins.slice().sort(function(a,b){return(b.el.classList.contains('is-on')-a.el.classList.contains('is-on'))||(b.p.h-a.p.h)}).forEach(function(x){if(!x.w)return;
   var pt=map.project([x.p.x,x.p.y]),lift=x.p.h?34:28,r={l:pt.x-x.w/2-4,r:pt.x+x.w/2+4,t:pt.y-lift-x.hh-4,b:pt.y-lift+4},sel=x.el.classList.contains('is-on'),
    hit=!sel&&(r.l<2||r.r>Wd-2||r.t<2||placed.some(function(o){return!(r.r<o.l||r.l>o.r||r.b<o.t||r.t>o.b)}));
   x.el.classList.toggle('is-compact',hit);x.el.style.zIndex=sel?5:hit?1:(x.p.h?4:3);if(!hit)placed.push(r)})}
 function mark(ll){var s=map&&map.getSource('nlam-sel');if(s)s.setData({type:'FeatureCollection',features:ll?[{type:'Feature',properties:{},geometry:{type:'Point',coordinates:ll}}]:[]})}
 function show(h,ll,opener,kb){pins.forEach(function(x){x.el.classList.remove('is-on')});if(opener)opener.classList.add('is-on');mark(opener?null:ll);last=opener||null;
  cb.innerHTML=h;card.hidden=false;queue();var narrow=fr.clientWidth<640,off=narrow?[0,-Math.round(card.offsetHeight/2)+10]:[LTR?150:-150,40];
  map.easeTo({center:ll,offset:off,duration:still?0:650});if(kb)try{xb.focus({preventScroll:true})}catch(e){}}
 function hide(){card.hidden=true;mark(null);pins.forEach(function(x){x.el.classList.remove('is-on')});queue();if(last)try{last.focus({preventScroll:true})}catch(e){}}
 xb.addEventListener('click',hide);document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!card.hidden)hide()});
 function kick(label,col,sq){return'<p class="nlam__ck"><span class="nlam__sw'+(sq?' nlam__sw--sq':'')+'" style="--c:'+col+'"></span>'+esc(label)+'</p>'}
 function title(h){return'<h3 class="nlam__ct" id="'+root.id+'-ch">'+h+'</h3>'}
 function openProj(p,el,kb){show(kick(T.proj,'var(--am-projects)')+title('<bdi>'+esc(p.n)+'</bdi>')+'<p>'+num(p.f)+'</p>'+(p.d?'<p class="nlam__cm">'+num(p.d)+'</p>':'')+
  '<a class="nlam__cta" href="'+esc(p.u)+'">'+esc(T.to_p)+'</a>',[p.x,p.y],el,kb)}
 function openRen(r){var ba='';
  if(r.b&&r.f)ba='<div class="nlam__ba"><div><b>'+esc(T.before)+'</b><span>'+num(r.b)+'</span></div><i aria-hidden="true">←</i><div><b>'+esc(T.after)+'</b><span>'+num(r.f)+'</span></div></div>';
  else if(r.f)ba='<div class="nlam__ba nlam__ba--one"><div><b>'+esc(T.newb)+'</b><span>'+num(r.f)+'</span></div></div>';
  show(kick(T.ren,'var(--am-renewal)',1)+title(num(r.a))+ba+(r.d?'<p class="nlam__cm">'+esc(T.dev)+num(r.d)+'</p>':'')+(r.s?'<p class="nlam__cm">'+esc(T.stage)+num(r.s)+'</p>':'')+
   (r.o?'<p class="nlam__cm">'+num(r.o)+'</p>':'')+(r.u?'<a class="nlam__cta" href="'+esc(r.u)+'">'+esc(T.to_c)+'</a>':''),[r.x,r.y],null)}
 function openPlace(p){var line=p.t+(p.a?' · '+p.a:''),extra=(p.c==='transit'&&C.fx&&C.fx[p.n]&&p.t.indexOf(T.lrt||'הקלה')>-1)?C.fx[p.n]:'';
  show(kick(T.cats[p.c],'var(--am-'+p.c+')')+title('<bdi>'+esc(p.n)+'</bdi>')+'<p>'+num(line)+'</p>'+(extra?'<p class="nlam__cm">'+num(extra)+'</p>':'')+
   (p.e&&p.e>20?'<p class="nlam__cm">'+esc(T.edge)+'</p>':''),[p.x,p.y],null)}
 function filters(){if(!map||!map.getLayer('nlam-places'))return;var cats=['edu','parks','shop','transit'].filter(function(k){return on[k]});
  map.setFilter('nlam-places',['in',['get','cat'],['literal',cats]]);map.setLayoutProperty('nlam-ren','visibility',on.renewal?'visible':'none');
  map.setLayoutProperty('nlam-halo','visibility',on.projects?'visible':'none');pins.forEach(function(x){x.el.style.display=on.projects?'':'none'})}
 for(var i=0;i<chips.length;i++)chips[i].addEventListener('click',function(){var k=this.getAttribute('data-cat');on[k]=!on[k];this.setAttribute('aria-pressed',on[k]?'true':'false');filters()});
 reset.addEventListener('click',function(){if(!card.hidden)hide();if(map)map.easeTo({center:HOME.center,zoom:HOME.zoom,pitch:HOME.pitch,bearing:HOME.bearing,duration:still?0:900})})}
W.nlamInit=function(){var a=document.querySelectorAll('.nlam[data-cfg]');for(var i=0;i<a.length;i++){try{one(a[i])}catch(e){}}};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',W.nlamInit);else W.nlamInit()})();
"""


def scope(css):
    """Every rule that starts at a component class gets the root in front (.nlam .nlam__lead, specificity 0,2,0), so
    the theme's `.entry-content p{font-size:16px!important}` (0,1,1) and the `.nlint h2` article styles lose."""
    out, i, n = [], 0, len(css)
    while i < n:
        while i < n and css[i] in ' \t\r\n}':
            out.append(css[i]); i += 1
        if i >= n:
            break
        j = css.find('{', i)
        if j < 0:
            out.append(css[i:]); break
        sel = css[i:j]
        lead = sel[:len(sel) - len(sel.lstrip())]
        body = sel.strip()
        if not body.startswith('@'):
            parts = [x.strip() for x in body.split(',')]
            body = ','.join(('.nlam ' + x) if x.startswith('.nlam__') else x for x in parts)
        out.append(lead + body + '{')
        if sel.strip().startswith('@'):
            i = j + 1; continue
        k = css.find('}', j)
        out.append(css[j + 1:k + 1])
        i = k + 1
    return ''.join(out)


CSS = scope(CSS)


def selectors(css):
    """Every selector of every rule (inside @container / @media too), for the '.nlam first' check."""
    sels = []
    for m in re.finditer(r'([^{}]+)\{', css):
        s = m.group(1).strip()
        if s.startswith('@'):
            continue
        sels += [x.strip() for x in s.split(',')]
    return sels


def load(key):
    return json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), key + '.json'), encoding='utf-8'))


if __name__ == '__main__':
    import gzip
    d = load('rova-4')
    bad = [s for s in selectors(CSS) if not s.startswith('.nlam')]
    assert not bad, bad
    h = html(d).encode('utf-8')
    c, j = CSS.encode('utf-8'), JS.encode('utf-8')
    gz = lambda b: len(gzip.compress(b, 9))
    print('html %d (gz %d) css %d (gz %d) js %d (gz %d) total %d (gz %d)' % (
        len(h), gz(h), len(c), gz(c), len(j), gz(j), len(h) + len(c) + len(j), gz(h + c + j)))
