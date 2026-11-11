# -*- coding: utf-8 -*-
"""The 1.72.646 hunks on the LIVE inc/project-stage.php (the 643 text, md5 5dad346d5f4efe6595a4897a2a5d9f34). HAD-712, Ben 11.11.2026:
"the film is there twice". Used by make_deploy646.py."""
LIVE_MD5 = "5dad346d5f4efe6595a4897a2a5d9f34"
A_OLD = ("\t\t\t. nadlan_ps_world_film_v2( $k, $t[2] ) // v104.40: the narrated v2 film leads (Ben, 3.10 evening)\n"
         "\t\t\t. '<h3 class=\"nlws-film__v1h\">' . esc_html( array( 'he' => 'הגרסה הראשונה', 'en' => 'The first version', 'fr' => 'La première version', 'ru' => 'Первая версия', 'ar' => 'النسخة الأولى' )[ $lang ] ?? 'הגרסה הראשונה' ) . '</h3>'\n"
         "\t\t\t. '<figure class=\"nlws-film__fig\">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '<figcaption>' . esc_html( $t[2] ) . '</figcaption></figure>'\n")
A_NEW = ("\t\t\t. nadlan_ps_world_film_v2( $k, $t[2] ) // v104.40: the narrated v2 film. 1.72.646 (Ben, 11.11.2026: \"the film is there twice\"): the first version left the page, one film and the facilities clip\n")
B_OLD = "\t\t\t. '.nlws-film figcaption{margin-top:8px;font-size:13px;color:#6B6558}</style>'\n"
B_NEW = ("\t\t\t. '.nlws-film figcaption{margin-top:8px;font-size:13px;color:#6B6558}'\n"
         "\t\t\t// 1.72.646: the page walk of 11.11.2026. A card with a heading and nothing under it is not shown; on a phone the comparison rows say what each number is\n"
         "\t\t\t. '#nlpjx-finance:not(:has(.nlpjx-fin>*)){display:none}'\n"
         "\t\t\t. '@media(max-width:782px){.nlpjx-comps td:nth-child(2)::before{content:\"מחיר מוערך למ״ר: \";color:#5b6770;font-size:12.5px}.nlpjx-comps td:nth-child(2)::after{content:\" ₪\"}.nlpjx-comps td:nth-child(3)::before{content:\"מרחק מהמגדלים: \";color:#5b6770;font-size:12.5px}}</style>'\n")
HUNKS = [(A_OLD, A_NEW), (B_OLD, B_NEW)]


def apply(txt):
    for a, b in HUNKS:
        if txt.count(a) != 1:
            raise SystemExit("k646: FATAL anchor x%d: %r" % (txt.count(a), a[:70]))
        txt = txt.replace(a, b)
    if "nlws-film__v1h\">" in txt or txt.count("#nlpjx-finance:not(:has(.nlpjx-fin>*))") != 1:
        raise SystemExit("k646: FATAL the film block is not as expected after the hunks")
    return txt
