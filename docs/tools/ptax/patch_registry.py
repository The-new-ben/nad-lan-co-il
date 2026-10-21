# -*- coding: utf-8 -*-
"""HAD-527 / Kikar tools #2: register the "ptax" tool in inc/instruments.php (the registry entry + the plain summary that
search engines and AI answers read before the script runs). Run once on the 1.72.477 file; refuses to run twice."""
import io
p = r"C:\Users\777\nad-lan\nad-lan-co-il\plugins\nadlan-config\inc\instruments.php"
s = io.open(p, encoding="utf-8", newline="").read()
assert "'ptax' =>" not in s, "already registered"
reg_end = "\t\t\t),\n\t\t) );\n"
assert s.count(reg_end) == 1, s.count(reg_end)
entry = ("\t\t\t),\n"
         "\t\t\t'ptax' => array(\n"
         "\t\t\t\t'name' => 'מחשבון מס רכישה', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · מס רכישה',\n"
         "\t\t\t\t'desc' => 'מחשב את מס הרכישה על דירה לפי המדרגות של רשות המסים בכל ארבעת המסלולים: דירה יחידה, דירה נוספת, עולה חדש ותושב חוץ, כולל קנייה של חלק מדירה, השיעור האפקטיבי והמס בכל מדרגה.',\n"
         "\t\t\t\t'data' => array( 'ptax.json' ),\n"
         "\t\t\t\t'related' => array( '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/mortgage-calculator/' => 'מחשבון משכנתא', '/real-estate-lawyer/' => 'עורך דין לקניית דירה', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),\n"
         "\t\t\t),\n"
         "\t\t) );\n")
s = s.replace(reg_end, entry)
sum_end = "\t\tif ( 'delay' === $id ) {"
assert s.count(sum_end) == 1
summary = ("\t\tif ( 'ptax' === $id ) {\n"
           "\t\t\t$path = dirname( __DIR__ ) . '/assets/instruments/data/ptax.json';\n"
           "\t\t\t$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;\n"
           "\t\t\tif ( ! is_array( $x ) || empty( $x['tracks']['single'] ) ) { return ''; }\n"
           "\t\t\t$fmt = function ( $br ) { $o = array(); $lo = 0; foreach ( $br as $b ) { $o[] = number_format( $b[1] * 100, $b[1] * 100 == (int) ( $b[1] * 100 ) ? 0 : 1 ) . '% ' . ( null === $b[0] ? 'מעל ' . number_format( $lo ) . ' ₪' : 'עד ' . number_format( $b[0] ) . ' ₪' ); $lo = $b[0]; } return implode( ', ', $o ); };\n"
           "\t\t\treturn '<p>מדרגות מס רכישה על דירת מגורים לפי רשות המסים, בתוקף מ־' . esc_html( date_i18n( 'j.n.Y', strtotime( $x['effective'] ) ) ) . ' ומוקפאות עד ' . esc_html( date_i18n( 'j.n.Y', strtotime( $x['frozen_until'] ) ) ) . '. דירה יחידה: ' . esc_html( $fmt( $x['tracks']['single'] ) )\n"
           "\t\t\t\t. '. דירה נוספת ותושב חוץ: ' . esc_html( $fmt( $x['tracks']['extra'] ) ) . '. עולה חדש: ' . esc_html( $fmt( $x['tracks']['oleh'] ) ) . '. המס מחושב על שווי הדירה כולה, וקונה של חלק משלם לפי החלק שלו.</p>';\n"
           "\t\t}\n")
s = s.replace(sum_end, summary + sum_end)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("ptax registered")
