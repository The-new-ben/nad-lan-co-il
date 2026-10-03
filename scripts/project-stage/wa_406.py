# -*- coding: utf-8 -*-
"""The PHP hunks of release 1.72.406 (V9, HAD-382, design v104.31): the owner's WhatsApp wording, 1.10.2026. "ייעוץ חינם" only on
the floating bar; every other WhatsApp button inside a page "לקבלת פרטים נוספים בוואטסאפ" (or "דברו איתנו בוואטסאפ"); no "from the
developer / not from the developer" line. Applied to the LIVE text by deploy406.py (each anchor exactly once) and by --apply to the
repo copies."""
import io, os, sys

PS = [  # inc/project-stage.php: the world pages' hero WhatsApp button and its prefilled message, five languages
    ("\t\t\t\t'wa'    => 'ייעוץ חינם',\n\t\t\t\t'wa_tx' => 'שלום, אשמח לייעוץ חינם על %s (nad-lan.co.il)',",
     "\t\t\t\t'wa'    => 'לקבלת פרטים נוספים בוואטסאפ', // v104.31 (HAD-382): \"ייעוץ חינם\" only on the floating bar\n\t\t\t\t'wa_tx' => 'שלום, אשמח לפרטים נוספים על %s (nad-lan.co.il)',"),
    ("\t\t\t\t'wa'    => 'Free advice',\n\t\t\t\t'wa_tx' => 'Hello, I would like free advice on %s (nad-lan.co.il)',",
     "\t\t\t\t'wa'    => 'More details on WhatsApp',\n\t\t\t\t'wa_tx' => 'Hello, I would like more details on %s (nad-lan.co.il)',"),
    ("\t\t\t\t'wa'    => 'Conseil gratuit',\n\t\t\t\t'wa_tx' => 'Bonjour, je souhaite un conseil gratuit sur les %s (nad-lan.co.il)',",
     "\t\t\t\t'wa'    => 'Plus de détails sur WhatsApp',\n\t\t\t\t'wa_tx' => 'Bonjour, je souhaite plus de détails sur les %s (nad-lan.co.il)',"),
    ("\t\t\t\t'wa'    => 'Бесплатная консультация',\n\t\t\t\t'wa_tx' => 'Здравствуйте, хочу бесплатную консультацию по проекту «%s» (nad-lan.co.il)',",
     "\t\t\t\t'wa'    => 'Подробнее в WhatsApp',\n\t\t\t\t'wa_tx' => 'Здравствуйте, хочу узнать подробнее о проекте «%s» (nad-lan.co.il)',"),
    ("\t\t\t\t'wa'    => 'استشارة مجانية',\n\t\t\t\t'wa_tx' => 'مرحباً، أود الحصول على استشارة مجانية حول %s (nad-lan.co.il)',",
     "\t\t\t\t'wa'    => 'مزيد من التفاصيل عبر واتساب',\n\t\t\t\t'wa_tx' => 'مرحباً، أود الحصول على مزيد من التفاصيل حول %s (nad-lan.co.il)',"),
]
CC = [  # inc/conversion-cta.php: the floating bar keeps "ייעוץ חינם"; its small line drops "not the developer" (owner, 1.10.2026)
    ('"לא מטעם היזם · מענה בוואטסאפ"', '"מענה בוואטסאפ"'),
    ('"Not the developer · on WhatsApp"', '"Reply on WhatsApp"'),
    ('"Pas le promoteur · sur WhatsApp"', '"Réponse sur WhatsApp"'),
    ('"Не от застройщика · в WhatsApp"', '"Ответ в WhatsApp"'),
    ('"ليست من المطور · على واتساب"', '"رد على واتساب"'),
]
HUNKS = {"inc/project-stage.php": PS, "inc/conversion-cta.php": CC}


def apply(rel, txt):
    for o, n in HUNKS[rel]:
        if txt.count(o) != 1:
            raise SystemExit(f"{rel}: anchor x{txt.count(o)}: {o[:60]!r}")
        txt = txt.replace(o, n)
    return txt


if __name__ == "__main__" and "--apply" in sys.argv:
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config")
    for rel in HUNKS:
        p = os.path.join(root, *rel.split("/"))
        t = io.open(p, encoding="utf-8", newline="").read()
        crlf = "\r\n" in t
        t = apply(rel, t.replace("\r\n", "\n"))
        io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
        print("applied to the repo copy:", rel)
