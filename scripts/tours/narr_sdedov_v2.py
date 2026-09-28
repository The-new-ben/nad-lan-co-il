# -*- coding: utf-8 -*-
"""The Sde Dov tour's corrected narration clips (1.72.311, design system SdeDovTour v57).

Clip 3 said "כ־480 דירות" for Rainbow (the developer's number is 459; 480 was the 2023 design plan), and clip 5 said
"בחרו דירה" (the tour has no apartment picking). Same recipe as the originals (docs/receipts/RECEIPT-TOURS-V5-2026-08-21.md):
edge-tts he-IL-AvriNeural -8% / en-US-ChristopherNeural -6%, numbers spoken as gender-correct words, vowel marks only on
the risky names, no SSML.

    python scripts/tours/narr_sdedov_v2.py        -> plugins/nadlan-config/assets/tours/narr-sdedov-{he,en}-{3,5}-v2.mp3
"""
import asyncio, os
import edge_tts

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "plugins", "nadlan-config", "assets", "tours")
CLIPS = {
    ("he", 3): "רֵיינְבּוֹ תל אביב של ישראל קנדה. מגדל דגל ושישה בנייני חצר, ארבע מאות חמישים ותשע דירות לפי היזם, במגרש הצמוד לפארק ולכיכר השער.",
    ("he", 5): "בין היום לעתיד... מכונת הזמן למעלה מחליפה בין אלפיים עשרים ושש לאלפיים שלושים וחמש. לחצו על כל בניין כדי להכיר אותו, וצאו לסיור חופשי ברחובות. ברוכים הבאים לשְׂדֵה דּוֹב.",
    ("en", 3): "Rainbow Tel Aviv by Israel Canada. A flagship tower and six courtyard buildings, four hundred fifty-nine homes by the developer's count, right by the park and the gate plaza.",
    ("en", 5): "Between today and tomorrow... the time machine up top switches between twenty twenty-six and twenty thirty-five. Tap any building to meet it, and take a free walk through the streets. Welcome to Sde Dov.",
}
VOICE = {"he": ("he-IL-AvriNeural", "-8%"), "en": ("en-US-ChristopherNeural", "-6%")}


async def main():
    os.makedirs(OUT, exist_ok=True)
    for (lang, i), text in CLIPS.items():
        voice, rate = VOICE[lang]
        path = os.path.join(OUT, "narr-sdedov-%s-%d-v2.mp3" % (lang, i))
        await edge_tts.Communicate(text, voice, rate=rate).save(path)
        print(path, os.path.getsize(path))

asyncio.run(main())
