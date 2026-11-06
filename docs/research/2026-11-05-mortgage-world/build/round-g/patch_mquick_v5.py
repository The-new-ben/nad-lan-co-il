# -*- coding: utf-8 -*-
"""Round G (T8, HAD-675): mquick v4 -> v5, the full monthly cost under the result. Applies anchored edits to the repo copy of
plugins/nadlan-config/assets/instruments/tools/mquick.js (each anchor must occur once). python patch_mquick_v5.py
After the first local check the insurance note (xn) was shortened by hand in mquick.js (the arnona sentence and "כתנאי למשכנתא"
dropped, the English shortened) to save about 40 px on a phone; mquick.js is the reference, not this script's xn strings."""
import io, os
H = os.path.dirname(os.path.abspath(__file__))
P = os.path.abspath(os.path.join(H, "..", "..", "..", "..", "..", "plugins", "nadlan-config", "assets", "instruments", "tools", "mquick.js"))
s = io.open(P, encoding="utf-8").read()
assert "fullCost" not in s, "already v5"


def one(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


one('name missing from it stays Hebrew with lang="he". Pure part: NLMQ.cityList / NLMQ.quarterEn (node test). */',
    'name missing from it stays Hebrew with lang="he". Pure part: NLMQ.cityList / NLMQ.quarterEn (node test).\n'
    '   v5 (round G, T8, HAD-675, 6.11.2026; benchmark row "taxes, insurance or HOA inside the monthly figure"): under the result, two\n'
    '   optional fields, "ביטוח חיים ומבנה" and "ארנונה וועד בית" (monthly, in shekels). They start EMPTY: there is no official price\n'
    '   table for mortgage insurance, so no number is invented and no zero is shown. Once a sum is typed, "העלות החודשית של הדירה" = the\n'
    '   payment + the typed costs, with only the typed parts in the breakdown, in all three modes; the copied text adds the line. A note\n'
    '   names the Capital Market Authority\'s comparison calculators (life.cma.gov.il, dira.cma.gov.il; both checked 6.11.2026). Pure part:\n'
    '   NLMQ.fullCost(pay, ins, arn) (node test). Everything else is v4. */')
one("  window.NLMQ = { payPer1: payPer1, solve: solve, TR: TR, cityList: cityList, quarterEn: quarterEn, CITY_EN: CITY_EN };",
    "  /* v5: the full monthly cost; a part that was not typed (0, empty or not a number) stays out of the sum and of the breakdown */\n"
    "  function fullCost(pay, ins, arn) { var a = ins > 0 ? ins : 0, b = arn > 0 ? arn : 0; return { total: (pay > 0 ? pay : 0) + a + b, ins: a, arn: b, any: a + b > 0 }; }\n"
    "  window.NLMQ = { payPer1: payPer1, solve: solve, TR: TR, cityList: cityList, quarterEn: quarterEn, CITY_EN: CITY_EN, fullCost: fullCost };")
one("""    + '#nlmq .nlmq__cq{display:block;margin:6px 0 0!important;font:400 12px/18px "IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace!important;color:#5E6A75!important}';""",
    """    + '#nlmq .nlmq__cq{display:block;margin:6px 0 0!important;font:400 12px/18px "IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace!important;color:#5E6A75!important}'
    /* v5: the full monthly cost (two fields side by side, also on a phone) */
    + '#nlmq .nlmq__more{display:flex;flex-direction:column;gap:10px}#nlmq .nlmq__x2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}'
    + '#nlmq .nlmq__x2 .nlmq__in{height:46px;padding:0 10px}#nlmq .nlmq__x2 .nlmq__in input{font-size:18px!important}#nlmq .nlmq__x2 .nlmq__lab{margin:0 0 6px!important}'
    + '#nlmq .nlmq__tot{display:flex;flex-direction:column;gap:2px;background:#F6F8F9;border-inline-start:3px solid #2F6F86;padding:10px 12px}#nlmq .nlmq__tot[hidden]{display:none!important}'
    + '#nlmq .nlmq__tl{font-size:13px;line-height:18px;color:#3E4C58}#nlmq .nlmq__tf{font:500 26px/32px "IBM Plex Mono",ui-monospace,monospace;color:#12202A}#nlmq .nlmq__tb{font:400 12px/18px "IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace;color:#5E6A75}'
    + '#nlmq p.nlmq__xn{margin:0!important;font-size:12px!important;line-height:18px!important;color:#5E6A75!important}#nlmq p.nlmq__xn a{color:#2F6F86!important}';""")
one("        city: 'City (median price, 4 rooms)', nocity: 'Choose a city'\n      } : {",
    "        city: 'City (median price, 4 rooms)', nocity: 'Choose a city',\n"
    "        xl: 'Other monthly costs, if you know them', ins: 'Life and structure insurance', arn: 'Arnona and building fees',\n"
    "        tl2: 'Full monthly cost of the home', tp: 'payment', ti: 'insurance', ta: 'arnona and building fees',\n"
    "        xn: 'Banks require mortgage life insurance and structure insurance, and you choose the insurer. The Capital Market Authority compares prices: "
    "<a href=\"https://life.cma.gov.il/\" target=\"_blank\" rel=\"noopener\">life insurance for a mortgage</a> · "
    "<a href=\"https://dira.cma.gov.il/\" target=\"_blank\" rel=\"noopener\">home and structure insurance</a> (in Hebrew). Arnona, the municipal tax, follows the city\\'s arnona order.',\n"
    "        cl: 'Full monthly cost with the costs I typed: '\n      } : {")
one("        city: 'עיר (מחיר חציוני, 4 חדרים)', nocity: 'בחרו עיר'\n      };",
    "        city: 'עיר (מחיר חציוני, 4 חדרים)', nocity: 'בחרו עיר',\n"
    "        xl: 'עלויות נוספות בחודש, אם ידועות לכם', ins: 'ביטוח חיים ומבנה', arn: 'ארנונה וועד בית',\n"
    "        tl2: 'העלות החודשית של הדירה', tp: 'החזר', ti: 'ביטוחים', ta: 'ארנונה וועד בית',\n"
    "        xn: 'הבנק דורש ביטוח חיים וביטוח מבנה כתנאי למשכנתא, ואתם בוחרים את חברת הביטוח. השוואת מחירים ברשות שוק ההון: "
    "<a href=\"https://life.cma.gov.il/\" target=\"_blank\" rel=\"noopener\">ביטוח חיים למשכנתא</a> · "
    "<a href=\"https://dira.cma.gov.il/\" target=\"_blank\" rel=\"noopener\">ביטוח מבנה</a>. הארנונה לפי צו הארנונה של העירייה.',\n"
    "        cl: 'העלות החודשית עם העלויות שהקלדתי: '\n      };")
one("""        + '<span class="nlmq__ltv" hidden></span></div>'\n""",
    """        + '<span class="nlmq__ltv" hidden></span></div>'
        + '<div class="nlmq__more"><span class="nlmq__lab" id="nlmq-xl">' + T.xl + '</span><div class="nlmq__x2" role="group" aria-labelledby="nlmq-xl">'
        + fld('nlmq-xi', 'ins', T.ins).replace('data-k="', 'data-x="') + fld('nlmq-xa', 'arn', T.arn).replace('data-k="', 'data-x="') + '</div>'
        + '<div class="nlmq__tot" aria-live="polite" hidden><span class="nlmq__tl">' + T.tl2 + '</span><span class="nlmq__tf"></span><span class="nlmq__tb"></span></div>'
        + '<p class="nlmq__xn">' + T.xn + '</p></div>'\n""")
one("var v = { mode: 'amount', amount: 1000000, price: 1600000, equity: 400000, pay: 6000, years: 25, bank: 'system', city: null };",
    "var v = { mode: 'amount', amount: 1000000, price: 1600000, equity: 400000, pay: 6000, years: 25, bank: 'system', city: null, ins: 0, arn: 0 };")
A7 = "'. ממוצע, לא הצעה אישית.';\n      }"
one(A7, "'. ממוצע, לא הצעה אישית.';\n"
        "        var fc = fullCost(r.pay, v.ins, v.arn), tb = q('.nlmq__tot');  // v5\n"
        "        tb.hidden = !fc.any;\n"
        "        if (fc.any) {\n"
        "          q('.nlmq__tf').innerHTML = '<bdi>' + IL(fc.total) + '</bdi>';\n"
        "          q('.nlmq__tb').innerHTML = [[T.tp, r.pay], [T.ti, fc.ins], [T.ta, fc.arn]].filter(function (x) { return x[1] > 0; })\n"
        "            .map(function (x) { return x[0] + ' <bdi>' + NF.format(Math.round(x[1])) + '</bdi>'; }).join(' + ');\n"
        "        }\n      }")
one("      /* v4: a city fills the price with its median 4-room deal; another typed price clears the city */",
    "      qa('input[data-x]').forEach(function (inp) {  // v5: empty until typed; an emptied field drops out of the sum\n"
    "        var k = inp.getAttribute('data-x');\n"
    "        inp.addEventListener('input', function () { var n = num(inp.value); v[k] = isFinite(n) && n > 0 ? n : 0; paint(); });\n"
    "        inp.addEventListener('blur', function () { inp.value = v[k] > 0 ? NF.format(v[k]) : ''; });\n"
    "      });\n"
    "      /* v4: a city fills the price with its median 4-room deal; another typed price clears the city */")
one("          var done = function () { b.textContent = T.copied;",
    "          var fx = fullCost(last.pay, v.ins, v.arn); if (fx.any) tx = tx.replace('\\n' + location.origin, ' ' + T.cl + IL(fx.total) + '.\\n' + location.origin);  // v5\n"
    "          var done = function () { b.textContent = T.copied;")
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("mquick v5 written,", len(s), "chars")
