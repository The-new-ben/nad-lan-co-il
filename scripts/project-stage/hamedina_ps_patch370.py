# -*- coding: utf-8 -*-
"""Kikar Hamedina P8 (1.72.370, HAD-375): the French, Russian and Arabic page tops, as anchored hunks on inc/project-stage.php.

The LIVE file is what 1.72.369 wrote: 65af09be + hamedina_ps_patch.py's hunks (md5 e6c9fc1c..., deploy-result-369.json). The
release copy of 1.72.370 is that text + these hunks; the branch file (which also carries the unreleased Batch 1/2) gets the same
hunks, so the two never drift. Every anchor sits inside 369's own Kikar Hamedina text, so the four stage projects (Rainbow, DUO,
Dimri, Ashira) are not touched: ps_identity_proof370 in gen_deploy370.py renders them byte for byte, before and after.

  1. words   : nadlan_ps_world_words() gains fr, ru and ar (the buttons, the WhatsApp message, the stage's title and hint)
  2. lang    : the world page passes its own language (fr, ru, ar) to the page top and to the world module, not 'en'
  3. config  : the 'hamedina' entry's i18n gains fr, ru and ar (name, builders, place, the picture's alt and sources, the six
               quick facts and the five project stages), every fact as in facts.md, the same as the Hebrew and English

  python scripts/project-stage/hamedina_ps_patch370.py --branch     apply the hunks to the working file (once)
  python scripts/project-stage/hamedina_ps_patch370.py --check      show which hunks the working file and the release carry
"""
import hashlib, io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hamedina_ps_patch as KP  # noqa: E402  the 369 hunks (the live base of this release)

REPO = KP.REPO
REL = KP.REL
LIVE_369_MD5 = "e6c9fc1c7f4df378588c974ef3305892"  # deploy-result-369.json: what 1.72.369 wrote

# ------------------------------------------------------------------------------------------------ 1. the page top's words
WORDS_DOC_OLD = """	/** The page top's own words in the page's language; the world speaks Hebrew and English (fr, ru, ar come at P8). */"""
WORDS_DOC_NEW = """	/** The page top's own words in the page's language: Hebrew, English, French, Russian and Arabic (P8, 1.72.370). */"""
WORDS_OLD = """				'rail'  => 'Professionals in the area',
			),
		);
		return isset( $w[ $lang ] ) ? $w[ $lang ] : $w['en'];"""
WORDS_NEW = """				'rail'  => 'Professionals in the area',
			),
			// P8 (1.72.370): written for each reader, not word for word from the English
			'fr' => array(
				'wa'    => 'Conseil gratuit',
				'wa_tx' => 'Bonjour, je souhaite un conseil gratuit sur les %s (nad-lan.co.il)',
				'sale'  => 'Appartements à vendre dans les tours',
				'tour'  => 'Visite virtuelle de la place',
				'stage' => 'Visite virtuelle des %s : les tours, les étages et la vue',
				'hint'  => 'Choisissez une tour, un étage et une orientation pour voir en illustration la vue et les heures de soleil depuis la fenêtre. Promenez-vous aussi sur la place et dans le parc, et découvrez tout ce qui se trouve à quelques pas.',
				'facts' => 'En bref',
				'prog'  => 'Avancement du projet',
				'rail'  => 'Professionnels du quartier',
			),
			'ru' => array(
				'wa'    => 'Бесплатная консультация',
				'wa_tx' => 'Здравствуйте, хочу бесплатную консультацию по проекту «%s» (nad-lan.co.il)',
				'sale'  => 'Квартиры на продажу в башнях',
				'tour'  => 'Виртуальная прогулка по площади',
				'stage' => 'Виртуальная прогулка: %s, этажи и вид из окон',
				'hint'  => 'Выберите башню, этаж и сторону света, чтобы увидеть на иллюстрации вид и часы солнца из окна. Можно также прогуляться по площади и парку и узнать, что находится в шаговой доступности.',
				'facts' => 'Коротко о проекте',
				'prog'  => 'Этап проекта',
				'rail'  => 'Специалисты района',
			),
			'ar' => array(
				'wa'    => 'استشارة مجانية',
				'wa_tx' => 'مرحباً، أود الحصول على استشارة مجانية حول %s (nad-lan.co.il)',
				'sale'  => 'شقق للبيع في الأبراج',
				'tour'  => 'جولة افتراضية في الميدان',
				'stage' => 'جولة افتراضية في %s: الأبراج والطوابق والإطلالة',
				'hint'  => 'اختاروا برجاً وطابقاً واتجاهاً لتروا في رسم توضيحي الإطلالة وساعات الشمس من النافذة. ويمكنكم أيضاً التجول سيراً في الميدان والحديقة واكتشاف كل ما يقع على مسافة قريبة.',
				'facts' => 'باختصار',
				'prog'  => 'مرحلة المشروع',
				'rail'  => 'مختصون في المنطقة',
			),
		);
		return isset( $w[ $lang ] ) ? $w[ $lang ] : $w['en'];"""

