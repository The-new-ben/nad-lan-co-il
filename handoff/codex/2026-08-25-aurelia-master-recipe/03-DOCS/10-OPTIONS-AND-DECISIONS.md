# אפשרויות והחלטות

לכל יכולת יש נתיב ייצור מומלץ ו־fallback ששומר על אותו מסע משתמש. המקור המפורט הוא `data/implementation-options.json`.

| יכולת | מומלץ | fallback תקין | אסור |
|---|---|---|---|
| מודל | GLB במנוע הקיים, מצלמה ו־hotspots לפרויקט | פוסטר תואם + שכבת hotspots באותם IDs | במה שחורה או מודל דקורטיבי |
| מלאי | collection אחת ב־NADLAN_SHOWROOM | cards מרונדרים מה־JSON הזהה | datasets נפרדים |
| תוכנית | panel בתוך ה־stage עם plan_id | dialog נגיש ששומר יחידה | תמונה לא קשורה |
| נוף | Mapbox + beam לפי azimuth וגובה | מפה georeferenced + beam | נוף גנרי |
| פנים | panorama עם hotspots | גלריה אינטראקטיבית ששומרת unit_id | PNG שמוצג כסיור |
| מתקנים | hotspots + detail | cards מאותו collection | icons לא לחיצים |
| סטודיו | studio.js + BOM | wizard עם אותו payload | בחירה ללא קוד/כמות |
| פנייה | endpoints הקיימים + context | handler WordPress עם אותו schema | טופס כללי |
| source | fetch ציבורי + snapshot/diff | View Source שמור ידנית | בדיקת editor DOM |

החלטות שסוכמו במתכון:

- נורות אינן חוסמות פרסום.
- מחיר ציבורי מופיע בביטחון לפי יחידה; מקור ורמת ביטחון נשארים פנימיים.
- אין טקסטי ״מחכים לחומרים״ ואין `0 חדרים`.
- הדמו ו־WordPress נשארים מוצרים נפרדים אבל חולקים חוזה.
- לא מאחדים את כל הפרויקטים לפני שפרויקט האב נבדק ואושר.
