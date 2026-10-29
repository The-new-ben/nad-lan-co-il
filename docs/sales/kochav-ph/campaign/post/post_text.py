# -*- coding: utf-8 -*-
"""The words of the organic post (29.10.2026), per language: post.txt (the post), comment.txt (the first comment, with the link:
links in the post body cut organic reach), short.txt (groups and X, one paragraph with the link). Facts from the live listing only.
  python post_text.py   -> out/<lang>/post.txt, comment.txt, short.txt"""
import io, os
from post_copy import LINK, UTM, LICENCE
H = os.path.dirname(os.path.abspath(__file__))
NB = " "
POST = {
 "he": """מיני פנטהאוז חדש בכוכב הצפון, תל אביב: 76 מ״ר של מרפסות בקומה 11 מתוך 12, ליד פארק הירקון.

בוקר עם קפה מול קו הרקיע של תל אביב, וערב עם חברים על המרפסת. 5 חדרים בבניין בוטיק חדש עם חדר כושר וחדר דיירים.

· כ-197 מ״ר בנוי, קומה 11 מתוך 12
· מרפסות של כ-76 מ״ר שנפתחות אל הים, הפארק וקו הרקיע של תל אביב
· מטבח עם אי ארוך, סוויטת הורים ואגף ילדים עם מרפסת לים
· 2 חניות, מחסן, ממ״ד ומעלית
· מגרשי טניס וכדורגל ליד הבית, והגשר החדש לפארק הירקון צפוי להיפתח ב-2027

מחיר: 18,000,000 ₪

כל הצילומים והסרטון צולמו בדירה עצמה. תמונת התוכנית היא הדמיה על פי תוכנית האדריכל.
לתיאום צפייה פרטית בוואטסאפ או בטלפון: 052-3631582
מיטל קציר, מתווכת מורשית (רישיון {lic}), נדל״ן על הים · בלעדיות

הסרטון המלא, תוכנית הדירה וכל הפרטים בתגובה הראשונה.

#כוכב_הצפון #פנטהאוז_למכירה #תל_אביב #פארק_הירקון""",
 "en": """A brand-new mini-penthouse in Kochav HaTzafon, Tel Aviv: 76 sqm of terraces on the 11th of 12 floors, next to Yarkon Park.

Morning coffee facing the Tel Aviv skyline, evenings with friends on the terrace. For sale in a new boutique building with a gym and a residents’ common room.

· 5 rooms (including the living room, per Israeli convention), about 197 sqm of built area
· About 76 sqm of terraces facing the sea, the park and the Tel Aviv skyline
· A long kitchen island, a principal suite, and a children’s wing with its own sea-view balcony
· 2 parking spaces, storage, a safe room and a lift
· Tennis courts and football pitches nearby; a new bridge into Yarkon Park is expected in 2027

Price: NIS 18,000,000 (about $5.9M / €5.1M)

All photos were taken, and the video filmed, in the apartment itself; the floor-plan image is a rendering of the architect’s plan.
Private viewings by WhatsApp or phone: +972 52-363-1582
Meital Katzir, licensed real-estate broker (Israeli licence no. {lic}), Nadlan Al HaYam · exclusive listing
מיטל קציר, מתווכת במקרקעין, רישיון {lic}

The full film, the floor plan and every detail are in the first comment.

#TelAviv #Penthouse #TelAvivRealEstate #LuxuryRealEstate""",
 "fr": """Mini-penthouse neuf à Kochav HaTzafon, Tel Aviv{nb}: 76{nb}m² de terrasses au 11e étage sur 12, à deux pas du parc HaYarkon.

Le café du matin face à la ligne d’horizon de Tel Aviv, les soirées entre amis sur la terrasse. À vendre dans le nord de Tel Aviv, dans un immeuble neuf à taille humaine avec salle de sport et salle commune.

· 5 pièces, environ 197{nb}m² habitables
· Environ 76{nb}m² de terrasses ouvertes sur la mer, le parc et la ligne d’horizon de Tel Aviv
· Une cuisine avec un long îlot, une suite parentale et une aile réservée aux enfants avec balcon vue mer
· 2 places de parking, une cave, une pièce sécurisée (mamad) et un ascenseur
· Courts de tennis et terrains de football tout près{nb}; une nouvelle passerelle vers le parc HaYarkon est attendue en 2027

Prix{nb}: 18{nb}000{nb}000{nb}₪ (environ 5,1{nb}M€ / 5,9{nb}M$)

Toutes les photos ont été prises dans l’appartement, et la vidéo y a été tournée{nb}; l’image du plan est une illustration d’après le plan de l’architecte.
Visites privées sur WhatsApp ou par téléphone{nb}: +972 52-363-1582
Meital Katzir, agent immobilier agréé en Israël (licence n°{nb}{lic}), Nadlan Al HaYam · exclusivité
מיטל קציר, מתווכת במקרקעין, רישיון {lic}

Le film complet, le plan et tous les détails sont dans le premier commentaire.

#TelAviv #Penthouse #ImmobilierIsrael #TelAvivImmobilier""",
 "ru": """Новый мини-пентхаус в Кохав ха-Цафон, Тель-Авив: 76{nb}м² террас на 11-м этаже из 12, в двух шагах от парка Яркон.

Утренний кофе с видом на силуэт Тель-Авива, вечера с друзьями на террасе. Продаётся в новом бутиковом доме на севере Тель-Авива, с тренажёрным залом и общей комнатой для жильцов.

· 5 комнат, около 197{nb}м²
· Около 76{nb}м² террас с видом на море, парк и силуэт Тель-Авива
· Кухня с длинным островом, родительский блок и детское крыло с балконом с видом на море
· 2 парковочных места, кладовая, защищённая комната (мамад) и лифт
· Рядом теннисные корты и футбольные поля; новый мост в парк Яркон должен открыться в 2027 году

Цена: 18{nb}000{nb}000{nb}₪ (около 5,9{nb}млн $ / 5,1{nb}млн €)

Все фото и видео сняты в самой квартире; изображение планировки является визуализацией по плану архитектора.
Индивидуальный просмотр, WhatsApp или телефон: +972 52-363-1582
Мейталь Кацир (Meital Katzir), лицензированный брокер (израильская лицензия №{nb}{lic}), Nadlan Al HaYam · эксклюзив
מיטל קציר, מתווכת במקרקעין, רישיון {lic}

Полный фильм, планировка и все подробности в первом комментарии.

#ТельАвив #Пентхаус #НедвижимостьИзраиля #НедвижимостьТельАвива"""}
COMMENT = {"he": "כל הפרטים, הסרטון המלא ותוכנית הדירה:\n{url}",
           "en": "All the details, the full film and the floor plan:\n{url}",
           "fr": "Tous les détails, le film complet et le plan{nb}:\n{url}",
           "ru": "Все подробности, полный фильм и планировка:\n{url}"}