# ------------------------------------------------------------------------------------------------ 2. the page's own language
LANG_OLD = """		$tl   = $he ? 'he' : 'en';"""
LANG_NEW = """		$tl   = in_array( $lang, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $lang : 'en'; // P8 (1.72.370): fr, ru and ar speak their own language"""

# ------------------------------------------------------------------------------------------------ 3. the config's fr, ru, ar
CONFIG_OLD = """							array( 'Occupancy', 'per the sources, 2026 to 2028', 'next' ),
						),
					),
				),
			),
		);
	}
}
"""
CONFIG_NEW = """							array( 'Occupancy', 'per the sources, 2026 to 2028', 'next' ),
						),
					),
					// P8 (1.72.370): the French, Russian and Arabic pages (/projects/hamedina-fr/, -ru, -ar). The same facts as the
					// Hebrew and English, from facts.md; the names as their sources write them in that language
					'fr' => array(
						'name'       => 'Tours Kikar Hamedina',
						'developer'  => 'Construites par Electra et Ashtrom',
						'place'      => 'Kikar Hamedina, nord de Tel Aviv',
						'poster_alt' => 'Illustration des tours Kikar Hamedina à Tel Aviv : trois tours torsadées autour du parc et de l’étang, au cœur de l’anneau d’immeubles de la place, avec la ville jusqu’à la mer',
						'src_line'   => 'Sources de l’illustration : immeubles, hauteurs, rues, jardins et arbres d’après la municipalité de <span>Tel Aviv-Jaffa</span> (données géographiques ouvertes, 09/2026) ; les tours d’après leur contour dans les données municipales et la rotation publiée de 1,25° par étage. L’emplacement de l’étang et des équipements du parc est indicatif.',
						'facts'      => array(
							array( 'Adresse', 'Kikar Hamedina, Tel Aviv', 'Sur la rue circulaire He Be’Iyar, nord de Tel Aviv' ),
							array( 'Tours', '3 tours torsadées', '40, 40 et 37 étages, selon Wikipédia et Ashtrom' ),
							array( 'Appartements', '453', 'Selon Ashtrom et Globes' ),
							array( 'La torsion', '1,25° par étage', 'Environ 50° sur une tour de 40 étages, selon Wikipédia' ),
							array( 'Le parc', 'Environ 4 hectares', 'Avec un étang écologique, une école et un centre communautaire, selon Globes et Mako' ),
							array( 'Avancement', 'Gros œuvre achevé', 'Le 23 avril 2026, selon le registre des chantiers de la municipalité' ),
						),
						'progress'   => array(
							array( 'Plan', '06/2013', 'done' ),
							array( 'Permis de construire', '12/2022', 'done' ),
							array( 'Gros œuvre achevé', '04/2026', 'done' ),
							array( 'En construction', 'aujourd’hui', 'now' ),
							array( 'Livraison', 'selon les sources, de 2026 à 2028', 'next' ),
						),
					),
					'ru' => array(
						'name'       => 'Башни Кикар ха-Медина',
						'developer'  => 'Строят Electra и Ashtrom',
						'place'      => 'Кикар ха-Медина, север Тель-Авива',
						'poster_alt' => 'Иллюстрация башен Кикар ха-Медина в Тель-Авиве: три закрученные башни вокруг парка и пруда, в кольце зданий площади, и город до самого моря',
						'src_line'   => 'Источники иллюстрации: здания, высоты, улицы, скверы и деревья по данным муниципалитета <span>Тель-Авива-Яффо</span> (открытые геоданные, 09.2026); башни по контуру из данных муниципалитета и опубликованному повороту 1,25° на каждом этаже. Места пруда и объектов парка показаны условно.',
						'facts'      => array(
							array( 'Адрес', 'Кикар ха-Медина, Тель-Авив', 'На кольцевой улице площади, север города' ),
							array( 'Башни', '3 закрученные башни', '40, 40 и 37 этажей, по данным Википедии и Ashtrom' ),
							array( 'Квартиры', '453', 'По данным Ashtrom и Globes' ),
							array( 'Поворот', '1,25° на этаж', 'Около 50° на башню в 40 этажей, по данным Википедии' ),
							array( 'Парк', 'Около 40 дунамов', 'С экологическим прудом, школой и общинным центром, по данным Globes и Mako' ),
							array( 'Статус', 'Каркас завершён', '23.04.2026, по реестру стройплощадок муниципалитета' ),
						),
						'progress'   => array(
							array( 'План', '06.2013', 'done' ),
							array( 'Разрешение на строительство', '12.2022', 'done' ),
							array( 'Каркас завершён', '04.2026', 'done' ),
							array( 'Строительство', 'сейчас', 'now' ),
							array( 'Заселение', 'по данным источников, с 2026 по 2028 год', 'next' ),
						),
					),
					'ar' => array(
						'name'       => 'أبراج كيكار همدينا',
						'developer'  => 'البناء: Electra وAshtrom',
						'place'      => 'كيكار همدينا، شمال تل أبيب',
						'poster_alt' => 'رسم توضيحي لأبراج كيكار همدينا في تل أبيب: ثلاثة أبراج ملتفّة حول الحديقة والبركة، داخل حلقة مباني الميدان، والمدينة ممتدة حتى البحر',
						'src_line'   => 'مصادر الرسم التوضيحي: المباني والارتفاعات والشوارع والحدائق والأشجار وفق بلدية <span>تل أبيب يافا</span> (بيانات جغرافية مفتوحة، 9.2026)؛ الأبراج وفق مخطط المبنى لدى البلدية والدوران المنشور بمقدار 1.25 درجة في كل طابق. موقع البركة ومرافق الحديقة توضيحي.',
						'facts'      => array(
							array( 'الموقع', 'كيكار همدينا، تل أبيب', 'على الشارع الدائري حول الميدان، شمال المدينة' ),
							array( 'الأبراج', '3 أبراج ملتفّة', '40 و40 و37 طابقاً، وفق ويكيبيديا وAshtrom' ),
							array( 'الشقق', '453', 'وفق Ashtrom وGlobes' ),
							array( 'الدوران', '1.25 درجة في كل طابق', 'نحو 50 درجة على امتداد برج من 40 طابقاً، وفق ويكيبيديا' ),
							array( 'الحديقة', 'نحو 40 دونماً', 'مع بركة بيئية ومدرسة ومركز جماهيري، وفق Globes وMako' ),
							array( 'الوضع', 'اكتمل الهيكل', 'في 23.4.2026، وفق سجل مواقع البناء في البلدية' ),
						),
						'progress'   => array(
							array( 'المخطط', '6.2013', 'done' ),
							array( 'رخصة البناء', '12.2022', 'done' ),
							array( 'اكتمال الهيكل', '4.2026', 'done' ),
							array( 'قيد البناء', 'الآن', 'now' ),
							array( 'السكن', 'وفق المصادر، بين 2026 و2028', 'next' ),
						),
					),
				),
			),
		);
	}
}
"""

