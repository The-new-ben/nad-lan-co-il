# /projects/ and the AI engines: question library (HAD-689 item 9, 10.11.2026)

Purpose: see which pages Google's AI box, ChatGPT and Perplexity cite for the "פרויקטים חדשים" family, and which passage they quote,
so the weakest passages on https://nad-lan.co.il/projects/ can be rewritten against what is actually cited. Built from the head phrase
and the families in `../israel/needs-matrix-2026-11-10.md` and `../israel/related-deep-2026-11-10.md`.

## How to run (for the research session)
- Browser: the owner's Chrome only ("gmktec", Claude in Chrome deviceId `3faca133-7015-4514-8329-3c39506b4ecd`). Never another browser.
- Google: google.co.il, Hebrew interface, signed in as the owner is. Record whether an AI box ("סקירה כללית מבוססת AI") appears; if not, write "absent". Never invent one.
- ChatGPT: chatgpt.com in the same Chrome, a NEW chat per question, search on (the globe). Perplexity: perplexity.ai, default mode.
- Pace: one question at a time, 20 to 40 seconds apart. No captchas: if one appears, stop that engine and note it.
- Never log in, never change any setting, never post or share anything.
- For each question and engine record: date and time; whether an answer appeared; the cited URLs in order; for every nad-lan.co.il citation, the exact
  quoted or paraphrased passage and the page section it came from; the first three cited competitors and the passage each was cited for.
- Output: `results-2026-11-XX.json` (one object per question per engine) and `summary-2026-11-XX.md` in this folder: a table of questions ×
  engines with "nad-lan cited: yes / no / which page", and the ten passages most cited across all engines with their sources.
- Report back in 5 lines: how many answers cited nad-lan, on which questions, and the three biggest gaps.

## The questions (Hebrew, as a person types or asks)

### Head and synonyms
1. פרויקטים חדשים
2. פרויקטים חדשים בישראל 2026
3. איפה רואים את כל הפרויקטים החדשים בארץ?
4. דירות חדשות מקבלן למכירה
5. דירות חדשות למכירה
6. אילו פרויקטים חדשים יש עכשיו בשיווק?
7. פרויקטים חדשים בתל אביב
8. פרויקטים חדשים בתל אביב מחירים
9. פרויקטים חדשים במרכז הארץ
10. פרויקטים חדשים במרכז תל אביב

### Budget ladder (Google's spelling)
11. דירות חדשות עד מיליון שקל
12. דירות חדשות עד 1.2 מיליון
13. דירות חדשות עד 1.5 מיליון
14. דירות חדשות עד 2 מיליון
15. דירות חדשות עד 2.5 מיליון
16. דירות חדשות עד 3 מיליון
17. מה אפשר לקנות היום ב־1.5 מיליון שקל דירה חדשה?
18. איפה עוד יש דירה חדשה מקבלן מתחת ל־2 מיליון במרכז?

### Stage
19. פרויקטים חדשים על הנייר
20. דירה על הנייר או דירה גמורה, מה עדיף?
21. פריסייל תל אביב
22. פרויקטים פריסייל 2026
23. פרויקטים חדשים בשיווק
24. פרויקטים בבנייה
25. דירות חדשות לאכלוס מיידי
26. דירות חדשות לאכלוס מיידי בתל אביב

### Neighbourhoods and places
27. פרויקטים חדשים ברמת אביב
28. פרויקטים חדשים בצפון תל אביב
29. פרויקטים חדשים ליד הים בתל אביב
30. פרויקטים חדשים בשדה דב
31. פרויקטים חדשים ברמת גן
32. פרויקטים חדשים בהרצליה

### Developers, prices, deals
33. איזה חברות בונות פרויקטים חדשים בתל אביב?
34. מי היזמים הגדולים בישראל היום?
35. מחיר דירת 4 חדרים חדשה בתל אביב
36. מחיר דירת 3 חדרים בתל אביב עם ממ"ד
37. פרויקטים חדשים 20 80
38. מבצעי קבלנים 2026
39. מה זה הלוואת קבלן?
40. האם כדאי לקנות דירה מקבלן עם הצמדה למדד תשומות הבנייה?

### Conversational (AI-engine style)
41. אני מחפש דירה חדשה ב־4 חדרים בתל אביב עד 4 מיליון, מה יש?
42. מה כדאי לבדוק לפני שחותמים על דירה מקבלן?
43. כמה זמן לוקח לבנות פרויקט חדש מהיתר עד מפתח?
44. איך משווים בין שני פרויקטים חדשים?
45. יש אתר שמרכז את כל הפרויקטים החדשים עם מחירים?

## After the run (main session)
- For each question where a competitor is cited and nad-lan is not: open the cited passage, compare with ours on /projects/, rewrite ours
  so it states the same need with our own data (number, date, place), shorter and more direct. Never copy their wording.
- Nothing is claimed as a result unless it was seen in the engine's answer.
