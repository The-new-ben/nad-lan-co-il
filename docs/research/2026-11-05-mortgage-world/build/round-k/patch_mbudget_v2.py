# -*- coding: utf-8 -*-
"""Round K (HAD-675): mbudget v1 -> v2. When no priced home for sale on the site fits the budget, the tool showed a dead end on its
own default example (1,926,000 vs the closest listing at 2,000,000). v2 keeps the note and adds up to three of the closest priced
homes ABOVE the budget, each labelled with how much it is above. Nothing else changes. python patch_mbudget_v2.py
After the first live check (it listed Tel Aviv homes 2.7 and 3 million above the budget) the filter was capped by hand in mbudget.js
at 15% above the budget (`+x.price <= max * 1.15`); mbudget.js is the reference, not this script."""
import io, os
H = os.path.dirname(os.path.abspath(__file__))
P = os.path.abspath(os.path.join(H, "..", "..", "..", "..", "..", "plugins", "nadlan-config", "assets", "instruments", "tools", "mbudget.js"))
s = io.open(P, encoding="utf-8").read()
assert "above:" not in s, "already v2"
def one(a, b):
    global s
    assert s.count(a) == 1, (a[:60], s.count(a)); s = s.replace(a, b)
one("   free, tested by test_mbudget.js in node). Hebrew only (RTL); no long dash anywhere in visible text. */",
    "   free, tested by test_mbudget.js in node). Hebrew only (RTL); no long dash anywhere in visible text.\n"
    "   v2 (round K, 6.11.2026): when no priced home fits, up to three of the closest priced homes ABOVE the budget, each with how much it\n"
    "   is above (the default example, 1,926,000, had none under it and one at 2,000,000). NLMB.listings returns `above` too. */")
one("    var fit = sale.filter(function (x) { return +x.price <= max; }).sort(function (a, b) { return b.price - a.price; });\n"
    "    return { priced: sale.length, count: fit.length, updated: nf && nf.updated ? String(nf.updated) : '',\n"
    "      items: fit.slice(0, lim || 6).map(function (x) { return { id: x.id, title: String(x.title), city: x.city ? String(x.city) : '', price: +x.price, rooms: +x.rooms || 0, sqm: +x.sqm || 0, url: safeUrl(x.url) }; }) };",
    "    var fit = sale.filter(function (x) { return +x.price <= max; }).sort(function (a, b) { return b.price - a.price; });\n"
    "    var up = sale.filter(function (x) { return +x.price > max; }).sort(function (a, b) { return a.price - b.price; });  // v2: the closest above\n"
    "    function card(x) { return { id: x.id, title: String(x.title), city: x.city ? String(x.city) : '', price: +x.price, rooms: +x.rooms || 0, sqm: +x.sqm || 0, url: safeUrl(x.url) }; }\n"
    "    return { priced: sale.length, count: fit.length, updated: nf && nf.updated ? String(nf.updated) : '',\n"
    "      items: fit.slice(0, lim || 6).map(card), above: up.slice(0, 3).map(card) };")
one("    if (!res.count) return '<p class=\"nli__note\">כרגע אין באתר דירה למכירה עם מחיר מפורסם עד ' + b(ils(m.price)) + '.</p>' + all;",
    "    if (!res.count) {\n"
    "      h = '<p class=\"nli__note\">כרגע אין באתר דירה למכירה עם מחיר מפורסם עד ' + b(ils(m.price)) + '.</p>';\n"
    "      if (res.above && res.above.length) {  // v2: the closest above the budget, each with the gap\n"
    "        h += '<p class=\"nlmb__meta\">' + (res.above.length > 1 ? 'הדירות הקרובות ביותר מעל הסכום:' : 'הדירה הקרובה ביותר מעל הסכום:') + '</p><ul class=\"nlmb__homes\">' + res.above.map(function (x) {\n"
    "          var meta = [x.city, x.rooms ? num(x.rooms, x.rooms % 1 ? 1 : 0) + ' חדרים' : '', x.sqm ? num(x.sqm) + ' מ״ר' : '', ils(x.price - m.price) + ' מעל הסכום'].filter(Boolean).map(esc).join(' · ');\n"
    "          return '<li class=\"nlmb__home\"><a href=\"' + esc(x.url) + '\">' + esc(x.title) + '</a><span class=\"nlmb__meta\">' + meta + '</span><strong>' + b(ils(x.price)) + '</strong></li>';\n"
    "        }).join('') + '</ul>';\n"
    "      }\n"
    "      return h + all;\n"
    "    }")
io.open(P, "w", encoding="utf-8", newline="").write(s); print("mbudget v2 written")
