# -*- coding: utf-8 -*-
"""The 1.72.647 hunks on the LIVE inc/project-stage.php (the 646 text, md5 764b4b771dcca97889ffb01b51fb7026). HAD-712, the content round
(Ben 11.11.2026: "do everything needed so this floats in search results and AI engines"). Used by make_deploy647.py.
  A. the project page's FAQPage took the first 12 visible question-and-answer pairs; the Kikar page now has 18, and the occupancy,
     parking, purchase-tax, floor, light-rail and rent questions fell out of the schema. The limit is 20.
  B. the Kikar film block prints a VideoObject for the narrated film (88.6 s measured from the file, uploaded 3.10.2026), in the page's
     language, so the film can appear in video results. Until now the block carried no VideoObject."""
LIVE_MD5 = "764b4b771dcca97889ffb01b51fb7026"
A_OLD = "\t\t\t\t\tforeach ( array_slice( $pairs, 0, 12 ) as $pr ) {\n"
A_NEW = "\t\t\t\t\tforeach ( array_slice( $pairs, 0, 20 ) as $pr ) { // 1.72.647: 20, not 12 (the Kikar page has 18 visible questions)\n"
B_OLD = "\t\treturn '<section class=\"nlws-film\" id=\"nlws-film\" dir=\"' . $t[3] . '\" lang=\"' . esc_attr( $lang ) . '\" aria-labelledby=\"nlws-film-h\">'\n"
B_NEW = ("\t\t// 1.72.647: a VideoObject for the narrated film, so it can appear in video results (88.6 s, measured; on the site since 3.10.2026)\n"
         "\t\t$vf  = 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-' . $k . '-';\n"
         "\t\t$vld = '<script type=\"application/ld+json\" id=\"nadlan-ps-film-v2\">' . wp_json_encode( array(\n"
         "\t\t\t'@context' => 'https://schema.org', '@type' => 'VideoObject', 'name' => $t[0], 'description' => $t[1],\n"
         "\t\t\t'thumbnailUrl' => array( $vf . '16x9-poster.jpg', $vf . '9x16-poster.jpg' ), 'uploadDate' => '2026-10-03T21:44:00+03:00',\n"
         "\t\t\t'duration' => 'PT89S', 'contentUrl' => $vf . '16x9-1.mp4', 'inLanguage' => $k,\n"
         "\t\t\t'publisher' => array( '@type' => 'Organization', 'name' => 'נדל״ן', 'url' => home_url( '/' ) ),\n"
         "\t\t), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';\n"
         "\t\treturn $vld . '<section class=\"nlws-film\" id=\"nlws-film\" dir=\"' . $t[3] . '\" lang=\"' . esc_attr( $lang ) . '\" aria-labelledby=\"nlws-film-h\">'\n")
HUNKS = [(A_OLD, A_NEW), (B_OLD, B_NEW)]


def apply(txt):
    for a, b in HUNKS:
        if txt.count(a) != 1:
            raise SystemExit("k647: FATAL anchor x%d: %r" % (txt.count(a), a[:70]))
        txt = txt.replace(a, b)
    if txt.count('nadlan-ps-film-v2') != 1 or "array_slice( $pairs, 0, 12 )" in txt:
        raise SystemExit("k647: FATAL the file is not as expected after the hunks")
    return txt
