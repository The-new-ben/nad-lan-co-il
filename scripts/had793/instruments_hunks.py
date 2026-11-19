# -*- coding: utf-8 -*-
"""HAD-793 hunks on the LIVE inc/instruments.php (md5 f869d5ca08a33a027553ea7dad9d58da, read 19.11.2026 10:48 UTC):
French and Russian for tools that carry an 'fr' / 'ru' block (first: mquick, the quick mortgage calculator)."""
LIVE_MD5 = "f869d5ca08a33a027553ea7dad9d58da"
H = [
 ("	function nadlan_nli_lang() { return function_exists( 'nadlan_pglang_lang' ) && 'en' === nadlan_pglang_lang() ? 'en' : 'he'; }",
  "	function nadlan_nli_lang() { $l = function_exists( 'nadlan_pglang_lang' ) ? nadlan_pglang_lang() : ''; return in_array( $l, array( 'en', 'fr', 'ru' ), true ) ? $l : 'he'; }  // HAD-793: fr and ru pages too"),
 ("return 'en' === nadlan_nli_lang() && ! empty( $t['en'] ) ? 'en' : 'he'; }",
  "$l = nadlan_nli_lang(); return 'he' !== $l && ! empty( $t[ $l ] ) ? $l : 'he'; }  /* HAD-793: a tool with an 'fr' or 'ru' block speaks it */"),
 ("	function nadlan_nli_t( $t, $lang ) { return 'en' === $lang && ! empty( $t['en'] ) ? array_merge( $t, $t['en'] ) : $t; }",
  "	function nadlan_nli_t( $t, $lang ) { return 'he' !== $lang && ! empty( $t[ $lang ] ) ? array_merge( $t, $t[ $lang ] ) : $t; }"),
 ("		$fonts = ( 'en' === nadlan_nli_lang() || $en_tool )",
  "		$fonts = ( 'he' !== nadlan_nli_lang() || $en_tool )"),
 ("		$h = '<section class=\"nli\" dir=\"' . ( $en ? 'ltr' : 'rtl' ) . '\" lang=\"' . $lang . '\"",
  "		$h = '<section class=\"nli\" dir=\"' . ( 'he' !== $lang ? 'ltr' : 'rtl' ) . '\" lang=\"' . $lang . '\""),
 ("	function nadlan_nli_summary( $id, $lang = 'he' ) {\n		if ( 'en' === $lang ) { return nadlan_nli_summary_en( $id ); }",
  "	function nadlan_nli_summary( $id, $lang = 'he' ) {\n		if ( 'en' === $lang ) { return nadlan_nli_summary_en( $id ); }\n		if ( 'fr' === $lang || 'ru' === $lang ) { return ''; }  // HAD-793: the fr / ru pages carry their own text around the tool"),
 ("(?:שאלות נפוצות|Frequently asked questions)[^<]{0,60}<\/h2>",
  "(?:שאלות נפוצות|Frequently asked questions|Questions fréquentes|Частые вопросы)[^<]{0,60}<\/h2>"),
 ("					'desc' => 'A quick Israeli mortgage calculator: the first monthly payment, the total repaid and the interest by mortgage amount, by home price and equity, or by the monthly payment that suits you, over 15 to 30 years, at the average track mix and rates of all banks or of one bank, from the latest Bank of Israel data.',\n				),",
  "					'desc' => 'A quick Israeli mortgage calculator: the first monthly payment, the total repaid and the interest by mortgage amount, by home price and equity, or by the monthly payment that suits you, over 15 to 30 years, at the average track mix and rates of all banks or of one bank, from the latest Bank of Israel data.',\n				),\n"
  "				'fr' => array(  // HAD-793 (19.11.2026): /fr/mortgage-calculator/\n"
  "					'name' => 'Simulateur de crédit immobilier en Israël', 'kicker' => 'Simulateur · Mashkanta', 'related' => array(),\n"
  "					'desc' => 'Simulateur de crédit immobilier israélien (mashkanta) : la première mensualité, le total remboursé et les intérêts selon le montant du prêt, le prix et l’apport, ou la mensualité qui vous convient, sur 15 à 30 ans, à la répartition et aux taux moyens de toutes les banques ou d’une banque, d’après les dernières données de la Banque d’Israël.',\n"
  "				),\n"
  "				'ru' => array(  // HAD-793 (19.11.2026): /ru/mortgage-calculator/\n"
  "					'name' => 'Ипотечный калькулятор Израиля', 'kicker' => 'Калькулятор · Машканта', 'related' => array(),\n"
  "					'desc' => 'Ипотечный калькулятор Израиля (машканта): первый ежемесячный платёж, сумма выплат и проценты по сумме ипотеки, по цене квартиры и собственным средствам или по комфортному платежу, на срок от 15 до 30 лет, по среднему составу и ставкам всех банков или одного банка, по последним данным Банка Израиля.',\n"
  "				),"),
]
