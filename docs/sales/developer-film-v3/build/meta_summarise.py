# meta_summarise.py - summarise the developer's own cards from meta_<slug>.json (captured Ad Library text). Read-only.
import json, re, sys
from collections import Counter
OWN = {"avisror": r"אביסרור|Avisror", "israel-canada": r"ישראל קנדה|Israel Canada|ICR", "dimri": r"דמרי - בנייה|י\.ח\.דמרי",
       "gindi": r"Gindi Holding|גינדי החזקות", "azorim": r"אזורים - Azorim"}
KW = ["3D", "תלת", "סיור", "360", "וירטואל", "הדמי", "פריסייל", "presale", "מחיר", "הרשמה", "מבצע", "דירות", "פנטהאוז", "בחירת דירה", "קומה"]
for slug, pat in OWN.items():
    d = json.load(open(f"../campaign-check/meta_{slug}.json", encoding="utf-8"))
    t = d.get("full_text", "")
    cards = re.split(r"\n(?=פעילה\n)", t)
    own = [c for c in cards if re.search(r"\n(" + pat + r")[^\n]*\n(?:ממומן|Sponsored)", c)]
    kw = {k: sum(1 for c in own if re.search(k, c, re.I)) for k in KW}
    # caption lines just before the CTA button
    caps = Counter()
    for c in own:
        m = re.search(r"\n([^\n]{3,80})\n(?:[^\n]{0,80}\n)?(Learn More|Sign Up|Send WhatsApp Message|Get Offer|Apply Now|Shop Now)\b", c)
        if m: caps[m.group(1)] += 1
    print(f"== {slug}: results line {d.get('results_line')}, cards loaded {d.get('library_id_count_loaded')}, own-advertiser cards parsed {len(own)}")
    print("   keyword hits (cards):", {k: v for k, v in kw.items() if v})
    print("   captions:", caps.most_common(8))
    if own:
        print("   sample:", re.sub(r"\s+", " ", own[0])[:260])
