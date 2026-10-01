# -*- coding: utf-8 -*-
"""1.72.391 (the V2 loop turn 4; HAD-380): inc/project-stage.php without source names on the Kikar Hamedina pages (the owner, 1.10:
"מספיק עם הקרדיטים ומספיק עם המקורות"); the facts stay, the sources stay in facts.md.
  - the quick facts (five languages): no "לפי ויקיפדיה ואשטרום" / "per Wikipedia" / "selon" / "по данным" / "وفق"; the apartments'
    line says the average size (facts.md 1.5) instead of its sources; occupancy "2026 עד 2028" without "לפי המקורות";
  - the deals block (Hebrew page): its intro and summary lines without sources, the intro opens "מידע גלוי"; a page config flag
    'deals_nosrc' drops the source column (only Kikar sets it; every other project keeps its column);
  - the basket's price hint (Hebrew; V4); the stage's hint line (five languages): the page's flow now (a tower, a floor, an apartment by its direction; the floor plan,
    the deal prices, the view from its windows), no longer promising the sun hours.
The illustration's data line (src_line: the municipality's open GIS layers) stays: it is the data licence's attribution.
HUNKS are applied to the LIVE text by the runner (each must match once) and to the branch file by `python kikar_php_391.py`."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config", "inc", "project-stage.php")

HUNKS = [
    # the deals renderer: an optional source column
    ("""		$h .= '<table class="nlpd__table"><thead><tr><th scope="col">קומה</th><th scope="col">הדירה</th><th scope="col">מחיר</th><th scope="col">למ״ר</th><th scope="col">מועד</th><th scope="col">מקור</th>""",
     """		$nosrc = ! empty( $ps['deals_nosrc'] ); // 1.72.391: a page that names no sources (Kikar Hamedina) drops the column
		$h .= '<table class="nlpd__table"><thead><tr><th scope="col">קומה</th><th scope="col">הדירה</th><th scope="col">מחיר</th><th scope="col">למ״ר</th><th scope="col">מועד</th>' . ( $nosrc ? '' : '<th scope="col">מקור</th>' ) . '"""),
    ("""				. '<td>' . esc_html( $d['date'] ) . '</td><td class="nlpd__src">' . $src . '</td>'""",
     """				. '<td>' . esc_html( $d['date'] ) . '</td>' . ( $nosrc ? '' : '<td class="nlpd__src">' . $src . '</td>' )"""),
    # Hebrew quick facts, progress, deals
    ("'40, 40 ו-37 קומות, לפי ויקיפדיה ואשטרום'", "'40, 40 ו-37 קומות'"),
    ("array( 'דירות', '453', 'לפי אשטרום וגלובס' )", "array( 'דירות', '453', 'בממוצע כ-150 מ״ר לדירה' )"),
    ("'כ-50 מעלות לאורך מגדל של 40 קומות, לפי ויקיפדיה'", "'כ-50 מעלות לאורך מגדל של 40 קומות'"),
    ("'עם אגם אקולוגי, בית ספר ומרכז קהילתי, לפי גלובס ומאקו'", "'עם אגם אקולוגי, בית ספר ומרכז קהילתי'"),
    ("'ב-23.4.2026, לפי רישום אתר הבנייה בעירייה'", "'ב-23.4.2026'"),
    ("array( 'אכלוס', 'לפי המקורות, 2026 עד 2028', 'next' )", "array( 'אכלוס', '2026 עד 2028', 'next' )"),
    ("""				'deals_intro'    => 'שלוש העסקאות במגדלים שפורסמו עם הקומה שלהן, כולן דירות 4 חדרים של 140 מ״ר, לפי גלובס (2.5.2025). באיזה מגדל נמכרה כל דירה לא פורסם, ולא כל העסקאות פורסמו.',""",
     """				'deals_intro'    => 'מידע גלוי: שלוש העסקאות במגדלים שפורסמו עם הקומה שלהן, כולן דירות 4 חדרים של 140 מ״ר. באיזה מגדל נמכרה כל דירה לא פורסם, ולא כל העסקאות פורסמו.',
				'deals_nosrc'    => true, // 1.72.391: no source column on this page (the sources stay in facts.md)
				// 1.72.391 (V4): the basket's price hint (BasketOne v86: shown, never multiplied into a price), public information
				'basket_hint'    => 'מידע גלוי: דירות 4 חדרים של 140 מ״ר בקומות 38 ו-39 נמכרו ב-9.58 עד 10.63 מיליון ₪, כ-71,000 ₪ למ״ר. המחיר של דירה מסוימת מהנציג.',"""),
    ("'שלוש דירות 4 חדרים בקומות 38 ו-39, 4.2024 עד 12.2024, לפי גלובס'", "'שלוש דירות 4 חדרים בקומות 38 ו-39, 4.2024 עד 12.2024'"),
    ("'ממוצע העסקאות במגדלים, ובקומות הגבוהות ובפנטהאוזים 80,000 עד 150,000 ₪ למ״ר, לפי מאקו (24.9.2026)'", "'ממוצע העסקאות במגדלים, ובקומות הגבוהות ובפנטהאוזים 80,000 עד 150,000 ₪ למ״ר'"),
    ("'רוב העסקאות סביב כיכר המדינה בשנה האחרונה, לפי נתוני רשות המסים (ice, 28.4.2026)'", "'רוב העסקאות סביב כיכר המדינה בשנה האחרונה'"),
    # English
    ("'40, 40 and 37 floors, per Wikipedia and Ashtrom'", "'40, 40 and 37 floors'"),
    ("array( 'Apartments', '453', 'Per Ashtrom and Globes' )", "array( 'Apartments', '453', 'About 150 m² on average' )"),
    ("'About 50° over a 40-floor tower, per Wikipedia'", "'About 50° over a 40-floor tower'"),
    ("'With an ecological pond, a school and a community centre, per Globes and Mako'", "'With an ecological pond, a school and a community centre'"),
    ("'On 23.4.2026, per the municipal building-site record'", "'On 23.4.2026'"),
    ("array( 'Occupancy', 'per the sources, 2026 to 2028', 'next' )", "array( 'Occupancy', '2026 to 2028', 'next' )"),
    # French
    ("'40, 40 et 37 étages, selon Wikipédia et Ashtrom'", "'40, 40 et 37 étages'"),
    ("array( 'Appartements', '453', 'Selon Ashtrom et Globes' )", "array( 'Appartements', '453', 'Environ 150 m² en moyenne' )"),
    ("'Environ 50° sur une tour de 40 étages, selon Wikipédia'", "'Environ 50° sur une tour de 40 étages'"),
    ("'Avec un étang écologique, une école et un centre communautaire, selon Globes et Mako'", "'Avec un étang écologique, une école et un centre communautaire'"),
    ("'Le 23 avril 2026, selon le registre des chantiers de la municipalité'", "'Le 23 avril 2026'"),
    ("array( 'Livraison', 'selon les sources, de 2026 à 2028', 'next' )", "array( 'Livraison', 'de 2026 à 2028', 'next' )"),
    # Russian
    ("'40, 40 и 37 этажей, по данным Википедии и Ashtrom'", "'40, 40 и 37 этажей'"),
    ("array( 'Квартиры', '453', 'По данным Ashtrom и Globes' )", "array( 'Квартиры', '453', 'В среднем около 150 м²' )"),
    ("'Около 50° на башню в 40 этажей, по данным Википедии'", "'Около 50° на башню в 40 этажей'"),
    ("'С экологическим прудом, школой и общинным центром, по данным Globes и Mako'", "'С экологическим прудом, школой и общинным центром'"),
    ("'23.04.2026, по реестру стройплощадок муниципалитета'", "'23.04.2026'"),
    ("array( 'Заселение', 'по данным источников, с 2026 по 2028 год', 'next' )", "array( 'Заселение', 'с 2026 по 2028 год', 'next' )"),
    # Arabic
    ("'40 و40 و37 طابقاً، وفق ويكيبيديا وAshtrom'", "'40 و40 و37 طابقاً'"),
    ("array( 'الشقق', '453', 'وفق Ashtrom وGlobes' )", "array( 'الشقق', '453', 'بمتوسط نحو 150 م² للشقة' )"),
    ("'نحو 50 درجة على امتداد برج من 40 طابقاً، وفق ويكيبيديا'", "'نحو 50 درجة على امتداد برج من 40 طابقاً'"),
    ("'مع بركة بيئية ومدرسة ومركز جماهيري، وفق Globes وMako'", "'مع بركة بيئية ومدرسة ومركز جماهيري'"),
    ("'في 23.4.2026، وفق سجل مواقع البناء في البلدية'", "'في 23.4.2026'"),
    ("array( 'السكن', 'وفق المصادر، بين 2026 و2028', 'next' )", "array( 'السكن', 'بين 2026 و2028', 'next' )"),
    # the stage's hint line: the page's flow, no sun-hours promise
    ("'בחרו מגדל, קומה וכיוון, וראו בהדמיה את הנוף ואת שעות השמש מהחלון. אפשר גם",
     "'בחרו מגדל, קומה ודירה לפי כיוון, וראו את תוכנית הקומה, את מחירי העסקאות ואת הנוף מהחלונות. אפשר גם"),
    ("'Choose a tower, a floor and a facing to see an illustration of the view and the hours of sun from the window. Or take",
     "'Choose a tower, a floor and an apartment by its direction to see the floor plan, the deal prices and the view from its windows. Or take"),
    ("'Choisissez une tour, un étage et une orientation pour voir en illustration la vue et les heures de soleil depuis la fenêtre. Promenez-vous",
     "'Choisissez une tour, un étage et un appartement selon son orientation pour voir le plan de l’étage, les prix des ventes et la vue depuis ses fenêtres. Promenez-vous"),
    ("'Выберите башню, этаж и сторону света, чтобы увидеть на иллюстрации вид и часы солнца из окна. Можно",
     "'Выберите башню, этаж и квартиру по стороне света, чтобы увидеть план этажа, цены сделок и вид из её окон. Можно"),
    ("'اختاروا برجاً وطابقاً واتجاهاً لتروا في رسم توضيحي الإطلالة وساعات الشمس من النافذة. ويمكنكم",
     "'اختاروا برجاً وطابقاً وشقة حسب اتجاهها لتروا مخطط الطابق وأسعار الصفقات والإطلالة من نوافذها. ويمكنكم"),
]
MARK = "'deals_nosrc'    => true"


def apply(text):
    if MARK in text:
        raise ValueError("already carries the 1.72.391 hunks")
    for old, new in HUNKS:
        n = text.count(old)
        if n != 1:
            raise ValueError(f"anchor x{n}: {old[:80]!r}")
        text = text.replace(old, new)
    return text


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    t = io.open(PS, encoding="utf-8", newline="").read()
    crlf = "\r\n" in t
    t2 = apply(t.replace("\r\n", "\n"))
    if crlf:
        t2 = t2.replace("\n", "\r\n")
    io.open(PS, "w", encoding="utf-8", newline="").write(t2)
    print(f"inc/project-stage.php: {len(HUNKS)} hunks applied (crlf={crlf})")
