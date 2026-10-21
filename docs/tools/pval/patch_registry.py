# -*- coding: utf-8 -*-
"""HAD-575 / Kikar tools #1: register "pval" in inc/instruments.php (entry + the plain summary with official medians that search
engines and AI answers read before the script runs). Refuses to run twice."""
import io, json, os
R = r"C:\Users\777\nad-lan\nad-lan-co-il\plugins\nadlan-config"
p = os.path.join(R, "inc", "instruments.php")
s = io.open(p, encoding="utf-8", newline="").read()
assert "'pval' =>" not in s, "already registered"
reg_end = "\t\t\t),\n\t\t) );\n"
assert s.count(reg_end) == 1
s = s.replace(reg_end, "\t\t\t),\n"
  "\t\t\t'pval' => array(\n"
  "\t\t\t\t'name' => 'מחשבון שווי דירה', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · שווי דירה',\n"
  "\t\t\t\t'desc' => 'כמה שווה דירה לפי העסקאות שנסגרו: המחיר החציוני לפי מספר החדרים בשכונה או בעיר (נתוני רשות המסים), עם התאמות למצב, לקומה ולבניין, טווח זהירות ובדיקת מחיר מבוקש, או חישוב לפי מחיר למ״ר.',\n"
  "\t\t\t\t'data' => array( 'value.json' ),\n"
  "\t\t\t\t'related' => array( '/apartment-prices/' => 'מחירון הדירות לפי עיר', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),\n"
  "\t\t\t),\n\t\t) );\n")
sum_end = "\t\tif ( 'pcost' === $id ) {"
assert s.count(sum_end) == 1
s = s.replace(sum_end, "\t\tif ( 'pval' === $id ) {\n"
  "\t\t\t$path = dirname( __DIR__ ) . '/assets/instruments/data/value.json';\n"
  "\t\t\t$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;\n"
  "\t\t\tif ( ! is_array( $x ) || empty( $x['cities'] ) ) { return ''; }\n"
  "\t\t\t$rows = '';\n"
  "\t\t\tforeach ( $x['cities'] as $name => $c ) { $rows .= '<tr><td>' . esc_html( $name ) . '</td><td>' . ( $c['r3'] ? esc_html( number_format( $c['r3'] ) ) : '-' ) . '</td><td>' . ( $c['r4'] ? esc_html( number_format( $c['r4'] ) ) : '-' ) . '</td><td>' . ( $c['r5'] ? esc_html( number_format( $c['r5'] ) ) : '-' ) . '</td></tr>'; }\n"
  "\t\t\treturn '<p>המחיר החציוני של דירות שנמכרו לפי מספר החדרים, ברבעון האחרון שפורסם לכל עיר (ברובן 1-3.2026), לפי נתוני רשות המסים (₪):</p><table><thead><tr><th>עיר</th><th>3 חדרים</th><th>4 חדרים</th><th>5 חדרים</th></tr></thead><tbody>' . $rows . '</tbody></table>';\n"
  "\t\t}\n" + sum_end)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("pval registered")
