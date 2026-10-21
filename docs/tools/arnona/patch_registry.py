# -*- coding: utf-8 -*-
"""HAD-575 / Kikar tools #4: register "arnona" in inc/instruments.php (entry + a plain summary of the 2026 rates). Once only."""
import io, os
p = r"C:\Users\777\nad-lan\nad-lan-co-il\plugins\nadlan-config\inc\instruments.php"
s = io.open(p, encoding="utf-8", newline="").read()
assert "'arnona' =>" not in s, "already registered"
reg_end = "\t\t\t),\n\t\t) );\n"
assert s.count(reg_end) == 1
s = s.replace(reg_end, "\t\t\t),\n"
  "\t\t\t'arnona' => array(\n"
  "\t\t\t\t'name' => 'מחשבון ארנונה תל אביב 2026', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · ארנונה',\n"
  "\t\t\t\t'desc' => 'ארנונה למגורים בתל אביב-יפו לשנת 2026 לפי צו הארנונה של העירייה: אזור, סוג הבניין לפי שנת הבנייה, שטח הדירה עם המרפסות, הנחות ותשלום דו־חודשי.',\n"
  "\t\t\t\t'data' => array( 'arnona-tlv.json' ),\n"
  "\t\t\t\t'related' => array( '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/property-value-estimator/' => 'מחשבון שווי דירה', '/tel-aviv-apartment-prices/' => 'מחירי דירות בתל אביב', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),\n"
  "\t\t\t),\n\t\t) );\n")
sum_end = "\t\tif ( 'pval' === $id ) {"
assert s.count(sum_end) == 1
s = s.replace(sum_end, "\t\tif ( 'arnona' === $id ) {\n"
  "\t\t\treturn '<p>ארנונה למגורים בתל אביב-יפו לשנת 2026, לפי צו הארנונה של העירייה (₪ למ״ר לשנה), בבניין שהושלם מ־2022 ואילך: אזור 1, דירה עד 140 מ״ר 112.99 ומעל 140 מ״ר 139.60; אזור 2, 90.71 ו־108.98; אזור 3, 78.39; אזורים 4 ו־5, 64.42. מעל 140 מ״ר כל הדירה מחויבת בתעריף הגבוה. מרפסות נכללות בשטח, חניה לא. עולה חדש: 50% על עד 100 מ״ר ל־12 חודשים.</p>';\n"
  "\t\t}\n" + sum_end)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("arnona registered")
