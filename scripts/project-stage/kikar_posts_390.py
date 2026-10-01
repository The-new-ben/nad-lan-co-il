# -*- coding: utf-8 -*-
"""V3 (1.10.2026, the V2 loop turn 3; HAD-380): the Kikar posts' prices as "מידע גלוי", with no source names on the page (the owner,
1.10: "מספיק עם הקרדיטים ומספיק עם המקורות"). The sources stay in docs/research/2026-09-30-kikar-hamedina/facts.md.
  1. the lead (all five): no "(Globes, 2.5.2025)" and no "per the municipal building-site record"; its last sentence is the page's
     new flow (a tower, a floor, an apartment by its direction, the view from its windows), the sun hours no longer promised;
  2. the price section (all five): the deals' range and average as public information, the tables with a date column instead of
     "source and date", no source name, one note;
  3. the sale section (all five): its two inline source names removed (the facts unchanged).
Edits docs/research/2026-09-30-kikar-hamedina/post-{he,en,fr,ru,ar}.html in place (the files the runner writes as the posts).
  python kikar_posts_390.py"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "research", "2026-09-30-kikar-hamedina")

LEAD = {
    "he": [("השלד הושלם ב-23.4.2026, לפי רישום אתר הבנייה בעירייה.", "השלד הושלם ב-23.4.2026."),
           ("ב-9.58 עד 10.63 מיליון ₪ (גלובס, 2.5.2025).", "ב-9.58 עד 10.63 מיליון ₪."),
           ("כאן בוחרים מגדל, קומה וכיוון, ורואים בהדמיה את הנוף ואת שעות השמש מהחלון.", "כאן בוחרים מגדל, קומה ודירה לפי כיוון, ורואים בהדמיה את הנוף מהחלונות שלה.")],
    "en": [("The frame was completed on 23.4.2026, per the municipal building-site record.", "The frame was completed on 23.4.2026."),
           ("sold for ₪9.58M to ₪10.63M (Globes, 2.5.2025).", "sold for ₪9.58M to ₪10.63M."),
           ("Here you choose a tower, a floor and a facing, and see an illustration of the view and the hours of sun from the window.",
            "Here you choose a tower, a floor and an apartment by its direction, and see an illustration of the view from its windows.")],
    "fr": [("Le gros œuvre a été achevé le 23 avril 2026, selon le registre des chantiers de la municipalité.", "Le gros œuvre a été achevé le 23 avril 2026."),
           ("entre 9,58 et 10,63 millions de shekels (Globes, 2 mai 2025).", "entre 9,58 et 10,63 millions de shekels."),
           ("Ici, vous choisissez une tour, un étage et une orientation, et découvrez en illustration la vue et les heures de soleil depuis la fenêtre.",
            "Ici, vous choisissez une tour, un étage et un appartement selon son orientation, et découvrez en illustration la vue depuis ses fenêtres.")],
    "ru": [("Каркас завершён 23.04.2026, по реестру стройплощадок муниципалитета.", "Каркас завершён 23.04.2026."),
           ("от 9,58 до 10,63 млн ₪ (Globes, 02.05.2025).", "от 9,58 до 10,63 млн ₪."),
           ("Здесь можно выбрать башню, этаж и сторону света и увидеть на иллюстрации вид и часы солнца из окна.",
            "Здесь можно выбрать башню, этаж и квартиру по стороне света и увидеть на иллюстрации вид из её окон.")],
    "ar": [("اكتمل الهيكل في 23.4.2026، وفق سجل مواقع البناء في بلدية تل أبيب يافا.", "اكتمل الهيكل في 23.4.2026."),
           ("بين 9.58 و10.63 مليون شيكل (Globes، 2.5.2025).", "بين 9.58 و10.63 مليون شيكل."),
           ("هنا تختارون برجاً وطابقاً واتجاهاً، وترون في رسم توضيحي الإطلالة وساعات الشمس من النافذة.",
            "هنا تختارون برجاً وطابقاً وشقة حسب اتجاهها، وترون في رسم توضيحي الإطلالة من نوافذها.")],
}
SALE = {
    "he": [(" בדרך כלל דרך משרדי תיווך (גלובס, 23.9.2025).", " בדרך כלל דרך משרדי תיווך."),
           ("ולפי ביזפורטל (19.4.2025) לכל היותר", "ולכל היותר")],
    "en": [("usually through brokers (Globes, 23.9.2025).", "usually through brokers."), ("and per Bizportal (19.4.2025) at most", "and at most")],
    "fr": [("par l’intermédiaire d’agences immobilières (Globes, 23/09/2025).", "par l’intermédiaire d’agences immobilières."),
           ("et, selon Bizportal (19/04/2025), 200 à 250", "et 200 à 250")],
    "ru": [("через агентства недвижимости (Globes, 23.09.2025).", "через агентства недвижимости."), (", и, по данным Bizportal (19.04.2025), на рынок", ", и на рынок")],
    "ar": [("عن طريق مكاتب الوساطة العقارية (Globes، 23.9.2025).", "عن طريق مكاتب الوساطة العقارية."), ("، ووفق Bizportal (19.4.2025) من المتوقع", "، ومن المتوقع")],
}
# the deals (facts.md 1.12): 140 m2, 4 rooms, floors 38/39: 10.63M (12.2024, 75,913/m2), 9.59M (5.2024, 68,520), 9.58M (4.2024, 68,405)
# average 9.93M, 70,946/m2; the towers' average ~65,000/m2, upper floors and penthouses 80,000-150,000/m2 (Mako 24.9.2026)
W = {
    "he": dict(k="מחירים ועסקאות · מידע גלוי", h2="מחירי הדירות במגדלי כיכר המדינה",
               p="שלוש דירות 4 חדרים של 140 מ״ר בקומות 38 ו-39 נמכרו ב-9.58 עד 10.63 מיליון ₪: בממוצע כ-9.93 מיליון ₪, כ-71,000 ₪ למ״ר (68,400 עד 75,900 ₪ למ״ר). ממוצע העסקאות במגדלים עומד על כ-65,000 ₪ למ״ר, ובקומות הגבוהות ובפנטהאוזים על 80,000 עד 150,000 ₪ למ״ר. אלה העסקאות שפורסמו עם הקומה שלהן; לא כל העסקאות פורסמו.",
               th=("קומה", "הדירה", "המחיר", "למ״ר", "מתי"), apt="4 חדרים · 140 מ״ר", m=lambda x: f"{x} מיליון ₪", ppm=lambda x: f"כ-{x} ₪",
               d=("12.2024", "5.2024", "4.2024"), h3a="מחירים מבוקשים שפורסמו", tha=("הדירה", "המחיר המבוקש", "מתי"),
               ask=[("פנטהאוז בקומה 39, 258 מ״ר ו-57 מ״ר מרפסות ומרפסת גג", "43 מיליון ₪", "4.2025"),
                    ("דירה בקומה 35, 154 מ״ר ומרפסת 12 מ״ר, לדרום-מזרח", "14.5 מיליון ₪", "9.2026"),
                    ("4 חדרים, 168 מ״ר ומרפסת כ-14.5 מ״ר, קומה גבוהה, נוף לים", "13.7 מיליון ₪", "1.2026"),
                    ("קומה 12, 148 מ״ר", "10.3 מיליון ₪", "4.2025"),
                    ("4 חדרים, 132 מ״ר ומרפסת כ-15.5 מ״ר, קומה 16", "10 מיליון ₪", "9.2026")],
               h3b="המחירים בסביבה", thb=("מה נמדד", "המחיר", "מתי"),
               area=[("רוב העסקאות סביב כיכר המדינה בשנה האחרונה", "63,000 עד 66,000 ₪ למ״ר", "4.2026"),
                     ("הממוצע בשכונת הצפון החדש, סביבת כיכר המדינה", "67,747 ₪ למ״ר", "7.2025")],
               note="כל המחירים כאן הם מידע גלוי שפורסם. מחיר מבוקש הוא המחיר שפורסם במודעה, לא מחיר של עסקה, והמחיר של דירה מסוימת נקבע מול המוכר."),
    "en": dict(k="Prices and deals · public information", h2="Apartment prices in Kikar Hamedina Towers",
               p="Three 4-room apartments of 140 m² on floors 38 and 39 sold for ₪9.58M to ₪10.63M: an average of about ₪9.93M, about ₪71,000 per m² (₪68,400 to ₪75,900 per m²). Deals in the towers average about ₪65,000 per m², and ₪80,000 to ₪150,000 per m² on the upper floors and in the penthouses. These are the deals published with their floor; not every deal was published.",
               th=("Floor", "The apartment", "Price", "Per m²", "Date"), apt="4 rooms · 140 m²", m=lambda x: f"₪{x}M", ppm=lambda x: f"about ₪{x}",
               d=("12.2024", "5.2024", "4.2024"), h3a="Asking prices that were published", tha=("The apartment", "Asking price", "Date"),
               ask=[("Penthouse on floor 39, 258 m² with 57 m² of terraces and balcony", "₪43M", "4.2025"),
                    ("Floor 35, 154 m² with a 12 m² balcony, facing south-east", "₪14.5M", "9.2026"),
                    ("4 rooms, 168 m² with a balcony of about 14.5 m², high floor, sea view", "₪13.7M", "1.2026"),
                    ("Floor 12, 148 m²", "₪10.3M", "4.2025"),
                    ("4 rooms, 132 m² with a balcony of about 15.5 m², floor 16", "₪10M", "9.2026")],
               h3b="Prices in the area", thb=("What was measured", "Price", "Date"),
               area=[("Most deals around Kikar Hamedina in the past year", "₪63,000 to ₪66,000 per m²", "4.2026"),
                     ("The average in the New North, Kikar Hamedina area", "₪67,747 per m²", "7.2025")],
               note="All prices here are published public information. An asking price is the price in a listing, not a deal, and the price of a particular apartment is set with its seller."),
    "fr": dict(k="Prix et ventes · information publique", h2="Prix des appartements dans les tours Kikar Hamedina",
               p="Trois appartements de 4 pièces de 140 m² aux 38e et 39e étages se sont vendus entre 9,58 et 10,63 M₪ : en moyenne environ 9,93 M₪, soit environ 71 000 ₪ le m² (de 68 400 à 75 900 ₪ le m²). Les ventes dans les tours se font en moyenne autour de 65 000 ₪ le m², et de 80 000 à 150 000 ₪ le m² dans les étages élevés et les penthouses. Ce sont les ventes publiées avec leur étage ; toutes les ventes ne l’ont pas été. Les prix sont exprimés en shekels (₪).",
               th=("Étage", "L’appartement", "Prix", "Au m²", "Date"), apt="4 pièces · 140 m²", m=lambda x: f"{x.replace('.', ',')} M₪", ppm=lambda x: f"environ {x.replace(',', ' ')} ₪",
               d=("12/2024", "05/2024", "04/2024"), h3a="Prix demandés publiés", tha=("L’appartement", "Prix demandé", "Date"),
               ask=[("Penthouse au 39e étage, 258 m² avec 57 m² de terrasses et de balcon", "43 M₪", "04/2025"),
                    ("35e étage, 154 m² avec un balcon de 12 m², orienté sud-est", "14,5 M₪", "09/2026"),
                    ("4 pièces, 168 m² avec un balcon d’environ 14,5 m², étage élevé, vue mer", "13,7 M₪", "01/2026"),
                    ("12e étage, 148 m²", "10,3 M₪", "04/2025"),
                    ("4 pièces, 132 m² avec un balcon d’environ 15,5 m², 16e étage", "10 M₪", "09/2026")],
               h3b="Les prix du quartier", thb=("Ce qui a été mesuré", "Prix", "Date"),
               area=[("La plupart des ventes autour de Kikar Hamedina sur la dernière année", "de 63 000 à 66 000 ₪ le m²", "04/2026"),
                     ("La moyenne du Nouveau Nord, secteur de Kikar Hamedina", "67 747 ₪ le m²", "07/2025")],
               note="Tous les prix présentés ici sont des informations publiques publiées. Un prix demandé est le prix affiché dans une annonce, pas celui d’une vente conclue ; le prix d’un appartement donné se fixe avec son vendeur."),
    "ru": dict(k="Цены и сделки · открытые данные", h2="Цены на квартиры в башнях Кикар ха-Медина",
               p="Три 4-комнатные квартиры (салон и три спальни) площадью 140 м² на 38-м и 39-м этажах проданы по цене от 9,58 до 10,63 млн ₪: в среднем около 9,93 млн ₪, около 71 000 ₪ за м² (от 68 400 до 75 900 ₪ за м²). Сделки в башнях в среднем проходят примерно по 65 000 ₪ за м², а на верхних этажах и в пентхаусах от 80 000 до 150 000 ₪ за м². Это сделки, опубликованные с указанием этажа; опубликованы не все сделки. Все цены указаны в шекелях (₪).",
               th=("Этаж", "Квартира", "Цена", "За м²", "Дата"), apt="4 комнаты · 140 м²", m=lambda x: f"{x.replace('.', ',')} млн ₪", ppm=lambda x: f"около {x.replace(',', ' ')} ₪",
               d=("12.2024", "05.2024", "04.2024"), h3a="Опубликованные цены предложения", tha=("Квартира", "Цена предложения", "Дата"),
               ask=[("Пентхаус на 39-м этаже, 258 м² и 57 м² террас и балкона", "43 млн ₪", "04.2025"),
                    ("35-й этаж, 154 м² и балкон 12 м², на юго-восток", "14,5 млн ₪", "09.2026"),
                    ("4 комнаты, 168 м² и балкон около 14,5 м², высокий этаж, вид на море", "13,7 млн ₪", "01.2026"),
                    ("12-й этаж, 148 м²", "10,3 млн ₪", "04.2025"),
                    ("4 комнаты, 132 м² и балкон около 15,5 м², 16-й этаж", "10 млн ₪", "09.2026")],
               h3b="Цены в районе", thb=("Что измерено", "Цена", "Дата"),
               area=[("Большинство сделок вокруг Кикар ха-Медина за последний год", "от 63 000 до 66 000 ₪ за м²", "04.2026"),
                     ("Средняя цена в Новом Севере, район Кикар ха-Медина", "67 747 ₪ за м²", "07.2025")],
               note="Все цены здесь: опубликованные открытые данные. Цена предложения означает цену в объявлении, а не цену сделки; цену конкретной квартиры определяют с её продавцом."),
    "ar": dict(k="الأسعار والصفقات · معلومات منشورة", h2="أسعار الشقق في أبراج كيكار همدينا",
               p="بيعت ثلاث شقق من 4 غرف بمساحة 140 م² في الطابقين 38 و39 بأسعار بين 9.58 و10.63 مليون ₪: بمتوسط نحو 9.93 مليون ₪، أي نحو 71,000 ₪ للمتر المربع (من 68,400 إلى 75,900 ₪ للمتر المربع). ويبلغ متوسط الصفقات في الأبراج نحو 65,000 ₪ للمتر المربع، ومن 80,000 إلى 150,000 ₪ للمتر المربع في الطوابق العليا والبنتهاوس. هذه هي الصفقات التي نُشرت مع رقم الطابق، ولم تُنشر كل الصفقات. جميع الأسعار بالشيكل (₪).",
               th=("الطابق", "الشقة", "السعر", "للمتر المربع", "التاريخ"), apt="4 غرف · 140 م²", m=lambda x: f"{x} مليون ₪", ppm=lambda x: f"نحو {x} ₪",
               d=("12.2024", "5.2024", "4.2024"), h3a="أسعار مطلوبة نُشرت", tha=("الشقة", "السعر المطلوب", "التاريخ"),
               ask=[("بنتهاوس في الطابق 39، مساحته 258 م² مع 57 م² من الشرفات وشرفة السطح", "43 مليون ₪", "4.2025"),
                    ("الطابق 35، مساحة 154 م² وشرفة 12 م²، باتجاه الجنوب الشرقي", "14.5 مليون ₪", "9.2026"),
                    ("4 غرف، 168 م² وشرفة نحو 14.5 م²، طابق مرتفع، إطلالة على البحر", "13.7 مليون ₪", "1.2026"),
                    ("الطابق 12، مساحة 148 م²", "10.3 مليون ₪", "4.2025"),
                    ("4 غرف، 132 م² وشرفة نحو 15.5 م²، الطابق 16", "10 ملايين ₪", "9.2026")],
               h3b="الأسعار في المنطقة", thb=("ما الذي قيس", "السعر", "التاريخ"),
               area=[("معظم الصفقات حول كيكار همدينا في السنة الأخيرة", "من 63,000 إلى 66,000 ₪ للمتر المربع", "4.2026"),
                     ("المتوسط في الشمال الجديد، منطقة كيكار همدينا", "67,747 ₪ للمتر المربع", "7.2025")],
               note="جميع الأسعار هنا معلومات منشورة. السعر المطلوب هو السعر المنشور في الإعلان، وليس سعر صفقة، ويُحدَّد سعر كل شقة مع بائعها."),
}
DEALS = [("38", "10.63", "75,900"), ("39", "9.59", "68,500"), ("38", "9.58", "68,400")]


def table(th, rows):
    return ("<table><thead><tr>" + "".join(f"<th>{h}</th>" for h in th) + "</tr></thead><tbody>\n" +
            "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>\n" for r in rows) + "</tbody></table>\n")


def prices(L):
    w = W[L]
    deals = [(f, w["apt"], w["m"](m), w["ppm"](p), d) for (f, m, p), d in zip(DEALS, w["d"])]
    return (f'<p class="nlws-k">{w["k"]}</p>\n<h2>{w["h2"]}</h2>\n<p>{w["p"]}</p>\n' + table(w["th"], deals) +
            f'<h3>{w["h3a"]}</h3>\n' + table(w["tha"], w["ask"]) + f'<h3>{w["h3b"]}</h3>\n' + table(w["thb"], w["area"]) +
            f'<p class="nlws-note">{w["note"]}</p>\n')


for L in ("he", "en", "fr", "ru", "ar"):
    p = os.path.join(RES, f"post-{L}.html")
    s = io.open(p, encoding="utf-8").read()
    if "מידע גלוי" in s or "public information" in s.lower() and L == "en":
        raise SystemExit(f"{L}: already patched")
    for a, b in LEAD[L] + SALE[L]:
        if s.count(a) != 1:
            raise SystemExit(f"{L}: anchor x{s.count(a)}: {a[:60]}")
        s = s.replace(a, b)
    i = s.index('id="nlws-prices"'); i = s.index(">", i) + 1
    j = s.index("</section>", i)
    s = s[:i] + "\n" + prices(L) + s[j:]
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    left = [w for w in ("גלובס", "מאקו", "ביזפורטל", "סותבי", "Globes", "Mako", "Bizportal", "Sotheby", "Israel Property Hub", "Anglo-Saxon", "אנגלו", "ice,", "ynet", "Madlan", "מדלן")
            if w in s[s.index('id="nlws-prices"'):s.index('</section>', s.index('id="nlws-prices"'))]]
    print(L, "patched; source names left in the price section:", left)
