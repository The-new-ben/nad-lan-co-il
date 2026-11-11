# -*- coding: utf-8 -*-
"""The 1.72.648 hunks on the LIVE inc/project-stage.php (the 647 text, md5 595cce7bcf87...). HAD-712, Ben 11.11.2026: "Calculator and
images". Used by make_deploy648.py.
  A. the Kikar price calculator gains a financing block under the purchase-tax rows: minimum equity (with the purchase tax), the largest
     mortgage the Bank of Israel rules allow (75% for a single home, 50% for an additional one), the first monthly repayment and the net
     income it needs. The repayment per million comes from the site's own Bank of Israel data (nadlan_mm_pay, the banking system's
     average track mix and rates, 25 years, the latest month); the income is the repayment over 40% (directive 329's risk line; the
     limit is 50%). The block is plain HTML with the default numbers, and the script recomputes it on every change.
  B. the calculator script fills the block when it is in the markup (only Kikar's has it) and window.NLPG_MM is printed.
  C. the calculator styles: the block.
  D. the block's data: window.NLPG_MM, printed by PHP from assets/instruments/data/boi-mortgage.json.
  E. the Kikar article's figures (.nlws-fig): one picture, two or three in a row, a label on the picture, a caption under it."""
LIVE_MD5_PREFIX = "595cce7bcf87"

FIN = ('<div class="nlpg__fin" data-pg="fin"><p class="nlpg__finh">מימון, לפי כללי בנק ישראל</p><dl class="nlpg__rows">'
       '<div><dt>הון עצמי מינימלי, כולל מס הרכישה</dt><dd data-pg="eq">כ-<span class="nlds-num">2.72</span> מיליון ₪</dd></div>'
       '<div><dt>משכנתא מרבית, <span class="nlds-num"><span data-pg="lp">75</span>%</span> מהמחיר</dt><dd data-pg="ln">כ-<span class="nlds-num">6.83</span> מיליון ₪</dd></div>'
       '<div><dt>החזר חודשי ראשון</dt><dd data-pg="mo">כ-<span class="nlds-num">37,000</span> ₪</dd></div>'
       '<div class="nlpg__inc"><dt>הכנסה נטו נדרשת</dt><dd><span data-pg="inc">כ-<span class="nlds-num">93,000</span> ₪</span> <small>בחודש</small></dd></div></dl>'
       '<p class="nlpg__fina">משכנתא ל-<span class="nlds-num">25</span> שנה בתמהיל ובריביות הממוצעים במערכת הבנקאית, <span class="nlds-num" data-pg="fm">9.2026</span> (בנק ישראל). '
       'הכנסה נדרשת לפי החזר של <span class="nlds-num">40%</span> מההכנסה הפנויה; המגבלה היא <span class="nlds-num">50%</span>. זה ההחזר הראשון, לפני שינויי ריבית ומדד.</p></div>')
A_OLD = '<dd data-pg="tt">כ-<span class="nlds-num">9.54</span> מיליון ₪</dd></div></dl><p class="nlpg__why" data-pg="why">אומדן לפי הקומה:'
A_NEW = '<dd data-pg="tt">כ-<span class="nlds-num">9.54</span> מיליון ₪</dd></div></dl>' + FIN + '<p class="nlpg__why" data-pg="why">אומדן לפי הקומה:'

B_OLD = "  q('why').innerHTML=esc(m.why).replace(/\\d[\\d,.]*(?:[-–]\\d[\\d,.]*)?/g,isl);draw(m,lo,hi,fl);\n"
JS_FIN = ("  var F=q('fin'),M=window.NLPG_MM;if(F&&M&&M.pm>0){var ltv=val('nlpg-t')==='more'?M.l2:M.l1,ln=mid*ltv,mo=ln*M.pm/1e6;\n"
          "   q('eq').innerHTML=put(T.approx,put(T.u_mil,isl(mil(mid-ln+t))));q('lp').textContent=Math.round(ltv*100);q('ln').innerHTML=put(T.approx,put(T.u_mil,isl(mil(ln))));\n"
          "   q('mo').innerHTML=put(T.approx,put(T.u_ils,isl(nfk(mo))));q('inc').innerHTML=put(T.approx,put(T.u_ils,isl(nfk(mo/M.pti))));if(M.ym)q('fm').textContent=M.ym}\n")
B_NEW = B_OLD + JS_FIN

C_OLD = "}\nNLPG_CSS;\n"
CSS_FIN = ("}\n/* 1.72.648: the financing block under the purchase-tax rows (equity, mortgage, repayment, the income it needs) */\n"
           ".nlpg .nlpg__fin{margin:12px 0 0 !important;background:#eaf2f5;border-radius:12px;padding:12px 12px 10px}\n"
           ".nlpg .nlpg__fin .nlpg__finh{margin:0 0 4px !important;font-size:12.5px !important;font-weight:700 !important;color:#1f4b5c !important}\n"
           ".nlpg .nlpg__fin .nlpg__rows{margin:0 !important}\n"
           ".nlpg .nlpg__fin .nlpg__rows>div{border-color:#d5e4ea !important}\n"
           ".nlpg .nlpg__inc dt{font-weight:700 !important;color:#14212b !important}\n"
           ".nlpg .nlpg__inc dd{font-size:20px !important;font-weight:700 !important;color:#14212b !important;white-space:nowrap}\n"
           ".nlpg .nlpg__inc dd small{font-size:13px;font-weight:600}\n"
           ".nlpg .nlpg__fin .nlpg__fina{margin:8px 0 0 !important;font-size:12px !important;line-height:1.5 !important;color:#4a5a66 !important}\n"
           "NLPG_CSS;\n")