HUNKS = [
    ("words-doc", WORDS_DOC_OLD, WORDS_DOC_NEW),
    ("words", WORDS_OLD, WORDS_NEW),
    ("lang", LANG_OLD, LANG_NEW),
    ("config-i18n", CONFIG_OLD, CONFIG_NEW),
]


def apply(text, label=""):
    for name, old, new in HUNKS:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"FATAL P8 hunk {name}: anchor x{n} in {label}")
        text = text.replace(old, new)
    return text


def carries(text):
    return {name: (new in text) for name, old, new in HUNKS}


def live369():
    """the text 1.72.369 wrote (65af09be + the 369 hunks), checked against its recorded md5"""
    t = KP.apply(KP.base_text(), KP.BASE_COMMIT)
    m = hashlib.md5(t.encode("utf-8")).hexdigest()
    if m != LIVE_369_MD5:
        raise SystemExit(f"FATAL: 65af09be + the 369 hunks is {m}, not what 1.72.369 wrote ({LIVE_369_MD5})")
    return t


def release_text():
    return apply(live369(), "the 369 release copy")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    path = os.path.join(REPO, *REL.split("/"))
    cur = io.open(path, encoding="utf-8", newline="").read()
    if "--branch" in sys.argv:
        if all(carries(cur).values()):
            print("the working file already carries every P8 hunk")
        else:
            io.open(path, "w", encoding="utf-8", newline="").write(apply(cur, "the working file"))
            print("applied", [h[0] for h in HUNKS], "to", REL)
    else:
        print("working file:", carries(cur))
        r = release_text()
        print("release copy (369 + P8):", hashlib.md5(r.encode("utf-8")).hexdigest(), carries(r))
