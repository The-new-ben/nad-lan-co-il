# Fingerprint ל־HTML הציבורי

## למה View Source הוא מקור נפרד

ה־DOM אחרי JavaScript אינו התגובה שקיבל crawler. לכן נשמרים שני fingerprints:

- **raw source:** גוף תגובת HTTP המדויקת;
- **rendered DOM:** מבנה הדף לאחר runtime.

שניהם חשובים, אבל title, canonical, favicon, hreflang, JSON-LD ובעלות על schema מתחילים ב־raw source.

## מה נשמר

- URL סופי, HTTP status, timestamp וגודל bytes;
- SHA-256 מלא;
- SHA נפרד ל־`<head>` ול־navigation כאשר ניתן;
- title/description/canonical/hreflang;
- מספר H1 וסדר headings;
- כל הצהרות favicon כולל owner, rel, href ו־sizes;
- כל JSON-LD לפי `@type` ובעלים;
- scripts, styles, preload/modulepreload;
- duplicate IDs;
- טקסטי המתנה, שמות פרויקט זר, notices לפני H1, קישורים 404 וקוד כפול.

## baseline Rainbow

- snapshot: `evidence/rainbow-public-source-2026-08-24.html`
- original captured SHA-256: `F40C4188C0A6AD9E4A9250022CBE0D79372C49E7A22D087B4C99FBC3152F7B9B`
- public-repository redacted copy SHA-256: `BE1F08AE1EB7B2F9025381DF9853B926052F883390B2365C30E77F2FE05691EA`
- canonical: 1; H1: 1; favicon declarations: 4; hreflang: 10; JSON-LD: 5; scripts: 58; styles: 34; duplicate IDs: 0.

ממצאים צפים שנשמרו ולא הוסתרו:

- כתום: ארבע הצהרות favicon משני owners—קשור ישירות להערת ה־favicon ב־SERP;
- כתום: notice לפני H1;
- צהוב: schema מופק בידי יותר מבעלים אחד;
- צהוב: 58 scripts ו־34 styles דורשים performance ownership;
- כתום: URL ישן של H-Infinity החזיר 404.

## התהליך ב־WordPress

1. editor לוחץ “צילום View Source ציבורי עכשיו”.
2. nonce ויכולת עריכה נבדקים.
3. `wp_remote_get` קורא את permalink הציבורי.
4. גוף התגובה נשמר immutable תחת `uploads/nadlan-source-snapshots/{post}/{timestamp-hash}.html`.
5. metadata נשמר ב־`_nadlan_source_snapshot_latest`.
6. הצ׳ק־ליסט מציג hash, זמן, file path וממצאים.
7. snapshot חדש מושווה לקודם; שינוי ב־menu/favicon/schema/scripts צף גם אם רכיב הפרויקט לא השתנה.

## כלל עדכון

לא מעדכנים baseline כדי “להחזיר ירוק”. קודם קוראים diff, מסווגים שינוי מכוון/לא מכוון, מריצים source detectors ודפדפן, ורק אז חותמים hash חדש עם בעלים ותאריך.
