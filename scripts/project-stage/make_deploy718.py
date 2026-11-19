# -*- coding: utf-8 -*-
"""make deploy718.py from deploy717.py: 1.72.718 = HAD-795 package 6, legal wording only (coordinator order 20.11.2026, after the
legal-sentence audit docs/rentals/bom/legal-claims-audit.md). Four sentences that real users see today said more than the law's text:
  HUNK inc/rentals-manager.php (v1 strings, he + en; printed in the visitors' live demo and in every landlord's app):
    1. the security cap is shown with its scope (s.25טו: not on rent above 20,000 a month, a lease of up to 3 months with no option,
       and other leases the section lists);
    2. the cap counts securities that cost the tenant money (s.25י(ב): bank guarantee, a guarantee from an insurer or licensed credit
       provider, cash), so the amount field and the cap label no longer read as if every cheque and note counts;
    3. the 90 / 60 day notices belong to an option to extend (s.25יב(ב),(ג)); without an option, a reasonable time (s.25יב(א));
    4. the 30-day repair line: a defect that is not minor, 30 days from the tenant's demand (s.25ח(ב)).
  SWAP assets/rentals/guide/he.html, en.html (public guide, chapter 6): the same 30-day sentence.
No layout, no new feature, nothing removed. The LAW numbers (3/30/90/60) and the JS are unchanged."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 717
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']

R = "inc/rentals-manager.php"
HUNKS = {R: [
    # English
    ("'sec_amount' => 'Deposit / guarantee amount (ILS)', 'sec_cap' => 'Legal cap for costly securities', 'sec_cap_f' => 'the lower of 3 months rent or one third of the total term rent',",
     "'sec_amount' => 'Cash deposit or bank guarantee amount (ILS)', 'sec_cap' => 'Legal cap on securities that cost the tenant money (bank guarantee, a guarantee from an insurer or licensed credit provider, cash)', 'sec_cap_f' => 'the lower of 3 months rent or the rent for one third of the lease term; the cap does not apply, among others, to rent above ILS 20,000 a month (updated each 1 January), to a lease of up to 3 months with no option, and to the other leases listed in s.25טו of the law',"),
    ("'sec_over' => 'Above the legal cap - check with a lawyer',",
     "'sec_over' => 'Above the legal cap, if the cap applies to this lease. Check with a lawyer',"),
    ("'notice_l' => 'Landlord notice window: {d} days before end', 'notice_t' => 'Tenant notice: {d} days',",
     "'notice_l' => 'If the landlord has an option to extend: notice no later than {d} days before the end. Without an option: a reasonable time before the end, whether you want to extend and on what terms', 'notice_t' => 'If the tenant has an option to extend: notice no later than {d} days before the end',"),
    ("'act_repair_std' => '{label}: open repair approaching 30-day limit'",
     "'act_repair_std' => '{label}: open repair nearing 30 days since it was logged (by law: 30 days from the tenant demand, for a defect that is not minor)'"),
    ("'act_sec' => '{label}: deposit above the legal cap'",
     "'act_sec' => '{label}: deposit above the legal cap (if the cap applies to this lease)'"),
    # Hebrew
    ("'sec_amount' => 'סכום הפיקדון / הערבות (₪)', 'sec_cap' => 'התקרה החוקית לבטוחות בעלות עלות', 'sec_cap_f' => 'הנמוך מבין 3 חודשי שכירות או שליש משכר הדירה לכל התקופה',",
     "'sec_amount' => 'סכום הפיקדון במזומן או הערבות הבנקאית (₪)', 'sec_cap' => 'התקרה בחוק לערובות שכרוכות בהוצאה כספית לשוכר (ערבות בנקאית, ערבות של חברת ביטוח או גוף אשראי מורשה, מזומן)', 'sec_cap_f' => 'הנמוך מבין שכר דירה של 3 חודשים או שכר הדירה לשליש מתקופת השכירות. התקרה לא חלה בין השאר על שכר דירה מעל 20,000 ₪ לחודש (הסכום מתעדכן ב-1 בינואר), על חוזה עד 3 חודשים בלי אופציה, ועל שאר החוזים שמנויים בסעיף 25טו לחוק',"),
    ("'sec_over' => 'מעל התקרה החוקית - בדקו עם עורך דין',",
     "'sec_over' => 'מעל התקרה בחוק, אם התקרה חלה על החוזה הזה. בדקו עם עורך דין',"),
    ("'notice_l' => 'חלון הודעת משכיר: {d} ימים לפני הסיום', 'notice_t' => 'הודעת שוכר: {d} ימים',",
     "'notice_l' => 'אם יש למשכיר אופציה להאריך: הודעה לא יאוחר מ-{d} ימים לפני הסיום. בלי אופציה: הודעה זמן סביר לפני הסיום, אם רוצים להאריך ובאילו תנאים', 'notice_t' => 'אם יש לשוכר אופציה להאריך: הודעה לא יאוחר מ-{d} ימים לפני הסיום',"),
    ("'act_repair_std' => '{label}: תקלה פתוחה מתקרבת למועד 30 הימים'",
     "'act_repair_std' => '{label}: תקלה פתוחה קרובה ל-30 יום מהרישום (בחוק: 30 יום מדרישת השוכר, לליקוי שאינו קל ערך)'"),
    ("'act_sec' => '{label}: פיקדון מעל התקרה החוקית'",
     "'act_sec' => '{label}: פיקדון מעל התקרה בחוק (אם התקרה חלה על החוזה)'"),
]}
LIVE_MD5 = {R: "936cef107b1a1b0aa2fbed2bf9186107"}

HE_NEW = ["התקרה בחוק לערובות שכרוכות בהוצאה כספית לשוכר", "אם יש למשכיר אופציה להאריך", "לליקוי שאינו קל ערך",
          "וליקוי אחר שאינו קל ערך לא יאוחר מ-<strong>30 יום</strong>", "נספר מיום שהשוכר דיווח עליה"]
HE_OLD = ["התקרה החוקית לבטוחות בעלות עלות", "חלון הודעת משכיר", "מתקרבת למועד 30 הימים", "ותקלה אחרת לא יאוחר מ-"]
EN_NEW = ["Legal cap on securities that cost the tenant money", "If the landlord has an option to extend", "for a defect that is not minor",
          "any other defect that is not minor no later than <strong>30 days</strong>", "counted from the day the tenant reported it"]
EN_OLD = ["Legal cap for costly securities", "Landlord notice window", "approaching 30-day limit", "any other no later than"]
ROWS = ("    ('/my-rentals/?t718a=1', %r, %r, []),\n"
        "    ('/my-rentals/?lang=en&t718a=1', %r, %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t718a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t718a=1', [], %r, []),\n") % (HE_NEW, E + HE_OLD, EN_NEW, E + EN_OLD, E, E)
kl_release.build_release(PREV, 718, ["assets/rentals/guide/he.html", "assets/rentals/guide/en.html"], [], HUNKS, LIVE_MD5, ROWS,
                         "rentals legal wording: security cap scope, which securities it counts, option notices, the 30-day repair line",
                         "HAD-795 package 6: rentals legal wording")