SHORT = {"he": "מיני פנטהאוז חדש למכירה בכוכב הצפון, תל אביב: 5 חדרים, 76 מ״ר מרפסות, קומה 11 מתוך 12, ליד פארק הירקון. 18,000,000 ₪. צפייה פרטית: מיטל קציר, 052-3631582 (רישיון תיווך {lic}). {url}",
         "en": "Brand-new mini-penthouse for sale in Kochav HaTzafon, Tel Aviv: 5 rooms, 76 sqm of terraces, 11th floor of 12, next to Yarkon Park. NIS 18M. Private viewing: Meital Katzir, +972 52-363-1582 (broker licence {lic}). {url}",
         "fr": "Mini-penthouse neuf à vendre à Kochav HaTzafon, Tel Aviv{nb}: 5 pièces, 76{nb}m² de terrasses, 11e étage sur 12, près du parc HaYarkon. 18{nb}M{nb}₪. Visite privée{nb}: Meital Katzir, +972 52-363-1582 (licence n°{nb}{lic}). {url}",
         "ru": "Новый мини-пентхаус на продажу в Кохав ха-Цафон, Тель-Авив: 5 комнат, 76{nb}м² террас, 11-й этаж 12-этажного дома, рядом парк Яркон. 18{nb}млн{nb}₪. Индивидуальный просмотр: Meital Katzir, +972 52-363-1582 (лицензия №{nb}{lic}). {url}"}
