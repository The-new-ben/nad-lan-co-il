# -*- coding: utf-8 -*-
"""Round R part 6 (1.72.616), found by the press of 1.72.615 at 390 px:
  - the chart scales to ~336 px on a phone, so 12-unit text drew at ~6 px: phone text is 20-22 units (~11 px), only every 6th month;
  - the last value and the last month were clipped at the right edge, and the low label sat on the last one: the last labels are
    anchored to the end, and a low point within 3 months of the last puts its label under the point;
  - the y-axis margin grows to 66 units so the bigger phone labels fit;
  - copy: if the clipboard refuses (no permission, an old browser), the textarea copy runs instead of nothing."""
import io, os
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
F = os.path.join(REPO, "plugins", "nadlan-config", "inc", "mortgage-market.php")
s = io.open(F, encoding="utf-8", newline="").read().replace(chr(13) + chr(10), chr(10))
pairs = [
    ("$w = 640; $hgt = 200; $pl = 46; $pr = 12; $pt = 16; $pb = 28;", "$w = 640; $hgt = 200; $pl = 66; $pr = 14; $pt = 22; $pb = 30;"),
    ("\t\t\tif ( 0 === $k % 3 || $k === $n - 1 ) { $h .= '<text x=\"' . $x( $k ) . '\" y=\"' . ( $hgt - 8 ) . '\" class=\"xa\">' . esc_html( nadlan_mm_short_month( $r['ym'] ) ) . '</text>'; }",
     "\t\t\tif ( 0 === $k % 3 || $k === $n - 1 ) { $h .= '<text x=\"' . $x( $k ) . '\" y=\"' . ( $hgt - 8 ) . '\" class=\"xa' . ( 0 === $k % 6 || $k === $n - 1 ? ' x6' : '' ) . ( $k === $n - 1 ? ' xe' : '' ) . '\">' . esc_html( nadlan_mm_short_month( $r['ym'] ) ) . '</text>'; }"),
    ("\t\tforeach ( array_unique( array( $hi, $lo, $n - 1 ) ) as $k ) {\n\t\t\t$h .= '<circle cx=\"' . $x( $k ) . '\" cy=\"' . $y( $rows[ $k ]['system'] ) . '\" r=\"4\" class=\"pt\"/><text x=\"' . $x( $k ) . '\" y=\"' . ( $y( $rows[ $k ]['system'] ) - 9 ) . '\" class=\"pv\">' . nadlan_mm_nf( $rows[ $k ]['system'] ) . '</text>';\n\t\t}",
     "\t\tforeach ( array_unique( array( $hi, $lo, $n - 1 ) ) as $k ) {\n"
     "\t\t\t$under = ( $k === $lo && $k !== $n - 1 && $n - 1 - $k <= 3 );  // a low next to the last point: its label goes under the point\n"
     "\t\t\t$h .= '<circle cx=\"' . $x( $k ) . '\" cy=\"' . $y( $rows[ $k ]['system'] ) . '\" r=\"4\" class=\"pt\"/><text x=\"' . $x( $k ) . '\" y=\"' . ( $y( $rows[ $k ]['system'] ) + ( $under ? 24 : -10 ) ) . '\" class=\"pv' . ( $k === $n - 1 ? ' pe' : '' ) . '\">' . nadlan_mm_nf( $rows[ $k ]['system'] ) . '</text>';\n"
     "\t\t}"),
    (".nlmm__fig .ya{text-anchor:end}.nlmm__fig .xa{text-anchor:middle}.nlmm__fig .pv{text-anchor:middle;fill:#12202A;font-size:13px}",
     ".nlmm__fig .ya{text-anchor:end}.nlmm__fig .xa{text-anchor:middle}.nlmm__fig .xa.xe{text-anchor:end}.nlmm__fig .pv{text-anchor:middle;fill:#12202A;font-size:13px}.nlmm__fig .pv.pe{text-anchor:end}"
     "@media (max-width:600px){.nlmm__fig text{font-size:20px}.nlmm__fig .pv{font-size:22px}.nlmm__fig .xa:not(.x6){display:none}}"),
    ("if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,function(){});}else{var a=document.createElement(\"textarea\");a.value=t;document.body.appendChild(a);a.select();try{document.execCommand(\"copy\");done();}catch(x){}a.remove();}",
     "var old=function(){var a=document.createElement(\"textarea\");a.value=t;a.setAttribute(\"readonly\",\"\");a.style.position=\"fixed\";a.style.opacity=\"0\";document.body.appendChild(a);a.select();try{if(document.execCommand(\"copy\")){done();}}catch(x){}a.remove();};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,old);}else{old();}"),
]
for a, b in pairs:
    assert s.count(a) == 1, ("anchor", a[:70], s.count(a))
    s = s.replace(a, b)
io.open(F, "w", encoding="utf-8", newline="").write(s.replace(chr(10), chr(13) + chr(10)))
print("ok")
