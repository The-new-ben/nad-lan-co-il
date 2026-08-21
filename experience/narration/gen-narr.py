# -*- coding: utf-8 -*-
# Sde Dov tour narration, he+en — per the measured pronunciation playbook:
# numbers as words (gender-correct), niqqud ONLY on risk words (brands, loan
# words, דב הוז), punctuation as the pacing tool, no SSML in text.
import asyncio, os
import edge_tts

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'narr')
os.makedirs(OUT, exist_ok=True)

HE_VOICE = 'he-IL-AvriNeural'
EN_VOICE = 'en-US-ChristopherNeural'

HE = [
 'כאן, על קו החוף של תל אביב, פעל עד אלפיים תשע עשרה שדה התעופה דּוֹב הוֹז. היום קם כאן הרובע החדש של העיר... כשישה עשר אלף דירות, בין הים לאִבְּן גְּבִירוֹל.',
 'המגדלים הראשונים כבר נבנים. דִּימְרִי יָמָה — שלושים ותשע קומות בקו הראשון לים... ארבע מאות חמישים ושמונה דירות במתחם אֶשְׁכּוֹל הדרומי.',
 'המסלול ההיסטורי של שדה התעופה נשאר... והופך לפארק המסלול. שדרה ירוקה שחוצה את הרובע, עם מבני הציבור של השכונה, ומעבר חופשי אל הים.',
 'רֵיינְבּוֹ תל אביב של ישראל קנדה — מגדל דגל ושישה בנייני חצר... כארבע מאות ושמונים דירות, במגרש הצמוד לפארק ולכיכר השער.',
 'אַשִירָה של אֲבִישְׂרוֹר — ארבעה בניינים בכניסה הדרומית לרובע... כארבע מאות ושש דירות, בין ציר אַיינְשְׁטֵיין לפארק המסלול.',
 'בין היום לעתיד — מכונת הזמן למעלה מחליפה בין אלפיים עשרים ושש לאלפיים שלושים וחמש. לחצו על כל בניין, בחרו דירה, וצאו לסיור חופשי ברחובות... ברוכים הבאים לשדה דב.',
]

EN = [
 'Here, on the Tel Aviv shoreline, Dov Hoz Airport operated until twenty nineteen. Today the city’s newest quarter rises in its place... about sixteen thousand homes between the sea and Ibn Gvirol.',
 'The first towers are already under construction. Dimri Yama — thirty-nine floors on the first line to the sea... four hundred and fifty-eight homes in the southern Eshkol compound.',
 'The airport’s historic runway remains... reborn as Runway Park. A green spine crossing the quarter, carrying its public buildings, and a free path to the sea.',
 'Rainbow Tel Aviv by Israel Canada — a flagship tower and six courtyard buildings... about four hundred and eighty homes, right by the park and the gate plaza.',
 'Ashira by Avisror — four buildings at the quarter’s southern entrance... about four hundred and six homes, between the Einstein corridor and Runway Park.',
 'Between today and tomorrow — the time machine up top switches twenty twenty-six and twenty thirty-five. Tap any building, pick an apartment, and take a free walk through the streets... Welcome to Sde Dov.',
]

async def gen(text, voice, rate, path):
    tts = edge_tts.Communicate(text, voice, rate=rate)
    await tts.save(path)
    print(os.path.basename(path), os.path.getsize(path), 'bytes')

async def main():
    for i, t in enumerate(HE):
        await gen(t, HE_VOICE, '-8%', os.path.join(OUT, 'narr-sdedov-he-%d.mp3' % i))
    for i, t in enumerate(EN):
        await gen(t, EN_VOICE, '-6%', os.path.join(OUT, 'narr-sdedov-en-%d.mp3' % i))

asyncio.run(main())
print('DONE 12 clips')