GROUP = {"he": "למכירה בכוכב הצפון, צפון תל אביב: מיני פנטהאוז חדש בקומה 11 מתוך 12, 5 חדרים, כ-197 מ״ר ו-76 מ״ר מרפסות שנפתחות אל הים, הפארק וקו הרקיע. בניין בוטיק חדש עם חדר כושר וחדר דיירים, ליד פארק הירקון. 18,000,000 ₪. כל הצילומים מהדירה עצמה. מיטל קציר, מתווכת מורשית, רישיון {lic} · וואטסאפ 052-3631582",
         "en": "For sale in Kochav HaTzafon, north Tel Aviv: a brand-new mini-penthouse on floor 11 of 12, 5 rooms, about 197 sqm and 76 sqm of terraces facing the sea, the park and the skyline. New boutique building with a gym and a common room, next to Yarkon Park. NIS 18,000,000. All photos were taken in the apartment. Meital Katzir, licensed broker, Israeli licence no. {lic} · WhatsApp +972 52-363-1582",
         "fr": "À vendre à Kochav HaTzafon, nord de Tel Aviv{nb}: mini-penthouse neuf au 11e étage sur 12, 5 pièces, environ 197{nb}m² et 76{nb}m² de terrasses face à la mer, au parc et à la ville. Immeuble neuf à taille humaine avec salle de sport et salle commune, près du parc HaYarkon. 18{nb}000{nb}000{nb}₪. Toutes les photos ont été prises dans l’appartement. Meital Katzir, agent immobilier agréé, licence n°{nb}{lic} · WhatsApp +972 52-363-1582",
         "ru": "Продаётся в Кохав ха-Цафон, север Тель-Авива: новый мини-пентхаус на 11-м этаже 12-этажного дома, 5 комнат, около 197{nb}м² и 76{nb}м² террас с видом на море, парк и город. Новый бутиковый дом с тренажёрным залом и общей комнатой, рядом парк Яркон. 18{nb}000{nb}000{nb}₪. Все фото сделаны в квартире. Мейталь Кацир, лицензированный брокер, лицензия №{nb}{lic} · WhatsApp +972 52-363-1582"}
GROUP_B = {"he": "חיפשתם דירה עם מרפסת אמיתית בצפון תל אביב? בכוכב הצפון, ליד פארק הירקון: מיני פנטהאוז חדש בקומה 11 מתוך 12, עם כ-76 מ״ר מרפסות לים, לפארק ולקו הרקיע. 5 חדרים, כ-197 מ״ר, מטבח עם אי ארוך, 2 חניות ומחסן, בבניין בוטיק חדש עם חדר כושר וחדר דיירים. 18,000,000 ₪. מיטל קציר, מתווכת מורשית, רישיון {lic} · וואטסאפ 052-3631582",
           "en": "Looking for a Tel Aviv home with real outdoor space? In Kochav HaTzafon, next to Yarkon Park: a brand-new mini-penthouse on floor 11 of 12 with about 76 sqm of terraces facing the sea, the park and the skyline. 5 rooms, about 197 sqm, a long kitchen island, 2 parking spaces and storage, in a new boutique building with a gym and a common room. NIS 18,000,000. Meital Katzir, licensed broker, Israeli licence no. {lic} · WhatsApp +972 52-363-1582",
           "fr": "Vous cherchez à Tel Aviv un appartement avec un vrai extérieur{nb}? À Kochav HaTzafon, près du parc HaYarkon{nb}: un mini-penthouse neuf au 11e étage sur 12, avec environ 76{nb}m² de terrasses face à la mer, au parc et à la ville. 5 pièces, environ 197{nb}m², un long îlot de cuisine, 2 places de parking et une cave, dans un immeuble neuf à taille humaine avec salle de sport et salle commune. 18{nb}000{nb}000{nb}₪. Meital Katzir, agent immobilier agréé, licence n°{nb}{lic} · WhatsApp +972 52-363-1582",
           "ru": "Ищете квартиру в Тель-Авиве с настоящими террасами? В Кохав ха-Цафон, рядом с парком Яркон: новый мини-пентхаус на 11-м этаже из 12, около 76{nb}м² террас с видом на море, парк и город. 5 комнат, около 197{nb}м², кухня с длинным островом, 2 парковочных места и кладовая, в новом бутиковом доме с тренажёрным залом и общей комнатой. 18{nb}000{nb}000{nb}₪. Мейталь Кацир, лицензированный брокер, лицензия №{nb}{lic} · WhatsApp +972 52-363-1582"}
for k in GROUP:  # two wordings for groups, posted by hand, one per group, never both in the same group
    GROUP[k] = GROUP[k] + "\n\n• • •\n\n" + GROUP_B[k]
for lang in POST:
    url = LINK[lang] + UTM % lang
    url_x = url.replace("utm_source=facebook", "utm_source=x")
    O = os.path.join(H, "out", lang); os.makedirs(O, exist_ok=True)
    for name, d in (("post", POST), ("comment", COMMENT), ("short", SHORT), ("group", GROUP)):
        t = d[lang].format(lic=LICENCE, nb=NB, url=url_x if name == "short" else url)
        io.open(os.path.join(O, name + ".txt"), "w", encoding="utf-8").write(t + "\n")
    p = POST[lang].format(lic=LICENCE, nb=NB)
    print(lang, "post", len(p), "chars | first two lines:", len(p.split("\n\n")[0]), "| short", len(SHORT[lang].format(lic=LICENCE, nb=NB, url="https://t.co/xxxxxxxxxx")), "(X counts a link as 23)")
