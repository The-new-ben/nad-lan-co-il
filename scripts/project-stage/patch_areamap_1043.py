# -*- coding: utf-8 -*-
"""Design v104.3 (30.9.2026 evening, HAD-375, with Codex): the area map names its places, with the icon of their kind.
- The owner: "on maps I don't want to see dots ... a school is a school icon, a restaurant is a restaurant icon".
- Codex found why the icons were black blobs: icons() stripped the <svg> wrapper together with fill="none" stroke="#fff".
- One icon per KIND (assets/arealife/place-icons.js, 47 kinds, 38 glyphs), in the group colour; the list rows use it too.
- Collision on: the nearest place wins (symbol-sort-key = walking minutes), far ones step back instead of piling up.
- Names from zoom 14, on the free side (text-variable-anchor, RTL-first in Hebrew/Arabic); a name with no room drops, its icon stays.
  python patch_areamap_1043.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "arealife", "areamap.js")
s = open(F, encoding="utf-8").read()
if "v104.3" in s:
    raise SystemExit("already patched")


def sub(old, new, name):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{name}] anchor found {n} times")
    s = s.replace(old, new)


# the kind's icon, with the group icon as the fallback when the icon file is missing
sub("  var svg = function (g, stroke) { return '<svg viewBox=\"0 0 16 16\" fill=\"none\" stroke=\"' + (stroke || 'currentColor') + '\" stroke-width=\"1.7\" stroke-linecap=\"round\" stroke-linejoin=\"round\">' + PATH[g] + '</svg>'; };\n",
    "  var svg = function (g, stroke) { return '<svg viewBox=\"0 0 16 16\" fill=\"none\" stroke=\"' + (stroke || 'currentColor') + '\" stroke-width=\"1.7\" stroke-linecap=\"round\" stroke-linejoin=\"round\">' + PATH[g] + '</svg>'; };\n"
    "  /* v104.3 (30.9): a place shows the icon of its KIND (assets/arealife/place-icons.js, loaded before this file): a school is a\n"
    "     school, a café a cup, a bus stop a bus. The seven group icons above stay for the group chips and as the fallback. */\n"
    "  var PI = function () { return window.NLPlaceIcons || null; };\n"
    "  var kindSvg = function (p, stroke) { var I = PI(); return I ? I.svg(p.k, p.g, stroke, 2.2) : svg(p.g, stroke); };\n",
    "kindSvg")

# the list rows and the popup: the kind's icon
sub("      b.innerHTML = '<i style=\"background:' + COLOR[p.g] + '\">' + svg(p.g) + '</i><span><b><bdi>'",
    "      b.innerHTML = '<i style=\"background:' + COLOR[p.g] + '\">' + kindSvg(p) + '</i><span><b><bdi>'",
    "list icon")

# the features carry the icon id of their kind
sub("properties: { i: PLACES.indexOf(p), g: p.g, name: nameOf(p), rank: (REG ? (p.walk || 99) : p.dist / 80) } };",
    "properties: { i: PLACES.indexOf(p), g: p.g, ic: iconId(p), name: nameOf(p), rank: (REG ? (p.walk || 99) : p.dist / 80) } };",
    "feature ic")

# the images: one per (kind glyph, group colour) in use; the wrapper keeps fill/stroke (the black-blob bug)
sub("""  function icons(map) {
    return Promise.all(ORDER.map(function (g) {
      return new Promise(function (res) {
        var img = new Image(48, 48);
        img.onload = function () { try { if (!map.hasImage('nlam-' + g)) map.addImage('nlam-' + g, img, { pixelRatio: 2 }); } catch (e) {} res(); };
        img.onerror = function () { res(); };
        img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48"><circle cx="24" cy="24" r="21" fill="' + COLOR[g] + '" stroke="#fff" stroke-width="4"/><g transform="translate(12 12) scale(1.5)">' + svg(g, '#fff').replace(/^<svg[^>]*>|<\\/svg>$/g, '') + '</g></svg>');
      });
    }));
  }