C_NEW = CSS_FIN

D_OLD = "\t\treturn '<style id=\"nlpg-css\">' . $css . '</style>' . $html . '<script id=\"nlpg-js\">' . $js . '</script>';\n"
D_NEW = ("\t\t// 1.72.648: the financing block's data, from the site's Bank of Israel file: the first payment on 1,000,000 ILS over 25 years at the\n"
         "\t\t// banking system's average mix and rates in the latest month, the LTV caps and the 40% payment-to-income line of directive 329\n"
         "\t\t$mm = '';\n"
         "\t\tif ( function_exists( 'nadlan_mm_data' ) && function_exists( 'nadlan_mm_pay' ) ) {\n"
         "\t\t\t$md = (array) nadlan_mm_data();\n"
         "\t\t\t$mo = isset( $md['by_bank']['months'] ) ? (array) $md['by_bank']['months'] : array();\n"
         "\t\t\t$mi = count( $mo ) - 1;\n"
         "\t\t\t$pm = $mi >= 0 ? (float) nadlan_mm_pay( $md, 'system', $mi ) : 0;\n"
         "\t\t\tif ( $pm > 1000 ) {\n"
         "\t\t\t\t$ym = explode( '-', (string) $mo[ $mi ] );\n"
         "\t\t\t\t$mm = '<script id=\"nlpg-mm\">window.NLPG_MM=' . wp_json_encode( array( 'pm' => (int) round( $pm ), 'ym' => (int) ( $ym[1] ?? 0 ) . '.' . (string) ( $ym[0] ?? '' ),\n"
         "\t\t\t\t\t'l1' => (float) ( $md['rules']['ltv']['single'] ?? 0.75 ), 'l2' => (float) ( $md['rules']['ltv']['invest'] ?? 0.5 ), 'pti' => (float) ( $md['rules']['pti_risk'] ?? 0.4 ) ) ) . ';</script>';\n"
         "\t\t\t}\n"
         "\t\t}\n"
         "\t\treturn '<style id=\"nlpg-css\">' . $css . '</style>' . $html . $mm . '<script id=\"nlpg-js\">' . $js . '</script>';\n")

E_OLD = "\t\t\t. '#nlpjx-finance:not(:has(.nlpjx-fin>*)){display:none}'\n"
FIG_CSS = (".nlws .nlws-fig{margin:18px 0 22px!important;padding:0!important;max-width:760px}"
           ".nlws .nlws-fig img{display:block!important;width:100%!important;height:auto!important;margin:0!important;border-radius:14px!important;background:#0d2129}"
           ".nlws .nlws-fig__g{display:grid;gap:6px}.nlws .nlws-fig__g--2{grid-template-columns:1fr 1fr}.nlws .nlws-fig__g--3{grid-template-columns:repeat(3,1fr)}"
           ".nlws .nlws-fig__g img{border-radius:12px!important;height:100%!important;object-fit:cover}"
           ".nlws .nlws-fig__i{position:relative;display:block}"
           ".nlws .nlws-fig__i b{position:absolute;bottom:8px;inset-inline-start:8px;background:rgba(13,33,41,.82);color:#fff;font:700 12.5px/1.2 Assistant,Heebo,sans-serif;padding:3px 9px;border-radius:999px}"
           ".nlws .nlws-fig figcaption{margin:7px 0 0!important;font-size:13px!important;line-height:1.5!important;color:#4a5a66!important;text-align:start!important}"
           ".nlws .nlws-fig figcaption b{color:#14212b}")
E_NEW = (E_OLD + "\t\t\t// 1.72.648: the article's figures (one picture, two or three in a row, a label on the picture, a caption under it)\n"
         "\t\t\t. '" + FIG_CSS + "'\n")

HUNKS = [(A_OLD, A_NEW), (B_OLD, B_NEW), (C_OLD, C_NEW), (D_OLD, D_NEW), (E_OLD, E_NEW)]


def apply(txt):
    for a, b in HUNKS:
        if txt.count(a) != 1:
            raise SystemExit("k648: FATAL anchor x%d: %r" % (txt.count(a), a[:70]))
        txt = txt.replace(a, b)
    if txt.count('data-pg="fin"') != 1 or txt.count("window.NLPG_MM=") != 1 or txt.count(".nlws .nlws-fig{") != 1:
        raise SystemExit("k648: FATAL the file is not as expected after the hunks")
    return txt