""",
    """  /* v104.3: the map pin of a place = the icon of its kind in its group colour. Codex (30.9) found the old pins painted black:
     the regex stripped the <svg> wrapper together with fill="none" stroke="#fff". The <g> below carries them. */
  function iconId(p) { var I = PI(); return 'nlpi-' + (I ? I.glyph(p.k, p.g) : 'g') + '-' + p.g; }
  function pinSrc(p) {
    var I = PI();
    if (I) return I.pinSvg(p.k, p.g, 52);
    return '<svg xmlns="http://www.w3.org/2000/svg" width="52" height="52" viewBox="0 0 52 52"><circle cx="26" cy="26" r="23" fill="' + COLOR[p.g] + '" stroke="#FAF7F1" stroke-width="3"/>'
      + '<g transform="translate(14 14) scale(1.5)" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + PATH[p.g] + '</g></svg>';
  }
  function icons(map) {
    var need = {};
    PLACES.forEach(function (p) { var id = iconId(p); if (!need[id]) need[id] = p; });
    return Promise.all(Object.keys(need).map(function (id) {
      return new Promise(function (res) {
        var img = new Image(52, 52);
        img.onload = function () { try { if (!map.hasImage(id)) map.addImage(id, img, { pixelRatio: 2 }); } catch (e) {} res(); };
        img.onerror = function () { res(); };
        img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(pinSrc(need[id]));
      });
    }));
  }
""",
    "icons")

# the layer: collision on, names from zoom 14 on the free side
sub("""      map.addLayer({ id: 'nlam-pin', type: 'symbol', source: 'nlam', layout: {
        'icon-image': ['concat', 'nlam-', ['get', 'g']], 'icon-size': ['interpolate', ['linear'], ['zoom'], 13, 0.62, 16, 0.9], 'icon-allow-overlap': true,
        'symbol-sort-key': ['get', 'rank'],
        'text-field': ['step', ['zoom'], '', 15.2, ['get', 'name']], 'text-font': ['DIN Pro Medium', 'Arial Unicode MS Regular'], 'text-size': 12,
        'text-offset': [0, 1.35], 'text-anchor': 'top', 'text-optional': true, 'text-max-width': 9 },
        paint: { 'text-color': '#14212B', 'text-halo-color': 'rgba(250,247,241,.95)', 'text-halo-width': 1.6 } });""",
    """      // v104.3: every place that has room shows its icon and its name; the nearest wins a collision (sort key = walking
      // minutes), the far ones step back instead of piling up; a name with no room drops and its icon stays
      map.addLayer({ id: 'nlam-pin', type: 'symbol', source: 'nlam', layout: {
        'icon-image': ['get', 'ic'], 'icon-size': ['interpolate', ['linear'], ['zoom'], 12, 0.72, 14, 0.88, 16, 1],
        'icon-allow-overlap': false, 'icon-padding': 1,
        'symbol-sort-key': ['get', 'rank'],
        'text-field': ['step', ['zoom'], '', 14, ['get', 'name']], 'text-font': ['DIN Pro Medium', 'Arial Unicode MS Regular'],
        'text-size': ['interpolate', ['linear'], ['zoom'], 14, 12, 17, 13.5],
        'text-variable-anchor': RTL ? ['right', 'left', 'top', 'bottom'] : ['left', 'right', 'top', 'bottom'],
        'text-radial-offset': 1.2, 'text-justify': 'auto', 'text-optional': true, 'text-max-width': 9, 'text-padding': 2 },
        paint: { 'text-color': '#14212B', 'text-halo-color': 'rgba(250,247,241,.96)', 'text-halo-width': 1.8 } });""",
    "layer")

open(F, "w", encoding="utf-8", newline="\n").write(s)
print("areamap.js patched", len(s))
